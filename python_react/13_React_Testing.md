# 🧪 13 — React Testing
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q10)](#medium)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is React Testing Library? What is its philosophy?

**Answer:**
RTL tests components the way **users interact with them** — querying by accessible attributes, not implementation details.

**Philosophy:** "The more your tests resemble the way your software is used, the more confidence they can give you."

```jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// ❌ Testing implementation details (fragile)
test('bad test', () => {
  const { container } = render(<Button label="Submit" />);
  expect(container.querySelector('.btn-primary')).toBeInTheDocument();
  // Breaks if you rename the CSS class
});

// ✅ Testing user behavior (resilient)
test('good test', async () => {
  const handleClick = jest.fn();
  render(<Button label="Submit" onClick={handleClick} />);

  // Query by what users see/interact with
  const button = screen.getByRole('button', { name: 'Submit' });
  await userEvent.click(button);

  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

---

### Q2. What is the difference between `getBy`, `queryBy`, and `findBy`?

**Answer:**

| Query | Returns | Throws if not found | Async |
|-------|---------|---------------------|-------|
| `getBy*` | Element | ✅ Yes | ❌ |
| `queryBy*` | Element or `null` | ❌ No | ❌ |
| `findBy*` | Promise\<Element\> | ✅ Yes | ✅ |

```jsx
import { render, screen } from '@testing-library/react';

test('query types', async () => {
  render(<UserProfile userId={1} />);

  // getBy — use when element SHOULD be present
  const title = screen.getByRole('heading', { name: 'Alice' });
  const email = screen.getByText('alice@example.com');
  const input = screen.getByLabelText('Email');

  // queryBy — use when element MIGHT not be present
  const errorMsg = screen.queryByRole('alert');
  expect(errorMsg).not.toBeInTheDocument();  // Doesn't throw if null

  // findBy — use for async elements (waits up to 1000ms)
  const loadedData = await screen.findByText('Loaded!');
  // Waits for element to appear in DOM

  // Multiple elements
  const items = screen.getAllByRole('listitem');
  expect(items).toHaveLength(3);
});

// Query priority (RTL recommends):
// 1. getByRole (most accessible)
// 2. getByLabelText (forms)
// 3. getByPlaceholderText
// 4. getByText
// 5. getByDisplayValue
// 6. getByAltText (images)
// 7. getByTitle
// 8. getByTestId (last resort)
```

---

### Q3. What is `userEvent` vs `fireEvent`?

**Answer:**
- `userEvent` — simulates **real user interactions** (fires multiple events, more realistic)
- `fireEvent` — fires a **single DOM event** (lower level, less realistic)

```jsx
import userEvent from '@testing-library/user-event';
import { fireEvent, render, screen } from '@testing-library/react';

test('userEvent vs fireEvent', async () => {
  const user = userEvent.setup();
  render(<SearchInput />);

  const input = screen.getByRole('textbox');

  // fireEvent — fires single event
  fireEvent.change(input, { target: { value: 'hello' } });
  // Only fires 'change' event

  // userEvent — simulates real typing (fires keydown, keypress, input, keyup)
  await user.type(input, 'hello');
  // Fires: focus, keydown, keypress, input, keyup for each character

  // userEvent for clicks
  const button = screen.getByRole('button');
  await user.click(button);  // Fires: pointerover, pointerenter, mouseover, mouseenter, pointermove, mousemove, pointerdown, mousedown, pointerup, mouseup, click

  // Use userEvent for most tests
  // Use fireEvent for simple, specific event testing
});
```

---

### Q4. What is Jest? `describe`, `it`, `test`?

**Answer:**
Jest is a **JavaScript testing framework** with built-in test runner, assertion library, and mocking.

```javascript
// describe — groups related tests
describe('Calculator', () => {
  // beforeEach — runs before each test in this describe
  beforeEach(() => {
    // Setup
  });

  afterEach(() => {
    // Cleanup
  });

  // it and test are identical — use whichever reads better
  it('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('throws on division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  // Nested describe
  describe('edge cases', () => {
    it('handles negative numbers', () => {
      expect(add(-1, -2)).toBe(-3);
    });
  });
});

// Common matchers
expect(value).toBe(5);                    // Strict equality (===)
expect(value).toEqual({ a: 1 });          // Deep equality
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeGreaterThan(3);
expect(array).toContain('item');
expect(array).toHaveLength(3);
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledWith(arg1, arg2);
expect(fn).toHaveBeenCalledTimes(2);
expect(promise).resolves.toBe('value');
expect(promise).rejects.toThrow('error');
```

---

### Q5. What is a snapshot test? Pros and cons?

**Answer:**
A snapshot test captures the **rendered output** of a component and compares it to a stored snapshot on subsequent runs.

```jsx
import { render } from '@testing-library/react';

// Create snapshot
test('Button renders correctly', () => {
  const { container } = render(
    <Button variant="primary" size="md">Click me</Button>
  );
  expect(container).toMatchSnapshot();
  // Creates __snapshots__/Button.test.js.snap
});

// Inline snapshot
test('Button inline snapshot', () => {
  const { container } = render(<Button>Click</Button>);
  expect(container).toMatchInlineSnapshot(`
    <div>
      <button class="btn btn-primary">
        Click
      </button>
    </div>
  `);
});

// Update snapshots: jest --updateSnapshot (or jest -u)

// ✅ Pros:
// - Easy to create
// - Catches unintended UI changes
// - Good for stable components

// ❌ Cons:
// - Easy to blindly update (lose value)
// - Large snapshots are hard to review
// - Brittle — breaks on any change (even whitespace)
// - Doesn't test behavior, only structure

// Better alternative: test behavior, not structure
test('Button shows loading state', () => {
  render(<Button isLoading>Submit</Button>);
  expect(screen.getByRole('button')).toBeDisabled();
  expect(screen.getByTestId('spinner')).toBeInTheDocument();
});
```

---

### Q6. What is mocking in tests? When would you mock an API call?

**Answer:**
Mocking replaces real implementations with **controlled fakes** to isolate the unit under test.

```jsx
import { render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Method 1: Mock with jest.fn()
test('calls onSubmit with form data', async () => {
  const mockSubmit = jest.fn().mockResolvedValue({ success: true });
  render(<LoginForm onSubmit={mockSubmit} />);

  await userEvent.type(screen.getByLabelText('Email'), 'alice@example.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password123');
  await userEvent.click(screen.getByRole('button', { name: 'Sign in' }));

  expect(mockSubmit).toHaveBeenCalledWith({
    email: 'alice@example.com',
    password: 'password123',
  });
});

// Method 2: Mock with MSW (Mock Service Worker) — recommended
const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'Alice', email: 'alice@example.com' }));
  }),

  rest.post('/api/login', (req, res, ctx) => {
    return res(ctx.json({ token: 'fake-token' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('loads and displays user', async () => {
  render(<UserProfile userId={1} />);

  expect(screen.getByText('Loading...')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });
});

// Override for specific test
test('shows error on failed request', async () => {
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) => {
      return res(ctx.status(500), ctx.json({ error: 'Server error' }));
    })
  );

  render(<UserProfile userId={1} />);
  await waitFor(() => {
    expect(screen.getByRole('alert')).toHaveTextContent('Server error');
  });
});
```

---

### Q7. What is `act()` in React testing?

**Answer:**
`act()` ensures all **state updates and effects are processed** before making assertions. RTL wraps most interactions in `act()` automatically.

```jsx
import { act, render, screen } from '@testing-library/react';

// RTL automatically wraps in act():
// - render()
// - fireEvent.*
// - userEvent.*
// - waitFor()

// Manual act() — needed for:
// - Direct state updates outside RTL
// - Custom hooks testing

import { renderHook, act } from '@testing-library/react';

test('useCounter hook', () => {
  const { result } = renderHook(() => useCounter(0));

  expect(result.current.count).toBe(0);

  act(() => {
    result.current.increment();  // State update must be wrapped in act()
  });

  expect(result.current.count).toBe(1);
});

// Testing async state updates
test('async state update', async () => {
  render(<AsyncComponent />);

  await act(async () => {
    await userEvent.click(screen.getByRole('button'));
    // Wait for all async operations to complete
  });

  expect(screen.getByText('Done!')).toBeInTheDocument();
});
```

---

### Q8. What is Cypress? How is it different from Jest + RTL?

**Answer:**

| Feature | Jest + RTL | Cypress |
|---------|-----------|---------|
| Type | Unit/Integration | E2E |
| Runs in | Node.js (jsdom) | Real browser |
| Speed | Fast | Slower |
| Debugging | Console | Visual time-travel |
| Network | Mocked | Real or intercepted |
| Use case | Component behavior | Full user flows |

```javascript
// Cypress — E2E test
describe('Login flow', () => {
  it('logs in successfully', () => {
    cy.visit('/login');

    cy.get('[data-testid="email-input"]').type('alice@example.com');
    cy.get('[data-testid="password-input"]').type('password123');
    cy.get('[data-testid="submit-button"]').click();

    // Assert redirect to dashboard
    cy.url().should('include', '/dashboard');
    cy.contains('Welcome, Alice').should('be.visible');
  });

  it('shows error on invalid credentials', () => {
    cy.visit('/login');
    cy.intercept('POST', '/api/login', { statusCode: 401 });  // Mock API

    cy.get('[data-testid="email-input"]').type('wrong@example.com');
    cy.get('[data-testid="password-input"]').type('wrongpassword');
    cy.get('[data-testid="submit-button"]').click();

    cy.get('[role="alert"]').should('contain', 'Invalid credentials');
  });
});

// Testing pyramid:
// Many unit tests (fast, cheap)
// Some integration tests (medium)
// Few E2E tests (slow, expensive)
```

---

### Q9. What is the difference between unit, integration, and E2E tests in React?

**Answer:**

```jsx
// UNIT TEST — single component in isolation
test('Button renders with correct label', () => {
  render(<Button label="Submit" />);
  expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
});

// INTEGRATION TEST — multiple components working together
test('Form submits data correctly', async () => {
  const mockApi = jest.fn().mockResolvedValue({ success: true });
  render(<LoginForm onSubmit={mockApi} />);

  await userEvent.type(screen.getByLabelText('Email'), 'alice@example.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password');
  await userEvent.click(screen.getByRole('button', { name: 'Sign in' }));

  await waitFor(() => {
    expect(mockApi).toHaveBeenCalledWith({
      email: 'alice@example.com',
      password: 'password',
    });
    expect(screen.getByText('Login successful!')).toBeInTheDocument();
  });
});

// E2E TEST — full application flow (Cypress/Playwright)
// cy.visit('/login')
// cy.get('input[name=email]').type('alice@example.com')
// cy.get('button[type=submit]').click()
// cy.url().should('eq', 'http://localhost:3000/dashboard')
```

---

### Q10. What is code coverage? What is a good target?

**Answer:**
Code coverage measures **what percentage of your code is executed** during tests.

```javascript
// Run with coverage
// jest --coverage

// Coverage report shows:
// Statements: 85%  — lines executed
// Branches:   78%  — if/else paths taken
// Functions:  90%  — functions called
// Lines:      85%  — lines executed

// Good targets (context-dependent):
// Critical business logic: 90%+
// UI components: 70-80%
// Utility functions: 90%+
// Overall: 70-80% is reasonable

// jest.config.js — enforce coverage thresholds
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.stories.{js,jsx}',
    '!src/index.js',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    // Per-file thresholds
    './src/utils/': {
      branches: 90,
      functions: 95,
    },
  },
};

// ⚠️ 100% coverage ≠ good tests
// Focus on testing behavior, not achieving coverage numbers
// A test that just calls a function without assertions is useless
```

---

### [← Back to Index](./00_INDEX.md) | [Next: Web Fundamentals →](./14_Web_Fundamentals.md)
