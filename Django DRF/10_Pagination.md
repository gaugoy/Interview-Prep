# 10 — Pagination
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What pagination styles does DRF provide?](#q1)
2. [⭐⭐ How do you customise page size or let the client choose it?](#q2)
3. [⭐⭐ Why is offset/page-number pagination slow on large tables, and what's the fix?](#q3)
4. [⭐ How do you change the paginated response format?](#q4)
5. [⭐ How do you paginate in an `APIView` (not a generic view)?](#q5)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What pagination styles does DRF provide?
**Answer:**
- **`PageNumberPagination`** — `?page=3`; response has `count`, `next`, `previous`, `results`. Simple, good for UIs with page numbers.
- **`LimitOffsetPagination`** — `?limit=20&offset=40`; flexible, client controls the window.
- **`CursorPagination`** — opaque `?cursor=...`; only next/previous, needs a stable `ordering` (default `-created`). Fast on big tables and stable when new rows are inserted, but no jumping to page N and no total count.

```python
REST_FRAMEWORK = {"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination", "PAGE_SIZE": 20}
```
Pagination applies only to list actions of generic views/ViewSets.

---

<a name="q2"></a>
## Q2. ⭐⭐ How do you customise page size or let the client choose it?
**Answer:** Subclass the paginator and set it on the view (`pagination_class`) or globally.

```python
class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"   # ?page_size=50
    max_page_size = 100                   # protect the server
```
Set `pagination_class = None` on a view to disable pagination.

---

<a name="q3"></a>
## Q3. ⭐⭐ Why is offset/page-number pagination slow on large tables, and what's the fix?
**Answer:** `OFFSET 100000` makes the database read and skip 100,000 rows, and `count` runs a `COUNT(*)` on every request — both get slower as data grows. Fix: `CursorPagination` (keyset — "rows after the last one I saw") on an indexed, unique-ish ordering field, and avoid total counts when not needed.

---

<a name="q4"></a>
## Q4. ⭐ How do you change the paginated response format?
**Answer:** Override `get_paginated_response()`:

```python
class MetaPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "meta": {"total": self.page.paginator.count, "page": self.page.number},
            "data": data,
        })
```

---

<a name="q5"></a>
## Q5. ⭐ How do you paginate in an `APIView` (not a generic view)?
**Answer:** Use the paginator manually:

```python
paginator = PageNumberPagination()
page = paginator.paginate_queryset(queryset, request, view=self)
serializer = BookSerializer(page, many=True)
return paginator.get_paginated_response(serializer.data)
```
