# 05 — Views, Generic Views & ViewSets
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What are the different ways to write views in DRF?](#q1)
2. [⭐⭐⭐ Difference between `APIView`, `GenericAPIView` and `ViewSet`?](#q2)
3. [⭐⭐ What's the difference between `ModelViewSet`, `ReadOnlyModelViewSet` and `ViewSet`?](#q3)
4. [⭐⭐⭐ `queryset` attribute vs `get_queryset()` — when do you override `get_queryset()`?](#q4)
5. [⭐⭐⭐ What are `perform_create`, `perform_update`, `perform_destroy` used for?](#q5)
6. [⭐⭐⭐ How do you add a custom endpoint to a ViewSet?](#q6)
7. [⭐⭐ What does `get_object()` do?](#q7)
8. [⭐⭐ How do you look up objects by slug/uuid instead of id?](#q8)
9. [⭐⭐ How do you apply different permissions/serializers per action in a ViewSet?](#q9)
10. [⭐ What are the concrete generic views?](#q10)
11. [⭐⭐ Function-based `@api_view` vs class-based views — when would you use FBV?](#q11)
12. [⭐ How do you return a custom response from `create()` (e.g. different status or extra data)?](#q12)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What are the different ways to write views in DRF?
**Answer:** From least to most abstraction:
1. **Function-based** with `@api_view(["GET", "POST"])`.
2. **`APIView`** — class with `get()`, `post()`… methods; you write the logic.
3. **`GenericAPIView` + mixins** — adds `queryset`, `serializer_class`, `get_object()`, pagination, filtering; mixins add `list/create/retrieve/update/destroy`.
4. **Concrete generic views** — `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`, etc.
5. **ViewSets** — group all actions for a resource in one class; URLs come from a router.

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ Difference between `APIView`, `GenericAPIView` and `ViewSet`?
**Answer:**
- `APIView` — full control, you write each HTTP method. Best for non-CRUD endpoints (login, reports, webhooks).
- `GenericAPIView` — `APIView` + queryset/serializer helpers; used with mixins for standard CRUD.
- `ViewSet` — maps **actions** (`list`, `create`, `retrieve`…) instead of HTTP methods; `ModelViewSet` gives full CRUD in a few lines and a router builds the URLs.
Rule of thumb: standard resource CRUD → `ModelViewSet`; custom flow → `APIView`.

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
```

---

<a name="q3"></a>
## Q3. ⭐⭐ What's the difference between `ModelViewSet`, `ReadOnlyModelViewSet` and `ViewSet`?
**Answer:** `ModelViewSet` = all CRUD actions. `ReadOnlyModelViewSet` = only `list` and `retrieve`. `ViewSet` (plain) = no actions — you implement `list()`, `retrieve()` etc. yourself. `GenericViewSet` = generic helpers but no actions; combine with selected mixins for e.g. "create + list only".

```python
class EventViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    ...
```

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ `queryset` attribute vs `get_queryset()` — when do you override `get_queryset()`?
**Answer:** Override `get_queryset()` whenever the queryset depends on the request — e.g. "users only see their own orders", or query-param filtering. DRF calls `.all()` on the class attribute each request so results aren't cached across requests, but anything request-specific must be in `get_queryset()`.

```python
def get_queryset(self):
    return Order.objects.filter(customer=self.request.user).select_related("customer")
```
**Follow-up:** Routers need a `basename` if there's no `queryset` attribute.

---

<a name="q5"></a>
## Q5. ⭐⭐⭐ What are `perform_create`, `perform_update`, `perform_destroy` used for?
**Answer:** Hooks in the generic mixins called after validation, where you call `serializer.save()`. Override them to inject extra data or side effects without rewriting `create()`:

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

def perform_destroy(self, instance):
    instance.is_deleted = True     # soft delete
    instance.save(update_fields=["is_deleted"])
```

---

<a name="q6"></a>
## Q6. ⭐⭐⭐ How do you add a custom endpoint to a ViewSet?
**Answer:** The `@action` decorator. `detail=True` → `/books/{pk}/publish/`; `detail=False` → `/books/recent/`. The router generates the URL.

```python
from rest_framework.decorators import action

class BookViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        book = self.get_object()
        book.status = "published"
        book.save(update_fields=["status"])
        return Response({"status": "published"})
```
You can set `permission_classes`, `serializer_class`, `url_path` per action.

---

<a name="q7"></a>
## Q7. ⭐⭐ What does `get_object()` do?
**Answer:** In detail views it: takes `get_queryset()`, applies filter backends, looks up by `lookup_field` (default `pk`) from the URL kwarg, raises 404 if not found, then calls `check_object_permissions()`. That's why object-level permissions only run when you use `get_object()`.

---

<a name="q8"></a>
## Q8. ⭐⭐ How do you look up objects by slug/uuid instead of id?
**Answer:** Set `lookup_field = "slug"` on the view (and `lookup_url_kwarg` if the URL name differs). For hyperlinked serializers set `extra_kwargs = {"url": {"lookup_field": "slug"}}`.

---

<a name="q9"></a>
## Q9. ⭐⭐ How do you apply different permissions/serializers per action in a ViewSet?
**Answer:** Use `self.action` in `get_permissions()` / `get_serializer_class()`.

```python
def get_permissions(self):
    if self.action in ("list", "retrieve"):
        return [AllowAny()]
    return [IsAdminUser()]
```

---

<a name="q10"></a>
## Q10. ⭐ What are the concrete generic views?
**Answer:** `CreateAPIView`, `ListAPIView`, `RetrieveAPIView`, `DestroyAPIView`, `UpdateAPIView`, `ListCreateAPIView`, `RetrieveUpdateAPIView`, `RetrieveDestroyAPIView`, `RetrieveUpdateDestroyAPIView`. Each is `GenericAPIView` + the matching mixins. Typical pair: `ListCreateAPIView` for `/books/` and `RetrieveUpdateDestroyAPIView` for `/books/<pk>/`.

---

<a name="q11"></a>
## Q11. ⭐⭐ Function-based `@api_view` vs class-based views — when would you use FBV?
**Answer:** FBVs are simple and explicit — good for one-off endpoints (health check, webhook). Class-based views win when you need reuse (mixins, inheritance), standard CRUD, or the generic machinery (pagination, filtering). Settings like permissions are added to FBVs with decorators (`@permission_classes([...])`).

---

<a name="q12"></a>
## Q12. ⭐ How do you return a custom response from `create()` (e.g. different status or extra data)?
**Answer:** Override `create()` in the ViewSet: validate, save, then return your own `Response`.

```python
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = serializer.save(customer=request.user)
    return Response({"order_id": order.id}, status=status.HTTP_201_CREATED)
```
