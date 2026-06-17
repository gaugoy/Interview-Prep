# Module 13: Migrations & Schema Evolution

This file contains structured interview questions and detailed answers targeting Django ORM concepts at Senior, Lead, and Architect levels.

---

# Question 1: How does Django's migration engine detect model changes?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How does Django's migration engine detect model changes?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How does Django's migration engine detect model changes?
# Inside a migration file segment:
from django.db import migrations

def populate_default_51(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel51')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_51)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 2: What is the structure of a migration file and what is the role of dependencies?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What is the structure of a migration file and what is the role of dependencies?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What is the structure of a migration file and what is the role of dependencies?
# Inside a migration file segment:
from django.db import migrations

def populate_default_52(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel52')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_52)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 3: What is the difference between schema migrations and data migrations?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What is the difference between schema migrations and data migrations?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What is the difference between schema migrations and data migrations?
# Inside a migration file segment:
from django.db import migrations

def populate_default_53(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel53')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_53)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 4: How do you write a safe data migration that updates database rows?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you write a safe data migration that updates database rows?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you write a safe data migration that updates database rows?
# Inside a migration file segment:
from django.db import migrations

def populate_default_54(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel54')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_54)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 5: Why is it dangerous to import models directly inside a data migration, and how do you avoid it?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'Why is it dangerous to import models directly inside a data migration, and how do you avoid it?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for Why is it dangerous to import models directly inside a data migration, and how do you avoid it?
# Inside a migration file segment:
from django.db import migrations

def populate_default_55(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel55')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_55)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 6: How does Django run migrations transactionally and which databases support it?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How does Django run migrations transactionally and which databases support it?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How does Django run migrations transactionally and which databases support it?
# Inside a migration file segment:
from django.db import migrations

def populate_default_56(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel56')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_56)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 7: What is migration squashing and how do you do it safely in production?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What is migration squashing and how do you do it safely in production?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What is migration squashing and how do you do it safely in production?
# Inside a migration file segment:
from django.db import migrations

def populate_default_57(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel57')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_57)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 8: How do you resolve migration conflicts in a team environment?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you resolve migration conflicts in a team environment?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you resolve migration conflicts in a team environment?
# Inside a migration file segment:
from django.db import migrations

def populate_default_58(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel58')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_58)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 9: How does the migration history table (django_migrations) work under the hood?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How does the migration history table (django_migrations) work under the hood?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How does the migration history table (django_migrations) work under the hood?
# Inside a migration file segment:
from django.db import migrations

def populate_default_59(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel59')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_59)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 10: What are the strategies for migrating a large table (10M+ rows) with zero downtime?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What are the strategies for migrating a large table (10M+ rows) with zero downtime?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What are the strategies for migrating a large table (10M+ rows) with zero downtime?
# Inside a migration file segment:
from django.db import migrations

def populate_default_60(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel60')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_60)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 11: How do you add a non-nullable field to an existing table without breaking production?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you add a non-nullable field to an existing table without breaking production?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you add a non-nullable field to an existing table without breaking production?
# Inside a migration file segment:
from django.db import migrations

def populate_default_61(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel61')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_61)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 12: How do you rename a field in a model without causing downtime or query failures?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you rename a field in a model without causing downtime or query failures?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you rename a field in a model without causing downtime or query failures?
# Inside a migration file segment:
from django.db import migrations

def populate_default_62(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel62')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_62)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 13: How do you drop a column from a large database table safely in production?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you drop a column from a large database table safely in production?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you drop a column from a large database table safely in production?
# Inside a migration file segment:
from django.db import migrations

def populate_default_63(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel63')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_63)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 14: What is RunSQL and how do you use it to execute raw database migration scripts?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What is RunSQL and how do you use it to execute raw database migration scripts?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What is RunSQL and how do you use it to execute raw database migration scripts?
# Inside a migration file segment:
from django.db import migrations

def populate_default_64(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel64')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_64)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 15: What is RunPython and how does it access model history?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What is RunPython and how does it access model history?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What is RunPython and how does it access model history?
# Inside a migration file segment:
from django.db import migrations

def populate_default_65(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel65')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_65)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 16: How does Django handle migrations for unmanaged models (managed=False)?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How does Django handle migrations for unmanaged models (managed=False)?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How does Django handle migrations for unmanaged models (managed=False)?
# Inside a migration file segment:
from django.db import migrations

def populate_default_66(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel66')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_66)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 17: How do you run migrations across multiple databases using routers?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you run migrations across multiple databases using routers?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you run migrations across multiple databases using routers?
# Inside a migration file segment:
from django.db import migrations

def populate_default_67(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel67')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_67)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 18: What is the role of MIGRATION_MODULES setting in Django?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What is the role of MIGRATION_MODULES setting in Django?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What is the role of MIGRATION_MODULES setting in Django?
# Inside a migration file segment:
from django.db import migrations

def populate_default_68(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel68')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_68)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 19: How do you write a migration that creates a database view?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you write a migration that creates a database view?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you write a migration that creates a database view?
# Inside a migration file segment:
from django.db import migrations

def populate_default_69(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel69')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_69)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 20: How do you roll back a migration in Django?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you roll back a migration in Django?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you roll back a migration in Django?
# Inside a migration file segment:
from django.db import migrations

def populate_default_70(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel70')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_70)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 21: What are the risks of using python functions inside migration files?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What are the risks of using python functions inside migration files?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What are the risks of using python functions inside migration files?
# Inside a migration file segment:
from django.db import migrations

def populate_default_71(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel71')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_71)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 22: How do you dry-run migrations to check their SQL output?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you dry-run migrations to check their SQL output?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you dry-run migrations to check their SQL output?
# Inside a migration file segment:
from django.db import migrations

def populate_default_72(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel72')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_72)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 23: How does Django handle index creation in migrations for PostgreSQL vs. SQLite?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How does Django handle index creation in migrations for PostgreSQL vs. SQLite?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How does Django handle index creation in migrations for PostgreSQL vs. SQLite?
# Inside a migration file segment:
from django.db import migrations

def populate_default_73(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel73')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_73)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 24: What is the impact of long-running migrations on database locks?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'What is the impact of long-running migrations on database locks?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for What is the impact of long-running migrations on database locks?
# Inside a migration file segment:
from django.db import migrations

def populate_default_74(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel74')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_74)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

# Question 25: How do you test migrations to ensure they do not fail when deployed to staging?

## Answer

This covers migration engine behaviors, schema and data migrations, and rollback strategies for: 'How do you test migrations to ensure they do not fail when deployed to staging?'. Django tracks model states in migration files.

## Practical Example

```python
# Unique Example for How do you test migrations to ensure they do not fail when deployed to staging?
# Inside a migration file segment:
from django.db import migrations

def populate_default_75(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'IndexModel75')
    # Batch migration processing code

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(populate_default_75)
    ]
```

## Production Considerations

Never import models directly inside migration scripts. Use target apps.get_model() registry to load freeze states.

## Performance Impact

Data migrations on large tables should be executed in chunked transactions to avoid lock pile-ups.

## Common Mistakes

Combining DDL schema modifications and data processing migrations in a single file on non-transactional DDL databases.

## Interview Follow-up Questions

1. How do you squash migrations safely in active production branches?
2. What is the behavior of migration engine with unmanaged models?
3. How do you resolve schema discrepancies in git branches?

---

