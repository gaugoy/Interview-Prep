# 14 — Testing DRF APIs
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ How do you test DRF APIs?](#q1)
2. [⭐⭐ `APIClient` vs `APIRequestFactory`?](#q2)
3. [⭐⭐ How do you authenticate in tests?](#q3)
4. [⭐⭐ What should you test in an API?](#q4)
5. [⭐ How do you mock external services in API tests?](#q5)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ How do you test DRF APIs?
**Answer:** Use `APITestCase` (Django `TestCase` with an `APIClient`) and make real requests to the endpoints; assert status codes, response data and DB state.

```python
from rest_framework.test import APITestCase
from rest_framework import status

class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("u1", password="pw")
        self.client.force_authenticate(user=self.user)

    def test_create_book(self):
        resp = self.client.post("/api/books/", {"title": "DRF", "price": "10.00"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_unauthenticated_gets_401(self):   # 401 with Token/JWT auth first; 403 with SessionAuthentication
        self.client.force_authenticate(user=None)
        self.assertEqual(self.client.get("/api/books/").status_code, status.HTTP_401_UNAUTHORIZED)
```

---

<a name="q2"></a>
## Q2. ⭐⭐ `APIClient` vs `APIRequestFactory`?
**Answer:** `APIClient` goes through the full stack (URLs, middleware, view) — integration-style tests. `APIRequestFactory` builds a request you pass directly to a view — faster unit tests of one view; use `force_authenticate(request, user=...)` with it.

---

<a name="q3"></a>
## Q3. ⭐⭐ How do you authenticate in tests?
**Answer:**
- `client.force_authenticate(user=u)` — skips real auth (fastest).
- `client.login(username=..., password=...)` — session auth.
- `client.credentials(HTTP_AUTHORIZATION="Bearer " + token)` — test the real token/JWT flow.

---

<a name="q4"></a>
## Q4. ⭐⭐ What should you test in an API?
**Answer:** Happy path (status + response shape), validation errors (400 + error fields), authentication (401), permissions (403/404 for other users' objects), filters/pagination, edge cases (empty list, invalid ids), and query count for list endpoints (`assertNumQueries`) to catch N+1.

---

<a name="q5"></a>
## Q5. ⭐ How do you mock external services in API tests?
**Answer:** Use `unittest.mock.patch` on the client/function that calls the external API (or libraries like `responses`/`requests-mock`), so tests are fast and don't depend on the network. Assert both the success and failure/timeout paths.

```python
@patch("payments.client.charge", return_value={"status": "ok"})
def test_checkout(self, mock_charge):
    resp = self.client.post("/api/checkout/", {...}, format="json")
    mock_charge.assert_called_once()
```
