# 🐍 Python — Interview Preparation (everything Python in one place)

All Python interview questions, split by topic. Every answer follows the same frame: **the answer in plain words (theory) → a short example only when code helps → Related links** to questions you should learn together. Difficulty: **(Easy)** · **(Medium)** · **(Hard)**.

- **[Question_Bank.md](./Question_Bank.md)** — every question in one list (fastest way to revise).
- React / Web / JavaScript live in [`../React/`](../React/00_INDEX.md).

## Topic files

| File | What's inside | Questions |
|---|---|---|
| [Python Fundamentals](./01_Fundamentals.md) | Core language: data types, mutability, operators, comprehensions, strings, functions, scope, modules, context managers. | 23 |
| [Object-Oriented Programming](./02_OOP.md) | Classes, inheritance, MRO, polymorphism, abstraction, SOLID, design patterns, dataclasses, dunder methods, descriptors, metaclasses. | 39 |
| [Functional Programming, Generators & Decorators](./03_Functional_and_Decorators.md) | Closures, lambdas, map/filter/reduce, pure functions, partial, iterators, generators, itertools, and decorators end to end. | 25 |
| [Concurrency: GIL, Threading, Multiprocessing & asyncio](./04_Concurrency.md) | How Python runs work in parallel or concurrently, and how to choose and use each tool. | 38 |
| [Memory Management & Garbage Collection](./05_Memory_Management.md) | Private heap, reference counting, the cyclic garbage collector, leaks and how to find them, and memory-efficient objects. | 13 |
| [Data Structures & Algorithms in Python](./06_DSA.md) | Big-O, built-in structure complexities, classic data structures, techniques and common algorithm problems. | 33 |
| [Python for Data, ML & Analytics](./07_Data_and_AI.md) | NumPy, Pandas, data pipelines, ML concepts, analytics and SQL questions asked in data-heavy roles. | 35 |
| [Testing, Type Hints & Tooling](./08_Testing_and_Tooling.md) | pytest, mocking, fixtures, TDD, PEP 8, type hints, virtual environments and packaging. | 10 |

## Suggested reading order
1. **Fundamentals** → 2. **OOP** → 3. **Functional & Decorators** → 4. **Concurrency** → 5. **Memory** → 6. **DSA** → 7. **Data & AI** (if the role is data-heavy) → 8. **Testing & Tooling**.

## 🔥 Most-asked questions — revise these first

| Priority | Question |
|---|---|
| ⭐⭐⭐ | [What is the GIL (Global Interpreter Lock) and why does it exist?](./04_Concurrency.md#q3) |
| ⭐⭐⭐ | [What are Python's mutable and immutable data types?](./01_Fundamentals.md#q2) |
| ⭐⭐⭐ | [What is a Python decorator? What problem does it solve?](./03_Functional_and_Decorators.md#q12) |
| ⭐⭐⭐ | [When do you use threading vs multiprocessing vs asyncio?](./04_Concurrency.md#q6) |
| ⭐⭐⭐ | [What is a coroutine? What do `async def` and `await` do?](./04_Concurrency.md#q24) |
| ⭐⭐⭐ | [How does Python manage memory?](./05_Memory_Management.md#q1) |
| ⭐⭐⭐ | [Why does Python need a garbage collector if it has reference counting?](./05_Memory_Management.md#q3) |
| ⭐⭐⭐ | [What are the 4 pillars of OOP?](./02_OOP.md#q1) |
| ⭐⭐⭐ | [What is MRO (Method Resolution Order)?](./02_OOP.md#q12) |
| ⭐⭐⭐ | [What is the difference between `@staticmethod` and `@classmethod`?](./02_OOP.md#q6) |
| ⭐⭐⭐ | [What is a generator? How is it different from a regular function?](./03_Functional_and_Decorators.md#q7) |
| ⭐⭐⭐ | [What is a closure in Python?](./03_Functional_and_Decorators.md#q1) |
| ⭐⭐⭐ | [What are `*args` and `**kwargs`?](./01_Fundamentals.md#q19) |
| ⭐⭐⭐ | [What is the difference between `deepcopy` and shallow copy?](./01_Fundamentals.md#q9) |
| ⭐⭐⭐ | [What is the LRU Cache? Implement it.](./06_DSA.md#q25) |
| ⭐⭐⭐ | [What is the time complexity of dictionary operations?](./06_DSA.md#q2) |
| ⭐⭐⭐ | [How would you process a CSV file larger than available RAM?](./07_Data_and_AI.md#q13) |
| ⭐⭐⭐ | [What is overfitting? How do you detect and prevent it?](./07_Data_and_AI.md#q22) |

## 🧠 Concept map — learn these together

Each chain builds on the previous idea; every question also has **Related:** links at the bottom of its answer.

| Chain | Questions |
|---|---|
| **Mutability → hashing → dicts** | [What are Python's mutable and immutable data types?](./01_Fundamentals.md#q2) → [How are `__eq__` and `__hash__` related? Why does my object become unhashable?](./02_OOP.md#q28) → [What is a hash table? How does Python's `dict` implement it?](./06_DSA.md#q5) |
| **Functions as objects → closures → decorators** | [What are `*args` and `**kwargs`?](./01_Fundamentals.md#q19) → [What is a closure in Python?](./03_Functional_and_Decorators.md#q1) → [What is a Python decorator? What problem does it solve?](./03_Functional_and_Decorators.md#q12) → [What is `__call__`? How can a class instance be made callable?](./02_OOP.md#q33) |
| **Attributes → property → descriptors → lookup order** | [What is the difference between `@property`, `@setter`, and `@deleter`?](./02_OOP.md#q31) → [What is a descriptor in Python?](./02_OOP.md#q34) → [How does Python look up an attribute on an object?](./02_OOP.md#q35) → [What is the difference between `__getattr__` and `__getattribute__`?](./02_OOP.md#q36) |
| **Inheritance → MRO → super() → mixins** | [What is inheritance? Single vs multiple?](./02_OOP.md#q9) → [What is MRO (Method Resolution Order)?](./02_OOP.md#q12) → [What is `super()`? Why is it important?](./02_OOP.md#q13) → [What is the diamond problem? How does Python resolve it?](./02_OOP.md#q14) → [What is a mixin? When would you use one?](./02_OOP.md#q15) |
| **Generators → lazy pipelines → coroutines → async/await** | [What is a generator? How is it different from a regular function?](./03_Functional_and_Decorators.md#q7) → [What is `yield from`?](./03_Functional_and_Decorators.md#q9) → [How does `await` work under the hood?](./04_Concurrency.md#q25) → [What is the difference between eager and lazy evaluation?](./07_Data_and_AI.md#q14) |
| **Reference counting → GIL → threads** | [What is reference counting?](./05_Memory_Management.md#q2) → [What is the GIL (Global Interpreter Lock) and why does it exist?](./04_Concurrency.md#q3) → [What is a race condition? Show an example and the fix.](./04_Concurrency.md#q8) |
| **fork → copy-on-write → memory** | [What are the start methods fork, spawn and forkserver?](./04_Concurrency.md#q18) → [How does memory behave with multiprocessing and `fork` (copy-on-write)?](./05_Memory_Management.md#q11) |
| **Caching: lru_cache → memoization → leaks** | [How do `functools.lru_cache` / `cache` work, and what are the gotchas?](./03_Functional_and_Decorators.md#q19) → [What is memoization? How does `functools.lru_cache` work?](./06_DSA.md#q21) → [What causes memory leaks in Python?](./05_Memory_Management.md#q6) |
