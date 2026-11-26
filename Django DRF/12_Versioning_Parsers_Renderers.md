# 12 — Versioning, Parsers, Renderers & File Upload
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐ How do you version an API in DRF?](#q1)
2. [⭐⭐ When do you need a new API version?](#q2)
3. [⭐⭐ What are parsers and renderers?](#q3)
4. [⭐⭐⭐ How do you handle file uploads in DRF?](#q4)
5. [⭐ How do you return a file download or CSV from a DRF view?](#q5)

---

<a name="q1"></a>
## Q1. ⭐⭐ How do you version an API in DRF?
**Answer:** Set a versioning scheme; DRF then sets `request.version`.
- `URLPathVersioning` — `/api/v1/books/` (most common, explicit).
- `NamespaceVersioning` — via URL namespaces.
- `AcceptHeaderVersioning` — `Accept: application/json; version=1.0`.
- `QueryParameterVersioning` — `?version=1`.
- `HostNameVersioning` — `v1.api.example.com`.

```python
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "ALLOWED_VERSIONS": ["v1", "v2"], "DEFAULT_VERSION": "v1",
}
# path("api/<str:version>/", include(router.urls))

def get_serializer_class(self):
    return BookSerializerV2 if self.request.version == "v2" else BookSerializer
```

---

<a name="q2"></a>
## Q2. ⭐⭐ When do you need a new API version?
**Answer:** Only for **breaking changes** — removing/renaming fields, changing types or meaning, changing required inputs. Adding optional fields or new endpoints is backward compatible and doesn't need a new version. Keep the old version running for a deprecation period and communicate the timeline.

---

<a name="q3"></a>
## Q3. ⭐⭐ What are parsers and renderers?
**Answer:** **Parsers** turn the incoming request body into `request.data` based on `Content-Type` — `JSONParser`, `FormParser`, `MultiPartParser`, `FileUploadParser`. **Renderers** turn `Response` data into the output format based on `Accept` — `JSONRenderer`, `BrowsableAPIRenderer`, plus third-party ones (XML, CSV). Configure globally or per view with `parser_classes` / `renderer_classes`.

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ How do you handle file uploads in DRF?
**Answer:** Send `multipart/form-data`; use a `FileField`/`ImageField` on the model and serializer — DRF's default parsers include `MultiPartParser`.

```python
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "file"]

    def validate_file(self, f):
        if f.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Max 5 MB.")
        return f

class DocumentViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    ...
```
Validate size and type, store files in object storage (S3/Azure Blob) in production, and don't trust the client's filename.

---

<a name="q5"></a>
## Q5. ⭐ How do you return a file download or CSV from a DRF view?
**Answer:** Return a Django `FileResponse`/`HttpResponse` (or `StreamingHttpResponse` for large exports) with `Content-Disposition: attachment`. Alternatively use a CSV renderer. For big exports, generate in a background task and return a download link.
