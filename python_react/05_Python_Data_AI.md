# 📊 05 — Python for Data & AI (Fractal-Specific)
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q12)](#medium)
- [🔴 Hard (Q13–Q20)](#hard)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is the difference between a Python list and a NumPy array?

**Answer:**

| Feature | Python List | NumPy Array |
|---------|------------|-------------|
| Type | Heterogeneous | Homogeneous (same dtype) |
| Memory | Object pointers | Contiguous block |
| Speed | Slow (Python loops) | Fast (C/Fortran) |
| Operations | Element-by-element | Vectorized |
| Memory usage | High | Low |

```python
import numpy as np
import time

# Python list — stores object references (each element is a Python object)
lst = [1, 2, 3, 4, 5]
lst_doubled = [x * 2 for x in lst]   # Python loop

# NumPy array — stores raw C values in contiguous memory
arr = np.array([1, 2, 3, 4, 5])
arr_doubled = arr * 2   # Vectorized C operation

# Performance comparison
data = list(range(1_000_000))
np_data = np.array(data)

start = time.time()
result = [x**2 for x in data]
print(f"List loop: {time.time()-start:.3f}s")   # ~0.15s

start = time.time()
result = np_data**2
print(f"NumPy:     {time.time()-start:.3f}s")   # ~0.003s (~50x faster)

# NumPy dtypes
arr_int = np.array([1, 2, 3], dtype=np.int32)
arr_float = np.array([1.0, 2.0, 3.0], dtype=np.float64)
arr_bool = np.array([True, False, True], dtype=np.bool_)

print(arr_int.dtype)    # int32
print(arr_int.shape)    # (3,)
print(arr_int.ndim)     # 1
print(arr_int.nbytes)   # 12 (3 × 4 bytes)
```

---

### Q2. What is vectorization in NumPy?

**Answer:**
Vectorization means applying operations to **entire arrays at once** using optimized C/Fortran code, instead of Python loops.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Arithmetic — element-wise
print(arr + 10)        # [11 12 13 14 15]
print(arr * 2)         # [ 2  4  6  8 10]
print(arr ** 2)        # [ 1  4  9 16 25]
print(np.sqrt(arr))    # [1.  1.41 1.73 2.  2.24]

# Comparison — returns boolean array
print(arr > 3)         # [False False False  True  True]
print(arr[arr > 3])    # [4 5] — boolean indexing

# Aggregations
print(arr.sum())       # 15
print(arr.mean())      # 3.0
print(arr.std())       # 1.414...
print(arr.min(), arr.max())  # 1 5

# 2D operations
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix.sum(axis=0))   # [12 15 18] — column sums
print(matrix.sum(axis=1))   # [ 6 15 24] — row sums
print(matrix.T)             # Transpose

# Matrix multiplication
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)    # Matrix multiply: [[19 22] [43 50]]
print(A * B)    # Element-wise:    [[ 5 12] [21 32]]
```

---

### Q3. What is broadcasting in NumPy?

**Answer:**
Broadcasting allows NumPy to perform operations on arrays of **different shapes** by automatically expanding the smaller array.

```python
import numpy as np

# Scalar broadcast
arr = np.array([1, 2, 3, 4, 5])
print(arr + 10)   # [11 12 13 14 15] — 10 broadcast to all elements

# 1D + 2D broadcast
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

row = np.array([10, 20, 30])   # Shape (3,)
print(matrix + row)
# [[11 22 33]
#  [14 25 36]
#  [17 28 39]]
# row is broadcast across each row of matrix

col = np.array([[10], [20], [30]])  # Shape (3, 1)
print(matrix + col)
# [[11 12 13]
#  [24 25 26]
#  [37 38 39]]
# col is broadcast across each column

# Broadcasting rules:
# 1. If arrays have different ndim, prepend 1s to smaller shape
# 2. Dimensions of size 1 are stretched to match the other
# 3. If sizes don't match and neither is 1 → error

# Practical: normalize each row
data = np.random.randn(100, 5)   # 100 samples, 5 features
mean = data.mean(axis=0)         # Shape (5,)
std = data.std(axis=0)           # Shape (5,)
normalized = (data - mean) / std  # Broadcasting: (100,5) - (5,) / (5,)
```

---

### Q4. What is a Pandas DataFrame vs a Series?

**Answer:**
- **Series** — 1D labeled array (like a column)
- **DataFrame** — 2D labeled table (like a spreadsheet or SQL table)

```python
import pandas as pd
import numpy as np

# Series — 1D
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s['b'])      # 20
print(s[s > 15])   # b 20, c 30, d 40

# DataFrame — 2D
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol', 'Dave'],
    'age': [25, 30, 35, 28],
    'salary': [70000, 85000, 90000, 75000],
    'dept': ['Engineering', 'Marketing', 'Engineering', 'HR']
})

# Basic info
print(df.shape)        # (4, 4)
print(df.dtypes)       # column types
print(df.describe())   # statistics
print(df.info())       # memory usage, null counts

# Accessing data
print(df['name'])           # Series — single column
print(df[['name', 'age']])  # DataFrame — multiple columns
print(df.iloc[0])           # First row by position
print(df.loc[0, 'name'])    # Row 0, column 'name'

# Filtering
engineers = df[df['dept'] == 'Engineering']
high_earners = df[df['salary'] > 80000]
```

---

### Q5. What is the difference between `loc` and `iloc`?

**Answer:**
- `loc` — **label-based** indexing (uses index labels and column names)
- `iloc` — **integer position-based** indexing (uses 0-based integers)

```python
import pandas as pd

df = pd.DataFrame({
    'A': [10, 20, 30, 40],
    'B': [50, 60, 70, 80],
    'C': [90, 100, 110, 120]
}, index=['row1', 'row2', 'row3', 'row4'])

# loc — label-based
print(df.loc['row1'])           # Row with label 'row1'
print(df.loc['row1', 'A'])      # 10
print(df.loc['row1':'row3', 'A':'B'])  # Slice by labels (inclusive!)

# iloc — position-based
print(df.iloc[0])               # First row (position 0)
print(df.iloc[0, 0])            # 10
print(df.iloc[0:3, 0:2])        # Slice by position (exclusive end!)

# ⚠️ Key difference: loc slicing is INCLUSIVE on both ends
# iloc slicing is EXCLUSIVE on the end (like Python slicing)

# Boolean indexing works with both
mask = df['A'] > 15
print(df.loc[mask, 'B'])        # B values where A > 15
print(df.loc[mask, ['A', 'C']]) # Multiple columns
```

---

### Q6. What is `groupby` in Pandas? How does it work?

**Answer:**
`groupby` implements the **split-apply-combine** pattern:
1. **Split** data into groups based on a key
2. **Apply** a function to each group
3. **Combine** results into a new DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'dept': ['Eng', 'Eng', 'HR', 'HR', 'Eng', 'HR'],
    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank'],
    'salary': [90000, 85000, 70000, 75000, 95000, 72000],
    'years': [5, 3, 7, 2, 8, 4]
})

# Basic groupby
grouped = df.groupby('dept')

# Aggregations
print(grouped['salary'].mean())
# dept
# Eng    90000.0
# HR     72333.3

print(grouped.agg({
    'salary': ['mean', 'max', 'min'],
    'years': 'mean'
}))

# Multiple group keys
df.groupby(['dept', 'years'])['salary'].mean()

# transform — returns same-size result (for adding group stats back)
df['dept_avg_salary'] = df.groupby('dept')['salary'].transform('mean')

# filter — keep groups meeting a condition
high_paying_depts = df.groupby('dept').filter(lambda g: g['salary'].mean() > 80000)

# apply — custom function per group
def top_earner(group):
    return group.nlargest(1, 'salary')

top_per_dept = df.groupby('dept').apply(top_earner)
```

---

### Q7. What is the difference between `merge`, `join`, and `concat`?

**Answer:**

| Operation | Use case | SQL equivalent |
|-----------|----------|---------------|
| `pd.merge()` | Join on specific columns | JOIN |
| `df.join()` | Join on index | JOIN on index |
| `pd.concat()` | Stack DataFrames | UNION ALL |

```python
import pandas as pd

employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Carol', 'Dave'],
    'dept_id': [10, 20, 10, 30]
})

departments = pd.DataFrame({
    'dept_id': [10, 20, 40],
    'dept_name': ['Engineering', 'Marketing', 'Finance']
})

# merge — like SQL JOIN
inner = pd.merge(employees, departments, on='dept_id', how='inner')
# Only rows with matching dept_id (Carol and Dave excluded)

left = pd.merge(employees, departments, on='dept_id', how='left')
# All employees, NaN for dept_name if no match

outer = pd.merge(employees, departments, on='dept_id', how='outer')
# All rows from both, NaN where no match

# concat — stack DataFrames
q1_sales = pd.DataFrame({'product': ['A', 'B'], 'sales': [100, 200]})
q2_sales = pd.DataFrame({'product': ['A', 'B'], 'sales': [150, 180]})

all_sales = pd.concat([q1_sales, q2_sales], ignore_index=True)
# Stacks rows vertically

# concat columns (axis=1)
combined = pd.concat([employees[['name']], departments[['dept_name']]], axis=1)
```

---

### Q8. What is a pivot table?

**Answer:**
A pivot table **reshapes data** by aggregating values across two dimensions (rows and columns).

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'date': ['2024-01', '2024-01', '2024-02', '2024-02', '2024-01', '2024-02'],
    'product': ['A', 'B', 'A', 'B', 'A', 'B'],
    'region': ['North', 'North', 'North', 'South', 'South', 'South'],
    'sales': [100, 200, 150, 180, 120, 160]
})

# Pivot table
pivot = df.pivot_table(
    values='sales',
    index='date',
    columns='product',
    aggfunc='sum',
    fill_value=0
)
print(pivot)
# product      A    B
# date
# 2024-01    220  200
# 2024-02    150  340

# Multiple aggregations
pivot2 = df.pivot_table(
    values='sales',
    index='date',
    columns='region',
    aggfunc=['sum', 'mean']
)

# Melt — reverse of pivot (wide → long format)
melted = pd.melt(pivot.reset_index(), id_vars='date',
                 var_name='product', value_name='sales')
```

---

### Q9. How would you handle missing values (NaN) in Pandas?

**Answer:**

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, np.nan, 3, np.nan, 5],
    'B': [np.nan, 2, 3, 4, 5],
    'C': ['x', 'y', np.nan, 'w', 'v']
})

# Detect missing values
print(df.isnull())          # Boolean mask
print(df.isnull().sum())    # Count per column
print(df.isnull().sum().sum())  # Total missing

# Drop missing values
df.dropna()                 # Drop rows with ANY NaN
df.dropna(how='all')        # Drop rows where ALL are NaN
df.dropna(subset=['A'])     # Drop rows where A is NaN
df.dropna(axis=1)           # Drop columns with NaN

# Fill missing values
df.fillna(0)                # Fill all NaN with 0
df['A'].fillna(df['A'].mean())   # Fill with column mean
df['A'].fillna(method='ffill')   # Forward fill (propagate last valid)
df['A'].fillna(method='bfill')   # Backward fill

# Interpolate
df['A'].interpolate(method='linear')   # Linear interpolation

# Strategy by column type
for col in df.select_dtypes(include=[np.number]).columns:
    df[col].fillna(df[col].median(), inplace=True)

for col in df.select_dtypes(include=['object']).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Check after
print(df.isnull().sum())   # Should be 0
```

---

### Q10. What is the difference between `apply`, `map`, and `applymap`?

**Answer:**

| Method | Applied to | Input | Use case |
|--------|-----------|-------|----------|
| `Series.map()` | Series | Element | Element-wise transform on Series |
| `Series.apply()` | Series | Element or Series | Custom function on Series |
| `DataFrame.apply()` | DataFrame | Row or Column (Series) | Function on rows/columns |
| `DataFrame.applymap()` / `map()` | DataFrame | Element | Element-wise on entire DataFrame |

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['alice', 'bob', 'carol'],
    'score': [85, 92, 78],
    'grade': ['B', 'A', 'C']
})

# Series.map — element-wise, great for mapping values
grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0}
df['gpa'] = df['grade'].map(grade_map)

# Series.apply — custom function
df['score_normalized'] = df['score'].apply(lambda x: (x - 70) / 30)

# DataFrame.apply — function on rows or columns
df['total'] = df[['score']].apply(lambda row: row.sum(), axis=1)
col_means = df[['score']].apply(lambda col: col.mean(), axis=0)

# DataFrame.applymap (pandas < 2.1) / map (pandas >= 2.1) — element-wise
df_str = df[['name', 'grade']].applymap(str.upper)

# Performance tip: vectorized operations >> apply >> map >> loops
# Use apply only when vectorized operations aren't possible
df['score_category'] = pd.cut(df['score'],
                               bins=[0, 70, 85, 100],
                               labels=['Low', 'Medium', 'High'])
```

---

### Q11. What is method chaining in Pandas?

**Answer:**
Method chaining applies multiple transformations in a **single expression**, improving readability.

```python
import pandas as pd

# Without chaining — verbose, creates intermediate variables
df1 = df.dropna()
df2 = df1[df1['salary'] > 50000]
df3 = df2.groupby('dept')['salary'].mean()
df4 = df3.reset_index()
df5 = df4.rename(columns={'salary': 'avg_salary'})
df6 = df5.sort_values('avg_salary', ascending=False)

# With chaining — clean pipeline
result = (
    df
    .dropna()
    .query('salary > 50000')
    .groupby('dept')['salary']
    .mean()
    .reset_index()
    .rename(columns={'salary': 'avg_salary'})
    .sort_values('avg_salary', ascending=False)
)

# .pipe() — insert custom functions into chain
def add_rank(df):
    df['rank'] = df['avg_salary'].rank(ascending=False)
    return df

result = (
    df
    .dropna()
    .query('salary > 50000')
    .groupby('dept')['salary'].mean()
    .reset_index()
    .rename(columns={'salary': 'avg_salary'})
    .pipe(add_rank)
    .sort_values('rank')
)

# ⚠️ Cons of chaining:
# - Harder to debug (can't inspect intermediate steps)
# - Use .assign() to add columns without breaking chain
result = (
    df
    .assign(salary_k=lambda x: x['salary'] / 1000)
    .assign(is_senior=lambda x: x['years'] > 5)
)
```

---

### Q12. What is the difference between wide and long (tidy) data formats?

**Answer:**
- **Wide format** — each variable has its own column (easier to read)
- **Long/Tidy format** — each row is one observation (better for analysis, plotting)

```python
import pandas as pd

# Wide format — one row per subject
wide = pd.DataFrame({
    'student': ['Alice', 'Bob'],
    'math': [90, 85],
    'science': [88, 92],
    'english': [75, 80]
})

# Long format — one row per observation
long = pd.DataFrame({
    'student': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob'],
    'subject': ['math', 'science', 'english', 'math', 'science', 'english'],
    'score': [90, 88, 75, 85, 92, 80]
})

# Convert wide → long (melt)
long = pd.melt(
    wide,
    id_vars=['student'],
    value_vars=['math', 'science', 'english'],
    var_name='subject',
    value_name='score'
)

# Convert long → wide (pivot)
wide_again = long.pivot(index='student', columns='subject', values='score')
wide_again.columns.name = None  # Remove column name
wide_again = wide_again.reset_index()

# When to use:
# Wide: human-readable reports, Excel
# Long: groupby, seaborn/matplotlib plotting, statistical analysis
```

---

<a name="hard"></a>
## 🔴 Hard

---

### Q13. How would you process a CSV file larger than available RAM?

**Answer:**

```python
import pandas as pd
import numpy as np

# Method 1: Chunking
def process_large_csv(filepath: str, chunk_size: int = 100_000):
    """Process file in chunks, aggregate results"""
    results = []

    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        # Process each chunk
        chunk_result = (
            chunk
            .dropna(subset=['value'])
            .query('status == "active"')
            .groupby('category')['value']
            .agg(['sum', 'count'])
        )
        results.append(chunk_result)

    # Combine chunk results
    final = pd.concat(results).groupby(level=0).sum()
    final['mean'] = final['sum'] / final['count']
    return final

# Method 2: Specify dtypes upfront (reduces memory)
dtypes = {
    'id': np.int32,
    'value': np.float32,
    'category': 'category',   # Categorical for low-cardinality strings
    'status': 'category',
}
df = pd.read_csv('large.csv', dtype=dtypes, usecols=['id', 'value', 'category'])

# Method 3: Dask — parallel, out-of-core processing
# import dask.dataframe as dd
# df = dd.read_csv('large.csv')  # Lazy — doesn't load yet
# result = df.groupby('category')['value'].mean().compute()  # Execute

# Method 4: Polars — faster than Pandas, lazy evaluation
# import polars as pl
# df = pl.scan_csv('large.csv')  # Lazy scan
# result = df.filter(pl.col('value') > 0).groupby('category').agg(pl.col('value').mean()).collect()

# Method 5: SQLite for very large files
import sqlite3
conn = sqlite3.connect(':memory:')
for chunk in pd.read_csv('large.csv', chunksize=100_000):
    chunk.to_sql('data', conn, if_exists='append', index=False)
result = pd.read_sql('SELECT category, AVG(value) FROM data GROUP BY category', conn)
```

---

### Q14. What is the difference between eager and lazy evaluation?

**Answer:**
- **Eager evaluation** — expressions are evaluated **immediately** when defined
- **Lazy evaluation** — expressions are evaluated **only when needed**

```python
# EAGER — Python default
lst = [x**2 for x in range(10)]   # Computed immediately, stored in memory
print(lst[0])   # Already computed

# LAZY — generators
gen = (x**2 for x in range(10))   # Not computed yet
print(next(gen))   # Computed on demand

# Lazy pipeline — nothing executes until consumed
import json

def read_file(path):
    with open(path) as f:
        yield from f                    # Lazy

def parse(lines):
    return (json.loads(l) for l in lines)  # Lazy

def filter_active(records):
    return (r for r in records if r['active'])  # Lazy

def extract(records, field):
    return (r[field] for r in records)  # Lazy

# Nothing has executed yet!
# pipeline = extract(filter_active(parse(read_file("data.jsonl"))), "name")
# for name in pipeline:  # NOW it executes, one record at a time
#     print(name)

# Pandas: lazy with query strings
df.query('salary > 50000 and dept == "Engineering"')  # Optimized internally

# Polars: truly lazy
# import polars as pl
# result = (
#     pl.scan_csv("data.csv")   # Lazy
#     .filter(pl.col("salary") > 50000)  # Lazy
#     .groupby("dept")          # Lazy
#     .agg(pl.col("salary").mean())  # Lazy
#     .collect()                # NOW execute
# )
```

---

### Q15. What is a data pipeline? Key considerations?

**Answer:**
A data pipeline is a series of **data processing steps** that move data from source to destination.

```
Source → Extract → Transform → Load → Destination
```

```python
from abc import ABC, abstractmethod
from typing import Iterator, Any
import logging

# Pipeline stage interface
class PipelineStage(ABC):
    @abstractmethod
    def process(self, data: Iterator) -> Iterator: ...

class ExtractStage(PipelineStage):
    def __init__(self, source: str):
        self.source = source

    def process(self, data=None) -> Iterator:
        # Read from source
        with open(self.source) as f:
            for line in f:
                yield line.strip()

class TransformStage(PipelineStage):
    def process(self, data: Iterator) -> Iterator:
        import json
        for record in data:
            try:
                parsed = json.loads(record)
                # Normalize
                parsed['name'] = parsed.get('name', '').strip().title()
                parsed['value'] = float(parsed.get('value', 0))
                yield parsed
            except (json.JSONDecodeError, ValueError) as e:
                logging.warning(f"Skipping invalid record: {e}")

class LoadStage(PipelineStage):
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size

    def process(self, data: Iterator) -> Iterator:
        batch = []
        for record in data:
            batch.append(record)
            if len(batch) >= self.batch_size:
                self._flush(batch)
                batch = []
                yield len(batch)
        if batch:
            self._flush(batch)

    def _flush(self, batch):
        print(f"Writing {len(batch)} records to DB")

# Key considerations:
# 1. Idempotency — running twice gives same result
# 2. Error handling — dead letter queue for failed records
# 3. Monitoring — track records processed, errors, latency
# 4. Backpressure — don't overwhelm downstream systems
# 5. Checkpointing — resume from failure point
# 6. Schema validation — validate data at each stage
```

---

### Q16. What is the difference between ETL and ELT?

**Answer:**

| | ETL | ELT |
|-|-----|-----|
| Order | Extract → **Transform** → Load | Extract → Load → **Transform** |
| Transform location | Before loading (external) | After loading (in data warehouse) |
| Best for | Traditional DW, sensitive data | Cloud DW (BigQuery, Snowflake, Redshift) |
| Flexibility | Less flexible | More flexible |
| Cost | Compute outside DW | Compute inside DW |

```python
# ETL — transform before loading
def etl_pipeline(source_db, target_db):
    # Extract
    raw_data = source_db.query("SELECT * FROM orders")

    # Transform (in Python/Spark)
    transformed = (
        raw_data
        .dropna()
        .assign(
            total=lambda df: df['quantity'] * df['price'],
            date=lambda df: pd.to_datetime(df['date'])
        )
        .query('total > 0')
    )

    # Load
    transformed.to_sql('orders_clean', target_db, if_exists='replace')

# ELT — load raw, transform in DW
def elt_pipeline(source_db, bigquery_client):
    # Extract + Load raw
    raw_data = source_db.query("SELECT * FROM orders")
    raw_data.to_gbq('dataset.orders_raw', project_id='my-project')

    # Transform in BigQuery (SQL)
    bigquery_client.query("""
        CREATE OR REPLACE TABLE dataset.orders_clean AS
        SELECT
            *,
            quantity * price AS total,
            PARSE_DATE('%Y-%m-%d', date) AS parsed_date
        FROM dataset.orders_raw
        WHERE quantity * price > 0
    """)
```

---

### Q17. What is feature engineering? Give 3 examples.

**Answer:**
Feature engineering transforms raw data into **informative features** that improve model performance.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100),
    'price': np.random.uniform(10, 100, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'user_id': np.random.randint(1, 20, 100),
    'text': ['sample text'] * 100
})

# 1. TEMPORAL FEATURES — extract from datetime
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['quarter'] = df['date'].dt.quarter

# 2. ENCODING CATEGORICAL VARIABLES
# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['category'], prefix='cat')

# Label encoding (for ordinal)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# Target encoding (mean of target per category)
target_mean = df.groupby('category')['price'].mean()
df['category_target_enc'] = df['category'].map(target_mean)

# 3. AGGREGATION FEATURES — user-level statistics
user_stats = df.groupby('user_id')['price'].agg([
    ('user_avg_price', 'mean'),
    ('user_total_spend', 'sum'),
    ('user_purchase_count', 'count'),
    ('user_max_price', 'max'),
])
df = df.merge(user_stats, on='user_id')

# 4. INTERACTION FEATURES
df['price_per_day'] = df['price'] / (df['day_of_week'] + 1)

# 5. BINNING / DISCRETIZATION
df['price_bucket'] = pd.cut(df['price'],
                             bins=[0, 25, 50, 75, 100],
                             labels=['low', 'medium', 'high', 'premium'])

# 6. ROLLING WINDOW FEATURES (time series)
df = df.sort_values('date')
df['price_7day_avg'] = df['price'].rolling(window=7, min_periods=1).mean()
df['price_7day_std'] = df['price'].rolling(window=7, min_periods=1).std()
```

---

### Q18. What is data leakage in machine learning?

**Answer:**
Data leakage occurs when **information from the test set or future data** is used during training, causing overly optimistic performance estimates.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({
    'feature': range(100),
    'target': range(100)
})

# ❌ LEAKAGE: Scaling before split
scaler = StandardScaler()
df['feature_scaled'] = scaler.fit_transform(df[['feature']])  # Uses ALL data stats!
X_train, X_test = train_test_split(df['feature_scaled'], test_size=0.2)
# Test data statistics leaked into training normalization

# ✅ CORRECT: Split first, then fit scaler on train only
X = df[['feature']]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # Fit on train only
X_test_scaled = scaler.transform(X_test)          # Transform test with train stats

# ❌ LEAKAGE: Target encoding without cross-validation
# df['cat_encoded'] = df.groupby('category')['target'].transform('mean')
# This uses target values from the same rows being predicted!

# ✅ CORRECT: Use cross-validation for target encoding
# from category_encoders import TargetEncoder
# encoder = TargetEncoder()
# X_train['cat_encoded'] = encoder.fit_transform(X_train['category'], y_train)
# X_test['cat_encoded'] = encoder.transform(X_test['category'])

# ❌ LEAKAGE: Using future data in time series
# df['next_day_price'] = df['price'].shift(-1)  # Future info!

# ✅ CORRECT: Only use past data
# df['prev_day_price'] = df['price'].shift(1)   # Past info only
```

---

### Q19. What is the difference between normalization and standardization?

**Answer:**

| | Normalization (Min-Max) | Standardization (Z-score) |
|-|------------------------|--------------------------|
| Formula | `(x - min) / (max - min)` | `(x - mean) / std` |
| Range | [0, 1] | No fixed range |
| Sensitive to outliers | ✅ Yes | Less so |
| Use when | Neural networks, KNN, image data | Linear models, SVM, PCA |

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

data = np.array([[1], [2], [3], [4], [100]])  # 100 is an outlier

# Normalization — scales to [0, 1]
min_max = MinMaxScaler()
normalized = min_max.fit_transform(data)
print(normalized.flatten())
# [0.    0.01  0.02  0.03  1.  ] — outlier dominates!

# Standardization — mean=0, std=1
standard = StandardScaler()
standardized = standard.fit_transform(data)
print(standardized.flatten())
# [-0.67 -0.63 -0.59 -0.55  2.44]

# Robust scaling — uses median and IQR (outlier-resistant)
robust = RobustScaler()
robust_scaled = robust.fit_transform(data)
print(robust_scaled.flatten())
# [-0.67 -0.33  0.    0.33 64.33] — outlier less impactful

# When to use:
# MinMaxScaler: bounded input needed (neural nets, image pixels)
# StandardScaler: normally distributed data, linear models
# RobustScaler: data with outliers
```

---

### Q20. What is cross-validation? Why is it important?

**Answer:**
Cross-validation evaluates model performance by training and testing on **multiple different splits** of the data, giving a more reliable estimate than a single train/test split.

```python
import numpy as np
from sklearn.model_selection import (
    cross_val_score, KFold, StratifiedKFold,
    TimeSeriesSplit, cross_validate
)
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
model = LogisticRegression()

# K-Fold CV — split into k folds, train on k-1, test on 1
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')
print(f"Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

# Stratified K-Fold — preserves class distribution in each fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf)

# Time Series Split — respects temporal order (no future leakage)
tscv = TimeSeriesSplit(n_splits=5)
# Each fold: train on past, test on future

# Multiple metrics at once
results = cross_validate(model, X, y, cv=5,
                         scoring=['accuracy', 'f1', 'roc_auc'])
print(f"Accuracy: {results['test_accuracy'].mean():.3f}")
print(f"F1:       {results['test_f1'].mean():.3f}")
print(f"AUC:      {results['test_roc_auc'].mean():.3f}")

# Why CV matters:
# Single split: high variance estimate (lucky/unlucky split)
# CV: averages over multiple splits → more reliable
# Detects overfitting: high train score, low CV score
```

---

### [← Back to Index](./00_INDEX.md) | [Next: Python Testing →](./06_Python_Testing.md)
