# Module 15: Concurrency & Locking (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/15_Concurrency.md)

## Table of Contents
1. (Easy) [What is the difference between Optimistic and Pessimistic locking?](#q1)
2. (Easy) [How do you implement pessimistic locking in Django using select_for_update()?](#q2)
3. (Medium) [What is the difference between select_for_update(nowait=True) and select_for_update(skip_locked=True)?](#q3)
4. (Medium) [How does select_for_update() behave when using multiple database backends?](#q4)
5. (Medium) [How do you apply locks only on specific related tables using select_for_update(of=(...))?](#q5)
6. (Medium) [What are database transaction isolation levels and how do they impact Django ORM?](#q6)
7. (Easy) [What is a Dirty Read, Non-repeatable Read, and Phantom Read?](#q7)
8. (Medium) [How do you prevent deadlocks in Django when executing concurrent queries?](#q8)
9. (Medium) [How do you implement optimistic concurrency control using a version field in Django?](#q9)
10. (Medium) [What is the performance cost of select_for_update() on high-throughput systems?](#q10)
11. (Medium) [How does Django handle lock timeouts in select_for_update()?](#q11)
12. (Medium) [How does select_for_update() interact with select_related?](#q12)
13. (Easy) [What happens when you call select_for_update() outside of a transaction block?](#q13)
14. (Medium) [How do you handle concurrency in background workers (e.g., Celery) using Django locks?](#q14)
15. (Hard) [How do you implement a distributed lock using Django's database backend?](#q15)
16. (Medium) [What is the lock type used by select_for_update() in PostgreSQL (e.g. FOR UPDATE vs. FOR SHARE)?](#q16)
17. (Medium) [How does skip_locked help in implementing high-throughput queue systems in the database?](#q17)
18. (Medium) [How do you handle transaction serialization failures in Django?](#q18)
19. (Medium) [What is the database locking behavior during bulk updates and creates?](#q19)
20. (Hard) [How do you write tests to simulate database deadlocks and race conditions?](#q20)
21. (Medium) [How does Django handle lock escalation at the database level?](#q21)
22. (Easy) [What is the difference between table-level locks and row-level locks?](#q22)
23. (Easy) [How do you perform concurrent updates using F expressions to avoid race conditions?](#q23)
24. (Medium) [How does Django 5.0 handle select_for_update in async context?](#q24)
25. (Medium) [How do you monitor database locks currently held by Django application processes?](#q25)
26. (Medium) [How do you configure row lock wait limits on a PostgreSQL database wrapper?](#q26)
27. (Medium) [Explain the risk of using select_for_update with pagination.](#q27)
28. (Medium) [How does optimistic locking behave under massive concurrent writes?](#q28)
29. (Medium) [How do you implement a lock that spans multiple requests in Django?](#q29)
30. (Hard) [What is the lock mode of PostgreSQL FOR NO KEY UPDATE?](#q30)
31. (Hard) [How do database locks affect replica sync pipelines?](#q31)
32. (Medium) [How do you verify if a QuerySet has skip_locked set in Python?](#q32)
33. (Hard) [Explain how to write a concurrency test using threading.Thread in Django TestCase.](#q33)
34. (Medium) [What is the lock impact of cascading delete operations?](#q34)
35. (Medium) [How does PostgreSQL Advisory Lock work in Django ORM?](#q35)

---

<a name="q1"></a>
## Q1. (Easy) What is the difference between Optimistic and Pessimistic locking?
**Answer:**
- **Pessimistic** — lock the row before changing it (`select_for_update()`); others wait. Safe, but blocks; good for high-contention data (stock, balances).
- **Optimistic** — don't lock; when saving, check the row wasn't changed (version field). If it was, reject/retry. No waiting; good when conflicts are rare.

---

<a name="q2"></a>
## Q2. (Easy) How do you implement pessimistic locking in Django using select_for_update()?
**Answer:** Inside `atomic()`, select the row with `select_for_update()`; other transactions trying to lock it wait until you commit.

```python
with transaction.atomic():
    item = Item.objects.select_for_update().get(pk=pk)
    if item.stock < qty:
        raise ValueError("Out of stock")
    item.stock -= qty
    item.save(update_fields=["stock"])
```

---

<a name="q3"></a>
## Q3. (Medium) What is the difference between select_for_update(nowait=True) and select_for_update(skip_locked=True)?
**Answer:** `nowait=True` → if a row is already locked, fail immediately with `DatabaseError` instead of waiting. `skip_locked=True` → silently skip locked rows and return the rest — perfect for job queues where workers each grab different rows. You can't use both together.

---

<a name="q4"></a>
## Q4. (Medium) How does select_for_update() behave when using multiple database backends?
**Answer:** PostgreSQL and Oracle support it fully (`nowait`, `skip_locked`, `of`; PostgreSQL also `no_key`). MySQL 8 supports `nowait`/`skip_locked`/`of`. **SQLite ignores it** (no row locks — it locks the whole DB on write). Using an unsupported option raises `NotSupportedError`. So tests on SQLite won't catch locking bugs.

---

<a name="q5"></a>
## Q5. (Medium) How do you apply locks only on specific related tables using select_for_update(of=(...))?
**Answer:** With `select_related`, PostgreSQL locks rows in **all** joined tables by default. `of=` limits it: `"self"` = the main model, or relation names.

```python
Order.objects.select_related("customer").select_for_update(of=("self",))
```
Required when a joined relation is nullable (PostgreSQL can't lock the nullable side of an outer join).

---

<a name="q6"></a>
## Q6. (Medium) What are database transaction isolation levels and how do they impact Django ORM?
**Answer:** They define what a transaction can see of others' changes:
- **Read Committed** (PostgreSQL & Django-MySQL default) — each query sees committed data at that moment.
- **Repeatable Read** — the whole transaction sees one snapshot.
- **Serializable** — behaves as if transactions ran one by one; conflicts raise errors.
Higher levels = fewer anomalies but more serialization failures you must retry. Set via `DATABASES["OPTIONS"]["isolation_level"]`.

---

<a name="q7"></a>
## Q7. (Easy) What is a Dirty Read, Non-repeatable Read, and Phantom Read?
**Answer:**
- **Dirty read** — you see another transaction's *uncommitted* change (doesn't happen in PostgreSQL).
- **Non-repeatable read** — reading the same row twice gives different values because someone committed in between.
- **Phantom read** — re-running a query returns new/missing rows because someone inserted/deleted in between.

---

<a name="q8"></a>
## Q8. (Medium) How do you prevent deadlocks in Django when executing concurrent queries?
**Answer:**
1. Lock rows in a consistent order: `select_for_update().order_by("pk")`.
2. Keep transactions short; lock as late as possible.
3. Touch fewer rows per transaction (batch).
4. Use `F()` updates instead of read-modify-write where possible.
5. Retry the transaction when the DB reports a deadlock.

---

<a name="q9"></a>
## Q9. (Medium) How do you implement optimistic concurrency control using a version field in Django?
**Answer:** Keep a `version` integer; update only if the version is still the one you read.

```python
updated = Document.objects.filter(pk=doc.pk, version=doc.version).update(
    body=new_body, version=F("version") + 1)
if updated == 0:
    raise ConflictError("Someone else changed this document")   # API → 409
```

---

<a name="q10"></a>
## Q10. (Medium) What is the performance cost of select_for_update() on high-throughput systems?
**Answer:** Requests touching the same rows are serialized — they queue behind each other, increasing latency and holding DB connections while waiting. Hot rows (a global counter, one popular product) become a bottleneck, and deadlock risk grows. Keep the locked section tiny, use `F()` updates, `skip_locked` for queues, or redesign hot rows (split counters).

---

<a name="q11"></a>
## Q11. (Medium) How does Django handle lock timeouts in select_for_update()?
**Answer:** Django has no timeout option — by default it waits as long as the DB lets it. Options: `nowait=True` (fail immediately), or set a DB lock timeout for the transaction.

```python
with transaction.atomic():
    connection.cursor().execute("SET LOCAL lock_timeout = '3s'")      # PostgreSQL
    obj = Item.objects.select_for_update().get(pk=pk)
```
(MySQL: `innodb_lock_wait_timeout`.)

---

<a name="q12"></a>
## Q12. (Medium) How does select_for_update() interact with select_related?
**Answer:** On PostgreSQL it locks rows in **every joined table** — you may lock the customer row just to update an order, causing extra contention. Use `of=("self",)` to lock only the main rows. Nullable relations (LEFT JOIN) can't be locked, so `of=` is needed there.

---

<a name="q13"></a>
## Q13. (Easy) What happens when you call select_for_update() outside of a transaction block?
**Answer:** Defining the queryset is fine, but **evaluating** it in autocommit mode raises `TransactionManagementError: select_for_update cannot be used outside of a transaction`. A lock released immediately would be useless, so Django refuses.

---

<a name="q14"></a>
## Q14. (Medium) How do you handle concurrency in background workers (e.g., Celery) using Django locks?
**Answer:**
- Several workers processing rows → `select_for_update(skip_locked=True)` so each grabs different rows.
- Only one instance of a job should run → a distributed lock (Redis lock or PostgreSQL advisory lock).
- Make tasks idempotent (unique constraints, status checks) because tasks can be retried or run twice.

---

<a name="q15"></a>
## Q15. (Hard) How do you implement a distributed lock using Django's database backend?
**Answer:** Options:
- PostgreSQL **advisory lock**: `SELECT pg_try_advisory_lock(key)` — app-defined lock, no table needed.
- A lock table with a unique row per lock name: insert to acquire (IntegrityError = taken), delete to release, plus an expiry column for crashed holders.
- `select_for_update(nowait=True)` on a row representing the resource.
Redis locks are a common alternative if Redis is already available.

---

<a name="q16"></a>
## Q16. (Medium) What is the lock type used by select_for_update() in PostgreSQL (e.g. FOR UPDATE vs. FOR SHARE)?
**Answer:** `select_for_update()` → `FOR UPDATE` (strongest row lock: blocks other updates, deletes and locks). `no_key=True` → `FOR NO KEY UPDATE` (weaker; doesn't block inserts of child rows referencing it). `FOR SHARE` / `FOR KEY SHARE` (read locks) aren't exposed by the ORM — raw SQL needed.

---

<a name="q17"></a>
## Q17. (Medium) How does skip_locked help in implementing high-throughput queue systems in the database?
**Answer:** Each worker selects a batch of pending jobs with `skip_locked=True`, so rows locked by other workers are skipped instead of waited on — workers never block each other or process the same job.

```python
with transaction.atomic():
    jobs = list(Job.objects.select_for_update(skip_locked=True)
                .filter(status="pending").order_by("id")[:10])
    for j in jobs:
        process(j); j.status = "done"; j.save(update_fields=["status"])
```

---

<a name="q18"></a>
## Q18. (Medium) How do you handle transaction serialization failures in Django?
**Answer:** With Repeatable Read/Serializable, PostgreSQL aborts conflicting transactions with a serialization failure (surfaces as `OperationalError`). That's expected: catch it **outside** `atomic()` and retry the whole transaction a few times with backoff. Keep the transaction body free of side effects so retries are safe.

---

<a name="q19"></a>
## Q19. (Medium) What is the database locking behavior during bulk updates and creates?
**Answer:** `update()` / `bulk_update()` lock every affected row until commit — large ones block other writers and can deadlock with concurrent updates in a different order. `bulk_create()` doesn't lock existing rows, but inserts can wait on each other for the same unique key. Batch large operations into small transactions.

---

<a name="q20"></a>
## Q20. (Hard) How do you write tests to simulate database deadlocks and race conditions?
**Answer:** Use `TransactionTestCase` (real commits) and run the competing code in two threads, using a `threading.Barrier`/`Event` so both reach the critical point together. Assert the final state (e.g. stock never negative) or that one side got the expected error. Close connections in each thread at the end. Use PostgreSQL, not SQLite.

---

<a name="q21"></a>
## Q21. (Medium) How does Django handle lock escalation at the database level?
**Answer:** Django doesn't — it's a database behaviour. SQL Server may escalate many row locks into a table lock (around 5,000 locks), blocking everyone; PostgreSQL never escalates. Avoid it by updating in smaller batches.

---

<a name="q22"></a>
## Q22. (Easy) What is the difference between table-level locks and row-level locks?
**Answer:** **Row-level** locks (from UPDATE, DELETE, `SELECT FOR UPDATE`) only block access to those rows — normal for OLTP. **Table-level** locks affect the whole table; heavy ones come from DDL (`ALTER TABLE`, migrations) or `LOCK TABLE` and can block all reads/writes. Normal queries take only light table locks that don't conflict.

---

<a name="q23"></a>
## Q23. (Easy) How do you perform concurrent updates using F expressions to avoid race conditions?
**Answer:** `F()` makes the database do the math, so there's no read-modify-write gap.

```python
Product.objects.filter(pk=pk).update(stock=F("stock") - 1)        # atomic in the DB
Product.objects.filter(pk=pk, stock__gte=1).update(stock=F("stock") - 1)   # + guard
```
In Python, `p.stock -= 1; p.save()` loses updates when two requests run at the same time.

---

<a name="q24"></a>
## Q24. (Medium) How does Django 5.0 handle select_for_update in async context?
**Answer:** It needs a transaction, and `atomic()` isn't supported in async code. Put the locking logic in a sync function and call it with `sync_to_async` so the transaction and lock live on one thread/connection.

---

<a name="q25"></a>
## Q25. (Medium) How do you monitor database locks currently held by Django application processes?
**Answer:** PostgreSQL: `pg_locks` joined with `pg_stat_activity` (who holds/waits, query, `wait_event_type = 'Lock'`), and `pg_blocking_pids(pid)` to find the blocker. Enable `log_lock_waits` to log waits longer than `deadlock_timeout`. Set `application_name` per service in connection options to see which app holds locks.

---

<a name="q26"></a>
## Q26. (Medium) How do you configure row lock wait limits on a PostgreSQL database wrapper?
**Answer:** Set `lock_timeout` for all connections via options, or per transaction with `SET LOCAL`.

```python
DATABASES["default"]["OPTIONS"] = {"options": "-c lock_timeout=5000 -c statement_timeout=30000"}
```
Queries waiting longer than that fail instead of hanging.

---

<a name="q27"></a>
## Q27. (Medium) Explain the risk of using select_for_update with pagination.
**Answer:** Locks last only for one transaction, so you can't "lock a page" across requests — and trying to hold locks while a user pages would block everyone. With LIMIT/OFFSET the set of locked rows shifts as data changes. For batch processing use `skip_locked` + `LIMIT` per transaction; for user edits use optimistic locking.

---

<a name="q28"></a>
## Q28. (Medium) How does optimistic locking behave under massive concurrent writes?
**Answer:** When many users update the same row, most updates fail the version check and retry, wasting work (livelock risk). Optimistic locking suits low-contention data. For hot rows, switch to pessimistic locking, atomic `F()` updates, or a queue that serializes the writes.

---

<a name="q29"></a>
## Q29. (Medium) How do you implement a lock that spans multiple requests in Django?
**Answer:** Don't hold a DB lock across requests. Use an application-level lock: a `locked_by` + `locked_until` column (claimed with a conditional `update()`), or a Redis lock with a TTL. Always add an expiry so a closed browser doesn't lock the record forever. Or use optimistic locking and just detect conflicts on save.

---

<a name="q30"></a>
## Q30. (Hard) What is the lock mode of PostgreSQL FOR NO KEY UPDATE?
**Answer:** A row lock weaker than `FOR UPDATE`: it blocks other updates/deletes of the row, but **not** `FOR KEY SHARE` locks — which PostgreSQL takes when other transactions insert child rows referencing this row. So it avoids blocking FK inserts when you're not changing the key. Django: `select_for_update(no_key=True)`.

---

<a name="q31"></a>
## Q31. (Hard) How do database locks affect replica sync pipelines?
**Answer:** Row locks on the primary aren't replicated, so replica reads aren't blocked by them. But long transactions on the primary delay when their changes appear on replicas, heavy DDL locks *are* replayed (blocking replica queries), and long queries on a replica can conflict with replay — causing either replication lag or cancelled replica queries.

---

<a name="q32"></a>
## Q32. (Medium) How do you verify if a QuerySet has skip_locked set in Python?
**Answer:** Check the query's internal flags (useful in tests):

```python
qs = Job.objects.select_for_update(skip_locked=True)
qs.query.select_for_update               # True
qs.query.select_for_update_skip_locked   # True
```
Or look for `SKIP LOCKED` in captured SQL.

---

<a name="q33"></a>
## Q33. (Hard) Explain how to write a concurrency test using threading.Thread in Django TestCase.
**Answer:** Use `TransactionTestCase` (plain `TestCase` wraps everything in one transaction, so threads won't see its data). Each thread gets its own connection; close it at the end.

```python
def worker():
    try:
        reserve_item(item_id)
    finally:
        connection.close()

threads = [threading.Thread(target=worker) for _ in range(5)]
[t.start() for t in threads]; [t.join() for t in threads]
self.assertEqual(Item.objects.get(pk=item_id).stock, 0)
```

---

<a name="q34"></a>
## Q34. (Medium) What is the lock impact of cascading delete operations?
**Answer:** Deleting a parent also deletes (and locks) every child row in the cascade, all in one transaction — a big delete can lock many rows across tables for a long time and deadlock with concurrent inserts into child tables. Delete in small batches and index the FK columns.

---

<a name="q35"></a>
## Q35. (Medium) How does PostgreSQL Advisory Lock work in Django ORM?
**Answer:** Advisory locks are app-defined locks on a number (not tied to rows). Use them via a cursor (or the `django-pglocks` package). `pg_advisory_xact_lock` is released automatically at transaction end; `pg_try_advisory_lock` doesn't wait.

```python
with transaction.atomic(), connection.cursor() as cur:
    cur.execute("SELECT pg_try_advisory_xact_lock(%s)", [hash_key("nightly-sync")])
    if not cur.fetchone()[0]:
        return            # another instance is running
    run_sync()
```
**Gotcha:** session-level advisory locks don't work with PgBouncer transaction pooling — use the `_xact_` versions.
