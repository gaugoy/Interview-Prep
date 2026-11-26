# 07 — Authentication (Session, Token, JWT, OAuth2)
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ Authentication vs authorization (permissions) in DRF?](#q1)
2. [⭐⭐⭐ What authentication classes does DRF provide?](#q2)
3. [⭐⭐⭐ What is JWT and how does it work?](#q3)
4. [⭐⭐⭐ How do you set up JWT in DRF?](#q4)
5. [⭐⭐⭐ Token auth vs JWT vs Session — which would you choose?](#q5)
6. [⭐⭐⭐ How do you log out / revoke a JWT?](#q6)
7. [⭐⭐ Where should a frontend store JWTs?](#q7)
8. [⭐⭐ How do you write a custom authentication class?](#q8)
9. [⭐⭐ Why does my API return 403 instead of 401 for unauthenticated users?](#q9)
10. [⭐⭐ Why does CSRF fail on my DRF POST with SessionAuthentication?](#q10)
11. [⭐ How do you integrate OAuth2 / SSO (e.g. Azure AD) with DRF?](#q11)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ Authentication vs authorization (permissions) in DRF?
**Answer:** **Authentication** = *who are you?* — identifies the user from the request (session cookie, token, JWT) and sets `request.user` / `request.auth`. **Authorization** = *what are you allowed to do?* — permission classes check `request.user` against the action. Authentication runs first; it never rejects a request by itself — unauthenticated requests just get `AnonymousUser`, and permissions decide.

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ What authentication classes does DRF provide?
**Answer:**
- `SessionAuthentication` — Django session cookie; good for same-domain web apps; enforces CSRF.
- `BasicAuthentication` — username/password on every request; only for testing/internal over HTTPS.
- `TokenAuthentication` — a static token per user from `rest_framework.authtoken`; header `Authorization: Token <key>`.
- `RemoteUserAuthentication` — trusts a header set by the web server/SSO.
Third-party: **JWT** (`djangorestframework-simplejwt`), **OAuth2** (`django-oauth-toolkit`). DRF tries classes in order; the first that returns a user wins.

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ What is JWT and how does it work?
**Answer:** JSON Web Token = `header.payload.signature`, base64url-encoded and signed (HMAC or RSA). The server issues it at login; the client sends `Authorization: Bearer <token>`; the server verifies the signature and expiry — **no DB lookup or session storage needed** (stateless). The payload is only encoded, not encrypted — never put secrets in it.

Typical setup uses two tokens: a short-lived **access** token and a longer-lived **refresh** token used to get new access tokens.

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ How do you set up JWT in DRF?
**Answer:** With `djangorestframework-simplejwt`:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,       # needs 'rest_framework_simplejwt.token_blacklist' app
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view()),          # username+password → access + refresh
    path("api/token/refresh/", TokenRefreshView.as_view()),     # refresh → new access
]
```

---

<a name="q5"></a>
## Q5. ⭐⭐⭐ Token auth vs JWT vs Session — which would you choose?
**Answer:**
- **Session** — browser app on the same domain; easy logout; needs CSRF protection.
- **DRF Token** — simple, but stored in DB, no expiry by default, one token per user; logout = delete token.
- **JWT** — stateless, scales across services, works well for mobile/SPA/microservices; but revoking before expiry needs a blacklist, and stolen tokens are valid until they expire — keep access tokens short-lived.
For enterprise SSO, use OAuth2/OpenID Connect (e.g. Azure AD) and validate the provider's tokens.

---

<a name="q6"></a>
## Q6. ⭐⭐⭐ How do you log out / revoke a JWT?
**Answer:** JWTs can't be "deleted" because the server doesn't store them. Options: short access-token lifetime + **blacklist the refresh token** on logout (simplejwt `token_blacklist` app, `RefreshToken(token).blacklist()`), rotate refresh tokens, or keep a deny-list (e.g. in Redis) of token `jti`s checked on each request. The client also discards its tokens.

---

<a name="q7"></a>
## Q7. ⭐⭐ Where should a frontend store JWTs?
**Answer:** Trade-off: `localStorage` is easy but readable by any injected JavaScript (XSS). An **HttpOnly, Secure, SameSite cookie** can't be read by JS, but then you need CSRF protection. A common approach: access token in memory, refresh token in an HttpOnly cookie.

---

<a name="q8"></a>
## Q8. ⭐⭐ How do you write a custom authentication class?
**Answer:** Subclass `BaseAuthentication`, implement `authenticate(request)`; return `(user, auth)` on success, `None` if this method doesn't apply (so the next class is tried), or raise `AuthenticationFailed` for bad credentials. Implement `authenticate_header()` if you want 401 responses with a `WWW-Authenticate` header.

```python
class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get("X-API-Key")
        if not key:
            return None
        try:
            client = ApiClient.objects.select_related("user").get(key=key, is_active=True)
        except ApiClient.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")
        return (client.user, client)
```

---

<a name="q9"></a>
## Q9. ⭐⭐ Why does my API return 403 instead of 401 for unauthenticated users?
**Answer:** DRF returns **401** only if the first authentication class provides `authenticate_header()` (Token, JWT, Basic do). `SessionAuthentication` doesn't, so with it first in the list unauthenticated requests get **403**. Put the token/JWT class first if clients rely on 401.

---

<a name="q10"></a>
## Q10. ⭐⭐ Why does CSRF fail on my DRF POST with SessionAuthentication?
**Answer:** `SessionAuthentication` enforces Django CSRF for authenticated requests, even though `APIView` is otherwise CSRF-exempt. The client must send the `X-CSRFToken` header (from the `csrftoken` cookie). Token/JWT auth don't need CSRF because the token isn't sent automatically by the browser.

---

<a name="q11"></a>
## Q11. ⭐ How do you integrate OAuth2 / SSO (e.g. Azure AD) with DRF?
**Answer:** The frontend logs in with the identity provider (e.g. MSAL) and sends the provider's access token as `Bearer`. The API validates it — signature using the provider's public keys (JWKS), issuer, audience, expiry — in a custom authentication class (or a library), then maps the token's user/roles to a Django user and groups for permissions. For being an OAuth2 provider yourself, use `django-oauth-toolkit`.
