# 🔄 10 — Component Lifecycle & Patterns
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q15)](#medium)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is the component lifecycle in React class components?

**Answer:**

```
MOUNTING                    UPDATING                      UNMOUNTING
constructor()               getDerivedStateFromProps()    componentWillUnmount()
getDerivedStateFromProps()  shouldComponentUpdate()
render()                    render()
componentDidMount()         getSnapshotBeforeUpdate()
                            componentDidUpdate()
```

```jsx
class LifecycleExample extends React.Component {
  // 1. MOUNTING — constructor
  constructor(props) {
    super(props);
    this.state = { data: null, count: 0 };
    // Initialize state, bind methods
    // ❌ Don't: fetch data, set up subscriptions
  }

  // 2. MOUNTING — getDerivedStateFromProps (rare)
  static getDerivedStateFromProps(props, state) {
    // Sync state with props — runs before every render
    // Return new state or null
    if (props.userId !== state.prevUserId) {
      return { data: null, prevUserId: props.userId };
    }
    return null;
  }

  // 3. MOUNTING — render (pure, no side effects)
  render() {
    return <div>{this.state.data}</div>;
  }

  // 4. MOUNTING — componentDidMount
  componentDidMount() {
    // ✅ Fetch data, set up subscriptions, access DOM
    this.fetchData();
    this.subscription = subscribe(this.props.id);
  }

  // 5. UPDATING — shouldComponentUpdate (optimization)
  shouldComponentUpdate(nextProps, nextState) {
    // Return false to skip re-render
    return nextProps.id !== this.props.id || nextState.count !== this.state.count;
  }

  // 6. UPDATING — getSnapshotBeforeUpdate (rare)
  getSnapshotBeforeUpdate(prevProps, prevState) {
    // Capture DOM info before update (e.g., scroll position)
    return this.listRef.scrollHeight;
  }

  // 7. UPDATING — componentDidUpdate
  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps.id !== this.props.id) {
      this.fetchData();  // Re-fetch when id changes
    }
    // snapshot from getSnapshotBeforeUpdate
    if (snapshot !== null) {
      this.listRef.scrollTop += this.listRef.scrollHeight - snapshot;
    }
  }

  // 8. UNMOUNTING — componentWillUnmount
  componentWillUnmount() {
    // ✅ Clean up: cancel requests, remove listeners, clear timers
    this.subscription.unsubscribe();
    clearInterval(this.timer);
  }
}
```

---

### Q2. What is `componentDidMount`? Functional equivalent?

**Answer:**
`componentDidMount` runs **once after the component is inserted into the DOM**. Functional equivalent: `useEffect` with empty dependency array `[]`.

```jsx
// Class
class DataLoader extends React.Component {
  componentDidMount() {
    fetch('/api/data')
      .then(res => res.json())
      .then(data => this.setState({ data }));
  }
}

// Functional equivalent
function DataLoader() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData);
  }, []);  // [] = run once after mount

  return <div>{data?.name}</div>;
}
```

---

### Q3. What is `componentDidUpdate`? Functional equivalent?

**Answer:**
`componentDidUpdate` runs **after every update** (re-render). Functional equivalent: `useEffect` with dependencies.

```jsx
// Class
class UserProfile extends React.Component {
  componentDidUpdate(prevProps) {
    if (prevProps.userId !== this.props.userId) {
      this.fetchUser(this.props.userId);
    }
  }
}

// Functional equivalent
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);  // Re-runs when userId changes
}
```

---

### Q4. What is `componentWillUnmount`? Functional equivalent?

**Answer:**
`componentWillUnmount` runs **just before the component is removed from the DOM**. Functional equivalent: the cleanup function returned from `useEffect`.

```jsx
// Class
class ChatRoom extends React.Component {
  componentDidMount() {
    this.socket = new WebSocket(this.props.url);
    this.socket.onmessage = this.handleMessage;
  }

  componentWillUnmount() {
    this.socket.close();  // Cleanup
  }
}

// Functional equivalent
function ChatRoom({ url }) {
  useEffect(() => {
    const socket = new WebSocket(url);
    socket.onmessage = handleMessage;

    return () => {
      socket.close();  // Cleanup = componentWillUnmount
    };
  }, [url]);
}
```

---

### Q5. What is `shouldComponentUpdate`? Functional equivalent?

**Answer:**
`shouldComponentUpdate` controls **whether a component re-renders**. Functional equivalent: `React.memo`.

```jsx
// Class
class ExpensiveComponent extends React.Component {
  shouldComponentUpdate(nextProps, nextState) {
    // Only re-render if id or data changed
    return nextProps.id !== this.props.id ||
           nextState.data !== this.state.data;
  }
}

// Functional equivalent: React.memo
const ExpensiveComponent = React.memo(
  function ExpensiveComponent({ id, data }) {
    return <div>{data}</div>;
  },
  // Custom comparison (optional)
  (prevProps, nextProps) => prevProps.id === nextProps.id
  // Return true = skip re-render (same as shouldComponentUpdate returning false)
);
```

---

### Q6. What is an Error Boundary? Why must it be a class component?

**Answer:**
An Error Boundary is a class component that **catches JavaScript errors in its child component tree** and displays a fallback UI instead of crashing.

**Why class only:** The lifecycle methods `getDerivedStateFromError` and `componentDidCatch` have no hook equivalents yet (as of React 18).

```jsx
import { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  // Render fallback UI after error (during render phase)
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  // Log error details (during commit phase)
  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error);
    console.error('Component stack:', errorInfo.componentStack);
    // Send to error tracking: Sentry, Datadog, etc.
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage — wrap sections independently for granular error handling
function App() {
  return (
    <ErrorBoundary fallback={<AppCrashed />}>
      <ErrorBoundary fallback={<ChartError />}>
        <AnalyticsChart />
      </ErrorBoundary>
      <ErrorBoundary fallback={<TableError />}>
        <DataTable />
      </ErrorBoundary>
    </ErrorBoundary>
  );
}

// Error boundaries do NOT catch:
// ❌ Event handlers (use try/catch)
// ❌ Async code (use try/catch in useEffect)
// ❌ Server-side rendering
// ❌ Errors in the error boundary itself
```

---

### Q7. What is `getDerivedStateFromError` vs `componentDidCatch`?

**Answer:**

| | `getDerivedStateFromError` | `componentDidCatch` |
|-|--------------------------|---------------------|
| Phase | Render phase | Commit phase |
| Purpose | Update state to show fallback | Log error, side effects |
| Side effects | ❌ Not allowed | ✅ Allowed |
| Called | During rendering | After DOM update |

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  // Called during render — update state to show fallback
  // Must be pure — no side effects
  static getDerivedStateFromError(error) {
    return { hasError: true };  // Triggers re-render with fallback
  }

  // Called after commit — for side effects (logging, analytics)
  componentDidCatch(error, info) {
    // info.componentStack shows which component threw
    logToSentry(error, info.componentStack);
    analytics.track('error', { message: error.message });
  }

  render() {
    if (this.state.hasError) return <Fallback />;
    return this.props.children;
  }
}
```

---

### Q8. What is the Compound Component pattern?

**Answer:**
Compound Components are **components that work together**, sharing implicit state through context. They provide a flexible, expressive API.

```jsx
import { createContext, useContext, useState } from 'react';

// Compound Component: Accordion
const AccordionContext = createContext(null);

function Accordion({ children, defaultOpen = null }) {
  const [openItem, setOpenItem] = useState(defaultOpen);

  const toggle = (id) => setOpenItem(prev => prev === id ? null : id);

  return (
    <AccordionContext.Provider value={{ openItem, toggle }}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
}

Accordion.Item = function AccordionItem({ id, children }) {
  return <div className="accordion-item">{children}</div>;
};

Accordion.Header = function AccordionHeader({ id, children }) {
  const { openItem, toggle } = useContext(AccordionContext);
  return (
    <button
      className={`accordion-header ${openItem === id ? 'open' : ''}`}
      onClick={() => toggle(id)}
      aria-expanded={openItem === id}
    >
      {children}
      <span>{openItem === id ? '▲' : '▼'}</span>
    </button>
  );
};

Accordion.Panel = function AccordionPanel({ id, children }) {
  const { openItem } = useContext(AccordionContext);
  if (openItem !== id) return null;
  return <div className="accordion-panel">{children}</div>;
};

// Clean, flexible usage
function FAQ() {
  return (
    <Accordion defaultOpen="q1">
      <Accordion.Item id="q1">
        <Accordion.Header id="q1">What is React?</Accordion.Header>
        <Accordion.Panel id="q1">React is a UI library...</Accordion.Panel>
      </Accordion.Item>
      <Accordion.Item id="q2">
        <Accordion.Header id="q2">What are hooks?</Accordion.Header>
        <Accordion.Panel id="q2">Hooks are functions...</Accordion.Panel>
      </Accordion.Item>
    </Accordion>
  );
}
```

---

### Q9. What is the Provider pattern in React?

**Answer:**
The Provider pattern uses Context to **inject dependencies** into a component tree, making them available to any descendant.

```jsx
// Multiple providers — compose them
function AppProviders({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <NotificationProvider>
            {children}
          </NotificationProvider>
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

// Or use a compose utility
function compose(...providers) {
  return ({ children }) =>
    providers.reduceRight(
      (acc, Provider) => <Provider>{acc}</Provider>,
      children
    );
}

const AppProviders = compose(
  QueryClientProvider,
  AuthProvider,
  ThemeProvider,
  NotificationProvider
);

function App() {
  return (
    <AppProviders>
      <Router>
        <Routes />
      </Router>
    </AppProviders>
  );
}
```

---

### Q10. What is the Container/Presentational pattern? Is it still relevant?

**Answer:**
- **Container** (Smart) — handles data fetching, state, business logic
- **Presentational** (Dumb) — only renders UI based on props

**Still relevant?** Partially. Custom hooks have replaced most of the need for container components, but the separation of concerns principle remains valuable.

```jsx
// ❌ Old way: Container component
class UserListContainer extends React.Component {
  state = { users: [], loading: true };

  componentDidMount() {
    fetchUsers().then(users => this.setState({ users, loading: false }));
  }

  render() {
    return <UserList users={this.state.users} loading={this.state.loading} />;
  }
}

// Presentational component — pure, testable
function UserList({ users, loading }) {
  if (loading) return <Spinner />;
  return (
    <ul>
      {users.map(user => <UserItem key={user.id} user={user} />)}
    </ul>
  );
}

// ✅ Modern way: Custom hook replaces container
function useUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers().then(users => {
      setUsers(users);
      setLoading(false);
    });
  }, []);

  return { users, loading };
}

// Component uses hook directly — no container needed
function UserListPage() {
  const { users, loading } = useUsers();
  return <UserList users={users} loading={loading} />;
}
```

---

### Q11. What is the difference between lifting state up and using context?

**Answer:**

| | Lifting State Up | Context |
|-|-----------------|---------|
| Scope | Nearby components | Entire subtree |
| Prop drilling | Still needed | Eliminated |
| Performance | Re-renders parent | Re-renders consumers |
| Complexity | Simple | More setup |
| Use when | 2-3 levels deep | Many levels deep |

```jsx
// Lifting state up — share state between siblings
function Parent() {
  const [selectedId, setSelectedId] = useState(null);

  return (
    <>
      <ItemList onSelect={setSelectedId} />
      <ItemDetail id={selectedId} />
    </>
  );
}

// Context — share state across many levels
const SelectionContext = createContext(null);

function App() {
  const [selectedId, setSelectedId] = useState(null);

  return (
    <SelectionContext.Provider value={{ selectedId, setSelectedId }}>
      <DeepTree />  {/* selectedId available anywhere inside */}
    </SelectionContext.Provider>
  );
}

// Rule: lift state to the lowest common ancestor
// Use context when lifting would cause excessive prop drilling
```

---

### Q12. What is `React.cloneElement`? When would you use it?

**Answer:**
`React.cloneElement` creates a **copy of a React element with new/merged props**. Used to inject props into children.

```jsx
import { cloneElement, Children } from 'react';

// Inject props into children
function RadioGroup({ children, name, value, onChange }) {
  return (
    <div role="radiogroup">
      {Children.map(children, child =>
        cloneElement(child, {
          name,           // Inject name prop
          checked: child.props.value === value,
          onChange,
        })
      )}
    </div>
  );
}

// Usage
function App() {
  const [selected, setSelected] = useState('a');

  return (
    <RadioGroup name="choice" value={selected} onChange={e => setSelected(e.target.value)}>
      <Radio value="a">Option A</Radio>
      <Radio value="b">Option B</Radio>
      <Radio value="c">Option C</Radio>
    </RadioGroup>
  );
}

// Modern alternative: use context instead of cloneElement
// cloneElement is fragile — breaks if children aren't React elements
```

---

### Q13. What is `React.forwardRef`? When would you use it?

> See [07_React_Fundamentals.md Q25](./07_React_Fundamentals.md) for the full answer.

**Quick summary:**
```jsx
// Use forwardRef when:
// ✅ Building reusable input/form components
// ✅ Building component libraries
// ✅ Need to expose DOM methods to parent

const Input = forwardRef(({ label, ...props }, ref) => (
  <div>
    <label>{label}</label>
    <input ref={ref} {...props} />
  </div>
));
```

---

### Q14. What is the difference between lifting state up and using context?

> See Q11 above.

---

### Q15. What is the Render Props pattern vs Custom Hooks?

**Answer:**

| | Render Props | Custom Hooks |
|-|-------------|-------------|
| Syntax | JSX-based | Function-based |
| Nesting | Can cause "wrapper hell" | Flat |
| Composability | Harder | Easy |
| TypeScript | Harder | Easier |
| Recommended | Legacy | ✅ Modern |

```jsx
// Render Props — old pattern
function MousePosition({ render }) {
  const [pos, setPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  return render(pos);
}

// Usage — verbose
function App() {
  return (
    <MousePosition
      render={({ x, y }) => <p>Mouse: {x}, {y}</p>}
    />
  );
}

// Custom Hook — modern, preferred
function useMousePosition() {
  const [pos, setPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  return pos;
}

// Usage — clean
function App() {
  const { x, y } = useMousePosition();
  return <p>Mouse: {x}, {y}</p>;
}

// Composing multiple hooks — no nesting
function Dashboard() {
  const { x, y } = useMousePosition();
  const { data } = useFetch('/api/data');
  const { theme } = useTheme();
  const { user } = useAuth();
  // All flat, no wrapper hell
}
```

---

### [← Back to Index](./00_INDEX.md) | [Next: Performance Optimization →](./11_Performance.md)
