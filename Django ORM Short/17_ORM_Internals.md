# Module 17: Django ORM Internals (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/17_ORM_Internals.md)

## Table of Contents
1. (Medium) [What is the role of the Query Compiler in django.db.models.sql?](#q1)
2. (Hard) [How does Django build the abstract syntax tree of a query internally?](#q2)
3. (Medium) [How does model state tracking work inside ModelInstances and ModelStates?](#q3)
4. (Medium) [Explain the internal execution sequence of QuerySet.all().](#q4)
5. (Hard) [How does Django represent SQL joins internally using the Join class?](#q5)
6. (Hard) [What is the purpose of django.db.models.sql.where.WhereNode?](#q6)
7. (Hard) [How does Django translate custom expressions to SQL using the as_sql method?](#q7)
8. (Hard) [How does connection backend class hierarchy work in Django?](#q8)
9. (Hard) [How does Django implement database-specific schema editors (BaseDatabaseSchemaEditor)?](#q9)
10. (Hard) [What is django.db.models.options.Options (_meta) class and how is it initialized?](#q10)
11. (Medium) [How does Django load model definitions and application registry during startup?](#q11)
12. (Medium) [What is the purpose of DeferredAttribute and how does it implement lazy loading?](#q12)
13. (Medium) [How does QuerySet manage its internal _result_cache?](#q13)
14. (Hard) [How does Django compile and escape query params?](#q14)
15. (Medium) [What is the relationship between django.db.connections and thread-locals?](#q15)
16. (Medium) [How does Django handle database connection cleanup after a request completes?](#q16)
17. (Hard) [How is the SQL compiler selected dynamically based on DATABASES configuration?](#q17)
18. (Hard) [What is the role of expression resolution (resolve_expression) in the query lifecycle?](#q18)
19. (Medium) [How does Django handle database backends loading dynamically?](#q19)
20. (Hard) [Explain how the ORM maps SQL results back into model instances (from_db).](#q20)
21. (Hard) [How do custom database backend extensions work?](#q21)
22. (Medium) [What is the internal structure of the model's primary key registry?](#q22)
23. (Medium) [How does Django ensure thread safety when evaluating queries?](#q23)
24. (Hard) [How does Django compile annotation expressions containing nested subqueries?](#q24)
25. (Hard) [What is the internal design of Django 5.0's GeneratedField database trigger/virtual column compilation?](#q25)
26. (Hard) [How does the compiler determine join promotion from INNER to LOUTER?](#q26)
27. (Hard) [What is the role of compiler.execute_sql method?](#q27)
28. (Medium) [How does Django track dirty fields internally?](#q28)
29. (Hard) [Explain the execution pipeline of QuerySet.delete().](#q29)
30. (Hard) [What is the relationship between ModelBase metaclass and migrations?](#q30)
31. (Hard) [How does Django resolve database backend specific parameter formats?](#q31)
32. (Medium) [What is the role of query.clone() method?](#q32)
33. (Medium) [How does the compiler escape wildcard characters in LIKE filters?](#q33)
34. (Medium) [Explain the internal representation of Q objects tree nodes.](#q34)
35. (Hard) [How do you write a custom connection backend wrapper?](#q35)

---

<a name="q1"></a>
## Q1. (Medium) What is the role of the Query Compiler in django.db.models.sql?
**Answer:** The QuerySet builds a backend-independent `Query` object; the **compiler** (`SQLCompiler` and its Insert/Update/Delete/Aggregate variants) turns it into actual SQL + params for a specific database, executes it, and converts result rows. Each backend can supply its own compiler classes for dialect differences.

---

<a name="q2"></a>
## Q2. (Hard) How does Django build the abstract syntax tree of a query internally?
**Answer:** `Query` holds the pieces: the base table and an alias map of joins, a `WhereNode` tree for conditions (built from `Q`/kwargs → lookup objects), lists of select columns and annotations (expression trees), ordering, grouping and limits. Every chain method clones `Query` and adds to these structures; nothing is SQL until compile time.

---

<a name="q3"></a>
## Q3. (Medium) How does model state tracking work inside ModelInstances and ModelStates?
**Answer:** Each instance has `_state` (a `ModelState`): `adding` (not yet saved — INSERT vs UPDATE, unique validation), `db` (alias it belongs to) and `fields_cache` (cached related objects). Field values live in `instance.__dict__`. Django doesn't track which fields changed.

---

<a name="q4"></a>
## Q4. (Medium) Explain the internal execution sequence of QuerySet.all().
**Answer:** `Model.objects.all()` → manager `get_queryset()` → `QuerySet.all()` returns a clone (`_chain()`), no SQL. On iteration: `_fetch_all()` → `ModelIterable` → `query.get_compiler(using)` → `execute_sql()` (SQL + params on a cursor) → rows converted and built via `Model.from_db()` → stored in `_result_cache` → prefetches run.

---

<a name="q5"></a>
## Q5. (Hard) How does Django represent SQL joins internally using the Join class?
**Answer:** Each joined table is a `Join` object in `query.alias_map`: table name, alias, parent alias, join type (`INNER JOIN` / `LEFT OUTER JOIN`), join columns and whether it's nullable. `setup_joins()` creates them when a lookup crosses relations and reuses existing ones where allowed. The compiler turns them into the `FROM ... JOIN ... ON ...` clause.

---

<a name="q6"></a>
## Q6. (Hard) What is the purpose of django.db.models.sql.where.WhereNode?
**Answer:** It's the tree for WHERE (and HAVING) conditions: a node has a connector (`AND`/`OR`), a `negated` flag and children — either lookups (`Exact`, `GreaterThan`…) or nested nodes. Its `as_sql()` compiles children recursively into SQL with parentheses and params. `Q` objects and filter kwargs are converted into this tree.

---

<a name="q7"></a>
## Q7. (Hard) How does Django translate custom expressions to SQL using the as_sql method?
**Answer:** Every expression implements `as_sql(compiler, connection)` returning `(sql, params)`. Composite expressions compile their children via `compiler.compile(child)` and combine them. Backend-specific variants are picked automatically by method name: `as_postgresql()`, `as_mysql()`, `as_sqlite()`.

```python
class Greatest2(Func):
    def as_sql(self, compiler, connection):
        lhs, lp = compiler.compile(self.source_expressions[0])
        rhs, rp = compiler.compile(self.source_expressions[1])
        return f"GREATEST({lhs}, {rhs})", lp + rp
```

---

<a name="q8"></a>
## Q8. (Hard) How does connection backend class hierarchy work in Django?
**Answer:** Each backend package (`django.db.backends.postgresql`) subclasses base classes from `backends.base`: `DatabaseWrapper` (connection, cursors, transactions), `DatabaseOperations` (SQL snippets/quoting), `DatabaseFeatures` (capability flags), `DatabaseSchemaEditor` (DDL), `DatabaseIntrospection`, `DatabaseCreation` (test DBs), `DatabaseClient` (`dbshell`). The wrapper ties them together.

---

<a name="q9"></a>
## Q9. (Hard) How does Django implement database-specific schema editors (BaseDatabaseSchemaEditor)?
**Answer:** `BaseDatabaseSchemaEditor` has methods like `create_model`, `add_field`, `alter_field`, `add_index` built from SQL templates (`sql_create_table`, `sql_create_index`…). Backends override templates or methods for their dialect — e.g. SQLite rebuilds tables (`_remake_table`) because its `ALTER TABLE` is limited. Migrations call these methods inside `with connection.schema_editor() as editor:`.

---

<a name="q10"></a>
## Q10. (Hard) What is django.db.models.options.Options (_meta) class and how is it initialized?
**Answer:** `Options` is the metadata object at `Model._meta`. `ModelBase` creates it from the inner `Meta` when the class is defined; fields and managers register via `contribute_to_class()`; relation information and full field lists are computed lazily after the app registry is ready and cached. Everything (ORM, admin, forms, migrations) reads model info from it.

---

<a name="q11"></a>
## Q11. (Medium) How does Django load model definitions and application registry during startup?
**Answer:** `django.setup()` → `apps.populate(INSTALLED_APPS)`: imports each `AppConfig`, then each app's `models` module (each model class registers itself in the registry), then calls every `AppConfig.ready()`. Until it finishes, using models raises `AppRegistryNotReady` — that's why you shouldn't import models at module level in some places.

---

<a name="q12"></a>
## Q12. (Medium) What is the purpose of DeferredAttribute and how does it implement lazy loading?
**Answer:** It's the descriptor behind each model field. When you read `obj.field`, Python first checks `obj.__dict__`; if the value isn't there (deferred by `only()`/`defer()`), `DeferredAttribute.__get__` loads it with `refresh_from_db(fields=[name])` — one query — and caches it in `__dict__`.

---

<a name="q13"></a>
## Q13. (Medium) How does QuerySet manage its internal _result_cache?
**Answer:** `_result_cache` is `None` until evaluation; `_fetch_all()` fills it with the full list of results (then runs prefetches). Iteration, `len()`, `bool()`, indexing of an evaluated queryset all read from it. Chaining creates a new queryset with an empty cache; `iterator()` never fills it.

---

<a name="q14"></a>
## Q14. (Hard) How does Django compile and escape query params?
**Answer:** Django never puts values into SQL text: each lookup produces SQL with placeholders (`%s`) and a list of params prepared by the field (`get_db_prep_value`). The DB driver sends/binds them separately, which prevents injection. Identifiers (table/column names) are quoted with `connection.ops.quote_name()`.

---

<a name="q15"></a>
## Q15. (Medium) What is the relationship between django.db.connections and thread-locals?
**Answer:** `connections` stores one `DatabaseWrapper` per alias per thread (using `asgiref.local.Local`, which also isolates async contexts). So each thread/request gets its own connection objects — they're never shared, which keeps transactions and cursors thread-safe.

---

<a name="q16"></a>
## Q16. (Medium) How does Django handle database connection cleanup after a request completes?
**Answer:** Django connects `close_old_connections()` to the `request_started` and `request_finished` signals. It closes connections that are past `CONN_MAX_AGE`, broken, or left in a bad transaction state; healthy persistent connections stay open for reuse. Outside requests (scripts, workers) you call it yourself.

---

<a name="q17"></a>
## Q17. (Hard) How is the SQL compiler selected dynamically based on DATABASES configuration?
**Answer:** `query.get_compiler(using)` takes the alias, gets that connection, and calls `connection.ops.compiler(query.compiler)` — which imports the class named by the query type (e.g. `"SQLCompiler"`, `"SQLInsertCompiler"`) from the backend's `compiler_module`. Backends without overrides use Django's default compiler module.

---

<a name="q18"></a>
## Q18. (Hard) What is the role of expression resolution (resolve_expression) in the query lifecycle?
**Answer:** When an expression is added to a query (`annotate`, `filter`, `update`), `resolve_expression(query)` is called on it: `F("x")` becomes a column reference, joins are set up, `OuterRef` is linked to the outer query, aggregates are validated, and output types are determined. Only resolved expressions can be compiled to SQL.

---

<a name="q19"></a>
## Q19. (Medium) How does Django handle database backends loading dynamically?
**Answer:** `ENGINE` in `DATABASES` is a dotted module path (e.g. `"django.db.backends.postgresql"` or `"mssql"`). On first use, `ConnectionHandler` imports `<ENGINE>.base` and instantiates its `DatabaseWrapper` with the settings dict. That's how third-party backends plug in.

---

<a name="q20"></a>
## Q20. (Hard) Explain how the ORM maps SQL results back into model instances (from_db).
**Answer:** The compiler fetches rows and applies field converters. `ModelIterable` then knows which columns belong to the model, `select_related` models and annotations; it calls `Model.from_db(db, field_names, values)` to create each instance without running `__init__` validation, sets `_state.adding = False` and `_state.db`, populates related objects, and sets annotations as attributes.

---

<a name="q21"></a>
## Q21. (Hard) How do custom database backend extensions work?
**Answer:** Create a package with a `base.py` whose `DatabaseWrapper` subclasses an existing backend, override what you need (e.g. connection params, `DatabaseFeatures`, operations, or `init_connection_state()` to run `SET` commands), and set `ENGINE` to that package. Common use: tweaks for a specific DB version or adding instrumentation.

---

<a name="q22"></a>
## Q22. (Medium) What is the internal structure of the model's primary key registry?
**Answer:** There's no separate registry: `Model._meta.pk` points to the primary key field (auto-created `id` using `DEFAULT_AUTO_FIELD`, or the field with `primary_key=True`, or the parent link in multi-table inheritance). `obj.pk` is a property that reads/writes that field's attribute, so code can use `pk` regardless of its name.

---

<a name="q23"></a>
## Q23. (Medium) How does Django ensure thread safety when evaluating queries?
**Answer:** Each thread has its own connection, and each `QuerySet` is a separate object — chain methods return clones instead of mutating. Model metadata is built once at startup and then read-only. Problems only arise if you share one evaluating QuerySet or model instance between threads yourself.

---

<a name="q24"></a>
## Q24. (Hard) How does Django compile annotation expressions containing nested subqueries?
**Answer:** The subquery's own `Query` is resolved against the outer query (linking `OuterRef`s to outer aliases, changing inner aliases to avoid clashes, e.g. `U0`), then compiled recursively by `as_sql()` into a parenthesised SQL fragment with its params, which is inserted into the outer SELECT/WHERE.

---

<a name="q25"></a>
## Q25. (Hard) What is the internal design of Django 5.0's GeneratedField database trigger/virtual column compilation?
**Answer:** No triggers are used. The schema editor compiles the field's expression (with values inlined) into the column definition: `GENERATED ALWAYS AS (<expr>) STORED` or `VIRTUAL` depending on `db_persist` and backend support. The field is marked `generated=True`, so Django leaves it out of INSERT/UPDATE statements.

---

<a name="q26"></a>
## Q26. (Hard) How does the compiler determine join promotion from INNER to LOUTER?
**Answer:** Joins start as INNER when the FK is non-nullable. Django promotes a join to LEFT OUTER when it could drop rows that should appear — nullable FKs, `OR` conditions where only one side uses the relation, `isnull=True` lookups, `select_related` on nullable FKs. It demotes back to INNER when a filter requires a match anyway. This logic (`JoinPromoter`) keeps results correct.

---

<a name="q27"></a>
## Q27. (Hard) What is the role of compiler.execute_sql method?
**Answer:** It runs the compiled SQL: calls `as_sql()`, opens a cursor on the connection, executes with params, and returns results according to `result_type` — a single row, multiple rows (in chunks, for iteration), a cursor, or nothing. Iteration uses it with chunked fetching (and server-side cursors for `iterator()`).

---

<a name="q28"></a>
## Q28. (Medium) How does Django track dirty fields internally?
**Answer:** It doesn't — `save()` writes every field unless you pass `update_fields`. The only related tracking is deferred fields (`get_deferred_fields()`), and saving a deferred instance updates only loaded fields. For real dirty tracking, store original values in `from_db()` / `__init__` and compare, or use `django-dirtyfields`.

---

<a name="q29"></a>
## Q29. (Hard) Explain the execution pipeline of QuerySet.delete().
**Answer:**
1. Create a `Collector` for the database.
2. If fast-delete is possible (no signals, nothing referencing the model), issue one `DELETE ... WHERE`.
3. Otherwise load the objects, then for each relation apply `on_delete` (collect cascades, prepare SET_NULL updates, raise for PROTECT/RESTRICT).
4. In one transaction: sort models by dependency, send `pre_delete`, run updates and deletes (children first), send `post_delete`.
5. Return `(total, {model: count})`.

---

<a name="q30"></a>
## Q30. (Hard) What is the relationship between ModelBase metaclass and migrations?
**Answer:** `ModelBase` builds the model class and its `_meta` at import time; the migration autodetector reads this metadata (fields, options) to build the current "to" state, and compares it with the state from migration files. During migrations, Django creates **historical** model classes from migration state (via the same metaclass), independent of your current code.

---

<a name="q31"></a>
## Q31. (Hard) How does Django resolve database backend specific parameter formats?
**Answer:** Django always writes `%s` placeholders. Drivers using another style get them translated by the backend — e.g. SQLite's cursor wrapper converts `%s` to `?`, Oracle uses named `:arg` params. A literal `%` in raw SQL with params must be written as `%%`.

---

<a name="q32"></a>
## Q32. (Medium) What is the role of query.clone() method?
**Answer:** It copies the `Query` object (alias map, where tree, annotations, ordering…) so a new QuerySet can be modified without changing the original. Every `filter()`, `order_by()` etc. works on a clone — that's what makes querysets immutable-looking and reusable.

---

<a name="q33"></a>
## Q33. (Medium) How does the compiler escape wildcard characters in LIKE filters?
**Answer:** For `contains`, `startswith`, `endswith` (and `i` versions), Django escapes `%`, `_` and `\` inside **your value** (`connection.ops.prep_for_like_query`) and adds its own `%` wildcards, so searching for `"50%"` matches the literal text. The value is still passed as a parameter.

---

<a name="q34"></a>
## Q34. (Medium) Explain the internal representation of Q objects tree nodes.
**Answer:** `Q` is a tree node with `connector` (`AND`/`OR`/`XOR`), `negated`, and `children` — each child is a `(lookup, value)` tuple or another `Q`. `&`, `|`, `^`, `~` build new nodes. When added to a query, the tree is converted into a `WhereNode` of lookup objects.

---

<a name="q35"></a>
## Q35. (Hard) How do you write a custom connection backend wrapper?
**Answer:** Subclass an existing backend's `DatabaseWrapper` in your own package's `base.py` and point `ENGINE` at it.

```python
# myproject/db/postgres_tagged/base.py
from django.db.backends.postgresql import base

class DatabaseWrapper(base.DatabaseWrapper):
    def init_connection_state(self):
        super().init_connection_state()
        with self.cursor() as cur:
            cur.execute("SET application_name = 'web'")
```
For per-query hooks (logging, tagging), `connection.execute_wrapper()` is simpler than a custom backend.
