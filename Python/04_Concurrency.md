# Concurrency: GIL, Threading, Multiprocessing & asyncio
### [← Python index](./README.md) · [Question Bank](./Question_Bank.md)

How Python runs work in parallel or concurrently, and how to choose and use each tool.

**Topics:** [Fundamentals](./01_Fundamentals.md) · [OOP](./02_OOP.md) · [Functional](./03_Functional_and_Decorators.md) · [Concurrency](./04_Concurrency.md) · [Memory](./05_Memory_Management.md) · [DSA](./06_DSA.md) · [Data & AI](./07_Data_and_AI.md) · [Testing](./08_Testing_and_Tooling.md)

## Table of Contents

**Part A — Concurrency basics & the GIL**
1. (Easy) [What is the difference between concurrency and parallelism?](#q1)
2. (Easy) [What is the difference between a process and a thread?](#q2)
3. (Medium) [What is the GIL (Global Interpreter Lock) and why does it exist?](#q3)
4. (Medium) [How does the GIL affect CPU-bound vs I/O-bound programs?](#q4)
5. (Medium) [Is the GIL being removed? What is free-threaded Python?](#q5)
6. (Easy) [When do you use threading vs multiprocessing vs asyncio?](#q6)

**Part B — Multithreading**
7. (Easy) [How do you create and run threads in Python?](#q7)
8. (Medium) [What is a race condition? Show an example and the fix.](#q8)
9. (Medium) [What are Lock, RLock, Semaphore, Event and Condition?](#q9)
10. (Medium) [What is a deadlock and how do you avoid it?](#q10)
11. (Medium) [How do threads safely share data? Explain the producer–consumer pattern.](#q11)
12. (Medium) [Are Python operations like `list.append()` or `x += 1` thread-safe?](#q12)
13. (Easy) [What is a daemon thread?](#q13)
14. (Medium) [What is thread-local storage?](#q14)
15. (Easy) [What is ThreadPoolExecutor and why use it instead of raw threads?](#q15)

**Part C — Multiprocessing**
16. (Easy) [How do you use multiprocessing in Python?](#q16)
17. (Medium) [How do processes share data and communicate?](#q17)
18. (Hard) [What are the start methods fork, spawn and forkserver?](#q18)
19. (Easy) [Why do you need `if __name__ == "__main__":` with multiprocessing?](#q19)
20. (Medium) [What are the limitations of passing data between processes (pickling)?](#q20)
21. (Medium) [What is the difference between `map`, `submit` and `as_completed` in executors?](#q21)
22. (Medium) [When is multiprocessing a bad idea?](#q22)

**Part D — Async programming (asyncio, async/await)**
23. (Easy) [What is asyncio and what is the event loop?](#q23)
24. (Easy) [What is a coroutine? What do `async def` and `await` do?](#q24)
25. (Medium) [How does `await` work under the hood?](#q25)
26. (Easy) [How do you run multiple coroutines concurrently?](#q26)
27. (Medium) [What is the difference between `gather`, `wait` and `TaskGroup`?](#q27)
28. (Medium) [What happens if you call blocking code inside an async function? How do you fix it?](#q28)
29. (Medium) [How do timeouts and cancellation work in asyncio?](#q29)
30. (Medium) [What are `async with`, `async for` and async generators?](#q30)
31. (Medium) [How do you limit concurrency, e.g. calling an API for 10,000 URLs?](#q31)
32. (Medium) [How do you build a producer–consumer pipeline with asyncio?](#q32)
33. (Medium) [What is the difference between threads and asyncio?](#q33)
34. (Medium) [How is async used in Django and FastAPI?](#q34)
35. (Medium) [What are common asyncio mistakes?](#q35)

**Part E — Scenario questions**
36. (Medium) [A web API must resize uploaded images (CPU-heavy). How do you design it?](#q36)
37. (Medium) [You need to call 5 external APIs for one request. How do you make it fast?](#q37)
38. (Hard) [A Python service is stuck / hanging in production. How do you debug it?](#q38)

---

## Part A — Concurrency basics & the GIL

<a name="q1"></a>
## Q1. (Easy) What is the difference between concurrency and parallelism?
**Answer:** **Concurrency** = dealing with many tasks at once by switching between them (one cook handling several dishes). **Parallelism** = actually running tasks at the same moment on multiple CPU cores (several cooks). In Python: threads and asyncio give concurrency; multiprocessing gives true parallelism for CPU work.

---

<a name="q2"></a>
## Q2. (Easy) What is the difference between a process and a thread?
**Answer:**
| | Process | Thread |
|---|---|---|
| Memory | Own separate memory space | Shares memory with other threads of the process |
| Creation cost | Heavy (new interpreter) | Light |
| Communication | Needs IPC (queues, pipes, shared memory) | Direct (shared variables) — needs locks |
| Crash impact | Isolated | One bad thread can affect the whole process |
| In Python | Bypasses the GIL → real parallel CPU work | Limited by the GIL for CPU work |

---

<a name="q3"></a>
## Q3. (Medium) What is the GIL (Global Interpreter Lock) and why does it exist?
**Answer:** The GIL is a lock in CPython that allows **only one thread to execute Python bytecode at a time**. It exists because CPython's memory management (reference counting) isn't thread-safe — without the GIL, two threads changing an object's reference count at once could corrupt memory. The GIL makes the interpreter simpler and single-threaded code fast, at the cost of no parallel CPU work in threads.

**Follow-up:** Does the GIL make my code thread-safe? → No. It protects interpreter internals, not your logic — a thread can be switched out in the middle of `count += 1`.

**Related:** [Memory · Q2](./05_Memory_Management.md#q2) — What is reference counting?

---

<a name="q4"></a>
## Q4. (Medium) How does the GIL affect CPU-bound vs I/O-bound programs?
**Answer:**
- **I/O-bound** (network, disk, DB): a thread **releases the GIL while waiting** for I/O, so other threads run → threads/asyncio give a big speed-up.
- **CPU-bound** (math, image processing, parsing): threads take turns holding the GIL → no speed-up (often slower due to switching). Use **multiprocessing** (or C extensions like NumPy that release the GIL).

```python
# I/O-bound: 10 downloads in ~1 second with threads instead of ~10 seconds sequentially
with ThreadPoolExecutor(max_workers=10) as ex:
    pages = list(ex.map(requests.get, urls))
```

---

<a name="q5"></a>
## Q5. (Medium) Is the GIL being removed? What is free-threaded Python?
**Answer:** Yes, gradually. **PEP 703** added an optional **free-threaded build** of CPython without the GIL: experimental in Python 3.13, officially supported (but still not the default) in 3.14 (`python3.14t`). Threads can then run Python code on multiple cores. Trade-offs: single-threaded code is slightly slower and some C extensions need updates. The normal `python` build still has the GIL.

---

<a name="q6"></a>
## Q6. (Easy) When do you use threading vs multiprocessing vs asyncio?
**Answer:**
| Workload | Best choice | Why |
|---|---|---|
| Many I/O calls, async libraries available (HTTP, DB) | **asyncio** | Thousands of tasks on one thread, very low overhead |
| I/O with blocking/sync libraries | **threading** (`ThreadPoolExecutor`) | GIL released during I/O |
| CPU-heavy work | **multiprocessing** (`ProcessPoolExecutor`) | Separate processes = separate GILs = real parallelism |
| Mixed | asyncio + `to_thread` / process pool for heavy parts | Keep the event loop free |

---

## Part B — Multithreading

<a name="q7"></a>
## Q7. (Easy) How do you create and run threads in Python?
**Answer:** Create `threading.Thread(target=..., args=...)`, call `start()`, and `join()` to wait for it to finish.

```python
import threading, time

def worker(name):
    time.sleep(1)
    print(f"{name} done")

threads = [threading.Thread(target=worker, args=(f"T{i}",)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()          # all 3 finish in ~1 second, not 3
```

---

<a name="q8"></a>
## Q8. (Medium) What is a race condition? Show an example and the fix.
**Answer:** A race condition is when the result depends on the timing of threads accessing shared data. `counter += 1` is really "read, add, write" — two threads can read the same value and one update gets lost. Fix it with a `Lock` so only one thread runs the critical section at a time.

```python
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        with lock:            # without the lock, the final value can be less than 200000
            counter += 1

t1, t2 = threading.Thread(target=increment), threading.Thread(target=increment)
t1.start(); t2.start(); t1.join(); t2.join()
print(counter)                # 200000
```

---

<a name="q9"></a>
## Q9. (Medium) What are Lock, RLock, Semaphore, Event and Condition?
**Answer:**
- **Lock** — one thread at a time in a critical section.
- **RLock** (re-entrant) — the **same** thread can acquire it again (useful for recursive functions/methods that call each other); a normal Lock would deadlock.
- **Semaphore(n)** — at most `n` threads at once (e.g. limit to 5 DB connections).
- **Event** — one thread signals, others wait (`event.set()` / `event.wait()`), e.g. "config loaded".
- **Condition** — wait until some state is true, with notify (classic producer/consumer before `queue.Queue`).

```python
pool_limit = threading.Semaphore(5)
def query():
    with pool_limit:          # max 5 threads inside at once
        run_db_query()
```

---

<a name="q10"></a>
## Q10. (Medium) What is a deadlock and how do you avoid it?
**Answer:** A deadlock happens when threads wait for each other forever — Thread 1 holds lock A and waits for B, Thread 2 holds B and waits for A.
Avoid it by:
1. Always acquiring locks in the **same order** everywhere.
2. Using timeouts: `lock.acquire(timeout=5)`.
3. Holding locks for as short a time as possible, never calling unknown code while holding one.
4. Preferring higher-level tools (`queue.Queue`, executors) over manual locks.

---

<a name="q11"></a>
## Q11. (Medium) How do threads safely share data? Explain the producer–consumer pattern.
**Answer:** Use `queue.Queue` — it's thread-safe (locking built in). Producers `put()` items, consumers `get()` them; `task_done()` + `join()` wait until everything is processed.

```python
import queue, threading

q = queue.Queue(maxsize=100)

def producer():
    for i in range(10):
        q.put(i)

def consumer():
    while True:
        item = q.get()
        print("processing", item)
        q.task_done()

threading.Thread(target=consumer, daemon=True).start()
producer()
q.join()          # wait until all items are processed
```

---

<a name="q12"></a>
## Q12. (Medium) Are Python operations like `list.append()` or `x += 1` thread-safe?
**Answer:** Single built-in operations on built-in types, like `list.append()` or `dict[key] = value`, are atomic in CPython because of the GIL. But compound operations are **not**: `x += 1`, `if key not in d: d[key] = ...`, or read-modify-write on objects can be interrupted between steps. Don't rely on GIL details — use a `Lock` or `Queue` for shared state (and free-threaded Python makes this even more important).

---

<a name="q13"></a>
## Q13. (Easy) What is a daemon thread?
**Answer:** A background thread that doesn't keep the program alive: when all non-daemon threads finish, Python exits and daemon threads are killed abruptly. Good for background helpers (heartbeat, log flusher); bad for work that must finish cleanly (it can stop mid-write).

```python
threading.Thread(target=heartbeat, daemon=True).start()
```

---

<a name="q14"></a>
## Q14. (Medium) What is thread-local storage?
**Answer:** `threading.local()` gives each thread its own copy of an attribute — e.g. a per-thread DB connection or request context, without passing it around. (Django uses this idea for DB connections; in async code use `contextvars` instead.)

```python
local = threading.local()
def handle(request_id):
    local.request_id = request_id     # each thread sees only its own value
    process()
```

---

<a name="q15"></a>
## Q15. (Easy) What is ThreadPoolExecutor and why use it instead of raw threads?
**Answer:** `concurrent.futures.ThreadPoolExecutor` keeps a pool of reusable threads, gives you `Future` objects (results and exceptions), and cleans up automatically. Simpler and safer than managing threads yourself.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=20) as ex:
    futures = {ex.submit(fetch, url): url for url in urls}
    for f in as_completed(futures):           # results as they finish
        try:
            print(futures[f], len(f.result()))
        except Exception as e:
            print("failed", futures[f], e)
```

---

## Part C — Multiprocessing

<a name="q16"></a>
## Q16. (Easy) How do you use multiprocessing in Python?
**Answer:** Each process has its own Python interpreter and GIL, so CPU work runs truly in parallel. Use `Pool` / `ProcessPoolExecutor` for most cases.

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor() as ex:          # defaults to number of CPU cores
        results = list(ex.map(cpu_heavy, [10**7] * 8))
```

---

<a name="q17"></a>
## Q17. (Medium) How do processes share data and communicate?
**Answer:** Processes don't share memory by default. Options:
- **`multiprocessing.Queue` / `Pipe`** — send messages (objects are pickled).
- **`Value` / `Array`** — small shared values in shared memory (with a lock).
- **`multiprocessing.shared_memory`** (3.8+) — share a raw buffer, e.g. a big NumPy array without copying.
- **`Manager`** — shared dict/list through a server process (easy but slower).
- External: Redis, DB, files.

```python
from multiprocessing import Process, Value

def add(counter):
    for _ in range(1000):
        with counter.get_lock():
            counter.value += 1

if __name__ == "__main__":
    c = Value("i", 0)
    ps = [Process(target=add, args=(c,)) for _ in range(4)]
    [p.start() for p in ps]; [p.join() for p in ps]
    print(c.value)      # 4000
```

---

<a name="q18"></a>
## Q18. (Hard) What are the start methods fork, spawn and forkserver?
**Answer:**
- **fork** — copies the parent process (fast, inherits memory), but unsafe if the parent has threads/locks (can deadlock).
- **spawn** — starts a fresh interpreter and imports your module (slow start, safest). Default on Windows and macOS.
- **forkserver** — a clean server process forks workers on request (safe and reasonably fast). Default on Linux since Python 3.14 (was `fork` before).
Set it with `multiprocessing.set_start_method("spawn")` or `get_context("spawn")`.

**Related:** [Memory · Q11](./05_Memory_Management.md#q11) — How does memory behave with multiprocessing and `fork` (copy-on-write)?

---

<a name="q19"></a>
## Q19. (Easy) Why do you need `if __name__ == "__main__":` with multiprocessing?
**Answer:** With `spawn`/`forkserver`, each child process **imports your main module**. Without the guard, the child would run the top-level code again — creating new processes recursively (error or fork bomb). The guard ensures process creation only happens in the parent.

---

<a name="q20"></a>
## Q20. (Medium) What are the limitations of passing data between processes (pickling)?
**Answer:** Arguments and results are **pickled** and copied between processes. So: lambdas, local functions, open files, DB connections, sockets and locks can't be sent (`PicklingError`); big objects are slow to copy. Pass small data (ids, file paths), let each worker open its own connections, and use shared memory for large arrays.

---

<a name="q21"></a>
## Q21. (Medium) What is the difference between `map`, `submit` and `as_completed` in executors?
**Answer:**
- `ex.map(fn, items)` — returns results **in input order**; simple; an exception appears when you reach that item.
- `ex.submit(fn, x)` — returns a `Future` for one call; flexible (different functions/args).
- `as_completed(futures)` — yields futures **as they finish** (fastest first), good for progress and handling failures one by one.
For many small CPU tasks, `map(..., chunksize=100)` reduces inter-process overhead.

---

<a name="q22"></a>
## Q22. (Medium) When is multiprocessing a bad idea?
**Answer:** When tasks are tiny (process start + pickling cost more than the work), when tasks need lots of shared state, when the work is I/O-bound (threads/asyncio are lighter), or when memory is tight (each process has its own copy of the interpreter and data). Also inside web servers — prefer a task queue (Celery/RabbitMQ) with separate worker processes.

---

## Part D — Async programming (asyncio, async/await)

<a name="q23"></a>
## Q23. (Easy) What is asyncio and what is the event loop?
**Answer:** `asyncio` is Python's library for **single-threaded concurrency** using coroutines. The **event loop** is a scheduler: it runs a task until the task `await`s something slow (network, sleep), then switches to another ready task, and resumes the first when its result is ready. So one thread can handle thousands of waiting I/O operations.

---

<a name="q24"></a>
## Q24. (Easy) What is a coroutine? What do `async def` and `await` do?
**Answer:** `async def` defines a **coroutine function**; calling it doesn't run it — it returns a coroutine object. `await` runs a coroutine (or other awaitable) and **pauses the current coroutine** until the result is ready, letting the event loop run other tasks meanwhile.

```python
import asyncio

async def fetch_user(uid):
    await asyncio.sleep(1)          # simulates a network call
    return {"id": uid}

async def main():
    user = await fetch_user(1)
    print(user)

asyncio.run(main())                 # starts the event loop
```

**Related:** [Functional · Q18](./03_Functional_and_Decorators.md#q18) — How do you write a decorator for async functions?

---

<a name="q25"></a>
## Q25. (Medium) How does `await` work under the hood?
**Answer:** Coroutines are built on generators: at an `await`, the coroutine **yields control** back to the event loop along with a Future it's waiting for. The loop registers interest in that I/O (via the OS selector — epoll/kqueue), runs other ready tasks, and when the I/O completes it sets the Future's result and resumes the coroutine right after the `await`. It's **cooperative**: a task only gives up control at an `await`.

**Related:** [Functional · Q9](./03_Functional_and_Decorators.md#q9) — What is `yield from`?

---

<a name="q26"></a>
## Q26. (Easy) How do you run multiple coroutines concurrently?
**Answer:** Awaiting one after another runs them **sequentially**. Use `asyncio.gather()` or tasks to run them concurrently.

```python
async def main():
    # sequential: ~3 seconds
    a = await fetch_user(1); b = await fetch_user(2); c = await fetch_user(3)

    # concurrent: ~1 second
    a, b, c = await asyncio.gather(fetch_user(1), fetch_user(2), fetch_user(3))

    # create_task: start now, await later
    task = asyncio.create_task(fetch_user(4))
    do_other_work()
    d = await task
```

---

<a name="q27"></a>
## Q27. (Medium) What is the difference between `gather`, `wait` and `TaskGroup`?
**Answer:**
- **`asyncio.gather(*aws)`** — runs all, returns results in order. If one fails, the exception is raised but the **others keep running**; `return_exceptions=True` returns errors as values.
- **`asyncio.wait(tasks, return_when=...)`** — returns `(done, pending)` sets; more control (e.g. `FIRST_COMPLETED`).
- **`asyncio.TaskGroup`** (3.11+) — structured concurrency: if one task fails, the **others are cancelled** and errors are raised together (`ExceptionGroup`). Preferred in modern code.

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch_user(1))
        t2 = tg.create_task(fetch_user(2))
    print(t1.result(), t2.result())       # all done here
```

---

<a name="q28"></a>
## Q28. (Medium) What happens if you call blocking code inside an async function? How do you fix it?
**Answer:** Blocking calls (`time.sleep`, `requests.get`, a sync DB driver, heavy CPU loops) **freeze the whole event loop** — every other task stops until it returns. Fixes: use async libraries (`asyncio.sleep`, `httpx`/`aiohttp`, async DB drivers); move unavoidable blocking calls to a thread with `asyncio.to_thread()`; move CPU-heavy work to a process pool.

```python
async def handler():
    await asyncio.sleep(1)                         # ✔ non-blocking
    data = await asyncio.to_thread(requests.get, url)   # ✔ sync library in a thread
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(process_pool, crunch, data)   # ✔ CPU work
    # time.sleep(1)  ✘ blocks every other task
```

---

<a name="q29"></a>
## Q29. (Medium) How do timeouts and cancellation work in asyncio?
**Answer:** `asyncio.timeout(seconds)` (3.11+) or `asyncio.wait_for(aw, timeout)` cancel the operation if it takes too long and raise `TimeoutError`. Cancelling a task (`task.cancel()`) raises `CancelledError` **inside** the coroutine at its current `await`, so it can clean up in `try/finally`. Don't swallow `CancelledError`.

```python
async def main():
    try:
        async with asyncio.timeout(2):
            await slow_api_call()
    except TimeoutError:
        print("gave up after 2s")
```

---

<a name="q30"></a>
## Q30. (Medium) What are `async with`, `async for` and async generators?
**Answer:**
- **`async with`** — async context manager (`__aenter__`/`__aexit__`), for resources whose open/close is async: HTTP sessions, DB connections, locks.
- **`async for`** — iterates an async iterator (each next item is awaited), e.g. streaming rows or messages.
- **Async generator** — `async def` with `yield`.

```python
async def read_events(stream):
    async for line in stream:          # waits for each line without blocking
        yield json.loads(line)

async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.example.com/items")
```

**Related:** [Fundamentals · Q23](./01_Fundamentals.md#q23) — What is the `with` statement and context managers?

---

<a name="q31"></a>
## Q31. (Medium) How do you limit concurrency, e.g. calling an API for 10,000 URLs?
**Answer:** Launching 10,000 requests at once can overload the API, hit rate limits or run out of sockets. Use an `asyncio.Semaphore` to allow only N in flight.

```python
sem = asyncio.Semaphore(50)

async def fetch(client, url):
    async with sem:                     # at most 50 requests at the same time
        r = await client.get(url, timeout=10)
        return r.status_code

async def main(urls):
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*(fetch(client, u) for u in urls))
```

---

<a name="q32"></a>
## Q32. (Medium) How do you build a producer–consumer pipeline with asyncio?
**Answer:** `asyncio.Queue` (not thread-safe — for tasks in the same loop): producers `await q.put()`, a fixed number of worker tasks `await q.get()`.

```python
async def worker(q):
    while True:
        item = await q.get()
        await process(item)
        q.task_done()

async def main(items):
    q = asyncio.Queue(maxsize=100)
    workers = [asyncio.create_task(worker(q)) for _ in range(5)]
    for it in items:
        await q.put(it)
    await q.join()                      # wait until everything is processed
    for w in workers:
        w.cancel()
```

---

<a name="q33"></a>
## Q33. (Medium) What is the difference between threads and asyncio?
**Answer:**
| | Threads | asyncio |
|---|---|---|
| Switching | **Preemptive** — the OS/interpreter can switch at any point | **Cooperative** — switches only at `await` |
| Race conditions | Anywhere → need locks | Only across `await` points → fewer bugs |
| Scale | Hundreds of threads (memory per thread) | Tens of thousands of tasks (cheap) |
| Libraries | Works with any blocking library | Needs async libraries (or `to_thread`) |
| CPU work | Limited by GIL | Blocks the loop — offload it |

---

<a name="q34"></a>
## Q34. (Medium) How is async used in Django and FastAPI?
**Answer:** **FastAPI** is async-native: `async def` endpoints run on the event loop (use async DB/HTTP clients); plain `def` endpoints are run in a thread pool automatically. **Django** supports async views under ASGI and an async ORM API (`aget`, `acount`, `async for`), but ORM calls still run in a thread internally; call sync-only code (like `transaction.atomic`) with `sync_to_async`, and async code from sync with `async_to_sync`.

---

<a name="q35"></a>
## Q35. (Medium) What are common asyncio mistakes?
**Answer:**
1. Forgetting `await` — you get a coroutine object and a "coroutine was never awaited" warning.
2. Blocking calls (`time.sleep`, `requests`) inside async code.
3. `create_task()` without keeping a reference — the task can be garbage-collected before finishing; keep tasks in a set or use `TaskGroup`.
4. Awaiting in a loop when you wanted concurrency (use `gather`/`TaskGroup`).
5. Swallowing `CancelledError`.
6. Calling `asyncio.run()` inside an already running loop (e.g. in Jupyter or inside another async function).

---

## Part E — Scenario questions

<a name="q36"></a>
## Q36. (Medium) A web API must resize uploaded images (CPU-heavy). How do you design it?
**Answer:** Don't do CPU work in the request (blocks the worker / event loop). Save the upload, push a job to a task queue (Celery/RabbitMQ), let separate worker **processes** resize images, and return `202 Accepted` with a job id the client can poll. For small, quick jobs inside an async service, use a `ProcessPoolExecutor` via `run_in_executor`.

---

<a name="q37"></a>
## Q37. (Medium) You need to call 5 external APIs for one request. How do you make it fast?
**Answer:** They're independent I/O calls, so run them **concurrently** instead of one after another: `asyncio.gather` with an async HTTP client (or a `ThreadPoolExecutor` in sync code). Total time ≈ the slowest call instead of the sum. Add per-call timeouts and handle partial failures (`return_exceptions=True`).

---

<a name="q38"></a>
## Q38. (Hard) A Python service is stuck / hanging in production. How do you debug it?
**Answer:**
1. `py-spy dump --pid <pid>` — see what every thread is doing right now (no restart needed).
2. `faulthandler.dump_traceback_later()` or `faulthandler.register(signal.SIGUSR1)` — print all thread stacks.
3. Look for threads waiting on locks (deadlock), a blocked event loop (`asyncio` debug mode warns about slow callbacks), or a hung network call without timeout.
4. Fix: consistent lock ordering, timeouts on every I/O call, no blocking calls in async code.

---
