# 01 — DRF Basics & Request/Response
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What is Django REST Framework and why use it over plain Django views?](#q1)
2. [⭐⭐⭐ What are the core components of DRF?](#q2)
3. [⭐⭐ What is the request lifecycle of a DRF API call?](#q3)
4. [⭐⭐⭐ Difference between DRF `Request` and Django `HttpRequest`?](#q4)
5. [⭐⭐ Difference between DRF `Response` and Django `HttpResponse`/`JsonResponse`?](#q5)
6. [⭐⭐ What is content negotiation in DRF?](#q6)
7. [⭐⭐ What is the browsable API and should it be enabled in production?](#q7)
8. [⭐⭐⭐ Which HTTP methods and status codes do you use for CRUD in a REST API?](#q8)
9. [⭐⭐⭐ Difference between PUT and PATCH?](#q9)
10. [⭐⭐ What makes an API "RESTful"? What does idempotent mean?](#q10)
11. [⭐⭐ Where do you configure DRF globally? Name common settings.](#q11)
12. [⭐ Does DRF support async views?](#q12)
13. [⭐⭐ How do you document a DRF API (OpenAPI/Swagger)?](#q13)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What is Django REST Framework and why use it over plain Django views?
**Answer:** DRF is a toolkit on top of Django for building REST APIs. Plain Django can return `JsonResponse`, but you would hand-write parsing, validation, auth, permissions, pagination and error formats yourself. DRF gives these as reusable, configurable pieces:
- **Serializers** — convert model instances ↔ JSON and validate input.
- **Views / ViewSets / Routers** — less boilerplate for CRUD endpoints.
- **Authentication, permissions, throttling** — pluggable classes.
- **Pagination, filtering, versioning, content negotiation**, and a **browsable API** for testing in the browser.

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ What are the core components of DRF?
**Answer:** Serializers, Views (`APIView`, generic views, ViewSets), Routers, `Request`/`Response`, Authentication classes, Permission classes, Throttle classes, Pagination classes, Filter backends, Parsers & Renderers, and Exception handling. Most of them can be set globally in `REST_FRAMEWORK` settings and overridden per view.

---

<a name="q3"></a>
## Q3. ⭐⭐ What is the request lifecycle of a DRF API call?
**Answer:**
1. Django URL routing → the DRF view's `dispatch()`.
2. Django `HttpRequest` is wrapped in a DRF `Request`.
3. `initial()` runs: **authentication → permissions → throttling** (in that order).
4. Your handler (`get`, `post`, `list`, `create`…) runs; serializer validates/serializes.
5. You return a `Response`; DRF picks a **renderer** (content negotiation) and renders JSON.
6. Any exception is caught by `handle_exception()` and turned into an error response by the exception handler.

**Follow-up:** "Where does authentication actually happen?" → lazily, when `request.user` is first accessed; `initial()` forces it via `perform_authentication()`.

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ Difference between DRF `Request` and Django `HttpRequest`?
**Answer:** DRF's `Request` wraps `HttpRequest` and adds:
- `request.data` — parsed body for **any** content type (JSON, form, multipart) and for POST/PUT/PATCH. Django's `request.POST` only handles form data on POST.
- `request.query_params` — clearer name for `request.GET`.
- `request.user` / `request.auth` — set by DRF authentication classes (e.g. `auth` holds the token).

---

<a name="q5"></a>
## Q5. ⭐⭐ Difference between DRF `Response` and Django `HttpResponse`/`JsonResponse`?
**Answer:** `Response(data, status=...)` takes plain Python data (unrendered). DRF chooses the output format at the end via content negotiation (JSON, browsable HTML, etc.). `JsonResponse` is always JSON and already rendered. Use `Response` inside DRF views so renderers, browsable API and exception handling work.

```python
from rest_framework.response import Response
from rest_framework import status

return Response({"id": obj.id}, status=status.HTTP_201_CREATED)
```

---

<a name="q6"></a>
## Q6. ⭐⭐ What is content negotiation in DRF?
**Answer:** Choosing the response format based on the client's `Accept` header (or `?format=json`). DRF matches the request against the view's `renderer_classes` and uses the first suitable one. Default renderers are `JSONRenderer` and `BrowsableAPIRenderer`.

---

<a name="q7"></a>
## Q7. ⭐⭐ What is the browsable API and should it be enabled in production?
**Answer:** An HTML interface DRF renders when you open an endpoint in a browser — you can see responses and submit forms. Very handy in development. In production it's commonly disabled (keep only `JSONRenderer`) to avoid exposing API structure and to save rendering cost.

```python
REST_FRAMEWORK = {"DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"]}
```

---

<a name="q8"></a>
## Q8. ⭐⭐⭐ Which HTTP methods and status codes do you use for CRUD in a REST API?
**Answer:**
| Action | Method | Success code |
|---|---|---|
| List / retrieve | GET | 200 |
| Create | POST | 201 |
| Full update | PUT | 200 |
| Partial update | PATCH | 200 |
| Delete | DELETE | 204 |

Common errors: 400 validation error, 401 not authenticated, 403 no permission, 404 not found, 405 method not allowed, 429 throttled, 500 server error.

---

<a name="q9"></a>
## Q9. ⭐⭐⭐ Difference between PUT and PATCH?
**Answer:** **PUT** replaces the whole resource — all required fields must be sent. **PATCH** updates only the fields sent. In DRF, `partial_update()` passes `partial=True` to the serializer so missing required fields are not an error.

---

<a name="q10"></a>
## Q10. ⭐⭐ What makes an API "RESTful"? What does idempotent mean?
**Answer:** REST principles: resources identified by URLs (nouns, e.g. `/orders/5/`), standard HTTP methods for actions, stateless requests (each carries its own auth), proper status codes, and a uniform representation (usually JSON).

**Idempotent** = repeating the same request gives the same result. GET, PUT, DELETE are idempotent; POST is not (two POSTs create two objects). PATCH may or may not be, depending on the operation.

---

<a name="q11"></a>
## Q11. ⭐⭐ Where do you configure DRF globally? Name common settings.
**Answer:** In `settings.py` under `REST_FRAMEWORK`. Anything set there can be overridden on a view with class attributes (`permission_classes`, `pagination_class`, …).

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
}
```

---

<a name="q12"></a>
## Q12. ⭐ Does DRF support async views?
**Answer:** Not natively. DRF views are synchronous; Django can run them under ASGI, but `APIView` itself isn't async. Options: keep DRF sync (fine for most APIs), use a third-party package like `adrf` for async views, or push slow work to background tasks (Celery/RabbitMQ).

---

<a name="q13"></a>
## Q13. ⭐⭐ How do you document a DRF API (OpenAPI/Swagger)?
**Answer:** Use **drf-spectacular** (current recommendation) to generate an OpenAPI 3 schema and serve Swagger UI / ReDoc. DRF's old CoreAPI schema support is deprecated. Use `@extend_schema` to describe custom actions or `SerializerMethodField` types.

```python
# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
```
