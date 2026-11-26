# 13 — Exception Handling & Error Responses
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ How does DRF handle exceptions?](#q1)
2. [⭐⭐⭐ How do you return a consistent error format across the API?](#q2)
3. [⭐⭐ How do you create a custom API exception?](#q3)
4. [⭐⭐ How do you handle unexpected errors (500) in production?](#q4)
5. [⭐ What does `get_object_or_404` do in DRF?](#q5)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ How does DRF handle exceptions?
**Answer:** Exceptions raised in a view are caught by `handle_exception()` and passed to the exception handler (default `rest_framework.views.exception_handler`). It converts DRF's `APIException` subclasses plus Django's `Http404` and `PermissionDenied` into proper responses (`{"detail": "..."}` with the right status). Any other exception returns `None` from the handler → it's re-raised → **500**.

Common built-ins: `ValidationError` (400), `NotAuthenticated` / `AuthenticationFailed` (401/403), `PermissionDenied` (403), `NotFound` (404), `MethodNotAllowed` (405), `Throttled` (429).

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ How do you return a consistent error format across the API?
**Answer:** Write a custom exception handler and register it in settings.

```python
# core/exceptions.py
from rest_framework.views import exception_handler

def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "success": False,
            "error": {"status": response.status_code, "details": response.data},
        }
    return response   # None → unhandled → 500 (log it, don't leak stack traces)

REST_FRAMEWORK = {"EXCEPTION_HANDLER": "core.exceptions.api_exception_handler"}
```

---

<a name="q3"></a>
## Q3. ⭐⭐ How do you create a custom API exception?
**Answer:** Subclass `APIException` with `status_code`, `default_detail`, `default_code`.

```python
class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Upstream service temporarily unavailable, try again later."
    default_code = "service_unavailable"

raise ServiceUnavailable()
```

---

<a name="q4"></a>
## Q4. ⭐⭐ How do you handle unexpected errors (500) in production?
**Answer:** Keep `DEBUG=False` so stack traces aren't returned; log the exception with context (request id, user, endpoint) to monitoring (Sentry/APM); return a generic JSON 500 message. Don't catch broad exceptions inside views just to return 400 — that hides real bugs.

---

<a name="q5"></a>
## Q5. ⭐ What does `get_object_or_404` do in DRF?
**Answer:** Fetches the object or raises `Http404`, which DRF turns into `{"detail": "Not found."}` with status 404. DRF has its own `rest_framework.generics.get_object_or_404` that also returns 404 for invalid lookup values (e.g. a bad UUID) instead of a 500.
