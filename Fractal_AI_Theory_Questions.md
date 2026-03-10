# 🧠 Fractal AI — Theory Questions Only
### Python + React | No Code, Pure Concepts

---

# 🐍 PYTHON — Theory Questions

---

## 📦 Category 1: Python Fundamentals

### 🟢 Easy

1. What is the difference between `is` and `==` in Python?
2. What are Python's mutable and immutable data types? Give examples of each.
3. What is the difference between a list and a tuple? When would you use one over the other?
4. What is the difference between `append()` and `extend()` on a list?
5. What are list comprehensions? How are they different from a regular `for` loop?
6. What is the difference between `//` (floor division) and `/` (true division)?
7. What is `None` in Python? How is it different from `0`, `False`, or an empty string?
8. What is the difference between `break`, `continue`, and `pass`?
9. What are Python's built-in data structures? Name at least 4.
10. What is string immutability in Python? What happens when you "modify" a string?
11. What is the difference between `deepcopy` and `shallow copy`?
12. What does the `in` operator do for lists vs dictionaries? Is there a performance difference?
13. What is unpacking in Python? Give an example.
14. What is the difference between `range()` and `xrange()`? (Python 2 vs 3)
15. What are f-strings? How are they different from `.format()` and `%` formatting?

---

### 🟡 Medium

16. What are `*args` and `**kwargs`? When would you use them?
17. What is a Python decorator? What problem does it solve?
18. What is the difference between a shallow copy and a deep copy of a nested object?
19. What is the Global Interpreter Lock (GIL)? How does it affect multi-threaded Python programs?
20. What is the difference between `__str__` and `__repr__`?
21. What are Python's dunder (magic) methods? Name 5 commonly used ones and their purpose.
22. What is the difference between `@staticmethod` and `@classmethod`?
23. What is a lambda function? When should you use it and when should you avoid it?
24. What is the difference between `sorted()` and `.sort()`?
25. What is a Python module vs a package?
26. What is `__init__.py` and why is it needed?
27. What is the difference between `global` and `nonlocal` keywords?
28. What are Python's truthy and falsy values? Name at least 6 falsy values.
29. What is the `with` statement and context managers? What does `__enter__` and `__exit__` do?
30. What is the difference between `isinstance()` and `type()`?

---

### 🔴 Hard

31. What is Python's memory management model? How does reference counting work?
32. What is a circular reference? How does Python's garbage collector handle it?
33. What is the difference between `__slots__` and a regular class? When would you use `__slots__`?
34. What is a metaclass in Python? When would you use one?
35. What is the difference between `__new__` and `__init__`?
36. What is the Python data model? How does operator overloading work?
37. What is the difference between `@property`, `@setter`, and `@deleter`?
38. What is name mangling in Python (double underscore prefix)?
39. What is the difference between `__getattr__` and `__getattribute__`?
40. What is `__call__`? How can a class instance be made callable?

---

## 📦 Category 2: Data Structures & Algorithms

### 🟢 Easy

41. What is the time complexity of common list operations: append, insert, delete, search?
42. What is the time complexity of dictionary lookup, insertion, and deletion?
43. What is the difference between a stack and a queue? What are their real-world use cases?
44. What is a linked list? How is it different from a Python list (array)?
45. What is a hash table? How does Python's `dict` implement it?
46. What is a hash collision? How is it resolved?
47. What is Big-O notation? What does O(1), O(n), O(log n), O(n²) mean?
48. What is the difference between linear search and binary search?
49. What is a set in Python? What are its time complexities for common operations?
50. What is a deque? When would you use it over a list?

---

### 🟡 Medium

51. What is a heap (min-heap / max-heap)? How does Python's `heapq` module work?
52. What is the difference between BFS (Breadth-First Search) and DFS (Depth-First Search)?
53. What is dynamic programming? What is the difference between memoization and tabulation?
54. What is a sliding window technique? When is it applicable?
55. What is a two-pointer technique? Give an example problem where it applies.
56. What is the difference between a stable and unstable sorting algorithm?
57. What sorting algorithm does Python use? What is its time and space complexity?
58. What is a trie (prefix tree)? What problems is it good for?
59. What is a graph? What is the difference between directed and undirected graphs?
60. What is the difference between a tree and a graph?
61. What is a binary search tree (BST)? What are its time complexities for search, insert, delete?
62. What is a balanced BST? Why does balance matter?
63. What is memoization? How does `functools.lru_cache` work?
64. What is the difference between recursion and iteration? What is tail recursion?
65. What is the time complexity of merge sort vs quicksort? When would you prefer one over the other?

---

### 🔴 Hard

66. What is amortized time complexity? Give an example using Python's list `append`.
67. What is the difference between a min-heap and a max-heap? How would you implement a max-heap using Python's `heapq`?
68. What is Dijkstra's algorithm? What problem does it solve and what is its time complexity?
69. What is the difference between greedy algorithms and dynamic programming?
70. What is a topological sort? When is it used?
71. What is the union-find (disjoint set) data structure? What problems does it solve?
72. What is the difference between NP, NP-hard, and NP-complete problems?
73. What is space-time tradeoff? Give a practical example.

---

## 📦 Category 3: Object-Oriented Programming

### 🟢 Easy

74. What are the 4 pillars of OOP? Define each one.
75. What is the difference between a class and an object (instance)?
76. What is a constructor? What is `__init__` in Python?
77. What is inheritance? What is the difference between single and multiple inheritance?
78. What is method overriding? How does it work in Python?
79. What is the difference between public, protected, and private attributes in Python?
80. What is `self` in Python? Why is it needed?

---

### 🟡 Medium

81. What is polymorphism? Give an example of duck typing in Python.
82. What is encapsulation? How does Python achieve it (since it has no true private)?
83. What is abstraction? How do abstract base classes (ABC) work in Python?
84. What is the difference between composition and inheritance? When would you prefer composition?
85. What is method resolution order (MRO)? What algorithm does Python use?
86. What is `super()`? Why is it important in multiple inheritance?
87. What is the difference between class variables and instance variables?
88. What is a mixin? When would you use one?
89. What is the Liskov Substitution Principle (LSP)?
90. What are SOLID principles? Briefly explain each one.

---

### 🔴 Hard

91. What is the difference between an interface and an abstract class? How does Python handle this?
92. What is the diamond problem in multiple inheritance? How does Python resolve it?
93. What is a descriptor in Python? How do `__get__`, `__set__`, and `__delete__` work?
94. What is the difference between `__init_subclass__` and metaclasses?
95. What design patterns have you used? Explain Singleton, Factory, and Observer patterns.

---

## 📦 Category 4: Functional Programming & Advanced Python

### 🟡 Medium

96. What is a closure in Python? What variables does it capture?
97. What is a generator? How is it different from a regular function?
98. What is the difference between `yield` and `return`?
99. What is `yield from`? When would you use it?
100. What is a generator expression vs a list comprehension? When would you use each?
101. What is `map()`, `filter()`, and `reduce()`? Are they still recommended in Python 3?
102. What is a pure function? What are its benefits?
103. What is immutability and why is it important in functional programming?
104. What is `functools.partial`? When is it useful?
105. What is `itertools`? Name 5 useful functions from it.

---

### 🔴 Hard

106. What is the difference between `threading`, `multiprocessing`, and `asyncio`? When would you use each?
107. What is an event loop in asyncio? How does `async/await` work?
108. What is the difference between `async def` and a regular function?
109. What is a coroutine? How is it different from a thread?
110. What is `concurrent.futures`? What is the difference between `ThreadPoolExecutor` and `ProcessPoolExecutor`?

---

## 📦 Category 5: Python for Data & AI (Fractal-Specific)

### 🟡 Medium

111. What is the difference between a Python list and a NumPy array? Why is NumPy faster?
112. What is vectorization in NumPy? Why is it preferred over Python loops?
113. What is broadcasting in NumPy? Give an example.
114. What is a Pandas DataFrame vs a Series?
115. What is the difference between `loc` and `iloc` in Pandas?
116. What is `groupby` in Pandas? How does it work internally (split-apply-combine)?
117. What is the difference between `merge`, `join`, and `concat` in Pandas?
118. What is a pivot table? When would you use it?
119. How would you handle missing values (NaN) in a Pandas DataFrame?
120. What is the difference between `apply`, `map`, and `applymap` in Pandas?
121. What is method chaining in Pandas? What are its pros and cons?
122. What is the difference between wide and long (tidy) data formats? When would you use each?

---

### 🔴 Hard

123. How would you process a CSV file that is larger than your available RAM?
124. What is the difference between eager and lazy evaluation? Give a Python example.
125. What is a data pipeline? What are the key considerations when designing one?
126. What is the difference between ETL and ELT?
127. What is feature engineering? Give 3 examples of common feature transformations.
128. What is data leakage in machine learning? How do you prevent it?
129. What is the difference between normalization and standardization?
130. What is cross-validation? Why is it important?

---

## 📦 Category 6: Python Testing & Best Practices

### 🟡 Medium

131. What is unit testing? What is the difference between unit, integration, and end-to-end tests?
132. What is `pytest`? How is it different from `unittest`?
133. What is a mock? When would you use `unittest.mock`?
134. What is a fixture in pytest?
135. What is test-driven development (TDD)?
136. What is PEP 8? Name 5 key style guidelines.
137. What is type hinting in Python? What are its benefits?
138. What is the difference between `typing.Optional` and `typing.Union`?
139. What is a virtual environment? Why is it important?
140. What is the difference between `requirements.txt` and `pyproject.toml`?

---

# ⚛️ REACT — Theory Questions

---

## 📦 Category 7: React Fundamentals

### 🟢 Easy

141. What is React? What problem does it solve?
142. What is the Virtual DOM? How does it differ from the real DOM?
143. What is JSX? Why does React use it?
144. What is the difference between a functional component and a class component?
145. What are props in React? Are they mutable?
146. What is state in React? How is it different from props?
147. What is the difference between controlled and uncontrolled components?
148. What is event handling in React? How is it different from vanilla JavaScript?
149. What is the `key` prop? Why is it important in lists?
150. What is conditional rendering in React? Name 3 ways to do it.
151. What is the difference between `null`, `undefined`, and `false` in JSX rendering?
152. What is a React fragment? Why would you use `<>...</>` instead of a `<div>`?
153. What is prop drilling? Why is it a problem?
154. What is the difference between `onClick={handleClick}` and `onClick={() => handleClick()}`?
155. What is the difference between `defaultProps` and default parameter values?

---

### 🟡 Medium

156. What is the difference between `React.createElement` and JSX?
157. What is reconciliation in React? How does the diffing algorithm work?
158. What are React's assumptions in its diffing algorithm?
159. What is the difference between mounting, updating, and unmounting?
160. What is a pure component? What is `React.memo`?
161. What is the difference between `React.memo` and `useMemo`?
162. What is the difference between `React.PureComponent` and `React.Component`?
163. What is a higher-order component (HOC)? Give an example use case.
164. What is the render props pattern? When would you use it?
165. What is the children prop? What is `React.Children`?

---

## 📦 Category 8: React Hooks

### 🟢 Easy

166. What are React hooks? Why were they introduced?
167. What are the rules of hooks?
168. What is `useState`? What does it return?
169. What is `useEffect`? What is it used for?
170. What is the difference between `useEffect` with no dependency array, an empty array `[]`, and a filled array?
171. What is the cleanup function in `useEffect`? When does it run?
172. What is `useRef`? What are its two main use cases?
173. What is the difference between `useState` and `useRef`?
174. What is `useContext`? How does it work?
175. What is `useReducer`? How is it different from `useState`?

---

### 🟡 Medium

176. What is `useMemo`? What problem does it solve?
177. What is `useCallback`? How is it different from `useMemo`?
178. When should you use `useMemo` vs `useCallback`?
179. What is a custom hook? What are the rules for creating one?
180. What is `useLayoutEffect`? How is it different from `useEffect`?
181. What is `useId`? When would you use it?
182. What is `useTransition`? What problem does it solve in React 18?
183. What is `useDeferredValue`? How is it different from `useTransition`?
184. What is `useImperativeHandle`? When would you use it with `forwardRef`?
185. What is `useDebugValue`? When is it useful?

---

### 🔴 Hard

186. What is stale closure in React hooks? Give an example and how to fix it.
187. What is the exhaustive-deps ESLint rule? Why is it important?
188. Why can't you call hooks inside conditions or loops?
189. What is the difference between `useEffect` and `useLayoutEffect` in terms of execution timing?
190. What happens if you update state inside `useEffect` without proper dependencies?

---

## 📦 Category 9: State Management

### 🟡 Medium

191. What is the Context API? When should you use it?
192. What are the limitations of the Context API for state management?
193. What is Redux? What are its three core principles?
194. What is the difference between Redux actions, reducers, and the store?
195. What is Redux Toolkit? How does it simplify Redux?
196. What is `createSlice` in Redux Toolkit?
197. What is `createAsyncThunk`? How does it handle async operations?
198. What is the difference between `useSelector` and `useDispatch`?
199. What is Zustand? How does it differ from Redux?
200. What is React Query (TanStack Query)? What problem does it solve?
201. What is the difference between server state and client state?
202. What is optimistic updating? When would you use it?
203. What is the difference between `staleTime` and `gcTime` in React Query?
204. What is Jotai? How does it differ from Recoil and Zustand?
205. When would you choose Redux over Context API? What are the tradeoffs?

---

## 📦 Category 10: Component Lifecycle & Patterns

### 🟡 Medium

206. What is the component lifecycle in React class components? Name the key lifecycle methods.
207. What is `componentDidMount`? What is its functional component equivalent?
208. What is `componentDidUpdate`? What is its functional component equivalent?
209. What is `componentWillUnmount`? What is its functional component equivalent?
210. What is `getDerivedStateFromProps`? When would you use it?
211. What is `shouldComponentUpdate`? What is its functional component equivalent?
212. What is `getSnapshotBeforeUpdate`? When would you use it?
213. What is an Error Boundary? Why must it be a class component?
214. What is `getDerivedStateFromError` vs `componentDidCatch`?
215. What is the Compound Component pattern? What problem does it solve?
216. What is the Provider pattern in React?
217. What is the Container/Presentational component pattern? Is it still relevant with hooks?
218. What is the difference between lifting state up and using context?
219. What is `React.forwardRef`? When would you use it?
220. What is `React.cloneElement`? When would you use it?

---

## 📦 Category 11: Performance Optimization

### 🟡 Medium

221. What causes unnecessary re-renders in React? Name at least 4 causes.
222. How does `React.memo` prevent re-renders? What are its limitations?
223. What is the difference between `React.memo` and `shouldComponentUpdate`?
224. What is code splitting? Why is it important for performance?
225. What is `React.lazy`? How does it work with `Suspense`?
226. What is tree shaking? How does it reduce bundle size?
227. What is virtual scrolling (windowing)? When would you use it?
228. What is the difference between debouncing and throttling? When would you use each?
229. What is lazy loading? How does it apply to images and components?
230. What is a skeleton screen? Why is it better than a spinner for perceived performance?

---

### 🔴 Hard

231. What is the React Profiler? How do you use it to identify performance bottlenecks?
232. What is the difference between time-to-interactive (TTI) and first contentful paint (FCP)?
233. What is hydration in React? What is the difference between SSR and CSR?
234. What is React Server Components (RSC)? How are they different from regular components?
235. What is concurrent rendering in React 18? What problems does it solve?
236. What is the Scheduler in React? What is time slicing?
237. What is `startTransition`? How does it improve user experience?
238. What is the difference between `Suspense` for data fetching vs code splitting?
239. What is memoization at the component level vs at the hook level?
240. What is the impact of context on performance? How do you mitigate it?

---

## 📦 Category 12: React Architecture & Ecosystem

### 🟡 Medium

241. What is the difference between Next.js and Create React App?
242. What is SSR (Server-Side Rendering)? What are its advantages and disadvantages?
243. What is SSG (Static Site Generation)? When would you use it?
244. What is ISR (Incremental Static Regeneration) in Next.js?
245. What is the difference between `getServerSideProps`, `getStaticProps`, and `getStaticPaths`?
246. What is React Router? What is the difference between `BrowserRouter` and `HashRouter`?
247. What is the difference between `useNavigate` and `useHistory`?
248. What is a protected route? How would you implement one?
249. What is Axios? How is it different from the native `fetch` API?
250. What is CORS? How does it affect React applications?
251. What is a service worker? How does it enable offline functionality?
252. What is PWA (Progressive Web App)?
253. What is Webpack? What does it do?
254. What is Vite? How is it different from Webpack?
255. What is TypeScript? What are the benefits of using it with React?

---

### 🔴 Hard

256. What is micro-frontend architecture? When would you use it?
257. What is module federation in Webpack 5?
258. What is the difference between monorepo and polyrepo? What tools support monorepos?
259. What is a design system? What are the benefits of using one?
260. What is accessibility (a11y) in React? Name 5 best practices.

---

## 📦 Category 13: Testing in React

### 🟡 Medium

261. What is React Testing Library? What is its testing philosophy?
262. What is the difference between `getBy`, `queryBy`, and `findBy` in React Testing Library?
263. What is `userEvent` vs `fireEvent`?
264. What is Jest? What is the difference between `describe`, `it`, and `test`?
265. What is a snapshot test? What are its pros and cons?
266. What is mocking in tests? When would you mock an API call?
267. What is `act()` in React testing? Why is it needed?
268. What is Cypress? How is it different from Jest + React Testing Library?
269. What is the difference between unit, integration, and E2E tests in a React context?
270. What is code coverage? What is a good coverage target?

---

## 📦 Category 14: Web Fundamentals (Expected at Fractal AI)

### 🟡 Medium

271. What is the difference between `localStorage`, `sessionStorage`, and cookies?
272. What is the difference between HTTP and HTTPS?
273. What are HTTP methods? What is the difference between GET, POST, PUT, PATCH, and DELETE?
274. What is REST? What are its constraints?
275. What is GraphQL? How is it different from REST?
276. What is WebSocket? How is it different from HTTP polling?
277. What is CSRF (Cross-Site Request Forgery)? How do you prevent it?
278. What is XSS (Cross-Site Scripting)? How do you prevent it in React?
279. What is the browser's event loop? What is the call stack, task queue, and microtask queue?
280. What is the difference between `setTimeout(fn, 0)` and a Promise?
281. What is the critical rendering path in a browser?
282. What is the difference between `async` and `defer` in script tags?
283. What is a CDN? How does it improve performance?
284. What is HTTP caching? What are `Cache-Control` headers?
285. What is the difference between `304 Not Modified` and `200 OK`?

---

## 📦 Category 15: AI/Analytics Concepts (Fractal AI Specific)

### 🟡 Medium

286. What is the difference between supervised, unsupervised, and reinforcement learning?
287. What is overfitting? How do you detect and prevent it?
288. What is the bias-variance tradeoff?
289. What is a confusion matrix? What are precision, recall, F1-score, and accuracy?
290. What is the difference between classification and regression?
291. What is feature importance? How would you explain a model's predictions to a non-technical stakeholder?
292. What is A/B testing? What statistical concepts are involved?
293. What is a data warehouse vs a data lake?
294. What is the difference between OLTP and OLAP?
295. What is a dashboard? What makes a good data visualization?
296. What is the difference between a KPI and a metric?
297. What is data normalization in the context of databases?
298. What is SQL? What is the difference between `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN`?
299. What is the difference between `GROUP BY` and `PARTITION BY` in SQL?
300. What is an index in a database? How does it improve query performance?

---

## 🎯 Quick-Fire Round (Common Verbal Questions)

301. What is the difference between `null` and `undefined` in JavaScript?
302. What is event bubbling and event capturing in the DOM?
303. What is `this` in JavaScript? How does arrow function affect `this`?
304. What is the difference between `==` and `===` in JavaScript?
305. What is a Promise? What is `async/await`?
306. What is the difference between `var`, `let`, and `const`?
307. What is closure in JavaScript?
308. What is the prototype chain in JavaScript?
309. What is the difference between `call`, `apply`, and `bind`?
310. What is a pure function in JavaScript?

---

## 📊 Summary: Questions by Category

| # | Category | Easy | Medium | Hard | Total |
|---|----------|------|--------|------|-------|
| 1 | Python Fundamentals | 15 | 15 | 10 | 40 |
| 2 | Data Structures & Algorithms | 10 | 15 | 8 | 33 |
| 3 | OOP | 7 | 7 | 5 | 19 |
| 4 | Functional & Advanced Python | — | 10 | 5 | 15 |
| 5 | Python for Data & AI | — | 12 | 8 | 20 |
| 6 | Python Testing & Best Practices | — | 10 | — | 10 |
| 7 | React Fundamentals | 15 | 10 | — | 25 |
| 8 | React Hooks | 10 | 10 | 5 | 25 |
| 9 | State Management | — | 15 | — | 15 |
| 10 | Component Lifecycle & Patterns | — | 15 | — | 15 |
| 11 | Performance Optimization | — | 10 | 10 | 20 |
| 12 | React Architecture & Ecosystem | — | 15 | 5 | 20 |
| 13 | Testing in React | — | 10 | — | 10 |
| 14 | Web Fundamentals | — | 15 | — | 15 |
| 15 | AI/Analytics Concepts | — | 15 | — | 15 |
| — | Quick-Fire JS Round | — | 10 | — | 10 |
| **Total** | | **57** | **194** | **56** | **307** |

---

> 💡 **Study tip:** For a 1-hour interview, focus on categories 1–3 (Python) and 7–11 (React). The AI/Analytics section (15) is a bonus differentiator — knowing even 5–6 answers from it will set you apart at Fractal AI.
