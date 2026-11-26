# Python — OOP & Decorators

Interview questions on object-oriented Python and decorators. **Questions already answered in `python_react/` are linked below instead of repeated** — read those first, then the new questions in Parts B and C. **(Easy)** fundamentals · **(Medium)** asked in most senior interviews · **(Hard)** internals / deep follow-ups.


## Table of Contents

**Part A — Already covered elsewhere** (links to `python_react/`)

**Part B — OOP (new)**
1. (Easy) [What is the difference between class attributes and instance attributes?](#q1)
2. (Easy) [What are dataclasses and why use them?](#q2)
3. (Medium) [Dataclass vs NamedTuple vs Pydantic model — when to use which?](#q3)
4. (Medium) [How are `__eq__` and `__hash__` related? Why does my object become unhashable?](#q4)
5. (Medium) [What is the difference between an ABC and a Protocol?](#q5)
6. (Medium) [Does Python support method overloading?](#q6)
7. (Easy) [What are Enums and why use them?](#q7)
8. (Medium) [What is monkey patching? When is it acceptable?](#q8)
9. (Hard) [How does Python look up an attribute on an object?](#q9)
10. (Medium) [How do you implement dependency injection in Python?](#q10)

**Part C — Decorators (new questions)**
11. (Easy) [When does a decorator run?](#q11)
12. (Medium) [How do you write a class-based decorator (and a stateful one)?](#q12)
13. (Medium) [What is a class decorator?](#q13)
14. (Medium) [How do you decorate methods of a class?](#q14)
15. (Hard) [How do you write a decorator that works both with and without arguments?](#q15)
16. (Medium) [How do you write a decorator for async functions?](#q16)
17. (Medium) [How do `functools.lru_cache` / `cache` work, and what are the gotchas?](#q17)
18. (Medium) [What is the difference between `@property`, `@functools.cached_property` and `@lru_cache` on a method?](#q18)
19. (Easy) [Which built-in / standard-library decorators should you know?](#q19)
20. (Medium) [What decorators do you use in Django, DRF, FastAPI and Celery?](#q20)
21. (Hard) [How do you keep type hints correct for decorated functions?](#q21)
22. (Medium) [Write a decorator that checks a user's role before running a function (RBAC).](#q22)
23. (Medium) [What are the downsides of decorators?](#q23)

---

## Part A — Already covered elsewhere (read there)

**OOP basics → [`python_react/03_OOP.md`](../python_react/03_OOP.md)**

| Topic | Link |
|---|---|
| 4 pillars of OOP | [03 · Q1](../python_react/03_OOP.md#q1-what-are-the-4-pillars-of-oop) |
| Class vs object | [03 · Q2](../python_react/03_OOP.md#q2-what-is-the-difference-between-a-class-and-an-object) |
| Constructor / `__init__` | [03 · Q3](../python_react/03_OOP.md#q3-what-is-a-constructor-what-is-__init__) |
| Inheritance (single vs multiple) | [03 · Q4](../python_react/03_OOP.md#q4-what-is-inheritance-single-vs-multiple) |
| Method overriding | [03 · Q5](../python_react/03_OOP.md#q5-what-is-method-overriding) |
| Public / protected / private | [03 · Q6](../python_react/03_OOP.md#q6-what-is-the-difference-between-public-protected-and-private-attributes) |
| `self` | [03 · Q7](../python_react/03_OOP.md#q7-what-is-self-in-python) |
| Polymorphism & duck typing | [03 · Q8](../python_react/03_OOP.md#q8-what-is-polymorphism-what-is-duck-typing) |
| Encapsulation | [03 · Q9](../python_react/03_OOP.md#q9-what-is-encapsulation-how-does-python-achieve-it) |
| Abstraction & ABCs | [03 · Q10](../python_react/03_OOP.md#q10-what-is-abstraction-how-do-abcs-work) |
| Composition vs inheritance | [03 · Q11](../python_react/03_OOP.md#q11-what-is-the-difference-between-composition-and-inheritance) |
| MRO | [03 · Q12](../python_react/03_OOP.md#q12-what-is-mro-method-resolution-order) |
| `super()` | [03 · Q13](../python_react/03_OOP.md#q13-what-is-super-why-is-it-important) |
| SOLID | [03 · Q14](../python_react/03_OOP.md#q14-what-are-solid-principles) |
| Diamond problem | [03 · Q15](../python_react/03_OOP.md#q15-what-is-the-diamond-problem-how-does-python-resolve-it) |
| Descriptors | [03 · Q16](../python_react/03_OOP.md#q16-what-is-a-descriptor-in-python) |
| Design patterns (Singleton, Factory, Observer) | [03 · Q17](../python_react/03_OOP.md#q17-what-design-patterns-have-you-used-explain-singleton-factory-observer) |
| Liskov Substitution | [03 · Q18](../python_react/03_OOP.md#q18-what-is-the-liskov-substitution-principle-lsp) |
| Mixins | [03 · Q19](../python_react/03_OOP.md#q19-what-is-a-mixin-when-would-you-use-one) |

**Class internals & decorator basics → [`python_react/01_Python_Fundamentals.md`](../python_react/01_Python_Fundamentals.md)**

| Topic | Link |
|---|---|
| What is a decorator, `functools.wraps`, decorator with arguments (retry), stacking order, timer example | [01 · Q17](../python_react/01_Python_Fundamentals.md#q17-what-is-a-python-decorator-what-problem-does-it-solve) |
| `@staticmethod` vs `@classmethod` | [01 · Q22](../python_react/01_Python_Fundamentals.md#q22-what-is-the-difference-between-staticmethod-and-classmethod) |
| `@property`, setter, deleter | [01 · Q37](../python_react/01_Python_Fundamentals.md#q37-what-is-the-difference-between-property-setter-and-deleter) |
| `__str__` vs `__repr__` | [01 · Q20](../python_react/01_Python_Fundamentals.md#q20-what-is-the-difference-between-__str__-and-__repr__) |
| Dunder methods (incl. `__iter__`, `__len__`) | [01 · Q21](../python_react/01_Python_Fundamentals.md#q21-what-are-pythons-dunder-magic-methods-name-5-commonly-used-ones) |
| Operator overloading & data model (incl. `@total_ordering`) | [01 · Q36](../python_react/01_Python_Fundamentals.md#q36-what-is-the-python-data-model-how-does-operator-overloading-work) |
| `__new__` vs `__init__` | [01 · Q35](../python_react/01_Python_Fundamentals.md#q35-what-is-the-difference-between-__new__-and-__init__) |
| Metaclasses (incl. `__init_subclass__`) | [01 · Q34](../python_react/01_Python_Fundamentals.md#q34-what-is-a-metaclass-in-python) |
| `__slots__` | [01 · Q33](../python_react/01_Python_Fundamentals.md#q33-what-is-__slots__-when-would-you-use-it) |
| Name mangling | [01 · Q38](../python_react/01_Python_Fundamentals.md#q38-what-is-name-mangling-in-python) |
| `__getattr__` vs `__getattribute__` | [01 · Q39](../python_react/01_Python_Fundamentals.md#q39-what-is-the-difference-between-__getattr__-and-__getattribute__) |
| `__call__` / callable instances | [01 · Q40](../python_react/01_Python_Fundamentals.md#q40-what-is-__call__-how-can-a-class-instance-be-made-callable) |
| Context managers & `@contextmanager` | [01 · Q29](../python_react/01_Python_Fundamentals.md#q29-what-is-the-with-statement-and-context-managers) |
| Mutable default argument bug | [01 · Q2](../python_react/01_Python_Fundamentals.md#q2-what-are-pythons-mutable-and-immutable-data-types) |

**Functional tools → [`python_react/04_Functional_Advanced_Python.md`](../python_react/04_Functional_Advanced_Python.md)**

| Topic | Link |
|---|---|
| Closures (how decorators keep state) | [04 · Q1](../python_react/04_Functional_Advanced_Python.md#q1-what-is-a-closure-in-python) |
| `functools.partial` | [04 · Q8](../python_react/04_Functional_Advanced_Python.md#q8-what-is-functoolspartial) |
| Immutability & frozen dataclasses | [04 · Q10](../python_react/04_Functional_Advanced_Python.md#q10-what-is-immutability-and-why-is-it-important-in-functional-programming) |

---

## Part B — OOP (new questions)

<a name="q1"></a>
## Q1. (Easy) What is the difference between class attributes and instance attributes?
**Answer:** A **class attribute** is defined on the class and shared by all instances; an **instance attribute** is set on `self` and belongs to one object. Reading `obj.x` checks the instance first, then the class. **Gotcha:** a *mutable* class attribute (list/dict) is shared — appending through one instance changes it for all.

```python
class Cart:
    tax_rate = 0.18          # class attribute — shared, fine (immutable)
    items = []               # ✘ shared list — bug

    def __init__(self):
        self.lines = []      # ✔ instance attribute — one per cart

a, b = Cart(), Cart()
a.items.append("pen")
print(b.items)               # ['pen']  ← b sees a's item
```

---

<a name="q2"></a>
## Q2. (Easy) What are dataclasses and why use them?
**Answer:** `@dataclass` auto-generates `__init__`, `__repr__` and `__eq__` (and optionally ordering, hashing, `__slots__`) from type-annotated fields — less boilerplate for classes that mainly hold data. Use `field(default_factory=list)` for mutable defaults and `__post_init__` for extra validation. Options: `frozen=True` (immutable), `order=True`, `slots=True`.

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    id: int
    customer: str
    items: list[str] = field(default_factory=list)   # not items=[] (shared!)

    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("id must be positive")

Order(1, "Ann")   # Order(id=1, customer='Ann', items=[])
```

---

<a name="q3"></a>
## Q3. (Medium) Dataclass vs NamedTuple vs Pydantic model — when to use which?
**Answer:**
| | `dataclass` | `NamedTuple` | Pydantic `BaseModel` |
|---|---|---|---|
| Mutable | Yes (unless `frozen`) | No | Yes (configurable) |
| Validation / type conversion | No (hints only) | No | **Yes** — validates and converts input |
| Speed / overhead | Light | Lightest, tuple-like | Heavier |
| Typical use | Internal data objects | Small immutable records | API input/output, config, parsing external data |

Rule: data from outside (requests, files, env) → Pydantic; internal objects → dataclass; tiny immutable records → NamedTuple.

---

<a name="q4"></a>
## Q4. (Medium) How are `__eq__` and `__hash__` related? Why does my object become unhashable?
**Answer:** Objects used as dict keys or in sets need `__hash__`, and **equal objects must have equal hashes**. If you define `__eq__` without `__hash__`, Python sets `__hash__ = None` → the object is unhashable (`TypeError: unhashable type`), to avoid broken dicts/sets. Define `__hash__` from the same **immutable** fields used in `__eq__`.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))

{Point(1, 2), Point(1, 2)}    # one element
```
(`@dataclass(frozen=True)` generates both correctly.)

---

<a name="q5"></a>
## Q5. (Medium) What is the difference between an ABC and a Protocol?
**Answer:** An **ABC** (`abc.ABC`, see [03 · Q10](../python_react/03_OOP.md#q10-what-is-abstraction-how-do-abcs-work)) is *nominal*: a class must **inherit** from it and implement the abstract methods. A **`typing.Protocol`** is *structural* ("static duck typing"): any class with matching methods satisfies it — no inheritance needed. Protocols are checked by type checkers (mypy), and at runtime only with `@runtime_checkable` + `isinstance`.

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, msg: str) -> None: ...

class EmailNotifier:                 # doesn't inherit anything
    def send(self, msg: str) -> None:
        print("email:", msg)

def alert(n: Notifier):              # mypy accepts EmailNotifier
    n.send("Disk full")
```
Use ABCs when you want to share base code and enforce implementation; Protocols for loose interfaces, especially with third-party classes.

---

<a name="q6"></a>
## Q6. (Medium) Does Python support method overloading?
**Answer:** Not like Java — defining a method twice just replaces the first. Alternatives: default/keyword arguments, `*args`, checking types, or **`functools.singledispatch`** (choose the implementation by the type of the first argument; `singledispatchmethod` for methods). `typing.overload` only adds type hints, not runtime behaviour.

```python
from functools import singledispatch

@singledispatch
def to_json(value):
    raise TypeError(f"Unsupported: {type(value)}")

@to_json.register
def _(value: int):
    return str(value)

@to_json.register
def _(value: list):
    return "[" + ",".join(to_json(v) for v in value) + "]"

to_json([1, 2])     # '[1,2]'
```

---

<a name="q7"></a>
## Q7. (Easy) What are Enums and why use them?
**Answer:** `enum.Enum` defines a fixed set of named constants. Safer than raw strings/ints: typos fail loudly, values are grouped, you can iterate them, and comparisons are clear. `StrEnum`/`IntEnum` also behave like str/int (handy for JSON/DB).

```python
from enum import Enum, StrEnum

class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"

order_status = Status.PAID
order_status == "paid"            # True (StrEnum)
[s.value for s in Status]         # ['pending', 'paid']
```

---

<a name="q8"></a>
## Q8. (Medium) What is monkey patching? When is it acceptable?
**Answer:** Changing a class, module or function **at runtime** — e.g. replacing a method. It's acceptable in **tests** (mocking: `unittest.mock.patch`) or as a temporary hotfix for a third-party bug. In application code it's risky: behaviour changes globally, it's hard to find, and it breaks on library upgrades.

```python
import requests
from unittest.mock import patch

with patch("requests.get") as fake_get:          # safe, scoped monkey patch in a test
    fake_get.return_value.status_code = 200
    assert requests.get("https://x").status_code == 200
```

---

<a name="q9"></a>
## Q9. (Hard) How does Python look up an attribute on an object?
**Answer:** For `obj.name`, Python (in `object.__getattribute__`):
1. Looks for a **data descriptor** (e.g. `@property`) on the class and its MRO → uses it.
2. Else looks in the **instance `__dict__`**.
3. Else uses a non-data descriptor or plain class attribute (methods, class attributes) found along the **MRO**.
4. Else calls `__getattr__` if defined, otherwise raises `AttributeError`.
That's why a `@property` beats an instance attribute of the same name, and why methods bind `self` automatically. Related: [03 · Q16](../python_react/03_OOP.md#q16-what-is-a-descriptor-in-python), [01 · Q39](../python_react/01_Python_Fundamentals.md#q39-what-is-the-difference-between-__getattr__-and-__getattribute__), [03 · Q12](../python_react/03_OOP.md#q12-what-is-mro-method-resolution-order).

---

<a name="q10"></a>
## Q10. (Medium) How do you implement dependency injection in Python?
**Answer:** Pass dependencies in (usually through `__init__`) instead of creating them inside the class. It makes code testable (inject a fake) and swappable (different DB/notifier per environment). Python rarely needs a DI framework — constructor injection with Protocols/ABCs is enough (FastAPI's `Depends` is a built-in DI system).

```python
class OrderService:
    def __init__(self, repo, notifier):        # injected, not created here
        self.repo, self.notifier = repo, notifier

    def place(self, order):
        self.repo.save(order)
        self.notifier.send(f"Order {order.id} placed")

service = OrderService(SqlOrderRepo(), EmailNotifier())          # production
test_service = OrderService(InMemoryRepo(), FakeNotifier())      # tests
```

---

## Part C — Decorators (new questions)

Basics (what a decorator is, `@functools.wraps`, decorators with arguments, stacking order) → [01 · Q17](../python_react/01_Python_Fundamentals.md#q17-what-is-a-python-decorator-what-problem-does-it-solve).

<a name="q11"></a>
## Q11. (Easy) When does a decorator run?
**Answer:** The decorator function runs **once, when the decorated function is defined** (usually at import time) — `@deco def f` means `f = deco(f)`. The inner `wrapper` runs **every time** you call `f`. So code in the outer body (e.g. registering a route) happens at import; code in `wrapper` happens per call.

```python
def register(func):
    print("registering", func.__name__)    # runs at import time
    return func

@register
def hello():                               # prints "registering hello" immediately
    print("hi")
```

---

<a name="q12"></a>
## Q12. (Medium) How do you write a class-based decorator (and a stateful one)?
**Answer:** A class whose `__init__` receives the function and whose `__call__` (see [01 · Q40](../python_react/01_Python_Fundamentals.md#q40-what-is-__call__-how-can-a-class-instance-be-made-callable)) runs on every call. Instance attributes give it state — e.g. counting calls.

```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hi {name}"

greet("Ann"); greet("Bob")
greet.calls        # 2
```
**Gotcha:** used on a method, a class-based decorator doesn't receive `self` unless it implements `__get__` — function-based decorators don't have this problem.

---

<a name="q13"></a>
## Q13. (Medium) What is a class decorator?
**Answer:** A decorator applied to a **class** — it receives the class and returns it (modified) or a replacement. Used to register classes, add methods/attributes, or generate code. `@dataclass` is the best-known example. It's a simpler alternative to metaclasses ([01 · Q34](../python_react/01_Python_Fundamentals.md#q34-what-is-a-metaclass-in-python)) for most cases.

```python
PLUGINS = {}

def plugin(name):
    def wrap(cls):
        PLUGINS[name] = cls        # register the class
        return cls
    return wrap

@plugin("csv")
class CsvExporter:
    def export(self, rows): ...

PLUGINS["csv"]().export(data)
```

---

<a name="q14"></a>
## Q14. (Medium) How do you decorate methods of a class?
**Answer:** A normal function-based decorator works on methods because `self` simply arrives as the first item in `*args`. If the decorator needs the instance, name it explicitly.

```python
def require_admin(method):
    @functools.wraps(method)
    def wrapper(self, user, *args, **kwargs):
        if not user.is_admin:
            raise PermissionError("admin only")
        return method(self, user, *args, **kwargs)
    return wrapper

class ReportService:
    @require_admin
    def delete_report(self, user, report_id):
        ...
```
Order with built-ins: put `@staticmethod` / `@classmethod` / `@property` on the **outside** (top).

---

<a name="q15"></a>
## Q15. (Hard) How do you write a decorator that works both with and without arguments?
**Answer:** Check whether the first argument is the function itself (`@retry`) or arguments were passed (`@retry(times=5)`).

```python
def retry(func=None, *, times=3):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return f(*args, **kwargs)
                except Exception:
                    if attempt == times:
                        raise
        return wrapper
    return decorator(func) if callable(func) else decorator

@retry                 # times=3
def a(): ...

@retry(times=5)
def b(): ...
```

---

<a name="q16"></a>
## Q16. (Medium) How do you write a decorator for async functions?
**Answer:** The wrapper must itself be `async def` and `await` the original; otherwise you return an un-awaited coroutine. To support both kinds, check `inspect.iscoroutinefunction(func)`.

```python
import functools, inspect, time

def timed(func):
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                print(f"{func.__name__}: {time.perf_counter() - start:.3f}s")
        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__}: {time.perf_counter() - start:.3f}s")
    return sync_wrapper
```

---

<a name="q17"></a>
## Q17. (Medium) How do `functools.lru_cache` / `cache` work, and what are the gotchas?
**Answer:** They memoize: results are stored by the call arguments, so repeated calls with the same arguments return instantly. `lru_cache(maxsize=128)` evicts least-recently-used entries; `cache` (3.9+) is unbounded. Inspect with `f.cache_info()`, reset with `f.cache_clear()`.
Gotchas:
- Arguments must be **hashable** (no lists/dicts).
- Unbounded `cache` can grow forever → memory leak.
- On **methods**, `self` is part of the key, so the cache keeps every instance alive.
- Per process only, no expiry — not a replacement for Redis.

```python
from functools import lru_cache

@lru_cache(maxsize=1024)
def exchange_rate(currency: str) -> float:
    return fetch_rate_from_api(currency)
```

---

<a name="q18"></a>
## Q18. (Medium) What is the difference between `@property`, `@functools.cached_property` and `@lru_cache` on a method?
**Answer:**
- **`@property`** — computed **every** access ([01 · Q37](../python_react/01_Python_Fundamentals.md#q37-what-is-the-difference-between-property-setter-and-deleter)).
- **`@cached_property`** — computed on first access, then stored in the instance's `__dict__`; freed with the instance; reset with `del obj.attr`. Best for expensive per-object values.
- **`@lru_cache` on a method** — shared cache keyed by `self` + args; keeps instances alive (leak risk). Prefer `cached_property` for per-instance caching.

```python
from functools import cached_property

class Report:
    def __init__(self, rows):
        self.rows = rows
    @cached_property
    def total(self):
        print("computing...")
        return sum(r.amount for r in self.rows)

r = Report(rows); r.total; r.total     # "computing..." printed once
```

---

<a name="q19"></a>
## Q19. (Easy) Which built-in / standard-library decorators should you know?
**Answer:**
| Decorator | Purpose |
|---|---|
| `@property`, `@staticmethod`, `@classmethod` | Class building blocks ([01 · Q37](../python_react/01_Python_Fundamentals.md#q37-what-is-the-difference-between-property-setter-and-deleter), [01 · Q22](../python_react/01_Python_Fundamentals.md#q22-what-is-the-difference-between-staticmethod-and-classmethod)) |
| `@abc.abstractmethod` | Force subclasses to implement ([03 · Q10](../python_react/03_OOP.md#q10-what-is-abstraction-how-do-abcs-work)) |
| `@functools.wraps` | Copy name/docstring/signature to wrappers ([01 · Q17](../python_react/01_Python_Fundamentals.md#q17-what-is-a-python-decorator-what-problem-does-it-solve)) |
| `@functools.lru_cache` / `@cache` | Memoization (Q17) |
| `@functools.cached_property` | Lazy per-instance attribute (Q18) |
| `@functools.singledispatch` | Overload by argument type (Q6) |
| `@functools.total_ordering` | Fill in comparison methods ([01 · Q36](../python_react/01_Python_Fundamentals.md#q36-what-is-the-python-data-model-how-does-operator-overloading-work)) |
| `@contextlib.contextmanager` | Build context managers from generators ([01 · Q29](../python_react/01_Python_Fundamentals.md#q29-what-is-the-with-statement-and-context-managers)) |
| `@dataclasses.dataclass` | Generate data-class boilerplate (Q2) |
| `@typing.override` (3.12+) | Mark a method as overriding (type checkers verify it) |

---

<a name="q20"></a>
## Q20. (Medium) What decorators do you use in Django, DRF, FastAPI and Celery?
**Answer:**
- **Django:** `@login_required`, `@permission_required`, `@require_http_methods`, `@csrf_exempt`, `@transaction.atomic`, `@cache_page`, `@receiver` (signals).
- **DRF:** `@api_view`, `@permission_classes`, `@action` (extra ViewSet routes).
- **FastAPI:** `@app.get("/items")` (route registration), `@app.middleware("http")`.
- **Celery:** `@shared_task` / `@app.task` (turn a function into a task).
- **pytest:** `@pytest.fixture`, `@pytest.mark.parametrize`.
They follow the same patterns: registration decorators (run at import) and wrapping decorators (run per call).

---

<a name="q21"></a>
## Q21. (Hard) How do you keep type hints correct for decorated functions?
**Answer:** A plain `def wrapper(*args, **kwargs)` loses the original signature for type checkers. Use `ParamSpec` and `TypeVar` (3.10+; generic syntax in 3.12+) so the decorated function keeps its parameter and return types.

```python
from typing import Callable, ParamSpec, TypeVar
import functools

P = ParamSpec("P")
R = TypeVar("R")

def logged(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("calling", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a: int, b: int) -> int:
    return a + b
# mypy still knows add(a: int, b: int) -> int
```

---

<a name="q22"></a>
## Q22. (Medium) Write a decorator that checks a user's role before running a function (RBAC).
**Answer:** A decorator factory that takes the allowed roles and checks the user before calling the function — keeps permission logic out of business code.

```python
def require_roles(*roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if not set(roles) & set(user.roles):
                raise PermissionError(f"{func.__name__} needs one of {roles}")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_roles("admin", "editor")
def publish_article(user, article_id):
    ...
```
In Django/DRF, prefer the framework's tools (`@permission_required`, permission classes) so checks are consistent.

---

<a name="q23"></a>
## Q23. (Medium) What are the downsides of decorators?
**Answer:** They hide behaviour (you must read the decorator to know what a function really does), add a small call overhead, make stack traces deeper, and — without `functools.wraps` — break `__name__`, docstrings, introspection and tools like pytest/Sphinx. Many stacked decorators make order bugs easy (e.g. auth check running after caching). Keep them small, well-named, and use `wraps`.
