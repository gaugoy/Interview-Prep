# Module 02: Model Design & Inheritance (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/02_Model_Design.md)

## Table of Contents
1. (Easy) [What are Abstract Base Models and when should you use them?](#q1)
2. (Medium) [How does Abstract Model inheritance affect database tables and indexes?](#q2)
3. (Easy) [What are Proxy Models and what are their architectural limitations?](#q3)
4. (Easy) [How does Multi-Table Inheritance (MTI) work in Django database-wise?](#q4)
5. (Medium) [What is the performance cost of Multi-Table Inheritance query-wise?](#q5)
6. (Easy) [How does Django's model validation framework work (full_clean(), clean(), clean_fields())?](#q6)
7. (Easy) [When is clean() called automatically in the model lifecycle?](#q7)
8. (Medium) [Explain the order of execution during a model.save() call.](#q8)
9. (Medium) [How do you prevent database race conditions in model custom save() methods?](#q9)
10. (Medium) [What is the difference between overriding save() and using a pre_save/post_save signal?](#q10)
11. (Medium) [Why should you avoid using Django signals for business logic?](#q11)
12. (Medium) [How does the model.delete() method work on bulk querysets versus individual instances?](#q12)
13. (Medium) [How does Django handle cascading deletes internally?](#q13)
14. (Easy) [How do you implement soft deletes in Django ORM?](#q14)
15. (Medium) [What are the issues with soft deletes and foreign key relationships?](#q15)
16. (Medium) [How does Django's content types framework work and what is its performance impact?](#q16)
17. (Medium) [What is the cost of GenericForeignKeys in database queries?](#q17)
18. (Medium) [How do you optimize queries involving generic relationships?](#q18)
19. (Medium) [How does Django handle model instance state tracking (_state)?](#q19)
20. (Medium) [What is the purpose of the from_db() method in Django models?](#q20)
21. (Medium) [How do you implement custom model lifecycle hooks?](#q21)
22. (Easy) [Explain how to design a self-referential model.](#q22)
23. (Medium) [What are the database schema implications of self-referential relationships?](#q23)
24. (Easy) [How do you handle circular dependencies between models in different apps?](#q24)
25. (Medium) [How does Django 5.0's db_default differ from standard default values?](#q25)
26. (Medium) [How does model subclassing affect migrations?](#q26)
27. (Medium) [What is the execution context of post_init signal?](#q27)
28. (Medium) [How do you write validation rules that query other models safely?](#q28)
29. (Medium) [How does django-polymorphic improve polymorphic querying?](#q29)
30. (Medium) [Explain table layout design for single-table inheritance in Django.](#q30)
31. (Medium) [How do you implement global model validators in settings?](#q31)
32. (Medium) [What is the relationship between model state and db connection?](#q32)
33. (Medium) [How do you write a custom pre_delete hook that intercepts deletes?](#q33)
34. (Hard) [How does the model manager get bounds to proxy subclasses?](#q34)
35. (Medium) [Explain how Django 5.0 resolves db_default values in bulk_create.](#q35)

---

<a name="q1"></a>
## Q1. (Easy) What are Abstract Base Models and when should you use them?
**Answer:** A model with `Meta: abstract = True` — no table of its own; its fields and methods are copied into every child model's table. Use it to share common fields (`created_at`, `updated_at`, `created_by`) without extra JOINs.

```python
class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Order(TimeStamped):
    total = models.DecimalField(max_digits=10, decimal_places=2)
```

---

<a name="q2"></a>
## Q2. (Medium) How does Abstract Model inheritance affect database tables and indexes?
**Answer:** Each child gets its own table with all inherited columns, indexes and constraints. Because names must be unique, use placeholders in inherited index/constraint names and `related_name`: `"%(app_label)s_%(class)s_..."`. There's no shared table, so you can't query "all children" at once.

---

<a name="q3"></a>
## Q3. (Easy) What are Proxy Models and what are their architectural limitations?
**Answer:** `Meta: proxy = True` — a new Python class over the **same table**. Use it to change behaviour: different default manager, ordering, methods, or a separate admin.
Limitations: can't add fields; must inherit from exactly one concrete model; queries still return the rows of the whole table unless the proxy's manager filters them.

```python
class ActiveUser(User):
    objects = ActiveUserManager()
    class Meta:
        proxy = True
```

---

<a name="q4"></a>
## Q4. (Easy) How does Multi-Table Inheritance (MTI) work in Django database-wise?
**Answer:** The parent and each child are concrete models with their **own tables**. The child table has a one-to-one primary key `<parent>_ptr_id` pointing to the parent row. Inherited fields live in the parent table, child-specific fields in the child table.

---

<a name="q5"></a>
## Q5. (Medium) What is the performance cost of Multi-Table Inheritance query-wise?
**Answer:** Every child query JOINs the parent table; every save writes two (or more) tables; getting the child from a parent (`place.restaurant`) is an extra query per row unless `select_related`. Deep hierarchies multiply the joins. Prefer abstract base classes or one table with a type column unless you truly need to query across all types.

---

<a name="q6"></a>
## Q6. (Easy) How does Django's model validation framework work (full_clean(), clean(), clean_fields())?
**Answer:** `full_clean()` runs, in order:
1. `clean_fields()` — each field's type, `max_length`, choices, validators.
2. `clean()` — your cross-field rules.
3. `validate_unique()` — unique checks.
4. `validate_constraints()` (Django 4.1+) — `Meta.constraints`.
It raises `ValidationError` with all errors. It is **not** called by `save()`.

---

<a name="q7"></a>
## Q7. (Easy) When is clean() called automatically in the model lifecycle?
**Answer:** Only by `ModelForm` validation (and the admin, which uses ModelForms). Not by `save()`, `create()`, `bulk_create()`, or DRF serializers. If you need it elsewhere, call `obj.full_clean()` yourself before saving.

---

<a name="q8"></a>
## Q8. (Medium) Explain the order of execution during a model.save() call.
**Answer:**
1. `pre_save` signal.
2. Each field's `pre_save()` (e.g. `auto_now` sets the time).
3. Parent tables saved first (multi-table inheritance).
4. `UPDATE` if the object exists, otherwise `INSERT` (new objects with a default pk go straight to INSERT).
5. `_state.adding = False`, `_state.db` set.
6. `post_save` signal (`created=True/False`).

---

<a name="q9"></a>
## Q9. (Medium) How do you prevent database race conditions in model custom save() methods?
**Answer:** Typical bug: generating a value with "read max, add 1" in `save()` — two requests get the same number. Fixes: let the DB do it (sequence / auto field, `F()` updates), add a **unique constraint** and retry on `IntegrityError`, or lock with `select_for_update()` inside `atomic()`. Save only changed fields with `update_fields` to avoid overwriting others' changes.

---

<a name="q10"></a>
## Q10. (Medium) What is the difference between overriding save() and using a pre_save/post_save signal?
**Answer:** Overriding `save()` keeps logic with the model, is explicit and easy to follow. Signals decouple code (useful for reacting to models you don't own, e.g. third-party apps) but hide the flow. Both are skipped by `update()`, `bulk_create()` and `bulk_update()`. Prefer `save()` or a service function for your own models.

---

<a name="q11"></a>
## Q11. (Medium) Why should you avoid using Django signals for business logic?
**Answer:** They make the flow implicit (hard to find who changes what), run synchronously inside the same transaction, aren't fired by bulk operations, make ordering between receivers unclear, and complicate testing. Use explicit service functions for business logic; keep signals for loose integration (cache invalidation, third-party models).

---

<a name="q12"></a>
## Q12. (Medium) How does the model.delete() method work on bulk querysets versus individual instances?
**Answer:** `obj.delete()` calls your model's `delete()`. `queryset.delete()` does **not** call each object's `delete()` method — custom delete logic is skipped. Both use Django's Collector to handle cascades, and both send `pre_delete`/`post_delete` signals per object. Both return `(count, {model: count})`.

---

<a name="q13"></a>
## Q13. (Medium) How does Django handle cascading deletes internally?
**Answer:** Django emulates `on_delete` in Python, not in the database. A `Collector` finds all related objects, applies the rule (CASCADE → delete them too, SET_NULL → update, PROTECT/RESTRICT → error), sends signals, and deletes in dependency order (children first) inside a transaction. That's why deleting one parent can run many queries.

---

<a name="q14"></a>
## Q14. (Easy) How do you implement soft deletes in Django ORM?
**Answer:** Add a `deleted_at` field, override `delete()` to set it, and use a default manager that hides deleted rows.

```python
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Document(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])
```

---

<a name="q15"></a>
## Q15. (Medium) What are the issues with soft deletes and foreign key relationships?
**Answer:** No real cascade — children of a soft-deleted parent stay "alive"; related managers and joins may still show deleted rows; unique constraints block re-creating the same value (use a conditional `UniqueConstraint(..., condition=Q(deleted_at__isnull=True))`); `queryset.delete()` bypasses your `delete()` (hard delete!) unless you add a custom QuerySet. Tables also grow forever — plan archiving.

---

<a name="q16"></a>
## Q16. (Medium) How does Django's content types framework work and what is its performance impact?
**Answer:** `django_content_type` has one row per model (`app_label`, `model`). It lets you reference "any model" by content-type id — used by permissions, admin logs and generic foreign keys. `ContentType.objects.get_for_model()` is cached in memory, so lookups are cheap. The real cost is generic relations: no JOINs or FK constraints.

---

<a name="q17"></a>
## Q17. (Medium) What is the cost of GenericForeignKeys in database queries?
**Answer:** A GFK is just `content_type_id` + `object_id`, with no real foreign key. So: no `select_related` (can't JOIN), prefetch needs one query per content type, no referential integrity (orphans possible), no `ON DELETE` behaviour, and filtering by target fields needs extra work. Needs a composite index on `(content_type, object_id)`.

---

<a name="q18"></a>
## Q18. (Medium) How do you optimize queries involving generic relationships?
**Answer:** `prefetch_related("content_object")` (one query per type; Django 5.0 `GenericPrefetch` for per-type querysets), add a `GenericRelation` on target models to enable reverse filtering and cascade deletes, index `(content_type, object_id)`, and store display data (title/type) on the row to avoid loading targets. If types are few and fixed, explicit nullable FKs are often simpler.

---

<a name="q19"></a>
## Q19. (Medium) How does Django handle model instance state tracking (_state)?
**Answer:** Each instance has `_state` (`ModelState`) with: `adding` (True until saved/loaded — used to decide INSERT vs UPDATE and for unique validation), `db` (which database alias it came from / was saved to), and `fields_cache` (cached related objects). Django doesn't track changed fields — you have to implement dirty tracking yourself.

---

<a name="q20"></a>
## Q20. (Medium) What is the purpose of the from_db() method in Django models?
**Answer:** A classmethod Django calls to build an instance from a database row. Override it to customize loading — commonly to remember original values for change detection.

```python
@classmethod
def from_db(cls, db, field_names, values):
    obj = super().from_db(db, field_names, values)
    obj._loaded_values = dict(zip(field_names, values))
    return obj
```

---

<a name="q21"></a>
## Q21. (Medium) How do you implement custom model lifecycle hooks?
**Answer:** Options: override `save()`/`delete()` and call methods like `before_save()` / `after_create()`; use signals; or use a library like `django-lifecycle` (`@hook(AFTER_CREATE)`). For side effects outside the DB, run them with `transaction.on_commit()`. Remember bulk operations skip all of these.

---

<a name="q22"></a>
## Q22. (Easy) Explain how to design a self-referential model.
**Answer:** A ForeignKey to `"self"` — e.g. categories, org charts, comment threads.

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True,
                               on_delete=models.CASCADE, related_name="children")
```
`null=True` for root nodes; `category.children.all()` gets direct children.

---

<a name="q23"></a>
## Q23. (Medium) What are the database schema implications of self-referential relationships?
**Answer:** The table has an FK column pointing at its own pk (indexed). Simple to store, but reading a whole tree needs many queries (one per level) or a recursive CTE. Deep cascades can delete large subtrees. For heavy tree reads use materialized path, nested sets (django-mptt), closure tables, or recursive CTE queries.

---

<a name="q24"></a>
## Q24. (Easy) How do you handle circular dependencies between models in different apps?
**Answer:** Use lazy string references (`models.ForeignKey("billing.Invoice", ...)`) instead of imports. For migrations, Django splits the cycle by creating one model first and adding the FK in a later migration; if needed, do that split manually. Often a circular dependency hints that the app boundaries should be redesigned.

---

<a name="q25"></a>
## Q25. (Medium) How does Django 5.0's db_default differ from standard default values?
**Answer:** `default` is applied **in Python** when the object is created. `db_default` sets a `DEFAULT` in the **database** column, so it also applies to rows inserted outside Django (raw SQL, other services) and can use DB functions like `Now()`.

```python
created_at = models.DateTimeField(db_default=Now())
```
On PostgreSQL the DB-generated value is returned after insert.

---

<a name="q26"></a>
## Q26. (Medium) How does model subclassing affect migrations?
**Answer:** Abstract base → its fields appear in each child's migration (changing the base creates migrations for all children). Proxy → a migration with `proxy=True`, no table. Multi-table → a new table with a `<parent>_ptr` one-to-one. Switching between these types later is a painful data migration — choose early.

---

<a name="q27"></a>
## Q27. (Medium) What is the execution context of post_init signal?
**Answer:** It fires at the end of `Model.__init__` — for **every** instance, including each row loaded from a queryset. So a slow receiver slows down every query; never run DB queries in it. It's used to snapshot initial values (dirty tracking).

---

<a name="q28"></a>
## Q28. (Medium) How do you write validation rules that query other models safely?
**Answer:** Put them in `clean()` (or a service), query using the same database (`self._state.db`), and exclude the current object on updates (`.exclude(pk=self.pk)`). But validation + save isn't atomic — another request can slip in between — so back critical rules with a **DB constraint** (unique/check) or a lock.

---

<a name="q29"></a>
## Q29. (Medium) How does django-polymorphic improve polymorphic querying?
**Answer:** With normal MTI, `Asset.objects.all()` returns base `Asset` objects. django-polymorphic stores a content type on each row and automatically returns the correct subclass instances (`Server`, `Laptop`), fetching child data with one extra query per subclass. Convenient, but adds queries — use `non_polymorphic()` when you only need base fields.

---

<a name="q30"></a>
## Q30. (Medium) Explain table layout design for single-table inheritance in Django.
**Answer:** Django has no built-in single-table inheritance, but you can emulate it: one concrete table with all fields (type-specific ones nullable) + a `type` column, and proxy models whose managers filter by type. No joins and simple queries; downsides are sparse nullable columns and weaker DB-level validation (use check constraints per type).

---

<a name="q31"></a>
## Q31. (Medium) How do you implement global model validators in settings?
**Answer:** Django has no setting for global model validators (`AUTH_PASSWORD_VALIDATORS` is only for passwords). Options: a shared abstract base model whose `clean()` applies common rules, reusable validator functions attached to fields, or system checks (`@register`) to enforce conventions at startup.

---

<a name="q32"></a>
## Q32. (Medium) What is the relationship between model state and db connection?
**Answer:** `instance._state.db` stores the alias the object was loaded from or saved to. Django uses it as a routing hint: `save()`, related lookups and lazy loading go to that same database. Relating objects from different databases is blocked by `allow_relation`.

---

<a name="q33"></a>
## Q33. (Medium) How do you write a custom pre_delete hook that intercepts deletes?
**Answer:** Connect a `pre_delete` receiver — it fires for both `obj.delete()` and `queryset.delete()`. To **block** a delete, raise an exception (the transaction rolls back). For simple "can't delete while referenced" rules, prefer `on_delete=models.PROTECT`.

```python
@receiver(pre_delete, sender=Invoice)
def block_paid(sender, instance, **kwargs):
    if instance.status == "paid":
        raise PermissionDenied("Paid invoices can't be deleted")
```

---

<a name="q34"></a>
## Q34. (Hard) How does the model manager get bounds to proxy subclasses?
**Answer:** Managers are inherited: a proxy model gets the parent's managers, bound to the proxy class, so `ProxyModel.objects` returns proxy instances. You can declare new managers on the proxy (e.g. one that filters by type); the first declared one becomes its default manager.

---

<a name="q35"></a>
## Q35. (Medium) Explain how Django 5.0 resolves db_default values in bulk_create.
**Answer:** For fields you didn't set, Django puts `DEFAULT` in the INSERT so the database fills the value. On backends that can return columns from insert (PostgreSQL), the generated values are sent back and set on the objects; elsewhere you must re-fetch them.
