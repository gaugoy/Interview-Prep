# 11 — Filtering, Searching & Ordering
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ How do you filter results in a DRF API?](#q1)
2. [⭐⭐ When do you write a custom `FilterSet`?](#q2)
3. [⭐⭐ How does `SearchFilter` work and what are its limits?](#q3)
4. [⭐⭐ Why should you restrict `ordering_fields`?](#q4)
5. [⭐ Are filters applied before or after permissions/pagination?](#q5)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ How do you filter results in a DRF API?
**Answer:** Three ways:
1. **Manually** in `get_queryset()` using `self.request.query_params`.
2. **django-filter** with `DjangoFilterBackend` and `filterset_fields` / a `FilterSet`.
3. **Built-in** `SearchFilter` (text search) and `OrderingFilter` (sorting).

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "author"]          # ?status=published&author=3
    search_fields = ["title", "author__name"]       # ?search=django
    ordering_fields = ["price", "created_at"]       # ?ordering=-price
    ordering = ["-created_at"]                       # default
```

---

<a name="q2"></a>
## Q2. ⭐⭐ When do you write a custom `FilterSet`?
**Answer:** When you need ranges, custom lookups or computed filters, not just exact matches.

```python
import django_filters

class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    published_after = django_filters.DateFilter(field_name="published_on", lookup_expr="gte")

    class Meta:
        model = Book
        fields = ["status"]

# view: filterset_class = BookFilter
```

---

<a name="q3"></a>
## Q3. ⭐⭐ How does `SearchFilter` work and what are its limits?
**Answer:** It builds `icontains` lookups OR-ed across `search_fields` for each search term. Prefixes change the lookup: `^` starts-with, `=` exact, `@` full-text (PostgreSQL), `$` regex. Limits: `icontains` can't use normal B-tree indexes, so it's slow on large tables — use PostgreSQL full-text search / trigram indexes or Elasticsearch for serious search.

---

<a name="q4"></a>
## Q4. ⭐⭐ Why should you restrict `ordering_fields`?
**Answer:** If you allow ordering on any field (`"__all__"`), clients can sort by unindexed or sensitive fields, causing slow queries or leaking info through order. Whitelist only indexed, safe fields.

---

<a name="q5"></a>
## Q5. ⭐ Are filters applied before or after permissions/pagination?
**Answer:** Order inside a list action: `get_queryset()` → `filter_queryset()` (all filter backends) → pagination → serialization. Filter backends are also applied in `get_object()`, so a filtered-out object returns 404 on detail too.
