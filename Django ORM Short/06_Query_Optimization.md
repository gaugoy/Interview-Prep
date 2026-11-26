# Module 06: Query Optimization (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/06_Query_Optimization.md)

## Table of Contents
1. (Easy) [What is the difference between select_related and prefetch_related?](#q1)
2. (Medium) [When does prefetch_related write a new query, and how is it executed?](#q2)
3. (Medium) [How does the Prefetch object allow customization of prefetching?](#q3)
4. (Easy) [What is the difference between only() and defer(), and what are the risks of using them?](#q4)
5. (Medium) [How does referencing a deferred field trigger database queries?](#q5)
6. (Easy) [What is the performance difference between values() and values_list()?](#q6)
7. (Medium) [How do you implement batch updates using bulk_update() and what are its limits?](#q7)
8. (Medium) [How does bulk_create() work database-wise and when are primary keys returned?](#q8)
9. (Easy) [Why is update() faster than looping and calling save(), and what does it bypass?](#q9)
10. (Easy) [How do you write a query to avoid the N+1 problem on reverse foreign keys?](#q10)
11. (Easy) [How does exists() optimize presence checks compared to count() or len()?](#q11)
12. (Medium) [What is the impact of select_related on outer joins and memory consumption?](#q12)
13. (Medium) [How do you optimize large scale deletions using Django ORM?](#q13)
14. (Easy) [How does django-debug-toolbar identify duplicate and slow queries?](#q14)
15. (Medium) [How do you use Explain() to analyze database query execution plans?](#q15)
16. (Easy) [What is the performance implication of fetching unrelated large text fields?](#q16)
17. (Medium) [How does prefetch_related handle deeply nested relationships?](#q17)
18. (Easy) [What are the limitations of select_related on many-to-many relationships?](#q18)
19. (Medium) [How do you optimize bulk inserts of millions of rows in Django?](#q19)
20. (Medium) [How do you perform batch deletions without violating database constraints?](#q20)
21. (Easy) [What is the database cost of order_by('?') for random row selection?](#q21)
22. (Medium) [How do you implement fast pagination without using OFFSET?](#q22)
23. (Easy) [How does values() affect the generation of model instances?](#q23)
24. (Medium) [How do you run raw SQL queries without bypassing Django's security filters?](#q24)
25. (Medium) [How does Django 5.0's GeneratedField optimize read queries by pre-calculating values?](#q25)
26. (Medium) [How does select_related interact with multi-table inheritance?](#q26)
27. (Medium) [What is the cost of query execution when using values() with prefetch_related?](#q27)
28. (Hard) [Explain the internal caching of prefetched querysets.](#q28)
29. (Medium) [How do you chunk a large QuerySet into small batches for updates?](#q29)
30. (Medium) [Explain how to write a query that prefetches only active items of a relation.](#q30)
31. (Medium) [How does django-cachalot optimize database queries globally?](#q31)
32. (Medium) [What is the database impact of using only() with deep select_related?](#q32)
33. (Hard) [How do you write a custom QuerySet iterator for fast object parsing?](#q33)
34. (Hard) [Explain the performance cost of prefetching polymorphic models.](#q34)
35. (Medium) [How do you identify slow Django queries using PostgreSQL pg_stat_statements?](#q35)
36. (Medium) [How do you catch and prevent N+1 query regressions automatically in tests and CI?](#q36)
37. (Medium) [How do you eliminate N+1 queries in DRF serializers (nested serializers, SerializerMethodField, source='fk.field')?](#q37)
38. (Medium) [Why does filtering across a multi-valued relationship return duplicate rows, and what is the cost of distinct() versus Exists?](#q38)
39. (Medium) [How do you avoid per-row get() or update_or_create() calls in data-sync jobs (in_bulk, dictionary lookups, bulk upserts)?](#q39)

---

<a name="q1"></a>
## Q1. (Easy) What is the difference between select_related and prefetch_related?
**Answer:** Both load related objects up front to avoid N+1 queries.
- `select_related` → one query with a SQL **JOIN**. Only for single-valued relations: forward ForeignKey and OneToOne.
- `prefetch_related` → a **separate query** per relation (`WHERE fk IN (...)`), joined in Python. Works for reverse FK, ManyToMany, generic relations (and FKs too).

```python
Order.objects.select_related("customer").prefetch_related("items")   # 2 queries total
```
**Follow-up:** When prefetch for a FK? → many rows sharing few related objects (avoids repeating wide JOIN data), or when the related data is in another database.

---

<a name="q2"></a>
## Q2. (Medium) When does prefetch_related write a new query, and how is it executed?
**Answer:** It's lazy — nothing runs until the main queryset is evaluated. Then Django runs the main query, collects the parent ids, and runs **one extra query per relation level** (`'items__product'` = 3 queries total). Results are grouped in Python and cached on each parent.
The cache is used by `.all()`, iteration, `len()`, `count()`, `exists()`. Calling `.filter()` / `.order_by()` on the relation creates a **new query per object** (N+1 again).
**Gotcha:** In Django 5.x, `iterator()` with prefetch requires `chunk_size`; the prefetch then runs once per chunk.

---

<a name="q3"></a>
## Q3. (Medium) How does the Prefetch object allow customization of prefetching?
**Answer:** `Prefetch(lookup, queryset=..., to_attr=...)` lets you control the prefetch query — filter, order, `select_related`, `only()`. `to_attr` stores the result as a plain list attribute.

```python
Project.objects.prefetch_related(
    Prefetch("tickets", queryset=Ticket.objects.filter(status="open").select_related("assignee"),
             to_attr="open_tickets"))
```
**Gotcha:** Without `to_attr`, the filtered list replaces the relation cache — `project.tickets.all()` would then return only open tickets.

---

<a name="q4"></a>
## Q4. (Easy) What is the difference between only() and defer(), and what are the risks of using them?
**Answer:** Both load model instances with fewer columns. `only("a", "b")` = load just these (+ pk). `defer("body")` = load everything except these. Useful to skip big text/JSON columns.
**Risk:** a deferred field is still accessible — touching it runs a query **per object**, so in a loop it becomes N+1. If you only need data, `values()` is safer.

---

<a name="q5"></a>
## Q5. (Medium) How does referencing a deferred field trigger database queries?
**Answer:** A deferred field's value is missing from the instance's `__dict__`. Access goes through a descriptor (`DeferredAttribute`), which sees the value is missing and calls `refresh_from_db(fields=[name])` — one `SELECT` by pk for that instance. It's cached afterwards, but it's per instance and per field: 2 deferred fields × 100 rows = 200 queries. Check with `obj.get_deferred_fields()`.

---

<a name="q6"></a>
## Q6. (Easy) What is the performance difference between values() and values_list()?
**Answer:** Same SQL. `values()` returns dicts, `values_list()` returns tuples (slightly cheaper); `flat=True` for one field, `named=True` for namedtuples. The real win of both is **skipping model instance creation**. Pick by the shape you need.
**Tip:** pass a queryset to `__in` instead of building a list — it becomes one subquery: `Reading.objects.filter(device__in=Device.objects.filter(active=True).values("id"))`.

---

<a name="q7"></a>
## Q7. (Medium) How do you implement batch updates using bulk_update() and what are its limits?
**Answer:** Use it when each row gets a **different** value computed in Python. Django sends one `UPDATE ... SET col = CASE WHEN id=1 THEN ... END` per batch.

```python
for t in tickets:
    t.priority = score(t)
Ticket.objects.bulk_update(tickets, ["priority"], batch_size=500)
```
**Limits:** no `save()` or signals, `auto_now` not applied, can't update the pk, big batches = huge CASE statements (set `batch_size`). Same value for all rows → use `queryset.update()` instead.

---

<a name="q8"></a>
## Q8. (Medium) How does bulk_create() work database-wise and when are primary keys returned?
**Answer:** One multi-row `INSERT ... VALUES (...), (...)` per batch. Skips `save()`, signals and M2M; doesn't work for multi-table-inheritance children. PKs are set on the objects only if the backend supports `RETURNING` (PostgreSQL, recent SQLite/MariaDB) — not with `ignore_conflicts=True`.
Upsert: `bulk_create(objs, update_conflicts=True, unique_fields=["code"], update_fields=["name"])` → `ON CONFLICT DO UPDATE`.

---

<a name="q9"></a>
## Q9. (Easy) Why is update() faster than looping and calling save(), and what does it bypass?
**Answer:** `qs.update(...)` is one `UPDATE ... WHERE` in the database. A loop is 1 SELECT + N UPDATEs, and each `save()` rewrites every column (risk of overwriting others' changes). `update()` works with `F()` for race-free increments.
**Bypasses:** `save()`, `pre_save`/`post_save` signals, `auto_now`, model validation — so cache invalidation or audit logic in signals won't run.

---

<a name="q10"></a>
## Q10. (Easy) How do you write a query to avoid the N+1 problem on reverse foreign keys?
**Answer:** Depends on what you need:
- Need the child rows → `prefetch_related("employees")`.
- Need only some children → `Prefetch(..., queryset=..., to_attr=...)`.
- Need only a count → `annotate(n=Count("employees"))` (no child rows loaded).
- Need the latest child → `Subquery` annotation.
`select_related` doesn't work on reverse FKs.

---

<a name="q11"></a>
## Q11. (Easy) How does exists() optimize presence checks compared to count() or len()?
**Answer:**
| Call | SQL | Cost |
|---|---|---|
| `exists()` | `SELECT 1 ... LIMIT 1` | stops at first match |
| `count()` | `SELECT COUNT(*)` | visits all matching rows |
| `len(qs)` | full SELECT | loads every row into Python |

Use `exists()` for yes/no, `count()` for the number, `len()` only if the rows are already loaded.
**Gotcha:** if nothing matches and there's no index, `exists()` still scans the table.

---

<a name="q12"></a>
## Q12. (Medium) What is the impact of select_related on outer joins and memory consumption?
**Answer:** Nullable FK → `LEFT OUTER JOIN`; non-null → `INNER JOIN`. Every joined table adds all its columns to every row, and repeated related rows are duplicated per row — Django also creates a separate related object per row (no identity map). Long chains on wide tables = big rows and memory. Narrow with `only()`, or use `prefetch_related` for FKs with few distinct values.

---

<a name="q13"></a>
## Q13. (Medium) How do you optimize large scale deletions using Django ORM?
**Answer:** `qs.delete()` emulates `on_delete` in Python: it collects related objects, cascades, and sends signals per object. A single fast `DELETE` happens only if there are no signals and nothing references the model (except `DO_NOTHING`); otherwise rows are loaded into memory first.
For large deletes:
1. Delete in small PK batches, each in its own short transaction.
2. Index all FK columns pointing to the table.
3. Avoid delete signals on big child tables.
4. For time-based data, drop/detach old **partitions** instead of deleting rows.

---

<a name="q14"></a>
## Q14. (Easy) How does django-debug-toolbar identify duplicate and slow queries?
**Answer:** It wraps the DB cursor during a request and records every query with time and stack trace. **Similar** = same SQL, different params → N+1. **Duplicate** = same SQL and params → repeated work (cache it). Slow queries are highlighted (`SQL_WARNING_THRESHOLD`) and you can EXPLAIN them. Dev only; for APIs use the browsable API, django-silk, or query-count tests.

---

<a name="q15"></a>
## Q15. (Medium) How do you use Explain() to analyze database query execution plans?
**Answer:** `qs.explain()` shows the database's plan for the exact SQL. `qs.explain(analyze=True)` (PostgreSQL) actually runs the query and shows real timings — use it on staging.
Look for: **Seq Scan** on a big table (missing index), estimated vs actual rows far apart (stale stats → `ANALYZE`), sorts spilling to disk, nested loops with huge loop counts.

```python
print(Shipment.objects.filter(status="in_transit").order_by("-created_at")[:50].explain(analyze=True))
```

---

<a name="q16"></a>
## Q16. (Easy) What is the performance implication of fetching unrelated large text fields?
**Answer:** Every selected column is read from disk, sent over the network, decoded and kept in memory. Large text/JSON values (stored out-of-line in PostgreSQL TOAST) add extra reads and decompression for every row even if unused. Fix: `defer()`/`only()`/`values()` on list views, or move rarely-used blobs to a separate one-to-one table.

---

<a name="q17"></a>
## Q17. (Medium) How does prefetch_related handle deeply nested relationships?
**Answer:** One query per level: `orders__items__product` → orders, then items for those orders, then products. Shared prefixes are fetched once. The risk is fan-out: deeper levels get big `IN` lists and lots of memory. Reduce levels with `select_related` inside a `Prefetch` (e.g. items with their product in one query), and bound the top level with pagination or `iterator(chunk_size=...)`.

---

<a name="q18"></a>
## Q18. (Easy) What are the limitations of select_related on many-to-many relationships?
**Answer:** It doesn't work — Django raises `FieldError`. A JOIN to a many-valued relation would return the parent once per related row, and Django doesn't fold rows back together. Use `prefetch_related` (one query joining the through table). You can still `select_related` the *target's* FKs inside a `Prefetch`, or use `ArrayAgg` (PostgreSQL) for read-only lists.

---

<a name="q19"></a>
## Q19. (Medium) How do you optimize bulk inserts of millions of rows in Django?
**Answer:**
1. Don't build all objects in memory — stream the source and insert in chunks.
2. `bulk_create(batch_size=1000–5000)`, committing per chunk.
3. For very large loads on PostgreSQL, use `COPY` (fastest); on SQL Server, bulk-load tools.
4. For one-off loads into empty tables, create secondary indexes after loading.
5. Run `ANALYZE` afterwards.

---

<a name="q20"></a>
## Q20. (Medium) How do you perform batch deletions without violating database constraints?
**Answer:** Delete **children before parents, in the same transaction**. `queryset.delete()` does this ordering for you. Problems appear with raw SQL or `DO_NOTHING`, because Django's FKs have no DB-level `ON DELETE` — the DB rejects orphaned rows. `PROTECT` raises `ProtectedError`, `RESTRICT` raises `RestrictedError`. On PostgreSQL Django's FKs are checked at commit, so each batch transaction must contain the whole parent + children subtree.

---

<a name="q21"></a>
## Q21. (Easy) What is the database cost of order_by('?') for random row selection?
**Answer:** It becomes `ORDER BY RANDOM()`: the DB generates a random value for **every** matching row and sorts them — a full scan even with `LIMIT 1`. Fine for small tables; on big tables use a cached id list + `random.sample`, `TABLESAMPLE` (PostgreSQL), or an indexed random-key column.

---

<a name="q22"></a>
## Q22. (Medium) How do you implement fast pagination without using OFFSET?
**Answer:** **Keyset (cursor) pagination**: instead of skipping N rows, ask for the rows after the last one seen. `OFFSET 100000` makes the DB read and discard 100k rows; keyset uses an index seek, so every page costs the same and it's stable when new rows arrive.

```python
qs.filter(Q(created_at__lt=ts) | Q(created_at=ts, id__lt=last_id)).order_by("-created_at", "-id")[:50]
```
Needs a unique tie-breaker (`id`) and an index on `(created_at, id)`. Trade-off: no "jump to page N". In DRF: `CursorPagination`.

---

<a name="q23"></a>
## Q23. (Easy) How does values() affect the generation of model instances?
**Answer:** No model instances are created — each row becomes a dict. That skips `__init__`, model state and `post_init` signals, so it's faster and lighter. Field converters still run (JSON decoded, dates timezone-aware). You lose model methods, properties, `get_FOO_display()` and `save()`. Best for read-only work: exports, reports, API payloads.

---

<a name="q24"></a>
## Q24. (Medium) How do you run raw SQL queries without bypassing Django's security filters?
**Answer:**
1. Always pass values as parameters: `Model.objects.raw(sql, [param])` / `cursor.execute(sql, [param])` — never f-strings.
2. Column/table names can't be parameters — whitelist them.
3. Raw SQL skips custom managers, so **re-apply your filters** manually (tenant, soft-delete, permissions) in the WHERE clause.

```python
Ticket.objects.raw("SELECT * FROM helpdesk_ticket WHERE tenant_id = %s AND title ILIKE %s",
                   [tenant_id, f"%{term}%"])
```

---

<a name="q25"></a>
## Q25. (Medium) How does Django 5.0's GeneratedField optimize read queries by pre-calculating values?
**Answer:** `GeneratedField` is a database generated column computed from other columns of the same row. With `db_persist=True` it's stored, so you can **index, filter and sort** on it instead of recomputing an `annotate()` in every query.

```python
line_total = models.GeneratedField(expression=F("quantity") * F("unit_price"),
                                   output_field=models.DecimalField(max_digits=14, decimal_places=2),
                                   db_persist=True)
```
The cost moves to writes; only same-row, deterministic expressions; after `save()` call `refresh_from_db()` to read the new value; adding one to a big table rewrites the table.

---

<a name="q26"></a>
## Q26. (Medium) How does select_related interact with multi-table inheritance?
**Answer:** A child model (e.g. `Server(Asset)`) has its own table linked by a one-to-one `asset_ptr`. Querying the child **always joins the parent** automatically. Going from parent to child (`asset.server`) is a reverse one-to-one — a query per row unless you use `Asset.objects.select_related("server", "laptop")` (LEFT JOINs). That's why MTI is costly; prefer abstract base classes or one table with a type column.

---

<a name="q27"></a>
## Q27. (Medium) What is the cost of query execution when using values() with prefetch_related?
**Answer:** No extra cost — because the prefetch is **silently skipped**. Prefetch needs model instances to attach its cache to; dicts can't hold it. So you get no related data and no error. Using `values("tags__name")` instead returns one row per tag (duplicates). Options: prefetch on instances, `ArrayAgg` (PostgreSQL), or two `values()` queries merged in Python.

---

<a name="q28"></a>
## Q28. (Hard) Explain the internal caching of prefetched querysets.
**Answer:** Results are stored on each parent instance in `_prefetched_objects_cache[relation_name]` (or as a list attribute with `to_attr`). The related manager checks this cache first, so `obj.items.all()` costs no query. It's per instance, per process — not a shared cache.
Invalidation: the related manager's `add/remove/clear/set/create` clear it; `Child.objects.create(parent=obj)` does **not** (stale data); `refresh_from_db()` clears it. To prefetch onto objects you already have: `prefetch_related_objects(list_of_objs, "items")`.

---

<a name="q29"></a>
## Q29. (Medium) How do you chunk a large QuerySet into small batches for updates?
**Answer:** Batch by primary key, not by offset:

```python
last = 0
while ids := list(Customer.objects.filter(pk__gt=last, region__isnull=True)
                  .order_by("pk").values_list("pk", flat=True)[:2000]):
    with transaction.atomic():
        Customer.objects.filter(pk__in=ids).update(region="EMEA")
    last = ids[-1]
```
Short transactions keep locks small, and the job can resume from `last`.
**Gotcha:** offset slicing (`qs[i:i+n]`) skips rows when your update changes which rows match the filter.

---

<a name="q30"></a>
## Q30. (Medium) Explain how to write a query that prefetches only active items of a relation.
**Answer:** Use a filtered `Prefetch` with `to_attr`. Since Django 4.2 you can also slice it to get the latest N per parent (Django uses a window function).

```python
approved = Comment.objects.filter(status="approved").order_by("-created_at")
Post.objects.prefetch_related(
    Prefetch("comments", queryset=approved, to_attr="approved_comments"),
    Prefetch("comments", queryset=approved[:3], to_attr="latest_comments"))
```
Only need a yes/no or a count? Annotate `Exists(...)` / `Count(..., filter=Q(...))` instead.

---

<a name="q31"></a>
## Q31. (Medium) How does django-cachalot optimize database queries globally?
**Answer:** It caches the result of every ORM SELECT (keyed by SQL + params) and invalidates **per table**: any ORM write to a table invalidates all cached queries that use it. Good for read-heavy, rarely-written tables (lookups, config). Bad for write-heavy tables (constant invalidation), and it can't see writes made outside Django (other services, DB jobs) → stale data. Explicit Redis cache-aside is often safer.

---

<a name="q32"></a>
## Q32. (Medium) What is the database impact of using only() with deep select_related?
**Answer:** The JOINs stay the same; only the column list shrinks across the joined tables (Django still adds pks and linking FKs). You save I/O, network and memory, not join work. Rules: deferring a relation you `select_related` raises `FieldError`; touching an unloaded field triggers a query per object. For read-only output, `values()` across the joins is simpler.

```python
Order.objects.select_related("customer").only("id", "total", "customer__name")
```

---

<a name="q33"></a>
## Q33. (Hard) How do you write a custom QuerySet iterator for fast object parsing?
**Answer:** QuerySets turn rows into objects via an *iterable class* (`ModelIterable`, `ValuesIterable`, …). Simplest public approach: `values_list()` + `iterator(chunk_size=...)` and build lightweight objects (dataclass/Pydantic) in a generator. For a reusable, chainable version, subclass `BaseIterable` and set `qs._iterable_class` in a custom QuerySet method — but that's an internal API, so test it on Django upgrades.

```python
def rows(qs):
    for device_id, day, value in qs.values_list("device_id", "day", "value").iterator(chunk_size=5000):
        yield MetricRow(device_id, day, value)
```

---

<a name="q34"></a>
## Q34. (Hard) Explain the performance cost of prefetching polymorphic models.
**Answer:** Related rows live in different tables, so prefetching costs **one query per type**: a GenericForeignKey prefetch runs one `IN` query per content type; django-polymorphic runs one base query + one per subclass (each joining the parent). Nested data per type needs its own `select_related` — Django 5.0's `GenericPrefetch("target", [qs_type_a, qs_type_b])` allows that. For lists/feeds, store display fields (title, type) on the row itself so targets don't need loading.

---

<a name="q35"></a>
## Q35. (Medium) How do you identify slow Django queries using PostgreSQL pg_stat_statements?
**Answer:** The extension aggregates stats per normalised query (`$1` placeholders): calls, total time, mean time, rows, buffer reads.
- Sort by **total time** → what costs the DB most overall (fix first).
- Sort by **mean time** → individually slow queries.
- Huge **calls** with tiny mean → N+1 pattern.
Map queries back to code by their tables/columns (or a route comment added to the SQL); reset stats after a fix to compare.

```sql
SELECT calls, mean_exec_time, total_exec_time, left(query, 80)
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;
```

---

<a name="q36"></a>
## Q36. (Medium) How do you catch and prevent N+1 query regressions automatically in tests and CI?
**Answer:** Count queries in tests with `assertNumQueries`, `CaptureQueriesContext`, or pytest-django's `django_assert_num_queries`. The best N+1 check: run the endpoint with 2 rows and with 20 rows and assert the **query count doesn't change**.

```python
with CaptureQueriesContext(connection) as ctx:
    self.client.get("/api/integrations/")
self.assertEqual(len(ctx.captured_queries), baseline)
```

---

<a name="q37"></a>
## Q37. (Medium) How do you eliminate N+1 queries in DRF serializers (nested serializers, SerializerMethodField, source='fk.field')?
**Answer:** Serializers read attributes per object, so `source="owner.name"`, nested serializers and method fields touching relations each query per row. Fix in the view's `get_queryset()`: `select_related` for FK paths, `prefetch_related` for many-valued ones, `annotate` for counts instead of `SerializerMethodField`. Keep them in sync with a `setup_eager_loading(qs)` method on the serializer that the view always calls.

```python
def get_queryset(self):
    return (Integration.objects.select_related("owner").prefetch_related("tags")
            .annotate(open_incidents=Count("incidents", filter=Q(incidents__resolved_at__isnull=True))))
```

---

<a name="q38"></a>
## Q38. (Medium) Why does filtering across a multi-valued relationship return duplicate rows, and what is the cost of distinct() versus Exists?
**Answer:** `Project.objects.filter(tickets__status="open")` JOINs tickets, so a project with 5 open tickets appears 5 times (and `count()` counts tickets). `distinct()` hides it but makes the DB de-duplicate the whole result (extra sort/hash). Better: `filter(Exists(Ticket.objects.filter(project=OuterRef("pk"), status="open")))` — a semi-join, no duplicates.
**Gotcha:** `filter(a__x=1, a__y=2)` = the same related row; `filter(a__x=1).filter(a__y=2)` = possibly different rows.

---

<a name="q39"></a>
## Q39. (Medium) How do you avoid per-row get() or update_or_create() calls in data-sync jobs (in_bulk, dictionary lookups, bulk upserts)?
**Answer:** `update_or_create()` in a loop = 2–3 queries + a transaction per record. Instead, per chunk:
1. Load existing rows once: `existing = Model.objects.in_bulk(keys, field_name="code")`.
2. Diff in Python → new rows and actually-changed rows.
3. `bulk_create(new)` + `bulk_update(changed, fields)`.
Or on PostgreSQL use one upsert: `bulk_create(objs, update_conflicts=True, unique_fields=["code"], update_fields=[...])`. Keep a unique constraint on the natural key so re-runs stay safe.
