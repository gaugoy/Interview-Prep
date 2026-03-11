# ⚡ 11 — Performance Optimization
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q10)](#medium)
- [🔴 Hard (Q11–Q20)](#hard)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What causes unnecessary re-renders in React?

**Answer:**
A component re-renders when:
1. Its **state** changes (via setter)
2. Its **props** change — including new object/array references
3. Its **parent** re-renders (even if props didn't change)
4. A **context** it consumes changes

```jsx
import { useState, memo, useCallback, useMemo } from 'react';

function Parent() {
  const [count, setCount] = useState(0);

  // ❌ Cause 2: New object reference every render
  const config = { theme: 'dark' };  // New object each render

  // ❌ Cause 2: New function reference every render
  const handleClick = () => console.log('clicked');

  // ❌ Cause 3: Child re-renders because Parent re-renders
  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <Child config={config} onClick={handleClick} />
    </div>
  );
}

// Solutions:
function ParentOptimized() {
  const [count, setCount] = useState(0);

  // ✅ Stable object reference
  const config = useMemo(() => ({ theme: 'dark' }), []);

  // ✅ Stable function reference
  const handleClick = useCallback(() => console.log('clicked'), []);

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <MemoizedChild config={config} onClick={handleClick} />
    </div>
  );
}

// ✅ Prevent re-render when props haven't changed
const MemoizedChild = memo(function Child({ config, onClick }) {
  console.log('Child rendered');
  return <button onClick={onClick}>{config.theme}</button>;
});
```

---

### Q2. How does `React.memo` prevent re-renders?

**Answer:**
`React.memo` wraps a component and **skips re-rendering if props haven't changed** (shallow comparison by default).

```jsx
import { memo, useState } from 'react';

// Without memo — re-renders every time parent renders
function ExpensiveList({ items }) {
  console.log('ExpensiveList rendered');
  return <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>;
}

// With memo — only re-renders when items changes
const ExpensiveList = memo(function ExpensiveList({ items }) {
  console.log('ExpensiveList rendered');
  return <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>;
});

// ⚠️ Shallow comparison — objects/arrays must be same reference
function Parent() {
  const [count, setCount] = useState(0);
  const items = [{ id: 1, name: 'Alice' }];  // ❌ New array every render!

  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <ExpensiveList items={items} />  {/* Still re-renders! */}
    </>
  );
}

// ✅ Fix: stable reference
function ParentFixed() {
  const [count, setCount] = useState(0);
  const items = useMemo(() => [{ id: 1, name: 'Alice' }], []);

  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <ExpensiveList items={items} />  {/* Won't re-render */}
    </>
  );
}

// Custom comparison
const SmartComponent = memo(
  function SmartComponent({ user, data }) {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => {
    // Return true = skip re-render
    return prevProps.user.id === nextProps.user.id &&
           prevProps.data.length === nextProps.data.length;
  }
);
```

---

### Q3. What is code splitting? Why is it important?

**Answer:**
Code splitting breaks your JavaScript bundle into **smaller chunks** that are loaded on demand, reducing initial load time.

```jsx
import { lazy, Suspense, useState } from 'react';

// Without code splitting — entire app in one bundle
import HeavyDashboard from './HeavyDashboard';  // Always loaded

// With code splitting — loaded only when needed
const HeavyDashboard = lazy(() => import('./HeavyDashboard'));
const AnalyticsPage = lazy(() => import('./pages/Analytics'));
const ReportsPage = lazy(() => import('./pages/Reports'));

// Suspense provides fallback while loading
function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  return (
    <div>
      <button onClick={() => setShowDashboard(true)}>Load Dashboard</button>

      {showDashboard && (
        <Suspense fallback={<div>Loading dashboard...</div>}>
          <HeavyDashboard />
        </Suspense>
      )}
    </div>
  );
}

// Route-based splitting — most common pattern
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Analytics = lazy(() => import('./pages/Analytics'));

function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

// Named export
const Chart = lazy(() =>
  import('./components/Chart').then(module => ({
    default: module.Chart  // Named export → default
  }))
);
```

---

### Q4. What is virtual scrolling (windowing)?

**Answer:**
Virtual scrolling renders **only the visible items** in a list, not all items. Essential for lists with thousands of items.

```jsx
import { FixedSizeList, VariableSizeList } from 'react-window';
import { useCallback } from 'react';

// Fixed height items
function VirtualList({ items }) {
  const Row = useCallback(({ index, style }) => (
    <div style={style} className="row">
      <span>{items[index].name}</span>
      <span>{items[index].value}</span>
    </div>
  ), [items]);

  return (
    <FixedSizeList
      height={600}           // Visible area height (px)
      width="100%"
      itemCount={items.length}
      itemSize={50}          // Each row height (px)
      overscanCount={5}      // Extra rows to render above/below
    >
      {Row}
    </FixedSizeList>
  );
}

// Variable height items
function VariableList({ items }) {
  const getItemSize = useCallback(index => {
    return items[index].isExpanded ? 100 : 50;
  }, [items]);

  return (
    <VariableSizeList
      height={600}
      width="100%"
      itemCount={items.length}
      itemSize={getItemSize}
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </VariableSizeList>
  );
}

// Without virtualization: 10,000 items = 10,000 DOM nodes
// With virtualization: 10,000 items = ~20 DOM nodes (only visible)
// Performance improvement: 50-100x for large lists
```

---

### Q5. What is the difference between debouncing and throttling?

**Answer:**
- **Debouncing** — delays execution until after a pause in calls (fires once after user stops)
- **Throttling** — limits execution to at most once per time period (fires at regular intervals)

```jsx
import { useState, useEffect, useCallback, useRef } from 'react';

// DEBOUNCE — wait until user stops typing
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);  // Cancel on new value
  }, [value, delay]);

  return debouncedValue;
}

// THROTTLE — limit to once per interval
function useThrottle(value, interval) {
  const [throttledValue, setThrottledValue] = useState(value);
  const lastUpdated = useRef(Date.now());

  useEffect(() => {
    const now = Date.now();
    if (now >= lastUpdated.current + interval) {
      lastUpdated.current = now;
      setThrottledValue(value);
    } else {
      const timer = setTimeout(() => {
        lastUpdated.current = Date.now();
        setThrottledValue(value);
      }, interval - (now - lastUpdated.current));
      return () => clearTimeout(timer);
    }
  }, [value, interval]);

  return throttledValue;
}

// Usage
function SearchBar() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);  // Search after 300ms pause

  useEffect(() => {
    if (debouncedQuery) fetchResults(debouncedQuery);
  }, [debouncedQuery]);

  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);
  const throttledScrollY = useThrottle(scrollY, 100);  // Max 10 updates/sec

  useEffect(() => {
    const handler = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handler);
    return () => window.removeEventListener('scroll', handler);
  }, []);

  return <p>Scroll: {throttledScrollY}px</p>;
}

// When to use:
// Debounce: search input, form validation, resize handler
// Throttle: scroll events, mouse move, game loop
```

---

### Q6. What is lazy loading? How does it apply to images and components?

**Answer:**
Lazy loading defers loading of resources until they're **actually needed** (visible or about to be visible).

```jsx
// Lazy loading images — native HTML
function ImageGallery({ images }) {
  return (
    <div>
      {images.map(img => (
        <img
          key={img.id}
          src={img.url}
          loading="lazy"        // Native browser lazy loading
          alt={img.alt}
          width={300}
          height={200}
        />
      ))}
    </div>
  );
}

// Lazy loading with Intersection Observer (more control)
function LazyImage({ src, alt }) {
  const [isVisible, setIsVisible] = useState(false);
  const imgRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();  // Stop observing once loaded
        }
      },
      { rootMargin: '200px' }  // Start loading 200px before visible
    );

    if (imgRef.current) observer.observe(imgRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={imgRef} style={{ minHeight: 200 }}>
      {isVisible ? (
        <img src={src} alt={alt} />
      ) : (
        <div className="placeholder" />
      )}
    </div>
  );
}

// Lazy loading components — React.lazy
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<ChartSkeleton />}>
          <HeavyChart />
        </Suspense>
      )}
    </>
  );
}
```

---

### Q7. What is a skeleton screen? Why is it better than a spinner?

**Answer:**
A skeleton screen shows a **placeholder that mimics the layout** of the content being loaded. It's better than a spinner because it reduces perceived loading time and prevents layout shift.

```jsx
// Spinner — user doesn't know what's coming
function WithSpinner({ isLoading, children }) {
  if (isLoading) return <div className="spinner" />;
  return children;
}

// Skeleton — user sees the shape of content
function UserCardSkeleton() {
  return (
    <div className="user-card skeleton">
      <div className="skeleton-avatar" />
      <div className="skeleton-content">
        <div className="skeleton-line skeleton-line--title" />
        <div className="skeleton-line skeleton-line--subtitle" />
        <div className="skeleton-line skeleton-line--text" />
      </div>
    </div>
  );
}

// CSS for skeleton animation
// .skeleton-line {
//   background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
//   background-size: 200% 100%;
//   animation: shimmer 1.5s infinite;
// }
// @keyframes shimmer {
//   0% { background-position: 200% 0; }
//   100% { background-position: -200% 0; }
// }

function UserList({ userId }) {
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <UserCardSkeleton />;
  return <UserCard user={user} />;
}
```

---

### Q8. What is tree shaking? How does it reduce bundle size?

**Answer:**
Tree shaking is a **dead code elimination** technique that removes unused exports from your bundle during build time.

```javascript
// ❌ Imports entire lodash (~70KB)
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ Imports only debounce (~2KB) — tree-shakeable
import debounce from 'lodash/debounce';
// or
import { debounce } from 'lodash-es';  // ES modules required for tree shaking

// ❌ Named import from CommonJS — NOT tree-shakeable
import { debounce } from 'lodash';  // Still imports all of lodash

// ✅ Named import from ES module — tree-shakeable
import { debounce } from 'lodash-es';

// Your own code — tree shaking works automatically with ES modules
// utils.js
export function used() { return 'used'; }
export function unused() { return 'unused'; }  // Removed by tree shaking

// main.js
import { used } from './utils';  // 'unused' is not included in bundle
```

---

### Q9. What is the difference between debouncing and throttling?

> See Q5 above for the full answer.

---

### Q10. What is a skeleton screen vs spinner?

> See Q7 above for the full answer.

---

<a name="hard"></a>
## 🔴 Hard

---

### Q11. What is the React Profiler? How do you use it?

**Answer:**
The React Profiler measures **how often components render and the cost of each render**. Available in React DevTools and as a `<Profiler>` component.

```jsx
import { Profiler } from 'react';

// Profiler component — wrap any subtree
function onRenderCallback(
  id,           // Component tree identifier
  phase,        // "mount" or "update"
  actualDuration,  // Time spent rendering
  baseDuration,    // Estimated time without memoization
  startTime,
  commitTime
) {
  console.log(`${id} (${phase}): ${actualDuration.toFixed(2)}ms`);
  // Log to analytics if actualDuration > threshold
  if (actualDuration > 16) {  // > 1 frame (60fps)
    analytics.track('slow_render', { component: id, duration: actualDuration });
  }
}

function App() {
  return (
    <Profiler id="Dashboard" onRender={onRenderCallback}>
      <Dashboard />
    </Profiler>
  );
}

// React DevTools Profiler:
// 1. Open DevTools → Profiler tab
// 2. Click Record
// 3. Interact with app
// 4. Stop recording
// 5. Analyze flame graph — wide bars = slow renders
// 6. Look for components that render too often

// Common findings:
// - Component renders 50 times when it should render 5
// - Expensive computation runs on every render
// - Large list re-renders when only one item changes
```

---

### Q12. What is the difference between TTI and FCP?

**Answer:**

| Metric | Full Name | Measures | Good |
|--------|-----------|---------|------|
| **FCP** | First Contentful Paint | When first content appears | < 1.8s |
| **LCP** | Largest Contentful Paint | When main content loads | < 2.5s |
| **TTI** | Time to Interactive | When page is fully interactive | < 3.8s |
| **CLS** | Cumulative Layout Shift | Visual stability | < 0.1 |
| **FID/INP** | Interaction to Next Paint | Input responsiveness | < 200ms |

```jsx
// Measuring Core Web Vitals in React
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function reportWebVitals(metric) {
  console.log(metric);
  // Send to analytics
  analytics.track('web_vital', {
    name: metric.name,
    value: metric.value,
    rating: metric.rating,  // 'good', 'needs-improvement', 'poor'
  });
}

getCLS(reportWebVitals);
getFID(reportWebVitals);
getFCP(reportWebVitals);
getLCP(reportWebVitals);
getTTFB(reportWebVitals);

// Improving metrics:
// FCP: Reduce render-blocking resources, use skeleton screens
// LCP: Optimize images, preload critical resources
// TTI: Code split, reduce JS bundle size
// CLS: Set explicit dimensions on images/videos
```

---

### Q13. What is hydration in React? SSR vs CSR?

**Answer:**

| | CSR (Client-Side Rendering) | SSR (Server-Side Rendering) |
|-|---------------------------|---------------------------|
| Initial HTML | Empty shell | Full HTML |
| First paint | Slow (wait for JS) | Fast |
| Interactivity | After JS loads | After hydration |
| SEO | Poor | Good |
| Server load | Low | High |

```jsx
// CSR — React renders everything in browser
// index.html: <div id="root"></div>
// React fills it in after JS loads

// SSR — Server renders HTML, React "hydrates" it
// Server sends: <div id="root"><h1>Hello Alice</h1>...</div>
// React attaches event listeners to existing HTML (hydration)

// Hydration mismatch — common bug
// Server renders: <p>Server time: 12:00:00</p>
// Client renders: <p>Server time: 12:00:01</p>
// React throws hydration error!

// Fix: suppress hydration warning for dynamic content
function TimeDisplay() {
  return (
    <p suppressHydrationWarning>
      {new Date().toLocaleTimeString()}
    </p>
  );
}

// Or use useEffect for client-only content
function ClientOnly({ children }) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;
  return children;
}
```

---

### Q14. What is React Server Components (RSC)?

**Answer:**
React Server Components run **exclusively on the server** — they can access databases, file systems, and APIs directly without sending the code to the client.

```jsx
// Server Component (default in Next.js 13+ App Router)
// No 'use client' directive = Server Component
async function UserProfile({ userId }) {
  // ✅ Direct database access — no API needed!
  const user = await db.users.findById(userId);

  // ✅ No JS sent to client for this component
  // ✅ Can use async/await directly
  // ❌ Cannot use useState, useEffect, event handlers

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
      {/* Client component for interactivity */}
      <FollowButton userId={userId} />
    </div>
  );
}

// Client Component — 'use client' directive
'use client';

function FollowButton({ userId }) {
  const [isFollowing, setIsFollowing] = useState(false);

  return (
    <button onClick={() => setIsFollowing(f => !f)}>
      {isFollowing ? 'Unfollow' : 'Follow'}
    </button>
  );
}

// Benefits of RSC:
// ✅ Zero bundle size for server components
// ✅ Direct data access (no API layer needed)
// ✅ Automatic code splitting
// ✅ Better performance (less JS to download)
```

---

### Q15. What is concurrent rendering in React 18?

**Answer:**
Concurrent rendering allows React to **interrupt, pause, and resume rendering**, keeping the UI responsive during expensive updates.

```jsx
import { startTransition, useTransition, useDeferredValue } from 'react';

// Before React 18: rendering was synchronous (blocking)
// React 18: rendering can be interrupted

// startTransition — mark non-urgent updates
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    setQuery(e.target.value);  // Urgent: update input immediately

    startTransition(() => {
      // Non-urgent: can be interrupted if user types again
      setResults(searchDatabase(e.target.value));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <Results data={results} />
    </>
  );
}

// Automatic batching (React 18)
// Before: only batched in event handlers
// After: batches ALL state updates (including setTimeout, Promises)

setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // React 18: single re-render (batched)
  // React 17: two re-renders
}, 1000);
```

---

### Q16. What is `startTransition`? How does it improve UX?

**Answer:**
`startTransition` marks state updates as **non-urgent transitions**, allowing React to prioritize urgent updates (like typing) over expensive ones (like filtering a large list).

```jsx
import { useState, startTransition, useTransition } from 'react';

// Without startTransition — typing feels laggy
function SlowSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(allItems);

  const handleChange = (e) => {
    setQuery(e.target.value);
    // This expensive filter blocks the input update!
    setResults(allItems.filter(item =>
      item.name.toLowerCase().includes(e.target.value.toLowerCase())
    ));
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      <List items={results} />  {/* 10,000 items */}
    </>
  );
}

// With startTransition — input stays responsive
function FastSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(allItems);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    const value = e.target.value;

    // Urgent: update input immediately (user sees their typing)
    setQuery(value);

    // Non-urgent: can be interrupted if user types again
    startTransition(() => {
      setResults(allItems.filter(item =>
        item.name.toLowerCase().includes(value.toLowerCase())
      ));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending ? <Spinner /> : <List items={results} />}
    </>
  );
}
```

---

### Q17. What is the impact of context on performance?

**Answer:**
Every component that consumes a context **re-renders when the context value changes**, even if it only uses part of the value.

```jsx
// ❌ Performance problem: one big context
const AppContext = createContext(null);

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [cart, setCart] = useState([]);

  // When cart changes, ALL consumers re-render (even those only using theme)
  return (
    <AppContext.Provider value={{ user, theme, cart, setUser, setTheme, setCart }}>
      {children}
    </AppContext.Provider>
  );
}

// ✅ Solution 1: Split contexts by update frequency
const UserContext = createContext(null);    // Changes rarely
const ThemeContext = createContext(null);   // Changes rarely
const CartContext = createContext(null);    // Changes often

// ✅ Solution 2: Memoize context value
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const value = useMemo(() => ({
    theme,
    setTheme,
  }), [theme]);  // Only new object when theme changes

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

// ✅ Solution 3: Use Zustand for high-frequency updates
// Zustand has fine-grained subscriptions — only re-renders when subscribed value changes
const useStore = create(set => ({
  cart: [],
  addToCart: (item) => set(state => ({ cart: [...state.cart, item] })),
}));

function CartIcon() {
  const cartCount = useStore(state => state.cart.length);  // Only re-renders when count changes
  return <span>{cartCount}</span>;
}
```

---

### Q18. What is memoization at component level vs hook level?

**Answer:**

```jsx
// Component level: React.memo
// Prevents re-render when props haven't changed
const ExpensiveComponent = memo(function({ data, onAction }) {
  return <div>{data.map(/* expensive render */)}</div>;
});

// Hook level: useMemo
// Prevents expensive computation on every render
function Component({ rawData, filter }) {
  // Computed value — only recalculates when rawData or filter changes
  const processedData = useMemo(() => {
    return rawData
      .filter(item => item.category === filter)
      .sort((a, b) => b.score - a.score)
      .slice(0, 100);
  }, [rawData, filter]);

  return <List items={processedData} />;
}

// Hook level: useCallback
// Prevents new function reference on every render
function Parent({ items }) {
  const handleDelete = useCallback((id) => {
    // Stable reference — MemoizedChild won't re-render
    setItems(prev => prev.filter(i => i.id !== id));
  }, []);

  return <MemoizedChild items={items} onDelete={handleDelete} />;
}

// When to use each:
// React.memo: when component is expensive to render AND receives stable props
// useMemo: when computation is expensive (>1ms) AND deps change infrequently
// useCallback: when passing callbacks to memoized children
```

---

### Q19. How would you optimize a list of 10,000 items?

**Answer:**

```jsx
import { FixedSizeList } from 'react-window';
import { memo, useCallback, useMemo } from 'react';

// Strategy 1: Virtual scrolling (most impactful)
function VirtualizedList({ items, onItemClick }) {
  const Row = useCallback(({ index, style }) => (
    <div style={style} onClick={() => onItemClick(items[index].id)}>
      <span>{items[index].name}</span>
      <span>{items[index].value}</span>
    </div>
  ), [items, onItemClick]);

  return (
    <FixedSizeList
      height={600}
      width="100%"
      itemCount={items.length}
      itemSize={50}
    >
      {Row}
    </FixedSizeList>
  );
}

// Strategy 2: Pagination
function PaginatedList({ items, pageSize = 50 }) {
  const [page, setPage] = useState(0);
  const visibleItems = useMemo(
    () => items.slice(page * pageSize, (page + 1) * pageSize),
    [items, page, pageSize]
  );

  return (
    <>
      {visibleItems.map(item => <Item key={item.id} item={item} />)}
      <Pagination
        total={items.length}
        pageSize={pageSize}
        current={page}
        onChange={setPage}
      />
    </>
  );
}

// Strategy 3: Infinite scroll
function InfiniteList({ fetchMore }) {
  const [items, setItems] = useState([]);
  const loaderRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          fetchMore().then(newItems =>
            setItems(prev => [...prev, ...newItems])
          );
        }
      },
      { threshold: 0.1 }
    );

    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => observer.disconnect();
  }, [fetchMore]);

  return (
    <>
      {items.map(item => <Item key={item.id} item={item} />)}
      <div ref={loaderRef}>Loading more...</div>
    </>
  );
}
```

---

### Q20. What is the React DevTools Profiler and how do you use it?

**Answer:**

```
Steps to profile a React app:
1. Install React DevTools browser extension
2. Open DevTools → "⚛️ Profiler" tab
3. Click the record button (●)
4. Interact with the app (click buttons, type, navigate)
5. Click stop (■)
6. Analyze results:
   - Flame graph: width = render time, color = slow (red) to fast (green)
   - Ranked chart: components sorted by render time
   - Component chart: how often a component rendered

Key things to look for:
- Components that render too frequently
- Components with long render times (>16ms = drops below 60fps)
- Unnecessary re-renders (gray = no change needed)

Common fixes after profiling:
- Add React.memo to frequently re-rendering components
- Add useMemo for expensive computations
- Add useCallback for callbacks passed to memoized children
- Split large components into smaller ones
- Move state closer to where it's used
```

```jsx
// Programmatic profiling
import { Profiler } from 'react';

const onRender = (id, phase, actualDuration) => {
  if (actualDuration > 16) {
    console.warn(`Slow render: ${id} took ${actualDuration.toFixed(2)}ms`);
  }
};

function App() {
  return (
    <Profiler id="App" onRender={onRender}>
      <Dashboard />
    </Profiler>
  );
}
```

---

### [← Back to Index](./00_INDEX.md) | [Next: React Architecture →](./12_React_Architecture.md)
