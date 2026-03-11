# 🌐 14 — Web Fundamentals
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q15)](#medium)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is the difference between `localStorage`, `sessionStorage`, and cookies?

**Answer:**

| Feature | localStorage | sessionStorage | Cookies |
|---------|-------------|----------------|---------|
| Capacity | ~5-10MB | ~5MB | ~4KB |
| Expiry | Never (manual) | Tab close | Configurable |
| Sent to server | ❌ | ❌ | ✅ (every request) |
| Accessible from JS | ✅ | ✅ | ✅ (unless HttpOnly) |
| Cross-tab | ✅ | ❌ | ✅ |

```javascript
// localStorage — persists until manually cleared
localStorage.setItem('theme', 'dark');
const theme = localStorage.getItem('theme');
localStorage.removeItem('theme');
localStorage.clear();

// sessionStorage — cleared when tab closes
sessionStorage.setItem('formData', JSON.stringify({ name: 'Alice' }));
const formData = JSON.parse(sessionStorage.getItem('formData'));

// Cookies — sent with every HTTP request
document.cookie = 'token=abc123; expires=Fri, 31 Dec 2024 23:59:59 GMT; path=/; Secure; SameSite=Strict';

// HttpOnly cookies (set by server) — not accessible from JS (XSS protection)
// Set-Cookie: token=abc123; HttpOnly; Secure; SameSite=Strict

// Use cases:
// localStorage: user preferences, theme, non-sensitive data
// sessionStorage: temporary form data, wizard steps
// Cookies: auth tokens (HttpOnly), session IDs
```

---

### Q2. What is the difference between HTTP and HTTPS?

**Answer:**
- **HTTP** — HyperText Transfer Protocol, data sent in **plain text**
- **HTTPS** — HTTP + **TLS/SSL encryption**, data encrypted in transit

```
HTTP:  Client ←→ Server (plain text — anyone can read)
HTTPS: Client ←→ Server (encrypted — only endpoints can read)

HTTPS process:
1. Client connects to server
2. Server sends SSL certificate (contains public key)
3. Client verifies certificate with Certificate Authority
4. Client and server negotiate encryption keys
5. All data encrypted with symmetric key
```

```javascript
// Always use HTTPS for:
// - Authentication (passwords, tokens)
// - Personal data
// - Payment information
// - Any sensitive data

// HTTP → HTTPS redirect (server-side)
// Express.js
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https') {
    res.redirect(`https://${req.header('host')}${req.url}`);
  } else {
    next();
  }
});
```

---

### Q3. What are HTTP methods? GET vs POST vs PUT vs PATCH vs DELETE?

**Answer:**

| Method | Purpose | Body | Idempotent | Safe |
|--------|---------|------|-----------|------|
| GET | Read | ❌ | ✅ | ✅ |
| POST | Create | ✅ | ❌ | ❌ |
| PUT | Replace | ✅ | ✅ | ❌ |
| PATCH | Partial update | ✅ | ❌ | ❌ |
| DELETE | Delete | Optional | ✅ | ❌ |

```javascript
// GET — retrieve resource
fetch('/api/users/1')  // GET by default

// POST — create new resource
fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Alice', email: 'alice@example.com' }),
});

// PUT — replace entire resource
fetch('/api/users/1', {
  method: 'PUT',
  body: JSON.stringify({ name: 'Alice Updated', email: 'alice@example.com', age: 31 }),
});

// PATCH — partial update
fetch('/api/users/1', {
  method: 'PATCH',
  body: JSON.stringify({ name: 'Alice Updated' }),  // Only update name
});

// DELETE — remove resource
fetch('/api/users/1', { method: 'DELETE' });

// Idempotent: calling multiple times = same result
// PUT /users/1 with same data → same result each time
// DELETE /users/1 → first call deletes, subsequent calls return 404 (same end state)
```

---

### Q4. What is REST? What are its constraints?

**Answer:**
REST (Representational State Transfer) is an **architectural style** for designing networked APIs.

**6 constraints:**
1. **Client-Server** — separation of concerns
2. **Stateless** — each request contains all needed info
3. **Cacheable** — responses can be cached
4. **Uniform Interface** — consistent resource identification
5. **Layered System** — client doesn't know if talking to server or proxy
6. **Code on Demand** (optional) — server can send executable code

```javascript
// RESTful API design
// Resources are nouns, HTTP methods are verbs

// ✅ RESTful
GET    /api/users          // List all users
GET    /api/users/1        // Get user 1
POST   /api/users          // Create user
PUT    /api/users/1        // Replace user 1
PATCH  /api/users/1        // Update user 1 partially
DELETE /api/users/1        // Delete user 1

GET    /api/users/1/posts  // Get posts for user 1
POST   /api/users/1/posts  // Create post for user 1

// ❌ Not RESTful
GET    /api/getUser?id=1
POST   /api/deleteUser
GET    /api/createUser

// HTTP status codes
// 200 OK, 201 Created, 204 No Content
// 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
// 409 Conflict, 422 Unprocessable Entity
// 500 Internal Server Error, 503 Service Unavailable
```

---

### Q5. What is GraphQL? How is it different from REST?

**Answer:**

| Feature | REST | GraphQL |
|---------|------|---------|
| Endpoints | Multiple | Single (`/graphql`) |
| Data fetching | Fixed response | Request exactly what you need |
| Over-fetching | Common | Eliminated |
| Under-fetching | Common (N+1) | Eliminated |
| Type system | Optional | Built-in |
| Versioning | URL versioning | Schema evolution |

```javascript
// REST — multiple requests, fixed responses
// GET /api/users/1 → { id, name, email, address, phone, ... }
// GET /api/users/1/posts → [{ id, title, content, ... }]
// GET /api/users/1/followers → [{ id, name, ... }]

// GraphQL — single request, exact data
const query = `
  query GetUserWithPosts($userId: ID!) {
    user(id: $userId) {
      name          # Only what we need
      email
      posts(first: 5) {
        title
        createdAt
      }
    }
  }
`;

fetch('/graphql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query,
    variables: { userId: '1' },
  }),
});

// GraphQL mutation
const mutation = `
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      id
      title
      createdAt
    }
  }
`;

// When to use GraphQL:
// ✅ Complex data requirements
// ✅ Multiple clients with different data needs (mobile vs web)
// ✅ Rapid iteration on frontend
// ❌ Simple CRUD APIs
// ❌ File uploads (use REST)
```

---

### Q6. What is WebSocket? How is it different from HTTP polling?

**Answer:**

| | HTTP Polling | WebSocket |
|-|-------------|-----------|
| Connection | New per request | Persistent |
| Direction | Client → Server | Bidirectional |
| Latency | High | Low |
| Overhead | High (headers) | Low |
| Use case | Infrequent updates | Real-time |

```javascript
// HTTP Polling — client repeatedly asks for updates
function pollForUpdates() {
  setInterval(async () => {
    const data = await fetch('/api/updates').then(r => r.json());
    updateUI(data);
  }, 1000);  // Ask every second — wasteful!
}

// Long Polling — server holds request until update available
async function longPoll() {
  while (true) {
    const data = await fetch('/api/updates?wait=true').then(r => r.json());
    updateUI(data);
    // Immediately make next request
  }
}

// WebSocket — persistent bidirectional connection
const ws = new WebSocket('wss://api.fractal.ai/stream');

ws.onopen = () => {
  console.log('Connected');
  ws.send(JSON.stringify({ type: 'subscribe', channel: 'metrics' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateDashboard(data);
};

ws.onclose = () => {
  console.log('Disconnected');
  // Reconnect logic
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Use WebSocket for: chat, live dashboards, collaborative editing, gaming
// Use SSE (Server-Sent Events) for: one-way server→client streams (simpler)
```

---

### Q7. What is CSRF? How do you prevent it?

**Answer:**
CSRF (Cross-Site Request Forgery) tricks a user's browser into making **unauthorized requests** to a site where they're authenticated.

```
Attack scenario:
1. User logs into bank.com (has session cookie)
2. User visits evil.com
3. evil.com has: <img src="https://bank.com/transfer?to=attacker&amount=1000">
4. Browser sends request WITH bank.com cookie → transfer happens!
```

```javascript
// Prevention 1: CSRF tokens
// Server generates unique token per session
// Client must include token in state-changing requests

// Express.js with csurf
const csrf = require('csurf');
app.use(csrf({ cookie: true }));

app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

// HTML form
// <input type="hidden" name="_csrf" value="<%= csrfToken %>">

// Prevention 2: SameSite cookies
// Set-Cookie: session=abc123; SameSite=Strict
// Browser won't send cookie on cross-site requests

// Prevention 3: Check Origin/Referer header
app.use((req, res, next) => {
  const origin = req.headers.origin || req.headers.referer;
  if (origin && !origin.startsWith('https://myapp.com')) {
    return res.status(403).json({ error: 'CSRF detected' });
  }
  next();
});

// Prevention 4: Custom request headers
// AJAX requests with custom headers can't be forged cross-origin
fetch('/api/transfer', {
  method: 'POST',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',  // Custom header
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ amount: 100 }),
});
```

---

### Q8. What is XSS? How do you prevent it in React?

**Answer:**
XSS (Cross-Site Scripting) injects **malicious scripts** into web pages viewed by other users.

```javascript
// Attack: user submits: <script>document.cookie</script>
// If rendered as HTML, script executes in victim's browser

// React automatically escapes JSX — safe by default
function Comment({ text }) {
  return <p>{text}</p>;  // ✅ Safe — React escapes HTML entities
  // <script>alert('xss')</script> → rendered as text, not executed
}

// ❌ DANGEROUS: dangerouslySetInnerHTML
function RichText({ html }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
  // If html contains <script>, it WILL execute!
}

// ✅ Safe: sanitize before using dangerouslySetInnerHTML
import DOMPurify from 'dompurify';

function SafeRichText({ html }) {
  const sanitized = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// Other XSS vectors to avoid:
// ❌ eval(userInput)
// ❌ document.write(userInput)
// ❌ element.innerHTML = userInput
// ❌ href={userInput}  — could be javascript:alert('xss')

// ✅ Safe href
function SafeLink({ url, children }) {
  const safeUrl = url.startsWith('http') ? url : '#';
  return <a href={safeUrl}>{children}</a>;
}

// Content Security Policy (CSP) — defense in depth
// <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
```

---

### Q9. What is the browser's event loop?

**Answer:**
The event loop is JavaScript's mechanism for handling **asynchronous operations** in a single-threaded environment.

```
Call Stack → executes synchronous code
Task Queue → setTimeout, setInterval, I/O callbacks
Microtask Queue → Promises, queueMicrotask (higher priority)

Event Loop:
1. Execute all synchronous code (empty call stack)
2. Process ALL microtasks (Promises)
3. Process ONE task from task queue
4. Render (if needed)
5. Repeat
```

```javascript
console.log('1');  // Sync

setTimeout(() => console.log('2'), 0);  // Task queue

Promise.resolve().then(() => console.log('3'));  // Microtask queue

console.log('4');  // Sync

// Output: 1, 4, 3, 2
// Explanation:
// 1. '1' — sync
// 2. setTimeout scheduled → task queue
// 3. Promise.then scheduled → microtask queue
// 4. '4' — sync
// 5. Call stack empty → process microtasks → '3'
// 6. Process task → '2'

// Practical implications:
async function example() {
  console.log('A');
  await Promise.resolve();  // Yields to microtask queue
  console.log('B');         // Runs after current sync code
}

example();
console.log('C');
// Output: A, C, B
```

---

### Q10. What is the difference between `setTimeout(fn, 0)` and a Promise?

**Answer:**
Both are asynchronous, but they use **different queues** with different priorities.

```javascript
// setTimeout(fn, 0) → Task Queue (macrotask)
// Promise.then → Microtask Queue (higher priority)

console.log('start');

setTimeout(() => console.log('setTimeout'), 0);

Promise.resolve()
  .then(() => console.log('promise 1'))
  .then(() => console.log('promise 2'));

console.log('end');

// Output:
// start
// end
// promise 1    ← microtask (runs before setTimeout)
// promise 2    ← microtask
// setTimeout   ← macrotask (runs after all microtasks)

// Why this matters:
// React state updates in event handlers are batched synchronously
// React state updates in setTimeout are NOT batched (React 17)
// React 18: automatic batching everywhere

// Use case: defer work to next tick
// setTimeout(fn, 0) — defer to next event loop iteration
// queueMicrotask(fn) — defer to end of current microtask queue
// requestAnimationFrame(fn) — defer to before next paint
```

---

### Q11. What is the critical rendering path?

**Answer:**
The critical rendering path is the sequence of steps the browser takes to **convert HTML/CSS/JS into pixels** on screen.

```
HTML → DOM
CSS  → CSSOM
DOM + CSSOM → Render Tree → Layout → Paint → Composite

Steps:
1. Parse HTML → build DOM
2. Parse CSS → build CSSOM
3. Combine → Render Tree (only visible elements)
4. Layout — calculate position and size of each element
5. Paint — fill in pixels
6. Composite — layer management (GPU)
```

```html
<!-- Optimize critical rendering path -->

<!-- 1. CSS in <head> — don't block rendering -->
<head>
  <link rel="stylesheet" href="critical.css">
  <!-- Inline critical CSS for fastest FCP -->
  <style>/* above-the-fold styles */</style>
</head>

<!-- 2. JS at end of body or with defer/async -->
<body>
  <!-- content -->
  <script src="app.js" defer></script>  <!-- Non-blocking -->
</body>

<!-- async: download in parallel, execute immediately when ready -->
<!-- defer: download in parallel, execute after HTML parsed -->

<!-- 3. Preload critical resources -->
<link rel="preload" href="hero-image.jpg" as="image">
<link rel="preload" href="main-font.woff2" as="font" crossorigin>

<!-- 4. Preconnect to external domains -->
<link rel="preconnect" href="https://api.fractal.ai">
```

---

### Q12. What is HTTP caching? What are `Cache-Control` headers?

**Answer:**
HTTP caching stores responses so future requests can be served faster.

```javascript
// Cache-Control directives
// max-age=3600 — cache for 1 hour
// no-cache — must revalidate with server before using cache
// no-store — don't cache at all
// public — can be cached by CDN
// private — only browser cache (not CDN)
// immutable — content never changes (use with content hash)

// Express.js cache headers
app.get('/api/data', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300');  // Cache 5 min
  res.json(data);
});

// Static assets — long cache with content hash
// main.a1b2c3d4.js → Cache-Control: public, max-age=31536000, immutable
// When content changes, filename changes → cache busted automatically

// API responses — short cache or no cache
// Cache-Control: no-cache (must revalidate)
// Cache-Control: no-store (never cache)

// ETag — conditional requests
// Server: ETag: "abc123"
// Client: If-None-Match: "abc123"
// Server: 304 Not Modified (if unchanged) or 200 with new content

// Last-Modified
// Server: Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
// Client: If-Modified-Since: Wed, 21 Oct 2024 07:28:00 GMT
// Server: 304 Not Modified or 200 with new content
```

---

### Q13. What is REST vs GraphQL vs WebSocket — when to use each?

**Answer:**

```
REST:
✅ Simple CRUD operations
✅ Public APIs (well-understood)
✅ File uploads/downloads
✅ Caching is important
Example: GET /api/products, POST /api/orders

GraphQL:
✅ Complex data requirements
✅ Multiple clients (mobile, web, desktop) with different needs
✅ Rapid frontend iteration
✅ Aggregating multiple data sources
Example: Query user + their posts + comments in one request

WebSocket:
✅ Real-time bidirectional communication
✅ Low latency required
✅ High-frequency updates
Example: Chat, live dashboards, collaborative editing, gaming

SSE (Server-Sent Events):
✅ Server → client only (one-way)
✅ Simpler than WebSocket
✅ Auto-reconnect built-in
Example: Live notifications, progress updates, stock prices
```

---

### Q14. What is the difference between `304 Not Modified` and `200 OK`?

**Answer:**

```
200 OK — full response with body
304 Not Modified — resource unchanged, use cached version (no body)

Flow:
1. Client: GET /api/data
   Server: 200 OK + ETag: "abc123" + body

2. Client: GET /api/data + If-None-Match: "abc123"
   Server: 304 Not Modified (no body — use cache!)
   OR
   Server: 200 OK + ETag: "xyz789" + new body (if changed)

Benefits of 304:
- Saves bandwidth (no body transmitted)
- Faster response
- Confirms data is still fresh
```

```javascript
// Express.js — automatic ETag support
app.use(express.static('public'));  // Automatically handles ETags

// Manual ETag
app.get('/api/data', (req, res) => {
  const data = getData();
  const etag = generateETag(data);

  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();  // Not modified
  }

  res.set('ETag', etag);
  res.json(data);
});
```

---

### Q15. What is the browser event loop? Call stack, task queue, microtask queue?

> See Q9 above for the full answer.

**Quick summary:**
```
Priority order:
1. Call Stack (synchronous code) — highest priority
2. Microtask Queue (Promises, queueMicrotask) — runs after each task
3. Task Queue (setTimeout, setInterval, I/O) — lowest priority
4. Render — between tasks

Rule: ALL microtasks run before the next task
```

---

### [← Back to Index](./00_INDEX.md) | [Next: AI & Analytics Concepts →](./15_AI_Analytics.md)
