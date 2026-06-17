# Module 19: Production Issues & Debugging

This file contains structured interview questions and detailed answers targeting Django ORM concepts at Senior, Lead, and Architect levels.

---

# Question 1: How do you identify slow Django ORM queries in a production PostgreSQL environment?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you identify slow Django ORM queries in a production PostgreSQL environment?'.

## Practical Example

```python
# Unique Example for How do you identify slow Django ORM queries in a production PostgreSQL environment?
from django.db import models

class ProdIssueModel76(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 2: How do you detect memory leaks caused by Django QuerySets in long-running Celery processes?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you detect memory leaks caused by Django QuerySets in long-running Celery processes?'.

## Practical Example

```python
# Unique Example for How do you detect memory leaks caused by Django QuerySets in long-running Celery processes?
from django.db import models

class ProdIssueModel77(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 3: How do you handle django.db.utils.InterfaceError: connection already closed in production?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you handle django.db.utils.InterfaceError: connection already closed in production?'.

## Practical Example

```python
# Unique Example for How do you handle django.db.utils.InterfaceError: connection already closed in production?
from django.db import models

class ProdIssueModel78(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 4: What causes OperationalError: database is locked in SQLite and how do you resolve it?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'What causes OperationalError: database is locked in SQLite and how do you resolve it?'.

## Practical Example

```python
# Unique Example for What causes OperationalError: database is locked in SQLite and how do you resolve it?
from django.db import models

class ProdIssueModel79(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 5: How do you debug 'Too many connections' issues on MySQL/PostgreSQL with Django?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you debug 'Too many connections' issues on MySQL/PostgreSQL with Django?'.

## Practical Example

```python
# Unique Example for How do you debug 'Too many connections' issues on MySQL/PostgreSQL with Django?
from django.db import models

class ProdIssueModel80(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 6: How do you track down which line of code generated a specific slow query?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you track down which line of code generated a specific slow query?'.

## Practical Example

```python
# Unique Example for How do you track down which line of code generated a specific slow query?
from django.db import models

class ProdIssueModel81(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 7: How do you monitor database connection pool utilization in Django?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you monitor database connection pool utilization in Django?'.

## Practical Example

```python
# Unique Example for How do you monitor database connection pool utilization in Django?
from django.db import models

class ProdIssueModel82(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 8: How do you handle database connection timeouts and reconnects?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you handle database connection timeouts and reconnects?'.

## Practical Example

```python
# Unique Example for How do you handle database connection timeouts and reconnects?
from django.db import models

class ProdIssueModel83(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 9: How do you debug data consistency issues caused by race conditions in production?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you debug data consistency issues caused by race conditions in production?'.

## Practical Example

```python
# Unique Example for How do you debug data consistency issues caused by race conditions in production?
from django.db import models

class ProdIssueModel84(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 10: How do you handle large transaction log (WAL) generation caused by bulk ORM operations?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you handle large transaction log (WAL) generation caused by bulk ORM operations?'.

## Practical Example

```python
# Unique Example for How do you handle large transaction log (WAL) generation caused by bulk ORM operations?
from django.db import models

class ProdIssueModel85(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 11: How do you recover from a failed database migration that left the database in a half-migrated state?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you recover from a failed database migration that left the database in a half-migrated state?'.

## Practical Example

```python
# Unique Example for How do you recover from a failed database migration that left the database in a half-migrated state?
from django.db import models

class ProdIssueModel86(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 12: How do you debug slow prefetch_related queries when prefetching large datasets?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you debug slow prefetch_related queries when prefetching large datasets?'.

## Practical Example

```python
# Unique Example for How do you debug slow prefetch_related queries when prefetching large datasets?
from django.db import models

class ProdIssueModel87(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 13: What is the production impact of missing foreign key indexes in Django?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'What is the production impact of missing foreign key indexes in Django?'.

## Practical Example

```python
# Unique Example for What is the production impact of missing foreign key indexes in Django?
from django.db import models

class ProdIssueModel88(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 14: How do you debug slow aggregation queries on tables with millions of rows?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you debug slow aggregation queries on tables with millions of rows?'.

## Practical Example

```python
# Unique Example for How do you debug slow aggregation queries on tables with millions of rows?
from django.db import models

class ProdIssueModel89(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 15: How do you resolve N+1 queries in Django admin panels?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you resolve N+1 queries in Django admin panels?'.

## Practical Example

```python
# Unique Example for How do you resolve N+1 queries in Django admin panels?
from django.db import models

class ProdIssueModel90(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 16: What causes high CPU usage on the database server from Django's count() queries?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'What causes high CPU usage on the database server from Django's count() queries?'.

## Practical Example

```python
# Unique Example for What causes high CPU usage on the database server from Django's count() queries?
from django.db import models

class ProdIssueModel91(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 17: How do you handle timezone mismatch issues between Django settings and PostgreSQL?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you handle timezone mismatch issues between Django settings and PostgreSQL?'.

## Practical Example

```python
# Unique Example for How do you handle timezone mismatch issues between Django settings and PostgreSQL?
from django.db import models

class ProdIssueModel92(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 18: How do you debug database deadlock errors in production logs?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you debug database deadlock errors in production logs?'.

## Practical Example

```python
# Unique Example for How do you debug database deadlock errors in production logs?
from django.db import models

class ProdIssueModel93(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 19: What are the risks of using Django's select_for_update() with a short timeout?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'What are the risks of using Django's select_for_update() with a short timeout?'.

## Practical Example

```python
# Unique Example for What are the risks of using Django's select_for_update() with a short timeout?
from django.db import models

class ProdIssueModel94(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 20: How do you debug issues with Django's database routing in production replica lag?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you debug issues with Django's database routing in production replica lag?'.

## Practical Example

```python
# Unique Example for How do you debug issues with Django's database routing in production replica lag?
from django.db import models

class ProdIssueModel95(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 21: How do you identify index bloat on production PostgreSQL tables managed by Django?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you identify index bloat on production PostgreSQL tables managed by Django?'.

## Practical Example

```python
# Unique Example for How do you identify index bloat on production PostgreSQL tables managed by Django?
from django.db import models

class ProdIssueModel96(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 22: How do you debug serialization failure errors in PostgreSQL repeatable read transactions?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you debug serialization failure errors in PostgreSQL repeatable read transactions?'.

## Practical Example

```python
# Unique Example for How do you debug serialization failure errors in PostgreSQL repeatable read transactions?
from django.db import models

class ProdIssueModel97(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 23: How do you profile memory consumption of Django model instances?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you profile memory consumption of Django model instances?'.

## Practical Example

```python
# Unique Example for How do you profile memory consumption of Django model instances?
from django.db import models

class ProdIssueModel98(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 24: What is the production impact of django.db.connection.queries in DEBUG=True mode?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'What is the production impact of django.db.connection.queries in DEBUG=True mode?'.

## Practical Example

```python
# Unique Example for What is the production impact of django.db.connection.queries in DEBUG=True mode?
from django.db import models

class ProdIssueModel99(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

# Question 25: How do you troubleshoot slow migrations on tables with 100M+ rows?

## Answer

This covers troubleshooting production bugs, deadlocks, connection leaks, and query profiling for: 'How do you troubleshoot slow migrations on tables with 100M+ rows?'.

## Practical Example

```python
# Unique Example for How do you troubleshoot slow migrations on tables with 100M+ rows?
from django.db import models

class ProdIssueModel100(models.Model):
    data = models.CharField(max_length=100)

# Profiling wrapper:
# import logging; logger = logging.getLogger('django.db.backends')
```

## Production Considerations

Install APM tools like Datadog or OpenTelemetry to capture trace parameters for database queries in production.

## Performance Impact

Logging connection counts and slow transaction executions alerts engineers before connection limits are reached.

## Common Mistakes

Enabling debug query logging (`connection.queries`) in production environments, leading to out-of-memory errors.

## Interview Follow-up Questions

1. How do you detect memory leaks caused by Django QuerySets in long-running processes?
2. How do you handle InterfaceError: connection already closed in production?
3. What are database deadlock resolution loops?

---

