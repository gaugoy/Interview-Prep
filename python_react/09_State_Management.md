# 🗃️ 09 — State Management
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q15)](#medium)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is the Context API? When should you use it?

**Answer:**
The Context API provides a way to **share values between components without prop drilling**. It's built into React — no extra library needed.

**Use Context for:** theme, auth, locale, low-frequency global state.

```jsx
import { createContext, useContext, useState, useMemo } from 'react';

// 1. Create context with default value
const ThemeContext = createContext({
  theme: 'light',
  toggleTheme: () => {},
});

// 2. Provider — wraps the component tree
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  // Memoize to prevent unnecessary re-renders of all consumers
  const value = useMemo(() => ({
    theme,
    toggleTheme: () => setTheme(t => t === 'light' ? 'dark' : 'light'),
  }), [theme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// 3. Custom hook — best practice
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}

// 4. Consumer — anywhere in the tree
function ThemedButton() {
  const { theme, toggleTheme } = useTheme();
  return (
    <button
      style={{ background: theme === 'light' ? '#fff' : '#333', color: theme === 'light' ? '#000' : '#fff' }}
      onClick={toggleTheme}
    >
      Toggle Theme
    </button>
  );
}

// App
function App() {
  return (
    <ThemeProvider>
      <Header />
      <Main />
      <Footer />
    </ThemeProvider>
  );
}
```

---

### Q2. What are the limitations of the Context API?

**Answer:**
1. **All consumers re-render** when context value changes (even if they only use part of it)
2. **No built-in selectors** — can't subscribe to only part of the context
3. **Not optimized for high-frequency updates** (e.g., mouse position, real-time data)
4. **No DevTools** — harder to debug than Redux

```jsx
// ❌ Problem: All consumers re-render when ANY value changes
const AppContext = createContext(null);

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState([]);

  // If notifications change, ALL consumers re-render (even those only using theme)
  return (
    <AppContext.Provider value={{ user, theme, notifications, setUser, setTheme, setNotifications }}>
      {children}
    </AppContext.Provider>
  );
}

// ✅ Solution 1: Split contexts by update frequency
const UserContext = createContext(null);
const ThemeContext = createContext(null);
const NotificationContext = createContext(null);

// ✅ Solution 2: Separate state and dispatch contexts
const StateContext = createContext(null);
const DispatchContext = createContext(null);

function Provider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <DispatchContext.Provider value={dispatch}>
      <StateContext.Provider value={state}>
        {children}
      </StateContext.Provider>
    </DispatchContext.Provider>
  );
}
// Components that only dispatch won't re-render when state changes
```

---

### Q3. What is Redux? What are its three core principles?

**Answer:**
Redux is a **predictable state container** for JavaScript apps. It centralizes application state and makes state changes predictable.

**Three core principles:**
1. **Single source of truth** — entire app state in one store
2. **State is read-only** — only way to change state is to dispatch an action
3. **Changes made with pure functions** — reducers are pure functions

```
Action → Reducer → Store → View → Action (cycle)
```

```jsx
// Core concepts:
// ACTION — plain object describing what happened
const incrementAction = { type: 'counter/increment' };
const addTodoAction = { type: 'todos/add', payload: { text: 'Learn Redux' } };

// REDUCER — pure function: (state, action) → newState
function counterReducer(state = 0, action) {
  switch (action.type) {
    case 'counter/increment': return state + 1;
    case 'counter/decrement': return state - 1;
    default: return state;
  }
}

// STORE — holds the state tree
import { createStore } from 'redux';
const store = createStore(counterReducer);

store.getState();           // 0
store.dispatch({ type: 'counter/increment' });
store.getState();           // 1

store.subscribe(() => {
  console.log('State changed:', store.getState());
});
```

---

### Q4. What is Redux Toolkit? How does it simplify Redux?

**Answer:**
Redux Toolkit (RTK) is the **official, opinionated way to write Redux**. It eliminates boilerplate and includes best practices by default.

**What RTK provides:**
- `createSlice` — combines actions + reducer
- `configureStore` — sets up store with DevTools + middleware
- `createAsyncThunk` — handles async operations
- Immer integration — write "mutating" code that's actually immutable

```jsx
import { createSlice, configureStore, createAsyncThunk } from '@reduxjs/toolkit';

// createSlice — generates actions and reducer together
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0, status: 'idle' },
  reducers: {
    increment: (state) => {
      state.value += 1;  // Immer allows "mutation" syntax
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    },
  },
});

// Auto-generated action creators
export const { increment, decrement, incrementByAmount } = counterSlice.actions;

// configureStore — sets up store with DevTools
const store = configureStore({
  reducer: {
    counter: counterSlice.reducer,
    // Add more slices here
  },
});

// In React component
import { useSelector, useDispatch } from 'react-redux';

function Counter() {
  const count = useSelector(state => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
    </div>
  );
}
```

---

### Q5. What is `createAsyncThunk`? How does it handle async operations?

**Answer:**
`createAsyncThunk` generates a thunk that dispatches **pending/fulfilled/rejected** actions automatically.

```jsx
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

// createAsyncThunk — handles async lifecycle
const fetchUser = createAsyncThunk(
  'users/fetchById',  // Action type prefix
  async (userId, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch');
      return await response.json();  // Becomes action.payload on success
    } catch (error) {
      return rejectWithValue(error.message);  // Becomes action.payload on failure
    }
  }
);

// Slice handles the three states
const usersSlice = createSlice({
  name: 'users',
  initialState: { data: null, loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

// Usage in component
function UserProfile({ userId }) {
  const dispatch = useDispatch();
  const { data: user, loading, error } = useSelector(state => state.users);

  useEffect(() => {
    dispatch(fetchUser(userId));
  }, [dispatch, userId]);

  if (loading) return <Spinner />;
  if (error) return <Error message={error} />;
  return <div>{user?.name}</div>;
}
```

---

### Q6. What is the difference between `useSelector` and `useDispatch`?

**Answer:**
- `useSelector` — **reads** state from the Redux store (subscribes to changes)
- `useDispatch` — **dispatches** actions to the Redux store

```jsx
import { useSelector, useDispatch } from 'react-redux';
import { increment, fetchUser } from './store';

function Dashboard() {
  const dispatch = useDispatch();

  // useSelector — subscribe to specific slice of state
  // Re-renders ONLY when the selected value changes
  const count = useSelector(state => state.counter.value);
  const user = useSelector(state => state.users.data);
  const isLoading = useSelector(state => state.users.loading);

  // Derived/computed values in selector
  const activeItems = useSelector(state =>
    state.items.list.filter(item => item.active)
  );

  // ⚠️ Avoid creating new objects/arrays in selector (causes re-renders)
  // ❌ const data = useSelector(state => ({ a: state.a, b: state.b }));
  // ✅ Use separate selectors or reselect library

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(fetchUser(1))}>Load User</button>
    </div>
  );
}
```

---

### Q7. What is Zustand? How does it differ from Redux?

**Answer:**
Zustand is a **minimal, fast state management library** with a simple API. No boilerplate, no providers needed.

| Feature | Redux | Zustand |
|---------|-------|---------|
| Boilerplate | High | Minimal |
| Provider | Required | Not required |
| DevTools | Excellent | Good |
| Bundle size | ~10KB | ~1KB |
| Learning curve | Steep | Gentle |
| Best for | Large apps, teams | Small-medium apps |

```jsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Create store — no Provider needed!
const useStore = create((set, get) => ({
  // State
  count: 0,
  user: null,
  items: [],

  // Actions (can be async)
  increment: () => set(state => ({ count: state.count + 1 })),
  decrement: () => set(state => ({ count: state.count - 1 })),

  setUser: (user) => set({ user }),

  fetchItems: async () => {
    const items = await fetch('/api/items').then(r => r.json());
    set({ items });
  },

  // Computed values using get()
  get activeItems() {
    return get().items.filter(item => item.active);
  },
}));

// With persistence middleware
const usePersistedStore = create(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'app-storage' }  // localStorage key
  )
);

// Usage — no Provider, no connect, no mapStateToProps
function Counter() {
  const count = useStore(state => state.count);
  const increment = useStore(state => state.increment);

  return (
    <div>
      <p>{count}</p>
      <button onClick={increment}>+</button>
    </div>
  );
}

// Fine-grained subscriptions — only re-renders when count changes
function CountDisplay() {
  const count = useStore(state => state.count);  // Only subscribes to count
  return <p>{count}</p>;
}
```

---

### Q8. What is React Query (TanStack Query)? What problem does it solve?

**Answer:**
React Query manages **server state** — data that lives on the server and needs to be fetched, cached, synchronized, and updated.

**Problems it solves:**
- Caching and deduplication of requests
- Background refetching
- Loading/error states
- Pagination and infinite scroll
- Optimistic updates
- Stale-while-revalidate pattern

```jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// useQuery — fetch and cache data
function UserProfile({ userId }) {
  const { data: user, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['user', userId],   // Cache key — unique identifier
    queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json()),
    staleTime: 5 * 60 * 1000,    // Data is fresh for 5 minutes
    gcTime: 10 * 60 * 1000,      // Keep in cache for 10 minutes
    retry: 3,                     // Retry failed requests 3 times
    refetchOnWindowFocus: true,   // Refetch when tab regains focus
  });

  if (isLoading) return <Spinner />;
  if (isError) return <Error message={error.message} />;

  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}

// useMutation — create/update/delete data
function CreatePost() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newPost) => fetch('/api/posts', {
      method: 'POST',
      body: JSON.stringify(newPost),
    }).then(r => r.json()),

    onSuccess: () => {
      // Invalidate and refetch posts list
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },

    onMutate: async (newPost) => {
      // Optimistic update — update UI before server responds
      await queryClient.cancelQueries({ queryKey: ['posts'] });
      const previousPosts = queryClient.getQueryData(['posts']);
      queryClient.setQueryData(['posts'], old => [...old, newPost]);
      return { previousPosts };  // Rollback data
    },

    onError: (err, newPost, context) => {
      // Rollback on error
      queryClient.setQueryData(['posts'], context.previousPosts);
    },
  });

  return (
    <button
      onClick={() => mutation.mutate({ title: 'New Post' })}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? 'Creating...' : 'Create Post'}
    </button>
  );
}
```

---

### Q9. What is the difference between server state and client state?

**Answer:**

| | Server State | Client State |
|-|-------------|-------------|
| Location | Remote server | Browser memory |
| Examples | User data, posts, products | Modal open/closed, form input, selected tab |
| Challenges | Caching, sync, stale data | Simpler |
| Tools | React Query, SWR | useState, Zustand, Redux |

```jsx
// Server state — lives on the server, needs fetching
// React Query is perfect for this
const { data: users } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
});

// Client state — lives only in the browser
// useState or Zustand is perfect for this
const [isModalOpen, setIsModalOpen] = useState(false);
const [selectedTab, setSelectedTab] = useState('overview');
const [formData, setFormData] = useState({ name: '', email: '' });

// ❌ Anti-pattern: storing server data in Redux
// Redux is for client state, not server state
// Don't duplicate server data in Redux — use React Query instead

// ✅ Correct separation:
// React Query → server state (users, posts, products)
// Zustand/useState → client state (UI state, user preferences)
```

---

### Q10. What is optimistic updating?

**Answer:**
Optimistic updating **immediately updates the UI** as if the operation succeeded, then rolls back if it fails. Makes the app feel faster.

```jsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function TodoList() {
  const queryClient = useQueryClient();

  const toggleTodo = useMutation({
    mutationFn: ({ id, completed }) =>
      fetch(`/api/todos/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({ completed }),
      }).then(r => r.json()),

    // Optimistic update
    onMutate: async ({ id, completed }) => {
      // Cancel any outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Snapshot previous value for rollback
      const previousTodos = queryClient.getQueryData(['todos']);

      // Optimistically update the cache
      queryClient.setQueryData(['todos'], (old) =>
        old.map(todo =>
          todo.id === id ? { ...todo, completed } : todo
        )
      );

      return { previousTodos };  // Context for rollback
    },

    onError: (err, variables, context) => {
      // Rollback to previous state
      queryClient.setQueryData(['todos'], context.previousTodos);
      toast.error('Failed to update todo');
    },

    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  return (/* render todos */);
}
```

---

### Q11. What is the difference between `staleTime` and `gcTime` in React Query?

**Answer:**
- `staleTime` — how long data is considered **fresh** (won't refetch)
- `gcTime` (formerly `cacheTime`) — how long **unused** data stays in cache before garbage collection

```jsx
useQuery({
  queryKey: ['user', userId],
  queryFn: fetchUser,

  staleTime: 5 * 60 * 1000,   // 5 minutes
  // Data is "fresh" for 5 minutes
  // During this time: no background refetch, even if component remounts

  gcTime: 10 * 60 * 1000,     // 10 minutes
  // After component unmounts, data stays in cache for 10 minutes
  // If component remounts within 10 min: shows cached data while refetching
  // After 10 min: data is garbage collected
});

// Timeline:
// t=0:  Fetch data → data is FRESH
// t=5m: Data becomes STALE → next access triggers background refetch
// t=10m (after unmount): Data is GARBAGE COLLECTED

// Common patterns:
// Static data (rarely changes): staleTime: Infinity
// Real-time data: staleTime: 0 (always refetch)
// User profile: staleTime: 5 * 60 * 1000 (5 min)
```

---

### Q12. When would you choose Redux over Context API?

**Answer:**

**Choose Redux when:**
- Large app with complex state interactions
- Need time-travel debugging (Redux DevTools)
- Multiple developers — need strict conventions
- Frequent state updates from many sources
- Need middleware (logging, analytics, side effects)

**Choose Context when:**
- Simple global state (theme, auth, locale)
- Small to medium app
- Low-frequency updates
- Want to avoid extra dependencies

```jsx
// Context is fine for:
const ThemeContext = createContext('light');  // Changes rarely
const AuthContext = createContext(null);      // Changes on login/logout

// Redux is better for:
// - Shopping cart with complex discount logic
// - Real-time collaborative features
// - Complex form state with validation
// - Undo/redo functionality

// Decision matrix:
// Simple + low frequency → Context
// Complex + high frequency → Redux or Zustand
// Server data → React Query
// Local UI state → useState
```

---

### Q13. What is Jotai? How does it differ from Recoil and Zustand?

**Answer:**
Jotai is an **atomic state management** library — state is split into small atoms that components subscribe to individually.

```jsx
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

// Define atoms (smallest unit of state)
const countAtom = atom(0);
const userAtom = atom(null);

// Derived atom (computed from other atoms)
const doubleCountAtom = atom(get => get(countAtom) * 2);

// Async atom
const userDataAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  return fetch(`/api/users/${userId}`).then(r => r.json());
});

// Usage
function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const doubleCount = useAtomValue(doubleCountAtom);  // Read-only

  return (
    <div>
      <p>Count: {count}, Double: {doubleCount}</p>
      <button onClick={() => setCount(c => c + 1)}>+</button>
    </div>
  );
}

// Only components using countAtom re-render when count changes
// Components using userAtom are unaffected

// Comparison:
// Zustand: store-based, one big store, simple API
// Jotai: atom-based, fine-grained subscriptions, React-like API
// Recoil: atom-based (Facebook), more complex, larger bundle
// Redux: action/reducer pattern, best DevTools, most boilerplate
```

---

### Q14. What is the difference between `useSelector` performance and Context performance?

**Answer:**

```jsx
// Context — ALL consumers re-render when value changes
const AppContext = createContext(null);

function AppProvider({ children }) {
  const [count, setCount] = useState(0);
  const [user, setUser] = useState(null);

  return (
    <AppContext.Provider value={{ count, user, setCount, setUser }}>
      {children}
    </AppContext.Provider>
  );
}

// ❌ UserDisplay re-renders when count changes (even though it only uses user)
function UserDisplay() {
  const { user } = useContext(AppContext);  // Subscribes to ENTIRE context
  return <div>{user?.name}</div>;
}

// Redux useSelector — fine-grained subscriptions
function UserDisplay() {
  const user = useSelector(state => state.user);  // Only re-renders when user changes
  return <div>{user?.name}</div>;
}

function CountDisplay() {
  const count = useSelector(state => state.count);  // Only re-renders when count changes
  return <div>{count}</div>;
}

// Solutions for Context performance:
// 1. Split contexts
// 2. Use useMemo for context value
// 3. Use useReducer + separate dispatch context
// 4. Switch to Zustand/Redux for high-frequency updates
```

---

### Q15. What is optimistic UI and when would you use it?

**Answer:**
Optimistic UI updates the interface **immediately** (assuming success) rather than waiting for the server response.

```jsx
// Without optimistic UI — feels slow
function LikeButton({ postId, initialLikes }) {
  const [likes, setLikes] = useState(initialLikes);
  const [isLoading, setIsLoading] = useState(false);

  const handleLike = async () => {
    setIsLoading(true);
    try {
      const result = await likePost(postId);  // Wait for server...
      setLikes(result.likes);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button onClick={handleLike} disabled={isLoading}>
      {isLoading ? '...' : `❤️ ${likes}`}
    </button>
  );
}

// With optimistic UI — feels instant
function LikeButton({ postId, initialLikes }) {
  const [likes, setLikes] = useState(initialLikes);
  const [isLiked, setIsLiked] = useState(false);

  const handleLike = async () => {
    // Optimistically update UI immediately
    setLikes(prev => prev + 1);
    setIsLiked(true);

    try {
      await likePost(postId);  // Server call in background
    } catch (error) {
      // Rollback on failure
      setLikes(prev => prev - 1);
      setIsLiked(false);
      toast.error('Failed to like post');
    }
  };

  return (
    <button onClick={handleLike}>
      {isLiked ? '❤️' : '🤍'} {likes}
    </button>
  );
}

// Use optimistic UI for:
// ✅ Like/follow buttons
// ✅ Todo completion
// ✅ Form submissions with high success rate
// ❌ Avoid for: financial transactions, irreversible actions
```

---

### [← Back to Index](./00_INDEX.md) | [Next: Component Lifecycle & Patterns →](./10_Lifecycle_Patterns.md)
