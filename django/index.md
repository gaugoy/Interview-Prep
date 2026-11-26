# 🐍 Django Interview Preparation Guide

> A comprehensive, indexed reference for Django technical interviews — covering Core Django, ORM, and Django REST Framework.

---

## 📚 Table of Contents

| # | Section | Topics Covered | Questions |
|---|---------|---------------|-----------|
| 01 | [Django Core Concepts](./01_Django_Core.md) | MVT, URLs, Views, Templates, Forms, Auth, Middleware, Signals, Admin, Security, Lifecycle | 20 |
| 02 | [Django ORM](./02_Django_ORM.md) | Models, QuerySets, Relationships, Aggregation, Optimization, Transactions, Migrations | 18 |
| 03 | [Django REST Framework](./03_DRF.md) | Serializers, ViewSets, Auth/JWT, Permissions, Throttling, Pagination, Testing | 18 |

**Total: 56 questions with detailed answers and code examples**

> **Going deeper:** the Senior/Lead-level ORM set lives in [`../Django ORM/`](../Django%20ORM/README.md) (704 questions). Its [06 Query Optimization](../Django%20ORM/06_Query_Optimization.md) module has been rewritten to the interview-ready standard (spoken answer → mechanism → STAR story → trade-offs → wrong answers → follow-ups) and is the best follow-up to ORM Q7, Q8, Q16 and Q18 below.

---

## 🎯 Top 20 Most Asked Questions

Weighted for a ~7-year Senior Backend / Full-Stack (Django + DRF) interview: ORM performance, transactions and DRF design come up in almost every loop. Stars are each question's own frequency rating.

| # | Priority | Question | Section |
|---|----------|---------|---------|
| 1 | ⭐⭐⭐ | [select_related and prefetch_related](./02_Django_ORM.md#q7) | ORM |
| 2 | ⭐⭐⭐ | [The N+1 Query Problem](./02_Django_ORM.md#q8) | ORM |
| 3 | ⭐⭐⭐ | [Django Request/Response Lifecycle](./01_Django_Core.md#q20) | Core |
| 4 | ⭐⭐⭐ | [Explain Django's MVT Architecture](./01_Django_Core.md#q1) | Core |
| 5 | ⭐⭐⭐ | [Database Transactions](./02_Django_ORM.md#q10) | ORM |
| 6 | ⭐⭐⭐ | [Serializers and ModelSerializer](./03_DRF.md#q2) | DRF |
| 7 | ⭐⭐⭐ | [APIView vs GenericAPIView vs ViewSet](./03_DRF.md#q5) | DRF |
| 8 | ⭐⭐⭐ | [Django Middleware](./01_Django_Core.md#q5) | Core |
| 9 | ⭐⭐⭐ | [F Expressions and Atomic Updates](./02_Django_ORM.md#q14) | ORM |
| 10 | ⭐⭐⭐ | [Aggregation and Annotation](./02_Django_ORM.md#q6) | ORM |
| 11 | ⭐⭐⭐ | [Django Signals](./01_Django_Core.md#q6) | Core |
| 12 | ⭐⭐⭐ | [Q Objects — Complex Queries](./02_Django_ORM.md#q5) | ORM |
| 13 | ⭐⭐⭐ | [Django Migrations](./02_Django_ORM.md#q12) | ORM |
| 14 | ⭐⭐⭐ | [Custom Model Managers and QuerySets](./02_Django_ORM.md#q11) | ORM |
| 15 | ⭐⭐⭐ | [Permissions and Custom Permission Classes](./03_DRF.md#q9) | DRF |
| 16 | ⭐⭐⭐ | [JWT Authentication](./03_DRF.md#q8) | DRF |
| 17 | ⭐⭐⭐ | [Django Authentication System](./01_Django_Core.md#q9) | Core |
| 18 | ⭐⭐⭐ | [Nested Serializers and Writable Relations](./03_DRF.md#q3) | DRF |
| 19 | ⭐⭐⭐ | [Django Security Best Practices](./01_Django_Core.md#q16) | Core |
| 20 | ⭐⭐ | [Django Caching](./01_Django_Core.md#q12) | Core |

---

## ⏱️ 1-Hour Interview Time Allocation

```
Django Core (20 min)
├── MVT + URL routing (5 min)
├── Views + Templates (5 min)
├── Auth + Middleware + Signals (5 min)
└── Admin + Security (5 min)

Django ORM (20 min)
├── Models + Relationships (5 min)
├── QuerySet API + Filtering (5 min)
├── Optimization (select/prefetch_related) (5 min)
└── Migrations + Transactions (5 min)

Django REST Framework (20 min)
├── Serializers (5 min)
├── Views + ViewSets (5 min)
├── Auth + Permissions (5 min)
└── Pagination + Testing (5 min)
```

---

## 🚀 Quick Reference Cheatsheet

### Django Request Lifecycle
```
Browser Request
    ↓
WSGI/ASGI Server (Gunicorn/Uvicorn)
    ↓
Django Middleware (process_request)
    ↓
URL Resolver → View Function/Class
    ↓
View → ORM → Database
    ↓
View → Template Rendering
    ↓
Django Middleware (process_response)
    ↓
HTTP Response → Browser
```

### Key Django Commands
```bash
django-admin startproject myproject
python manage.py startapp myapp
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
python manage.py collectstatic
python manage.py runserver
python manage.py test
```

### ORM Quick Reference
```python
# Basic CRUD
Model.objects.all()
Model.objects.get(pk=1)
Model.objects.filter(field=value)
Model.objects.create(field=value)
Model.objects.update(field=value)
Model.objects.delete()

# Optimization
Model.objects.select_related('fk_field')
Model.objects.prefetch_related('m2m_field')
Model.objects.only('field1', 'field2')
Model.objects.defer('large_field')

# Aggregation
from django.db.models import Count, Sum, Avg, Max, Min
Model.objects.aggregate(total=Count('id'))
Model.objects.annotate(count=Count('related'))
```

---

## 📖 How to Use This Guide

1. **Start with `index.md`** — get the big picture and priority questions
2. **Read each section file** — questions are ordered easy → hard
3. **Practice code examples** — type them out, don't just read
4. **Focus on ⭐⭐⭐ questions** — highest interview frequency
5. **Review follow-up questions** — interviewers often dig deeper

---

*Navigate to any section using the links in the Table of Contents above.*
