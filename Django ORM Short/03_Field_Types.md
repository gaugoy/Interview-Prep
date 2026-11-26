# Module 03: Field Types & Validation (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/03_Field_Types.md)

## Table of Contents
1. (Medium) [How does Django 5.0's GeneratedField work and how is it defined?](#q1)
2. (Easy) [What is the difference between blank=True and null=True at the database and form level?](#q2)
3. (Hard) [How do you implement and validate custom Field subclasses in Django?](#q3)
4. (Easy) [What is the performance and storage difference between CharField and TextField?](#q4)
5. (Easy) [How does DecimalField avoid floating-point errors in the database?](#q5)
6. (Easy) [What are the database representation differences between FloatField and DecimalField?](#q6)
7. (Medium) [How does Django handle JSONField querying and indexing?](#q7)
8. (Medium) [What is the storage implication of UUIDField versus AutoField for primary keys?](#q8)
9. (Easy) [How do you handle binary data storage in Django using BinaryField?](#q9)
10. (Easy) [What are the database implications of using FileField and ImageField?](#q10)
11. (Easy) [How does Django handle timezone-aware DateTimeFields under the hood?](#q11)
12. (Easy) [What is the impact of auto_now and auto_now_add on model updates?](#q12)
13. (Easy) [How do you use IPAddressField and what database validation does it provide?](#q13)
14. (Medium) [How does Django validate constraints before writing fields to the database?](#q14)
15. (Easy) [Explain the usage and database mapping of PositiveIntegerField and PositiveSmallIntegerField.](#q15)
16. (Easy) [What is DurationField and how is it stored in different databases?](#q16)
17. (Easy) [What is the difference between EmailField and CharField?](#q17)
18. (Easy) [How does Django handle ChoiceField choices at the database level?](#q18)
19. (Medium) [How do you define lazy/dynamic choices for a field?](#q19)
20. (Easy) [What is SlugField and how does it relate to indexing and URLs?](#q20)
21. (Medium) [How does Django 5.0's db_default handle complex database-level defaults?](#q21)
22. (Easy) [How do you write a custom validator for a model field?](#q22)
23. (Easy) [What are the risks of using FloatField for monetary calculations?](#q23)
24. (Medium) [How does Django map ArrayField in PostgreSQL database backend?](#q24)
25. (Hard) [How do custom database representation conversion methods work (to_python, get_prep_value, from_db_value)?](#q25)
26. (Hard) [How does JSONField index compilation happen in Postgres?](#q26)
27. (Easy) [What is the purpose of FileField storage parameter?](#q27)
28. (Medium) [How does Django convert dates dynamically to timezone offsets?](#q28)
29. (Medium) [How do you validate uniqueness of a combination of fields in model clean?](#q29)
30. (Easy) [What is the default db column name compilation strategy?](#q30)
31. (Hard) [How do you implement field encryption transparently in Django models?](#q31)
32. (Easy) [Explain the database storage size difference between SmallIntegerField and BigIntegerField.](#q32)
33. (Easy) [How does Django handle choices validation in forms vs models?](#q33)
34. (Medium) [What is the impact of changing a CharField max_length on indexing?](#q34)
35. (Medium) [How does Django 5.0 compile GeneratedField on SQLite backend?](#q35)

---

<a name="q1"></a>
## Q1. (Medium) How does Django 5.0's GeneratedField work and how is it defined?
**Answer:** A column whose value the **database** computes from other columns in the same row. You give an expression, an `output_field` and `db_persist` (`True` = stored, `False` = virtual, computed on read).

```python
class Item(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    total = models.GeneratedField(expression=F("price") * F("qty"),
                                  output_field=models.DecimalField(max_digits=12, decimal_places=2),
                                  db_persist=True)
```
Read-only in Django; call `refresh_from_db()` after save to see the new value.

---

<a name="q2"></a>
## Q2. (Easy) What is the difference between blank=True and null=True at the database and form level?
**Answer:** `null=True` → the **database** column allows NULL. `blank=True` → **validation/forms** allow an empty value. For text fields use `blank=True` only (store empty string, avoid two "empty" values); for numbers/dates/FKs that can be empty, use both.

---

<a name="q3"></a>
## Q3. (Hard) How do you implement and validate custom Field subclasses in Django?
**Answer:** Subclass an existing field (or `Field`) and implement the conversions: `from_db_value()` (DB → Python), `to_python()` (forms/deserialization → Python), `get_prep_value()` (Python → DB), and `deconstruct()` if you add constructor arguments (needed for migrations). Validate with `validators` or by overriding `validate()`.

```python
class LowercaseEmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.lower() if value else value
```

---

<a name="q4"></a>
## Q4. (Easy) What is the performance and storage difference between CharField and TextField?
**Answer:** `CharField` needs `max_length` → `varchar(n)`; `TextField` → unlimited `text`. In PostgreSQL both are stored the same way and perform the same; the difference is validation (length limit) and forms (input vs textarea). In MySQL, `TEXT` columns have limits for indexing and may be stored off-page. Use CharField for short, bounded values you filter on.

---

<a name="q5"></a>
## Q5. (Easy) How does DecimalField avoid floating-point errors in the database?
**Answer:** It maps to a fixed-point `numeric(max_digits, decimal_places)` column and to Python's `Decimal`, which store exact decimal values — `0.1 + 0.2` is exactly `0.3`. Floats are binary approximations. Always use `DecimalField` for money.

---

<a name="q6"></a>
## Q6. (Easy) What are the database representation differences between FloatField and DecimalField?
**Answer:** `FloatField` → `double precision` (8-byte binary float, approximate, fast). `DecimalField` → `numeric(p, s)` (exact, fixed number of decimal places, a bit slower, variable size). Float for measurements/science; Decimal for money and anything that must add up exactly.

---

<a name="q7"></a>
## Q7. (Medium) How does Django handle JSONField querying and indexing?
**Answer:** Query into keys with `__`: `filter(data__owner__name="Ann")`, `data__has_key="x"`, `data__contains={"k": 1}`. On PostgreSQL it's `jsonb`; index containment queries with a `GinIndex(fields=["data"])`, and a specific key with an expression index.

```python
class Meta:
    indexes = [GinIndex(fields=["data"], name="event_data_gin")]
```

---

<a name="q8"></a>
## Q8. (Medium) What is the storage implication of UUIDField versus AutoField for primary keys?
**Answer:** `AutoField`/`BigAutoField` = 4/8 bytes, sequential — compact, index-friendly. `UUIDField` = 16 bytes on PostgreSQL (`uuid`), 32-char string on MySQL. Random UUIDv4 values insert all over the index → bigger, fragmented indexes and slower inserts at scale. UUIDs are good for public/unguessable ids or distributed generation; a common compromise is integer pk + a separate UUID column.

---

<a name="q9"></a>
## Q9. (Easy) How do you handle binary data storage in Django using BinaryField?
**Answer:** `BinaryField` stores raw bytes (`bytea` on PostgreSQL); it's not editable in forms by default. Fine for small blobs (hashes, small encrypted values). For files/images, store them in file/object storage and keep only the path (`FileField`) — large blobs bloat the DB and backups.

---

<a name="q10"></a>
## Q10. (Easy) What are the database implications of using FileField and ImageField?
**Answer:** The database stores only a **path string** (`varchar(100)` by default); the file lives in the configured storage (disk, S3, Azure Blob). Deleting a row does **not** delete the file — clean up yourself. `ImageField` adds image validation (Pillow) and optional width/height fields.

---

<a name="q11"></a>
## Q11. (Easy) How does Django handle timezone-aware DateTimeFields under the hood?
**Answer:** With `USE_TZ = True` (default), Django stores datetimes in **UTC** (PostgreSQL `timestamptz`) and returns aware datetimes in UTC. Conversion to the user's timezone happens in templates/forms (`TIME_ZONE` / `timezone.activate()`). Always use `timezone.now()`, not `datetime.now()`.

---

<a name="q12"></a>
## Q12. (Easy) What is the impact of auto_now and auto_now_add on model updates?
**Answer:** `auto_now_add=True` sets the value once on create; `auto_now=True` sets it on **every `save()`**. Both make the field non-editable. Gotcha: `queryset.update()` and `bulk_update()` don't touch `auto_now` fields — set them explicitly.

---

<a name="q13"></a>
## Q13. (Easy) How do you use IPAddressField and what database validation does it provide?
**Answer:** `IPAddressField` was removed; use `GenericIPAddressField(protocol="both" | "IPv4" | "IPv6", unpack_ipv4=False)`. It validates the format and normalizes IPv6. On PostgreSQL it's stored as `inet` (database-validated); elsewhere as `char(39)`.

---

<a name="q14"></a>
## Q14. (Medium) How does Django validate constraints before writing fields to the database?
**Answer:** Only if you call `full_clean()` (ModelForms do): it checks field validators, `clean()`, unique fields and (since 4.1) `Meta.constraints` via `validate_constraints()`. `save()` itself doesn't validate — the database enforces NOT NULL, unique, FK and check constraints and raises `IntegrityError`.

---

<a name="q15"></a>
## Q15. (Easy) Explain the usage and database mapping of PositiveIntegerField and PositiveSmallIntegerField.
**Answer:** Integers that can't be negative. PostgreSQL: `integer`/`smallint` with a `CHECK (col >= 0)`; MySQL: `UNSIGNED` columns. `PositiveSmallIntegerField` holds 0–32767 (2 bytes) — good for ages, counts, ratings; `PositiveIntegerField` 0–2,147,483,647.

---

<a name="q16"></a>
## Q16. (Easy) What is DurationField and how is it stored in different databases?
**Answer:** Stores a `timedelta`. PostgreSQL uses `interval`; other databases store it as a `bigint` of microseconds. You can do arithmetic with it in queries (`F("end") - F("start")` produces durations).

---

<a name="q17"></a>
## Q17. (Easy) What is the difference between EmailField and CharField?
**Answer:** `EmailField` is a `CharField` (default `max_length=254`) with an `EmailValidator` — same DB column (`varchar`). Validation runs in forms/`full_clean()`, not on `save()`. It doesn't lowercase or check uniqueness — add those yourself.

---

<a name="q18"></a>
## Q18. (Easy) How does Django handle ChoiceField choices at the database level?
**Answer:** Only the value is stored in a normal column; the database knows nothing about the choices (no constraint). Choices are enforced in forms/`full_clean()`. For a DB guarantee add a `CheckConstraint(condition=Q(status__in=[...]))`. Use `models.TextChoices` for readable choices.

```python
class Status(models.TextChoices):
    NEW = "new", "New"
    DONE = "done", "Done"
status = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW)
```

---

<a name="q19"></a>
## Q19. (Medium) How do you define lazy/dynamic choices for a field?
**Answer:** Since Django 5.0, `choices` can be a **callable**, evaluated when needed (and not baked into migrations). For choices that come from database data, a ForeignKey is usually the better design.

```python
def currency_choices():
    return [(c, c) for c in settings.CURRENCIES]
currency = models.CharField(max_length=3, choices=currency_choices)
```

---

<a name="q20"></a>
## Q20. (Easy) What is SlugField and how does it relate to indexing and URLs?
**Answer:** A `CharField` for URL-friendly strings (letters, numbers, `-`, `_`), e.g. `/blog/my-first-post/`. It has `db_index=True` by default because you look objects up by it; usually also `unique=True`. Generate it with `django.utils.text.slugify()`.

---

<a name="q21"></a>
## Q21. (Medium) How does Django 5.0's db_default handle complex database-level defaults?
**Answer:** `db_default` accepts literals or database expressions, compiled into the column's `DEFAULT` clause: `db_default=Now()`, `db_default=Lower(Value("X"))`, etc. The DB computes the value at insert — also for inserts outside Django. Expressions must be valid as DB defaults (no references to other columns).

---

<a name="q22"></a>
## Q22. (Easy) How do you write a custom validator for a model field?
**Answer:** A function that raises `ValidationError`, attached to the field. Runs in forms and `full_clean()` (not on plain `save()`).

```python
def validate_even(value):
    if value % 2:
        raise ValidationError("%(v)s is not even", params={"v": value})

quantity = models.IntegerField(validators=[validate_even])
```

---

<a name="q23"></a>
## Q23. (Easy) What are the risks of using FloatField for monetary calculations?
**Answer:** Floats can't represent most decimal fractions exactly (`0.1 + 0.2 = 0.30000000000000004`), so totals drift and rounding errors pile up — invoices don't match. Use `DecimalField` + Python `Decimal` (or store integer cents).

---

<a name="q24"></a>
## Q24. (Medium) How does Django map ArrayField in PostgreSQL database backend?
**Answer:** `django.contrib.postgres.fields.ArrayField(base_field)` → a native PostgreSQL array column (e.g. `varchar(50)[]`). Query with `__contains`, `__overlap`, `__len`, index lookups (`tags__0`). Index with `GinIndex` for contains/overlap. PostgreSQL only; for real relations a M2M is usually better.

---

<a name="q25"></a>
## Q25. (Hard) How do custom database representation conversion methods work (to_python, get_prep_value, from_db_value)?
**Answer:**
- `from_db_value(value, expression, connection)` — DB value → Python object, when loading rows.
- `to_python(value)` — any input (forms, deserialization) → Python object; used in validation.
- `get_prep_value(value)` — Python object → DB-ready value for saves and lookups (`get_db_prep_value` adds backend-specific conversion).

---

<a name="q26"></a>
## Q26. (Hard) How does JSONField index compilation happen in Postgres?
**Answer:** `GinIndex(fields=["data"])` compiles to `CREATE INDEX ... USING gin ("data")`, which speeds up `@>` containment and key-existence lookups. For one key, an expression index like `Index(KeyTextTransform("status", "data"), name=...)` becomes `CREATE INDEX ... (("data" ->> 'status'))`, used by `filter(data__status="x")` style queries on that key.

---

<a name="q27"></a>
## Q27. (Easy) What is the purpose of FileField storage parameter?
**Answer:** It chooses where the file is saved — local disk, S3, Azure Blob, etc. — per field, overriding the default storage. It can be a callable (to pick storage at runtime). Django 4.2+ configures storages via the `STORAGES` setting.

```python
document = models.FileField(upload_to="docs/%Y/%m/", storage=private_storage)
```

---

<a name="q28"></a>
## Q28. (Medium) How does Django convert dates dynamically to timezone offsets?
**Answer:** Datetimes are stored in UTC and converted to the **current timezone** (default `TIME_ZONE`, or one set per request with `timezone.activate()`) for display and form input. Use `timezone.localtime(dt)` in code. Date functions in queries (`TruncDate`, `__date`) use the current timezone, so "today" means the user's day.

---

<a name="q29"></a>
## Q29. (Medium) How do you validate uniqueness of a combination of fields in model clean?
**Answer:** Best: `Meta.constraints = [UniqueConstraint(fields=["team", "user"], name="uniq_team_user")]` — enforced by the DB, and `full_clean()` validates it with a nice error. Checking manually in `clean()` alone isn't safe against concurrent requests.

---

<a name="q30"></a>
## Q30. (Easy) What is the default db column name compilation strategy?
**Answer:** Column = field name (`first_name`); ForeignKeys get `_id` (`author_id`). Override with `db_column`. Table name = `<app_label>_<model name lowercased>` (`shop_orderitem`); override with `Meta.db_table`.

---

<a name="q31"></a>
## Q31. (Hard) How do you implement field encryption transparently in Django models?
**Answer:** A custom field that encrypts in `get_prep_value()` and decrypts in `from_db_value()` (e.g. with `cryptography.Fernet`), so code works with plain values. Trade-offs: you can't filter, sort or index encrypted values (unless you add a deterministic hash column for lookups), key management/rotation is your job, and the column gets bigger. Database-level/disk encryption is an alternative for "at rest" requirements.

---

<a name="q32"></a>
## Q32. (Easy) Explain the database storage size difference between SmallIntegerField and BigIntegerField.
**Answer:** `SmallIntegerField` = 2 bytes (−32,768 to 32,767), `IntegerField` = 4 bytes (±2.1 billion), `BigIntegerField` = 8 bytes (±9.2 × 10¹⁸). Use the smallest that safely fits; for primary keys of big tables use `BigAutoField` (Django's default since 3.2).

---

<a name="q33"></a>
## Q33. (Easy) How does Django handle choices validation in forms vs models?
**Answer:** ModelForms render choices as a select and validate the submitted value. Models validate choices only in `full_clean()`. Plain `save()`, `create()`, `update()` and bulk operations accept any value — the DB has no check unless you add a `CheckConstraint`.

---

<a name="q34"></a>
## Q34. (Medium) What is the impact of changing a CharField max_length on indexing?
**Answer:** It creates an `AlterField` migration (`ALTER COLUMN TYPE varchar(n)`). On PostgreSQL, **increasing** the length is a quick metadata change; **decreasing** must check/rewrite data. On MySQL it can rebuild the table, and long `varchar` columns may exceed index size limits (utf8mb4 = 4 bytes per char).

---

<a name="q35"></a>
## Q35. (Medium) How does Django 5.0 compile GeneratedField on SQLite backend?
**Answer:** SQLite supports generated columns (3.31+), both virtual (`db_persist=False`) and stored (`db_persist=True`). Django writes `GENERATED ALWAYS AS (expr) VIRTUAL/STORED`. Since SQLite can't add a stored generated column with `ALTER TABLE`, Django rebuilds the table when you add one to an existing model.
