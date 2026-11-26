# 03 — Serializer Validation
### [← Question Bank](./Question_Bank.md)

## Table of Contents
1. [⭐⭐⭐ What are the ways to validate data in a DRF serializer?](#q1)
2. [⭐⭐ In what order do validations run?](#q2)
3. [⭐⭐⭐ What does `is_valid(raise_exception=True)` do?](#q3)
4. [⭐⭐ What does the error response format look like?](#q4)
5. [⭐⭐ Does `ModelSerializer` call the model's `clean()` / `full_clean()`?](#q5)
6. [⭐⭐ How do you validate uniqueness across fields?](#q6)
7. [⭐⭐ How do you access the request user or instance inside validation?](#q7)
8. [⭐ How do you write a reusable validator?](#q8)
9. [⭐⭐ Where should business validation live — serializer, model, or service layer?](#q9)

---

<a name="q1"></a>
## Q1. ⭐⭐⭐ What are the ways to validate data in a DRF serializer?
**Answer:** Three levels:
1. **Field-level** — `validate_<field_name>(self, value)`, returns the cleaned value.
2. **Object-level** — `validate(self, attrs)`, for rules involving multiple fields; returns `attrs`.
3. **Validators** — reusable functions/classes on a field (`validators=[...]`) or in `Meta.validators` (e.g. `UniqueTogetherValidator`).
Raise `serializers.ValidationError` in all of them.

```python
class BookingSerializer(serializers.ModelSerializer):
    def validate_guests(self, value):
        if value < 1:
            raise serializers.ValidationError("At least 1 guest.")
        return value

    def validate(self, attrs):
        if attrs["check_out"] <= attrs["check_in"]:
            raise serializers.ValidationError("check_out must be after check_in.")
        return attrs
```

---

<a name="q2"></a>
## Q2. ⭐⭐ In what order do validations run?
**Answer:** `is_valid()` → for each field: type conversion + field validators + `validate_<field>()` → then `Meta.validators` (e.g. unique-together) → then `validate()`. If field-level validation fails, `validate()` is not called. All field errors are collected together and returned at once.

---

<a name="q3"></a>
## Q3. ⭐⭐⭐ What does `is_valid(raise_exception=True)` do?
**Answer:** If validation fails it raises `ValidationError`, which DRF's exception handler converts into a **400** response with `serializer.errors`. Without it, you must check the return value and build the 400 response yourself.

---

<a name="q4"></a>
## Q4. ⭐⭐ What does the error response format look like?
**Answer:** A dict of field → list of messages; object-level errors go under `non_field_errors`.

```json
{"email": ["This field is required."], "non_field_errors": ["check_out must be after check_in."]}
```
To attach an object-level error to a specific field: `raise serializers.ValidationError({"check_out": "Must be after check_in."})`.

---

<a name="q5"></a>
## Q5. ⭐⭐ Does `ModelSerializer` call the model's `clean()` / `full_clean()`?
**Answer:** **No.** DRF validation is separate from Django model validation. Field constraints (max_length, choices, unique) are mapped to serializer validators, but custom logic in `Model.clean()` is not run. Either duplicate the rule in the serializer or call `full_clean()` yourself (e.g. in `validate()` on a temporary instance) — or put shared rules in a service/validator function used by both.

---

<a name="q6"></a>
## Q6. ⭐⭐ How do you validate uniqueness across fields?
**Answer:** Use `UniqueTogetherValidator` (auto-added by `ModelSerializer` for `unique_together` / `UniqueConstraint` on fields), or add it explicitly. Also keep the DB constraint — serializer checks alone can still race under concurrent requests.

```python
class Meta:
    model = Membership
    fields = ["user", "team"]
    validators = [UniqueTogetherValidator(queryset=Membership.objects.all(), fields=["user", "team"])]
```

---

<a name="q7"></a>
## Q7. ⭐⭐ How do you access the request user or instance inside validation?
**Answer:** `self.context["request"].user` for the user; `self.instance` is the object being updated (None on create) — useful for rules like "can't change status from closed".

---

<a name="q8"></a>
## Q8. ⭐ How do you write a reusable validator?
**Answer:** A function (or class with `__call__`) that raises `ValidationError`, attached via `validators=[...]`.

```python
def no_profanity(value):
    if "badword" in value.lower():
        raise serializers.ValidationError("Not allowed.")

title = serializers.CharField(validators=[no_profanity])
```

---

<a name="q9"></a>
## Q9. ⭐⭐ Where should business validation live — serializer, model, or service layer?
**Answer:** Input/format rules (required, types, ranges) → serializer. Data-integrity rules → DB constraints (unique, check). Complex business rules used by APIs, admin and jobs → a service/domain function, called from the serializer or view, so the rule isn't duplicated. Keep serializers thin.
