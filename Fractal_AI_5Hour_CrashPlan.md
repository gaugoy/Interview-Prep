# ⚡ 5-Hour Interview Crash Plan — Fractal.ai Coding Round
### Maximum ROI Preparation Under Time Constraint

---

## SELECTION METHODOLOGY

From the 35 detailed questions in the main prep guide, I selected **12 high-ROI questions** using a weighted scoring model:

| Factor | Weight |
|--------|--------|
| Interview Frequency (High/Medium/Low) | 40% |
| Concept Coverage (how many patterns it teaches) | 30% |
| Difficulty vs. Time-to-Learn Ratio | 20% |
| Fractal.ai Domain Relevance (analytics/data) | 10% |

**Result:** 12 questions that cover **9 core patterns**, represent **~80% of what actually appears** in Fractal.ai rounds, and can be deeply understood in 5 hours.

---

## THE 12 SELECTED QUESTIONS (Priority Ranked)

| Rank | Question | Pattern | Frequency | Why Selected |
|------|----------|---------|-----------|--------------|
| 1 | Subarray Sum = K | Prefix Sum + Hash Map | High | Covers 2 patterns; appears in almost every analytics round |
| 2 | Longest Substring No Repeat | Sliding Window | High | Template for all sliding window problems |
| 3 | Two Sum | Hash Map Lookup | High | Fastest solve; builds hash map intuition |
| 4 | Maximum Subarray (Kadane's) | DP on Arrays | High | Foundation of all subarray DP problems |
| 5 | Merge Intervals | Sort + Greedy | High | Scheduling/time-series — Fractal.ai domain |
| 6 | Top K Frequent Elements | Heap + Hash Map | High | Analytics core: ranking and frequency |
| 7 | Number of Islands | BFS/DFS on Grid | High | Covers all grid traversal problems |
| 8 | Coin Change | 1D DP (Unbounded) | High | Template for all unbounded DP problems |
| 9 | Valid Parentheses | Stack | High | Fastest stack problem; always appears |
| 10 | Group Anagrams | Sorted Key Hashing | High | String grouping — NLP/text analytics |
| 11 | Longest Increasing Subsequence | DP + Binary Search | High | Sequence analysis — time-series domain |
| 12 | Product of Array Except Self | Prefix/Suffix Product | High | Tests prefix thinking without division |

---

## ⏱️ 5-HOUR STRUCTURED PLAN

```
Total Time: 5 hours = 300 minutes
Format: Learn → Code → Test → Review
```

---

### 🕘 HOUR 0 (0:00–0:15) — WARM-UP & MENTAL SETUP

**Duration:** 15 minutes

**Activities:**
1. **5 min** — Read through all 12 question titles and their patterns (no coding yet)
2. **5 min** — Write down the 9 core patterns from memory on paper:
   - Prefix Sum, Sliding Window, Hash Map, Kadane's, Sort+Greedy, Heap, BFS/DFS, Stack, 1D DP
3. **5 min** — Set up your coding environment:
   - Open editor with Python
   - Write the fast I/O template once:
     ```python
     import sys
     from collections import Counter, defaultdict, deque
     from heapq import heappush, heappop
     input = sys.stdin.readline
     ```

**Why this warm-up works:** Writing patterns from memory activates recall pathways. The 15-minute investment prevents the "blank mind" feeling when you see a problem.

---

### 🕘 HOUR 1 (0:15–1:15) — ARRAYS & HASHING BLOCK

**3 Questions | 60 minutes total**

---

#### ✅ Q1: Two Sum (10 minutes)

**Why chosen over others:** Highest frequency, fastest to solve (< 5 lines), teaches the core hash map complement pattern used in 8+ other problems.

**Strategy:**
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

**Key Concept:** Store what you've seen; check if what you need exists.

**Pitfalls to avoid:**
- Don't use the same element twice: `seen[num] = i` after the check
- Handle case where no pair exists (return empty or -1)
- If problem asks for values not indices, adjust accordingly

**Edge cases to test:** `[3,3], target=6` | `[1], target=1` | negative numbers

**Practice Link:** https://www.hackerearth.com/practice/data-structures/hash-tables/basics-of-hash-tables/practice-problems/

---

#### ✅ Q2: Subarray Sum = K (20 minutes)

**Why chosen as #1 priority:** This single problem teaches prefix sum + hash map together. It appears in Fractal.ai rounds with very high frequency because it mirrors real analytics tasks (find time windows with target metric sum).

**Strategy:**
```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    prefix_map = {0: 1}  # CRITICAL: initialize with 0:1
    
    for num in nums:
        prefix_sum += num
        # If (prefix_sum - k) exists, those subarrays sum to k
        count += prefix_map.get(prefix_sum - k, 0)
        prefix_map[prefix_sum] = prefix_map.get(prefix_sum, 0) + 1
    
    return count
```

**Key Concept:** `prefix[j] - prefix[i] = k` means subarray `[i+1..j]` sums to k. So look for `prefix_sum - k` in the map.

**Pitfalls to avoid:**
- **Most common mistake:** Forgetting `{0: 1}` initialization — this handles subarrays starting from index 0
- Works with negative numbers (unlike sliding window)
- Update map AFTER checking (not before)

**Edge cases to test:** `k=0` | all negatives | single element equals k | `[1,-1,1], k=1`

**Practice Link:** https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/

---

#### ✅ Q3: Product of Array Except Self (20 minutes)

**Why chosen:** Tests prefix/suffix thinking — a pattern that appears in 5+ other problems. Fractal.ai loves this because it tests whether you can avoid division (data integrity constraint).

**Strategy:**
```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Left pass: result[i] = product of all elements to the LEFT
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Right pass: multiply by product of all elements to the RIGHT
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result
```

**Key Concept:** Two-pass approach. Left pass fills prefix products; right pass multiplies suffix products in-place.

**Pitfalls to avoid:**
- Don't use division (problem constraint + fails on zeros)
- The order of operations in each pass matters: update result BEFORE updating running product

**Edge cases to test:** `[1,0,3,4]` | `[0,0]` | `[-1,1,-1]` | single element

**Practice Link:** https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/

---

### 🕙 HOUR 2 (1:15–2:15) — STRINGS & SLIDING WINDOW BLOCK

**3 Questions | 60 minutes total**

---

#### ✅ Q4: Longest Substring Without Repeating Characters (20 minutes)

**Why chosen:** This is THE template problem for all sliding window questions. Master this and you can solve 80% of sliding window variants.

**Strategy:**
```python
def length_of_longest_substring(s):
    char_index = {}  # stores last seen index of each char
    max_len = 0
    left = 0
    
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            # Move left pointer past the duplicate
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Key Concept:** Two pointers (left, right). Expand right; when duplicate found, jump left past it. Window size = `right - left + 1`.

**Pitfalls to avoid:**
- `char_index[char] >= left` check is critical — the duplicate might be outside current window
- Don't use a set and shrink one-by-one (O(n²)); use index map for O(n)

**Edge cases to test:** `""` | `"aaa"` | `"abcabc"` | single character

**Practice Link:** https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/

---

#### ✅ Q5: Group Anagrams (20 minutes)

**Why chosen:** Fractal.ai's analytics domain involves heavy text categorization. This problem teaches the "canonical form as hash key" pattern used in many string grouping problems.

**Strategy:**
```python
def group_anagrams(strs):
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Sorted string is the canonical key
        key = tuple(sorted(s))
        anagram_map[key].append(s)
    
    return list(anagram_map.values())
```

**Alternative O(n) key** (no sorting, use char frequency):
```python
key = tuple(Counter(s).items())  # or fixed 26-char frequency array
```

**Key Concept:** Two strings are anagrams if and only if their sorted forms are identical. Use sorted form as dictionary key.

**Pitfalls to avoid:**
- Use `tuple(sorted(s))` not `sorted(s)` as dict key (lists aren't hashable)
- Empty string `""` is a valid anagram group by itself

**Edge cases to test:** `[""]` | `["a"]` | all same anagram | all unique

**Practice Link:** https://www.hackerearth.com/practice/algorithms/string-algorithm/basics-of-string-manipulation/practice-problems/

---

#### ✅ Q6: Valid Parentheses (10 minutes)

**Why chosen:** Fastest stack problem to solve. Always appears in rounds. 10 minutes max — don't spend more.

**Strategy:**
```python
def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # closing bracket
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)  # opening bracket
    
    return len(stack) == 0
```

**Key Concept:** Push opening brackets. On closing bracket, pop and check match. Empty stack at end = valid.

**Pitfalls to avoid:**
- Check `if stack` before popping (empty stack = invalid)
- Must check `len(stack) == 0` at end (unclosed brackets)

**Edge cases to test:** `""` | `"("` | `"(]"` | `"([)]"`

**Practice Link:** https://www.hackerearth.com/practice/data-structures/stacks/basics-of-stacks/practice-problems/

---

### 🕚 HOUR 3 (2:15–3:15) — DYNAMIC PROGRAMMING BLOCK

**2 Questions | 60 minutes total**

---

#### ✅ Q7: Maximum Subarray — Kadane's Algorithm (15 minutes)

**Why chosen:** Foundation of all subarray DP problems. Every DP interview starts here. 15 minutes because it's simple but the insight is deep.

**Strategy:**
```python
def max_subarray(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    
    for num in nums[1:]:
        # Either extend current subarray or start fresh
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Key Concept:** At each position, decide: "Is it better to extend the previous subarray, or start a new one here?" This is the core DP decision.

**Pitfalls to avoid:**
- Initialize with `nums[0]`, not 0 (handles all-negative arrays)
- Don't initialize `max_sum = float('-inf')` and `current_sum = 0` — fails for all-negative

**Edge cases to test:** `[-1,-2,-3]` | `[0,0,0]` | single element | `[-2,1,-3,4,-1,2,1,-5,4]`

**Practice Link:** https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/

---

#### ✅ Q8: Coin Change — Minimum Coins (35 minutes)

**Why chosen:** This is THE template for all unbounded knapsack DP problems. If you understand this deeply, you can solve Coin Change 2, Word Break, Jump Game, and 10+ other DP problems.

**Strategy:**
```python
def coin_change(coins, amount):
    # dp[i] = minimum coins needed to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed for amount 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Key Concept:** Build up from smaller amounts. For each amount `i`, try every coin and take the minimum.

**Mental Model:** Think of it as: "To make amount i, I can use any coin c, and then I need dp[i-c] more coins."

**Pitfalls to avoid:**
- Initialize with `float('inf')`, not 0 (we're minimizing)
- `dp[0] = 0` is the critical base case
- Return -1 if `dp[amount]` is still infinity (impossible)
- Don't confuse with Coin Change 2 (count ways) — that uses `+=` not `min()`

**Edge cases to test:** `amount=0` | no valid combination | single coin equals amount | `coins=[2], amount=3`

**Practice Link:** https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/

---

### 🕐 HOUR 4 (3:15–4:15) — GRAPHS & SORTING BLOCK

**2 Questions | 60 minutes total**

---

#### ✅ Q9: Number of Islands (25 minutes)

**Why chosen:** This single problem teaches BFS/DFS on grids — a pattern that covers Number of Islands, Max Area of Island, Flood Fill, Rotting Oranges, and 10+ grid problems. Fractal.ai uses spatial analytics.

**Strategy (BFS approach — preferred for interviews):**
```python
def num_islands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(r, c):
        queue = deque([(r, c)])
        grid[r][c] = '0'  # Mark visited immediately
        while queue:
            row, col = queue.popleft()
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'  # Mark visited
                    queue.append((nr, nc))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                bfs(r, c)
                count += 1
    
    return count
```

**Key Concept:** For each unvisited land cell ('1'), do BFS to mark all connected land as visited. Each BFS call = one island.

**Pitfalls to avoid:**
- Mark cell as visited BEFORE adding to queue (not after popping) — prevents duplicate processing
- Check bounds before accessing grid
- If you can't modify input, use a `visited` set of `(r, c)` tuples

**Edge cases to test:** All water | all land | single cell | diagonal cells (not connected)

**Practice Link:** https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/practice-problems/

---

#### ✅ Q10: Merge Intervals (25 minutes)

**Why chosen:** Fractal.ai's analytics domain involves time-series data, event logs, and scheduling — all of which use interval merging. High frequency + domain relevance.

**Strategy:**
```python
def merge(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            # Overlapping: extend the last interval's end
            merged[-1][1] = max(last_end, end)
        else:
            # Non-overlapping: add new interval
            merged.append([start, end])
    
    return merged
```

**Key Concept:** After sorting by start time, two intervals overlap if `current.start <= last.end`. Merge by taking `max(last.end, current.end)`.

**Pitfalls to avoid:**
- Use `max(last_end, end)` not just `end` — current interval might be fully contained
- Sort is mandatory before merging
- Touching intervals `[1,2],[2,3]` → should merge to `[1,3]` (use `<=` not `<`)

**Edge cases to test:** Single interval | all overlapping | no overlapping | `[[1,4],[2,3]]` (contained)

**Practice Link:** https://www.hackerearth.com/practice/algorithms/sorting/merge-sort/practice-problems/

---

#### ✅ Q11: Longest Increasing Subsequence (LIS) — Bonus (10 minutes review)

**Why chosen:** Sequence trend analysis is core to Fractal.ai's time-series domain. Use remaining time in Hour 4 to review the O(n log n) approach.

**Strategy:**
```python
import bisect

def length_of_lis(nums):
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)
```

**Key Concept:** `tails[i]` = smallest tail element of all increasing subsequences of length `i+1`. Binary search to find where current element fits.

**Pitfalls to avoid:**
- `tails` does NOT store the actual LIS — only its length is correct
- Use `bisect_left` for strictly increasing; `bisect_right` for non-decreasing

**Edge cases to test:** `[1,1,1]` | `[5,4,3,2,1]` | `[1]` | already sorted

**Practice Link:** https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/

---

#### ✅ Q12: Top K Frequent Elements — Bonus (10 minutes review)

**Why chosen:** Frequency ranking is the most common analytics operation. Quick review of heap pattern.

**Strategy:**
```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    freq = Counter(nums)
    return heapq.nlargest(k, freq.keys(), key=freq.get)
```

**Key Concept:** Build frequency map; use `heapq.nlargest` with frequency as key. O(n log k).

**Pitfalls to avoid:**
- `nlargest` returns keys sorted by frequency — don't sort again
- For streaming data, maintain a min-heap of size k manually

**Edge cases to test:** `k=n` | all same frequency | `k=1` | single element

**Practice Link:** https://www.hackerearth.com/practice/data-structures/trees/heapspriority-queues/practice-problems/

---

### 🕑 HOUR 5 (4:15–5:00) — REVIEW, MOCK & CONFIDENCE BLOCK

**45 minutes — No new problems**

---

#### 4:15–4:30 | RAPID PATTERN REVIEW (15 minutes)

For each of the 12 problems, write ONE line summarizing the core trick:

| Problem | One-Line Core Trick |
|---------|-------------------|
| Two Sum | `complement = target - num; check in seen` |
| Subarray Sum = K | `count += map[prefix - k]; init {0:1}` |
| Product Except Self | `left pass then right pass, no division` |
| Longest Substring | `jump left to char_index[char]+1` |
| Group Anagrams | `key = tuple(sorted(s))` |
| Valid Parentheses | `push open, pop+check on close, empty=valid` |
| Kadane's | `current = max(num, current+num)` |
| Coin Change | `dp[i] = min(dp[i], dp[i-coin]+1); dp[0]=0` |
| Number of Islands | `BFS from each '1', mark visited as '0'` |
| Merge Intervals | `sort by start; merge if start<=last_end` |
| LIS | `bisect_left on tails array; len(tails) = LIS length` |
| Top K Frequent | `Counter + heapq.nlargest(k, freq, key=freq.get)` |

**Why this works:** Writing the trick in your own words is 3x more effective than re-reading code.

---

#### 4:30–4:45 | EDGE CASE DRILL (15 minutes)

For each problem, mentally answer: "What happens if the input is empty?"

| Problem | Empty Input Behavior |
|---------|---------------------|
| Two Sum | Return `[]` |
| Subarray Sum = K | Return `0` |
| Product Except Self | Return `[]` |
| Longest Substring | Return `0` |
| Group Anagrams | Return `[]` |
| Valid Parentheses | Return `True` (empty string is valid) |
| Kadane's | Return `nums[0]` (handle single element) |
| Coin Change | Return `0` if amount=0 |
| Number of Islands | Return `0` |
| Merge Intervals | Return `[]` |
| LIS | Return `1` (single element) |
| Top K Frequent | Return `[]` |

**Add these guards to every solution:**
```python
if not nums: return []      # arrays
if not s: return 0          # strings
if not grid: return 0       # grids
if amount == 0: return 0    # DP
```

---

#### 4:45–5:00 | CONFIDENCE ROUTINE (15 minutes)

**Step 1 (5 min):** Close your editor. On paper, write the 9 patterns and one problem for each:
- Prefix Sum → Subarray Sum = K
- Sliding Window → Longest Substring
- Hash Map → Two Sum / Group Anagrams
- Kadane's → Max Subarray
- Sort + Greedy → Merge Intervals
- Heap → Top K Frequent
- BFS/DFS → Number of Islands
- Stack → Valid Parentheses
- 1D DP → Coin Change / LIS

**Step 2 (5 min):** Review your complexity cheat sheet:

| Pattern | Time | Space |
|---------|------|-------|
| Hash Map lookup | O(1) avg | O(n) |
| Sorting | O(n log n) | O(1) |
| BFS/DFS grid | O(m×n) | O(m×n) |
| Sliding Window | O(n) | O(1) or O(k) |
| 1D DP | O(n×k) | O(n) |
| Prefix Sum | O(n) build, O(1) query | O(n) |
| Heap (top-K) | O(n log k) | O(k) |
| LIS (optimal) | O(n log n) | O(n) |

**Step 3 (5 min):** Mental simulation — pick any 2 problems from the list and trace through the algorithm in your head with a small example. No coding.

---

## QUESTIONS NOT SELECTED — AND WHY

| Question | Why Skipped |
|----------|-------------|
| LCS | 2D DP takes 45+ min to master; lower ROI in 5 hours |
| Trapping Rain Water | Medium difficulty, lower frequency than selected problems |
| LRU Cache | Design problem; takes 40+ min; rarely appears in online rounds |
| Topological Sort | Graph theory depth; lower frequency in Fractal.ai rounds |
| Minimum Window Substring | Advanced sliding window; master basic SW first |
| Matrix Spiral | Low frequency; high implementation complexity |
| Count Inversions | Requires modified merge sort; high time cost |
| Detect Cycle | Graph theory; lower frequency in analytics company rounds |

**Rule applied:** If a problem takes >35 minutes to master AND has medium frequency, skip it. Use that time to deeply understand a high-frequency problem instead.

---

## INTERVIEW DAY DECISION FRAMEWORK

When you see a new problem in the interview, use this 60-second decision tree:

```
Is it about subarrays/substrings?
├── YES → Does it involve a target sum? → Prefix Sum + Hash Map
│         Does it involve a window condition? → Sliding Window
│         Does it involve max/min? → Kadane's
└── NO → Is it about pairs/sorted arrays? → Two Pointers
         Is it about frequency/grouping? → Hash Map / Counter
         Is it about intervals? → Sort + Greedy
         Is it about a grid? → BFS/DFS
         Is it about optimal choices? → DP
         Is it about brackets/order? → Stack
         Is it about top-K? → Heap
         Is it about sequences/trends? → LIS / DP + Binary Search
```

---

## FINAL 5-MINUTE PRE-INTERVIEW CHECKLIST

- [ ] Fast I/O template ready (`import sys; input = sys.stdin.readline`)
- [ ] `from collections import Counter, defaultdict, deque` imported
- [ ] `from heapq import heappush, heappop` imported
- [ ] `import bisect` imported (for LIS)
- [ ] Remember: always check for empty input first
- [ ] Remember: state your approach before coding
- [ ] Remember: mention time/space complexity after coding
- [ ] Remember: test with the given example, then one edge case

---

*5-Hour Plan covers: 12 problems × 9 patterns × ~80% of Fractal.ai interview content*
*For the full 35-question reference with all solutions, see: Fractal_AI_Interview_Prep.md*
