# Module 19: Production Issues & Debugging (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/19_Production_Issues.md)

## Table of Contents
1. (Medium) [How do you identify slow Django ORM queries in a production PostgreSQL environment?](#q1)
2. (Medium) [How do you detect memory leaks caused by Django QuerySets in long-running Celery processes?](#q2)
3. (Medium) [How do you handle django.db.utils.InterfaceError: connection already closed in production?](#q3)
4. (Easy) [What causes OperationalError: database is locked in SQLite and how do you resolve it?](#q4)
5. (Medium) [How do you debug 'Too many connections' issues on MySQL/PostgreSQL with Django?](#q5)
6. (Medium) [How do you track down which line of code generated a specific slow query?](#q6)
7. (Medium) [How do you monitor database connection pool utilization in Django?](#q7)
8. (Medium) [How do you handle database connection timeouts and reconnects?](#q8)
9. (Hard) [How do you debug data consistency issues caused by race conditions in production?](#q9)
10. (Medium) [How do you handle large transaction log (WAL) generation caused by bulk ORM operations?](#q10)
11. (Medium) [How do you recover from a failed database migration that left the database in a half-migrated state?](#q11)
12. (Medium) [How do you debug slow prefetch_related queries when prefetching large datasets?](#q12)
13. (Medium) [What is the production impact of missing foreign key indexes in Django?](#q13)
14. (Medium) [How do you debug slow aggregation queries on tables with millions of rows?](#q14)
15. (Easy) [How do you resolve N+1 queries in Django admin panels?](#q15)
16. (Medium) [What causes high CPU usage on the database server from Django's count() queries?](#q16)
17. (Medium) [How do you handle timezone mismatch issues between Django settings and PostgreSQL?](#q17)
18. (Medium) [How do you debug database deadlock errors in production logs?](#q18)
19. (Medium) [What are the risks of using Django's select_for_update() with a short timeout?](#q19)
20. (Medium) [How do you debug issues with Django's database routing in production replica lag?](#q20)
21. (Medium) [How do you identify index bloat on production PostgreSQL tables managed by Django?](#q21)
22. (Medium) [How do you debug serialization failure errors in PostgreSQL repeatable read transactions?](#q22)
23. (Medium) [How do you profile memory consumption of Django model instances?](#q23)
24. (Easy) [What is the production impact of django.db.connection.queries in DEBUG=True mode?](#q24)
25. (Hard) [How do you troubleshoot slow migrations on tables with 100M+ rows?](#q25)
26. (Hard) [How do you configure pg_sentinel with Django to monitor queries?](#q26)
27. (Medium) [How do you profile celery tasks database latency metrics?](#q27)
28. (Medium) [What causes transaction rollback errors inside nested atomic blocks?](#q28)
29. (Medium) [How do you debug connection timeouts in PgBouncer pool?](#q29)
30. (Hard) [How do you troubleshoot database memory exhaustion under traffic spikes?](#q30)
31. (Medium) [What is the impact of unclosed cursors in custom DB scripts?](#q31)
32. (Medium) [How do you write a script to auto-kill long running idle-in-transaction connections?](#q32)
33. (Medium) [How do you trace ORM query latency using OpenTelemetry?](#q33)
34. (Medium) [How do you identify index scans that have degraded to sequential scans?](#q34)
35. (Medium) [What is the production risk of using bulk_update without an explicit fields list?](#q35)

---

<a name="q1"></a>
## Q1. (Medium) How do you identify slow Django ORM queries in a production PostgreSQL environment?
**Answer:**
1. `pg_stat_statements` — rank queries by total and mean time.
2. `log_min_duration_statement` (e.g. 500 ms) / `auto_explain` — log slow queries with plans.
3. APM tracing (Datadog, New Relic, OpenTelemetry) — link slow SQL to endpoints.
4. Reproduce with `EXPLAIN ANALYZE` on staging and fix (index, N+1, rewrite).

---

<a name="q2"></a>
## Q2. (Medium) How do you detect memory leaks caused by Django QuerySets in long-running Celery processes?
**Answer:** Typical causes: evaluating huge querysets (`list(Model.objects.all())`), keeping querysets/instances in module-level caches, and `DEBUG=True` storing every query in `connection.queries`. Detect with worker memory metrics and `tracemalloc`. Fix: `iterator(chunk_size=...)`, `values()`, process in batches, `DEBUG=False`, and `worker_max_tasks_per_child` / `worker_max_memory_per_child` to recycle workers.

---

<a name="q3"></a>
## Q3. (Medium) How do you handle django.db.utils.InterfaceError: connection already closed in production?
**Answer:** The process is using a connection the DB/proxy already closed (idle timeout, DB restart, failover). Common in long-running workers that don't go through the request cycle. Fix: call `close_old_connections()` before/after each task, enable `CONN_HEALTH_CHECKS = True`, keep `CONN_MAX_AGE` below the server/proxy idle timeout, and retry idempotent work.

---

<a name="q4"></a>
## Q4. (Easy) What causes OperationalError: database is locked in SQLite and how do you resolve it?
**Answer:** SQLite allows only one writer at a time; another connection held a write lock longer than the timeout (concurrent requests, long transactions). Fix: increase `OPTIONS["timeout"]`, keep transactions short, enable WAL mode — or use PostgreSQL for anything with concurrent writes.

---

<a name="q5"></a>
## Q5. (Medium) How do you debug 'Too many connections' issues on MySQL/PostgreSQL with Django?
**Answer:** Count connections: workers × threads × DB aliases (+ Celery, cron, scripts). Check `pg_stat_activity` grouped by `application_name`/state — lots of `idle` means persistent connections are held; `idle in transaction` means code leaves transactions open. Fix: a pooler (PgBouncer / Django 5.1 pool), lower `CONN_MAX_AGE`, close connections in workers, and right-size worker counts.

---

<a name="q6"></a>
## Q6. (Medium) How do you track down which line of code generated a specific slow query?
**Answer:** APM traces show the stack/endpoint for each query; in dev, django-debug-toolbar shows the stack trace. In production, tag SQL with a comment (route/task name) via `connection.execute_wrapper()` or sqlcommenter, so logs and `pg_stat_activity` show the source; then search the code for the table/filter pattern.

---

<a name="q7"></a>
## Q7. (Medium) How do you monitor database connection pool utilization in Django?
**Answer:** With PgBouncer, `SHOW POOLS` / `SHOW STATS` (active, waiting clients, wait time) exported to monitoring. On the DB, `pg_stat_activity` counts by state. Alert on waiting clients and connections near `max_connections`. With Django 5.1's pool, psycopg pool stats can be exposed too.

---

<a name="q8"></a>
## Q8. (Medium) How do you handle database connection timeouts and reconnects?
**Answer:** Set `connect_timeout` and `statement_timeout` in `OPTIONS` so calls fail fast, enable `CONN_HEALTH_CHECKS`, and retry **idempotent** operations a few times with backoff. Django won't reconnect in the middle of a request automatically — a dropped connection fails that request; the next request gets a new connection.

---

<a name="q9"></a>
## Q9. (Hard) How do you debug data consistency issues caused by race conditions in production?
**Answer:** Look for read-modify-write code (`obj.count += 1; obj.save()`), check-then-insert (`if not exists: create`) and missing constraints. Confirm with logs/audit timestamps showing overlapping requests. Fix: `F()` updates, unique constraints + handle `IntegrityError`, `select_for_update()` for critical sections, optimistic locking. Then repair bad data with a one-off script.

---

<a name="q10"></a>
## Q10. (Medium) How do you handle large transaction log (WAL) generation caused by bulk ORM operations?
**Answer:** Huge `update()`/`delete()`/backfills write a lot of WAL → disk usage, replica lag, backup growth. Batch them in small transactions with pauses, avoid updating unchanged rows, drop/attach partitions instead of mass deletes, run heavy jobs off-peak, and monitor replication lag while they run.

---

<a name="q11"></a>
## Q11. (Medium) How do you recover from a failed database migration that left the database in a half-migrated state?
**Answer:** On PostgreSQL migrations are transactional, so a failure usually rolls back fully — fix and re-run. On MySQL (non-transactional DDL), or with `atomic = False`, inspect what was applied (`\d table`, `showmigrations`), manually complete or undo the partial changes, then mark state with `migrate --fake app 00xx` so `django_migrations` matches reality. Prefer small migrations to limit the damage.

---

<a name="q12"></a>
## Q12. (Medium) How do you debug slow prefetch_related queries when prefetching large datasets?
**Answer:** Check what's slow: a huge `IN (...)` list, a missing index on the FK, or too many child rows loaded into memory. Fix: paginate/chunk the parent set, filter children with `Prefetch(queryset=...)`, add the FK index, trim columns with `only()`, or replace with an aggregate/annotation if you only need counts.

---

<a name="q13"></a>
## Q13. (Medium) What is the production impact of missing foreign key indexes in Django?
**Answer:** Django indexes FKs by default, but they can go missing (`db_index=False`, legacy/unmanaged tables, raw SQL tables). Then reverse lookups (`customer.orders.all()`), joins and especially deletes of parents (checking/cascading children) do full scans of the child table — slow queries and long locks.

---

<a name="q14"></a>
## Q14. (Medium) How do you debug slow aggregation queries on tables with millions of rows?
**Answer:** `EXPLAIN ANALYZE`: look for seq scans, big sorts/hashes spilling to disk, and joins multiplying rows before GROUP BY. Fix: filter earlier (WHERE, indexed date range), aggregate on the narrowest table, use covering indexes, increase `work_mem` for the query, or pre-aggregate into summary tables / materialized views.

---

<a name="q15"></a>
## Q15. (Easy) How do you resolve N+1 queries in Django admin panels?
**Answer:** Use `list_select_related` for FK columns, override `get_queryset()` to add `prefetch_related`/`annotate` for computed columns, avoid model methods in `list_display` that query per row, and use `autocomplete_fields`/`raw_id_fields` instead of huge FK dropdowns.

```python
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "item_count"]
    list_select_related = ["customer"]
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(n=Count("items"))
    def item_count(self, obj):
        return obj.n
```

---

<a name="q16"></a>
## Q16. (Medium) What causes high CPU usage on the database server from Django's count() queries?
**Answer:** `COUNT(*)` must visit every matching row; on big tables it runs constantly from admin changelists, DRF `PageNumberPagination` (counts every page request) and dashboards. Fix: cursor pagination (no count), cache counts, estimated counts (`pg_class.reltuples`) for large lists, `show_full_result_count = False` in admin, and indexes for filtered counts.

---

<a name="q17"></a>
## Q17. (Medium) How do you handle timezone mismatch issues between Django settings and PostgreSQL?
**Answer:** Keep `USE_TZ = True`, store `timestamptz` (UTC), and let Django set the connection timezone to UTC. Problems usually come from naive datetimes (`datetime.now()` — use `timezone.now()`), raw SQL using `now()::date` in the server's timezone, or legacy `timestamp without time zone` columns. Convert to local time only at display.

---

<a name="q18"></a>
## Q18. (Medium) How do you debug database deadlock errors in production logs?
**Answer:** PostgreSQL logs both conflicting statements and processes on `deadlock detected`. Find the two code paths and see that they lock the same rows/tables in a different order. Fix: lock in a consistent order (`order_by("pk")` with `select_for_update`), shorten transactions, reduce rows per transaction, and add a retry for the rare remaining cases.

---

<a name="q19"></a>
## Q19. (Medium) What are the risks of using Django's select_for_update() with a short timeout?
**Answer:** With `nowait=True` or a short `lock_timeout`, requests fail whenever a row is briefly locked — under load that means many errors and retries (more load). It also hides the real problem (long-held locks). Use it with clear user errors/retries, and keep lock-holding transactions short instead.

---

<a name="q20"></a>
## Q20. (Medium) How do you debug issues with Django's database routing in production replica lag?
**Answer:** Symptoms: "I saved it but it's not there" right after a write. Confirm by checking replica lag (`now() - pg_last_xact_replay_timestamp()`) and which alias served the read (logs/query tags). Fix: read-your-writes from the primary after writes (sticky primary per user for a short time), route reads inside transactions to the primary, skip lagging replicas in the router.

---

<a name="q21"></a>
## Q21. (Medium) How do you identify index bloat on production PostgreSQL tables managed by Django?
**Answer:** Compare index size to expected size with a bloat-estimation query or `pgstattuple`/`pgstatindex` (low leaf density = bloat); watch `pg_relation_size` growing while row count is stable; check autovacuum activity in `pg_stat_user_tables`. Fix with `REINDEX INDEX CONCURRENTLY` or `pg_repack`.

---

<a name="q22"></a>
## Q22. (Medium) How do you debug serialization failure errors in PostgreSQL repeatable read transactions?
**Answer:** "could not serialize access due to concurrent update" means two transactions modified the same data under Repeatable Read/Serializable — this is expected behaviour, not a bug. Find which transactions overlap (logs), make sure the code **retries the whole transaction**, keep transactions short, or use Read Committed + explicit locks where strict isolation isn't needed.

---

<a name="q23"></a>
## Q23. (Medium) How do you profile memory consumption of Django model instances?
**Answer:** Use `tracemalloc` snapshots or `memray` around the code, and compare: model instances vs `values()` dicts vs `values_list()` tuples for the same rows. Big wins usually come from not loading everything at once (`iterator()`), selecting fewer columns, and not keeping references to instances after processing.

---

<a name="q24"></a>
## Q24. (Easy) What is the production impact of django.db.connection.queries in DEBUG=True mode?
**Answer:** With `DEBUG=True` Django keeps every executed query in memory (`connection.queries`, capped at 9000 per connection), which grows memory in long-running processes, and also exposes error pages with settings/stack traces — a security risk. Always run production with `DEBUG=False`.

---

<a name="q25"></a>
## Q25. (Hard) How do you troubleshoot slow migrations on tables with 100M+ rows?
**Answer:** Check with `sqlmigrate` what SQL runs: table rewrites (type changes, adding non-null columns on old PostgreSQL), plain `CREATE INDEX`, or a slow `RunPython` loop. Look at `pg_locks`/`pg_stat_activity` for lock waits. Fix: concurrent index creation, expand/contract instead of rewrites, batched backfills run outside the migration, and `lock_timeout` so it fails fast instead of blocking traffic.

---

<a name="q26"></a>
## Q26. (Hard) How do you configure pg_sentinel with Django to monitor queries?
**Answer:** `pgsentinel` is a PostgreSQL extension that samples active sessions into `pg_active_session_history` (like Oracle ASH), so you can see which queries and wait events were busy at any past moment. Install it on the DB server (`shared_preload_libraries`, `CREATE EXTENSION pgsentinel`) — no Django change needed. Set `application_name` per service in `OPTIONS` so samples show which app ran the query.

---

<a name="q27"></a>
## Q27. (Medium) How do you profile celery tasks database latency metrics?
**Answer:** Use APM/OpenTelemetry instrumentation for Celery + Django DB (spans per task with query timings), or a `connection.execute_wrapper()` that times queries and records count/total per task (via task signals). Track queries-per-task and DB time-per-task to spot N+1 and slow queries in jobs.

---

<a name="q28"></a>
## Q28. (Medium) What causes transaction rollback errors inside nested atomic blocks?
**Answer:** A DB error inside an atomic block that you **caught inside the same block** leaves the transaction broken; the next query raises `TransactionManagementError: An error occurred in the current transaction`. Fix: wrap the risky statement in its own inner `atomic()` (savepoint) and catch the exception outside it.

---

<a name="q29"></a>
## Q29. (Medium) How do you debug connection timeouts in PgBouncer pool?
**Answer:** Check `SHOW POOLS` — many `cl_waiting` means the pool is too small or server connections are held too long. Look for long transactions (`idle in transaction`) and slow queries holding connections, and check `pool_size`, `max_client_conn`, `query_wait_timeout`. Fix the long-held connections first, then resize the pool.

---

<a name="q30"></a>
## Q30. (Hard) How do you troubleshoot database memory exhaustion under traffic spikes?
**Answer:** Each connection uses memory, and each sort/hash in a query can use up to `work_mem` (several per query). Too many connections × heavy queries → memory exhaustion. Fix: limit connections with a pooler, lower `work_mem` globally (raise per heavy job), kill/limit runaway queries with `statement_timeout`, and remove the heavy queries causing big sorts (indexes, pagination).

---

<a name="q31"></a>
## Q31. (Medium) What is the impact of unclosed cursors in custom DB scripts?
**Answer:** Unclosed cursors keep result sets and memory on client/server; server-side cursors can keep a transaction/snapshot open, blocking VACUUM and holding locks. Always use `with connection.cursor() as cur:` and close connections at the end of scripts.

---

<a name="q32"></a>
## Q32. (Medium) How do you write a script to auto-kill long running idle-in-transaction connections?
**Answer:** Best: let PostgreSQL do it with `idle_in_transaction_session_timeout` (e.g. `'5min'`). As a script:

```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
WHERE state = 'idle in transaction' AND now() - state_change > interval '10 minutes';
```
Then find and fix the code that leaves transactions open.

---

<a name="q33"></a>
## Q33. (Medium) How do you trace ORM query latency using OpenTelemetry?
**Answer:** Install the OpenTelemetry Django and DB driver instrumentations (`opentelemetry-instrumentation-django`, `-psycopg`), configure an exporter (OTLP → Jaeger/Tempo/Datadog), and each request trace shows DB spans with SQL and duration. Optionally add sqlcommenter to put trace ids into SQL comments for DB-side correlation.

---

<a name="q34"></a>
## Q34. (Medium) How do you identify index scans that have degraded to sequential scans?
**Answer:** Watch `pg_stat_user_tables` (`seq_scan` / `seq_tup_read` rising on big tables) and `pg_stat_user_indexes` (`idx_scan` dropping), and use `auto_explain` to capture plans of slow queries. Causes: stale statistics (`ANALYZE`), a query change wrapping the column in a function, type mismatch, or the planner deciding the filter isn't selective.

---

<a name="q35"></a>
## Q35. (Medium) What is the production risk of using bulk_update without an explicit fields list?
**Answer:** `bulk_update()` requires `fields`; the risk is listing **too many** (e.g. every field "to be safe"): you overwrite columns other processes changed since you loaded the objects (lost updates), build huge CASE statements, and write lots of WAL. List only the fields you actually changed.
