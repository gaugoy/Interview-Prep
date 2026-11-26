# Memory Management & Garbage Collection
### [← Python index](./README.md) · [Question Bank](./Question_Bank.md)

Private heap, reference counting, the cyclic garbage collector, leaks and how to find them, and memory-efficient objects.

**Topics:** [Fundamentals](./01_Fundamentals.md) · [OOP](./02_OOP.md) · [Functional](./03_Functional_and_Decorators.md) · [Concurrency](./04_Concurrency.md) · [Memory](./05_Memory_Management.md) · [DSA](./06_DSA.md) · [Data & AI](./07_Data_and_AI.md) · [Testing](./08_Testing_and_Tooling.md)

## Table of Contents

**Part A — How Python manages memory**
1. (Medium) [How does Python manage memory?](#q1)
2. (Easy) [What is reference counting?](#q2)
3. (Medium) [Why does Python need a garbage collector if it has reference counting?](#q3)
4. (Medium) [How does the generational garbage collector work?](#q4)
5. (Medium) [What can you do with the `gc` module? When would you tune it?](#q5)

**Part B — Leaks, tools & production behaviour**
6. (Medium) [What causes memory leaks in Python?](#q6)
7. (Medium) [How do you find a memory leak in a Python application?](#q7)
8. (Medium) [What is a weak reference and when do you use it?](#q8)
9. (Medium) [Does `sys.getsizeof()` show the real memory used by an object?](#q9)
10. (Hard) [Does Python release memory back to the operating system?](#q10)
11. (Hard) [How does memory behave with multiprocessing and `fork` (copy-on-write)?](#q11)

**Part C — Memory-efficient objects**
12. (Medium) [What are `__slots__` and how do they save memory?](#q12)
13. (Medium) [What is `__del__` and why should you be careful with it?](#q13)

---

## Part A — How Python manages memory

<a name="q1"></a>
## Q1. (Medium) How does Python manage memory?
**Answer:** All objects live on a **private heap** managed by the interpreter.
- **Allocation:** small objects (≤ 512 bytes) come from Python's own allocator **pymalloc** (memory grouped into arenas → pools → blocks, fast and less fragmentation); bigger ones from the system `malloc`.
- **Freeing:** mainly **reference counting** — an object is freed immediately when its count reaches 0.
- **Cycles:** a **garbage collector** finds groups of objects that reference each other but are unreachable.
You don't manage memory manually, but you control it by how long you keep references.

**Related:** [Functional · Q7](./03_Functional_and_Decorators.md#q7) — What is a generator? How is it different from a regular function?

---

<a name="q2"></a>
## Q2. (Easy) What is reference counting?
**Answer:** Every object keeps a count of how many references point to it. Assigning it to a variable, putting it in a list, or passing it to a function increases the count; `del`, reassignment or leaving scope decreases it. At 0 the object is freed **immediately** — that's why files are closed promptly in CPython when the last reference goes away.

```python
import sys
a = []
b = a
print(sys.getrefcount(a))   # 3 → a, b, and the temporary argument to getrefcount
del b
print(sys.getrefcount(a))   # 2
```

**Related:** [Concurrency · Q3](./04_Concurrency.md#q3) — What is the GIL (Global Interpreter Lock) and why does it exist? · [Fundamentals · Q1](./01_Fundamentals.md#q1) — What is the difference between `is` and `==` in Python?

---

<a name="q3"></a>
## Q3. (Medium) Why does Python need a garbage collector if it has reference counting?
**Answer:** Reference counting can't free **reference cycles**: objects that point to each other keep each other's count above 0 even when nothing else uses them.

```python
class Node:
    def __init__(self):
        self.other = None

a, b = Node(), Node()
a.other, b.other = b, a     # cycle
del a, b                    # counts never reach 0 → only the cyclic GC can free them
```
The `gc` module periodically finds such unreachable groups and frees them.

---

<a name="q4"></a>
## Q4. (Medium) How does the generational garbage collector work?
**Answer:** The cyclic GC tracks container objects (lists, dicts, class instances). It's **generational**, based on the idea that most objects die young: new objects go into the youngest generation, which is checked often; objects that survive are promoted to older generations that are checked rarely. A collection is triggered when allocations minus deallocations exceed a threshold (`gc.get_threshold()`). Classic CPython used three generations (0, 1, 2); Python 3.14 made the collector **incremental** with a young and an old generation, to reduce pause times.

---

<a name="q5"></a>
## Q5. (Medium) What can you do with the `gc` module? When would you tune it?
**Answer:**
- `gc.collect()` — force a collection (e.g. after freeing a big structure in a batch job).
- `gc.disable()` / `gc.enable()` — turn off the cyclic GC (reference counting still works).
- `gc.set_threshold()` — collect less often to reduce overhead in allocation-heavy code.
- `gc.freeze()` — move existing objects out of GC tracking, used before forking workers to keep copy-on-write memory shared.
- `gc.get_objects()`, `gc.get_referrers()` — debug what's holding objects.
Tune only when profiling shows GC pauses or overhead; most apps never need it.

---

## Part B — Leaks, tools & production behaviour

<a name="q6"></a>
## Q6. (Medium) What causes memory leaks in Python?
**Answer:** Python leaks are usually **objects kept alive by references you forgot about**:
- Global/module-level caches or lists that only grow (unbounded `dict` cache, `lru_cache` without `maxsize`).
- Objects stored in class attributes or singletons.
- Event listeners/callbacks never unregistered.
- Reference cycles involving objects with `__del__` (older Python) or C extensions.
- Loading huge datasets fully (e.g. `list(queryset)` of millions of rows) in long-running workers.
- Debug features that store history (Django `DEBUG=True` stores every SQL query).

**Related:** [Functional · Q19](./03_Functional_and_Decorators.md#q19) — How do `functools.lru_cache` / `cache` work, and what are the gotchas?

---

<a name="q7"></a>
## Q7. (Medium) How do you find a memory leak in a Python application?
**Answer:**
1. Watch process memory (RSS) over time — steady growth = likely leak.
2. `tracemalloc` — take two snapshots and compare which lines allocated the most new memory.
3. `objgraph` / `gc.get_referrers()` — see which object types are growing and what holds them.
4. `memray` or `py-spy` — profile in production-like runs.

```python
import tracemalloc
tracemalloc.start()
snap1 = tracemalloc.take_snapshot()
run_suspicious_code()
snap2 = tracemalloc.take_snapshot()
for stat in snap2.compare_to(snap1, "lineno")[:5]:
    print(stat)                # top 5 lines by memory growth
```

---

<a name="q8"></a>
## Q8. (Medium) What is a weak reference and when do you use it?
**Answer:** A weak reference (`weakref`) points to an object **without increasing its reference count**, so it doesn't keep the object alive. Used for caches and observer lists where entries should disappear when the object is no longer used elsewhere: `weakref.WeakValueDictionary`, `WeakKeyDictionary`, `WeakSet`.

```python
import weakref
cache = weakref.WeakValueDictionary()
img = load_image("a.png")
cache["a"] = img
del img                   # image freed; "a" disappears from the cache automatically
```

---

<a name="q9"></a>
## Q9. (Medium) Does `sys.getsizeof()` show the real memory used by an object?
**Answer:** No — it's **shallow**: it returns the size of the object itself, not the objects it references. A list's size doesn't include its elements. For the real total, walk the references recursively or use tools like `pympler.asizeof` or `tracemalloc`.

```python
sys.getsizeof([1, 2, 3])               # ~88 bytes: just the list (pointer array)
sys.getsizeof(["x" * 10_000] * 3)      # same small number — the big string isn't counted
```

---

<a name="q10"></a>
## Q10. (Hard) Does Python release memory back to the operating system?
**Answer:** Not always. Freed small objects return to pymalloc's pools for reuse **inside** the process; an arena is returned to the OS only when it's completely empty. With fragmentation (a few live objects scattered across many arenas), the process memory (RSS) stays high even after you delete data. Large objects allocated by `malloc` are usually returned. In long-running workers, recycle processes periodically (e.g. Gunicorn `max_requests`, Celery `worker_max_tasks_per_child`).

---

<a name="q11"></a>
## Q11. (Hard) How does memory behave with multiprocessing and `fork` (copy-on-write)?
**Answer:** With `fork`, the child shares the parent's memory pages until one of them writes to a page (**copy-on-write**). In Python, even *reading* an object updates its reference count (a write), so pages get copied anyway and memory usage grows in each worker. Mitigations: load shared data before forking and call `gc.freeze()` (as Gunicorn/Instagram do), keep large data in NumPy arrays or `shared_memory` (no per-object refcounts), or load data lazily per worker.

**Related:** [Concurrency · Q18](./04_Concurrency.md#q18) — What are the start methods fork, spawn and forkserver?

---

## Part C — Memory-efficient objects

<a name="q12"></a>
## Q12. (Medium) What are `__slots__` and how do they save memory?
**Answer:** Normally each instance stores its attributes in a per-instance `__dict__`. Declaring `__slots__` stores attributes in fixed slots instead — no `__dict__`, so each instance uses noticeably less memory and attribute access is slightly faster. Useful when creating millions of small objects. Downside: you can't add new attributes dynamically.

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y
# Point(1, 2).z = 3  → AttributeError
```
(`@dataclass(slots=True)` does the same for dataclasses.)

**Related:** [OOP · Q26](./02_OOP.md#q26) — What are dataclasses and why use them? · [OOP · Q2](./02_OOP.md#q2) — What is the difference between a class and an object?

---

<a name="q13"></a>
## Q13. (Medium) What is `__del__` and why should you be careful with it?
**Answer:** `__del__` is a finalizer called when the object is about to be destroyed. Problems: you don't control **when** it runs (with cycles it waits for the GC; at interpreter shutdown it may not run at all), exceptions in it are ignored, and it can accidentally resurrect objects. For cleanup use **context managers** (`with`) or `weakref.finalize` instead.

**Related:** [Fundamentals · Q23](./01_Fundamentals.md#q23) — What is the `with` statement and context managers?

---
