# Django ORM Senior & Lead Interview Preparation Repository

Welcome to the ultimate Django ORM Interview Preparation Repository. This guide is specifically curated for Senior, Lead, Staff, and Principal Engineers, as well as Database Architects. It covers deep database internals, optimization patterns, transaction management, migration strategies, and scalability design patterns using Django 5.0.

---

## 🗺️ Learning Path & Roadmaps

### 1. Senior Engineer Roadmap (Years 5-8)
Focuses on writing clean, optimized, and database-friendly queries, understanding model design trade-offs, and resolving common bottlenecks.
*   **Model Layer Design**: Abstract vs. Proxy models, Multi-table Inheritance performance.
*   **Query Optimization**: `select_related` vs. `prefetch_related`, QuerySet slicing, caching, and deferred fields (`only`/`defer`).
*   **Advanced Querying**: `F` and `Q` expressions, aggregation, annotation, and basic database functions.
*   **Transaction Management**: `transaction.atomic`, savepoints, and basic concurrency.

### 2. Lead / Staff / Architect Roadmap (Years 8+)
Focuses on system architecture, high-scale database systems, query compilation, custom database backends, migrations of multi-million row tables, and multi-database setups.
*   **Scaling & Partitioning**: Scaling read-heavy workloads, table partitioning, sharding, and caching.
*   **Migrations**: Squashing migrations, zero-downtime schema changes on production tables, and safe data migrations.
*   **Concurrency**: Lock levels (`select_for_update`), deadlock prevention, and transaction isolation levels.
*   **ORM Internals**: Query compilation, custom model managers, custom expressions, and database router architectures.
*   **Multi-tenant & Distributed Systems**: Database routing, read replicas, and distributed transactions.

---

## 📊 Modules & Folder Structure

All **704 questions** are 100% unique (no duplicate concepts) and follow a mandatory 12-section structure mapped to Django 5.x behaviour.

**Rewrite status:** modules marked ✅ have been rewritten to the interview-ready answer standard — each `# Answer` opens with a ~30–45 sec **spoken answer**, `# Production Scenario` is a STAR story grounded in the PNI Hub stack (replace every `[fill-in]` with your real metric), `# Performance Impact` holds trade-offs / when-not-to, and `# Common Mistakes` lists the wrong answers interviewers hear. Modules marked ⏳ still contain the original templated answers and are queued for rewrite (see `AGENT_INDEX.md` §3).

| Module | Filename | Primary Target Audience | Questions Count | Rewrite Status |
| :--- | :--- | :--- | :--- | :--- |
| **01** | [01_ORM_Fundamentals.md](./01_ORM_Fundamentals.md) | Fundamental to Senior | 35 | ⏳ Pending rewrite |
| **02** | [02_Model_Design.md](./02_Model_Design.md) | Senior | 35 | ⏳ Pending rewrite |
| **03** | [03_Field_Types.md](./03_Field_Types.md) | Senior | 35 | ⏳ Pending rewrite |
| **04** | [04_Model_Meta_Options.md](./04_Model_Meta_Options.md) | Senior | 35 | ⏳ Pending rewrite |
| **05** | [05_Managers_and_QuerySets.md](./05_Managers_and_QuerySets.md) | Senior / Lead | 35 | ⏳ Pending rewrite |
| **06** | [06_Query_Optimization.md](./06_Query_Optimization.md) | Senior / Lead | 39 | ✅ Interview-ready (rewritten 2026-11-26) |
| **07** | [07_Relationships.md](./07_Relationships.md) | Senior | 35 | ⏳ Pending rewrite |
| **08** | [08_Transactions.md](./08_Transactions.md) | Senior / Lead | 35 | ⏳ Pending rewrite |
| **09** | [09_Aggregation_and_Annotation.md](./09_Aggregation_and_Annotation.md) | Senior / Lead | 35 | ⏳ Pending rewrite |
| **10** | [10_Subquery_and_Exists.md](./10_Subquery_and_Exists.md) | Senior / Lead | 35 | ⏳ Pending rewrite |
| **11** | [11_Database_Functions.md](./11_Database_Functions.md) | Senior | 35 | ⏳ Pending rewrite |
| **12** | [12_Indexing.md](./12_Indexing.md) | Senior / Lead | 35 | ⏳ Pending rewrite |
| **13** | [13_Migrations.md](./13_Migrations.md) | Senior / Lead | 35 | ⏳ Pending rewrite |
| **14** | [14_Multi_Database.md](./14_Multi_Database.md) | Lead / Architect | 35 | ⏳ Pending rewrite |
| **15** | [15_Concurrency.md](./15_Concurrency.md) | Lead / Architect | 35 | ⏳ Pending rewrite |
| **16** | [16_Scaling_Strategies.md](./16_Scaling_Strategies.md) | Lead / Architect | 35 | ⏳ Pending rewrite |
| **17** | [17_ORM_Internals.md](./17_ORM_Internals.md) | Lead / Architect | 35 | ⏳ Pending rewrite |
| **18** | [18_Architecture_Questions.md](./18_Architecture_Questions.md) | Lead / Architect | 35 | ⏳ Pending rewrite |
| **19** | [19_Production_Issues.md](./19_Production_Issues.md) | Lead / Architect | 35 | ⏳ Pending rewrite |
| **20** | [20_Lead_Level_Scenarios.md](./20_Lead_Level_Scenarios.md) | Lead / Architect | 35 | ⏳ Pending rewrite |

---

## 🔥 Most Frequently Asked Interview Questions

1. **How does Django QuerySet lazy evaluation work internally?** (See [01_ORM_Fundamentals.md](./01_ORM_Fundamentals.md))
2. **What is the difference between `select_related` and `prefetch_related` and when does prefetch write a new query?** (See [06_Query_Optimization.md](./06_Query_Optimization.md))
3. **How does `transaction.atomic` manage database savepoints under the hood?** (See [08_Transactions.md](./08_Transactions.md))
4. **How do you safely migrate a 2TB table with zero downtime in production?** (See [20_Lead_Level_Scenarios.md](./20_Lead_Level_Scenarios.md))
5. **How does the Query Compiler translate ORM syntax into SQL?** (See [17_ORM_Internals.md](./17_ORM_Internals.md))
