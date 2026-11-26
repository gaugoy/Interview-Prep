# Module 14: Multi-Database Architectures (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/14_Multi_Database.md)

## Table of Contents
1. (Easy) [How do you configure multiple database connections in DATABASES setting?](#q1)
2. (Easy) [What is a Database Router and how do you implement one?](#q2)
3. (Easy) [How do the four router methods work (db_for_read, db_for_write, allow_relation, allow_migrate)?](#q3)
4. (Medium) [How do you implement a read-replica setup using database routers?](#q4)
5. (Medium) [What is replication lag and how do you handle read-after-write consistency?](#q5)
6. (Easy) [How do you force a QuerySet to execute against a specific database using using()?](#q6)
7. (Easy) [How do you save a model instance to a specific database using save(using=...)?](#q7)
8. (Easy) [What are the limitations of database relations across different databases?](#q8)
9. (Medium) [How do you handle foreign key relationships in a multi-database setup?](#q9)
10. (Easy) [How do you run migrations on a specific database using migrate --database?](#q10)
11. (Hard) [How do you implement horizontal sharding concepts using Django ORM?](#q11)
12. (Hard) [How do you handle distributed transactions across multiple databases in Django?](#q12)
13. (Medium) [What is the failover strategy in a multi-database Django configuration?](#q13)
14. (Medium) [How do you write tests for multi-database configurations?](#q14)
15. (Medium) [What is allow_relation router method and how does it prevent cross-database joins?](#q15)
16. (Medium) [How do you route admin panel actions to a specific database?](#q16)
17. (Hard) [How do you implement dynamic tenant database routing?](#q17)
18. (Medium) [What are the connection management implications of having 100+ database connections in Django?](#q18)
19. (Easy) [How do you handle session database routing separately from core data?](#q19)
20. (Medium) [What is the impact of multi-db routing on Django contenttypes framework?](#q20)
21. (Medium) [How do you write a custom manager that routes queries to a read replica automatically?](#q21)
22. (Easy) [What is the difference between db_alias and using()?](#q22)
23. (Medium) [How do database routers interact with Celery background tasks?](#q23)
24. (Medium) [How do you clean up connections for multiple databases?](#q24)
25. (Medium) [Explain Django 5.0's async database backend routing operations.](#q25)
26. (Medium) [How does database router allow_migrate block django test suite tables?](#q26)
27. (Hard) [Explain the role of ConnectionHandler in multi-db connections.](#q27)
28. (Medium) [How do you execute cross-database aggregation in Python memory?](#q28)
29. (Medium) [What is the risk of using transaction.atomic() across multiple databases?](#q29)
30. (Medium) [How does django-multidb-router manage read replica failovers?](#q30)
31. (Easy) [Explain the structure of connection.queries under multi-db setup.](#q31)
32. (Medium) [How do you configure database-level replication status health-checks?](#q32)
33. (Medium) [What is the performance overhead of dynamic database routing?](#q33)
34. (Medium) [How do you route queries based on thread local context?](#q34)
35. (Medium) [How do you enforce write locks on replica connections to prevent accidental writes?](#q35)

---

<a name="q1"></a>
## Q1. (Easy) How do you configure multiple database connections in DATABASES setting?
**Answer:** Add more aliases to `DATABASES`; `default` is required.

```python
DATABASES = {
    "default": {"ENGINE": "django.db.backends.postgresql", "NAME": "app"},
    "replica": {"ENGINE": "django.db.backends.postgresql", "NAME": "app", "HOST": "replica-host"},
    "ods": {"ENGINE": "mssql", "NAME": "ODS", "HOST": "sql-host"},
}
DATABASE_ROUTERS = ["core.routers.AppRouter"]
```

---

<a name="q2"></a>
## Q2. (Easy) What is a Database Router and how do you implement one?
**Answer:** A class that tells Django which database to use for reads, writes, relations and migrations. Return an alias, or `None` to let the next router (or `default`) decide.

```python
class AppRouter:
    def db_for_read(self, model, **hints):
        return "ods" if model._meta.app_label == "ods" else None
    def db_for_write(self, model, **hints):
        return "ods" if model._meta.app_label == "ods" else None
    def allow_relation(self, obj1, obj2, **hints):
        return obj1._state.db == obj2._state.db
    def allow_migrate(self, db, app_label, **hints):
        return (db == "ods") == (app_label == "ods")
```

---

<a name="q3"></a>
## Q3. (Easy) How do the four router methods work (db_for_read, db_for_write, allow_relation, allow_migrate)?
**Answer:**
- `db_for_read(model)` → alias for SELECTs.
- `db_for_write(model)` → alias for INSERT/UPDATE/DELETE.
- `allow_relation(obj1, obj2)` → may these two objects be related (FK/M2M)? Usually only if same DB.
- `allow_migrate(db, app_label, model_name)` → should this model's migrations run on this DB?
Routers are tried in order; the first non-`None` answer wins.

---

<a name="q4"></a>
## Q4. (Medium) How do you implement a read-replica setup using database routers?
**Answer:** Send reads to replicas, writes to the primary, and allow relations between them (same data).

```python
class ReplicaRouter:
    def db_for_read(self, model, **hints):
        return random.choice(["replica1", "replica2"])
    def db_for_write(self, model, **hints):
        return "default"
    def allow_relation(self, obj1, obj2, **hints):
        return True
    def allow_migrate(self, db, app_label, **hints):
        return db == "default"
```
**Gotcha:** replication lag — a read right after a write may not see it.

---

<a name="q5"></a>
## Q5. (Medium) What is replication lag and how do you handle read-after-write consistency?
**Answer:** Replicas apply the primary's changes with a delay, so a user may not see what they just saved. Fixes: read from the primary right after a write (e.g. "stick to primary" for that user for a few seconds via session/cookie flag), use `.using("default")` for critical reads, and route all reads inside transactions to the primary.

---

<a name="q6"></a>
## Q6. (Easy) How do you force a QuerySet to execute against a specific database using using()?
**Answer:** `using(alias)` overrides the router for that queryset.

```python
Order.objects.using("replica").filter(status="paid")
```

---

<a name="q7"></a>
## Q7. (Easy) How do you save a model instance to a specific database using save(using=...)?
**Answer:** `obj.save(using="archive")` writes to that alias (also `delete(using=...)`). The instance remembers its DB in `obj._state.db`. **Gotcha:** saving an object loaded from one DB into another keeps the same pk — it may overwrite a different row there; set `pk=None` to insert as new.

---

<a name="q8"></a>
## Q8. (Easy) What are the limitations of database relations across different databases?
**Answer:** Django doesn't support FK/M2M relations across databases: no JOINs (`select_related`) across them, no DB-level foreign key constraints, no cross-DB transactions. You store the id as a plain field and fetch/merge in Python.

---

<a name="q9"></a>
## Q9. (Medium) How do you handle foreign key relationships in a multi-database setup?
**Answer:** Keep related models in the same database. If they must be split, replace the FK with a plain id field (`customer_code = CharField()`), fetch related rows with a second query on the other alias (`in_bulk`) and merge in Python. Validate the id exists in code, since the DB can't enforce it.

---

<a name="q10"></a>
## Q10. (Easy) How do you run migrations on a specific database using migrate --database?
**Answer:** `python manage.py migrate --database=reports`. `migrate` only touches the `default` DB unless you pass `--database`. Your router's `allow_migrate` decides which models get created there.

---

<a name="q11"></a>
## Q11. (Hard) How do you implement horizontal sharding concepts using Django ORM?
**Answer:** Define one alias per shard and pick the alias from a shard key (tenant id, region) — in a router using hints, or explicitly with `using(shard_for(tenant_id))`. Keep all data of one tenant on one shard so queries never cross shards. Cross-shard reports must query each shard and merge in Python. Re-sharding requires a data-migration plan.

---

<a name="q12"></a>
## Q12. (Hard) How do you handle distributed transactions across multiple databases in Django?
**Answer:** Django can't make two databases commit atomically. Options: design so one business transaction touches one DB; outbox pattern (write the change + an event in one DB, a worker applies it to the other); saga with compensating actions; idempotent retries. Nesting `atomic(using=...)` blocks only *narrows* the risk window.

---

<a name="q13"></a>
## Q13. (Medium) What is the failover strategy in a multi-database Django configuration?
**Answer:** Usually failover happens below Django: a DB proxy/virtual IP or DNS name (managed DB, Patroni, PgBouncer/HAProxy) points to the new primary, and Django just reconnects. In the app: connection health checks, short timeouts, a router that falls back from a dead replica to the primary, and retries for idempotent operations.

---

<a name="q14"></a>
## Q14. (Medium) How do you write tests for multi-database configurations?
**Answer:** Declare which databases a test may use; Django creates test DBs for them.

```python
class ReportTests(TestCase):
    databases = {"default", "reports"}
```
Test the router directly (call `db_for_read` etc.), use `assertNumQueries(n, using="reports")`. For replicas, set `"TEST": {"MIRROR": "default"}` so the replica alias reads the test primary.

---

<a name="q15"></a>
## Q15. (Medium) What is allow_relation router method and how does it prevent cross-database joins?
**Answer:** When you assign a related object (`order.customer = c`), Django asks `allow_relation(order, customer)`. Returning `False` raises `ValueError`, so you can't accidentally link objects from different databases (which would break JOINs and integrity). Return `True` for primary/replica (same data).

---

<a name="q16"></a>
## Q16. (Medium) How do you route admin panel actions to a specific database?
**Answer:** Subclass `ModelAdmin` and pass `using` in the key methods:

```python
class ODSAdmin(admin.ModelAdmin):
    using = "ods"
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)
    def delete_model(self, request, obj):
        obj.delete(using=self.using)
```
Also override `formfield_for_foreignkey` to query the same DB.

---

<a name="q17"></a>
## Q17. (Hard) How do you implement dynamic tenant database routing?
**Answer:** Middleware identifies the tenant (subdomain/header/user) and stores its alias in a context variable; the router returns that alias. Aliases can be added to `connections.databases` at startup from a tenant table.

```python
current_db = contextvars.ContextVar("current_db", default="default")
class TenantRouter:
    def db_for_read(self, model, **hints): return current_db.get()
    db_for_write = db_for_read
```
Reset the context at the end of each request; background tasks must set it explicitly.

---

<a name="q18"></a>
## Q18. (Medium) What are the connection management implications of having 100+ database connections in Django?
**Answer:** Each worker thread can open one connection **per alias** it touches, so workers × aliases can exceed the DB's `max_connections`. Mitigate: `CONN_MAX_AGE` tuned per alias, close connections when idle, use a pooler (PgBouncer / Django 5.1 pool), and avoid touching many tenants' DBs from one worker.

---

<a name="q19"></a>
## Q19. (Easy) How do you handle session database routing separately from core data?
**Answer:** Route the sessions app to its own alias in the router (`app_label == "sessions"`), or better, use a cache-based session backend (`SESSION_ENGINE = "django.contrib.sessions.backends.cache"` with Redis) so session reads/writes don't hit the main DB.

---

<a name="q20"></a>
## Q20. (Medium) What is the impact of multi-db routing on Django contenttypes framework?
**Answer:** Content types and permissions are created per database during `migrate`, and their ids can differ between databases. Generic foreign keys across databases don't work. Keep `contenttypes`/`auth` on one database (route them to `default`) and make sure apps using GenericForeignKey live in the same DB.

---

<a name="q21"></a>
## Q21. (Medium) How do you write a custom manager that routes queries to a read replica automatically?
**Answer:**

```python
class ReplicaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using("replica")

class Report(models.Model):
    objects = models.Manager()          # primary
    replica = ReplicaManager()          # Report.replica.filter(...)
```
Keeping a separate manager makes replica reads explicit (and avoids stale reads after writes).

---

<a name="q22"></a>
## Q22. (Easy) What is the difference between db_alias and using()?
**Answer:** `using("alias")` is the QuerySet/`save()` method to pick a database. "db_alias" is just the name of a database in `DATABASES` — e.g. passed as `using=` or available as `schema_editor.connection.alias` inside migrations (to make data migrations run only on the right database). Django's `Meta` has no `db_alias` option; routing per model is done in a router.

---

<a name="q23"></a>
## Q23. (Medium) How do database routers interact with Celery background tasks?
**Answer:** Routers work the same in workers, but anything request-based (thread-local/context tenant, "stick to primary after write") isn't there. Pass the tenant/alias as a task argument and set it at task start. Tasks triggered after a write should read from the primary (replica may lag). Call `close_old_connections()` in long-running workers.

---

<a name="q24"></a>
## Q24. (Medium) How do you clean up connections for multiple databases?
**Answer:** Django closes/recycles all aliases at the end of each request. In scripts, threads and workers do it yourself: `connections.close_all()` when done, or `close_old_connections()` periodically (it respects `CONN_MAX_AGE` and health).

---

<a name="q25"></a>
## Q25. (Medium) Explain Django 5.0's async database backend routing operations.
**Answer:** Async ORM methods (`aget`, `acount`, `async for`) use the same routers and `using()` as sync code. The DB call still runs in a thread with that thread's connection. Context-variable based routing works in async code (contextvars follow the task); thread-locals don't — so prefer `contextvars`.

---

<a name="q26"></a>
## Q26. (Medium) How does database router allow_migrate block django test suite tables?
**Answer:** During test setup Django runs migrations on each test database, and `allow_migrate` still applies. If it returns `False` for an app on an alias, those tables aren't created there, and tests querying them fail with "relation does not exist". Make sure tests' `databases` and `allow_migrate` agree (and `MIRROR` replicas).

---

<a name="q27"></a>
## Q27. (Hard) Explain the role of ConnectionHandler in multi-db connections.
**Answer:** `django.db.connections` is a `ConnectionHandler`: a dict-like object that lazily creates one `DatabaseWrapper` per alias **per thread/async context** from `DATABASES`. `connections["reports"]` returns the current thread's wrapper for that alias; `connections.close_all()` closes them all. `django.db.connection` is just a shortcut for `connections["default"]`.

---

<a name="q28"></a>
## Q28. (Medium) How do you execute cross-database aggregation in Python memory?
**Answer:** Aggregate in each database first (so only small results come back), then combine in Python.

```python
pg = dict(Order.objects.values_list("region").annotate(Sum("total")))
ods = dict(LegacyOrder.objects.using("ods").values_list("region").annotate(Sum("amount")))
combined = {r: pg.get(r, 0) + ods.get(r, 0) for r in pg.keys() | ods.keys()}
```
Never pull raw rows from both and aggregate in Python if the DB can do it.

---

<a name="q29"></a>
## Q29. (Medium) What is the risk of using transaction.atomic() across multiple databases?
**Answer:** `atomic()` covers one alias. Writes routed to another database run outside the transaction — they commit even if your block rolls back. Even nested `atomic(using="a")` + `atomic(using="b")` can leave one committed and the other rolled back if a failure happens between the two commits.

---

<a name="q30"></a>
## Q30. (Medium) How does django-multidb-router manage read replica failovers?
**Answer:** It sends reads to replicas and writes to the primary, and "pins" a user to the primary for a short time after they write (cookie-based) to avoid replication-lag surprises. It doesn't do health-based failover by itself — replica failure handling is done by your DB proxy or a custom router that skips unhealthy replicas.

---

<a name="q31"></a>
## Q31. (Easy) Explain the structure of connection.queries under multi-db setup.
**Answer:** `connection.queries` only shows queries of the `default` alias. Each alias has its own list: `connections["reports"].queries` — a list of `{"sql": ..., "time": ...}` dicts, only collected when `DEBUG=True`. To see all: loop over `connections.all()`.

---

<a name="q32"></a>
## Q32. (Medium) How do you configure database-level replication status health-checks?
**Answer:** Periodically check replication lag on replicas (PostgreSQL: `SELECT now() - pg_last_xact_replay_timestamp()`), expose it in a health endpoint, and have the router skip replicas whose lag exceeds a threshold (cache the result for a few seconds so you don't check per query).

---

<a name="q33"></a>
## Q33. (Medium) What is the performance overhead of dynamic database routing?
**Answer:** Router methods run on every query, so keep them trivial (dict lookup, context variable). Overhead is negligible unless the router does I/O (DB/cache lookups) — cache any tenant → alias mapping in memory. The bigger cost is many aliases = many connections.

---

<a name="q34"></a>
## Q34. (Medium) How do you route queries based on thread local context?
**Answer:** Middleware sets the alias in a thread-local (or better, `contextvars.ContextVar`, which also works in async), the router reads it, and the middleware resets it in `finally`. Forgetting to reset leaks the alias to the next request on that thread.

---

<a name="q35"></a>
## Q35. (Medium) How do you enforce write locks on replica connections to prevent accidental writes?
**Answer:** At the database: use a read-only DB user for the replica alias, or set `default_transaction_read_only = on` (replicas are already read-only at the server). In Django: the router never returns the replica for `db_for_write`, and you can raise an error in `db_for_write` if someone forces `using("replica")` on a write.
