# Module 11: Database Functions (Short Answers)
### [← All modules](./README.md) · [Long answers](../Django%20ORM/11_Database_Functions.md)

## Table of Contents
1. (Easy) [What are Django Database Functions and how do they work?](#q1)
2. (Easy) [How does Cast function convert data types at the database level?](#q2)
3. (Easy) [How do you handle NULL values using Coalesce in Django ORM?](#q3)
4. (Easy) [How does Concat join multiple string fields and how is it handled across DBs?](#q4)
5. (Easy) [What is the Length function and how do you use it in filtering?](#q5)
6. (Easy) [How do you perform case insensitivity using Lower and Upper database functions?](#q6)
7. (Easy) [How does Trunc function work for date/time fields?](#q7)
8. (Easy) [What is the difference between Trunc and Extract for datetime operations?](#q8)
9. (Easy) [How do you calculate time differences using expression subtraction in Django?](#q9)
10. (Easy) [What are text manipulation functions (Replace, Substr, Trim) and how do they compile?](#q10)
11. (Easy) [How do you use database functions in annotations and filters together?](#q11)
12. (Easy) [How does Django handle database-specific functions (e.g., MD5, SHA1)?](#q12)
13. (Medium) [How do you write a custom database function in Django ORM?](#q13)
14. (Medium) [How does Django 5.0 support date and time truncations with time zones?](#q14)
15. (Medium) [What is the performance impact of applying database functions on indexed columns?](#q15)
16. (Medium) [How do you implement a search index using functional annotations?](#q16)
17. (Easy) [How do you calculate math functions (Abs, Ceil, Floor, Round, Power) using ORM?](#q17)
18. (Easy) [What is the difference between Python-level string operations and DB-level functions?](#q18)
19. (Medium) [How do you use database functions with conditional Case/When statements?](#q19)
20. (Hard) [How does Django convert database-returned values back to Python objects for custom functions?](#q20)
21. (Medium) [How do you use database functions to parse JSONField properties?](#q21)
22. (Medium) [What are the limitations of SQLite regarding math and datetime database functions?](#q22)
23. (Easy) [How do you handle string padding (LPad, RPad) in Django ORM?](#q23)
24. (Medium) [How do you extract parts of a string using regex database functions (e.g., Substr)?](#q24)
25. (Easy) [How do you calculate percentages using database-level math functions?](#q25)
26. (Hard) [Explain the internal design of Func and Transform classes.](#q26)
27. (Medium) [How does Django compile the Coalesce function with multiple fallbacks?](#q27)
28. (Easy) [What is the role of the output_field parameter in database functions?](#q28)
29. (Medium) [How do you calculate geo-spatial distances using database functions?](#q29)
30. (Hard) [Explain how to write a database function that executes custom PostgreSQL procedures.](#q30)
31. (Easy) [How does TruncDate differ from TruncTime?](#q31)
32. (Medium) [What is the compile time overhead of nesting 5 database functions?](#q32)
33. (Medium) [How do you calculate moving averages using window database functions?](#q33)
34. (Easy) [Explain how database functions handle NULL propagation.](#q34)
35. (Medium) [How do you convert date formats using database-level string parsing?](#q35)

---

<a name="q1"></a>
## Q1. (Easy) What are Django Database Functions and how do they work?
**Answer:** Classes in `django.db.models.functions` (`Lower`, `Concat`, `Coalesce`, `TruncMonth`, `Cast`…) that compile to SQL functions, so the work happens in the database. Use them in `annotate()`, `filter()`, `order_by()`, `update()`, and indexes.

```python
User.objects.annotate(email_l=Lower("email")).filter(email_l="ann@x.com")
```

---

<a name="q2"></a>
## Q2. (Easy) How does Cast function convert data types at the database level?
**Answer:** `Cast(expression, output_field)` → SQL `CAST(... AS type)` (or `::type` on PostgreSQL). Useful to convert text JSON values to numbers, ints to text, or dates.

```python
Event.objects.annotate(amount=Cast(KT("payload__amount"), DecimalField(max_digits=10, decimal_places=2)))
```

---

<a name="q3"></a>
## Q3. (Easy) How do you handle NULL values using Coalesce in Django ORM?
**Answer:** `Coalesce(a, b, ...)` returns the first non-NULL value — default values for missing data.

```python
User.objects.annotate(display=Coalesce("nickname", "first_name", Value("Guest")))
Order.objects.aggregate(total=Coalesce(Sum("amount"), Value(0), output_field=DecimalField()))
```

---

<a name="q4"></a>
## Q4. (Easy) How does Concat join multiple string fields and how is it handled across DBs?
**Answer:** `Concat("first_name", Value(" "), "last_name")` joins strings. Django compiles it per backend (`||` / `CONCAT()`) and treats NULL as empty string so one NULL doesn't make the whole result NULL. Mixed types need `output_field=CharField()`.

---

<a name="q5"></a>
## Q5. (Easy) What is the Length function and how do you use it in filtering?
**Answer:** `Length("field")` returns string length. Use it in annotations, or as a lookup (registered transform).

```python
Article.objects.annotate(title_len=Length("title")).filter(title_len__gt=80)
Article.objects.filter(title__length__gt=80)     # after CharField.register_lookup(Length)
```

---

<a name="q6"></a>
## Q6. (Easy) How do you perform case insensitivity using Lower and Upper database functions?
**Answer:** Lowercase both sides, or use the `iexact` lookup.

```python
User.objects.annotate(e=Lower("email")).filter(e=email.lower())
User.objects.filter(email__iexact=email)
```
On big tables add a functional index `Index(Lower("email"), name=...)` so it's indexed.

---

<a name="q7"></a>
## Q7. (Easy) How does Trunc function work for date/time fields?
**Answer:** `Trunc` cuts a date/datetime down to a unit (year, month, week, day, hour…), mostly for grouping by period.

```python
Order.objects.annotate(month=TruncMonth("created_at")).values("month").annotate(total=Sum("amount"))
```

---

<a name="q8"></a>
## Q8. (Easy) What is the difference between Trunc and Extract for datetime operations?
**Answer:** `Trunc` returns a **date/datetime** rounded down (`2026-11-01 00:00` for November). `Extract` returns a **number** — one part of the date (`11` for the month, `2026` for the year). Trunc for time-series grouping; Extract for "all orders in any March" or day-of-week analysis.

---

<a name="q9"></a>
## Q9. (Easy) How do you calculate time differences using expression subtraction in Django?
**Answer:** Subtract datetime fields with `F()`; the result is a duration.

```python
Ticket.objects.annotate(
    resolution=ExpressionWrapper(F("closed_at") - F("opened_at"), output_field=DurationField())
).filter(resolution__gt=timedelta(days=2))
```

---

<a name="q10"></a>
## Q10. (Easy) What are text manipulation functions (Replace, Substr, Trim) and how do they compile?
**Answer:** `Replace("phone", Value("-"), Value(""))` → `REPLACE()`, `Substr("code", 1, 3)` → `SUBSTRING()`, `Trim`/`LTrim`/`RTrim` → `TRIM()`. They run in the DB, so you can use them in bulk updates:

```python
Customer.objects.update(phone=Replace("phone", Value(" "), Value("")))
```

---

<a name="q11"></a>
## Q11. (Easy) How do you use database functions in annotations and filters together?
**Answer:** Annotate the function result, then filter on the annotation; or use it directly as a lookup/expression.

```python
Order.objects.annotate(year=ExtractYear("created_at")).filter(year=2026)
Order.objects.filter(created_at__year=2026)       # simpler built-in lookup
```

---

<a name="q12"></a>
## Q12. (Easy) How does Django handle database-specific functions (e.g., MD5, SHA1)?
**Answer:** Django ships `MD5`, `SHA1`, `SHA256`, etc. and compiles them per backend; on databases that lack them (SQLite) Django registers Python implementations. For anything else, write a custom `Func` or use `RawSQL`.

```python
User.objects.annotate(email_hash=MD5("email"))
```

---

<a name="q13"></a>
## Q13. (Medium) How do you write a custom database function in Django ORM?
**Answer:** Subclass `Func` and set the SQL function name (and output type).

```python
class Similarity(Func):
    function = "SIMILARITY"            # PostgreSQL pg_trgm
    output_field = FloatField()

Product.objects.annotate(sim=Similarity("name", Value("laptop"))).order_by("-sim")
```
Use `template` for custom syntax and `as_<vendor>()` methods for backend differences.

---

<a name="q14"></a>
## Q14. (Medium) How does Django 5.0 support date and time truncations with time zones?
**Answer:** With `USE_TZ`, `Trunc*` and `Extract*` convert to the **current time zone** before truncating, so "day" means the user's local day. You can pass `tzinfo=` explicitly: `TruncDay("created_at", tzinfo=ZoneInfo("Asia/Kolkata"))`.

---

<a name="q15"></a>
## Q15. (Medium) What is the performance impact of applying database functions on indexed columns?
**Answer:** Wrapping a column in a function (`Lower("email")`, `TruncDate("created_at")`) usually **prevents the normal index** from being used → full scan. Fixes: a functional index on the same expression, a range filter instead (`created_at__gte=start, created_at__lt=end` instead of `__date=`), or a stored GeneratedField.

---

<a name="q16"></a>
## Q16. (Medium) How do you implement a search index using functional annotations?
**Answer:** Index the expression you search on, and query with the exact same expression.

```python
class Meta:
    indexes = [models.Index(Lower("name"), name="product_lower_name_idx")]
Product.objects.annotate(n=Lower("name")).filter(n__startswith="lap")
```
For full-text search on PostgreSQL: `SearchVector` + a `GinIndex` (or a stored `SearchVectorField`).

---

<a name="q17"></a>
## Q17. (Easy) How do you calculate math functions (Abs, Ceil, Floor, Round, Power) using ORM?
**Answer:** Import from `django.db.models.functions` and use like any expression.

```python
Product.objects.annotate(rounded=Round("price", 2), diff=Abs(F("price") - F("cost")),
                         sq=Power("rating", 2))
```
`Round` with a precision argument is supported since Django 4.0.

---

<a name="q18"></a>
## Q18. (Easy) What is the difference between Python-level string operations and DB-level functions?
**Answer:** Python operations need the rows loaded first (one round-trip + memory), then work per object. DB functions run inside the query — you can filter, sort, group and bulk-update by the result without loading rows. Use DB functions for filtering/bulk work; Python for complex logic on a few objects.

---

<a name="q19"></a>
## Q19. (Medium) How do you use database functions with conditional Case/When statements?
**Answer:**

```python
User.objects.annotate(label=Case(
    When(last_login__isnull=True, then=Value("never")),
    When(last_login__lt=Now() - timedelta(days=90), then=Value("inactive")),
    default=Value("active")))
```
`When` conditions and `then` values can be any expressions or functions.

---

<a name="q20"></a>
## Q20. (Hard) How does Django convert database-returned values back to Python objects for custom functions?
**Answer:** Through the function's `output_field`: the field's converters (`from_db_value`, backend converters) turn the raw DB value into a Python type (`Decimal`, `datetime`, dict). If the output field is wrong or missing, you get the raw value or a "Cannot resolve expression type" error — set `output_field` explicitly.

---

<a name="q21"></a>
## Q21. (Medium) How do you use database functions to parse JSONField properties?
**Answer:** Use key lookups/transforms: `KT("data__owner__name")` (Django 4.2+) gets a key as text; then `Cast` it for numbers or dates.

```python
from django.db.models.fields.json import KT
Event.objects.annotate(user=KT("payload__user__id"),
                       amount=Cast(KT("payload__amount"), IntegerField())).filter(amount__gt=100)
```

---

<a name="q22"></a>
## Q22. (Medium) What are the limitations of SQLite regarding math and datetime database functions?
**Answer:** SQLite has few built-in math and date functions, so Django registers Python implementations for many of them — they work, but run row by row in Python (slower) and can't use indexes. Timezone handling and some lookups differ. Don't rely on SQLite to test DB-function-heavy code meant for PostgreSQL.

---

<a name="q23"></a>
## Q23. (Easy) How do you handle string padding (LPad, RPad) in Django ORM?
**Answer:** `LPad(expression, length, fill_text)` / `RPad(...)`.

```python
Invoice.objects.annotate(number=LPad(Cast("id", CharField()), 8, Value("0")))   # 00000042
```

---

<a name="q24"></a>
## Q24. (Medium) How do you extract parts of a string using regex database functions (e.g., Substr)?
**Answer:** For fixed positions use `Substr` (+ `StrIndex` to find a separator). Django has no regex-extract function — filter with the `__regex` lookup, or write a custom `Func` (PostgreSQL `SUBSTRING(x FROM pattern)` / `REGEXP_REPLACE`).

```python
User.objects.annotate(domain=Substr("email", StrIndex("email", Value("@")) + 1))
```

---

<a name="q25"></a>
## Q25. (Easy) How do you calculate percentages using database-level math functions?
**Answer:** Divide with decimal/float output and guard against division by zero.

```python
Campaign.objects.annotate(ctr=Case(
    When(impressions=0, then=Value(0.0)),
    default=Round(Cast("clicks", FloatField()) * 100.0 / F("impressions"), 2)))
```
Cast first — integer division would truncate to 0.

---

<a name="q26"></a>
## Q26. (Hard) Explain the internal design of Func and Transform classes.
**Answer:** `Func` is a generic SQL function expression: it has `function` (name), `template` (`"%(function)s(%(expressions)s)"`), source expressions and an `output_field`, and its `as_sql()` fills the template. `Transform` is a one-argument `Func` registered on a field so it can be used inside lookups (`email__lower`, `created_at__year`), chaining with other lookups.

---

<a name="q27"></a>
## Q27. (Medium) How does Django compile the Coalesce function with multiple fallbacks?
**Answer:** `Coalesce("a", "b", Value("x"))` → `COALESCE("a", "b", 'x')`. All arguments must resolve to compatible types — otherwise set `output_field`. It needs at least two expressions.

---

<a name="q28"></a>
## Q28. (Easy) What is the role of the output_field parameter in database functions?
**Answer:** It tells Django the result's type: which converters to apply to returned values, which lookups are allowed on the annotation, and how to combine mixed types (e.g. `Integer * Decimal`). Missing it with mixed inputs raises "Expression contains mixed types".

---

<a name="q29"></a>
## Q29. (Medium) How do you calculate geo-spatial distances using database functions?
**Answer:** With GeoDjango (PostGIS) and a `PointField`:

```python
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
Store.objects.filter(location__dwithin=(point, D(km=5))) \
             .annotate(dist=Distance("location", point)).order_by("dist")
```
Use a spatial (GiST) index on the geometry column.

---

<a name="q30"></a>
## Q30. (Hard) Explain how to write a database function that executes custom PostgreSQL procedures.
**Answer:** For a SQL **function** that returns a value, wrap it in a custom `Func` and use it in queries. For a **procedure** (no return value, `CALL`), use a cursor.

```python
class RiskScore(Func):
    function = "calc_risk_score"       # CREATE FUNCTION calc_risk_score(int) ...
    output_field = IntegerField()
Customer.objects.annotate(risk=RiskScore("id"))

with connection.cursor() as cur:
    cur.execute("CALL refresh_daily_stats(%s)", [day])
```

---

<a name="q31"></a>
## Q31. (Easy) How does TruncDate differ from TruncTime?
**Answer:** On a datetime, `TruncDate` keeps only the **date** part (returns a `date`), `TruncTime` keeps only the **time** part (returns a `time`). Both respect the current time zone.

---

<a name="q32"></a>
## Q32. (Medium) What is the compile time overhead of nesting 5 database functions?
**Answer:** Small — compiling a few nested expressions takes microseconds. The bigger cost is in the database: nested functions on a column prevent index use and run per row. Indexes on the expression or a GeneratedField fix that.

---

<a name="q33"></a>
## Q33. (Medium) How do you calculate moving averages using window database functions?
**Answer:** `Avg` inside a `Window` with a row frame.

```python
from django.db.models import RowRange
DailySale.objects.annotate(ma7=Window(Avg("amount"), order_by=F("day").asc(),
                                      frame=RowRange(start=-6, end=0)))
```

---

<a name="q34"></a>
## Q34. (Easy) Explain how database functions handle NULL propagation.
**Answer:** In SQL, most functions and arithmetic return NULL if any input is NULL (`price * NULL` = NULL, `UPPER(NULL)` = NULL). Exceptions: `Coalesce` (made for it), Django's `Concat` (treats NULL as empty) and aggregates (ignore NULL). Wrap inputs in `Coalesce` when NULL is possible.

---

<a name="q35"></a>
## Q35. (Medium) How do you convert date formats using database-level string parsing?
**Answer:** Django has no built-in date-format function; write a small `Func` for the DB's function (PostgreSQL `TO_CHAR` / `TO_DATE`).

```python
class ToChar(Func):
    function = "TO_CHAR"
    output_field = CharField()
Order.objects.annotate(month_label=ToChar("created_at", Value("YYYY-MM")))
```
Often simpler to format in Python after loading.
