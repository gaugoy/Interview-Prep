# 🔌 03 — Django REST Framework (DRF)
### [← Back to Index](./README.md)

---

## Table of Contents
1. [What is DRF? Core Components](#q1)
2. [Serializers and ModelSerializer](#q2)
3. [Nested Serializers and Writable Relations](#q3)
4. [Custom Serializer Validation](#q4)
5. [APIView vs GenericAPIView vs ViewSet](#q5)
6. [Routers and URL Configuration](#q6)
7. [Authentication Methods](#q7)
8. [JWT Authentication](#q8)
9. [Permissions and Custom Permission Classes](#q9)
10. [Throttling and Rate Limiting](#q10)
11. [Pagination Styles](#q11)
12. [Filtering, Searching, and Ordering](#q12)
13. [API Versioning](#q13)
14. [Renderers and Parsers](#q14)
15. [Testing REST APIs](#q15)
16. [Building a Complete CRUD API](#q16)
17. [Exception Handling](#q17)
18. [DRF Settings and Configuration](#q18)

---

<a name="q1"></a>
## Q1. ⭐⭐ What is DRF? Core Components

**Answer:**
Django REST Framework (DRF) is a powerful toolkit for building **Web APIs** on top of Django.

**Core components:**

| Component | Purpose |
|-----------|---------|
| **Serializer** | Convert model instances ↔ JSON/dict |
| **View / ViewSet** | Handle HTTP requests |
| **Router** | Auto-generate URL patterns |
| **Authentication** | Identify who is making the request |
| **Permission** | Determine if request is allowed |
| **Throttle** | Rate limiting |
| **Pagination** | Split large result sets |
| **Filter** | Filter/search/order querysets |
| **Renderer** | Format response (JSON, HTML, etc.) |
| **Parser** | Parse request body (JSON, form, etc.) |

```python
# Installation
# pip install djangorestframework

# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ Serializers and ModelSerializer

**Answer:**
Serializers convert complex data types (model instances, querysets) to **native Python datatypes** that can be rendered to JSON, and vice versa.

```python
from rest_framework import serializers
from .models import Article, Tag, User


# Basic Serializer — manual field definition
class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    status = serializers.ChoiceField(choices=['draft', 'published'])
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


# ModelSerializer — auto-generates fields from model
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'status', 'author', 'created_at']
        # Or: fields = '__all__'
        read_only_fields = ['id', 'created_at', 'author']
        extra_kwargs = {
            'content': {'write_only': True},  # Don't include in response
            'title': {'min_length': 5},
        }

    # Add computed/extra fields
    author_name = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return obj.author.get_full_name() if obj.author else None

    def get_word_count(self, obj):
        return len(obj.content.split())

    # Override create to set author from request
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


# Usage
# Serializing (model → JSON)
article = Article.objects.get(pk=1)
serializer = ArticleSerializer(article)
data = serializer.data  # OrderedDict

# Serializing many objects
articles = Article.objects.all()
serializer = ArticleSerializer(articles, many=True)
data = serializer.data  # List of OrderedDicts

# Deserializing (JSON → model)
data = {'title': 'Hello', 'content': 'World', 'status': 'draft'}
serializer = ArticleSerializer(data=data)
if serializer.is_valid():
    article = serializer.save()  # Calls create()
else:
    print(serializer.errors)

# Partial update (PATCH)
serializer = ArticleSerializer(article, data={'title': 'New Title'}, partial=True)
if serializer.is_valid():
    serializer.save()  # Calls update()
```

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ Nested Serializers and Writable Relations

**Answer:**

```python
from rest_framework import serializers
from .models import Article, Tag, Comment, User


# Read-only nested serializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):
    # Nested read-only
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # Write using IDs
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'author_id', 'tags', 'tag_ids']


# Writable nested serializer — create/update related objects
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']


class ArticleWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'comments']

    def create(self, validated_data):
        comments_data = validated_data.pop('comments', [])
        article = Article.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(article=article, **comment_data)
        return article

    def update(self, instance, validated_data):
        comments_data = validated_data.pop('comments', None)
        instance = super().update(instance, validated_data)

        if comments_data is not None:
            # Replace all comments
            instance.comments.all().delete()
            for comment_data in comments_data:
                Comment.objects.create(article=instance, **comment_data)

        return instance


# StringRelatedField — uses __str__
class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)  # Uses Tag.__str__()
    author = serializers.StringRelatedField()          # Uses User.__str__()

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'tags']
```

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ Custom Serializer Validation

**Answer:**

```python
from rest_framework import serializers
from django.utils import timezone


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'status', 'publish_date', 'category']

    # Field-level validation: validate_<fieldname>
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")

        # Check uniqueness (excluding current instance on update)
        qs = Article.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("An article with this title already exists.")

        return value.strip()

    def validate_publish_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Publish date cannot be in the past.")
        return value

    # Cross-field validation: validate()
    def validate(self, attrs):
        status = attrs.get('status')
        publish_date = attrs.get('publish_date')

        if status == 'published' and not publish_date:
            raise serializers.ValidationError({
                'publish_date': 'Publish date is required when status is published.'
            })

        if status == 'draft' and publish_date:
            attrs['publish_date'] = None  # Clear publish date for drafts

        return attrs


# Custom validators (reusable)
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Article.objects.all(),
                message="This title is already taken.",
                lookup='iexact',
            )
        ]
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'author']
        validators = [
            UniqueTogetherValidator(
                queryset=Article.objects.all(),
                fields=['title', 'author'],
                message="You already have an article with this title.",
            )
        ]


# Custom validator function
def validate_no_profanity(value):
    banned_words = ['spam', 'scam']
    for word in banned_words:
        if word in value.lower():
            raise serializers.ValidationError(f"Content contains banned word: {word}")
    return value

class ArticleSerializer(serializers.ModelSerializer):
    content = serializers.CharField(validators=[validate_no_profanity])
```

---

<a name="q5"></a>
## Q5. ⭐⭐⭐ APIView vs GenericAPIView vs ViewSet

**Answer:**

| Class | Level | Use Case |
|-------|-------|---------|
| `APIView` | Low | Full control, custom logic |
| `GenericAPIView` + Mixins | Medium | Standard CRUD with customization |
| `ModelViewSet` | High | Full CRUD with minimal code |
| `ReadOnlyModelViewSet` | High | List + Retrieve only |

```python
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    ListAPIView, CreateAPIView, RetrieveAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, action


# 1. APIView — full control
class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.filter(status='published')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get_object(self, pk):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 2. GenericAPIView — less boilerplate
class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.select_related('author').all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_destroy(self, instance):
        # Soft delete instead of hard delete
        instance.is_deleted = True
        instance.save()


# 3. ModelViewSet — full CRUD in one class
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.select_related('author', 'category').all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(status='published')
        return qs

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ArticleDetailSerializer
        return ArticleCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Custom action — adds extra endpoint
    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        article = self.get_object()
        article.publish()
        return Response({'status': 'published'})

    @action(detail=False, methods=['get'], url_path='my-articles')
    def my_articles(self, request):
        articles = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


# Function-based view with @api_view decorator
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

---

<a name="q6"></a>
## Q6. ⭐⭐ Routers and URL Configuration

**Answer:**

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

# DefaultRouter — includes API root view
router = DefaultRouter()
router.register('articles', views.ArticleViewSet, basename='article')
router.register('users', views.UserViewSet, basename='user')
router.register('tags', views.TagViewSet, basename='tag')

# Generated URLs:
# GET    /articles/          → list
# POST   /articles/          → create
# GET    /articles/{pk}/     → retrieve
# PUT    /articles/{pk}/     → update
# PATCH  /articles/{pk}/     → partial_update
# DELETE /articles/{pk}/     → destroy
# POST   /articles/{pk}/publish/    → custom action (detail=True)
# GET    /articles/my-articles/     → custom action (detail=False)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    # Manual URLs for APIView
    path('api/v1/search/', views.SearchView.as_view(), name='search'),
]

# Nested routers (drf-nested-routers)
# pip install drf-nested-routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('articles', views.ArticleViewSet, basename='article')

articles_router = routers.NestedDefaultRouter(router, 'articles', lookup='article')
articles_router.register('comments', views.CommentViewSet, basename='article-comments')

# Generated URLs:
# GET /articles/{article_pk}/comments/
# POST /articles/{article_pk}/comments/
# GET /articles/{article_pk}/comments/{pk}/
```

---

<a name="q7"></a>
## Q7. ⭐⭐⭐ Authentication Methods

**Answer:**

| Method | How it works | Use case |
|--------|-------------|---------|
| **Session** | Cookie-based, Django sessions | Browser clients |
| **Token** | Static token in header | Simple APIs, mobile |
| **JWT** | Signed token, stateless | SPAs, microservices |
| **Basic** | Base64 username:password | Development only |
| **OAuth2** | Third-party auth | Social login |

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Token Authentication
# pip install djangorestframework
# INSTALLED_APPS += ['rest_framework.authtoken']
# python manage.py migrate

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })

# Client usage:
# Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# Per-view authentication override
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class MyView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
```

---

<a name="q8"></a>
## Q8. ⭐⭐⭐ JWT Authentication

**Answer:**
JWT (JSON Web Token) is a **stateless, self-contained token** — no server-side session storage needed.

```python
# pip install djangorestframework-simplejwt

# settings.py
from datetime import timedelta

INSTALLED_APPS += ['rest_framework_simplejwt']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,       # Issue new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,    # Blacklist old refresh tokens
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

# Custom token with extra claims
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['is_staff'] = user.is_staff
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Client usage:
# POST /api/token/ → {"access": "...", "refresh": "..."}
# Authorization: Bearer <access_token>
# POST /api/token/refresh/ → {"refresh": "..."} → {"access": "..."}
```

---

<a name="q9"></a>
## Q9. ⭐⭐⭐ Permissions and Custom Permission Classes

**Answer:**

```python
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser, AllowAny,
    IsAuthenticatedOrReadOnly, DjangoModelPermissions,
    BasePermission, SAFE_METHODS
)

# Built-in permissions
class ArticleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]           # Must be logged in
    # permission_classes = [IsAdminUser]             # Must be admin
    # permission_classes = [AllowAny]                # No restriction
    # permission_classes = [IsAuthenticatedOrReadOnly]  # Read: anyone, Write: auth


# Custom permission classes
class IsOwnerOrReadOnly(BasePermission):
    """Allow read to anyone, write only to object owner."""

    def has_permission(self, request, view):
        # Allow all GET, HEAD, OPTIONS requests
        if request.method in SAFE_METHODS:
            return True
        # Write requires authentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in SAFE_METHODS:
            return True
        # Write permissions only to owner
        return obj.author == request.user


class IsVerifiedUser(BasePermission):
    """Only verified users can access."""
    message = 'Your account must be verified to perform this action.'

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_verified
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# Combining permissions (AND logic)
class ArticleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

# OR logic — use list with |
from rest_framework.permissions import OperandHolder

# Per-action permissions
class ArticleViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create']:
            return [IsAuthenticated(), IsVerifiedUser()]
        else:  # update, partial_update, destroy
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
```

---

<a name="q10"></a>
## Q10. ⭐⭐ Throttling and Rate Limiting

**Answer:**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'login': '5/minute',
        'burst': '60/minute',
        'sustained': '1000/day',
    },
}

# Built-in throttle classes
# AnonRateThrottle — limits unauthenticated requests by IP
# UserRateThrottle — limits authenticated requests by user
# ScopedRateThrottle — different rates for different views

# Custom throttle
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'  # Uses 'login' rate from DEFAULT_THROTTLE_RATES

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


# Per-view throttling
class LoginView(APIView):
    throttle_classes = [LoginRateThrottle]
    permission_classes = [AllowAny]

    def post(self, request):
        # Login logic
        pass


class ArticleViewSet(ModelViewSet):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]


# Custom throttle with Redis
from rest_framework.throttling import SimpleRateThrottle

class IPRateThrottle(SimpleRateThrottle):
    scope = 'ip'

    def get_cache_key(self, request, view):
        ident = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }
```

---

<a name="q11"></a>
## Q11. ⭐⭐ Pagination Styles

**Answer:**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# 1. PageNumberPagination — ?page=2&page_size=10
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100
    page_query_param = 'page'

# Response:
# {
#   "count": 150,
#   "next": "http://api.example.com/articles/?page=3",
#   "previous": "http://api.example.com/articles/?page=1",
#   "results": [...]
# }


# 2. LimitOffsetPagination — ?limit=10&offset=20
from rest_framework.pagination import LimitOffsetPagination

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


# 3. CursorPagination — cursor-based (for real-time feeds)
from rest_framework.pagination import CursorPagination

class ArticleCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'  # Must be unique, stable ordering
    cursor_query_param = 'cursor'

# Response:
# {
#   "next": "http://api.example.com/articles/?cursor=cD0yMDIz...",
#   "previous": null,
#   "results": [...]
# }


# Apply pagination to ViewSet
class ArticleViewSet(ModelViewSet):
    pagination_class = StandardPagination

    # Or disable pagination for specific action
    @action(detail=False, methods=['get'])
    def all_articles(self, request):
        self.pagination_class = None
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


# Custom pagination response format
class CustomPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'page': self.page.number,
                'pages': self.page.paginator.num_pages,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'data': data,
        })
```

---

<a name="q12"></a>
## Q12. ⭐⭐ Filtering, Searching, and Ordering

**Answer:**

```python
# pip install django-filter

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

import django_filters
from rest_framework import filters


# 1. DjangoFilterBackend — exact field filtering
class ArticleFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')
    author = django_filters.NumberFilter(field_name='author__id')
    published_after = django_filters.DateFilter(
        field_name='published_at', lookup_expr='gte'
    )
    published_before = django_filters.DateFilter(
        field_name='published_at', lookup_expr='lte'
    )
    min_views = django_filters.NumberFilter(field_name='views', lookup_expr='gte')
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')

    class Meta:
        model = Article
        fields = ['status', 'author', 'category']


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_class = ArticleFilter

    # 2. SearchFilter — ?search=django
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        'title',           # Exact match
        '^title',          # Starts with
        '=title',          # Exact
        '@content',        # Full-text search (PostgreSQL)
        'author__email',   # Related field
    ]

    # 3. OrderingFilter — ?ordering=-published_at,title
    ordering_fields = ['title', 'published_at', 'views', 'created_at']
    ordering = ['-published_at']  # Default ordering

# Usage:
# GET /articles/?status=published
# GET /articles/?search=django
# GET /articles/?ordering=-views
# GET /articles/?published_after=2024-01-01&min_views=100
# GET /articles/?status=published&search=django&ordering=-views&page=2
```

---

<a name="q13"></a>
## Q13. ⭐ API Versioning

**Answer:**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
}

# 1. URL Path Versioning — /api/v1/articles/
# urls.py
urlpatterns = [
    path('api/<str:version>/', include('api.urls')),
]

# 2. Query Parameter Versioning — /api/articles/?version=v2
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
}

# 3. Header Versioning — Accept: application/json; version=v2
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
}

# Using version in views
class ArticleViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ArticleSerializerV2
        return ArticleSerializer

    def list(self, request, *args, **kwargs):
        if request.version == 'v2':
            # v2 response format
            pass
        return super().list(request, *args, **kwargs)
```

---

<a name="q14"></a>
## Q14. ⭐ Renderers and Parsers

**Answer:**

```python
# Renderers — format the response
# Parsers — parse the request body

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # HTML browser UI
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',  # File uploads
    ],
}

# Per-view renderer/parser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import MultiPartParser, FormParser

class ArticleViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]  # JSON only, no browser UI

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES['file']
        # Process file
        return Response({'filename': file.name})

# Custom renderer — CSV export
import csv
from io import StringIO
from rest_framework.renderers import BaseRenderer

class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not data:
            return ''
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

class ArticleExportView(ListAPIView):
    queryset = Article.objects.values('id', 'title', 'status', 'views')
    serializer_class = ArticleSerializer
    renderer_classes = [JSONRenderer, CSVRenderer]
    # GET /articles/export/ → JSON
    # GET /articles/export/?format=csv → CSV
    # GET /articles/export/ with Accept: text/csv → CSV
```

---

<a name="q15"></a>
## Q15. ⭐⭐⭐ Testing REST APIs

**Answer:**

```python
# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Article

User = get_user_model()


class ArticleAPITests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(
            email='alice@example.com',
            password='testpass123',
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
        )

        # Create test data
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content',
            status='published',
            author=self.user,
        )

        # Authenticate
        self.client.force_authenticate(user=self.user)

    def test_list_articles(self):
        response = self.client.get('/api/v1/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_article(self):
        data = {
            'title': 'New Article',
            'content': 'New content',
            'status': 'draft',
        }
        response = self.client.post('/api/v1/articles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Article')
        self.assertEqual(Article.objects.count(), 2)

    def test_create_article_unauthenticated(self):
        self.client.force_authenticate(user=None)  # Logout
        data = {'title': 'New Article', 'content': 'Content', 'status': 'draft'}
        response = self.client.post('/api/v1/articles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_article(self):
        response = self.client.get(f'/api/v1/articles/{self.article.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Article')

    def test_update_article_owner(self):
        data = {'title': 'Updated Title', 'content': 'Updated content', 'status': 'published'}
        response = self.client.put(f'/api/v1/articles/{self.article.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')

    def test_update_article_not_owner(self):
        other_user = User.objects.create_user(email='bob@example.com', password='pass')
        self.client.force_authenticate(user=other_user)
        data = {'title': 'Hacked Title'}
        response = self.client.patch(f'/api/v1/articles/{self.article.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_article(self):
        response = self.client.delete(f'/api/v1/articles/{self.article.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)

    def test_filter_by_status(self):
        Article.objects.create(title='Draft', content='...', status='draft', author=self.user)
        response = self.client.get('/api/v1/articles/?status=published')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search(self):
        response = self.client.get('/api/v1/articles/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_jwt_authentication(self):
        # Get token
        response = self.client.post('/api/token/', {
            'email': 'alice@example.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Use token
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_throttling(self):
        # Test rate limiting
        for _ in range(5):
            self.client.post('/api/token/', {'email': 'wrong', 'password': 'wrong'})
        response = self.client.post('/api/token/', {'email': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
```

---

<a name="q16"></a>
## Q16. ⭐⭐⭐ Building a Complete CRUD API

**Answer:**
A complete example tying everything together:

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, default='draft')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='articles')
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# serializers.py
class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    tag_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'status', 'author_name', 'tag_count', 'created_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', many=True, write_only=True, required=False
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'status', 'author', 'tags', 'tag_ids', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title too short.")
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags.set(tags)
        return instance


# views.py
import django_filters
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count


class ArticleFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    author = django_filters.NumberFilter(field_name='author__id')
    published_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Article
        fields = ['status', 'author']


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'content', 'author__email']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return (
            Article.objects
            .select_related('author')
            .prefetch_related('tags')
            .annotate(tag_count=Count('tags'))
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        article = self.get_object()
        if article.author != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        article.status = 'published'
        article.save()
        return Response(ArticleDetailSerializer(article).data)

    @action(detail=False, methods=['get'])
    def my_articles(self, request):
        articles = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


# urls.py
router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='article')
urlpatterns = [path('api/v1/', include(router.urls))]
```

---

<a name="q17"></a>
## Q17. ⭐⭐ Exception Handling

**Answer:**

```python
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException, ValidationError, NotFound,
    PermissionDenied, AuthenticationFailed, NotAuthenticated
)
from rest_framework import status


# Custom exception handler
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'error': {
                'status_code': response.status_code,
                'message': response.data,
            }
        }

    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler',
}


# Custom exceptions
class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable.'
    default_code = 'service_unavailable'


class QuotaExceeded(APIException):
    status_code = 429
    default_detail = 'API quota exceeded.'
    default_code = 'quota_exceeded'


# Using exceptions in views
class ArticleViewSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Article.DoesNotExist:
            raise NotFound('Article not found.')

    def create(self, request, *args, **kwargs):
        if request.user.articles.count() >= 100:
            raise QuotaExceeded('You have reached the maximum number of articles.')
        return super().create(request, *args, **kwargs)
```

---

<a name="q18"></a>
## Q18. ⭐⭐ DRF Settings and Configuration

**Answer:**

```python
# settings.py — comprehensive DRF configuration
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    # Permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },

    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Renderers
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    # Parsers
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],

    # Versioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],

    # Exception handling
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler',

    # Schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.openapi.AutoSchema',

    # Date/time format
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
    'DATE_FORMAT': '%Y-%m-%d',

    # Test
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
```

---

### [← Back to Index](./README.md)

---

## 🏁 Complete! Quick Revision Checklist

### Django Core
- [ ] MVT pattern — Model=data, View=controller, Template=presentation
- [ ] Middleware order: request top→bottom, response bottom→top
- [ ] Signals: `post_save`, `pre_delete`, custom signals, connect in `apps.py`
- [ ] Auth: `AbstractUser`, `AUTH_USER_MODEL`, `@login_required`
- [ ] Security: `DEBUG=False`, HTTPS settings, CSRF, parameterized SQL

### Django ORM
- [ ] `select_related` = JOIN (FK/O2O), `prefetch_related` = separate queries (M2M)
- [ ] N+1 problem: detect with Debug Toolbar, fix with select/prefetch_related
- [ ] `aggregate()` = single dict, `annotate()` = per-row field
- [ ] `Q()` objects for OR/NOT queries
- [ ] `F()` expressions for atomic DB-level updates
- [ ] `transaction.atomic()` for atomicity, `on_commit()` for post-commit tasks

### DRF
- [ ] `ModelSerializer` auto-generates fields, `validate_<field>` for field validation
- [ ] `APIView` = full control, `ModelViewSet` = full CRUD minimal code
- [ ] JWT: access token (short-lived) + refresh token (long-lived)
- [ ] Permissions: `has_permission` (view-level), `has_object_permission` (object-level)
- [ ] `@action(detail=True/False)` for custom endpoints on ViewSets
- [ ] Test with `APITestCase`, `force_authenticate()`, check status codes
