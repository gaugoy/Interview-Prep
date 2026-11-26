# Module 08: Database Transactions (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/08_Transactions.md)

## Table of Contents
1. (Easy) [How does transaction.atomic() work internally?](#q1)
2. (Easy) [What is the difference between database-level autocommit and Django's transaction mode?](#q2)
3. (Medium) [How does Django manage savepoints in nested transaction.atomic() blocks?](#q3)
4. (Easy) [How do you roll back a transaction manually inside an atomic block?](#q4)
5. (Medium) [What are the side effects of catching database exceptions inside atomic blocks?](#q5)
6. (Easy) [How does transaction.on_commit() work and why is it crucial for task queues (e.g., Celery)?](#q6)
7. (Medium) [What happens to database connections when an atomic block raises an exception?](#q7)
8. (Medium) [How do you implement transaction-level isolation levels in Django?](#q8)
9. (Medium) [What is the performance impact of using large atomic blocks in production?](#q9)
10. (Medium) [How do you handle nested transactions with multiple database connections?](#q10)
11. (Hard) [Explain how database savepoints can exhaust PostgreSQL transaction ID limits.](#q11)
12. (Medium) [How does Django prevent transactional deadlocks when executing concurrent transactions?](#q12)
13. (Medium) [What happens when you mix non-database operations (like API calls) inside atomic blocks?](#q13)
14. (Medium) [How do you write tests that require real database commits instead of rollbacks?](#q14)
15. (Easy) [What is the difference between TransactionTestCase and TestCase in Django testing?](#q15)
16. (Medium) [How does transaction.atomic() handle threading?](#q16)
17. (Medium) [What is the risk of using autocommit=False in Django database configuration?](#q17)
18. (Easy) [How do you execute raw SQL transaction commands inside Django?](#q18)
19. (Easy) [How does atomic interact with select_for_update?](#q19)
20. (Easy) [What happens if the application crashes in the middle of an atomic block?](#q20)
21. (Medium) [How do you safely retry failed transactions due to serialization errors?](#q21)
22. (Medium) [How does Django 5.0 handle asynchronous transaction management?](#q22)
23. (Hard) [What is the impact of connection pooling on transaction state cleanup?](#q23)
24. (Medium) [How do you handle multi-database transaction routing?](#q24)
25. (Hard) [How do you implement 2-phase commit concepts using Django ORM?](#q25)
26. (Medium) [How does transaction.on_commit() handle nested transaction blocks?](#q26)
27. (Medium) [What is the impact of transaction.atomic() on database connection lifetime?](#q27)
28. (Medium) [How do you inspect the active transaction state using django.db.transaction?](#q28)
29. (Medium) [Explain the interaction between transaction commits and database triggers.](#q29)
30. (Easy) [How does Django handle transaction rollbacks on MySQL MyISAM tables?](#q30)
31. (Medium) [What is the difference between SELECT FOR UPDATE and SELECT FOR SHARE in transactions?](#q31)
32. (Medium) [How do you write transactional tests with database-level isolation mocks?](#q32)
33. (Hard) [Explain the role of atomic block savepoint creation logic.](#q33)
34. (Medium) [How do you monitor transaction execution duration in production APMs?](#q34)
35. (Medium) [What is the impact of database connection disconnect on active transactions?](#q35)
36. (Medium) [How does Django handle the ACID properties of a database transaction? ⭐ Asked in my interview](#q36)

---

<a name="q1"></a>
## Q1. (Easy) How does transaction.atomic() work internally?
**Answer:** The outermost `atomic()` starts a transaction (turns autocommit off → `BEGIN`). A nested `atomic()` creates a **savepoint**. On normal exit: outer → `COMMIT`, inner → `RELEASE SAVEPOINT`. On exception: outer → `ROLLBACK`, inner → `ROLLBACK TO SAVEPOINT`, and the exception continues upward. Works as a decorator or context manager.

```python
with transaction.atomic():
    order.save()
    Payment.objects.create(order=order, amount=order.total)
```

---

<a name="q2"></a>
## Q2. (Easy) What is the difference between database-level autocommit and Django's transaction mode?
**Answer:** Django runs in **autocommit** by default: every query is committed immediately. Inside `atomic()` Django switches autocommit off so several queries commit or roll back together. `ATOMIC_REQUESTS = True` wraps every view in one transaction (simple, but transactions last the whole request).

---

<a name="q3"></a>
## Q3. (Medium) How does Django manage savepoints in nested transaction.atomic() blocks?
**Answer:** Each nested `atomic()` creates a savepoint. If the inner block fails, only its work is undone (`ROLLBACK TO SAVEPOINT`) and the outer transaction can continue — if you catch the exception outside the inner block. If the inner block succeeds, the savepoint is released; nothing is committed until the outermost block exits. `atomic(savepoint=False)` skips the savepoint (an inner failure then breaks the whole transaction).

---

<a name="q4"></a>
## Q4. (Easy) How do you roll back a transaction manually inside an atomic block?
**Answer:** Either raise an exception (cleanest), or mark it for rollback without raising:

```python
with transaction.atomic():
    do_work()
    if not valid:
        transaction.set_rollback(True)     # rolled back when the block exits
```
There's also the low-level savepoint API: `sid = transaction.savepoint()` → `transaction.savepoint_rollback(sid)`.

---

<a name="q5"></a>
## Q5. (Medium) What are the side effects of catching database exceptions inside atomic blocks?
**Answer:** After a DB error the transaction is broken (PostgreSQL: "current transaction is aborted"). If you catch the error *inside* the same atomic block and keep querying, Django raises `TransactionManagementError`. Fix: wrap the risky statement in its own inner `atomic()` and catch outside it — only that savepoint is rolled back.

```python
with transaction.atomic():
    try:
        with transaction.atomic():
            Tag.objects.create(name=name)
    except IntegrityError:
        pass                      # outer transaction still usable
```

---

<a name="q6"></a>
## Q6. (Easy) How does transaction.on_commit() work and why is it crucial for task queues (e.g., Celery)?
**Answer:** `on_commit(func)` runs `func` only **after the transaction commits**; if it rolls back, the callback is discarded. Crucial for tasks: if you enqueue a Celery task inside the transaction, the worker may run before the commit and not find the row (or process a row that is later rolled back).

```python
transaction.on_commit(lambda: send_invoice.delay(order.id))
```
Outside any transaction it runs immediately.

---

<a name="q7"></a>
## Q7. (Medium) What happens to database connections when an atomic block raises an exception?
**Answer:** The transaction (or savepoint) is rolled back and the exception propagates. The connection itself stays open and usable after the block exits. If the error was a broken connection, Django marks it unusable and it's closed/replaced at the end of the request.

---

<a name="q8"></a>
## Q8. (Medium) How do you implement transaction-level isolation levels in Django?
**Answer:** Set it per connection in `DATABASES["OPTIONS"]` (PostgreSQL default: READ COMMITTED; Django's MySQL backend defaults to READ COMMITTED too). For a single transaction, run `SET TRANSACTION ISOLATION LEVEL ...` as the first statement inside `atomic()`.

```python
from psycopg import IsolationLevel
DATABASES["default"]["OPTIONS"] = {"isolation_level": IsolationLevel.SERIALIZABLE}
```
Higher levels mean more serialization errors — the code must retry.

---

<a name="q9"></a>
## Q9. (Medium) What is the performance impact of using large atomic blocks in production?
**Answer:** Long transactions hold row locks longer (other requests wait or deadlock), keep a DB connection busy, prevent VACUUM from cleaning old rows (bloat), increase replica lag, and make rollbacks expensive. Keep transactions short: only the writes that must be atomic, no slow work inside.

---

<a name="q10"></a>
## Q10. (Medium) How do you handle nested transactions with multiple database connections?
**Answer:** Each database alias has its own transaction. `atomic()` only covers `default` unless you pass `using`: `atomic(using="reports")`. You can nest both, but there's **no atomicity across databases** — one can commit and the other fail. Use compensation/outbox patterns for cross-DB consistency.

---

<a name="q11"></a>
## Q11. (Hard) Explain how database savepoints can exhaust PostgreSQL transaction ID limits.
**Answer:** In PostgreSQL every savepoint that writes data gets its own sub-transaction ID. Creating savepoints in tight loops (e.g. `atomic()` per row inside an outer transaction) burns transaction IDs much faster, pushing toward wraparound if VACUUM can't keep up. Also, more than 64 sub-transactions in one transaction overflow a cache and slow down the whole server. Avoid per-row nested `atomic()` in big loops; use `savepoint=False` or batch work.

---

<a name="q12"></a>
## Q12. (Medium) How does Django prevent transactional deadlocks when executing concurrent transactions?
**Answer:** It doesn't — the database detects deadlocks and kills one transaction (`OperationalError: deadlock detected`). You prevent them by: locking rows in a **consistent order** (`select_for_update().order_by("pk")`), keeping transactions short, touching fewer rows, and retrying the failed transaction.

---

<a name="q13"></a>
## Q13. (Medium) What happens when you mix non-database operations (like API calls) inside atomic blocks?
**Answer:** Two problems: the external call can't be rolled back (email sent, payment charged, but DB rolls back), and a slow call keeps the transaction and its locks open. Do external work **after commit** with `on_commit()`, or use an outbox table processed by a background worker.

---

<a name="q14"></a>
## Q14. (Medium) How do you write tests that require real database commits instead of rollbacks?
**Answer:** Use `TransactionTestCase` — it really commits and then truncates tables after each test (slower). For just testing `on_commit` callbacks in a normal `TestCase`, use `captureOnCommitCallbacks(execute=True)`.

```python
with self.captureOnCommitCallbacks(execute=True) as callbacks:
    self.client.post("/orders/", data)
self.assertEqual(len(callbacks), 1)
```

---

<a name="q15"></a>
## Q15. (Easy) What is the difference between TransactionTestCase and TestCase in Django testing?
**Answer:** `TestCase` wraps each test in a transaction and rolls it back — fast, but nothing is really committed (so `on_commit` doesn't fire and you can't test real transaction behaviour). `TransactionTestCase` lets transactions commit and cleans up by truncating tables — slower, needed for testing commits, `select_for_update` across threads, or raw transaction behaviour.

---

<a name="q16"></a>
## Q16. (Medium) How does transaction.atomic() handle threading?
**Answer:** Each thread has its own DB connection, so `atomic()` only affects the current thread's connection. Other threads can't see uncommitted data and aren't part of the transaction. Starting a thread inside an atomic block does **not** share the transaction with it.

---

<a name="q17"></a>
## Q17. (Medium) What is the risk of using autocommit=False in Django database configuration?
**Answer:** `"AUTOCOMMIT": False` disables Django's transaction management: everything runs in one implicit transaction until you commit manually. Risks: forgotten commits (lost data), very long open transactions, held locks, and confusing interaction with `atomic()`. Almost always keep the default (`True`) and use `atomic()`.

---

<a name="q18"></a>
## Q18. (Easy) How do you execute raw SQL transaction commands inside Django?
**Answer:** Don't send `BEGIN`/`COMMIT`/`ROLLBACK` yourself — Django won't know about them. Wrap raw SQL in `atomic()`; raw statements on the same connection join that transaction. Session settings for one transaction can use `SET LOCAL`.

```python
with transaction.atomic(), connection.cursor() as cur:
    cur.execute("SET LOCAL statement_timeout = '5s'")
    cur.execute("UPDATE stock SET qty = qty - %s WHERE id = %s", [n, pk])
```

---

<a name="q19"></a>
## Q19. (Easy) How does atomic interact with select_for_update?
**Answer:** `select_for_update()` locks the selected rows until the transaction ends, so it **must run inside `atomic()`** — evaluating it in autocommit raises `TransactionManagementError`. Locks are released at commit/rollback.

```python
with transaction.atomic():
    acc = Account.objects.select_for_update().get(pk=pk)
    acc.balance -= amount
    acc.save()
```

---

<a name="q20"></a>
## Q20. (Easy) What happens if the application crashes in the middle of an atomic block?
**Answer:** Nothing is half-saved. The connection drops and the database automatically rolls back the uncommitted transaction. `on_commit` callbacks never run. That's the whole point of atomicity.

---

<a name="q21"></a>
## Q21. (Medium) How do you safely retry failed transactions due to serialization errors?
**Answer:** Catch the error **outside** the atomic block and rerun the whole transaction a few times with a short backoff. The transaction body must be safe to repeat (no external side effects inside).

```python
for attempt in range(3):
    try:
        with transaction.atomic():
            transfer(a, b, amount)
        break
    except OperationalError:          # serialization failure / deadlock
        time.sleep(0.1 * (attempt + 1))
```

---

<a name="q22"></a>
## Q22. (Medium) How does Django 5.0 handle asynchronous transaction management?
**Answer:** `transaction.atomic()` is not supported in async code yet. Put the transactional logic in a sync function and call it with `sync_to_async`, so it runs in one thread on one connection.

```python
@sync_to_async
def place_order(data):
    with transaction.atomic():
        ...
await place_order(data)
```

---

<a name="q23"></a>
## Q23. (Hard) What is the impact of connection pooling on transaction state cleanup?
**Answer:** A pooled connection must be returned clean — no open transaction. Django doesn't leave transactions open after `atomic()`, but session-level state (`SET` without `LOCAL`, temp tables, advisory locks, server-side cursors) can leak to the next user. With PgBouncer **transaction pooling**, each transaction may run on a different server connection, so session state isn't kept at all — use `SET LOCAL`, disable server-side cursors.

---

<a name="q24"></a>
## Q24. (Medium) How do you handle multi-database transaction routing?
**Answer:** The router decides which database a query uses, but `atomic()` only covers the alias you give it (default `default`). If the router sends a write to another alias, it's **not** inside your transaction. Use `atomic(using=router.db_for_write(Model))` or `atomic(using="alias")` explicitly, and keep each transaction to one database.

---

<a name="q25"></a>
## Q25. (Hard) How do you implement 2-phase commit concepts using Django ORM?
**Answer:** Django has no 2-phase commit support. Options: avoid needing it (one database per transaction); use the **saga** pattern (each step commits locally, failures run compensating actions); use an **outbox** table + worker for reliable cross-system updates. Raw `PREPARE TRANSACTION` exists in PostgreSQL but is rarely worth the operational risk.

---

<a name="q26"></a>
## Q26. (Medium) How does transaction.on_commit() handle nested transaction blocks?
**Answer:** Callbacks registered in a nested block wait for the **outermost** commit. If an inner savepoint is rolled back, callbacks registered inside it are discarded; others still run after the final commit, in registration order.

---

<a name="q27"></a>
## Q27. (Medium) What is the impact of transaction.atomic() on database connection lifetime?
**Answer:** The connection is held for the whole block and can't be closed or returned to a pool until the transaction ends. `CONN_MAX_AGE` cleanup happens at request boundaries, never in the middle of an atomic block. Long blocks = connections tied up = pool exhaustion under load.

---

<a name="q28"></a>
## Q28. (Medium) How do you inspect the active transaction state using django.db.transaction?
**Answer:**
- `connection.in_atomic_block` → inside `atomic()`?
- `transaction.get_autocommit()` → autocommit on/off.
- `transaction.get_rollback()` → is the current block marked for rollback?
Useful in helpers that require a transaction, e.g. `assert connection.in_atomic_block`.

---

<a name="q29"></a>
## Q29. (Medium) Explain the interaction between transaction commits and database triggers.
**Answer:** Triggers run inside the same transaction as the statement that fired them, so their changes commit or roll back together with yours. Deferred constraint triggers run at `COMMIT`, so their errors show up at commit time (e.g. `IntegrityError` when the atomic block exits).

---

<a name="q30"></a>
## Q30. (Easy) How does Django handle transaction rollbacks on MySQL MyISAM tables?
**Answer:** It can't — MyISAM doesn't support transactions, so `atomic()` rollback doesn't undo anything. Use InnoDB (the default in modern MySQL).

---

<a name="q31"></a>
## Q31. (Medium) What is the difference between SELECT FOR UPDATE and SELECT FOR SHARE in transactions?
**Answer:** `FOR UPDATE` takes an exclusive row lock — others can't update or lock those rows until you commit. `FOR SHARE` lets several transactions read-lock the same rows but blocks updates — useful to make sure a parent row isn't changed/deleted while you work. Django has `select_for_update()` (plus `no_key=True` → `FOR NO KEY UPDATE`); `FOR SHARE` needs raw SQL.

---

<a name="q32"></a>
## Q32. (Medium) How do you write transactional tests with database-level isolation mocks?
**Answer:** Keep the DB real and mock only external effects. Use `TestCase` for normal logic, `captureOnCommitCallbacks` to check post-commit work, `TransactionTestCase` + threads to test locking/concurrency, and `mock.patch` for external services so a rollback test can assert they weren't called.

---

<a name="q33"></a>
## Q33. (Hard) Explain the role of atomic block savepoint creation logic.
**Answer:** On `__enter__`, if no transaction is active Django turns autocommit off (starts the transaction); if one is active and `savepoint=True`, it creates a savepoint and pushes its id on a stack. On `__exit__` it pops the id and either releases it (success) or rolls back to it (error). With `savepoint=False`, an inner error just marks the whole transaction for rollback.

---

<a name="q34"></a>
## Q34. (Medium) How do you monitor transaction execution duration in production APMs?
**Answer:** APM tools (Datadog, New Relic, OpenTelemetry) trace DB spans per request/task. On PostgreSQL, watch `pg_stat_activity` (`xact_start`, state `idle in transaction`), set `idle_in_transaction_session_timeout`, and log long transactions. Alert on long-running and idle-in-transaction sessions.

---

<a name="q35"></a>
## Q35. (Medium) What is the impact of database connection disconnect on active transactions?
**Answer:** The database rolls back the uncommitted transaction. Django raises `OperationalError`/`InterfaceError`, marks the connection unusable, and replaces it at the next request. Nothing is committed, so you can safely retry the whole unit of work (if it's idempotent).

---

<a name="q36"></a>
## Q36. (Medium) How does Django handle the ACID properties of a database transaction? ⭐ Asked in my interview
**Answer:** ACID is guaranteed by the **database** (PostgreSQL, MySQL InnoDB, SQL Server); Django doesn't implement it, it gives you the tools to **use** it correctly.

| Property | Meaning | Who guarantees it | What you use in Django |
|---|---|---|---|
| **A**tomicity | All statements succeed or none do | DB (COMMIT / ROLLBACK) | `transaction.atomic()`, savepoints, `ATOMIC_REQUESTS` |
| **C**onsistency | Data always moves from one valid state to another | DB constraints + your rules | `unique`, FK, `CheckConstraint`, `UniqueConstraint`, `full_clean()` |
| **I**solation | Concurrent transactions don't see each other's half-done work | DB isolation level + locks | `isolation_level` setting, `select_for_update()`, `F()` |
| **D**urability | Once committed, data survives a crash | DB (write-ahead log, disk flush, replication) | `transaction.on_commit()` for side effects |

**Atomicity** — By default Django is in **autocommit**: every single query commits on its own, so two `save()` calls are *not* atomic together. Wrap related writes in `atomic()`: the outer block runs `BEGIN … COMMIT`, any exception → `ROLLBACK`; nested blocks become savepoints, so an inner failure can be undone alone.

```python
from django.db import transaction
from django.db.models import F

def transfer(from_id, to_id, amount):
    with transaction.atomic():                                   # Atomicity
        src = Account.objects.select_for_update().get(pk=from_id)    # Isolation (row lock)
        if src.balance < amount:
            raise ValueError("Insufficient funds")               # → ROLLBACK, nothing saved
        Account.objects.filter(pk=from_id).update(balance=F("balance") - amount)
        Account.objects.filter(pk=to_id).update(balance=F("balance") + amount)
        transaction.on_commit(lambda: notify_transfer.delay(from_id, to_id))   # after Durability
```

**Consistency** — The database rejects invalid data via constraints (NOT NULL, unique, foreign key, check) and raises `IntegrityError`; inside `atomic()` that rolls back the whole transaction. Define rules as DB constraints (`CheckConstraint(condition=Q(balance__gte=0), name="balance_non_negative")`). Django's `full_clean()` validation is app-level and **not** called by `save()` — so the DB constraint is the real guarantee.

**Isolation** — Controlled by the database's isolation level (PostgreSQL default **Read Committed**; Django's MySQL backend also uses Read Committed). Change it in `DATABASES["OPTIONS"]["isolation_level"]` (e.g. Serializable — then retry serialization errors). Within Read Committed, protect read-modify-write code with `select_for_update()` (pessimistic lock), `F()` expressions (atomic in-DB update), or a version field (optimistic lock).

**Durability** — Once `COMMIT` returns, the database has written it to its write-ahead log on disk, so a crash won't lose it; replicas/backups add more safety. Django's job is to know **when** the commit happened: run emails, Celery tasks and API calls in `transaction.on_commit()`, never inside the block — otherwise they could fire for data that later rolls back.

**Gotcha:** ACID covers **one database**. With multiple databases (`atomic(using="other")`), there's no atomicity across them — use the outbox/saga pattern.
**Follow-up:** Is `model.save()` atomic? → A single `save()` is (one statement; multi-table inheritance saves are wrapped in a transaction internally), but several `save()` calls are only atomic together inside `atomic()`.

