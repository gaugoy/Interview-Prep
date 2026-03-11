# 🐍 Django Interview Preparation Guide

> A comprehensive, indexed reference for Django technical interviews — covering Core Django, ORM, and Django REST Framework.

---

## 📚 Table of Contents

| # | Section | Topics Covered | Questions |
|---|---------|---------------|-----------|
| 01 | [Django Core Concepts](./01_Django_Core.md) | MVT, URLs, Views, Templates, Forms, Auth, Middleware, Signals, Admin | 30 |
| 02 | [Django ORM](./02_Django_ORM.md) | Models, QuerySets, Relationships, Aggregation, Optimization, Migrations | 25 |
| 03 | [Django REST Framework](./03_DRF.md) | Serializers, ViewSets, Auth, Permissions, Pagination, Testing | 25 |

**Total: 80 questions with detailed answers and code examples**

---

## 🎯 Top 20 Most Asked Questions

| Priority | Question | Section |
|----------|---------|---------|
| ⭐⭐⭐ | Explain Django's MVT architecture | Core |
| ⭐⭐⭐ | What is the difference between `select_related` and `prefetch_related`? | ORM |
| ⭐⭐⭐ | How do serializers work in DRF? | DRF |
| ⭐⭐⭐ | What is the N+1 query problem and how do you fix it? | ORM |
| ⭐⭐⭐ | Difference between `APIView`, `GenericAPIView`, and `ViewSet`? | DRF |
| ⭐⭐⭐ | How does Django authentication work? | Core |
| ⭐⭐⭐ | What are Django signals? When would you use them? | Core |
| ⭐⭐⭐ | Explain Django middleware and write a custom one | Core |
| ⭐⭐⭐ | What is `Q` object? How do you do complex queries? | ORM |
| ⭐⭐⭐ | How do you implement JWT authentication in DRF? | DRF |
| ⭐⭐ | What are class-based views? Pros and cons vs FBVs? | Core |
| ⭐⭐ | How do Django migrations work? | ORM |
| ⭐⭐ | What is `annotate` vs `aggregate`? | ORM |
| ⭐⭐ | How do you write custom permissions in DRF? | DRF |
| ⭐⭐ | What is `prefetch_related` with `Prefetch` object? | ORM |
| ⭐⭐ | How does Django caching work? | Core |
| ⭐⭐ | What are custom model managers? | ORM |
| ⭐⭐ | How do you handle nested serializers? | DRF |
| ⭐⭐ | What is throttling in DRF? | DRF |
| ⭐⭐ | How do you optimize Django admin for large datasets? | Core |

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
