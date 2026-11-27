<div align="center">

# 🎯 Interview Prep — Backend & Full-Stack Question Bank

**A personal, continuously-updated interview knowledge base for Senior Backend / Full-Stack engineers —
Python · Django · Django ORM · DRF · React · LangChain · LangGraph — with theory-first answers you can say out loud.**

![Questions](https://img.shields.io/badge/questions-2188-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12--3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.15+-A30000?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18%2F19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![LangChain](https://img.shields.io/badge/LangChain%20%26%20LangGraph-1.x-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![FastAPI](https://img.shields.io/badge/Viewer-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/license-All%20rights%20reserved-lightgrey?style=for-the-badge)

[📚 Contents](#-whats-inside) · [🆕 Release notes](#-release-notes) · [🚀 Quick start](#-quick-start) · [🧭 How to study](#-how-to-study) · [🔧 How it's built](#-how-its-maintained) · [👤 Author](#-author--copyright)

</div>

---

## 💡 About

This repository is my end-to-end interview preparation system. It collects the questions that are actually asked in
backend and full-stack interviews — from fundamentals to Lead/Architect-level scenarios — and answers each one the
way you'd explain it to an interviewer:

- 🗣️ **Theory first** — a plain-English explanation of *what*, *how it works underneath* and *why it matters*.
- 💻 **Code only when it helps** — short, runnable snippets, never boilerplate.
- 🔗 **Connected** — every answer links to related questions, so learning one topic leads you to the next.
- ⭐ **Real interviews** — questions I've been asked are marked and tracked in [`My_Interview_Questions.md`](./My_Interview_Questions.md).

Everything is plain Markdown: readable on GitHub, searchable, version-controlled — and browsable in a small local web app.

---

## 📚 What's inside

<!-- AUTO:CONTENTS:START -->
| | Section | What it covers | Questions | Style |
|---|---|---|---:|---|
| 🐍 | [**Python**](./Python/README.md) | Fundamentals, OOP, functional & decorators, concurrency (GIL, threads, multiprocessing, asyncio), memory & GC, DSA, data & AI, testing | 216 | Theory-first, topic clusters |
| 🗄️ | [**Django ORM — Short**](./Django%20ORM%20Short/README.md) | 20 ORM modules: queries, optimization, transactions, migrations, multi-DB, concurrency, scaling, internals, Lead scenarios | 705 | ⚡ Quick-revision booklet |
| 📖 | [**Django ORM — Deep**](./Django%20ORM/README.md) | The same 700+ questions with long answers: mechanics, SQL, trade-offs, scaling | 704 | 🔬 Deep dive (rewrite in progress) |
| 🔌 | [**Django REST Framework**](./Django%20DRF/README.md) | Serializers, validation, views & ViewSets, auth/JWT, permissions, throttling, pagination, testing, production scenarios | 131 | ⚡ Quick revision |
| 🌱 | [**Django (compact)**](./django/index.md) | Core Django, ORM and DRF essentials — the most-asked set | 56 | ⭐ Frequency-ranked |
| ⚛️ | [**React & Web**](./React/00_INDEX.md) | React fundamentals, hooks, state, performance, architecture, testing, web fundamentals, JavaScript | 156 | 🚧 Restructure planned |
| 🦜 | [**LangChain & LangGraph**](./LangChain%20LangGraph/README.md) | GenAI: LCEL, prompts, structured output, memory, RAG, tools & agents, LangGraph, checkpointing & HITL, multi-agent, LangSmith, production, system design | 220 | 🤖 GenAI, project-tied answers |
| 🎯 | **Company guides** | Focused crash plans & theory sheets (e.g. `Fractal_AI_*.md`) | — | Targeted prep |

> 📊 **2188 questions** in total · per-file counts and difficulty mix: [`index/INDEX.md`](./index/INDEX.md)
<!-- AUTO:CONTENTS:END -->

<!-- AUTO:GLANCE:START -->
🟢 **340** easy · 🟡 **832** medium · 🔴 **312** hard · ⚪ 704 untagged · ⭐ **1** asked in my interviews
<!-- AUTO:GLANCE:END -->

---

## 🆕 Release notes

Every update to the question bank is published as a **GitHub Release** listing exactly which questions were
**added**, which answers were **updated** and what was **removed** — grouped by section, with direct links.

<div align="center">

[![Latest release](https://img.shields.io/github/v/release/gaugoy/Interview-Prep?style=for-the-badge&label=latest%20release&color=success)](https://github.com/gaugoy/Interview-Prep/releases/latest)
&nbsp;
[![All releases](https://img.shields.io/badge/all-release%20notes-blue?style=for-the-badge)](https://github.com/gaugoy/Interview-Prep/releases)

</div>

---

## 🚀 Quick start

**Read on GitHub** — start with the [📚 contents table](#-whats-inside) above; every section has its own index and a `Question_Bank.md` listing all questions with direct links.

**Browse locally in the viewer** (search, topic sidebar, mark questions as covered):

```bash
git clone https://github.com/gaugoy/Interview-Prep.git
cd Interview-Prep
pip install -r src/app/requirements.txt
./run.sh                      # → http://localhost:8000   (API docs: /docs)
```

**Find a question from the terminal:**

```bash
python3 tools/find.py select_related prefetch     # search titles across all sections
python3 tools/find.py gil --stack Python
python3 tools/find.py --asked                      # questions asked in my real interviews
```

---

## 🧭 How to study

| When | Read | Why |
|---|---|---|
| 📅 Weeks before | [Python](./Python/README.md) → [Django ORM Short](./Django%20ORM%20Short/README.md) → [DRF](./Django%20DRF/README.md) | Build the foundation, topic by topic |
| 🔍 Going deeper | [Django ORM — Deep](./Django%20ORM/README.md) modules, Python *Hard* questions | Internals, trade-offs, scaling stories |
| ⏰ The day before | Each section's `Question_Bank.md` + ⭐⭐⭐ / *(Hard)* items + [`My_Interview_Questions.md`](./My_Interview_Questions.md) | Fast revision of what's asked most |

Difficulty tags: **(Easy)** fundamentals · **(Medium)** asked in most senior interviews · **(Hard)** internals / Lead-level. DRF and `django/` use ⭐⭐⭐ = asked in almost every interview.

---

## 🗂️ Repository structure

```text
Interview-Prep/
├── 🐍 Python/              # all Python topics (01–08) + README + Question_Bank
├── 🗄️ Django ORM Short/    # 20 ORM modules — short booklet answers
├── 📖 Django ORM/          # 20 ORM modules — deep answers + Question_Bank (705 titles)
├── 🔌 Django DRF/          # 16 DRF sections + Question_Bank
├── 🌱 django/              # compact Django / ORM / DRF set
├── ⚛️ React/               # React, web & JavaScript (to be restructured)
├── 🧾 index/               # generated question catalog + counts (don't edit)
├── 🧰 tools/               # index, search & validation scripts
├── 🖥️ src/app/             # FastAPI + vanilla-JS viewer
├── 🤖 prompts/ · PROMPTS.md · CLAUDE.md · AGENT_INDEX.md   # AI-maintenance instructions
└── ⭐ My_Interview_Questions.md
```

---

## 🔧 How it's maintained

This repo is maintained as **content-as-code**, with AI assistance and automated checks:

- 🤖 **Prompt system** — [`PROMPTS.md`](./PROMPTS.md) routes each request to one stack prompt in [`prompts/`](./prompts/00_shared_rules.md); shared rules apply everywhere.
- 🧾 **Generated index** — `tools/build_index.py` produces [`index/catalog.json`](./index/INDEX.md) with a stable id per question and keeps this README's counts current — nothing is hand-counted.
- 🏷️ **Release notes** — on every push to `main`, a GitHub Action compares the index with the previous release and publishes the added / updated / removed questions as a GitHub Release (`tools/release_notes.py`).
- ✅ **Validation** — `tools/validate.py` checks anchors, links, question banks and that every Python snippet parses. It runs after every AI edit (Claude Code hooks), before every commit (`.githooks/pre-commit`) and in CI (GitHub Actions).
- ⚡ **Slash commands** — `/prep-add-question`, `/prep-improve`, `/prep-audit`, `/prep-find`, `/prep-check`.

After cloning, enable the commit checks once: `git config core.hooksPath .githooks` · Details: [`tools/README.md`](./tools/README.md).

---

## 👤 Author & copyright

<div align="center">

**Gaurav Goyal** — Senior Software Engineer · Backend & Full-Stack (Python · Django · DRF · FastAPI · React)

[![GitHub](https://img.shields.io/badge/GitHub-gaugoy-181717?style=flat-square&logo=github)](https://github.com/gaugoy)

</div>

© 2026 **Gaurav Goyal**. All rights reserved.

All content in this repository — questions, answers, explanations, code examples, prompts, tools and the viewer
application — was authored and curated by Gaurav Goyal. No part of it may be copied, republished, redistributed or
used commercially without prior written permission from the author. You're welcome to read it and to link to it.
See [`LICENSE`](./LICENSE).

<div align="center">

⭐ *If this helped you prepare, a star on the repository is appreciated.* ⭐

</div>
