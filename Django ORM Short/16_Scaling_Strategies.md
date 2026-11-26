# Module 16: Scaling & Partitioning Strategies (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/16_Scaling_Strategies.md)

## Table of Contents
1. (Hard) [How do you design an ORM scaling strategy for tables with 500M+ rows?](#q1)
2. (Hard) [How do you implement table partitioning (range, list, hash) in Django models?](#q2)
3. (Medium) [How do you integrate Redis/Memcached cache with Django ORM to prevent database hits?](#q3)
4. (Medium) [What is cache stampede and how do you prevent it in Django?](#q4)
5. (Medium) [How do you implement denormalization safely and keep data in sync using signals vs. database triggers?](#q5)
6. (Medium) [What are read replicas and how do you load balance database read queries?](#q6)
7. (Medium) [How does connection pooling improve Django ORM performance at scale?](#q7)
8. (Medium) [How do you configure pgbouncer with Django and what is transaction pooling vs. session pooling?](#q8)
9. (Medium) [What is the impact of long-running operations on Django connection management?](#q9)
10. (Medium) [How do you optimize Django ORM for write-heavy workloads?](#q10)
11. (Medium) [How do you scale read-heavy workloads using query caching and materialised views?](#q11)
12. (Easy) [What is the difference between database sharding and partitioning?](#q12)
13. (Hard) [How do you implement database sharding in a Django architecture?](#q13)
14. (Medium) [What is database index bloat and how do you resolve it at scale?](#q14)
15. (Medium) [How do you use Django ORM to query partitioned database tables?](#q15)
16. (Medium) [What is the performance impact of UUID primary keys on database indexing at scale?](#q16)
17. (Medium) [How do you implement data archiving strategies for old data in Django?](#q17)
18. (Medium) [What is the role of database-level load balancers (e.g., ProxySQL) with Django ORM?](#q18)
19. (Medium) [How do you manage connection limits on PostgreSQL when scaling Celery workers?](#q19)
20. (Hard) [How do you implement horizontal scale-out for Django model storage?](#q20)
21. (Medium) [What are materialized views and how do you map them to Django models?](#q21)
22. (Medium) [How do you refresh materialized views asynchronously?](#q22)
23. (Medium) [What is the query overhead of Django's default session and authentication backends at scale?](#q23)
24. (Medium) [How does Django 5.0's db_default optimize database inserts under high load?](#q24)
25. (Medium) [How do you monitor database CPU, IO, and memory usage spikes caused by Django ORM?](#q25)
26. (Hard) [Explain how to implement list partitioning in Django.](#q26)
27. (Medium) [How do you write a cleanup job that deletes old rows in small chunks?](#q27)
28. (Medium) [What is the index size comparison of Integer vs UUID at 100M rows?](#q28)
29. (Hard) [How do you write custom SQL to partition tables in PostgreSQL migrations?](#q29)
30. (Medium) [Explain the concept of write amplification in indexes.](#q30)
31. (Hard) [How do you integrate PgBouncer transaction pooling with transaction.atomic?](#q31)
32. (Medium) [What is the database impact of connection timeouts under traffic spikes?](#q32)
33. (Hard) [How do you configure range partitioning by date in Django?](#q33)
34. (Medium) [How do you write a script to check for fragmented indexes?](#q34)
35. (Hard) [How does table partitioning affect unique constraints?](#q35)

---

<a name="q1"></a>
## Q1. (Hard) How do you design an ORM scaling strategy for tables with 500M+ rows?
**Answer:**
1. Every query filters on indexed columns and is paginated with keyset pagination — never unbounded scans or OFFSET.
2. Partition the table (usually by date) so queries and retention touch only recent partitions.
3. Fetch only needed columns (`values()`/`only()`), avoid N+1, avoid `COUNT(*)` on the whole table.
4. Pre-aggregate for dashboards (summary tables / materialized views).
5. Route heavy reads to replicas; cache hot data.
6. Batch all writes/backfills; archive old data.

---

<a name="q2"></a>
## Q2. (Hard) How do you implement table partitioning (range, list, hash) in Django models?
**Answer:** Django has no built-in partitioning. Create the partitioned table with `RunSQL` (`PARTITION BY RANGE/LIST/HASH`) and partitions, and keep the model as a normal (often `managed=False`) model pointing to the parent table — queries work unchanged. Packages like `django-postgres-extra` help. Note the partition key must be part of the primary key/unique constraints.

---

<a name="q3"></a>
## Q3. (Medium) How do you integrate Redis/Memcached cache with Django ORM to prevent database hits?
**Answer:** Cache-aside: read from cache, on miss query the DB and store the result; invalidate on write.

```python
def get_product(pk):
    return cache.get_or_set(f"product:{pk}", lambda: Product.objects.get(pk=pk), 600)

def update_product(p):
    p.save()
    transaction.on_commit(lambda: cache.delete(f"product:{p.pk}"))
```
Cache serialized values (dicts) rather than querysets; pick TTLs per data type.

---

<a name="q4"></a>
## Q4. (Medium) What is cache stampede and how do you prevent it in Django?
**Answer:** When a popular cache key expires, many requests miss at the same time and all hit the DB together. Prevent with: a lock so only one request rebuilds (`cache.add("lock:key", 1, 30)`), random jitter in TTLs, refreshing the value before it expires (background job / cache warming), or serving the stale value while one request refreshes.

---

<a name="q5"></a>
## Q5. (Medium) How do you implement denormalization safely and keep data in sync using signals vs. database triggers?
**Answer:** Denormalize = store a copy/derived value (e.g. `order_count` on customer) to avoid joins/aggregates.
- **Signals/app code**: easy to write, but skipped by `update()`, bulk ops and raw SQL.
- **DB triggers**: always run (any writer), but logic is hidden in the DB and harder to test.
- Or recompute periodically with a job.
Use `F()` updates in the same transaction, and have a repair job that recomputes values.

---

<a name="q6"></a>
## Q6. (Medium) What are read replicas and how do you load balance database read queries?
**Answer:** Copies of the primary DB kept up to date by replication, used only for reads. In Django, a router sends reads to replicas (random/round-robin across aliases) and writes to the primary; or one replica endpoint behind a load balancer/proxy. Handle replication lag (read your own writes from the primary).

---

<a name="q7"></a>
## Q7. (Medium) How does connection pooling improve Django ORM performance at scale?
**Answer:** Opening a PostgreSQL connection is expensive (a new server process, authentication). A pool keeps connections open and reuses them, saving latency per request and capping the total connections the DB sees. Options: `CONN_MAX_AGE` (persistent, per worker), Django 5.1's PostgreSQL pool, or PgBouncer in front of the DB.

---

<a name="q8"></a>
## Q8. (Medium) How do you configure pgbouncer with Django and what is transaction pooling vs. session pooling?
**Answer:** Point Django's `HOST`/`PORT` at PgBouncer.
- **Session pooling** — a client keeps one server connection for its whole session; everything works, but saves fewer connections.
- **Transaction pooling** — a server connection is assigned per transaction; scales much better, but session features break (server-side cursors, session `SET`, advisory locks, prepared statements).
With transaction pooling set `DISABLE_SERVER_SIDE_CURSORS = True` and usually `CONN_MAX_AGE = 0`.

---

<a name="q9"></a>
## Q9. (Medium) What is the impact of long-running operations on Django connection management?
**Answer:** A long request/task holds its DB connection (and maybe locks) the whole time, so under load the pool runs out and others wait. Long transactions also block VACUUM. Keep DB work short, move slow work (API calls, file processing) outside transactions or to background jobs, and call `close_old_connections()` in long-running workers.

---

<a name="q10"></a>
## Q10. (Medium) How do you optimize Django ORM for write-heavy workloads?
**Answer:** Batch writes (`bulk_create`/`bulk_update`), use `update()`/`F()` instead of read-modify-write, keep transactions short, minimise indexes on hot tables, avoid signals on hot models, use queues to smooth spikes, and partition big append-only tables. For very high insert rates use `COPY` or buffered inserts.

---

<a name="q11"></a>
## Q11. (Medium) How do you scale read-heavy workloads using query caching and materialised views?
**Answer:** Cache hot query results in Redis (cache-aside, invalidate on write or short TTL); use read replicas; and for expensive reports, materialized views or summary tables refreshed by a scheduled job, exposed through unmanaged models. Paginate and keep responses small.

---

<a name="q12"></a>
## Q12. (Easy) What is the difference between database sharding and partitioning?
**Answer:** **Partitioning** splits one table into smaller pieces **inside one database** (transparent to queries). **Sharding** splits data across **multiple database servers** — scales writes and storage beyond one machine, but the app must route queries and cross-shard queries/transactions become hard.

---

<a name="q13"></a>
## Q13. (Hard) How do you implement database sharding in a Django architecture?
**Answer:** One DB alias per shard; choose the shard from a shard key (tenant/customer id) via a lookup table or hash; route with a router or `using(shard)`. Keep all data of one tenant on one shard, generate globally unique ids (UUID/snowflake), and do cross-shard reports by querying each shard and merging (or in a warehouse). Plan re-sharding from day one.

---

<a name="q14"></a>
## Q14. (Medium) What is database index bloat and how do you resolve it at scale?
**Answer:** Dead entries from updates/deletes make indexes bigger than needed, wasting cache and I/O. At scale: tune autovacuum for hot tables, monitor bloat, and rebuild bloated indexes online with `REINDEX CONCURRENTLY` or `pg_repack` during quiet periods. Fewer updates to indexed columns reduces it.

---

<a name="q15"></a>
## Q15. (Medium) How do you use Django ORM to query partitioned database tables?
**Answer:** Normally — the model points at the parent table and PostgreSQL routes queries to partitions. Include the partition key in filters (e.g. `created_at__gte=...`) so the planner can skip partitions (**partition pruning**); queries without it scan every partition.

---

<a name="q16"></a>
## Q16. (Medium) What is the performance impact of UUID primary keys on database indexing at scale?
**Answer:** UUIDs are 16 bytes vs 8 for `bigint`, so the pk index and every FK index are bigger. Random UUIDv4 values insert at random places in the B-tree → page splits, poor cache locality, more I/O on inserts (especially in clustered-index databases). Time-ordered UUIDs (v7) or bigint pk + separate public UUID avoid most of this.

---

<a name="q17"></a>
## Q17. (Medium) How do you implement data archiving strategies for old data in Django?
**Answer:** Define retention rules; move old rows to an archive table/database or cold storage (S3/Parquet) with a scheduled job in batches, then delete them from the hot table. With partitioning, detach old partitions (instant). Keep archive data queryable if needed (unmanaged model on the archive DB).

---

<a name="q18"></a>
## Q18. (Medium) What is the role of database-level load balancers (e.g., ProxySQL) with Django ORM?
**Answer:** A proxy (ProxySQL for MySQL; PgBouncer/HAProxy/Pgpool for PostgreSQL) sits between Django and the DBs: connection pooling, read/write splitting, health checks and failover — without changing Django code. Watch out for routing reads that need fresh data to lagging replicas.

---

<a name="q19"></a>
## Q19. (Medium) How do you manage connection limits on PostgreSQL when scaling Celery workers?
**Answer:** Each worker process/thread can hold its own connection, so total = processes × concurrency × aliases. Control it: lower worker concurrency, put PgBouncer in front, close connections after tasks (`CONN_MAX_AGE = 0` or `close_old_connections()`), and size `max_connections` for web + workers together.

---

<a name="q20"></a>
## Q20. (Hard) How do you implement horizontal scale-out for Django model storage?
**Answer:** Steps in order: vertical scaling + indexing → read replicas → caching → partitioning big tables → move some domains (e.g. logs, analytics) to separate databases via routers → shard by tenant when one primary can't handle the writes. Non-relational data (events, search, blobs) can move to purpose-built stores.

---

<a name="q21"></a>
## Q21. (Medium) What are materialized views and how do you map them to Django models?
**Answer:** A materialized view stores the result of a query as a table (unlike a normal view, which re-runs each time) — great for heavy reports. Create it with `RunSQL` and map it with an unmanaged model.

```python
class SalesSummary(models.Model):
    region = models.CharField(max_length=50, primary_key=True)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    class Meta:
        managed = False
        db_table = "sales_summary_mv"
```

---

<a name="q22"></a>
## Q22. (Medium) How do you refresh materialized views asynchronously?
**Answer:** Run `REFRESH MATERIALIZED VIEW CONCURRENTLY view_name` from a scheduled job (cron/Celery beat). `CONCURRENTLY` keeps the view readable during refresh but needs a unique index on the view. Refresh interval = how stale the data may be.

```python
with connection.cursor() as cur:
    cur.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY sales_summary_mv")
```

---

<a name="q23"></a>
## Q23. (Medium) What is the query overhead of Django's default session and authentication backends at scale?
**Answer:** With DB sessions, each request reads the session row (and writes it if modified), and `request.user` adds a user query — plus permission queries when checked. At scale use cached sessions (Redis: `cache` or `cached_db` engine), cache permission sets per request, and use token/JWT auth for APIs where it fits.

---

<a name="q24"></a>
## Q24. (Medium) How does Django 5.0's db_default optimize database inserts under high load?
**Answer:** The DB computes default values (e.g. `Now()`, sequences) itself, so Django doesn't need to compute or send them, and the values are consistent across all writers. The gain is mostly consistency and simpler inserts from other systems rather than raw speed.

---

<a name="q25"></a>
## Q25. (Medium) How do you monitor database CPU, IO, and memory usage spikes caused by Django ORM?
**Answer:** Infrastructure metrics (cloud monitoring / Prometheus exporters) for CPU, I/O, connections; `pg_stat_statements` to see which queries cost the most; `pg_stat_activity` for what runs right now; APM tracing to link slow queries to endpoints; slow-query logs (`log_min_duration_statement`). Correlate spikes with deploys and cron jobs.

---

<a name="q26"></a>
## Q26. (Hard) Explain how to implement list partitioning in Django.
**Answer:** Partition by a discrete value (region, tenant type) with `RunSQL`:

```sql
CREATE TABLE sales_order (id bigserial, region text NOT NULL, ..., PRIMARY KEY (id, region))
    PARTITION BY LIST (region);
CREATE TABLE sales_order_eu PARTITION OF sales_order FOR VALUES IN ('EU');
CREATE TABLE sales_order_us PARTITION OF sales_order FOR VALUES IN ('US');
```
Model points at `sales_order`; filtering by `region` prunes partitions. Add a DEFAULT partition for unexpected values.

---

<a name="q27"></a>
## Q27. (Medium) How do you write a cleanup job that deletes old rows in small chunks?
**Answer:**

```python
def purge_old_logs(cutoff, batch=5000):
    while ids := list(Log.objects.filter(created_at__lt=cutoff)
                      .values_list("id", flat=True)[:batch]):
        Log.objects.filter(id__in=ids).delete()
        time.sleep(0.1)            # let replication / other traffic breathe
```
Small batches keep locks short; index `created_at`. For time-based data, dropping partitions is even better.

---

<a name="q28"></a>
## Q28. (Medium) What is the index size comparison of Integer vs UUID at 100M rows?
**Answer:** Keys are 4 bytes (int) / 8 bytes (bigint) vs 16 bytes (UUID), plus per-entry overhead, so a UUID pk index is roughly 1.5–2× the size of a bigint one — and every FK index referencing it grows too. Random UUIDv4 adds fragmentation on top. At 100M rows that's gigabytes of extra index and less of it fits in memory.

---

<a name="q29"></a>
## Q29. (Hard) How do you write custom SQL to partition tables in PostgreSQL migrations?
**Answer:** Use `RunSQL` with forward and reverse SQL, and tell Django about the model with `state_operations` (or use an unmanaged model).

```python
migrations.RunSQL(
    sql="""CREATE TABLE events_event (id bigserial, created_at timestamptz NOT NULL, data jsonb,
                                      PRIMARY KEY (id, created_at)) PARTITION BY RANGE (created_at);""",
    reverse_sql="DROP TABLE events_event;")
```
Create future partitions with a scheduled job (or `pg_partman`).

---

<a name="q30"></a>
## Q30. (Medium) Explain the concept of write amplification in indexes.
**Answer:** One logical write causes many physical writes: the table row, every index entry, WAL for each, and (in PostgreSQL) a new row version on UPDATE — which may need new entries in all indexes. More indexes and frequent updates of indexed columns = more amplification, slower writes and more replication traffic.

---

<a name="q31"></a>
## Q31. (Hard) How do you integrate PgBouncer transaction pooling with transaction.atomic?
**Answer:** `atomic()` works fine — the whole transaction runs on one server connection. What breaks are things that live **outside** a transaction: session `SET` (use `SET LOCAL`), session advisory locks (use `pg_advisory_xact_lock`), server-side cursors (`DISABLE_SERVER_SIDE_CURSORS = True`) and prepared statements. Keep transactions short, since each holds a server connection.

---

<a name="q32"></a>
## Q32. (Medium) What is the database impact of connection timeouts under traffic spikes?
**Answer:** When the pool is exhausted, requests wait and then fail with connection timeouts; retries make the spike worse (thundering herd). Mitigate with a pooler, sensible pool/queue sizes and timeouts, statement timeouts so slow queries free connections, rate limiting/back-pressure, and caching to reduce DB load.

---

<a name="q33"></a>
## Q33. (Hard) How do you configure range partitioning by date in Django?
**Answer:** Create a parent table `PARTITION BY RANGE (created_at)` via `RunSQL`, then monthly partitions:

```sql
CREATE TABLE events_event_2026_11 PARTITION OF events_event
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
```
A scheduled job creates next month's partition in advance and detaches/drops old ones. Queries filtering on `created_at` hit only the relevant partitions.

---

<a name="q34"></a>
## Q34. (Medium) How do you write a script to check for fragmented indexes?
**Answer:** On PostgreSQL use the `pgstattuple` extension (`pgstatindex('index_name')` → `avg_leaf_density`, `leaf_fragmentation`) or a known bloat-estimate query; on SQL Server `sys.dm_db_index_physical_stats` (`avg_fragmentation_in_percent`). Run it from a management command/cron and report indexes above a threshold for `REINDEX CONCURRENTLY`.

---

<a name="q35"></a>
## Q35. (Hard) How does table partitioning affect unique constraints?
**Answer:** In PostgreSQL a unique constraint (including the primary key) on a partitioned table **must include the partition key** — uniqueness is only enforced per partition. So `id` alone can't be the pk; it becomes `(id, created_at)`. For global uniqueness of another column, you need a separate lookup table or application-level checks.
