# Module 04: Model Meta Options (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/04_Model_Meta_Options.md)

## Table of Contents
1. (Easy) [What is the purpose of the Model Meta class and how is it evaluated?](#q1)
2. (Easy) [How does db_table option affect database table naming?](#q2)
3. (Easy) [How do you define composite or multi-column indexes using indexes in Meta?](#q3)
4. (Easy) [What is the difference between unique_together and UniqueConstraint in Meta?](#q4)
5. (Easy) [How do you define CheckConstraint to enforce row-level validation?](#q5)
6. (Easy) [What is the impact of the ordering option in Meta on all queries?](#q6)
7. (Easy) [How do you disable default ordering for a specific query to improve performance?](#q7)
8. (Easy) [What is the managed option in Meta and when should you set it to False?](#q8)
9. (Medium) [How does the db_alias option affect model database routing?](#q9)
10. (Medium) [How do you implement partial indexes using constraints and indexes in Meta?](#q10)
11. (Medium) [What is the select_on_save option and how does it affect insert vs update logic?](#q11)
12. (Easy) [What is the verbose_name and verbose_name_plural options in Meta?](#q12)
13. (Easy) [How does the default_permissions option work in Django model Meta?](#q13)
14. (Easy) [How do you define custom permissions in Meta and load them into the database?](#q14)
15. (Hard) [What is the base_manager_name option and when should you customize it?](#q15)
16. (Medium) [What is the default_manager_name option and how does it differ from base_manager_name?](#q16)
17. (Easy) [How does the get_latest_by option affect QuerySet.latest() and earliest()?](#q17)
18. (Medium) [How do you enforce database-level unique constraints with conditions?](#q18)
19. (Easy) [What is the proxy option in Meta and how does it restrict table creation?](#q19)
20. (Easy) [How does abstract option in Meta change class inheritance behavior?](#q20)
21. (Hard) [How does Django construct the _meta API internally?](#q21)
22. (Easy) [How do you dynamically access a model's fields using the _meta API?](#q22)
23. (Medium) [What are the risks of using ordering in Meta when performing annotations?](#q23)
24. (Medium) [How does Django handle index names and constraint names dynamically?](#q24)
25. (Medium) [Explain how to configure database-level constraints using Django 5.0 Meta constraints.](#q25)
26. (Medium) [How does ordering affect union() query operations?](#q26)
27. (Easy) [What is the default_related_name option and when is it useful?](#q27)
28. (Medium) [How do you define a case-insensitive unique constraint in Meta?](#q28)
29. (Hard) [What is the internal design of django.db.models.options.Options?](#q29)
30. (Medium) [How does db_tablespace affect physical table location?](#q30)
31. (Medium) [How do you retrieve all reverse relations via the _meta API?](#q31)
32. (Medium) [What happens if you define multiple default managers in a model?](#q32)
33. (Medium) [How do you define index conditions using Q objects?](#q33)
34. (Easy) [How do check constraints validate field ranges in SQL?](#q34)
35. (Medium) [Explain how unique constraints resolve null values in PostgreSQL vs MySQL.](#q35)

---

<a name="q1"></a>
## Q1. (Easy) What is the purpose of the Model Meta class and how is it evaluated?
**Answer:** `class Meta` holds model-level settings that aren't fields: table name, ordering, indexes, constraints, permissions, verbose names, abstract/proxy/managed. When the model class is created, Django reads `Meta` once and stores everything in `Model._meta` (an `Options` object) used by the ORM, migrations, admin and forms.

---

<a name="q2"></a>
## Q2. (Easy) How does db_table option affect database table naming?
**Answer:** By default the table is `<app_label>_<modelname>` (e.g. `shop_order`). `db_table = "orders"` sets an exact name — useful for legacy databases or naming conventions. Changing it later creates a rename-table migration.

---

<a name="q3"></a>
## Q3. (Easy) How do you define composite or multi-column indexes using indexes in Meta?
**Answer:**

```python
class Meta:
    indexes = [models.Index(fields=["customer", "-created_at"], name="order_cust_created_idx")]
```
Column order matters: the index helps queries that filter on the first column(s) (`customer`, or `customer` + `created_at`), not on `created_at` alone.

---

<a name="q4"></a>
## Q4. (Easy) What is the difference between unique_together and UniqueConstraint in Meta?
**Answer:** Both make a combination of fields unique. `UniqueConstraint` is the modern, more powerful option: it supports a `condition` (partial unique), expressions (e.g. `Lower("email")`), `nulls_distinct`, custom error messages and deferrable constraints. `unique_together` may be deprecated in future — use `UniqueConstraint`.

```python
constraints = [models.UniqueConstraint(fields=["team", "user"], name="uniq_team_user")]
```

---

<a name="q5"></a>
## Q5. (Easy) How do you define CheckConstraint to enforce row-level validation?
**Answer:** A database `CHECK` rule on each row.

```python
class Meta:
    constraints = [
        models.CheckConstraint(condition=Q(end_date__gt=F("start_date")), name="end_after_start"),
        models.CheckConstraint(condition=Q(price__gte=0), name="price_non_negative"),
    ]
```
(Django ≤ 5.0 uses `check=` instead of `condition=`.) The DB rejects bad rows with `IntegrityError`; `full_clean()` also validates it.

---

<a name="q6"></a>
## Q6. (Easy) What is the impact of the ordering option in Meta on all queries?
**Answer:** `ordering = ["-created_at"]` adds `ORDER BY` to every query that doesn't specify its own order — convenient, but every list query pays for a sort (and needs a matching index on big tables). It also affects `first()`/`last()` and admin.

---

<a name="q7"></a>
## Q7. (Easy) How do you disable default ordering for a specific query to improve performance?
**Answer:** Call `order_by()` with no arguments — it removes the `ORDER BY`.

```python
Order.objects.filter(status="paid").order_by().values("customer").annotate(n=Count("id"))
```
Useful for counts, aggregations, `exists()` and bulk processing where order doesn't matter.

---

<a name="q8"></a>
## Q8. (Easy) What is the managed option in Meta and when should you set it to False?
**Answer:** `managed = False` tells migrations not to create, alter or drop the table — Django just uses it. Use it for existing legacy tables, tables owned by another system, or database views. You keep the model in sync with the real schema yourself.

---

<a name="q9"></a>
## Q9. (Medium) How does the db_alias option affect model database routing?
**Answer:** There's no `db_alias` option in `Meta`. Which database a model uses is decided by **database routers** (`DATABASE_ROUTERS`) or per query with `using("alias")`. A common pattern is a custom Meta-like class attribute (e.g. `database = "ods"`) that your router reads.

---

<a name="q10"></a>
## Q10. (Medium) How do you implement partial indexes using constraints and indexes in Meta?
**Answer:** Add a `condition` so only matching rows are indexed — smaller, faster index for a common filter.

```python
indexes = [models.Index(fields=["created_at"], condition=Q(status="pending"), name="pending_created_idx")]
```
Supported on PostgreSQL and SQLite. Queries must include the same condition to use it.

---

<a name="q11"></a>
## Q11. (Medium) What is the select_on_save option and how does it affect insert vs update logic?
**Answer:** Normally `save()` on an object with a pk runs `UPDATE`, and if no row was updated, `INSERT`. With `select_on_save = True`, Django first does a `SELECT` to check if the row exists. Only needed in rare cases where `UPDATE` reports 0 rows even though the row exists (e.g. certain DB triggers). Default `False`.

---

<a name="q12"></a>
## Q12. (Easy) What is the verbose_name and verbose_name_plural options in Meta?
**Answer:** Human-readable names for the model used in the admin and messages: `verbose_name = "order item"`, `verbose_name_plural = "order items"`. Default is derived from the class name (`OrderItem` → "order item", plural adds "s").

---

<a name="q13"></a>
## Q13. (Easy) How does the default_permissions option work in Django model Meta?
**Answer:** Django auto-creates `add`, `change`, `delete`, `view` permissions per model. `default_permissions = ("add", "view")` creates only those; `()` creates none (e.g. for read-only or internal models).

---

<a name="q14"></a>
## Q14. (Easy) How do you define custom permissions in Meta and load them into the database?
**Answer:** List them in `permissions`; they're created when you run `migrate` (via a `post_migrate` handler).

```python
class Meta:
    permissions = [("approve_invoice", "Can approve invoice")]
# check: user.has_perm("billing.approve_invoice")
```

---

<a name="q15"></a>
## Q15. (Hard) What is the base_manager_name option and when should you customize it?
**Answer:** The base manager is used by Django internally — e.g. when following a ForeignKey (`order.customer`) and in some internal operations — and it must **not filter out rows**, or related objects "disappear". Default is a plain `Manager`. Customize only to add methods/behaviour, never filtering.

---

<a name="q16"></a>
## Q16. (Medium) What is the default_manager_name option and how does it differ from base_manager_name?
**Answer:** `default_manager_name` picks `_default_manager` — used by the admin, `dumpdata`, generic views and reverse related managers (`customer.order_set`). `base_manager_name` picks `_base_manager` — used for forward relation access and internals. By default the default manager is the first one defined in the class.

---

<a name="q17"></a>
## Q17. (Easy) How does the get_latest_by option affect QuerySet.latest() and earliest()?
**Answer:** `get_latest_by = "created_at"` lets you call `Order.objects.latest()` / `earliest()` without arguments. Without it, you must pass the field: `latest("created_at")`. Raises `DoesNotExist` when empty.

---

<a name="q18"></a>
## Q18. (Medium) How do you enforce database-level unique constraints with conditions?
**Answer:** `UniqueConstraint` with `condition` — a partial unique index.

```python
constraints = [models.UniqueConstraint(fields=["email"], condition=Q(deleted_at__isnull=True),
                                       name="uniq_active_email")]
```
Classic use: soft delete (only active rows must be unique), "one default address per user".

---

<a name="q19"></a>
## Q19. (Easy) What is the proxy option in Meta and how does it restrict table creation?
**Answer:** `proxy = True` creates no table — the proxy uses the parent's table and only changes Python behaviour (managers, methods, ordering, admin). It can't add fields and must have exactly one concrete parent.

---

<a name="q20"></a>
## Q20. (Easy) How does abstract option in Meta change class inheritance behavior?
**Answer:** `abstract = True` → no table, can't be queried or instantiated; children copy its fields into their own tables. Without it, inheriting from a concrete model gives multi-table inheritance (two tables + join). Children don't inherit `abstract=True` itself.

---

<a name="q21"></a>
## Q21. (Hard) How does Django construct the _meta API internally?
**Answer:** When a model class is created, the `ModelBase` metaclass builds an `Options` object from `Meta`, attaches it as `_meta`, and each field/manager adds itself via `contribute_to_class()`. Relation info and the full field list are computed lazily once all models are loaded (the app registry is ready) and then cached.

---

<a name="q22"></a>
## Q22. (Easy) How do you dynamically access a model's fields using the _meta API?
**Answer:**

```python
Order._meta.get_fields()              # all fields incl. reverse relations
Order._meta.get_field("total")        # one field
[f.name for f in Order._meta.concrete_fields]
Order._meta.db_table, Order._meta.app_label, Order._meta.verbose_name
```
Used for generic exports, serializers, admin-like tools.

---

<a name="q23"></a>
## Q23. (Medium) What are the risks of using ordering in Meta when performing annotations?
**Answer:** In older Django versions Meta ordering fields were added to `GROUP BY`, breaking aggregations; since Django 3.1 they're ignored in GROUP BY. Still, default ordering adds sorting cost to aggregations/subqueries and can surprise you in `values()` + `distinct()`. Use `order_by()` to clear it when grouping.

---

<a name="q24"></a>
## Q24. (Medium) How does Django handle index names and constraint names dynamically?
**Answer:** `Meta.indexes` and `Meta.constraints` need explicit `name`s (in abstract bases use `%(app_label)s` / `%(class)s` placeholders). For `db_index=True`, unique fields and FKs, Django generates names from table + columns + a hash suffix, truncated to the DB's identifier length limit.

---

<a name="q25"></a>
## Q25. (Medium) Explain how to configure database-level constraints using Django 5.0 Meta constraints.
**Answer:** Use `UniqueConstraint` and `CheckConstraint` in `Meta.constraints`. Django 5.0 adds `violation_error_code` (alongside `violation_error_message` from 4.1) for friendly validation errors, and `nulls_distinct` on `UniqueConstraint` (PostgreSQL 15+). They're created by migrations and validated by `full_clean()`.

```python
models.UniqueConstraint(fields=["sku"], name="uniq_sku",
                        violation_error_message="SKU already exists", violation_error_code="dup_sku")
```

---

<a name="q26"></a>
## Q26. (Medium) How does ordering affect union() query operations?
**Answer:** In `qs1.union(qs2)`, the individual querysets' ordering (including Meta ordering) isn't applied — only an `order_by()` on the **combined** result counts, and it can only use columns from the select list. Some backends error on ORDER BY inside the parts, so clear ordering on the parts and order the result.

---

<a name="q27"></a>
## Q27. (Easy) What is the default_related_name option and when is it useful?
**Answer:** Sets the reverse relation name for all FKs/M2Ms on the model: `default_related_name = "orders"` → `customer.orders.all()` instead of `customer.order_set`. Useful for consistency, and in abstract bases with `%(class)s` to avoid name clashes.

---

<a name="q28"></a>
## Q28. (Medium) How do you define a case-insensitive unique constraint in Meta?
**Answer:** Use an expression in `UniqueConstraint` (Django 4.0+):

```python
from django.db.models.functions import Lower
constraints = [models.UniqueConstraint(Lower("email"), name="uniq_email_ci")]
```
Alternatively a PostgreSQL `citext` column with normal `unique=True`.

---

<a name="q29"></a>
## Q29. (Hard) What is the internal design of django.db.models.options.Options?
**Answer:** `Options` (the `_meta` object) stores model metadata: `db_table`, `app_label`, ordering, indexes, constraints, managers, and the field lists (`local_fields`, `concrete_fields`, `many_to_many`, `related_objects`). Expensive lists are computed lazily and cached (`get_fields()` cache), and the cache is reset when models are added. It's the central place the ORM, migrations and admin read model info from.

---

<a name="q30"></a>
## Q30. (Medium) How does db_tablespace affect physical table location?
**Answer:** On databases with tablespaces (PostgreSQL, Oracle), `Meta.db_tablespace = "fast_ssd"` creates the table in that tablespace; indexes can have their own (`db_tablespace` on `Index`, or `DEFAULT_INDEX_TABLESPACE`). Used to put hot tables/indexes on faster disks. Ignored by SQLite/MySQL.

---

<a name="q31"></a>
## Q31. (Medium) How do you retrieve all reverse relations via the _meta API?
**Answer:** Reverse relations are auto-created, non-concrete fields:

```python
reverse = [f for f in Customer._meta.get_fields() if f.auto_created and not f.concrete]
for rel in reverse:
    print(rel.name, rel.related_model, rel.one_to_many or rel.many_to_many)
```
`Customer._meta.related_objects` gives the same list.

---

<a name="q32"></a>
## Q32. (Medium) What happens if you define multiple default managers in a model?
**Answer:** There's only one default manager: the **first** manager defined in the class (or the one named in `Meta.default_manager_name`). Others are just extra managers. Order matters — putting a filtering manager first makes it the default, which affects admin, dumpdata and reverse relations.

---

<a name="q33"></a>
## Q33. (Medium) How do you define index conditions using Q objects?
**Answer:** Pass a `Q` to `condition` on an `Index` (partial index):

```python
models.Index(fields=["user"], condition=Q(is_active=True) & Q(role="admin"), name="active_admin_idx")
```
Queries must filter on the same condition for the planner to use it.

---

<a name="q34"></a>
## Q34. (Easy) How do check constraints validate field ranges in SQL?
**Answer:** The `Q` is compiled into a `CHECK` clause, evaluated by the DB on every insert/update:

```sql
ALTER TABLE shop_product ADD CONSTRAINT price_range CHECK ("price" >= 0 AND "price" <= 100000);
```
Rows violating it fail with `IntegrityError`.

---

<a name="q35"></a>
## Q35. (Medium) Explain how unique constraints resolve null values in PostgreSQL vs MySQL.
**Answer:** By default both treat NULLs as **distinct** — many rows can have NULL in a unique column. PostgreSQL 15+ can treat NULLs as equal: `UniqueConstraint(fields=[...], nulls_distinct=False)` (Django 5.0). (SQL Server treats NULLs as equal in unique indexes — only one NULL allowed.)
