# Module 12: Database Indexing & Constraints (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/12_Indexing.md)

## Table of Contents
1. (Easy) [What is a database index and how do you declare it in Django?](#q1)
2. (Easy) [What is the difference between db_index=True on a field and indexes in Meta?](#q2)
3. (Medium) [How does a B-Tree index work under the hood?](#q3)
4. (Medium) [What is a Partial Index and how do you implement it in Django?](#q4)
5. (Medium) [What is a Functional Index and how do you implement it (e.g. indexing lowercase email)?](#q5)
6. (Easy) [What is a Composite (multi-column) Index and how does the column order matter?](#q6)
7. (Easy) [How does Django 5.0 implement unique constraints using UniqueConstraint in Meta?](#q7)
8. (Medium) [What is the difference between a unique database index and a unique constraint?](#q8)
9. (Medium) [How do you implement partial unique constraints in Django?](#q9)
10. (Easy) [How does indexing affect INSERT, UPDATE, and DELETE performance?](#q10)
11. (Medium) [How do you identify missing indexes in a production database?](#q11)
12. (Hard) [How does Django compile functional index expressions to SQL?](#q12)
13. (Medium) [What are the indexing strategies for JSONFields in PostgreSQL (GIN vs. B-Tree)?](#q13)
14. (Medium) [How does indexing affect foreign key lookups and cascading deletes?](#q14)
15. (Medium) [What is the risk of having too many indexes on a table?](#q15)
16. (Easy) [How does Django handle index renaming and deletion in migrations?](#q16)
17. (Medium) [How do you create an index concurrently in PostgreSQL without locking the table?](#q17)
18. (Medium) [What are covering indexes (indexes with INCLUDE columns) and does Django support them?](#q18)
19. (Medium) [How do you implement text search indexes (e.g., GinIndex, GiSTIndex) in Django?](#q19)
20. (Medium) [How does query optimizer use indexes when executing ORM queries?](#q20)
21. (Medium) [What is the performance difference between a clustered index and a non-clustered index?](#q21)
22. (Easy) [How do you enforce database-level validation using CheckConstraint?](#q22)
23. (Medium) [What is the index usage difference between LIKE queries and exact matches?](#q23)
24. (Easy) [How do you inspect if a Django index is being used by the database?](#q24)
25. (Medium) [How do you add database indexes on a through table in a ManyToMany relationship?](#q25)
26. (Medium) [How do unique constraints validate case insensitivity in PostgreSQL?](#q26)
27. (Hard) [What is the internal design of Index and Constraint classes?](#q27)
28. (Medium) [How does PostgreSQL handle NULL values in unique constraints?](#q28)
29. (Hard) [What is index bloat and how do you resolve it on active production tables?](#q29)
30. (Hard) [Explain the role of OpClass in composite indexes.](#q30)
31. (Medium) [How do check constraints interact with bulk_create?](#q31)
32. (Medium) [What is the execution cost of GIN index lookups?](#q32)
33. (Medium) [How do you drop an index safely without causing write delays?](#q33)
34. (Medium) [How do composite constraints validate multi-column logic?](#q34)
35. (Easy) [Explain how to write a unique constraint with a custom error message in Django 5.0.](#q35)

---

<a name="q1"></a>
## Q1. (Easy) What is a database index and how do you declare it in Django?
**Answer:** A separate sorted structure that lets the DB find rows without scanning the whole table — like a book's index. Faster reads on the indexed columns, slightly slower writes.

```python
email = models.EmailField(db_index=True)
class Meta:
    indexes = [models.Index(fields=["status", "-created_at"], name="order_status_created_idx")]
```

---

<a name="q2"></a>
## Q2. (Easy) What is the difference between db_index=True on a field and indexes in Meta?
**Answer:** `db_index=True` makes a simple single-column index with an auto-generated name. `Meta.indexes` supports multi-column, partial (`condition`), functional (expressions), covering (`include`), other index types (GIN, GiST, BRIN) and explicit names. Use `Meta.indexes` for anything beyond one column.

---

<a name="q3"></a>
## Q3. (Medium) How does a B-Tree index work under the hood?
**Answer:** A balanced tree of sorted keys: the DB walks from the root down to a leaf in a few steps (O(log n)), and leaves are linked in order, so it supports `=`, `<`, `>`, `BETWEEN`, sorting and prefix `LIKE 'abc%'`. Each leaf entry points to the table row. It's the default index type everywhere.

---

<a name="q4"></a>
## Q4. (Medium) What is a Partial Index and how do you implement it in Django?
**Answer:** An index on only the rows matching a condition — smaller and faster when queries always target that subset (e.g. pending jobs).

```python
models.Index(fields=["created_at"], condition=Q(status="pending"), name="pending_jobs_idx")
```
The query must include the same condition. PostgreSQL and SQLite support it.

---

<a name="q5"></a>
## Q5. (Medium) What is a Functional Index and how do you implement it (e.g. indexing lowercase email)?
**Answer:** An index on an expression instead of a raw column, so queries filtering on that expression can use it.

```python
from django.db.models.functions import Lower
class Meta:
    indexes = [models.Index(Lower("email"), name="user_email_lower_idx")]
# used by: User.objects.filter(email__iexact=...)  or  annotate(e=Lower("email")).filter(e=...)
```

---

<a name="q6"></a>
## Q6. (Easy) What is a Composite (multi-column) Index and how does the column order matter?
**Answer:** One index on several columns, sorted by the first, then the second, etc. It helps queries that use the **leftmost** columns: an index on `(customer_id, created_at)` helps `customer_id = ?` and `customer_id = ? ORDER BY created_at`, but not `created_at` alone. Put equality filters first, then range/sort columns.

---

<a name="q7"></a>
## Q7. (Easy) How does Django 5.0 implement unique constraints using UniqueConstraint in Meta?
**Answer:** `UniqueConstraint` in `Meta.constraints` creates a unique constraint/index in the DB. It supports multiple fields, `condition` (partial), expressions (`Lower("email")`), `nulls_distinct` (5.0, PostgreSQL 15+), `deferrable`, and custom `violation_error_message`/`violation_error_code` used by `full_clean()`.

```python
models.UniqueConstraint(fields=["tenant", "code"], name="uniq_tenant_code")
```

---

<a name="q8"></a>
## Q8. (Medium) What is the difference between a unique database index and a unique constraint?
**Answer:** Both prevent duplicates, and in PostgreSQL a unique constraint is implemented with a unique index. The constraint is the logical rule (can be referenced by foreign keys, can be deferrable); a unique index is the physical structure (can be partial or on expressions). Django creates a unique index when you use `condition` or expressions.

---

<a name="q9"></a>
## Q9. (Medium) How do you implement partial unique constraints in Django?
**Answer:**

```python
models.UniqueConstraint(fields=["user"], condition=Q(is_default=True), name="one_default_address")
```
Only rows matching the condition must be unique — e.g. one default address per user, unique email only among non-deleted users.

---

<a name="q10"></a>
## Q10. (Easy) How does indexing affect INSERT, UPDATE, and DELETE performance?
**Answer:** Every index must be updated on each write: INSERT adds an entry to every index; UPDATE touches indexes of changed columns (PostgreSQL may avoid it with HOT updates if no indexed column changed); DELETE leaves dead entries to clean up. More indexes = slower writes, more storage and WAL.

---

<a name="q11"></a>
## Q11. (Medium) How do you identify missing indexes in a production database?
**Answer:** Find slow/heavy queries in `pg_stat_statements` and run `EXPLAIN ANALYZE` — look for Seq Scans on big tables with selective filters. Check `pg_stat_user_tables` for tables with high `seq_scan` and few `idx_scan`. Also check that every FK and common filter/order column is indexed.

---

<a name="q12"></a>
## Q12. (Hard) How does Django compile functional index expressions to SQL?
**Answer:** The expressions are resolved against the model like a query and compiled to SQL inside `CREATE INDEX`, with values inlined (DDL can't use parameters):

```sql
CREATE INDEX "user_email_lower_idx" ON "auth_user" ((LOWER("email")));
```
The expression must be deterministic (immutable) on PostgreSQL.

---

<a name="q13"></a>
## Q13. (Medium) What are the indexing strategies for JSONFields in PostgreSQL (GIN vs. B-Tree)?
**Answer:**
- **GIN** on the whole column → fast `contains` (`@>`), `has_key`, `has_any_keys` across any keys.
- **B-tree expression index** on one key (`KT("data__status")`) → fast equality/range/sort on that key; smaller.
Choose B-tree for one or two hot keys, GIN for flexible key/containment queries.

---

<a name="q14"></a>
## Q14. (Medium) How does indexing affect foreign key lookups and cascading deletes?
**Answer:** Django indexes FK columns by default. Without that index, every `customer.orders.all()` and every delete of a parent (finding children to cascade/check) scans the whole child table. Keep FK indexes unless the column is the first column of another composite index.

---

<a name="q15"></a>
## Q15. (Medium) What is the risk of having too many indexes on a table?
**Answer:** Slower writes (each index updated), more disk and memory (indexes compete for cache), more WAL and replication lag, longer VACUUM and backups, and sometimes worse plans. Remove unused or duplicate indexes (check `idx_scan = 0` in `pg_stat_user_indexes`).

---

<a name="q16"></a>
## Q16. (Easy) How does Django handle index renaming and deletion in migrations?
**Answer:** Removing an index from `Meta.indexes` generates `RemoveIndex`; changing its name generates `RenameIndex` (Django 4.1+), which renames it without rebuilding. Removing `db_index=True` generates an `AlterField` that drops the index.

---

<a name="q17"></a>
## Q17. (Medium) How do you create an index concurrently in PostgreSQL without locking the table?
**Answer:** Use `AddIndexConcurrently` in a non-atomic migration — builds the index without blocking writes (slower, can't run in a transaction).

```python
from django.contrib.postgres.operations import AddIndexConcurrently
class Migration(migrations.Migration):
    atomic = False
    operations = [AddIndexConcurrently("order", models.Index(fields=["email"], name="order_email_idx"))]
```
If it fails it leaves an INVALID index — drop and retry.

---

<a name="q18"></a>
## Q18. (Medium) What are covering indexes (indexes with INCLUDE columns) and does Django support them?
**Answer:** A covering index stores extra columns in the index leaves, so a query can be answered from the index alone (index-only scan) without reading the table. Django supports it on PostgreSQL:

```python
models.Index(fields=["customer"], include=["total", "status"], name="order_cust_cover_idx")
```

---

<a name="q19"></a>
## Q19. (Medium) How do you implement text search indexes (e.g., GinIndex, GiSTIndex) in Django?
**Answer:** For full-text search, index a `SearchVector` (or a stored `SearchVectorField`) with GIN; for fuzzy `icontains`/similarity, a trigram GIN index (`pg_trgm`).

```python
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
class Meta:
    indexes = [GinIndex(SearchVector("title", "body", config="english"), name="article_search_idx"),
               GinIndex(fields=["title"], opclasses=["gin_trgm_ops"], name="article_title_trgm")]
```

---

<a name="q20"></a>
## Q20. (Medium) How does query optimizer use indexes when executing ORM queries?
**Answer:** The planner estimates the cost of each option using table statistics: seq scan vs index scan vs bitmap scan vs index-only scan. It uses an index when the filter is **selective** (returns a small fraction of rows) and the condition matches the index (leftmost columns, same expression). For low-selectivity filters, a seq scan can be cheaper and is chosen on purpose.

---

<a name="q21"></a>
## Q21. (Medium) What is the performance difference between a clustered index and a non-clustered index?
**Answer:** A **clustered** index stores the table rows themselves in index order (MySQL InnoDB primary key, SQL Server clustered index) — range scans on it are very fast. **Non-clustered** indexes point to rows elsewhere, needing an extra lookup. PostgreSQL has no maintained clustered index (`CLUSTER` reorders once). This is why random UUID primary keys hurt InnoDB/SQL Server inserts.

---

<a name="q22"></a>
## Q22. (Easy) How do you enforce database-level validation using CheckConstraint?
**Answer:**

```python
class Meta:
    constraints = [models.CheckConstraint(condition=Q(quantity__gte=1), name="qty_positive")]
```
The DB rejects invalid rows from any source (raw SQL, bulk operations) with `IntegrityError`; `full_clean()` validates it too. (`check=` instead of `condition=` in Django ≤ 5.0.)

---

<a name="q23"></a>
## Q23. (Medium) What is the index usage difference between LIKE queries and exact matches?
**Answer:** Exact match (`=`) uses a normal B-tree. `startswith` (`LIKE 'abc%'`) can use a B-tree — on PostgreSQL Django adds an extra `varchar_pattern_ops` index for indexed `CharField`s for this. `contains`/`icontains` (`'%abc%'`) can't use a B-tree → full scan; use a trigram GIN index or full-text search.

---

<a name="q24"></a>
## Q24. (Easy) How do you inspect if a Django index is being used by the database?
**Answer:** Run `qs.explain()` and look for `Index Scan using <name>`. Over time, check `pg_stat_user_indexes.idx_scan` — an index that stays at 0 isn't used and may be dropped.

---

<a name="q25"></a>
## Q25. (Medium) How do you add database indexes on a through table in a ManyToMany relationship?
**Answer:** The automatic through table already has FK indexes and a unique pair. For extra indexes, use a custom `through` model and declare `Meta.indexes` there.

```python
class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [models.Index(fields=["tag", "-added_at"], name="tag_added_idx")]
```

---

<a name="q26"></a>
## Q26. (Medium) How do unique constraints validate case insensitivity in PostgreSQL?
**Answer:** A normal unique constraint is case-sensitive (`Ann@x.com` ≠ `ann@x.com`). For case-insensitive uniqueness use an expression constraint `UniqueConstraint(Lower("email"), name=...)`, or a `citext` column, or a non-deterministic collation (`db_collation`).

---

<a name="q27"></a>
## Q27. (Hard) What is the internal design of Index and Constraint classes?
**Answer:** Both are small objects stored in `Meta` that know how to generate their DDL: `create_sql()` / `remove_sql()` called by the schema editor, and `deconstruct()` so migrations can serialize them. Constraints also implement `validate()` (used by `full_clean()`). Subclasses like `GinIndex`, `ExclusionConstraint` override the SQL template.

---

<a name="q28"></a>
## Q28. (Medium) How does PostgreSQL handle NULL values in unique constraints?
**Answer:** By default NULLs are considered **distinct**, so many rows can have NULL in a unique column. PostgreSQL 15+ supports `NULLS NOT DISTINCT` → only one NULL allowed; in Django: `UniqueConstraint(fields=["code"], nulls_distinct=False, name=...)` (5.0+).

---

<a name="q29"></a>
## Q29. (Hard) What is index bloat and how do you resolve it on active production tables?
**Answer:** In PostgreSQL, updates and deletes leave dead index entries; VACUUM marks space reusable but doesn't shrink the index, so heavily updated indexes grow larger than needed (bloat) → more I/O and memory. Fix with `REINDEX INDEX CONCURRENTLY` (PostgreSQL 12+) or `pg_repack`, and prevent it with well-tuned autovacuum.

---

<a name="q30"></a>
## Q30. (Hard) Explain the role of OpClass in composite indexes.
**Answer:** An operator class tells the index which operators it supports for a column (e.g. `varchar_pattern_ops` for `LIKE 'x%'`, `gin_trgm_ops` for trigram search). Django's `OpClass` (4.1+) sets one per expression in an index:

```python
from django.contrib.postgres.indexes import OpClass
models.Index(OpClass(Lower("name"), name="varchar_pattern_ops"), name="name_prefix_idx")
```
For plain columns you can use `opclasses=[...]` with `fields`.

---

<a name="q31"></a>
## Q31. (Medium) How do check constraints interact with bulk_create?
**Answer:** `bulk_create()` skips model validation, so Django doesn't check constraints first — but the **database** still enforces them: one bad row makes the whole batch fail with `IntegrityError`. Validate rows beforehand (e.g. `full_clean()` per object) if you need a clean error per row.

---

<a name="q32"></a>
## Q32. (Medium) What is the execution cost of GIN index lookups?
**Answer:** GIN lookups are fast for containment/full-text/trigram queries, but writes are expensive (each value is split into many index entries). PostgreSQL buffers new entries in a pending list (`fastupdate`), which makes some reads slower until it's merged. GIN indexes are also large. Good for read-heavy search columns.

---

<a name="q33"></a>
## Q33. (Medium) How do you drop an index safely without causing write delays?
**Answer:** Use `DROP INDEX CONCURRENTLY` — in Django `RemoveIndexConcurrently` (non-atomic migration). A plain `DROP INDEX` takes an exclusive lock and waits behind running queries. Before dropping, confirm it's unused (`idx_scan`) and not backing a constraint.

---

<a name="q34"></a>
## Q34. (Medium) How do composite constraints validate multi-column logic?
**Answer:** A `UniqueConstraint` over several fields checks the **combination**; a `CheckConstraint` with `Q` objects can compare columns (`Q(end__gt=F("start"))`) or express "if A then B" logic (`Q(status="shipped", shipped_at__isnull=False) | ~Q(status="shipped")`). For "no overlapping ranges" on PostgreSQL, use `ExclusionConstraint`.

---

<a name="q35"></a>
## Q35. (Easy) Explain how to write a unique constraint with a custom error message in Django 5.0.
**Answer:**

```python
models.UniqueConstraint(fields=["tenant", "email"], name="uniq_tenant_email",
                        violation_error_message="This email is already registered for this tenant.",
                        violation_error_code="duplicate_email")
```
The message/code appear in `ValidationError` from `full_clean()` (ModelForms, admin). `violation_error_code` is new in 5.0.
