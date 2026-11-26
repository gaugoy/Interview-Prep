# 16 — Scenario-Based & Common Production Issues
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ An endpoint is slow in production but fast locally. How do you debug it?](#q1)
2. [⭐⭐⭐ Users can see or edit other users' data. What went wrong and how do you fix it?](#q2)
3. [⭐⭐⭐ The frontend gets CORS errors calling the API. How do you fix it?](#q3)
4. [⭐⭐⭐ `request.user` is `AnonymousUser` even though the client sends a token. Why?](#q4)
5. [⭐⭐⭐ A client retries a POST and duplicate orders get created. How do you prevent it?](#q5)
6. [⭐⭐ Two users update the same record at the same time and one change is lost. What do you do?](#q6)
7. [⭐⭐ A serializer field isn't being saved. What do you check?](#q7)
8. [⭐⭐ How do you implement soft delete in a DRF API?](#q8)
9. [⭐⭐ The API returns stale data after an update. Possible causes?](#q9)
10. [⭐⭐ How do you design an endpoint that calls a slow or unreliable third-party API?](#q10)
11. [⭐⭐ How do you handle timezones in API responses?](#q11)
12. [⭐⭐ How do you secure a DRF API in production? (checklist)](#q12)
13. [⭐⭐ How would you implement a multi-tenant API?](#q13)
14. [⭐ How do you build a webhook receiver endpoint in DRF?](#q14)
15. [⭐ An endpoint returns 500 only for some records. How do you approach it?](#q15)

---

Short "how would you handle…" answers. Give the cause first, then the fix.

<a name="q1"></a>
## Q1. ⭐⭐⭐ An endpoint is slow in production but fast locally. How do you debug it?
**Answer:** Local data is small, so N+1 and missing indexes are hidden. Steps: check APM/logs for which endpoint and how many queries → reproduce with production-like data → count queries (debug-toolbar/silk, `CaptureQueriesContext`) → fix N+1 with `select_related`/`prefetch_related`/`annotate` → check slow SQL with `EXPLAIN` and add indexes → paginate/trim fields → cache if still needed. Then add a query-count test so it doesn't come back.

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ Users can see or edit other users' data. What went wrong and how do you fix it?
**Answer:** Usually the ViewSet's `queryset` returns all rows and only object-level permissions were added — but object permissions don't run on list views, and a missing check on one action exposes everything. Fix: scope data in `get_queryset()` (e.g. `filter(owner=request.user)` or by tenant), keep object-level permission classes for edit rules, never accept `owner`/`tenant_id` from the client, and add tests that user A gets 404 on user B's objects.

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ The frontend gets CORS errors calling the API. How do you fix it?
**Answer:** The browser blocks cross-origin requests unless the API returns the right `Access-Control-Allow-*` headers. Use `django-cors-headers`: add `CorsMiddleware` near the top of `MIDDLEWARE` (before `CommonMiddleware`) and whitelist origins with `CORS_ALLOWED_ORIGINS` (don't use allow-all in production). If cookies are used, set `CORS_ALLOW_CREDENTIALS = True` and `CSRF_TRUSTED_ORIGINS`. CORS is a browser rule — Postman working doesn't mean CORS is configured.

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ `request.user` is `AnonymousUser` even though the client sends a token. Why?
**Answer:** Common causes: the auth class isn't in `DEFAULT_AUTHENTICATION_CLASSES` (or the view overrides `authentication_classes`), wrong header format (`Bearer` vs `Token` prefix), a proxy/server stripping the `Authorization` header (e.g. Apache needs `WSGIPassAuthorization On`), an expired token, or checking `request.user` in Django middleware — DRF authenticates inside the view, so middleware sees the session user only.

---

<a name="q5"></a>
## Q5. ⭐⭐⭐ A client retries a POST and duplicate orders get created. How do you prevent it?
**Answer:** POST isn't idempotent. Add an **idempotency key**: the client sends a unique `Idempotency-Key` header; the server stores it with the result (DB unique constraint or Redis) and returns the saved response on repeats. Also add DB unique constraints on natural keys and disable double-submit on the frontend.

---

<a name="q6"></a>
## Q6. ⭐⭐ Two users update the same record at the same time and one change is lost. What do you do?
**Answer:** That's a lost update. Options: **optimistic locking** — a `version` field (or `updated_at`) sent by the client; update with `filter(pk=..., version=v).update(..., version=v+1)` and return **409 Conflict** if 0 rows changed. **Pessimistic locking** — `select_for_update()` inside `transaction.atomic()` for short critical sections (stock, balances). For counters use `F()` expressions.

---

<a name="q7"></a>
## Q7. ⭐⭐ A serializer field isn't being saved. What do you check?
**Answer:** Is it in `Meta.fields`? Is it `read_only` (explicitly, in `read_only_fields`, or auto — e.g. `auto_now`, `editable=False`, a `SerializerMethodField`)? Is the client using the exact field name? For nested/M2M data, did you override `create()`/`update()` and pop + save it? Did a custom `create()` forget to pass it on? Print `serializer.validated_data` to see what survived validation.

---

<a name="q8"></a>
## Q8. ⭐⭐ How do you implement soft delete in a DRF API?
**Answer:** Add `is_deleted` / `deleted_at` to the model, override `perform_destroy()` to set it instead of deleting, and exclude deleted rows in `get_queryset()` (or a custom default manager). Return 204 as usual. Remember unique constraints may need a condition (`UniqueConstraint(..., condition=Q(is_deleted=False))`).

---

<a name="q9"></a>
## Q9. ⭐⭐ The API returns stale data after an update. Possible causes?
**Answer:** Response caching without invalidation (or `cache_page` without varying by user), a read replica lagging behind the primary right after a write, Redis cache invalidated by signals that `update()`/`bulk_*` don't fire, or a CDN/proxy caching GET responses. Fix the specific layer: invalidate on write (`on_commit`), read-your-own-writes from the primary, correct cache headers.

---

<a name="q10"></a>
## Q10. ⭐⭐ How do you design an endpoint that calls a slow or unreliable third-party API?
**Answer:** Set timeouts on the HTTP call, retry with backoff for transient errors, map failures to a clear error (502/503) instead of a 500, and don't hold a DB transaction open during the call. If the user doesn't need the result immediately, do it in a background task and return 202. Cache results that don't change often.

---

<a name="q11"></a>
## Q11. ⭐⭐ How do you handle timezones in API responses?
**Answer:** Keep `USE_TZ = True`, store UTC, and return ISO-8601 datetimes with offset (DRF's default). Let the client convert to local time. Accept timezone-aware input; reject or clearly define naive datetimes.

---

<a name="q12"></a>
## Q12. ⭐⭐ How do you secure a DRF API in production? (checklist)
**Answer:** HTTPS only; authentication on by default (`IsAuthenticated` globally, open endpoints explicitly); data scoped in `get_queryset()`; no `fields = "__all__"` (avoid leaking fields); input validation; throttling on login and public endpoints; CORS whitelist; `DEBUG=False` and no stack traces; short-lived tokens; browsable API disabled; secrets in env/vault; dependency updates; audit logging for sensitive actions.

---

<a name="q13"></a>
## Q13. ⭐⭐ How would you implement a multi-tenant API?
**Answer:** Identify the tenant per request (from the user, a header, or subdomain) in authentication/middleware, then **always** filter by tenant in `get_queryset()` — ideally via a base ViewSet/mixin so nobody forgets — and set the tenant on create in `perform_create()`. Add tests that cross-tenant access returns 404. Separate schemas/databases are options when stronger isolation is required.

---

<a name="q14"></a>
## Q14. ⭐ How do you build a webhook receiver endpoint in DRF?
**Answer:** A small `APIView` with `AllowAny` permission but **signature verification** (HMAC of the body with a shared secret, compared using `hmac.compare_digest`), quick 200 response, processing in a background task, and idempotency by event id because providers retry.

---

<a name="q15"></a>
## Q15. ⭐ An endpoint returns 500 only for some records. How do you approach it?
**Answer:** Check the error log/trace for the failing id. Usual causes: a `None` related object accessed in a serializer (`source="author.name"` when author is null → set `allow_null`/`default`), bad legacy data failing a field conversion, or a division/format error in a `SerializerMethodField`. Fix the code to handle the case, add a test with that data, and clean the data if needed.
