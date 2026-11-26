# Module 07: Relationships & Joins (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/07_Relationships.md)

## Table of Contents
1. (Easy) [How does ForeignKey represent relationships at the database level?](#q1)
2. (Easy) [What is the role of related_name and related_query_name in reverse lookups?](#q2)
3. (Easy) [How does ManyToManyField work with automatic join tables?](#q3)
4. (Easy) [How do you define and use a custom ManyToManyField through table?](#q4)
5. (Easy) [What is the difference between OneToOneField and ForeignKey with unique=True?](#q5)
6. (Easy) [How does Django handle cascading delete options (CASCADE, SET_NULL, PROTECT, RESTRICT, DO_NOTHING)?](#q6)
7. (Easy) [How do you resolve circular dependency issues in model relationships?](#q7)
8. (Easy) [How does self-referencing ForeignKey work (e.g. parent-child models)?](#q8)
9. (Easy) [How do you write a query that spans multiple relationships (e.g., filter on grand-child model)?](#q9)
10. (Medium) [What is the performance impact of deep joins across 5+ tables in Django ORM?](#q10)
11. (Medium) [How does Django reuse join tables when chaining filters on relationships?](#q11)
12. (Medium) [How does using a custom through table affect M2M managers and querysets?](#q12)
13. (Medium) [What are the limitations of CASCADE delete on large datasets?](#q13)
14. (Medium) [How do you query models with generic relationships using ContentTypes?](#q14)
15. (Medium) [How do you build a polymorphic relationship in Django?](#q15)
16. (Easy) [What are the database schema implications of using a OneToOneField?](#q16)
17. (Easy) [How do you prevent duplicate rows in M2M through tables using constraints?](#q17)
18. (Easy) [How does Django handle forward and reverse prefetching on relationships?](#q18)
19. (Medium) [What is the difference between select_related and joins at the SQL level?](#q19)
20. (Medium) [How do you design a high-performance tree structure in Django (e.g., MPTT vs. Adjacency List)?](#q20)
21. (Medium) [What is the impact of null=True on foreign keys at the index level?](#q21)
22. (Medium) [How does Django clean up M2M tables when a model instance is deleted?](#q22)
23. (Medium) [How do you prefetch relation attributes on a through model?](#q23)
24. (Medium) [What are the issues when using multi-table inheritance with foreign keys?](#q24)
25. (Medium) [How do you write queries using Django 5.0's GeneratedField on related models?](#q25)
26. (Medium) [Explain the constraint naming strategy for foreign keys in migrations.](#q26)
27. (Hard) [How does Django compile reverse generic relations to SQL?](#q27)
28. (Medium) [What is the performance overhead of using django-mptt at scale?](#q28)
29. (Hard) [How do you configure database-level foreign key constraints to defer validation?](#q29)
30. (Medium) [What is the database cost of cascading updates on key values?](#q30)
31. (Easy) [How do you write a query that checks if a many-to-many relationship is empty?](#q31)
32. (Medium) [How does prefetch_related compile when using values_list() on related fields?](#q32)
33. (Hard) [How do you optimize tree queries using PostgreSQL Common Table Expressions (CTE)?](#q33)
34. (Medium) [What are the risks of using DO_NOTHING cascade option?](#q34)
35. (Hard) [How do you enforce composite foreign keys in Django models?](#q35)

---

<a name="q1"></a>
## Q1. (Easy) How does ForeignKey represent relationships at the database level?
**Answer:** A column `<field>_id` holding the related row's primary key, an index on it, and a foreign-key constraint (on PostgreSQL `DEFERRABLE INITIALLY DEFERRED`). `on_delete` behaviour is handled by Django in Python, not by the DB constraint.

---

<a name="q2"></a>
## Q2. (Easy) What is the role of related_name and related_query_name in reverse lookups?
**Answer:** `related_name` names the reverse accessor on the other model (`customer.orders.all()` instead of `customer.order_set`). `related_query_name` names it in filters (`Customer.objects.filter(order__total__gt=100)`); it defaults to `related_name` if set, otherwise the model name. `related_name="+"` disables the reverse relation.

```python
customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
```

---

<a name="q3"></a>
## Q3. (Easy) How does ManyToManyField work with automatic join tables?
**Answer:** Django creates a hidden join table (e.g. `blog_article_tags`) with an `id`, two FK columns (`article_id`, `tag_id`) and a unique constraint on the pair. You manage links with `article.tags.add()`, `.remove()`, `.set()`, `.clear()`; querying `article.tags.all()` joins through that table.

---

<a name="q4"></a>
## Q4. (Easy) How do you define and use a custom ManyToManyField through table?
**Answer:** Use `through=` when the relationship needs extra data (role, date joined).

```python
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    joined_at = models.DateField(auto_now_add=True)

class Group(models.Model):
    members = models.ManyToManyField(Person, through=Membership)

group.members.add(person, through_defaults={"role": "admin"})
```

---

<a name="q5"></a>
## Q5. (Easy) What is the difference between OneToOneField and ForeignKey with unique=True?
**Answer:** Same database structure (unique FK column). The difference is in Python: `OneToOneField`'s reverse accessor returns **one object** (`user.profile`) and raises `DoesNotExist` if missing; with `ForeignKey(unique=True)` the reverse is a manager (`user.profile_set.first()`). Django also warns you to use `OneToOneField` instead.

---

<a name="q6"></a>
## Q6. (Easy) How does Django handle cascading delete options (CASCADE, SET_NULL, PROTECT, RESTRICT, DO_NOTHING)?
**Answer:**
- `CASCADE` — delete the child too.
- `SET_NULL` — set FK to NULL (needs `null=True`); `SET_DEFAULT` / `SET(...)` similar.
- `PROTECT` — block the delete (`ProtectedError`).
- `RESTRICT` — block, unless the child is also being deleted through another CASCADE path.
- `DO_NOTHING` — Django does nothing; the DB constraint may reject the delete.
All except `DO_NOTHING` are emulated in Python by Django.

---

<a name="q7"></a>
## Q7. (Easy) How do you resolve circular dependency issues in model relationships?
**Answer:** Refer to models by string (`ForeignKey("billing.Invoice", ...)`) so neither module imports the other. Migrations handle the cycle by creating one table first and adding the FK in a later operation. If two apps constantly need each other, consider merging them or moving shared models to a common app.

---

<a name="q8"></a>
## Q8. (Easy) How does self-referencing ForeignKey work (e.g. parent-child models)?
**Answer:** `ForeignKey("self", null=True, related_name="children")` — the FK points to another row of the same table. `node.parent` goes up, `node.children.all()` goes down one level. Fetching a whole tree needs one query per level, a recursive CTE, or a tree library.

---

<a name="q9"></a>
## Q9. (Easy) How do you write a query that spans multiple relationships (e.g., filter on grand-child model)?
**Answer:** Chain field names with `__`; Django adds the JOINs.

```python
Customer.objects.filter(orders__items__product__category="books").distinct()
```
Through multi-valued relations a customer can match several times — add `distinct()` or use `Exists()`.

---

<a name="q10"></a>
## Q10. (Medium) What is the performance impact of deep joins across 5+ tables in Django ORM?
**Answer:** Each join adds planning and execution work; through multi-valued relations rows multiply (needing `distinct`), wide rows grow, and the planner may pick bad join orders. Fix: select only needed columns, index every join column, replace filters on many-valued paths with `Exists`, split into a prefetch, or denormalise/pre-aggregate for read-heavy screens.

---

<a name="q11"></a>
## Q11. (Medium) How does Django reuse join tables when chaining filters on relationships?
**Answer:** Conditions in **one** `filter()` call on a multi-valued relation use the **same join** — they must match the same related row. Separate `filter()` calls on a multi-valued relation create **new joins** — each condition can match a different row.

```python
Blog.objects.filter(entries__title__contains="Django", entries__year=2024)        # same entry
Blog.objects.filter(entries__title__contains="Django").filter(entries__year=2024) # any entries
```
For single-valued relations (FK forward) the join is always reused.

---

<a name="q12"></a>
## Q12. (Medium) How does using a custom through table affect M2M managers and querysets?
**Answer:** Since Django 2.2, `add()`, `create()` and `set()` work with custom through models — pass extra fields via `through_defaults` (required if they have no default). `remove()`/`clear()` delete through rows. You can filter on through fields (`group.members.filter(membership__role="admin")`) or query the through model directly.

---

<a name="q13"></a>
## Q13. (Medium) What are the limitations of CASCADE delete on large datasets?
**Answer:** Because Django emulates CASCADE in Python, deleting one parent with millions of children loads/collects them, fires signals, and deletes in one big transaction — slow, memory-heavy, long locks, replica lag. Delete children in batches first, keep child tables signal-free, index FKs, or drop partitions for time-based data.

---

<a name="q14"></a>
## Q14. (Medium) How do you query models with generic relationships using ContentTypes?
**Answer:** Filter by content type + object id, or add a `GenericRelation` to enable normal reverse filtering.

```python
ct = ContentType.objects.get_for_model(Article)
Comment.objects.filter(content_type=ct, object_id=article.pk)

class Article(models.Model):
    comments = GenericRelation(Comment)
Article.objects.filter(comments__text__icontains="great")
```

---

<a name="q15"></a>
## Q15. (Medium) How do you build a polymorphic relationship in Django?
**Answer:** Options:
- **GenericForeignKey** — point to any model (flexible, no FK integrity).
- **Multiple nullable FKs** + a check constraint that exactly one is set (real FKs, works when types are few).
- **Multi-table inheritance / django-polymorphic** — FK to a base model, get subclasses back.
Pick by how many target types there are and whether you need DB integrity.

---

<a name="q16"></a>
## Q16. (Easy) What are the database schema implications of using a OneToOneField?
**Answer:** A FK column with a **unique** constraint (so one row on each side at most), indexed. If it's the primary key (`primary_key=True`, as in multi-table inheritance), the child table shares the parent's pk value. Splitting a wide table into two 1:1 tables means a JOIN when you need both.

---

<a name="q17"></a>
## Q17. (Easy) How do you prevent duplicate rows in M2M through tables using constraints?
**Answer:** The automatic through table already has a unique pair. For a custom through model add it yourself:

```python
class Meta:
    constraints = [models.UniqueConstraint(fields=["person", "group"], name="uniq_membership")]
```

---

<a name="q18"></a>
## Q18. (Easy) How does Django handle forward and reverse prefetching on relationships?
**Answer:** Forward FK (`order.customer`): `select_related` (JOIN) or `prefetch_related` (`customer_id IN (...)`, one shared object per customer). Reverse FK / M2M (`customer.orders`): only `prefetch_related` — one query `WHERE customer_id IN (...)`, grouped in Python and cached on each parent.

---

<a name="q19"></a>
## Q19. (Medium) What is the difference between select_related and joins at the SQL level?
**Answer:** Both produce a JOIN. `select_related` also **selects the related table's columns** and builds related objects. A filter on a relation (`filter(customer__country="IN")`) only joins to apply the WHERE — related columns aren't selected, so accessing `order.customer` still queries unless you also `select_related`.

---

<a name="q20"></a>
## Q20. (Medium) How do you design a high-performance tree structure in Django (e.g., MPTT vs. Adjacency List)?
**Answer:**
- **Adjacency list** (`parent` FK) — simple, cheap writes; subtree reads need recursion/CTE.
- **MPTT / nested sets** (django-mptt) — fast subtree reads, but inserts/moves update many rows.
- **Materialized path** (django-treebeard) — path string like `0001.0003`; fast subtree via prefix.
- **Closure table** — table of all ancestor/descendant pairs; fast reads, more storage.
Read-heavy, rarely changing trees → MPTT/path; write-heavy → adjacency list + recursive CTE.

---

<a name="q21"></a>
## Q21. (Medium) What is the impact of null=True on foreign keys at the index level?
**Answer:** The FK column still gets an index, and NULLs are stored in it. If most rows are NULL, the index is mostly wasted — a partial index on non-null values is smaller. Nullable FKs also make `select_related` use LEFT OUTER JOINs.

---

<a name="q22"></a>
## Q22. (Medium) How does Django clean up M2M tables when a model instance is deleted?
**Answer:** Rows in the through table have FKs to both sides with CASCADE, so deleting either object deletes its through rows (Django's Collector handles it). The other side's objects are not deleted. `m2m_changed` signals are **not** sent for this cleanup.

---

<a name="q23"></a>
## Q23. (Medium) How do you prefetch relation attributes on a through model?
**Answer:** Prefetch the **through** relation (not the M2M) so you get its extra fields, and `select_related` the target inside it.

```python
groups = Group.objects.prefetch_related(
    Prefetch("membership_set", queryset=Membership.objects.select_related("person")))
for m in groups[0].membership_set.all():
    print(m.person.name, m.role)
```

---

<a name="q24"></a>
## Q24. (Medium) What are the issues when using multi-table inheritance with foreign keys?
**Answer:** A FK to the parent model can point to any child, but you get a parent object (extra query/`select_related` to reach the child). A FK to a child means every access joins the parent table. Deletes cascade across parent and child tables. Mixing many MTI levels with FKs quickly creates heavy joins.

---

<a name="q25"></a>
## Q25. (Medium) How do you write queries using Django 5.0's GeneratedField on related models?
**Answer:** Treat it like any column: filter/order across the relation, e.g. `Order.objects.filter(lines__line_total__gte=1000)` or `select_related` to read it. It's indexable if stored. A GeneratedField itself can't reference **related** model fields — only columns of its own row.

---

<a name="q26"></a>
## Q26. (Medium) Explain the constraint naming strategy for foreign keys in migrations.
**Answer:** Django generates FK constraint names from the table, column, a short hash and the target, like `shop_order_customer_id_1a2b3c4d_fk_shop_customer_id`, truncated to the DB's name length limit. The hash keeps names unique and stable. You rarely need them, except for raw SQL or debugging migrations.

---

<a name="q27"></a>
## Q27. (Hard) How does Django compile reverse generic relations to SQL?
**Answer:** A `GenericRelation` filter becomes a JOIN on **both** columns:

```sql
INNER JOIN comments_comment ON (blog_article.id = comments_comment.object_id
                                AND comments_comment.content_type_id = 7)
```
That's why `(content_type, object_id)` should have a composite index, and `object_id` should match the target pk type to avoid casts.

---

<a name="q28"></a>
## Q28. (Medium) What is the performance overhead of using django-mptt at scale?
**Answer:** Reads (descendants, ancestors) are fast single queries using `lft`/`rght` ranges. Writes are costly: inserting or moving a node updates `lft/rght` of many rows in the tree and locks them, so heavy concurrent writes contend. Rebuilding big trees is slow. Good for mostly-read trees (categories), not for frequently changing ones.

---

<a name="q29"></a>
## Q29. (Hard) How do you configure database-level foreign key constraints to defer validation?
**Answer:** On PostgreSQL, Django's FKs are already `DEFERRABLE INITIALLY DEFERRED` — checked at commit, so inside a transaction you can temporarily have rows pointing to not-yet-inserted parents. For unique constraints use `UniqueConstraint(..., deferrable=models.Deferrable.DEFERRED)`. MySQL doesn't support deferred constraints.

---

<a name="q30"></a>
## Q30. (Medium) What is the database cost of cascading updates on key values?
**Answer:** Django doesn't cascade primary-key changes: if you change a pk, child FKs still point to the old value (or the DB constraint fails). Changing keys means updating every child row — expensive and lock-heavy. Avoid mutable primary keys; use surrogate (auto/UUID) keys and keep business codes in separate unique columns.

---

<a name="q31"></a>
## Q31. (Easy) How do you write a query that checks if a many-to-many relationship is empty?
**Answer:**

```python
Article.objects.filter(tags__isnull=True)                         # LEFT JOIN, no tags
Article.objects.filter(~Exists(Article.tags.through.objects.filter(article=OuterRef("pk"))))
```
For one object: `not article.tags.exists()`.

---

<a name="q32"></a>
## Q32. (Medium) How does prefetch_related compile when using values_list() on related fields?
**Answer:** It doesn't combine: `prefetch_related` is ignored with `values_list()` (needs model instances). `values_list("tags__name")` itself is a JOIN returning one row per tag. For one row per parent with related values, use `ArrayAgg` (PostgreSQL) or two queries merged in Python.

---

<a name="q33"></a>
## Q33. (Hard) How do you optimize tree queries using PostgreSQL Common Table Expressions (CTE)?
**Answer:** A recursive CTE fetches a whole subtree in one query. Django has no CTE API — use raw SQL or the `django-cte` package.

```python
Category.objects.raw("""
    WITH RECURSIVE tree AS (
        SELECT * FROM shop_category WHERE id = %s
        UNION ALL
        SELECT c.* FROM shop_category c JOIN tree t ON c.parent_id = t.id)
    SELECT * FROM tree""", [root_id])
```
Index `parent_id`.

---

<a name="q34"></a>
## Q34. (Medium) What are the risks of using DO_NOTHING cascade option?
**Answer:** Django does nothing on delete, so the database FK constraint will reject deleting a parent that still has children (`IntegrityError` at commit), or, if there's no constraint (`db_constraint=False`), you get orphan rows pointing to missing parents. Only use it when the DB or your own code handles cleanup.

---

<a name="q35"></a>
## Q35. (Hard) How do you enforce composite foreign keys in Django models?
**Answer:** Django doesn't support composite foreign keys (Django 5.2 added composite **primary** keys, but FKs to them aren't supported). Options: use a surrogate pk on the target and a normal FK; keep the two columns + a `UniqueConstraint` on the target and add the composite FK constraint with `RunSQL`; or the private `ForeignObject` API (advanced, unofficial).
