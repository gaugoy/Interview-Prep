# 🐼 Pandas Interview Cheat Sheet
### For Senior Software Engineers (6 YOE) — Technical Interview Preparation

---

## 📋 Table of Contents

### Theory Section
1. [DataFrame vs Series](#1-dataframe-vs-series)
2. [Indexing Methods: loc, iloc, at, iat](#2-indexing-methods-loc-iloc-at-iat)
3. [Memory Optimization](#3-memory-optimization)
4. [Handling Missing Data](#4-handling-missing-data)
5. [Merging and Joining Strategies](#5-merging-and-joining-strategies)
6. [GroupBy Mechanics](#6-groupby-mechanics)
7. [Time Series Handling](#7-time-series-handling)
8. [Performance Best Practices](#8-performance-best-practices)

### Coding Section
9. [Data Cleaning and Preprocessing](#9-data-cleaning-and-preprocessing)
10. [Filtering and Conditional Selection](#10-filtering-and-conditional-selection)
11. [Aggregation and GroupBy Operations](#11-aggregation-and-groupby-operations)
12. [Merging, Joining, and Concatenating](#12-merging-joining-and-concatenating)
13. [Pivot Tables and Reshaping](#13-pivot-tables-and-reshaping)
14. [Handling Null Values](#14-handling-null-values)
15. [Apply, Map, and Applymap](#15-apply-map-and-applymap)
16. [Time Series Manipulation](#16-time-series-manipulation)
17. [Performance Optimization](#17-performance-optimization)

---

# THEORY SECTION

---

## 1. DataFrame vs Series

### Q: What is the fundamental difference between a Series and a DataFrame? When would you use one over the other?

**Answer:**

| Feature | Series | DataFrame |
|---------|--------|-----------|
| Dimensions | 1D (single column) | 2D (rows × columns) |
| Index | Single index | Row index + column labels |
| Data types | Homogeneous (single dtype) | Heterogeneous (mixed dtypes per column) |
| Analogy | NumPy array with labels | Dict of Series sharing the same index |
| Memory | Lower overhead | Higher overhead |

**Key Internals:**
- A `DataFrame` is essentially a dict of `Series` objects sharing the same index.
- Each column in a DataFrame is a Series.
- Both are backed by NumPy arrays (or Arrow arrays in newer pandas).

```python
import pandas as pd
import numpy as np

# Series: single column of data
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'], name='values')

# DataFrame: multiple columns
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z']
})

# A DataFrame column IS a Series
print(type(df['A']))  # <class 'pandas.core.series.Series'>
print(df['A'].values is df['A'].to_numpy())  # False (copy), but same data
```

**⚠️ Gotcha:** `df['col']` returns a Series (view or copy depending on operation). `df[['col']]` returns a single-column DataFrame. This distinction matters for chaining operations.

**Senior-level insight:** When a DataFrame has a single column, prefer keeping it as a DataFrame if you'll be doing join/merge operations — Series don't have column labels for joining.

---

## 2. Indexing Methods: loc, iloc, at, iat

### Q: Explain the difference between `loc`, `iloc`, `at`, and `iat`. What are the performance implications?

**Answer:**

| Method | Type | Returns | Use Case |
|--------|------|---------|----------|
| `loc` | Label-based | Scalar/Series/DataFrame | Flexible label selection, boolean masks |
| `iloc` | Integer position-based | Scalar/Series/DataFrame | Positional slicing, NumPy-style |
| `at` | Label-based | Scalar only | Fast single-value access by label |
| `iat` | Integer position-based | Scalar only | Fast single-value access by position |

**Performance:** `at`/`iat` are ~10x faster than `loc`/`iloc` for single scalar access because they skip overhead of returning a Series/DataFrame.

```python
df = pd.DataFrame({'A': [10, 20, 30], 'B': [40, 50, 60]}, index=['x', 'y', 'z'])

# loc: label-based (inclusive on both ends for slices!)
df.loc['x':'y', 'A']        # rows x to y (INCLUSIVE), column A
df.loc[df['A'] > 10, 'B']   # boolean mask

# iloc: position-based (exclusive end, like Python slicing)
df.iloc[0:2, 0]             # rows 0,1 (NOT 2), column 0
df.iloc[-1, :]              # last row, all columns

# at/iat: scalar access only
df.at['x', 'A']             # 10 — label-based
df.iat[0, 0]                # 10 — position-based
```

**⚠️ Critical Gotcha — `loc` slicing is INCLUSIVE:**
```python
# Python list slicing: [0:2] → indices 0, 1 (NOT 2)
# iloc[0:2]            → rows 0, 1 (NOT 2) — consistent with Python
# loc['a':'c']         → rows 'a', 'b', 'c' (INCLUSIVE of 'c') — DIFFERENT!
```

**⚠️ SettingWithCopyWarning:**
```python
# BAD: chained indexing — may not modify original
df[df['A'] > 10]['B'] = 99  # SettingWithCopyWarning!

# GOOD: use loc with boolean mask
df.loc[df['A'] > 10, 'B'] = 99  # Correct
```

**Senior-level insight:** The `SettingWithCopyWarning` is one of the most common pandas bugs in production. Always use `.loc` for conditional assignment. In pandas 2.0+, Copy-on-Write (CoW) changes this behavior — understand the migration path.

---

## 3. Memory Optimization

### Q: How do you optimize memory usage in pandas? What are the key strategies for large datasets?

**Answer:**

**1. Downcast Numeric Types**
```
int64 (8 bytes) → int8/int16/int32 (1/2/4 bytes)
float64 (8 bytes) → float32 (4 bytes)
```

**2. Use Categorical for Low-Cardinality Strings**
```
object dtype: stores Python string objects (~50 bytes each)
category dtype: stores integer codes + lookup table (~1 byte per value)
```

**3. Sparse Arrays for Mostly-Null Data**

**4. Read in Chunks for Large Files**

**Memory comparison:**

| dtype | Bytes per element | Notes |
|-------|------------------|-------|
| bool | 1 | |
| int8 | 1 | -128 to 127 |
| int16 | 2 | -32768 to 32767 |
| int32 | 4 | ~±2 billion |
| int64 | 8 | Default integer |
| float32 | 4 | ~7 decimal digits precision |
| float64 | 8 | Default float |
| object | ~50+ | Python string heap allocation |
| category | ~1-4 | Depends on cardinality |

```python
import pandas as pd
import numpy as np

# Check memory usage
df.memory_usage(deep=True)  # deep=True includes object dtype actual size
df.info(memory_usage='deep')

# Optimize function
def optimize_dtypes(df):
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # <50% unique → categorical
            df[col] = df[col].astype('category')
    return df
```

**⚠️ Gotcha:** `float32` loses precision. Avoid for financial calculations. Use `float64` or `Decimal` for money.

**Senior-level insight:** `category` dtype is a game-changer for string columns with repeated values (e.g., country, status, department). A column with 1M rows but only 50 unique values can go from ~50MB to ~1MB.

---

## 4. Handling Missing Data

### Q: Explain pandas' missing data representations. What is the difference between `NaN`, `None`, `NaT`, and `pd.NA`? How do you handle them?

**Answer:**

| Value | Type | Used For | Notes |
|-------|------|----------|-------|
| `np.nan` | float | Numeric columns | IEEE 754 float, propagates in math |
| `None` | Python object | Object dtype | Python's null, slower |
| `pd.NaT` | NaT | Datetime columns | "Not a Time" |
| `pd.NA` | NAType | Nullable integer/boolean | Pandas 1.0+ extension types |

**Key behaviors:**
```python
import numpy as np
import pandas as pd

# NaN arithmetic propagates
np.nan + 5          # nan
np.nan == np.nan    # False! (IEEE 754)
pd.isna(np.nan)     # True

# None in numeric context becomes NaN
s = pd.Series([1, None, 3])
s.dtype              # float64 (None → NaN, forces float)

# Nullable integer (pd.NA doesn't force float)
s = pd.Series([1, pd.NA, 3], dtype='Int64')  # capital I = nullable
s.dtype              # Int64
s.sum()              # 4 (skips NA)
```

**Missing data detection:**
```python
df.isna()           # element-wise boolean mask
df.notna()          # inverse
df.isna().sum()     # count per column
df.isna().any()     # any missing per column
df.isna().all()     # all missing per column
```

**Handling strategies:**

| Strategy | Method | When to Use |
|----------|--------|-------------|
| Drop rows | `df.dropna()` | Small % missing, MCAR |
| Drop columns | `df.dropna(axis=1)` | Column mostly empty |
| Fill constant | `df.fillna(0)` | Known default value |
| Forward fill | `df.ffill()` | Time series, carry last known |
| Backward fill | `df.bfill()` | Time series |
| Fill with stat | `df.fillna(df.mean())` | Numeric, MAR assumption |
| Interpolate | `df.interpolate()` | Numeric, smooth data |

**⚠️ Gotcha:** `df.fillna(df.mean())` only works on numeric columns. For mixed DataFrames, use `df.fillna(df.select_dtypes(include='number').mean())`.

**Senior-level insight:** Understand the difference between MCAR (Missing Completely At Random), MAR (Missing At Random), and MNAR (Missing Not At Random). The imputation strategy should match the missingness mechanism. Blindly filling with mean can introduce bias.

---

## 5. Merging and Joining Strategies

### Q: Explain the different join types in pandas. What is the difference between `merge`, `join`, and `concat`? When does each perform poorly?

**Answer:**

**Join Types:**

| Type | Behavior | SQL Equivalent |
|------|----------|----------------|
| `inner` | Only matching rows | INNER JOIN |
| `left` | All left rows + matching right | LEFT JOIN |
| `right` | All right rows + matching left | RIGHT JOIN |
| `outer` | All rows from both | FULL OUTER JOIN |
| `cross` | Cartesian product | CROSS JOIN |

**`merge` vs `join` vs `concat`:**

| Function | Primary Use | Key Difference |
|----------|-------------|----------------|
| `pd.merge()` | Join on columns or index | Most flexible, SQL-like |
| `df.join()` | Join on index | Shorthand for index-based merge |
| `pd.concat()` | Stack DataFrames | No key matching, just stacking |

```python
# merge: column-based join
pd.merge(df1, df2, on='key', how='inner')
pd.merge(df1, df2, left_on='id', right_on='user_id', how='left')

# join: index-based (faster when index is already set)
df1.join(df2, how='inner')  # joins on index by default
df1.set_index('id').join(df2.set_index('id'))

# concat: stacking (no key matching)
pd.concat([df1, df2], axis=0)  # stack rows (union of columns)
pd.concat([df1, df2], axis=1)  # stack columns (union of rows)
```

**Performance considerations:**
- Merging on **indexed columns** is O(n) vs O(n log n) for unindexed
- `merge` with `sort=False` is faster when order doesn't matter
- Large cross joins (cartesian) can cause OOM — always validate join keys first

**⚠️ Gotcha — Duplicate keys cause row explosion:**
```python
# If df1 has 3 rows with key=1 and df2 has 3 rows with key=1
# Inner join produces 3×3 = 9 rows!
# Always check: df['key'].duplicated().sum() before merging
```

**⚠️ Gotcha — `concat` resets nothing by default:**
```python
df_combined = pd.concat([df1, df2])
# Index may have duplicates! Use:
df_combined = pd.concat([df1, df2], ignore_index=True)
```

**Senior-level insight:** For production pipelines, always validate join cardinality. A `1:1` join that silently becomes `1:many` due to dirty data is a common source of bugs. Use `validate` parameter: `pd.merge(df1, df2, on='key', validate='1:1')`.

---

## 6. GroupBy Mechanics

### Q: How does GroupBy work internally? Explain the split-apply-combine paradigm and the difference between `transform`, `agg`, and `apply`.

**Answer:**

**Split-Apply-Combine:**
1. **Split**: Partition DataFrame into groups based on key(s)
2. **Apply**: Apply a function to each group independently
3. **Combine**: Concatenate results back into a single DataFrame/Series

**Internal mechanics:**
- GroupBy creates a lazy object — no computation until you call an aggregation
- Groups are stored as a dict of `{group_key: [row_indices]}`
- Memory: O(n) for index storage, actual data not duplicated

**`agg` vs `transform` vs `apply`:**

| Method | Output Shape | Returns | Use Case |
|--------|-------------|---------|----------|
| `agg` | Reduced (one row per group) | Scalar per group | Summary statistics |
| `transform` | Same shape as input | Value for each original row | Normalize, fill with group stat |
| `apply` | Flexible | Anything | Complex custom logic |
| `filter` | Subset of original | Groups meeting condition | Remove groups |

```python
df = pd.DataFrame({
    'dept': ['Eng', 'Eng', 'HR', 'HR'],
    'salary': [100, 120, 80, 90]
})

# agg: one row per group
df.groupby('dept')['salary'].agg(['mean', 'max'])
# dept    mean   max
# Eng     110    120
# HR       85     90

# transform: same shape as original (for normalization, filling)
df['salary_zscore'] = df.groupby('dept')['salary'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# apply: most flexible, but slowest
df.groupby('dept').apply(lambda g: g.nlargest(1, 'salary'))
```

**⚠️ Gotcha — `apply` with `group_keys`:**
```python
# In pandas 2.0+, group_keys=False by default in apply
# This changes index behavior — be explicit:
df.groupby('dept', group_keys=False).apply(func)
```

**⚠️ Gotcha — `agg` with named aggregations (pandas 0.25+):**
```python
# Old way (deprecated):
df.groupby('dept').agg({'salary': ['mean', 'max']})

# New way (named aggregation — cleaner column names):
df.groupby('dept').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max')
)
```

**Senior-level insight:** `transform` is underused but powerful. Use it to add group-level statistics back to the original DataFrame without a merge. E.g., `df['pct_of_dept'] = df['salary'] / df.groupby('dept')['salary'].transform('sum')`.

---

## 7. Time Series Handling

### Q: How does pandas handle time series data? Explain DatetimeIndex, resampling, rolling windows, and timezone handling.

**Answer:**

**Core time types:**

| Type | Description |
|------|-------------|
| `Timestamp` | Single point in time (pandas equivalent of datetime) |
| `DatetimeIndex` | Index of Timestamps — enables time-based slicing |
| `Period` | Fixed-frequency time span (e.g., month, quarter) |
| `Timedelta` | Duration between two times |

**DatetimeIndex enables powerful slicing:**
```python
df = pd.DataFrame({'value': range(100)},
                  index=pd.date_range('2023-01-01', periods=100, freq='D'))

df['2023-03']           # All of March 2023
df['2023-01':'2023-03'] # Jan through March (inclusive!)
df.loc['2023-01-15']    # Specific date
```

**Resampling (changing frequency):**
```python
# Downsample: daily → monthly
df.resample('ME').mean()   # Month End
df.resample('W').sum()     # Weekly sum
df.resample('QE').last()   # Quarter End, last value

# Upsample: daily → hourly (creates NaN, needs fill)
df.resample('h').ffill()   # Forward fill
df.resample('h').interpolate()
```

**Rolling windows:**
```python
# Rolling mean (moving average)
df['rolling_7d'] = df['value'].rolling(window=7).mean()
df['rolling_7d_min3'] = df['value'].rolling(window=7, min_periods=3).mean()

# Expanding window (cumulative)
df['cumulative_mean'] = df['value'].expanding().mean()

# Exponentially weighted
df['ewm'] = df['value'].ewm(span=7).mean()
```

**Timezone handling:**
```python
# Localize naive datetime to timezone
df.index = df.index.tz_localize('UTC')

# Convert between timezones
df.index = df.index.tz_convert('US/Eastern')

# Remove timezone info
df.index = df.index.tz_localize(None)
```

**⚠️ Gotcha — Frequency aliases changed in pandas 2.2:**
```
Old: 'M' (month end), 'Q' (quarter end), 'A' (year end)
New: 'ME', 'QE', 'YE' (explicit "End")
Old aliases deprecated — update your code!
```

**Senior-level insight:** When working with DST (Daylight Saving Time), `tz_localize` can raise `AmbiguousTimeError` or `NonExistentTimeError`. Use `ambiguous='NaT'` or `nonexistent='shift_forward'` to handle gracefully.

---

## 8. Performance Best Practices

### Q: What are the key performance principles in pandas? How do you profile and optimize a slow pandas pipeline?

**Answer:**

**Performance hierarchy (fastest to slowest):**
1. **Vectorized NumPy operations** — operates on entire array at C speed
2. **Pandas built-in methods** — optimized, often calls NumPy internally
3. **`apply` with built-in functions** — some optimization
4. **`apply` with Python lambdas** — Python-speed loop
5. **Explicit Python `for` loops** — slowest, avoid at all costs

**Profiling tools:**
```python
import time
%timeit df['col'].apply(lambda x: x * 2)   # Jupyter magic
%timeit df['col'] * 2                        # Compare

# cProfile for full pipeline
import cProfile
cProfile.run('my_function(df)')

# memory_profiler
from memory_profiler import profile
@profile
def process(df): ...
```

**Key optimizations:**

| Technique | Speedup | Notes |
|-----------|---------|-------|
| Vectorization over apply | 10-100x | Use `df['col'] * 2` not `apply(lambda x: x*2)` |
| `query()` for filtering | 2-5x | Uses numexpr, avoids Python overhead |
| `eval()` for expressions | 2-5x | Same as query, for assignments |
| Set index before join | 5-10x | Index lookup is O(1) vs O(n) scan |
| `category` dtype | 2-10x | For string groupby/sort operations |
| Chunked reading | Memory | `pd.read_csv(chunksize=10000)` |
| `engine='pyarrow'` | 2-5x | Faster I/O in pandas 1.4+ |

**⚠️ Gotcha — `apply` is not magic:**
```python
# People think apply is "vectorized" — it's NOT
# apply is a Python-level loop with overhead
# Only use apply when no vectorized alternative exists
```

**Senior-level insight:** The biggest performance wins usually come from:
1. Reducing data size early (filter before transform)
2. Using appropriate dtypes (category, int32 vs int64)
3. Avoiding `apply` in favor of vectorized operations
4. Using `pd.eval()` for complex boolean expressions on large DataFrames

---

# CODING SECTION

---

## 9. Data Cleaning and Preprocessing

### Problem 1: Clean a messy real-world dataset

```python
import pandas as pd
import numpy as np

# Simulate messy data
data = {
    'Name': ['  Alice ', 'BOB', 'charlie', None, 'ALICE'],
    'Age': ['25', '30', 'unknown', '28', '25'],
    'Salary': ['$50,000', '$60,000', '$55,000', None, '$50,000'],
    'Email': ['alice@example.com', 'bob@example.com', 'invalid-email', 
               'dave@example.com', 'alice@example.com'],
    'JoinDate': ['2020-01-15', '2019-06-30', '2021-13-01', '2020-03-22', '2020-01-15']
}
df = pd.DataFrame(data)

# ── Step 1: Standardize string columns ──────────────────────────────────────
df['Name'] = df['Name'].str.strip().str.title()  # Remove whitespace, title case
# Output: ['Alice', 'Bob', 'Charlie', None, 'Alice']

# ── Step 2: Handle numeric columns with non-numeric values ──────────────────
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')  # 'unknown' → NaN
# errors='coerce': invalid → NaN | 'raise': raise error | 'ignore': keep original

# ── Step 3: Clean currency strings ──────────────────────────────────────────
df['Salary'] = (df['Salary']
                .str.replace('$', '', regex=False)
                .str.replace(',', '', regex=False)
                .pipe(pd.to_numeric, errors='coerce'))

# ── Step 4: Validate email format ───────────────────────────────────────────
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
df['Email_Valid'] = df['Email'].str.match(email_pattern)

# ── Step 5: Parse dates with error handling ─────────────────────────────────
df['JoinDate'] = pd.to_datetime(df['JoinDate'], errors='coerce')
# '2021-13-01' (invalid month 13) → NaT

# ── Step 6: Remove duplicates ───────────────────────────────────────────────
# Keep first occurrence, consider all columns
df_clean = df.drop_duplicates()

# Keep first occurrence based on Name only
df_clean = df.drop_duplicates(subset=['Name'], keep='first')

# ── Step 7: Report data quality ─────────────────────────────────────────────
print("Missing values per column:")
print(df.isna().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"\nData types:\n{df.dtypes}")
```

### Problem 2: Detect and handle outliers

```python
def remove_outliers_iqr(df, column):
    """Remove outliers using IQR method (robust to non-normal distributions)."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    mask = df[column].between(lower, upper)
    print(f"Removed {(~mask).sum()} outliers from '{column}'")
    return df[mask]

def cap_outliers_zscore(df, column, threshold=3):
    """Cap outliers using Z-score (assumes normal distribution)."""
    mean = df[column].mean()
    std = df[column].std()
    df[column] = df[column].clip(
        lower=mean - threshold * std,
        upper=mean + threshold * std
    )
    return df

# Usage
df = pd.DataFrame({'salary': [50000, 55000, 60000, 1000000, 52000, 58000]})
df_clean = remove_outliers_iqr(df, 'salary')
# Removed 1 outliers from 'salary'
```

**💡 Best Practice:** Always visualize data before choosing outlier strategy. IQR is more robust for skewed data; Z-score assumes normality.

---

## 10. Filtering and Conditional Selection

### Problem 3: Complex multi-condition filtering

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'dept': np.random.choice(['Eng', 'HR', 'Finance', 'Marketing'], 1000),
    'salary': np.random.randint(40000, 150000, 1000),
    'years_exp': np.random.randint(0, 20, 1000),
    'performance': np.random.choice(['Low', 'Medium', 'High', 'Excellent'], 1000),
    'remote': np.random.choice([True, False], 1000)
})

# ── Method 1: Boolean indexing (most common) ─────────────────────────────────
mask = (
    (df['dept'] == 'Eng') &
    (df['salary'] > 80000) &
    (df['years_exp'] >= 5) &
    (df['performance'].isin(['High', 'Excellent']))
)
result = df[mask]

# ── Method 2: query() — more readable, faster on large DataFrames ────────────
result = df.query(
    "dept == 'Eng' and salary > 80000 and years_exp >= 5 "
    "and performance in ['High', 'Excellent']"
)

# ── Method 3: query() with variable interpolation ───────────────────────────
min_salary = 80000
min_exp = 5
result = df.query("salary > @min_salary and years_exp >= @min_exp")

# ── Method 4: np.where for conditional column creation ──────────────────────
df['salary_band'] = np.where(
    df['salary'] < 60000, 'Low',
    np.where(df['salary'] < 100000, 'Mid', 'High')
)

# ── Method 5: pd.cut for binning ────────────────────────────────────────────
df['exp_bucket'] = pd.cut(
    df['years_exp'],
    bins=[0, 2, 5, 10, 20],
    labels=['Junior', 'Mid', 'Senior', 'Principal'],
    right=True  # (0,2] — right-inclusive
)

# ── Method 6: Filter with string methods ────────────────────────────────────
df_emails = pd.DataFrame({'email': ['alice@gmail.com', 'bob@company.org', 'charlie@gmail.com']})
gmail_users = df_emails[df_emails['email'].str.endswith('@gmail.com')]
contains_alice = df_emails[df_emails['email'].str.contains('alice', case=False, na=False)]
```

**⚠️ Gotcha — `&` vs `and` in pandas:**
```python
# WRONG: 'and' doesn't work element-wise
df[df['A'] > 0 and df['B'] > 0]  # ValueError!

# CORRECT: use & with parentheses (operator precedence!)
df[(df['A'] > 0) & (df['B'] > 0)]  # Correct
```

**⚠️ Gotcha — `isin` with NaN:**
```python
# NaN is NOT in any list — use separate check
df[df['col'].isin(['a', 'b']) | df['col'].isna()]
```

---

## 11. Aggregation and GroupBy Operations

### Problem 4: Multi-level aggregation with named aggregations

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'region': ['North', 'North', 'South', 'South', 'East', 'East'],
    'product': ['A', 'B', 'A', 'B', 'A', 'B'],
    'sales': [100, 200, 150, 250, 120, 180],
    'units': [10, 20, 15, 25, 12, 18],
    'date': pd.date_range('2023-01-01', periods=6, freq='ME')
})

# ── Named aggregation (pandas 0.25+) ─────────────────────────────────────────
result = df.groupby('region').agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    max_sales=('sales', 'max'),
    total_units=('units', 'sum'),
    num_products=('product', 'nunique'),
    # Custom aggregation
    sales_per_unit=('sales', lambda x: x.sum() / df.loc[x.index, 'units'].sum())
)
print(result)
# Output:
#         total_sales  avg_sales  max_sales  total_units  num_products  sales_per_unit
# region
# East            300      150.0        180           30             2        10.0
# North           300      150.0        200           30             2        10.0
# South           400      200.0        250           40             2        10.0

# ── Multi-level groupby ──────────────────────────────────────────────────────
result_multi = df.groupby(['region', 'product']).agg(
    total_sales=('sales', 'sum'),
    avg_units=('units', 'mean')
).reset_index()

# ── transform: add group stats back to original DataFrame ───────────────────
df['region_total'] = df.groupby('region')['sales'].transform('sum')
df['pct_of_region'] = df['sales'] / df['region_total'] * 100

# ── filter: keep only groups meeting a condition ─────────────────────────────
# Keep only regions with total sales > 350
high_sales_regions = df.groupby('region').filter(lambda g: g['sales'].sum() > 350)

# ── Cumulative operations within groups ──────────────────────────────────────
df_sorted = df.sort_values(['region', 'date'])
df_sorted['cumulative_sales'] = df_sorted.groupby('region')['sales'].cumsum()
df_sorted['running_avg'] = df_sorted.groupby('region')['sales'].expanding().mean().values

# ── Rank within groups ───────────────────────────────────────────────────────
df['sales_rank_in_region'] = df.groupby('region')['sales'].rank(
    method='dense',  # 'average', 'min', 'max', 'first', 'dense'
    ascending=False
)
```

### Problem 5: Pivot-style aggregation with multiple functions

```python
# Multiple aggregation functions per column
result = df.groupby('region').agg({
    'sales': ['sum', 'mean', 'std', 'count'],
    'units': ['sum', 'mean']
})

# Flatten multi-level column names
result.columns = ['_'.join(col).strip() for col in result.columns]
# sales_sum, sales_mean, sales_std, sales_count, units_sum, units_mean
```

**💡 Performance tip:** `groupby` with `as_index=False` avoids setting group keys as index, which can be faster when you'll call `reset_index()` anyway.

---

## 12. Merging, Joining, and Concatenating

### Problem 6: Complex merge scenarios with validation

```python
import pandas as pd

employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve'],
    'dept_id': [10, 20, 10, 30, 20]
})

departments = pd.DataFrame({
    'dept_id': [10, 20, 40],  # Note: dept 30 missing, dept 40 has no employees
    'dept_name': ['Engineering', 'HR', 'Finance']
})

salaries = pd.DataFrame({
    'emp_id': [1, 2, 3, 1],  # Note: emp 1 has TWO salary records (duplicate!)
    'salary': [90000, 70000, 85000, 95000]
})

# ── Inner join: only matching rows ──────────────────────────────────────────
inner = pd.merge(employees, departments, on='dept_id', how='inner')
# Dave (dept 30) excluded — no matching department

# ── Left join: all employees, NaN for missing dept ──────────────────────────
left = pd.merge(employees, departments, on='dept_id', how='left')
# Dave gets dept_name = NaN

# ── Validate join cardinality ────────────────────────────────────────────────
try:
    safe_merge = pd.merge(employees, salaries, on='emp_id', 
                          how='left', validate='1:1')
except pd.errors.MergeError as e:
    print(f"Merge validation failed: {e}")
    # "Merge keys are not unique in right dataset"

# ── Indicator column: track row origin ──────────────────────────────────────
merged = pd.merge(employees, departments, on='dept_id', how='outer', indicator=True)
print(merged['_merge'].value_counts())
# both          3  (matched)
# left_only     2  (employees without dept)
# right_only    1  (dept without employees)

# ── Multi-key merge ──────────────────────────────────────────────────────────
df1 = pd.DataFrame({'year': [2022, 2022, 2023], 'month': [1, 2, 1], 'val': [10, 20, 30]})
df2 = pd.DataFrame({'year': [2022, 2023], 'month': [1, 1], 'extra': ['a', 'b']})
result = pd.merge(df1, df2, on=['year', 'month'], how='left')

# ── Merge with different column names ────────────────────────────────────────
result = pd.merge(employees, salaries, 
                  left_on='emp_id', right_on='emp_id',
                  suffixes=('_emp', '_sal'))  # Handle duplicate column names

# ── Concatenation with keys (creates MultiIndex) ─────────────────────────────
df_2022 = pd.DataFrame({'sales': [100, 200]})
df_2023 = pd.DataFrame({'sales': [150, 250]})
combined = pd.concat([df_2022, df_2023], keys=['2022', '2023'])
# MultiIndex: (year, original_index)
combined.loc['2022']  # Access 2022 data
```

**⚠️ Gotcha — Suffix collision:**
```python
# If both DataFrames have 'date' column and you don't specify suffixes:
pd.merge(df1, df2, on='id')  # Creates 'date_x', 'date_y' automatically
# Always specify suffixes explicitly for clarity:
pd.merge(df1, df2, on='id', suffixes=('_left', '_right'))
```

---

## 13. Pivot Tables and Reshaping

### Problem 7: Pivot, melt, stack, and unstack

```python
import pandas as pd
import numpy as np

# Sample sales data
df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=12, freq='ME'),
    'region': ['North', 'South'] * 6,
    'product': ['A', 'A', 'B', 'B'] * 3,
    'sales': np.random.randint(100, 500, 12),
    'units': np.random.randint(10, 50, 12)
})

# ── pivot_table: aggregated pivot ────────────────────────────────────────────
pivot = pd.pivot_table(
    df,
    values='sales',
    index='region',
    columns='product',
    aggfunc='sum',
    fill_value=0,       # Replace NaN with 0
    margins=True,       # Add row/column totals
    margins_name='Total'
)
print(pivot)
# product  A    B  Total
# region
# North   ...  ...  ...
# South   ...  ...  ...
# Total   ...  ...  ...

# ── pivot: no aggregation (requires unique index/column combos) ───────────────
df_unique = df.drop_duplicates(subset=['region', 'product'])
pivot_simple = df_unique.pivot(index='region', columns='product', values='sales')

# ── melt: wide → long format (inverse of pivot) ──────────────────────────────
wide_df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'math': [90, 85],
    'science': [88, 92],
    'english': [75, 80]
})

long_df = pd.melt(
    wide_df,
    id_vars=['name'],           # Columns to keep as-is
    value_vars=['math', 'science', 'english'],  # Columns to unpivot
    var_name='subject',         # Name for the variable column
    value_name='score'          # Name for the value column
)
print(long_df)
# name    subject  score
# Alice   math     90
# Bob     math     85
# Alice   science  88
# ...

# ── stack/unstack: work with MultiIndex ──────────────────────────────────────
multi_df = df.set_index(['region', 'product'])

# stack: columns → rows (wide → long)
stacked = multi_df.stack()  # Creates another level in index

# unstack: rows → columns (long → wide)
unstacked = multi_df.unstack('product')  # product level becomes columns
unstacked = multi_df.unstack(level=-1)   # Same as above (last level)

# ── crosstab: frequency table ────────────────────────────────────────────────
ct = pd.crosstab(
    df['region'], 
    df['product'],
    values=df['sales'],
    aggfunc='sum',
    normalize='index'  # Row percentages
)
```

**⚠️ Gotcha — `pivot` vs `pivot_table`:**
```python
# pivot: raises ValueError if duplicate (index, column) combinations exist
# pivot_table: aggregates duplicates (default aggfunc='mean')
# Always use pivot_table unless you're certain data is unique
```

---

## 14. Handling Null Values

### Problem 8: Advanced null handling strategies

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=10, freq='h'),
    'temperature': [20.0, np.nan, np.nan, 23.0, np.nan, 25.0, np.nan, 27.0, np.nan, 29.0],
    'category': ['A', None, 'B', None, 'A', None, 'B', 'A', None, 'B'],
    'value': [1, 2, np.nan, 4, 5, np.nan, 7, 8, np.nan, 10]
})

# ── Strategy 1: Forward/Backward fill (time series) ──────────────────────────
df['temp_ffill'] = df['temperature'].ffill()
df['temp_bfill'] = df['temperature'].bfill()

# Limit consecutive fills
df['temp_ffill_limit'] = df['temperature'].ffill(limit=1)  # Fill max 1 consecutive NaN

# ── Strategy 2: Interpolation ────────────────────────────────────────────────
df['temp_linear'] = df['temperature'].interpolate(method='linear')
df['temp_time'] = df['temperature'].interpolate(method='time')  # Time-aware
df['temp_spline'] = df['temperature'].interpolate(method='spline', order=2)

# ── Strategy 3: Fill with group statistics ───────────────────────────────────
df['value_group_mean'] = df.groupby('category')['value'].transform(
    lambda x: x.fillna(x.mean())
)

# ── Strategy 4: Conditional filling ─────────────────────────────────────────
# Fill NaN in 'value' with 0 only where category is 'A'
df.loc[(df['value'].isna()) & (df['category'] == 'A'), 'value'] = 0

# ── Strategy 5: dropna with thresholds ───────────────────────────────────────
# Drop rows with ANY null
df.dropna()

# Drop rows with ALL nulls
df.dropna(how='all')

# Keep rows with at least 3 non-null values
df.dropna(thresh=3)

# Drop nulls only considering specific columns
df.dropna(subset=['temperature', 'value'])

# ── Strategy 6: Detect null patterns ────────────────────────────────────────
null_report = pd.DataFrame({
    'null_count': df.isna().sum(),
    'null_pct': df.isna().mean() * 100,
    'dtype': df.dtypes
}).sort_values('null_pct', ascending=False)
print(null_report)

# ── Strategy 7: Nullable integer type ────────────────────────────────────────
# Regular int64 cannot hold NaN (gets converted to float64)
s_float = pd.Series([1, None, 3])  # dtype: float64
print(s_float.dtype)  # float64

# Use Int64 (capital I) for nullable integers
s_int = pd.Series([1, pd.NA, 3], dtype='Int64')
print(s_int.dtype)  # Int64
print(s_int.sum())  # 4 (skips NA, stays integer)
```

**⚠️ Gotcha — `fillna` doesn't modify in place by default:**
```python
df['col'].fillna(0)          # Returns new Series, df unchanged!
df['col'] = df['col'].fillna(0)  # Correct
df['col'].fillna(0, inplace=True)  # Also works (but inplace is being deprecated)
```

---

## 15. Apply, Map, and Applymap

### Problem 9: Choosing the right function application method

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['alice smith', 'bob jones', 'charlie brown'],
    'score': [85, 92, 78],
    'grade': ['B', 'A', 'C']
})

# ── map: element-wise on a SERIES (pandas 2.1+: also replaces applymap) ──────
# Use for: simple element-wise transformations, dict mapping

# Dict mapping (replaces values, NaN for missing keys)
grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0}
df['gpa'] = df['grade'].map(grade_map)

# Function mapping
df['name_upper'] = df['name'].map(str.upper)

# ── apply on Series: element-wise or aggregate ───────────────────────────────
# Element-wise (like map but more flexible)
df['score_normalized'] = df['score'].apply(lambda x: (x - 70) / 30)

# Aggregate (returns scalar)
print(df['score'].apply(lambda x: x ** 2).sum())

# ── apply on DataFrame: row-wise or column-wise ──────────────────────────────
# axis=0 (default): apply function to each COLUMN
col_stats = df[['score']].apply(lambda col: col.describe())

# axis=1: apply function to each ROW
def classify_student(row):
    if row['score'] >= 90:
        return 'Excellent'
    elif row['score'] >= 80:
        return 'Good'
    else:
        return 'Needs Improvement'

df['classification'] = df.apply(classify_student, axis=1)

# ── applymap / map (DataFrame): element-wise on entire DataFrame ──────────────
# pandas < 2.1: df.applymap()
# pandas >= 2.1: df.map() (applymap deprecated)
numeric_df = df[['score', 'gpa']]
formatted = numeric_df.map(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')

# ── PERFORMANCE COMPARISON ───────────────────────────────────────────────────
import time

n = 100000
s = pd.Series(range(n))

# Method 1: apply (Python loop) — SLOWEST
t1 = time.time()
result1 = s.apply(lambda x: x * 2)
print(f"apply: {time.time() - t1:.4f}s")

# Method 2: map (slightly faster than apply for simple ops)
t2 = time.time()
result2 = s.map(lambda x: x * 2)
print(f"map: {time.time() - t2:.4f}s")

# Method 3: vectorized — FASTEST
t3 = time.time()
result3 = s * 2
print(f"vectorized: {time.time() - t3:.4f}s")

# Typical output:
# apply: 0.0450s
# map:   0.0380s
# vectorized: 0.0003s  ← ~150x faster!

# ── When apply IS necessary ──────────────────────────────────────────────────
# 1. Complex multi-column logic
def complex_transform(row):
    base = row['score'] * 1.1
    if row['grade'] == 'A':
        return base * 1.2
    return base

df['adjusted_score'] = df.apply(complex_transform, axis=1)

# 2. Functions that return multiple values
def extract_name_parts(name):
    parts = name.split()
    return pd.Series({'first': parts[0], 'last': parts[-1] if len(parts) > 1 else ''})

name_parts = df['name'].apply(extract_name_parts)
df = pd.concat([df, name_parts], axis=1)
```

**⚠️ Gotcha — `apply` with `result_type`:**
```python
# When apply returns a list/array per row, use result_type='expand'
df.apply(lambda row: [row['score'], row['score'] * 2], axis=1, result_type='expand')
# Returns DataFrame with 2 columns instead of Series of lists
```

---

## 16. Time Series Manipulation

### Problem 10: Real-world time series analysis

```python
import pandas as pd
import numpy as np

# Generate realistic time series data
np.random.seed(42)
dates = pd.date_range('2022-01-01', '2023-12-31', freq='D')
df = pd.DataFrame({
    'date': dates,
    'sales': np.random.normal(1000, 100, len(dates)) + 
             np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 200,  # Seasonality
    'temperature': np.random.normal(15, 10, len(dates))
})
df = df.set_index('date')

# ── Date component extraction ────────────────────────────────────────────────
df['year'] = df.index.year
df['month'] = df.index.month
df['day_of_week'] = df.index.dayofweek  # 0=Monday, 6=Sunday
df['quarter'] = df.index.quarter
df['is_weekend'] = df.index.dayofweek >= 5
df['week_of_year'] = df.index.isocalendar().week

# ── Resampling ───────────────────────────────────────────────────────────────
monthly = df['sales'].resample('ME').agg({
    'total': 'sum',
    'avg': 'mean',
    'max': 'max',
    'min': 'min'
})

# Custom resampling with multiple aggregations
weekly = df.resample('W').agg(
    total_sales=('sales', 'sum'),
    avg_temp=('temperature', 'mean')
)

# ── Rolling statistics ────────────────────────────────────────────────────────
df['ma_7d'] = df['sales'].rolling(window=7).mean()
df['ma_30d'] = df['sales'].rolling(window=30).mean()
df['std_7d'] = df['sales'].rolling(window=7).std()

# Rolling with min_periods (avoid NaN at start)
df['ma_7d_min3'] = df['sales'].rolling(window=7, min_periods=3).mean()

# ── Lag features (common in ML feature engineering) ──────────────────────────
df['sales_lag1'] = df['sales'].shift(1)   # Yesterday's sales
df['sales_lag7'] = df['sales'].shift(7)   # Same day last week
df['sales_diff'] = df['sales'].diff(1)    # Day-over-day change
df['sales_pct_change'] = df['sales'].pct_change(1)  # % change

# ── Date arithmetic ──────────────────────────────────────────────────────────
df['days_since_start'] = (df.index - df.index[0]).days

# Business day offset
from pandas.tseries.offsets import BDay, MonthEnd
next_bday = pd.Timestamp('2023-12-29') + BDay(1)  # Next business day
month_end = pd.Timestamp('2023-11-15') + MonthEnd(1)  # Next month end

# ── Handling irregular time series ───────────────────────────────────────────
# Detect gaps
time_diffs = df.index.to_series().diff()
gaps = time_diffs[time_diffs > pd.Timedelta('1D')]
print(f"Gaps in data: {len(gaps)}")

# Fill gaps by reindexing
full_range = pd.date_range(df.index.min(), df.index.max(), freq='D')
df_complete = df.reindex(full_range)  # NaN for missing dates
df_complete = df_complete.ffill()     # Forward fill gaps

# ── Period-over-period comparison ────────────────────────────────────────────
monthly_sales = df['sales'].resample('ME').sum()
yoy_growth = monthly_sales.pct_change(12) * 100  # Year-over-year %
mom_growth = monthly_sales.pct_change(1) * 100   # Month-over-month %

# ── Timezone-aware operations ────────────────────────────────────────────────
df_utc = df.copy()
df_utc.index = df_utc.index.tz_localize('UTC')
df_ist = df_utc.copy()
df_ist.index = df_ist.index.tz_convert('Asia/Kolkata')

# ── Business hours filtering ─────────────────────────────────────────────────
hourly_df = pd.DataFrame(
    {'value': range(24)},
    index=pd.date_range('2023-01-02', periods=24, freq='h')  # Monday
)
business_hours = hourly_df.between_time('09:00', '17:00')
```

**⚠️ Gotcha — `resample` requires DatetimeIndex:**
```python
# If date is a column (not index), set it first:
df.set_index('date').resample('ME').sum()
# OR use on= parameter:
df.resample('ME', on='date').sum()
```

---

## 17. Performance Optimization

### Problem 11: Vectorization vs loops — real benchmarks

```python
import pandas as pd
import numpy as np
import time

# Setup
np.random.seed(42)
n = 500000
df = pd.DataFrame({
    'a': np.random.randn(n),
    'b': np.random.randn(n),
    'category': np.random.choice(['X', 'Y', 'Z'], n),
    'value': np.random.randint(1, 100, n)
})

def benchmark(func, *args, name='', **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    print(f"{name}: {elapsed:.4f}s")
    return result

# ── Problem: Compute hypotenuse for each row ──────────────────────────────────

# BAD: Python for loop
def hyp_loop(df):
    result = []
    for _, row in df.iterrows():
        result.append((row['a']**2 + row['b']**2)**0.5)
    return result

# BETTER: apply (still Python-level)
def hyp_apply(df):
    return df.apply(lambda row: (row['a']**2 + row['b']**2)**0.5, axis=1)

# BEST: vectorized NumPy
def hyp_vectorized(df):
    return np.sqrt(df['a']**2 + df['b']**2)

# Note: iterrows is too slow for 500k rows, test with smaller n
small_df = df.head(10000)
benchmark(hyp_loop, small_df, name='iterrows loop')    # ~5.0s
benchmark(hyp_apply, small_df, name='apply')           # ~0.5s
benchmark(hyp_vectorized, df, name='vectorized')       # ~0.01s

# ── Problem: Conditional column based on multiple conditions ──────────────────

# BAD: apply
def classify_apply(df):
    def classify(row):
        if row['a'] > 0 and row['b'] > 0:
            return 'Q1'
        elif row['a'] < 0 and row['b'] > 0:
            return 'Q2'
        elif row['a'] < 0 and row['b'] < 0:
            return 'Q3'
        else:
            return 'Q4'
    return df.apply(classify, axis=1)

# GOOD: np.select (vectorized multi-condition)
def classify_vectorized(df):
    conditions = [
        (df['a'] > 0) & (df['b'] > 0),
        (df['a'] < 0) & (df['b'] > 0),
        (df['a'] < 0) & (df['b'] < 0),
    ]
    choices = ['Q1', 'Q2', 'Q3']
    return np.select(conditions, choices, default='Q4')

benchmark(classify_apply, df, name='apply classify')        # ~25s
benchmark(classify_vectorized, df, name='np.select')        # ~0.05s
# 500x speedup!

# ── Problem: String operations ────────────────────────────────────────────────

df_str = pd.DataFrame({'text': ['Hello World'] * 100000})

# BAD: apply with Python string methods
benchmark(lambda: df_str['text'].apply(lambda x: x.lower()), name='apply lower')

# GOOD: pandas str accessor (vectorized)
benchmark(lambda: df_str['text'].str.lower(), name='str.lower')

# ── Problem: Filtering large DataFrame ───────────────────────────────────────

# GOOD: boolean indexing
benchmark(lambda: df[df['value'] > 50], name='boolean index')

# BETTER: query() — uses numexpr for large DataFrames
benchmark(lambda: df.query('value > 50'), name='query')

# ── Memory-efficient chunked processing ──────────────────────────────────────
def process_large_csv(filepath, chunksize=10000):
    """Process large CSV without loading entirely into memory."""
    results = []
    for chunk in pd.read_csv(filepath, chunksize=chunksize):
        # Process each chunk
        chunk_result = chunk.groupby('category')['value'].sum()
        results.append(chunk_result)
    
    # Combine chunk results
    return pd.concat(results).groupby(level=0).sum()

# ── eval() for complex expressions ───────────────────────────────────────────
# Avoids creating intermediate arrays
df['result'] = df.eval('a * 2 + b ** 2 - value / 10')
# vs:
df['result'] = df['a'] * 2 + df['b'] ** 2 - df['value'] / 10
# eval() is faster for large DataFrames (uses numexpr)
```

### Problem 12: Efficient I/O and data type optimization

```python
import pandas as pd
import numpy as np

# ── Optimized CSV reading ─────────────────────────────────────────────────────
df = pd.read_csv(
    'data.csv',
    dtype={
        'id': 'int32',           # Specify dtypes upfront (avoid inference)
        'category': 'category',  # Categorical from the start
        'flag': 'bool'
    },
    usecols=['id', 'category', 'value'],  # Only load needed columns
    parse_dates=['date'],                  # Parse dates during read
    nrows=1000,                            # Limit rows for testing
    skiprows=lambda i: i > 0 and i % 2 == 0,  # Skip every other row
)

# ── Parquet: best format for pandas data ─────────────────────────────────────
# Parquet preserves dtypes, supports column pruning, much faster than CSV
df.to_parquet('data.parquet', engine='pyarrow', compression='snappy')
df = pd.read_parquet('data.parquet', columns=['id', 'value'])  # Column pruning

# ── Memory optimization pipeline ─────────────────────────────────────────────
def optimize_dataframe(df, verbose=True):
    """Optimize DataFrame memory usage."""
    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type == 'object':
            # Convert low-cardinality strings to category
            num_unique = df[col].nunique()
            num_total = len(df[col])
            if num_unique / num_total < 0.5:
                df[col] = df[col].astype('category')
        
        elif col_type in ['int64', 'int32']:
            c_min = df[col].min()
            c_max = df[col].max()
            if c_min >= np.iinfo(np.int8).min and c_max <= np.iinfo(np.int8).max:
                df[col] = df[col].astype(np.int8)
            elif c_min >= np.iinfo(np.int16).min and c_max <= np.iinfo(np.int16).max:
                df[col] = df[col].astype(np.int16)
            elif c_min >= np.iinfo(np.int32).min and c_max <= np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)
        
        elif col_type == 'float64':
            df[col] = df[col].astype(np.float32)
    
    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    if verbose:
        print(f"Memory reduced: {start_mem:.2f} MB → {end_mem:.2f} MB "
              f"({100 * (start_mem - end_mem) / start_mem:.1f}% reduction)")
    return df

# Usage
np.random.seed(42)
df_large = pd.DataFrame({
    'id': np.random.randint(0, 1000000, 100000),
    'category': np.random.choice(['A', 'B', 'C', 'D'], 100000),
    'value': np.random.randn(100000),
    'count': np.random.randint(0, 255, 100000)
})
df_optimized = optimize_dataframe(df_large)
# Memory reduced: 3.05 MB → 0.48 MB (84.3% reduction)
```

**⚠️ Gotcha — `iterrows` is the slowest iteration method:**
```python
# Speed ranking for row iteration (fastest to slowest):
# 1. Vectorized operations          ← Always prefer
# 2. df.itertuples()                ← Returns namedtuples, ~10x faster than iterrows
# 3. df.to_dict('records') + loop   ← Pure Python dicts
# 4. df.iterrows()                  ← Slowest, creates Series per row

# If you MUST iterate rows, use itertuples:
for row in df.itertuples(index=False):
    print(row.salary, row.dept)  # Attribute access, not dict lookup
```

---

# 🚀 QUICK REFERENCE CARD

## Essential One-Liners

```python
# ── DataFrame Inspection ─────────────────────────────────────────────────────
df.shape                          # (rows, cols)
df.dtypes                         # Column data types
df.describe(include='all')        # Stats for all columns
df.info(memory_usage='deep')      # Memory + dtypes summary
df.nunique()                      # Unique values per column
df.value_counts(normalize=True)   # Frequency table (%)

# ── Selection ────────────────────────────────────────────────────────────────
df.head(10) / df.tail(10)         # First/last N rows
df.sample(n=100, random_state=42) # Random sample
df.nlargest(5, 'salary')          # Top 5 by salary
df.nsmallest(5, 'salary')         # Bottom 5 by salary
df.select_dtypes(include='number')# Numeric columns only
df.filter(like='sales')           # Columns containing 'sales'
df.filter(regex='^Q[1-4]_')       # Columns matching regex

# ── Transformation ───────────────────────────────────────────────────────────
df.rename(columns={'old': 'new'})                    # Rename columns
df.rename(columns=str.lower)                         # Lowercase all columns
df.columns = df.columns.str.replace(' ', '_').str.lower()  # Normalize names
df.assign(new_col=lambda x: x['a'] + x['b'])        # Add column (chainable)
df.pipe(my_function)                                 # Apply function to df
df.sort_values('col', ascending=False, na_position='last')
df.reset_index(drop=True)                            # Reset index, discard old

# ── String Operations ────────────────────────────────────────────────────────
df['col'].str.strip()             # Remove whitespace
df['col'].str.lower() / .upper()  # Case conversion
df['col'].str.split(',', expand=True)  # Split into multiple columns
df['col'].str.extract(r'(\d+)')   # Regex extraction
df['col'].str.replace(r'\s+', ' ', regex=True)  # Normalize whitespace
df['col'].str.len()               # String length

# ── Date Operations ──────────────────────────────────────────────────────────
pd.to_datetime(df['date'], format='%Y-%m-%d')
df['date'].dt.year / .month / .day / .hour
df['date'].dt.day_name()          # 'Monday', 'Tuesday', etc.
df['date'].dt.is_month_end        # Boolean
(df['end'] - df['start']).dt.days # Duration in days

# ── Aggregation Shortcuts ────────────────────────────────────────────────────
df.groupby('col').size()          # Count rows per group (includes NaN)
df.groupby('col').count()         # Count non-null per group
df.groupby('col').first()         # First row per group
df.groupby('col').last()          # Last row per group
df.groupby('col').nth(0)          # Nth row per group (0-indexed)
```

---

## Common Pitfalls Summary

| Pitfall | Wrong | Right |
|---------|-------|-------|
| Chained assignment | `df[mask]['col'] = val` | `df.loc[mask, 'col'] = val` |
| Boolean operators | `df[A > 0 and B > 0]` | `df[(A > 0) & (B > 0)]` |
| loc slice inclusive | Expecting exclusive end | `loc['a':'c']` includes 'c' |
| NaN comparison | `x == np.nan` | `pd.isna(x)` |
| inplace mutation | `df.sort_values(inplace=True)` | `df = df.sort_values()` (CoW) |
| apply performance | Using apply for math | Use vectorized ops |
| Duplicate index after concat | `pd.concat([a, b])` | `pd.concat([a, b], ignore_index=True)` |
| Row explosion in merge | Merging without checking duplicates | Validate with `validate='1:1'` |
| float32 precision | Using float32 for money | Use float64 or Decimal |
| Frequency aliases (2.2+) | `resample('M')` | `resample('ME')` |

---

## Complexity Reference

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| `df[mask]` boolean filter | O(n) | Linear scan |
| `df.loc[label]` | O(1) avg | Hash lookup on index |
| `df.sort_values()` | O(n log n) | Timsort |
| `df.merge()` on indexed col | O(n) | Hash join |
| `df.merge()` on unindexed col | O(n log n) | Sort-merge join |
| `df.groupby().agg()` | O(n) | Single pass |
| `df.pivot_table()` | O(n log n) | Groupby + reshape |
| `df.drop_duplicates()` | O(n) | Hash-based |
| `df.apply(func, axis=1)` | O(n × func_cost) | Python loop |
| Vectorized ops (`df * 2`) | O(n) | C-speed array ops |

---

## pandas Version Compatibility Notes

| Feature | Introduced | Notes |
|---------|-----------|-------|
| Named aggregation `agg(name=(...))` | 0.25 | Replaces dict-based agg |
| `pd.NA` (nullable types) | 1.0 | `Int64`, `boolean`, `StringDtype` |
| `df.map()` on DataFrame | 2.1 | Replaces `applymap` |
| Copy-on-Write (CoW) | 2.0 (opt-in) | Default in 3.0 |
| Frequency alias changes (`ME`, `QE`) | 2.2 | Old aliases deprecated |
| `ArrowDtype` support | 1.5 | `pd.ArrowDtype(pa.int32())` |
| `case_when` | 2.2 | Vectorized conditional |

---

*Last updated for pandas 2.x — Always check [pandas docs](https://pandas.pydata.org/docs/) for latest API changes.*
