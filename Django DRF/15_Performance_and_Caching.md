# 15 — Performance & Caching
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What is the N+1 problem in DRF and how do you fix it?](#q1)
2. [⭐⭐ How do you make a slow list endpoint faster?](#q2)
3. [⭐⭐ How do you cache API responses in DRF?](#q3)
4. [⭐⭐ How do you invalidate cached API data when it changes?](#q4)
5. [⭐ Are DRF serializers slow? What can you do?](#q5)
6. [⭐⭐ How do you handle long-running work triggered by an API call?](#q6)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What is the N+1 problem in DRF and how do you fix it?
**Answer:** Serializers read attributes object by object. Nested serializers, `source="author.name"`, related fields and `SerializerMethodField`s that touch relations each run one query **per object** → 1 query for the list + N for relations. Fix in the view's `get_queryset()`:
- `select_related()` for ForeignKey / OneToOne (SQL JOIN).
- `prefetch_related()` for reverse FK / ManyToMany (one extra query).
- `annotate()` for counts/sums instead of `SerializerMethodField` queries.

```python
def get_queryset(self):
    return (Post.objects
            .select_related("author")
            .prefetch_related("tags")
            .annotate(comment_count=Count("comments")))
```
Detect with django-debug-toolbar / django-silk, or `assertNumQueries` in tests.

---

<a name="q2"></a>
## Q2. ⭐⭐ How do you make a slow list endpoint faster?
**Answer:** In order of usual impact:
1. Fix N+1 (`select_related` / `prefetch_related` / `annotate`).
2. Paginate, and use cursor pagination on large tables.
3. Return fewer fields — a lighter list serializer, `only()` for wide tables.
4. Add DB indexes for the filter/order fields.
5. Cache responses or expensive computations (Redis).
6. Move heavy work out of the request (background tasks).

---

<a name="q3"></a>
## Q3. ⭐⭐ How do you cache API responses in DRF?
**Answer:** For whole responses, use Django's `cache_page` via `method_decorator` on `list`/`retrieve` (or `dispatch`). Make the cache vary by user/headers if responses differ per user (`vary_on_headers("Authorization")`), otherwise users may see each other's data. For finer control, cache computed data in Redis with explicit keys and invalidate on writes.

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

---

<a name="q4"></a>
## Q4. ⭐⭐ How do you invalidate cached API data when it changes?
**Answer:** Options: delete the cache key in `perform_create/update/destroy` (or `transaction.on_commit` so it runs after the DB commit), use versioned keys (bump a version number on write), or short TTLs for data that can be slightly stale. Watch out: `queryset.update()` and `bulk_*` skip signals, so signal-based invalidation misses them.

---

<a name="q5"></a>
## Q5. ⭐ Are DRF serializers slow? What can you do?
**Answer:** For very large responses, serializer field processing in Python can be significant. Options: smaller list serializers, `values()` + a plain `Serializer` or build dicts directly for read-only bulk endpoints, paginate, or cache. Measure first — usually the database (N+1) is the real problem, not the serializer.

---

<a name="q6"></a>
## Q6. ⭐⭐ How do you handle long-running work triggered by an API call?
**Answer:** Don't do it inside the request. Save a job record, enqueue a background task (Celery / RabbitMQ), and return **202 Accepted** with a job id; the client polls a status endpoint or gets a webhook/notification. Enqueue with `transaction.on_commit()` so the worker doesn't start before the data is committed.
