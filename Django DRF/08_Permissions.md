# 08 — Permissions
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What are permission classes in DRF? Name the built-in ones.](#q1)
2. [⭐⭐⭐ `has_permission` vs `has_object_permission`?](#q2)
3. [⭐⭐⭐ Write a custom permission: only the owner can edit, others can read.](#q3)
4. [⭐⭐ How do you combine permissions with OR / NOT?](#q4)
5. [⭐⭐ How do you implement role-based access control (RBAC) in DRF?](#q5)
6. [⭐⭐ What status code is returned when a permission fails?](#q6)
7. [⭐ How does `DjangoModelPermissions` work?](#q7)
8. [⭐⭐ Should I hide unauthorized objects with 403 or 404?](#q8)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What are permission classes in DRF? Name the built-in ones.
**Answer:** Classes that decide if a request may proceed, run after authentication. Built-ins:
- `AllowAny` — everyone.
- `IsAuthenticated` — logged-in users only.
- `IsAdminUser` — `user.is_staff`.
- `IsAuthenticatedOrReadOnly` — anyone can read (GET/HEAD/OPTIONS), only logged-in users can write.
- `DjangoModelPermissions` — maps methods to Django model perms (`add/change/delete/view`).
- `DjangoObjectPermissions` — per-object perms (with a backend like django-guardian).
Set globally with `DEFAULT_PERMISSION_CLASSES` or per view with `permission_classes`. All classes in the list must pass (AND).

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ `has_permission` vs `has_object_permission`?
**Answer:** `has_permission(request, view)` — runs for **every** request, before the handler (view-level). `has_object_permission(request, view, obj)` — runs only when `get_object()` (or `check_object_permissions`) is called, i.e. on detail actions (retrieve/update/delete).

**Gotcha:** object permissions are **not** applied to list views — filter the list in `get_queryset()` instead.

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ Write a custom permission: only the owner can edit, others can read.
**Answer:**
```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = "Only the owner can modify this object."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:      # GET, HEAD, OPTIONS
            return True
        return obj.owner == request.user

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```

---

<a name="q4"></a>
## Q4. ⭐⭐ How do you combine permissions with OR / NOT?
**Answer:** DRF supports `&`, `|` and `~` operators on permission classes:
```python
permission_classes = [IsAuthenticated & (IsOwner | IsAdminUser)]
```

---

<a name="q5"></a>
## Q5. ⭐⭐ How do you implement role-based access control (RBAC) in DRF?
**Answer:** Map roles to Django groups (or a role field/table), then write permission classes that check the role, optionally per action. Keep data scoping in `get_queryset()` (e.g. user sees only their department's records) and action rules in permission classes.

```python
class HasRole(BasePermission):
    def has_permission(self, request, view):
        required = getattr(view, "required_roles", {}).get(view.action, set())
        user_roles = set(request.user.groups.values_list("name", flat=True))
        return not required or bool(required & user_roles)

class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasRole]
    required_roles = {"destroy": {"admin"}, "create": {"admin", "editor"}}
```
Cache the user's roles per request if checked often.

---

<a name="q6"></a>
## Q6. ⭐⭐ What status code is returned when a permission fails?
**Answer:** **403 Forbidden** if the user is authenticated (or the auth scheme gives no `WWW-Authenticate` header); **401** if not authenticated and the auth class supports a `WWW-Authenticate` header. A custom `message` attribute on the permission class sets the error text.

---

<a name="q7"></a>
## Q7. ⭐ How does `DjangoModelPermissions` work?
**Answer:** It requires the user to have the model permission matching the method: POST → `add`, PUT/PATCH → `change`, DELETE → `delete` (GET needs only authentication by default; subclass to require `view`). It needs a `queryset` on the view to know the model.

---

<a name="q8"></a>
## Q8. ⭐⭐ Should I hide unauthorized objects with 403 or 404?
**Answer:** Filtering them out in `get_queryset()` returns **404**, which doesn't reveal the object exists — usually preferred for private data (other users' orders). 403 is fine when the existence isn't sensitive and you want a clear "not allowed" message.
