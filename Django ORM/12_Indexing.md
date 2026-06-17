# Module 12: Database Indexing & Constraints

This file contains structured interview questions and detailed answers targeting Django ORM concepts at Senior, Lead, and Architect levels.

---

# Question 1: What is a database index and how do you declare it in Django?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is a database index and how do you declare it in Django?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is a database index and how do you declare it in Django?
from django.db import models

class IndexModel26(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_26'),
            models.Index(fields=['code'], name='valid_code_idx_26', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 2: What is the difference between db_index=True on a field and indexes in Meta?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is the difference between db_index=True on a field and indexes in Meta?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is the difference between db_index=True on a field and indexes in Meta?
from django.db import models

class IndexModel27(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_27'),
            models.Index(fields=['code'], name='valid_code_idx_27', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 3: How does a B-Tree index work under the hood?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How does a B-Tree index work under the hood?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How does a B-Tree index work under the hood?
from django.db import models

class IndexModel28(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_28'),
            models.Index(fields=['code'], name='valid_code_idx_28', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 4: What is a Partial Index and how do you implement it in Django?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is a Partial Index and how do you implement it in Django?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is a Partial Index and how do you implement it in Django?
from django.db import models

class IndexModel29(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_29'),
            models.Index(fields=['code'], name='valid_code_idx_29', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 5: What is a Functional Index and how do you implement it (e.g. indexing lowercase email)?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is a Functional Index and how do you implement it (e.g. indexing lowercase email)?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is a Functional Index and how do you implement it (e.g. indexing lowercase email)?
from django.db import models

class IndexModel30(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_30'),
            models.Index(fields=['code'], name='valid_code_idx_30', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 6: What is a Composite (multi-column) Index and how does the column order matter?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is a Composite (multi-column) Index and how does the column order matter?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is a Composite (multi-column) Index and how does the column order matter?
from django.db import models

class IndexModel31(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_31'),
            models.Index(fields=['code'], name='valid_code_idx_31', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 7: How does Django 5.0 implement unique constraints using UniqueConstraint in Meta?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How does Django 5.0 implement unique constraints using UniqueConstraint in Meta?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How does Django 5.0 implement unique constraints using UniqueConstraint in Meta?
from django.db import models

class IndexModel32(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_32'),
            models.Index(fields=['code'], name='valid_code_idx_32', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 8: What is the difference between a unique database index and a unique constraint?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is the difference between a unique database index and a unique constraint?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is the difference between a unique database index and a unique constraint?
from django.db import models

class IndexModel33(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_33'),
            models.Index(fields=['code'], name='valid_code_idx_33', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 9: How do you implement partial unique constraints in Django?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How do you implement partial unique constraints in Django?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How do you implement partial unique constraints in Django?
from django.db import models

class IndexModel34(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_34'),
            models.Index(fields=['code'], name='valid_code_idx_34', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 10: How does indexing affect INSERT, UPDATE, and DELETE performance?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How does indexing affect INSERT, UPDATE, and DELETE performance?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How does indexing affect INSERT, UPDATE, and DELETE performance?
from django.db import models

class IndexModel35(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_35'),
            models.Index(fields=['code'], name='valid_code_idx_35', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 11: How do you identify missing indexes in a production database?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How do you identify missing indexes in a production database?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How do you identify missing indexes in a production database?
from django.db import models

class IndexModel36(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_36'),
            models.Index(fields=['code'], name='valid_code_idx_36', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 12: How does Django compile functional index expressions to SQL?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How does Django compile functional index expressions to SQL?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How does Django compile functional index expressions to SQL?
from django.db import models

class IndexModel37(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_37'),
            models.Index(fields=['code'], name='valid_code_idx_37', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 13: What are the indexing strategies for JSONFields in PostgreSQL (GIN vs. B-Tree)?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What are the indexing strategies for JSONFields in PostgreSQL (GIN vs. B-Tree)?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What are the indexing strategies for JSONFields in PostgreSQL (GIN vs. B-Tree)?
from django.db import models

class IndexModel38(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_38'),
            models.Index(fields=['code'], name='valid_code_idx_38', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 14: How does indexing affect foreign key lookups and cascading deletes?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How does indexing affect foreign key lookups and cascading deletes?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How does indexing affect foreign key lookups and cascading deletes?
from django.db import models

class IndexModel39(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_39'),
            models.Index(fields=['code'], name='valid_code_idx_39', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 15: What is the risk of having too many indexes on a table?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is the risk of having too many indexes on a table?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is the risk of having too many indexes on a table?
from django.db import models

class IndexModel40(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_40'),
            models.Index(fields=['code'], name='valid_code_idx_40', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 16: How does Django handle index renaming and deletion in migrations?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How does Django handle index renaming and deletion in migrations?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How does Django handle index renaming and deletion in migrations?
from django.db import models

class IndexModel41(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_41'),
            models.Index(fields=['code'], name='valid_code_idx_41', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 17: How do you create an index concurrently in PostgreSQL without locking the table?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How do you create an index concurrently in PostgreSQL without locking the table?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How do you create an index concurrently in PostgreSQL without locking the table?
from django.db import models

class IndexModel42(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_42'),
            models.Index(fields=['code'], name='valid_code_idx_42', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 18: What are covering indexes (indexes with INCLUDE columns) and does Django support them?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What are covering indexes (indexes with INCLUDE columns) and does Django support them?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What are covering indexes (indexes with INCLUDE columns) and does Django support them?
from django.db import models

class IndexModel43(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_43'),
            models.Index(fields=['code'], name='valid_code_idx_43', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 19: How do you implement text search indexes (e.g., GinIndex, GiSTIndex) in Django?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How do you implement text search indexes (e.g., GinIndex, GiSTIndex) in Django?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How do you implement text search indexes (e.g., GinIndex, GiSTIndex) in Django?
from django.db import models

class IndexModel44(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_44'),
            models.Index(fields=['code'], name='valid_code_idx_44', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 20: How does query optimizer use indexes when executing ORM queries?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How does query optimizer use indexes when executing ORM queries?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How does query optimizer use indexes when executing ORM queries?
from django.db import models

class IndexModel45(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_45'),
            models.Index(fields=['code'], name='valid_code_idx_45', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 21: What is the performance difference between a clustered index and a non-clustered index?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is the performance difference between a clustered index and a non-clustered index?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is the performance difference between a clustered index and a non-clustered index?
from django.db import models

class IndexModel46(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_46'),
            models.Index(fields=['code'], name='valid_code_idx_46', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 22: How do you enforce database-level validation using CheckConstraint?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How do you enforce database-level validation using CheckConstraint?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How do you enforce database-level validation using CheckConstraint?
from django.db import models

class IndexModel47(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_47'),
            models.Index(fields=['code'], name='valid_code_idx_47', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 23: What is the index usage difference between LIKE queries and exact matches?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'What is the index usage difference between LIKE queries and exact matches?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for What is the index usage difference between LIKE queries and exact matches?
from django.db import models

class IndexModel48(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_48'),
            models.Index(fields=['code'], name='valid_code_idx_48', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 24: How do you inspect if a Django index is being used by the database?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How do you inspect if a Django index is being used by the database?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How do you inspect if a Django index is being used by the database?
from django.db import models

class IndexModel49(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_49'),
            models.Index(fields=['code'], name='valid_code_idx_49', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

# Question 25: How do you add database indexes on a through table in a ManyToMany relationship?

## Answer

This covers database-level indexing, indexing types, and unique constraints for: 'How do you add database indexes on a through table in a ManyToMany relationship?'. Indexes guide the database engine to target data directly.

## Practical Example

```python
# Unique Example for How do you add database indexes on a through table in a ManyToMany relationship?
from django.db import models

class IndexModel50(models.Model):
    code = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['code'], name='code_idx_50'),
            models.Index(fields=['code'], name='valid_code_idx_50', condition=models.Q(is_valid=True))
        ]
```

## Production Considerations

Always create indexes concurrently on production systems using raw database tools or specialized migration runners to prevent table lock outages.

## Performance Impact

Speeds up query reads from O(N) scans to O(log N) index lookups, but slows down bulk writes.

## Common Mistakes

Adding indexes to fields with low cardinality (e.g. status) where sequential scans are preferred by query planners.

## Interview Follow-up Questions

1. What is the difference between BTree indexes and GIN indexes in JSONField searches?
2. How does a Composite Index column sorting rule affect lookup queries?
3. Explain functional indexes implementation in Django.

---

