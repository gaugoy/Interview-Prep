# Python Fundamentals
### [← Python index](./README.md) · [Question Bank](./Question_Bank.md)

Core language: data types, mutability, operators, comprehensions, strings, functions, scope, modules, context managers.

**Topics:** [Fundamentals](./01_Fundamentals.md) · [OOP](./02_OOP.md) · [Functional](./03_Functional_and_Decorators.md) · [Concurrency](./04_Concurrency.md) · [Memory](./05_Memory_Management.md) · [DSA](./06_DSA.md) · [Data & AI](./07_Data_and_AI.md) · [Testing](./08_Testing_and_Tooling.md)

## Table of Contents

**Part A — Data types & mutability**
1. (Easy) [What is the difference between `is` and `==` in Python?](#q1)
2. (Easy) [What are Python's mutable and immutable data types?](#q2)
3. (Easy) [What is the difference between a list and a tuple?](#q3)
4. (Easy) [What are Python's built-in data structures?](#q4)
5. (Easy) [What is string immutability? What happens when you "modify" a string?](#q5)
6. (Easy) [What is `None`? How is it different from `0`, `False`, or `""`?](#q6)
7. (Medium) [What are Python's truthy and falsy values?](#q7)
8. (Medium) [What is the difference between `isinstance()` and `type()`?](#q8)
9. (Easy) [What is the difference between `deepcopy` and shallow copy?](#q9)

**Part B — Operators, syntax & built-ins**
10. (Easy) [What is the difference between `append()` and `extend()`?](#q10)
11. (Easy) [What does the `in` operator do for lists vs dictionaries?](#q11)
12. (Medium) [What is the difference between `sorted()` and `.sort()`?](#q12)
13. (Easy) [What are list comprehensions? How are they different from a `for` loop?](#q13)
14. (Easy) [What is unpacking in Python?](#q14)
15. (Easy) [What is the difference between `//` and `/`?](#q15)
16. (Easy) [What is the difference between `break`, `continue`, and `pass`?](#q16)
17. (Easy) [What is the difference between `range()` in Python 2 vs 3?](#q17)
18. (Easy) [What are f-strings? How are they different from `.format()` and `%`?](#q18)

**Part C — Functions, scope, modules & context managers**
19. (Medium) [What are `*args` and `**kwargs`?](#q19)
20. (Medium) [What is the difference between `global` and `nonlocal`?](#q20)
21. (Medium) [What is a Python module vs a package?](#q21)
22. (Medium) [What is `__init__.py` and why is it needed?](#q22)
23. (Medium) [What is the `with` statement and context managers?](#q23)

---

## Part A — Data types & mutability

<a name="q1"></a>
## Q1. (Easy) What is the difference between `is` and `==` in Python?
**Answer:** Every object has an **identity** (where it lives in memory, `id()`), a type and a value. `==` calls `__eq__` and compares **values** — a class can define what "equal" means. `is` compares **identities**, can't be overridden, and is the fastest check. CPython caches some immutable objects (small ints, interned strings), so `is` sometimes *looks* like it compares values — that's an implementation detail, so never use `is` for numbers or strings.

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

**Related:** [Memory · Q2](./05_Memory_Management.md#q2) — What is reference counting?

---

<a name="q2"></a>
## Q2. (Easy) What are Python's mutable and immutable data types?
**Answer:** A variable is just a **name bound to an object**. **Immutable** objects can't change after creation — any "change" builds a new object and rebinds the name. **Mutable** objects change in place, and every name pointing to them sees the change. This matters for: dict keys / set items (must be hashable → normally immutable), function arguments (a function can mutate a list you pass in), and default arguments (evaluated **once** when the function is defined, so a mutable default is shared between calls).

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

**Related:** [OOP · Q28](./02_OOP.md#q28) — How are `__eq__` and `__hash__` related? Why does my object become unhashable? · [Fundamentals · Q9](#q9) — What is the difference between `deepcopy` and shallow copy?

---

<a name="q3"></a>
## Q3. (Easy) What is the difference between a list and a tuple?
**Answer:** Both are ordered sequences that allow duplicates and indexing. A **list** is mutable — use it for a collection of similar items that grows or shrinks. A **tuple** is immutable — use it for a fixed record of related values (a row, coordinates, a function returning several values). Because a tuple can't change, it's hashable (if its items are), so it can be a dict key or set member, and Python stores it more compactly and creates it faster.

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

<a name="q4"></a>
## Q4. (Easy) What are Python's built-in data structures?
**Answer:** Python has four core built-in collections: **list** (ordered, mutable sequence), **tuple** (ordered, immutable), **dict** (key → value mapping with O(1) average lookup; keeps insertion order since 3.7) and **set** (unique items, O(1) membership checks). `dict` and `set` are hash tables, so keys/items must be hashable. The `collections` module adds specialised versions: `deque` (fast at both ends), `defaultdict`, `Counter`, `namedtuple`, `OrderedDict`.


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

**Related:** [DSA · Q1](./06_DSA.md#q1) — What is the time complexity of common list operations? · [DSA · Q10](./06_DSA.md#q10) — What is a deque? When would you use it over a list?

---

<a name="q5"></a>
## Q5. (Easy) What is string immutability? What happens when you "modify" a string?
**Answer:** A `str` can't be changed after it's created: methods like `upper()` or `replace()` return a **new** string, and `s += "x"` creates a new object and rebinds `s`. Immutability makes strings hashable (usable as dict keys), safe to share across the program, and lets CPython reuse (intern) them. The downside: building a string piece by piece in a loop may copy it again and again — collect the pieces in a list and use `"".join(pieces)`.

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

**Related:** [DSA · Q1](./06_DSA.md#q1) — What is the time complexity of common list operations?

---

<a name="q6"></a>
## Q6. (Easy) What is `None`? How is it different from `0`, `False`, or `""`?
**Answer:** `None` is a single object (a **singleton**) of type `NoneType` meaning "no value" — it's what a function returns when it has no `return`, and a common placeholder for optional arguments. `0`, `False` and `""` are real values that simply happen to be falsy. So `None == 0` is `False`, but all four fail an `if` test. Check for None with `is None` (identity), because `if not x` can't tell None apart from 0 or an empty string.

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

<a name="q7"></a>
## Q7. (Medium) What are Python's truthy and falsy values?
**Answer:** Any object can be used in a condition. Python calls the object's `__bool__`; if that isn't defined it uses `__len__` (length 0 → False); if neither exists, the object is truthy. Falsy values: `None`, `False`, numeric zeros (`0`, `0.0`, `0j`) and empty strings/collections. That's why `if items:` is the Pythonic way to check for a non-empty list — but be careful when `0` or `""` are valid values (use `is None` instead).

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

<a name="q8"></a>
## Q8. (Medium) What is the difference between `isinstance()` and `type()`?
**Answer:** `type(obj)` returns the object's **exact** class; `isinstance(obj, cls)` checks whether the object is an instance of `cls` **or any subclass** of it (it also accepts a tuple of classes and works with abstract base classes like `collections.abc.Iterable`). Since a subclass should be usable wherever its parent is (Liskov principle), `isinstance` is almost always the right check; `type(x) is Cls` is only for the rare case where subclasses must be rejected.

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

<a name="q9"></a>
## Q9. (Easy) What is the difference between `deepcopy` and shallow copy?
**Answer:** Assignment never copies — it just creates another name for the same object. A **shallow copy** creates a new outer container but fills it with references to the **same** inner objects, so changing a nested list shows up in both. A **deep copy** (`copy.deepcopy`) recursively copies the inner objects too (and handles cycles), so the copy is completely independent — but it's slower and uses more memory.

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

**Related:** [Fundamentals · Q2](#q2) — What are Python's mutable and immutable data types?

---

## Part B — Operators, syntax & built-ins

<a name="q10"></a>
## Q10. (Easy) What is the difference between `append()` and `extend()`?
**Answer:** Both modify the list **in place** and return `None`. `append(x)` adds its argument as **one** new element — appending a list creates a nested list. `extend(iterable)` loops over its argument and adds **each item**; `+=` on a list does the same. Gotcha: `lst.extend("abc")` adds `'a'`, `'b'`, `'c'` because a string is iterable.

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

<a name="q11"></a>
## Q11. (Easy) What does the `in` operator do for lists vs dictionaries?
**Answer:** `x in container` calls the container's `__contains__`. For a **list or tuple**, Python compares items one by one → O(n). For a **set or dict**, it hashes `x` and jumps straight to the right bucket → O(1) on average. For a dict, `in` checks the **keys**, not the values. So if you check membership many times, convert the list to a set once.

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

**Related:** [DSA · Q2](./06_DSA.md#q2) — What is the time complexity of dictionary operations?

---

<a name="q12"></a>
## Q12. (Medium) What is the difference between `sorted()` and `.sort()`?
**Answer:** `list.sort()` sorts the list **in place** and returns `None` (a reminder that it changed the list); it exists only on lists. `sorted(iterable)` works on **any iterable** and returns a **new** list, leaving the input unchanged. Both accept `key=` (a function computed once per element) and `reverse=`, and both use **Timsort**: O(n log n) and **stable** — equal elements keep their original order, so you can sort by several keys in steps.

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

**Related:** [DSA · Q17](./06_DSA.md#q17) — What sorting algorithm does Python use?

---

<a name="q13"></a>
## Q13. (Easy) What are list comprehensions? How are they different from a `for` loop?
**Answer:** A comprehension builds a new list (or dict/set) from an iterable in one expression: `[expression for item in iterable if condition]`. It's usually faster than a `for` loop with `.append()` because the loop runs in specialised bytecode without looking up and calling `append` each time. Use it for simple transform/filter logic; use a normal loop when there are side effects or the logic needs several lines — readability first. In Python 3 the loop variable doesn't leak out of the comprehension.

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

<a name="q14"></a>
## Q14. (Easy) What is unpacking in Python?
**Answer:** Unpacking assigns the items of **any iterable** to several names in one statement; the number of names must match the number of items, unless one name has a `*`, which collects the remaining items into a list. The same idea works in function calls (`f(*args_list, **kwargs_dict)` spreads positional/keyword arguments) and in literals (`[*a, *b]`, `{**d1, **d2}`). The swap `a, b = b, a` works because the right side is built as a tuple first.

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

<a name="q15"></a>
## Q15. (Easy) What is the difference between `//` and `/`?
**Answer:** `/` is **true division**: it always returns a float (`4 / 2` → `2.0`). `//` is **floor division**: it rounds the result *down* (toward negative infinity) and returns an int for int inputs (a float if either operand is a float). `%` gives the remainder that matches `//`, so `a == (a // b) * b + a % b` always holds — that's why `-7 // 2` is `-4` and `-7 % 2` is `1`.

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

<a name="q16"></a>
## Q16. (Easy) What is the difference between `break`, `continue`, and `pass`?
**Answer:** `break` stops the nearest loop immediately. `continue` skips the rest of the current iteration and jumps to the next one. `pass` is a statement that does nothing — used where Python's syntax requires a block but there's nothing to do yet. Loops also have an `else` clause that runs **only if the loop finished without `break`** — handy for search loops ("not found" case).

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

<a name="q17"></a>
## Q17. (Easy) What is the difference between `range()` in Python 2 vs 3?
**Answer:** In Python 3, `range` is a **lazy, immutable sequence**: it stores only start, stop and step and computes each number on demand, so `range(10**9)` uses almost no memory. It still supports `len()`, indexing, slicing and fast `in` checks for integers. In Python 2, `range` built a full list and `xrange` was the lazy version; Python 3 kept only the lazy one and named it `range`.

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

<a name="q18"></a>
## Q18. (Easy) What are f-strings? How are they different from `.format()` and `%`?
**Answer:** Python has three formatting styles: `%` (old C-style), `str.format()` (3.0+) and **f-strings** (3.6+). f-strings evaluate expressions written directly inside `{}` at runtime, so they're the most readable and usually the fastest. They support the same format mini-language (`{value:.2f}`, `{x:>10}`), the conversions `!r` / `!s` / `!a`, and `{x=}` for debugging. `%`-style is still used where libraries expect it (e.g. `logging` lazy formatting).

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
print(f"{name.upper()}")    # ALICE — any expression works inside {}
print(f"{score:>10.2f}")    # right-align with width 10

# Debugging (Python 3.8+)
x = 42
print(f"{x=}")              # x=42 — prints name and value

# Performance: f-strings > .format() > % formatting
```

---

## Part C — Functions, scope, modules & context managers

<a name="q19"></a>
## Q19. (Medium) What are `*args` and `**kwargs`?
**Answer:** `*args` and `**kwargs` let a function accept any number of extra arguments: `*args` collects extra **positional** arguments into a tuple, `**kwargs` collects extra **keyword** arguments into a dict (the names are only convention — the `*` / `**` matter). They're used for flexible APIs and to **forward** arguments unchanged (decorators, wrappers, calling a parent `__init__`). Parameter order: normal → `*args` → keyword-only → `**kwargs`; a bare `*` makes the following parameters keyword-only.

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

**Related:** [Functional · Q12](./03_Functional_and_Decorators.md#q12) — What is a Python decorator? What problem does it solve?

---

<a name="q20"></a>
## Q20. (Medium) What is the difference between `global` and `nonlocal`?
**Answer:** Python resolves names with the **LEGB** rule: Local → Enclosing function → Global (module) → Built-ins. Reading a variable searches outward automatically, but **assigning** to a name inside a function makes it local by default (decided at compile time). `global x` says assignments go to the module-level `x`; `nonlocal x` says they go to the nearest enclosing function's `x` (used in closures, e.g. a counter). Without them you get `UnboundLocalError` when you read the name before assigning it.

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

**Related:** [Functional · Q1](./03_Functional_and_Decorators.md#q1) — What is a closure in Python?

---

<a name="q21"></a>
## Q21. (Medium) What is a Python module vs a package?
**Answer:** A **module** is a single `.py` file — a namespace of functions, classes and variables; it's executed once on first import and cached in `sys.modules`. A **package** is a directory of modules (and sub-packages) that organises code hierarchically with dotted imports (`app.services.billing`). Python finds both through `sys.path`. A regular package has an `__init__.py`; without one, Python 3.3+ treats the directory as a namespace package.

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

<a name="q22"></a>
## Q22. (Medium) What is `__init__.py` and why is it needed?
**Answer:** `__init__.py` marks a directory as a **regular package** and runs the first time the package is imported. Use it to expose a clean public API (re-export the important names), define `__all__` for `from package import *`, and do light package setup. Keep it small — heavy imports there slow down every import of the package and can cause circular imports. Since Python 3.3 a folder without it still works as a namespace package, but an explicit `__init__.py` is the normal practice.

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

<a name="q23"></a>
## Q23. (Medium) What is the `with` statement and context managers?
**Answer:** A context manager defines **setup and cleanup** around a block of code. `with obj as x:` calls `obj.__enter__()` (its return value goes into `x`), runs the block, then **always** calls `obj.__exit__(exc_type, exc, tb)` — even if an exception or `return` happens. If `__exit__` returns `True`, the exception is suppressed. It replaces `try/finally` for resources: files, locks, DB transactions (`transaction.atomic()`), network connections. `@contextmanager` lets you write one as a generator: the code before `yield` is the setup, the code after it is the cleanup.

The `with` statement ensures **setup and teardown** code runs reliably, even if an exception occurs. It calls `__enter__` on entry and `__exit__` on exit.

```python
# File handling — most common use
with open("data.txt", "r") as f:
    content = f.read()
# File is automatically closed here, even if exception occurs

# Custom context manager using class
import time

class Timer:
    def __enter__(self):
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

**Related:** [Concurrency · Q30](./04_Concurrency.md#q30) — What are `async with`, `async for` and async generators? · [Memory · Q13](./05_Memory_Management.md#q13) — What is `__del__` and why should you be careful with it?

---
