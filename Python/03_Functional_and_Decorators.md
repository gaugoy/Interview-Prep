# Functional Programming, Generators & Decorators
### [← Python index](./README.md) · [Question Bank](./Question_Bank.md)

Closures, lambdas, map/filter/reduce, pure functions, partial, iterators, generators, itertools, and decorators end to end.

**Topics:** [Fundamentals](./01_Fundamentals.md) · [OOP](./02_OOP.md) · [Functional](./03_Functional_and_Decorators.md) · [Concurrency](./04_Concurrency.md) · [Memory](./05_Memory_Management.md) · [DSA](./06_DSA.md) · [Data & AI](./07_Data_and_AI.md) · [Testing](./08_Testing_and_Tooling.md)

## Table of Contents

**Part A — Functional programming**
1. (Medium) [What is a closure in Python?](#q1)
2. (Medium) [What is a lambda function? When should you use/avoid it?](#q2)
3. (Medium) [What is `map()`, `filter()`, and `reduce()`?](#q3)
4. (Medium) [What is a pure function?](#q4)
5. (Medium) [What is `functools.partial`?](#q5)
6. (Medium) [What is immutability and why is it important in functional programming?](#q6)

**Part B — Iterators & generators**
7. (Medium) [What is a generator? How is it different from a regular function?](#q7)
8. (Medium) [What is the difference between `yield` and `return`?](#q8)
9. (Medium) [What is `yield from`?](#q9)
10. (Medium) [What is a generator expression vs a list comprehension?](#q10)
11. (Medium) [What is `itertools`? Name 5 useful functions.](#q11)

**Part C — Decorators**
12. (Medium) [What is a Python decorator? What problem does it solve?](#q12)
13. (Easy) [When does a decorator run?](#q13)
14. (Medium) [How do you write a class-based decorator (and a stateful one)?](#q14)
15. (Medium) [What is a class decorator?](#q15)
16. (Medium) [How do you decorate methods of a class?](#q16)
17. (Hard) [How do you write a decorator that works both with and without arguments?](#q17)
18. (Medium) [How do you write a decorator for async functions?](#q18)
19. (Medium) [How do `functools.lru_cache` / `cache` work, and what are the gotchas?](#q19)
20. (Medium) [What is the difference between `@property`, `@functools.cached_property` and `@lru_cache` on a method?](#q20)
21. (Easy) [Which built-in / standard-library decorators should you know?](#q21)
22. (Medium) [What decorators do you use in Django, DRF, FastAPI and Celery?](#q22)
23. (Hard) [How do you keep type hints correct for decorated functions?](#q23)
24. (Medium) [Write a decorator that checks a user's role before running a function (RBAC).](#q24)
25. (Medium) [What are the downsides of decorators?](#q25)

---

## Part A — Functional programming

<a name="q1"></a>
## Q1. (Medium) What is a closure in Python?
**Answer:**
A closure is an **inner function that remembers variables from its enclosing scope**, even after the outer function has returned.

Three conditions for a closure:
1. There must be a nested function
2. The nested function must refer to a variable in the enclosing scope
3. The enclosing function must return the nested function

```python
# Basic closure
def make_multiplier(factor: float):
    def multiply(x: float) -> float:
        return x * factor   # 'factor' is captured from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# Inspect closure variables
print(double.__closure__[0].cell_contents)  # 2

# Practical use: configurable data transformers
def make_normalizer(mean: float, std: float):
    """Captures training statistics"""
    def normalize(x):
        return (x - mean) / std
    return normalize

# Fit on training data
normalizer = make_normalizer(mean=50.0, std=10.0)

# Apply to any data — training stats are captured
test_data = [45, 55, 60, 40]
normalized = [normalizer(x) for x in test_data]
print(normalized)  # [-0.5, 0.5, 1.0, -1.0]

# ⚠️ Common gotcha: late binding in loops
funcs = [lambda x: x * i for i in range(5)]
print([f(2) for f in funcs])  # [8, 8, 8, 8, 8] — all use i=4!

# Fix: capture i at definition time
funcs = [lambda x, i=i: x * i for i in range(5)]
print([f(2) for f in funcs])  # [0, 2, 4, 6, 8] ✅
```

**Related:** [Functional · Q12](#q12) — What is a Python decorator? What problem does it solve? · [Fundamentals · Q20](./01_Fundamentals.md#q20) — What is the difference between `global` and `nonlocal`?

---

<a name="q2"></a>
## Q2. (Medium) What is a lambda function? When should you use/avoid it?
**Answer:** A lambda is an **anonymous function limited to one expression**: `lambda args: expression` — it returns the expression's value automatically and can't contain statements (no assignments, loops or `try`). It's ideal for short callbacks passed to other functions, like `key=` in `sorted()`, `max()` or `min()`. Avoid naming lambdas or putting real logic in them — a `def` with a name is easier to read, test and debug (tracebacks just say `<lambda>`).

A lambda is an **anonymous, single-expression function**. Use it for short, throwaway functions — especially as arguments to `sorted()`, `map()`, `filter()`.

```python
# Lambda syntax: lambda args: expression
square = lambda x: x**2
print(square(5))  # 25

# Common use: sorting
students = [{"name": "Alice", "grade": 90}, {"name": "Bob", "grade": 85}]
sorted_students = sorted(students, key=lambda s: s["grade"], reverse=True)

# With map/filter
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))

# ✅ Use lambda for: simple one-liners as arguments
# ❌ Avoid lambda for: complex logic, reusable functions, anything needing a docstring

# Prefer list comprehension over map/filter with lambda
doubled = [x * 2 for x in nums]       # More readable
evens = [x for x in nums if x % 2 == 0]
```

---

<a name="q3"></a>
## Q3. (Medium) What is `map()`, `filter()`, and `reduce()`?
**Answer:** These are classic functional-programming tools. `map(f, iterable)` applies `f` to every item; `filter(pred, iterable)` keeps only the items where `pred` returns true — both return **lazy iterators** in Python 3. `functools.reduce(f, iterable, initial)` combines all items into **one value** by repeatedly calling `f(accumulator, item)`. In modern Python, comprehensions are usually clearer than `map`/`filter` with lambdas, and built-ins like `sum`, `max`, `any`, `all` replace most uses of `reduce`.

These are functional programming tools for transforming collections.

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

# map(func, iterable) — apply func to each element
doubled = list(map(lambda x: x * 2, nums))
# [2, 4, 6, 8, 10]

# filter(func, iterable) — keep elements where func returns True
evens = list(filter(lambda x: x % 2 == 0, nums))
# [2, 4]

# reduce(func, iterable) — accumulate to single value
total = reduce(lambda acc, x: acc + x, nums)
# 15 (1+2+3+4+5)

# Modern Python preference: use comprehensions instead
doubled = [x * 2 for x in nums]
evens = [x for x in nums if x % 2 == 0]
total = sum(nums)

# When map/filter ARE useful:
# 1. With existing named functions (no lambda needed)
words = ["hello", "world", "python"]
lengths = list(map(len, words))          # [5, 5, 6]
upper = list(map(str.upper, words))      # ['HELLO', 'WORLD', 'PYTHON']

# 2. map returns a lazy iterator — useful in pipelines
result = sum(map(lambda x: x**2, range(1_000_000)))  # No intermediate list
```

---

<a name="q4"></a>
## Q4. (Medium) What is a pure function?
**Answer:** A **pure function**'s output depends only on its inputs, and it has **no side effects** (it doesn't change globals, its arguments, files or the database, and doesn't print). Calling it twice with the same arguments always gives the same result (referential transparency). That makes it easy to test, reason about, cache (`lru_cache`) and run in parallel. Real programs need side effects, so the practical goal is a pure core of business logic with the side effects pushed to the edges.

A pure function:
1. Always returns the **same output for the same input**
2. Has **no side effects** (doesn't modify external state)

```python
# ✅ Pure function
def add(a: int, b: int) -> int:
    return a + b

def square(x: float) -> float:
    return x ** 2

# ❌ Impure — depends on external state
total = 0
def add_to_total(x):
    global total
    total += x   # Side effect: modifies global
    return total

# ❌ Impure — modifies input
def append_item(lst, item):
    lst.append(item)   # Mutates the input list
    return lst

# ✅ Pure version
def append_item_pure(lst, item):
    return lst + [item]   # Returns new list

# Benefits of pure functions:
# ✅ Easy to test (no mocks needed)
# ✅ Easy to reason about
# ✅ Safe to parallelize
# ✅ Cacheable (memoizable)
# ✅ Composable

# Functional composition
from functools import reduce

def compose(*funcs):
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)

double = lambda x: x * 2
add_one = lambda x: x + 1
square = lambda x: x ** 2

transform = compose(double, add_one, square)  # double(add_one(square(x)))
print(transform(3))  # double(add_one(9)) = double(10) = 20
```

**Related:** [Functional · Q19](#q19) — How do `functools.lru_cache` / `cache` work, and what are the gotchas?

---

<a name="q5"></a>
## Q5. (Medium) What is `functools.partial`?
**Answer:** `functools.partial(func, *args, **kwargs)` returns a new callable with some arguments **already fixed**; when you call it, it merges the stored arguments with the new ones and calls `func`. It's a clean alternative to small wrapper functions or lambdas — useful for callbacks, `map()`, and configuring a library function once (e.g. a pre-configured `json.dumps`). The result exposes `.func`, `.args` and `.keywords` for introspection.

`partial` creates a new function with **some arguments pre-filled** (partial application).

```python
from functools import partial

# Regular function
def power(base, exponent):
    return base ** exponent

# Create specialized versions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))   # 25
print(cube(3))     # 27

# Practical use: configuring functions for pipelines
import json

# Pre-configure json.dumps with specific settings
pretty_json = partial(json.dumps, indent=2, sort_keys=True)
compact_json = partial(json.dumps, separators=(',', ':'))

data = {"b": 2, "a": 1}
print(pretty_json(data))   # Formatted, sorted
print(compact_json(data))  # Compact

# With map — apply function with fixed argument
multiply_by_10 = partial(lambda x, factor: x * factor, factor=10)
result = list(map(multiply_by_10, [1, 2, 3, 4, 5]))
print(result)  # [10, 20, 30, 40, 50]
```

---

<a name="q6"></a>
## Q6. (Medium) What is immutability and why is it important in functional programming?
**Answer:** An **immutable** object can't be changed after creation — to "modify" it you create a new object. Functional programming relies on this: if data can't change, functions can't affect each other through shared state, so code is easier to reason about, safe to share between threads, and values can be hashed and cached. Python isn't a purely functional language, but you get immutability with tuples, frozensets, `frozen=True` dataclasses and NamedTuples, and by returning new collections instead of mutating inputs.

Immutability means **data cannot be changed after creation**. Instead of modifying data, you create new data.

```python
# Mutable approach — risky
def process_data_mutable(data: list) -> list:
    data.sort()          # Modifies original!
    data.append("done")  # Modifies original!
    return data

original = [3, 1, 2]
result = process_data_mutable(original)
print(original)  # [1, 2, 3, 'done'] — original changed!

# Immutable approach — safe
def process_data_immutable(data: list) -> list:
    sorted_data = sorted(data)   # New list
    return sorted_data + ["done"]  # New list

original = [3, 1, 2]
result = process_data_immutable(original)
print(original)  # [3, 1, 2] — unchanged ✅

# Python immutable types: int, float, str, tuple, frozenset
# Use tuples instead of lists when data shouldn't change
config = (host, port, db_name)  # Immutable config

# frozenset for immutable sets
allowed_methods = frozenset({"GET", "POST", "PUT", "DELETE"})

# dataclasses with frozen=True
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError
```

---

## Part B — Iterators & generators

<a name="q7"></a>
## Q7. (Medium) What is a generator? How is it different from a regular function?
**Answer:**
A generator is a function that uses `yield` to **lazily produce values one at a time**, pausing execution between yields. It returns a generator object (iterator).

| Feature | Regular Function | Generator |
|---------|-----------------|-----------|
| Returns | Value once | Values lazily |
| Memory | All at once | One at a time |
| State | Lost after return | Preserved between yields |
| Keyword | `return` | `yield` |

```python
# Regular function — creates entire list in memory
def get_squares_list(n):
    return [x**2 for x in range(n)]

# Generator — produces one value at a time
def get_squares_gen(n):
    for x in range(n):
        yield x**2

import sys
lst = get_squares_list(1_000_000)
gen = get_squares_gen(1_000_000)

print(sys.getsizeof(lst))  # ~8MB
print(sys.getsizeof(gen))  # ~112 bytes

# Generator is an iterator
gen = get_squares_gen(5)
print(next(gen))   # 0
print(next(gen))   # 1
print(next(gen))   # 4
# for loop calls next() automatically
for val in get_squares_gen(5):
    print(val)

# Generator expression (like list comprehension but lazy)
squares = (x**2 for x in range(1_000_000))  # No memory allocated yet
total = sum(squares)  # Consumed lazily
```

**Related:** [Memory · Q1](./05_Memory_Management.md#q1) — How does Python manage memory? · [Data & AI · Q13](./07_Data_and_AI.md#q13) — How would you process a CSV file larger than available RAM?

---

<a name="q8"></a>
## Q8. (Medium) What is the difference between `yield` and `return`?
**Answer:** `return` **ends** a function and hands back one value; the function's local state is discarded. `yield` turns the function into a **generator function**: calling it returns a generator object without running the body; each `next()` runs the body until the next `yield`, hands out that value and **pauses** — keeping all local variables — then resumes from that point on the next call. When the generator finishes (or hits `return`) it raises `StopIteration`, which `for` loops handle automatically; a `return value` inside a generator becomes `StopIteration.value`.

- `return` — **terminates** the function and returns a value
- `yield` — **pauses** the function, returns a value, and **resumes** from the same point on next call

```python
def countdown_return(n):
    result = []
    while n > 0:
        result.append(n)
        n -= 1
    return result   # Returns all at once

def countdown_yield(n):
    while n > 0:
        yield n     # Pauses here, resumes on next()
        n -= 1

# return — all values computed upfront
for x in countdown_return(5):
    print(x)

# yield — computed on demand
for x in countdown_yield(5):
    print(x)

# A function with yield is a generator function
# Calling it returns a generator object (doesn't execute the body yet)
gen = countdown_yield(5)
print(type(gen))   # <class 'generator'>

# return inside a generator raises StopIteration
def gen_with_return():
    yield 1
    yield 2
    return "done"   # Raises StopIteration with value "done"
    yield 3         # Never reached

g = gen_with_return()
print(next(g))  # 1
print(next(g))  # 2
# next(g)       # StopIteration: done
```

---

<a name="q9"></a>
## Q9. (Medium) What is `yield from`?
**Answer:** `yield from iterable` hands control to a **sub-iterator or sub-generator**: every value it produces goes straight to the caller, values and exceptions sent in with `send()` / `throw()` are forwarded to it, and the sub-generator's `return` value becomes the value of the `yield from` expression. It replaces the manual `for x in it: yield x` loop and is how generators are composed (and how coroutines were built before `async`/`await`).

`yield from` **delegates to a sub-generator**, forwarding all values, exceptions, and the return value.

```python
# Without yield from — manual delegation
def chain_manual(*iterables):
    for it in iterables:
        for item in it:
            yield item

# With yield from — cleaner
def chain(*iterables):
    for it in iterables:
        yield from it   # Delegates to sub-iterator

print(list(chain([1, 2], [3, 4], [5, 6])))
# [1, 2, 3, 4, 5, 6]

# yield from with generators
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # Recursive delegation
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], [5, 6]])))
# [1, 2, 3, 4, 5, 6]

# yield from also forwards send() and throw()
def inner():
    value = yield "inner"
    return f"inner got: {value}"

def outer():
    result = yield from inner()   # Forwards send() to inner
    print(f"outer got: {result}")
    yield "outer done"

g = outer()
print(next(g))          # "inner"
print(g.send("hello"))  # "outer done" (after printing "outer got: inner got: hello")
```

**Related:** [Concurrency · Q25](./04_Concurrency.md#q25) — How does `await` work under the hood?

---

<a name="q10"></a>
## Q10. (Medium) What is a generator expression vs a list comprehension?
**Answer:** The syntax is the same except for the brackets. A **list comprehension** `[...]` runs immediately and stores every result in a list — reusable, indexable, supports `len()`, but memory grows with the data. A **generator expression** `(...)` returns a **lazy iterator** that computes each item only when asked — near-constant memory, but it can be consumed **only once**. Use a generator when you stream through data once (`sum(x * x for x in data)`), a list when you need the results more than once.

- **List comprehension** `[...]` — creates the **entire list in memory** immediately
- **Generator expression** `(...)` — creates a **lazy iterator**, computes values on demand

```python
import sys

# List comprehension — eager, all in memory
squares_list = [x**2 for x in range(1_000_000)]
print(sys.getsizeof(squares_list))  # ~8MB

# Generator expression — lazy, minimal memory
squares_gen = (x**2 for x in range(1_000_000))
print(sys.getsizeof(squares_gen))   # ~112 bytes

# Use generator when:
# ✅ You only need to iterate once
# ✅ Working with large/infinite sequences
# ✅ Chaining transformations (pipeline)

# Use list when:
# ✅ You need to iterate multiple times
# ✅ You need indexing (gen[0] doesn't work)
# ✅ You need len()

# Generator pipeline — nothing executes until consumed
import json

def read_lines(filepath):
    with open(filepath) as f:
        yield from f

def parse_json(lines):
    return (json.loads(line) for line in lines)

def filter_active(records):
    return (r for r in records if r.get('active'))

def extract_names(records):
    return (r['name'] for r in records)

# Compose pipeline — lazy, memory efficient
# names = extract_names(filter_active(parse_json(read_lines("data.jsonl"))))
# for name in names:  # Only now does data flow through
#     print(name)
```

**Related:** [Data & AI · Q14](./07_Data_and_AI.md#q14) — What is the difference between eager and lazy evaluation?

---

<a name="q11"></a>
## Q11. (Medium) What is `itertools`? Name 5 useful functions.
**Answer:** `itertools` is a standard-library module of fast (written in C), memory-efficient building blocks that work on iterators **lazily**. Main groups: infinite iterators (`count`, `cycle`, `repeat`); combining and slicing (`chain`, `islice`, `zip_longest`, `pairwise`, `batched` in 3.12+); grouping and filtering (`groupby` — groups only **consecutive** equal keys, so sort first — `takewhile`, `dropwhile`); and combinatorics (`product`, `permutations`, `combinations`). They let you process large or infinite streams without building lists.

`itertools` provides **memory-efficient iterator building blocks** for working with sequences.

```python
import itertools

# 1. chain — combine multiple iterables
combined = list(itertools.chain([1, 2], [3, 4], [5, 6]))
# [1, 2, 3, 4, 5, 6]

# 2. islice — slice an iterator (lazy)
gen = (x**2 for x in range(1_000_000))
first_5 = list(itertools.islice(gen, 5))
# [0, 1, 4, 9, 16]

# 3. groupby — group consecutive elements
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A [('A', 1), ('A', 2)]
# B [('B', 3), ('B', 4)]
# A [('A', 5)]

# 4. product — cartesian product
for combo in itertools.product([1, 2], ['a', 'b']):
    print(combo)
# (1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')

# 5. combinations / permutations
print(list(itertools.combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]

print(list(itertools.permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# 6. accumulate — running totals
import operator
print(list(itertools.accumulate([1, 2, 3, 4, 5])))
# [1, 3, 6, 10, 15]

print(list(itertools.accumulate([1, 2, 3, 4, 5], operator.mul)))
# [1, 2, 6, 24, 120] — running product (factorial!)

# 7. cycle — infinite cycling
colors = itertools.cycle(['red', 'green', 'blue'])
for _ in range(6):
    print(next(colors))
# red, green, blue, red, green, blue
```

---

## Part C — Decorators

<a name="q12"></a>
## Q12. (Medium) What is a Python decorator? What problem does it solve?
**Answer:** Functions are **first-class objects** in Python — you can pass them to other functions and return them. A decorator is a callable that takes a function and returns a new one (usually a wrapper that calls the original). `@decorator` above `def f` is just shorthand for `f = decorator(f)`, applied **once** when the function is defined. Because the wrapper is a closure, it can run code before/after the call, change arguments or results, or skip the call entirely. Always use `functools.wraps` so the wrapper keeps the original's name, docstring and signature.

A decorator is a function that **wraps another function** to add behavior before/after it runs, without modifying the original function. It solves the **cross-cutting concerns** problem (logging, auth, caching, timing).

```python
import functools
import time

# Simple decorator
def timer(func):
    @functools.wraps(func)  # Preserves __name__, __doc__ of original
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.1)

slow_function()  # slow_function took 0.1001s

# Decorator with arguments (factory pattern)
def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Retry {attempt + 1}/{max_attempts}: {e}")
        return wrapper
    return decorator

@retry(max_attempts=3)
def fetch_data(url):
    pass  # might fail

# Stacking decorators (applied bottom-up)
@timer
@retry(max_attempts=3)
def api_call():
    pass
# Equivalent to: timer(retry(3)(api_call))
```

**Related:** [Fundamentals · Q19](./01_Fundamentals.md#q19) — What are `*args` and `**kwargs`? · [Functional · Q1](#q1) — What is a closure in Python? · [OOP · Q33](./02_OOP.md#q33) — What is `__call__`? How can a class instance be made callable?

---

<a name="q13"></a>
## Q13. (Easy) When does a decorator run?
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

<a name="q14"></a>
## Q14. (Medium) How do you write a class-based decorator (and a stateful one)?
**Answer:** A class whose `__init__` receives the function and whose `__call__` (see [OOP · Q33](./02_OOP.md#q33)) runs on every call. Instance attributes give it state — e.g. counting calls.

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

<a name="q15"></a>
## Q15. (Medium) What is a class decorator?
**Answer:** A decorator applied to a **class** — it receives the class and returns it (modified) or a replacement. Used to register classes, add methods/attributes, or generate code. `@dataclass` is the best-known example. It's a simpler alternative to metaclasses ([OOP · Q38](./02_OOP.md#q38)) for most cases.

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

**Related:** [OOP · Q38](./02_OOP.md#q38) — What is a metaclass in Python?

---

<a name="q16"></a>
## Q16. (Medium) How do you decorate methods of a class?
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

<a name="q17"></a>
## Q17. (Hard) How do you write a decorator that works both with and without arguments?
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

<a name="q18"></a>
## Q18. (Medium) How do you write a decorator for async functions?
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

**Related:** [Concurrency · Q24](./04_Concurrency.md#q24) — What is a coroutine? What do `async def` and `await` do?

---

<a name="q19"></a>
## Q19. (Medium) How do `functools.lru_cache` / `cache` work, and what are the gotchas?
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

**Related:** [Memory · Q6](./05_Memory_Management.md#q6) — What causes memory leaks in Python? · [DSA · Q21](./06_DSA.md#q21) — What is memoization? How does `functools.lru_cache` work? · [Functional · Q4](#q4) — What is a pure function?

---

<a name="q20"></a>
## Q20. (Medium) What is the difference between `@property`, `@functools.cached_property` and `@lru_cache` on a method?
**Answer:**
- **`@property`** — computed **every** access ([OOP · Q31](./02_OOP.md#q31)).
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

**Related:** [OOP · Q31](./02_OOP.md#q31) — What is the difference between `@property`, `@setter`, and `@deleter`?

---

<a name="q21"></a>
## Q21. (Easy) Which built-in / standard-library decorators should you know?
**Answer:**
| Decorator | Purpose |
|---|---|
| `@property`, `@staticmethod`, `@classmethod` | Class building blocks ([OOP · Q31](./02_OOP.md#q31), [OOP · Q6](./02_OOP.md#q6)) |
| `@abc.abstractmethod` | Force subclasses to implement ([OOP · Q18](./02_OOP.md#q18)) |
| `@functools.wraps` | Copy name/docstring/signature to wrappers ([Functional · Q12](#q12)) |
| `@functools.lru_cache` / `@cache` | Memoization ([Functional · Q19](#q19)) |
| `@functools.cached_property` | Lazy per-instance attribute ([Functional · Q20](#q20)) |
| `@functools.singledispatch` | Overload by argument type ([OOP · Q24](./02_OOP.md#q24)) |
| `@functools.total_ordering` | Fill in comparison methods ([OOP · Q30](./02_OOP.md#q30)) |
| `@contextlib.contextmanager` | Build context managers from generators ([Fundamentals · Q23](./01_Fundamentals.md#q23)) |
| `@dataclasses.dataclass` | Generate data-class boilerplate ([OOP · Q26](./02_OOP.md#q26)) |
| `@typing.override` (3.12+) | Mark a method as overriding (type checkers verify it) |

**Related:** [OOP · Q6](./02_OOP.md#q6) — What is the difference between `@staticmethod` and `@classmethod`?

---

<a name="q22"></a>
## Q22. (Medium) What decorators do you use in Django, DRF, FastAPI and Celery?
**Answer:**
- **Django:** `@login_required`, `@permission_required`, `@require_http_methods`, `@csrf_exempt`, `@transaction.atomic`, `@cache_page`, `@receiver` (signals).
- **DRF:** `@api_view`, `@permission_classes`, `@action` (extra ViewSet routes).
- **FastAPI:** `@app.get("/items")` (route registration), `@app.middleware("http")`.
- **Celery:** `@shared_task` / `@app.task` (turn a function into a task).
- **pytest:** `@pytest.fixture`, `@pytest.mark.parametrize`.
They follow the same patterns: registration decorators (run at import) and wrapping decorators (run per call).

---

<a name="q23"></a>
## Q23. (Hard) How do you keep type hints correct for decorated functions?
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

**Related:** [Testing · Q7](./08_Testing_and_Tooling.md#q7) — What is type hinting in Python? What are its benefits?

---

<a name="q24"></a>
## Q24. (Medium) Write a decorator that checks a user's role before running a function (RBAC).
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

<a name="q25"></a>
## Q25. (Medium) What are the downsides of decorators?
**Answer:** They hide behaviour (you must read the decorator to know what a function really does), add a small call overhead, make stack traces deeper, and — without `functools.wraps` — break `__name__`, docstrings, introspection and tools like pytest/Sphinx. Many stacked decorators make order bugs easy (e.g. auth check running after caching). Keep them small, well-named, and use `wraps`.

---
