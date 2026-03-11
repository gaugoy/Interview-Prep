# 🗄️ 02 — Django ORM
### [← Back to Index](./README.md)

---

## Table of Contents
1. [Model Creation and Field Types](#q1)
2. [Model Relationships](#q2)
3. [QuerySet API and Chaining](#q3)
4. [Filtering, Excluding, and Lookups](#q4)
5. [Q Objects — Complex Queries](#q5)
6. [Aggregation and Annotation](#q6)
7. [select_related and prefetch_related](#q7)
8. [The N+1 Query Problem](#q8)
9. [Raw SQL Queries](#q9)
10. [Database Transactions](#q10)
11. [Custom Model Managers and QuerySets](#q11)
12. [Django Migrations](#q12)
13. [Database Indexing](#q13)
14. [F Expressions and Atomic Updates](#q14)
15. [Model Inheritance](#q15)
16. [Bulk Operations](#q16)
17. [QuerySet Evaluation and Caching](#q17)
18. [Values, ValuesListand Defer/Only](#q18)

---

<a name="q1"></a>
## Q1. ⭐⭐ Model Creation and Field Types

**Answer:**

```python
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

User = get_user_model()


class Article(models.Model):
    # String fields
    title = models.CharField(max_length=200)          # VARCHAR
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()                       # TEXT (unlimited)
    summary = models.TextField(blank=True)

    # Numeric fields
    views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    price = models.FloatField(null=True, blank=True)

    # Boolean
    is_published = models.BooleanField(default=False)
    is_featured = models.NullBooleanField()  # True/False/None

    # Date/Time
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Set on create
    updated_at = models.DateTimeField(auto_now=True)      # Set on every save
    publish_date = models.DateField(null=True, blank=True)

    # Choice field
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )

    # File fields
    thumbnail = models.ImageField(upload_to='articles/%Y/%m/', blank=True)
    attachment = models.FileField(upload_to='attachments/', blank=True)

    # JSON field (PostgreSQL / Django 3.1+)
    metadata = models.JSONField(default=dict, blank=True)

    # UUID
    import uuid
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Email, URL
    source_url = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)

    # IP Address
    author_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['slug']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_per_author'
            ),
            models.CheckConstraint(
                check=models.Q(rating__gte=0) & models.Q(rating__lte=10),
                name='valid_rating_range'
            ),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article-detail', kwargs={'slug': self.slug})

    @property
    def is_draft(self):
        return self.status == self.STATUS_DRAFT

    def publish(self):
        from django.utils import timezone
        self.status = self.STATUS_PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at'])
```

**Key field options:**
- `null=True` — allow NULL in database
- `blank=True` — allow empty in forms/validation
- `default=` — default value
- `unique=True` — database-level uniqueness
- `db_index=True` — create database index
- `editable=False` — hide from forms/admin

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ Model Relationships

**Answer:**

```python
from django.db import models


# ForeignKey — Many-to-One
class Article(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,       # Delete articles when user deleted
        related_name='articles',        # user.articles.all()
        related_query_name='article',   # User.objects.filter(article__title=...)
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,      # Set to NULL when category deleted
        null=True,
        related_name='articles',
    )

# on_delete options:
# CASCADE     — delete related objects
# SET_NULL    — set FK to NULL (requires null=True)
# SET_DEFAULT — set FK to default value
# PROTECT     — prevent deletion if related objects exist (raises ProtectedError)
# RESTRICT    — like PROTECT but allows deletion if related objects also deleted
# DO_NOTHING  — do nothing (may cause DB integrity errors)


# ManyToManyField
class Article(models.Model):
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='articles',
    )
    # With through model (extra fields on relationship)
    collaborators = models.ManyToManyField(
        'auth.User',
        through='ArticleCollaborator',
        related_name='collaborated_articles',
    )

class ArticleCollaborator(models.Model):
    """Through model for Article-User M2M with extra fields."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)  # Extra field
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['article', 'user']]


# OneToOneField
class UserProfile(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='profile',  # user.profile
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)


# Querying relationships
user = User.objects.get(pk=1)

# ForeignKey — reverse access
articles = user.articles.all()                    # All articles by user
articles = user.articles.filter(status='published')

# ManyToMany
article = Article.objects.get(pk=1)
article.tags.all()                                # All tags
article.tags.add(tag1, tag2)                      # Add tags
article.tags.remove(tag1)                         # Remove tag
article.tags.set([tag1, tag2])                    # Replace all tags
article.tags.clear()                              # Remove all tags

# Through model
ArticleCollaborator.objects.create(
    article=article, user=user, role='editor'
)

# OneToOne — reverse access
user.profile                                      # Direct access (raises DoesNotExist if none)
getattr(user, 'profile', None)                    # Safe access
```

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ QuerySet API and Chaining

**Answer:**
QuerySets are **lazy** — they don't hit the database until evaluated.

```python
from django.db.models import Q, F, Count, Sum, Avg

# QuerySets are lazy — no DB hit yet
qs = Article.objects.all()
qs = qs.filter(status='published')
qs = qs.order_by('-published_at')
# DB hit happens here:
for article in qs:  # Evaluation
    print(article.title)

# Chaining — each method returns a new QuerySet
articles = (
    Article.objects
    .filter(status='published')
    .filter(author__is_active=True)
    .exclude(category__name='Spam')
    .select_related('author', 'category')
    .prefetch_related('tags')
    .order_by('-published_at', 'title')
    .distinct()
    [:10]  # LIMIT 10
)

# Methods that return QuerySets (lazy):
# filter(), exclude(), order_by(), reverse()
# select_related(), prefetch_related()
# values(), values_list(), only(), defer()
# annotate(), aggregate() (aggregate returns dict, not QS)
# distinct(), union(), intersection(), difference()
# select_for_update()

# Methods that evaluate the QuerySet (DB hit):
# list(qs), len(qs), bool(qs)
# qs[0], qs[0:5]  (slicing)
# for obj in qs
# qs.count(), qs.exists()
# qs.get(), qs.first(), qs.last()
# qs.create(), qs.update(), qs.delete()
# qs.aggregate()

# Useful single-object methods
Article.objects.get(pk=1)           # Raises DoesNotExist or MultipleObjectsReturned
Article.objects.get_or_create(slug='hello', defaults={'title': 'Hello'})
Article.objects.update_or_create(slug='hello', defaults={'title': 'Hello World'})
Article.objects.first()             # First by ordering, or None
Article.objects.last()              # Last by ordering, or None
Article.objects.earliest('created_at')
Article.objects.latest('created_at')
Article.objects.exists()            # True/False — faster than count() > 0
Article.objects.count()             # SELECT COUNT(*)
```

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ Filtering, Excluding, and Field Lookups

**Answer:**

```python
# Basic filtering
Article.objects.filter(status='published')
Article.objects.exclude(status='draft')

# Field lookups (double underscore __)
Article.objects.filter(title__exact='Hello')        # = 'Hello'
Article.objects.filter(title__iexact='hello')       # case-insensitive =
Article.objects.filter(title__contains='Django')    # LIKE '%Django%'
Article.objects.filter(title__icontains='django')   # case-insensitive LIKE
Article.objects.filter(title__startswith='How')     # LIKE 'How%'
Article.objects.filter(title__endswith='Guide')     # LIKE '%Guide'
Article.objects.filter(title__in=['A', 'B', 'C'])   # IN ('A', 'B', 'C')
Article.objects.filter(views__gt=100)               # > 100
Article.objects.filter(views__gte=100)              # >= 100
Article.objects.filter(views__lt=100)               # < 100
Article.objects.filter(views__lte=100)              # <= 100
Article.objects.filter(views__range=(10, 100))      # BETWEEN 10 AND 100
Article.objects.filter(published_at__date=date.today())
Article.objects.filter(published_at__year=2024)
Article.objects.filter(published_at__month=3)
Article.objects.filter(published_at__isnull=True)   # IS NULL
Article.objects.filter(thumbnail__isnull=False)     # IS NOT NULL

# Traversing relationships with __
Article.objects.filter(author__email='alice@example.com')
Article.objects.filter(author__profile__is_verified=True)
Article.objects.filter(tags__name='python')
Article.objects.filter(tags__name__in=['python', 'django'])

# Chaining filters (AND)
Article.objects.filter(status='published').filter(views__gt=100)
# Equivalent to:
Article.objects.filter(status='published', views__gt=100)

# Exclude (NOT)
Article.objects.exclude(status='draft')
Article.objects.exclude(author__isnull=True)

# Combining filter and exclude
Article.objects.filter(status='published').exclude(category__name='Spam')
```

---

<a name="q5"></a>
## Q5. ⭐⭐⭐ Q Objects — Complex Queries

**Answer:**
`Q` objects allow **OR, AND, NOT** combinations in queries.

```python
from django.db.models import Q

# OR query
Article.objects.filter(
    Q(status='published') | Q(is_featured=True)
)
# SQL: WHERE status = 'published' OR is_featured = TRUE

# AND query (same as chaining filters)
Article.objects.filter(
    Q(status='published') & Q(views__gt=100)
)

# NOT query
Article.objects.filter(~Q(status='draft'))
# SQL: WHERE NOT status = 'draft'

# Complex combinations
Article.objects.filter(
    (Q(status='published') | Q(is_featured=True)) &
    Q(author__is_active=True) &
    ~Q(category__name='Spam')
)

# Dynamic Q object building
def search_articles(query=None, status=None, author_id=None):
    filters = Q()  # Empty Q — no-op

    if query:
        filters &= Q(title__icontains=query) | Q(content__icontains=query)

    if status:
        filters &= Q(status=status)

    if author_id:
        filters &= Q(author_id=author_id)

    return Article.objects.filter(filters)

# Usage
results = search_articles(query='django', status='published')
```

---

<a name="q6"></a>
## Q6. ⭐⭐⭐ Aggregation and Annotation

**Answer:**
- `aggregate()` — returns a **single dict** with computed values across all rows
- `annotate()` — adds a **computed field to each row** in the QuerySet

```python
from django.db.models import Count, Sum, Avg, Max, Min, F, Value
from django.db.models.functions import Coalesce, TruncMonth

# aggregate() — single result
stats = Article.objects.aggregate(
    total=Count('id'),
    total_views=Sum('views'),
    avg_views=Avg('views'),
    max_views=Max('views'),
    min_views=Min('views'),
)
# {'total': 150, 'total_views': 45000, 'avg_views': 300.0, ...}

# Filtered aggregate
published_stats = Article.objects.filter(
    status='published'
).aggregate(
    count=Count('id'),
    avg_rating=Avg('rating'),
)

# annotate() — per-row computed field
# Count articles per author
authors = User.objects.annotate(
    article_count=Count('articles'),
    published_count=Count('articles', filter=Q(articles__status='published')),
).order_by('-article_count')

for author in authors:
    print(f"{author.email}: {author.article_count} articles")

# Count tags per article
articles = Article.objects.annotate(
    tag_count=Count('tags'),
    avg_collaborator_rating=Avg('collaborators__profile__rating'),
).filter(tag_count__gt=2)  # Filter on annotation!

# Group by with annotate
from django.db.models.functions import TruncMonth

monthly_stats = (
    Article.objects
    .filter(status='published')
    .annotate(month=TruncMonth('published_at'))
    .values('month')
    .annotate(count=Count('id'), total_views=Sum('views'))
    .order_by('month')
)
# [{'month': datetime(2024, 1, 1), 'count': 12, 'total_views': 3400}, ...]

# Conditional annotation
from django.db.models import Case, When, IntegerField

articles = Article.objects.annotate(
    popularity_score=Case(
        When(views__gte=10000, then=Value(3)),
        When(views__gte=1000, then=Value(2)),
        When(views__gte=100, then=Value(1)),
        default=Value(0),
        output_field=IntegerField(),
    )
)
```

---

<a name="q7"></a>
## Q7. ⭐⭐⭐ select_related and prefetch_related

**Answer:**
Both optimize queries for related objects, but work differently:

| | `select_related` | `prefetch_related` |
|-|-----------------|-------------------|
| Relationship | ForeignKey, OneToOne | ManyToMany, reverse FK |
| SQL | Single JOIN query | Separate queries + Python join |
| When to use | FK/O2O (single object) | M2M, reverse FK (multiple objects) |

```python
# Without optimization — N+1 problem
articles = Article.objects.all()  # 1 query
for article in articles:
    print(article.author.email)   # N queries (one per article)!
    print(article.category.name)  # N more queries!

# select_related — SQL JOIN (for FK and OneToOne)
articles = Article.objects.select_related('author', 'category').all()
# 1 query with JOIN — fetches author and category in same query
for article in articles:
    print(article.author.email)   # No extra query — already fetched
    print(article.category.name)  # No extra query

# Traverse multiple levels
articles = Article.objects.select_related(
    'author',
    'author__profile',  # Follow FK chain
    'category',
)

# prefetch_related — separate queries (for M2M and reverse FK)
articles = Article.objects.prefetch_related('tags', 'comments').all()
# 3 queries: articles + tags + comments
for article in articles:
    print(article.tags.all())     # No extra query — already prefetched
    print(article.comments.all()) # No extra query

# Prefetch with custom queryset (Prefetch object)
from django.db.models import Prefetch

approved_comments = Comment.objects.filter(is_approved=True).select_related('author')

articles = Article.objects.prefetch_related(
    Prefetch('comments', queryset=approved_comments, to_attr='approved_comments')
).all()

for article in articles:
    print(article.approved_comments)  # Only approved comments, pre-fetched

# Combine both
articles = (
    Article.objects
    .select_related('author', 'category')       # FK — JOIN
    .prefetch_related('tags', 'collaborators')  # M2M — separate queries
    .filter(status='published')
)
```

---

<a name="q8"></a>
## Q8. ⭐⭐⭐ The N+1 Query Problem

**Answer:**
The N+1 problem occurs when fetching N objects triggers **N additional queries** for related data.

```python
# ❌ N+1 problem — 1 + N queries
articles = Article.objects.all()  # Query 1: SELECT * FROM articles
for article in articles:
    # Query 2, 3, 4... N+1: SELECT * FROM users WHERE id = ?
    print(article.author.email)

# With 100 articles → 101 queries!

# ✅ Fix with select_related — 1 query
articles = Article.objects.select_related('author').all()
for article in articles:
    print(article.author.email)  # No extra query

# ❌ N+1 with M2M
articles = Article.objects.all()
for article in articles:
    tags = article.tags.all()  # N queries!

# ✅ Fix with prefetch_related — 2 queries
articles = Article.objects.prefetch_related('tags').all()
for article in articles:
    tags = article.tags.all()  # No extra query

# Detecting N+1 with Django Debug Toolbar
# Install: pip install django-debug-toolbar
# Shows query count per request

# Detecting with django-silk or logging
import logging
logger = logging.getLogger('django.db.backends')
# settings.py:
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

# Detecting programmatically
from django.test.utils import override_settings
from django.db import connection, reset_queries

settings.DEBUG = True
reset_queries()

articles = list(Article.objects.all())
for a in articles:
    _ = a.author.email

print(f"Queries: {len(connection.queries)}")  # Shows N+1
```

---

<a name="q9"></a>
## Q9. ⭐⭐ Raw SQL Queries

**Answer:**

```python
from django.db import connection

# Method 1: Manager.raw() — returns model instances
articles = Article.objects.raw(
    'SELECT * FROM articles_article WHERE status = %s ORDER BY published_at DESC',
    ['published']
)
for article in articles:
    print(article.title)  # Full model instances

# With annotations from raw SQL
articles = Article.objects.raw('''
    SELECT a.*, COUNT(c.id) as comment_count
    FROM articles_article a
    LEFT JOIN articles_comment c ON c.article_id = a.id
    GROUP BY a.id
''')

# Method 2: cursor.execute() — for non-model queries
with connection.cursor() as cursor:
    cursor.execute('''
        SELECT category_id, COUNT(*) as count, AVG(views) as avg_views
        FROM articles_article
        WHERE status = %s
        GROUP BY category_id
        ORDER BY count DESC
    ''', ['published'])

    rows = cursor.fetchall()
    # [(1, 45, 234.5), (2, 32, 189.2), ...]

    # Named columns
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

# ⚠️ Always use parameterized queries — NEVER string formatting
# ❌ DANGEROUS:
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
# ✅ SAFE:
cursor.execute("SELECT * FROM users WHERE name = %s", [user_input])
```

---

<a name="q10"></a>
## Q10. ⭐⭐⭐ Database Transactions

**Answer:**
Transactions ensure **atomicity** — either all operations succeed or all are rolled back.

```python
from django.db import transaction

# Method 1: atomic() decorator
@transaction.atomic
def transfer_credits(from_user, to_user, amount):
    from_user.credits -= amount
    from_user.save()
    # If this raises an exception, the above save is rolled back
    to_user.credits += amount
    to_user.save()

# Method 2: atomic() context manager
def create_order(user, items):
    with transaction.atomic():
        order = Order.objects.create(user=user, status='pending')
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
            )
        # Deduct inventory
        for item in items:
            Product.objects.filter(pk=item['product'].pk).update(
                stock=F('stock') - item['quantity']
            )
        # If any step fails, entire transaction rolls back
    return order

# Savepoints — nested transactions
def complex_operation():
    with transaction.atomic():
        do_step_1()

        try:
            with transaction.atomic():  # Creates savepoint
                do_risky_step_2()
        except Exception:
            pass  # Rolls back to savepoint, outer transaction continues

        do_step_3()

# on_commit — run code AFTER transaction commits
def create_user(email, password):
    with transaction.atomic():
        user = User.objects.create_user(email=email, password=password)
        # This runs ONLY if transaction commits successfully
        transaction.on_commit(lambda: send_welcome_email.delay(user.pk))
    return user

# select_for_update — pessimistic locking
def reserve_seat(seat_id, user):
    with transaction.atomic():
        seat = Seat.objects.select_for_update().get(pk=seat_id)
        if seat.is_available:
            seat.user = user
            seat.is_available = False
            seat.save()
            return True
        return False
```

---

<a name="q11"></a>
## Q11. ⭐⭐⭐ Custom Model Managers and QuerySets

**Answer:**

```python
from django.db import models
from django.utils import timezone


# Custom QuerySet — chainable methods
class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')

    def draft(self):
        return self.filter(status='draft')

    def featured(self):
        return self.filter(is_featured=True)

    def recent(self, days=30):
        since = timezone.now() - timezone.timedelta(days=days)
        return self.filter(published_at__gte=since)

    def by_author(self, user):
        return self.filter(author=user)

    def with_stats(self):
        return self.annotate(
            comment_count=models.Count('comments'),
            tag_count=models.Count('tags'),
        )

    def popular(self, min_views=1000):
        return self.filter(views__gte=min_views).order_by('-views')


# Custom Manager — entry point for QuerySet
class ArticleManager(models.Manager):
    def get_queryset(self):
        # Default queryset — always exclude deleted
        return ArticleQuerySet(self.model, using=self._db).filter(
            is_deleted=False
        )

    # Convenience methods that delegate to QuerySet
    def published(self):
        return self.get_queryset().published()

    def featured(self):
        return self.get_queryset().featured()

    def for_homepage(self):
        return (
            self.get_queryset()
            .published()
            .featured()
            .select_related('author', 'category')
            .prefetch_related('tags')
            .order_by('-published_at')
            [:5]
        )


class Article(models.Model):
    # ...fields...
    is_deleted = models.BooleanField(default=False)

    # Replace default manager
    objects = ArticleManager()

    # Keep access to unfiltered queryset
    all_objects = models.Manager()

    class Meta:
        default_manager_name = 'objects'


# Usage — chainable!
Article.objects.published()
Article.objects.published().featured()
Article.objects.published().recent(days=7).popular()
Article.objects.for_homepage()

# Access deleted articles
Article.all_objects.filter(is_deleted=True)
```

---

<a name="q12"></a>
## Q12. ⭐⭐⭐ Django Migrations

**Answer:**
Migrations track **schema changes** and apply them to the database.

```bash
# Create migrations from model changes
python manage.py makemigrations
python manage.py makemigrations articles  # Specific app
python manage.py makemigrations --name add_views_field articles

# Apply migrations
python manage.py migrate
python manage.py migrate articles         # Specific app
python manage.py migrate articles 0003   # Migrate to specific version
python manage.py migrate articles zero   # Rollback all migrations for app

# Inspect migrations
python manage.py showmigrations
python manage.py showmigrations articles
python manage.py sqlmigrate articles 0001  # Show SQL for migration
python manage.py migrate --plan           # Show what will be applied
```

```python
# migrations/0002_add_views_field.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=300),  # Changed from 200
        ),
    ]


# Data migration — transform existing data
class Migration(migrations.Migration):
    dependencies = [('articles', '0003_add_slug')]

    def populate_slugs(apps, schema_editor):
        Article = apps.get_model('articles', 'Article')
        from django.utils.text import slugify
        for article in Article.objects.all():
            article.slug = slugify(article.title)
            article.save(update_fields=['slug'])

    def reverse_populate_slugs(apps, schema_editor):
        Article = apps.get_model('articles', 'Article')
        Article.objects.update(slug='')

    operations = [
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
    ]


# Squash migrations (combine many into one)
# python manage.py squashmigrations articles 0001 0010
```

**Common migration issues:**
- `makemigrations` detects no changes → check `INSTALLED_APPS`
- Migration conflicts → `python manage.py makemigrations --merge`
- Fake migrations → `python manage.py migrate --fake articles 0001`

---

<a name="q13"></a>
## Q13. ⭐⭐ Database Indexing

**Answer:**

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # Single field index
    slug = models.SlugField(unique=True)                      # Unique index
    status = models.CharField(max_length=20)
    published_at = models.DateTimeField(null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # ForeignKey automatically creates an index

    class Meta:
        indexes = [
            # Composite index — for queries filtering on both fields
            models.Index(fields=['status', 'published_at'],
                         name='idx_status_published'),

            # Partial index (PostgreSQL) — index only published articles
            models.Index(
                fields=['published_at'],
                name='idx_published_articles',
                condition=models.Q(status='published'),
            ),

            # Functional index (PostgreSQL)
            models.Index(
                models.functions.Upper('title'),
                name='idx_upper_title',
            ),
        ]

        # Unique together (creates unique composite index)
        unique_together = [['author', 'slug']]

        # Or use UniqueConstraint (preferred)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'slug'],
                name='unique_author_slug'
            ),
        ]

# When to add indexes:
# ✅ Columns frequently used in WHERE clauses
# ✅ Columns used in JOIN conditions (FKs auto-indexed)
# ✅ Columns used in ORDER BY
# ✅ Columns used in GROUP BY
# ❌ Small tables (full scan is faster)
# ❌ Columns with low cardinality (e.g., boolean — not worth it)
# ❌ Columns rarely queried
# ❌ Tables with very high write volume (index maintenance overhead)

# Check query performance with EXPLAIN
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("EXPLAIN ANALYZE SELECT * FROM articles_article WHERE status = 'published'")
    print(cursor.fetchall())
```

---

<a name="q14"></a>
## Q14. ⭐⭐⭐ F Expressions and Atomic Updates

**Answer:**
`F()` expressions reference **database column values** without loading them into Python — enabling atomic updates.

```python
from django.db.models import F

# ❌ Race condition — two requests could both read 100, both write 101
article = Article.objects.get(pk=1)
article.views = article.views + 1  # Read into Python
article.save()                     # Write back

# ✅ Atomic update — database does the increment
Article.objects.filter(pk=1).update(views=F('views') + 1)
# SQL: UPDATE articles SET views = views + 1 WHERE id = 1

# F() in filter
Article.objects.filter(views__gt=F('likes'))  # views > likes

# F() in annotations
from django.db.models import ExpressionWrapper, FloatField

articles = Article.objects.annotate(
    engagement_rate=ExpressionWrapper(
        F('likes') * 100.0 / F('views'),
        output_field=FloatField()
    )
)

# F() with related fields
Article.objects.filter(views__gt=F('author__profile__follower_count'))

# Combining F() expressions
Article.objects.update(
    score=F('views') * 0.3 + F('likes') * 0.7
)

# F() with dates
from datetime import timedelta
from django.db.models import DurationValue

# Articles where deadline is within 7 days of creation
Article.objects.filter(
    deadline__lte=F('created_at') + timedelta(days=7)
)
```

---

<a name="q15"></a>
## Q15. ⭐⭐ Model Inheritance

**Answer:**

```python
# 1. Abstract Base Class — no DB table, shared fields
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # No DB table created

class Article(TimestampedModel):
    title = models.CharField(max_length=200)
    # Gets created_at and updated_at from parent

class Comment(TimestampedModel):
    content = models.TextField()
    # Gets created_at and updated_at from parent


# 2. Multi-table Inheritance — separate DB table per model
class Content(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Article(Content):
    content = models.TextField()
    # DB: content_article table with OneToOne to content_content

class Video(Content):
    url = models.URLField()
    # DB: content_video table with OneToOne to content_content

# Access parent
article = Article.objects.get(pk=1)
article.title        # From Content
article.content      # From Article
article.content_ptr  # OneToOne to Content


# 3. Proxy Models — same DB table, different Python behavior
class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

class PublishedArticle(Article):
    """Proxy model — same table, different manager/methods."""
    class Meta:
        proxy = True

    objects = PublishedArticleManager()  # Custom manager

    def get_absolute_url(self):
        return f'/published/{self.pk}/'

# Use case: different admin views, different default ordering
```

---

<a name="q16"></a>
## Q16. ⭐⭐ Bulk Operations

**Answer:**

```python
# bulk_create — insert many rows in one query
articles = [
    Article(title=f'Article {i}', status='draft', author=user)
    for i in range(1000)
]
Article.objects.bulk_create(articles, batch_size=100)
# One query (or batches of 100) instead of 1000 queries

# bulk_create options
Article.objects.bulk_create(
    articles,
    batch_size=100,
    ignore_conflicts=True,  # Skip duplicates (PostgreSQL)
    update_conflicts=True,  # Upsert (PostgreSQL 4.1+)
    update_fields=['title', 'status'],
    unique_fields=['slug'],
)

# bulk_update — update many rows
articles = Article.objects.filter(status='draft')
for article in articles:
    article.status = 'published'

Article.objects.bulk_update(articles, ['status'], batch_size=100)
# One query instead of N queries

# QuerySet.update() — update all matching rows
Article.objects.filter(status='draft').update(
    status='published',
    published_at=timezone.now()
)
# SQL: UPDATE articles SET status='published', published_at=NOW() WHERE status='draft'

# QuerySet.delete() — delete all matching rows
Article.objects.filter(
    status='draft',
    created_at__lt=timezone.now() - timedelta(days=30)
).delete()
# Returns (count, {model: count}) tuple

# iterator() — memory-efficient iteration for large querysets
for article in Article.objects.all().iterator(chunk_size=1000):
    process(article)
# Fetches 1000 rows at a time instead of loading all into memory
```

---

<a name="q17"></a>
## Q17. ⭐⭐ QuerySet Evaluation and Caching

**Answer:**

```python
# QuerySets are lazy — no DB hit until evaluated
qs = Article.objects.filter(status='published')  # No DB hit
qs = qs.order_by('-published_at')                # No DB hit

# Evaluation triggers (DB hit):
list(qs)          # Evaluate and cache all results
bool(qs)          # True if any results
len(qs)           # Count (evaluates all)
qs[0]             # Single item (no full cache)
qs[0:5]           # Slice (no full cache)
for obj in qs:    # Iterate (evaluates and caches)
    pass

# QuerySet caching — once evaluated, results are cached
articles = Article.objects.all()
list(articles)    # DB hit — results cached
list(articles)    # No DB hit — uses cache
articles[0]       # No DB hit — uses cache

# ⚠️ Slicing does NOT cache
articles = Article.objects.all()
articles[0]       # DB hit
articles[0]       # DB hit again! (slicing bypasses cache)

# Force evaluation and cache
articles = list(Article.objects.all())  # Evaluate once
articles[0]       # No DB hit

# exists() vs count() vs bool()
# exists() — fastest, stops at first result
if Article.objects.filter(status='published').exists():
    pass

# count() — SELECT COUNT(*) — no data fetched
total = Article.objects.count()

# bool(qs) — evaluates entire queryset (slow for large sets)
if Article.objects.filter(status='published'):  # ❌ Slow
    pass
if Article.objects.filter(status='published').exists():  # ✅ Fast
    pass
```

---

<a name="q18"></a>
## Q18. ⭐⭐ values(), values_list(), defer(), only()

**Answer:**

```python
# values() — returns dicts instead of model instances
Article.objects.values('id', 'title', 'status')
# [{'id': 1, 'title': 'Hello', 'status': 'published'}, ...]

# values() with related fields
Article.objects.values('id', 'title', 'author__email')
# [{'id': 1, 'title': 'Hello', 'author__email': 'alice@example.com'}, ...]

# values_list() — returns tuples
Article.objects.values_list('id', 'title')
# [(1, 'Hello'), (2, 'World'), ...]

# values_list with flat=True — returns flat list (single field only)
Article.objects.values_list('id', flat=True)
# [1, 2, 3, 4, ...]

# Use case: get list of IDs
article_ids = Article.objects.filter(status='published').values_list('id', flat=True)

# only() — fetch only specified fields (defers the rest)
articles = Article.objects.only('id', 'title', 'status')
# SELECT id, title, status FROM articles
# Accessing other fields triggers additional queries!

# defer() — fetch all fields EXCEPT specified
articles = Article.objects.defer('content', 'metadata')
# SELECT id, title, status, ... (everything except content and metadata)

# When to use:
# values()/values_list(): when you don't need model methods, serialization
# only(): when you have large fields (TextField, JSONField) you don't need
# defer(): when you want most fields but skip a few large ones

# Comparison
Article.objects.all()                    # Full model instances — all fields
Article.objects.only('id', 'title')      # Model instances — limited fields
Article.objects.values('id', 'title')    # Dicts — limited fields
Article.objects.values_list('id', flat=True)  # Flat list of IDs
```

---

### [← Back to Index](./README.md) | [Next: Django REST Framework →](./03_DRF.md)
