# Module 19: Production Issues & Debugging

This file contains structured interview questions and detailed answers targeting Django ORM concepts at Senior, Lead, and Architect levels.

---

# Question 1: How do you identify slow Django ORM queries in a production PostgreSQL environment?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you identify slow Django ORM queries in a production PostgreSQL environment?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 2: How do you detect memory leaks caused by Django QuerySets in long-running Celery processes?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you detect memory leaks caused by Django QuerySets in long-running Celery processes?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 3: How do you handle django.db.utils.InterfaceError: connection already closed in production?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you handle django.db.utils.InterfaceError: connection already closed in production?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 4: What causes OperationalError: database is locked in SQLite and how do you resolve it?

## Answer

Concurrency conflicts arise when multiple requests attempt to read and write the same database record simultaneously. Django provides: 1) Optimistic locking (verifying record version on update using F expressions or version checks), 2) Pessimistic locking (locking rows using `select_for_update()`). Pessimistic locks prevent other queries from modifying or reading locked rows depending on lock parameters.

## Practical Example

```python
# Pessimistic locking: locks the row until the transaction commits
with transaction.atomic():
    account = Account.objects.select_for_update().get(id=1)
    account.balance -= amount
    account.save()
```

## Production Considerations

Using `select_for_update()` without a timeout or parameters like `nowait=True` or `skip_locked=True` can lead to application workers hanging and waiting indefinitely for locks, causing cascading timeouts.

## Performance Impact

Guarantees data consistency at the cost of concurrency. `skip_locked=True` improves performance when designing queue consumers by letting workers skip busy rows.

## Common Mistakes

Using `select_for_update()` outside of a transaction block. In Django, this raises a TransactionManagementError because locks require an open transaction boundary.

## Interview Follow-up Questions

1. What is the difference between nowait=True and skip_locked=True?
2. How does select_for_update work with related models via the 'of' argument?
3. How do you write a test for optimistic lock conflicts?

---

# Question 5: How do you debug 'Too many connections' issues on MySQL/PostgreSQL with Django?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you debug 'Too many connections' issues on MySQL/PostgreSQL with Django?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 6: How do you track down which line of code generated a specific slow query?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you track down which line of code generated a specific slow query?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 7: How do you monitor database connection pool utilization in Django?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you monitor database connection pool utilization in Django?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 8: How do you handle database connection timeouts and reconnects?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you handle database connection timeouts and reconnects?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 9: How do you debug data consistency issues caused by race conditions in production?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you debug data consistency issues caused by race conditions in production?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 10: How do you handle large transaction log (WAL) generation caused by bulk ORM operations?

## Answer

Django manages database transactions using `transaction.atomic()`. When entering an atomic block, Django opens a transaction (or creates a savepoint if nested). If the block executes successfully, the changes are committed. If an exception is raised, the changes are rolled back. Internally, Django wraps connection operations with autocommit controls to enforce transaction limits.

## Practical Example

```python
from django.db import transaction

try:
    with transaction.atomic():
        user.save()
        profile.save()
        # If either fails, both roll back
except DatabaseError:
        # Handle rollback recovery
```

## Production Considerations

Keep atomic blocks as short as possible. Performing external API requests or slow operations inside atomic blocks holds database locks open longer, starving connection pools.

## Performance Impact

Groups multiple writes into a single commit, reducing IO overhead. However, long-running transactions increase table and row locking times.

## Common Mistakes

Catching database exceptions inside an atomic block without letting the block fail, which raises a `TransactionManagementError` on subsequent database writes because the transaction is marked as broken.

## Interview Follow-up Questions

1. How does transaction.on_commit() ensure safety for side effects?
2. What are transaction savepoints and how do nested atomic blocks use them?
3. How do database isolation levels affect transaction conflicts in Django?

---

# Question 11: How do you recover from a failed database migration that left the database in a half-migrated state?

## Answer

Migrating a multi-terabyte table with zero downtime requires a multi-phase write-and-sync strategy. Running a standard Django migration with a DDL change (e.g., adding a column with a default value or changing a data type) will lock the table, causing a production outage. The architecture pattern is: 1) Add the new column as nullable without a default value (light DDL lock), 2) Update code to write to both old and new columns, 3) Run a background data migration to backfill historical data in small batches, 4) Add default constraints and make the column non-nullable (if required) using separate lock-safe migrations, 5) Clean up and deploy code referencing only the new column.

## Practical Example

```python
# Inside a custom data migration using batch processing:
def backfill_data(apps, schema_editor):
    UserActivity = apps.get_model('analytics', 'UserActivity')
    batch_size = 5000
    last_id = 0
    while True:
        # Keyset pagination to prevent memory bloat and slow offsets
        batch = UserActivity.objects.filter(id__gt=last_id).order_by('id')[:batch_size]
        if not batch.exists():
            break
        for item in batch:
            item.new_field = transform(item.old_field)
        # Perform bulk update for this batch
        UserActivity.objects.bulk_update(batch, ['new_field'])
        last_id = batch[len(batch)-1].id
```

## Production Considerations

Always disable auto-commit and run background backfills in separate transactions to avoid holding locks. Use rate limiters to sleep between batches to allow replica replication and prevent replica lag.

## Performance Impact

Prevents long-running locks on the table, maintaining application response times during schema and data migrations.

## Common Mistakes

Running a single large migration query like `UPDATE my_table SET new_col = old_col` on a 2TB table, which will lock the table, blow up the transaction log (WAL), and crash the database.

## Interview Follow-up Questions

1. How do you use PostgreSQL's VACUUM or pg_repack after migrating data?
2. How do you write a Django migration that runs raw SQL concurrently?
3. What is the role of django_migrations table during zero-downtime deployment?

---

# Question 12: How do you debug slow prefetch_related queries when prefetching large datasets?

## Answer

The N+1 query problem occurs when the application executes one query to fetch parent records and then N additional queries to fetch related children records. To eliminate this, Django provides `select_related` (which performs a SQL JOIN for single-valued relationships like ForeignKey or OneToOneField) and `prefetch_related` (which performs a separate SQL query with an `IN` clause to fetch multi-valued relations like ManyToManyField or reverse ForeignKeys, then joins them in Python memory).

## Practical Example

```python
# Optimized: select_related performs a single SQL JOIN
books = Book.objects.select_related('author').filter(in_print=True)
for book in books:
    print(book.author.name)  # No additional DB query

# Optimized: prefetch_related executes exactly 2 queries
authors = Author.objects.prefetch_related('books').all()
for author in authors:
    print(author.books.all())  # Read from Python memory cache
```

## Production Considerations

In microservice environments or high-throughput systems, prefetching can consume considerable application memory if the fetched dataset is large. Always limit fields retrieved using `.only()` or `.defer()` when prefetching massive tables.

## Performance Impact

Changes database complexity from O(N) queries to O(1) or O(K) where K is the number of prefetched relationships. This reduces latency significantly.

## Common Mistakes

Using `prefetch_related` and then applying filters on the related manager inside a loop (e.g., `author.books.filter(genre='sci-fi')`), which completely bypasses the prefetch cache and triggers an additional SQL query.

## Interview Follow-up Questions

1. How does Django's Prefetch object allow filtering of prefetched querysets?
2. What is the difference in SQL structure between select_related and prefetch_related?
3. How do you clear or reset the prefetch cache of a model instance?

---

# Question 13: What is the production impact of missing foreign key indexes in Django?

## Answer

Indexes speed up data retrieval by providing quick lookups at the expense of write latency and disk space. Django supports defining standard indexes, partial indexes (with conditions), composite indexes (spanning multiple fields), and functional indexes (using database expressions/functions) in the model Meta options.

## Practical Example

```python
# Functional and Partial Index in model Meta:
class Meta:
    indexes = [
        models.Index(
            fields=['last_name', 'first_name'],
            name='author_name_idx'
        ),
        models.Index(
            OpClass(Lower('email'), name='varchar_pattern_ops'),
            name='author_email_lower_idx'
        ),
    ]
```

## Production Considerations

Always create indexes concurrently in production using custom SQL or database migration wrappers to prevent locking the table for writes during index creation.

## Performance Impact

Changes lookups from O(N) sequential scan to O(log N) index seek. However, too many indexes slow down INSERT/UPDATE writes.

## Common Mistakes

Indexing columns with low cardinality (e.g., booleans like `is_active`), where the database optimizer will ignore the index and perform a full table scan anyway.

## Interview Follow-up Questions

1. What is the difference between unique_together and UniqueConstraint?
2. How do you index a JSONField key in Django for PostgreSQL?
3. When should you use a composite index over multiple single-field indexes?

---

# Question 14: How do you debug slow aggregation queries on tables with millions of rows?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you debug slow aggregation queries on tables with millions of rows?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 15: How do you resolve N+1 queries in Django admin panels?

## Answer

The N+1 query problem occurs when the application executes one query to fetch parent records and then N additional queries to fetch related children records. To eliminate this, Django provides `select_related` (which performs a SQL JOIN for single-valued relationships like ForeignKey or OneToOneField) and `prefetch_related` (which performs a separate SQL query with an `IN` clause to fetch multi-valued relations like ManyToManyField or reverse ForeignKeys, then joins them in Python memory).

## Practical Example

```python
# Optimized: select_related performs a single SQL JOIN
books = Book.objects.select_related('author').filter(in_print=True)
for book in books:
    print(book.author.name)  # No additional DB query

# Optimized: prefetch_related executes exactly 2 queries
authors = Author.objects.prefetch_related('books').all()
for author in authors:
    print(author.books.all())  # Read from Python memory cache
```

## Production Considerations

In microservice environments or high-throughput systems, prefetching can consume considerable application memory if the fetched dataset is large. Always limit fields retrieved using `.only()` or `.defer()` when prefetching massive tables.

## Performance Impact

Changes database complexity from O(N) queries to O(1) or O(K) where K is the number of prefetched relationships. This reduces latency significantly.

## Common Mistakes

Using `prefetch_related` and then applying filters on the related manager inside a loop (e.g., `author.books.filter(genre='sci-fi')`), which completely bypasses the prefetch cache and triggers an additional SQL query.

## Interview Follow-up Questions

1. How does Django's Prefetch object allow filtering of prefetched querysets?
2. What is the difference in SQL structure between select_related and prefetch_related?
3. How do you clear or reset the prefetch cache of a model instance?

---

# Question 16: What causes high CPU usage on the database server from Django's count() queries?

## Answer

This concept covers advanced database configurations and behaviors for: 'What causes high CPU usage on the database server from Django's count() queries?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 17: How do you handle timezone mismatch issues between Django settings and PostgreSQL?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you handle timezone mismatch issues between Django settings and PostgreSQL?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 18: How do you debug database deadlock errors in production logs?

## Answer

Concurrency conflicts arise when multiple requests attempt to read and write the same database record simultaneously. Django provides: 1) Optimistic locking (verifying record version on update using F expressions or version checks), 2) Pessimistic locking (locking rows using `select_for_update()`). Pessimistic locks prevent other queries from modifying or reading locked rows depending on lock parameters.

## Practical Example

```python
# Pessimistic locking: locks the row until the transaction commits
with transaction.atomic():
    account = Account.objects.select_for_update().get(id=1)
    account.balance -= amount
    account.save()
```

## Production Considerations

Using `select_for_update()` without a timeout or parameters like `nowait=True` or `skip_locked=True` can lead to application workers hanging and waiting indefinitely for locks, causing cascading timeouts.

## Performance Impact

Guarantees data consistency at the cost of concurrency. `skip_locked=True` improves performance when designing queue consumers by letting workers skip busy rows.

## Common Mistakes

Using `select_for_update()` outside of a transaction block. In Django, this raises a TransactionManagementError because locks require an open transaction boundary.

## Interview Follow-up Questions

1. What is the difference between nowait=True and skip_locked=True?
2. How does select_for_update work with related models via the 'of' argument?
3. How do you write a test for optimistic lock conflicts?

---

# Question 19: What are the risks of using Django's select_for_update() with a short timeout?

## Answer

Concurrency conflicts arise when multiple requests attempt to read and write the same database record simultaneously. Django provides: 1) Optimistic locking (verifying record version on update using F expressions or version checks), 2) Pessimistic locking (locking rows using `select_for_update()`). Pessimistic locks prevent other queries from modifying or reading locked rows depending on lock parameters.

## Practical Example

```python
# Pessimistic locking: locks the row until the transaction commits
with transaction.atomic():
    account = Account.objects.select_for_update().get(id=1)
    account.balance -= amount
    account.save()
```

## Production Considerations

Using `select_for_update()` without a timeout or parameters like `nowait=True` or `skip_locked=True` can lead to application workers hanging and waiting indefinitely for locks, causing cascading timeouts.

## Performance Impact

Guarantees data consistency at the cost of concurrency. `skip_locked=True` improves performance when designing queue consumers by letting workers skip busy rows.

## Common Mistakes

Using `select_for_update()` outside of a transaction block. In Django, this raises a TransactionManagementError because locks require an open transaction boundary.

## Interview Follow-up Questions

1. What is the difference between nowait=True and skip_locked=True?
2. How does select_for_update work with related models via the 'of' argument?
3. How do you write a test for optimistic lock conflicts?

---

# Question 20: How do you debug issues with Django's database routing in production replica lag?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you debug issues with Django's database routing in production replica lag?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 21: How do you identify index bloat on production PostgreSQL tables managed by Django?

## Answer

Indexes speed up data retrieval by providing quick lookups at the expense of write latency and disk space. Django supports defining standard indexes, partial indexes (with conditions), composite indexes (spanning multiple fields), and functional indexes (using database expressions/functions) in the model Meta options.

## Practical Example

```python
# Functional and Partial Index in model Meta:
class Meta:
    indexes = [
        models.Index(
            fields=['last_name', 'first_name'],
            name='author_name_idx'
        ),
        models.Index(
            OpClass(Lower('email'), name='varchar_pattern_ops'),
            name='author_email_lower_idx'
        ),
    ]
```

## Production Considerations

Always create indexes concurrently in production using custom SQL or database migration wrappers to prevent locking the table for writes during index creation.

## Performance Impact

Changes lookups from O(N) sequential scan to O(log N) index seek. However, too many indexes slow down INSERT/UPDATE writes.

## Common Mistakes

Indexing columns with low cardinality (e.g., booleans like `is_active`), where the database optimizer will ignore the index and perform a full table scan anyway.

## Interview Follow-up Questions

1. What is the difference between unique_together and UniqueConstraint?
2. How do you index a JSONField key in Django for PostgreSQL?
3. When should you use a composite index over multiple single-field indexes?

---

# Question 22: How do you debug serialization failure errors in PostgreSQL repeatable read transactions?

## Answer

Django manages database transactions using `transaction.atomic()`. When entering an atomic block, Django opens a transaction (or creates a savepoint if nested). If the block executes successfully, the changes are committed. If an exception is raised, the changes are rolled back. Internally, Django wraps connection operations with autocommit controls to enforce transaction limits.

## Practical Example

```python
from django.db import transaction

try:
    with transaction.atomic():
        user.save()
        profile.save()
        # If either fails, both roll back
except DatabaseError:
        # Handle rollback recovery
```

## Production Considerations

Keep atomic blocks as short as possible. Performing external API requests or slow operations inside atomic blocks holds database locks open longer, starving connection pools.

## Performance Impact

Groups multiple writes into a single commit, reducing IO overhead. However, long-running transactions increase table and row locking times.

## Common Mistakes

Catching database exceptions inside an atomic block without letting the block fail, which raises a `TransactionManagementError` on subsequent database writes because the transaction is marked as broken.

## Interview Follow-up Questions

1. How does transaction.on_commit() ensure safety for side effects?
2. What are transaction savepoints and how do nested atomic blocks use them?
3. How do database isolation levels affect transaction conflicts in Django?

---

# Question 23: How do you profile memory consumption of Django model instances?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you profile memory consumption of Django model instances?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 24: What is the production impact of django.db.connection.queries in DEBUG=True mode?

## Answer

This concept covers advanced database configurations and behaviors for: 'What is the production impact of django.db.connection.queries in DEBUG=True mode?'. It deals with persistence rules, validation, and integration with the backend engine.

## Practical Example

```python
# Standard advanced configuration pattern
from django.db import models

class AuditModel(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Production Considerations

Always verify the database schema constraints generated in migrations. Ensure validation rules match at both application and database level to prevent corrupt data.

## Performance Impact

Minimizes application latency by reducing database roundtrips, utilizing query caching, and avoiding heavy table scans.

## Common Mistakes

Hardcoding configurations or bypassing standard ORM abstraction levels, which breaks database driver portability.

## Interview Follow-up Questions

1. How does this feature behave under high concurrent write load?
2. How do you write a Django unit test to validate this behavior?
3. What is the migration rollback strategy for this configuration?

---

# Question 25: How do you troubleshoot slow migrations on tables with 100M+ rows?

## Answer

Migrating a multi-terabyte table with zero downtime requires a multi-phase write-and-sync strategy. Running a standard Django migration with a DDL change (e.g., adding a column with a default value or changing a data type) will lock the table, causing a production outage. The architecture pattern is: 1) Add the new column as nullable without a default value (light DDL lock), 2) Update code to write to both old and new columns, 3) Run a background data migration to backfill historical data in small batches, 4) Add default constraints and make the column non-nullable (if required) using separate lock-safe migrations, 5) Clean up and deploy code referencing only the new column.

## Practical Example

```python
# Inside a custom data migration using batch processing:
def backfill_data(apps, schema_editor):
    UserActivity = apps.get_model('analytics', 'UserActivity')
    batch_size = 5000
    last_id = 0
    while True:
        # Keyset pagination to prevent memory bloat and slow offsets
        batch = UserActivity.objects.filter(id__gt=last_id).order_by('id')[:batch_size]
        if not batch.exists():
            break
        for item in batch:
            item.new_field = transform(item.old_field)
        # Perform bulk update for this batch
        UserActivity.objects.bulk_update(batch, ['new_field'])
        last_id = batch[len(batch)-1].id
```

## Production Considerations

Always disable auto-commit and run background backfills in separate transactions to avoid holding locks. Use rate limiters to sleep between batches to allow replica replication and prevent replica lag.

## Performance Impact

Prevents long-running locks on the table, maintaining application response times during schema and data migrations.

## Common Mistakes

Running a single large migration query like `UPDATE my_table SET new_col = old_col` on a 2TB table, which will lock the table, blow up the transaction log (WAL), and crash the database.

## Interview Follow-up Questions

1. How do you use PostgreSQL's VACUUM or pg_repack after migrating data?
2. How do you write a Django migration that runs raw SQL concurrently?
3. What is the role of django_migrations table during zero-downtime deployment?

---

