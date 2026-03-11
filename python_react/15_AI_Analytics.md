# 🤖 15 — AI & Analytics Concepts (Fractal AI Specific)
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q15)](#medium)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is the difference between supervised, unsupervised, and reinforcement learning?

**Answer:**

| Type | Training Data | Goal | Examples |
|------|--------------|------|---------|
| **Supervised** | Labeled (X, y) | Predict y from X | Classification, Regression |
| **Unsupervised** | Unlabeled (X only) | Find patterns | Clustering, Dimensionality reduction |
| **Reinforcement** | Rewards/penalties | Maximize reward | Game playing, Robotics |

```python
# Supervised — learn from labeled examples
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

X_train = [[1, 2], [3, 4], [5, 6], [7, 8]]
y_train = [0, 0, 1, 1]  # Labels provided

model = RandomForestClassifier()
model.fit(X_train, y_train)
predictions = model.predict([[2, 3]])  # [0]

# Unsupervised — find structure without labels
from sklearn.cluster import KMeans

X = [[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]]
kmeans = KMeans(n_clusters=2)
kmeans.fit(X)
print(kmeans.labels_)  # [0, 0, 0, 1, 1, 1] — two clusters found

# Reinforcement — agent learns from environment
# Agent takes action → receives reward → updates policy
# Examples: AlphaGo, ChatGPT (RLHF), recommendation systems
```

---

### Q2. What is overfitting? How do you detect and prevent it?

**Answer:**
Overfitting occurs when a model **memorizes training data** instead of learning general patterns — performs well on training data but poorly on new data.

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Overfitting detection: large gap between train and test scores
model = DecisionTreeClassifier(max_depth=None)  # Unlimited depth
model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)  # 1.0 — memorized!
test_score = model.score(X_test, y_test)     # 0.75 — poor generalization

print(f"Train: {train_score:.2f}, Test: {test_score:.2f}")
# Train: 1.00, Test: 0.75 → OVERFITTING

# Prevention techniques:
# 1. Regularization (L1/L2)
from sklearn.linear_model import Ridge, Lasso
ridge = Ridge(alpha=1.0)  # L2 regularization

# 2. Limit model complexity
model = DecisionTreeClassifier(max_depth=5)  # Limit tree depth

# 3. More training data
# 4. Dropout (neural networks)
# 5. Early stopping
# 6. Cross-validation to detect overfitting
cv_scores = cross_val_score(model, X, y, cv=5)
print(f"CV: {cv_scores.mean():.2f} ± {cv_scores.std():.2f}")
```

---

### Q3. What is the bias-variance tradeoff?

**Answer:**
- **Bias** — error from wrong assumptions (underfitting — model too simple)
- **Variance** — error from sensitivity to training data (overfitting — model too complex)
- **Total Error = Bias² + Variance + Irreducible Noise**

```
High Bias (Underfitting):
- Model too simple
- High training error AND high test error
- Example: Linear model for non-linear data

High Variance (Overfitting):
- Model too complex
- Low training error BUT high test error
- Example: Deep decision tree

Sweet spot: balance bias and variance

Bias ↑ as model complexity ↓
Variance ↑ as model complexity ↑

Solutions:
- High bias: more features, more complex model, less regularization
- High variance: more data, simpler model, more regularization, dropout
```

```python
# Visualizing bias-variance tradeoff
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Underfitting (high bias)
model_simple = Pipeline([
    ('poly', PolynomialFeatures(degree=1)),
    ('linear', LinearRegression())
])

# Good fit
model_good = Pipeline([
    ('poly', PolynomialFeatures(degree=3)),
    ('linear', LinearRegression())
])

# Overfitting (high variance)
model_complex = Pipeline([
    ('poly', PolynomialFeatures(degree=15)),
    ('linear', LinearRegression())
])
```

---

### Q4. What is a confusion matrix? Precision, recall, F1, accuracy?

**Answer:**

```
Confusion Matrix:
                 Predicted Positive  Predicted Negative
Actual Positive       TP                  FN
Actual Negative       FP                  TN

Accuracy  = (TP + TN) / (TP + TN + FP + FN)  — overall correctness
Precision = TP / (TP + FP)                    — of predicted positives, how many are correct?
Recall    = TP / (TP + FN)                    — of actual positives, how many did we catch?
F1 Score  = 2 * (Precision * Recall) / (Precision + Recall)  — harmonic mean
```

```python
from sklearn.metrics import (
    confusion_matrix, classification_report,
    accuracy_score, precision_score, recall_score, f1_score
)

y_true = [1, 1, 1, 0, 0, 0, 1, 0]
y_pred = [1, 1, 0, 0, 0, 1, 1, 0]

print(confusion_matrix(y_true, y_pred))
# [[2 1]   ← TN=2, FP=1
#  [1 4]]  ← FN=1, TP=4

print(classification_report(y_true, y_pred))

# When to use which metric:
# Accuracy: balanced classes, equal cost of errors
# Precision: cost of false positives is high (spam filter — don't block real emails)
# Recall: cost of false negatives is high (cancer detection — don't miss cases)
# F1: imbalanced classes, need balance of precision and recall
# AUC-ROC: overall model performance across all thresholds
```

---

### Q5. What is the difference between classification and regression?

**Answer:**

| | Classification | Regression |
|-|---------------|-----------|
| Output | Discrete class | Continuous value |
| Examples | Spam/not spam, churn prediction | Price prediction, sales forecast |
| Metrics | Accuracy, F1, AUC | MAE, RMSE, R² |
| Algorithms | Logistic Regression, Random Forest, SVM | Linear Regression, XGBoost, Neural Networks |

```python
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Classification — predict category
# "Will this customer churn?" → Yes/No
clf = RandomForestClassifier()
clf.fit(X_train, y_train)  # y_train: [0, 1, 1, 0, ...]
proba = clf.predict_proba(X_test)  # [[0.8, 0.2], [0.3, 0.7], ...]

# Regression — predict value
# "What will this customer's lifetime value be?" → $1,234
reg = RandomForestRegressor()
reg.fit(X_train, y_train)  # y_train: [1200, 3400, 890, ...]
predictions = reg.predict(X_test)  # [1150, 3200, 920, ...]

# Regression metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)  # 1.0 = perfect, 0 = baseline
```

---

### Q6. What is feature importance? How would you explain a model to a non-technical stakeholder?

**Answer:**
Feature importance measures **how much each feature contributes** to the model's predictions.

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Feature importance
feature_names = ['age', 'income', 'tenure', 'num_products', 'is_active']
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance_df)
# feature      importance
# income       0.35
# tenure       0.28
# age          0.18
# num_products 0.12
# is_active    0.07

# SHAP values — more interpretable
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, feature_names=feature_names)

# Explaining to non-technical stakeholders:
# "Our model predicts customer churn with 87% accuracy.
#  The most important factors are:
#  1. Income (35%) — lower income customers churn more
#  2. Tenure (28%) — newer customers are more likely to leave
#  3. Age (18%) — younger customers churn more
#  
#  For customer ID 12345, the model predicts 73% churn probability
#  mainly because their income dropped 20% last quarter."
```

---

### Q7. What is A/B testing? What statistical concepts are involved?

**Answer:**
A/B testing compares two versions (A and B) to determine which performs better, using **statistical hypothesis testing**.

```python
import numpy as np
from scipy import stats

# Scenario: Testing two versions of a button
# Version A (control): 1000 users, 100 conversions (10%)
# Version B (treatment): 1000 users, 130 conversions (13%)

n_a, conv_a = 1000, 100
n_b, conv_b = 1000, 130

rate_a = conv_a / n_a  # 0.10
rate_b = conv_b / n_b  # 0.13

# Two-proportion z-test
# H0: rate_a == rate_b (no difference)
# H1: rate_a != rate_b (there is a difference)

pooled_rate = (conv_a + conv_b) / (n_a + n_b)
se = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/n_a + 1/n_b))
z_stat = (rate_b - rate_a) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"Z-statistic: {z_stat:.3f}")
print(f"P-value: {p_value:.4f}")
print(f"Significant: {p_value < 0.05}")

# Key concepts:
# p-value: probability of seeing this result if H0 is true
# p < 0.05: statistically significant (reject H0)
# Statistical power: probability of detecting a real effect
# Sample size: larger = more power to detect small effects
# Confidence interval: range where true effect likely falls

# Practical significance vs statistical significance:
# 0.1% improvement might be statistically significant with 1M users
# but not worth the engineering effort (practical significance)
```

---

### Q8. What is a data warehouse vs a data lake?

**Answer:**

| Feature | Data Warehouse | Data Lake |
|---------|---------------|-----------|
| Data type | Structured | All types (structured, semi, unstructured) |
| Schema | Schema-on-write | Schema-on-read |
| Processing | ETL | ELT |
| Users | Business analysts | Data scientists |
| Query speed | Fast | Slower |
| Cost | Higher | Lower |
| Examples | Snowflake, BigQuery, Redshift | S3, Azure Data Lake, GCS |

```
Data Lake:
Raw data → S3/GCS → Process when needed
✅ Cheap storage
✅ All data types (JSON, CSV, images, logs)
✅ Flexible schema
❌ Slower queries
❌ Can become "data swamp" without governance

Data Warehouse:
Cleaned data → Snowflake/BigQuery → Fast queries
✅ Fast analytical queries
✅ Consistent schema
✅ Business-ready
❌ Expensive
❌ Only structured data

Modern approach: Data Lakehouse (Delta Lake, Apache Iceberg)
Combines benefits of both: cheap storage + fast queries + ACID transactions
```

---

### Q9. What is the difference between OLTP and OLAP?

**Answer:**

| Feature | OLTP | OLAP |
|---------|------|------|
| Purpose | Transactions | Analytics |
| Operations | INSERT, UPDATE, DELETE | SELECT (aggregations) |
| Data volume | Small per query | Large |
| Query complexity | Simple | Complex |
| Optimization | Write speed | Read speed |
| Examples | PostgreSQL, MySQL | BigQuery, Snowflake, Redshift |

```sql
-- OLTP: operational queries
-- "Process this order"
INSERT INTO orders (user_id, product_id, amount) VALUES (123, 456, 99.99);
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 456;

-- OLAP: analytical queries
-- "What were our top 10 products by revenue last quarter?"
SELECT
    p.name,
    SUM(o.amount) as total_revenue,
    COUNT(*) as order_count
FROM orders o
JOIN products p ON o.product_id = p.id
WHERE o.created_at >= '2024-01-01'
  AND o.created_at < '2024-04-01'
GROUP BY p.name
ORDER BY total_revenue DESC
LIMIT 10;
```

---

### Q10. What makes a good data visualization?

**Answer:**
A good visualization **communicates insights clearly** to the intended audience.

```
Principles of good data visualization:

1. CLARITY — one clear message per chart
   ✅ "Revenue grew 40% YoY"
   ❌ 15 metrics on one chart

2. APPROPRIATE CHART TYPE
   - Trend over time → Line chart
   - Comparison → Bar chart
   - Part of whole → Pie/Donut (max 5 slices)
   - Distribution → Histogram/Box plot
   - Correlation → Scatter plot
   - Geographic → Map

3. HONEST AXES
   ✅ Y-axis starts at 0 for bar charts
   ❌ Truncated axis to exaggerate differences

4. COLOR PURPOSEFULLY
   ✅ Use color to encode data (not decoration)
   ✅ Colorblind-friendly palettes
   ❌ Rainbow colors for continuous data

5. REDUCE CHART JUNK
   ✅ Remove gridlines, borders, 3D effects
   ✅ Direct labels instead of legends

6. CONTEXT
   ✅ Include units, time period, data source
   ✅ Highlight key insight with annotation
```

---

### Q11. What is the difference between a KPI and a metric?

**Answer:**
- **Metric** — any measurable value (page views, clicks, revenue)
- **KPI** (Key Performance Indicator) — a **critical metric** tied to a business objective

```
Metrics: page views, bounce rate, session duration, clicks, conversions
KPIs: Monthly Active Users (MAU), Customer Acquisition Cost (CAC),
      Net Promoter Score (NPS), Customer Lifetime Value (CLV),
      Churn Rate, Revenue Growth Rate

Good KPIs are:
✅ Specific — clearly defined
✅ Measurable — quantifiable
✅ Actionable — you can influence it
✅ Relevant — tied to business goals
✅ Time-bound — measured over a period

Example for Fractal AI:
KPI: Model accuracy improvement (business goal: better predictions)
Metric: Training loss, validation accuracy, inference time
```

---

### Q12. What is SQL? Key JOIN types?

**Answer:**

```sql
-- Sample tables
-- users: id, name, dept_id
-- departments: id, name

-- INNER JOIN — only matching rows
SELECT u.name, d.name as dept
FROM users u
INNER JOIN departments d ON u.dept_id = d.id;
-- Returns: users WITH a matching department

-- LEFT JOIN — all left rows + matching right
SELECT u.name, d.name as dept
FROM users u
LEFT JOIN departments d ON u.dept_id = d.id;
-- Returns: ALL users, NULL dept if no match

-- RIGHT JOIN — all right rows + matching left
SELECT u.name, d.name as dept
FROM users u
RIGHT JOIN departments d ON u.dept_id = d.id;
-- Returns: ALL departments, NULL user if no match

-- FULL OUTER JOIN — all rows from both
SELECT u.name, d.name as dept
FROM users u
FULL OUTER JOIN departments d ON u.dept_id = d.id;
-- Returns: ALL users AND ALL departments

-- CROSS JOIN — cartesian product
SELECT u.name, d.name
FROM users u
CROSS JOIN departments d;
-- Returns: every user × every department combination

-- Self JOIN — join table with itself
SELECT e.name as employee, m.name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

---

### Q13. What is the difference between `GROUP BY` and `PARTITION BY`?

**Answer:**
- `GROUP BY` — **aggregates rows** into groups (reduces row count)
- `PARTITION BY` — **window function** that computes over groups without reducing rows

```sql
-- GROUP BY — reduces to one row per group
SELECT
    dept_id,
    AVG(salary) as avg_salary,
    COUNT(*) as headcount
FROM employees
GROUP BY dept_id;
-- Result: one row per department

-- PARTITION BY — keeps all rows, adds aggregate as column
SELECT
    name,
    dept_id,
    salary,
    AVG(salary) OVER (PARTITION BY dept_id) as dept_avg_salary,
    salary - AVG(salary) OVER (PARTITION BY dept_id) as diff_from_avg,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) as salary_rank
FROM employees;
-- Result: all rows, with department average added to each row

-- Running total
SELECT
    date,
    revenue,
    SUM(revenue) OVER (ORDER BY date) as cumulative_revenue
FROM daily_sales;

-- Moving average
SELECT
    date,
    revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM daily_sales;
```

---

### Q14. What is an index in a database? How does it improve performance?

**Answer:**
An index is a **data structure** (usually B-tree) that allows the database to find rows quickly without scanning the entire table.

```sql
-- Without index: full table scan O(n)
SELECT * FROM users WHERE email = 'alice@example.com';
-- Scans every row!

-- Create index
CREATE INDEX idx_users_email ON users(email);

-- With index: B-tree lookup O(log n)
SELECT * FROM users WHERE email = 'alice@example.com';
-- Jumps directly to the row!

-- Composite index
CREATE INDEX idx_users_dept_salary ON users(dept_id, salary);
-- Efficient for: WHERE dept_id = 1 AND salary > 50000
-- Also efficient for: WHERE dept_id = 1 (leftmost prefix)
-- NOT efficient for: WHERE salary > 50000 (not leftmost)

-- When to add indexes:
-- ✅ Columns in WHERE clauses
-- ✅ Columns in JOIN conditions
-- ✅ Columns in ORDER BY
-- ❌ Columns rarely queried
-- ❌ Small tables (full scan is fine)
-- ❌ Columns with many writes (index maintenance overhead)

-- EXPLAIN to see query plan
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';
-- Shows: Seq Scan (no index) vs Index Scan (with index)
```

---

### Q15. What is data normalization in databases?

**Answer:**
Normalization organizes data to **reduce redundancy** and improve data integrity.

```sql
-- ❌ Unnormalized (1NF violation — repeating groups)
-- orders: id, customer_name, customer_email, product1, product2, product3

-- ✅ 1NF — atomic values, no repeating groups
-- orders: id, customer_id, product_id, quantity

-- ❌ 2NF violation — partial dependency
-- order_items: order_id, product_id, product_name, quantity
-- product_name depends only on product_id, not the full key

-- ✅ 2NF — remove partial dependencies
-- order_items: order_id, product_id, quantity
-- products: id, name, price

-- ❌ 3NF violation — transitive dependency
-- employees: id, dept_id, dept_name
-- dept_name depends on dept_id, not employee id

-- ✅ 3NF — remove transitive dependencies
-- employees: id, dept_id
-- departments: id, name

-- Normal forms:
-- 1NF: atomic values, no repeating groups
-- 2NF: 1NF + no partial dependencies (all non-key columns depend on full key)
-- 3NF: 2NF + no transitive dependencies
-- BCNF: stricter version of 3NF

-- When to denormalize:
-- Read-heavy analytics (joins are expensive)
-- Data warehouses often use star schema (denormalized)
```

---

### [← Back to Index](./00_INDEX.md) | [Next: JavaScript Quick-Fire →](./16_JavaScript_QuickFire.md)
