# 09 — Throttling (Rate Limiting)
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What is throttling in DRF and which classes exist?](#q1)
2. [⭐⭐ How does DRF store throttle state? What can go wrong?](#q2)
3. [⭐⭐ Throttling vs permissions — is throttling a security feature?](#q3)
4. [⭐ How do you write a custom throttle?](#q4)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What is throttling in DRF and which classes exist?
**Answer:** Throttling limits how many requests a client can make in a time window, returning **429 Too Many Requests** (with a `Retry-After` header) when exceeded. Built-ins:
- `AnonRateThrottle` — by IP for anonymous users.
- `UserRateThrottle` — by user id for authenticated users.
- `ScopedRateThrottle` — different limits per endpoint via `throttle_scope`.

```python
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/hour", "user": "1000/hour", "login": "5/min"},
}

class LoginView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"
```

---

<a name="q2"></a>
## Q2. ⭐⭐ How does DRF store throttle state? What can go wrong?
**Answer:** It stores request timestamps in **Django's cache**. With the default local-memory cache, each worker process has its own counter, so limits are not shared across processes/servers — use a shared cache like **Redis** in production. Behind a proxy/load balancer, configure `NUM_PROXIES` so the client IP is read correctly from `X-Forwarded-For`; otherwise all users may share the proxy's IP.

---

<a name="q3"></a>
## Q3. ⭐⭐ Throttling vs permissions — is throttling a security feature?
**Answer:** Throttling controls **usage/fairness** (protect resources, limit brute force), permissions control **access**. DRF docs say throttling shouldn't be your only defence against abuse — it's approximate and can be bypassed by changing IPs; combine with a gateway/WAF rate limiting and account lockouts for login.

---

<a name="q4"></a>
## Q4. ⭐ How do you write a custom throttle?
**Answer:** Subclass `SimpleRateThrottle` and implement `get_cache_key()` (what identifies the client), or `BaseThrottle` with `allow_request()` for fully custom logic.

```python
class APIKeyThrottle(SimpleRateThrottle):
    scope = "apikey"
    def get_cache_key(self, request, view):
        key = request.headers.get("X-API-Key")
        return self.cache_format % {"scope": self.scope, "ident": key} if key else None   # None = don't throttle
```
