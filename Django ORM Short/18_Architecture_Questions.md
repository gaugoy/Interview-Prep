# Module 18: Architecture & Design Patterns (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/18_Architecture_Questions.md)

## Table of Contents
1. (Medium) [Active Record vs. Data Mapper pattern: Which one is Django ORM and what are the trade-offs?](#q1)
2. (Medium) [How do you implement the Repository Pattern on top of Django ORM?](#q2)
3. (Medium) [What are the architectural pros and cons of using Django Service Layer vs. Model Methods?](#q3)
4. (Hard) [How do you design a clean CQRS (Command Query Responsibility Segregation) architecture in Django?](#q4)
5. (Hard) [How do you isolate Django models from domain logic in clean/hexagonal architecture?](#q5)
6. (Medium) [What is the impact of using Fat Models vs. Fat Views vs. Service Classes?](#q6)
7. (Medium) [How do you handle validation at different architecture layers (ORM, serializers, forms, domain)?](#q7)
8. (Hard) [How do you design a robust multi-tenant architecture (shared db/shared schema vs. shared db/isolated schema vs. isolated db)?](#q8)
9. (Medium) [What are the architectural trade-offs of using Generic Foreign Keys?](#q9)
10. (Medium) [How do you implement a soft delete system that is transparent to the business domain layer?](#q10)
11. (Hard) [How do you decouple database schema changes from application code deployments?](#q11)
12. (Medium) [What is the best architecture for auditing changes to model fields in production?](#q12)
13. (Hard) [How do you architect event-driven updates in Django using database change data capture (CDC) vs. signals?](#q13)
14. (Medium) [When is it architecturally appropriate to use raw SQL instead of Django ORM?](#q14)
15. (Medium) [How do you handle API versioning when model fields are refactored or deleted?](#q15)
16. (Medium) [What are the structural trade-offs of using Single Table Inheritance vs. Class Table Inheritance?](#q16)
17. (Medium) [How do you isolate query-only models for reporting screens?](#q17)
18. (Hard) [How do you architect a database configuration for an application with 10,000+ tenants?](#q18)
19. (Medium) [How do you design the model layer for search integration (e.g., Elasticsearch with Django)?](#q19)
20. (Medium) [What are the architecture issues with model signals in distributed systems?](#q20)
21. (Hard) [How do you structure database connection lifetime for serverless deployments (AWS Lambda) of Django?](#q21)
22. (Medium) [How do you enforce architecture-level read-only locks on certain models?](#q22)
23. (Medium) [How do you decouple Django's default auth models from your domain customer models?](#q23)
24. (Easy) [What is the role of django-environ and settings configuration in database architecture?](#q24)
25. (Medium) [How does Django 5.0's GeneratedField help in pushing domain calculations into the persistence layer?](#q25)
26. (Medium) [How do you design a robust retry queue pattern for transient database connection drops?](#q26)
27. (Medium) [Explain the role of Database Isolation layers in microservices.](#q27)
28. (Hard) [How do you implement secure data erasure (right to be forgotten) under GDPR using ORM?](#q28)
29. (Medium) [How do you configure dynamic custom domain mapping for tenant sites?](#q29)
30. (Medium) [What is the architectural impact of using UUIDv4 for indexes on write throughput?](#q30)
31. (Hard) [How do you design audit tables that store change history without double writes?](#q31)
32. (Medium) [Explain the Outbox Pattern in event-driven Django architectures.](#q32)
33. (Hard) [How do you implement API rate limiting at the database layer using sliding windows?](#q33)
34. (Hard) [Explain table partitioning architecture for multi-tenant SaaS platforms.](#q34)
35. (Medium) [How do you isolate legacy databases in Django using unmanaged models?](#q35)

---

<a name="q1"></a>
## Q1. (Medium) Active Record vs. Data Mapper pattern: Which one is Django ORM and what are the trade-offs?
**Answer:** Django is **Active Record**: a model object represents a row and saves itself (`obj.save()`). Pros: simple, fast to build, great admin/forms integration. Cons: domain logic is tied to the database model, harder to unit-test without a DB. **Data Mapper** (SQLAlchemy ORM) keeps plain domain objects separate from persistence — more flexible, more code.

---

<a name="q2"></a>
## Q2. (Medium) How do you implement the Repository Pattern on top of Django ORM?
**Answer:** A class that hides queries behind domain methods, so business code doesn't use the ORM directly.

```python
class OrderRepository:
    def get(self, order_id) -> Order:
        return Order.objects.select_related("customer").get(pk=order_id)
    def open_for_customer(self, customer_id):
        return list(Order.objects.filter(customer_id=customer_id, status="open"))
```
Useful for testing (fake repositories) and swapping storage, but in Django it often duplicates what custom QuerySets already give you — use it where the abstraction pays off.

---

<a name="q3"></a>
## Q3. (Medium) What are the architectural pros and cons of using Django Service Layer vs. Model Methods?
**Answer:** **Model methods**: logic close to data, good for rules about a single object (`order.can_cancel()`). **Service functions**: orchestrate workflows across models, transactions and external calls (`place_order(cart, user)`), easier to test and reuse from views, APIs, tasks. Common split: simple per-object behaviour on models, multi-step use cases in services.

---

<a name="q4"></a>
## Q4. (Hard) How do you design a clean CQRS (Command Query Responsibility Segregation) architecture in Django?
**Answer:** Separate writes (commands → service functions with validation and transactions on the primary DB) from reads (queries → optimized read models: `values()` querysets, denormalized tables, materialized views, search index, or replicas). Keep read models in sync with events/outbox or scheduled refreshes. Worth it when read and write needs differ a lot; overkill for simple CRUD.

---

<a name="q5"></a>
## Q5. (Hard) How do you isolate Django models from domain logic in clean/hexagonal architecture?
**Answer:** Put business rules in plain Python domain classes/functions that don't import Django; define interfaces (repositories) for persistence; implement them with Django ORM in an adapter layer that converts models ↔ domain objects. Views/APIs call use-case services. You lose some Django convenience (admin, ModelForms) for testability and independence.

---

<a name="q6"></a>
## Q6. (Medium) What is the impact of using Fat Models vs. Fat Views vs. Service Classes?
**Answer:**
- **Fat views** — logic tied to HTTP, duplicated across views/APIs/tasks. Avoid.
- **Fat models** — reusable, but models grow huge and mix many concerns.
- **Service classes/functions** — clear use cases, easy to test and reuse; risk of becoming "anemic" models if overdone.
Thin views + small model methods + services for workflows is a common balance.

---

<a name="q7"></a>
## Q7. (Medium) How do you handle validation at different architecture layers (ORM, serializers, forms, domain)?
**Answer:**
- **Forms/serializers** — input shape and format (required, types, lengths).
- **Domain/service** — business rules ("can't ship unpaid order").
- **Model `clean()`** — object consistency (used by admin/forms).
- **Database constraints** — final guarantee (unique, check, FK) that also catches races.
Don't rely only on the top layer; critical rules belong in the DB too.

---

<a name="q8"></a>
## Q8. (Hard) How do you design a robust multi-tenant architecture (shared db/shared schema vs. shared db/isolated schema vs. isolated db)?
**Answer:**
| Model | Isolation | Cost / ops | Scales to |
|---|---|---|---|
| Shared schema + `tenant_id` column | weakest (app must filter) | cheapest, simple migrations | many tenants |
| Schema per tenant (django-tenants) | medium | migrations per schema | hundreds–thousands |
| Database per tenant | strongest | most expensive, routing + connections | few large tenants |
Choose by isolation/compliance needs and tenant count; shared schema needs tenant filtering enforced in a base manager/queryset.

---

<a name="q9"></a>
## Q9. (Medium) What are the architectural trade-offs of using Generic Foreign Keys?
**Answer:** Pros: one model can relate to any other (comments, tags, activity logs) without schema changes. Cons: no FK constraints (orphans), no JOINs/`select_related`, more queries, harder reporting and migrations. Use for truly generic cross-cutting features; prefer real FKs when the set of targets is known.

---

<a name="q10"></a>
## Q10. (Medium) How do you implement a soft delete system that is transparent to the business domain layer?
**Answer:** A base model/QuerySet where `delete()` sets `deleted_at`, the default manager hides deleted rows, an `all_objects` manager for admin/recovery, conditional unique constraints, and explicit handling of related objects. Domain code just calls `delete()` and queries as normal. Add a periodic job to hard-delete/archive old soft-deleted rows.

---

<a name="q11"></a>
## Q11. (Hard) How do you decouple database schema changes from application code deployments?
**Answer:** Use **expand/contract**: every schema change is backward compatible with the running code version. Add new columns/tables first (expand), deploy code that uses both, backfill, switch reads, then remove old structures in a later release (contract). Run migrations as a separate step before the code rollout, and avoid locking migrations.

---

<a name="q12"></a>
## Q12. (Medium) What is the best architecture for auditing changes to model fields in production?
**Answer:** Options:
- **App-level history** (django-simple-history, django-auditlog) — easy, knows the user, but skipped by `update()`/bulk/raw SQL.
- **DB triggers** writing to an audit table — catches every change, but no app user unless you pass it in a session variable.
- **CDC** (logical replication / Debezium) streaming changes to an audit store.
For compliance, combine DB-level capture with the app user context.

---

<a name="q13"></a>
## Q13. (Hard) How do you architect event-driven updates in Django using database change data capture (CDC) vs. signals?
**Answer:** **Signals** run in-process inside the transaction: easy, but lost on crash, skipped by bulk updates, and not reliable for other services. **CDC** reads the database log (logical replication, Debezium) and publishes every committed change to a broker — reliable and complete, but more infrastructure. The **outbox pattern** sits in between: write an event row in the same transaction; a worker publishes it.

---

<a name="q14"></a>
## Q14. (Medium) When is it architecturally appropriate to use raw SQL instead of Django ORM?
**Answer:** When the ORM can't express it (recursive CTEs, LATERAL joins, complex window frames, DB-specific features), when a hot query needs exact hand-tuned SQL, for bulk operations (`COPY`, `MERGE`), or for reporting on legacy schemas. Keep it parameterised, wrapped in one function, and tested; everything else stays in the ORM.

---

<a name="q15"></a>
## Q15. (Medium) How do you handle API versioning when model fields are refactored or deleted?
**Answer:** Decouple API from models: serializers (per version) map fields, so `v1` can keep returning the old field name computed from the new structure while `v2` uses the new one. Change the database with expand/contract, deprecate old fields with a timeline, and remove them only when no client uses the old version.

---

<a name="q16"></a>
## Q16. (Medium) What are the structural trade-offs of using Single Table Inheritance vs. Class Table Inheritance?
**Answer:** **Single table** (one table + type column): no joins, simple queries, but many nullable columns and weaker constraints. **Class table** (Django multi-table inheritance): normalized, strict columns per type, but every child query joins and writes touch multiple tables. Few type-specific fields → single table; many distinct fields and cross-type queries rare → separate tables.

---

<a name="q17"></a>
## Q17. (Medium) How do you isolate query-only models for reporting screens?
**Answer:** Create read-only models (`managed = False`) on top of database views/materialized views or reporting tables, route them to a replica or reporting database, and block writes (override `save()`/`delete()` to raise, read-only DB user). Reporting queries then don't touch or lock the transactional tables.

---

<a name="q18"></a>
## Q18. (Hard) How do you architect a database configuration for an application with 10,000+ tenants?
**Answer:** Database-per-tenant doesn't scale to 10k (connections, migrations, cost). Use a shared database with a `tenant_id` on every table (enforced by base managers / row-level security), tenant-leading composite indexes, partitioning or sharding by tenant as data grows, and separate dedicated databases only for a few very large/regulated tenants.

---

<a name="q19"></a>
## Q19. (Medium) How do you design the model layer for search integration (e.g., Elasticsearch with Django)?
**Answer:** PostgreSQL stays the source of truth; Elasticsearch holds a denormalized search document per object. Index updates happen asynchronously after commit (signals/outbox → task queue → bulk index), with a full re-index command for recovery. Search returns ids, then load fresh objects from the DB if needed. Libraries: django-elasticsearch-dsl.

---

<a name="q20"></a>
## Q20. (Medium) What are the architecture issues with model signals in distributed systems?
**Answer:** Signals are in-process and synchronous: other services never see them, they fire before commit (listeners may act on data that rolls back), they're skipped by bulk updates/raw SQL, and they hide control flow. For cross-service events use `on_commit` + a message broker, the outbox pattern, or CDC.

---

<a name="q21"></a>
## Q21. (Hard) How do you structure database connection lifetime for serverless deployments (AWS Lambda) of Django?
**Answer:** Each function instance can open its own connection, and many concurrent instances can exhaust the database. Use a proxy pooler (RDS Proxy / PgBouncer), keep `CONN_MAX_AGE` low or 0 (or reuse a warm instance's connection with health checks), set short timeouts, and limit function concurrency.

---

<a name="q22"></a>
## Q22. (Medium) How do you enforce architecture-level read-only locks on certain models?
**Answer:** Layers of protection: a DB user with only SELECT permission (or route the model to a read-only alias), override `save()`/`delete()` to raise, a read-only QuerySet that blocks `update()`/`delete()`, and read-only admin. The DB permission is the real guarantee.

---

<a name="q23"></a>
## Q23. (Medium) How do you decouple Django's default auth models from your domain customer models?
**Answer:** Use a custom user model from day one (`AUTH_USER_MODEL`, minimal: login identity only) and keep business data in separate models (`Customer`, `Employee`) linked by a OneToOne/FK. Reference users via `settings.AUTH_USER_MODEL` / `get_user_model()`. This lets one person have several roles and keeps auth concerns separate.

---

<a name="q24"></a>
## Q24. (Easy) What is the role of django-environ and settings configuration in database architecture?
**Answer:** It reads configuration from environment variables (12-factor style), e.g. `DATABASES = {"default": env.db("DATABASE_URL")}` — so each environment has its own credentials/hosts without code changes and secrets stay out of the repo. Pool, timeout and replica settings are configured the same way.

---

<a name="q25"></a>
## Q25. (Medium) How does Django 5.0's GeneratedField help in pushing domain calculations into the persistence layer?
**Answer:** Simple, deterministic calculations on a row (totals, normalized values, derived flags) are computed by the DB, so every writer (Django, scripts, other services) gets the same value and you can index/filter on it. Keep it to stable, same-row formulas; real business rules that change often or need other tables belong in code.

---

<a name="q26"></a>
## Q26. (Medium) How do you design a robust retry queue pattern for transient database connection drops?
**Answer:** Retry only **transient** errors (`OperationalError`, connection lost) and only for **idempotent** units of work, with exponential backoff + jitter and a max attempts limit. Retry the whole transaction (never the middle of one), call `close_old_connections()` before retrying, and send permanently failing jobs to a dead-letter queue.

---

<a name="q27"></a>
## Q27. (Medium) Explain the role of Database Isolation layers in microservices.
**Answer:** Each service owns its database; others access its data only through its API or events — never by querying its tables. This lets services change schemas and scale independently. Cost: no cross-service joins or transactions, so you need events, data duplication (read models) and eventual consistency.

---

<a name="q28"></a>
## Q28. (Hard) How do you implement secure data erasure (right to be forgotten) under GDPR using ORM?
**Answer:** Find all personal data for the user (map it per model), then delete or **anonymize** it in one transaction — anonymize where records must be kept (invoices, audit), delete elsewhere. Also purge caches, search indexes, files and backups policy, and log the erasure request itself. A registry of "personal data fields" per model keeps this maintainable.

---

<a name="q29"></a>
## Q29. (Medium) How do you configure dynamic custom domain mapping for tenant sites?
**Answer:** Store `domain → tenant` in a table, cache it, and resolve it in middleware from `request.get_host()`, setting the current tenant (and its DB/schema). Allowed hosts must accept those domains (validate against the table), and TLS certificates are handled at the proxy/load balancer.

---

<a name="q30"></a>
## Q30. (Medium) What is the architectural impact of using UUIDv4 for indexes on write throughput?
**Answer:** Random keys insert into random index pages, causing page splits, poor cache hit rates and more I/O — write throughput drops as tables grow (worst on clustered-index DBs like InnoDB/SQL Server). Use bigint keys internally with a UUID public id, or time-ordered UUIDs (v7) that insert near the end of the index.

---

<a name="q31"></a>
## Q31. (Hard) How do you design audit tables that store change history without double writes?
**Answer:** Let the database capture changes: a trigger on the table writes the old/new row (e.g. as JSONB) into an audit table within the same statement, or use CDC from the WAL. The application does a single write; pass the user/request id via `SET LOCAL app.user_id = ...` so the trigger can record who did it.

---

<a name="q32"></a>
## Q32. (Medium) Explain the Outbox Pattern in event-driven Django architectures.
**Answer:** In the same transaction as your business change, insert an event row into an `outbox` table. A separate worker reads unsent rows, publishes them to the broker (RabbitMQ/Kafka) and marks them sent. Because the event is committed atomically with the data, you never publish events for rolled-back changes or lose events on crash. Consumers must be idempotent (at-least-once delivery).

---

<a name="q33"></a>
## Q33. (Hard) How do you implement API rate limiting at the database layer using sliding windows?
**Answer:** Store request timestamps (or per-minute counters) per client and count those in the window before allowing a request — e.g. `RequestLog.objects.filter(client=c, at__gte=now - 60s).count()`, or an atomic upsert of a per-window counter. It works, but adds writes on every request; Redis is usually better for rate limiting, with the DB for durable quotas/billing.

---

<a name="q34"></a>
## Q34. (Hard) Explain table partitioning architecture for multi-tenant SaaS platforms.
**Answer:** Partition big shared tables by `tenant_id` (list/hash) or by time, with tenant-leading indexes. Benefits: tenant queries prune to one partition, large tenants can get their own partition (or be moved to another DB), and per-tenant data deletion = dropping a partition. Primary keys must include the partition key.

---

<a name="q35"></a>
## Q35. (Medium) How do you isolate legacy databases in Django using unmanaged models?
**Answer:** Generate models with `inspectdb`, set `managed = False` and `db_table`, route them to a separate alias with a router (and `allow_migrate` returning False for it), and give the app a read-only DB user if it shouldn't write. Wrap access in a small service layer so the legacy schema doesn't leak through the codebase.
