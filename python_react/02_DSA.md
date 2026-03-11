# 🧮 02 — Data Structures & Algorithms
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟢 Easy (Q1–Q10)](#easy)
- [🟡 Medium (Q11–Q25)](#medium)
- [🔴 Hard (Q26–Q33)](#hard)

---

<a name="easy"></a>
## 🟢 Easy

---

### Q1. What is the time complexity of common list operations?

| Operation | Time | Notes |
|-----------|------|-------|
| `lst[i]` | O(1) | Random access |
| `append(x)` | O(1) amortized | Occasional O(n) resize |
| `pop()` (end) | O(1) | |
| `pop(i)` (middle) | O(n) | Shifts elements |
| `insert(i, x)` | O(n) | Shifts elements |
| `x in lst` | O(n) | Linear scan |
| `len(lst)` | O(1) | Stored as attribute |
| `lst.sort()` | O(n log n) | Timsort |
| `lst + lst2` | O(n+m) | Creates new list |

```python
# Demonstration
import timeit

lst = list(range(100_000))

# O(1) — fast regardless of size
timeit.timeit(lambda: lst[-1], number=100_000)

# O(n) — slow for large lists
timeit.timeit(lambda: 99_999 in lst, number=1_000)

# Use deque for O(1) operations at both ends
from collections import deque
dq = deque(lst)
dq.appendleft(0)   # O(1)
dq.popleft()       # O(1)
```

---

### Q2. What is the time complexity of dictionary operations?

| Operation | Average | Worst Case | Notes |
|-----------|---------|------------|-------|
| `d[key]` | O(1) | O(n) | Hash collision |
| `d[key] = val` | O(1) | O(n) | |
| `del d[key]` | O(1) | O(n) | |
| `key in d` | O(1) | O(n) | |
| `len(d)` | O(1) | | |
| `d.keys()` | O(1) | | Returns view |
| Iteration | O(n) | | |

```python
# Why O(1)? Hash function maps key → bucket index
# Collision resolution: open addressing (CPython)

# Worst case O(n): all keys hash to same bucket (rare with good hash)

# dict is ordered (insertion order) since Python 3.7
d = {'b': 2, 'a': 1, 'c': 3}
print(list(d.keys()))  # ['b', 'a', 'c'] — insertion order preserved
```

---

### Q3. What is the difference between a stack and a queue?

**Answer:**
- **Stack** — LIFO (Last In, First Out): push/pop from the same end
- **Queue** — FIFO (First In, First Out): enqueue at back, dequeue from front

```python
from collections import deque

# Stack — use list or deque
stack = []
stack.append(1)    # push
stack.append(2)
stack.append(3)
print(stack.pop()) # 3 — LIFO

# Queue — use deque (O(1) both ends) NOT list (list.pop(0) is O(n))
queue = deque()
queue.append(1)      # enqueue
queue.append(2)
queue.append(3)
print(queue.popleft())  # 1 — FIFO

# Real-world use cases:
# Stack: undo/redo, function call stack, DFS, expression parsing
# Queue: BFS, task scheduling, print queue, message broker

# Python's queue module for thread-safe queues
from queue import Queue, LifoQueue, PriorityQueue
```

---

### Q4. What is a linked list? How is it different from a Python list?

**Answer:**
A linked list is a sequence of **nodes**, each containing data and a pointer to the next node.

| Feature | Python List (Array) | Linked List |
|---------|---------------------|-------------|
| Memory | Contiguous | Non-contiguous |
| Index access | O(1) | O(n) |
| Insert at head | O(n) | O(1) |
| Insert at tail | O(1) amortized | O(1) with tail pointer |
| Memory overhead | Low | High (pointer per node) |

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Build: 1 → 2 → 3
head = ListNode(1, ListNode(2, ListNode(3)))

# Traverse
current = head
while current:
    print(current.val)
    current = current.next

# Reverse a linked list (common interview question)
def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev  # new head

# Python doesn't have a built-in linked list
# Use collections.deque for O(1) operations at both ends
```

---

### Q5. What is a hash table? How does Python's `dict` implement it?

**Answer:**
A hash table maps keys to values using a **hash function** to compute an index into an array of buckets.

```
key → hash(key) → index → bucket → value
```

```python
# Python dict internals (simplified):
# 1. Compute hash: hash("name") → some integer
# 2. Map to index: index = hash % table_size
# 3. Store (key, value) at that index
# 4. On collision: probe next slot (open addressing in CPython)

# Custom hashable object
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))  # Tuple hash

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

p1 = Point(1, 2)
p2 = Point(1, 2)
d = {p1: "origin"}
print(d[p2])  # "origin" — p1 == p2 and hash(p1) == hash(p2)

# Rule: if __eq__ is defined, __hash__ must also be defined
# Mutable objects (list, dict) are not hashable — can't be dict keys
```

---

### Q6. What is a hash collision? How is it resolved?

**Answer:**
A collision occurs when two different keys produce the **same hash index**.

**Resolution strategies:**
1. **Open addressing** (CPython's approach) — probe next available slot
2. **Chaining** — each bucket holds a linked list of entries

```python
# Demonstration of collision concept
print(hash("abc") % 8)   # some index
print(hash("bca") % 8)   # might be same index → collision

# CPython uses open addressing with pseudo-random probing
# Load factor: when dict is ~2/3 full, it resizes (doubles) to reduce collisions

# Why this matters:
# - Good hash function → uniform distribution → O(1) average
# - Bad hash function → many collisions → O(n) worst case
# - Python's built-in types have well-designed hash functions
```

---

### Q7. What is Big-O notation?

**Answer:**
Big-O describes the **upper bound** of an algorithm's time or space complexity as input size grows.

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Dict lookup, array index |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Linear search, single loop |
| O(n log n) | Linearithmic | Merge sort, Timsort |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Recursive Fibonacci (naive) |
| O(n!) | Factorial | Permutations |

```python
# O(1) — constant
def get_first(lst): return lst[0]

# O(log n) — binary search
def binary_search(lst, target):
    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] == target: return mid
        elif lst[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1

# O(n) — single pass
def find_max(lst): return max(lst)

# O(n²) — nested loops
def has_duplicate(lst):
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]: return True
    return False

# O(n) — better approach using set
def has_duplicate_fast(lst): return len(lst) != len(set(lst))
```

---

### Q8. What is the difference between linear search and binary search?

| Feature | Linear Search | Binary Search |
|---------|--------------|---------------|
| Time | O(n) | O(log n) |
| Requirement | None | **Sorted** array |
| Space | O(1) | O(1) iterative |

```python
# Linear search — works on unsorted data
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# Binary search — requires sorted data
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # Avoids overflow
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Python's bisect module
import bisect
arr = [1, 3, 5, 7, 9, 11]
idx = bisect.bisect_left(arr, 7)   # 3 — index where 7 would be inserted
print(arr[idx] == 7)               # True — found
```

---

### Q9. What is a set in Python? What are its time complexities?

**Answer:**
A set is an **unordered collection of unique, hashable elements** backed by a hash table.

| Operation | Time |
|-----------|------|
| `add(x)` | O(1) avg |
| `remove(x)` | O(1) avg |
| `x in s` | O(1) avg |
| `s1 \| s2` (union) | O(len(s1) + len(s2)) |
| `s1 & s2` (intersection) | O(min(len(s1), len(s2))) |
| `s1 - s2` (difference) | O(len(s1)) |

```python
# Set operations
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}

print(a | b)   # {1, 2, 3, 4, 5, 6, 7} — union
print(a & b)   # {3, 4, 5}             — intersection
print(a - b)   # {1, 2}                — difference
print(a ^ b)   # {1, 2, 6, 7}         — symmetric difference

# Common use: remove duplicates while preserving order
def unique_ordered(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

print(unique_ordered([3, 1, 2, 1, 3, 4]))  # [3, 1, 2, 4]
```

---

### Q10. What is a deque? When would you use it over a list?

**Answer:**
`deque` (double-ended queue) supports **O(1) append and pop from both ends**, unlike a list which is O(n) for operations at the front.

```python
from collections import deque

dq = deque([1, 2, 3])
dq.appendleft(0)    # O(1) — [0, 1, 2, 3]
dq.append(4)        # O(1) — [0, 1, 2, 3, 4]
dq.popleft()        # O(1) — returns 0
dq.pop()            # O(1) — returns 4

# maxlen — sliding window
window = deque(maxlen=3)
for x in [1, 2, 3, 4, 5]:
    window.append(x)
    print(list(window))
# [1] → [1,2] → [1,2,3] → [2,3,4] → [3,4,5]

# Use deque when:
# ✅ BFS (queue)
# ✅ Sliding window
# ✅ Undo/redo history with max size
# ✅ Frequent insertions/deletions at both ends
```

---

<a name="medium"></a>
## 🟡 Medium

---

### Q11. What is a heap? How does Python's `heapq` work?

**Answer:**
A heap is a **complete binary tree** where each parent is smaller (min-heap) or larger (max-heap) than its children. Python's `heapq` implements a **min-heap**.

```python
import heapq

# heapq operates on a regular list
nums = [3, 1, 4, 1, 5, 9, 2, 6]
heapq.heapify(nums)          # O(n) — convert list to heap in-place
print(nums[0])               # 1 — smallest element always at index 0

heapq.heappush(nums, 0)      # O(log n) — add element
print(heapq.heappop(nums))   # O(log n) — remove and return smallest

# Get N smallest/largest
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
print(heapq.nsmallest(3, data))  # [1, 1, 2]
print(heapq.nlargest(3, data))   # [9, 6, 5]

# Max-heap trick: negate values
max_heap = [-x for x in data]
heapq.heapify(max_heap)
print(-heapq.heappop(max_heap))  # 9 — largest

# Priority queue with tuples (priority, item)
tasks = []
heapq.heappush(tasks, (3, "low priority"))
heapq.heappush(tasks, (1, "high priority"))
heapq.heappush(tasks, (2, "medium priority"))
print(heapq.heappop(tasks))  # (1, 'high priority')
```

---

### Q12. What is the difference between BFS and DFS?

| Feature | BFS | DFS |
|---------|-----|-----|
| Data structure | Queue | Stack (or recursion) |
| Order | Level by level | Deep first |
| Shortest path | ✅ (unweighted) | ❌ |
| Memory | O(w) — width | O(h) — height |
| Use cases | Shortest path, level order | Topological sort, cycle detection, maze |

```python
from collections import deque

# Graph as adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [], 'E': [], 'F': []
}

# BFS — uses queue
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

# DFS — uses stack (iterative) or recursion
def dfs(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    return order

print(bfs(graph, 'A'))   # ['A', 'B', 'C', 'D', 'E', 'F']
print(dfs(graph, 'A'))   # ['A', 'B', 'D', 'E', 'C', 'F']
```

---

### Q13. What is dynamic programming? Memoization vs tabulation?

**Answer:**
DP solves problems by breaking them into **overlapping subproblems** and storing results to avoid recomputation.

- **Memoization** (top-down): recursive + cache results
- **Tabulation** (bottom-up): iterative + fill table

```python
# Classic: Fibonacci

# ❌ Naive recursion — O(2ⁿ)
def fib_naive(n):
    if n <= 1: return n
    return fib_naive(n-1) + fib_naive(n-2)

# ✅ Memoization (top-down) — O(n) time, O(n) space
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1: return n
    return fib_memo(n-1) + fib_memo(n-2)

# ✅ Tabulation (bottom-up) — O(n) time, O(n) space
def fib_tab(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# ✅ Space-optimized — O(n) time, O(1) space
def fib_opt(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Coin change problem — classic DP
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change([1, 5, 10, 25], 36))  # 3 (25+10+1)
```

---

### Q14. What is the sliding window technique?

**Answer:**
Sliding window maintains a **window of elements** that slides through the array, avoiding redundant recomputation. Used for subarray/substring problems.

```python
# Maximum sum subarray of size k
def max_sum_subarray(arr, k):
    n = len(arr)
    if n < k:
        return -1

    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, n):
        window_sum += arr[i] - arr[i - k]  # Slide: add new, remove old
        max_sum = max(max_sum, window_sum)

    return max_sum

print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3))  # 9 (5+1+3)

# Variable-size window: longest substring with at most k distinct chars
def longest_k_distinct(s, k):
    char_count = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        char_count[char] = char_count.get(char, 0) + 1

        while len(char_count) > k:
            left_char = s[left]
            char_count[left_char] -= 1
            if char_count[left_char] == 0:
                del char_count[left_char]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len

print(longest_k_distinct("araaci", 2))  # 4 ("araa")
```

---

### Q15. What is the two-pointer technique?

**Answer:**
Two pointers move through an array (from both ends or at different speeds) to solve problems in O(n) instead of O(n²).

```python
# Two Sum in sorted array
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

# Remove duplicates from sorted array (in-place)
def remove_duplicates(nums):
    if not nums: return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1

# Detect cycle in linked list (Floyd's algorithm)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# Container with most water
def max_water(heights):
    left, right = 0, len(heights) - 1
    max_area = 0
    while left < right:
        area = min(heights[left], heights[right]) * (right - left)
        max_area = max(max_area, area)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return max_area
```

---

### Q16. What is the difference between stable and unstable sorting?

**Answer:**
- **Stable sort** — preserves the **relative order** of equal elements
- **Unstable sort** — may change the relative order of equal elements

```python
students = [
    {"name": "Alice", "grade": 90},
    {"name": "Bob",   "grade": 85},
    {"name": "Carol", "grade": 90},
]

# Python's sort is STABLE (Timsort)
# Sort by grade — Alice and Carol both have 90, Alice stays before Carol
sorted_students = sorted(students, key=lambda s: s["grade"])
print([s["name"] for s in sorted_students])
# ['Bob', 'Alice', 'Carol'] — Alice before Carol (stable)

# Multi-key sort using stability
# Sort by grade desc, then name asc
result = sorted(students, key=lambda s: (-s["grade"], s["name"]))
```

---

### Q17. What sorting algorithm does Python use?

**Answer:**
Python uses **Timsort** — a hybrid of merge sort and insertion sort.

| Property | Value |
|----------|-------|
| Time (best) | O(n) — already sorted |
| Time (average) | O(n log n) |
| Time (worst) | O(n log n) |
| Space | O(n) |
| Stable | ✅ Yes |

```python
# Timsort finds "runs" (already sorted sequences) and merges them
# Insertion sort for small runs (< 64 elements)
# Merge sort for larger sequences

# Python's sort is highly optimized — usually faster than manual implementations
import random
data = random.sample(range(1_000_000), 1_000_000)
data.sort()  # Timsort — very fast in practice
```

---

### Q18. What is a trie (prefix tree)?

**Answer:**
A trie is a tree where each node represents a **character**, and paths from root to leaf spell out words. Used for autocomplete, spell check, IP routing.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

trie = Trie()
for word in ["apple", "app", "application", "apply"]:
    trie.insert(word)

print(trie.search("app"))         # True
print(trie.search("ap"))          # False
print(trie.starts_with("appl"))   # True
```

---

### Q19. What is a graph? Directed vs undirected?

**Answer:**
A graph is a set of **vertices (nodes)** connected by **edges**.

- **Directed (digraph)** — edges have direction (A → B ≠ B → A)
- **Undirected** — edges are bidirectional (A — B = B — A)
- **Weighted** — edges have costs/distances
- **Cyclic/Acyclic** — contains/doesn't contain cycles

```python
# Adjacency list representation (most common)
# Undirected graph
undirected = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# Directed graph
directed = {
    0: [1, 2],
    1: [3],
    2: [3],
    3: []
}

# Adjacency matrix (for dense graphs)
# matrix[i][j] = 1 if edge from i to j
n = 4
matrix = [[0] * n for _ in range(n)]
matrix[0][1] = 1  # edge 0 → 1

# Weighted graph
weighted = {
    'A': [('B', 4), ('C', 2)],
    'B': [('D', 3)],
    'C': [('B', 1), ('D', 5)],
    'D': []
}
```

---

### Q20. What is a binary search tree (BST)?

**Answer:**
A BST is a binary tree where for every node:
- All values in the **left subtree** are **less than** the node
- All values in the **right subtree** are **greater than** the node

| Operation | Average | Worst (unbalanced) |
|-----------|---------|-------------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

```python
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if not node:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        return node

    def search(self, val):
        return self._search(self.root, val)

    def _search(self, node, val):
        if not node or node.val == val:
            return node
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    def inorder(self):
        """Returns sorted values"""
        result = []
        def traverse(node):
            if node:
                traverse(node.left)
                result.append(node.val)
                traverse(node.right)
        traverse(self.root)
        return result
```

---

### Q21. What is memoization? How does `functools.lru_cache` work?

**Answer:**
Memoization caches the results of function calls so repeated calls with the same arguments return the cached result.

```python
from functools import lru_cache
import time

# Without memoization — O(2ⁿ)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

# With lru_cache — O(n)
@lru_cache(maxsize=128)  # Cache up to 128 results
def fib_cached(n):
    if n <= 1: return n
    return fib_cached(n-1) + fib_cached(n-2)

# lru_cache uses a dict internally: {args: result}
# LRU = Least Recently Used — evicts oldest when maxsize reached
# maxsize=None → unlimited cache (use cache instead)

from functools import cache  # Python 3.9+ — equivalent to lru_cache(maxsize=None)

@cache
def expensive_computation(n):
    time.sleep(0.1)
    return n * n

# Cache info
print(fib_cached.cache_info())
# CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)

fib_cached.cache_clear()  # Clear the cache
```

---

### Q22. What is the difference between recursion and iteration?

**Answer:**
- **Recursion** — function calls itself; uses call stack; elegant but can cause stack overflow
- **Iteration** — uses loops; more memory-efficient; generally faster

```python
import sys

# Python's default recursion limit
print(sys.getrecursionlimit())  # 1000

# Recursive factorial — O(n) time, O(n) space (call stack)
def factorial_recursive(n):
    if n <= 1: return 1
    return n * factorial_recursive(n - 1)

# Iterative factorial — O(n) time, O(1) space
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Convert recursion to iteration using explicit stack
def dfs_iterative(graph, start):
    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])

# Increase recursion limit (use carefully)
sys.setrecursionlimit(10_000)
```

---

### Q23. What is the time complexity of merge sort vs quicksort?

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |

```python
# Merge sort — guaranteed O(n log n), stable
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Quicksort — O(n²) worst case (sorted input with bad pivot)
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]  # Middle pivot avoids worst case
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)

# When to use:
# Merge sort: need stable sort, linked lists, external sorting
# Quicksort: in-place sorting, cache-friendly, average case faster
```

---

### Q24. What is amortized time complexity?

**Answer:**
Amortized analysis averages the cost of operations over a sequence, even if individual operations are occasionally expensive.

```python
import sys

# Python list append — amortized O(1)
# Occasionally triggers O(n) resize, but averaged over n appends = O(1)

lst = []
sizes = []
for i in range(20):
    lst.append(i)
    sizes.append(sys.getsizeof(lst))

# You'll see sizes jump at: 0, 4, 8, 16, 25, 35... (growth factor ~1.125)
# Each resize doubles capacity → total work = n + n/2 + n/4 + ... = 2n = O(n)
# Per operation: O(n) / n operations = O(1) amortized

# Same concept applies to:
# - dict resizing
# - StringBuilder in Java
# - Dynamic arrays in general
```

---

### Q25. What is the LRU Cache? Implement it.

**Answer:**
LRU (Least Recently Used) cache evicts the least recently accessed item when capacity is full.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()  # Maintains insertion order

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
            self.cache.popitem(last=False)  # Remove LRU (first item)

# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))   # 1 — access key 1 (now most recent)
cache.put(3, 3)       # evicts key 2 (least recently used)
print(cache.get(2))   # -1 (evicted)
print(cache.get(3))   # 3
cache.put(4, 4)       # evicts key 1
print(cache.get(1))   # -1 (evicted)
print(cache.get(3))   # 3
print(cache.get(4))   # 4
```

---

<a name="hard"></a>
## 🔴 Hard

---

### Q26. What is Dijkstra's algorithm?

**Answer:**
Dijkstra finds the **shortest path** from a source to all other vertices in a **weighted graph with non-negative edges**.

```python
import heapq
from typing import Dict, List, Tuple

def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Dict[str, int]:
    """
    graph: {node: [(neighbor, weight), ...]}
    Returns: {node: shortest_distance_from_start}
    Time: O((V + E) log V) with min-heap
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]  # (distance, node)

    while heap:
        dist, node = heapq.heappop(heap)

        if dist > distances[node]:
            continue  # Stale entry

        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return distances

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('D', 3), ('C', 1)],
    'C': [('B', 1), ('D', 5)],
    'D': []
}
print(dijkstra(graph, 'A'))
# {'A': 0, 'B': 3, 'C': 2, 'D': 6}
```

---

### Q27. What is the difference between greedy algorithms and DP?

| Feature | Greedy | Dynamic Programming |
|---------|--------|---------------------|
| Approach | Local optimal choice | All subproblems |
| Correctness | Not always optimal | Always optimal |
| Speed | Usually faster | Slower |
| Examples | Huffman, Dijkstra, Activity Selection | Knapsack, LCS, Edit Distance |

```python
# Greedy: Activity Selection (always pick earliest ending activity)
def activity_selection(activities):
    activities.sort(key=lambda x: x[1])  # Sort by end time
    selected = [activities[0]]
    for start, end in activities[1:]:
        if start >= selected[-1][1]:
            selected.append((start, end))
    return selected

# DP: 0/1 Knapsack (greedy doesn't work here)
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]  # Don't take item i
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])

    return dp[n][capacity]

print(knapsack([2, 3, 4, 5], [3, 4, 5, 6], 8))  # 10
```

---

### Q28. What is topological sort?

**Answer:**
Topological sort orders vertices of a **Directed Acyclic Graph (DAG)** such that for every edge u→v, u comes before v. Used for task scheduling, build systems, dependency resolution.

```python
from collections import deque

def topological_sort_kahn(graph, in_degree):
    """Kahn's algorithm — BFS-based"""
    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(graph):
        return []  # Cycle detected
    return result

# Example: course prerequisites
# 0 → 1 → 3
# 0 → 2 → 3
graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
in_degree = {0: 0, 1: 1, 2: 1, 3: 2}
print(topological_sort_kahn(graph, in_degree))  # [0, 1, 2, 3] or [0, 2, 1, 3]
```

---

### Q29. What is the union-find (disjoint set) data structure?

**Answer:**
Union-Find tracks which elements belong to the same **connected component**. Used for Kruskal's MST, cycle detection, network connectivity.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """Path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union by rank"""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already connected (cycle!)
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

# Detect cycle in undirected graph
def has_cycle(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return True  # Edge connects already-connected nodes
    return False

print(has_cycle(4, [(0,1), (1,2), (2,3), (3,1)]))  # True
```

---

### Q30. What is space-time tradeoff?

**Answer:**
Space-time tradeoff means using **more memory to reduce computation time** (or vice versa).

```python
# Example 1: Two Sum
# Time O(n²), Space O(1) — brute force
def two_sum_slow(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

# Time O(n), Space O(n) — hash map tradeoff
def two_sum_fast(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i

# Example 2: Fibonacci
# Time O(2ⁿ), Space O(n) — naive recursion
# Time O(n), Space O(n) — memoization (trade space for time)
# Time O(n), Space O(1) — iterative (optimal both)

# Example 3: Precomputed lookup tables
import math
# Precompute log values once
log_table = {i: math.log(i) for i in range(1, 10001)}
# Now O(1) lookup instead of O(1) computation (but saves repeated computation)
```

---

### Q31. Merge K sorted arrays.

```python
import heapq
from typing import List

def merge_k_sorted(arrays: List[List[int]]) -> List[int]:
    """
    Min-heap approach: O(N log k) time, O(k) space
    N = total elements, k = number of arrays
    """
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

print(merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

### Q32. Find the longest common subsequence (LCS).

```python
def lcs(s1: str, s2: str) -> int:
    """
    DP approach: O(m*n) time and space
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

print(lcs("ABCBDAB", "BDCAB"))  # 4 ("BCAB" or "BDAB")
```

---

### Q33. Find all permutations of a string/array.

```python
from typing import List

def permutations(nums: List[int]) -> List[List[int]]:
    """Backtracking: O(n * n!) time"""
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()

    backtrack([], nums)
    return result

print(permutations([1, 2, 3]))
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]

# Using itertools
from itertools import permutations as iperms
print(list(iperms([1, 2, 3])))
```

---

### [← Back to Index](./00_INDEX.md) | [Next: OOP →](./03_OOP.md)
