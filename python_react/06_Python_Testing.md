# 🧪 06 — Python Testing & Best Practices
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟡 Medium (Q1–Q10)](#medium)

---

<a name="medium"></a>
## 🟡 Medium

---

### Q1. What is unit testing? Unit vs integration vs E2E?

**Answer:**

| Type | Scope | Speed | Dependencies | Example |
|------|-------|-------|-------------|---------|
| **Unit** | Single function/class | Very fast | Mocked | Test `calculate_tax()` |
| **Integration** | Multiple components | Medium | Real or partial | Test DB + service layer |
| **E2E** | Full system | Slow | Real | Test user login flow |

```python
# Unit test — isolated, fast, no external dependencies
import pytest

def calculate_tax(income: float, rate: float = 0.2) -> float:
    if income < 0:
        raise ValueError("Income cannot be negative")
    return income * rate

class TestCalculateTax:
    def test_basic_calculation(self):
        assert calculate_tax(1000) == 200.0

    def test_custom_rate(self):
        assert calculate_tax(1000, rate=0.3) == 300.0

    def test_zero_income(self):
        assert calculate_tax(0) == 0.0

    def test_negative_income_raises(self):
        with pytest.raises(ValueError, match="Income cannot be negative"):
            calculate_tax(-100)

    def test_float_precision(self):
        result = calculate_tax(100.5, rate=0.1)
        assert abs(result - 10.05) < 1e-9  # Float comparison
```

---

### Q2. What is `pytest`? How is it different from `unittest`?

**Answer:**

| Feature | pytest | unittest |
|---------|--------|---------|
| Syntax | Simple functions | Class-based |
| Assertions | Plain `assert` | `assertEqual`, `assertTrue`, etc. |
| Fixtures | `@pytest.fixture` | `setUp`/`tearDown` |
| Parametrize | `@pytest.mark.parametrize` | Manual loops |
| Discovery | Auto-discovers `test_*.py` | Requires `TestCase` |
| Output | Detailed, colored | Basic |

```python
# unittest style
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.add(2, 3), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.divide(10, 0)

    def tearDown(self):
        pass

# pytest style — simpler, more Pythonic
class Calculator:
    def add(self, a, b): return a + b
    def divide(self, a, b): return a / b

def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)

# Parametrize — test multiple inputs
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add_parametrized(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected
```

---

### Q3. What is a mock? When would you use `unittest.mock`?

**Answer:**
A mock is a **fake object** that replaces a real dependency during testing. Use mocks to:
- Isolate the unit under test
- Avoid slow/expensive operations (DB, API calls, file I/O)
- Test error conditions that are hard to reproduce

```python
from unittest.mock import Mock, MagicMock, patch, call
import pytest

# Mock — basic fake object
mock = Mock()
mock.method(1, 2)
mock.method.assert_called_once_with(1, 2)
mock.method.return_value = 42
print(mock.method())  # 42

# patch — replace real object with mock during test
class UserService:
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id: int) -> dict:
        user = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user

def test_get_user_success():
    mock_db = Mock()
    mock_db.query.return_value = {"id": 1, "name": "Alice"}

    service = UserService(mock_db)
    user = service.get_user(1)

    assert user["name"] == "Alice"
    mock_db.query.assert_called_once_with("SELECT * FROM users WHERE id = 1")

def test_get_user_not_found():
    mock_db = Mock()
    mock_db.query.return_value = None

    service = UserService(mock_db)
    with pytest.raises(ValueError, match="User 99 not found"):
        service.get_user(99)

# patch as decorator — replaces during test, restores after
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    mock_get.return_value.status_code = 200

    # Your code that calls requests.get
    import requests
    response = requests.get("https://api.example.com")
    assert response.json() == {"status": "ok"}

# patch as context manager
def test_file_read():
    with patch('builtins.open', mock_open(read_data="hello world")):
        with open("file.txt") as f:
            content = f.read()
    assert content == "hello world"
```

---

### Q4. What is a fixture in pytest?

**Answer:**
A fixture is a **reusable setup/teardown function** that provides test dependencies. Fixtures support dependency injection and scoping.

```python
import pytest
import sqlite3

# Basic fixture
@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):   # pytest injects the fixture
    assert calculator.add(2, 3) == 5

# Fixture with teardown (yield)
@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    yield conn          # Test runs here
    conn.close()        # Teardown after test

def test_insert_user(db_connection):
    db_connection.execute("INSERT INTO users VALUES (1, 'Alice')")
    cursor = db_connection.execute("SELECT * FROM users")
    assert cursor.fetchone() == (1, 'Alice')

# Fixture scopes
@pytest.fixture(scope="session")   # Created once per test session
def expensive_resource():
    return setup_expensive_thing()

@pytest.fixture(scope="module")    # Created once per module
def module_resource():
    return setup_module_thing()

@pytest.fixture(scope="function")  # Default: created per test
def function_resource():
    return setup_function_thing()

# Fixture with parameters
@pytest.fixture(params=["sqlite", "postgres"])
def database(request):
    if request.param == "sqlite":
        return SQLiteDB()
    return PostgresDB()

# conftest.py — shared fixtures across test files
# Place fixtures in conftest.py to share across multiple test files
```

---

### Q5. What is test-driven development (TDD)?

**Answer:**
TDD is a development process where you **write tests before writing code**:

1. **Red** — Write a failing test
2. **Green** — Write minimal code to pass the test
3. **Refactor** — Improve code while keeping tests green

```python
# TDD Example: Building a Stack class

# Step 1: RED — write failing test
def test_stack_push_and_pop():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2   # LIFO

def test_stack_empty():
    stack = Stack()
    assert stack.is_empty() is True
    stack.push(1)
    assert stack.is_empty() is False

def test_stack_pop_empty_raises():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek():
    stack = Stack()
    stack.push(42)
    assert stack.peek() == 42
    assert stack.is_empty() is False  # peek doesn't remove

# Step 2: GREEN — minimal implementation
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

# Step 3: REFACTOR — improve without breaking tests
# (add type hints, docstrings, optimize if needed)

# Benefits of TDD:
# ✅ Forces you to think about API before implementation
# ✅ Built-in regression tests
# ✅ Confidence to refactor
# ✅ Documentation through tests
```

---

### Q6. What is PEP 8? Name 5 key style guidelines.

**Answer:**
PEP 8 is Python's **official style guide** for writing readable code.

```python
# 1. INDENTATION — 4 spaces (not tabs)
def good_function():
    if True:
        return 1

# 2. LINE LENGTH — max 79 characters (99 for modern projects)
# ❌ Too long
result = some_function(argument_one, argument_two, argument_three, argument_four)

# ✅ Break it up
result = some_function(
    argument_one,
    argument_two,
    argument_three,
    argument_four
)

# 3. NAMING CONVENTIONS
class MyClass:          # PascalCase for classes
    my_attribute = 1    # snake_case for variables/functions
    MY_CONSTANT = 42    # UPPER_CASE for constants
    _protected = True   # Single underscore for protected
    __private = True    # Double underscore for private

def my_function():      # snake_case for functions
    pass

# 4. BLANK LINES
# 2 blank lines between top-level definitions
class FirstClass:
    pass


class SecondClass:
    pass


# 1 blank line between methods
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass

# 5. IMPORTS — one per line, grouped: stdlib → third-party → local
import os
import sys

import numpy as np
import pandas as pd

from mypackage import mymodule

# 6. WHITESPACE
x = 1           # ✅ Spaces around =
y = x + 1       # ✅ Spaces around operators
lst[1:3]        # ✅ No spaces in slices
func(arg=1)     # ✅ No spaces around = in keyword args

# 7. DOCSTRINGS
def calculate(x: float, y: float) -> float:
    """
    Calculate the sum of two numbers.

    Args:
        x: First number
        y: Second number

    Returns:
        Sum of x and y

    Raises:
        TypeError: If inputs are not numeric
    """
    return x + y
```

---

### Q7. What is type hinting in Python? What are its benefits?

**Answer:**
Type hints (PEP 484) add **optional type annotations** to Python code. They don't affect runtime but enable static analysis.

```python
from typing import List, Dict, Optional, Union, Tuple, Any, Callable
from typing import TypeVar, Generic

# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# Complex types
def process(
    data: List[Dict[str, Any]],
    key: str,
    default: Optional[float] = None
) -> List[float]:
    return [item.get(key, default) for item in data]

# Union — multiple possible types
def parse_id(id_val: Union[str, int]) -> int:
    return int(id_val)

# Python 3.10+ — use | instead of Union
def parse_id_new(id_val: str | int) -> int:
    return int(id_val)

# Optional — can be None (shorthand for Union[X, None])
def find_user(user_id: int) -> Optional[dict]:
    return None  # or a dict

# Callable
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

# TypeVar — generic functions
T = TypeVar('T')

def first(lst: List[T]) -> Optional[T]:
    return lst[0] if lst else None

# Benefits:
# ✅ IDE autocomplete and error detection
# ✅ Static analysis with mypy
# ✅ Self-documenting code
# ✅ Catch bugs before runtime
# ✅ Better refactoring support

# Run mypy: mypy my_file.py
```

---

### Q8. What is the difference between `typing.Optional` and `typing.Union`?

**Answer:**
- `Optional[X]` is shorthand for `Union[X, None]`
- `Union[X, Y]` means the value can be type X **or** type Y

```python
from typing import Optional, Union

# Optional[str] == Union[str, None]
def find_name(user_id: int) -> Optional[str]:
    # Returns a string or None
    return "Alice" if user_id == 1 else None

# Union — multiple non-None types
def parse_value(val: Union[str, int, float]) -> float:
    return float(val)

# Python 3.10+ syntax
def find_name_new(user_id: int) -> str | None:
    return "Alice" if user_id == 1 else None

def parse_value_new(val: str | int | float) -> float:
    return float(val)

# Common patterns
from typing import List, Dict

def process(
    items: List[Union[str, int]],   # List of strings or ints
    config: Optional[Dict] = None   # Optional config dict
) -> None:
    pass
```

---

### Q9. What is a virtual environment? Why is it important?

**Answer:**
A virtual environment is an **isolated Python environment** with its own packages, separate from the system Python.

```bash
# Create virtual environment
python -m venv myenv

# Activate (Windows)
myenv\Scripts\activate

# Activate (Mac/Linux)
source myenv/bin/activate

# Install packages (isolated to this env)
pip install numpy pandas

# Save dependencies
pip freeze > requirements.txt

# Recreate environment
pip install -r requirements.txt

# Deactivate
deactivate
```

```python
# Why virtual environments matter:
# 1. Project isolation — different projects can use different package versions
# 2. No conflicts — project A needs numpy 1.x, project B needs numpy 2.x
# 3. Reproducibility — requirements.txt captures exact versions
# 4. Clean system — don't pollute global Python installation

# Modern alternatives:
# - poetry: dependency management + packaging
# - pipenv: combines pip + virtualenv
# - conda: for data science (handles non-Python deps too)
# - uv: ultra-fast Python package manager (Rust-based)

# pyproject.toml (modern standard)
# [project]
# name = "myproject"
# version = "1.0.0"
# dependencies = [
#     "numpy>=1.24",
#     "pandas>=2.0",
# ]
```

---

### Q10. What is the difference between `requirements.txt` and `pyproject.toml`?

**Answer:**

| Feature | `requirements.txt` | `pyproject.toml` |
|---------|-------------------|-----------------|
| Standard | Informal | PEP 517/518 official |
| Metadata | None | Full project metadata |
| Dev deps | Separate file | `[project.optional-dependencies]` |
| Build system | Not specified | Specified |
| Tool config | Separate files | Unified |

```toml
# pyproject.toml — modern, unified configuration
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "fractal-analytics"
version = "1.0.0"
description = "Analytics platform"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24",
    "pandas>=2.0",
    "scikit-learn>=1.3",
    "fastapi>=0.100",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "mypy",
    "black",
    "ruff",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=html"

[tool.mypy]
strict = true
python_version = "3.10"

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
```

```bash
# requirements.txt — simple, widely supported
numpy>=1.24
pandas>=2.0
scikit-learn>=1.3

# Install
pip install -r requirements.txt

# Generate from current env
pip freeze > requirements.txt
```

---

### [← Back to Index](./00_INDEX.md) | [Next: React Fundamentals →](./07_React_Fundamentals.md)
