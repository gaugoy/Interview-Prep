# Django DRF — Question Bank (questions only)

Quick revision list of every DRF question, section by section. Click a question to jump to its answer.

⭐⭐⭐ = asked in almost every interview · ⭐⭐ = common · ⭐ = occasional

**Total: 131 questions across 16 sections.**

## [01 — DRF Basics & Request/Response](./01_DRF_Basics.md) — 13 Q

1. ⭐⭐⭐ [What is Django REST Framework and why use it over plain Django views?](./01_DRF_Basics.md#q1)
2. ⭐⭐⭐ [What are the core components of DRF?](./01_DRF_Basics.md#q2)
3. ⭐⭐ [What is the request lifecycle of a DRF API call?](./01_DRF_Basics.md#q3)
4. ⭐⭐⭐ [Difference between DRF `Request` and Django `HttpRequest`?](./01_DRF_Basics.md#q4)
5. ⭐⭐ [Difference between DRF `Response` and Django `HttpResponse`/`JsonResponse`?](./01_DRF_Basics.md#q5)
6. ⭐⭐ [What is content negotiation in DRF?](./01_DRF_Basics.md#q6)
7. ⭐⭐ [What is the browsable API and should it be enabled in production?](./01_DRF_Basics.md#q7)
8. ⭐⭐⭐ [Which HTTP methods and status codes do you use for CRUD in a REST API?](./01_DRF_Basics.md#q8)
9. ⭐⭐⭐ [Difference between PUT and PATCH?](./01_DRF_Basics.md#q9)
10. ⭐⭐ [What makes an API "RESTful"? What does idempotent mean?](./01_DRF_Basics.md#q10)
11. ⭐⭐ [Where do you configure DRF globally? Name common settings.](./01_DRF_Basics.md#q11)
12. ⭐ [Does DRF support async views?](./01_DRF_Basics.md#q12)
13. ⭐⭐ [How do you document a DRF API (OpenAPI/Swagger)?](./01_DRF_Basics.md#q13)

---

## [02 — Serializers](./02_Serializers.md) — 15 Q

1. ⭐⭐⭐ [What is a serializer in DRF?](./02_Serializers.md#q1)
2. ⭐⭐⭐ [Difference between `Serializer` and `ModelSerializer`?](./02_Serializers.md#q2)
3. ⭐⭐⭐ [How does `serializer.save()` decide between `create()` and `update()`?](./02_Serializers.md#q3)
4. ⭐⭐⭐ [What is the difference between `serializer.data`, `validated_data` and `initial_data`?](./02_Serializers.md#q4)
5. ⭐⭐⭐ [What are `read_only`, `write_only`, `required`, `allow_null` and `default`?](./02_Serializers.md#q5)
6. ⭐⭐⭐ [What is `SerializerMethodField`?](./02_Serializers.md#q6)
7. ⭐⭐ [What does the `source` argument do?](./02_Serializers.md#q7)
8. ⭐⭐ [How do you serialize multiple objects? What is `many=True`?](./02_Serializers.md#q8)
9. ⭐⭐ [What is serializer `context` and how do you access the request in a serializer?](./02_Serializers.md#q9)
10. ⭐⭐ [What are `to_representation()` and `to_internal_value()`?](./02_Serializers.md#q10)
11. ⭐⭐ [How do you automatically set the logged-in user on an object?](./02_Serializers.md#q11)
12. ⭐⭐ [How do you use different serializers for read and write (or list vs detail)?](./02_Serializers.md#q12)
13. ⭐ [What is `HyperlinkedModelSerializer`?](./02_Serializers.md#q13)
14. ⭐⭐ [How do you make a field conditionally included, e.g. only for admins?](./02_Serializers.md#q14)
15. ⭐ [What is a custom serializer field?](./02_Serializers.md#q15)

---

## [03 — Serializer Validation](./03_Validation.md) — 9 Q

1. ⭐⭐⭐ [What are the ways to validate data in a DRF serializer?](./03_Validation.md#q1)
2. ⭐⭐ [In what order do validations run?](./03_Validation.md#q2)
3. ⭐⭐⭐ [What does `is_valid(raise_exception=True)` do?](./03_Validation.md#q3)
4. ⭐⭐ [What does the error response format look like?](./03_Validation.md#q4)
5. ⭐⭐ [Does `ModelSerializer` call the model's `clean()` / `full_clean()`?](./03_Validation.md#q5)
6. ⭐⭐ [How do you validate uniqueness across fields?](./03_Validation.md#q6)
7. ⭐⭐ [How do you access the request user or instance inside validation?](./03_Validation.md#q7)
8. ⭐ [How do you write a reusable validator?](./03_Validation.md#q8)
9. ⭐⭐ [Where should business validation live — serializer, model, or service layer?](./03_Validation.md#q9)

---

## [04 — Relations & Nested Serializers](./04_Relations_and_Nested_Serializers.md) — 8 Q

1. ⭐⭐⭐ [How do you represent related objects in a serializer?](./04_Relations_and_Nested_Serializers.md#q1)
2. ⭐⭐⭐ [What is a nested serializer?](./04_Relations_and_Nested_Serializers.md#q2)
3. ⭐⭐⭐ [How do you make nested serializers writable?](./04_Relations_and_Nested_Serializers.md#q3)
4. ⭐⭐ [What does `depth` in `Meta` do and why is it limited?](./04_Relations_and_Nested_Serializers.md#q4)
5. ⭐⭐ [How do you accept an id on write but return a nested object on read?](./04_Relations_and_Nested_Serializers.md#q5)
6. ⭐⭐ [How do you handle many-to-many fields in a serializer?](./04_Relations_and_Nested_Serializers.md#q6)
7. ⭐ [How do you limit the choices of a related field per user?](./04_Relations_and_Nested_Serializers.md#q7)
8. ⭐⭐ [How do you bulk-create objects through a serializer?](./04_Relations_and_Nested_Serializers.md#q8)

---

## [05 — Views, Generic Views & ViewSets](./05_Views_and_ViewSets.md) — 12 Q

1. ⭐⭐⭐ [What are the different ways to write views in DRF?](./05_Views_and_ViewSets.md#q1)
2. ⭐⭐⭐ [Difference between `APIView`, `GenericAPIView` and `ViewSet`?](./05_Views_and_ViewSets.md#q2)
3. ⭐⭐ [What's the difference between `ModelViewSet`, `ReadOnlyModelViewSet` and `ViewSet`?](./05_Views_and_ViewSets.md#q3)
4. ⭐⭐⭐ [`queryset` attribute vs `get_queryset()` — when do you override `get_queryset()`?](./05_Views_and_ViewSets.md#q4)
5. ⭐⭐⭐ [What are `perform_create`, `perform_update`, `perform_destroy` used for?](./05_Views_and_ViewSets.md#q5)
6. ⭐⭐⭐ [How do you add a custom endpoint to a ViewSet?](./05_Views_and_ViewSets.md#q6)
7. ⭐⭐ [What does `get_object()` do?](./05_Views_and_ViewSets.md#q7)
8. ⭐⭐ [How do you look up objects by slug/uuid instead of id?](./05_Views_and_ViewSets.md#q8)
9. ⭐⭐ [How do you apply different permissions/serializers per action in a ViewSet?](./05_Views_and_ViewSets.md#q9)
10. ⭐ [What are the concrete generic views?](./05_Views_and_ViewSets.md#q10)
11. ⭐⭐ [Function-based `@api_view` vs class-based views — when would you use FBV?](./05_Views_and_ViewSets.md#q11)
12. ⭐ [How do you return a custom response from `create()` (e.g. different status or extra data)?](./05_Views_and_ViewSets.md#q12)

---

## [06 — Routers & URLs](./06_Routers_and_URLs.md) — 5 Q

1. ⭐⭐⭐ [What are routers in DRF?](./06_Routers_and_URLs.md#q1)
2. ⭐⭐ [`SimpleRouter` vs `DefaultRouter`?](./06_Routers_and_URLs.md#q2)
3. ⭐⭐ [What is `basename` and when is it required?](./06_Routers_and_URLs.md#q3)
4. ⭐ [How do you create nested routes like `/projects/{id}/tasks/`?](./06_Routers_and_URLs.md#q4)
5. ⭐ [How do you reverse a DRF URL?](./06_Routers_and_URLs.md#q5)

---

## [07 — Authentication (Session, Token, JWT, OAuth2)](./07_Authentication.md) — 11 Q

1. ⭐⭐⭐ [Authentication vs authorization (permissions) in DRF?](./07_Authentication.md#q1)
2. ⭐⭐⭐ [What authentication classes does DRF provide?](./07_Authentication.md#q2)
3. ⭐⭐⭐ [What is JWT and how does it work?](./07_Authentication.md#q3)
4. ⭐⭐⭐ [How do you set up JWT in DRF?](./07_Authentication.md#q4)
5. ⭐⭐⭐ [Token auth vs JWT vs Session — which would you choose?](./07_Authentication.md#q5)
6. ⭐⭐⭐ [How do you log out / revoke a JWT?](./07_Authentication.md#q6)
7. ⭐⭐ [Where should a frontend store JWTs?](./07_Authentication.md#q7)
8. ⭐⭐ [How do you write a custom authentication class?](./07_Authentication.md#q8)
9. ⭐⭐ [Why does my API return 403 instead of 401 for unauthenticated users?](./07_Authentication.md#q9)
10. ⭐⭐ [Why does CSRF fail on my DRF POST with SessionAuthentication?](./07_Authentication.md#q10)
11. ⭐ [How do you integrate OAuth2 / SSO (e.g. Azure AD) with DRF?](./07_Authentication.md#q11)

---

## [08 — Permissions](./08_Permissions.md) — 8 Q

1. ⭐⭐⭐ [What are permission classes in DRF? Name the built-in ones.](./08_Permissions.md#q1)
2. ⭐⭐⭐ [`has_permission` vs `has_object_permission`?](./08_Permissions.md#q2)
3. ⭐⭐⭐ [Write a custom permission: only the owner can edit, others can read.](./08_Permissions.md#q3)
4. ⭐⭐ [How do you combine permissions with OR / NOT?](./08_Permissions.md#q4)
5. ⭐⭐ [How do you implement role-based access control (RBAC) in DRF?](./08_Permissions.md#q5)
6. ⭐⭐ [What status code is returned when a permission fails?](./08_Permissions.md#q6)
7. ⭐ [How does `DjangoModelPermissions` work?](./08_Permissions.md#q7)
8. ⭐⭐ [Should I hide unauthorized objects with 403 or 404?](./08_Permissions.md#q8)

---

## [09 — Throttling (Rate Limiting)](./09_Throttling.md) — 4 Q

1. ⭐⭐⭐ [What is throttling in DRF and which classes exist?](./09_Throttling.md#q1)
2. ⭐⭐ [How does DRF store throttle state? What can go wrong?](./09_Throttling.md#q2)
3. ⭐⭐ [Throttling vs permissions — is throttling a security feature?](./09_Throttling.md#q3)
4. ⭐ [How do you write a custom throttle?](./09_Throttling.md#q4)

---

## [10 — Pagination](./10_Pagination.md) — 5 Q

1. ⭐⭐⭐ [What pagination styles does DRF provide?](./10_Pagination.md#q1)
2. ⭐⭐ [How do you customise page size or let the client choose it?](./10_Pagination.md#q2)
3. ⭐⭐ [Why is offset/page-number pagination slow on large tables, and what's the fix?](./10_Pagination.md#q3)
4. ⭐ [How do you change the paginated response format?](./10_Pagination.md#q4)
5. ⭐ [How do you paginate in an `APIView` (not a generic view)?](./10_Pagination.md#q5)

---

## [11 — Filtering, Searching & Ordering](./11_Filtering_Search_Ordering.md) — 5 Q

1. ⭐⭐⭐ [How do you filter results in a DRF API?](./11_Filtering_Search_Ordering.md#q1)
2. ⭐⭐ [When do you write a custom `FilterSet`?](./11_Filtering_Search_Ordering.md#q2)
3. ⭐⭐ [How does `SearchFilter` work and what are its limits?](./11_Filtering_Search_Ordering.md#q3)
4. ⭐⭐ [Why should you restrict `ordering_fields`?](./11_Filtering_Search_Ordering.md#q4)
5. ⭐ [Are filters applied before or after permissions/pagination?](./11_Filtering_Search_Ordering.md#q5)

---

## [12 — Versioning, Parsers, Renderers & File Upload](./12_Versioning_Parsers_Renderers.md) — 5 Q

1. ⭐⭐ [How do you version an API in DRF?](./12_Versioning_Parsers_Renderers.md#q1)
2. ⭐⭐ [When do you need a new API version?](./12_Versioning_Parsers_Renderers.md#q2)
3. ⭐⭐ [What are parsers and renderers?](./12_Versioning_Parsers_Renderers.md#q3)
4. ⭐⭐⭐ [How do you handle file uploads in DRF?](./12_Versioning_Parsers_Renderers.md#q4)
5. ⭐ [How do you return a file download or CSV from a DRF view?](./12_Versioning_Parsers_Renderers.md#q5)

---

## [13 — Exception Handling & Error Responses](./13_Exception_Handling.md) — 5 Q

1. ⭐⭐⭐ [How does DRF handle exceptions?](./13_Exception_Handling.md#q1)
2. ⭐⭐⭐ [How do you return a consistent error format across the API?](./13_Exception_Handling.md#q2)
3. ⭐⭐ [How do you create a custom API exception?](./13_Exception_Handling.md#q3)
4. ⭐⭐ [How do you handle unexpected errors (500) in production?](./13_Exception_Handling.md#q4)
5. ⭐ [What does `get_object_or_404` do in DRF?](./13_Exception_Handling.md#q5)

---

## [14 — Testing DRF APIs](./14_Testing.md) — 5 Q

1. ⭐⭐⭐ [How do you test DRF APIs?](./14_Testing.md#q1)
2. ⭐⭐ [`APIClient` vs `APIRequestFactory`?](./14_Testing.md#q2)
3. ⭐⭐ [How do you authenticate in tests?](./14_Testing.md#q3)
4. ⭐⭐ [What should you test in an API?](./14_Testing.md#q4)
5. ⭐ [How do you mock external services in API tests?](./14_Testing.md#q5)

---

## [15 — Performance & Caching](./15_Performance_and_Caching.md) — 6 Q

1. ⭐⭐⭐ [What is the N+1 problem in DRF and how do you fix it?](./15_Performance_and_Caching.md#q1)
2. ⭐⭐ [How do you make a slow list endpoint faster?](./15_Performance_and_Caching.md#q2)
3. ⭐⭐ [How do you cache API responses in DRF?](./15_Performance_and_Caching.md#q3)
4. ⭐⭐ [How do you invalidate cached API data when it changes?](./15_Performance_and_Caching.md#q4)
5. ⭐ [Are DRF serializers slow? What can you do?](./15_Performance_and_Caching.md#q5)
6. ⭐⭐ [How do you handle long-running work triggered by an API call?](./15_Performance_and_Caching.md#q6)

---

## [16 — Scenario-Based & Common Production Issues](./16_Scenario_Based_and_Production_Issues.md) — 15 Q

1. ⭐⭐⭐ [An endpoint is slow in production but fast locally. How do you debug it?](./16_Scenario_Based_and_Production_Issues.md#q1)
2. ⭐⭐⭐ [Users can see or edit other users' data. What went wrong and how do you fix it?](./16_Scenario_Based_and_Production_Issues.md#q2)
3. ⭐⭐⭐ [The frontend gets CORS errors calling the API. How do you fix it?](./16_Scenario_Based_and_Production_Issues.md#q3)
4. ⭐⭐⭐ [`request.user` is `AnonymousUser` even though the client sends a token. Why?](./16_Scenario_Based_and_Production_Issues.md#q4)
5. ⭐⭐⭐ [A client retries a POST and duplicate orders get created. How do you prevent it?](./16_Scenario_Based_and_Production_Issues.md#q5)
6. ⭐⭐ [Two users update the same record at the same time and one change is lost. What do you do?](./16_Scenario_Based_and_Production_Issues.md#q6)
7. ⭐⭐ [A serializer field isn't being saved. What do you check?](./16_Scenario_Based_and_Production_Issues.md#q7)
8. ⭐⭐ [How do you implement soft delete in a DRF API?](./16_Scenario_Based_and_Production_Issues.md#q8)
9. ⭐⭐ [The API returns stale data after an update. Possible causes?](./16_Scenario_Based_and_Production_Issues.md#q9)
10. ⭐⭐ [How do you design an endpoint that calls a slow or unreliable third-party API?](./16_Scenario_Based_and_Production_Issues.md#q10)
11. ⭐⭐ [How do you handle timezones in API responses?](./16_Scenario_Based_and_Production_Issues.md#q11)
12. ⭐⭐ [How do you secure a DRF API in production? (checklist)](./16_Scenario_Based_and_Production_Issues.md#q12)
13. ⭐⭐ [How would you implement a multi-tenant API?](./16_Scenario_Based_and_Production_Issues.md#q13)
14. ⭐ [How do you build a webhook receiver endpoint in DRF?](./16_Scenario_Based_and_Production_Issues.md#q14)
15. ⭐ [An endpoint returns 500 only for some records. How do you approach it?](./16_Scenario_Based_and_Production_Issues.md#q15)
