# ⚡ 16 — JavaScript Quick-Fire Round
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q10)](#medium)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is the difference between `null` and `undefined`?

**Answer:**
- `undefined` — variable declared but **not assigned** a value (JavaScript's default)
- `null` — intentional **absence of value** (explicitly set by developer)

```javascript
let x;
console.log(x);           // undefined — declared, not assigned

let y = null;
console.log(y);           // null — intentionally empty

console.log(typeof undefined);  // "undefined"
console.log(typeof null);       // "object" ← famous JS bug (legacy)

// Equality
console.log(null == undefined);   // true  (loose equality — both "empty")
console.log(null === undefined);  // false (strict equality — different types)

// Nullish coalescing — handles both null and undefined
const value = null ?? 'default';      // 'default'
const value2 = undefined ?? 'default'; // 'default'
const value3 = 0 ?? 'default';        // 0 (0 is not null/undefined)

// Optional chaining
const user = null;
console.log(user?.name);        // undefined (no error)
console.log(user?.address?.city); // undefined (no error)

// Common patterns
function getUser(id) {
  if (!id) return null;  // Intentional absence
  return fetchUser(id);
}

function processData(data) {
  const name = data.name ?? 'Anonymous';  // Default if null/undefined
  const age = data.age || 18;             // Default if falsy (0 also replaced!)
}
```

---

### Q2. What is event bubbling and event capturing?

**Answer:**
- **Capturing** (trickling) — event travels **down** from root to target
- **Bubbling** — event travels **up** from target to root (default)

```html
<div id="outer">
  <div id="middle">
    <button id="inner">Click me</button>
  </div>
</div>
```

```javascript
// Event flow: outer → middle → inner (capturing) → inner → middle → outer (bubbling)

// Bubbling (default) — addEventListener with false or no 3rd arg
document.getElementById('outer').addEventListener('click', () => {
  console.log('outer bubbling');
});
document.getElementById('inner').addEventListener('click', () => {
  console.log('inner bubbling');
});
// Click button: "inner bubbling" → "outer bubbling"

// Capturing — addEventListener with true
document.getElementById('outer').addEventListener('click', () => {
  console.log('outer capturing');
}, true);
// Click button: "outer capturing" → "inner bubbling"

// Stop bubbling
document.getElementById('inner').addEventListener('click', (e) => {
  e.stopPropagation();  // Stops event from bubbling up
  console.log('inner — stopped');
});

// Event delegation — use bubbling to handle events on parent
document.getElementById('list').addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    console.log('Clicked:', e.target.textContent);
  }
});
// Works for dynamically added <li> elements too!
```

---

### Q3. What is `this` in JavaScript? How does arrow function affect it?

**Answer:**
`this` refers to the **execution context** — the object that "owns" the current code.

```javascript
// 1. Global context
console.log(this);  // window (browser) or {} (Node.js)

// 2. Object method — this = the object
const user = {
  name: 'Alice',
  greet() {
    console.log(this.name);  // 'Alice'
  },
};
user.greet();

// 3. Regular function — this depends on how it's called
function greet() {
  console.log(this);  // window (non-strict) or undefined (strict)
}

// 4. Arrow function — this is LEXICALLY bound (inherits from enclosing scope)
const obj = {
  name: 'Alice',
  greetRegular: function() {
    setTimeout(function() {
      console.log(this.name);  // undefined — 'this' is window in callback
    }, 100);
  },
  greetArrow: function() {
    setTimeout(() => {
      console.log(this.name);  // 'Alice' — arrow inherits 'this' from greetArrow
    }, 100);
  },
};

// 5. Class — this = instance
class Counter {
  count = 0;
  increment() {
    this.count++;  // this = Counter instance
  }
}

// 6. Explicit binding
function greet(greeting) {
  console.log(`${greeting}, ${this.name}`);
}
const alice = { name: 'Alice' };
greet.call(alice, 'Hello');    // Hello, Alice
greet.apply(alice, ['Hi']);    // Hi, Alice
const boundGreet = greet.bind(alice);
boundGreet('Hey');             // Hey, Alice
```

---

### Q4. What is the difference between `==` and `===`?

**Answer:**
- `==` (loose equality) — **type coercion** before comparison
- `===` (strict equality) — **no type coercion**, must be same type AND value

```javascript
// == with type coercion
console.log(1 == '1');      // true  (string '1' coerced to number 1)
console.log(0 == false);    // true  (false coerced to 0)
console.log(null == undefined); // true (special case)
console.log('' == false);   // true  (both coerce to 0)
console.log([] == false);   // true  ([] → '' → 0, false → 0)

// === without coercion
console.log(1 === '1');     // false (different types)
console.log(0 === false);   // false (different types)
console.log(null === undefined); // false (different types)

// ✅ Always use === (avoids confusing coercion rules)
// Exception: null check (null == undefined catches both)
if (value == null) {  // Catches both null and undefined
  // ...
}

// Object comparison — both == and === compare by reference
const a = { x: 1 };
const b = { x: 1 };
console.log(a == b);   // false (different objects)
console.log(a === b);  // false (different objects)
console.log(a === a);  // true  (same reference)
```

---

### Q5. What is a Promise? What is `async/await`?

**Answer:**
A Promise represents a **future value** — the result of an asynchronous operation.

```javascript
// Promise states: pending → fulfilled | rejected

// Creating a Promise
const fetchUser = (id) => new Promise((resolve, reject) => {
  setTimeout(() => {
    if (id > 0) {
      resolve({ id, name: 'Alice' });  // Success
    } else {
      reject(new Error('Invalid ID'));  // Failure
    }
  }, 1000);
});

// Using Promise
fetchUser(1)
  .then(user => console.log(user.name))  // 'Alice'
  .catch(err => console.error(err.message))
  .finally(() => console.log('Done'));

// Promise chaining
fetchUser(1)
  .then(user => fetchPosts(user.id))  // Returns another Promise
  .then(posts => console.log(posts))
  .catch(err => console.error(err));

// Promise.all — run in parallel, wait for all
const [user, posts, comments] = await Promise.all([
  fetchUser(1),
  fetchPosts(1),
  fetchComments(1),
]);

// Promise.allSettled — wait for all, even if some fail
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(-1),  // Will reject
]);
// [{ status: 'fulfilled', value: {...} }, { status: 'rejected', reason: Error }]

// async/await — syntactic sugar over Promises
async function loadUserData(userId) {
  try {
    const user = await fetchUser(userId);    // Pauses here
    const posts = await fetchPosts(user.id); // Pauses here
    return { user, posts };
  } catch (error) {
    console.error('Failed:', error.message);
    throw error;  // Re-throw if needed
  }
}

// Parallel with async/await
async function loadAll(userId) {
  const [user, posts] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
  ]);
  return { user, posts };
}
```

---

### Q6. What is the difference between `var`, `let`, and `const`?

**Answer:**

| Feature | `var` | `let` | `const` |
|---------|-------|-------|---------|
| Scope | Function | Block | Block |
| Hoisting | Yes (undefined) | Yes (TDZ) | Yes (TDZ) |
| Re-declare | ✅ | ❌ | ❌ |
| Re-assign | ✅ | ✅ | ❌ |
| Global object | ✅ | ❌ | ❌ |

```javascript
// var — function scoped, hoisted
function example() {
  console.log(x);  // undefined (hoisted, not error)
  var x = 5;
  console.log(x);  // 5

  if (true) {
    var y = 10;  // Function scoped — accessible outside if block
  }
  console.log(y);  // 10
}

// let — block scoped, TDZ (Temporal Dead Zone)
function example2() {
  // console.log(x);  // ReferenceError: Cannot access 'x' before initialization
  let x = 5;

  if (true) {
    let y = 10;  // Block scoped
  }
  // console.log(y);  // ReferenceError: y is not defined
}

// const — block scoped, must be initialized, can't be reassigned
const PI = 3.14159;
// PI = 3;  // TypeError: Assignment to constant variable

// ⚠️ const doesn't make objects immutable!
const user = { name: 'Alice' };
user.name = 'Bob';  // ✅ OK — modifying property, not reassigning
// user = {};       // ❌ Error — reassigning the variable

// Best practice: use const by default, let when reassignment needed, avoid var
```

---

### Q7. What is closure in JavaScript?

**Answer:**
A closure is a function that **remembers variables from its outer scope** even after the outer function has returned.

```javascript
// Basic closure
function makeCounter(initial = 0) {
  let count = initial;  // Captured by inner functions

  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
    reset: () => { count = initial; },
  };
}

const counter = makeCounter(10);
console.log(counter.increment());  // 11
console.log(counter.increment());  // 12
console.log(counter.decrement());  // 11
console.log(counter.getCount());   // 11

// Each call creates a new closure
const counter2 = makeCounter(0);
console.log(counter2.getCount());  // 0 — independent from counter

// Practical use: memoization
function memoize(fn) {
  const cache = {};  // Captured by wrapper
  return function(...args) {
    const key = JSON.stringify(args);
    if (key in cache) return cache[key];
    cache[key] = fn(...args);
    return cache[key];
  };
}

const expensiveCalc = memoize((n) => {
  console.log('Computing...');
  return n * n;
});

expensiveCalc(5);  // Computing... 25
expensiveCalc(5);  // 25 (cached, no "Computing...")

// ⚠️ Classic closure bug in loops
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 3, 3, 3 (all share same i)
}

// Fix 1: let (block scoped)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 0, 1, 2
}

// Fix 2: IIFE
for (var i = 0; i < 3; i++) {
  ((j) => setTimeout(() => console.log(j), 100))(i);  // 0, 1, 2
}
```

---

### Q8. What is the prototype chain in JavaScript?

**Answer:**
Every JavaScript object has a `[[Prototype]]` — a reference to another object. When a property isn't found on an object, JavaScript looks up the **prototype chain**.

```javascript
// Prototype chain
const animal = {
  breathe() { return 'breathing'; },
};

const dog = Object.create(animal);  // dog's prototype = animal
dog.bark = function() { return 'woof'; };

console.log(dog.bark());     // 'woof' — own property
console.log(dog.breathe());  // 'breathing' — found on prototype
console.log(dog.toString()); // '[object Object]' — found on Object.prototype

// Prototype chain: dog → animal → Object.prototype → null

// Class syntax (syntactic sugar over prototypes)
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    return `${this.name} makes a sound`;
  }
}

class Dog extends Animal {
  speak() {
    return `${this.name} barks`;
  }
}

const d = new Dog('Rex');
console.log(d.speak());  // 'Rex barks'
console.log(d instanceof Dog);    // true
console.log(d instanceof Animal); // true

// Prototype chain: d → Dog.prototype → Animal.prototype → Object.prototype → null

// hasOwnProperty — check if property is own (not inherited)
console.log(d.hasOwnProperty('name'));   // true (own)
console.log(d.hasOwnProperty('speak')); // false (on prototype)
```

---

### Q9. What is the difference between `call`, `apply`, and `bind`?

**Answer:**
All three set `this` explicitly, but differ in how they pass arguments and when they execute.

```javascript
function greet(greeting, punctuation) {
  return `${greeting}, ${this.name}${punctuation}`;
}

const alice = { name: 'Alice' };
const bob = { name: 'Bob' };

// call — invoke immediately, args as comma-separated
console.log(greet.call(alice, 'Hello', '!'));   // Hello, Alice!
console.log(greet.call(bob, 'Hi', '.'));        // Hi, Bob.

// apply — invoke immediately, args as array
console.log(greet.apply(alice, ['Hello', '!'])); // Hello, Alice!
console.log(greet.apply(bob, ['Hi', '.']));      // Hi, Bob.

// bind — returns NEW function with this bound (doesn't invoke)
const greetAlice = greet.bind(alice);
console.log(greetAlice('Hey', '?'));  // Hey, Alice?

// Partial application with bind
const greetAliceHello = greet.bind(alice, 'Hello');
console.log(greetAliceHello('!'));  // Hello, Alice!
console.log(greetAliceHello('?'));  // Hello, Alice?

// Practical use: fixing this in callbacks
class Timer {
  constructor() {
    this.seconds = 0;
  }

  start() {
    // ❌ this is undefined in callback
    // setInterval(function() { this.seconds++; }, 1000);

    // ✅ bind fixes this
    setInterval(function() { this.seconds++; }.bind(this), 1000);

    // ✅ Arrow function also works
    setInterval(() => { this.seconds++; }, 1000);
  }
}

// Summary:
// call(thisArg, arg1, arg2)  → invoke now, spread args
// apply(thisArg, [arg1, arg2]) → invoke now, array args
// bind(thisArg, arg1)         → return new function, don't invoke
```

---

### Q10. What is a pure function in JavaScript?

**Answer:**
A pure function:
1. Always returns the **same output for the same input**
2. Has **no side effects** (doesn't modify external state)

```javascript
// ✅ Pure functions
const add = (a, b) => a + b;
const double = (arr) => arr.map(x => x * 2);  // Returns new array
const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

// ❌ Impure — depends on external state
let multiplier = 2;
const multiply = (x) => x * multiplier;  // Result changes if multiplier changes

// ❌ Impure — modifies external state (side effect)
const users = [];
const addUser = (user) => {
  users.push(user);  // Mutates external array
  return users;
};

// ✅ Pure version
const addUserPure = (users, user) => [...users, user];  // Returns new array

// ❌ Impure — I/O side effects
const logAndDouble = (x) => {
  console.log(x);  // Side effect
  return x * 2;
};

// Benefits of pure functions:
// ✅ Predictable — same input → same output
// ✅ Testable — no mocks needed
// ✅ Cacheable — memoizable
// ✅ Parallelizable — no shared state
// ✅ Composable — easy to chain

// Function composition
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const transform = pipe(
  x => x * 2,
  x => x + 1,
  x => x.toString()
);

console.log(transform(5));  // "11" (5*2=10, 10+1=11, "11")
```

---

## 🎯 Bonus: Common JavaScript Gotchas

```javascript
// 1. typeof null === 'object' (bug)
typeof null === 'object'  // true — use === null instead

// 2. NaN is not equal to itself
NaN === NaN  // false — use Number.isNaN(value)

// 3. Floating point
0.1 + 0.2 === 0.3  // false (0.30000000000000004)
Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON  // true ✅

// 4. Array.isArray vs typeof
typeof []  // 'object' — not helpful
Array.isArray([])  // true ✅

// 5. parseInt gotcha
parseInt('08')  // 8 (modern JS)
parseInt('08', 10)  // 8 — always specify radix ✅

// 6. Truthy/falsy
Boolean(0)    // false
Boolean('')   // false
Boolean([])   // true  ← empty array is truthy!
Boolean({})   // true  ← empty object is truthy!

// 7. Spread vs Object.assign (shallow copy)
const obj = { a: 1, nested: { b: 2 } };
const copy = { ...obj };
copy.nested.b = 99;
console.log(obj.nested.b);  // 99 — shallow copy!

// 8. Array destructuring with default
const [a = 1, b = 2] = [10];
console.log(a, b);  // 10, 2

// 9. Short-circuit evaluation
const result = condition && expensiveOperation();  // Only runs if condition is truthy
const value = maybeNull || 'default';  // Use ?? for null/undefined only
```

---

### [← Back to Index](./00_INDEX.md)

---

## 🏁 You're Ready!

All 16 sections complete. Here's your final prep checklist:

- [ ] **Python:** GIL, decorators, generators, OOP pillars, list/dict complexity
- [ ] **DSA:** Two Sum (hash map), Binary Search, LRU Cache, BFS/DFS
- [ ] **React:** useEffect patterns, useMemo vs useCallback, custom hooks
- [ ] **State:** Context limitations, Redux vs Zustand, React Query
- [ ] **Performance:** React.memo, virtual scrolling, code splitting
- [ ] **AI/Analytics:** Overfitting, confusion matrix, SQL JOINs, GROUP BY vs PARTITION BY
- [ ] **Mindset:** Think out loud, clarify before coding, state complexity

**Good luck at Fractal AI! 🚀**
