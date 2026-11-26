# Module 09: Aggregation & Annotation (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/09_Aggregation_and_Annotation.md)

## Table of Contents
1. (Easy) [What is the difference between aggregate() and annotate()?](#q1)
2. (Easy) [How does Django translate annotate() into SQL GROUP BY clauses?](#q2)
3. (Easy) [What is the difference between Count('field') and Count('field', distinct=True)?](#q3)
4. (Medium) [How do you combine multiple annotations on the same queryset without duplicate counting?](#q4)
5. (Medium) [How does Django decide which columns to include in the GROUP BY clause?](#q5)
6. (Easy) [How do you filter annotated values using filter() after annotate()?](#q6)
7. (Medium) [What is the SQL difference when placing filter() before vs. after annotate()?](#q7)
8. (Medium) [How do you perform conditional aggregation using Case and When?](#q8)
9. (Easy) [How does Django handle aggregation over reverse relation querysets?](#q9)
10. (Medium) [What is the performance cost of performing aggregate functions on large tables?](#q10)
11. (Medium) [How do you aggregate JSONField values in Django ORM?](#q11)
12. (Medium) [How do you use Window functions in Django annotations?](#q12)
13. (Medium) [What are window functions (e.g., RowNumber, Rank, Lead, Lag) and how do they compile?](#q13)
14. (Easy) [How do you partition window functions using the partition_by argument?](#q14)
15. (Easy) [How do you order window functions using the order_by argument?](#q15)
16. (Easy) [What is the database backend support variance for window functions?](#q16)
17. (Medium) [How do you write a custom aggregate function in Django?](#q17)
18. (Easy) [How does Django handle NULL values in aggregate operations (e.g., Coalesce)?](#q18)
19. (Medium) [How do you calculate running totals using Django ORM?](#q19)
20. (Medium) [What are the risks of using ordering in model Meta when grouping data?](#q20)
21. (Medium) [How do you annotate a queryset with data from a related model using Subquery?](#q21)
22. (Easy) [Explain how to use Count with the filter argument (conditional counting).](#q22)
23. (Medium) [How do you annotate a queryset with a list of related primary keys?](#q23)
24. (Medium) [What are the performance implications of deep joins within annotations?](#q24)
25. (Medium) [How does Django 5.0 optimize annotations containing GeneratedField?](#q25)
26. (Medium) [How do you write an annotation that calculates string concatenation across rows?](#q26)
27. (Hard) [Explain how window function frame clauses compile in Django.](#q27)
28. (Medium) [What is the difference between Sum and Avg performance on large datasets?](#q28)
29. (Medium) [How do you write an annotation that filters out duplicates using distinct values?](#q29)
30. (Medium) [How do you annotate a query with date differences in days?](#q30)
31. (Hard) [How does Django aggregate over polymorphic models?](#q31)
32. (Medium) [What is the performance cost of filtering an annotated column?](#q32)
33. (Hard) [How do you write a custom window function in Django?](#q33)
34. (Hard) [Explain the compile timeline for complex annotations.](#q34)
35. (Medium) [How do you write aggregate queries that exclude specific rows using a negative filter?](#q35)

---

<a name="q1"></a>
## Q1. (Easy) What is the difference between aggregate() and annotate()?
**Answer:** `aggregate()` returns **one dict** summarising the whole queryset (`{"total": 5000}`) and ends the chain. `annotate()` adds a computed value **to each row** and returns a queryset you can keep filtering/ordering.

```python
Order.objects.aggregate(total=Sum("amount"))                 # {'total': Decimal('5000')}
Customer.objects.annotate(order_count=Count("orders"))       # each customer.order_count
```

---

<a name="q2"></a>
## Q2. (Easy) How does Django translate annotate() into SQL GROUP BY clauses?
**Answer:** An aggregate annotation needs grouping:
- `Model.objects.annotate(...)` → `GROUP BY` the model's columns (on PostgreSQL just its pk).
- `values("field").annotate(...)` → `GROUP BY field` (one row per distinct value).

```python
Order.objects.values("status").annotate(n=Count("id"))
# SELECT status, COUNT(id) AS n FROM shop_order GROUP BY status
```

---

<a name="q3"></a>
## Q3. (Easy) What is the difference between Count('field') and Count('field', distinct=True)?
**Answer:** `Count("x")` counts all non-NULL values (including duplicates). `distinct=True` counts unique values only — needed when joins duplicate rows, e.g. counting authors of books when the query also joins tags.

---

<a name="q4"></a>
## Q4. (Medium) How do you combine multiple annotations on the same queryset without duplicate counting?
**Answer:** Two aggregates over **different multi-valued relations** multiply each other (JOIN fan-out): 3 books × 4 reviews = 12 for both counts.

```python
Author.objects.annotate(books=Count("books"), reviews=Count("reviews"))   # wrong
Author.objects.annotate(books=Count("books", distinct=True),
                        reviews=Count("reviews", distinct=True))          # fine for counts
```
For `Sum`/`Avg`, `distinct` doesn't help — use a `Subquery` per aggregate.

---

<a name="q5"></a>
## Q5. (Medium) How does Django decide which columns to include in the GROUP BY clause?
**Answer:** It groups by everything in the SELECT that isn't an aggregate: the `values()` fields, or all model columns (collapsed to the pk on PostgreSQL, where other columns depend on it). Non-aggregate annotations and `order_by` fields can also be added to GROUP BY — which can change your groups unexpectedly. Meta ordering is ignored for GROUP BY since Django 3.1.

---

<a name="q6"></a>
## Q6. (Easy) How do you filter annotated values using filter() after annotate()?
**Answer:** Filtering on the annotation becomes a `HAVING` clause.

```python
Customer.objects.annotate(n=Count("orders")).filter(n__gte=5)
# ... GROUP BY customer.id HAVING COUNT(orders.id) >= 5
```

---

<a name="q7"></a>
## Q7. (Medium) What is the SQL difference when placing filter() before vs. after annotate()?
**Answer:** `filter()` **before** `annotate()` → `WHERE` — limits which rows are aggregated. `filter()` **after** on the annotation → `HAVING` — filters the groups.

```python
Customer.objects.filter(orders__status="paid").annotate(n=Count("orders"))  # counts only paid orders
Customer.objects.annotate(n=Count("orders")).filter(n__gt=0)                # filter on the count
```
**Gotcha:** a filter on the relation *after* annotate may add a second join and change counts.

---

<a name="q8"></a>
## Q8. (Medium) How do you perform conditional aggregation using Case and When?
**Answer:** Usually `filter=` on the aggregate is simpler; `Case/When` is useful for weighted or mapped values.

```python
Order.objects.aggregate(
    paid=Count("id", filter=Q(status="paid")),
    weighted=Sum(Case(When(priority="high", then=Value(2)), default=Value(1))),
)
```

---

<a name="q9"></a>
## Q9. (Easy) How does Django handle aggregation over reverse relation querysets?
**Answer:** Use the reverse name in the aggregate; Django adds a LEFT JOIN + GROUP BY.

```python
Customer.objects.annotate(total_spent=Sum("orders__amount"))
customer.orders.aggregate(Sum("amount"))     # for one object
```
Customers without orders get `None` — use `default=0` or `Coalesce`.

---

<a name="q10"></a>
## Q10. (Medium) What is the performance cost of performing aggregate functions on large tables?
**Answer:** Aggregates read every matching row (often a full scan) and may sort or hash for GROUP BY — on huge tables that's seconds and lots of I/O. Reduce it with selective `WHERE` + indexes (index-only scans), aggregate on a time window, or pre-aggregate into summary tables / materialized views refreshed by a job.

---

<a name="q11"></a>
## Q11. (Medium) How do you aggregate JSONField values in Django ORM?
**Answer:** Extract the key, cast it to a number, then aggregate.

```python
from django.db.models.fields.json import KeyTextTransform
Event.objects.annotate(amount=Cast(KeyTextTransform("amount", "payload"), DecimalField())) \
             .aggregate(total=Sum("amount"))
```
If you aggregate a JSON key often, move it to a real column (or GeneratedField).

---

<a name="q12"></a>
## Q12. (Medium) How do you use Window functions in Django annotations?
**Answer:** Wrap a function in `Window(...)` — it computes a value per row over a group **without collapsing rows** (unlike GROUP BY).

```python
from django.db.models import Window
from django.db.models.functions import Rank
Employee.objects.annotate(
    dept_rank=Window(Rank(), partition_by=[F("department")], order_by=F("salary").desc()))
```

---

<a name="q13"></a>
## Q13. (Medium) What are window functions (e.g., RowNumber, Rank, Lead, Lag) and how do they compile?
**Answer:**
- `RowNumber` — 1, 2, 3… within the partition.
- `Rank` / `DenseRank` — rank with gaps / without gaps for ties.
- `Lag` / `Lead` — value from the previous / next row (e.g. change vs yesterday).
They compile to `FUNC() OVER (PARTITION BY ... ORDER BY ...)`.

---

<a name="q14"></a>
## Q14. (Easy) How do you partition window functions using the partition_by argument?
**Answer:** `partition_by` splits rows into groups; the function restarts for each group — like GROUP BY, but rows are kept. `partition_by=[F("customer")]` → separate ranking/running total per customer. Without it, the whole result is one partition.

---

<a name="q15"></a>
## Q15. (Easy) How do you order window functions using the order_by argument?
**Answer:** `order_by` defines the row order inside each partition — needed for `RowNumber`, `Rank`, `Lag/Lead` and running totals. It's separate from the queryset's `order_by()`, which orders the final output.

```python
Window(Sum("amount"), partition_by=[F("account")], order_by=F("created_at").asc())
```

---

<a name="q16"></a>
## Q16. (Easy) What is the database backend support variance for window functions?
**Answer:** Supported on PostgreSQL, MySQL 8+, MariaDB 10.2+, SQLite 3.25+, Oracle and SQL Server; older versions raise `NotSupportedError`. Some functions or frame options vary by database. Filtering on window results is supported since Django 4.2.

---

<a name="q17"></a>
## Q17. (Medium) How do you write a custom aggregate function in Django?
**Answer:** Subclass `Aggregate` with the SQL function name and output type.

```python
class BoolAnd(models.Aggregate):
    function = "BOOL_AND"            # PostgreSQL
    output_field = models.BooleanField()

Project.objects.annotate(all_done=BoolAnd("tasks__done"))
```
Use `template` for special syntax and `allow_distinct = True` if `DISTINCT` is allowed.

---

<a name="q18"></a>
## Q18. (Easy) How does Django handle NULL values in aggregate operations (e.g., Coalesce)?
**Answer:** SQL aggregates ignore NULLs, and over zero rows `Sum`/`Avg`/`Max` return `None` (`Count` returns 0). Use `default=` (Django 4.0+) or `Coalesce`.

```python
Order.objects.filter(status="x").aggregate(total=Sum("amount", default=0))
```

---

<a name="q19"></a>
## Q19. (Medium) How do you calculate running totals using Django ORM?
**Answer:** A `Sum` window ordered by date (per account with `partition_by`).

```python
Transaction.objects.annotate(
    running_balance=Window(Sum("amount"), partition_by=[F("account")],
                           order_by=[F("created_at").asc(), F("id").asc()]))
```
Add a unique tie-breaker (`id`) so equal timestamps don't share a total.

---

<a name="q20"></a>
## Q20. (Medium) What are the risks of using ordering in model Meta when grouping data?
**Answer:** In old Django versions Meta ordering columns were added to GROUP BY, splitting groups and giving wrong counts. Since Django 3.1 Meta ordering is ignored in GROUP BY queries. An explicit `order_by("field")` on a non-grouped field can still add it to GROUP BY — order only by grouped fields or annotations.

---

<a name="q21"></a>
## Q21. (Medium) How do you annotate a queryset with data from a related model using Subquery?
**Answer:** A correlated `Subquery` with `OuterRef` returns one value per row — e.g. the latest order date.

```python
latest = Order.objects.filter(customer=OuterRef("pk")).order_by("-created_at")
Customer.objects.annotate(last_order_at=Subquery(latest.values("created_at")[:1]))
```

---

<a name="q22"></a>
## Q22. (Easy) Explain how to use Count with the filter argument (conditional counting).
**Answer:** `filter=Q(...)` counts only matching related rows; compiles to `COUNT(...) FILTER (WHERE ...)` on PostgreSQL (CASE WHEN elsewhere).

```python
Customer.objects.annotate(
    paid_orders=Count("orders", filter=Q(orders__status="paid")),
    open_orders=Count("orders", filter=Q(orders__status="open")))
```

---

<a name="q23"></a>
## Q23. (Medium) How do you annotate a queryset with a list of related primary keys?
**Answer:** On PostgreSQL use `ArrayAgg`.

```python
from django.contrib.postgres.aggregates import ArrayAgg
Article.objects.annotate(tag_ids=ArrayAgg("tags__id", distinct=True, filter=Q(tags__isnull=False), default=[]))
```
Other databases: prefetch and build the list in Python.

---

<a name="q24"></a>
## Q24. (Medium) What are the performance implications of deep joins within annotations?
**Answer:** Aggregating across several joins multiplies rows before grouping (slow and can inflate results), makes large GROUP BYs, and needs indexes on every join column. Use `Subquery` aggregates per relation, aggregate on the nearest table, or pre-computed summary tables.

---

<a name="q25"></a>
## Q25. (Medium) How does Django 5.0 optimize annotations containing GeneratedField?
**Answer:** A stored `GeneratedField` is a real column, so instead of annotating an expression in every query (`annotate(total=F("qty") * F("price"))`), you read/aggregate/filter the precomputed column — and it can be indexed. `Sum("line_total")` is simpler and can use the index for filters.

---

<a name="q26"></a>
## Q26. (Medium) How do you write an annotation that calculates string concatenation across rows?
**Answer:** On PostgreSQL use `StringAgg` (MySQL: a custom `GROUP_CONCAT` aggregate).

```python
from django.contrib.postgres.aggregates import StringAgg
Article.objects.annotate(tag_list=StringAgg("tags__name", delimiter=", ", distinct=True))
```
(`Concat` joins fields of the **same** row, not across rows.)

---

<a name="q27"></a>
## Q27. (Hard) Explain how window function frame clauses compile in Django.
**Answer:** `frame=RowRange(start, end)` or `ValueRange(...)` limits which rows in the partition are used. `None` = unbounded, `0` = current row, negative = preceding, positive = following. Example: 7-row moving average:

```python
Window(Avg("value"), order_by=F("day").asc(), frame=RowRange(start=-6, end=0))
# AVG(value) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

---

<a name="q28"></a>
## Q28. (Medium) What is the difference between Sum and Avg performance on large datasets?
**Answer:** Practically the same — both scan the same rows once; `Avg` just keeps a count too. Cost is driven by how many rows are read (filters, indexes) and data type (`numeric` is slower than integer/float math), not by Sum vs Avg.

---

<a name="q29"></a>
## Q29. (Medium) How do you write an annotation that filters out duplicates using distinct values?
**Answer:** Use `distinct=True` on aggregates that support it (`Count`, `Sum`, `Avg`, `ArrayAgg`, `StringAgg`).

```python
Store.objects.annotate(unique_customers=Count("orders__customer", distinct=True))
```
For "latest row per group" on PostgreSQL: `order_by("customer", "-created_at").distinct("customer")`.

---

<a name="q30"></a>
## Q30. (Medium) How do you annotate a query with date differences in days?
**Answer:** Subtract the dates into a duration, then extract days.

```python
from django.db.models.functions import ExtractDay
Ticket.objects.annotate(
    open_for=ExpressionWrapper(F("closed_at") - F("created_at"), output_field=DurationField())
).annotate(days_open=ExtractDay("open_for"))
```

---

<a name="q31"></a>
## Q31. (Hard) How does Django aggregate over polymorphic models?
**Answer:** With multi-table inheritance, aggregate on the **parent** for shared fields (one table) or on each child for child fields (joins parent). With GenericForeignKey there's no single table to join — aggregate per content type and combine. If you often aggregate across types, keep the measured value in the shared/parent table.

---

<a name="q32"></a>
## Q32. (Medium) What is the performance cost of filtering an annotated column?
**Answer:** A filter on an aggregate is a `HAVING` — the DB must aggregate **all** groups first, then discard some; indexes can't help the HAVING itself. Push as much filtering as possible into `WHERE` (filter before annotate). Filters on non-aggregate annotations (expressions) also can't use normal indexes — use a functional index or a GeneratedField.

---

<a name="q33"></a>
## Q33. (Hard) How do you write a custom window function in Django?
**Answer:** Subclass `Func`, set the SQL name, mark it `window_compatible = True`, and use it inside `Window()`.

```python
class PercentRank(models.Func):
    function = "PERCENT_RANK"
    output_field = models.FloatField()
    window_compatible = True

Employee.objects.annotate(pct=Window(PercentRank(), order_by=F("salary").asc()))
```
(Django already has `PercentRank`; this pattern is for functions it doesn't ship.)

---

<a name="q34"></a>
## Q34. (Hard) Explain the compile timeline for complex annotations.
**Answer:** When you call `annotate()`, each expression is **resolved** (field references → columns, joins set up, output types checked) and stored on the query. At evaluation, the compiler decides SELECT / GROUP BY / HAVING, then each expression's `as_sql()` produces SQL + params (backend-specific variants via `as_postgresql()` etc.). Subqueries are compiled recursively inside.

---

<a name="q35"></a>
## Q35. (Medium) How do you write aggregate queries that exclude specific rows using a negative filter?
**Answer:** Exclude in the WHERE, or exclude inside the aggregate with a negated `Q`.

```python
Order.objects.exclude(status="cancelled").aggregate(Sum("amount"))
Customer.objects.annotate(valid_total=Sum("orders__amount", filter=~Q(orders__status="cancelled")))
```
**Gotcha:** `exclude()` across multi-valued relations can exclude parents with *any* matching child — check the SQL.
