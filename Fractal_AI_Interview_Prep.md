# Fractal.ai Coding Interview Preparation Guide
### HackerEarth Online Coding Round — Complete Reference Document

---

## TABLE OF CONTENTS

1. [Overview of Fractal.ai Coding Round](#1-overview-of-fractalai-coding-round)
2. [Complete Question List (35 Questions)](#2-complete-question-list)
3. [HackerEarth-Specific Patterns](#3-hackerearth-specific-patterns)
4. [Preparation Plan](#4-preparation-plan)
5. [Top 50 Must-Solve Questions](#5-top-50-must-solve-questions)
6. [Final Recommendations](#6-final-recommendations)

---

## 1. OVERVIEW OF FRACTAL.AI CODING ROUND

### Round Structure

| Parameter | Details |
|-----------|---------|
| **Platform** | HackerEarth (primary), HackerRank (secondary) |
| **Number of Problems** | 2–3 coding problems |
| **Duration** | 60–90 minutes |
| **Difficulty Level** | Easy to Medium (rarely Hard) |
| **Negative Marking** | None |
| **Language Support** | Python, Java, C++, C, JavaScript |

### Skills Evaluated

| Skill | Weight |
|-------|--------|
| Data Structures & Algorithms (DSA) | High |
| Problem-solving & Pattern Recognition | High |
| Edge-case Handling | Medium-High |
| Time/Space Complexity Optimization | Medium-High |
| Code Readability & Structure | Medium |
| Mathematical Reasoning | Medium |

### Typical Problem Distribution

- **Problem 1:** Easy — Arrays/Strings/Hashing (warm-up)
- **Problem 2:** Medium — DP/Two Pointers/Sliding Window
- **Problem 3 (if present):** Medium — Graphs/Recursion/Greedy

### Key Observations from Past Rounds

- Fractal.ai focuses heavily on **data manipulation** problems (reflecting their analytics domain)
- Expect **large input constraints** (N up to 10^5 or 10^6) — brute force will TLE
- **String parsing** and **frequency counting** appear very frequently
- Problems often have **real-world data context** (sales data, user logs, sequences)
- Clean I/O handling is critical on HackerEarth

---

## 2. COMPLETE QUESTION LIST

---

### Q1. Two Sum

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Hashing |
| **Pattern** | Hash Map Lookup |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Tests hash map usage and complement-based thinking; foundational for analytics data lookups |
| **Common Edge Cases** | Duplicate elements, negative numbers, single element array, no valid pair |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/hash-tables/basics-of-hash-tables/practice-problems/ |

**Core Idea:** For each element `x`, check if `target - x` exists in a hash map.

---

### Q2. Maximum Subarray Sum (Kadane's Algorithm)

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Dynamic Programming |
| **Pattern** | Kadane's Algorithm / DP on arrays |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) |
| **Why Fractal.ai Asks** | Classic DP warm-up; tests understanding of local vs global optima — relevant in time-series analysis |
| **Common Edge Cases** | All negative numbers, single element, array of zeros |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** `current_max = max(arr[i], current_max + arr[i])`, track global max.

---

### Q3. Longest Substring Without Repeating Characters

| Attribute | Details |
|-----------|---------|
| **Category** | Strings, Hashing |
| **Pattern** | Sliding Window + Hash Set |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(min(n, charset)) |
| **Why Fractal.ai Asks** | Tests sliding window mastery; string processing is core to NLP/analytics pipelines |
| **Common Edge Cases** | Empty string, all same characters, single character, Unicode characters |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/ |

**Core Idea:** Expand right pointer; when duplicate found, shrink left pointer past the duplicate.

---

### Q4. Find All Duplicates in an Array

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Hashing |
| **Pattern** | Index as Hash / Frequency Count |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) extra (in-place marking) |
| **Why Fractal.ai Asks** | Data deduplication is a core analytics task; tests in-place array manipulation |
| **Common Edge Cases** | No duplicates, all duplicates, single element |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/ |

**Core Idea:** For each `arr[i]`, negate `arr[abs(arr[i])-1]`; if already negative, it's a duplicate.

---

### Q5. Merge Intervals

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Sorting |
| **Pattern** | Sort + Greedy Merge |
| **Time Complexity** | O(n log n) |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Interval merging is used in scheduling, time-series data, and event log analysis |
| **Common Edge Cases** | Single interval, all overlapping, no overlapping, touching intervals |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/sorting/merge-sort/practice-problems/ |

**Core Idea:** Sort by start time; merge if `current.start <= last_merged.end`.

---

### Q6. Valid Parentheses

| Attribute | Details |
|-----------|---------|
| **Category** | Strings, Stack |
| **Pattern** | Stack-based Matching |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Tests stack usage; relevant for parsing structured data (JSON, XML, logs) |
| **Common Edge Cases** | Empty string, only opening brackets, only closing brackets, nested mixed brackets |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/stacks/basics-of-stacks/practice-problems/ |

**Core Idea:** Push opening brackets; on closing bracket, check if top of stack matches.

---

### Q7. Product of Array Except Self

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays |
| **Pattern** | Prefix Product + Suffix Product |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) extra (output array not counted) |
| **Why Fractal.ai Asks** | Tests prefix/suffix thinking without division; common in feature engineering contexts |
| **Common Edge Cases** | Array with zeros (one zero, two zeros), negative numbers, single element |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/ |

**Core Idea:** Build left-product array, then multiply with right-product in a single right-to-left pass.

---

### Q8. Subarray Sum Equals K

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Hashing |
| **Pattern** | Prefix Sum + Hash Map |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Prefix sum is a fundamental analytics pattern; counting subarrays with target sum is a classic |
| **Common Edge Cases** | k=0, negative numbers, single element equals k, all zeros |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** `count += prefix_map[prefix_sum - k]`; store prefix sums in hash map.

---

### Q9. Longest Common Subsequence (LCS)

| Attribute | Details |
|-----------|---------|
| **Category** | Dynamic Programming, Strings |
| **Pattern** | 2D DP Table |
| **Time Complexity** | O(m×n) |
| **Space Complexity** | O(m×n) or O(min(m,n)) optimized |
| **Why Fractal.ai Asks** | Classic DP; used in diff algorithms, DNA sequence analysis, NLP similarity |
| **Common Edge Cases** | Empty strings, identical strings, no common characters, single character strings |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** `dp[i][j] = dp[i-1][j-1]+1` if chars match, else `max(dp[i-1][j], dp[i][j-1])`.

---

### Q10. Coin Change (Minimum Coins)

| Attribute | Details |
|-----------|---------|
| **Category** | Dynamic Programming |
| **Pattern** | Unbounded Knapsack / Bottom-up DP |
| **Time Complexity** | O(amount × n) |
| **Space Complexity** | O(amount) |
| **Why Fractal.ai Asks** | Tests DP optimization thinking; analogous to resource allocation problems in analytics |
| **Common Edge Cases** | Amount = 0, no valid combination, single coin equals amount, very large amount |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** `dp[i] = min(dp[i], dp[i - coin] + 1)` for each coin.

---

### Q11. Number of Islands (BFS/DFS on Grid)

| Attribute | Details |
|-----------|---------|
| **Category** | Graphs, BFS/DFS, Matrix |
| **Pattern** | Connected Components via BFS/DFS |
| **Time Complexity** | O(m×n) |
| **Space Complexity** | O(m×n) |
| **Why Fractal.ai Asks** | Grid traversal is common in spatial analytics; tests graph thinking on 2D data |
| **Common Edge Cases** | All water, all land, single cell, diagonal islands (not connected) |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/practice-problems/ |

**Core Idea:** For each unvisited '1', do BFS/DFS marking all connected '1's as visited; count starts.

---

### Q12. Rotate Array by K Positions

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays |
| **Pattern** | Reversal Algorithm |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) |
| **Why Fractal.ai Asks** | Tests in-place manipulation; common in data pipeline transformations |
| **Common Edge Cases** | k > n, k = 0, k = n, single element, negative k |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/ |

**Core Idea:** Reverse entire array, then reverse first k, then reverse remaining n-k.

---

### Q13. Longest Palindromic Substring

| Attribute | Details |
|-----------|---------|
| **Category** | Strings, Dynamic Programming |
| **Pattern** | Expand Around Center |
| **Time Complexity** | O(n²) |
| **Space Complexity** | O(1) |
| **Why Fractal.ai Asks** | String pattern recognition; tests ability to handle both odd/even length palindromes |
| **Common Edge Cases** | Single character, all same characters, no palindrome longer than 1, entire string is palindrome |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/ |

**Core Idea:** For each center (n centers for odd, n-1 for even), expand while characters match.

---

### Q14. Top K Frequent Elements

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Hashing, Heap |
| **Pattern** | Frequency Map + Min-Heap or Bucket Sort |
| **Time Complexity** | O(n log k) with heap; O(n) with bucket sort |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Frequency analysis is core to analytics; top-K is a fundamental data science operation |
| **Common Edge Cases** | k = n, all same frequency, k = 1, negative numbers |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/trees/heapspriority-queues/practice-problems/ |

**Core Idea:** Build frequency map; use min-heap of size k or bucket sort by frequency.

---

### Q15. Trapping Rain Water

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays |
| **Pattern** | Two Pointers or Prefix/Suffix Max |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) with two pointers |
| **Why Fractal.ai Asks** | Tests multi-dimensional thinking; classic optimization problem showing algorithmic maturity |
| **Common Edge Cases** | Monotonically increasing/decreasing, flat array, two elements, all same height |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/ |

**Core Idea:** Two pointers from both ends; water at position = min(left_max, right_max) - height[i].

---

### Q16. Binary Search on Answer (Minimum/Maximum Feasibility)

| Attribute | Details |
|-----------|---------|
| **Category** | Binary Search |
| **Pattern** | Binary Search on Answer Space |
| **Time Complexity** | O(n log(max_val)) |
| **Space Complexity** | O(1) |
| **Why Fractal.ai Asks** | Tests ability to convert optimization problems to decision problems; common in resource allocation |
| **Common Edge Cases** | Single element, all same values, answer at boundary |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/searching/binary-search/practice-problems/ |

**Core Idea:** Binary search on the answer; write a `feasible(mid)` function to check validity.

---

### Q17. Group Anagrams

| Attribute | Details |
|-----------|---------|
| **Category** | Strings, Hashing |
| **Pattern** | Sorted String as Hash Key |
| **Time Complexity** | O(n × k log k) where k = max string length |
| **Space Complexity** | O(n × k) |
| **Why Fractal.ai Asks** | String grouping/categorization is common in text analytics and NLP preprocessing |
| **Common Edge Cases** | Empty strings, single character strings, all unique, all same anagram group |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/ |

**Core Idea:** Use sorted version of each string as dictionary key; group strings with same key.

---

### Q18. Climbing Stairs / Fibonacci DP

| Attribute | Details |
|-----------|---------|
| **Category** | Dynamic Programming, Recursion |
| **Pattern** | Bottom-up DP / Memoization |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) optimized |
| **Why Fractal.ai Asks** | Simplest DP problem; tests understanding of overlapping subproblems and optimal substructure |
| **Common Edge Cases** | n=1, n=2, very large n (overflow), n=0 |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** `dp[i] = dp[i-1] + dp[i-2]`; only need last two values.

---

### Q19. Find the Missing Number

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Math |
| **Pattern** | XOR or Gauss Sum Formula |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) |
| **Why Fractal.ai Asks** | Data integrity checks; tests mathematical reasoning and bit manipulation |
| **Common Edge Cases** | Missing first element, missing last element, n=1, array with 0 |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/ |

**Core Idea:** `missing = n*(n+1)/2 - sum(arr)` or XOR all indices and elements.

---

### Q20. Sliding Window Maximum

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Deque |
| **Pattern** | Monotonic Deque (Sliding Window) |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(k) |
| **Why Fractal.ai Asks** | Moving window analytics (rolling max, rolling statistics) is fundamental in time-series analysis |
| **Common Edge Cases** | k=1, k=n, all same elements, decreasing array |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/ |

**Core Idea:** Maintain a deque of indices in decreasing order; front is always the max for current window.

---

### Q21. Longest Increasing Subsequence (LIS)

| Attribute | Details |
|-----------|---------|
| **Category** | Dynamic Programming, Binary Search |
| **Pattern** | DP O(n²) or Patience Sorting O(n log n) |
| **Time Complexity** | O(n log n) optimal |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Sequence analysis is core to time-series and trend detection in analytics |
| **Common Edge Cases** | All same elements, strictly decreasing, single element, already sorted |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** Maintain a `tails` array; binary search for position to replace or extend.

---

### Q22. Word Break Problem

| Attribute | Details |
|-----------|---------|
| **Category** | Dynamic Programming, Strings |
| **Pattern** | DP with Dictionary Lookup |
| **Time Complexity** | O(n²) |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | NLP tokenization; tests DP on strings — relevant for text analytics |
| **Common Edge Cases** | Empty string, word not in dictionary, overlapping words, single character words |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** `dp[i] = True` if any `dp[j]` is True and `s[j:i]` is in word set.

---

### Q23. Detect Cycle in Directed Graph

| Attribute | Details |
|-----------|---------|
| **Category** | Graphs, DFS |
| **Pattern** | DFS with Coloring (White/Gray/Black) |
| **Time Complexity** | O(V + E) |
| **Space Complexity** | O(V) |
| **Why Fractal.ai Asks** | Dependency resolution, pipeline validation; tests graph traversal depth |
| **Common Edge Cases** | Self-loop, disconnected graph, single node, no edges |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/graphs/depth-first-search/practice-problems/ |

**Core Idea:** DFS with 3 states: unvisited(0), in-stack(1), done(2); cycle if we reach state 1.

---

### Q24. Kth Largest Element in Array

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Heap, Sorting |
| **Pattern** | Min-Heap of size K or QuickSelect |
| **Time Complexity** | O(n log k) heap; O(n) average QuickSelect |
| **Space Complexity** | O(k) |
| **Why Fractal.ai Asks** | Percentile/ranking computation is fundamental in analytics and reporting |
| **Common Edge Cases** | k=1, k=n, duplicate elements, negative numbers |
| **Difficulty** | Medium |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/trees/heapspriority-queues/practice-problems/ |

**Core Idea:** Maintain min-heap of size k; if new element > heap top, replace top.

---

### Q25. Matrix Spiral Order Traversal

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Matrix |
| **Pattern** | Boundary Shrinking |
| **Time Complexity** | O(m×n) |
| **Space Complexity** | O(1) extra |
| **Why Fractal.ai Asks** | 2D data traversal; tests ability to handle complex iteration patterns in matrix data |
| **Common Edge Cases** | Single row, single column, 1×1 matrix, non-square matrix |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/arrays/2-d/practice-problems/ |

**Core Idea:** Maintain top/bottom/left/right boundaries; traverse and shrink after each direction.

---

### Q26. Count Inversions in Array

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Sorting |
| **Pattern** | Modified Merge Sort |
| **Time Complexity** | O(n log n) |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Inversion count measures disorder/correlation; used in ranking algorithms and data quality |
| **Common Edge Cases** | Already sorted (0 inversions), reverse sorted (max inversions), all same elements |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/sorting/merge-sort/practice-problems/ |

**Core Idea:** During merge sort, when right element is placed before left elements, add count of remaining left elements.

---

### Q27. Minimum Path Sum in Grid

| Attribute | Details |
|-----------|---------|
| **Category** | Dynamic Programming, Matrix |
| **Pattern** | 2D DP Grid |
| **Time Complexity** | O(m×n) |
| **Space Complexity** | O(m×n) or O(n) optimized |
| **Why Fractal.ai Asks** | Path optimization in grids; analogous to cost minimization in supply chain analytics |
| **Common Edge Cases** | 1×1 grid, single row, single column, grid with zeros |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/2-dimensional/practice-problems/ |

**Core Idea:** `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`.

---

### Q28. Anagram Check / Character Frequency

| Attribute | Details |
|-----------|---------|
| **Category** | Strings, Hashing |
| **Pattern** | Frequency Array / Hash Map |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) — fixed 26 characters |
| **Why Fractal.ai Asks** | String comparison is fundamental; tests efficient character counting |
| **Common Edge Cases** | Different lengths, empty strings, case sensitivity, special characters |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/ |

**Core Idea:** Count character frequencies in both strings; compare frequency arrays.

---

### Q29. Shortest Path in Unweighted Graph (BFS)

| Attribute | Details |
|-----------|---------|
| **Category** | Graphs, BFS |
| **Pattern** | BFS Level-by-Level Traversal |
| **Time Complexity** | O(V + E) |
| **Space Complexity** | O(V) |
| **Why Fractal.ai Asks** | Network analysis, recommendation systems; tests BFS fundamentals |
| **Common Edge Cases** | Source = destination, disconnected graph, no path exists, single node |
| **Difficulty** | Easy-Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/practice-problems/ |

**Core Idea:** BFS from source; distance array tracks minimum hops to each node.

---

### Q30. Balanced Binary Tree Check

| Attribute | Details |
|-----------|---------|
| **Category** | Trees, Recursion |
| **Pattern** | Post-order DFS with Height Calculation |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(h) — recursion stack |
| **Why Fractal.ai Asks** | Tree balance is fundamental; tests recursive thinking and bottom-up computation |
| **Common Edge Cases** | Empty tree, single node, skewed tree, complete binary tree |
| **Difficulty** | Easy |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/trees/binary-and-nary-trees/practice-problems/ |

**Core Idea:** Return -1 if unbalanced subtree found; otherwise return height. Check `|left_h - right_h| <= 1`.

---

### Q31. Maximum Product Subarray

| Attribute | Details |
|-----------|---------|
| **Category** | Arrays, Dynamic Programming |
| **Pattern** | Track Both Max and Min Products |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(1) |
| **Why Fractal.ai Asks** | Extension of Kadane's; tests handling of negative numbers and zeros in DP |
| **Common Edge Cases** | All negatives (even count), single zero, single element, alternating negatives |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/ |

**Core Idea:** Track `max_prod` and `min_prod`; on negative number, swap them before updating.

---

### Q32. Implement LRU Cache

| Attribute | Details |
|-----------|---------|
| **Category** | Design, Hashing, Linked List |
| **Pattern** | Hash Map + Doubly Linked List |
| **Time Complexity** | O(1) for get and put |
| **Space Complexity** | O(capacity) |
| **Why Fractal.ai Asks** | Caching is critical in data systems; tests system design thinking at code level |
| **Common Edge Cases** | Capacity = 1, get non-existent key, update existing key, eviction order |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/data-structures/linked-list/singly-linked-list/practice-problems/ |

**Core Idea:** HashMap for O(1) lookup; doubly linked list for O(1) insertion/deletion at head/tail.

---

### Q33. String Compression / Run-Length Encoding

| Attribute | Details |
|-----------|---------|
| **Category** | Strings |
| **Pattern** | Two Pointers / Counting |
| **Time Complexity** | O(n) |
| **Space Complexity** | O(n) |
| **Why Fractal.ai Asks** | Data compression is relevant in analytics storage; tests string manipulation skills |
| **Common Edge Cases** | All unique characters, single character, already compressed, numbers in string |
| **Difficulty** | Easy |
| **Frequency** | High |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/ |

**Core Idea:** Count consecutive same characters; append char + count (skip count if 1).

---

### Q34. Topological Sort

| Attribute | Details |
|-----------|---------|
| **Category** | Graphs, DAG |
| **Pattern** | Kahn's Algorithm (BFS) or DFS-based |
| **Time Complexity** | O(V + E) |
| **Space Complexity** | O(V) |
| **Why Fractal.ai Asks** | Task scheduling, dependency resolution in ML pipelines; tests DAG understanding |
| **Common Edge Cases** | Cycle in graph (no valid order), single node, disconnected DAG |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/graphs/topological-sort/practice-problems/ |

**Core Idea:** Kahn's: compute in-degrees; repeatedly remove nodes with in-degree 0.

---

### Q35. Minimum Window Substring

| Attribute | Details |
|-----------|---------|
| **Category** | Strings, Sliding Window |
| **Pattern** | Variable-size Sliding Window + Frequency Map |
| **Time Complexity** | O(n + m) |
| **Space Complexity** | O(m) — pattern character set |
| **Why Fractal.ai Asks** | Advanced sliding window; tests ability to handle complex window conditions |
| **Common Edge Cases** | Pattern longer than string, no valid window, pattern has duplicates, entire string is answer |
| **Difficulty** | Medium |
| **Frequency** | Medium |
| **Practice Links** | https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/ |

**Core Idea:** Expand right until all pattern chars covered; shrink left while still valid; track minimum window.

---

## 3. HACKEREARTH-SPECIFIC PATTERNS

### 3.1 Input/Output Heavy Questions

HackerEarth problems often require careful I/O handling:

```python
# Python fast I/O template for HackerEarth
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    # ... solution
    print(result)

main()
```

**Key Tips:**
- Use `sys.stdin.readline` instead of `input()` for large inputs
- Use `'\n'.join(map(str, results))` instead of multiple `print()` calls
- Avoid `print()` inside loops for large outputs

---

### 3.2 Large Constraint Handling

| Constraint | Required Approach |
|------------|------------------|
| N ≤ 10³ | O(n²) acceptable |
| N ≤ 10⁴ | O(n² log n) borderline |
| N ≤ 10⁵ | O(n log n) required |
| N ≤ 10⁶ | O(n) required |
| N ≤ 10⁹ | O(log n) or O(1) required |

---

### 3.3 Common HackerEarth Problem Templates

#### Template 1: Prefix Sum Array
```python
# Build prefix sum
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i+1] = prefix[i] + arr[i]

# Range sum query [l, r] (0-indexed)
range_sum = prefix[r+1] - prefix[l]
```

#### Template 2: Sliding Window (Fixed Size)
```python
# Window of size k
window_sum = sum(arr[:k])
max_sum = window_sum
for i in range(k, n):
    window_sum += arr[i] - arr[i-k]
    max_sum = max(max_sum, window_sum)
```

#### Template 3: BFS Grid Traversal
```python
from collections import deque

def bfs(grid, start_r, start_c):
    rows, cols = len(grid), len(grid[0])
    visited = [[False]*cols for _ in range(rows)]
    queue = deque([(start_r, start_c, 0)])  # (row, col, distance)
    visited[start_r][start_c] = True
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    
    while queue:
        r, c, dist = queue.popleft()
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, dist+1))
```

#### Template 4: Two Pointers
```python
left, right = 0, n-1
while left < right:
    current = arr[left] + arr[right]
    if current == target:
        # found
        left += 1; right -= 1
    elif current < target:
        left += 1
    else:
        right -= 1
```

#### Template 5: Binary Search
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

### 3.4 String Parsing Patterns

```python
# Frequency count
from collections import Counter
freq = Counter(s)

# Check if all characters are alphanumeric
s.isalnum()

# Split and process
words = s.strip().split()

# Reverse words
' '.join(reversed(s.split()))
```

---

### 3.5 DP on Arrays — Common Patterns

| Problem Type | DP State | Transition |
|-------------|----------|------------|
| Max subarray | `dp[i]` = max ending at i | `max(arr[i], dp[i-1]+arr[i])` |
| LIS | `dp[i]` = LIS ending at i | `max(dp[j]+1)` for j < i, arr[j] < arr[i] |
| Knapsack | `dp[i][w]` = max value | `max(dp[i-1][w], dp[i-1][w-wt]+val)` |
| Coin change | `dp[amount]` = min coins | `min(dp[a], dp[a-coin]+1)` |
| Edit distance | `dp[i][j]` = min ops | Based on match/insert/delete/replace |

---

## 4. PREPARATION PLAN

---

### 4.1 TWO-DAY CRASH PLAN

#### Day 1 (6–8 hours): Core Patterns

| Time Block | Topic | Problems to Solve |
|------------|-------|------------------|
| 9:00–10:30 | Arrays + Hashing | Two Sum, Find Duplicates, Missing Number |
| 10:30–12:00 | Sliding Window | Longest Substring No Repeat, Max Subarray Sum |
| 12:00–13:00 | **Break** | Review notes |
| 13:00–14:30 | Prefix Sum + Two Pointers | Subarray Sum = K, Product Except Self, Trapping Rain Water |
| 14:30–16:00 | Strings | Group Anagrams, Anagram Check, String Compression |
| 16:00–17:30 | Basic DP | Climbing Stairs, Coin Change, LCS |
| 17:30–18:30 | Stack/Queue | Valid Parentheses, Sliding Window Maximum |

**Day 1 Goal:** Master O(n) array/string patterns and basic DP.

---

#### Day 2 (6–8 hours): Advanced Patterns + Mock

| Time Block | Topic | Problems to Solve |
|------------|-------|------------------|
| 9:00–10:30 | Graphs (BFS/DFS) | Number of Islands, Shortest Path, Cycle Detection |
| 10:30–12:00 | Advanced DP | LIS, Word Break, Maximum Product Subarray |
| 12:00–13:00 | **Break** | Review Day 1 mistakes |
| 13:00–14:00 | Sorting + Greedy | Merge Intervals, Top K Frequent, Kth Largest |
| 14:00–15:00 | Binary Search | Binary Search on Answer, Kth Smallest |
| 15:00–17:00 | **MOCK TEST** | Solve 2–3 problems under 90-minute timer |
| 17:00–18:00 | Review + I/O Practice | HackerEarth I/O templates, edge cases |

**Day 2 Goal:** Cover graphs, advanced DP, and simulate actual test conditions.

---

### 4.2 SEVEN-DAY PLAN

| Day | Focus Area | Key Topics | Target Problems |
|-----|-----------|------------|-----------------|
| **Day 1** | Arrays Fundamentals | Prefix sum, two pointers, sliding window | Q1, Q4, Q7, Q8, Q12, Q15 |
| **Day 2** | Strings & Hashing | Frequency maps, anagrams, string parsing | Q3, Q17, Q28, Q33, Q35 |
| **Day 3** | Dynamic Programming I | 1D DP, Kadane's, Fibonacci variants | Q2, Q10, Q18, Q31 |
| **Day 4** | Dynamic Programming II | 2D DP, LCS, LIS, Word Break | Q9, Q21, Q22, Q27 |
| **Day 5** | Graphs & Trees | BFS, DFS, cycle detection, topological sort | Q11, Q23, Q29, Q30, Q34 |
| **Day 6** | Sorting, Heap, Binary Search | Merge intervals, top-K, binary search on answer | Q5, Q14, Q16, Q24, Q26 |
| **Day 7** | Mock Tests + Review | Full mock (90 min), review all patterns | 2 full mock tests |

---

### 4.3 FOURTEEN-DAY COMPLETE PLAN

| Day | Focus | Topics |
|-----|-------|--------|
| 1 | Arrays I | Basic traversal, prefix sums, range queries |
| 2 | Arrays II | Two pointers, sliding window, in-place operations |
| 3 | Hashing | Hash maps, frequency counting, grouping |
| 4 | Strings I | Basic manipulation, palindromes, anagrams |
| 5 | Strings II | Sliding window on strings, KMP, Z-algorithm basics |
| 6 | Sorting & Searching | Merge sort, quick sort, binary search variants |
| 7 | **Mid-Week Mock** | 90-minute timed test + review |
| 8 | Stack & Queue | Monotonic stack, deque, expression evaluation |
| 9 | DP I | 1D DP, memoization, tabulation |
| 10 | DP II | 2D DP, knapsack variants, string DP |
| 11 | Trees | Binary tree traversals, BST, height/balance |
| 12 | Graphs I | BFS, DFS, connected components |
| 13 | Graphs II | Shortest path, topological sort, cycle detection |
| 14 | **Final Mock** | 2 full mock tests + comprehensive review |

---

### 4.4 Most Important Patterns to Master for Fractal.ai

**Tier 1 — Must Know (High Frequency)**

1. **Prefix Sum** — Range queries, subarray sums
2. **Sliding Window** — Fixed and variable size windows
3. **Hash Map / Frequency Count** — Grouping, lookup, counting
4. **Two Pointers** — Sorted arrays, palindromes, pair sums
5. **Kadane's Algorithm** — Maximum subarray variants
6. **BFS on Grid** — Connected components, shortest path

**Tier 2 — Should Know (Medium Frequency)**

7. **Binary Search on Answer** — Optimization problems
8. **1D DP** — Fibonacci-style, coin change, LIS
9. **Merge Sort / Count Inversions** — Divide and conquer
10. **Stack-based Problems** — Monotonic stack, valid brackets
11. **Heap / Priority Queue** — Top-K, streaming median

**Tier 3 — Good to Know (Lower Frequency)**

12. **2D DP** — Grid paths, LCS, edit distance
13. **Topological Sort** — Dependency problems
14. **Trie** — Prefix matching, autocomplete
15. **Union-Find** — Connected components, cycle detection

---

## 5. TOP 50 MUST-SOLVE QUESTIONS

### Difficulty Spread: 20 Easy | 25 Medium | 5 Hard

#### EASY (20 Questions)

| # | Problem | Category | Platform |
|---|---------|----------|----------|
| 1 | Two Sum | Arrays/Hash | HackerEarth |
| 2 | Missing Number | Arrays/Math | HackerEarth |
| 3 | Valid Parentheses | Stack | HackerEarth |
| 4 | Climbing Stairs | DP | HackerEarth |
| 5 | Reverse String | Strings | HackerEarth |
| 6 | Palindrome Check | Strings | HackerEarth |
| 7 | Anagram Check | Strings/Hash | HackerEarth |
| 8 | Find Max/Min in Array | Arrays | HackerEarth |
| 9 | Rotate Array | Arrays | HackerEarth |
| 10 | String Compression | Strings | HackerEarth |
| 11 | Count Vowels/Consonants | Strings | HackerEarth |
| 12 | Fibonacci (Iterative) | Math/DP | HackerEarth |
| 13 | Binary Search | Searching | HackerEarth |
| 14 | Balanced Parentheses | Stack | HackerEarth |
| 15 | Remove Duplicates (Sorted) | Arrays | HackerEarth |
| 16 | Merge Two Sorted Arrays | Arrays/Sorting | HackerEarth |
| 17 | First Non-Repeating Character | Strings/Hash | HackerEarth |
| 18 | Count Occurrences | Arrays/Hash | HackerEarth |
| 19 | Power of Two Check | Math/Bit | HackerEarth |
| 20 | Balanced Binary Tree | Trees | HackerEarth |

#### MEDIUM (25 Questions)

| # | Problem | Category | Platform |
|---|---------|----------|----------|
| 21 | Maximum Subarray (Kadane's) | Arrays/DP | HackerEarth |
| 22 | Longest Substring No Repeat | Strings/SW | HackerEarth |
| 23 | Product Except Self | Arrays | HackerEarth |
| 24 | Subarray Sum = K | Arrays/Hash | HackerEarth |
| 25 | Merge Intervals | Arrays/Sort | HackerEarth |
| 26 | Top K Frequent Elements | Hash/Heap | HackerEarth |
| 27 | Group Anagrams | Strings/Hash | HackerEarth |
| 28 | Longest Common Subsequence | DP | HackerEarth |
| 29 | Coin Change | DP | HackerEarth |
| 30 | Longest Increasing Subsequence | DP | HackerEarth |
| 31 | Number of Islands | Graphs/BFS | HackerEarth |
| 32 | Kth Largest Element | Heap | HackerEarth |
| 33 | Trapping Rain Water | Arrays | HackerEarth |
| 34 | Sliding Window Maximum | Arrays/Deque | HackerEarth |
| 35 | Word Break | DP/Strings | HackerEarth |
| 36 | Minimum Path Sum Grid | DP/Matrix | HackerEarth |
| 37 | Longest Palindromic Substring | Strings/DP | HackerEarth |
| 38 | Count Inversions | Sort/Divide | HackerEarth |
| 39 | Topological Sort | Graphs | HackerEarth |
| 40 | Detect Cycle (Directed) | Graphs/DFS | HackerEarth |
| 41 | Maximum Product Subarray | Arrays/DP | HackerEarth |
| 42 | Binary Search on Answer | Binary Search | HackerEarth |
| 43 | Minimum Window Substring | Strings/SW | HackerEarth |
| 44 | Matrix Spiral Traversal | Arrays/Matrix | HackerEarth |
| 45 | LRU Cache Implementation | Design | HackerEarth |

#### HARD (5 Questions)

| # | Problem | Category | Platform |
|---|---------|----------|----------|
| 46 | Median of Two Sorted Arrays | Binary Search | HackerEarth |
| 47 | Edit Distance | DP/Strings | HackerEarth |
| 48 | Largest Rectangle in Histogram | Stack | HackerEarth |
| 49 | Word Ladder (BFS) | Graphs/BFS | HackerEarth |
| 50 | Regular Expression Matching | DP/Strings | HackerEarth |

---

### Practice Resources

| Platform | Link | Best For |
|----------|------|----------|
| HackerEarth Practice | https://www.hackerearth.com/practice/ | All categories |
| HackerEarth Algorithms | https://www.hackerearth.com/practice/algorithms/ | Algorithm patterns |
| HackerEarth Data Structures | https://www.hackerearth.com/practice/data-structures/ | DS problems |
| HackerEarth DP | https://www.hackerearth.com/practice/algorithms/dynamic-programming/ | DP problems |
| HackerEarth Graphs | https://www.hackerearth.com/practice/algorithms/graphs/ | Graph problems |
| HackerEarth Strings | https://www.hackerearth.com/practice/algorithms/string-algorithm/ | String problems |
| HackerEarth Sorting | https://www.hackerearth.com/practice/algorithms/sorting/ | Sorting problems |
| HackerEarth Searching | https://www.hackerearth.com/practice/algorithms/searching/ | Search problems |

---

## 6. FINAL RECOMMENDATIONS

### 6.1 Fractal.ai-Specific Tips

1. **Focus on Data Manipulation Problems**
   - Fractal.ai is an analytics company; expect problems involving frequency analysis, data aggregation, and sequence processing
   - Practice problems that involve counting, grouping, and summarizing data

2. **Master Python for Analytics Context**
   - Python is preferred; use `collections.Counter`, `collections.defaultdict`, `heapq`
   - Know list comprehensions and generator expressions for clean code

3. **Always Handle Edge Cases**
   - Empty inputs, single elements, all same values, negative numbers
   - Fractal.ai tests edge cases heavily — mention them in your approach

4. **Optimize from the Start**
   - Don't submit O(n²) solutions for n=10⁵; think about complexity before coding
   - If brute force is O(n²), think: can prefix sum, hash map, or sorting reduce it to O(n log n)?

5. **Clean Code Matters**
   - Use meaningful variable names
   - Add brief comments for complex logic
   - Structure your solution with helper functions

---

### 6.2 Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Integer overflow (Java/C++) | Use `long` or check constraints |
| Off-by-one in binary search | Use `left <= right` and `mid = left + (right-left)//2` |
| Modifying array while iterating | Use a copy or two-pointer approach |
| Not handling empty input | Always add `if not arr: return ...` |
| Slow I/O in Python | Use `sys.stdin.readline` |
| Forgetting to reset visited array | Initialize fresh for each test case |

---

### 6.3 Day-of-Test Strategy

1. **Read all problems first** (5 minutes) — identify which is easiest
2. **Solve easiest problem first** — secure partial/full marks
3. **For each problem:**
   - Identify the pattern (2 min)
   - Write approach in comments (2 min)
   - Code the solution (15–20 min)
   - Test with examples + edge cases (5 min)
4. **If stuck:** Move to next problem; return with fresh eyes
5. **Last 10 minutes:** Review all submissions, check edge cases

---

### 6.4 Key Python Libraries for HackerEarth

```python
from collections import Counter, defaultdict, deque
from heapq import heappush, heappop, nlargest, nsmallest
from itertools import combinations, permutations
from functools import lru_cache
import sys
import bisect  # for binary search on sorted lists

# Fast input
input = sys.stdin.readline

# Fast output
import sys
print = sys.stdout.write  # use print(str(x) + '\n')
```

---

### 6.5 Pattern Recognition Quick Reference

| If the problem asks for... | Use this pattern |
|---------------------------|-----------------|
| Subarray with max/min sum | Kadane's Algorithm |
| Subarray with target sum | Prefix Sum + Hash Map |
| Longest substring with condition | Sliding Window |
| Pair with target sum | Two Pointers (sorted) or Hash Map |
| Top K elements | Min-Heap of size K |
| Frequency of elements | Counter / Hash Map |
| Overlapping intervals | Sort + Greedy Merge |
| Shortest path (unweighted) | BFS |
| Connected components | BFS/DFS or Union-Find |
| Optimal substructure | Dynamic Programming |
| Sorted + search | Binary Search |
| Dependency ordering | Topological Sort |
| Balanced brackets | Stack |
| Sliding max/min | Monotonic Deque |

---

*Document prepared for Fractal.ai HackerEarth Coding Round Preparation*
*Last Updated: March 2026*
*Total Questions Covered: 35 detailed + 50 must-solve list*
*Preparation Plans: 2-day, 7-day, 14-day*
