# 04 — Relations & Nested Serializers
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ How do you represent related objects in a serializer?](#q1)
2. [⭐⭐⭐ What is a nested serializer?](#q2)
3. [⭐⭐⭐ How do you make nested serializers writable?](#q3)
4. [⭐⭐ What does `depth` in `Meta` do and why is it limited?](#q4)
5. [⭐⭐ How do you accept an id on write but return a nested object on read?](#q5)
6. [⭐⭐ How do you handle many-to-many fields in a serializer?](#q6)
7. [⭐ How do you limit the choices of a related field per user?](#q7)
8. [⭐⭐ How do you bulk-create objects through a serializer?](#q8)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ How do you represent related objects in a serializer?
**Answer:** Options:
- `PrimaryKeyRelatedField` — just the id (default in `ModelSerializer`).
- `StringRelatedField` — the object's `__str__` (read-only).
- `SlugRelatedField(slug_field="name")` — a unique field like a name/code.
- `HyperlinkedRelatedField` — a URL.
- A **nested serializer** — the full object.
Writable related fields need a `queryset=` (to look up the object on input).

```python
tags = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Tag.objects.all())
```

---

<a name="q2"></a>
## Q2. ⭐⭐⭐ What is a nested serializer?
**Answer:** Using one serializer as a field of another to return related objects inline.

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text"]

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)   # reverse FK via related_name
    class Meta:
        model = Post
        fields = ["id", "title", "comments"]
```
Remember to `prefetch_related("comments")` in the view, otherwise each post triggers a query.

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ How do you make nested serializers writable?
**Answer:** By default `ModelSerializer` raises an error for writable nested fields ("does not support writable nested fields by default"). You must override `create()` (and `update()`) and save the children yourself, usually inside a transaction.

```python
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "items"]

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        OrderItem.objects.bulk_create([OrderItem(order=order, **i) for i in items])
        return order
```
For `update()`, decide a strategy: replace all children, or match by id and update/create/delete. Libraries like `drf-writable-nested` exist, but explicit code is usually clearer.

---

<a name="q4"></a>
## Q4. ⭐⭐ What does `depth` in `Meta` do and why is it limited?
**Answer:** `depth = 1` automatically nests related objects one level deep without writing nested serializers. It's **read-only**, includes all fields of related models (can expose too much), and causes extra queries. Fine for quick prototypes; explicit nested serializers are better for real APIs.

---

<a name="q5"></a>
## Q5. ⭐⭐ How do you accept an id on write but return a nested object on read?
**Answer:** Common pattern — two fields, one read-only nested and one write-only id:

```python
author = AuthorSerializer(read_only=True)
author_id = serializers.PrimaryKeyRelatedField(source="author", queryset=Author.objects.all(), write_only=True)
```
Alternative: keep the PK field and override `to_representation()` to expand it.

---

<a name="q6"></a>
## Q6. ⭐⭐ How do you handle many-to-many fields in a serializer?
**Answer:** `ModelSerializer` gives `PrimaryKeyRelatedField(many=True)`; the client sends a list of ids, and the default `create`/`update` call `.set()` on the M2M after saving the object. For M2M with a custom `through` model carrying extra fields, write it explicitly (serialize the through model, create through rows in `create()`).

---

<a name="q7"></a>
## Q7. ⭐ How do you limit the choices of a related field per user?
**Answer:** Set the field's queryset dynamically in `__init__` using the request in context:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    user = self.context["request"].user
    self.fields["project"].queryset = Project.objects.filter(members=user)
```
This prevents users from attaching objects they shouldn't access.

---

<a name="q8"></a>
## Q8. ⭐⭐ How do you bulk-create objects through a serializer?
**Answer:** Pass `many=True` with a list. By default that calls `create()` per item. For real bulk inserts, give the serializer a custom `list_serializer_class` whose `create()` uses `bulk_create`.

```python
class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return Book.objects.bulk_create([Book(**item) for item in validated_data])

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "price"]
        list_serializer_class = BookListSerializer
```
Note: `bulk_create` skips `save()` and signals.
