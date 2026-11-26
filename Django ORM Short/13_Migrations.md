# Module 13: Migrations & Schema Evolution (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/13_Migrations.md)

## Table of Contents
1. (Easy) [How does Django's migration engine detect model changes?](#q1)
2. (Easy) [What is the structure of a migration file and what is the role of dependencies?](#q2)
3. (Easy) [What is the difference between schema migrations and data migrations?](#q3)
4. (Medium) [How do you write a safe data migration that updates database rows?](#q4)
5. (Medium) [Why is it dangerous to import models directly inside a data migration, and how do you avoid it?](#q5)
6. (Medium) [How does Django run migrations transactionally and which databases support it?](#q6)
7. (Medium) [What is migration squashing and how do you do it safely in production?](#q7)
8. (Easy) [How do you resolve migration conflicts in a team environment?](#q8)
9. (Easy) [How does the migration history table (django_migrations) work under the hood?](#q9)
10. (Hard) [What are the strategies for migrating a large table (10M+ rows) with zero downtime?](#q10)
11. (Medium) [How do you add a non-nullable field to an existing table without breaking production?](#q11)
12. (Medium) [How do you rename a field in a model without causing downtime or query failures?](#q12)
13. (Medium) [How do you drop a column from a large database table safely in production?](#q13)
14. (Easy) [What is RunSQL and how do you use it to execute raw database migration scripts?](#q14)
15. (Medium) [What is RunPython and how does it access model history?](#q15)
16. (Easy) [How does Django handle migrations for unmanaged models (managed=False)?](#q16)
17. (Medium) [How do you run migrations across multiple databases using routers?](#q17)
18. (Easy) [What is the role of MIGRATION_MODULES setting in Django?](#q18)
19. (Medium) [How do you write a migration that creates a database view?](#q19)
20. (Easy) [How do you roll back a migration in Django?](#q20)
21. (Medium) [What are the risks of using python functions inside migration files?](#q21)
22. (Easy) [How do you dry-run migrations to check their SQL output?](#q22)
23. (Medium) [How does Django handle index creation in migrations for PostgreSQL vs. SQLite?](#q23)
24. (Medium) [What is the impact of long-running migrations on database locks?](#q24)
25. (Medium) [How do you test migrations to ensure they do not fail when deployed to staging?](#q25)
26. (Hard) [What is the internal design of MigrationAutodetector?](#q26)
27. (Hard) [How does migration squashing resolve Circular Dependency errors?](#q27)
28. (Medium) [How do you execute post-migration signals safely?](#q28)
29. (Hard) [Explain the role of StateApps inside RunPython execution context.](#q29)
30. (Hard) [How do you write a database migration that changes field types without locking?](#q30)
31. (Medium) [Explain the interaction between migrations and connection pooling.](#q31)
32. (Medium) [What is the risk of using schema_editor.execute inside RunPython?](#q32)
33. (Medium) [How do you enforce read-only tables in Django using custom migrations?](#q33)
34. (Medium) [How does migration autodetector handle default value updates?](#q34)
35. (Easy) [What is the structure of django_migrations database table?](#q35)

---

<a name="q1"></a>
## Q1. (Easy) How does Django's migration engine detect model changes?
**Answer:** `makemigrations` rebuilds the project state from existing migration files, compares it with your current models, and writes the differences as operations (`AddField`, `AlterField`, …) in a new migration file. It never looks at the actual database.

---

<a name="q2"></a>
## Q2. (Easy) What is the structure of a migration file and what is the role of dependencies?
**Answer:** A `Migration` class with `dependencies` (migrations that must run first — same app's previous migration, other apps' migrations for FKs) and `operations` (list of changes). Dependencies build a graph so Django applies migrations in a safe order across apps.

```python
class Migration(migrations.Migration):
    dependencies = [("shop", "0004_order_status")]
    operations = [migrations.AddField("order", "note", models.TextField(blank=True))]
```

---

<a name="q3"></a>
## Q3. (Easy) What is the difference between schema migrations and data migrations?
**Answer:** **Schema** migrations change structure (tables, columns, indexes) and are usually auto-generated. **Data** migrations change rows (backfill, transform, seed) and you write them with `RunPython`/`RunSQL` — create an empty one with `makemigrations app --empty`.

---

<a name="q4"></a>
## Q4. (Medium) How do you write a safe data migration that updates database rows?
**Answer:** Use the historical model from `apps`, process in batches, and provide a reverse.

```python
def forwards(apps, schema_editor):
    Order = apps.get_model("shop", "Order")
    Order.objects.filter(status="").update(status="new")

class Migration(migrations.Migration):
    dependencies = [("shop", "0005_order_status")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
```
For big tables, update in PK batches (or run as a management command outside the deploy).

---

<a name="q5"></a>
## Q5. (Medium) Why is it dangerous to import models directly inside a data migration, and how do you avoid it?
**Answer:** A direct import uses the **current** model code, but the migration must work against the schema as it was at that point in history. Later field changes break old migrations (missing/renamed columns). Always use `apps.get_model("app", "Model")` — the historical version.

---

<a name="q6"></a>
## Q6. (Medium) How does Django run migrations transactionally and which databases support it?
**Answer:** Each migration runs in a transaction on databases with transactional DDL — **PostgreSQL and SQLite** — so a failure rolls it back fully. **MySQL and Oracle** auto-commit DDL, so a failed migration can leave the schema half-changed. Set `atomic = False` on a migration that can't run in a transaction (e.g. `CREATE INDEX CONCURRENTLY`).

---

<a name="q7"></a>
## Q7. (Medium) What is migration squashing and how do you do it safely in production?
**Answer:** `squashmigrations app 0001 0040` combines many migrations into one (with a `replaces` list) to speed up test DB creation and clean history.
Safe steps: squash → deploy with both old and squashed files (Django knows they're equivalent) → once every environment has applied them, delete the old files and remove `replaces`. Review `RunPython` steps — they're copied over and may need fixing.

---

<a name="q8"></a>
## Q8. (Easy) How do you resolve migration conflicts in a team environment?
**Answer:** Two branches each added `0007_*` → Django sees two leaf nodes and refuses to migrate. Fix: `makemigrations --merge` (creates a merge migration), or delete your unapplied migration, pull, and regenerate it on top. Run `makemigrations --check` in CI to catch missing migrations.

---

<a name="q9"></a>
## Q9. (Easy) How does the migration history table (django_migrations) work under the hood?
**Answer:** Every applied migration is recorded as a row (`app`, `name`, `applied`). `migrate` compares the migration files' graph with this table and runs only those not recorded. `migrate --fake` adds a row without running the SQL; rolling back deletes the row.

---

<a name="q10"></a>
## Q10. (Hard) What are the strategies for migrating a large table (10M+ rows) with zero downtime?
**Answer:**
1. Use **expand → migrate → contract**: add new structure in a backward-compatible way, backfill in batches, switch code, remove old structure in a later release.
2. Avoid operations that rewrite or lock the table (type changes, adding non-null without default on old DBs).
3. Create indexes `CONCURRENTLY`.
4. Set `lock_timeout` so a migration fails fast instead of blocking traffic.
5. Run backfills outside the deploy as batched jobs.

---

<a name="q11"></a>
## Q11. (Medium) How do you add a non-nullable field to an existing table without breaking production?
**Answer:**
1. Add it as `null=True` (or with a default — on PostgreSQL 11+ a constant default is fast; Django 5.0 also has `db_default`).
2. Deploy code that writes the field.
3. Backfill old rows in batches.
4. Change to `null=False` in a later migration.

---

<a name="q12"></a>
## Q12. (Medium) How do you rename a field in a model without causing downtime or query failures?
**Answer:** A direct rename breaks running old code that still uses the old name. Options:
- Rename only in Python: keep the column with `db_column="old_name"` — no DB change.
- Real rename: add new column → write to both → backfill → switch reads → drop old column later.

---

<a name="q13"></a>
## Q13. (Medium) How do you drop a column from a large database table safely in production?
**Answer:**
1. Deploy code that no longer uses the field (remove it from the model's usage first).
2. Remove the field from Django's state without touching the DB (`SeparateDatabaseAndState`), so old code still running doesn't break.
3. In a later release, drop the column with a real migration.
Dropping is quick on PostgreSQL (metadata), but it still needs a short exclusive lock — set `lock_timeout`.

---

<a name="q14"></a>
## Q14. (Easy) What is RunSQL and how do you use it to execute raw database migration scripts?
**Answer:** An operation that runs raw SQL — for things the ORM can't express (views, triggers, extensions). Give `reverse_sql` so it can be rolled back, and `state_operations` if it changes something Django should know about. (A `CONCURRENTLY` statement like the one below needs `atomic = False` on the migration.)

```python
migrations.RunSQL(
    "CREATE INDEX CONCURRENTLY idx_order_email ON shop_order (lower(email));",
    reverse_sql="DROP INDEX CONCURRENTLY idx_order_email;")
```

---

<a name="q15"></a>
## Q15. (Medium) What is RunPython and how does it access model history?
**Answer:** `RunPython(forwards, reverse_code)` runs Python functions during migration. They receive `apps` (historical models, as of that migration) and `schema_editor`. Historical models have fields but **no custom methods**, and only managers marked `use_in_migrations = True`.

---

<a name="q16"></a>
## Q16. (Easy) How does Django handle migrations for unmanaged models (managed=False)?
**Answer:** Migrations are still created (to track the model's state), but Django runs **no DDL** for them — it won't create, alter or drop the table. Used for existing legacy tables or database views managed outside Django.

---

<a name="q17"></a>
## Q17. (Medium) How do you run migrations across multiple databases using routers?
**Answer:** Run `migrate --database=alias` for each database. For every operation, Django asks the router's `allow_migrate(db, app_label, ...)` and skips models that don't belong there. In `RunPython`, check `schema_editor.connection.alias` so data migrations only run on the right DB.

---

<a name="q18"></a>
## Q18. (Easy) What is the role of MIGRATION_MODULES setting in Django?
**Answer:** Maps an app to a different migrations package: `MIGRATION_MODULES = {"blog": "blog.db_migrations"}`. Setting an app to `None` disables its migrations (tables created directly from models) — sometimes used to speed up tests.

---

<a name="q19"></a>
## Q19. (Medium) How do you write a migration that creates a database view?
**Answer:** Create the view with `RunSQL` and map it with an unmanaged model.

```python
migrations.RunSQL(
    "CREATE VIEW sales_summary AS SELECT region, SUM(total) AS total FROM shop_order GROUP BY region;",
    reverse_sql="DROP VIEW sales_summary;")

class SalesSummary(models.Model):
    region = models.CharField(max_length=50, primary_key=True)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    class Meta:
        managed = False
        db_table = "sales_summary"
```

---

<a name="q20"></a>
## Q20. (Easy) How do you roll back a migration in Django?
**Answer:** Migrate back to the previous migration: `python manage.py migrate shop 0004` (undoes everything after 0004), or `migrate shop zero` to undo all. It only works if operations are reversible — `RunPython`/`RunSQL` need reverse code. In production, a "fix-forward" migration is often safer than rolling back.

---

<a name="q21"></a>
## Q21. (Medium) What are the risks of using python functions inside migration files?
**Answer:** Imported functions/models change over time and can break old migrations; functions referenced in migrations (e.g. a `default=` callable or `upload_to`) must keep existing at the same import path forever; slow Python loops over big tables block deploys; and missing `reverse_code` makes migrations irreversible. Keep migration code self-contained.

---

<a name="q22"></a>
## Q22. (Easy) How do you dry-run migrations to check their SQL output?
**Answer:**
- `python manage.py sqlmigrate shop 0007` — show the SQL of one migration.
- `python manage.py migrate --plan` — list what would run.
- `python manage.py makemigrations --check --dry-run` — detect missing migrations (CI).

---

<a name="q23"></a>
## Q23. (Medium) How does Django handle index creation in migrations for PostgreSQL vs. SQLite?
**Answer:** On PostgreSQL, `AddIndex` runs a normal `CREATE INDEX`, which blocks writes on the table; use `AddIndexConcurrently` (from `django.contrib.postgres.operations`, migration `atomic = False`) on big tables. SQLite has no concurrent option and for many `ALTER` operations Django rebuilds the whole table (copy + rename).

---

<a name="q24"></a>
## Q24. (Medium) What is the impact of long-running migrations on database locks?
**Answer:** Many `ALTER TABLE` operations take an exclusive lock that blocks all reads and writes. Worse, if the migration waits behind a long query, every new query queues behind the migration — an outage. Mitigate with `lock_timeout`, concurrent index creation, batched backfills, and deploying migrations at low traffic.

---

<a name="q25"></a>
## Q25. (Medium) How do you test migrations to ensure they do not fail when deployed to staging?
**Answer:** Run `makemigrations --check` in CI, apply all migrations on a fresh DB in CI, test risky data migrations against a copy of production data on staging (timing and locks), test reverse migrations, and use `django-test-migrations` for unit tests of specific migrations.

---

<a name="q26"></a>
## Q26. (Hard) What is the internal design of MigrationAutodetector?
**Answer:** It receives two project states — "from" (built from migration files) and "to" (current models) — and runs a series of `generate_*` steps (created/deleted models, added/removed/altered fields, renames, indexes, constraints). Ambiguous cases like renames are confirmed through a questioner (the prompts you see). Then it sorts operations by dependency and splits them into migration files per app.

---

<a name="q27"></a>
## Q27. (Hard) How does migration squashing resolve Circular Dependency errors?
**Answer:** Squashing can create a circular dependency when two apps' migrations depend on each other (A needs B's table, B has an FK to A). Fix by squashing smaller ranges, moving the cross-app FK into a separate later migration, or editing dependencies by hand so the graph is acyclic again.

---

<a name="q28"></a>
## Q28. (Medium) How do you execute post-migration signals safely?
**Answer:** `post_migrate` runs after `migrate` (also during tests and for every database). Handlers should be idempotent (`get_or_create`), use the `using` argument for the right DB, and use the `apps` argument (historical models) instead of importing models. Avoid heavy work there.

---

<a name="q29"></a>
## Q29. (Hard) Explain the role of StateApps inside RunPython execution context.
**Answer:** `StateApps` is a temporary app registry built from migration state — the `apps` argument in `RunPython`. It contains "fake" historical model classes that match the schema at that migration. That's why `apps.get_model()` works with old schemas, and why those models lack your custom methods.

---

<a name="q30"></a>
## Q30. (Hard) How do you write a database migration that changes field types without locking?
**Answer:** Most type changes rewrite the table under an exclusive lock (e.g. `int` → `bigint`). Zero-lock approach: add a new column with the new type → dual-write → backfill in batches → swap (rename columns in a short transaction) → drop the old one. Some changes are metadata-only on PostgreSQL (e.g. increasing `varchar` length, varchar → text).

---

<a name="q31"></a>
## Q31. (Medium) Explain the interaction between migrations and connection pooling.
**Answer:** Run migrations directly against the database, not through PgBouncer transaction pooling — migrations may rely on session settings and `CREATE INDEX CONCURRENTLY` can't run inside a transaction. Long migrations also hold one connection while app connections queue behind locks; pooled app connections may keep cached plans of old schemas.

---

<a name="q32"></a>
## Q32. (Medium) What is the risk of using schema_editor.execute inside RunPython?
**Answer:** It runs raw DDL that Django's migration state doesn't know about, so state and real schema can drift (future autodetected migrations go wrong). It may not be reversible and runs inside the migration's transaction. Prefer proper operations or `RunSQL` with `state_operations`.

---

<a name="q33"></a>
## Q33. (Medium) How do you enforce read-only tables in Django using custom migrations?
**Answer:** Enforce it in the database with `RunSQL`: revoke write privileges from the app user (`REVOKE INSERT, UPDATE, DELETE ON table FROM app_user`) or add a trigger that raises an error on writes. In Django, you can also override `save()`/`delete()` and use a read-only manager, but DB-level is the real guarantee.

---

<a name="q34"></a>
## Q34. (Medium) How does migration autodetector handle default value updates?
**Answer:** Changing `default=` creates an `AlterField` migration, but Django doesn't keep defaults in the database (it applies them in Python), so it usually runs no real SQL. With Django 5.0 `db_default`, changing it does `ALTER COLUMN ... SET DEFAULT` in the DB.

---

<a name="q35"></a>
## Q35. (Easy) What is the structure of django_migrations database table?
**Answer:** Four columns: `id`, `app` (app label), `name` (migration name, e.g. `0004_order_status`), `applied` (timestamp). One row per applied migration.
