# ⚙️ 04 — Functional & Advanced Python
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q10)](#medium)
- [🔴 Hard (Q11–Q15)](#hard)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is a closure in Python?

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

---

### Q2. What is a generator? How is it different from a regular function?

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

---

### Q3. What is the difference between `yield` and `return`?

**Answer:**
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

### Q4. What is `yield from`?

**Answer:**
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

---

### Q5. What is a generator expression vs a list comprehension?

**Answer:**
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

---

### Q6. What is `map()`, `filter()`, and `reduce()`?

**Answer:**
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

### Q7. What is a pure function?

**Answer:**
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

---

### Q8. What is `functools.partial`?

**Answer:**
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

### Q9. What is `itertools`? Name 5 useful functions.

**Answer:**
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

### Q10. What is immutability and why is it important in functional programming?

**Answer:**
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

<a name="hard"></a>
## 🔴 Hard

---

### Q11. What is the difference between `threading`, `multiprocessing`, and `asyncio`?

**Answer:**

| Feature | threading | multiprocessing | asyncio |
|---------|-----------|----------------|---------|
| Parallelism | ❌ (GIL) | ✅ (separate processes) | ❌ (single thread) |
| Concurrency | ✅ | ✅ | ✅ |
| Best for | I/O-bound | CPU-bound | I/O-bound |
| Memory | Shared | Separate | Shared |
| Overhead | Low | High | Very low |
| Complexity | Medium | High | Medium |

```python
import threading
import multiprocessing
import asyncio
import time

# THREADING — I/O-bound tasks
def download(url):
    time.sleep(1)  # Simulate network I/O
    return f"Downloaded {url}"

# Sequential: 3 seconds
# Threaded: ~1 second (GIL released during I/O)
threads = [threading.Thread(target=download, args=(f"url{i}",)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()

# MULTIPROCESSING — CPU-bound tasks
def compute(n):
    return sum(i * i for i in range(n))

# Sequential: slow
# Multiprocessing: ~4x faster on 4 cores
with multiprocessing.Pool(4) as pool:
    results = pool.map(compute, [10**6] * 4)

# ASYNCIO — I/O-bound, high concurrency
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, f"https://api.example.com/{i}") for i in range(100)]
        results = await asyncio.gather(*tasks)  # 100 concurrent requests!

# asyncio.run(main())

# Decision tree:
# CPU-bound (ML training, image processing) → multiprocessing
# I/O-bound, many connections (web scraping, API calls) → asyncio
# I/O-bound, simple (file I/O, DB queries) → threading or asyncio
```

---

### Q12. What is an event loop in asyncio? How does `async/await` work?

**Answer:**
The event loop is a **single-threaded scheduler** that manages coroutines. It runs one coroutine at a time but switches between them when they're waiting for I/O.

```python
import asyncio

# async def creates a coroutine function
async def greet(name: str, delay: float):
    print(f"Hello, {name}!")
    await asyncio.sleep(delay)   # Yields control to event loop
    print(f"Goodbye, {name}!")

# Coroutine execution
async def main():
    # Sequential — total 3 seconds
    await greet("Alice", 1)
    await greet("Bob", 2)

    # Concurrent — total ~2 seconds (max of 1, 2)
    await asyncio.gather(
        greet("Alice", 1),
        greet("Bob", 2),
    )

asyncio.run(main())

# How it works:
# 1. Event loop starts
# 2. Runs greet("Alice") until it hits await asyncio.sleep(1)
# 3. Suspends Alice, starts greet("Bob")
# 4. Bob hits await asyncio.sleep(2), suspends
# 5. After 1s, Alice resumes and finishes
# 6. After 2s, Bob resumes and finishes

# async/await is syntactic sugar for coroutines
# await = "pause here and let other coroutines run"

# asyncio.gather — run multiple coroutines concurrently
# asyncio.create_task — schedule coroutine without waiting
# asyncio.wait_for — add timeout
async def with_timeout():
    try:
        result = await asyncio.wait_for(greet("Alice", 10), timeout=2.0)
    except asyncio.TimeoutError:
        print("Timed out!")
```

---

### Q13. What is a coroutine? How is it different from a thread?

**Answer:**

| Feature | Coroutine | Thread |
|---------|-----------|--------|
| Scheduling | Cooperative (explicit yield) | Preemptive (OS decides) |
| Switching | At `await` points | Anytime |
| Memory | ~1KB | ~1MB |
| Max count | Millions | Thousands |
| Race conditions | Rare (explicit switching) | Common (need locks) |

```python
import asyncio

# Coroutine — cooperative multitasking
async def producer(queue: asyncio.Queue):
    for i in range(5):
        await queue.put(i)
        print(f"Produced: {i}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # Sentinel

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        await asyncio.sleep(0.2)

async def main():
    queue = asyncio.Queue(maxsize=3)
    await asyncio.gather(
        producer(queue),
        consumer(queue),
    )

asyncio.run(main())

# Key insight: coroutines are NOT parallel — they're concurrent
# Only one coroutine runs at a time
# Switching happens ONLY at await points (predictable)
# This makes them much safer than threads (no race conditions on shared data)
```

---

### Q14. What is `concurrent.futures`?

**Answer:**
`concurrent.futures` provides a **high-level interface** for both threading and multiprocessing with a unified API.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time

def io_task(n):
    time.sleep(1)
    return f"IO result {n}"

def cpu_task(n):
    return sum(i * i for i in range(n))

# ThreadPoolExecutor — for I/O-bound
with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit tasks
    futures = [executor.submit(io_task, i) for i in range(5)]

    # Get results as they complete
    for future in as_completed(futures):
        print(future.result())

# map() — simpler interface
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(io_task, range(5)))

# ProcessPoolExecutor — for CPU-bound
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_task, [10**6] * 4))

# Exception handling
with ThreadPoolExecutor() as executor:
    future = executor.submit(lambda: 1/0)
    try:
        result = future.result()
    except ZeroDivisionError as e:
        print(f"Task failed: {e}")

# Future methods:
# future.result()    — block until done, raise exception if failed
# future.done()      — check if complete
# future.cancel()    — cancel if not started
# future.add_done_callback(fn) — callback when done
```

---

### Q15. What is the difference between `async def` and a regular function?

**Answer:**

```python
import asyncio
import inspect

# Regular function — executes immediately, returns value
def regular():
    return 42

result = regular()
print(result)   # 42

# Async function — returns a coroutine object (not executed yet!)
async def async_func():
    return 42

coro = async_func()
print(coro)     # <coroutine object async_func at 0x...>
print(inspect.iscoroutine(coro))  # True

# Must be awaited or run with asyncio.run()
result = asyncio.run(async_func())
print(result)   # 42

# Inside async context, use await
async def main():
    result = await async_func()   # Execute the coroutine
    print(result)   # 42

# Key differences:
# 1. async def returns a coroutine, not the value
# 2. Must be awaited to get the value
# 3. Can only use await inside async def
# 4. Enables non-blocking I/O

# Async generators
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0)   # Yield control
        yield i

async def consume():
    async for value in async_range(5):
        print(value)

# Async context managers
class AsyncDB:
    async def __aenter__(self):
        print("Connecting...")
        return self

    async def __aexit__(self, *args):
        print("Disconnecting...")

async def use_db():
    async with AsyncDB() as db:
        pass  # Use db
```

---

### [← Back to Index](./00_INDEX.md) | [Next: Python for Data & AI →](./05_Python_Data_AI.md)
