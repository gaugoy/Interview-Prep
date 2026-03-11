# 🐍 01 — Python Fundamentals
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟢 Easy (Q1–Q15)](#easy)
- [🟡 Medium (Q16–Q30)](#medium)
- [🔴 Hard (Q31–Q40)](#hard)

---

<a name="easy"></a>
## 🟢 Easy

---

### Q1. What is the difference between `is` and `==` in Python?

**Answer:**
- `==` checks **value equality** — do the two objects have the same value?
- `is` checks **identity** — do the two variables point to the **same object in memory**?

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  — same values
print(a is b)   # False — different objects in memory
print(a is c)   # True  — c is just another name for a

# ⚠️ Gotcha: CPython caches small integers (-5 to 256) and interned strings
x = 256; y = 256
print(x is y)   # True  (cached)

x = 257; y = 257
print(x is y)   # False (not cached — new objects)
```

> **Interview tip:** Always use `==` for value comparison. Use `is` only for `None` checks: `if x is None`.

---

### Q2. What are Python's mutable and immutable data types?

**Answer:**
- **Immutable:** `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes` — cannot be changed after creation
- **Mutable:** `list`, `dict`, `set`, `bytearray` — can be modified in place

```python
# Immutable — reassignment creates a new object
s = "hello"
id_before = id(s)
s += " world"
print(id(s) == id_before)  # False — new string object

# Mutable — modified in place
lst = [1, 2, 3]
id_before = id(lst)
lst.append(4)
print(id(lst) == id_before)  # True — same object

# ⚠️ Classic bug: mutable default argument
def add_item(item, lst=[]):   # lst is created ONCE at function definition
    lst.append(item)
    return lst

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2] ← unexpected! shared across calls

# ✅ Fix
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---

### Q3. What is the difference between a list and a tuple?

**Answer:**
| Feature | List | Tuple |
|---------|------|-------|
| Mutability | Mutable | Immutable |
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` |
| Performance | Slightly slower | Slightly faster |
| Use case | Collection that changes | Fixed data, dict keys, unpacking |
| Memory | More | Less |

```python
# Tuple as dict key (possible because immutable)
location = {(40.7128, -74.0060): "New York"}

# Named tuple — best of both worlds
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(p.x, p.y)   # 3 4
print(p[0])       # 3 — still indexable
```

---

### Q4. What is the difference between `append()` and `extend()`?

**Answer:**
- `append(x)` — adds `x` as a **single element** (even if x is a list)
- `extend(iterable)` — adds **each element** of the iterable individually

```python
a = [1, 2, 3]
b = [1, 2, 3]

a.append([4, 5])   # [1, 2, 3, [4, 5]]  ← nested list
b.extend([4, 5])   # [1, 2, 3, 4, 5]    ← flat

# extend is equivalent to +=
c = [1, 2, 3]
c += [4, 5]        # [1, 2, 3, 4, 5]
```

---

### Q5. What are list comprehensions? How are they different from a `for` loop?

**Answer:**
List comprehensions are a concise, readable way to create lists. They are generally **faster** than equivalent `for` loops because they are optimized at the C level in CPython.

```python
# For loop
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x**2)

# List comprehension — same result, more Pythonic
squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# Nested comprehension (flatten a 2D list)
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6]

# Dict comprehension
word_lengths = {word: len(word) for word in ["apple", "banana", "cherry"]}
# {'apple': 5, 'banana': 6, 'cherry': 6}

# Set comprehension
unique_lengths = {len(word) for word in ["apple", "banana", "cherry"]}
# {5, 6}
```

---

### Q6. What is the difference between `//` and `/`?

**Answer:**
- `/` — **true division**, always returns a float
- `//` — **floor division**, returns the largest integer ≤ result

```python
print(7 / 2)    # 3.5  (float)
print(7 // 2)   # 3    (floor)
print(-7 // 2)  # -4   (floors toward negative infinity, not toward zero!)
print(7 % 2)    # 1    (modulo)

# Useful: check if n is divisible
def is_even(n): return n % 2 == 0
def get_page(index, page_size=10): return index // page_size
```

---

### Q7. What is `None`? How is it different from `0`, `False`, or `""`?

**Answer:**
`None` is Python's null value — it represents the **absence of a value**. It is a singleton of type `NoneType`.

```python
print(None == 0)      # False
print(None == False)  # False
print(None == "")     # False
print(bool(None))     # False — None is falsy

# All falsy values in Python:
# None, False, 0, 0.0, 0j, "", [], {}, set(), ()

# Always use 'is' to check for None
def find_user(id):
    return None  # user not found

user = find_user(42)
if user is None:      # ✅ correct
    print("Not found")
if not user:          # ⚠️ risky — also catches 0, [], ""
    print("Not found")
```

---

### Q8. What is the difference between `break`, `continue`, and `pass`?

**Answer:**
- `break` — **exits** the loop entirely
- `continue` — **skips** the current iteration, moves to next
- `pass` — **does nothing**, placeholder for empty blocks

```python
# break
for i in range(10):
    if i == 5:
        break       # stops at 5
    print(i)        # 0 1 2 3 4

# continue
for i in range(10):
    if i % 2 == 0:
        continue    # skip even numbers
    print(i)        # 1 3 5 7 9

# pass — used as placeholder
class MyClass:
    pass            # valid empty class

def todo_function():
    pass            # implement later

# for/else — else runs if loop completes without break
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed without break")  # This prints
```

---

### Q9. What are Python's built-in data structures?

**Answer:**

| Structure | Type | Ordered | Mutable | Duplicates | Key-Value |
|-----------|------|---------|---------|------------|-----------|
| `list` | Sequence | ✅ | ✅ | ✅ | ❌ |
| `tuple` | Sequence | ✅ | ❌ | ✅ | ❌ |
| `dict` | Mapping | ✅ (3.7+) | ✅ | Keys: ❌ | ✅ |
| `set` | Set | ❌ | ✅ | ❌ | ❌ |
| `frozenset` | Set | ❌ | ❌ | ❌ | ❌ |
| `str` | Sequence | ✅ | ❌ | ✅ | ❌ |

```python
from collections import deque, defaultdict, Counter, OrderedDict

# deque — O(1) append/pop from both ends
dq = deque([1, 2, 3])
dq.appendleft(0)   # [0, 1, 2, 3]
dq.popleft()       # 0

# defaultdict — no KeyError on missing keys
dd = defaultdict(list)
dd['a'].append(1)  # {'a': [1]}

# Counter — count occurrences
c = Counter("abracadabra")
print(c.most_common(3))  # [('a', 5), ('b', 2), ('r', 2)]
```

---

### Q10. What is string immutability? What happens when you "modify" a string?

**Answer:**
Strings in Python are immutable — you cannot change a character in place. Any "modification" creates a **new string object**.

```python
s = "hello"
# s[0] = 'H'  # ❌ TypeError: 'str' object does not support item assignment

# Each operation creates a new string
s = s.upper()       # new object "HELLO"
s = s + " world"    # new object "HELLO world"

# ⚠️ Performance: string concatenation in a loop is O(n²)
# ❌ Slow
result = ""
for word in words:
    result += word + " "

# ✅ Fast — join is O(n)
result = " ".join(words)

# Strings are interned (cached) for small/identifier-like strings
a = "hello"
b = "hello"
print(a is b)  # True (interned)
```

---

### Q11. What is the difference between `deepcopy` and shallow copy?

**Answer:**
- **Shallow copy** — creates a new object but **references** the same nested objects
- **Deep copy** — creates a new object AND **recursively copies** all nested objects

```python
import copy

original = [[1, 2], [3, 4]]

# Shallow copy — 3 ways
shallow1 = original.copy()
shallow2 = list(original)
shallow3 = original[:]

shallow1[0].append(99)
print(original)   # [[1, 2, 99], [3, 4]] ← original affected!

# Deep copy
deep = copy.deepcopy(original)
deep[0].append(99)
print(original)   # [[1, 2], [3, 4]] ← original NOT affected

# When to use:
# Shallow: top-level list of immutables (ints, strings)
# Deep: nested mutable structures (list of lists, list of dicts)
```

---

### Q12. What does the `in` operator do for lists vs dictionaries?

**Answer:**
- For **lists**: `in` does a **linear scan** — O(n)
- For **dicts/sets**: `in` uses a **hash lookup** — O(1) average

```python
import time

data_list = list(range(1_000_000))
data_dict = {i: True for i in range(1_000_000)}
data_set  = set(range(1_000_000))

# List: O(n) — scans every element
start = time.time()
999_999 in data_list
print(f"List: {time.time()-start:.6f}s")   # ~0.01s

# Dict: O(1) — hash lookup
start = time.time()
999_999 in data_dict
print(f"Dict: {time.time()-start:.6f}s")   # ~0.000001s

# Rule: if you need frequent membership checks, use a set or dict
```

---

### Q13. What is unpacking in Python?

**Answer:**
Unpacking assigns elements of an iterable to multiple variables in one statement.

```python
# Basic unpacking
a, b, c = [1, 2, 3]
x, y = (10, 20)

# Extended unpacking with *
first, *rest = [1, 2, 3, 4, 5]
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

*init, last = [1, 2, 3, 4, 5]
print(last)   # 5

# Swap without temp variable
a, b = 1, 2
a, b = b, a   # a=2, b=1

# Unpacking in function calls
def add(x, y, z): return x + y + z
nums = [1, 2, 3]
print(add(*nums))          # 6

params = {'x': 1, 'y': 2, 'z': 3}
print(add(**params))       # 6

# Nested unpacking
(a, b), c = (1, 2), 3
print(a, b, c)  # 1 2 3
```

---

### Q14. What is the difference between `range()` in Python 2 vs 3?

**Answer:**
- **Python 2:** `range()` returns a **list** (eager, memory-heavy); `xrange()` returns an iterator (lazy)
- **Python 3:** `range()` returns a **range object** (lazy, like Python 2's `xrange`); `xrange()` no longer exists

```python
# Python 3
r = range(1_000_000)
print(type(r))        # <class 'range'>
print(r[500_000])     # 500000 — supports indexing
print(len(r))         # 1000000 — supports len()
print(500_000 in r)   # True — O(1) membership check!

# Memory efficient — doesn't store all values
import sys
print(sys.getsizeof(range(1_000_000)))  # 48 bytes
print(sys.getsizeof(list(range(1_000_000))))  # ~8MB
```

---

### Q15. What are f-strings? How are they different from `.format()` and `%`?

**Answer:**
f-strings (Python 3.6+) are the **fastest and most readable** string formatting method.

```python
name = "Alice"
score = 95.678

# % formatting (old, C-style)
print("Hello %s, score: %.2f" % (name, score))

# .format() (Python 3.0+)
print("Hello {}, score: {:.2f}".format(name, score))

# f-string (Python 3.6+) — fastest, most readable
print(f"Hello {name}, score: {score:.2f}")

# f-string features
print(f"{2 + 2}")           # 4 — expressions
print(f"{name!r}")          # 'Alice' — repr
print(f"{name!u}")          # ALICE — uppercase (3.12+)
print(f"{score:>10.2f}")    # right-align with width 10

# Debugging (Python 3.8+)
x = 42
print(f"{x=}")              # x=42 — prints name and value

# Performance: f-strings > .format() > % formatting
```

---

<a name="medium"></a>
## 🟡 Medium

---

### Q16. What are `*args` and `**kwargs`?

**Answer:**
- `*args` — collects extra **positional** arguments into a **tuple**
- `**kwargs` — collects extra **keyword** arguments into a **dict**

```python
def describe(*args, **kwargs):
    print(f"args: {args}")      # tuple
    print(f"kwargs: {kwargs}")  # dict

describe(1, 2, 3, name="Alice", age=30)
# args: (1, 2, 3)
# kwargs: {'name': 'Alice', 'age': 30}

# Order matters: positional → *args → keyword-only → **kwargs
def func(a, b, *args, key="default", **kwargs):
    pass

# Forwarding arguments (common in wrappers/decorators)
def wrapper(*args, **kwargs):
    print("Before")
    result = original_func(*args, **kwargs)
    print("After")
    return result
```

---

### Q17. What is a Python decorator? What problem does it solve?

**Answer:**
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

---

### Q18. What is the difference between shallow copy and deep copy of a nested object?

> See Q11 above for the full answer with examples.

**Key rule:** If your data has nested mutable objects (list of lists, list of dicts), always use `copy.deepcopy()`.

---

### Q19. What is the GIL (Global Interpreter Lock)?

**Answer:**
The GIL is a **mutex in CPython** that ensures only **one thread executes Python bytecode at a time**, even on multi-core CPUs. It exists to protect Python's memory management (reference counting) from race conditions.

```python
import threading
import multiprocessing
import time

# ❌ Threading does NOT speed up CPU-bound tasks (GIL blocks parallelism)
def cpu_task(n):
    return sum(i * i for i in range(n))

# ✅ Threading DOES help I/O-bound tasks (GIL is released during I/O)
def io_task():
    time.sleep(1)  # GIL released during sleep/I/O

# ✅ Multiprocessing bypasses GIL (separate processes, separate GILs)
with multiprocessing.Pool(4) as pool:
    results = pool.map(cpu_task, [10**6] * 4)  # True parallelism

# ✅ asyncio — single-threaded, cooperative concurrency for I/O
import asyncio
async def fetch(url):
    pass  # non-blocking I/O

# Decision tree:
# CPU-bound  → multiprocessing
# I/O-bound  → asyncio (preferred) or threading
# Mixed      → asyncio + thread pool for blocking I/O
```

> **Interview tip:** Mention that PyPy, Jython, and the upcoming Python 3.13 "no-GIL" build address this limitation.

---

### Q20. What is the difference between `__str__` and `__repr__`?

**Answer:**
- `__str__` — **human-readable** string, used by `print()` and `str()`
- `__repr__` — **unambiguous** developer representation, used in REPL and `repr()`; should ideally be valid Python to recreate the object

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"  # Unambiguous

    def __str__(self):
        return f"({self.x}, {self.y})"            # Human-friendly

p = Point(3, 4)
print(str(p))    # (3, 4)       ← __str__
print(repr(p))   # Point(3, 4)  ← __repr__
print(p)         # (3, 4)       ← print() uses __str__

# In a list, __repr__ is used
print([p])       # [Point(3, 4)]

# Rule: always define __repr__; __str__ is optional
```

---

### Q21. What are Python's dunder (magic) methods? Name 5 commonly used ones.

**Answer:**
Dunder methods (double underscore) allow classes to implement Python's built-in behaviors.

| Method | Triggered by | Purpose |
|--------|-------------|---------|
| `__init__` | `MyClass()` | Constructor |
| `__str__` | `str(obj)`, `print(obj)` | Human-readable string |
| `__repr__` | `repr(obj)`, REPL | Developer string |
| `__len__` | `len(obj)` | Length |
| `__getitem__` | `obj[key]` | Indexing/slicing |
| `__setitem__` | `obj[key] = val` | Assignment |
| `__contains__` | `x in obj` | Membership test |
| `__iter__` | `for x in obj` | Iteration |
| `__eq__` | `obj1 == obj2` | Equality |
| `__lt__` | `obj1 < obj2` | Less than |
| `__add__` | `obj1 + obj2` | Addition |
| `__enter__`/`__exit__` | `with obj:` | Context manager |

```python
class DataSet:
    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return f"DataSet({self._data!r})"

ds = DataSet([1, 2, 3, 4, 5])
print(len(ds))      # 5
print(ds[2])        # 3
print(3 in ds)      # True
for x in ds: print(x)
```

---

### Q22. What is the difference between `@staticmethod` and `@classmethod`?

**Answer:**
- **Instance method** — receives `self` (the instance)
- `@classmethod` — receives `cls` (the class); used for factory methods, alternative constructors
- `@staticmethod` — receives neither; utility function logically grouped with the class

```python
class Temperature:
    unit = "Celsius"

    def __init__(self, value):
        self.value = value

    # Instance method — accesses instance data
    def to_fahrenheit(self):
        return self.value * 9/5 + 32

    # Class method — accesses class data, used as factory
    @classmethod
    def from_fahrenheit(cls, f_value):
        return cls((f_value - 32) * 5/9)

    @classmethod
    def set_unit(cls, unit):
        cls.unit = unit

    # Static method — no access to instance or class
    @staticmethod
    def is_valid(value):
        return -273.15 <= value  # absolute zero check

t1 = Temperature(100)
t2 = Temperature.from_fahrenheit(212)  # factory
print(Temperature.is_valid(-300))      # False
```

---

### Q23. What is a lambda function? When should you use/avoid it?

**Answer:**
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

### Q24. What is the difference between `sorted()` and `.sort()`?

**Answer:**
- `sorted()` — **built-in function**, works on any iterable, returns a **new list**
- `.sort()` — **list method**, sorts **in place**, returns `None`

```python
nums = [3, 1, 4, 1, 5, 9]

# sorted() — non-destructive, works on any iterable
new_list = sorted(nums)           # [1, 1, 3, 4, 5, 9]
print(nums)                       # [3, 1, 4, 1, 5, 9] — unchanged

# .sort() — in-place, only for lists
nums.sort()
print(nums)                       # [1, 1, 3, 4, 5, 9] — modified

# Both support key and reverse
words = ["banana", "apple", "cherry"]
sorted(words, key=len)            # ['apple', 'banana', 'cherry']
sorted(words, key=str.lower)      # case-insensitive
sorted(words, reverse=True)       # ['cherry', 'banana', 'apple']

# Python uses Timsort — O(n log n), stable
```

---

### Q25. What is a Python module vs a package?

**Answer:**
- **Module** — a single `.py` file containing Python code
- **Package** — a directory containing multiple modules and an `__init__.py` file

```
mypackage/
├── __init__.py        ← makes it a package
├── utils.py           ← module
├── models.py          ← module
└── subpackage/
    ├── __init__.py
    └── helpers.py
```

```python
# Importing
import mypackage.utils           # import module
from mypackage import models     # import module from package
from mypackage.utils import func # import specific function

# __init__.py controls what's exposed
# mypackage/__init__.py
from .utils import helper_func   # expose at package level
from .models import DataModel

# Now users can do:
from mypackage import helper_func  # instead of mypackage.utils.helper_func
```

---

### Q26. What is `__init__.py` and why is it needed?

**Answer:**
`__init__.py` marks a directory as a Python **package**. It runs when the package is imported and can:
1. Make the package importable
2. Control what's exported (`__all__`)
3. Run initialization code

```python
# mypackage/__init__.py
__all__ = ['DataModel', 'process']  # Controls 'from mypackage import *'

from .models import DataModel
from .utils import process

# In Python 3.3+, "namespace packages" work without __init__.py
# but explicit __init__.py is still best practice
```

---

### Q27. What is the difference between `global` and `nonlocal`?

**Answer:**
- `global` — refers to a variable in the **module-level** scope
- `nonlocal` — refers to a variable in the **nearest enclosing function** scope (not global)

```python
x = 10  # global

def outer():
    y = 20  # enclosing scope

    def inner():
        global x    # refers to module-level x
        nonlocal y  # refers to outer()'s y

        x = 100     # modifies global x
        y = 200     # modifies outer's y

    inner()
    print(y)  # 200

outer()
print(x)  # 100

# ⚠️ Avoid global/nonlocal when possible — makes code harder to reason about
# Prefer returning values or using class attributes
```

---

### Q28. What are Python's truthy and falsy values?

**Answer:**
In Python, any object can be evaluated in a boolean context. **Falsy** values evaluate to `False`.

**Falsy values:**
```python
# All of these are falsy:
bool(None)       # False
bool(False)      # False
bool(0)          # False
bool(0.0)        # False
bool(0j)         # False (complex zero)
bool("")         # False
bool([])         # False
bool({})         # False
bool(set())      # False
bool(())         # False

# Everything else is truthy
bool(1)          # True
bool("0")        # True (non-empty string)
bool([0])        # True (non-empty list)
bool(-1)         # True

# Custom class truthiness via __bool__ or __len__
class MyList:
    def __init__(self, data):
        self.data = data
    def __bool__(self):
        return len(self.data) > 0
```

---

### Q29. What is the `with` statement and context managers?

**Answer:**
The `with` statement ensures **setup and teardown** code runs reliably, even if an exception occurs. It calls `__enter__` on entry and `__exit__` on exit.

```python
# File handling — most common use
with open("data.txt", "r") as f:
    content = f.read()
# File is automatically closed here, even if exception occurs

# Custom context manager using class
class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

with Timer() as t:
    sum(range(1_000_000))
# Elapsed: 0.0234s

# Custom context manager using contextlib (simpler)
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Setup")
    try:
        yield "resource"
    finally:
        print("Teardown")

with managed_resource() as r:
    print(f"Using {r}")
# Setup → Using resource → Teardown
```

---

### Q30. What is the difference between `isinstance()` and `type()`?

**Answer:**
- `type(obj)` — returns the **exact type** of an object
- `isinstance(obj, cls)` — returns `True` if obj is an instance of `cls` **or any subclass**

```python
class Animal: pass
class Dog(Animal): pass

dog = Dog()

print(type(dog) == Dog)       # True
print(type(dog) == Animal)    # False — exact type check

print(isinstance(dog, Dog))   # True
print(isinstance(dog, Animal))# True  ← respects inheritance

# isinstance with multiple types
print(isinstance(42, (int, float)))  # True

# ✅ Prefer isinstance() in most cases — it's more Pythonic and handles inheritance
# Use type() only when you need exact type matching
```

---

<a name="hard"></a>
## 🔴 Hard

---

### Q31. What is Python's memory management model?

**Answer:**
Python uses **reference counting** as its primary memory management mechanism, supplemented by a **cyclic garbage collector**.

```python
import sys
import gc

# Reference counting
a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount's argument)

b = a
print(sys.getrefcount(a))  # 3

del b
print(sys.getrefcount(a))  # 2

# When refcount hits 0, memory is freed immediately
# This is why Python is generally memory-safe without explicit free()

# Memory pools — Python uses a private heap
# Small objects (< 512 bytes) use pymalloc (pool allocator)
# Larger objects use the system allocator

# Object sizes
print(sys.getsizeof(42))        # 28 bytes (int)
print(sys.getsizeof("hello"))   # 54 bytes (str)
print(sys.getsizeof([]))        # 56 bytes (empty list)
print(sys.getsizeof({}))        # 64 bytes (empty dict)
```

---

### Q32. What is a circular reference? How does Python handle it?

**Answer:**
A circular reference occurs when two or more objects reference each other, preventing their reference counts from reaching zero.

```python
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

node1 = Node("A")
node2 = Node("B")
node1.ref = node2   # A → B
node2.ref = node1   # B → A (cycle!)

del node1
del node2
# Both nodes still have refcount = 1 (from each other)
# Reference counting alone cannot free them

# Python's cyclic GC (gc module) detects and breaks cycles
gc.collect()  # Force collection

# gc runs automatically in 3 generations
print(gc.get_threshold())  # (700, 10, 10) — collection thresholds

# Avoid cycles when possible:
# 1. Use weakref for back-references
import weakref

class Parent:
    def __init__(self):
        self.children = []

class Child:
    def __init__(self, parent):
        self.parent = weakref.ref(parent)  # weak reference — doesn't increase refcount
```

---

### Q33. What is `__slots__`? When would you use it?

**Answer:**
`__slots__` replaces the per-instance `__dict__` with a fixed set of attributes, reducing memory usage by ~40-50%.

```python
import sys

# Regular class — uses __dict__ per instance
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Slots class — no __dict__, fixed attributes
class SlottedPoint:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

r = RegularPoint(1, 2)
s = SlottedPoint(1, 2)

print(sys.getsizeof(r))  # ~48 bytes + dict overhead (~232 bytes)
print(sys.getsizeof(s))  # ~56 bytes (no dict)

# Use __slots__ when:
# ✅ Creating millions of instances (e.g., data records)
# ✅ Memory is critical
# ❌ Don't use when: you need dynamic attributes, pickling, multiple inheritance
```

---

### Q34. What is a metaclass in Python?

**Answer:**
A metaclass is the **class of a class** — it controls how classes are created. `type` is the default metaclass.

```python
# type is the metaclass of all classes
print(type(int))    # <class 'type'>
print(type(str))    # <class 'type'>
print(type(list))   # <class 'type'>

# Creating a class dynamically with type
MyClass = type('MyClass', (object,), {'x': 10, 'greet': lambda self: "hello"})
obj = MyClass()
print(obj.x)        # 10
print(obj.greet())  # hello

# Custom metaclass — use case: auto-register subclasses
class PluginMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:  # Don't register the base class itself
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class CSVPlugin(Plugin): pass
class JSONPlugin(Plugin): pass

print(PluginMeta.registry)
# {'CSVPlugin': <class 'CSVPlugin'>, 'JSONPlugin': <class 'JSONPlugin'>}

# Modern alternative: __init_subclass__ (simpler, Python 3.6+)
class Plugin:
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin._registry[cls.__name__] = cls
```

---

### Q35. What is the difference between `__new__` and `__init__`?

**Answer:**
- `__new__` — **creates** the instance (allocates memory), called first, returns the new object
- `__init__` — **initializes** the instance (sets attributes), called after `__new__`

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance  # Always return the same instance

    def __init__(self, value):
        self.value = value

s1 = Singleton(10)
s2 = Singleton(20)
print(s1 is s2)    # True — same object
print(s1.value)    # 20 — __init__ ran again on same object

# __new__ is also used for immutable types
class PositiveInt(int):
    def __new__(cls, value):
        if value <= 0:
            raise ValueError("Must be positive")
        return super().__new__(cls, value)

n = PositiveInt(5)   # OK
# PositiveInt(-1)    # ValueError
```

---

### Q36. What is the Python data model? How does operator overloading work?

**Answer:**
The Python data model defines how objects interact with the language's built-in operations through dunder methods.

```python
from functools import total_ordering

@total_ordering  # Auto-generates missing comparison methods
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):  # scalar * vector
        return self.__mul__(scalar)

    def __abs__(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)    # Vector(4, 6)
print(v1 * 3)     # Vector(3, 6)
print(3 * v1)     # Vector(3, 6)
print(abs(v2))    # 5.0
print(v1 < v2)    # True
```

---

### Q37. What is the difference between `@property`, `@setter`, and `@deleter`?

**Answer:**
`@property` creates a **managed attribute** — you can add validation, computation, or side effects to attribute access.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius  # Private storage

    @property
    def radius(self):
        """Getter — called on circle.radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter — called on circle.radius = 5"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @radius.deleter
    def radius(self):
        """Deleter — called on del circle.radius"""
        del self._radius

    @property
    def area(self):
        """Computed property — no setter needed"""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.radius)   # 5    — calls getter
c.radius = 10     # calls setter
print(c.area)     # 314.159...
# c.radius = -1   # ValueError
```

---

### Q38. What is name mangling in Python?

**Answer:**
Name mangling transforms `__attr` (double underscore prefix) to `_ClassName__attr`, making it harder (but not impossible) to access from outside the class.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Stored as _BankAccount__balance

    def get_balance(self):
        return self.__balance

acc = BankAccount(1000)
# print(acc.__balance)          # AttributeError
print(acc._BankAccount__balance)  # 1000 — still accessible if you know the mangled name
print(acc.get_balance())          # 1000 — proper way

# Single underscore _ = convention for "internal use"
# Double underscore __ = name mangling (not truly private)
# Python has no true private attributes
```

---

### Q39. What is the difference between `__getattr__` and `__getattribute__`?

**Answer:**
- `__getattribute__` — called on **every** attribute access (even existing ones)
- `__getattr__` — called only when the attribute is **not found** through normal means (fallback)

```python
class LazyLoader:
    """Load attributes on demand"""

    def __getattr__(self, name):
        # Only called when attribute doesn't exist
        print(f"Loading {name}...")
        value = self._load(name)
        setattr(self, name, value)  # Cache it
        return value

    def _load(self, name):
        return f"data_for_{name}"

obj = LazyLoader()
print(obj.config)   # Loading config... → data_for_config
print(obj.config)   # data_for_config (cached, __getattr__ not called again)

# __getattribute__ — intercepts ALL attribute access
class Logged:
    def __getattribute__(self, name):
        print(f"Accessing: {name}")
        return super().__getattribute__(name)  # Must call super() to avoid infinite recursion
```

---

### Q40. What is `__call__`? How can a class instance be made callable?

**Answer:**
`__call__` makes an instance **callable like a function** — `obj()` triggers `obj.__call__()`.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
print(callable(double))  # True

# Real-world use: stateful function objects, ML model inference
class TextClassifier:
    def __init__(self, model_path):
        self.model = self._load(model_path)

    def _load(self, path):
        return {}  # load model

    def __call__(self, text: str) -> str:
        # Preprocess → predict → postprocess
        return "positive"

classifier = TextClassifier("model.pkl")
result = classifier("This product is great!")  # Callable like a function
```

---

### [← Back to Index](./00_INDEX.md) | [Next: Data Structures & Algorithms →](./02_DSA.md)
