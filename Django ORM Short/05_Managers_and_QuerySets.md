# Module 05: Managers and QuerySets (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/05_Managers_and_QuerySets.md)

## Table of Contents
1. (Easy) [How do you create a custom Model Manager in Django?](#q1)
2. (Easy) [What is the difference between a custom Manager and a custom QuerySet?](#q2)
3. (Easy) [How do you implement chainable methods using custom QuerySet classes?](#q3)
4. (Medium) [How does Django construct the default Manager (objects) under the hood?](#q4)
5. (Easy) [How do you override the default manager's base QuerySet?](#q5)
6. (Medium) [What is the risk of overriding the default manager with custom filters?](#q6)
7. (Hard) [How does the base manager handle serialized data and relationships?](#q7)
8. (Easy) [How do you use multiple managers on a single model?](#q8)
9. (Medium) [How does Django select the manager to use for foreign key lookups?](#q9)
10. (Medium) [What is the difference between Manager.from_queryset() and custom managers?](#q10)
11. (Hard) [How does django.db.models.manager.ManagerDescriptor work?](#q11)
12. (Medium) [How do you implement soft delete logic in a custom Manager and QuerySet?](#q12)
13. (Easy) [How do you bypass custom manager filters when you need raw table access?](#q13)
14. (Medium) [Explain the lifecycle of a QuerySet instance creation inside a Manager.](#q14)
15. (Easy) [How do you implement custom business logic methods inside a manager?](#q15)
16. (Medium) [What is the relation between Django managers and the database backend routing?](#q16)
17. (Medium) [How do you write a manager that automatically annotates every queryset?](#q17)
18. (Medium) [What are the performance implications of auto-annotating managers?](#q18)
19. (Easy) [How do you use custom managers in django.contrib.admin?](#q19)
20. (Medium) [What is the purpose of _db attribute in QuerySets and Managers?](#q20)
21. (Easy) [How does Django's as_manager() method convert a QuerySet to a Manager?](#q21)
22. (Medium) [How do custom managers interact with M2M through tables?](#q22)
23. (Medium) [How do you handle manager validation and initialization arguments?](#q23)
24. (Easy) [How do you write tests for custom managers and querysets?](#q24)
25. (Medium) [How does Django 5.0 handle managers in asynchronous environments?](#q25)
26. (Medium) [How do you build a manager that routes writes to primary and reads to replica?](#q26)
27. (Hard) [Explain the relationship between Manager and Model class preparation.](#q27)
28. (Easy) [What is the purpose of contributed managers in django.contrib?](#q28)
29. (Hard) [How do custom managers support prefetch_related queries?](#q29)
30. (Medium) [How do you dynamically swap model managers at runtime?](#q30)
31. (Medium) [Explain how QuerySet.defer interacts with custom manager annotations.](#q31)
32. (Medium) [How does Django prevent multiple managers from overlapping in model schema?](#q32)
33. (Easy) [What is the execution overhead of manager descriptors?](#q33)
34. (Hard) [How do you implement a soft delete manager that handles cascades?](#q34)
35. (Easy) [How do you fetch raw SQL output directly from a Manager method?](#q35)

---

<a name="q1"></a>
## Q1. (Easy) How do you create a custom Model Manager in Django?
**Answer:** Subclass `models.Manager` and attach it to the model.

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")

class Article(models.Model):
    status = models.CharField(max_length=20)
    objects = models.Manager()
    published = PublishedManager()     # Article.published.all()
```

---

<a name="q2"></a>
## Q2. (Easy) What is the difference between a custom Manager and a custom QuerySet?
**Answer:** A **Manager** is the entry point on the model (`Article.objects`) — good for table-level methods like `create_user()`. A **QuerySet** subclass holds filter methods that can be **chained** (`.published().recent()`). Best practice: put filters on a custom QuerySet and expose them via the manager (`as_manager()` / `from_queryset()`).

---

<a name="q3"></a>
## Q3. (Easy) How do you implement chainable methods using custom QuerySet classes?
**Answer:** Methods return `self.filter(...)`, so they chain in any order.

```python
class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published")
    def by_author(self, user):
        return self.filter(author=user)

class Article(models.Model):
    objects = ArticleQuerySet.as_manager()

Article.objects.published().by_author(u).order_by("-created_at")
```

---

<a name="q4"></a>
## Q4. (Medium) How does Django construct the default Manager (objects) under the hood?
**Answer:** If a model defines no managers, Django adds `objects = models.Manager()` during class creation. A manager is mostly a proxy: `Article.objects.filter(...)` calls `get_queryset()` (a new `QuerySet(model=Article)`) and then `.filter(...)` on it. Each manager method returns a fresh queryset.

---

<a name="q5"></a>
## Q5. (Easy) How do you override the default manager's base QuerySet?
**Answer:** Override `get_queryset()` — everything from that manager starts from it.

```python
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).select_related("company")
```

---

<a name="q6"></a>
## Q6. (Medium) What is the risk of overriding the default manager with custom filters?
**Answer:** The first manager is the default one, used by admin, `dumpdata`, reverse relations and some internals. If it filters (e.g. hides inactive rows), those rows "disappear": admins can't see them, reverse relations miss them, data exports are incomplete, and `get()` raises `DoesNotExist` for hidden rows. Keep `objects = models.Manager()` first and add the filtered one as a second manager.

---

<a name="q7"></a>
## Q7. (Hard) How does the base manager handle serialized data and relationships?
**Answer:** Django uses `_base_manager` (a plain unfiltered `Manager` by default) for forward relation access (`order.customer`) and internal work, so related objects are always found even if your default manager filters. Serializing with `dumpdata` uses the default manager unless you pass `--all` (then the base manager). Never make the base manager filter rows.

---

<a name="q8"></a>
## Q8. (Easy) How do you use multiple managers on a single model?
**Answer:** Define several manager attributes, each with its own `get_queryset()`; the first one is the default.

```python
class Ticket(models.Model):
    objects = models.Manager()
    open = OpenTicketManager()
    archived = ArchivedTicketManager()
```

---

<a name="q9"></a>
## Q9. (Medium) How does Django select the manager to use for foreign key lookups?
**Answer:** Forward access (`order.customer`) uses the related model's `_base_manager` (unfiltered). Reverse/M2M managers (`customer.orders.all()`) are built from the related model's **default manager** class, so its filters apply. You can pick a specific manager for a reverse relation: `customer.orders(manager="active").all()`.

---

<a name="q10"></a>
## Q10. (Medium) What is the difference between Manager.from_queryset() and custom managers?
**Answer:** `Manager.from_queryset(MyQuerySet)` creates a manager class that copies the QuerySet's methods onto the manager, and you can still subclass it to add manager-only methods. `MyQuerySet.as_manager()` is the shortcut when you need no extra manager methods. Writing a manager by hand means re-implementing each method — no chaining.

```python
class ArticleManager(models.Manager.from_queryset(ArticleQuerySet)):
    def create_draft(self, **kw):
        return self.create(status="draft", **kw)
```

---

<a name="q11"></a>
## Q11. (Hard) How does django.db.models.manager.ManagerDescriptor work?
**Answer:** Managers are installed on the model class through a descriptor. Accessing `Article.objects` returns the manager; accessing it on an instance (`article.objects`) raises `AttributeError: Manager isn't accessible via instances` — managers are for table-level operations. It also blocks managers on abstract or swapped models.

---

<a name="q12"></a>
## Q12. (Medium) How do you implement soft delete logic in a custom Manager and QuerySet?
**Answer:** A QuerySet whose `delete()` sets a flag, and a manager that hides deleted rows.

```python
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.now())
    def alive(self):
        return self.filter(deleted_at__isnull=True)

class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().alive()

class Doc(models.Model):
    deleted_at = models.DateTimeField(null=True)
    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()
```

---

<a name="q13"></a>
## Q13. (Easy) How do you bypass custom manager filters when you need raw table access?
**Answer:** Keep an unfiltered manager (`all_objects = models.Manager()`), or use `Model._base_manager`. For SQL-level access use `Model.objects.raw()` or `connection.cursor()`.

---

<a name="q14"></a>
## Q14. (Medium) Explain the lifecycle of a QuerySet instance creation inside a Manager.
**Answer:** `Article.objects.filter(x=1)` → the manager calls `get_queryset()` → a new `QuerySet(model, using=self._db)` is created with an empty `Query` → `.filter()` clones it and adds the condition → the clone is returned (still lazy) → SQL runs only when evaluated. Every manager call starts a fresh queryset (no shared cache).

---

<a name="q15"></a>
## Q15. (Easy) How do you implement custom business logic methods inside a manager?
**Answer:** Add methods for table-level operations, e.g. creation with defaults or reporting helpers. Keep row filtering on the QuerySet.

```python
class OrderManager(models.Manager):
    def create_from_cart(self, cart):
        order = self.create(customer=cart.customer, total=cart.total())
        OrderItem.objects.bulk_create([OrderItem(order=order, **i) for i in cart.items()])
        return order
```
Complex workflows often fit better in a service layer.

---

<a name="q16"></a>
## Q16. (Medium) What is the relation between Django managers and the database backend routing?
**Answer:** Managers call the router when they build querysets (`db_for_read`/`db_for_write`). `Model.objects.db_manager("replica")` returns a manager bound to that alias (useful for manager methods like `create_user`), while `Model.objects.using("replica")` gives a queryset on that alias.

---

<a name="q17"></a>
## Q17. (Medium) How do you write a manager that automatically annotates every queryset?
**Answer:**

```python
class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(book_count=Count("books"))
```
Every query now has `book_count`. Usually better as an explicit QuerySet method (`.with_book_count()`) so you only pay for it when needed.

---

<a name="q18"></a>
## Q18. (Medium) What are the performance implications of auto-annotating managers?
**Answer:** Every query — even `get()` by pk, `exists()`, `count()` and admin lists — now includes the JOIN + GROUP BY, which can be much slower. Multiple auto-annotations over different relations can also inflate counts. Prefer opt-in QuerySet methods.

---

<a name="q19"></a>
## Q19. (Easy) How do you use custom managers in django.contrib.admin?
**Answer:** The admin uses the model's **default manager**. To change what the admin shows (e.g. include soft-deleted rows, add `select_related`), override `ModelAdmin.get_queryset()`:

```python
class DocAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Doc.all_objects.select_related("owner")
```

---

<a name="q20"></a>
## Q20. (Medium) What is the purpose of _db attribute in QuerySets and Managers?
**Answer:** `_db` stores the database alias chosen explicitly (`using()` / `db_manager()`). If it's `None`, the router decides at query time. Querysets created from a manager inherit its `_db`.

---

<a name="q21"></a>
## Q21. (Easy) How does Django's as_manager() method convert a QuerySet to a Manager?
**Answer:** `MyQuerySet.as_manager()` builds a Manager class (via `Manager.from_queryset`) that copies the QuerySet's public methods onto the manager, then returns an instance of it. So `Article.objects.published()` works and stays chainable.

---

<a name="q22"></a>
## Q22. (Medium) How do custom managers interact with M2M through tables?
**Answer:** `article.tags.all()` uses the target model's (`Tag`) default manager class, so its filters apply to the M2M results. The through model is a normal model and can have its own managers — query it directly when you need the extra fields (`ArticleTag.objects.filter(article=a).select_related("tag")`).

---

<a name="q23"></a>
## Q23. (Medium) How do you handle manager validation and initialization arguments?
**Answer:** A manager can take arguments in `__init__` (e.g. a status to filter). If it's used in migrations (`use_in_migrations = True`), it must be serializable — implement `deconstruct()` or keep args simple. Validate arguments in `__init__` and raise early.

```python
class StatusManager(models.Manager):
    def __init__(self, status):
        super().__init__()
        self.status = status
    def get_queryset(self):
        return super().get_queryset().filter(status=self.status)
```

---

<a name="q24"></a>
## Q24. (Easy) How do you write tests for custom managers and querysets?
**Answer:** Create a few rows that should and shouldn't match, call the method, assert the results — and optionally the query count.

```python
def test_published(self):
    a = Article.objects.create(status="published")
    Article.objects.create(status="draft")
    self.assertQuerySetEqual(Article.objects.published(), [a])
```

---

<a name="q25"></a>
## Q25. (Medium) How does Django 5.0 handle managers in asynchronous environments?
**Answer:** Managers expose async versions of DB-hitting methods: `await Article.objects.aget(pk=1)`, `acreate()`, `acount()`, `async for a in Article.objects.filter(...)`. Your own custom methods are sync unless you write `async def` versions (wrapping sync logic with `sync_to_async` if it uses transactions).

---

<a name="q26"></a>
## Q26. (Medium) How do you build a manager that routes writes to primary and reads to replica?
**Answer:** Usually a router does this globally. For explicit per-use control:

```python
class ReplicaReadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using("replica")   # reads only

class Report(models.Model):
    objects = models.Manager()          # reads + writes on primary
    replica = ReplicaReadManager()
```
Writes (`save()`/`create()`) still go to the primary through `objects`.

---

<a name="q27"></a>
## Q27. (Hard) Explain the relationship between Manager and Model class preparation.
**Answer:** When the model class is created, each manager's `contribute_to_class()` registers it in `_meta` (with creation order). After the class is fully prepared, Django sets up `_default_manager` and `_base_manager` and installs the manager descriptors. Managers from abstract parents are inherited by children.

---

<a name="q28"></a>
## Q28. (Easy) What is the purpose of contributed managers in django.contrib?
**Answer:** Some contrib apps ship managers with domain helpers: `UserManager` (`create_user`, `create_superuser` — hashes passwords), `ContentTypeManager` (`get_for_model` with caching), `CurrentSiteManager` (filters by current site). Extend them (e.g. a custom user manager) instead of replacing their logic.

---

<a name="q29"></a>
## Q29. (Hard) How do custom managers support prefetch_related queries?
**Answer:** Prefetching a reverse FK/M2M builds its query from the related model's **default manager**, so its filters apply to prefetched results. To prefetch with different rules, pass an explicit queryset: `Prefetch("orders", queryset=Order.all_objects.all())`.

---

<a name="q30"></a>
## Q30. (Medium) How do you dynamically swap model managers at runtime?
**Answer:** Don't reassign managers at runtime (it affects every thread). Instead choose between existing managers (`Model.objects` vs `Model.all_objects`), use `db_manager()` for another database, or use a related manager by name: `obj.related(manager="archived").all()`.

---

<a name="q31"></a>
## Q31. (Medium) Explain how QuerySet.defer interacts with custom manager annotations.
**Answer:** `defer()`/`only()` work on concrete columns; annotations added by the manager are still computed and selected — you can't defer an annotation. If you need a lighter query, start from a manager/QuerySet method without the annotation.

---

<a name="q32"></a>
## Q32. (Medium) How does Django prevent multiple managers from overlapping in model schema?
**Answer:** Managers are just class attributes with no database columns, so they never touch the schema. Name clashes behave like normal Python attributes: a later definition (or a child class) overrides an earlier one. Django's system checks report clashes between managers/fields and reverse accessors where relevant. Give managers distinct names.

---

<a name="q33"></a>
## Q33. (Easy) What is the execution overhead of manager descriptors?
**Answer:** Negligible — accessing `Model.objects` is a simple descriptor lookup returning the manager. Real costs come from what the manager's `get_queryset()` adds (joins, annotations), not from the manager itself.

---

<a name="q34"></a>
## Q34. (Hard) How do you implement a soft delete manager that handles cascades?
**Answer:** Django's cascade only runs on real deletes. In the soft `delete()`, also soft-delete dependents explicitly, inside a transaction (or use a library like `django-safedelete`).

```python
def soft_delete(self):
    with transaction.atomic():
        now = timezone.now()
        self.comments.update(deleted_at=now)
        self.attachments.update(deleted_at=now)
        type(self).all_objects.filter(pk=self.pk).update(deleted_at=now)
```

---

<a name="q35"></a>
## Q35. (Easy) How do you fetch raw SQL output directly from a Manager method?
**Answer:** Use `self.raw()` for model instances, or a cursor for arbitrary results.

```python
class OrderManager(models.Manager):
    def revenue_by_region(self):
        with connection.cursor() as cur:
            cur.execute("SELECT region, SUM(total) FROM shop_order GROUP BY region")
            return cur.fetchall()
```
Always pass values as params.
