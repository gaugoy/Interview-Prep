# Module 06: Query Optimization

Interview-ready answers on Django 5.x query optimization, Senior → Lead level.

**How to use each question:** `# Answer` opens with a **spoken answer** (~30–45 sec, no code) — say that first. `# Internal ORM Mechanics`, `# SQL Generated` and `# Code Example` are the mechanism you explain when the interviewer digs in. `# Production Scenario` is a STAR story grounded in the PNI Hub stack — **adapt it to what you actually did** and replace every `[fill-in]` with your real number (never quote a number you can't defend). `# Performance Impact` holds the trade-offs / when-not-to, and `# Common Mistakes` lists the wrong answers interviewers hear most.

---

# Question

What is the difference between select_related and prefetch_related?

# Why Interviewer Asks This

It is the most common Django performance question. The interviewer wants to hear *how* each one talks to the database (one JOIN vs. a second `IN` query), which relationship types each supports, and that you choose by data shape rather than by a memorised rule.

# Answer

**Spoken answer:** "Both fix the N+1 problem — loading related objects up front instead of one query per row — but differently. `select_related` adds a SQL JOIN, so the parent and its related row come back in a single query; it only works for single-valued relations, meaning forward ForeignKey and OneToOne. `prefetch_related` runs a second query per relation — `WHERE fk IN (all the parent ids)` — and stitches the results together in Python, so it handles multi-valued relations: reverse ForeignKey, ManyToMany, generic relations. My rule of thumb: JOIN when each row has exactly one related object; prefetch when it can have many, or when a JOIN would repeat a lot of wide data."

**Why it matters:** N+1 is invisible in development with ten rows and becomes the dominant latency in production. Every lazy access is a separate network round-trip, so the cost scales with page size, not with how much data you actually need.

**Distinctions worth saying out loud:**
- `select_related` → 1 query; INNER JOIN for a non-null FK, LEFT OUTER JOIN for `null=True`.
- `prefetch_related` → 1 + one query per lookup, merged in Python; works for *any* relation (including forward FK) and accepts a custom queryset via `Prefetch`.
- `select_related` on a many-valued relation raises `FieldError` — Django refuses to multiply parent rows.

# Internal ORM Mechanics

- `select_related('customer')` sets `query.select_related`; the compiler adds the JOIN and the related table's columns to the SELECT list. `ModelIterable` builds both objects from each row and stores the related one in `order._state.fields_cache['customer']`, so `order.customer` never hits the database.
- `prefetch_related('items')` only records the lookup in `_prefetch_related_lookups`. After the main query is evaluated, `prefetch_related_objects()` collects the parent keys, asks the relation descriptor for its prefetch queryset (`get_prefetch_querysets()` in 5.0+), runs `OrderItem.objects.filter(order__in=[...])`, groups the children by `order_id` in Python and stores each group in `order._prefetched_objects_cache['items']`. `order.items.all()` reads from that cache.
- A prefetched forward FK *shares* one instance among all parents pointing to it; `select_related` builds a fresh related instance per row, because Django has no identity map.

# SQL Generated

```python
orders = Order.objects.select_related('customer').prefetch_related('items')
```

```sql
-- Query 1: the JOIN (customer FK is NOT NULL → INNER JOIN)
SELECT "shop_order"."id", "shop_order"."customer_id", "shop_order"."total", "shop_order"."placed_at",
       "shop_customer"."id", "shop_customer"."name", "shop_customer"."email"
FROM "shop_order"
INNER JOIN "shop_customer" ON ("shop_order"."customer_id" = "shop_customer"."id");

-- Query 2: the prefetch — ONE query for every order's items
SELECT "shop_orderitem"."id", "shop_orderitem"."order_id", "shop_orderitem"."product_id", "shop_orderitem"."quantity"
FROM "shop_orderitem"
WHERE "shop_orderitem"."order_id" IN (101, 102, 103 /* …every order id from query 1 */);
```

# Code Example

```python
# shop/models.py
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    placed_at = models.DateTimeField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

# Before: 1 + N + N queries
for order in Order.objects.all()[:50]:
    order.customer.name        # +1 query per order (forward FK)
    len(order.items.all())     # +1 query per order (reverse FK)

# After: exactly 2 queries, whatever the page size
orders = (Order.objects
          .select_related('customer')   # single-valued → JOIN
          .prefetch_related('items')    # multi-valued  → second query
          [:50])
```

# Production Scenario

**From experience (STAR):** **S** — On PNI Hub, the DRF endpoint behind the integrations dashboard returned each integration with its owner, tags and recent sync runs. **T** — p95 latency had crept to [fill-in] ms as the integration count grew; debug-toolbar showed [fill-in] queries per page. **A** — I added `select_related('owner')` for the FK, `prefetch_related('tags')` for the M2M and a filtered `Prefetch` for recent runs, then locked the query count with an `assertNumQueries` test so it couldn't regress. **R** — queries per request went from [fill-in] (growing with page size) to a constant [fill-in]; p95 dropped from [fill-in] to [fill-in] ms.

# Performance Impact

- N+1 costs one round-trip per row; both techniques make that constant (1, or 1 + K for K lookups).
- `select_related` cost: wider rows. When many parents share few related rows (10,000 orders, 50 customers), the customer columns repeat on every row and Django builds 10,000 customer objects.
- `prefetch_related` cost: an extra round-trip plus a large `IN` list. On SQL Server the ~2,100-parameter limit means very large parent sets must be chunked.

**Trade-offs / when NOT to use it:**
- Don't `select_related` long chains of wide tables "just in case" — every column is fetched whether or not it is used.
- Don't prefetch children when you only need a number — `annotate(Count(...))` is one query and ships no child rows.
- For a single `get()`, one lazy access is one extra query; optimising it is rarely worth the noise.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`select_related` is for ForeignKey, `prefetch_related` is for ManyToMany." Incomplete — prefetch works on FKs too, and `select_related` follows OneToOne in both directions.
- "`prefetch_related` does a JOIN." It runs a separate query; for M2M that query joins the *through* table, not the parent.
- "Filtering a prefetched relation uses the cache." `.filter()` on `obj.items` is a new query per object.
- "Add both everywhere." Unused prefetches still execute — each one is a wasted query.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Either works; un-fixed N+1 is already ~1K round-trips | Negligible | ACCESS SHARE only (MVCC read, no row locks) |
| **Medium** | 1M | Paginate; per page it's 1 JOIN query or 1 + K prefetch queries | JOIN repeats related columns per row | ACCESS SHARE only |
| **Large** | 100M | Index on the FK column used by the JOIN / `IN` list is mandatory | Prefetch `IN` list grows with page size — keep pages bounded | ACCESS SHARE; avoid long-open read transactions |
| **Massive** | 1B+ | Related data may sit in another DB/shard — a JOIN is impossible, only prefetch-style stitching works | Stream with `iterator(chunk_size=...)` | Route reads to replicas |

**Scaling note:** past a single database, `select_related` stops being an option (it is one SQL statement), so the prefetch *pattern* — collect keys, query, merge in Python — is what survives.

# Follow-up Questions

1. When would you prefetch a *forward* ForeignKey instead of using `select_related`?
2. What happens if you call `.filter()` on a relation you already prefetched?
3. How would you prove in a test that an endpoint has no N+1?

# Related Topics

* Module 06 Q2 — when the prefetch query actually runs
* Module 06 Q3 — customising prefetches with `Prefetch`
* Module 06 Q37 — N+1 inside DRF serializers
* Module 07 Q18 — forward vs. reverse prefetching

---

# Question

When does prefetch_related write a new query, and how is it executed?

# Why Interviewer Asks This

Checks that you know prefetching is lazy and tied to evaluation, how many queries a lookup path really costs, and — most importantly — which operations silently bypass the prefetch cache and bring the N+1 back.

# Answer

**Spoken answer:** "`prefetch_related` doesn't run anything when you call it — it just records the lookup. When the main queryset is evaluated, Django runs the parent query, collects all the parent keys, then runs one extra query per relation in the lookup path using `WHERE fk IN (...)`. So `prefetch_related('items__product')` is three queries total, no matter how many orders there are. Results are grouped in Python and cached on each parent. The catch: only plain access uses that cache — `.all()`, iteration, `len()`, `count()`, `exists()`. As soon as you call `.filter()` or `.order_by()` on the relation, Django builds a fresh query — per object."

**The reasoning:** batching only works because Django waits until it knows the full set of parents, so the trigger is evaluation of the outer queryset, not the `prefetch_related()` call.

- **When:** on evaluation — iteration, `list()`, `len()`, `bool()`, pickling. Never at definition time.
- **How many:** 1 for parents + 1 per level of each lookup path. Shared prefixes are fetched once (`'items'` + `'items__product'` fetches items once).
- **No parents → no prefetch query** at all.
- **Django 5.x:** `iterator()` on a prefetching queryset *requires* `chunk_size`; the prefetch then runs once per chunk.

# Internal ORM Mechanics

`QuerySet._fetch_all()` fills `_result_cache`, then calls `_prefetch_related_objects()` → `prefetch_related_objects(instances, *lookups)`. For each level it calls `get_prefetcher()` to find the relation descriptor, then `prefetch_one_level()`, which asks the descriptor for `get_prefetch_querysets(instances)`. That returns the related queryset already filtered by `fk__in`, plus two key-extractor functions (one for children, one for parents). Django evaluates it, builds `{key: [children]}`, and stores each list in `parent._prefetched_objects_cache[cache_name]` as a QuerySet with a pre-filled `_result_cache`. The related manager's `get_queryset()` checks that cache first. Any chaining method (`filter`, `exclude`, `order_by`, `values`) clones the queryset, which drops the result cache and hits the database.

# SQL Generated

```python
orders = list(Order.objects.prefetch_related('items__product'))
```

```sql
SELECT "shop_order"."id", "shop_order"."customer_id", "shop_order"."total" FROM "shop_order";

SELECT "shop_orderitem"."id", "shop_orderitem"."order_id", "shop_orderitem"."product_id", "shop_orderitem"."quantity"
FROM "shop_orderitem" WHERE "shop_orderitem"."order_id" IN (101, 102, 103);

-- product ids are de-duplicated before this query
SELECT "shop_product"."id", "shop_product"."sku", "shop_product"."name"
FROM "shop_product" WHERE "shop_product"."id" IN (7, 9, 15);
```

# Code Example

```python
qs = Order.objects.prefetch_related('items__product')   # nothing has run yet
orders = list(qs)                                        # 3 queries happen here

order = orders[0]
order.items.all()                    # cache hit — 0 queries
order.items.count()                  # cache hit — len() of the cached list
order.items.exists()                 # cache hit
order.items.filter(quantity__gt=1)   # NEW query — a filter can't be answered from the cache
order.items.order_by('-quantity')    # NEW query

# Django 5.x: iterator() + prefetch needs chunk_size (ValueError otherwise)
for order in qs.iterator(chunk_size=2000):   # one prefetch round per 2,000 orders
    ...
```

# Production Scenario

**From experience (STAR):** **S** — One of our ten django-crontab jobs on PNI Hub built a nightly integration-health report: every integration, its endpoints and their last status. **T** — It either loaded everything into memory with `.all()` or, after someone switched to `.iterator()`, silently became N+1 at [fill-in] queries per run. **A** — I used `prefetch_related(...)` with `iterator(chunk_size=2000)`, so each chunk gets exactly one prefetch query per relation, and moved the one place that called `.filter()` on the relation to a `Prefetch(..., to_attr=...)`. **R** — runtime went from [fill-in] to [fill-in] minutes with flat memory; query count became [fill-in] per chunk instead of per row.

# Performance Impact

- Each level costs one round-trip plus Python grouping that is O(children) — usually far cheaper than N round-trips.
- Very large parent sets produce very large `IN` lists: more planning time and parameter transfer, and a hard failure on SQL Server's ~2,100-parameter limit unless you chunk.
- The real risk is the *hidden* N+1 when code chains on a prefetched relation.

**Trade-offs / when NOT to use it:**
- If different call sites need differently filtered children, prefetch each variant with `Prefetch(..., to_attr=...)` instead of chaining.
- If you only need counts or sums, `annotate()` instead — no child rows travel at all.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "It runs when you call `prefetch_related()`." No — it runs when the outer queryset is evaluated.
- "It's one extra query per object." It's one per relation *level*.
- "`.first()` on a prefetched relation is free." Only if the relation is ordered; without default ordering `.first()` adds `order_by('pk')` → new query.
- "`iterator()` just skips the prefetch." In Django 5.x it raises `ValueError` unless you pass `chunk_size`.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | 1 + K queries, all fast | All children held on parents | ACCESS SHARE only |
| **Medium** | 1M | Prefetch per page; never prefetch an unpaginated table | Bounded by page size | ACCESS SHARE only |
| **Large** | 100M | `iterator(chunk_size=...)` so each chunk has its own bounded `IN` list | Flat — one chunk of parents + children at a time | ACCESS SHARE; server-side cursor holds a snapshot open |
| **Massive** | 1B+ | Batch by PK range in a job; prefetch per batch | Flat | Prefer replicas; keep each read short to avoid holding back VACUUM |

# Follow-up Questions

1. How many queries does `prefetch_related('a', 'a__b', 'a__b__c')` run?
2. How do you prefetch onto objects you already have in a list (e.g. from a cache)?
3. Why does `prefetch_related` + `iterator()` need `chunk_size` in Django 5.x?

# Related Topics

* Module 06 Q28 — how the prefetch cache is stored and invalidated
* Module 06 Q17 — deeply nested prefetches
* Module 01 Q9 — when `iterator()` makes multiple queries

---

# Question

How does the Prefetch object allow customization of prefetching?

# Why Interviewer Asks This

Separates "I add `prefetch_related`" from "I control what gets prefetched": filtering, ordering, trimming columns, nesting a JOIN inside the prefetch, and knowing the `to_attr` and lookup-ordering rules that cause subtle bugs.

# Answer

**Spoken answer:** "A plain `prefetch_related('tickets')` fetches every related row through the default manager. The `Prefetch` object lets me supply my own queryset for that second query, so I can filter to open tickets, order them, trim columns with `only()`, and even `select_related` the ticket's assignee inside the prefetch so that doesn't become its own N+1. With `to_attr`, the results land on a plain list attribute like `project.open_tickets` — which makes it obvious to the next developer that this is a filtered subset, not the whole relation."

**The reasoning:** prefetch_related without a queryset assumes you want *all* children; real screens almost never do. `Prefetch(lookup, queryset=None, to_attr=None)` lets you push that filtering into SQL instead of filtering in Python.

- The queryset must be for the **related model**, and can't be a `values()` queryset.
- **Without `to_attr`**, the filtered results *replace* the relation cache — `project.tickets.all()` then silently returns only open tickets. That is the main foot-gun.
- `to_attr` gives a list (no QuerySet wrapper, slightly faster) and can be the root of further lookups: `'open_tickets__comments'`.
- **Order matters:** a `Prefetch` must come before any string lookup that traverses it, and the same lookup path with a different queryset raises `ValueError`.

# Internal ORM Mechanics

`prefetch_related_objects()` normalises every string lookup into a `Prefetch`. At the level matching your lookup's final hop, `Prefetch.get_current_querysets(level)` (5.0+) returns your queryset; the descriptor's `get_prefetch_querysets(instances, querysets=[your_qs])` adds the `project_id__in` filter *on top of it*. So your `filter`, `order_by`, `select_related` and `only` all end up in a single SQL statement. With `to_attr`, `prefetch_one_level()` does `setattr(obj, to_attr, list_of_children)` instead of writing to `_prefetched_objects_cache`.

# SQL Generated

```sql
SELECT "pm_project"."id", "pm_project"."name" FROM "pm_project";

SELECT "pm_ticket"."id", "pm_ticket"."project_id", "pm_ticket"."title", "pm_ticket"."status",
       "pm_ticket"."assignee_id", "pm_ticket"."created_at",
       "auth_user"."id", "auth_user"."username"
FROM "pm_ticket"
LEFT OUTER JOIN "auth_user" ON ("pm_ticket"."assignee_id" = "auth_user"."id")   -- assignee is nullable
WHERE ("pm_ticket"."status" = 'open' AND "pm_ticket"."project_id" IN (1, 2, 3))
ORDER BY "pm_ticket"."created_at" DESC;
```

# Code Example

```python
from django.db.models import Prefetch

open_tickets = (Ticket.objects
                .filter(status='open')
                .select_related('assignee')                     # JOIN inside the prefetch query
                .only('id', 'project_id', 'title', 'status', 'created_at',
                      'assignee__id', 'assignee__username')      # keep project_id: it's the join key
                .order_by('-created_at'))

projects = Project.objects.prefetch_related(
    Prefetch('tickets', queryset=open_tickets, to_attr='open_tickets'),
)

for p in projects:                       # 2 queries in total
    for t in p.open_tickets:             # plain list
        print(p.name, t.title, t.assignee.username if t.assignee else '-')
```

# Production Scenario

**From experience (STAR):** **S** — The PNI Hub integration-detail API showed only *failed* sync runs from the last 24 hours, each with its endpoint. **T** — The first version prefetched every run (months of history) and filtered in Python, which cost [fill-in] ms and [fill-in] MB per request. **A** — I replaced it with `Prefetch('sync_runs', queryset=SyncRun.objects.filter(status='failed', started_at__gte=cutoff).select_related('endpoint'), to_attr='recent_failures')`, so filtering happened in SQL using the `(integration_id, started_at)` index. **R** — rows transferred dropped from [fill-in] to [fill-in] and latency from [fill-in] to [fill-in] ms.

# Performance Impact

- Filtering in the prefetch query means only the rows you display cross the network.
- `select_related` inside the prefetch removes an entire extra level (and its `IN` list).
- `only()` in the prefetch narrows wide child rows — but it must keep the FK used to match children to parents.

**Trade-offs / when NOT to use it:**
- If you need the *full* relation elsewhere on the same objects, always use `to_attr`; overriding the default cache confuses every other caller.
- If you need only "latest one" or a count, a `Subquery`/`annotate` is often simpler than a prefetch.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Prefetch then `.filter()` in the template." That's a query per object — the filter belongs in `Prefetch(queryset=...)`.
- "`to_attr` is just cosmetic." It changes the type (list vs. manager) and protects the default relation cache.
- Using `only()` in the prefetch queryset *without the FK* (`project_id`) — Django then lazy-loads the FK on every child to match it to a parent: a brand-new N+1.
- Passing a `values()` queryset to `Prefetch` — not allowed; prefetch needs model instances.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Same as plain prefetch | Slightly lower | ACCESS SHARE only |
| **Medium** | 1M | Child filter should hit an index like `(project_id, status)` | Only matching children loaded | ACCESS SHARE only |
| **Large** | 100M | Composite index `(fk, filter_col, order_col)` lets the prefetch avoid a sort | Bounded by filter + page size | ACCESS SHARE only |
| **Massive** | 1B+ | Use sliced prefetches (top-N per parent, Django 4.2+) or pre-aggregated tables | Bounded | Replicas; partition child table by time |

# Follow-up Questions

1. What happens if you prefetch the same relation twice with different querysets?
2. How do you prefetch only the latest 3 children per parent?
3. Why can `only()` inside a `Prefetch` reintroduce N+1?

# Related Topics

* Module 06 Q30 — prefetching only active / latest-N items
* Module 06 Q4 — `only()` and `defer()`
* Module 07 Q23 — prefetching through-model attributes

---

# Question

What is the difference between only() and defer(), and what are the risks of using them?

# Why Interviewer Asks This

Tests whether you know column-level loading control and — more importantly — its failure mode: deferred fields that get touched later turn one query into N+1, and the coupling between querysets and the code that consumes them becomes fragile.

# Answer

**Spoken answer:** "Both control which *columns* Django loads while still giving you model instances. `only()` is an allow-list — load these fields plus the primary key; `defer()` is a deny-list — load everything except these. I use them for wide tables, typically to skip a big text or JSON blob on list screens. The risk is that deferred fields are still accessible: touch one and Django silently runs a query for that row. In a loop, that's N+1 again. So I only defer columns I'm sure the downstream code — templates, serializers, `__str__`, signals — never reads; if I truly need just data, I reach for `values()` instead."

**The reasoning:** column trimming saves I/O, network and Python decoding, but it creates an implicit contract between the queryset and every consumer of the objects.

- `only('a', 'b')` → SELECT pk, a, b. `defer('blob')` → SELECT all columns except blob.
- Chaining: successive `only()` calls *replace* the list; successive `defer()` calls *accumulate*; `defer(None)` clears.
- `save()` on a deferred instance updates only the loaded fields — Django passes them as `update_fields` automatically.
- Combined with `select_related`, the FK must not be deferred: `only('title', 'author__name')` works, `only('title')` + `select_related('author')` raises `FieldError`.

# Internal ORM Mechanics

`only()`/`defer()` store the field set in `query.deferred_loading` as `(field_names, is_defer)`. The compiler's `get_select()` uses it to build the column list. When rows come back, `Model.from_db()` receives only the loaded values; the missing attnames are simply absent from `instance.__dict__`. Access goes through the class-level `DeferredAttribute` descriptor, which notices the missing key and calls `instance.refresh_from_db(fields=[name])`. `instance.get_deferred_fields()` tells you which fields were not loaded.

# SQL Generated

```python
Article.objects.only('title', 'published_at')
Article.objects.defer('body', 'seo_metadata')
article.body          # on an instance loaded with only()
```

```sql
SELECT "cms_article"."id", "cms_article"."title", "cms_article"."published_at" FROM "cms_article";

SELECT "cms_article"."id", "cms_article"."title", "cms_article"."slug", "cms_article"."published_at",
       "cms_article"."author_id" FROM "cms_article";        -- body and seo_metadata skipped

-- one extra query per instance, per deferred field touched
SELECT "cms_article"."id", "cms_article"."body" FROM "cms_article" WHERE "cms_article"."id" = 42 LIMIT 21;
```

# Code Example

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()                # can be 100s of KB
    seo_metadata = models.JSONField(default=dict)
    published_at = models.DateTimeField(null=True)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)

# List page: never needs body/seo_metadata
cards = Article.objects.defer('body', 'seo_metadata').select_related('author')

# Same idea as an allow-list, including a field across the JOIN
cards = Article.objects.select_related('author').only('title', 'slug', 'published_at', 'author__username')

# Safety net in a test / shell
a = cards.first()
assert 'body' in a.get_deferred_fields()
```

# Production Scenario

**From experience (STAR):** **S** — Some PNI Hub models mirror wide legacy tables from the MSSQL ODS, with `NVARCHAR(MAX)` description and payload columns. **T** — The list endpoint only displayed [fill-in] short columns but was transferring [fill-in] KB per row. **A** — I added `defer()` on the blob columns in the list view's `get_queryset`, kept the detail view on full loads, and added a test asserting the list serializer's fields are never in `get_deferred_fields()`. **R** — payload per page fell from [fill-in] to [fill-in] and DB time from [fill-in] to [fill-in] ms.

# Performance Impact

- Saves disk reads (especially TOAST/LOB pages), network bytes and Python decoding for skipped columns.
- Does **not** change which rows are read or how the JOINs are planned — the win is purely per-column.
- Every later access to a deferred field = one query per instance.

**Trade-offs / when NOT to use it:**
- Narrow tables: the saving is negligible and you've added fragility.
- Read-only data shaping: `values()`/`values_list()` is clearer and can't lazy-load anything.
- Querysets passed to code you don't control (admin, third-party serializers) — you can't guarantee they won't touch deferred fields.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Deferred fields are `None`." They're *lazy*, not empty — access triggers a query.
- "`only()` makes the query use an index-only scan." Rarely; it trims columns, it doesn't change the access path in most real queries.
- "`only()` and `defer()` stack the same way." `only()` replaces, `defer()` accumulates.
- Forgetting `__str__`, `Meta.ordering`, signals or `full_clean()` read fields you deferred.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Little measurable difference | Small saving | ACCESS SHARE only |
| **Medium** | 1M | Noticeable on list pages with large text columns | Proportional to skipped bytes | ACCESS SHARE only |
| **Large** | 100M | Large win when skipped columns are TOASTed (no detoast reads) | Big saving on exports/jobs | ACCESS SHARE only |
| **Massive** | 1B+ | Consider moving blobs to a 1:1 side table or object storage | — | ACCESS SHARE only |

# Follow-up Questions

1. What happens when you call `save()` on an instance loaded with `only()`?
2. How would you detect deferred-field N+1 in a test suite?
3. When would you choose `values()` over `only()`?

# Related Topics

* Module 06 Q5 — how a deferred field triggers its query
* Module 06 Q16 — the cost of large text fields
* Module 06 Q32 — `only()` with deep `select_related`

---

# Question

How does referencing a deferred field trigger database queries?

# Why Interviewer Asks This

A mechanism question: can you explain the descriptor that implements lazy loading, predict exactly how many queries a loop will run, and show how you would detect it.

# Answer

**Spoken answer:** "When a field is deferred, its value just isn't in the instance's `__dict__`. Model fields are backed by a descriptor on the class — `DeferredAttribute` — so when you read `article.body`, the descriptor sees the value is missing and calls `refresh_from_db(fields=['body'])`, which is a `SELECT` for that one column, by primary key, for that one instance. It caches the result, so the second read is free. But it's per instance and per field: read two deferred fields across 100 rows and that's 200 extra queries. That's why I treat deferred loading as a contract with the consumer, and I verify it with query-count tests."

**The reasoning:** Django chose "lazy but correct" over "fail loudly", so a mistake costs performance instead of raising an error — which is exactly why it slips into production.

- 1 query per (instance × deferred field touched). Not batched.
- The first access caches the value in `__dict__`; later reads don't query.
- Also triggered indirectly: `__str__`, `get_absolute_url()`, serializers, signals, `model_to_dict`, admin list columns.

# Internal ORM Mechanics

Each concrete field contributes a `DeferredAttribute` to the model class (`Field.descriptor_class`). Normal attribute lookup finds the value in `instance.__dict__` first, so loaded fields never reach the descriptor. For a missing attname, `DeferredAttribute.__get__` first checks whether the value can be taken from a parent in a multi-table-inheritance chain (`_check_parent_chain`); if not, it calls `instance.refresh_from_db(fields=[field_name])`. That builds `Model._base_manager.db_manager(using).filter(pk=...).only(field_name).get()` against the instance's own database (`instance._state.db`) — important with multiple databases — and copies the value back. Django 5.1 added `refresh_from_db(from_queryset=...)` if you need to control that queryset (e.g. lock it).

# SQL Generated

```python
for a in Article.objects.only('id', 'title')[:3]:
    print(a.title, len(a.body))
```

```sql
SELECT "cms_article"."id", "cms_article"."title" FROM "cms_article" LIMIT 3;
SELECT "cms_article"."id", "cms_article"."body" FROM "cms_article" WHERE "cms_article"."id" = 1 LIMIT 21;
SELECT "cms_article"."id", "cms_article"."body" FROM "cms_article" WHERE "cms_article"."id" = 2 LIMIT 21;
SELECT "cms_article"."id", "cms_article"."body" FROM "cms_article" WHERE "cms_article"."id" = 3 LIMIT 21;
```

# Code Example

```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

qs = Article.objects.only('id', 'title')[:3]

with CaptureQueriesContext(connection) as ctx:
    for a in qs:
        a.body          # deferred → query
        a.body          # cached now → no query
print(len(ctx.captured_queries))   # 1 + 3 = 4

a = Article.objects.only('id', 'title').first()
a.get_deferred_fields()            # {'slug', 'body', 'seo_metadata', 'published_at', 'author_id'}
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub DRF list view used `only()` for speed. **T** — A teammate later added a `status_label` field to the serializer that read a column not in the `only()` list; latency jumped by [fill-in] ms with no obvious cause. **A** — `CaptureQueriesContext` in the endpoint test showed one `SELECT ... WHERE id = %s` per row; I moved the column list into the serializer (`Meta.fields` drives `only()`), so they can't drift apart, and kept the query-count test as a guard. **R** — queries per page back to [fill-in]; the regression test has caught [fill-in] similar changes since.

# Performance Impact

- Each lazy load is a full round-trip with a PK lookup — fast individually, disastrous in a loop.
- It also opens a query outside whatever batching you designed, so connection-pool usage and DB CPU scale with rows.

**Trade-offs / when NOT to use it:**
- If a field might be needed by *any* consumer, don't defer it — the saving is smaller than one extra round-trip per row.
- When you need the field sometimes, two querysets (list vs. detail) are clearer than one deferred queryset.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Django loads all deferred fields together on first access." It loads only the field you touched.
- "It raises an error if the field wasn't loaded." It silently queries.
- "It's cached on the queryset." It's cached on the *instance* — each instance queries separately.
- Assuming the lazy load uses the default database; it uses the instance's own `_state.db`.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | N extra PK lookups — tolerable but wasteful | Minimal | ACCESS SHARE only |
| **Medium** | 1M | Any loop over a page multiplies round-trips | Minimal | ACCESS SHARE only |
| **Large** | 100M | Batch jobs touching a deferred field = one query per row = hours | Minimal | ACCESS SHARE; increased connection hold time |
| **Massive** | 1B+ | Treat as a bug; enforce with query-budget tests | — | — |

# Follow-up Questions

1. Which database does a deferred-field load go to in a multi-DB setup?
2. How would you make the serializer and the `only()` list impossible to drift apart?
3. How does `refresh_from_db()` differ from re-fetching with `get()`?

# Related Topics

* Module 06 Q4 — `only()` vs `defer()`
* Module 17 Q12 — `DeferredAttribute` internals
* Module 06 Q36 — enforcing query budgets in CI

---

# Question

What is the performance difference between values() and values_list()?

# Why Interviewer Asks This

A calibration question. A strong answer says the SQL is identical, the real win of both is skipping model instantiation, and the choice between them is about the shape of data you need — plus one or two practical tricks such as passing a `values()` queryset as a subquery.

# Answer

**Spoken answer:** "At the database level there's no difference — `values()` and `values_list()` produce exactly the same SELECT. The difference is in Python: `values()` gives you a dict per row, `values_list()` gives you a tuple, and tuples are a little cheaper to build. The big performance win of *both* is that they skip creating model instances, which is where most of the ORM's per-row overhead lives. So I pick by shape: `values()` when I'm building JSON or a report, `values_list('id', flat=True)` for a list of ids, and `named=True` when I want tuple speed with readable attribute access."

**The reasoning:**
- SQL: identical. Python: dict vs. tuple — a small difference you'd only notice on very large result sets.
- Versus model instances: no `__init__`, no `_state`, no descriptors, no `post_init` signal — that's the meaningful gap.
- `flat=True` (single field) returns scalars; `named=True` returns namedtuples.
- Don't materialise ids just to filter: pass the queryset itself and Django emits a subquery.

# Internal ORM Mechanics

Both methods call `_values()`, which sets `query.values_select` and swaps the queryset's `_iterable_class`: `ValuesIterable` (dict), `ValuesListIterable` (tuple), `FlatValuesListIterable` (scalar) or `NamedValuesListIterable` (namedtuple). The compiler and SQL are identical; only the row-to-object step differs. Field converters (`from_db_value`, e.g. JSON decoding, Decimal handling) still run for both.

# SQL Generated

```python
Device.objects.filter(status='active').values('id', 'name')
Device.objects.filter(status='active').values_list('id', 'name')
Reading.objects.filter(device__in=Device.objects.filter(status='active').values('id'))
```

```sql
-- values() and values_list(): the same statement
SELECT "iot_device"."id", "iot_device"."name" FROM "iot_device" WHERE "iot_device"."status" = 'active';

-- queryset passed as a filter value → subquery, one round-trip
SELECT "iot_reading"."id", "iot_reading"."device_id", "iot_reading"."value", "iot_reading"."taken_at"
FROM "iot_reading"
WHERE "iot_reading"."device_id" IN (SELECT U0."id" FROM "iot_device" U0 WHERE U0."status" = 'active');
```

# Code Example

```python
Device.objects.values('id', 'name')[:2]
# [{'id': 1, 'name': 'pump-01'}, {'id': 2, 'name': 'pump-02'}]

Device.objects.values_list('id', 'name')[:2]
# [(1, 'pump-01'), (2, 'pump-02')]

Device.objects.values_list('id', flat=True)[:2]
# [1, 2]

for d in Device.objects.values_list('id', 'name', named=True):
    print(d.id, d.name)          # Row(id=1, name='pump-01')

# Anti-pattern: two round-trips and a huge IN list
ids = list(Device.objects.filter(status='active').values_list('id', flat=True))
Reading.objects.filter(device_id__in=ids)

# Better: one statement with a subquery
Reading.objects.filter(device__in=Device.objects.filter(status='active').values('id'))
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub cache-warming cron job pushed lookup tables (integration id → name, owner, status) into Redis every [fill-in] minutes. **T** — It loaded full model instances for [fill-in] rows just to build a dict. **A** — I switched to `values_list('id', 'name', 'owner_id', 'status', named=True)` and built the cache payload directly from the tuples, and replaced one `list(...ids...)` + `__in` with a subquery. **R** — job runtime went from [fill-in] to [fill-in] s and peak memory from [fill-in] to [fill-in] MB.

# Performance Impact

- Same DB cost. Python cost: instances > dicts > tuples.
- The saving grows with row count and with how "heavy" the model is (many fields, custom `__init__`, `post_init` receivers).

**Trade-offs / when NOT to use it:**
- You lose model behaviour: methods, properties, `get_FOO_display()`, `save()`. Don't use it where business logic expects instances.
- Positional tuples are brittle when someone reorders the field list — prefer `named=True` or `values()` in shared code.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`values_list()` generates a faster query." The SQL is identical.
- "`values()` doesn't run field converters." It does — JSON is still decoded, decimals are still `Decimal`.
- Materialising an id list to feed `__in` instead of passing the queryset as a subquery.
- Using `values()` across a multi-valued relation and being surprised by duplicate rows.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | No meaningful difference | Negligible | ACCESS SHARE only |
| **Medium** | 1M | Tuples/dicts clearly beat instances in Python time | Dicts > tuples, both << instances | ACCESS SHARE only |
| **Large** | 100M | Combine with `.iterator(chunk_size=...)` to stream | Flat when streamed | ACCESS SHARE; server-side cursor on PostgreSQL |
| **Massive** | 1B+ | Push aggregation into SQL; only ship results | — | Replicas |

# Follow-up Questions

1. When does `values()` change the GROUP BY of a query?
2. What does `values_list(named=True)` return and when would you use it?
3. Why is passing a queryset to `__in` better than passing a list of ids?

# Related Topics

* Module 06 Q23 — what `values()` skips
* Module 06 Q27 — `values()` with `prefetch_related`
* Module 09 Q2 — `values()` + `annotate()` and GROUP BY

---

# Question

How do you implement batch updates using bulk_update() and what are its limits?

# Why Interviewer Asks This

Tests whether you can update many rows with *different* values efficiently, and whether you know what `bulk_update()` skips (save, signals, auto_now) and where it breaks down (huge CASE statements, parameter limits, duplicates).

# Answer

**Spoken answer:** "`bulk_update()` is for when every row needs a different value that I computed in Python. I load the objects, change attributes, then call `bulk_update(objs, ['field1', 'field2'], batch_size=...)`. Django turns each batch into a single UPDATE with a `CASE WHEN id = 1 THEN ... WHEN id = 2 THEN ...` per field. That's one statement per batch instead of one per row. The limits: it bypasses `save()` and signals, it doesn't touch `auto_now` fields unless I set and list them, it can't update primary keys, and large batches create huge CASE expressions — so I always set `batch_size`. If every row gets the *same* value, I don't use it at all; a plain `queryset.update()` is far cheaper."

**The reasoning:** you are trading N round-trips for one big statement per batch; that's a big win up to the point where the statement itself becomes expensive to build and plan.

- Returns the number of rows matched (Django 4.0+).
- `fields` is required and should be minimal.
- Duplicate objects in `objs`: only the first is applied.
- Backends cap batch size by their parameter limits; on SQL Server (~2,100 parameters) I set `batch_size` explicitly.

# Internal ORM Mechanics

For each batch, Django builds one `When(pk=obj.pk, then=value)` per object per field, wraps them in a `Case(..., output_field=field)` (on PostgreSQL it adds a cast because `requires_casted_case_in_updates` is true), and issues `QuerySet.filter(pk__in=batch_pks).update(**{field: case})`. The batch size defaults to `connection.ops.bulk_batch_size()`, which considers the number of parameters per object. All batches run inside one `transaction.atomic(savepoint=False)`.

# SQL Generated

```python
Ticket.objects.bulk_update(tickets, ['priority', 'sla_due_at'], batch_size=500)
```

```sql
UPDATE "helpdesk_ticket"
SET "priority" = (CASE WHEN ("helpdesk_ticket"."id" = 1) THEN 'high'
                       WHEN ("helpdesk_ticket"."id" = 2) THEN 'low'
                       ELSE NULL END)::varchar(10),
    "sla_due_at" = (CASE WHEN ("helpdesk_ticket"."id" = 1) THEN '2026-11-27T10:00:00+00:00'::timestamptz
                         WHEN ("helpdesk_ticket"."id" = 2) THEN '2026-11-30T10:00:00+00:00'::timestamptz
                         ELSE NULL END)::timestamp with time zone
WHERE "helpdesk_ticket"."id" IN (1, 2);
```

# Code Example

```python
from django.db import transaction
from django.utils import timezone

def reprioritise(ticket_ids, scorer):
    tickets = list(Ticket.objects.filter(id__in=ticket_ids).only('id', 'severity', 'customer_tier', 'priority', 'sla_due_at', 'updated_at'))
    now = timezone.now()
    for t in tickets:
        t.priority, t.sla_due_at = scorer(t)     # per-row value computed in Python
        t.updated_at = now                       # auto_now is NOT applied by bulk_update
    with transaction.atomic():
        return Ticket.objects.bulk_update(tickets, ['priority', 'sla_due_at', 'updated_at'], batch_size=500)

# Same value for every row? Don't use bulk_update:
Ticket.objects.filter(id__in=ticket_ids).update(priority='high', updated_at=timezone.now())
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub sync job pulled status codes for integration endpoints from an upstream system and mapped each to a health score. **T** — It called `save()` per endpoint: [fill-in] UPDATEs per run, each a round-trip, holding a connection from our pool for [fill-in] minutes. **A** — I computed scores in Python, called `bulk_update(endpoints, ['health_score', 'checked_at'], batch_size=500)` per chunk, and only included endpoints whose score had actually changed. **R** — UPDATE statements fell from [fill-in] to [fill-in] and runtime from [fill-in] to [fill-in].

# Performance Impact

- Round-trips: N → N / batch_size.
- Each statement grows with batch_size × fields; very large CASE expressions are slow to parse/plan and hold row locks on the whole batch until commit.
- Rows are locked for the duration of the surrounding transaction.

**Trade-offs / when NOT to use it:**
- Same value for all rows → `update()`. Value derived from other columns → `update(col=F(...))`.
- You need `save()` side effects (signals, audit history, cache invalidation) → you must replicate them explicitly or not use it.
- Huge volumes → staging table + `UPDATE ... FROM` in raw SQL is usually faster than giant CASE statements.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`bulk_update` sends signals / calls `save()`." It does neither.
- "It updates `updated_at` automatically." `auto_now` is not applied; set the value and list the field.
- Omitting `batch_size` on large lists and hitting parameter limits or massive statements.
- Updating every field "to be safe" — this rewrites unchanged columns and enlarges each statement.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | 1–2 statements | All objects in memory | ROW EXCLUSIVE + row locks on updated rows until commit |
| **Medium** | 1M | Chunk the *load* too (don't hold 1M instances); batch_size a few hundred | Bounded by chunk | Row locks per batch; commit per chunk |
| **Large** | 100M | Prefer staging table + `UPDATE ... FROM` | Flat with chunking | Short transactions to limit lock time and WAL bursts |
| **Massive** | 1B+ | Rethink: set-based SQL or a rebuilt table | — | Throttle to protect replicas |

# Follow-up Questions

1. Why is `queryset.update()` preferable when all rows get the same value?
2. How do you keep audit/history behaviour if you switch from `save()` to `bulk_update()`?
3. What happens if the same object appears twice in the list?

# Related Topics

* Module 06 Q9 — `update()` vs. looping `save()`
* Module 06 Q29 — chunking large querysets for updates
* Module 19 Q35 — `bulk_update` field-list risks

---

# Question

How does bulk_create() work database-wise and when are primary keys returned?

# Why Interviewer Asks This

Checks that you know `bulk_create()` is a multi-row INSERT that skips the model lifecycle, which backends return generated PKs, and how conflict handling (`ignore_conflicts`, `update_conflicts`) changes that.

# Answer

**Spoken answer:** "`bulk_create()` takes a list of unsaved instances and writes them with one multi-row `INSERT ... VALUES (...), (...)` per batch, instead of one INSERT per object. Because it doesn't call `save()`, no signals fire and nothing per-instance runs. Whether the objects get their primary keys back depends on the backend: PostgreSQL, and recent SQLite and MariaDB, support `RETURNING`, so Django sets the ids; MySQL doesn't. With `ignore_conflicts=True` you don't get ids back. For upserts there's `update_conflicts=True` with `unique_fields` and `update_fields`, which becomes `ON CONFLICT DO UPDATE` — and since Django 5.0 that also sets the PKs on PostgreSQL."

**The reasoning:**
- One statement per batch; `batch_size` controls statement size.
- No `save()`, no `pre_save`/`post_save`, no M2M assignment, not usable for multi-table-inheritance children.
- PK return is governed by `connection.features.can_return_rows_from_bulk_insert` — check it for your backend (I check it for the SQL Server backend rather than assume).

# Internal ORM Mechanics

`bulk_create()` validates the objects, splits them into objects with and without a PK set, and calls `_batched_insert()`. Each batch becomes an `InsertQuery` compiled by `SQLInsertCompiler` into a multi-row VALUES statement. If the backend can return rows and no conflict-ignore is requested, the compiler appends `RETURNING` and Django assigns the returned PKs (and any `db_returning` fields) back onto the objects, marking `_state.adding = False` and `_state.db`. With `update_conflicts`, the backend's `on_conflict_suffix_sql()` adds `ON CONFLICT (...) DO UPDATE SET col = EXCLUDED.col`.

# SQL Generated

```python
Event.objects.bulk_create(events, batch_size=1000)
Event.objects.bulk_create(events, update_conflicts=True, unique_fields=['source', 'external_id'], update_fields=['payload', 'received_at'])
```

```sql
INSERT INTO "events_event" ("source", "external_id", "kind", "payload", "received_at")
VALUES ('crm', 'A-1', 'contact.updated', '{"id": 1}'::jsonb, '2026-11-26T09:00:00+00:00'::timestamptz),
       ('crm', 'A-2', 'contact.created', '{"id": 2}'::jsonb, '2026-11-26T09:00:01+00:00'::timestamptz)
RETURNING "events_event"."id";

INSERT INTO "events_event" ("source", "external_id", "kind", "payload", "received_at")
VALUES (...), (...)
ON CONFLICT("source", "external_id") DO UPDATE
SET "payload" = EXCLUDED."payload", "received_at" = EXCLUDED."received_at"
RETURNING "events_event"."id";
```

# Code Example

```python
from django.db import connection

class Event(models.Model):
    source = models.CharField(max_length=30)
    external_id = models.CharField(max_length=64)
    kind = models.CharField(max_length=50)
    payload = models.JSONField()
    received_at = models.DateTimeField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['source', 'external_id'], name='uniq_event_source_ext')]

events = [Event(source='crm', external_id=r['id'], kind=r['type'], payload=r, received_at=r['ts']) for r in batch]
created = Event.objects.bulk_create(events, batch_size=1000)

if connection.features.can_return_rows_from_bulk_insert:
    assert all(e.pk for e in created)          # ids populated (PostgreSQL)

# Idempotent re-delivery of the same events → upsert
Event.objects.bulk_create(events, update_conflicts=True,
                          unique_fields=['source', 'external_id'],
                          update_fields=['payload', 'received_at'])
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub consumes integration events from RabbitMQ; at-least-once delivery means duplicates. **T** — The consumer did `get_or_create()` per message — [fill-in] queries per message and occasional `IntegrityError` races between consumers. **A** — I buffered messages and wrote them with `bulk_create(update_conflicts=True, unique_fields=['source', 'external_id'], ...)` backed by a `UniqueConstraint`, acking messages only after the batch committed. **R** — inserts per second went from [fill-in] to [fill-in], duplicate-key errors went to zero, and DB round-trips per message dropped to roughly [fill-in].

# Performance Impact

- Round-trips: N → N / batch_size; parsing and WAL overhead per row also drops.
- Every index on the table still has to be updated per row — the insert cost is dominated by index maintenance at scale.
- Very large batches mean large statements and long-held locks on unique-index entries.

**Trade-offs / when NOT to use it:**
- Need signals, custom `save()` logic or M2M wiring → you must do that explicitly afterwards.
- Multi-table inheritance children → not supported.
- Millions of rows → `COPY` (PostgreSQL) or bulk-load tools beat `bulk_create`.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "PKs are always set after `bulk_create`." Only on backends that support returning rows, and not with `ignore_conflicts=True`.
- "`post_save` fires for each object." No signals fire.
- "`ignore_conflicts` is a safe upsert." It silently drops the conflicting rows — the existing row is *not* updated.
- No `batch_size` on huge lists.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | One statement | Trivial | ROW EXCLUSIVE; no locks on existing rows |
| **Medium** | 1M | Batches of ~1–5K; build objects from a generator | Bounded per batch | Unique-index checks can wait on concurrent inserts of the same key |
| **Large** | 100M | Use `COPY`; consider dropping/rebuilding secondary indexes for one-off loads | Flat if streamed | ROW EXCLUSIVE; WAL volume drives replica lag |
| **Massive** | 1B+ | Partitioned target; parallel loaders per partition | — | Throttle; monitor replication lag |

# Follow-up Questions

1. Why doesn't `ignore_conflicts=True` return primary keys?
2. How would you make an event consumer idempotent with `bulk_create`?
3. When would you choose `COPY` over `bulk_create`?

# Related Topics

* Module 06 Q19 — bulk inserts of millions of rows
* Module 06 Q39 — sync jobs with in_bulk and upserts
* Module 02 Q35 — `db_default` in `bulk_create`

---

# Question

Why is update() faster than looping and calling save(), and what does it bypass?

# Why Interviewer Asks This

Separates people who know the ORM cost model (round-trips, full-row writes, race windows) from those who don't, and checks that you know the side effects you lose — a common source of production bugs.

# Answer

**Spoken answer:** "`queryset.update()` becomes a single `UPDATE ... WHERE` executed entirely in the database: one round-trip, no rows loaded into Python. Looping and calling `save()` means loading every row, then one UPDATE per object, and by default each `save()` writes *every* column — so you also risk overwriting changes another process made in between. `update()` is also atomic per statement and works with `F()` expressions for race-free increments. What you lose: it doesn't call `save()`, doesn't send `pre_save`/`post_save` signals, doesn't apply `auto_now`, and doesn't run validation. So any logic hanging off those — audit history, cache invalidation, search indexing — won't run unless you trigger it explicitly."

**The reasoning:**
- 1 statement vs. 1 SELECT + N UPDATEs.
- No Python objects, no per-row serialization.
- Full-row `save()` = lost-update risk; `update()` touches only named columns.
- Returns the number of rows matched.

# Internal ORM Mechanics

`QuerySet.update(**kwargs)` builds an `UpdateQuery` from the current filters, resolves each value (literals, `F()`, `Case`, `Subquery`), and compiles with `SQLUpdateCompiler`. Filters that span relations are turned into `WHERE pk IN (SELECT ...)` because an UPDATE can only target one table; you can't *set* fields on related models. `Model.save()`, by contrast, runs `pre_save` signals, `Field.pre_save()` (which is where `auto_now` lives), then an UPDATE of all concrete fields (unless `update_fields`), then `post_save`.

# SQL Generated

```python
Subscription.objects.filter(status='active', expires_at__lt=now).update(status='expired', updated_at=now)
```

```sql
-- update(): one statement
UPDATE "billing_subscription"
SET "status" = 'expired', "updated_at" = '2026-11-26T00:00:00+00:00'::timestamptz
WHERE ("billing_subscription"."expires_at" < '2026-11-26T00:00:00+00:00'::timestamptz
       AND "billing_subscription"."status" = 'active');

-- loop + save(): one SELECT, then N of these, each rewriting every column
UPDATE "billing_subscription"
SET "customer_id" = 7, "plan_id" = 3, "status" = 'expired', "expires_at" = '...', "updated_at" = '...'
WHERE "billing_subscription"."id" = 1;
```

# Code Example

```python
from django.db.models import F
from django.utils import timezone

now = timezone.now()

# Slow and racy: N round-trips, full-row writes
for sub in Subscription.objects.filter(status='active', expires_at__lt=now):
    sub.status = 'expired'
    sub.save()

# Fast: one statement
expired = Subscription.objects.filter(status='active', expires_at__lt=now).update(status='expired', updated_at=now)

# Race-free counter
Plan.objects.filter(pk=plan_id).update(active_subscriptions=F('active_subscriptions') - 1)

# Keep side effects explicit when you bypass save()
def expire_subscriptions(now):
    ids = list(Subscription.objects.filter(status='active', expires_at__lt=now).values_list('id', flat=True))
    Subscription.objects.filter(id__in=ids).update(status='expired', updated_at=now)
    cache.delete_many([f'sub:{i}' for i in ids])        # what post_save used to do
    return len(ids)
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub caches integration summaries in Redis and invalidated them from a `post_save` receiver. **T** — After a nightly job was optimised from `save()` loops to `update()`, the dashboard showed stale statuses until TTL expiry — a correctness bug hidden by a performance fix. **A** — I moved the update and the invalidation into one QuerySet method (`mark_stale_and_invalidate()`), used `transaction.on_commit` for the cache delete, and documented that `update()` bypasses signals. **R** — the job stayed at [fill-in] s instead of [fill-in] min, and stale reads disappeared.

# Performance Impact

- Round-trips: 1 vs. N + 1. No Python objects. Write volume limited to named columns.
- Row locks are taken on all matched rows in one statement — a huge `update()` can lock a lot of rows for a long time; chunk very large ones.

**Trade-offs / when NOT to use it:**
- Logic that *must* run per row (complex validation, external calls, history models) → loop or bulk_update plus explicit hooks.
- Massive updates on hot tables → chunk by PK range to keep lock time and WAL bursts small.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`update()` triggers `post_save`." It doesn't.
- "`auto_now` fields update automatically." Not with `update()`; set them explicitly.
- "`save()` only writes changed fields." It writes every field unless you pass `update_fields`.
- "You can do `update(author__name='x')`." You can filter across relations, not set related fields.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | One fast statement | None in Python | ROW EXCLUSIVE + row locks on matched rows |
| **Medium** | 1M | Index on filter columns matters more than anything else | None | Row locks on every matched row until commit |
| **Large** | 100M | Chunk by PK range; avoid one statement touching millions | None | Short transactions to avoid blocking writers |
| **Massive** | 1B+ | Partition-level operations; throttle for replica lag | None | Monitor WAL generation |

# Follow-up Questions

1. How do you keep audit history if you use `update()`?
2. What does `update()` return and how would you use it for optimistic locking?
3. How does `update()` handle a filter that spans a relation?

# Related Topics

* Module 06 Q7 — `bulk_update()`
* Module 15 Q23 — F expressions to avoid race conditions
* Module 15 Q9 — optimistic locking with a version field

---

# Question

How do you write a query to avoid the N+1 problem on reverse foreign keys?

# Why Interviewer Asks This

Reverse FKs (`department.employees.all()`) are the most common N+1 in real code. The interviewer wants you to choose the right tool by what the screen actually needs — rows, a filtered subset, a count, or the latest child.

# Answer

**Spoken answer:** "A reverse foreign key is a one-to-many relation, so a JOIN isn't the answer — it would repeat the parent for every child. The fix depends on what the page needs. If it needs the child rows, `prefetch_related('employees')` gives me two queries total. If it needs only some children, a `Prefetch` object with a filtered queryset. If it only needs a number — headcount — I don't load children at all; I `annotate(Count(...))`, which is one query with GROUP BY. And if it needs only the latest child, a `Subquery` annotation. The mistake I see most is prefetching thousands of rows just to call `len()` on them."

**Choosing the tool:**
- All children → `prefetch_related('employees')`.
- Filtered/ordered children → `Prefetch('employees', queryset=..., to_attr=...)`.
- Counts/sums → `annotate(n=Count('employees', filter=Q(...)))`.
- Latest child / one value → `annotate(x=Subquery(...))`.

# Internal ORM Mechanics

The reverse accessor (`employees`, set by `related_name`) is a `ReverseManyToOneDescriptor`. Without prefetching, each access builds `Employee.objects.filter(department=instance)` — one query per department. `prefetch_related` makes the descriptor produce one `department_id IN (...)` query and group by `department_id`. `annotate(Count('employees'))` instead joins the child table and adds GROUP BY — on PostgreSQL Django groups by the parent PK only, because the other columns are functionally dependent on it.

# SQL Generated

```python
Department.objects.annotate(
    headcount=Count('employees', filter=Q(employees__employment_status='active'))
).prefetch_related(
    Prefetch('employees', queryset=Employee.objects.filter(employment_status='active').only('id', 'name', 'department_id'), to_attr='active_staff')
)
```

```sql
SELECT "hr_department"."id", "hr_department"."name",
       COUNT("hr_employee"."id") FILTER (WHERE "hr_employee"."employment_status" = 'active') AS "headcount"
FROM "hr_department"
LEFT OUTER JOIN "hr_employee" ON ("hr_department"."id" = "hr_employee"."department_id")
GROUP BY "hr_department"."id";

SELECT "hr_employee"."id", "hr_employee"."name", "hr_employee"."department_id"
FROM "hr_employee"
WHERE ("hr_employee"."employment_status" = 'active' AND "hr_employee"."department_id" IN (1, 2, 3));
```

# Code Example

```python
from django.db.models import Count, OuterRef, Prefetch, Q, Subquery

# N+1: one query per department
for d in Department.objects.all():
    print(d.name, d.employees.count())

# Only need the number → 1 query, no child rows
for d in Department.objects.annotate(headcount=Count('employees')):
    print(d.name, d.headcount)

# Need the rows (filtered) → 2 queries
depts = Department.objects.prefetch_related(
    Prefetch('employees',
             queryset=Employee.objects.filter(employment_status='active').only('id', 'name', 'department_id'),
             to_attr='active_staff'))

# Need just the latest hire → 1 query with a correlated subquery
latest = Employee.objects.filter(department=OuterRef('pk')).order_by('-hired_on')
depts = Department.objects.annotate(latest_hire=Subquery(latest.values('name')[:1]))
```

# Production Scenario

**From experience (STAR):** **S** — The PNI Hub analytics dashboard (fed by ~30k new rows/day) listed each integration with its error count for the day and its last error message. **T** — The view called `integration.errors.filter(day=today).count()` and `.order_by('-at').first()` per row, which cost [fill-in] queries per page load. **A** — I replaced both with annotations: `Count('errors', filter=Q(errors__day=today))` and a `Subquery` for the last message, backed by an `(integration_id, day)` index. **R** — one query per page instead of [fill-in]; page time went from [fill-in] to [fill-in] ms.

# Performance Impact

- prefetch: 2 queries but ships every child row — cost grows with children per parent.
- annotate Count: 1 query, aggregation done in the DB, nothing shipped but the number.
- Subquery: 1 query; correlated per parent row, so it needs an index on `(fk, order_col)`.

**Trade-offs / when NOT to use it:**
- Two `Count`s over *different* multi-valued relations in one query inflate each other (JOIN fan-out) — use `distinct=True` or subqueries.
- Don't prefetch huge child sets for a summary screen — aggregate instead.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Use `select_related('employees')`." Not possible for reverse FK — `FieldError`.
- "Prefetch, then `len()` for counts." Works, but ships every row just to count it.
- Prefetching and then calling `.filter()` in the loop — new query per object.
- Forgetting the FK (`department_id`) in `only()` inside the `Prefetch`.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Any approach is fast once N+1 is gone | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Index on child FK is critical for both prefetch and JOIN/aggregate | Prefetch holds all children per page | ACCESS SHARE only |
| **Large** | 100M | Prefer aggregates/subqueries; prefetch only bounded subsets | Keep children per page bounded | ACCESS SHARE only |
| **Massive** | 1B+ | Pre-aggregate into summary tables refreshed by jobs | Minimal | Replicas for dashboards |

# Follow-up Questions

1. Why do two `Count` annotations on different relations give wrong numbers?
2. When is a `Subquery` better than a prefetch?
3. How would you show "latest 3 children per parent" efficiently?

# Related Topics

* Module 06 Q30 — prefetching only active / latest-N items
* Module 09 Q4 — multiple annotations without double counting
* Module 10 Q11 — Subquery for the latest related record

---

# Question

How does exists() optimize presence checks compared to count() or len()?

# Why Interviewer Asks This

A cost-model question at the database level: does the candidate know what each call makes the database do — stop at the first row, count every match, or ship every row — and the cases where `exists()` is *not* fast. (Module 01 Q6 covers the `if queryset:` truthiness/caching angle; this one is about database cost.)

# Answer

**Spoken answer:** "They answer different questions at very different costs. `exists()` becomes `SELECT 1 ... LIMIT 1`, so the database can stop at the first matching row. `count()` becomes `SELECT COUNT(*)`, so it has to visit every matching row — on PostgreSQL that usually means checking row visibility too, because of MVCC. `len(queryset)` is the worst: it fetches every row and builds every model instance just to count them in Python. So: `exists()` when I need a yes/no, `count()` when I need the number, and `len()` only when I've already loaded the rows anyway. One nuance — `exists()` is only fast if the database can find a match quickly. If nothing matches and there's no usable index, it still scans the whole table to prove that."

**The reasoning:**
- `exists()` → early exit at first match.
- `count()` → full count of matches (index-only scans help if the visibility map is current).
- `len()` → full fetch + instantiation.
- If you'll iterate the rows anyway, evaluate once and test the result — calling `exists()` first adds a round-trip.

# Internal ORM Mechanics

`QuerySet.exists()` checks `_result_cache` first; if already evaluated it returns `bool(self._result_cache)` with no query. Otherwise it calls `query.has_results()`, which clones the query, clears ordering and the select list, adds `SELECT 1 AS "a"` and `LIMIT 1`. `count()` also checks the cache (`len(self._result_cache)`), otherwise calls `query.get_count()`, which wraps the query in `COUNT(*)` — with a subquery if the query has `distinct`, slicing or aggregates. `len()` calls `_fetch_all()`. `QuerySet.contains(obj)` (4.0+) is the `exists()` equivalent for "is this object in the set".

# SQL Generated

```python
qs = Order.objects.filter(customer_id=7, status='pending')
qs.exists(); qs.count(); len(qs)
```

```sql
SELECT 1 AS "a" FROM "shop_order"
WHERE ("shop_order"."customer_id" = 7 AND "shop_order"."status" = 'pending') LIMIT 1;

SELECT COUNT(*) AS "__count" FROM "shop_order"
WHERE ("shop_order"."customer_id" = 7 AND "shop_order"."status" = 'pending');

SELECT "shop_order"."id", "shop_order"."customer_id", "shop_order"."status", "shop_order"."total", "shop_order"."placed_at"
FROM "shop_order"
WHERE ("shop_order"."customer_id" = 7 AND "shop_order"."status" = 'pending');
```

# Code Example

```python
pending = Order.objects.filter(customer_id=7, status='pending')

# Yes/no only → exists()
if pending.exists():
    raise ValidationError('Customer already has a pending order')

# Need the number, not the rows → count()
badge = pending.count()

# Will render the rows anyway → evaluate once, reuse the cache
orders = list(pending[:20])
if orders:                       # no extra query
    render(orders)

# Membership of a specific object
if pending.contains(order):      # SELECT 1 ... WHERE ... AND id = %s LIMIT 1
    ...
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub's RBAC layer checked "does this user have any active role grant for this integration?" on every API request. **T** — It was written as `if user.grants.filter(...).count() > 0`, running a full COUNT on a grants table of [fill-in] rows on every request. **A** — I changed it to `exists()`, added a composite index on `(user_id, integration_id, is_active)` so the first match is an index seek, and cached the resulting role set per request. **R** — that check went from [fill-in] ms to [fill-in] ms and DB CPU on the hot path dropped by [fill-in]%.

# Performance Impact

- `exists()`: best case one index probe; worst case (no match, no index) a full scan.
- `count()`: always proportional to matching rows; on huge tables `COUNT(*)` is a classic CPU hog (admin changelists, DRF page counts).
- `len()`: proportional to rows *and* row width, plus Python instantiation.

**Trade-offs / when NOT to use it:**
- Don't call `exists()` and then iterate — that's two queries where one would do.
- For approximate big-table counts (pagination UI), consider estimated counts from `pg_class.reltuples` instead of `COUNT(*)`.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`exists()` is always O(1)." Only when an index (or an early row) satisfies it.
- "`count()` is free with an index." It still visits every matching index entry and often the heap for visibility.
- "`len(qs)` and `qs.count()` are the same." One ships every row, the other ships one number.
- Using `if qs.count() > 0:` for presence checks.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | All three are fast | `len()` loads all rows | ACCESS SHARE only |
| **Medium** | 1M | `count()` noticeably slower than `exists()`; `len()` unacceptable | `len()` = 1M instances | ACCESS SHARE only |
| **Large** | 100M | `exists()` needs an index on filter columns; `count()` may take seconds | — | ACCESS SHARE only |
| **Massive** | 1B+ | Use estimated counts or pre-computed counters | — | Replicas for counting |

# Follow-up Questions

1. When can `exists()` be as slow as `count()`?
2. How would you show a total count on a 100M-row admin changelist?
3. Why is `if qs:` followed by a loop fine, but `if qs.exists():` followed by a loop wasteful?

# Related Topics

* Module 01 Q6 — `if queryset:` vs `exists()` (truthiness and caching)
* Module 19 Q16 — `count()` and DB CPU
* Module 10 Q13 — SQL generated by `Exists`

---

# Question

What is the impact of select_related on outer joins and memory consumption?

# Why Interviewer Asks This

Goes past "select_related is good": does the candidate understand when Django emits LEFT OUTER JOINs, how row width and duplication grow, and that Django creates a separate Python object per row because there is no identity map?

# Answer

**Spoken answer:** "`select_related` uses an INNER JOIN when the foreign key is non-nullable and a LEFT OUTER JOIN when it's `null=True`, because rows without a related object still have to come back. Every joined table adds all its columns to every row. So with a chain like `ticket → project → client` on wide tables, the row gets big fast, and if many tickets share the same project, the project's columns are repeated for each one — and Django builds a separate project object for each ticket, since it has no identity map. So it's a great tool for one or two narrow FK hops; for low-cardinality relations repeated across many rows, prefetching the FK can actually use less memory because the related object is fetched once and shared."

**The reasoning:**
- `null=True` FK → LEFT OUTER JOIN; non-null → INNER JOIN.
- Filtering on a field of a LEFT-joined relation *promotes* it to INNER JOIN (rows without a match can't satisfy the filter).
- Width: sum of all joined tables' columns × rows. Duplication: repeated related data per row, one Python object per row.
- `select_related()` with no args follows every non-null FK recursively — avoid it in production code.

# Internal ORM Mechanics

The compiler's `get_related_selections()` walks the requested paths, calls `query.setup_joins()` for each, and chooses `INNER` or `LOUTER` per join based on nullability; `Query.promote_joins()` / `demote_joins()` adjust join types when filters require it. For each row, `RelatedPopulator` instances slice the row into per-model chunks and call `Model.from_db()` for each related model, storing the result in the parent's `_state.fields_cache`. There is no cache keyed by PK across rows — two tickets in the same project get two distinct `Project` objects.

# SQL Generated

```python
Ticket.objects.select_related('assignee', 'project__client')
Ticket.objects.select_related('assignee').filter(assignee__team='platform')
```

```sql
-- assignee is nullable → LEFT OUTER; project and client are NOT NULL → INNER
SELECT "helpdesk_ticket".*, "auth_user".*, "pm_project".*, "crm_client".*
FROM "helpdesk_ticket"
LEFT OUTER JOIN "auth_user" ON ("helpdesk_ticket"."assignee_id" = "auth_user"."id")
INNER JOIN "pm_project" ON ("helpdesk_ticket"."project_id" = "pm_project"."id")
INNER JOIN "crm_client" ON ("pm_project"."client_id" = "crm_client"."id");

-- filtering on the nullable relation promotes it to INNER JOIN
SELECT "helpdesk_ticket".*, "auth_user".*
FROM "helpdesk_ticket"
INNER JOIN "auth_user" ON ("helpdesk_ticket"."assignee_id" = "auth_user"."id")
WHERE "auth_user"."team" = 'platform';
```

(`.*` used for brevity; Django lists every column explicitly.)

# Code Example

```python
tickets = list(Ticket.objects.select_related('project')[:1000])
tickets[0].project is tickets[1].project    # False even if same project → 1,000 Project objects

# Few distinct projects, many tickets → prefetch the FK: projects fetched once and shared
tickets = list(Ticket.objects.prefetch_related('project')[:1000])
tickets[0].project is tickets[1].project    # True when they share a project

# Narrow the JOIN to the columns you need
Ticket.objects.select_related('project').only('id', 'title', 'project__name')
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub CSV export of [fill-in] sync-run rows used `select_related('integration__owner', 'integration__department')`. **T** — The worker's memory peaked at [fill-in] GB because each row carried full copies of integration, owner and department — only ~[fill-in] distinct integrations existed. **A** — I switched to `values_list()` with just the needed columns across the joins, streamed with `iterator(chunk_size=5000)`, and wrote rows directly to the CSV. **R** — memory dropped to [fill-in] MB and export time from [fill-in] to [fill-in].

# Performance Impact

- Network/memory ∝ rows × (sum of joined table widths).
- LEFT OUTER JOINs give the planner less freedom to reorder and can keep a large outer table in play.
- Python time: one `from_db()` per related model per row.

**Trade-offs / when NOT to use it:**
- Many rows, few distinct related objects → `prefetch_related` on the FK, or `values()` for read-only output.
- Deep chains on wide tables → narrow with `only()`, or don't join at all if the template doesn't need it.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`select_related` always uses INNER JOIN." Nullable FKs get LEFT OUTER JOIN.
- "Django reuses the same related object across rows." No identity map — one object per row.
- "`select_related()` with no args is a safe default." It follows every non-null FK, often far more than needed.
- "More joins is always better than more queries." Not when the joins multiply width and duplication.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Negligible either way | Duplicated objects don't matter | ACCESS SHARE only |
| **Medium** | 1M | Join cost depends on FK indexes and join order | Width × rows starts to matter for exports | ACCESS SHARE only |
| **Large** | 100M | Hash joins on big tables; keep joins to what you display | Stream, or use `values()` | ACCESS SHARE only |
| **Massive** | 1B+ | Denormalise display fields or pre-join in a reporting table | — | Replicas / warehouse |

# Follow-up Questions

1. When does Django promote a LEFT OUTER JOIN to INNER JOIN?
2. Why can `prefetch_related` on a ForeignKey use less memory than `select_related`?
3. How would you export 10M joined rows without running out of memory?

# Related Topics

* Module 06 Q1 — select_related vs prefetch_related
* Module 17 Q26 — join promotion internals
* Module 06 Q32 — `only()` with deep `select_related`

---

# Question

How do you optimize large scale deletions using Django ORM?

# Why Interviewer Asks This

`queryset.delete()` looks like one statement but often isn't. The interviewer wants to know whether you understand Django's delete Collector — cascades emulated in Python, signals, when "fast delete" applies — and how that behaves on millions of rows.

# Answer

**Spoken answer:** "In Django, `delete()` is not just `DELETE FROM ... WHERE`. Django emulates `on_delete` in Python: a Collector walks every relation that points at the model, gathers the objects to cascade, set-null or protect, and fires `pre_delete`/`post_delete` signals per object. Only when nothing needs Python handling — no signal receivers and nothing pointing at the model except `DO_NOTHING` relations — can Django 'fast delete' with a single statement. A model with even one CASCADE child gets loaded into memory first, and then its children can be fast-deleted by foreign key. On millions of rows that means huge memory use, one long transaction, lots of WAL and replica lag. So for large deletes I delete in PK-range batches with short transactions, keep signal receivers off the bulky child tables so they stay fast-deletable, make sure every FK column pointing at the table is indexed, and for time-series data I don't delete rows at all — I drop or detach old partitions."

**The reasoning:**
- `delete()` returns `(total, {model_label: count})` — a hint that it handles many tables.
- Fast delete of a queryset needs: no `pre_delete`/`post_delete`/`m2m_changed` receivers, no multi-table-inheritance parents, no GenericRelations, and **every relation pointing at the model set to `DO_NOTHING`**.
- Children reached through CASCADE are fast-deleted (`DELETE ... WHERE fk IN (...)`) if they meet the same conditions — so keeping big child tables signal-free matters most.
- Django-created FK constraints have no `ON DELETE` clause in 5.x, so the DB won't cascade for you.
- Unindexed child FKs make every cascade a sequential scan.

# Internal ORM Mechanics

`QuerySet.delete()` creates a `Collector(using=db)` and calls `collect(qs)`. `can_fast_delete()` is true only if the model has no signal listeners, no concrete parents, no private fields with `bulk_related_objects` (GenericRelation) and every candidate relation is `DO_NOTHING`; then the queryset goes to `fast_deletes` and runs as one `DELETE ... WHERE`. Otherwise the Collector evaluates the queryset, and for each related field either adds a fast-delete queryset for the children (when they qualify) or loads them in batches (sized by `connection.ops.bulk_batch_size`) and applies `on_delete` (CASCADE → collect again, SET_NULL → field updates, PROTECT/RESTRICT → errors). `Collector.delete()` sorts models into dependency order, sends `pre_delete` per instance, runs field updates, fast deletes and batched `DELETE ... WHERE id IN (...)`, then `post_delete` — all in one `transaction.atomic()`.

# SQL Generated

```python
SyncRun.objects.filter(started_at__lt=cutoff).delete()   # SyncRunLog has FK → SyncRun (CASCADE)
```

```sql
-- SyncRun has a CASCADE child, so it can't be fast-deleted: Django loads the parents first
SELECT "ops_syncrun"."id", ... FROM "ops_syncrun" WHERE "ops_syncrun"."started_at" < '2026-08-01T00:00:00+00:00'::timestamptz;

-- SyncRunLog has no receivers and no dependents → fast-deleted by FK, never loaded
DELETE FROM "ops_syncrunlog" WHERE "ops_syncrunlog"."run_id" IN (1, 2, 3 /* … */);

-- then the parents
DELETE FROM "ops_syncrun" WHERE "ops_syncrun"."id" IN (1, 2, 3 /* … */);
```

# Code Example

```python
import time
from django.db import transaction

def purge_sync_runs(cutoff, batch=5000, pause=0.1):
    """Delete old runs in small, short transactions so locks, WAL and replica lag stay bounded."""
    total = 0
    while True:
        ids = list(SyncRun.objects.filter(started_at__lt=cutoff)
                   .order_by('pk').values_list('pk', flat=True)[:batch])
        if not ids:
            return total
        with transaction.atomic():
            deleted, _ = SyncRun.objects.filter(pk__in=ids).delete()
        total += deleted
        time.sleep(pause)        # let replication and OLTP traffic breathe

# Child FK must be indexed or every cascade scans the child table
class SyncRunLog(models.Model):
    run = models.ForeignKey(SyncRun, on_delete=models.CASCADE, related_name='logs')   # db_index=True by default
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub keeps sync-run history and per-run logs from ten scheduled django-crontab jobs. **T** — A retention job ran `SyncRun.objects.filter(started_at__lt=cutoff).delete()` once a month; it held a transaction for [fill-in] minutes and spiked memory to [fill-in] GB, because an audit `post_delete` receiver on the *log* model forced Django to load every log row instead of fast-deleting them, and it lagged the read replica by [fill-in] s. **A** — I moved the audit write into the job (one summary row per batch) so the log table became fast-deletable again, ran the purge nightly in 5,000-row PK batches, and added the missing index on the log table's FK. **R** — each batch now commits in [fill-in] ms, replica lag stays under [fill-in] s and memory is flat.

# Performance Impact

- Non-fast delete: memory ∝ rows (all collected instances) and one transaction for everything.
- Each deleted row = WAL + index entry removal in every index; table bloat until VACUUM.
- Missing FK indexes on child tables turn each cascade batch into a sequential scan.

**Trade-offs / when NOT to use it:**
- Time-series or retention data → partition by time and `DETACH`/`DROP PARTITION` (metadata operation, near-instant).
- Deleting an entire table → `TRUNCATE` (but it takes ACCESS EXCLUSIVE and bypasses Django entirely).
- `_raw_delete()` skips cascades and signals — private API; only with full knowledge of the FK graph.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`delete()` is one SQL statement." Only in the fast-delete case — and any CASCADE child rules that out for the parent.
- "The database handles CASCADE." In Django 5.x the cascade is emulated in Python; the DB constraint has no `ON DELETE` action.
- "Just wrap it in one big transaction." That maximises lock time, WAL burst and replica lag.
- Forgetting that a single `pre_delete`/`post_delete` receiver (audit, cache) on a big child table forces Django to load every child row.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Plain `delete()` is fine | Trivial | ROW EXCLUSIVE + row locks until commit |
| **Medium** | 1M | Batch by PK; keep big child tables fast-deletable | Bounded per batch | Short transactions per batch |
| **Large** | 100M | Batched deletes + VACUUM tuning, or partition drops | Flat | Row locks per batch; watch replica lag |
| **Massive** | 1B+ | Partitioning is the only sane retention strategy | — | DETACH PARTITION CONCURRENTLY (PG14+) |

# Follow-up Questions

1. What conditions allow Django to fast-delete, and why does one CASCADE child rule it out for the parent?
2. Why do child-table FK indexes matter for deleting parents?
3. How does partitioning change your retention strategy?

# Related Topics

* Module 06 Q20 — batch deletions without violating constraints
* Module 16 Q27 — chunked cleanup jobs
* Module 20 Q24 — deleting 50M rows a day with zero impact

---

# Question

How does django-debug-toolbar identify duplicate and slow queries?

# Why Interviewer Asks This

Tests practical debugging tooling: how the toolbar captures SQL, the difference between "similar" and "duplicate" queries (each points to a different bug), and the tool's limits for JSON APIs and production.

# Answer

**Spoken answer:** "The SQL panel wraps each database connection's cursor for the duration of a request, so every query is recorded with its SQL, parameters, duration and the Python stack trace that issued it. It then groups them: 'similar' means the same SQL with different parameters — that's the signature of an N+1 loop; 'duplicate' means the same SQL *and* the same parameters — that's the same data being fetched repeatedly, which points to missing caching or a repeated permission check. Queries slower than a configurable threshold are highlighted, and you can run EXPLAIN on any of them from the panel. It's a development tool though — for JSON APIs I lean on the browsable API, django-silk, or a query-count test, and in production on `pg_stat_statements`."

**The reasoning:**
- Similar = N+1 → fix with select/prefetch/annotate.
- Duplicate = redundant work → fix with caching, `cached_property`, or passing data down.
- The stack trace is what makes it actionable — it tells you which line issued the query.

# Internal ORM Mechanics

On each request, the SQL panel's `enable_instrumentation()` wraps the cursor of every configured connection (`connections[alias]`) with a tracking wrapper that times `execute`/`executemany` and records SQL, params, duration, alias, transaction status and a filtered stack trace. At the end of the request, the panel computes a fingerprint of the SQL without params to group "similar" queries, and SQL + params to group "duplicate" ones; it flags queries above `SQL_WARNING_THRESHOLD` (milliseconds, default 500). It only renders on HTML responses for requests that pass `SHOW_TOOLBAR_CALLBACK` (by default: `DEBUG=True` and `REMOTE_ADDR` in `INTERNAL_IPS`).

# SQL Generated

What the panel typically surfaces (illustrative):

```sql
-- "similar" ×N  → N+1: same statement, different params
SELECT "pm_project"."id", "pm_project"."name" FROM "pm_project" WHERE "pm_project"."id" = 14 LIMIT 21;
SELECT "pm_project"."id", "pm_project"."name" FROM "pm_project" WHERE "pm_project"."id" = 15 LIMIT 21;

-- "duplicate" ×N → identical statement and params, e.g. a permission lookup per object
SELECT "auth_group"."name" FROM "auth_group"
INNER JOIN "auth_user_groups" ON ("auth_group"."id" = "auth_user_groups"."group_id")
WHERE "auth_user_groups"."user_id" = 12;
```

# Code Example

```python
# settings/dev.py — never in production settings
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_CONFIG = {'SQL_WARNING_THRESHOLD': 100}   # ms — highlight anything slower

# urls.py
from django.conf import settings
from django.urls import include, path
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

# Fixing a "duplicate": compute once per request
from django.utils.functional import cached_property

class RBACContext:
    def __init__(self, user):
        self.user = user

    @cached_property
    def role_names(self):
        return set(self.user.groups.values_list('name', flat=True))
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub uses Azure AD (MSAL) login with RBAC roles mapped to Django groups. **T** — The integration list page felt slow; the toolbar showed [fill-in] *duplicate* group lookups (a permission check per row) and [fill-in] *similar* project queries. **A** — I cached the user's role set once per request on an RBAC context object and added `select_related('project')`; I used the toolbar's stack traces to find both call sites in minutes. **R** — queries per page went from [fill-in] to [fill-in]; TTFB from [fill-in] to [fill-in] ms.

# Performance Impact

- The toolbar itself adds overhead (stack capture per query) — timings are inflated and relative, not absolute.
- It changes nothing in production unless misconfigured — which is a security risk (it exposes SQL and settings).

**Trade-offs / when NOT to use it:**
- JSON APIs: the toolbar needs an HTML response — use the DRF browsable API, django-silk, or `CaptureQueriesContext` in tests.
- Production: use `pg_stat_statements`, slow-query logs and APM tracing instead.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Duplicate and similar mean the same thing." Similar = same shape (N+1); duplicate = identical query (redundant work).
- "The toolbar timings are production timings." They're local and inflated by instrumentation.
- Enabling it via `DEBUG=True` on a shared or production server.
- "It doesn't work for APIs." It does through the browsable API; for pure JSON clients use other tools.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Dev data hides N+1 — seed realistic volumes | Toolbar stores every query per request | ACCESS SHARE only |
| **Medium** | 1M | Toolbar EXPLAIN on a prod-like copy gives realistic plans | — | ACCESS SHARE only |
| **Large** | 100M | Local data can't reproduce the plan; use staging + `pg_stat_statements` | — | — |
| **Massive** | 1B+ | Rely on production observability, not dev tools | — | — |

# Follow-up Questions

1. What's the difference between a "similar" and a "duplicate" query, and how do you fix each?
2. How do you find N+1 queries in a JSON-only API?
3. What do you use in production instead?

# Related Topics

* Module 06 Q35 — `pg_stat_statements`
* Module 06 Q36 — query-count tests in CI
* Module 19 Q6 — tracing a slow query back to its line of code

---

# Question

How do you use Explain() to analyze database query execution plans?

# Why Interviewer Asks This

Senior engineers are expected to *read* a plan, not just generate one. The interviewer wants `QuerySet.explain()` usage, the danger of `ANALYZE` on heavy queries, and the four or five signals in a plan that tell you what to fix.

# Answer

**Spoken answer:** "`QuerySet.explain()` asks the database how it will execute the exact SQL Django generated. On PostgreSQL I usually call `explain(analyze=True, buffers=True)` on a staging copy, which actually runs the query and shows real row counts and timings next to the estimates. Then I look for a few things: a sequential scan on a big table where I expected an index scan; estimated rows wildly different from actual rows, which usually means stale statistics or correlated columns; a sort or hash spilling to disk; and nested loops with a huge number of loops. Each of those points to a fix — an index, `ANALYZE`, a better composite index order, or rewriting the query. I'm careful that `analyze=True` really executes the query."

**The reasoning:**
- `explain()` = plan only (estimates). `explain(analyze=True)` = runs it, actual numbers.
- Options on PostgreSQL: `analyze`, `verbose`, `buffers`, `settings`, `summary`, `wal`, `format='json'|'text'|'yaml'|'xml'`.
- It works on SELECT querysets; for an `update()`/`delete()`, capture the SQL and EXPLAIN it inside a rolled-back transaction.

# Internal ORM Mechanics

`QuerySet.explain(format=None, **options)` clones the query, sets `query.explain_info`, and runs it through the normal compiler. The backend's `explain_query_prefix(format, **options)` validates the options and prepends e.g. `EXPLAIN (ANALYZE true, BUFFERS true)` on PostgreSQL. The plan rows are joined into a string. Because it reuses the compiler, the explained SQL is exactly what your queryset sends — including joins from `select_related`, `ORDER BY` from `Meta.ordering` and the `LIMIT` from slicing. Support for options varies by backend; on SQL Server I take the actual execution plan from SSMS or Query Store instead.

# SQL Generated

```python
qs = Shipment.objects.filter(status='in_transit', carrier_id=42).order_by('-created_at')[:50]
print(qs.explain(analyze=True, buffers=True))
```

```sql
EXPLAIN (ANALYZE true, BUFFERS true)
SELECT "logistics_shipment"."id", "logistics_shipment"."status", "logistics_shipment"."carrier_id", "logistics_shipment"."created_at"
FROM "logistics_shipment"
WHERE ("logistics_shipment"."carrier_id" = 42 AND "logistics_shipment"."status" = 'in_transit')
ORDER BY "logistics_shipment"."created_at" DESC
LIMIT 50;
```

Typical output shape (illustrative):

```text
Limit  (actual rows=50 loops=1)
  ->  Sort  (Sort Method: external merge  Disk: …)          ← spill: no index matches ORDER BY
        ->  Seq Scan on logistics_shipment                 ← full table scan
              Filter: ((carrier_id = 42) AND ((status)::text = 'in_transit'::text))
              Rows Removed by Filter: …                      ← most rows thrown away
Buffers: shared hit=… read=…                                 ← read = disk I/O
```

# Code Example

```python
qs = Shipment.objects.filter(status='in_transit', carrier_id=42).order_by('-created_at')[:50]

print(qs.explain())                                   # estimates only, safe on prod
print(qs.explain(analyze=True, buffers=True))         # executes the query — use on staging
plan = qs.explain(format='json', analyze=True)        # machine-readable, e.g. for CI checks

# Fix suggested by the plan: equality columns first, then the ORDER BY column
class Shipment(models.Model):
    carrier = models.ForeignKey('Carrier', on_delete=models.PROTECT)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=['carrier', 'status', '-created_at'], name='ship_carrier_status_created')]

# After migrating, the plan should read: Limit → Index Scan using ship_carrier_status_created
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub analytics endpoint filtered the ~30k-rows/day metrics table by integration and date range and sorted by timestamp. **T** — It took [fill-in] s at month-end. **A** — `explain(analyze=True, buffers=True)` on staging showed a sequential scan, a disk-spilling sort and estimates off by [fill-in]×. I added a composite index `(integration_id, recorded_at)`, ran `ANALYZE`, and confirmed the new plan was an index scan with no sort node. **R** — the query went from [fill-in] s to [fill-in] ms, and I saved before/after plans in the PR.

# Performance Impact

- `explain()` without analyze is cheap (planning only).
- `analyze=True` costs a full execution — dangerous for heavy queries on production primaries.
- Plans are data-dependent: a plan on a 1K-row dev database tells you little about production.

**Trade-offs / when NOT to use it:**
- Don't tune from dev-sized data — use staging with production-like volume and fresh statistics.
- Don't add indexes based on one plan alone; check write cost and whether `pg_stat_statements` says the query matters.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`explain()` is free." With `analyze=True` it runs the full query.
- "Seq scan is always bad." On small tables or low-selectivity filters, it's the right plan.
- Reading only total time and ignoring estimated vs. actual rows — the most useful signal.
- Forgetting that `Meta.ordering` and slicing change the SQL being explained.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Plans are uninformative — planner prefers seq scans | — | ACCESS SHARE only |
| **Medium** | 1M | Index vs. seq scan choices become real; check selectivity | Sorts may spill past `work_mem` | ACCESS SHARE only |
| **Large** | 100M | Watch partition pruning, parallel workers, bitmap scans | `BUFFERS` read vs. hit matters | ACCESS SHARE; ANALYZE on staging only |
| **Massive** | 1B+ | Plan stability matters — stats targets, extended statistics | — | Use auto_explain sampling in prod |

# Follow-up Questions

1. What does a large gap between estimated and actual rows tell you, and how do you fix it?
2. Why can't you trust a plan from your laptop's database?
3. How would you EXPLAIN an `update()` safely?

# Related Topics

* Module 12 Q24 — checking whether an index is used
* Module 10 Q17 — debugging slow subqueries with EXPLAIN
* Module 19 Q34 — index scans degrading to seq scans

---

# Question

What is the performance implication of fetching unrelated large text fields?

# Why Interviewer Asks This

Checks whether you understand the physical cost of wide rows — disk pages, TOAST/LOB storage, network, decoding, memory — and can propose both a query-level fix and a schema-level one. (Module 06 Q4 covers the `only()`/`defer()` API itself.)

# Answer

**Spoken answer:** "Every column you SELECT has to be read, shipped over the network, decoded into Python and held in memory, even if no one looks at it. For large text or JSON columns that's expensive: on PostgreSQL, values over roughly 2 KB are stored out-of-line in TOAST and usually compressed, so selecting them means extra page reads and decompression for every row. On SQL Server, `NVARCHAR(MAX)` works similarly with LOB pages. On a list endpoint that only shows a title and a status, a `SELECT *` can move a hundred times more data than the page needs. The fix at the query level is `defer()`, `only()` or `values()`; at the schema level, if the blob is rarely read, I move it to a one-to-one side table or object storage."

**The reasoning:**
- Cost is per row × per byte — it scales with both page size and blob size.
- PostgreSQL only detoasts a value when the column is actually output, so *not selecting it* avoids that I/O entirely.
- Serialization layers (DRF, JSON encoding) multiply the cost if the field ends up in responses.

# Internal ORM Mechanics

By default Django selects every concrete column (`get_default_columns()`), so a `TextField`/`JSONField`/`BinaryField` is fetched on every query. The driver materialises each value (psycopg decodes text; Django's `JSONField.from_db_value` runs `json.loads` per row), and the string lives in the instance's `__dict__` until garbage-collected. `defer('body')` removes the column from the SELECT list; the value is only loaded if the attribute is touched later.

# SQL Generated

```python
IntegrationLog.objects.filter(integration_id=9).order_by('-created_at')[:100]
IntegrationLog.objects.filter(integration_id=9).defer('request_payload', 'response_body').order_by('-created_at')[:100]
```

```sql
-- default: drags both blobs (often TOASTed) for 100 rows
SELECT "ops_integrationlog"."id", "ops_integrationlog"."integration_id", "ops_integrationlog"."status_code",
       "ops_integrationlog"."created_at", "ops_integrationlog"."request_payload", "ops_integrationlog"."response_body"
FROM "ops_integrationlog" WHERE "ops_integrationlog"."integration_id" = 9
ORDER BY "ops_integrationlog"."created_at" DESC LIMIT 100;

-- deferred: TOAST is never touched
SELECT "ops_integrationlog"."id", "ops_integrationlog"."integration_id", "ops_integrationlog"."status_code",
       "ops_integrationlog"."created_at"
FROM "ops_integrationlog" WHERE "ops_integrationlog"."integration_id" = 9
ORDER BY "ops_integrationlog"."created_at" DESC LIMIT 100;
```

# Code Example

```python
class IntegrationLog(models.Model):
    integration = models.ForeignKey('Integration', on_delete=models.CASCADE)
    status_code = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(db_index=True)
    request_payload = models.JSONField()        # often several KB
    response_body = models.TextField()          # can be very large

# Query-level fix for list views
class IntegrationLogViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        qs = IntegrationLog.objects.filter(integration_id=self.kwargs['integration_pk'])
        if self.action == 'list':
            qs = qs.defer('request_payload', 'response_body')
        return qs.order_by('-created_at')

# Schema-level fix when blobs are rarely read: vertical split
class IntegrationLogBody(models.Model):
    log = models.OneToOneField(IntegrationLog, on_delete=models.CASCADE, primary_key=True, related_name='body')
    request_payload = models.JSONField()
    response_body = models.TextField()
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub stores request/response payloads for each of its 5+ enterprise integrations for troubleshooting. **T** — The log list endpoint returned [fill-in] KB per page and took [fill-in] ms, though the UI only showed status, time and endpoint. **A** — I deferred both payload columns on the list action, kept them on the detail action, and excluded them from the list serializer. **R** — payload per page dropped from [fill-in] to [fill-in] KB and p95 from [fill-in] to [fill-in] ms; DB buffer reads fell by [fill-in]%.

# Performance Impact

- Disk: TOAST/LOB pages read per row; decompression CPU.
- Network: bytes per row × rows.
- Python: decoding (and `json.loads` for JSON) per row; memory until the objects are freed.
- Cache efficiency: wide rows push useful pages out of the buffer cache.

**Trade-offs / when NOT to use it:**
- Small text columns (a few hundred bytes) aren't worth deferring.
- Vertical splitting adds a JOIN or second query when you *do* need the blob, and another table to migrate and back up.
- Object storage for blobs means losing transactional consistency with the row — design for orphans.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "The database only reads what the app uses." It reads what the SELECT asks for.
- "Compression makes big columns free." It saves disk but adds CPU to decompress every selected value.
- "It doesn't matter on PostgreSQL because of TOAST." TOAST helps only when the column is *not* selected.
- Deferring the blob but leaving it in the list serializer — deferred N+1.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Barely visible | Small | ACCESS SHARE only |
| **Medium** | 1M | List endpoints and exports slow down visibly | Proportional to blob size | ACCESS SHARE only |
| **Large** | 100M | TOAST I/O dominates; table size balloons | Exports can OOM workers | ACCESS SHARE; VACUUM of TOAST tables matters |
| **Massive** | 1B+ | Move blobs out (side table, object storage, archive) | — | Partition logs by time |

# Follow-up Questions

1. How does TOAST work, and when is a value moved out of line?
2. When would you split a blob into a separate one-to-one table?
3. How do you stop a DRF list serializer from touching a deferred field?

# Related Topics

* Module 06 Q4 — `only()` vs `defer()`
* Module 03 Q4 — CharField vs TextField storage
* Module 06 Q5 — deferred-field N+1

---

# Question

How does prefetch_related handle deeply nested relationships?

# Why Interviewer Asks This

Checks whether you can predict the query count of a multi-level lookup, combine `select_related` inside a `Prefetch` to remove levels, and recognise the scaling risks of large `IN` lists at the deeper levels.

# Answer

**Spoken answer:** "For a lookup like `orders__items__product`, Django walks the path one level at a time: it loads the customers, collects their ids and prefetches orders; then collects those order ids and prefetches items; then collects product ids and prefetches products. So it's one query per level, and lookups that share a prefix reuse the earlier level. The cost to watch is the *fan-out*: a page of 50 customers can turn into 5,000 order ids and 50,000 item ids at the next level, so the `IN` lists — and the memory — grow multiplicatively. My two tools are `select_related` inside a `Prefetch` to collapse single-valued hops into the same query, and bounding the top level, by pagination or chunked iteration."

**The reasoning:**
- Queries = 1 + number of distinct levels in all lookup paths.
- Each level uses the keys from the level above — fan-out multiplies `IN` list size.
- A `Prefetch` with `select_related` turns "items, then products" into one query.
- Define a filtered `Prefetch` *before* deeper string lookups that traverse it, so they reuse the filtered set.

# Internal ORM Mechanics

`prefetch_related_objects()` splits each lookup on `__` and processes levels breadth-first, tracking `done_queries` by the prefetch path so a prefix like `orders` is fetched only once. At each level it gathers the objects reached so far (`obj_list`), runs `prefetch_one_level()`, and the next level's `obj_list` becomes the union of all children just fetched. If a level is already cached (e.g. via `select_related` inside the previous level's queryset), Django detects `is_fetched` and skips querying it.

# SQL Generated

```python
Customer.objects.filter(region='EU').prefetch_related(
    Prefetch('orders', queryset=Order.objects.filter(placed_at__gte=since)),
    Prefetch('orders__items', queryset=OrderItem.objects.select_related('product')),
)
```

```sql
SELECT ... FROM "shop_customer" WHERE "shop_customer"."region" = 'EU';

SELECT ... FROM "shop_order"
WHERE ("shop_order"."placed_at" >= '2026-10-01T00:00:00+00:00'::timestamptz AND "shop_order"."customer_id" IN (1, 2, 3));

-- product folded into the items query via select_related: 3 queries, not 4
SELECT "shop_orderitem".*, "shop_product".*
FROM "shop_orderitem"
INNER JOIN "shop_product" ON ("shop_orderitem"."product_id" = "shop_product"."id")
WHERE "shop_orderitem"."order_id" IN (101, 102, 103 /* … */);
```

# Code Example

```python
from django.db.models import Prefetch

recent_orders = Order.objects.filter(placed_at__gte=since).only('id', 'customer_id', 'placed_at', 'total')
items_with_product = OrderItem.objects.select_related('product').only(
    'id', 'order_id', 'quantity', 'product__id', 'product__name', 'product__sku')

customers = (Customer.objects.filter(region='EU')
             .prefetch_related(
                 Prefetch('orders', queryset=recent_orders),          # must come first
                 Prefetch('orders__items', queryset=items_with_product),
             ))

# Bound the fan-out for jobs: prefetch per chunk of customers
for c in customers.iterator(chunk_size=200):
    for o in c.orders.all():
        for i in o.items.all():
            ...
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub compliance report walked integration → endpoints → recent sync runs → errors. **T** — The naive version issued [fill-in] queries; the first prefetch fix brought that to four, but the error-level `IN` list hit [fill-in] ids and the worker used [fill-in] GB. **A** — I folded `endpoint` into the runs query with `select_related`, filtered runs to the reporting window in a `Prefetch`, and iterated integrations with `iterator(chunk_size=200)` so each chunk's tree stayed bounded. **R** — memory flat at [fill-in] MB, runtime from [fill-in] to [fill-in] min.

# Performance Impact

- Queries: constant per level — good.
- `IN` list size and memory: multiplicative fan-out — the real limit.
- SQL Server's ~2,100-parameter limit can make deep prefetches fail outright; chunk the root set.

**Trade-offs / when NOT to use it:**
- If you only need aggregates at the deepest level, annotate them on the parent level instead of loading the whole tree.
- For reporting over huge trees, a single SQL query with GROUP BY (or a reporting view) beats building millions of objects.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Nested prefetch is one query per object at each level." It's one per level.
- "Prefetch order doesn't matter." A filtered `Prefetch` must be declared before string lookups that traverse it.
- Prefetching four levels for a page that displays two.
- Not bounding the root queryset in jobs — the tree for the whole table ends up in memory.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | 1 query per level | Whole tree fits easily | ACCESS SHARE only |
| **Medium** | 1M | Fan-out makes deeper `IN` lists large | Paginate the root | ACCESS SHARE only |
| **Large** | 100M | Chunk the root with `iterator(chunk_size=...)` | Flat per chunk | ACCESS SHARE; consider replicas |
| **Massive** | 1B+ | Aggregate in SQL / reporting tables instead of object trees | — | Warehouse / replicas |

# Follow-up Questions

1. How many queries does `prefetch_related('a__b', 'a__c')` run?
2. How would you remove one level of a nested prefetch?
3. What breaks first as nested prefetch data grows — query count, `IN` list size or memory?

# Related Topics

* Module 06 Q2 — when and how prefetch queries run
* Module 06 Q3 — the `Prefetch` object
* Module 19 Q12 — debugging slow prefetches on large datasets

---

# Question

What are the limitations of select_related on many-to-many relationships?

# Why Interviewer Asks This

Confirms you understand *why* Django won't JOIN multi-valued relations, how prefetch handles M2M (including the through-table JOIN), and what you can do when you need related data in a single query.

# Answer

**Spoken answer:** "`select_related` simply doesn't work on many-to-many or reverse foreign keys — Django raises a `FieldError`. That's deliberate: a JOIN to a many-valued relation returns one row per related object, so an article with five tags would come back five times, and Django would have to fold those rows back into one object — which it doesn't do, because it has no identity map. So for M2M you use `prefetch_related`, which runs one extra query that joins the through table to the target table and filters by the parent ids. If you need the related data in the same query — say for a read-only list — on PostgreSQL I'd use an `ArrayAgg` annotation. And with an explicit through model, I can query the through model itself with `select_related` on both sides."

**The reasoning:**
- `select_related` = single-valued relations only.
- M2M prefetch = one query joining `through` + `target`, filtered by `through.source_id IN (...)`.
- You *can* `select_related` inside the M2M prefetch on the target's own FKs.
- With a custom through model, the through model is a normal model with two FKs.

# Internal ORM Mechanics

`select_related()` validates its lookups in the compiler's `get_related_selections()`; any path segment that isn't a forward FK/OneToOne or reverse OneToOne raises `FieldError: Invalid field name(s) given in select_related`. For M2M, `ManyToManyDescriptor`'s manager builds the prefetch queryset as `Tag.objects.filter(article_tags__article_id__in=...)` — a JOIN to the through table — and adds an extra select `_prefetch_related_val_article_id` so each returned tag can be assigned to the right article(s).

# SQL Generated

```python
Article.objects.select_related('tags')          # FieldError
Article.objects.prefetch_related(Prefetch('tags', queryset=Tag.objects.select_related('category')))
```

```text
django.core.exceptions.FieldError: Invalid field name(s) given in select_related: 'tags'. Choices are: author
```

```sql
SELECT "cms_article"."id", "cms_article"."title", "cms_article"."author_id" FROM "cms_article";

SELECT ("cms_article_tags"."article_id") AS "_prefetch_related_val_article_id",
       "cms_tag"."id", "cms_tag"."name", "cms_tag"."category_id",
       "cms_tagcategory"."id", "cms_tagcategory"."label"
FROM "cms_tag"
INNER JOIN "cms_article_tags" ON ("cms_tag"."id" = "cms_article_tags"."tag_id")
INNER JOIN "cms_tagcategory" ON ("cms_tag"."category_id" = "cms_tagcategory"."id")
WHERE "cms_article_tags"."article_id" IN (1, 2, 3);
```

# Code Example

```python
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Prefetch, Q

# 1) Standard: prefetch the M2M (2 queries), JOIN the tag's own FK inside it
articles = Article.objects.select_related('author').prefetch_related(
    Prefetch('tags', queryset=Tag.objects.select_related('category')))

# 2) Read-only list on PostgreSQL: one query, tag names as an array
rows = (Article.objects
        .annotate(tag_names=ArrayAgg('tags__name', distinct=True, filter=Q(tags__isnull=False), default=[]))
        .values('id', 'title', 'tag_names'))

# 3) Explicit through model: query it directly with select_related on both FKs
class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    added_by = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)

links = ArticleTag.objects.filter(article__in=page_ids).select_related('tag', 'added_by')
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub integrations are tagged with business domains and owning teams (both M2M). **T** — A teammate tried `select_related('tags')`, got a `FieldError`, then "fixed" it with `values('id', 'name', 'tags__name')`, which returned [fill-in]× duplicated rows and wrong counts on the dashboard. **A** — I used `prefetch_related` for the API (instances needed) and an `ArrayAgg` annotation for the CSV export (read-only, one query). **R** — correct counts, [fill-in] queries per page, export time from [fill-in] to [fill-in] s.

# Performance Impact

- M2M prefetch: one query per M2M lookup, always joining the through table — index both through-table FK columns (Django does by default).
- `ArrayAgg`: one query, but GROUP BY over a JOIN; combining two such aggregates over different relations multiplies rows unless you use `distinct=True` or subqueries.

**Trade-offs / when NOT to use it:**
- `ArrayAgg`/`JSONBAgg` are PostgreSQL-only and return raw values, not instances.
- Querying the through model directly is great for reports but bypasses the M2M manager API.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "You can `select_related` a ManyToManyField." `FieldError`.
- "M2M prefetch doesn't JOIN anything." It joins the through table.
- Working around it with `values('tags__name')` and getting row explosion.
- "Prefetch can't use `select_related`." It can — on the *target* model's FKs inside a `Prefetch`.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Prefetch is trivially fast | Small | ACCESS SHARE only |
| **Medium** | 1M | Through-table indexes on both FKs matter | Proportional to links per page | ACCESS SHARE only |
| **Large** | 100M | Through tables are often the biggest table — composite PK/unique `(a_id, b_id)` | Use aggregates for read-only lists | ACCESS SHARE only |
| **Massive** | 1B+ | Denormalise tags (ArrayField + GIN) or move to a search index | — | — |

# Follow-up Questions

1. Why doesn't Django fold JOINed multi-valued rows back into objects?
2. How do you show tag names for 1,000 articles in a single query?
3. When would you query a through model directly?

# Related Topics

* Module 07 Q3 — M2M join tables
* Module 07 Q23 — prefetching through-model attributes
* Module 09 Q23 — annotating with lists of related values

---

# Question

How do you optimize bulk inserts of millions of rows in Django?

# Why Interviewer Asks This

Tests whether you can move beyond `bulk_create` and reason about the whole pipeline — memory on the Python side, batch and transaction size, index and constraint maintenance, WAL/replication, and native bulk-load paths like `COPY`.

# Answer

**Spoken answer:** "At millions of rows, the ORM is no longer the bottleneck you optimise around — the pipeline is. First, I never build a million model instances in memory; I stream the source and insert in batches with `bulk_create(batch_size=...)`, committing per batch so locks and WAL stay bounded. Second, if it's PostgreSQL and the volume is really large, I skip `INSERT` and use `COPY` through the psycopg cursor, which is the fastest path into Postgres. On SQL Server the equivalent is a bulk-load path, like pyodbc's `fast_executemany` or `BULK INSERT`. Third, I think about indexes: every secondary index is updated per row, so for a one-off backfill into an empty table I'd create indexes after loading. And for all-or-nothing loads, I load into a staging table, validate, and then swap or `INSERT ... SELECT`."

**The reasoning:**
- Python memory: generators + `islice`, never a giant list.
- Round-trips: batching (`bulk_create`) or streaming (`COPY`).
- DB work per row: index maintenance, constraints, triggers, WAL.
- Transaction size: per-batch commits vs. a staging table when atomicity matters.

# Internal ORM Mechanics

`bulk_create` builds one multi-row `INSERT` per batch through `SQLInsertCompiler`, with one bound parameter per field per row, plus `RETURNING` for PKs where supported — that's parameter binding, statement parsing and planning per batch. `COPY ... FROM STDIN` streams rows in the COPY protocol with no per-statement parsing, which is why it's much faster for large volumes. Django's `connection.cursor()` returns a `CursorWrapper` that proxies unknown attributes to the driver cursor, so psycopg 3's `cursor.copy()` is reachable directly.

# SQL Generated

```sql
-- bulk_create(batch_size=5000): one statement per batch
INSERT INTO "iot_reading" ("device_id", "value", "taken_at")
VALUES (1, 21.4, '2026-11-26T00:00:00+00:00'::timestamptz), (1, 21.6, '...'), /* … 5,000 rows */
RETURNING "iot_reading"."id";

-- COPY: one streaming command for the whole load
COPY "iot_reading" ("device_id", "value", "taken_at") FROM STDIN;
```

# Code Example

```python
from itertools import islice
from django.db import connection, transaction

def chunked(iterable, size):
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch

# Option 1 — ORM, streamed and batched
def load_readings_orm(rows, batch=5000):
    for chunk in chunked(rows, batch):
        with transaction.atomic():
            Reading.objects.bulk_create(
                [Reading(device_id=r['device_id'], value=r['value'], taken_at=r['ts']) for r in chunk],
                batch_size=batch)

# Option 2 — PostgreSQL COPY via psycopg 3 (fastest)
def load_readings_copy(rows):
    table = Reading._meta.db_table
    with transaction.atomic(), connection.cursor() as cur:
        with cur.copy(f'COPY "{table}" ("device_id", "value", "taken_at") FROM STDIN') as copy:
            for r in rows:                               # rows can be a generator
                copy.write_row((r['device_id'], r['value'], r['ts']))
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub backfilled [fill-in] historical analytics rows from the MSSQL ODS into PostgreSQL when we launched the analytics dashboard (which then grows by ~30k rows/day). **T** — A first attempt with `save()` per row was projected to take [fill-in] hours and grew memory unboundedly. **A** — I streamed rows from the ODS cursor via our MSSQL router alias, wrote them to PostgreSQL with `COPY` in [fill-in]-row transactions, created the secondary indexes after the load, and then ran `ANALYZE`. **R** — the backfill finished in [fill-in] minutes with flat memory and replica lag under [fill-in] s.

# Performance Impact

- `save()` per row < `bulk_create` batches < `COPY` — each step removes per-row round-trips and parsing.
- Index maintenance per row is usually the dominant DB cost at scale.
- WAL volume drives replica lag; huge single transactions also delay VACUUM.

**Trade-offs / when NOT to use it:**
- `COPY` bypasses all model logic — no defaults computed in Python, no validation, no signals. Validate upstream.
- Dropping indexes for a load is only sane on a table no one else is using.
- Per-batch commits mean a failure leaves a partial load — make the job idempotent (natural keys, upserts) or use a staging table.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Just call `bulk_create` with all million objects." Memory blows up, and one giant statement/transaction is slow and risky.
- "One transaction for the whole load is safest." It maximises lock time, WAL burst and rollback cost.
- Ignoring index and trigger cost — then wondering why throughput drops as the table grows.
- Forgetting `ANALYZE` after a bulk load, so the planner uses stale statistics.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | `bulk_create` in one call | Trivial | ROW EXCLUSIVE |
| **Medium** | 1M | Batches of ~1–5K, per-batch transactions | Bounded by batch | ROW EXCLUSIVE; short transactions |
| **Large** | 100M | `COPY`, indexes built after, `ANALYZE` | Streamed | ROW EXCLUSIVE; monitor WAL and replica lag |
| **Massive** | 1B+ | Parallel `COPY` per partition; load into new partitions and attach | Streamed | ATTACH PARTITION; throttle replication impact |

# Follow-up Questions

1. Why is `COPY` faster than a multi-row INSERT?
2. How do you make a batched load idempotent if it fails halfway?
3. Would you drop indexes before a load on a live table? Why not?

# Related Topics

* Module 06 Q8 — `bulk_create()` internals and PK return
* Module 19 Q10 — WAL generation from bulk operations
* Module 16 Q10 — write-heavy workloads

---

# Question

How do you perform batch deletions without violating database constraints?

# Why Interviewer Asks This

Builds on Q13: once you batch deletes or bypass the Collector, foreign keys start biting. The interviewer wants delete ordering, how PROTECT/RESTRICT behave, PostgreSQL's deferred FK checks, and how to keep each batch consistent.

# Answer

**Spoken answer:** "The rule is: children before parents, inside the same transaction. When I use `queryset.delete()`, Django's Collector already orders the deletes by dependency and applies `on_delete`, so CASCADE and SET_NULL just work, while PROTECT raises `ProtectedError` and RESTRICT raises `RestrictedError` unless the restricted object is being deleted via another cascade. Problems appear when I bypass that — raw SQL, `_raw_delete`, or models with `DO_NOTHING` — because Django creates foreign keys without `ON DELETE` rules, so the database refuses to orphan rows. On PostgreSQL, Django's FKs are `DEFERRABLE INITIALLY DEFERRED`, which means the check happens at commit; so each batch transaction must contain the parent *and* all its dependents. In practice: pick a batch of parent ids, delete grandchildren, children, then parents, commit, repeat."

**The reasoning:**
- Consistency boundary = one batch = one transaction containing the whole subtree.
- PROTECT/RESTRICT are business rules — decide explicitly what to do with protected rows; don't just catch the error.
- `DO_NOTHING` means *you* own the cleanup; the DB will raise `IntegrityError` at commit.

# Internal ORM Mechanics

The Collector builds a dependency graph of models and sorts it so dependent rows are deleted first (`Collector.sort()`), then runs field updates (SET_NULL/SET_DEFAULT), fast deletes and instance deletes in one `atomic()` block. PROTECT is raised while collecting; RESTRICT is checked after collection, so it allows deletion when the restricted object is reachable via a CASCADE from the same delete. In PostgreSQL, Django's schema editor creates FKs with `DEFERRABLE INITIALLY DEFERRED`, so constraint checks run at `COMMIT`; on MySQL and SQL Server checks are immediate, so statement order matters inside the transaction too.

# SQL Generated

```python
with transaction.atomic():
    Attachment.objects.filter(ticket__project_id__in=ids).delete()
    Ticket.objects.filter(project_id__in=ids).delete()
    Project.objects.filter(id__in=ids).delete()
```

```sql
BEGIN;
DELETE FROM "helpdesk_attachment"
WHERE "helpdesk_attachment"."ticket_id" IN (SELECT U0."id" FROM "helpdesk_ticket" U0 WHERE U0."project_id" IN (11, 12));
DELETE FROM "helpdesk_ticket" WHERE "helpdesk_ticket"."project_id" IN (11, 12);
DELETE FROM "pm_project" WHERE "pm_project"."id" IN (11, 12);
COMMIT;   -- deferred FK checks run here on PostgreSQL
```

# Code Example

```python
from django.db import transaction
from django.db.models import ProtectedError

def purge_archived_projects(batch=200):
    while True:
        ids = list(Project.objects.filter(status='archived').order_by('pk').values_list('pk', flat=True)[:batch])
        if not ids:
            break
        try:
            with transaction.atomic():
                # explicit order for large subtrees: deepest first, so each step has little left to cascade
                Attachment.objects.filter(ticket__project_id__in=ids).delete()
                Ticket.objects.filter(project_id__in=ids).delete()
                Project.objects.filter(id__in=ids).delete()
        except ProtectedError as exc:
            # e.g. Invoice → Project is PROTECT: park these and continue
            blocked = {obj.project_id for obj in exc.protected_objects}
            Project.objects.filter(id__in=blocked).update(status='archived_blocked')
```

# Production Scenario

**From experience (STAR):** **S** — Decommissioning an integration in PNI Hub meant removing endpoints, credentials references, sync runs and logs, but audit records had to stay. **T** — A raw-SQL cleanup script failed with FK violations at commit and left operators unsure what had been deleted. **A** — I rewrote it with the ORM, batching by integration id, deleting the subtree deepest-first in one transaction per batch, and made the audit FK `PROTECT` so the job explicitly archived audit rows first. **R** — the cleanup became repeatable and idempotent; [fill-in] integrations were decommissioned with zero FK errors.

# Performance Impact

- Each batch holds row locks on the whole subtree until commit — keep batches small on hot tables.
- Subquery deletes (`ticket__project_id__in`) need indexes on every FK in the path.
- Deferred FK checks on PostgreSQL add work at commit proportional to rows changed.

**Trade-offs / when NOT to use it:**
- If the model graph is complex, let `queryset.delete()` collect for you on small batches — correctness beats hand-ordering.
- If you're deleting whole time ranges, dropping partitions avoids FK work entirely (with partition-aware FKs).

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Disable FK constraints during the delete." That's how you create orphans permanently.
- "Delete parents first, the DB will cascade." Not with Django-created FKs in 5.x — no `ON DELETE CASCADE` at the DB level.
- "PROTECT and RESTRICT are the same." RESTRICT allows the delete if the object is also being removed via another CASCADE path.
- Committing children and parents in different transactions — a crash in between leaves inconsistent data.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Plain `delete()` with the Collector | Trivial | Row locks until commit |
| **Medium** | 1M | Batches of parents; explicit deepest-first fast deletes | Bounded | Row locks per subtree batch |
| **Large** | 100M | FK indexes everywhere; throttle batches | Flat | Short transactions; watch lock waits from OLTP |
| **Massive** | 1B+ | Partition-aligned retention to avoid row-level deletes | — | DETACH/DROP PARTITION |

# Follow-up Questions

1. What does `DEFERRABLE INITIALLY DEFERRED` change for your batch design?
2. How would you handle rows protected by `on_delete=PROTECT` in a bulk cleanup?
3. When is `DO_NOTHING` a reasonable choice?

# Related Topics

* Module 06 Q13 — Django's delete Collector
* Module 07 Q6 — on_delete options
* Module 07 Q34 — risks of DO_NOTHING

---

# Question

What is the database cost of order_by('?') for random row selection?

# Why Interviewer Asks This

A classic trap: `order_by('?')` looks innocent and works fine in development. The interviewer wants to hear why it's a full scan plus sort, and which alternative you'd pick given the data shape.

# Answer

**Spoken answer:** "`order_by('?')` becomes `ORDER BY RANDOM()` on PostgreSQL, `RAND()` on MySQL, `NEWID()` on SQL Server. To honour it, the database has to generate a random value for *every* row that matches the filter and then sort them all — even if I only want one. The `LIMIT` doesn't let it skip work; at best it uses a top-N heap sort to save memory. So the cost grows with the table. It's fine for a few thousand rows; on millions, I'd use an alternative: pick random ids from a cached id list, use `TABLESAMPLE` on PostgreSQL when approximate sampling is fine, or keep an indexed random-key column and seek into it."

**The reasoning:**
- Cost = full scan of matching rows + random() per row + sort. LIMIT doesn't avoid the scan.
- No index can help, because the sort key is computed at query time.
- Pick the alternative by requirement: exact uniform randomness, approximate sampling, or "random-ish" featured items.

# Internal ORM Mechanics

`order_by('?')` adds a `Random()` expression to the ordering; the compiler renders it with the backend's random function (`RANDOM()` on PostgreSQL/SQLite, `RAND()` on MySQL, `NEWID()` on SQL Server). Combined with slicing it becomes `ORDER BY RANDOM() ASC LIMIT n`. Nothing about it is index-aware.

# SQL Generated

```python
Article.objects.filter(status='published').order_by('?')[:5]
```

```sql
SELECT "cms_article"."id", "cms_article"."title", ...
FROM "cms_article"
WHERE "cms_article"."status" = 'published'
ORDER BY RANDOM() ASC
LIMIT 5;

-- PostgreSQL approximate alternative: samples ~1% of pages, no full scan
SELECT "id" FROM "cms_article" TABLESAMPLE SYSTEM (1) WHERE "status" = 'published' LIMIT 5;
```

# Code Example

```python
import random
from django.core.cache import cache

# 1) Small tables: order_by('?') is fine
Tip.objects.order_by('?').first()

# 2) Uniform sample from a cached id list (refresh the list on a schedule)
def random_published(n=5):
    ids = cache.get_or_set('published_article_ids',
                           lambda: list(Article.objects.filter(status='published').values_list('id', flat=True)),
                           timeout=600)
    picked = random.sample(ids, k=min(n, len(ids)))
    return list(Article.objects.filter(id__in=picked))

# 3) Indexed random key: seek instead of sort
class Article(models.Model):
    ...
    random_key = models.FloatField(default=random.random, db_index=True)

def random_article():
    r = random.random()
    return (Article.objects.filter(status='published', random_key__gte=r).order_by('random_key').first()
            or Article.objects.filter(status='published').order_by('random_key').first())   # wrap around
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub data-quality job spot-checked a random sample of synced records against the source system each night. **T** — It used `order_by('?')[:500]` over a table of [fill-in] rows and took [fill-in] s, all spent scanning and sorting. **A** — Because the check only needed an approximate sample, I switched to a raw `TABLESAMPLE SYSTEM` query on PostgreSQL returning ids, then loaded those rows with the ORM. **R** — the sampling step went from [fill-in] s to [fill-in] ms with no change in what the check caught.

# Performance Impact

- O(N) scan + O(N log k) top-N sort for N matching rows.
- CPU and temp memory scale with table size; can spill to disk.
- The cached-id-list approach moves cost to a periodic job and Redis memory.

**Trade-offs / when NOT to use it:**
- `TABLESAMPLE SYSTEM` is page-level and clustered — not uniform per row; `BERNOULLI` is per row but scans more.
- Random-key columns give slight bias around gaps and need a default on new rows.
- Cached id lists can be stale — fine for "featured", not for "fair lottery".

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`LIMIT 1` makes it fast." It still computes and sorts all matching rows.
- "Add an index on the column." No index helps a sort key computed at query time.
- "Pick a random id between min and max." Gaps from deletes make it biased and can miss entirely.
- Using `count()` + random `OFFSET` — two queries, and OFFSET still walks the rows.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | `order_by('?')` is fine | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Noticeably slow per call; avoid on hot paths | Sort memory | ACCESS SHARE only |
| **Large** | 100M | Unacceptable; use sampling or indexed random key | Temp files on disk | ACCESS SHARE only |
| **Massive** | 1B+ | Pre-computed samples, `TABLESAMPLE`, or search engine random scoring | — | — |

# Follow-up Questions

1. Why can't an index make `ORDER BY RANDOM()` fast?
2. How would you pick a uniformly random row from 100M rows?
3. What's the difference between `TABLESAMPLE SYSTEM` and `BERNOULLI`?

# Related Topics

* Module 06 Q22 — why OFFSET is slow
* Module 06 Q24 — raw SQL safely
* Module 16 Q11 — caching read-heavy workloads

---

# Question

How do you implement fast pagination without using OFFSET?

# Why Interviewer Asks This

Pagination is where large-table performance problems show up first. The interviewer wants keyset (seek/cursor) pagination: why OFFSET degrades, how keyset works with a unique tie-breaker and a matching index, and what you give up.

# Answer

**Spoken answer:** "With `OFFSET`, the database still has to read and throw away every row before the page — page 10,000 reads 500,000 rows to return 50 — so deep pages get slower and slower, and if rows are inserted while someone pages, they see duplicates or miss rows. Keyset pagination fixes both: instead of 'skip N', I say 'give me the next 50 rows after the last one I saw', using `WHERE (created_at, id) < (last_created_at, last_id) ORDER BY created_at DESC, id DESC LIMIT 50`. With a composite index on those columns that's an index seek, so every page costs the same. The trade-offs are that you can't jump to page 37, and the ordering must be deterministic — hence the `id` tie-breaker. In DRF, `CursorPagination` implements this for you."

**The reasoning:**
- OFFSET cost ∝ page depth; keyset cost ∝ page size.
- Keyset is stable under concurrent inserts.
- Needs: deterministic ordering (unique tie-breaker), an index matching the ORDER BY, and an opaque cursor.
- Also avoids `COUNT(*)` for "page X of Y".

# Internal ORM Mechanics

Django has no public row-value comparison for filters, so the seek condition is written as `Q(created_at__lt=ts) | Q(created_at=ts, id__lt=pk)`. Adding a redundant `created_at__lte=ts` gives the planner a simple range to drive the index scan. Slicing `[:50]` becomes `LIMIT 50` without OFFSET. DRF's `CursorPagination` encodes the position (value of the first ordering field, plus an offset for ties) in a base64 cursor and builds a similar filter.

# SQL Generated

```sql
-- OFFSET: reads and discards 500,000 rows first
SELECT ... FROM "audit_auditevent" ORDER BY "created_at" DESC, "id" DESC LIMIT 50 OFFSET 500000;

-- Keyset: index seek straight to the next page
SELECT "audit_auditevent"."id", "audit_auditevent"."actor_id", "audit_auditevent"."action", "audit_auditevent"."created_at"
FROM "audit_auditevent"
WHERE ("audit_auditevent"."created_at" <= '2026-11-20T10:00:00+00:00'::timestamptz
       AND ("audit_auditevent"."created_at" < '2026-11-20T10:00:00+00:00'::timestamptz
            OR ("audit_auditevent"."created_at" = '2026-11-20T10:00:00+00:00'::timestamptz AND "audit_auditevent"."id" < 98765)))
ORDER BY "audit_auditevent"."created_at" DESC, "audit_auditevent"."id" DESC
LIMIT 50;
```

# Code Example

```python
from django.db.models import Q
from rest_framework.pagination import CursorPagination

class AuditEvent(models.Model):
    actor = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    action = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=['-created_at', '-id'], name='audit_created_id_idx')]

def audit_page(cursor=None, size=50):
    qs = AuditEvent.objects.order_by('-created_at', '-id')
    if cursor:
        ts, pk = cursor
        qs = qs.filter(created_at__lte=ts).filter(Q(created_at__lt=ts) | Q(created_at=ts, id__lt=pk))
    rows = list(qs[:size])
    next_cursor = (rows[-1].created_at, rows[-1].id) if len(rows) == size else None
    return rows, next_cursor

# DRF: the same idea, built in
class AuditCursorPagination(CursorPagination):
    page_size = 50
    ordering = '-created_at'      # immutable, high-cardinality field
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub's audit-trail API (who changed which integration setting) is used by admins and by an external compliance tool that pages through everything. **T** — With `PageNumberPagination`, deep pages took [fill-in] s and the tool occasionally reported duplicate events while new ones were being written. **A** — I switched the endpoint to `CursorPagination` ordered by `-created_at`, added a matching index, and dropped the total-count field the tool didn't need. **R** — every page now returns in about [fill-in] ms regardless of depth, and duplicates disappeared.

# Performance Impact

- OFFSET: O(offset + limit) rows read per page, plus `COUNT(*)` for page totals.
- Keyset: O(limit) with an index seek; no count needed.

**Trade-offs / when NOT to use it:**
- No random page access ("jump to page 37") and no exact total without a separate count.
- Ordering by a mutable or low-cardinality column breaks cursor stability.
- Admin-style UIs over small, filtered sets are fine with OFFSET — don't over-engineer.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "OFFSET is fast with an index." The index still has to be walked past the skipped rows.
- Keyset on `created_at` alone — duplicate timestamps cause skipped or repeated rows; add a unique tie-breaker.
- No index matching the ORDER BY — keyset then degrades to a sort.
- Exposing raw ids/timestamps as the cursor without encoding or validating it.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | OFFSET is fine | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Deep OFFSET pages noticeably slow | — | ACCESS SHARE only |
| **Large** | 100M | Keyset mandatory for APIs and exports | — | ACCESS SHARE only |
| **Massive** | 1B+ | Keyset within a partition (e.g. per month); prune by date | — | Replicas for exports |

# Follow-up Questions

1. Why does keyset pagination need a unique tie-breaker column?
2. How does DRF's `CursorPagination` handle non-unique ordering values?
3. How would you show "total results" with keyset pagination?

# Related Topics

* Module 15 Q27 — risks of `select_for_update` with pagination
* Module 12 Q6 — composite index column order
* Module 06 Q29 — chunking with PK ranges

---

# Question

How does values() affect the generation of model instances?

# Why Interviewer Asks This

A mechanism question about what the ORM *skips* when you ask for dicts — and the practical consequences: what still works (converters), what doesn't (methods, `get_FOO_display`, signals), and when that trade is worth it. (Q6 compares `values()` with `values_list()`.)

# Answer

**Spoken answer:** "`values()` changes what Django builds from each row. Normally every row goes through `Model.from_db()`, which creates an instance with its `_state`, sets every field, and sends the `post_init` signal. With `values()`, Django swaps in a different iterator that just zips column names and values into a dict — no model class involved. Field converters still run, so JSON is still decoded and dates are still timezone-aware. What you lose is behaviour: no methods, no properties, no `get_status_display()`, no `save()`, no lazy relations. So it's my default for read-only work — exports, aggregates, building API payloads in jobs — and I keep instances where business logic lives on the model."

**The reasoning:**
- Skipped: `Model.__init__`/`from_db`, `ModelState`, descriptors, `post_init` receivers, deferred-loading machinery.
- Kept: SQL compilation, field converters (`from_db_value`), timezone handling.
- Relations: `values('author__name')` adds a JOIN and returns the value directly; there are no related objects to lazy-load (so no hidden N+1).

# Internal ORM Mechanics

`values()` sets `_iterable_class = ValuesIterable`. `ValuesIterable.__iter__` gets the compiler, builds the list of names (`query.extra_select`, `values_select`, `annotation_select`) and yields `dict(zip(names, row))` for each row from `compiler.results_iter()`. `results_iter` applies converters from `get_converters()` regardless of iterable class. `ModelIterable`, by contrast, calls `model_cls.from_db(db, init_list, row[...])`, populates `select_related` objects via `RelatedPopulator`, and attaches annotations as attributes.

# SQL Generated

```python
Invoice.objects.filter(status='overdue').values('id', 'number', 'amount', 'customer__name')
```

```sql
SELECT "billing_invoice"."id", "billing_invoice"."number", "billing_invoice"."amount", "crm_customer"."name"
FROM "billing_invoice"
INNER JOIN "crm_customer" ON ("billing_invoice"."customer_id" = "crm_customer"."id")
WHERE "billing_invoice"."status" = 'overdue';
```

# Code Example

```python
inv = Invoice.objects.filter(status='overdue').first()
inv.get_status_display()          # works: model instance
inv.days_overdue                  # works: @property on the model

row = Invoice.objects.filter(status='overdue').values('id', 'status', 'amount', 'issued_on').first()
row['amount']                     # Decimal('120.00') — converters still applied
row['issued_on']                  # datetime.date(...)
# row.get_status_display()        # AttributeError — it's a dict

# Getting display labels without instances
STATUS_LABELS = dict(Invoice.Status.choices)
rows = [{**r, 'status_label': STATUS_LABELS[r['status']]}
        for r in Invoice.objects.values('id', 'status', 'amount').iterator(chunk_size=5000)]
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub reporting job generated a daily CSV of integration activity for business stakeholders. **T** — It instantiated [fill-in] model objects and a `post_init` receiver (used for change tracking) ran for each one, so the job took [fill-in] minutes. **A** — Since the job was read-only, I switched to `values()` with explicit columns across the joins plus `iterator(chunk_size=5000)`, mapping choice labels from a dict. **R** — runtime dropped from [fill-in] to [fill-in] and the change-tracking receiver no longer ran for read-only work.

# Performance Impact

- Python CPU: dict creation is much cheaper than full instance construction (+ signals).
- Memory: a dict per row vs. instance `__dict__` + `_state` per row.
- DB cost: unchanged for the same columns.

**Trade-offs / when NOT to use it:**
- Business logic in model methods/properties → you'd duplicate it for dicts.
- Code that later calls `save()` or follows relations needs instances.
- Mixed codebases where some callers expect instances — returning dicts from a shared manager method surprises people.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`values()` returns raw database values." Converters still run — you get Python types.
- "`values()` makes the SQL faster." The SQL is the same for the same columns; the savings are in Python.
- "You can still call model methods." It's a dict.
- Forgetting that `values()` across a multi-valued relation returns one dict per related row.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Not worth changing working code | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Clear CPU win for read-only jobs | Dicts << instances | ACCESS SHARE only |
| **Large** | 100M | `values()` + `iterator(chunk_size=...)` to stream | Flat | ACCESS SHARE; server-side cursor |
| **Massive** | 1B+ | Aggregate in SQL; export with `COPY TO` | — | Replicas |

# Follow-up Questions

1. Do field converters run with `values()`? Why does it matter for JSONField?
2. What happens to `select_related` when you call `values()`?
3. How do you get choice display labels without model instances?

# Related Topics

* Module 06 Q6 — `values()` vs `values_list()`
* Module 17 Q20 — how rows become instances (`from_db`)
* Module 06 Q33 — custom iterables for fast parsing

---

# Question

How do you run raw SQL queries without bypassing Django's security filters?

# Why Interviewer Asks This

Raw SQL is a security and correctness hazard. The interviewer expects parameter binding, the identifier-whitelisting problem, and — the senior part — awareness that raw SQL silently skips the *row-level* filters your managers and permission layer apply (tenant scoping, soft delete, RBAC).

# Answer

**Spoken answer:** "Two layers of protection get bypassed with raw SQL, and I deal with both. The first is SQL injection: I always pass values as parameters — `Model.objects.raw(sql, params)` or `cursor.execute(sql, params)` — so the driver binds them; I never format user input into the string. Identifiers like column names can't be parameters, so for a user-chosen sort column I map it through a whitelist and quote it with `connection.ops.quote_name`. The second, which people forget, is the *application* filters: custom managers that hide soft-deleted rows, tenant scoping, RBAC restrictions. Raw SQL doesn't go through those, so I re-apply them explicitly in the WHERE clause — or better, keep the ORM for scoping and only use raw SQL for the piece the ORM can't express."

**The reasoning:**
- Values → always parameters (`%s` placeholders, a list/tuple of params).
- Identifiers → whitelist + `quote_name`.
- Row-level policy → re-apply explicitly; raw SQL ignores managers.
- Prefer ORM escape hatches first: `RawSQL` in annotations, `Func`, custom lookups.

# Internal ORM Mechanics

`Manager.raw(raw_query, params)` returns a `RawQuerySet`; Django passes the SQL and params unchanged to `cursor.execute()`, and the driver does the binding. It routes via `router.db_for_read()` and maps columns to model fields by name — the primary key must be selected. It does **not** use the model's default manager filters, because there is no queryset to filter. `connection.cursor()` gives a `CursorWrapper` on the `default` alias (use `connections['alias']` for others); with `params` provided, a literal `%` in the SQL must be written as `%%`.

# SQL Generated

```python
Ticket.objects.raw(sql, [tenant_id, f'%{term}%'])
```

```sql
-- what Django sends; the driver binds the two parameters safely
SELECT id, title, priority, created_at
FROM helpdesk_ticket
WHERE tenant_id = %s AND deleted_at IS NULL AND title ILIKE %s
ORDER BY "created_at" DESC
LIMIT 100;
```

# Code Example

```python
from django.db import connection, connections

SORTABLE = {'created': 'created_at', 'priority': 'priority'}      # identifier whitelist

def search_tickets(user, term, sort='created'):
    column = connection.ops.quote_name(SORTABLE.get(sort, 'created_at'))
    sql = f"""
        SELECT id, title, priority, created_at
        FROM helpdesk_ticket
        WHERE tenant_id = %s              -- re-applied tenant scoping
          AND deleted_at IS NULL          -- re-applied soft-delete filter
          AND title ILIKE %s
        ORDER BY {column} DESC
        LIMIT 100
    """
    return list(Ticket.objects.raw(sql, [user.tenant_id, f'%{term}%']))

# NEVER: f"... WHERE title ILIKE '%{term}%'"   → injection

# Reporting query on a secondary database alias
with connections['ods'].cursor() as cur:
    cur.execute('SELECT plant_code, SUM(qty) FROM dbo.shipments WHERE ship_date >= %s GROUP BY plant_code', [since])
    rows = cur.fetchall()
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub reads reporting data from the MSSQL ODS through a custom router alias, and some queries use SQL Server-specific features the ORM can't express. **T** — An early version built the WHERE clause with string formatting from API filters, and it skipped the RBAC restriction that limited users to their business units. **A** — I rewrote it with bound parameters, a whitelist for sortable columns, and a helper that always appends the user's allowed business-unit ids as a parameterised `IN` clause; I added tests with injection-style inputs. **R** — the pen-test finding was closed and [fill-in] raw queries were migrated to the same helper.

# Performance Impact

- Parameterised queries let the database reuse plans (prepared/cached plans) — usually *faster* than string-built SQL.
- Re-applying scoping filters needs the right indexes (`tenant_id` leading in composite indexes).

**Trade-offs / when NOT to use it:**
- If the ORM can express it (Subquery, Window, Func, conditional aggregation), stay in the ORM — you keep managers, routers and type conversion.
- Raw SQL couples you to one backend's dialect — painful with PostgreSQL *and* SQL Server in one codebase.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "I escape quotes myself." Use parameters; manual escaping is how injections happen.
- "Parameters work for table/column names." They don't — identifiers need a whitelist.
- "`raw()` still applies my custom manager's filter." It doesn't.
- Quoting the placeholder: `'%s'` — that breaks binding; write `%s` bare.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | No difference vs. ORM | Same | ACCESS SHARE only |
| **Medium** | 1M | Plan reuse from parameters helps | Use `iterator()` on RawQuerySet | ACCESS SHARE only |
| **Large** | 100M | Raw SQL often used for window/CTE queries — still parameterise | Stream with cursor `fetchmany` | ACCESS SHARE only |
| **Massive** | 1B+ | Move heavy reporting to replicas/warehouse | — | — |

# Follow-up Questions

1. How do you safely let users choose the sort column?
2. Why doesn't `Manager.raw()` apply your custom manager's filters?
3. When is `RawSQL` inside an annotation better than `Manager.raw()`?

# Related Topics

* Module 01 Q21 — SQL injection with raw queries
* Module 18 Q14 — when raw SQL is architecturally appropriate
* Module 01 Q30 — raw queries with multiple databases

---

# Question

How does Django 5.0's GeneratedField optimize read queries by pre-calculating values?

# Why Interviewer Asks This

Tests knowledge of a newer Django feature *and* the trade-off it represents: moving computation from read time to write time, making it indexable, and knowing its constraints. (Module 03 Q1 covers defining the field; this question is about the read-path win.)

# Answer

**Spoken answer:** "`GeneratedField`, added in Django 5.0, maps to a database generated column: the value is computed by the database from other columns in the same row. With `db_persist=True` it's a *stored* column — computed on every insert or update and saved on disk — which means I can index it, filter on it and sort by it like any other column. That replaces the pattern where every query re-computes `annotate(total=F('qty') * F('price'))`, which can't use an index. It's also consistent no matter who writes the row — our Django app, a sync job or another service. The cost moves to writes: every update recomputes it, and changing the expression later means rewriting the column on a big table."

**The reasoning:**
- Read side: indexable, filterable, no per-query expression.
- Write side: computed on insert/update (stored) — write amplification.
- Constraints: deterministic expressions only, same-row columns only, never written by Django (any value you assign in Python is ignored), and in Django 5.x you must `refresh_from_db()` to see the new value after `save()`.
- PostgreSQL supports stored generated columns; with Django 5.x on PostgreSQL use `db_persist=True`.

# Internal ORM Mechanics

`GeneratedField(expression=..., output_field=..., db_persist=...)` compiles the expression with the schema editor into `GENERATED ALWAYS AS (...) STORED` (or `VIRTUAL` where supported). Django treats it as read-only: fields with `generated=True` are excluded from the INSERT and UPDATE column lists in `Model._save_table()`, so assigning to the attribute in Python has no effect on the row. Because the value is computed by the database, the in-memory instance isn't updated after `save()` in Django 5.x — reload with `refresh_from_db()`.

# SQL Generated

```python
OrderLine.objects.filter(line_total__gte=10000).order_by('-line_total')[:20]
```

```sql
-- migration
ALTER TABLE "shop_orderline"
  ADD COLUMN "line_total" numeric(14, 2) GENERATED ALWAYS AS (("quantity" * "unit_price")) STORED;
CREATE INDEX "orderline_total_idx" ON "shop_orderline" ("line_total");

-- read: a plain indexed column, no per-row computation
SELECT "shop_orderline"."id", "shop_orderline"."quantity", "shop_orderline"."unit_price", "shop_orderline"."line_total"
FROM "shop_orderline"
WHERE "shop_orderline"."line_total" >= 10000
ORDER BY "shop_orderline"."line_total" DESC
LIMIT 20;
```

# Code Example

```python
from django.db import models
from django.db.models import F

class OrderLine(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='lines')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.GeneratedField(
        expression=F('quantity') * F('unit_price'),
        output_field=models.DecimalField(max_digits=14, decimal_places=2),
        db_persist=True,
    )

    class Meta:
        indexes = [models.Index(fields=['line_total'], name='orderline_total_idx')]

# Before: computed on every query, not indexable
OrderLine.objects.annotate(total=F('quantity') * F('unit_price')).filter(total__gte=10000)

# After: indexed column
OrderLine.objects.filter(line_total__gte=10000)

line = OrderLine.objects.create(order=o, quantity=3, unit_price='19.99')
line.refresh_from_db(fields=['line_total'])       # Django 5.x: needed to read the DB-computed value
```

# Production Scenario

**From experience (STAR):** **S** — The PNI Hub analytics dashboard filtered and sorted sync runs by duration (`finished_at - started_at`), computed in an annotation on every request. **T** — Sorting by that annotation forced a full scan and sort over [fill-in] rows; p95 was [fill-in] s. **A** — Because those rows are effectively write-once, I added a stored `GeneratedField` for duration with an index, created in a migration during a low-traffic window since adding it rewrites the table. **R** — the "slowest runs" query became an index scan at [fill-in] ms, and the value was identical for rows written by every job.

# Performance Impact

- Reads: index usable; no per-row expression evaluation.
- Writes: recomputed on every insert/update of a source column; extra storage plus index maintenance.
- DDL: adding or changing a stored generated column rewrites the table under an ACCESS EXCLUSIVE lock.

**Trade-offs / when NOT to use it:**
- Values depending on other rows/tables, `now()` or non-immutable functions → not allowed; use a denormalised column maintained by code or a trigger.
- Frequently changing expressions → each change is a heavy migration.
- Tiny tables or rarely queried values → an annotation is simpler.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "GeneratedField is computed in Python." It's computed by the database.
- "The instance has the new value after `save()`." Not in Django 5.x — `refresh_from_db()`.
- "It can reference related models." Same-row columns only.
- "Adding one is a cheap migration." On large tables it rewrites the whole table.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Little difference vs. annotate | Small extra storage | ACCESS EXCLUSIVE briefly on ADD COLUMN |
| **Medium** | 1M | Indexed filter/sort clearly wins | Column + index size | Table rewrite on add — schedule it |
| **Large** | 100M | Big read wins; migration must be planned (new table + backfill + swap) | Significant | ACCESS EXCLUSIVE rewrite is not acceptable live |
| **Massive** | 1B+ | Add per partition / on new partitions only | — | Partition-by-partition rollout |

# Follow-up Questions

1. Stored vs. virtual generated columns — what's the trade-off?
2. Why can't a generated column reference another table?
3. How would you add a generated column to a 100M-row table without downtime?

# Related Topics

* Module 03 Q1 — defining GeneratedField
* Module 17 Q25 — GeneratedField compilation internals
* Module 13 Q30 — changing field types without locking

---

# Question

How does select_related interact with multi-table inheritance?

# Why Interviewer Asks This

Multi-table inheritance (MTI) hides JOINs and N+1s behind normal-looking attribute access. The interviewer wants to know that child queries always join the parent, that parent→child access is a reverse OneToOne (and a per-row query unless you `select_related` it), and what that does to performance.

# Answer

**Spoken answer:** "With multi-table inheritance, each child model has its own table with a one-to-one `parent_ptr` primary key pointing to the parent table. So when I query a child, Django always INNER JOINs the parent table to get the inherited fields — that's automatic, I don't need `select_related` for it. Going the other way, from a parent row to its child — `asset.server` — is a reverse one-to-one lookup, and that's a query per row unless I add `select_related('server', 'laptop')`, which becomes one LEFT OUTER JOIN per child type. Accessing a child that doesn't exist raises `DoesNotExist`. So MTI costs a JOIN on every child read and an insert into two tables on every write — which is why I usually prefer abstract base classes or a single table with a type column unless I truly need to query across all types."

**The reasoning:**
- Child → parent: implicit INNER JOIN on every query.
- Parent → child: reverse OneToOne → `select_related('child')` turns N queries into LEFT OUTER JOINs.
- Multiple child types → one LEFT JOIN each; wide and sparse rows.
- Libraries (`django-polymorphic`, `django-model-utils` `InheritanceManager.select_subclasses()`) automate the "return the right subclass" pattern.

# Internal ORM Mechanics

The child model gets an auto-created `OneToOneField(parent_link=True)` named `<parent>_ptr` that is also its primary key. `Options.get_parent_list()` lets the compiler include parent columns via `setup_joins()` on the parent link for every child query. The reverse accessor on the parent (`asset.server`) is a `ReverseOneToOneDescriptor`; it's valid in `select_related` because it's single-valued, and the compiler uses LEFT OUTER JOIN since the child may not exist. When an instance is loaded through `select_related('server')` and no child row exists, the descriptor caches that absence and raises `RelatedObjectDoesNotExist` without another query.

# SQL Generated

```python
Server.objects.all()
Asset.objects.select_related('server', 'laptop', 'owner')
```

```sql
-- child query: parent is always joined
SELECT "inventory_asset"."id", "inventory_asset"."name", "inventory_asset"."owner_id",
       "inventory_server"."asset_ptr_id", "inventory_server"."cpu_cores"
FROM "inventory_server"
INNER JOIN "inventory_asset" ON ("inventory_server"."asset_ptr_id" = "inventory_asset"."id");

-- parent query with children selected: one LEFT JOIN per subtype
SELECT "inventory_asset".*, "inventory_server".*, "inventory_laptop".*, "auth_user".*
FROM "inventory_asset"
LEFT OUTER JOIN "inventory_server" ON ("inventory_asset"."id" = "inventory_server"."asset_ptr_id")
LEFT OUTER JOIN "inventory_laptop" ON ("inventory_asset"."id" = "inventory_laptop"."asset_ptr_id")
INNER JOIN "auth_user" ON ("inventory_asset"."owner_id" = "auth_user"."id");
```

# Code Example

```python
class Asset(models.Model):                         # concrete parent → its own table
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.PROTECT)

class Server(Asset):
    cpu_cores = models.PositiveSmallIntegerField()

class Laptop(Asset):
    serial = models.CharField(max_length=50)

def describe(asset):
    try:
        return f'server, {asset.server.cpu_cores} cores'
    except Server.DoesNotExist:
        pass
    try:
        return f'laptop {asset.laptop.serial}'
    except Laptop.DoesNotExist:
        return 'generic asset'

# N+1: up to 2 extra queries per asset
[describe(a) for a in Asset.objects.all()]

# 1 query: children resolved by LEFT JOINs
[describe(a) for a in Asset.objects.select_related('server', 'laptop', 'owner')]
```

# Production Scenario

**From experience (STAR):** **S** — An early PNI Hub design modelled integration connectors with MTI: a base `Connector` and subclasses for REST, SFTP and database connectors. **T** — The connector list page triggered [fill-in] queries (a reverse one-to-one lookup per subtype per row), and every connector save wrote to two tables. **A** — Short term I added `select_related` for every subtype; long term we moved to one `Connector` table with a `kind` column and a JSONField for type-specific settings validated by Pydantic schemas. **R** — the list page went to [fill-in] queries and [fill-in] ms, and adding a new connector type no longer needed a new table.

# Performance Impact

- Every child read = JOIN to the parent; deep hierarchies = chained JOINs.
- Writes insert/update two or more tables in a transaction.
- Selecting all subtypes from the parent = many LEFT JOINs producing wide, mostly-NULL rows.

**Trade-offs / when NOT to use it:**
- Shared fields but no cross-type queries → abstract base class (no JOINs).
- Few type-specific fields → single table + type column (+ JSON for the rest).
- MTI is reasonable when you genuinely query "all assets" often and subtypes have many distinct columns.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Querying `Server` needs `select_related('asset_ptr')`." The parent JOIN is automatic.
- "`asset.server` is free." It's a reverse OneToOne query per row unless selected.
- "Parent queries return subclass instances." They return `Asset` objects; you need `select_subclasses()`/django-polymorphic or explicit access.
- Treating MTI like abstract inheritance — they produce completely different schemas.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | JOIN overhead invisible | Small | ACCESS SHARE only |
| **Medium** | 1M | PK-to-PK JOINs are cheap but constant on every read | Wide rows when selecting subtypes | ACCESS SHARE only |
| **Large** | 100M | Two large tables joined on every read; writes touch both | — | Row locks on both tables per write |
| **Massive** | 1B+ | Avoid MTI; partitioning two linked tables consistently is hard | — | — |

# Follow-up Questions

1. How does MTI differ from abstract base classes at the schema level?
2. How would you return the correct subclass for each row in a mixed list?
3. How would you migrate away from MTI on a live system?

# Related Topics

* Module 02 Q4 — how MTI works database-wise
* Module 02 Q5 — performance cost of MTI
* Module 06 Q34 — prefetching polymorphic models

---

# Question

What is the cost of query execution when using values() with prefetch_related?

# Why Interviewer Asks This

A precise-knowledge question with a trap: combining them doesn't cost an extra query — prefetching is silently skipped. The interviewer wants that fact, the common wrong workaround (row explosion), and the patterns that actually work.

# Answer

**Spoken answer:** "The surprising answer is that the prefetch costs nothing, because it doesn't run. Prefetching works by attaching a cache to each model instance, and a dict from `values()` can't hold that cache — so Django silently skips the prefetch. No error, no second query, and no related data in the result. The usual workaround people reach for is putting the relation in `values()`, like `values('id', 'tags__name')`, but that JOINs and returns one row per tag, so you get duplicates. What I do instead: if I need instances, prefetch on instances and build dicts myself; on PostgreSQL I can aggregate with `ArrayAgg` into one row per parent; or I do a 'manual prefetch' — two `values()` queries merged in Python by key, which also works across databases."

**The reasoning:**
- `prefetch_related()` + `values()` → prefetch silently ignored (dicts/tuples can't carry `_prefetched_objects_cache`).
- `values('rel__field')` on a multi-valued relation → JOIN → N rows per parent.
- Working patterns: instances + prefetch; `ArrayAgg`/`JSONBAgg`; manual two-query merge.

# Internal ORM Mechanics

After `_fetch_all()`, `prefetch_related_objects()` tries to prepare each result by setting `obj._prefetched_objects_cache = {}`. For a dict that raises `AttributeError` (and `TypeError` for tuples from `values_list(flat=True)`); Django catches it, marks the objects as unsuitable and stops processing lookups — by design, because "prefetch_related() doesn't make sense" for non-instances. So the cost is zero queries, and the result has no related data.

# SQL Generated

```python
Article.objects.prefetch_related('tags').values('id', 'title')         # prefetch skipped
Article.objects.values('id', 'title', 'tags__name')                     # row explosion
```

```sql
-- only ONE query runs; the prefetch is silently dropped
SELECT "cms_article"."id", "cms_article"."title" FROM "cms_article";

-- one row per (article, tag) pair
SELECT "cms_article"."id", "cms_article"."title", "cms_tag"."name"
FROM "cms_article"
LEFT OUTER JOIN "cms_article_tags" ON ("cms_article"."id" = "cms_article_tags"."article_id")
LEFT OUTER JOIN "cms_tag" ON ("cms_article_tags"."tag_id" = "cms_tag"."id");
```

# Code Example

```python
from collections import defaultdict
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q

# A) PostgreSQL: aggregate to one row per article
rows = (Article.objects
        .annotate(tag_names=ArrayAgg('tags__name', distinct=True, filter=Q(tags__isnull=False), default=[]))
        .values('id', 'title', 'tag_names'))
# filter= drops the NULL produced by the LEFT JOIN when an article has no tags

# B) Manual prefetch: two values() queries merged by key (portable; works across DB aliases)
articles = list(Article.objects.filter(status='published').values('id', 'title'))
links = (Article.tags.through.objects
         .filter(article_id__in=[a['id'] for a in articles])
         .values_list('article_id', 'tag__name'))
by_article = defaultdict(list)
for article_id, tag in links:
    by_article[article_id].append(tag)
for a in articles:
    a['tags'] = by_article[a['id']]
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub export joined integrations (PostgreSQL) with owning cost centres that live in the MSSQL ODS. **T** — The first version did `values()` + `prefetch_related` and shipped a file with empty cost-centre columns — no error anywhere. **A** — I replaced it with the manual-prefetch pattern: `values()` from PostgreSQL, collect the cost-centre codes, one chunked `values()` query against the ODS alias via our router, merge in Python. **R** — correct data, [fill-in] queries total instead of [fill-in], and the same helper is now used for [fill-in] other cross-database reports.

# Performance Impact

- `values()` + `prefetch_related`: one query; the related data is simply missing.
- `values('rel__x')`: one query, but rows × children — network and dedup cost.
- `ArrayAgg`: one query with GROUP BY; DB does the folding.
- Manual merge: two queries + O(rows) Python merge — predictable and portable.

**Trade-offs / when NOT to use it:**
- `ArrayAgg` is PostgreSQL-only and awkward with several multi-valued relations at once.
- Manual merges are more code — wrap them in a QuerySet/helper method and test them.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "It runs the prefetch and then converts to dicts." It skips the prefetch entirely.
- "It raises an error." It fails silently.
- "Just add `tags__name` to `values()`." Duplicates rows and breaks counts.
- Calling `.distinct()` to hide the duplicates — it hides the symptom and costs a sort/hash.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | All patterns fast | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Row explosion multiplies transfer by avg children per row | Duplicated parent data | ACCESS SHARE only |
| **Large** | 100M | Prefer ArrayAgg or manual merge per chunk | Bounded per chunk | ACCESS SHARE only |
| **Massive** | 1B+ | Pre-aggregate into reporting tables | — | Replicas / warehouse |

# Follow-up Questions

1. Why can't Django prefetch onto dicts?
2. How would you combine related data from two different databases in one response?
3. What goes wrong with two `ArrayAgg`s over different relations in the same query?

# Related Topics

* Module 06 Q18 — select_related limits on M2M
* Module 14 Q28 — cross-database aggregation in Python
* Module 09 Q23 — annotating related ids/values

---

# Question

Explain the internal caching of prefetched querysets.

# Why Interviewer Asks This

Prefetch caching causes subtle staleness bugs. The interviewer wants to know where results are stored, what reads from that cache, what invalidates it (and what doesn't), and how to prefetch onto objects you already have.

# Answer

**Spoken answer:** "Prefetched results live on each parent instance, in a dict called `_prefetched_objects_cache`, keyed by the relation name. When you call `project.tickets.all()`, the related manager checks that dict first and returns the cached queryset, so there's no query. With `to_attr`, it's just a plain list attribute instead. The cache is per instance and per process — it's not shared across requests like Redis. And it's not automatically invalidated: the related manager's `add()`, `remove()`, `clear()` and `set()` do clear it, but if someone creates a ticket with `Ticket.objects.create(project=p)`, `p`'s cache is now stale. `refresh_from_db()` clears it. And if I already have instances — from pagination or from a cache — I can attach prefetches with `prefetch_related_objects()`."

**The reasoning:**
- Storage: `instance._prefetched_objects_cache[name]` (a QuerySet with filled result cache) or `setattr(instance, to_attr, list)`.
- Forward FK/OneToOne prefetches go into the field cache, the same place `select_related` uses.
- Invalidation: related-manager writes clear it; direct model writes don't; `refresh_from_db()` does.
- Lifetime: as long as the instance lives — beware long-lived objects in workers.

# Internal ORM Mechanics

`prefetch_one_level()` writes `obj._prefetched_objects_cache[cache_name] = qs` where `qs` is the manager's queryset with `_result_cache` set to the children and `_prefetch_done = True`. The related manager's `get_queryset()` begins with `try: return self.instance._prefetched_objects_cache[self.prefetch_cache_name]`. Mutating manager methods call `self._remove_prefetched_objects()`, which pops that key. `Model.refresh_from_db()` with no `fields` resets `_prefetched_objects_cache = {}`; with `fields`, it removes only the named entries. `prefetch_related_objects(instances, *lookups)` is the same engine used by `QuerySet`, applied to any list of instances of one model.

# SQL Generated

```python
projects = list(Project.objects.prefetch_related('tickets'))
projects[0].tickets.all()            # no SQL
projects[0].refresh_from_db()        # SELECT for the project; prefetch cache cleared
projects[0].tickets.all()            # SQL again
```

```sql
SELECT ... FROM "pm_project";
SELECT ... FROM "pm_ticket" WHERE "pm_ticket"."project_id" IN (1, 2, 3);
-- refresh_from_db()
SELECT ... FROM "pm_project" WHERE "pm_project"."id" = 1 LIMIT 21;
-- first access after the refresh
SELECT ... FROM "pm_ticket" WHERE "pm_ticket"."project_id" = 1;
```

# Code Example

```python
from django.db.models import prefetch_related_objects

projects = list(Project.objects.prefetch_related('tickets'))
p = projects[0]
p._prefetched_objects_cache.keys()          # dict_keys(['tickets'])

Ticket.objects.create(project=p, title='New')    # direct create → cache NOT cleared
len(p.tickets.all())                              # stale count

p.tickets.create(title='Another')           # via the related manager → cache cleared
len(p.tickets.all())                        # fresh query, correct

# Prefetch onto instances you already have (page slice, cached list, etc.)
page = list(Project.objects.order_by('name')[:25])
prefetch_related_objects(page, 'tickets', 'members')
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub DRF `create` action added a sync run to an integration and then serialised the integration with its runs in the response. **T** — The response didn't include the new run: the view had loaded the integration with `prefetch_related('sync_runs')` before creating the run with `SyncRun.objects.create(...)`. **A** — I created it via `integration.sync_runs.create(...)`, which clears the prefetch cache, and for the bulk path called `integration.refresh_from_db()` before serialising. **R** — the bug was fixed and I added a regression test asserting the response contains the new run.

# Performance Impact

- Cache hits cost zero queries; invalidation costs one re-query on next access.
- Memory: the cached children live as long as the parent instances — a worker that keeps instances around (module-level caches, long loops) can grow memory.

**Trade-offs / when NOT to use it:**
- Don't rely on prefetch caches across writes in the same request — re-query or refresh deliberately.
- Don't treat prefetch as an application cache — it's per evaluation; use Redis for cross-request caching.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "The prefetch cache is shared across requests." It's on the instance, in one process.
- "Django invalidates it when related rows change." Only through the related manager's own write methods.
- "`to_attr` results are a QuerySet." They're a list.
- Not knowing `prefetch_related_objects()` exists for already-loaded instances.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Cache hits are free | Children held per parent | ACCESS SHARE only |
| **Medium** | 1M | Same — per page | Bounded by page | ACCESS SHARE only |
| **Large** | 100M | Jobs: drop references per chunk so caches are freed | Watch long-lived instances | ACCESS SHARE only |
| **Massive** | 1B+ | Use streamed iteration; never cache instances module-wide | — | — |

# Follow-up Questions

1. Which operations clear the prefetch cache and which don't?
2. How do you prefetch onto a list you got from Redis?
3. Where is a prefetched *forward* ForeignKey stored?

# Related Topics

* Module 06 Q2 — when prefetch queries run
* Module 17 Q13 — `_result_cache` internals
* Module 01 Q4 — QuerySet caching and when it's bypassed

---

# Question

How do you chunk a large QuerySet into small batches for updates?

# Why Interviewer Asks This

Every long-running job eventually does this. The interviewer is looking for keyset (PK-range) batching, short transactions per batch, the OFFSET-skipping bug, idempotency/resumability, and awareness of locks and replicas.

# Answer

**Spoken answer:** "I never iterate a huge queryset with `.all()`, because that loads everything into memory, and I avoid slicing with offsets, because if my update changes which rows match the filter, the offsets shift and I skip rows — a classic bug. Instead I batch by primary key: fetch the next N ids greater than the last id I processed, ordered by id, update those in a short transaction, remember the last id, repeat. Each batch is small enough to keep locks short and WAL bursts small, and the job is resumable from the last id if it crashes. If the new value is the same for all rows or derivable in SQL, I use `update()` per batch; if it's computed in Python, `bulk_update()`."

**The reasoning:**
- Keyset by PK → constant cost per batch, no skipped rows.
- One transaction per batch → bounded locks, bounded rollback, replicas keep up.
- Idempotent updates + a checkpoint (last PK) → safe restarts.
- Optional throttling (sleep) to protect OLTP traffic.

# Internal ORM Mechanics

`filter(pk__gt=last).order_by('pk').values_list('pk', flat=True)[:n]` compiles to an index range scan on the primary key with `LIMIT n`, so each batch costs the same no matter how far into the table you are. Slicing with an offset compiles to `LIMIT n OFFSET k`, which re-evaluates the filter each time — if processed rows no longer match, every row shifts left and the next offset skips them. `iterator(chunk_size=...)` streams reads with a server-side cursor on PostgreSQL but holds one cursor and snapshot open for the whole run, which is fine for reads but not for a long update job.

# SQL Generated

```sql
-- batch selection: index range scan on the PK
SELECT "crm_customer"."id" FROM "crm_customer"
WHERE ("crm_customer"."id" > 40000 AND "crm_customer"."region" IS NULL)
ORDER BY "crm_customer"."id" ASC LIMIT 2000;

-- batch update (values computed in Python → bulk_update → CASE)
UPDATE "crm_customer" SET "region" = (CASE WHEN ("crm_customer"."id" = 40001) THEN 'EMEA' ... ELSE NULL END)::varchar(10)
WHERE "crm_customer"."id" IN (40001, 40002, /* … */);
```

# Code Example

```python
import time
from django.db import transaction

def backfill_region(batch=2000, pause=0.05, start_after=0):
    last_pk = start_after
    while True:
        ids = list(Customer.objects
                   .filter(pk__gt=last_pk, region__isnull=True)
                   .order_by('pk')
                   .values_list('pk', flat=True)[:batch])
        if not ids:
            return last_pk
        with transaction.atomic():
            customers = list(Customer.objects.filter(pk__in=ids).select_related('address'))
            for c in customers:
                c.region = region_for(c.address.country)     # idempotent
            Customer.objects.bulk_update(customers, ['region'], batch_size=500)
        last_pk = ids[-1]
        checkpoint('backfill_region', last_pk)               # e.g. Redis key or a job-state table
        time.sleep(pause)                                    # yield to OLTP traffic and replicas

# The bug to avoid: OFFSET slicing over a filter that the update changes
qs = Customer.objects.filter(region__isnull=True).order_by('pk')
for start in range(0, total, 2000):
    chunk = qs[start:start + 2000]      # rows already updated drop out → every other batch is skipped
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub needed to backfill a normalised `business_unit` field on [fill-in] synced records after a data-model change, while ten scheduled jobs and the APIs kept running. **T** — A one-shot `update()` would lock too many rows and lag the replica; an earlier offset-based script had silently skipped [fill-in]% of rows. **A** — I wrote a PK-range batched backfill as a management command, run via django-crontab off-hours, with a Redis checkpoint, a small sleep between batches, and a final verification query counting remaining NULLs. **R** — it completed in [fill-in] with zero skipped rows; replica lag stayed under [fill-in] s and no API latency alerts fired.

# Performance Impact

- Each batch: one PK range scan + one UPDATE; cost constant across the table.
- Locks: held only for one batch; WAL generated in small bursts.
- Throughput vs. impact is tuned with batch size and pause.

**Trade-offs / when NOT to use it:**
- Small tables: a single `update()` is simpler and fine.
- Value expressible in SQL: `filter(pk__in=ids).update(col=...)` per batch — or a single set-based `UPDATE ... FROM` for one-off migrations in a maintenance window.
- Batches need an index-friendly key; UUID PKs still work (ordered comparison), but locality is worse.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Use `qs[i:i+n]` in a loop." OFFSET gets slower per batch and skips rows when the filter changes.
- "Wrap the whole job in one `atomic()`." Long locks, huge rollback, replica lag.
- "`iterator()` solves it." It solves memory for reads; it doesn't give you short transactions or resumability.
- No checkpoint — a crash at 90% means starting over.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | One `update()` | Trivial | Row locks briefly |
| **Medium** | 1M | PK batches of 1–5K | Bounded per batch | Row locks per batch |
| **Large** | 100M | Batches + throttling + checkpoints; run off-peak | Flat | Short transactions; watch replica lag and autovacuum |
| **Massive** | 1B+ | Parallel workers over disjoint PK ranges or partitions | Flat per worker | Coordinate to avoid lock contention |

# Follow-up Questions

1. Why does OFFSET-based batching skip rows during an update?
2. How do you make a batched backfill resumable and idempotent?
3. How would you parallelise it safely?

# Related Topics

* Module 06 Q7 — `bulk_update()`
* Module 16 Q27 — chunked cleanup jobs
* Module 13 Q4 — safe data migrations

---

# Question

Explain how to write a query that prefetches only active items of a relation.

# Why Interviewer Asks This

A very practical prefetch scenario. The interviewer wants a filtered `Prefetch` with `to_attr`, an explanation of why filtering after prefetching fails, and — at senior level — "latest N per parent" via sliced prefetches (Django 4.2+) and when a boolean annotation is enough.

# Answer

**Spoken answer:** "I use a `Prefetch` object with a filtered queryset — `Prefetch('comments', queryset=Comment.objects.filter(status='approved'), to_attr='approved_comments')`. The filter goes into the single prefetch query, so only active rows are transferred. I always use `to_attr` here, because without it the filtered list replaces the relation's cache and `post.comments.all()` would silently return only approved comments to any other code. If I need only the latest few per parent, since Django 4.2 I can slice the prefetch queryset — `[:3]` — and Django implements it with a `ROW_NUMBER()` window function per parent. And if all I need is 'has any active item', I don't prefetch at all; I annotate an `Exists`."

**The reasoning:**
- Filter in `Prefetch(queryset=...)`, not in the loop.
- `to_attr` to avoid poisoning the default relation cache.
- Latest-N per parent → sliced `Prefetch` (window function, needs DB support for window functions).
- Boolean → `annotate(has_active=Exists(...))`; count → `annotate(Count(..., filter=Q(...)))`.

# Internal ORM Mechanics

The prefetch machinery adds `post_id__in=[...]` to your queryset. If that queryset is sliced, `_filter_prefetch_queryset()` removes the LIMIT/OFFSET and instead adds a `Window(RowNumber(), partition_by=<fk>, order_by=<your ordering>)` predicate bounded by the slice, which the compiler wraps in a subquery (a "qualify" emulation) because a window result can't be filtered in the same WHERE. Without window-function support it raises `NotSupportedError`.

# SQL Generated

```python
Post.objects.prefetch_related(
    Prefetch('comments', queryset=Comment.objects.filter(status='approved').order_by('-created_at')[:3], to_attr='latest_comments'))
```

```sql
SELECT ... FROM "blog_post";

-- sliced prefetch (simplified): top 3 approved comments per post in ONE query
SELECT * FROM (
    SELECT "blog_comment"."id", "blog_comment"."post_id", "blog_comment"."body", "blog_comment"."created_at",
           ROW_NUMBER() OVER (PARTITION BY "blog_comment"."post_id" ORDER BY "blog_comment"."created_at" DESC) AS "qual0"
    FROM "blog_comment"
    WHERE ("blog_comment"."status" = 'approved' AND "blog_comment"."post_id" IN (1, 2, 3))
) "qualify"
WHERE "qual0" <= 3;
```

# Code Example

```python
from django.db.models import Count, Exists, OuterRef, Prefetch, Q

approved = Comment.objects.filter(status='approved').order_by('-created_at')

posts = Post.objects.prefetch_related(
    Prefetch('comments', queryset=approved, to_attr='approved_comments'),     # all approved
    Prefetch('comments', queryset=approved[:3], to_attr='latest_comments'),   # top 3 per post (4.2+)
)

for p in posts:                      # 3 queries total
    p.approved_comments              # list
    p.latest_comments                # list, at most 3
    p.comments.all()                 # still the FULL relation (cache untouched thanks to to_attr)

# Only need a flag or a number? Don't prefetch rows at all.
posts = Post.objects.annotate(
    has_pending=Exists(Comment.objects.filter(post=OuterRef('pk'), status='pending')),
    approved_count=Count('comments', filter=Q(comments__status='approved')),
)
```

# Production Scenario

**From experience (STAR):** **S** — The PNI Hub integration list shows each integration with its *active* endpoints and the three most recent failed sync runs. **T** — The original code prefetched all endpoints and all runs, then filtered and sliced in the serializer, transferring [fill-in] rows per page. **A** — I used `Prefetch('endpoints', queryset=Endpoint.objects.filter(is_enabled=True), to_attr='active_endpoints')` and a sliced `Prefetch` for the last three failed runs, plus an `Exists` annotation for the "has open incident" badge. **R** — rows transferred per page dropped from [fill-in] to [fill-in], and response time from [fill-in] to [fill-in] ms.

# Performance Impact

- Filtered prefetch: only matching rows cross the network; needs an index on `(fk, filter_col)`.
- Sliced prefetch: the window function processes all matching children for the page's parents, then keeps N — index on `(fk, order_col)` keeps that cheap.
- `Exists`/`Count` annotations: no child rows at all.

**Trade-offs / when NOT to use it:**
- Parents with tens of thousands of children: the window function still scans them; consider a "latest" denormalised column or a `Subquery` for latest-1.
- Without `to_attr`, the filtered result silently changes `obj.relation.all()` semantics for the rest of the request.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Prefetch, then `.filter(status='approved')` in the loop." New query per parent.
- "Slice the prefetch queryset — it limits the whole result to 3." Since 4.2 it's per parent; before 4.2 slicing was an error.
- Filtered `Prefetch` without `to_attr` — other code now sees a partial relation.
- Prefetching rows only to compute a boolean or a count.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Any approach fine | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Composite index `(fk, status, created_at)` serves filter + order | Only active rows loaded | ACCESS SHARE only |
| **Large** | 100M | Sliced prefetch scans all children of the page's parents — keep pages small | Bounded by N per parent | ACCESS SHARE only |
| **Massive** | 1B+ | Partial index on active rows; or denormalised "latest" pointers | — | — |

# Follow-up Questions

1. How does Django implement a sliced prefetch?
2. Why is `to_attr` important when the `Prefetch` queryset is filtered?
3. When would you use `Exists` instead of a prefetch?

# Related Topics

* Module 06 Q3 — the `Prefetch` object
* Module 10 Q12 — `Exists` to annotate booleans
* Module 12 Q4 — partial indexes

---

# Question

How does django-cachalot optimize database queries globally?

# Why Interviewer Asks This

Tests whether you understand automatic ORM query caching — how it keys and invalidates results, which workloads it suits, and the consistency traps (writes from outside Django, table-level invalidation churn) that make an experienced engineer cautious about it.

# Answer

**Spoken answer:** "django-cachalot caches the result of every ORM SELECT in your cache backend, keyed by the SQL and its parameters, and invalidates by *table*: whenever Django writes to a table, every cached query that touched that table becomes stale. That gives you near-zero-effort caching for read-heavy, rarely-written tables — lookup tables, configuration, reference data. But the granularity is coarse: one write to a busy table throws away all its cached queries, so on write-heavy tables you just churn the cache. And it only knows about writes that go through Django — if another service, a database job or a replication feed changes the data, cachalot serves stale results. So I'd scope it to an explicit allow-list of tables, or more often I'd use explicit cache-aside caching with keys I control."

**The reasoning:**
- Key = SQL + params (+ database alias); value = the result rows.
- Invalidation = per-table timestamps; any ORM write to a table invalidates every cached query that used it.
- Great for: high read/write ratio, small-to-medium result sets, data changed only through Django.
- Bad for: hot write tables, data written by other systems, per-user queries with low reuse.

# Internal ORM Mechanics

Cachalot patches the SQL compilers' `execute_sql`. For a read, it computes a cache key from the SQL, params and alias, and looks up the result along with the *table invalidation timestamps* for every table the query references; a cached result is valid only if it was stored after the latest invalidation of each of those tables. Writes (`SQLInsertCompiler`, `SQLUpdateCompiler`, `SQLDeleteCompiler`, and raw cursor writes it can parse) bump the invalidation timestamp of the affected tables. It is transaction-aware: invalidations inside an `atomic()` block are kept local and applied on commit. Settings such as `CACHALOT_ONLY_CACHABLE_TABLES`, `CACHALOT_UNCACHABLE_TABLES` and `CACHALOT_TIMEOUT` control scope.

# SQL Generated

```sql
-- first call: hits the DB, result stored under hash(SQL + params + alias)
SELECT "catalog_region"."id", "catalog_region"."code", "catalog_region"."name" FROM "catalog_region" ORDER BY "catalog_region"."code" ASC;

-- any ORM write to catalog_region bumps its invalidation timestamp:
UPDATE "catalog_region" SET "name" = 'EMEA North' WHERE "catalog_region"."id" = 4;
-- → the next SELECT above misses the cache and goes back to the DB
```

# Code Example

```python
# settings.py
INSTALLED_APPS += ['cachalot']
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.redis.RedisCache', 'LOCATION': REDIS_URL}}

# Scope it explicitly to slow-changing reference tables
CACHALOT_ONLY_CACHABLE_TABLES = frozenset({'catalog_region', 'catalog_costcentre', 'catalog_integrationtype'})
CACHALOT_TIMEOUT = 60 * 60

# Reads anywhere in the codebase now hit Redis after the first call
regions = list(Region.objects.order_by('code'))

# The alternative I usually prefer: explicit cache-aside with a versioned key
def get_regions():
    return cache.get_or_set('regions:v3', lambda: list(Region.objects.order_by('code').values('id', 'code', 'name')), 3600)
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub reference data (business units, cost centres) is synced into PostgreSQL from the MSSQL ODS by a django-crontab job, and read on almost every API request. **T** — We evaluated cachalot to cut [fill-in] repeated lookups per request. **A** — Because the sync job writes through the ORM, table-level invalidation would work for those tables — but other tables were also updated by a stored procedure outside Django, which cachalot can't see. I chose explicit cache-aside for reference data instead: a cache-warming cron job writes versioned Redis keys after each sync, and the API reads them. **R** — DB queries per request dropped by [fill-in], with no stale-data risk from out-of-band writes.

# Performance Impact

- Cache hit: a Redis round-trip instead of a DB query — a win when the query is non-trivial or the DB is the bottleneck.
- Every read also checks table invalidation keys; every write invalidates whole tables.
- Memory in Redis grows with distinct queries (each parameter combination is a separate entry).

**Trade-offs / when NOT to use it:**
- Write-heavy tables → constant invalidation; overhead without hits.
- Data written outside Django (other services, DB jobs, CDC) → stale reads.
- Very simple PK lookups → a Redis round-trip isn't much cheaper than an indexed DB lookup.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "It caches per row and invalidates the changed row." It invalidates by table.
- "It's always consistent." Only for writes it observes.
- "Turn it on for everything." Hot tables churn the cache and add overhead.
- Using the local-memory cache backend with several processes — each process has its own cache and invalidations don't propagate.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Reference tables: excellent hit rates | Small Redis footprint | ACCESS SHARE on misses only |
| **Medium** | 1M | Fine for read-mostly tables; check hit ratio | Grows with distinct queries | — |
| **Large** | 100M | Large result sets are expensive to serialise into cache | Can be large | — |
| **Massive** | 1B+ | Use purpose-built caches/materialised views instead | — | — |

# Follow-up Questions

1. Why does table-level invalidation make cachalot unsuitable for write-heavy tables?
2. How would you cache reference data that is written by a non-Django process?
3. How do you prevent a cache stampede when a hot key expires?

# Related Topics

* Module 16 Q3 — Redis/Memcached with the ORM
* Module 16 Q4 — cache stampede
* Module 06 Q28 — the per-instance prefetch cache (not a shared cache)

---

# Question

What is the database impact of using only() with deep select_related?

# Why Interviewer Asks This

Checks that you understand what column trimming across joins does and doesn't change at the database (fewer columns, same joins), the FK-column rules Django enforces, and the fragility this introduces.

# Answer

**Spoken answer:** "Combining them narrows the SELECT list across every joined table: `select_related('customer__account_manager').only('id', 'total', 'customer__name', 'customer__account_manager__email')` still does the same JOINs, but only pulls those columns plus the primary keys and the foreign keys needed to link the objects. So the database still does the join work; what you save is bytes — reading wide columns, network transfer, and Python decoding — which matters when the joined tables are wide. The risks are that Django raises a `FieldError` if you defer a relation you're also selecting, and that any code touching a column you didn't load — `__str__`, a serializer, a signal — silently triggers a query per object, per level. For read-only screens I'd often just use `values()` across the joins instead."

**The reasoning:**
- JOINs: unchanged. Columns: trimmed per table. Planner: mostly unchanged.
- Django auto-includes the PK of each model and the FK columns that link them.
- Naming `customer__name` in `only()` implicitly keeps the `customer` relation; deferring the relation while selecting it is an error.

# Internal ORM Mechanics

`only()` records the field paths in `query.deferred_loading`. When the compiler builds `select_related` columns (`get_related_selections()`), it consults `get_select_mask()` — a nested mask per model — to choose which concrete columns to emit for each joined model. If a relation used by `select_related` is excluded by the mask, `select_related_descend()` raises `FieldError: Field X cannot be both deferred and traversed using select_related at the same time`. Each related object is built with `from_db()` using only the masked columns; the rest become deferred attributes.

# SQL Generated

```python
(Order.objects
 .select_related('customer__account_manager')
 .only('id', 'total', 'customer__name', 'customer__account_manager__email'))
```

```sql
SELECT "shop_order"."id", "shop_order"."customer_id", "shop_order"."total",
       "shop_customer"."id", "shop_customer"."name", "shop_customer"."account_manager_id",
       "auth_user"."id", "auth_user"."email"
FROM "shop_order"
INNER JOIN "shop_customer" ON ("shop_order"."customer_id" = "shop_customer"."id")
LEFT OUTER JOIN "auth_user" ON ("shop_customer"."account_manager_id" = "auth_user"."id");
```

# Code Example

```python
qs = (Order.objects
      .select_related('customer__account_manager')
      .only('id', 'total', 'customer__name', 'customer__account_manager__email'))

for o in qs:
    o.customer.name                         # loaded
    o.customer.account_manager.email        # loaded (if not None)
    o.customer.email                        # deferred → one query per order!

# Error: the relation is selected but deferred
Order.objects.select_related('customer').only('id', 'total')
# FieldError: Field Order.customer cannot be both deferred and traversed using select_related at the same time.

# Read-only alternative with no lazy-loading risk
Order.objects.values('id', 'total', 'customer__name', 'customer__account_manager__email')
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub DRF endpoint returned sync runs with integration name, owner email and department code — three levels of joins over wide tables mirrored from the ODS. **T** — Each row carried [fill-in] columns but the serializer used [fill-in]. **A** — I added `only()` with the exact column paths the serializer used, generated from the serializer's field list in one helper so the two couldn't drift, and added a query-count test. **R** — bytes per page dropped from [fill-in] to [fill-in] KB and latency by [fill-in] ms; the join plan itself didn't change, which matched expectations.

# Performance Impact

- Less I/O (especially skipped TOAST/LOB columns), less network, less Python decoding.
- No change to join algorithms or row counts; rarely enables index-only scans across joins.
- Risk of per-object, per-level lazy loads.

**Trade-offs / when NOT to use it:**
- Narrow joined tables: savings are negligible.
- Querysets shared across many consumers: column lists become a hidden contract — prefer `values()` or a dedicated read model.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`only()` reduces the number of joins." It reduces columns only.
- "You can defer the FK and still `select_related` it." `FieldError`.
- "Django won't include FK columns I didn't list." It includes PKs and linking FKs automatically.
- Forgetting `__str__` or the admin touches unlisted fields.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | No noticeable change | Small | ACCESS SHARE only |
| **Medium** | 1M | Noticeable on wide joined tables | Proportional to trimmed bytes | ACCESS SHARE only |
| **Large** | 100M | Joins dominate; trimming helps transfer, not plan | Big win for exports | ACCESS SHARE only |
| **Massive** | 1B+ | Denormalised read tables beat deep joins | — | Replicas |

# Follow-up Questions

1. Which columns does Django always include even with `only()`?
2. Why does deferring a relation you `select_related` raise an error?
3. How would you keep a serializer and an `only()` list in sync?

# Related Topics

* Module 06 Q4 — `only()` vs `defer()`
* Module 06 Q12 — select_related joins and memory
* Module 06 Q37 — N+1 in DRF serializers

---

# Question

How do you write a custom QuerySet iterator for fast object parsing?

# Why Interviewer Asks This

A deeper ORM-extension question: does the candidate know how QuerySets turn rows into Python objects (`_iterable_class`), the public alternatives, and the trade-off of relying on semi-private APIs for speed?

# Answer

**Spoken answer:** "Every QuerySet has an iterable class that turns database rows into Python objects — `ModelIterable` for instances, `ValuesIterable` for dicts and so on. When I need to stream a lot of rows into something lighter than model instances — a slotted dataclass, a Pydantic model for an API — the first choice is the public API: `values_list(...)` with `iterator(chunk_size=...)` and a small generator that builds my objects. That gets almost all of the speed-up. If I want it reusable and chainable, I can write a `BaseIterable` subclass and set it as the queryset's `_iterable_class` in a custom QuerySet method — that's how Django's own `values()` works — but `_iterable_class` is internal, so I pin and test it across Django upgrades."

**The reasoning:**
- The cost of instances is per-row `from_db()`, `_state`, descriptors and signals.
- Public path: `values_list()` + `iterator(chunk_size)` + a generator → no instances, streamed.
- Custom iterable: chainable QuerySet API returning your type; relies on `_iterable_class`.
- Measure first — the DB and network are often the real bottleneck.

# Internal ORM Mechanics

`QuerySet.__iter__` → `_fetch_all()` → `list(self._iterable_class(self))`; `iterator()` uses the same class with `chunked_fetch=True` (server-side cursor on PostgreSQL) and doesn't fill `_result_cache`. A `BaseIterable` subclass receives `queryset`, `chunked_fetch` and `chunk_size`, and implements `__iter__`, typically by calling `queryset.query.get_compiler(queryset.db).results_iter(...)` — which already applies field converters — and yielding whatever objects you like. `_iterable_class` is preserved by `_clone()`, so chaining keeps it.

# SQL Generated

```sql
-- same SQL as values_list('device_id', 'day', 'value'); only the Python side differs
SELECT "iot_dailymetric"."device_id", "iot_dailymetric"."day", "iot_dailymetric"."value"
FROM "iot_dailymetric"
WHERE "iot_dailymetric"."day" >= '2026-11-01'::date;
```

# Code Example

```python
from dataclasses import dataclass
from datetime import date
from django.db import models
from django.db.models.query import BaseIterable

@dataclass(slots=True, frozen=True)
class MetricRow:
    device_id: int
    day: date
    value: float

# 1) Public API — usually enough
def metric_rows(qs, chunk=5000):
    for row in qs.values_list('device_id', 'day', 'value').iterator(chunk_size=chunk):
        yield MetricRow(*row)

# 2) Reusable, chainable custom iterable (relies on the internal _iterable_class hook)
class MetricRowIterable(BaseIterable):
    def __iter__(self):
        compiler = self.queryset.query.get_compiler(self.queryset.db)
        for row in compiler.results_iter(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size):
            yield MetricRow(*row)

class DailyMetricQuerySet(models.QuerySet):
    def as_rows(self):
        qs = self.values_list('device_id', 'day', 'value')   # fixes the column order
        qs._iterable_class = MetricRowIterable
        return qs

class DailyMetric(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE)
    day = models.DateField()
    value = models.FloatField()
    objects = DailyMetricQuerySet.as_manager()

for r in DailyMetric.objects.filter(day__gte=date(2026, 11, 1)).as_rows().iterator(chunk_size=5000):
    ...   # r is a MetricRow
```

# Production Scenario

**From experience (STAR):** **S** — A PNI Hub FastAPI service shared the Django models to serve analytics data as Pydantic responses. **T** — Building Django instances and converting them to Pydantic models for [fill-in] rows cost [fill-in] ms per request in Python alone. **A** — I added a QuerySet method that returns `values_list(named=True)` rows streamed with `iterator(chunk_size=...)` and validated them in one pass with a Pydantic `TypeAdapter`; I kept the custom-iterable version behind a test that runs on every Django upgrade. **R** — Python-side time per request dropped from [fill-in] to [fill-in] ms with identical output.

# Performance Impact

- Removes per-row instance construction and signals; memory flat when streamed.
- No DB-side change.
- Converters still run — JSON decoding can still dominate for JSON-heavy rows.

**Trade-offs / when NOT to use it:**
- `_iterable_class` is not public API — behaviour can change between releases.
- If the code needs model methods or `save()`, you need instances.
- `values_list(named=True)` or plain dicts are simpler and usually fast enough.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Override `__iter__` on the QuerySet." That breaks caching, `iterator()` and slicing semantics; the iterable class is the hook.
- "Use `raw()` to make it faster." It still builds model instances.
- Building a custom iterable before measuring that instantiation is the bottleneck.
- Forgetting that the column order in `values_list()` defines the tuple layout your iterable relies on.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Not worth it | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Clear Python-time win for exports/jobs | Slotted objects are compact | ACCESS SHARE only |
| **Large** | 100M | Stream with `chunk_size`; server-side cursor on PostgreSQL | Flat | ACCESS SHARE; cursor holds a snapshot |
| **Massive** | 1B+ | `COPY TO` / warehouse exports beat any Python iterator | — | Replicas |

# Follow-up Questions

1. How does `values()` use the iterable-class hook internally?
2. What changes when you call `iterator()` on PostgreSQL?
3. Why might converters still dominate even after removing instance creation?

# Related Topics

* Module 06 Q23 — what `values()` skips
* Module 01 Q8 — `iterator()` vs normal evaluation
* Module 17 Q20 — how rows become instances

---

# Question

Explain the performance cost of prefetching polymorphic models.

# Why Interviewer Asks This

Polymorphic relations (GenericForeignKey, django-polymorphic) multiply queries per type and defeat simple JOINs. The interviewer wants you to count queries correctly, know Django 5.0's `GenericPrefetch`, and recognise when to denormalise instead.

# Answer

**Spoken answer:** "With a polymorphic relation, the related rows live in different tables, so prefetching costs one query per distinct type rather than one per relation. A `GenericForeignKey` prefetch groups the objects by content type and runs one `id IN (...)` query per type; with django-polymorphic, the base query returns base rows and then one extra query per subclass to fetch the real child objects — each joining the parent table. So an activity feed pointing at five types costs five or six queries, and if those objects need their own related data, each type needs its own `select_related`. Django 5.0's `GenericPrefetch` lets me pass one queryset per content type for exactly that. And for feeds or lists, I often denormalise the display fields — title, type, URL — onto the feed row so the list doesn't need to resolve targets at all."

**The reasoning:**
- GFK prefetch: 1 query per distinct content type in the page (+ ContentType lookups, cached).
- django-polymorphic: 1 base + 1 per subclass present; child queries JOIN the parent (MTI).
- Nested data per type: use `GenericPrefetch` querysets with `select_related`.
- Simplest scaling move: denormalise what lists display.

# Internal ORM Mechanics

`GenericForeignKey.get_prefetch_querysets()` groups instances by `content_type_id`, and for each type runs `ct.get_all_objects_for_this_type(pk__in=ids)` (or your supplied queryset when using `GenericPrefetch(lookup, querysets)`), then matches results back by `(content_type, object_id)`. `ContentType.objects.get_for_id()` is cached per process. django-polymorphic's `PolymorphicQuerySet` fetches base rows, groups them by `polymorphic_ctype`, and runs one query per real subclass to replace base objects with subclass instances.

# SQL Generated

```python
from django.contrib.contenttypes.prefetch import GenericPrefetch

ActivityEvent.objects.prefetch_related(
    GenericPrefetch('target', [Ticket.objects.select_related('project'),
                               Deployment.objects.only('id', 'version', 'status')])
).order_by('-created_at')[:100]
```

```sql
SELECT "feed_activityevent"."id", "feed_activityevent"."content_type_id", "feed_activityevent"."object_id", ...
FROM "feed_activityevent" ORDER BY "feed_activityevent"."created_at" DESC LIMIT 100;

-- one query per content type present on the page
SELECT "helpdesk_ticket".*, "pm_project".* FROM "helpdesk_ticket"
INNER JOIN "pm_project" ON ("helpdesk_ticket"."project_id" = "pm_project"."id")
WHERE "helpdesk_ticket"."id" IN (12, 57, 90);

SELECT "ops_deployment"."id", "ops_deployment"."version", "ops_deployment"."status"
FROM "ops_deployment" WHERE "ops_deployment"."id" IN (3, 8);
```

# Code Example

```python
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.prefetch import GenericPrefetch

class ActivityEvent(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    verb = models.CharField(max_length=30)
    # denormalised display fields → list pages never need to resolve `target`
    target_label = models.CharField(max_length=200)
    target_kind = models.CharField(max_length=30)
    created_at = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [models.Index(fields=['content_type', 'object_id'])]

# Feed list: zero target queries
feed = ActivityEvent.objects.only('id', 'verb', 'target_label', 'target_kind', 'created_at').order_by('-created_at')[:100]

# Detail view needing real objects: one query per type, each with its own joins (Django 5.0+)
events = ActivityEvent.objects.prefetch_related(
    GenericPrefetch('target', [Ticket.objects.select_related('project'), Deployment.objects.all()])
).order_by('-created_at')[:100]
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub has an activity timeline mixing config changes, sync failures, deployments and access grants, modelled with a generic foreign key. **T** — The timeline API issued [fill-in] queries per page: one GFK lookup per event plus N+1s inside each target type. **A** — For the list, I denormalised label/kind/link onto the event row at write time; for the expanded view I used `GenericPrefetch` with a tuned queryset per type. **R** — list queries dropped to [fill-in] per page and p95 from [fill-in] to [fill-in] ms.

# Performance Impact

- Queries scale with the number of *types* per page, plus per-type nested relations.
- No DB-level FK on `object_id` → no referential integrity, no JOIN-based optimisation, and you need a composite index on `(content_type_id, object_id)`.
- MTI-backed polymorphism adds a parent JOIN to every subclass query.

**Trade-offs / when NOT to use it:**
- Denormalised display fields must be kept in sync (write-time update or a periodic repair job).
- If the type set is small and fixed, explicit nullable FKs per type (with a check constraint) are often simpler and JOIN-able.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`select_related('target')` works on a GFK." It doesn't — GFKs can't be joined.
- "A GFK prefetch is one query." It's one per content type.
- Missing the `(content_type, object_id)` index — reverse generic lookups then scan.
- Forgetting the targets' own relations → N+1 inside each type.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | A few queries per page | Small | ACCESS SHARE only |
| **Medium** | 1M | Composite `(content_type_id, object_id)` index essential | Per-type caches | ACCESS SHARE only |
| **Large** | 100M | Denormalise list fields; resolve targets only on detail | — | ACCESS SHARE only |
| **Massive** | 1B+ | Feed tables partitioned by time; fan-out-on-write feeds | — | — |

# Follow-up Questions

1. How many queries does a GFK prefetch over 5 content types run?
2. What does `GenericPrefetch` add over a plain `prefetch_related('target')`?
3. When would you replace a GFK with explicit foreign keys?

# Related Topics

* Module 02 Q17 — cost of GenericForeignKeys
* Module 02 Q29 — django-polymorphic
* Module 18 Q9 — architectural trade-offs of GFKs

---

# Question

How do you identify slow Django queries using PostgreSQL pg_stat_statements?

# Why Interviewer Asks This

Production query analysis is a senior responsibility. The interviewer wants to know how the extension aggregates queries, which columns you sort by and why (total vs. mean vs. calls), how you tie normalised SQL back to Django code, and how you use it before/after a fix.

# Answer

**Spoken answer:** "`pg_stat_statements` records every statement the server runs, normalised — literals replaced by `$1`, `$2` — and aggregates per query shape: number of calls, total and mean execution time, rows, and buffer hits versus reads. I look at it three ways. Sorted by *total* time, it shows what's costing the database the most overall — often a fast query called millions of times. Sorted by *mean* time, it shows individually slow queries. And very high call counts with tiny means are the production fingerprint of an N+1. To map a normalised query back to Django code, I recognise the table and column pattern, and we tag queries with a comment for the route or job name. After a fix I reset or snapshot the stats and compare."

**The reasoning:**
- Total time → where the DB spends its capacity (fix these first).
- Mean time → individually slow queries (index/plan problems).
- Calls → N+1 and chatty code.
- `shared_blks_read` vs `shared_blks_hit` → disk I/O vs. cache.

# Internal ORM Mechanics

The extension (loaded via `shared_preload_libraries`, then `CREATE EXTENSION pg_stat_statements`) hooks the executor and keys statistics by `queryid`, a hash of the parsed query tree — so comments and literal values don't create separate entries; the stored text is the first-seen variant. On the Django side, queries are already parameterised by the driver, so each ORM call site produces one stable shape. `connection.execute_wrapper()` lets you wrap every query a connection runs — the hook for adding a route/job tag comment (visible in `pg_stat_activity` and slow-query logs; in `pg_stat_statements` you see whichever tagged variant arrived first).

# SQL Generated

```sql
-- top offenders by total time (PG13+ column names)
SELECT queryid,
       calls,
       round(total_exec_time::numeric, 1)  AS total_ms,
       round(mean_exec_time::numeric, 2)   AS mean_ms,
       rows,
       shared_blks_read,
       left(query, 120)                    AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- N+1 fingerprints: many calls, tiny mean
SELECT calls, round(mean_exec_time::numeric, 3) AS mean_ms, left(query, 120)
FROM pg_stat_statements
WHERE calls > 100000 AND mean_exec_time < 1
ORDER BY calls DESC LIMIT 20;

SELECT pg_stat_statements_reset();   -- start a clean measurement window (needs privileges)
```

# Code Example

```python
# middleware.py — tag every query with the route so logs and pg_stat_activity show the call site
from django.db import connections

class QueryTagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        route = getattr(request.resolver_match, 'view_name', None) or request.path
        def tagger(execute, sql, params, many, context):
            return execute(f'/* route={route} */ {sql}', params, many, context)
        with connections['default'].execute_wrapper(tagger):
            return self.get_response(request)

# Same idea for cron jobs: wrap the job body with a job=<name> tagger
```

(`request.resolver_match` is only set after URL resolution; in middleware that runs before the view, fall back to the path or set the tag in a view decorator.)

# Production Scenario

**From experience (STAR):** **S** — PNI Hub's PostgreSQL instance showed rising CPU at [fill-in]% during business hours with no single slow endpoint in APM. **T** — Find what was actually consuming the database. **A** — `pg_stat_statements` sorted by total time showed the top entry was a permission lookup called [fill-in] times per hour with a sub-millisecond mean — an N+1 in the RBAC check — and the second was a dashboard aggregate with a [fill-in] ms mean. I fixed the first with per-request role caching, the second with a composite index, then reset the stats and compared a day later. **R** — DB CPU dropped to [fill-in]%, and the top-20 list became our weekly performance review input.

# Performance Impact

- The extension's overhead is small and widely accepted in production; `track_planning` adds more.
- Reading the view is cheap; resetting it loses history — snapshot to a table first if you want trends.

**Trade-offs / when NOT to use it:**
- It aggregates — it can't show you one specific slow execution or its parameters; pair it with `log_min_duration_statement` / `auto_explain`.
- On SQL Server, the equivalent is Query Store / `sys.dm_exec_query_stats`.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Sort by mean time and fix the top one." You may optimise a rare query while a hot one burns the CPU — check total time too.
- "Comments split the stats per route." `queryid` ignores comments; use logs for per-call attribution.
- "It shows parameter values." It shows normalised placeholders.
- Never resetting/snapshotting — the numbers then mix months of old code paths.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Little signal — everything is fast | Fixed shared memory (`pg_stat_statements.max`) | — |
| **Medium** | 1M | Total-time ranking finds hot paths | — | — |
| **Large** | 100M | Combine with `auto_explain` for plans of slow calls | Raise `.max` if entries are evicted | — |
| **Massive** | 1B+ | Ship snapshots to monitoring for trends and regressions per deploy | — | — |

# Follow-up Questions

1. Why rank by total time rather than mean time?
2. How would you map a normalised query back to the Django code that issued it?
3. What do you use alongside `pg_stat_statements` to see an individual slow execution?

# Related Topics

* Module 19 Q1 — identifying slow ORM queries in production
* Module 19 Q6 — tracing a query to its line of code
* Module 06 Q14 — django-debug-toolbar in development

---

# Question

How do you catch and prevent N+1 query regressions automatically in tests and CI?

# Why Interviewer Asks This

Fixing an N+1 once is easy; keeping it fixed as a team ships features is the senior skill. The interviewer wants concrete tooling (`assertNumQueries`, `CaptureQueriesContext`, pytest-django fixtures) and, crucially, a test design that detects *scaling* query counts rather than brittle exact numbers.

# Answer

**Spoken answer:** "I make query counts part of the test suite. Django's `assertNumQueries` and `CaptureQueriesContext`, or pytest-django's `django_assert_num_queries` fixture, let me assert how many queries a block of code runs. The trick is what to assert. An exact number like 'seven' breaks every time someone adds a harmless query. What really matters for N+1 is that the count doesn't grow with the data, so for key endpoints I run the request with two rows, then with twenty, and assert the counts are equal. In development I also log a warning when a request exceeds a query budget. Together that catches N+1s in code review instead of in production."

**The reasoning:**
- N+1 = query count proportional to rows → test the *slope*, not just the number.
- Exact-count assertions are fine for small, stable units (a manager method), brittle for whole endpoints.
- Multi-database: count per alias (`assertNumQueries(n, using='ods')`) and declare `databases` on the test case.
- Dev-time signals: a query-budget middleware, django-debug-toolbar, or packages like nplusone.

# Internal ORM Mechanics

`CaptureQueriesContext(connection)` forces `connection.force_debug_cursor = True` for the block, so the connection records every executed statement in `connection.queries_log` even with `DEBUG=False`; on exit it exposes `captured_queries`. `TestCase.assertNumQueries(num, func=None, *args, using='default')` wraps the same context manager and fails with the list of captured SQL — which makes the failure message actionable. Each alias is a separate connection, so queries on another alias are counted separately.

# SQL Generated

No new SQL — the point is to *count* what's emitted. A failing assertion prints something like:

```text
AssertionError: 23 != 3 : 23 queries executed, 3 expected
Captured queries were:
1. SELECT ... FROM "pni_integration" ...
2. SELECT ... FROM "auth_user" WHERE "auth_user"."id" = 4 LIMIT 21
3. SELECT ... FROM "auth_user" WHERE "auth_user"."id" = 9 LIMIT 21
...
```

# Code Example

```python
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

class IntegrationListQueryBudgetTests(TestCase):
    databases = {'default'}

    def setUp(self):
        self.client.force_login(UserFactory())

    def _queries_for_list(self):
        with CaptureQueriesContext(connection) as ctx:
            resp = self.client.get('/api/integrations/')
            self.assertEqual(resp.status_code, 200)
        return len(ctx.captured_queries)

    def test_query_count_does_not_scale_with_rows(self):
        IntegrationFactory.create_batch(2, with_tags=3)
        small = self._queries_for_list()
        IntegrationFactory.create_batch(20, with_tags=3)
        self.assertEqual(self._queries_for_list(), small)   # flat → no N+1

    def test_manager_method_exact_count(self):
        IntegrationFactory.create_batch(5)
        with self.assertNumQueries(2):                       # base query + one prefetch
            list(Integration.objects.with_owner_and_tags())

# pytest-django equivalent
def test_list_budget(client, django_assert_max_num_queries):
    with django_assert_max_num_queries(6):
        client.get('/api/integrations/')
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub has [fill-in] DRF endpoints maintained by several developers; N+1s kept reappearing after serializer changes. **T** — Make regressions fail in CI rather than show up as latency alerts. **A** — I added "flat query count" tests (2 rows vs. 20 rows) for the [fill-in] highest-traffic endpoints, exact-count tests for shared QuerySet methods, and a dev-only middleware that logs any request over [fill-in] queries with the top repeated SQL. **R** — the tests caught [fill-in] N+1 regressions in PRs over [fill-in] months; production N+1 incidents dropped to [fill-in].

# Performance Impact

- Test overhead is negligible — queries are recorded in memory for the block only.
- The real impact is upstream: performance regressions are caught at PR time.

**Trade-offs / when NOT to use it:**
- Exact counts on whole endpoints create churn — prefer "flat with data" or a max budget.
- Query counts don't catch *slow* queries; pair with EXPLAIN checks or staging benchmarks for heavy endpoints.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "We find N+1s with the debug toolbar." Only if someone looks — tests make it automatic.
- Asserting exact counts everywhere, then disabling the tests because they're "flaky".
- Testing with one row — a single row can't reveal N+1.
- Forgetting queries on secondary aliases (`using=`) in multi-DB code.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Tests use 2 vs. 20 rows — enough to expose the slope | Negligible | Test DB, transactional rollback |
| **Medium** | 1M | Add a query budget per endpoint in staging | — | — |
| **Large** | 100M | Combine with `pg_stat_statements` call counts in prod | — | — |
| **Massive** | 1B+ | Track queries-per-request as an SLO metric in APM | — | — |

# Follow-up Questions

1. Why is "the count must not change with row count" a better assertion than an exact number?
2. How do you count queries on a second database alias in a test?
3. How would you surface N+1s in development without tests?

# Related Topics

* Module 06 Q14 — django-debug-toolbar
* Module 06 Q37 — N+1 in DRF serializers
* Module 05 Q24 — testing custom managers and querysets

---

# Question

How do you eliminate N+1 queries in DRF serializers (nested serializers, SerializerMethodField, source='fk.field')?

# Why Interviewer Asks This

This is where most real-world Django N+1s live. The interviewer wants you to explain why serializers cause them, where the fix belongs (the view's `get_queryset()`), and a pattern that keeps the serializer and the queryset in sync as fields change.

# Answer

**Spoken answer:** "Serializers don't know anything about querysets — they just read attributes off each object. So every `source='owner.name'`, every nested serializer, every related field and every `SerializerMethodField` that touches a relation becomes a lazy query per object. The fix belongs in the view's `get_queryset()`: `select_related` for single-valued paths like `owner`, `prefetch_related` for many-valued ones like `tags`, and `annotate` for anything that's really a count or a flag, instead of computing it in a method field. To stop the two from drifting apart, I put a `setup_eager_loading` class method on the serializer that the view always calls — so whoever adds a field also adds the loading. And a query-count test on the endpoint locks it in."

**The reasoning:**
- Per-object attribute access is the N+1 source: `source='fk.x'`, nested serializers, `StringRelatedField` (`__str__`), `PrimaryKeyRelatedField(many=True)`, `SerializerMethodField`.
- Fix in `get_queryset()`; pagination slices first, so the prefetch runs only for the page.
- Counts and booleans → annotations exposed as read-only fields.
- Also watch per-object permission checks (`has_object_permission`) and hyperlinked fields.

# Internal ORM Mechanics

`ListSerializer.to_representation()` iterates the (already paginated) queryset and calls the child serializer's `to_representation()` per object; each field's `get_attribute()` walks the `source` path with `getattr`, which triggers the FK descriptor (one query if not cached) or the related manager (`.all()` → one query unless prefetched). DRF's `GenericAPIView.paginate_queryset()` slices the queryset before evaluation, so `prefetch_related` lookups apply only to the page's objects — the `IN` list is page-sized.

# SQL Generated

```python
Integration.objects.select_related('owner').prefetch_related('tags').annotate(
    open_incidents=Count('incidents', filter=Q(incidents__resolved_at__isnull=True)))
```

```sql
SELECT "pni_integration"."id", "pni_integration"."name", "pni_integration"."status", "pni_integration"."owner_id",
       COUNT("pni_incident"."id") FILTER (WHERE "pni_incident"."resolved_at" IS NULL) AS "open_incidents",
       "auth_user"."id", "auth_user"."first_name", "auth_user"."last_name"
FROM "pni_integration"
INNER JOIN "auth_user" ON ("pni_integration"."owner_id" = "auth_user"."id")
LEFT OUTER JOIN "pni_incident" ON ("pni_integration"."id" = "pni_incident"."integration_id")
GROUP BY "pni_integration"."id", "auth_user"."id"
ORDER BY "pni_integration"."name" ASC
LIMIT 50;

SELECT ("pni_integration_tags"."integration_id") AS "_prefetch_related_val_integration_id", "pni_tag"."id", "pni_tag"."name"
FROM "pni_tag" INNER JOIN "pni_integration_tags" ON ("pni_tag"."id" = "pni_integration_tags"."tag_id")
WHERE "pni_integration_tags"."integration_id" IN (1, 2, 3 /* …this page only */);
```

# Code Example

```python
from django.db.models import Count, Q
from rest_framework import serializers, viewsets

class IntegrationSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)        # FK path
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')        # M2M
    open_incidents = serializers.IntegerField(read_only=True)                                # annotation

    class Meta:
        model = Integration
        fields = ['id', 'name', 'status', 'owner_name', 'tags', 'open_incidents']

    @classmethod
    def setup_eager_loading(cls, queryset):
        return (queryset
                .select_related('owner')
                .prefetch_related('tags')
                .annotate(open_incidents=Count('incidents', filter=Q(incidents__resolved_at__isnull=True))))

class IntegrationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IntegrationSerializer

    def get_queryset(self):
        qs = Integration.objects.filter(business_unit__in=self.request.user.allowed_business_units())
        return self.get_serializer_class().setup_eager_loading(qs).order_by('name')

# Anti-pattern this replaces:
#   open_incidents = serializers.SerializerMethodField()
#   def get_open_incidents(self, obj):
#       return obj.incidents.filter(resolved_at__isnull=True).count()     # 1 query per row
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub's main integrations endpoint is consumed by the React dashboard and by [fill-in] internal tools, and returns owner, tags, endpoint count and open-incident count per integration. **T** — It made [fill-in] queries for a 50-row page, mostly from `SerializerMethodField`s and a `source='owner.email'`. **A** — I moved counts to annotations, added `setup_eager_loading` on the serializer and called it from `get_queryset`, and added a "flat query count" test. **R** — queries per page went from [fill-in] to [fill-in] (constant), p95 from [fill-in] to [fill-in] ms, and later field additions came with their loading in the same PR.

# Performance Impact

- Queries per page: O(rows × relations) → O(1) per relation.
- Annotations move counting into the DB — no child rows shipped.
- Prefetch size is bounded by page size because DRF paginates before evaluating.

**Trade-offs / when NOT to use it:**
- Two `Count`s over different multi-valued relations in one query inflate each other — use `distinct=True` or `Subquery` counts.
- Don't eagerly load data for fields that are excluded by a `?fields=` sparse-fieldset feature — make `setup_eager_loading` field-aware if you have one.
- Writable nested serializers have separate concerns (validation, transactions) — keep read optimisation in read paths.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Add `select_related` in the serializer." Serializers don't build querysets — the view does.
- "`SerializerMethodField` is fine for counts." It's a query per row unless backed by an annotation or prefetch.
- Forgetting `StringRelatedField`/`__str__` touches FKs.
- Optimising `list` but not `retrieve`, or the reverse — both go through `get_queryset()`.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | N+1 already visible on a 50-row page | Small | ACCESS SHARE only |
| **Medium** | 1M | Pagination mandatory; eager loading per page | Bounded by page | ACCESS SHARE only |
| **Large** | 100M | Use keyset/cursor pagination; annotate rather than prefetch large child sets | Bounded | ACCESS SHARE only |
| **Massive** | 1B+ | Serve list views from a read model / search index | — | Replicas |

# Follow-up Questions

1. Why is the view, not the serializer, the right place to optimise queries?
2. How do you keep `get_queryset()` in sync with serializer fields as they change?
3. What goes wrong with two `Count` annotations on different relations?

# Related Topics

* Module 06 Q1 — select_related vs prefetch_related
* Module 06 Q36 — query-count tests in CI
* Module 09 Q4 — multiple annotations without double counting

---

# Question

Why does filtering across a multi-valued relationship return duplicate rows, and what is the cost of distinct() versus Exists?

# Why Interviewer Asks This

A very common production bug: lists showing the same object twice, wrong counts, broken pagination. The interviewer wants the JOIN-level explanation, what `distinct()` really costs, and the better semi-join alternatives. (Module 10 Q3 covers `Exists` itself; this is about the duplicate problem.)

# Answer

**Spoken answer:** "When you filter through a one-to-many or many-to-many relation — `Project.objects.filter(tickets__status='open')` — Django has to JOIN the tickets table, and SQL returns one row per matching ticket. A project with five open tickets appears five times. `distinct()` hides that, but it makes the database de-duplicate the whole result set — a sort or hash over every selected column — and it interacts badly with ordering by related fields and with counting. The better fix is to express what you actually mean, which is 'projects where an open ticket *exists*': an `Exists` subquery or `pk__in` a subquery. That's a semi-join — the database stops at the first match per project, and there are no duplicates to remove."

**The reasoning:**
- JOIN to a multi-valued relation = one row per related match.
- `distinct()` = extra de-duplication over all selected columns; more expensive with wide rows.
- `Exists` / `__in` subquery = semi-join, no duplicates, often a better plan.
- Separate `.filter()` calls on the same multi-valued relation create separate JOINs (different matching rows); one `.filter()` with both conditions means "the same related row".

# Internal ORM Mechanics

A lookup that traverses a reverse FK or M2M sets up a JOIN with `m2m=True` (multi-valued) in `Query.setup_joins()`. Django doesn't de-duplicate these rows itself. `distinct()` sets `query.distinct = True` → `SELECT DISTINCT` over the full select list; if you `order_by()` a field not in the select list, Django adds it to the SELECT, which can change what "distinct" means. `count()` on a distinct query wraps it in a subquery. `Exists(...)` compiles to `EXISTS (SELECT 1 ... LIMIT 1)` and `filter(pk__in=qs.values('project_id'))` to `IN (SELECT ...)`, both of which planners execute as semi-joins.

# SQL Generated

```python
Project.objects.filter(tickets__status='open')
Project.objects.filter(tickets__status='open').distinct()
Project.objects.filter(Exists(Ticket.objects.filter(project=OuterRef('pk'), status='open')))
```

```sql
-- duplicates: one row per open ticket
SELECT "pm_project"."id", "pm_project"."name" FROM "pm_project"
INNER JOIN "pm_ticket" ON ("pm_project"."id" = "pm_ticket"."project_id")
WHERE "pm_ticket"."status" = 'open';

-- distinct: join, then de-duplicate everything
SELECT DISTINCT "pm_project"."id", "pm_project"."name" FROM "pm_project"
INNER JOIN "pm_ticket" ON ("pm_project"."id" = "pm_ticket"."project_id")
WHERE "pm_ticket"."status" = 'open';

-- semi-join: no duplicates, stops at first match per project
SELECT "pm_project"."id", "pm_project"."name" FROM "pm_project"
WHERE EXISTS (SELECT 1 AS "a" FROM "pm_ticket" U0
              WHERE (U0."project_id" = ("pm_project"."id") AND U0."status" = 'open') LIMIT 1);
```

# Code Example

```python
from django.db.models import Exists, OuterRef

# Bug: duplicates, and wrong counts
Project.objects.filter(tickets__status='open').count()        # counts tickets, not projects!

# Works, but pays for DISTINCT
Project.objects.filter(tickets__status='open').distinct()

# Preferred: say what you mean
open_tickets = Ticket.objects.filter(project=OuterRef('pk'), status='open')
Project.objects.filter(Exists(open_tickets))

# Equivalent IN-subquery form
Project.objects.filter(pk__in=Ticket.objects.filter(status='open').values('project_id'))

# Semantics trap with multi-valued relations:
Project.objects.filter(tickets__status='open', tickets__priority='high')            # SAME ticket is open AND high
Project.objects.filter(tickets__status='open').filter(tickets__priority='high')     # an open ticket AND (maybe another) high ticket — two JOINs
```

# Production Scenario

**From experience (STAR):** **S** — PNI Hub's integration search let users filter by tag and by "has failed runs in the last 24h". **T** — Users reported integrations appearing several times and page totals that didn't match; someone had added `.distinct()`, which then made the query take [fill-in] s because the select list included a JSON config column. **A** — I replaced both relation filters with `Exists` subqueries, removed `distinct()`, and added an index on `(integration_id, status, started_at)` for the runs subquery. **R** — duplicates gone, counts correct, and the query dropped from [fill-in] s to [fill-in] ms.

# Performance Impact

- JOIN + duplicates: more rows transferred, wrong counts, unstable pagination.
- `DISTINCT`: sort/hash over every selected column; worse with wide rows or many matches per parent.
- `EXISTS`/`IN` semi-join: one probe per parent, early exit — with an index on the child FK + filter columns.

**Trade-offs / when NOT to use it:**
- If you also need *data* from the related rows, a JOIN (or prefetch) is appropriate — but then aggregate or prefetch instead of de-duplicating.
- `distinct()` is reasonable for small result sets where readability wins.
- PostgreSQL's `distinct('field')` (DISTINCT ON) is the right tool for "latest per group", not for this problem.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "Django removes duplicates automatically." It doesn't.
- "`distinct()` is free." It's an extra de-duplication step over all columns.
- "Two chained `.filter()` calls equal one `.filter()` with both conditions." Not for multi-valued relations.
- Using `.count()` on the duplicated queryset and reporting it as a number of parents.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | `distinct()` is fine | Trivial | ACCESS SHARE only |
| **Medium** | 1M | Duplicates multiply transfer; DISTINCT sort becomes visible | Sort memory | ACCESS SHARE only |
| **Large** | 100M | `Exists` with a composite child index is far cheaper than JOIN + DISTINCT | DISTINCT may spill to disk | ACCESS SHARE only |
| **Massive** | 1B+ | Denormalised flags (e.g. `has_failed_runs`) maintained by jobs | — | — |

# Follow-up Questions

1. Why do two chained `.filter()` calls on a multi-valued relation behave differently from one?
2. Why can `distinct()` combined with `order_by('related__field')` still return duplicates?
3. When is `IN (subquery)` better or worse than `EXISTS`?

# Related Topics

* Module 10 Q3 — `Exists` vs `filter(related__isnull=False)`
* Module 07 Q11 — join reuse when chaining filters
* Module 10 Q22 — IN vs EXISTS vs JOIN

---

# Question

How do you avoid per-row get() or update_or_create() calls in data-sync jobs (in_bulk, dictionary lookups, bulk upserts)?

# Why Interviewer Asks This

Integration and sync jobs are where "query in a loop" quietly costs hours. The interviewer wants the cost of the naive loop, the load-once/diff/bulk-write pattern, database upserts with `bulk_create(update_conflicts=True)`, and the concurrency and idempotency concerns that come with them.

# Answer

**Spoken answer:** "The naive sync loop — for each external record, `update_or_create()` — costs two or three queries per record, inside its own transaction, with a `SELECT ... FOR UPDATE`. For thirty thousand records that's tens of thousands of round-trips. The pattern I use instead: for each chunk of incoming records, load all the existing rows in one query with `in_bulk(keys, field_name='external_code')`, which gives me a dict; diff in Python to split into new rows and rows that actually changed; then write with one `bulk_create` and one `bulk_update`. On PostgreSQL I can go further and use a real upsert — `bulk_create(update_conflicts=True, unique_fields=[...], update_fields=[...])` — which is `INSERT ... ON CONFLICT DO UPDATE` and is also safe against concurrent inserts. Plus a unique constraint on the natural key, so the job is idempotent."

**The reasoning:**
- `update_or_create` per row = SELECT FOR UPDATE + UPDATE/INSERT per row, in a transaction each.
- Load-once/diff/bulk-write = ~3 queries per chunk; skipping unchanged rows avoids pointless writes (and WAL).
- DB upsert = 1 statement per batch, race-safe via the unique constraint.
- Chunk keys to respect parameter limits (SQL Server ~2,100).

# Internal ORM Mechanics

`update_or_create()` opens `transaction.atomic()`, runs `select_for_update().get(**lookup)`, then either `save(update_fields=...)` or `create()` (with an `IntegrityError` retry path). `in_bulk(id_list, field_name=...)` runs one `filter(field__in=...)` query (batched automatically if the backend has a parameter limit) and returns `{key: instance}`; `field_name` must be unique (a field with `unique=True` or a single-field unconditional `UniqueConstraint`). `bulk_create(update_conflicts=True, ...)` compiles via the backend's `on_conflict_suffix_sql()` to `ON CONFLICT (...) DO UPDATE SET col = EXCLUDED.col` and, in Django 5.0+, returns PKs on PostgreSQL.

# SQL Generated

```sql
-- naive loop: per record
BEGIN;
SELECT ... FROM "finance_costcentre" WHERE "finance_costcentre"."code" = 'CC-1001' LIMIT 21 FOR UPDATE;
UPDATE "finance_costcentre" SET "name" = ..., "owner_email" = ... WHERE "finance_costcentre"."id" = 17;
COMMIT;

-- chunked: one load query
SELECT ... FROM "finance_costcentre" WHERE "finance_costcentre"."code" IN ('CC-1001', 'CC-1002', /* … */);

-- or a single upsert per batch (PostgreSQL)
INSERT INTO "finance_costcentre" ("code", "name", "owner_email")
VALUES ('CC-1001', 'Plant Ops', 'a@corp.example'), ('CC-1002', 'R&D', 'b@corp.example')
ON CONFLICT("code") DO UPDATE SET "name" = EXCLUDED."name", "owner_email" = EXCLUDED."owner_email"
RETURNING "finance_costcentre"."id";
```

# Code Example

```python
from itertools import islice
from django.db import transaction

def chunked(iterable, size):
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch

class CostCentre(models.Model):
    code = models.CharField(max_length=20, unique=True)      # natural key from the source system
    name = models.CharField(max_length=200)
    owner_email = models.EmailField()

def sync_cost_centres(source_rows, chunk=1000):
    created = updated = 0
    for batch in chunked(source_rows, chunk):
        existing = CostCentre.objects.in_bulk([r['code'] for r in batch], field_name='code')
        to_create, to_update = [], []
        for r in batch:
            obj = existing.get(r['code'])
            if obj is None:
                to_create.append(CostCentre(code=r['code'], name=r['name'], owner_email=r['owner']))
            elif (obj.name, obj.owner_email) != (r['name'], r['owner']):     # write only real changes
                obj.name, obj.owner_email = r['name'], r['owner']
                to_update.append(obj)
        with transaction.atomic():
            CostCentre.objects.bulk_create(to_create, batch_size=500)
            CostCentre.objects.bulk_update(to_update, ['name', 'owner_email'], batch_size=500)
        created, updated = created + len(to_create), updated + len(to_update)
    return created, updated

# PostgreSQL: race-safe upsert in one statement per batch
def upsert_cost_centres(source_rows):
    for batch in chunked(source_rows, 1000):
        CostCentre.objects.bulk_create(
            [CostCentre(code=r['code'], name=r['name'], owner_email=r['owner']) for r in batch],
            update_conflicts=True, unique_fields=['code'], update_fields=['name', 'owner_email'])
```

# Production Scenario

**From experience (STAR):** **S** — One of PNI Hub's django-crontab sync jobs mirrors reference data from the MSSQL ODS into PostgreSQL every [fill-in] minutes. **T** — It used `update_or_create()` per record — [fill-in] queries per run and [fill-in] minutes of runtime — and runs overlapped when the ODS was slow, causing lock waits. **A** — I rewrote it as read-chunk-from-ODS → `in_bulk` → diff → `bulk_create`/`bulk_update` (only changed rows), added a unique constraint on the source code, and guarded the job with a Redis lock so two runs can't overlap. **R** — runtime dropped from [fill-in] to [fill-in] s, write volume fell by [fill-in]% because unchanged rows are skipped, and overlap-related lock waits disappeared.

# Performance Impact

- Round-trips: ~2–3 per record → ~3 per chunk (or 1 with upsert).
- Writes: only changed rows → less WAL, less index churn, less replica lag.
- Memory: one chunk of source rows + existing instances.

**Trade-offs / when NOT to use it:**
- The diff-in-Python approach has a race window between `in_bulk` and `bulk_create` — a concurrent insert raises `IntegrityError`; use the upsert or a job-level lock.
- `bulk_*` skip `save()` and signals — any history/audit hooks must be explicit.
- Upsert support and syntax differ by backend; on SQL Server I use a staging table + `MERGE` in raw SQL if the backend doesn't support `update_conflicts`.

# Common Mistakes

**Common wrong answers interviewers hear:**
- "`update_or_create` is one query." It's a locked SELECT plus a write, in a transaction, per call.
- "`ignore_conflicts=True` handles updates." It silently skips existing rows.
- Re-writing every row every run, even when nothing changed.
- No unique constraint on the natural key — duplicates creep in when runs overlap.

# Scaling Considerations

| Dataset Scale | Row Count | Execution Time | Memory Footprint | Database Lock Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 1K | Even the naive loop is tolerable — but the pattern costs nothing extra | Trivial | Row locks per write |
| **Medium** | 1M | Chunked diff/upsert; skip unchanged rows | Bounded per chunk | Row locks per batch; job-level lock to avoid overlaps |
| **Large** | 100M | Delta feeds (changed-since watermark) instead of full scans of the source | Bounded | Short transactions; watch replica lag |
| **Massive** | 1B+ | CDC from the source + idempotent upserts | — | Partition-aware batches |

# Follow-up Questions

1. Why does `update_or_create` use `select_for_update`, and what does that cost in a loop?
2. How do you make a sync job safe if two runs overlap?
3. How would you do an upsert on a backend without `ON CONFLICT` support?

# Related Topics

* Module 06 Q8 — `bulk_create()` and conflict handling
* Module 06 Q7 — `bulk_update()`
* Module 15 Q14 — concurrency in background workers

---
