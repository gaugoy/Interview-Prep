# 02 — Serializers
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What is a serializer in DRF?](#q1)
2. [⭐⭐⭐ Difference between `Serializer` and `ModelSerializer`?](#q2)
3. [⭐⭐⭐ How does `serializer.save()` decide between `create()` and `update()`?](#q3)
4. [⭐⭐⭐ What is the difference between `serializer.data`, `validated_data` and `initial_data`?](#q4)
5. [⭐⭐⭐ What are `read_only`, `write_only`, `required`, `allow_null` and `default`?](#q5)
6. [⭐⭐⭐ What is `SerializerMethodField`?](#q6)
7. [⭐⭐ What does the `source` argument do?](#q7)
8. [⭐⭐ How do you serialize multiple objects? What is `many=True`?](#q8)
9. [⭐⭐ What is serializer `context` and how do you access the request in a serializer?](#q9)
10. [⭐⭐ What are `to_representation()` and `to_internal_value()`?](#q10)
11. [⭐⭐ How do you automatically set the logged-in user on an object?](#q11)
12. [⭐⭐ How do you use different serializers for read and write (or list vs detail)?](#q12)
13. [⭐ What is `HyperlinkedModelSerializer`?](#q13)
14. [⭐⭐ How do you make a field conditionally included, e.g. only for admins?](#q14)
15. [⭐ What is a custom serializer field?](#q15)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What is a serializer in DRF?
**Answer:** A serializer converts complex data (model instances, querysets) into Python primitives that can be rendered to JSON — **serialization** — and converts incoming JSON back into validated Python data / model instances — **deserialization + validation**. It's similar to a Django Form, but for APIs.

```python
serializer = BookSerializer(book)            # out: serializer.data
serializer = BookSerializer(data=request.data)  # in
serializer.is_valid(raise_exception=True)
serializer.save()
```

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ Difference between `Serializer` and `ModelSerializer`?
**Answer:** `Serializer` — you declare every field and write `create()`/`update()` yourself. Use it for non-model data (login payload, report filters) or full control.
`ModelSerializer` — generates fields from the model, adds model validators (e.g. unique), and provides default `create()`/`update()`.

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "price"]
        read_only_fields = ["id"]
```

**Follow-up:** Avoid `fields = "__all__"` in real APIs — new model fields get exposed automatically.

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ How does `serializer.save()` decide between `create()` and `update()`?
**Answer:** If the serializer was created with an instance (`Serializer(instance, data=...)`), `save()` calls `update(instance, validated_data)`; otherwise it calls `create(validated_data)`. Extra keyword args to `save()` are merged into `validated_data` — the standard way to set fields not sent by the client:

```python
serializer.save(owner=request.user)
```

---

<a name="q4"></a>
## Q4. ⭐⭐⭐ What is the difference between `serializer.data`, `validated_data` and `initial_data`?
**Answer:**
- `initial_data` — raw input passed as `data=`.
- `validated_data` — cleaned input, available after `is_valid()`; used in `create`/`update`.
- `data` — the output representation (after save, or of the instance).
Accessing `.data` before calling `is_valid()` on input data raises an error.

---

<a name="q5"></a>
## Q5. ⭐⭐⭐ What are `read_only`, `write_only`, `required`, `allow_null` and `default`?
**Answer:**
- `read_only=True` — included in output, ignored in input (e.g. `id`, `created_at`).
- `write_only=True` — accepted in input, never returned (e.g. `password`).
- `required=False` — field can be omitted.
- `allow_null=True` — `null` is accepted; `allow_blank=True` — empty string accepted (CharField).
- `default=` — value used when missing (implies not required).

```python
class Meta:
    model = User
    fields = ["id", "username", "password"]
    extra_kwargs = {"password": {"write_only": True}}
```

---

<a name="q6"></a>
## Q6. ⭐⭐⭐ What is `SerializerMethodField`?
**Answer:** A read-only field whose value comes from a method `get_<field_name>(self, obj)`. Good for computed values. Downside: it can't be written, and if it queries the DB it causes N+1 queries in list views — prefer annotations in the queryset for counts.

```python
class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    def get_book_count(self, obj):
        return obj.books.count()      # 1 query per row → better: annotate in the view
```

---

<a name="q7"></a>
## Q7. ⭐⭐ What does the `source` argument do?
**Answer:** Maps a serializer field to a different attribute, a related field, or a method on the model.

```python
author_name = serializers.CharField(source="author.name", read_only=True)
full_name = serializers.CharField(source="get_full_name", read_only=True)
```
`source="*"` passes the whole object to the field (used for custom fields).

---

<a name="q8"></a>
## Q8. ⭐⭐ How do you serialize multiple objects? What is `many=True`?
**Answer:** `BookSerializer(queryset, many=True)` — DRF wraps the serializer in a `ListSerializer` that serializes each item. For input, `many=True` with a list of dicts validates each item and `save()` calls `create()` per item (one INSERT each) unless you customise `ListSerializer.create()` to use `bulk_create`.

---

<a name="q9"></a>
## Q9. ⭐⭐ What is serializer `context` and how do you access the request in a serializer?
**Answer:** `context` is a dict passed to the serializer for extra info. Generic views/ViewSets automatically pass `request`, `view` and `format` (via `get_serializer_context()`), so you use `self.context["request"]`. If you create a serializer manually, pass it yourself:

```python
serializer = BookSerializer(book, context={"request": request})
```
Needed for things like `HyperlinkedModelSerializer` (absolute URLs) and `CurrentUserDefault`.

---

<a name="q10"></a>
## Q10. ⭐⭐ What are `to_representation()` and `to_internal_value()`?
**Answer:** `to_representation(instance)` controls **output** — override to rename, hide or add keys. `to_internal_value(data)` controls **input parsing** before validation. Overriding `to_representation` is common, e.g. to show a nested object on read while accepting an id on write.

```python
def to_representation(self, instance):
    data = super().to_representation(instance)
    data["author"] = AuthorSerializer(instance.author).data
    return data
```

---

<a name="q11"></a>
## Q11. ⭐⭐ How do you automatically set the logged-in user on an object?
**Answer:** Two common ways:
1. In the view: `def perform_create(self, serializer): serializer.save(owner=self.request.user)`.
2. In the serializer: a hidden field.
```python
owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
```
Never trust an `owner` id sent by the client.

---

<a name="q12"></a>
## Q12. ⭐⭐ How do you use different serializers for read and write (or list vs detail)?
**Answer:** Override `get_serializer_class()` in the view.

```python
def get_serializer_class(self):
    if self.action == "list":
        return BookListSerializer       # few fields
    if self.action in ("create", "update", "partial_update"):
        return BookWriteSerializer
    return BookDetailSerializer
```

---

<a name="q13"></a>
## Q13. ⭐ What is `HyperlinkedModelSerializer`?
**Answer:** Like `ModelSerializer` but represents relations as URLs instead of primary keys, and includes a `url` field for the object itself. It needs `request` in the context and correctly named routes (`<model>-detail`).

---

<a name="q14"></a>
## Q14. ⭐⭐ How do you make a field conditionally included, e.g. only for admins?
**Answer:** Pop it in `__init__` or `to_representation` based on `self.context["request"].user`.

```python
def to_representation(self, instance):
    data = super().to_representation(instance)
    if not self.context["request"].user.is_staff:
        data.pop("internal_notes", None)
    return data
```

---

<a name="q15"></a>
## Q15. ⭐ What is a custom serializer field?
**Answer:** Subclass `serializers.Field` and implement `to_representation(value)` and `to_internal_value(data)` — for formats DRF doesn't provide (e.g. a "lat,lng" string ↔ Point, or encrypted values).
