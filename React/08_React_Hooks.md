# 🪝 08 — React Hooks
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟢 Easy (Q1–Q10)](#easy)
- [🟡 Medium (Q11–Q20)](#medium)
- [🔴 Hard (Q21–Q25)](#hard)

---

<a name="easy"></a>
## 🟢 Easy

---

### Q1. What are React hooks? Why were they introduced?

**Answer:**
Hooks are **functions that let functional components use state and lifecycle features** previously only available in class components.

**Why introduced (React 16.8, 2019):**
1. **Reuse stateful logic** — HOCs and render props were complex
2. **Avoid class complexity** — `this`, binding, lifecycle confusion
3. **Better code organization** — related logic stays together

```jsx
// Rules of Hooks (must follow):
// 1. Only call hooks at the TOP LEVEL (not inside loops, conditions, nested functions)
// 2. Only call hooks from REACT FUNCTIONS (not regular JS functions)

// ❌ Wrong — conditional hook call
function Bad({ condition }) {
  if (condition) {
    const [state, setState] = useState(0);  // Breaks rules!
  }
}

// ✅ Correct — always call at top level
function Good({ condition }) {
  const [state, setState] = useState(0);  // Always called
  if (condition) {
    // Use state here
  }
}
```

---

### Q2. What are the rules of hooks?

**Answer:**
1. **Only call hooks at the top level** — not inside loops, conditions, or nested functions
2. **Only call hooks from React functions** — functional components or custom hooks

```jsx
// Why these rules exist:
// React relies on the ORDER of hook calls to associate state with the right hook
// If hooks are called conditionally, the order can change between renders

// React internally tracks hooks as a linked list:
// Render 1: useState(0) → useEffect → useState('')
// Render 2: useState(0) → useEffect → useState('')  ← must match!

// ❌ Breaks order — React can't match hooks correctly
function BrokenComponent({ showExtra }) {
  const [a, setA] = useState(0);
  if (showExtra) {
    const [b, setB] = useState('');  // Conditional hook!
  }
  const [c, setC] = useState(false);
  // If showExtra changes: hook order changes → React throws error
}

// ✅ Move condition inside the hook usage
function FixedComponent({ showExtra }) {
  const [a, setA] = useState(0);
  const [b, setB] = useState('');   // Always called
  const [c, setC] = useState(false);

  // Use b conditionally
  if (showExtra) {
    console.log(b);
  }
}
```

---

### Q3. What is `useState`? What does it return?

**Answer:**
`useState` adds **local state** to a functional component. It returns a tuple: `[currentValue, setterFunction]`.

```jsx
import { useState } from 'react';

function Counter() {
  // Returns [state, setState]
  const [count, setCount] = useState(0);  // 0 is initial value

  // Setter: direct value
  const increment = () => setCount(count + 1);

  // Setter: functional update (preferred when new state depends on old)
  const incrementSafe = () => setCount(prev => prev + 1);

  // Multiple state variables
  const [name, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Object state — must spread to avoid losing other fields
  const [user, setUser] = useState({ name: '', age: 0, email: '' });
  const updateName = (name) => setUser(prev => ({ ...prev, name }));

  // Lazy initialization — function runs only on first render
  const [expensiveState] = useState(() => computeExpensiveValue());

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={incrementSafe}>+</button>
    </div>
  );
}

// ⚠️ State updates are ASYNCHRONOUS — don't read state right after setting
function Async() {
  const [count, setCount] = useState(0);

  const handleClick = () => {
    setCount(count + 1);
    console.log(count);  // Still 0! State hasn't updated yet
    // Use useEffect to react to state changes
  };
}
```

---

### Q4. What is `useEffect`? What is it used for?

**Answer:**
`useEffect` lets you perform **side effects** in functional components — data fetching, subscriptions, DOM manipulation, timers.

```jsx
import { useState, useEffect } from 'react';

function DataFetcher({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Side effect: fetch data
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(setUser);

    // Cleanup function (optional)
    return () => {
      // Cancel subscriptions, clear timers, abort requests
    };
  }, [userId]);  // Dependency array

  return <div>{user?.name}</div>;
}

// Common use cases:
// 1. Data fetching
// 2. Setting up subscriptions (WebSocket, EventEmitter)
// 3. Manually changing the DOM (document.title)
// 4. Setting up timers
// 5. Logging/analytics
```

---

### Q5. What is the difference between `useEffect` with no deps, `[]`, and `[deps]`?

**Answer:**

| Pattern | When it runs |
|---------|-------------|
| `useEffect(fn)` | After **every** render |
| `useEffect(fn, [])` | Once after **mount** only |
| `useEffect(fn, [a, b])` | After mount + when `a` or `b` changes |

```jsx
function Examples({ id, name }) {
  // Pattern 1: No dependency array — runs after EVERY render
  useEffect(() => {
    console.log('Runs after every render');
  });

  // Pattern 2: Empty array — runs ONCE after mount
  useEffect(() => {
    console.log('Runs once on mount');
    const timer = setInterval(() => console.log('tick'), 1000);
    return () => clearInterval(timer);  // Cleanup on unmount
  }, []);

  // Pattern 3: With dependencies — runs when deps change
  useEffect(() => {
    console.log(`id or name changed: ${id}, ${name}`);
    fetchData(id);
  }, [id, name]);  // Re-runs when id OR name changes

  // ⚠️ Missing dependency — stale closure bug
  useEffect(() => {
    // Uses 'id' but doesn't list it as dependency
    // Will always use the initial value of id!
    fetchData(id);  // ❌ id might be stale
  }, []);  // Should be [id]
}
```

---

### Q6. What is the cleanup function in `useEffect`?

**Answer:**
The cleanup function runs **before the component unmounts** and **before the effect re-runs** (when dependencies change). It prevents memory leaks.

```jsx
import { useState, useEffect } from 'react';

function ChatRoom({ roomId }) {
  useEffect(() => {
    // Setup
    const connection = createConnection(roomId);
    connection.connect();
    console.log(`Connected to room ${roomId}`);

    // Cleanup — runs when:
    // 1. Component unmounts
    // 2. roomId changes (before re-running effect)
    return () => {
      connection.disconnect();
      console.log(`Disconnected from room ${roomId}`);
    };
  }, [roomId]);

  return <div>Room: {roomId}</div>;
}

// Cleanup for timers
function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);

    return () => clearInterval(interval);  // Prevent memory leak
  }, []);

  return <p>Seconds: {seconds}</p>;
}

// Cleanup for event listeners
function WindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth });

  useEffect(() => {
    const handleResize = () => setSize({ width: window.innerWidth });
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return <p>Width: {size.width}</p>;
}
```

---

### Q7. What is `useRef`? What are its two main use cases?

**Answer:**
`useRef` returns a **mutable ref object** whose `.current` property persists across renders **without triggering re-renders**.

**Two main use cases:**
1. **DOM access** — get a reference to a DOM element
2. **Mutable value** — store a value that persists across renders without causing re-renders

```jsx
import { useRef, useEffect, useState } from 'react';

// Use case 1: DOM access
function AutoFocusInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current.focus();  // Focus on mount
  }, []);

  return <input ref={inputRef} placeholder="Auto-focused" />;
}

// Use case 2: Mutable value (no re-render)
function StopWatch() {
  const [time, setTime] = useState(0);
  const intervalRef = useRef(null);  // Store interval ID

  const start = () => {
    intervalRef.current = setInterval(() => {
      setTime(t => t + 1);
    }, 1000);
  };

  const stop = () => {
    clearInterval(intervalRef.current);
  };

  return (
    <div>
      <p>Time: {time}s</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  );
}

// Track previous value
function usePrevious(value) {
  const ref = useRef();
  useEffect(() => {
    ref.current = value;  // Update after render
  });
  return ref.current;  // Returns previous value
}

function Component({ count }) {
  const prevCount = usePrevious(count);
  return <p>Now: {count}, Before: {prevCount}</p>;
}
```

---

### Q8. What is the difference between `useState` and `useRef`?

**Answer:**

| Feature | `useState` | `useRef` |
|---------|-----------|---------|
| Triggers re-render | ✅ Yes | ❌ No |
| Persists across renders | ✅ Yes | ✅ Yes |
| Mutable | Via setter only | Direct mutation |
| Use for | UI state | DOM refs, timers, previous values |

```jsx
function Comparison() {
  const [stateCount, setStateCount] = useState(0);
  const refCount = useRef(0);

  const incrementState = () => {
    setStateCount(c => c + 1);  // Triggers re-render
  };

  const incrementRef = () => {
    refCount.current += 1;  // No re-render!
    console.log(refCount.current);  // Updated immediately
  };

  console.log('Rendered!');  // Only logs when stateCount changes

  return (
    <div>
      <p>State: {stateCount}</p>
      <p>Ref: {refCount.current}</p>  {/* Won't update in UI without re-render */}
      <button onClick={incrementState}>State +1</button>
      <button onClick={incrementRef}>Ref +1 (no re-render)</button>
    </div>
  );
}
```

---

### Q9. What is `useContext`? How does it work?

**Answer:**
`useContext` subscribes a component to a **React context**, allowing it to read the context value without prop drilling.

```jsx
import { createContext, useContext, useState } from 'react';

// 1. Create context
const AuthContext = createContext(null);

// 2. Provide context
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async (credentials) => {
    const user = await authenticate(credentials);
    setUser(user);
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// 3. Custom hook for consuming context (best practice)
function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// 4. Consume anywhere in the tree
function UserMenu() {
  const { user, logout } = useAuth();  // No prop drilling!

  if (!user) return <LoginButton />;
  return (
    <div>
      <span>Hello, {user.name}</span>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

// App setup
function App() {
  return (
    <AuthProvider>
      <Header />  {/* UserMenu is deep inside Header */}
    </AuthProvider>
  );
}
```

---

### Q10. What is `useReducer`? How is it different from `useState`?

**Answer:**
`useReducer` manages **complex state logic** using a reducer function (like Redux). Prefer it when state has multiple sub-values or complex transitions.

```jsx
import { useReducer } from 'react';

// Reducer — pure function: (state, action) → newState
function counterReducer(state, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    case 'RESET':
      return { count: 0 };
    case 'SET':
      return { count: action.payload };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>+</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>-</button>
      <button onClick={() => dispatch({ type: 'RESET' })}>Reset</button>
      <button onClick={() => dispatch({ type: 'SET', payload: 10 })}>Set 10</button>
    </div>
  );
}

// When to use useReducer vs useState:
// useState: simple values, independent state variables
// useReducer: ✅ multiple related state values
//             ✅ next state depends on previous
//             ✅ complex state transitions
//             ✅ want to separate state logic from UI
```

---

<a name="medium"></a>
## 🟡 Medium

---

### Q11. What is `useMemo`? What problem does it solve?

**Answer:**
`useMemo` **memoizes the result of an expensive computation**, recalculating only when dependencies change.

```jsx
import { useState, useMemo } from 'react';

function DataDashboard({ data, filter, sortBy }) {
  // ❌ Without useMemo — recalculates on EVERY render
  const processedData = data
    .filter(item => item.category === filter)
    .sort((a, b) => a[sortBy] - b[sortBy]);

  // ✅ With useMemo — only recalculates when data, filter, or sortBy changes
  const processedData2 = useMemo(() => {
    console.log('Processing data...');
    return data
      .filter(item => item.category === filter)
      .sort((a, b) => a[sortBy] - b[sortBy]);
  }, [data, filter, sortBy]);

  // Derived statistics
  const stats = useMemo(() => ({
    count: processedData2.length,
    total: processedData2.reduce((sum, item) => sum + item.value, 0),
    avg: processedData2.length
      ? processedData2.reduce((sum, item) => sum + item.value, 0) / processedData2.length
      : 0,
  }), [processedData2]);

  return (
    <div>
      <p>Count: {stats.count}, Avg: {stats.avg.toFixed(2)}</p>
      {processedData2.map(item => <Row key={item.id} item={item} />)}
    </div>
  );
}

// useMemo vs useCallback:
// useMemo   → memoizes a VALUE (result of computation)
// useCallback → memoizes a FUNCTION (reference)
```

---

### Q12. What is `useCallback`? How is it different from `useMemo`?

**Answer:**
`useCallback` **memoizes a function reference**, preventing it from being recreated on every render. Essential when passing callbacks to memoized child components.

```jsx
import { useState, useCallback, memo } from 'react';

// Without useCallback — new function reference every render
function Parent() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState([]);

  // ❌ New function on every render → ChildList always re-renders
  const handleDelete = (id) => {
    setItems(prev => prev.filter(i => i.id !== id));
  };

  // ✅ Stable function reference → ChildList only re-renders when needed
  const handleDelete2 = useCallback((id) => {
    setItems(prev => prev.filter(i => i.id !== id));
  }, []);  // No deps because we use functional update

  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <ChildList items={items} onDelete={handleDelete2} />
    </>
  );
}

// memo prevents re-render if props haven't changed
const ChildList = memo(function ChildList({ items, onDelete }) {
  console.log('ChildList rendered');
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          {item.name}
          <button onClick={() => onDelete(item.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
});

// Summary:
// useMemo(() => computeValue(), [deps])   → memoized VALUE
// useCallback(() => doSomething(), [deps]) → memoized FUNCTION
// useCallback(fn, deps) === useMemo(() => fn, deps)
```

---

### Q13. When should you use `useMemo` vs `useCallback`?

**Answer:**

```jsx
// Use useMemo when:
// ✅ Expensive computation (filtering, sorting large arrays)
// ✅ Creating objects/arrays passed to memoized children
// ✅ Derived state that's expensive to compute

const filteredData = useMemo(() =>
  largeDataset.filter(item => item.active),
  [largeDataset]
);

const chartConfig = useMemo(() => ({
  data: processedData,
  options: { responsive: true, ... }
}), [processedData]);

// Use useCallback when:
// ✅ Passing callbacks to memoized child components
// ✅ Callbacks used as useEffect dependencies
// ✅ Event handlers that are expensive to create

const handleSubmit = useCallback(async (formData) => {
  await submitForm(formData);
  onSuccess();
}, [onSuccess]);

// ⚠️ DON'T over-optimize:
// - useMemo/useCallback have their own cost (memory + comparison)
// - Only use when you have a measurable performance problem
// - Profile first with React DevTools Profiler

// Rule of thumb:
// 1. Write code without memoization
// 2. Measure performance
// 3. Add memoization only where it helps
```

---

### Q14. What is a custom hook? What are the rules?

**Answer:**
A custom hook is a **JavaScript function starting with `use`** that can call other hooks. It extracts reusable stateful logic from components.

```jsx
import { useState, useEffect, useCallback } from 'react';

// Custom hook: useFetch
function useFetch(url) {
  const [state, setState] = useState({
    data: null,
    loading: true,
    error: null,
  });

  const [refetchIndex, setRefetchIndex] = useState(0);

  const refetch = useCallback(() => setRefetchIndex(i => i + 1), []);

  useEffect(() => {
    if (!url) return;

    const controller = new AbortController();
    setState(prev => ({ ...prev, loading: true, error: null }));

    fetch(url, { signal: controller.signal })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => setState({ data, loading: false, error: null }))
      .catch(err => {
        if (err.name !== 'AbortError') {
          setState({ data: null, loading: false, error: err.message });
        }
      });

    return () => controller.abort();
  }, [url, refetchIndex]);

  return { ...state, refetch };
}

// Custom hook: useLocalStorage
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStoredValue = useCallback((newValue) => {
    setValue(newValue);
    localStorage.setItem(key, JSON.stringify(newValue));
  }, [key]);

  return [value, setStoredValue];
}

// Custom hook: useDebounce
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchBar() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);
  const { data, loading } = useFetch(
    debouncedQuery ? `/api/search?q=${debouncedQuery}` : null
  );
  const [recentSearches, setRecentSearches] = useLocalStorage('searches', []);

  return (
    <input value={query} onChange={e => setQuery(e.target.value)} />
  );
}
```

---

### Q15. What is `useLayoutEffect`? How is it different from `useEffect`?

**Answer:**

| | `useEffect` | `useLayoutEffect` |
|-|------------|------------------|
| Timing | After browser paint (async) | Before browser paint (sync) |
| Blocks paint | ❌ No | ✅ Yes |
| Use for | Data fetching, subscriptions | DOM measurements, preventing flicker |

```jsx
import { useEffect, useLayoutEffect, useRef, useState } from 'react';

// useLayoutEffect — measure DOM before paint
function Tooltip({ text, targetRef }) {
  const tooltipRef = useRef(null);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  useLayoutEffect(() => {
    // Runs synchronously after DOM update, before paint
    // Perfect for DOM measurements — no visual flicker
    const target = targetRef.current.getBoundingClientRect();
    const tooltip = tooltipRef.current.getBoundingClientRect();

    setPosition({
      top: target.top - tooltip.height - 8,
      left: target.left + (target.width - tooltip.width) / 2,
    });
  }, [text]);  // Recalculate when text changes

  return (
    <div
      ref={tooltipRef}
      style={{ position: 'fixed', top: position.top, left: position.left }}
    >
      {text}
    </div>
  );
}

// Execution order:
// 1. React renders (pure)
// 2. React commits to DOM
// 3. useLayoutEffect cleanup (sync)
// 4. useLayoutEffect (sync)
// 5. Browser paints ← user sees this
// 6. useEffect cleanup (async)
// 7. useEffect (async)

// Rule: use useEffect by default
// Use useLayoutEffect only when you need to measure/modify DOM before paint
```

---

### Q16. What is `useTransition`? (React 18)

**Answer:**
`useTransition` marks state updates as **non-urgent**, allowing React to keep the UI responsive while processing expensive updates.

```jsx
import { useState, useTransition } from 'react';

function SearchResults() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    const value = e.target.value;

    // Urgent update — update input immediately
    setQuery(value);

    // Non-urgent update — can be interrupted/deferred
    startTransition(() => {
      // This expensive update won't block the input
      const filtered = searchLargeDataset(value);
      setResults(filtered);
    });
  };

  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </div>
  );
}

// Without useTransition: typing feels laggy (expensive update blocks input)
// With useTransition: input stays responsive, results update when ready
```

---

### Q17. What is `useDeferredValue`? How is it different from `useTransition`?

**Answer:**

| | `useTransition` | `useDeferredValue` |
|-|----------------|-------------------|
| Controls | The state update | The value itself |
| Use when | You own the state setter | You receive value as prop |

```jsx
import { useState, useDeferredValue, memo } from 'react';

// useDeferredValue — defer a value that comes from props or state
function SearchPage() {
  const [query, setQuery] = useState('');

  // Deferred version — lags behind query during fast typing
  const deferredQuery = useDeferredValue(query);

  const isStale = query !== deferredQuery;

  return (
    <div>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <div style={{ opacity: isStale ? 0.5 : 1 }}>
        {/* Uses deferred value — won't block typing */}
        <ExpensiveResults query={deferredQuery} />
      </div>
    </div>
  );
}

// ExpensiveResults only re-renders when deferredQuery changes
const ExpensiveResults = memo(function({ query }) {
  const results = searchLargeDataset(query);  // Expensive
  return <ResultsList results={results} />;
});
```

---

### Q18. What is `useId`?

**Answer:**
`useId` generates a **stable, unique ID** that's consistent between server and client renders. Used for accessibility attributes.

```jsx
import { useId } from 'react';

function FormField({ label, type = 'text' }) {
  const id = useId();  // Generates unique ID like ":r0:", ":r1:", etc.

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} type={type} />
    </div>
  );
}

// Multiple IDs from one useId call
function RadioGroup({ options }) {
  const id = useId();

  return (
    <fieldset>
      {options.map((option, index) => (
        <div key={option.value}>
          <input
            type="radio"
            id={`${id}-${index}`}
            name={id}
            value={option.value}
          />
          <label htmlFor={`${id}-${index}`}>{option.label}</label>
        </div>
      ))}
    </fieldset>
  );
}

// Why not Math.random() or counter?
// Math.random() → different on server vs client → hydration mismatch
// Counter → not stable across re-renders
// useId → stable, unique, SSR-safe
```

---

### Q19. What is `useImperativeHandle`?

**Answer:**
`useImperativeHandle` customizes the **instance value exposed to parent components** when using `forwardRef`. It lets you expose only specific methods.

```jsx
import { forwardRef, useRef, useImperativeHandle } from 'react';

// Without useImperativeHandle — exposes entire DOM node
const Input = forwardRef((props, ref) => (
  <input ref={ref} {...props} />
));
// Parent can call ANY DOM method: ref.current.style.color = 'red', etc.

// With useImperativeHandle — expose only what you want
const FancyInput = forwardRef(function FancyInput({ placeholder }, ref) {
  const inputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    // Only expose these methods
    focus: () => inputRef.current.focus(),
    blur: () => inputRef.current.blur(),
    clear: () => { inputRef.current.value = ''; },
    getValue: () => inputRef.current.value,
    shake: () => {
      inputRef.current.classList.add('shake');
      setTimeout(() => inputRef.current.classList.remove('shake'), 500);
    },
  }), []);  // Dependencies for recreating the handle

  return <input ref={inputRef} placeholder={placeholder} />;
});

// Parent usage
function Form() {
  const inputRef = useRef(null);

  const handleSubmit = () => {
    const value = inputRef.current.getValue();
    if (!value) {
      inputRef.current.shake();  // Custom method!
      inputRef.current.focus();
    }
  };

  return (
    <>
      <FancyInput ref={inputRef} placeholder="Required field" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}
```

---

### Q20. What is `useDebugValue`?

**Answer:**
`useDebugValue` adds a **label to custom hooks** in React DevTools, making them easier to debug.

```jsx
import { useState, useEffect, useDebugValue } from 'react';

function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  // Shows "Online" or "Offline" in React DevTools
  useDebugValue(isOnline ? 'Online' : 'Offline');

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}

// With formatter function (for expensive formatting)
function useUser(userId) {
  const [user, setUser] = useState(null);

  // Second arg: formatter — only called when DevTools is open
  useDebugValue(user, user => user ? `User: ${user.name}` : 'Loading...');

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  return user;
}
```

---

<a name="hard"></a>
## 🔴 Hard

---

### Q21. What is a stale closure in React hooks?

**Answer:**
A stale closure occurs when a hook **captures an old value** of a variable from a previous render, leading to bugs.

```jsx
import { useState, useEffect, useRef, useCallback } from 'react';

// ❌ Stale closure bug
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      // 'count' is captured from the first render — always 0!
      setCount(count + 1);  // ❌ Stale closure: count is always 0
    }, 1000);
    return () => clearInterval(interval);
  }, []);  // Empty deps — effect only runs once, captures count=0

  return <p>Count: {count}</p>;  // Shows 1, then stays at 1
}

// ✅ Fix 1: Functional update (doesn't need to read count)
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(prev => prev + 1);  // ✅ Always uses latest value
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return <p>Count: {count}</p>;
}

// ✅ Fix 2: Add count to dependencies (re-creates interval on each change)
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(count + 1);  // ✅ count is fresh (re-runs when count changes)
    }, 1000);
    return () => clearInterval(interval);
  }, [count]);  // Re-runs when count changes

  return <p>Count: {count}</p>;
}

// ✅ Fix 3: useRef to always have latest value
function Counter() {
  const [count, setCount] = useState(0);
  const countRef = useRef(count);
  countRef.current = count;  // Always up-to-date

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(countRef.current + 1);  // ✅ Always reads latest
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return <p>Count: {count}</p>;
}
```

---

### Q22. What is the exhaustive-deps ESLint rule?

**Answer:**
The `exhaustive-deps` rule (from `eslint-plugin-react-hooks`) warns when `useEffect`, `useMemo`, or `useCallback` are missing dependencies.

```jsx
// ❌ Missing dependency — ESLint warning
function Component({ userId, onLoad }) {
  useEffect(() => {
    fetchUser(userId).then(onLoad);  // Uses userId and onLoad
  }, []);  // ⚠️ ESLint: 'userId' and 'onLoad' are missing from deps

  // ❌ This causes stale closure bugs!
}

// ✅ Include all dependencies
function Component({ userId, onLoad }) {
  useEffect(() => {
    fetchUser(userId).then(onLoad);
  }, [userId, onLoad]);  // ✅ All deps listed

  // But now: if onLoad is a new function every render, effect re-runs every render!
}

// ✅ Better: stabilize onLoad with useCallback in parent
function Parent() {
  const handleLoad = useCallback((user) => {
    console.log(user);
  }, []);  // Stable reference

  return <Component userId={1} onLoad={handleLoad} />;
}

// When to disable the rule (rare):
useEffect(() => {
  // Intentionally only run on mount
  initializeAnalytics();
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);
```

---

### Q23. Why can't you call hooks inside conditions or loops?

**Answer:**
React tracks hooks by their **call order**. If hooks are called conditionally, the order can change between renders, causing React to associate state with the wrong hook.

```jsx
// React internally maintains a "hook list" per component:
// Render 1: [useState(0), useEffect, useState('')]
//            Hook 1       Hook 2     Hook 3

// ❌ If Hook 2 is conditional:
// Render 1 (condition=true):  [useState(0), useEffect, useState('')]
// Render 2 (condition=false): [useState(0), useState('')]
//                              Hook 1 ✅    Hook 2 ← React thinks this is useEffect!

function BrokenComponent({ showExtra }) {
  const [a, setA] = useState(0);  // Hook 1

  if (showExtra) {
    useEffect(() => {  // Hook 2 — only sometimes!
      console.log('extra effect');
    }, []);
  }

  const [b, setB] = useState('');  // Hook 3 (or 2 if showExtra=false)
  // React associates wrong state with wrong hook!
}

// ✅ Move condition INSIDE the hook
function FixedComponent({ showExtra }) {
  const [a, setA] = useState(0);  // Hook 1 — always

  useEffect(() => {  // Hook 2 — always
    if (showExtra) {
      console.log('extra effect');
    }
  }, [showExtra]);

  const [b, setB] = useState('');  // Hook 3 — always
}
```

---

### Q24. What happens if you update state inside `useEffect` without proper dependencies?

**Answer:**
It can cause **infinite render loops** or **stale state bugs**.

```jsx
// ❌ Infinite loop
function InfiniteLoop() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(count + 1);  // Updates state → triggers re-render → effect runs again → ...
  });  // No dependency array — runs after EVERY render

  return <p>{count}</p>;  // Never renders — infinite loop!
}

// ❌ Infinite loop with dependency
function AlsoInfiniteLoop() {
  const [data, setData] = useState([]);

  useEffect(() => {
    setData([...data, 'new item']);  // Creates new array → data changes → effect re-runs
  }, [data]);  // data is a dependency but we're also setting it!
}

// ✅ Fix: use functional update (doesn't need data as dependency)
function Fixed() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData().then(newItem => {
      setData(prev => [...prev, newItem]);  // Functional update
    });
  }, []);  // Only runs once
}

// ✅ Fix: use a flag to prevent re-running
function WithFlag() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetchUser().then(data => {
      if (!cancelled) setUser(data);
    });
    return () => { cancelled = true; };
  }, []);
}
```

---

### Q25. Build a complete custom hook: `useAsync`

**Answer:**

```jsx
import { useState, useEffect, useCallback, useRef } from 'react';

// Generic async hook with loading, error, and abort support
function useAsync(asyncFn, deps = []) {
  const [state, setState] = useState({
    status: 'idle',  // 'idle' | 'loading' | 'success' | 'error'
    data: null,
    error: null,
  });

  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => { mountedRef.current = false; };
  }, []);

  const execute = useCallback(async (...args) => {
    setState({ status: 'loading', data: null, error: null });

    try {
      const data = await asyncFn(...args);
      if (mountedRef.current) {
        setState({ status: 'success', data, error: null });
      }
      return data;
    } catch (error) {
      if (mountedRef.current) {
        setState({ status: 'error', data: null, error });
      }
      throw error;
    }
  }, deps);

  return {
    ...state,
    execute,
    isIdle: state.status === 'idle',
    isLoading: state.status === 'loading',
    isSuccess: state.status === 'success',
    isError: state.status === 'error',
  };
}

// Usage
function UserProfile({ userId }) {
  const fetchUser = useCallback(
    () => fetch(`/api/users/${userId}`).then(r => r.json()),
    [userId]
  );

  const { data: user, isLoading, isError, error, execute } = useAsync(fetchUser, [userId]);

  useEffect(() => {
    execute();
  }, [execute]);

  if (isLoading) return <Spinner />;
  if (isError) return <Error message={error.message} onRetry={execute} />;
  if (!user) return null;

  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={execute}>Refresh</button>
    </div>
  );
}
```

---

### [← Back to Index](./00_INDEX.md) | [Next: State Management →](./09_State_Management.md)
