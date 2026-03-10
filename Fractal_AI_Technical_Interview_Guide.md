# 🎯 Fractal AI — 1-Hour Technical Interview Prep Guide
### Python + React | Organized by Category & Difficulty

---

## ⏱️ 3 Tips for the 1-Hour Interview

1. **Think out loud, always.** Interviewers at AI/analytics companies like Fractal care as much about *how* you think as the final answer. Narrate your approach before writing code: "I'm thinking of using a hash map here for O(1) lookups..."

2. **Clarify before coding.** Spend 30–60 seconds asking clarifying questions (edge cases, input constraints, expected output). This shows engineering maturity and prevents wasted effort.

3. **Manage time actively.** If stuck on a hard problem for >5 minutes, say: "Let me start with a brute-force approach and then optimize." A working O(n²) solution is better than silence. Always mention the time/space complexity of your solution.

---

# 🐍 PYTHON

---

## 📦 Category 1: Python Fundamentals

### 🟢 Easy

---

**Q1: What is the difference between `is` and `==` in Python?**

> `==` checks **value equality**; `is` checks **identity** (same object in memory).

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  — same values
print(a is b)   # False — different objects
print(a is c)   # True  — same object (c points to a)

# Gotcha: small integers (-5 to 256) are cached
x = 256
y = 256
print(x is y)   # True (cached)

x = 257
y = 257
print(x is y)   # False (not cached)
```

---

**Q2: What are Python's mutable vs immutable types?**

| Immutable | Mutable |
|-----------|---------|
| `int`, `float`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset` | `bytearray` |

> **Key insight:** Using a mutable default argument is a classic Python bug:

```python
# ❌ Bug: list is shared across all calls
def append_to(element, to=[]):
    to.append(element)
    return to

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] — unexpected!

# ✅ Fix
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```

---

**Q3: Explain list comprehensions vs generator expressions.**

```python
# List comprehension — creates entire list in memory
squares_list = [x**2 for x in range(1000000)]  # ~8MB

# Generator expression — lazy evaluation, memory efficient
squares_gen = (x**2 for x in range(1000000))   # ~120 bytes

# Use generators when you only need to iterate once
total = sum(x**2 for x in range(1000000))  # No intermediate list

# With condition
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

---

### 🟡 Medium

---

**Q4: What are `*args` and `**kwargs`? When would you use them?**

```python
def log_event(event_type, *args, **kwargs):
    """
    *args  → variable positional arguments (tuple)
    **kwargs → variable keyword arguments (dict)
    """
    print(f"Event: {event_type}")
    print(f"Positional: {args}")
    print(f"Named: {kwargs}")

log_event("click", "button1", "button2", user="alice", timestamp=1234567890)
# Event: click
# Positional: ('button1', 'button2')
# Named: {'user': 'alice', 'timestamp': 1234567890}

# Unpacking with * and **
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))       # 6

params = {'a': 1, 'b': 2, 'c': 3}
print(add(**params))    # 6
```

---

**Q5: Explain Python decorators with a practical example.**

```python
import time
import functools

# Decorator factory (with arguments)
def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)  # Preserves original function metadata
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt+1} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url):
    # Simulates an API call that might fail
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return {"data": "success"}

# Real-world use cases: logging, caching, auth, rate limiting, timing
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper
```

---

**Q6: What is the GIL (Global Interpreter Lock) and how does it affect concurrency?**

> The GIL is a mutex in CPython that allows only **one thread to execute Python bytecode at a time**, even on multi-core systems.

```python
import threading
import multiprocessing
import asyncio

# ❌ Threading — limited by GIL for CPU-bound tasks
# ✅ Threading — works well for I/O-bound tasks (network, disk)
def io_bound_task():
    import time
    time.sleep(1)  # GIL is released during I/O

# ✅ Multiprocessing — bypasses GIL, true parallelism for CPU-bound
def cpu_bound_task(n):
    return sum(i * i for i in range(n))

with multiprocessing.Pool(4) as pool:
    results = pool.map(cpu_bound_task, [10**6] * 4)

# ✅ asyncio — single-threaded concurrency for I/O-bound
async def fetch(url):
    # Non-blocking I/O
    pass

# Rule of thumb:
# CPU-bound → multiprocessing
# I/O-bound → asyncio or threading
```

---

### 🔴 Hard

---

**Q7: Explain Python's memory management and garbage collection.**

```python
import sys
import gc

# Reference counting — primary mechanism
a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount arg)

b = a
print(sys.getrefcount(a))  # 3

del b
print(sys.getrefcount(a))  # 2

# Cyclic garbage collector handles reference cycles
class Node:
    def __init__(self):
        self.ref = None

node1 = Node()
node2 = Node()
node1.ref = node2  # node1 → node2
node2.ref = node1  # node2 → node1 (cycle!)

del node1
del node2
# Reference counts are 1 each (not 0), so refcount alone can't free them
# Python's cyclic GC (gc module) detects and collects these

gc.collect()  # Force collection

# Memory optimization tips:
# 1. Use __slots__ to reduce per-instance memory
class Point:
    __slots__ = ['x', 'y']  # ~40% less memory than dict-based
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 2. Use generators for large datasets
# 3. Use numpy arrays instead of Python lists for numerical data
```

---

## 📦 Category 2: Data Structures & Algorithms

### 🟢 Easy

---

**Q8: Reverse a string / check if a string is a palindrome.**

```python
# Reverse a string
s = "hello"
reversed_s = s[::-1]          # "olleh"
reversed_s = "".join(reversed(s))  # "olleh"

# Palindrome check
def is_palindrome(s: str) -> bool:
    # Clean: lowercase, alphanumeric only
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

# Two-pointer approach (O(n) time, O(1) space)
def is_palindrome_two_pointer(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("A man, a plan, a canal: Panama"))  # True
```

---

**Q9: Find the two numbers in a list that sum to a target.**

```python
from typing import List, Optional

def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Brute force: O(n²) time, O(1) space
    Hash map:    O(n)  time, O(n) space  ← preferred
    """
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None

print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
```

---

### 🟡 Medium

---

**Q10: Implement a stack using a queue and vice versa.**

```python
from collections import deque

# Stack using two queues
class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        # Rotate so newest element is at front
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q

# LRU Cache — very common in AI/data pipeline interviews
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove LRU item

cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))   # 1
cache.put(3, 3)       # evicts key 2
print(cache.get(2))   # -1 (not found)
```

---

**Q11: Find the longest substring without repeating characters.**

```python
def length_of_longest_substring(s: str) -> int:
    """
    Sliding window approach: O(n) time, O(min(m,n)) space
    where m = charset size
    """
    char_index = {}  # char → last seen index
    max_len = 0
    left = 0

    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1  # Shrink window
        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

print(length_of_longest_substring("abcabcbb"))  # 3 ("abc")
print(length_of_longest_substring("pwwkew"))    # 3 ("wke")
print(length_of_longest_substring(""))          # 0
```

---

**Q12: Binary search and its variants.**

```python
from typing import List

def binary_search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2  # Avoids integer overflow
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Find first occurrence (leftmost)
def search_first(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

# Search in rotated sorted array
def search_rotated(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

---

### 🔴 Hard

---

**Q13: Merge K sorted lists / arrays (common in data pipeline interviews).**

```python
import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Min-heap approach: O(N log k) time, O(k) space
    N = total nodes, k = number of lists
    """
    heap = []
    
    # Initialize heap with first node of each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    dummy = ListNode(0)
    current = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next

# Simpler version with arrays (more common in data engineering)
def merge_k_sorted_arrays(arrays: List[List[int]]) -> List[int]:
    heap = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    
    result = []
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))
    
    return result

print(merge_k_sorted_arrays([[1,4,7],[2,5,8],[3,6,9]]))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 📦 Category 3: Object-Oriented Programming

### 🟡 Medium

---

**Q14: Explain the 4 pillars of OOP with Python examples.**

```python
# 1. ENCAPSULATION — bundling data + methods, restricting direct access
class BankAccount:
    def __init__(self, balance: float):
        self.__balance = balance  # Private attribute (name mangling)
    
    @property
    def balance(self) -> float:
        return self.__balance
    
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__balance += amount
    
    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

# 2. INHERITANCE — reusing and extending behavior
class Animal:
    def __init__(self, name: str):
        self.name = name
    
    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says Meow!"

# 3. POLYMORPHISM — same interface, different behavior
animals = [Dog("Rex"), Cat("Whiskers"), Dog("Buddy")]
for animal in animals:
    print(animal.speak())  # Each calls its own speak()

# 4. ABSTRACTION — hiding complexity, exposing interface
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def load(self, source: str) -> None: ...
    
    @abstractmethod
    def transform(self) -> None: ...
    
    @abstractmethod
    def save(self, destination: str) -> None: ...
    
    def run_pipeline(self, source: str, destination: str) -> None:
        """Template method pattern"""
        self.load(source)
        self.transform()
        self.save(destination)
```

---

**Q15: What are `classmethod`, `staticmethod`, and instance methods?**

```python
class DataModel:
    _registry = {}  # Class-level state
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
    
    # Instance method — has access to self (instance)
    def describe(self) -> str:
        return f"Model: {self.name} v{self.version}"
    
    # Class method — has access to cls (class), not instance
    # Use for: alternative constructors, factory methods
    @classmethod
    def from_dict(cls, data: dict) -> 'DataModel':
        return cls(data['name'], data['version'])
    
    @classmethod
    def register(cls, model: 'DataModel') -> None:
        cls._registry[model.name] = model
    
    # Static method — no access to self or cls
    # Use for: utility functions logically related to the class
    @staticmethod
    def validate_version(version: str) -> bool:
        import re
        return bool(re.match(r'^\d+\.\d+\.\d+$', version))

# Usage
m1 = DataModel("GPT", "4.0.0")
m2 = DataModel.from_dict({"name": "BERT", "version": "1.0.0"})
print(DataModel.validate_version("2.1.3"))  # True
```

---

**Q16: Explain Python's MRO (Method Resolution Order) and `super()`.**

```python
# Diamond inheritance problem
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")
        super().method()

class C(A):
    def method(self):
        print("C.method")
        super().method()

class D(B, C):
    def method(self):
        print("D.method")
        super().method()

d = D()
d.method()
# D.method → B.method → C.method → A.method
# Python uses C3 linearization algorithm

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

---

## 📦 Category 4: Python for Data & AI (Fractal-Specific)

### 🟡 Medium

---

**Q17: How would you handle large datasets efficiently in Python?**

```python
import pandas as pd
import numpy as np

# 1. Use chunking for large CSV files
def process_large_csv(filepath: str, chunk_size: int = 10000):
    results = []
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        # Process each chunk
        processed = chunk.groupby('category')['value'].sum()
        results.append(processed)
    return pd.concat(results).groupby(level=0).sum()

# 2. Optimize dtypes to reduce memory
def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Low cardinality
            df[col] = df[col].astype('category')
    return df

# 3. Vectorized operations vs loops
import time

data = np.random.randn(1_000_000)

# ❌ Slow: Python loop
start = time.time()
result = [x**2 for x in data]
print(f"Loop: {time.time() - start:.3f}s")

# ✅ Fast: NumPy vectorized
start = time.time()
result = data**2
print(f"NumPy: {time.time() - start:.3f}s")  # ~50x faster
```

---

**Q18: Explain closures and how they're used in Python.**

```python
# Closure: inner function that captures variables from enclosing scope
def make_multiplier(factor: float):
    def multiply(x: float) -> float:
        return x * factor  # 'factor' is captured from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))   # 10
print(triple(5))   # 15

# Practical use: configurable data transformers
def make_normalizer(mean: float, std: float):
    def normalize(x):
        return (x - mean) / std
    return normalize

# Fit on training data
train_mean, train_std = 50.0, 10.0
normalizer = make_normalizer(train_mean, train_std)

# Apply to any data (captures training stats)
test_data = [45, 55, 60, 40]
normalized = [normalizer(x) for x in test_data]
print(normalized)  # [-0.5, 0.5, 1.0, -1.0]
```

---

**Q19: What are Python generators and when would you use them in a data pipeline?**

```python
from typing import Generator, Iterator
import json

# Generator function — yields values lazily
def read_jsonl(filepath: str) -> Generator[dict, None, None]:
    """Stream large JSONL files without loading all into memory"""
    with open(filepath, 'r') as f:
        for line in f:
            yield json.loads(line.strip())

# Generator pipeline — compose transformations lazily
def filter_records(records, key: str, value):
    return (r for r in records if r.get(key) == value)

def extract_field(records, field: str):
    return (r[field] for r in records if field in r)

# Compose pipeline — nothing executes until consumed
# records = read_jsonl("data.jsonl")
# active = filter_records(records, "status", "active")
# names = extract_field(active, "name")
# result = list(names)  # Only now does data flow through

# yield from — delegate to sub-generator
def chain_files(filepaths: list) -> Iterator[dict]:
    for path in filepaths:
        yield from read_jsonl(path)

# send() — two-way communication with generator
def running_average() -> Generator[float, float, None]:
    total = 0.0
    count = 0
    while True:
        value = yield (total / count if count else 0)
        total += value
        count += 1

avg = running_average()
next(avg)           # Prime the generator
print(avg.send(10)) # 10.0
print(avg.send(20)) # 15.0
print(avg.send(30)) # 20.0
```

---

# ⚛️ REACT

---

## 📦 Category 5: React Hooks

### 🟢 Easy

---

**Q20: What is the difference between `useState` and `useRef`?**

```jsx
import { useState, useRef, useEffect } from 'react';

function Counter() {
  // useState: triggers re-render when value changes
  const [count, setCount] = useState(0);
  
  // useRef: persists value across renders WITHOUT triggering re-render
  const renderCount = useRef(0);
  const inputRef = useRef(null);  // DOM reference
  
  useEffect(() => {
    renderCount.current += 1;  // Mutate directly, no re-render
  });
  
  return (
    <div>
      <p>Count: {count}</p>
      <p>Renders: {renderCount.current}</p>
      <input ref={inputRef} />
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={() => inputRef.current.focus()}>Focus Input</button>
    </div>
  );
}

// Key differences:
// useState → reactive, causes re-render
// useRef   → mutable container, no re-render, persists across renders
// useRef use cases: DOM access, storing previous values, timers/intervals
```

---

**Q21: Explain `useEffect` with all its dependency array patterns.**

```jsx
import { useState, useEffect } from 'react';

function DataFetcher({ userId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Pattern 1: No dependency array → runs after EVERY render
  useEffect(() => {
    console.log('Runs after every render');
  });

  // Pattern 2: Empty array [] → runs ONCE after mount
  useEffect(() => {
    console.log('Runs once on mount');
    return () => console.log('Cleanup on unmount');
  }, []);

  // Pattern 3: With dependencies → runs when deps change
  useEffect(() => {
    let cancelled = false;  // Cleanup flag for race conditions
    
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        if (!cancelled) {  // Ignore if component unmounted or userId changed
          setData(data);
          setLoading(false);
        }
      });
    
    return () => {
      cancelled = true;  // Cleanup: cancel stale requests
    };
  }, [userId]);  // Re-run when userId changes

  if (loading) return <div>Loading...</div>;
  return <div>{JSON.stringify(data)}</div>;
}
```

---

### 🟡 Medium

---

**Q22: What is `useMemo` and `useCallback`? When should you use them?**

```jsx
import { useState, useMemo, useCallback, memo } from 'react';

// useMemo: memoize COMPUTED VALUES (expensive calculations)
function DataDashboard({ data, filter }) {
  // ❌ Without useMemo: recalculates on every render
  // const filteredData = data.filter(item => item.category === filter);
  
  // ✅ With useMemo: only recalculates when data or filter changes
  const filteredData = useMemo(() => {
    console.log('Filtering data...');
    return data.filter(item => item.category === filter);
  }, [data, filter]);
  
  const stats = useMemo(() => ({
    count: filteredData.length,
    total: filteredData.reduce((sum, item) => sum + item.value, 0),
    avg: filteredData.length 
      ? filteredData.reduce((sum, item) => sum + item.value, 0) / filteredData.length 
      : 0
  }), [filteredData]);
  
  return <div>{stats.count} items, avg: {stats.avg.toFixed(2)}</div>;
}

// useCallback: memoize FUNCTIONS (stable references for child components)
function ParentComponent() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState([]);
  
  // ❌ Without useCallback: new function reference on every render
  // const handleDelete = (id) => setItems(items.filter(i => i.id !== id));
  
  // ✅ With useCallback: stable reference, ChildList won't re-render unnecessarily
  const handleDelete = useCallback((id) => {
    setItems(prev => prev.filter(i => i.id !== id));
  }, []);  // No deps because we use functional update
  
  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <ChildList items={items} onDelete={handleDelete} />
    </>
  );
}

// memo: prevent re-render if props haven't changed
const ChildList = memo(({ items, onDelete }) => {
  console.log('ChildList rendered');
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          {item.name}
          <button onClick={() => onDelete(item.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
});

// Rule of thumb:
// Don't over-optimize! Use these only when:
// 1. You have measurable performance issues
// 2. The computation is genuinely expensive
// 3. You're passing callbacks to memoized children
```

---

**Q23: Build a custom hook for data fetching.**

```jsx
import { useState, useEffect, useCallback } from 'react';

// Custom hook — reusable stateful logic
function useFetch(url, options = {}) {
  const [state, setState] = useState({
    data: null,
    loading: true,
    error: null,
  });
  
  const [refetchIndex, setRefetchIndex] = useState(0);
  
  const refetch = useCallback(() => {
    setRefetchIndex(i => i + 1);
  }, []);
  
  useEffect(() => {
    if (!url) return;
    
    const controller = new AbortController();
    
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    fetch(url, { ...options, signal: controller.signal })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return res.json();
      })
      .then(data => setState({ data, loading: false, error: null }))
      .catch(err => {
        if (err.name !== 'AbortError') {
          setState({ data: null, loading: false, error: err.message });
        }
      });
    
    return () => controller.abort();
  }, [url, refetchIndex]);
  
  return { ...state, refetch };
}

// Usage
function UserProfile({ userId }) {
  const { data: user, loading, error, refetch } = useFetch(
    userId ? `/api/users/${userId}` : null
  );
  
  if (loading) return <Spinner />;
  if (error) return <Error message={error} onRetry={refetch} />;
  return <div>{user?.name}</div>;
}
```

---

**Q24: Explain `useReducer` and when to prefer it over `useState`.**

```jsx
import { useReducer } from 'react';

// Action types as constants (prevents typos)
const ACTIONS = {
  ADD_ITEM: 'ADD_ITEM',
  REMOVE_ITEM: 'REMOVE_ITEM',
  UPDATE_QUANTITY: 'UPDATE_QUANTITY',
  CLEAR_CART: 'CLEAR_CART',
};

// Pure reducer function — easy to test
function cartReducer(state, action) {
  switch (action.type) {
    case ACTIONS.ADD_ITEM: {
      const existing = state.items.find(i => i.id === action.payload.id);
      if (existing) {
        return {
          ...state,
          items: state.items.map(i =>
            i.id === action.payload.id
              ? { ...i, quantity: i.quantity + 1 }
              : i
          ),
        };
      }
      return {
        ...state,
        items: [...state.items, { ...action.payload, quantity: 1 }],
      };
    }
    case ACTIONS.REMOVE_ITEM:
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload.id),
      };
    case ACTIONS.CLEAR_CART:
      return { ...state, items: [] };
    default:
      return state;
  }
}

const initialState = { items: [], discount: 0 };

function ShoppingCart() {
  const [cart, dispatch] = useReducer(cartReducer, initialState);
  
  const total = cart.items.reduce(
    (sum, item) => sum + item.price * item.quantity, 0
  );
  
  return (
    <div>
      {cart.items.map(item => (
        <div key={item.id}>
          {item.name} × {item.quantity}
          <button onClick={() => dispatch({ type: ACTIONS.REMOVE_ITEM, payload: { id: item.id } })}>
            Remove
          </button>
        </div>
      ))}
      <p>Total: ${total.toFixed(2)}</p>
      <button onClick={() => dispatch({ type: ACTIONS.CLEAR_CART })}>Clear</button>
    </div>
  );
}

// Use useReducer when:
// ✅ State has multiple sub-values
// ✅ Next state depends on previous state
// ✅ Complex state transitions (like a state machine)
// ✅ You want to separate state logic from UI
```

---

## 📦 Category 6: State Management

### 🟡 Medium

---

**Q25: Explain React Context API and its limitations.**

```jsx
import { createContext, useContext, useState, useMemo } from 'react';

// 1. Create context with default value
const ThemeContext = createContext({
  theme: 'light',
  toggleTheme: () => {},
});

// 2. Provider component — split state and dispatch to avoid unnecessary re-renders
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  // Memoize context value to prevent unnecessary re-renders
  const value = useMemo(() => ({
    theme,
    toggleTheme: () => setTheme(t => t === 'light' ? 'dark' : 'light'),
  }), [theme]);
  
  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// 3. Custom hook for consuming context (with error boundary)
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage
function ThemedButton() {
  const { theme, toggleTheme } = useTheme();
  return (
    <button
      style={{ background: theme === 'light' ? '#fff' : '#333' }}
      onClick={toggleTheme}
    >
      Toggle Theme
    </button>
  );
}

// ⚠️ Context limitations:
// 1. All consumers re-render when context value changes
// 2. Not optimized for high-frequency updates (use Zustand/Redux for that)
// 3. No built-in selector support (unlike Redux useSelector)
// Solution: Split contexts by update frequency, or use state management library
```

---

**Q26: When would you use Redux vs Context API vs Zustand?**

```jsx
// CONTEXT API — best for:
// ✅ Low-frequency updates (theme, auth, locale)
// ✅ Simple apps without complex state interactions
// ✅ No extra dependencies

// REDUX TOOLKIT — best for:
// ✅ Large apps with complex state
// ✅ Need for time-travel debugging (Redux DevTools)
// ✅ Predictable state with strict unidirectional flow
// ✅ Team environments with clear conventions

import { createSlice, configureStore } from '@reduxjs/toolkit';

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState: { data: [], filters: {}, loading: false },
  reducers: {
    setFilters: (state, action) => {
      state.filters = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
  },
  // Handle async with createAsyncThunk
});

// ZUSTAND — best for:
// ✅ Simple global state without boilerplate
// ✅ Performance-critical apps (fine-grained subscriptions)
// ✅ Small to medium apps

import { create } from 'zustand';

const useStore = create((set, get) => ({
  data: [],
  filters: {},
  loading: false,
  
  setFilters: (filters) => set({ filters }),
  
  fetchData: async () => {
    set({ loading: true });
    const data = await fetch('/api/data').then(r => r.json());
    set({ data, loading: false });
  },
  
  // Computed values
  get filteredData() {
    return get().data.filter(/* apply filters */);
  },
}));
```

---

## 📦 Category 7: Component Lifecycle & Patterns

### 🟡 Medium

---

**Q27: What is the component lifecycle in React (functional components)?**

```jsx
import { useState, useEffect, useLayoutEffect, useRef } from 'react';

function LifecycleDemo({ id }) {
  const [data, setData] = useState(null);
  const mountTime = useRef(Date.now());
  
  // MOUNT — equivalent to componentDidMount
  useEffect(() => {
    console.log('Component mounted');
    // Initialize subscriptions, fetch data, set up timers
    
    // UNMOUNT — equivalent to componentWillUnmount
    return () => {
      console.log('Component unmounted');
      // Clean up subscriptions, cancel requests, clear timers
    };
  }, []);
  
  // UPDATE — equivalent to componentDidUpdate
  useEffect(() => {
    console.log(`id changed to: ${id}`);
    // React to prop/state changes
  }, [id]);
  
  // useLayoutEffect — fires synchronously BEFORE browser paint
  // Use for: DOM measurements, preventing visual flicker
  useLayoutEffect(() => {
    // Runs synchronously after DOM mutations but before paint
    // Equivalent to componentDidMount/Update but synchronous
  }, []);
  
  // Render phase — pure, no side effects
  return <div>{data?.name}</div>;
}

// Lifecycle order:
// 1. Render (pure)
// 2. DOM update
// 3. useLayoutEffect cleanup (sync)
// 4. useLayoutEffect (sync)
// 5. Browser paint
// 6. useEffect cleanup (async)
// 7. useEffect (async)
```

---

**Q28: Explain React's reconciliation and the importance of `key` prop.**

```jsx
// React uses a diffing algorithm (O(n)) with two assumptions:
// 1. Elements of different types produce different trees
// 2. Keys hint which elements are stable across renders

// ❌ Bad: using index as key (causes bugs with reordering/deletion)
function BadList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item.name}</li>  // Index shifts on delete!
      ))}
    </ul>
  );
}

// ✅ Good: use stable, unique IDs
function GoodList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

// Key trick: force component remount (reset state)
function ProfilePage({ userId }) {
  return (
    // When userId changes, React destroys and recreates UserProfile
    // This resets all internal state — useful for "fresh start"
    <UserProfile key={userId} userId={userId} />
  );
}
```

---

## 📦 Category 8: Performance Optimization

### 🔴 Hard

---

**Q29: How would you optimize a React app that renders a list of 10,000 items?**

```jsx
import { useState, useCallback } from 'react';
import { FixedSizeList as List } from 'react-window';  // Virtual scrolling

// SOLUTION 1: Virtual scrolling (most impactful)
function VirtualizedList({ items }) {
  const Row = useCallback(({ index, style }) => (
    <div style={style}>
      {items[index].name} — {items[index].value}
    </div>
  ), [items]);
  
  return (
    <List
      height={600}        // Visible area height
      itemCount={items.length}
      itemSize={50}       // Each row height
      width="100%"
    >
      {Row}
    </List>
  );
}

// SOLUTION 2: Pagination
function PaginatedList({ items, pageSize = 50 }) {
  const [page, setPage] = useState(0);
  const start = page * pageSize;
  const visibleItems = items.slice(start, start + pageSize);
  
  return (
    <>
      {visibleItems.map(item => <Item key={item.id} item={item} />)}
      <button onClick={() => setPage(p => p - 1)} disabled={page === 0}>Prev</button>
      <button onClick={() => setPage(p => p + 1)} disabled={start + pageSize >= items.length}>Next</button>
    </>
  );
}

// SOLUTION 3: Infinite scroll with Intersection Observer
function InfiniteList({ fetchMore }) {
  const [items, setItems] = useState([]);
  const loaderRef = useRef(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) {
          fetchMore().then(newItems => setItems(prev => [...prev, ...newItems]));
        }
      },
      { threshold: 0.1 }
    );
    
    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => observer.disconnect();
  }, [fetchMore]);
  
  return (
    <>
      {items.map(item => <Item key={item.id} item={item} />)}
      <div ref={loaderRef}>Loading more...</div>
    </>
  );
}
```

---

**Q30: What is code splitting and lazy loading in React?**

```jsx
import { lazy, Suspense, useState } from 'react';

// Code splitting with React.lazy — loads component only when needed
const HeavyDashboard = lazy(() => import('./HeavyDashboard'));
const AnalyticsChart = lazy(() => 
  import('./AnalyticsChart').then(module => ({
    default: module.AnalyticsChart  // Named export
  }))
);

function App() {
  const [showDashboard, setShowDashboard] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShowDashboard(true)}>Load Dashboard</button>
      
      {showDashboard && (
        <Suspense fallback={<div>Loading dashboard...</div>}>
          <HeavyDashboard />
        </Suspense>
      )}
    </div>
  );
}

// Route-based code splitting (most common pattern)
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Analytics = lazy(() => import('./pages/Analytics'));
const Reports = lazy(() => import('./pages/Reports'));

function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

---

## 📦 Category 9: Advanced React Patterns

### 🔴 Hard

---

**Q31: Explain the Compound Component pattern.**

```jsx
import { createContext, useContext, useState } from 'react';

// Compound Components — components that work together, sharing implicit state
// Example: Tabs component

const TabsContext = createContext(null);

function Tabs({ children, defaultTab }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabList({ children }) {
  return <div className="tab-list" role="tablist">{children}</div>;
};

Tabs.Tab = function Tab({ id, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
      className={activeTab === id ? 'active' : ''}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function TabPanel({ id, children }) {
  const { activeTab } = useContext(TabsContext);
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
};

// Clean, flexible usage
function Dashboard() {
  return (
    <Tabs defaultTab="overview">
      <Tabs.List>
        <Tabs.Tab id="overview">Overview</Tabs.Tab>
        <Tabs.Tab id="analytics">Analytics</Tabs.Tab>
        <Tabs.Tab id="reports">Reports</Tabs.Tab>
      </Tabs.List>
      <Tabs.Panel id="overview"><OverviewContent /></Tabs.Panel>
      <Tabs.Panel id="analytics"><AnalyticsContent /></Tabs.Panel>
      <Tabs.Panel id="reports"><ReportsContent /></Tabs.Panel>
    </Tabs>
  );
}
```

---

**Q32: How do you handle errors in React? Explain Error Boundaries.**

```jsx
import { Component } from 'react';

// Error Boundaries — must be class components (no hook equivalent yet)
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }
  
  // Render fallback UI after error
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  // Log error details
  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
    // Send to error tracking service (Sentry, Datadog, etc.)
    // logErrorToService(error, errorInfo);
    this.setState({ errorInfo });
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>Something went wrong.</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage — wrap sections independently
function App() {
  return (
    <ErrorBoundary fallback={<div>App crashed</div>}>
      <ErrorBoundary fallback={<div>Chart failed to load</div>}>
        <AnalyticsChart />
      </ErrorBoundary>
      <ErrorBoundary fallback={<div>Table failed to load</div>}>
        <DataTable />
      </ErrorBoundary>
    </ErrorBoundary>
  );
}

// Note: Error boundaries do NOT catch:
// - Event handlers (use try/catch)
// - Async code (use try/catch in useEffect)
// - Server-side rendering errors
// - Errors in the error boundary itself
```

---

## 📦 Category 10: AI/Analytics Specific (Fractal AI Focus)

### 🟡 Medium

---

**Q33: How would you build a real-time data dashboard in React?**

```jsx
import { useState, useEffect, useRef, useCallback } from 'react';

// WebSocket hook for real-time data
function useWebSocket(url) {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('connecting');
  const wsRef = useRef(null);
  const reconnectTimeout = useRef(null);
  
  const connect = useCallback(() => {
    wsRef.current = new WebSocket(url);
    
    wsRef.current.onopen = () => setStatus('connected');
    
    wsRef.current.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      setData(parsed);
    };
    
    wsRef.current.onclose = () => {
      setStatus('disconnected');
      // Auto-reconnect with exponential backoff
      reconnectTimeout.current = setTimeout(connect, 3000);
    };
    
    wsRef.current.onerror = () => setStatus('error');
  }, [url]);
  
  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectTimeout.current);
      wsRef.current?.close();
    };
  }, [connect]);
  
  const send = useCallback((message) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);
  
  return { data, status, send };
}

// Throttled chart updates (prevent too many re-renders)
function useThrottledValue(value, delay = 100) {
  const [throttled, setThrottled] = useState(value);
  const lastUpdate = useRef(Date.now());
  
  useEffect(() => {
    const now = Date.now();
    if (now - lastUpdate.current >= delay) {
      setThrottled(value);
      lastUpdate.current = now;
    } else {
      const timeout = setTimeout(() => {
        setThrottled(value);
        lastUpdate.current = Date.now();
      }, delay - (now - lastUpdate.current));
      return () => clearTimeout(timeout);
    }
  }, [value, delay]);
  
  return throttled;
}

function RealTimeDashboard() {
  const { data, status } = useWebSocket('wss://api.fractal.ai/stream');
  const throttledData = useThrottledValue(data, 200);  // Max 5 updates/sec
  
  return (
    <div>
      <StatusIndicator status={status} />
      {throttledData && <MetricsChart data={throttledData} />}
    </div>
  );
}
```

---

**Q34: How would you implement a search with debouncing in React?**

```jsx
import { useState, useEffect, useCallback } from 'react';

// Custom debounce hook
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);  // Cancel on value change
  }, [value, delay]);
  
  return debouncedValue;
}

// Search component with debouncing + abort controller
function SearchBar({ onResults }) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const debouncedQuery = useDebounce(query, 300);  // Wait 300ms after typing stops
  
  useEffect(() => {
    if (!debouncedQuery.trim()) {
      onResults([]);
      return;
    }
    
    const controller = new AbortController();
    setLoading(true);
    
    fetch(`/api/search?q=${encodeURIComponent(debouncedQuery)}`, {
      signal: controller.signal
    })
      .then(res => res.json())
      .then(results => {
        onResults(results);
        setLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') setLoading(false);
      });
    
    return () => controller.abort();  // Cancel previous request
  }, [debouncedQuery, onResults]);
  
  return (
    <div>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search analytics..."
      />
      {loading && <Spinner />}
    </div>
  );
}
```

---

## 📦 Category 11: System Design & Architecture

### 🔴 Hard

---

**Q35: How would you design a frontend architecture for an AI analytics platform?**

```
📐 High-Level Architecture for Fractal AI Dashboard

┌─────────────────────────────────────────────────────────┐
│                    React Application                     │
├─────────────────────────────────────────────────────────┤
│  Pages (Route-based code splitting)                      │
│  ├── /dashboard    → Overview metrics                    │
│  ├── /analytics    → Deep-dive charts                    │
│  ├── /models       → ML model management                 │
│  └── /reports      → Generated reports                   │
├─────────────────────────────────────────────────────────┤
│  State Management                                        │
│  ├── Server State  → React Query / TanStack Query        │
│  │   (caching, background refetch, optimistic updates)   │
│  └── Client State  → Zustand                             │
│      (UI state, filters, user preferences)               │
├─────────────────────────────────────────────────────────┤
│  Data Layer                                              │
│  ├── REST API      → Axios with interceptors             │
│  ├── WebSocket     → Real-time metric streaming          │
│  └── GraphQL       → Flexible data fetching              │
├─────────────────────────────────────────────────────────┤
│  Performance                                             │
│  ├── Virtual scrolling (react-window)                    │
│  ├── Chart memoization (recharts/D3)                     │
│  ├── Web Workers for heavy computations                  │
│  └── Service Worker for offline support                  │
└─────────────────────────────────────────────────────────┘
```

```jsx
// React Query for server state — handles caching, refetching, loading states
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useModelMetrics(modelId, timeRange) {
  return useQuery({
    queryKey: ['metrics', modelId, timeRange],
    queryFn: () => fetchMetrics(modelId, timeRange),
    staleTime: 5 * 60 * 1000,    // Consider fresh for 5 minutes
    gcTime: 10 * 60 * 1000,      // Keep in cache for 10 minutes
    refetchInterval: 30 * 1000,  // Background refetch every 30s
    select: (data) => ({         // Transform/select data
      accuracy: data.metrics.accuracy,
      f1Score: data.metrics.f1,
      predictions: data.predictions.slice(-100),
    }),
  });
}

function ModelDashboard({ modelId }) {
  const [timeRange, setTimeRange] = useState('7d');
  const { data, isLoading, error } = useModelMetrics(modelId, timeRange);
  
  if (isLoading) return <MetricsSkeleton />;
  if (error) return <ErrorState error={error} />;
  
  return (
    <div>
      <MetricsCard accuracy={data.accuracy} f1={data.f1Score} />
      <PredictionChart data={data.predictions} />
    </div>
  );
}
```

---

## 📦 Quick Reference: Complexity Cheat Sheet

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| Binary Search | O(log n) | O(1) | Sorted array required |
| Hash Map lookup | O(1) avg | O(n) | Amortized |
| Sorting (Timsort) | O(n log n) | O(n) | Python's default |
| BFS/DFS | O(V+E) | O(V) | Graph traversal |
| Heap push/pop | O(log n) | O(n) | Priority queue |
| Dynamic Programming | Varies | Varies | Memoize overlapping subproblems |

---

## 📦 Python Quick Wins to Mention

```python
# Walrus operator (Python 3.8+)
if (n := len(data)) > 10:
    print(f"List is too long ({n} elements)")

# Structural pattern matching (Python 3.10+)
match command:
    case "quit": quit()
    case "help": show_help()
    case _: print("Unknown command")

# dataclasses — clean data containers
from dataclasses import dataclass, field
from typing import List

@dataclass
class ModelConfig:
    name: str
    version: str
    hyperparams: dict = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Model name cannot be empty")

# TypedDict for type-safe dicts
from typing import TypedDict

class MetricResult(TypedDict):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
```

---

## 🎯 Final Checklist Before the Interview

- [ ] Review Big-O notation for common operations
- [ ] Practice explaining your thought process out loud
- [ ] Know the difference between `==` and `is`, mutable vs immutable
- [ ] Be able to implement a custom React hook from scratch
- [ ] Understand when to use `useMemo`/`useCallback` (and when NOT to)
- [ ] Know Python's GIL and when to use threading vs multiprocessing
- [ ] Be ready to discuss a past project involving data processing or UI performance
- [ ] Prepare 2–3 questions to ask the interviewer about Fractal AI's tech stack

---

*Good luck! Remember: clarity of thought > perfect syntax. Interviewers want to see how you reason.*
