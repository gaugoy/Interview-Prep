# Module 13: Migrations & Schema Evolution

This file contains structured interview questions and detailed answers targeting Django ORM concepts at Senior, Lead, and Architect levels.

---

# Question 1: How does Django's migration engine detect model changes?

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

# Question 2: What is the structure of a migration file and what is the role of dependencies?

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

# Question 3: What is the difference between schema migrations and data migrations?

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

# Question 4: How do you write a safe data migration that updates database rows?

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

# Question 5: Why is it dangerous to import models directly inside a data migration, and how do you avoid it?

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

# Question 6: How does Django run migrations transactionally and which databases support it?

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

# Question 7: What is migration squashing and how do you do it safely in production?

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

# Question 8: How do you resolve migration conflicts in a team environment?

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

# Question 9: How does the migration history table (django_migrations) work under the hood?

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

# Question 10: What are the strategies for migrating a large table (10M+ rows) with zero downtime?

## Answer

This concept covers advanced database configurations and behaviors for: 'What are the strategies for migrating a large table (10M+ rows) with zero downtime?'. It deals with persistence rules, validation, and integration with the backend engine.

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

# Question 11: How do you add a non-nullable field to an existing table without breaking production?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you add a non-nullable field to an existing table without breaking production?'. It deals with persistence rules, validation, and integration with the backend engine.

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

# Question 12: How do you rename a field in a model without causing downtime or query failures?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you rename a field in a model without causing downtime or query failures?'. It deals with persistence rules, validation, and integration with the backend engine.

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

# Question 13: How do you drop a column from a large database table safely in production?

## Answer

This concept covers advanced database configurations and behaviors for: 'How do you drop a column from a large database table safely in production?'. It deals with persistence rules, validation, and integration with the backend engine.

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

# Question 14: What is RunSQL and how do you use it to execute raw database migration scripts?

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

# Question 15: What is RunPython and how does it access model history?

## Answer

This concept covers advanced database configurations and behaviors for: 'What is RunPython and how does it access model history?'. It deals with persistence rules, validation, and integration with the backend engine.

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

# Question 16: How does Django handle migrations for unmanaged models (managed=False)?

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

# Question 17: How do you run migrations across multiple databases using routers?

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

# Question 18: What is the role of MIGRATION_MODULES setting in Django?

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

# Question 19: How do you write a migration that creates a database view?

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

# Question 20: How do you roll back a migration in Django?

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

# Question 21: What are the risks of using python functions inside migration files?

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

# Question 22: How do you dry-run migrations to check their SQL output?

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

# Question 23: How does Django handle index creation in migrations for PostgreSQL vs. SQLite?

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

# Question 24: What is the impact of long-running migrations on database locks?

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

# Question 25: How do you test migrations to ensure they do not fail when deployed to staging?

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

