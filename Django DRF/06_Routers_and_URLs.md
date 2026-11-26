# 06 — Routers & URLs
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What are routers in DRF?](#q1)
2. [⭐⭐ `SimpleRouter` vs `DefaultRouter`?](#q2)
3. [⭐⭐ What is `basename` and when is it required?](#q3)
4. [⭐ How do you create nested routes like `/projects/{id}/tasks/`?](#q4)
5. [⭐ How do you reverse a DRF URL?](#q5)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What are routers in DRF?
**Answer:** Routers generate URL patterns automatically from ViewSets. You register a ViewSet with a prefix and get list and detail routes plus routes for `@action`s.

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
urlpatterns = [path("api/", include(router.urls))]
# /api/books/        → list, create
# /api/books/{pk}/   → retrieve, update, partial_update, destroy
```

---

<a name="q2"></a>
## Q2. ⭐⭐ `SimpleRouter` vs `DefaultRouter`?
**Answer:** `DefaultRouter` = `SimpleRouter` + an API root view (`/api/` listing all endpoints) + optional format suffixes (`.json`). `SimpleRouter` is leaner if you don't want those.

---

<a name="q3"></a>
## Q3. ⭐⭐ What is `basename` and when is it required?
**Answer:** The prefix used for route names (`book-list`, `book-detail`). DRF derives it from the ViewSet's `queryset` attribute; if the ViewSet only defines `get_queryset()`, you must pass `basename` explicitly. Route names are used by `reverse()` and hyperlinked serializers.

---

<a name="q4"></a>
## Q4. ⭐ How do you create nested routes like `/projects/{id}/tasks/`?
**Answer:** Either a third-party package (`drf-nested-routers`), an `@action(detail=True)` on the parent ViewSet, or manual `path()` entries with a URL kwarg that the child ViewSet uses in `get_queryset()`:

```python
path("projects/<int:project_pk>/tasks/", TaskViewSet.as_view({"get": "list", "post": "create"}))

def get_queryset(self):
    return Task.objects.filter(project_id=self.kwargs["project_pk"])
```

---

<a name="q5"></a>
## Q5. ⭐ How do you reverse a DRF URL?
**Answer:** `rest_framework.reverse.reverse("book-detail", args=[pk], request=request)` — same as Django's `reverse` but returns an absolute URL when `request` is passed (and respects versioning).
