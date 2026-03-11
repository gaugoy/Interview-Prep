# 🏗️ 01 — Django Core Concepts
### [← Back to Index](./README.md)

---

## Table of Contents
1. [Django MVT Architecture](#q1)
2. [Project vs App Structure](#q2)
3. [URL Routing and Path Converters](#q3)
4. [Function-Based vs Class-Based Views](#q4)
5. [Django Middleware](#q5)
6. [Django Signals](#q6)
7. [Django Forms and Validation](#q7)
8. [Django Templates and Template Tags](#q8)
9. [Django Authentication System](#q9)
10. [Permissions and Authorization](#q10)
11. [Session Management](#q11)
12. [Django Caching](#q12)
13. [Static and Media Files](#q13)
14. [Django Admin Customization](#q14)
15. [Custom Management Commands](#q15)
16. [Django Security Best Practices](#q16)
17. [Settings Configuration and Environments](#q17)
18. [Context Processors](#q18)
19. [Generic Class-Based Views (GCBV)](#q19)
20. [Django Request/Response Lifecycle](#q20)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ Explain Django's MVT Architecture

**Answer:**
Django follows the **MVT (Model-View-Template)** pattern — a variation of MVC where Django's "View" acts as the controller.

| MVT Component | Role | MVC Equivalent |
|--------------|------|----------------|
| **Model** | Data layer — defines DB schema, business logic | Model |
| **View** | Logic layer — processes requests, returns responses | Controller |
| **Template** | Presentation layer — HTML with template tags | View |

```
HTTP Request
    ↓
urls.py  →  View (views.py)
                ↓
            Model (models.py) ↔ Database
                ↓
            Template (.html)
                ↓
HTTP Response
```

```python
# models.py — Model layer
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


# views.py — View layer (acts as controller)
from django.shortcuts import render, get_object_or_404
from .models import Article

def article_list(request):
    articles = Article.objects.select_related('author').all()
    return render(request, 'articles/list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/detail.html', {'article': article})


# urls.py — URL routing
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article-list'),
    path('articles/<int:pk>/', views.article_detail, name='article-detail'),
]
```

```html
<!-- templates/articles/list.html — Template layer -->
{% extends 'base.html' %}

{% block content %}
  <h1>Articles</h1>
  {% for article in articles %}
    <article>
      <h2><a href="{% url 'article-detail' article.pk %}">{{ article.title }}</a></h2>
      <p>By {{ article.author.get_full_name }} on {{ article.published_at|date:"M d, Y" }}</p>
    </article>
  {% empty %}
    <p>No articles yet.</p>
  {% endfor %}
{% endblock %}
```

**Follow-up questions:**
- How is MVT different from MVC?
- What happens between a request and a response in Django?

**Interviewer looks for:** Understanding that Django's "View" is the controller, not the presentation layer.

---

<a name="q2"></a>
## Q2. ⭐⭐ Explain Django Project vs App Structure

**Answer:**
- **Project** — the entire Django application (one per deployment)
- **App** — a self-contained module within the project (reusable)

```
myproject/                    ← Project root
├── manage.py
├── myproject/                ← Project package
│   ├── __init__.py
│   ├── settings.py           ← Configuration
│   ├── urls.py               ← Root URL config
│   ├── wsgi.py               ← WSGI entry point
│   └── asgi.py               ← ASGI entry point
├── users/                    ← App: user management
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── serializers.py
│   ├── tests.py
│   ├── migrations/
│   └── templates/users/
├── articles/                 ← App: article management
│   └── ...
└── requirements.txt
```

```python
# myproject/settings.py — register apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    # Local apps
    'users.apps.UsersConfig',
    'articles.apps.ArticlesConfig',
]

# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals  # Connect signals when app is ready
```

**Best practices:**
- One app per domain concept (users, orders, products)
- Apps should be reusable and loosely coupled
- Use `apps.py` `ready()` to connect signals

---

<a name="q3"></a>
## Q3. ⭐⭐ URL Routing and Path Converters

**Answer:**
Django's URL dispatcher maps URL patterns to view functions using `urlpatterns`.

```python
# myproject/urls.py — root URL config
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('core.urls')),
]

# users/urls.py — app-level URL config
from django.urls import path, re_path
from . import views

app_name = 'users'  # Namespace

urlpatterns = [
    # Path converters: int, str, slug, uuid, path
    path('', views.UserListView.as_view(), name='list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('<slug:username>/', views.UserProfileView.as_view(), name='profile'),
    path('<uuid:token>/verify/', views.VerifyEmailView.as_view(), name='verify'),

    # re_path — regex patterns
    re_path(r'^(?P<year>[0-9]{4})/$', views.ArchiveView.as_view(), name='archive'),
]
```

```python
# Path converter types
path('<int:pk>/', ...)       # Matches integers: 1, 42, 100
path('<str:name>/', ...)     # Matches non-empty strings (no /)
path('<slug:slug>/', ...)    # Matches slugs: my-article-title
path('<uuid:token>/', ...)   # Matches UUIDs: 550e8400-e29b-41d4-a716-446655440000
path('<path:subpath>/', ...) # Matches any string including /

# Custom path converter
class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value

from django.urls import register_converter
register_converter(FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('<yyyy:year>/', views.year_archive),
]

# Reverse URL resolution
from django.urls import reverse

url = reverse('users:detail', kwargs={'pk': 1})  # '/users/1/'
url = reverse('users:profile', args=['alice'])    # '/users/alice/'
```

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ Function-Based Views vs Class-Based Views

**Answer:**

| Feature | FBV | CBV |
|---------|-----|-----|
| Simplicity | ✅ Simple | ❌ More complex |
| Reusability | ❌ Manual | ✅ Inheritance |
| HTTP methods | Manual if/else | Automatic dispatch |
| Mixins | ❌ | ✅ |
| Readability | ✅ Explicit | ❌ Magic methods |

```python
# Function-Based View (FBV)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Article
from .forms import ArticleForm

@login_required
@require_http_methods(['GET', 'POST'])
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article-detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'articles/form.html', {'form': form})


# Class-Based View (CBV) — equivalent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/form.html'
    success_url = reverse_lazy('article-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Custom CBV with method dispatch
from django.views import View
from django.http import JsonResponse

class ArticleAPIView(View):
    def get(self, request, pk=None):
        if pk:
            article = get_object_or_404(Article, pk=pk)
            return JsonResponse({'title': article.title})
        articles = list(Article.objects.values('id', 'title'))
        return JsonResponse({'articles': articles})

    def post(self, request):
        import json
        data = json.loads(request.body)
        article = Article.objects.create(**data, author=request.user)
        return JsonResponse({'id': article.pk}, status=201)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return JsonResponse({}, status=204)
```

**Follow-up:** When would you prefer FBV over CBV?
- FBV: simple one-off views, complex custom logic
- CBV: CRUD operations, reusable patterns, when using DRF

---

<a name="q5"></a>
## Q5. ⭐⭐⭐ Django Middleware

**Answer:**
Middleware is a **hook into Django's request/response processing** — a lightweight plugin system for globally altering input or output.

```python
# Middleware execution order:
# Request:  M1 → M2 → M3 → View
# Response: M3 → M2 → M1 → Client

# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'myapp.middleware.RequestTimingMiddleware',  # Custom
]
```

```python
# myapp/middleware.py

import time
import logging

logger = logging.getLogger(__name__)


# Style 1: Function-based middleware (modern, recommended)
def request_timing_middleware(get_response):
    """Log request processing time."""

    def middleware(request):
        start = time.time()
        response = get_response(request)
        duration = time.time() - start

        logger.info(
            f"{request.method} {request.path} "
            f"→ {response.status_code} ({duration:.3f}s)"
        )
        response['X-Processing-Time'] = f"{duration:.3f}s"
        return response

    return middleware


# Style 2: Class-based middleware
class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time setup on server start

    def __call__(self, request):
        # Code before view
        start = time.time()

        response = self.get_response(request)

        # Code after view
        duration = time.time() - start
        response['X-Processing-Time'] = f"{duration:.3f}s"
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Called just before Django calls the view. Return None to continue."""
        pass

    def process_exception(self, request, exception):
        """Called when a view raises an exception."""
        logger.error(f"Exception in {request.path}: {exception}")
        return None  # Return None to let Django handle it

    def process_template_response(self, request, response):
        """Called after view returns a TemplateResponse."""
        return response


# Practical example: API key authentication middleware
class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-Key')
            if not api_key or not self._is_valid_key(api_key):
                from django.http import JsonResponse
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        return self.get_response(request)

    def _is_valid_key(self, key):
        from .models import APIKey
        return APIKey.objects.filter(key=key, is_active=True).exists()
```

**Follow-up:** What is the difference between middleware and decorators?
- Middleware: global, applies to all requests
- Decorators: per-view, more granular control

---

<a name="q6"></a>
## Q6. ⭐⭐⭐ Django Signals

**Answer:**
Signals allow **decoupled applications to get notified** when certain actions occur elsewhere in the framework.

```python
# Built-in signals:
# pre_save, post_save, pre_delete, post_delete
# m2m_changed, request_started, request_finished
# user_logged_in, user_logged_out, user_login_failed

# users/signals.py
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver, Signal
from django.contrib.auth import get_user_model

User = get_user_model()

# @receiver decorator — connect signal to handler
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile when a User is created."""
    if created:
        from .models import Profile
        Profile.objects.create(user=instance)
        # Send welcome email
        from .tasks import send_welcome_email
        send_welcome_email.delay(instance.pk)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Keep Profile in sync with User."""
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(pre_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """Clean up before user deletion."""
    import logging
    logging.getLogger(__name__).info(f"Deleting user: {instance.email}")


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Track login activity."""
    from .models import LoginActivity
    LoginActivity.objects.create(
        user=user,
        ip_address=request.META.get('REMOTE_ADDR'),
    )


# Custom signals
order_completed = Signal()  # Custom signal

# Sending a custom signal
def complete_order(order):
    order.status = 'completed'
    order.save()
    order_completed.send(sender=order.__class__, order=order)

# Receiving a custom signal
@receiver(order_completed)
def on_order_completed(sender, order, **kwargs):
    send_invoice(order)
    update_inventory(order)


# Connect signals in apps.py (preferred over module-level)
# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals  # noqa — triggers @receiver decorators
```

**When to use signals vs direct calls:**
- ✅ Signals: decoupled apps, third-party integrations, audit logging
- ❌ Signals: when you need the return value, when order matters, simple same-app logic (use direct calls instead — signals make code harder to trace)

---

<a name="q7"></a>
## Q7. ⭐⭐ Django Forms and Validation

**Answer:**
Django forms handle **HTML form rendering, data validation, and cleaning**.

```python
# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Article, User


# ModelForm — tied to a model
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'editor'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {'title': 'Article Title'}
        help_texts = {'title': 'Max 200 characters'}

    # Field-level validation: clean_<fieldname>
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters.")
        # Check uniqueness
        qs = Article.objects.filter(title__iexact=title)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("An article with this title already exists.")
        return title.strip()

    # Cross-field validation: clean()
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title', '')
        content = cleaned_data.get('content', '')

        if title and content and title.lower() in content.lower():
            raise ValidationError("Content should not repeat the title verbatim.")
        return cleaned_data


# Standalone Form (not tied to model)
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        initial='medium'
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        blocked = ['spam@example.com']
        if email in blocked:
            raise ValidationError("This email address is not allowed.")
        return email.lower()


# View using the form
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.cleaned_data is now safe to use
            send_contact_email(form.cleaned_data)
            return redirect('contact-success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
```

```html
<!-- Template rendering -->
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <!-- Or render manually: -->
  {% for field in form %}
    <div class="field {% if field.errors %}error{% endif %}">
      {{ field.label_tag }}
      {{ field }}
      {% for error in field.errors %}
        <span class="error">{{ error }}</span>
      {% endfor %}
    </div>
  {% endfor %}
  <button type="submit">Submit</button>
</form>
```

---

<a name="q8"></a>
## Q8. ⭐⭐ Django Templates and Template Tags

**Answer:**

```html
<!-- base.html — base template -->
<!DOCTYPE html>
<html>
<head>
  <title>{% block title %}My Site{% endblock %}</title>
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>
  {% include 'partials/navbar.html' %}

  <main>
    {% block content %}{% endblock %}
  </main>

  {% block scripts %}{% endblock %}
</body>
</html>

<!-- articles/list.html — child template -->
{% extends 'base.html' %}
{% load humanize %}

{% block title %}Articles — {{ block.super }}{% endblock %}

{% block content %}
  <!-- Variables -->
  <h1>{{ page_title }}</h1>

  <!-- Filters -->
  <p>{{ article.published_at|date:"F j, Y" }}</p>
  <p>{{ article.content|truncatewords:50|linebreaks }}</p>
  <p>{{ article.views|intcomma }}</p>  <!-- humanize filter -->

  <!-- Tags -->
  {% for article in articles %}
    {% if article.is_published %}
      <article>
        <h2>{{ article.title|title }}</h2>
        <p>{{ article.author.get_full_name|default:"Anonymous" }}</p>
      </article>
    {% endif %}
  {% empty %}
    <p>No articles found.</p>
  {% endfor %}

  <!-- URL tag -->
  <a href="{% url 'article-detail' pk=article.pk %}">Read more</a>

  <!-- With tag — create variable in template -->
  {% with total=articles.count %}
    <p>{{ total }} article{{ total|pluralize }}</p>
  {% endwith %}
{% endblock %}
```

```python
# Custom template tags and filters
# myapp/templatetags/myapp_tags.py
from django import template
from django.utils.html import format_html

register = template.Library()

# Simple filter
@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

# Filter with is_safe (output is safe HTML)
@register.filter(is_safe=True)
def badge(value, color='blue'):
    return format_html('<span class="badge badge-{}">{}</span>', color, value)

# Simple tag
@register.simple_tag
def current_year():
    from datetime import date
    return date.today().year

# Simple tag with context
@register.simple_tag(takes_context=True)
def active_link(context, url_name):
    request = context['request']
    from django.urls import reverse
    return 'active' if request.path == reverse(url_name) else ''

# Inclusion tag — renders a template
@register.inclusion_tag('partials/user_card.html', takes_context=True)
def user_card(context, user):
    return {'user': user, 'request': context['request']}
```

```html
<!-- Using custom tags -->
{% load myapp_tags %}

{{ price|multiply:1.18 }}
{{ status|badge:"green" }}
<footer>© {% current_year %}</footer>
<a class="{% active_link 'home' %}">Home</a>
{% user_card request.user %}
```

---

<a name="q9"></a>
## Q9. ⭐⭐⭐ Django Authentication System

**Answer:**
Django provides a complete authentication system: users, passwords, groups, permissions, and sessions.

```python
# Authentication views (built-in)
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
]

# Custom User model (recommended for all projects)
# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# settings.py
AUTH_USER_MODEL = 'users.User'  # Must be set BEFORE first migration!

# Authentication in views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'auth/login.html')

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

@permission_required('articles.add_article', raise_exception=True)
def create_article(request):
    pass

# CBV authentication
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'dashboard.html')

class AdminView(PermissionRequiredMixin, View):
    permission_required = 'articles.change_article'
```

---

<a name="q10"></a>
## Q10. ⭐⭐ Permissions and Authorization

**Answer:**

```python
# Django's built-in permission system
# Each model gets 4 permissions: add, change, delete, view

# Checking permissions
user.has_perm('articles.add_article')
user.has_perm('articles.change_article')
user.has_perms(['articles.add_article', 'articles.change_article'])

# Assigning permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Article)
permission = Permission.objects.get(content_type=content_type, codename='publish_article')
user.user_permissions.add(permission)

# Groups
from django.contrib.auth.models import Group

editors_group = Group.objects.create(name='Editors')
editors_group.permissions.add(permission)
user.groups.add(editors_group)

# Custom permissions on model
class Article(models.Model):
    class Meta:
        permissions = [
            ('publish_article', 'Can publish articles'),
            ('feature_article', 'Can feature articles on homepage'),
        ]

# Object-level permissions (django-guardian)
from guardian.shortcuts import assign_perm, get_objects_for_user

assign_perm('articles.change_article', user, article_instance)
user.has_perm('articles.change_article', article_instance)

articles = get_objects_for_user(user, 'articles.change_article', Article)

# Template permission checks
# {% if perms.articles.add_article %}
#   <a href="{% url 'article-create' %}">New Article</a>
# {% endif %}
```

---

<a name="q11"></a>
## Q11. ⭐⭐ Session Management

**Answer:**

```python
# settings.py — session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'       # Default: DB
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # Redis/Memcached
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # Cache + DB fallback
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'   # File system
# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'  # Cookie

SESSION_COOKIE_AGE = 1209600       # 2 weeks (seconds)
SESSION_COOKIE_SECURE = True       # HTTPS only
SESSION_COOKIE_HTTPONLY = True     # No JS access
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Using sessions in views
def shopping_cart(request):
    # Get session data
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        product_id = request.POST['product_id']
        quantity = int(request.POST.get('quantity', 1))

        # Modify session
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True  # Force save if mutating nested objects

    # Delete session key
    if 'clear' in request.POST:
        del request.session['cart']

    # Flush entire session (logout)
    # request.session.flush()

    return render(request, 'cart.html', {'cart': cart})

# Session expiry
request.session.set_expiry(300)   # Expire in 5 minutes
request.session.set_expiry(0)     # Expire when browser closes
request.session.set_expiry(None)  # Use SESSION_COOKIE_AGE
```

---

<a name="q12"></a>
## Q12. ⭐⭐ Django Caching

**Answer:**

```python
# settings.py — cache backends
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# 1. Per-view caching
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

@cache_page(60 * 15)  # Cache for 15 minutes
@vary_on_headers('Accept-Language')
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

# CBV caching
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')
class ArticleListView(ListView):
    model = Article

# 2. Template fragment caching
# {% load cache %}
# {% cache 900 article_list %}
#   {% for article in articles %}...{% endfor %}
# {% endcache %}

# 3. Low-level cache API
from django.core.cache import cache

def get_article(pk):
    cache_key = f'article_{pk}'
    article = cache.get(cache_key)

    if article is None:
        article = Article.objects.select_related('author').get(pk=pk)
        cache.set(cache_key, article, timeout=60 * 30)  # 30 min

    return article

# Cache with versioning
cache.set('key', value, version=2)
cache.get('key', version=2)
cache.incr_version('key')  # Invalidate old version

# Cache invalidation on save
from django.db.models.signals import post_save

@receiver(post_save, sender=Article)
def invalidate_article_cache(sender, instance, **kwargs):
    cache.delete(f'article_{instance.pk}')
    cache.delete('article_list')

# Cache many keys at once
cache.set_many({'a': 1, 'b': 2, 'c': 3})
cache.get_many(['a', 'b', 'c'])
cache.delete_many(['a', 'b', 'c'])
```

---

<a name="q13"></a>
## Q13. ⭐⭐ Static and Media Files

**Answer:**

```python
# settings.py
import os

# Static files (CSS, JS, images bundled with app)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # collectstatic destination
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Additional static dirs

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py — serve media in development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your urls
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Note: Never use this in production! Use Nginx/S3 instead.

# Model with file upload
class Article(models.Model):
    thumbnail = models.ImageField(
        upload_to='articles/thumbnails/%Y/%m/',  # Dynamic path
        blank=True,
        null=True
    )
    attachment = models.FileField(
        upload_to='articles/attachments/',
        validators=[FileExtensionValidator(['pdf', 'docx'])]
    )

# Custom upload_to function
def article_thumbnail_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'articles/{instance.pk}/thumbnail.{ext}'

thumbnail = models.ImageField(upload_to=article_thumbnail_path)

# Template usage
# {% load static %}
# <link rel="stylesheet" href="{% static 'css/main.css' %}">
# <img src="{{ article.thumbnail.url }}">

# Production: AWS S3 with django-storages
# pip install django-storages boto3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
AWS_STORAGE_BUCKET_NAME = 'my-bucket'
AWS_S3_REGION_NAME = 'us-east-1'
```

---

<a name="q14"></a>
## Q14. ⭐⭐ Django Admin Customization

**Answer:**

```python
# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # List view
    list_display = ['title', 'author', 'status', 'thumbnail_preview', 'published_at']
    list_filter = ['status', 'category', 'published_at']
    search_fields = ['title', 'content', 'author__email']
    list_editable = ['status']
    list_per_page = 25
    date_hierarchy = 'published_at'
    ordering = ['-published_at']

    # Detail view
    fieldsets = [
        ('Content', {
            'fields': ['title', 'content', 'thumbnail']
        }),
        ('Metadata', {
            'fields': ['author', 'category', 'tags', 'status'],
            'classes': ['collapse'],  # Collapsible section
        }),
        ('Timestamps', {
            'fields': ['published_at'],
            'classes': ['collapse'],
        }),
    ]
    readonly_fields = ['published_at', 'thumbnail_preview']
    filter_horizontal = ['tags']  # M2M widget
    raw_id_fields = ['author']    # FK with many options — use popup search
    autocomplete_fields = ['category']

    # Custom column with HTML
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50">', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Preview'

    # Custom actions
    actions = ['publish_articles', 'unpublish_articles']

    @admin.action(description='Publish selected articles')
    def publish_articles(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} articles published.')

    @admin.action(description='Unpublish selected articles')
    def unpublish_articles(self, request, queryset):
        queryset.update(status='draft')

    # Optimize queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')

    # Inline admin
    inlines = [CommentInline]


class CommentInline(admin.TabularInline):  # or StackedInline
    model = Comment
    extra = 0  # No empty forms
    readonly_fields = ['created_at']
    fields = ['author', 'content', 'is_approved', 'created_at']


# Customize admin site
admin.site.site_header = 'My Company Admin'
admin.site.site_title = 'My Company'
admin.site.index_title = 'Dashboard'
```

---

<a name="q15"></a>
## Q15. ⭐ Custom Management Commands

**Answer:**

```python
# myapp/management/commands/send_digests.py
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send weekly digest emails to subscribers'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=7,
                            help='Number of days to include in digest')
        parser.add_argument('--dry-run', action='store_true',
                            help='Preview without sending emails')
        parser.add_argument('user_ids', nargs='*', type=int,
                            help='Specific user IDs (optional)')

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        user_ids = options['user_ids']

        since = timezone.now() - timedelta(days=days)

        from users.models import User
        from articles.models import Article

        users = User.objects.filter(is_subscribed=True)
        if user_ids:
            users = users.filter(pk__in=user_ids)

        articles = Article.objects.filter(
            published_at__gte=since,
            status='published'
        ).order_by('-published_at')

        if not articles.exists():
            self.stdout.write(self.style.WARNING('No articles found for digest.'))
            return

        sent = 0
        for user in users.iterator():
            if dry_run:
                self.stdout.write(f'[DRY RUN] Would send digest to {user.email}')
            else:
                try:
                    send_digest_email(user, articles)
                    sent += 1
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f'Failed to send to {user.email}: {e}')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {sent} digest emails.')
        )

# Usage:
# python manage.py send_digests
# python manage.py send_digests --days=14
# python manage.py send_digests --dry-run
# python manage.py send_digests 1 2 3  # Specific users
```

---

<a name="q16"></a>
## Q16. ⭐⭐⭐ Django Security Best Practices

**Answer:**

```python
# settings.py — production security settings
DEBUG = False
ALLOWED_HOSTS = ['mysite.com', 'www.mysite.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Clickjacking
X_FRAME_OPTIONS = 'DENY'

# Content type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS filter
SECURE_BROWSER_XSS_FILTER = True

# Secret key — use environment variable
import os
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Database — never hardcode credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
    }
}
```

```python
# CSRF protection
# Django includes CsrfViewMiddleware by default
# In templates: {% csrf_token %}
# In AJAX:
# headers: {'X-CSRFToken': getCookie('csrftoken')}

# SQL injection prevention — always use ORM or parameterized queries
# ❌ NEVER do this:
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# ✅ Use ORM:
User.objects.filter(name=user_input)

# ✅ Or parameterized raw SQL:
cursor.execute("SELECT * FROM users WHERE name = %s", [user_input])

# XSS prevention — Django auto-escapes template variables
# {{ user_input }}  → auto-escaped ✅
# {{ user_input|safe }}  → NOT escaped ❌ (only use for trusted content)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Rate limiting with django-ratelimit
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    pass
```

---

<a name="q17"></a>
## Q17. ⭐⭐ Settings Configuration and Environments

**Answer:**

```python
# Split settings by environment
# config/settings/
#   __init__.py
#   base.py       ← shared settings
#   development.py
#   production.py
#   testing.py

# base.py
from pathlib import Path
import os
from decouple import config  # pip install python-decouple

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')
INSTALLED_APPS = [...]
MIDDLEWARE = [...]

# development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
INTERNAL_IPS = ['127.0.0.1']

# production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 60,  # Persistent connections
    }
}

# .env file
# SECRET_KEY=your-secret-key-here
# DB_NAME=mydb
# DB_USER=myuser
# DB_PASSWORD=mypassword
# DB_HOST=localhost

# Run with specific settings:
# DJANGO_SETTINGS_MODULE=config.settings.production python manage.py runserver
```

---

<a name="q18"></a>
## Q18. ⭐ Context Processors

**Answer:**
Context processors add **variables to every template context** automatically.

```python
# myapp/context_processors.py
from .models import Category, Notification

def global_categories(request):
    """Add categories to every template."""
    return {
        'global_categories': Category.objects.filter(is_active=True)
    }

def unread_notifications(request):
    """Add notification count for authenticated users."""
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return {'unread_notification_count': count}
    return {'unread_notification_count': 0}

# settings.py — register context processors
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            # Custom
            'myapp.context_processors.global_categories',
            'myapp.context_processors.unread_notifications',
        ],
    },
}]

# Now available in ALL templates:
# {{ global_categories }}
# {{ unread_notification_count }}
```

---

<a name="q19"></a>
## Q19. ⭐⭐ Generic Class-Based Views (GCBV)

**Answer:**

```python
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView, RedirectView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 10
    ordering = ['-published_at']

    def get_queryset(self):
        qs = super().get_queryset().filter(status='published')
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs.select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super().get_object()
        # Increment view count
        Article.objects.filter(pk=obj.pk).update(views=models.F('views') + 1)
        return obj


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content', 'category']
    template_name = 'articles/form.html'
    success_url = reverse_lazy('article-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'content', 'category']
    template_name = 'articles/form.html'

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        # Users can only edit their own articles
        return super().get_queryset().filter(author=self.request.user)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/confirm_delete.html'
    success_url = reverse_lazy('article-list')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
```

---

<a name="q20"></a>
## Q20. ⭐⭐⭐ Django Request/Response Lifecycle

**Answer:**

```
1. Browser sends HTTP request to server

2. WSGI/ASGI server (Gunicorn/Uvicorn) receives request
   → Creates WSGIRequest/ASGIRequest object

3. Django Middleware (process_request)
   → SecurityMiddleware: HTTPS redirect, security headers
   → SessionMiddleware: loads session from DB/cache
   → AuthenticationMiddleware: sets request.user
   → CsrfViewMiddleware: validates CSRF token

4. URL Resolver
   → Matches URL pattern in urlpatterns
   → Extracts URL parameters

5. View function/class is called
   → Accesses request.user, request.GET, request.POST
   → Queries database via ORM
   → Processes business logic

6. Template rendering (if applicable)
   → Template engine processes .html file
   → Context variables substituted
   → Template tags/filters executed

7. Response created (HttpResponse/JsonResponse/TemplateResponse)

8. Django Middleware (process_response)
   → SessionMiddleware: saves session
   → SecurityMiddleware: adds security headers

9. WSGI/ASGI server sends HTTP response to browser
```

```python
# Inspecting the request object
def my_view(request):
    print(request.method)          # 'GET', 'POST', etc.
    print(request.path)            # '/articles/1/'
    print(request.GET)             # QueryDict: {'page': ['2']}
    print(request.POST)            # QueryDict: {'title': ['Hello']}
    print(request.FILES)           # Uploaded files
    print(request.user)            # Authenticated user or AnonymousUser
    print(request.session)         # Session dict
    print(request.META)            # HTTP headers + server info
    print(request.headers)         # HTTP headers (Django 2.2+)
    print(request.content_type)    # 'application/json'
    print(request.is_ajax())       # Deprecated; check headers instead
    print(request.META.get('HTTP_X_REQUESTED_WITH'))
```

---

### [← Back to Index](./README.md) | [Next: Django ORM →](./02_Django_ORM.md)
