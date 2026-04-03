# ⚛️ 07 — React Fundamentals
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟢 Easy (Q1–Q15)](#easy)
- [🟡 Medium (Q16–Q25)](#medium)

---

<a name="easy"></a>
## 🟢 Easy

---

### Q1. What is React? What problem does it solve?

**Answer:**
React is a **JavaScript library for building user interfaces**, developed by Facebook/Meta. It solves the problem of efficiently updating the DOM when application state changes.

**Core idea:** `UI = f(state)` — the UI is a pure function of state. When state changes, React re-renders the component tree efficiently.

```jsx
// Without React — manual DOM manipulation (error-prone)
document.getElementById('count').textContent = count;
document.getElementById('btn').addEventListener('click', () => {
  count++;
  document.getElementById('count').textContent = count;
});

// With React — declarative, React handles DOM updates
function Counter() {
  const [count, setCount] = React.useState(0);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
// React figures out what changed and updates only that part of the DOM
```

---

### Q 1.1 What are the major features of React?

  React offers a powerful set of features that have made it one of the most popular JavaScript libraries for building user interfaces:

  **Core Features:**

  - **Component-Based Architecture**: React applications are built using components - independent, reusable pieces of code that return HTML via a render function. This modular approach enables better code organization, reusability, and maintenance.

  - **Virtual DOM**: React creates an in-memory data structure cache, computes the resulting differences, and efficiently updates only the changed parts in the browser DOM. This approach significantly improves performance compared to direct DOM manipulation.

  - **JSX (JavaScript XML)**: A syntax extension that allows writing HTML-like code in JavaScript. JSX makes the code more readable and expressive while providing the full power of JavaScript.

  - **Unidirectional Data Flow**: React follows a one-way data binding model where data flows from parent to child components. This makes the code more predictable and easier to debug.

  - **Declarative UI**: React allows you to describe what your UI should look like for a given state, and it handles the DOM updates when the underlying data changes.

  **Advanced Features:**

  - **React Hooks**: Introduced in React 16.8, hooks allow using state and other React features in functional components without writing classes.

  - **Context API**: Provides a way to share values between components without explicitly passing props through every level of the component tree.

  - **Error Boundaries**: Components that catch JavaScript errors anywhere in their child component tree and display fallback UI instead of crashing.

  - **Server-Side Rendering (SSR)**: Enables rendering React components on the server before sending HTML to the client, improving performance and SEO.

  - **Concurrent Mode**: A set of new features (in development) that help React apps stay responsive and gracefully adjust to the user's device capabilities and network speed.

  - **React Server Components**: A new feature that allows components to be rendered entirely on the server, reducing bundle size and improving performance.

  - **Suspense**: A feature that lets your components "wait" for something before rendering, supporting code-splitting and data fetching with cleaner code.

  These features collectively make React powerful for building everything from small widgets to complex, large-scale web applications.

---

### Q2. What is the Virtual DOM?

**Answer:**
The Virtual DOM is a **lightweight JavaScript representation** of the real DOM. React uses it to minimize expensive real DOM operations.

**Process:**
1. State changes → React creates a new Virtual DOM tree
2. React **diffs** the new tree against the previous one (reconciliation)
3. React calculates the **minimum set of changes** needed
4. React applies only those changes to the real DOM (commit phase)

```
State Change
     ↓
New Virtual DOM
     ↓
Diff (reconciliation) ← Previous Virtual DOM
     ↓
Minimal DOM updates
     ↓
Real DOM updated
```

```jsx
// React batches multiple state updates into one render
function Example() {
  const [a, setA] = React.useState(0);
  const [b, setB] = React.useState(0);

  const handleClick = () => {
    setA(1);  // Doesn't trigger render yet
    setB(2);  // Doesn't trigger render yet
    // React batches both → single re-render (React 18+)
  };
}
```

---


### Q3. What is JSX?

**Answer:**
JSX (JavaScript XML) is a **syntax extension** that lets you write HTML-like code in JavaScript. It's compiled to `React.createElement()` calls by Babel.

```jsx
// JSX
const element = <h1 className="title">Hello, {name}!</h1>;

// Compiled to:
const element = React.createElement(
  'h1',
  { className: 'title' },
  `Hello, ${name}!`
);

// JSX rules:
// 1. Must return a single root element (or Fragment)
// 2. Use className instead of class
// 3. Use htmlFor instead of for
// 4. Self-close empty tags: <img />, <br />
// 5. JavaScript expressions in {}
// 6. camelCase for event handlers: onClick, onChange

function Component({ name, isActive }) {
  return (
    <>  {/* Fragment — no extra DOM node */}
      <h1 className={isActive ? 'active' : 'inactive'}>
        Hello, {name}!
      </h1>
      <p style={{ color: 'blue', fontSize: '16px' }}>
        {isActive ? 'Active' : 'Inactive'}
      </p>
    </>
  );
}
```

---

### Q4. What is the difference between functional and class components?

**Answer:**

| Feature | Functional | Class |
|---------|-----------|-------|
| Syntax | Function | `class extends React.Component` |
| State | `useState` hook | `this.state` |
| Lifecycle | `useEffect` | `componentDidMount`, etc. |
| `this` | Not needed | Required |
| Performance | Slightly better | Slightly worse |
| Recommended | ✅ Yes (modern) | ❌ Legacy |

```jsx
// Class component (legacy)
class Greeting extends React.Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  componentDidMount() {
    document.title = `Count: ${this.state.count}`;
  }

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          Increment
        </button>
      </div>
    );
  }
}

// Functional component (modern — preferred)
function Greeting() {
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}
```

---

### Q5. What are props in React? Are they mutable?

**Answer:**
Props (properties) are **read-only inputs** passed from parent to child components. They are **immutable** — a component cannot modify its own props.

```jsx
// Parent passes props
function App() {
  return (
    <UserCard
      name="Alice"
      age={30}
      isAdmin={true}
      onClick={() => console.log('clicked')}
      children={<span>Extra content</span>}
    />
  );
}

// Child receives props
function UserCard({ name, age, isAdmin, onClick, children }) {
  // ❌ Cannot modify props
  // name = "Bob";  // This would be wrong

  return (
    <div onClick={onClick}>
      <h2>{name}</h2>
      <p>Age: {age}</p>
      {isAdmin && <span>Admin</span>}
      {children}
    </div>
  );
}

// Default props
function Button({ label = "Click me", variant = "primary", disabled = false }) {
  return <button disabled={disabled} className={variant}>{label}</button>;
}

// Prop types validation (runtime)
import PropTypes from 'prop-types';
Button.propTypes = {
  label: PropTypes.string.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary']),
  disabled: PropTypes.bool,
};
```

---

### Q6. What is state in React? How is it different from props?

**Answer:**

| | Props | State |
|-|-------|-------|
| Source | Parent component | Component itself |
| Mutable | ❌ No | ✅ Yes (via setter) |
| Triggers re-render | When parent re-renders | When updated via setter |
| Ownership | Parent owns it | Component owns it |

```jsx
function TrafficLight() {
  // State — owned and managed by this component
  const [color, setColor] = React.useState('red');

  const cycle = () => {
    setColor(prev => {
      if (prev === 'red') return 'green';
      if (prev === 'green') return 'yellow';
      return 'red';
    });
  };

  return (
    <div>
      <Light color={color} />  {/* color is a PROP to Light */}
      <button onClick={cycle}>Next</button>
    </div>
  );
}

function Light({ color }) {  // color is a PROP — read-only
  return <div style={{ background: color, width: 50, height: 50 }} />;
}

// State update rules:
// 1. Never mutate state directly: state.items.push(x) ❌
// 2. Always use the setter: setItems([...items, x]) ✅
// 3. Use functional update when new state depends on old:
//    setCount(prev => prev + 1) ✅ (not setCount(count + 1))
```

---

### Q7. What is the difference between controlled and uncontrolled components?

**Answer:**
- **Controlled** — form data is managed by **React state** (single source of truth)
- **Uncontrolled** — form data is managed by the **DOM** (accessed via ref)

```jsx
import { useState, useRef } from 'react';

// Controlled component — React controls the value
function ControlledForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ name, email });  // Always up-to-date
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}           // React controls value
        onChange={e => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Submit</button>
    </form>
  );
}

// Uncontrolled component — DOM controls the value
function UncontrolledForm() {
  const nameRef = useRef(null);
  const emailRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({
      name: nameRef.current.value,   // Read from DOM on submit
      email: emailRef.current.value,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input ref={nameRef} defaultValue="" placeholder="Name" />
      <input ref={emailRef} defaultValue="" placeholder="Email" />
      <button type="submit">Submit</button>
    </form>
  );
}

// Use controlled when: validation, conditional rendering, dynamic forms
// Use uncontrolled when: file inputs, integrating with non-React code
```

---

### Q8. What is event handling in React?

**Answer:**
React uses **synthetic events** — cross-browser wrappers around native DOM events. Event handlers are camelCase and receive a `SyntheticEvent` object.

```jsx
function EventDemo() {
  const handleClick = (e) => {
    e.preventDefault();      // Prevent default behavior
    e.stopPropagation();     // Stop event bubbling
    console.log(e.target);   // The element that triggered the event
    console.log(e.currentTarget);  // The element with the handler
  };

  const handleChange = (e) => {
    console.log(e.target.value);  // Input value
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      console.log('Enter pressed');
    }
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      console.log('Ctrl+S');
    }
  };

  // Passing arguments to handlers
  const handleItemClick = (id) => (e) => {
    console.log(`Item ${id} clicked`);
  };

  return (
    <div>
      <button onClick={handleClick}>Click me</button>
      <input onChange={handleChange} onKeyDown={handleKeyDown} />
      {[1, 2, 3].map(id => (
        <div key={id} onClick={handleItemClick(id)}>Item {id}</div>
      ))}
    </div>
  );
}
```

---

### Q9. What is the `key` prop? Why is it important?

**Answer:**
The `key` prop helps React **identify which items in a list have changed**, been added, or removed. It must be **unique among siblings** and **stable** across renders.

```jsx
// ❌ Bad: using index as key
function BadList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item.name}</li>
        // If items are reordered or deleted, index shifts
        // React may reuse wrong component instances
        // Can cause bugs with input state, animations
      ))}
    </ul>
  );
}

// ✅ Good: using stable unique ID
function GoodList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

// Key trick: force component remount (reset all state)
function ProfilePage({ userId }) {
  return (
    // When userId changes, React destroys and recreates UserProfile
    // All internal state is reset — useful for "fresh start"
    <UserProfile key={userId} userId={userId} />
  );
}

// Keys must be unique among siblings, not globally
function App() {
  return (
    <>
      <ul>
        {list1.map(item => <li key={item.id}>{item.name}</li>)}
      </ul>
      <ul>
        {list2.map(item => <li key={item.id}>{item.name}</li>)}
        {/* Same IDs as list1 are fine — different parent */}
      </ul>
    </>
  );
}
```

---

### Q10. What is conditional rendering in React?

**Answer:**
React supports several patterns for conditionally rendering elements:

```jsx
function Dashboard({ user, isLoading, error, items }) {
  // 1. if/else (outside JSX)
  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      {/* 2. Ternary operator */}
      {user ? <UserGreeting name={user.name} /> : <GuestGreeting />}

      {/* 3. Short-circuit && (render if truthy) */}
      {user.isAdmin && <AdminPanel />}

      {/* 4. Nullish coalescing for defaults */}
      <p>{user.bio ?? 'No bio provided'}</p>

      {/* 5. Switch-like with object map */}
      {{
        'loading': <Spinner />,
        'error': <ErrorMessage />,
        'success': <DataTable data={items} />,
      }[status]}

      {/* ⚠️ Gotcha: 0 is falsy but renders as "0" */}
      {items.length && <List items={items} />}  {/* Renders "0" if empty! */}
      {items.length > 0 && <List items={items} />}  {/* ✅ Correct */}
    </div>
  );
}
```

---

### Q11. What is the difference between `null`, `undefined`, and `false` in JSX?

**Answer:**
`null`, `undefined`, `false`, and `true` are **valid children** in JSX but **render nothing**. This is intentional — it enables conditional rendering.

```jsx
function Example() {
  return (
    <div>
      {null}        {/* Renders nothing */}
      {undefined}   {/* Renders nothing */}
      {false}       {/* Renders nothing */}
      {true}        {/* Renders nothing */}
      {0}           {/* ⚠️ Renders "0" — number 0 IS rendered! */}
      {""}          {/* Renders empty string (nothing visible) */}
      {NaN}         {/* ⚠️ Renders "NaN" */}
    </div>
  );
}

// Common bug:
function List({ items }) {
  return (
    <div>
      {items.length && <ul>...</ul>}
      {/* If items is empty: renders "0" not nothing! */}

      {/* Fix: */}
      {items.length > 0 && <ul>...</ul>}
      {/* Or: */}
      {!!items.length && <ul>...</ul>}
    </div>
  );
}
```

---

### Q12. What is a React Fragment?

**Answer:**
A Fragment lets you **group multiple elements without adding an extra DOM node**.

```jsx
// ❌ Extra div wrapper — pollutes DOM
function TableRow({ data }) {
  return (
    <div>  {/* Invalid: div inside table */}
      <td>{data.name}</td>
      <td>{data.age}</td>
    </div>
  );
}

// ✅ Fragment — no extra DOM node
function TableRow({ data }) {
  return (
    <>
      <td>{data.name}</td>
      <td>{data.age}</td>
    </>
  );
}

// Long syntax — supports key prop (needed in lists)
function List({ items }) {
  return (
    <dl>
      {items.map(item => (
        <React.Fragment key={item.id}>
          <dt>{item.term}</dt>
          <dd>{item.definition}</dd>
        </React.Fragment>
      ))}
    </dl>
  );
}
```

---

### Q13. What is prop drilling? Why is it a problem?

**Answer:**
Prop drilling is passing props through **multiple intermediate components** that don't need them, just to reach a deeply nested component.

```jsx
// ❌ Prop drilling — theme passed through every level
function App() {
  const [theme, setTheme] = useState('dark');
  return <Layout theme={theme} setTheme={setTheme} />;
}

function Layout({ theme, setTheme }) {
  return <Sidebar theme={theme} setTheme={setTheme} />;
  // Layout doesn't use theme, just passes it down
}

function Sidebar({ theme, setTheme }) {
  return <ThemeToggle theme={theme} setTheme={setTheme} />;
  // Sidebar doesn't use theme either
}

function ThemeToggle({ theme, setTheme }) {
  // Finally uses it!
  return <button onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}>
    Current: {theme}
  </button>;
}

// ✅ Solutions:
// 1. Context API — for global state
// 2. State management (Zustand, Redux)
// 3. Component composition — pass components as props
function App() {
  const [theme, setTheme] = useState('dark');
  return (
    <Layout
      sidebar={<ThemeToggle theme={theme} setTheme={setTheme} />}
    />
  );
}
```

---

### Q14. What is the difference between `onClick={handleClick}` and `onClick={() => handleClick()}`?

**Answer:**
- `onClick={handleClick}` — passes the **function reference** (no new function created on each render)
- `onClick={() => handleClick()}` — creates a **new arrow function** on every render

```jsx
function Example({ id, onDelete }) {
  // ✅ Direct reference — no new function per render
  return <button onClick={onDelete}>Delete</button>;

  // ⚠️ Arrow function — new function created every render
  // (minor performance issue, but usually fine)
  return <button onClick={() => onDelete()}>Delete</button>;

  // ✅ When you need to pass arguments — arrow function is necessary
  return <button onClick={() => onDelete(id)}>Delete</button>;

  // ✅ Alternative: bind in render (same as arrow function)
  return <button onClick={onDelete.bind(null, id)}>Delete</button>;

  // ✅ Best: useCallback for stable reference with args
  const handleDelete = useCallback(() => onDelete(id), [id, onDelete]);
  return <button onClick={handleDelete}>Delete</button>;
}
```

---

### Q15. What is the difference between `defaultProps` and default parameter values?

**Answer:**
- `defaultProps` — class component static property (legacy)
- Default parameter values — modern, preferred approach for functional components

```jsx
// ❌ defaultProps (legacy, deprecated for functional components)
function Button({ label, variant }) {
  return <button className={variant}>{label}</button>;
}
Button.defaultProps = {
  label: 'Click me',
  variant: 'primary',
};

// ✅ Default parameter values (modern)
function Button({ label = 'Click me', variant = 'primary', disabled = false }) {
  return <button className={variant} disabled={disabled}>{label}</button>;
}

// With TypeScript
interface ButtonProps {
  label?: string;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  onClick?: () => void;
}

function Button({
  label = 'Click me',
  variant = 'primary',
  disabled = false,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
}
```

---

<a name="medium"></a>
## 🟡 Medium

---

### Q16. What is reconciliation in React? How does the diffing algorithm work?

**Answer:**
Reconciliation is React's process of **comparing the new Virtual DOM with the previous one** and determining the minimum changes needed to update the real DOM.

**Two key assumptions (heuristics):**
1. Elements of **different types** produce different trees (React destroys and rebuilds)
2. The **`key` prop** hints which elements are stable across renders

```jsx
// Assumption 1: Different types → destroy and rebuild
// Before:
<div><Counter /></div>

// After:
<span><Counter /></span>
// React destroys Counter (loses state), creates new span + Counter

// Assumption 2: Same type → update in place
// Before:
<div className="before" title="stuff" />

// After:
<div className="after" title="stuff" />
// React only updates className attribute

// List reconciliation — why keys matter
// Before: [A, B, C]
// After:  [A, B, C, D]
// Without key: React updates A, B, C, inserts D ✅

// Before: [A, B, C]
// After:  [D, A, B, C]  (D inserted at beginning)
// Without key: React updates ALL items (thinks A→D, B→A, etc.) ❌
// With key: React moves A, B, C and inserts D ✅

function List({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>  {/* key enables efficient reconciliation */}
          <input defaultValue={item.name} />
        </li>
      ))}
    </ul>
  );
}
```

---

### Q17. What is a pure component? What is `React.memo`?

**Answer:**
A pure component **only re-renders when its props or state change**. `React.memo` is the functional component equivalent of `PureComponent`.

```jsx
import { memo, useState } from 'react';

// Without memo — re-renders every time parent renders
function ExpensiveChild({ data }) {
  console.log('ExpensiveChild rendered');
  return <div>{data.value}</div>;
}

// With memo — only re-renders when props change (shallow comparison)
const ExpensiveChild = memo(function ExpensiveChild({ data }) {
  console.log('ExpensiveChild rendered');
  return <div>{data.value}</div>;
});

function Parent() {
  const [count, setCount] = useState(0);
  const data = { value: 'static' };  // ⚠️ New object every render!

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <ExpensiveChild data={data} />
      {/* Still re-renders! data is a new object each time */}
    </div>
  );
}

// Fix: useMemo to stabilize the object
function Parent() {
  const [count, setCount] = useState(0);
  const data = useMemo(() => ({ value: 'static' }), []);  // Stable reference

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <ExpensiveChild data={data} />  {/* Now truly memoized */}
    </div>
  );
}

// Custom comparison function
const ExpensiveChild = memo(
  function ExpensiveChild({ user }) {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
  // Return true = skip re-render, false = re-render
);
```

---

### Q18. What is a Higher-Order Component (HOC)?

**Answer:**
A HOC is a **function that takes a component and returns a new enhanced component**. It's a pattern for reusing component logic.

```jsx
// HOC pattern: withAuth
function withAuth(WrappedComponent) {
  return function AuthenticatedComponent(props) {
    const { isAuthenticated, user } = useAuth();

    if (!isAuthenticated) {
      return <Navigate to="/login" />;
    }

    return <WrappedComponent {...props} user={user} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
const ProtectedProfile = withAuth(Profile);

// HOC: withLoading
function withLoading(WrappedComponent) {
  return function WithLoadingComponent({ isLoading, ...props }) {
    if (isLoading) return <Spinner />;
    return <WrappedComponent {...props} />;
  };
}

// HOC: withErrorBoundary
function withErrorBoundary(WrappedComponent, FallbackComponent) {
  return class extends React.Component {
    state = { hasError: false };

    static getDerivedStateFromError() {
      return { hasError: true };
    }

    render() {
      if (this.state.hasError) return <FallbackComponent />;
      return <WrappedComponent {...this.props} />;
    }
  };
}

// Modern alternative: custom hooks (preferred over HOCs)
// HOCs add wrapper components; hooks don't
function Dashboard() {
  const { user } = useAuth();  // Custom hook — no wrapper needed
  const { isLoading } = useLoading();
  // ...
}
```

---

### Q19. What is the render props pattern?

**Answer:**
Render props is a pattern where a component receives a **function as a prop** that it calls to render its output, sharing stateful logic.

```jsx
// Render props pattern
class MouseTracker extends React.Component {
  state = { x: 0, y: 0 };

  handleMouseMove = (e) => {
    this.setState({ x: e.clientX, y: e.clientY });
  };

  render() {
    return (
      <div onMouseMove={this.handleMouseMove}>
        {/* Call the render prop with current state */}
        {this.props.render(this.state)}
      </div>
    );
  }
}

// Usage
function App() {
  return (
    <MouseTracker
      render={({ x, y }) => (
        <p>Mouse position: {x}, {y}</p>
      )}
    />
  );
}

// children as function (common variation)
function DataFetcher({ url, children }) {
  const { data, loading, error } = useFetch(url);
  return children({ data, loading, error });
}

function App() {
  return (
    <DataFetcher url="/api/users">
      {({ data, loading, error }) => {
        if (loading) return <Spinner />;
        if (error) return <Error />;
        return <UserList users={data} />;
      }}
    </DataFetcher>
  );
}

// Modern alternative: custom hooks (preferred)
function App() {
  const { data, loading, error } = useFetch('/api/users');
  if (loading) return <Spinner />;
  return <UserList users={data} />;
}
```

---

### Q20. What is the `children` prop?

**Answer:**
`children` is a special prop that contains whatever is placed **between the opening and closing tags** of a component.

```jsx
// children as JSX
function Card({ children, title, className = '' }) {
  return (
    <div className={`card ${className}`}>
      {title && <h2 className="card-title">{title}</h2>}
      <div className="card-body">
        {children}
      </div>
    </div>
  );
}

// Usage
function App() {
  return (
    <Card title="User Profile">
      <Avatar src="/photo.jpg" />
      <p>Alice, Software Engineer</p>
      <Button>Follow</Button>
    </Card>
  );
}

// React.Children utilities
function List({ children }) {
  const count = React.Children.count(children);
  const items = React.Children.toArray(children);

  return (
    <ul>
      {React.Children.map(children, (child, index) => (
        <li key={index}>
          {React.cloneElement(child, { index })}  {/* Add props to children */}
        </li>
      ))}
    </ul>
  );
}

// Slot pattern — named children
function Layout({ header, sidebar, children }) {
  return (
    <div className="layout">
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{children}</main>
    </div>
  );
}

function App() {
  return (
    <Layout
      header={<NavBar />}
      sidebar={<SideMenu />}
    >
      <MainContent />
    </Layout>
  );
}
```

---

### Q21. What is `React.createElement`?

**Answer:**
`React.createElement(type, props, ...children)` is the underlying function that JSX compiles to.

```jsx
// JSX
const element = (
  <div className="container">
    <h1>Hello</h1>
    <p>World</p>
  </div>
);

// Compiled JavaScript
const element = React.createElement(
  'div',
  { className: 'container' },
  React.createElement('h1', null, 'Hello'),
  React.createElement('p', null, 'World')
);

// Result: a plain JavaScript object (Virtual DOM node)
// {
//   type: 'div',
//   props: {
//     className: 'container',
//     children: [
//       { type: 'h1', props: { children: 'Hello' } },
//       { type: 'p', props: { children: 'World' } }
//     ]
//   }
// }
```

---

### Q22. What is the difference between mounting, updating, and unmounting?

**Answer:**
- **Mounting** — component is created and inserted into the DOM for the first time
- **Updating** — component re-renders due to state or prop changes
- **Unmounting** — component is removed from the DOM

```jsx
import { useState, useEffect } from 'react';

function LifecycleDemo({ id }) {
  const [data, setData] = useState(null);

  // MOUNT — runs once after first render
  useEffect(() => {
    console.log('Mounted!');
    const subscription = subscribe(id);

    // UNMOUNT — cleanup function
    return () => {
      console.log('Unmounted!');
      subscription.unsubscribe();
    };
  }, []);

  // UPDATE — runs when id changes
  useEffect(() => {
    console.log(`id changed to ${id}`);
    fetchData(id).then(setData);
  }, [id]);

  return <div>{data?.name}</div>;
}

// Mounting order:
// 1. Component function runs (render)
// 2. DOM is updated
// 3. useLayoutEffect runs (sync)
// 4. Browser paints
// 5. useEffect runs (async)

// Unmounting:
// 1. useEffect cleanup runs
// 2. useLayoutEffect cleanup runs
// 3. Component removed from DOM
```

---

### Q23. What is `React.PureComponent` vs `React.Component`?

**Answer:**
- `React.Component` — re-renders whenever `setState` or `forceUpdate` is called
- `React.PureComponent` — implements `shouldComponentUpdate` with **shallow comparison** of props and state

```jsx
// React.Component — always re-renders on setState
class RegularComponent extends React.Component {
  render() {
    console.log('RegularComponent rendered');
    return <div>{this.props.value}</div>;
  }
}

// React.PureComponent — skips re-render if props/state unchanged (shallow)
class PureComp extends React.PureComponent {
  render() {
    console.log('PureComponent rendered');
    return <div>{this.props.value}</div>;
  }
}

// ⚠️ Shallow comparison caveat
class Parent extends React.Component {
  state = { items: [1, 2, 3] };

  addItem = () => {
    // ❌ Mutating state — PureComponent won't detect change!
    this.state.items.push(4);
    this.setState({ items: this.state.items });

    // ✅ New array — PureComponent detects change
    this.setState({ items: [...this.state.items, 4] });
  };
}

// Functional equivalent: React.memo
const PureFunctional = React.memo(function({ value }) {
  return <div>{value}</div>;
});
```

---

### Q24. What is prop drilling and how do you solve it?

> See Q13 for the full answer. Solutions summary:

```jsx
// Solution 1: Context API (for global/shared state)
const ThemeContext = createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <DeepChild />  {/* No prop passing needed */}
    </ThemeContext.Provider>
  );
}

function DeepChild() {
  const theme = useContext(ThemeContext);  // Direct access
  return <div className={theme}>Content</div>;
}

// Solution 2: Component composition (pass components, not data)
function App() {
  const [user] = useState({ name: 'Alice' });
  return (
    <Layout
      header={<Header user={user} />}  {/* Pass component, not data */}
    />
  );
}

// Solution 3: State management (Zustand)
const useStore = create(set => ({
  user: null,
  setUser: (user) => set({ user }),
}));

function DeepChild() {
  const user = useStore(state => state.user);  // Direct access anywhere
  return <div>{user?.name}</div>;
}
```

---

### Q25. What is `React.forwardRef`?

**Answer:**
`forwardRef` allows a component to **pass a ref through to a child DOM element or component**.

```jsx
import { forwardRef, useRef } from 'react';

// Without forwardRef — ref doesn't reach the input
function Input({ placeholder }) {
  return <input placeholder={placeholder} />;
}

// With forwardRef — ref is forwarded to the input
const Input = forwardRef(function Input({ placeholder, ...props }, ref) {
  return <input ref={ref} placeholder={placeholder} {...props} />;
});

// Usage
function Form() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current.focus();  // Works because ref is forwarded
  };

  return (
    <>
      <Input ref={inputRef} placeholder="Enter text" />
      <button onClick={focusInput}>Focus</button>
    </>
  );
}

// Combined with useImperativeHandle — expose custom methods
const FancyInput = forwardRef(function FancyInput(props, ref) {
  const inputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => { inputRef.current.value = ''; },
    getValue: () => inputRef.current.value,
  }));

  return <input ref={inputRef} {...props} />;
});

function Parent() {
  const ref = useRef(null);
  return (
    <>
      <FancyInput ref={ref} />
      <button onClick={() => ref.current.clear()}>Clear</button>
    </>
  );
}
```

---

### [← Back to Index](./00_INDEX.md) | [Next: React Hooks →](./08_React_Hooks.md)
