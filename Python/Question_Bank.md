# Python — Question Bank

Every Python interview question in one list, grouped by topic. Click to jump to the answer.
**(Easy)** fundamentals · **(Medium)** asked in most senior interviews · **(Hard)** internals / deep follow-ups.
**Total: 216 questions in 8 topic files.**


## [Python Fundamentals](./01_Fundamentals.md) — 23 Q

**Part A — Data types & mutability**

1. (Easy) [What is the difference between `is` and `==` in Python?](./01_Fundamentals.md#q1)
2. (Easy) [What are Python's mutable and immutable data types?](./01_Fundamentals.md#q2)
3. (Easy) [What is the difference between a list and a tuple?](./01_Fundamentals.md#q3)
4. (Easy) [What are Python's built-in data structures?](./01_Fundamentals.md#q4)
5. (Easy) [What is string immutability? What happens when you "modify" a string?](./01_Fundamentals.md#q5)
6. (Easy) [What is `None`? How is it different from `0`, `False`, or `""`?](./01_Fundamentals.md#q6)
7. (Medium) [What are Python's truthy and falsy values?](./01_Fundamentals.md#q7)
8. (Medium) [What is the difference between `isinstance()` and `type()`?](./01_Fundamentals.md#q8)
9. (Easy) [What is the difference between `deepcopy` and shallow copy?](./01_Fundamentals.md#q9)

**Part B — Operators, syntax & built-ins**

10. (Easy) [What is the difference between `append()` and `extend()`?](./01_Fundamentals.md#q10)
11. (Easy) [What does the `in` operator do for lists vs dictionaries?](./01_Fundamentals.md#q11)
12. (Medium) [What is the difference between `sorted()` and `.sort()`?](./01_Fundamentals.md#q12)
13. (Easy) [What are list comprehensions? How are they different from a `for` loop?](./01_Fundamentals.md#q13)
14. (Easy) [What is unpacking in Python?](./01_Fundamentals.md#q14)
15. (Easy) [What is the difference between `//` and `/`?](./01_Fundamentals.md#q15)
16. (Easy) [What is the difference between `break`, `continue`, and `pass`?](./01_Fundamentals.md#q16)
17. (Easy) [What is the difference between `range()` in Python 2 vs 3?](./01_Fundamentals.md#q17)
18. (Easy) [What are f-strings? How are they different from `.format()` and `%`?](./01_Fundamentals.md#q18)

**Part C — Functions, scope, modules & context managers**

19. (Medium) [What are `*args` and `**kwargs`?](./01_Fundamentals.md#q19)
20. (Medium) [What is the difference between `global` and `nonlocal`?](./01_Fundamentals.md#q20)
21. (Medium) [What is a Python module vs a package?](./01_Fundamentals.md#q21)
22. (Medium) [What is `__init__.py` and why is it needed?](./01_Fundamentals.md#q22)
23. (Medium) [What is the `with` statement and context managers?](./01_Fundamentals.md#q23)

---

## [Object-Oriented Programming](./02_OOP.md) — 39 Q

**Part A — Classes & objects**

1. (Easy) [What are the 4 pillars of OOP?](./02_OOP.md#q1)
2. (Easy) [What is the difference between a class and an object?](./02_OOP.md#q2)
3. (Easy) [What is a constructor? What is `__init__`?](./02_OOP.md#q3)
4. (Easy) [What is `self` in Python?](./02_OOP.md#q4)
5. (Easy) [What is the difference between class attributes and instance attributes?](./02_OOP.md#q5)
6. (Medium) [What is the difference between `@staticmethod` and `@classmethod`?](./02_OOP.md#q6)
7. (Medium) [What is the difference between `__str__` and `__repr__`?](./02_OOP.md#q7)
8. (Easy) [What is the difference between public, protected, and private attributes?](./02_OOP.md#q8)

**Part B — Inheritance & polymorphism**

9. (Easy) [What is inheritance? Single vs multiple?](./02_OOP.md#q9)
10. (Easy) [What is method overriding?](./02_OOP.md#q10)
11. (Medium) [What is polymorphism? What is duck typing?](./02_OOP.md#q11)
12. (Medium) [What is MRO (Method Resolution Order)?](./02_OOP.md#q12)
13. (Medium) [What is `super()`? Why is it important?](./02_OOP.md#q13)
14. (Hard) [What is the diamond problem? How does Python resolve it?](./02_OOP.md#q14)
15. (Hard) [What is a mixin? When would you use one?](./02_OOP.md#q15)
16. (Medium) [What is the difference between composition and inheritance?](./02_OOP.md#q16)

**Part C — Encapsulation, abstraction & design**

17. (Medium) [What is encapsulation? How does Python achieve it?](./02_OOP.md#q17)
18. (Medium) [What is abstraction? How do ABCs work?](./02_OOP.md#q18)
19. (Medium) [What is the difference between an ABC and a Protocol?](./02_OOP.md#q19)
20. (Medium) [What are SOLID principles?](./02_OOP.md#q20)
21. (Hard) [What is the Liskov Substitution Principle (LSP)?](./02_OOP.md#q21)
22. (Medium) [How do you implement dependency injection in Python?](./02_OOP.md#q22)
23. (Hard) [What design patterns have you used? Explain Singleton, Factory, Observer.](./02_OOP.md#q23)
24. (Medium) [Does Python support method overloading?](./02_OOP.md#q24)
25. (Easy) [What are Enums and why use them?](./02_OOP.md#q25)

**Part D — Data classes & special methods**

26. (Easy) [What are dataclasses and why use them?](./02_OOP.md#q26)
27. (Medium) [Dataclass vs NamedTuple vs Pydantic model — when to use which?](./02_OOP.md#q27)
28. (Medium) [How are `__eq__` and `__hash__` related? Why does my object become unhashable?](./02_OOP.md#q28)
29. (Medium) [What are Python's dunder (magic) methods? Name 5 commonly used ones.](./02_OOP.md#q29)
30. (Hard) [What is the Python data model? How does operator overloading work?](./02_OOP.md#q30)
31. (Hard) [What is the difference between `@property`, `@setter`, and `@deleter`?](./02_OOP.md#q31)
32. (Hard) [What is name mangling in Python?](./02_OOP.md#q32)
33. (Hard) [What is `__call__`? How can a class instance be made callable?](./02_OOP.md#q33)

**Part E — Internals: descriptors, attribute lookup, metaclasses**

34. (Hard) [What is a descriptor in Python?](./02_OOP.md#q34)
35. (Hard) [How does Python look up an attribute on an object?](./02_OOP.md#q35)
36. (Hard) [What is the difference between `__getattr__` and `__getattribute__`?](./02_OOP.md#q36)
37. (Hard) [What is the difference between `__new__` and `__init__`?](./02_OOP.md#q37)
38. (Hard) [What is a metaclass in Python?](./02_OOP.md#q38)
39. (Medium) [What is monkey patching? When is it acceptable?](./02_OOP.md#q39)

---

## [Functional Programming, Generators & Decorators](./03_Functional_and_Decorators.md) — 25 Q

**Part A — Functional programming**

1. (Medium) [What is a closure in Python?](./03_Functional_and_Decorators.md#q1)
2. (Medium) [What is a lambda function? When should you use/avoid it?](./03_Functional_and_Decorators.md#q2)
3. (Medium) [What is `map()`, `filter()`, and `reduce()`?](./03_Functional_and_Decorators.md#q3)
4. (Medium) [What is a pure function?](./03_Functional_and_Decorators.md#q4)
5. (Medium) [What is `functools.partial`?](./03_Functional_and_Decorators.md#q5)
6. (Medium) [What is immutability and why is it important in functional programming?](./03_Functional_and_Decorators.md#q6)

**Part B — Iterators & generators**

7. (Medium) [What is a generator? How is it different from a regular function?](./03_Functional_and_Decorators.md#q7)
8. (Medium) [What is the difference between `yield` and `return`?](./03_Functional_and_Decorators.md#q8)
9. (Medium) [What is `yield from`?](./03_Functional_and_Decorators.md#q9)
10. (Medium) [What is a generator expression vs a list comprehension?](./03_Functional_and_Decorators.md#q10)
11. (Medium) [What is `itertools`? Name 5 useful functions.](./03_Functional_and_Decorators.md#q11)

**Part C — Decorators**

12. (Medium) [What is a Python decorator? What problem does it solve?](./03_Functional_and_Decorators.md#q12)
13. (Easy) [When does a decorator run?](./03_Functional_and_Decorators.md#q13)
14. (Medium) [How do you write a class-based decorator (and a stateful one)?](./03_Functional_and_Decorators.md#q14)
15. (Medium) [What is a class decorator?](./03_Functional_and_Decorators.md#q15)
16. (Medium) [How do you decorate methods of a class?](./03_Functional_and_Decorators.md#q16)
17. (Hard) [How do you write a decorator that works both with and without arguments?](./03_Functional_and_Decorators.md#q17)
18. (Medium) [How do you write a decorator for async functions?](./03_Functional_and_Decorators.md#q18)
19. (Medium) [How do `functools.lru_cache` / `cache` work, and what are the gotchas?](./03_Functional_and_Decorators.md#q19)
20. (Medium) [What is the difference between `@property`, `@functools.cached_property` and `@lru_cache` on a method?](./03_Functional_and_Decorators.md#q20)
21. (Easy) [Which built-in / standard-library decorators should you know?](./03_Functional_and_Decorators.md#q21)
22. (Medium) [What decorators do you use in Django, DRF, FastAPI and Celery?](./03_Functional_and_Decorators.md#q22)
23. (Hard) [How do you keep type hints correct for decorated functions?](./03_Functional_and_Decorators.md#q23)
24. (Medium) [Write a decorator that checks a user's role before running a function (RBAC).](./03_Functional_and_Decorators.md#q24)
25. (Medium) [What are the downsides of decorators?](./03_Functional_and_Decorators.md#q25)

---

## [Concurrency: GIL, Threading, Multiprocessing & asyncio](./04_Concurrency.md) — 38 Q

**Part A — Concurrency basics & the GIL**

1. (Easy) [What is the difference between concurrency and parallelism?](./04_Concurrency.md#q1)
2. (Easy) [What is the difference between a process and a thread?](./04_Concurrency.md#q2)
3. (Medium) [What is the GIL (Global Interpreter Lock) and why does it exist?](./04_Concurrency.md#q3)
4. (Medium) [How does the GIL affect CPU-bound vs I/O-bound programs?](./04_Concurrency.md#q4)
5. (Medium) [Is the GIL being removed? What is free-threaded Python?](./04_Concurrency.md#q5)
6. (Easy) [When do you use threading vs multiprocessing vs asyncio?](./04_Concurrency.md#q6)

**Part B — Multithreading**

7. (Easy) [How do you create and run threads in Python?](./04_Concurrency.md#q7)
8. (Medium) [What is a race condition? Show an example and the fix.](./04_Concurrency.md#q8)
9. (Medium) [What are Lock, RLock, Semaphore, Event and Condition?](./04_Concurrency.md#q9)
10. (Medium) [What is a deadlock and how do you avoid it?](./04_Concurrency.md#q10)
11. (Medium) [How do threads safely share data? Explain the producer–consumer pattern.](./04_Concurrency.md#q11)
12. (Medium) [Are Python operations like `list.append()` or `x += 1` thread-safe?](./04_Concurrency.md#q12)
13. (Easy) [What is a daemon thread?](./04_Concurrency.md#q13)
14. (Medium) [What is thread-local storage?](./04_Concurrency.md#q14)
15. (Easy) [What is ThreadPoolExecutor and why use it instead of raw threads?](./04_Concurrency.md#q15)

**Part C — Multiprocessing**

16. (Easy) [How do you use multiprocessing in Python?](./04_Concurrency.md#q16)
17. (Medium) [How do processes share data and communicate?](./04_Concurrency.md#q17)
18. (Hard) [What are the start methods fork, spawn and forkserver?](./04_Concurrency.md#q18)
19. (Easy) [Why do you need `if __name__ == "__main__":` with multiprocessing?](./04_Concurrency.md#q19)
20. (Medium) [What are the limitations of passing data between processes (pickling)?](./04_Concurrency.md#q20)
21. (Medium) [What is the difference between `map`, `submit` and `as_completed` in executors?](./04_Concurrency.md#q21)
22. (Medium) [When is multiprocessing a bad idea?](./04_Concurrency.md#q22)

**Part D — Async programming (asyncio, async/await)**

23. (Easy) [What is asyncio and what is the event loop?](./04_Concurrency.md#q23)
24. (Easy) [What is a coroutine? What do `async def` and `await` do?](./04_Concurrency.md#q24)
25. (Medium) [How does `await` work under the hood?](./04_Concurrency.md#q25)
26. (Easy) [How do you run multiple coroutines concurrently?](./04_Concurrency.md#q26)
27. (Medium) [What is the difference between `gather`, `wait` and `TaskGroup`?](./04_Concurrency.md#q27)
28. (Medium) [What happens if you call blocking code inside an async function? How do you fix it?](./04_Concurrency.md#q28)
29. (Medium) [How do timeouts and cancellation work in asyncio?](./04_Concurrency.md#q29)
30. (Medium) [What are `async with`, `async for` and async generators?](./04_Concurrency.md#q30)
31. (Medium) [How do you limit concurrency, e.g. calling an API for 10,000 URLs?](./04_Concurrency.md#q31)
32. (Medium) [How do you build a producer–consumer pipeline with asyncio?](./04_Concurrency.md#q32)
33. (Medium) [What is the difference between threads and asyncio?](./04_Concurrency.md#q33)
34. (Medium) [How is async used in Django and FastAPI?](./04_Concurrency.md#q34)
35. (Medium) [What are common asyncio mistakes?](./04_Concurrency.md#q35)

**Part E — Scenario questions**

36. (Medium) [A web API must resize uploaded images (CPU-heavy). How do you design it?](./04_Concurrency.md#q36)
37. (Medium) [You need to call 5 external APIs for one request. How do you make it fast?](./04_Concurrency.md#q37)
38. (Hard) [A Python service is stuck / hanging in production. How do you debug it?](./04_Concurrency.md#q38)

---

## [Memory Management & Garbage Collection](./05_Memory_Management.md) — 13 Q

**Part A — How Python manages memory**

1. (Medium) [How does Python manage memory?](./05_Memory_Management.md#q1)
2. (Easy) [What is reference counting?](./05_Memory_Management.md#q2)
3. (Medium) [Why does Python need a garbage collector if it has reference counting?](./05_Memory_Management.md#q3)
4. (Medium) [How does the generational garbage collector work?](./05_Memory_Management.md#q4)
5. (Medium) [What can you do with the `gc` module? When would you tune it?](./05_Memory_Management.md#q5)

**Part B — Leaks, tools & production behaviour**

6. (Medium) [What causes memory leaks in Python?](./05_Memory_Management.md#q6)
7. (Medium) [How do you find a memory leak in a Python application?](./05_Memory_Management.md#q7)
8. (Medium) [What is a weak reference and when do you use it?](./05_Memory_Management.md#q8)
9. (Medium) [Does `sys.getsizeof()` show the real memory used by an object?](./05_Memory_Management.md#q9)
10. (Hard) [Does Python release memory back to the operating system?](./05_Memory_Management.md#q10)
11. (Hard) [How does memory behave with multiprocessing and `fork` (copy-on-write)?](./05_Memory_Management.md#q11)

**Part C — Memory-efficient objects**

12. (Medium) [What are `__slots__` and how do they save memory?](./05_Memory_Management.md#q12)
13. (Medium) [What is `__del__` and why should you be careful with it?](./05_Memory_Management.md#q13)

---

## [Data Structures & Algorithms in Python](./06_DSA.md) — 33 Q

**Part A — Core data structures & complexity**

1. (Easy) [What is the time complexity of common list operations?](./06_DSA.md#q1)
2. (Easy) [What is the time complexity of dictionary operations?](./06_DSA.md#q2)
3. (Easy) [What is the difference between a stack and a queue?](./06_DSA.md#q3)
4. (Easy) [What is a linked list? How is it different from a Python list?](./06_DSA.md#q4)
5. (Easy) [What is a hash table? How does Python's `dict` implement it?](./06_DSA.md#q5)
6. (Easy) [What is a hash collision? How is it resolved?](./06_DSA.md#q6)
7. (Easy) [What is Big-O notation?](./06_DSA.md#q7)
8. (Easy) [What is the difference between linear search and binary search?](./06_DSA.md#q8)
9. (Easy) [What is a set in Python? What are its time complexities?](./06_DSA.md#q9)
10. (Easy) [What is a deque? When would you use it over a list?](./06_DSA.md#q10)

**Part B — Techniques & classic structures**

11. (Medium) [What is a heap? How does Python's `heapq` work?](./06_DSA.md#q11)
12. (Medium) [What is the difference between BFS and DFS?](./06_DSA.md#q12)
13. (Medium) [What is dynamic programming? Memoization vs tabulation?](./06_DSA.md#q13)
14. (Medium) [What is the sliding window technique?](./06_DSA.md#q14)
15. (Medium) [What is the two-pointer technique?](./06_DSA.md#q15)
16. (Medium) [What is the difference between stable and unstable sorting?](./06_DSA.md#q16)
17. (Medium) [What sorting algorithm does Python use?](./06_DSA.md#q17)
18. (Medium) [What is a trie (prefix tree)?](./06_DSA.md#q18)
19. (Medium) [What is a graph? Directed vs undirected?](./06_DSA.md#q19)
20. (Medium) [What is a binary search tree (BST)?](./06_DSA.md#q20)
21. (Medium) [What is memoization? How does `functools.lru_cache` work?](./06_DSA.md#q21)
22. (Medium) [What is the difference between recursion and iteration?](./06_DSA.md#q22)
23. (Medium) [What is the time complexity of merge sort vs quicksort?](./06_DSA.md#q23)
24. (Medium) [What is amortized time complexity?](./06_DSA.md#q24)
25. (Medium) [What is the LRU Cache? Implement it.](./06_DSA.md#q25)

**Part C — Advanced algorithms & problems**

26. (Hard) [What is Dijkstra's algorithm?](./06_DSA.md#q26)
27. (Hard) [What is the difference between greedy algorithms and DP?](./06_DSA.md#q27)
28. (Hard) [What is topological sort?](./06_DSA.md#q28)
29. (Hard) [What is the union-find (disjoint set) data structure?](./06_DSA.md#q29)
30. (Hard) [What is space-time tradeoff?](./06_DSA.md#q30)
31. (Hard) [Merge K sorted arrays.](./06_DSA.md#q31)
32. (Hard) [Find the longest common subsequence (LCS).](./06_DSA.md#q32)
33. (Hard) [Find all permutations of a string/array.](./06_DSA.md#q33)

---

## [Python for Data, ML & Analytics](./07_Data_and_AI.md) — 35 Q

**Part A — NumPy & Pandas**

1. (Medium) [What is the difference between a Python list and a NumPy array?](./07_Data_and_AI.md#q1)
2. (Medium) [What is vectorization in NumPy?](./07_Data_and_AI.md#q2)
3. (Medium) [What is broadcasting in NumPy?](./07_Data_and_AI.md#q3)
4. (Medium) [What is a Pandas DataFrame vs a Series?](./07_Data_and_AI.md#q4)
5. (Medium) [What is the difference between `loc` and `iloc`?](./07_Data_and_AI.md#q5)
6. (Medium) [What is `groupby` in Pandas? How does it work?](./07_Data_and_AI.md#q6)
7. (Medium) [What is the difference between `merge`, `join`, and `concat`?](./07_Data_and_AI.md#q7)
8. (Medium) [What is a pivot table?](./07_Data_and_AI.md#q8)
9. (Medium) [How would you handle missing values (NaN) in Pandas?](./07_Data_and_AI.md#q9)
10. (Medium) [What is the difference between `apply`, `map`, and `applymap`?](./07_Data_and_AI.md#q10)
11. (Medium) [What is method chaining in Pandas?](./07_Data_and_AI.md#q11)
12. (Medium) [What is the difference between wide and long (tidy) data formats?](./07_Data_and_AI.md#q12)

**Part B — Data engineering**

13. (Hard) [How would you process a CSV file larger than available RAM?](./07_Data_and_AI.md#q13)
14. (Hard) [What is the difference between eager and lazy evaluation?](./07_Data_and_AI.md#q14)
15. (Hard) [What is a data pipeline? Key considerations?](./07_Data_and_AI.md#q15)
16. (Hard) [What is the difference between ETL and ELT?](./07_Data_and_AI.md#q16)

**Part C — Machine-learning concepts**

17. (Hard) [What is feature engineering? Give 3 examples.](./07_Data_and_AI.md#q17)
18. (Hard) [What is data leakage in machine learning?](./07_Data_and_AI.md#q18)
19. (Hard) [What is the difference between normalization and standardization?](./07_Data_and_AI.md#q19)
20. (Hard) [What is cross-validation? Why is it important?](./07_Data_and_AI.md#q20)
21. (Medium) [What is the difference between supervised, unsupervised, and reinforcement learning?](./07_Data_and_AI.md#q21)
22. (Medium) [What is overfitting? How do you detect and prevent it?](./07_Data_and_AI.md#q22)
23. (Medium) [What is the bias-variance tradeoff?](./07_Data_and_AI.md#q23)
24. (Medium) [What is a confusion matrix? Precision, recall, F1, accuracy?](./07_Data_and_AI.md#q24)
25. (Medium) [What is the difference between classification and regression?](./07_Data_and_AI.md#q25)
26. (Medium) [What is feature importance? How would you explain a model to a non-technical stakeholder?](./07_Data_and_AI.md#q26)
27. (Medium) [What is A/B testing? What statistical concepts are involved?](./07_Data_and_AI.md#q27)

**Part D — Analytics, warehousing & SQL**

28. (Medium) [What is a data warehouse vs a data lake?](./07_Data_and_AI.md#q28)
29. (Medium) [What is the difference between OLTP and OLAP?](./07_Data_and_AI.md#q29)
30. (Medium) [What makes a good data visualization?](./07_Data_and_AI.md#q30)
31. (Medium) [What is the difference between a KPI and a metric?](./07_Data_and_AI.md#q31)
32. (Medium) [What is SQL? Key JOIN types?](./07_Data_and_AI.md#q32)
33. (Medium) [What is the difference between `GROUP BY` and `PARTITION BY`?](./07_Data_and_AI.md#q33)
34. (Medium) [What is an index in a database? How does it improve performance?](./07_Data_and_AI.md#q34)
35. (Medium) [What is data normalization in databases?](./07_Data_and_AI.md#q35)

---

## [Testing, Type Hints & Tooling](./08_Testing_and_Tooling.md) — 10 Q

**Part A — Testing**

1. (Medium) [What is unit testing? Unit vs integration vs E2E?](./08_Testing_and_Tooling.md#q1)
2. (Medium) [What is `pytest`? How is it different from `unittest`?](./08_Testing_and_Tooling.md#q2)
3. (Medium) [What is a mock? When would you use `unittest.mock`?](./08_Testing_and_Tooling.md#q3)
4. (Medium) [What is a fixture in pytest?](./08_Testing_and_Tooling.md#q4)
5. (Medium) [What is test-driven development (TDD)?](./08_Testing_and_Tooling.md#q5)

**Part B — Code quality & tooling**

6. (Medium) [What is PEP 8? Name 5 key style guidelines.](./08_Testing_and_Tooling.md#q6)
7. (Medium) [What is type hinting in Python? What are its benefits?](./08_Testing_and_Tooling.md#q7)
8. (Medium) [What is the difference between `typing.Optional` and `typing.Union`?](./08_Testing_and_Tooling.md#q8)
9. (Medium) [What is a virtual environment? Why is it important?](./08_Testing_and_Tooling.md#q9)
10. (Medium) [What is the difference between `requirements.txt` and `pyproject.toml`?](./08_Testing_and_Tooling.md#q10)
