# 🏛️ 12 — React Architecture & Ecosystem
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q15)](#medium)
- [🔴 Hard (Q16–Q20)](#hard)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is the difference between Next.js and Create React App?

**Answer:**

| Feature | Create React App | Next.js |
|---------|-----------------|---------|
| Rendering | CSR only | CSR, SSR, SSG, ISR |
| Routing | React Router (manual) | File-based (automatic) |
| API routes | ❌ | ✅ |
| SEO | Poor | Excellent |
| Performance | Good | Better |
| Status | Deprecated | ✅ Actively maintained |

```jsx
// CRA — client-side only, manual routing
// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

// Next.js — file-based routing, multiple rendering strategies
// app/page.tsx → /
// app/about/page.tsx → /about
// app/users/[id]/page.tsx → /users/123

// Next.js page with SSR
export default async function UserPage({ params }) {
  const user = await fetch(`/api/users/${params.id}`).then(r => r.json());
  return <UserProfile user={user} />;
}

// Next.js API route
// app/api/users/route.ts
export async function GET(request) {
  const users = await db.users.findAll();
  return Response.json(users);
}
```

---

### Q2. What is SSR (Server-Side Rendering)?

**Answer:**
SSR renders the React component tree **on the server** for each request, sending fully-formed HTML to the client.

**Advantages:** Better SEO, faster First Contentful Paint, works without JavaScript
**Disadvantages:** Higher server load, slower Time to First Byte, more complex

```jsx
// Next.js App Router — SSR by default for async components
async function ProductPage({ params }) {
  // Runs on server — can access DB directly
  const product = await db.products.findById(params.id);

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />  {/* Client component */}
    </div>
  );
}

// Next.js Pages Router — getServerSideProps
export async function getServerSideProps({ params, req, res }) {
  const product = await fetchProduct(params.id);

  if (!product) {
    return { notFound: true };
  }

  return {
    props: { product },  // Passed to page component
  };
}

export default function ProductPage({ product }) {
  return <div>{product.name}</div>;
}
```

---

### Q3. What is SSG (Static Site Generation)?

**Answer:**
SSG pre-renders pages **at build time**, generating static HTML files. Fastest possible delivery — served from CDN.

```jsx
// Next.js Pages Router — getStaticProps
export async function getStaticProps() {
  const posts = await fetchAllPosts();

  return {
    props: { posts },
    revalidate: 60,  // ISR: regenerate every 60 seconds
  };
}

// getStaticPaths — for dynamic routes
export async function getStaticPaths() {
  const posts = await fetchAllPosts();

  return {
    paths: posts.map(post => ({ params: { id: post.id } })),
    fallback: 'blocking',  // Generate on-demand for unknown paths
  };
}

// Next.js App Router — static by default for non-async components
// Force static generation
export const dynamic = 'force-static';

// When to use SSG:
// ✅ Blog posts, documentation, marketing pages
// ✅ Content that doesn't change per user
// ✅ Maximum performance needed
// ❌ User-specific content, real-time data
```

---

### Q4. What is ISR (Incremental Static Regeneration)?

**Answer:**
ISR combines SSG and SSR — pages are **statically generated but can be regenerated** in the background after a specified time.

```jsx
// Next.js Pages Router
export async function getStaticProps() {
  const data = await fetchData();

  return {
    props: { data },
    revalidate: 60,  // Regenerate at most once every 60 seconds
  };
}

// Next.js App Router — fetch with revalidation
async function DataPage() {
  const data = await fetch('/api/data', {
    next: { revalidate: 60 }  // Cache for 60 seconds
  }).then(r => r.json());

  return <DataDisplay data={data} />;
}

// On-demand revalidation
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';

export async function POST(request) {
  const { path } = await request.json();
  revalidatePath(path);  // Trigger regeneration
  return Response.json({ revalidated: true });
}

// ISR flow:
// 1. First request: serve stale static page
// 2. Background: regenerate page
// 3. Next request: serve fresh page
```

---

### Q5. What is React Router? `BrowserRouter` vs `HashRouter`?

**Answer:**

| | BrowserRouter | HashRouter |
|-|--------------|------------|
| URL format | `/about` | `/#/about` |
| Server config | Needs server setup | No server config needed |
| SEO | Better | Worse |
| Use case | Production apps | Static hosting, legacy |

```jsx
import { BrowserRouter, HashRouter, Routes, Route, Link, useNavigate, useParams, useLocation } from 'react-router-dom';

// BrowserRouter — uses HTML5 History API
function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/users/123">User 123</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users/:id" element={<UserProfile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

// Hooks
function UserProfile() {
  const { id } = useParams();           // URL params
  const navigate = useNavigate();       // Programmatic navigation
  const location = useLocation();       // Current location

  return (
    <div>
      <p>User ID: {id}</p>
      <button onClick={() => navigate(-1)}>Back</button>
      <button onClick={() => navigate('/home')}>Home</button>
    </div>
  );
}

// Protected route
function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
}
```

---

### Q6. What is the difference between `useNavigate` and `useHistory`?

**Answer:**
- `useHistory` — React Router v5 (legacy)
- `useNavigate` — React Router v6 (current)

```jsx
// React Router v5 — useHistory
import { useHistory } from 'react-router-dom';

function OldComponent() {
  const history = useHistory();
  history.push('/home');
  history.replace('/home');
  history.goBack();
}

// React Router v6 — useNavigate
import { useNavigate } from 'react-router-dom';

function NewComponent() {
  const navigate = useNavigate();

  navigate('/home');           // Push (adds to history)
  navigate('/home', { replace: true });  // Replace (no back button)
  navigate(-1);                // Go back
  navigate(1);                 // Go forward

  // With state
  navigate('/dashboard', { state: { from: 'login' } });
}
```

---

### Q7. What is a protected route? How would you implement one?

**Answer:**
A protected route **redirects unauthenticated users** to a login page.

```jsx
import { Navigate, useLocation, Outlet } from 'react-router-dom';

// Method 1: Wrapper component
function ProtectedRoute({ children }) {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <Spinner />;

  if (!user) {
    // Redirect to login, save current location for redirect back
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

// Method 2: Layout route (React Router v6)
function AuthLayout() {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <Spinner />;
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />;

  return <Outlet />;  // Renders child routes
}

// Usage
function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/public" element={<PublicPage />} />

      {/* Protected routes */}
      <Route element={<AuthLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

// Login page — redirect back after login
function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const handleLogin = async (credentials) => {
    await login(credentials);
    const from = location.state?.from?.pathname || '/dashboard';
    navigate(from, { replace: true });
  };
}
```

---

### Q8. What is Axios? How is it different from `fetch`?

**Answer:**

| Feature | fetch | Axios |
|---------|-------|-------|
| Built-in | ✅ | ❌ (npm install) |
| JSON auto-parse | ❌ | ✅ |
| Request interceptors | ❌ | ✅ |
| Response interceptors | ❌ | ✅ |
| Timeout | Manual | Built-in |
| Error on 4xx/5xx | ❌ (must check ok) | ✅ |
| Upload progress | ❌ | ✅ |

```jsx
// fetch — manual JSON parsing, manual error handling
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);  // Must check manually
  }
  return response.json();  // Must parse manually
}

// Axios — automatic JSON, throws on 4xx/5xx
import axios from 'axios';

async function fetchUser(id) {
  const { data } = await axios.get(`/api/users/${id}`);
  return data;  // Already parsed
}

// Axios instance with interceptors
const api = axios.create({
  baseURL: 'https://api.fractal.ai',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor — add auth token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor — handle errors globally
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      logout();
      navigate('/login');
    }
    return Promise.reject(error);
  }
);
```

---

### Q9. What is CORS? How does it affect React applications?

**Answer:**
CORS (Cross-Origin Resource Sharing) is a browser security mechanism that **restricts HTTP requests to different origins** (domain, protocol, or port).

```javascript
// CORS error: React app on localhost:3000 calling API on localhost:8000
// Browser blocks the request unless server allows it

// Server fix (Express.js)
const cors = require('cors');
app.use(cors({
  origin: ['http://localhost:3000', 'https://myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,  // Allow cookies
}));

// Development fix: proxy in package.json (CRA)
// package.json
{
  "proxy": "http://localhost:8000"
}
// Now /api/users → http://localhost:8000/api/users (no CORS)

// Vite proxy
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
}

// Preflight request — browser sends OPTIONS before POST/PUT
// Server must respond to OPTIONS with CORS headers
```

---

### Q10. What is a service worker? How does it enable offline functionality?

**Answer:**
A service worker is a **JavaScript file that runs in the background**, separate from the main thread. It can intercept network requests and cache responses.

```javascript
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(reg => console.log('SW registered'))
    .catch(err => console.error('SW failed:', err));
}

// sw.js — service worker
const CACHE_NAME = 'app-v1';
const STATIC_ASSETS = ['/', '/index.html', '/main.js', '/styles.css'];

// Install — cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
});

// Fetch — serve from cache, fall back to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;  // Cache hit

      return fetch(event.request).then(response => {
        // Cache new responses
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      });
    }).catch(() => caches.match('/offline.html'))  // Offline fallback
  );
});
```

---

### Q11. What is Webpack? What does it do?

**Answer:**
Webpack is a **module bundler** that takes your JavaScript modules (and other assets) and bundles them into optimized files for the browser.

```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js',  // Start point

  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',  // Cache busting
  },

  module: {
    rules: [
      // Transform JSX/TypeScript
      { test: /\.(js|jsx|ts|tsx)$/, use: 'babel-loader' },
      // Handle CSS
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
      // Handle images
      { test: /\.(png|jpg|svg)$/, type: 'asset/resource' },
    ],
  },

  plugins: [
    new HtmlWebpackPlugin({ template: './public/index.html' }),
  ],

  optimization: {
    splitChunks: {
      chunks: 'all',  // Code splitting
    },
  },
};

// What Webpack does:
// 1. Resolves module imports (import/require)
// 2. Transforms code (Babel, TypeScript, CSS)
// 3. Bundles everything into optimized files
// 4. Code splitting — separate vendor bundle
// 5. Tree shaking — removes unused code
// 6. Hot Module Replacement (HMR) in development
```

---

### Q12. What is Vite? How is it different from Webpack?

**Answer:**

| Feature | Webpack | Vite |
|---------|---------|------|
| Dev server startup | Slow (bundles everything) | Instant (native ESM) |
| HMR speed | Seconds | Milliseconds |
| Build tool | Webpack | Rollup |
| Config complexity | High | Low |
| Ecosystem | Mature | Growing |

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],

  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },

  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['recharts', 'd3'],
        },
      },
    },
  },
});

// Why Vite is faster in development:
// Webpack: bundles ALL modules before serving → slow startup
// Vite: serves modules as native ES modules → instant startup
// Only transforms files when requested by browser
// HMR: only updates the changed module, not the whole bundle
```

---

### Q13. What is TypeScript? Benefits with React?

**Answer:**
TypeScript is a **typed superset of JavaScript** that adds static type checking.

```tsx
// TypeScript with React
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'viewer';
}

interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  className?: string;
}

// Typed functional component
const UserCard: React.FC<UserCardProps> = ({ user, onEdit, className }) => {
  return (
    <div className={className}>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      {onEdit && (
        <button onClick={() => onEdit(user)}>Edit</button>
      )}
    </div>
  );
};

// Typed hooks
const [user, setUser] = useState<User | null>(null);
const [users, setUsers] = useState<User[]>([]);

// Typed custom hook
function useFetch<T>(url: string): {
  data: T | null;
  loading: boolean;
  error: string | null;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(url)
      .then(r => r.json() as Promise<T>)
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}

// Usage with type inference
const { data: user } = useFetch<User>('/api/users/1');
// user is typed as User | null
```

---

### Q14. What is React Router's `useLocation` and `useParams`?

**Answer:**

```jsx
import { useLocation, useParams, useSearchParams } from 'react-router-dom';

// useParams — access URL parameters
// Route: /users/:id/posts/:postId
function PostDetail() {
  const { id, postId } = useParams();
  return <div>User {id}, Post {postId}</div>;
}

// useLocation — access current URL info
function Analytics() {
  const location = useLocation();

  console.log(location.pathname);  // /users/123
  console.log(location.search);    // ?tab=posts&page=2
  console.log(location.hash);      // #section-1
  console.log(location.state);     // { from: '/login' }

  useEffect(() => {
    // Track page views
    analytics.page(location.pathname);
  }, [location.pathname]);

  return null;
}

// useSearchParams — access and update query string
function FilteredList() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filter = searchParams.get('filter') || 'all';
  const page = parseInt(searchParams.get('page') || '1');

  const updateFilter = (newFilter) => {
    setSearchParams({ filter: newFilter, page: '1' });
  };

  return (
    <div>
      <select value={filter} onChange={e => updateFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="active">Active</option>
      </select>
      <p>Page: {page}</p>
    </div>
  );
}
```

---

### Q15. What is accessibility (a11y) in React?

**Answer:**
Accessibility ensures your app is usable by people with disabilities (screen readers, keyboard navigation, etc.).

```jsx
// 1. Semantic HTML
function GoodForm() {
  return (
    <form>
      {/* ✅ label associated with input */}
      <label htmlFor="email">Email</label>
      <input id="email" type="email" />

      {/* ✅ button, not div */}
      <button type="submit">Submit</button>
    </form>
  );
}

// 2. ARIA attributes
function Modal({ isOpen, onClose, title, children }) {
  return isOpen ? (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-describedby="modal-content"
    >
      <h2 id="modal-title">{title}</h2>
      <div id="modal-content">{children}</div>
      <button onClick={onClose} aria-label="Close modal">×</button>
    </div>
  ) : null;
}

// 3. Keyboard navigation
function Dropdown({ options, onSelect }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') setIsOpen(false);
    if (e.key === 'Enter' || e.key === ' ') setIsOpen(o => !o);
  };

  return (
    <div>
      <button
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        onClick={() => setIsOpen(o => !o)}
        onKeyDown={handleKeyDown}
      >
        Select option
      </button>
      {isOpen && (
        <ul role="listbox">
          {options.map(opt => (
            <li
              key={opt.value}
              role="option"
              tabIndex={0}
              onClick={() => onSelect(opt)}
              onKeyDown={e => e.key === 'Enter' && onSelect(opt)}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// 4. Focus management
function FocusTrap({ children }) {
  const ref = useRef(null);

  useEffect(() => {
    const focusable = ref.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    focusable[0]?.focus();  // Focus first element
  }, []);

  return <div ref={ref}>{children}</div>;
}
```

---

<a name="hard"></a>
## 🔴 Hard

---

### Q16. What is micro-frontend architecture?

**Answer:**
Micro-frontends extend microservices to the frontend — **independent teams own independent parts** of the UI, each deployable separately.

```
Traditional monolith:
┌─────────────────────────────────┐
│         Single React App        │
│  Header + Sidebar + Dashboard   │
│  + Analytics + Reports + Admin  │
└─────────────────────────────────┘

Micro-frontends:
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Shell   │ │Analytics │ │ Reports  │
│  (host)  │ │  (MFE)   │ │  (MFE)   │
└──────────┘ └──────────┘ └──────────┘
     ↑ Composes all MFEs at runtime
```

```javascript
// Module Federation (Webpack 5) — most common approach
// analytics/webpack.config.js (remote)
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'analytics',
      filename: 'remoteEntry.js',
      exposes: {
        './Dashboard': './src/Dashboard',
        './Chart': './src/Chart',
      },
      shared: ['react', 'react-dom'],  // Share React to avoid duplicates
    }),
  ],
};

// shell/webpack.config.js (host)
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'shell',
      remotes: {
        analytics: 'analytics@http://analytics.fractal.ai/remoteEntry.js',
        reports: 'reports@http://reports.fractal.ai/remoteEntry.js',
      },
    }),
  ],
};

// shell/App.jsx
const AnalyticsDashboard = lazy(() => import('analytics/Dashboard'));
const ReportsPage = lazy(() => import('reports/ReportsPage'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/analytics" element={<AnalyticsDashboard />} />
        <Route path="/reports" element={<ReportsPage />} />
      </Routes>
    </Suspense>
  );
}
```

---

### Q17. What is the difference between monorepo and polyrepo?

**Answer:**

| | Monorepo | Polyrepo |
|-|---------|---------|
| Code location | Single repository | Multiple repositories |
| Code sharing | Easy | Harder (npm packages) |
| Atomic changes | ✅ | ❌ |
| CI/CD | More complex | Simpler per repo |
| Tools | Nx, Turborepo, pnpm workspaces | Standard git |

```
Monorepo structure:
my-company/
├── apps/
│   ├── web/          (React app)
│   ├── mobile/       (React Native)
│   └── admin/        (React app)
├── packages/
│   ├── ui/           (Shared components)
│   ├── utils/        (Shared utilities)
│   └── api-client/   (Shared API client)
└── package.json      (workspace root)
```

```json
// package.json (root) — pnpm workspaces
{
  "name": "my-company",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev --parallel",
    "test": "turbo run test"
  }
}
```

---

### Q18. What is a design system? Benefits?

**Answer:**
A design system is a **collection of reusable components, design tokens, and guidelines** that ensure consistency across products.

```jsx
// Design tokens — single source of truth for design values
// tokens.js
export const tokens = {
  colors: {
    primary: { 50: '#eff6ff', 500: '#3b82f6', 900: '#1e3a8a' },
    gray: { 50: '#f9fafb', 500: '#6b7280', 900: '#111827' },
  },
  spacing: { 1: '4px', 2: '8px', 4: '16px', 8: '32px' },
  typography: {
    fontSizes: { sm: '14px', md: '16px', lg: '18px', xl: '24px' },
    fontWeights: { normal: 400, medium: 500, bold: 700 },
  },
  borderRadius: { sm: '4px', md: '8px', lg: '16px', full: '9999px' },
};

// Component with design system
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled = false,
  children,
  onClick,
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded transition-colors';

  const variantStyles = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
    danger: 'bg-red-500 text-white hover:bg-red-600',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]}`}
      disabled={disabled || isLoading}
      onClick={onClick}
    >
      {isLoading && <Spinner className="mr-2" />}
      {children}
    </button>
  );
}
```

---

### Q19. What is PWA (Progressive Web App)?

**Answer:**
A PWA is a web app that uses modern web APIs to deliver **app-like experiences** — installable, offline-capable, push notifications.

```javascript
// PWA requirements:
// 1. HTTPS
// 2. Web App Manifest
// 3. Service Worker

// public/manifest.json
{
  "name": "Fractal Analytics",
  "short_name": "Fractal",
  "description": "AI-powered analytics platform",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}

// Install prompt
function InstallButton() {
  const [deferredPrompt, setDeferredPrompt] = useState(null);

  useEffect(() => {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    });
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    setDeferredPrompt(null);
  };

  if (!deferredPrompt) return null;
  return <button onClick={handleInstall}>Install App</button>;
}
```

---

### Q20. What is accessibility testing in React?

**Answer:**

```jsx
// 1. axe-core — automated accessibility testing
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('Button has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

// 2. React Testing Library — accessibility-first queries
import { render, screen } from '@testing-library/react';

test('Form is accessible', () => {
  render(<LoginForm />);

  // Query by accessible name (what screen readers announce)
  const emailInput = screen.getByLabelText('Email address');
  const submitButton = screen.getByRole('button', { name: 'Sign in' });

  expect(emailInput).toBeInTheDocument();
  expect(submitButton).toBeInTheDocument();
});

// 3. Manual testing checklist:
// ✅ Tab through all interactive elements
// ✅ All interactive elements reachable by keyboard
// ✅ Focus indicator visible
// ✅ Screen reader announces content correctly
// ✅ Color contrast ratio ≥ 4.5:1 (WCAG AA)
// ✅ Images have alt text
// ✅ Form errors announced to screen readers
```

---

### [← Back to Index](./00_INDEX.md) | [Next: React Testing →](./13_React_Testing.md)
