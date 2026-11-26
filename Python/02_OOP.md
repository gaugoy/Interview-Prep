# Object-Oriented Programming
### [← Python index](./README.md) · [Question Bank](./Question_Bank.md)

Classes, inheritance, MRO, polymorphism, abstraction, SOLID, design patterns, dataclasses, dunder methods, descriptors, metaclasses.

**Topics:** [Fundamentals](./01_Fundamentals.md) · [OOP](./02_OOP.md) · [Functional](./03_Functional_and_Decorators.md) · [Concurrency](./04_Concurrency.md) · [Memory](./05_Memory_Management.md) · [DSA](./06_DSA.md) · [Data & AI](./07_Data_and_AI.md) · [Testing](./08_Testing_and_Tooling.md)

## Table of Contents

**Part A — Classes & objects**
1. (Easy) [What are the 4 pillars of OOP?](#q1)
2. (Easy) [What is the difference between a class and an object?](#q2)
3. (Easy) [What is a constructor? What is `__init__`?](#q3)
4. (Easy) [What is `self` in Python?](#q4)
5. (Easy) [What is the difference between class attributes and instance attributes?](#q5)
6. (Medium) [What is the difference between `@staticmethod` and `@classmethod`?](#q6)
7. (Medium) [What is the difference between `__str__` and `__repr__`?](#q7)
8. (Easy) [What is the difference between public, protected, and private attributes?](#q8)

**Part B — Inheritance & polymorphism**
9. (Easy) [What is inheritance? Single vs multiple?](#q9)
10. (Easy) [What is method overriding?](#q10)
11. (Medium) [What is polymorphism? What is duck typing?](#q11)
12. (Medium) [What is MRO (Method Resolution Order)?](#q12)
13. (Medium) [What is `super()`? Why is it important?](#q13)
14. (Hard) [What is the diamond problem? How does Python resolve it?](#q14)
15. (Hard) [What is a mixin? When would you use one?](#q15)
16. (Medium) [What is the difference between composition and inheritance?](#q16)

**Part C — Encapsulation, abstraction & design**
17. (Medium) [What is encapsulation? How does Python achieve it?](#q17)
18. (Medium) [What is abstraction? How do ABCs work?](#q18)
19. (Medium) [What is the difference between an ABC and a Protocol?](#q19)
20. (Medium) [What are SOLID principles?](#q20)
21. (Hard) [What is the Liskov Substitution Principle (LSP)?](#q21)
22. (Medium) [How do you implement dependency injection in Python?](#q22)
23. (Hard) [What design patterns have you used? Explain Singleton, Factory, Observer.](#q23)
24. (Medium) [Does Python support method overloading?](#q24)
25. (Easy) [What are Enums and why use them?](#q25)

**Part D — Data classes & special methods**
26. (Easy) [What are dataclasses and why use them?](#q26)
27. (Medium) [Dataclass vs NamedTuple vs Pydantic model — when to use which?](#q27)
28. (Medium) [How are `__eq__` and `__hash__` related? Why does my object become unhashable?](#q28)
29. (Medium) [What are Python's dunder (magic) methods? Name 5 commonly used ones.](#q29)
30. (Hard) [What is the Python data model? How does operator overloading work?](#q30)
31. (Hard) [What is the difference between `@property`, `@setter`, and `@deleter`?](#q31)
32. (Hard) [What is name mangling in Python?](#q32)
33. (Hard) [What is `__call__`? How can a class instance be made callable?](#q33)

**Part E — Internals: descriptors, attribute lookup, metaclasses**
34. (Hard) [What is a descriptor in Python?](#q34)
35. (Hard) [How does Python look up an attribute on an object?](#q35)
36. (Hard) [What is the difference between `__getattr__` and `__getattribute__`?](#q36)
37. (Hard) [What is the difference between `__new__` and `__init__`?](#q37)
38. (Hard) [What is a metaclass in Python?](#q38)
39. (Medium) [What is monkey patching? When is it acceptable?](#q39)

---

## Part A — Classes & objects

<a name="q1"></a>
## Q1. (Easy) What are the 4 pillars of OOP?
**Answer:** OOP organises code around **objects** that bundle state (attributes) and behaviour (methods). The four pillars describe how: **encapsulation** keeps data and the code that changes it together and hides internals; **inheritance** lets a class reuse and extend another; **polymorphism** lets different types be used through the same interface; **abstraction** exposes what an object does while hiding how. In Python these are applied mostly through conventions and protocols (duck typing, `_private` names, ABCs) rather than strict language rules.

| Pillar | Definition | Python Mechanism |
|--------|-----------|-----------------|
| **Encapsulation** | Bundle data + methods; restrict direct access | `_protected`, `__private`, `@property` |
| **Inheritance** | Reuse and extend behavior from parent class | `class Child(Parent)` |
| **Polymorphism** | Same interface, different behavior per type | Method overriding, duck typing |
| **Abstraction** | Hide complexity, expose only what's needed | `ABC`, `@abstractmethod` |

```python
from abc import ABC, abstractmethod

# 1. ENCAPSULATION
class BankAccount:
    def __init__(self, balance: float):
        self.__balance = balance          # Private

    @property
    def balance(self) -> float:
        return self.__balance             # Controlled access

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

# 2. INHERITANCE
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says Meow!"

# 3. POLYMORPHISM
animals = [Dog("Rex"), Cat("Whiskers"), Dog("Buddy")]
for animal in animals:
    print(animal.speak())   # Each calls its own speak()

# 4. ABSTRACTION
class DataProcessor(ABC):
    @abstractmethod
    def load(self, source: str): ...

    @abstractmethod
    def transform(self): ...

    @abstractmethod
    def save(self, destination: str): ...

    def run_pipeline(self, source: str, destination: str):
        """Template method — defines the algorithm skeleton"""
        self.load(source)
        self.transform()
        self.save(destination)
```

---

<a name="q2"></a>
## Q2. (Easy) What is the difference between a class and an object?
**Answer:** A **class** defines a new type: it describes what data its objects hold and what they can do. An **object** is one concrete instance created by calling the class; each instance has its own attribute namespace (`__dict__`) for its state, while methods and class attributes live once on the class and are shared by all instances. In Python a class is itself an object (of type `type`), created when the `class` statement runs.

- **Class** — a **blueprint/template** that defines attributes and methods
- **Object (instance)** — a **concrete realization** of a class with its own state

```python
# Class — defined once
class Car:
    wheels = 4          # Class variable — shared by all instances

    def __init__(self, brand: str, model: str):
        self.brand = brand   # Instance variable — unique per instance
        self.model = model

    def describe(self) -> str:
        return f"{self.brand} {self.model} ({self.wheels} wheels)"

# Objects — created from the class
car1 = Car("Toyota", "Camry")
car2 = Car("Honda", "Civic")

print(car1.describe())   # Toyota Camry (4 wheels)
print(car2.describe())   # Honda Civic (4 wheels)

# Each object has its own namespace
print(car1.__dict__)     # {'brand': 'Toyota', 'model': 'Camry'}
print(Car.__dict__)      # Contains 'wheels', 'describe', etc.

# id() shows they are different objects
print(id(car1) == id(car2))  # False
```

**Related:** [Memory · Q12](./05_Memory_Management.md#q12) — What are `__slots__` and how do they save memory?

---

<a name="q3"></a>
## Q3. (Easy) What is a constructor? What is `__init__`?
**Answer:** When you call `Person(...)`, Python first calls `__new__` to **create** the object and then `__init__` to set its initial state. So `__init__` is technically an **initializer**: it receives the new instance as `self`, assigns instance attributes, validates input and returns `None`. Python has one `__init__` per class (no constructor overloading) — use default arguments or `@classmethod` alternative constructors instead. `__del__` is a finalizer whose timing isn't guaranteed, so don't rely on it for cleanup.

`__init__` is Python's **initializer** (not technically a constructor — `__new__` creates the object, `__init__` initializes it). It runs automatically when an instance is created.

```python
class Person:
    count = 0  # Class variable

    def __init__(self, name: str, age: int):
        # Instance initialization
        self.name = name
        self.age = age
        Person.count += 1   # Track total instances

    def __del__(self):
        # Finalizer — runs when the object is freed. ⚠️ Timing is not guaranteed
        # (cycles, other Python implementations), so don't rely on it in real code.
        Person.count -= 1

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"

p1 = Person("Alice", 30)
p2 = Person("Bob", 25)
print(Person.count)   # 2

del p1
print(Person.count)   # 1
```

**Related:** [OOP · Q37](#q37) — What is the difference between `__new__` and `__init__`?

---

<a name="q4"></a>
## Q4. (Easy) What is `self` in Python?
**Answer:** Python methods are ordinary functions stored in the class. When you call `obj.method()`, Python turns it into `Class.method(obj)` — the instance is passed **explicitly** as the first parameter, which by convention is named `self`. Through `self` a method reads and changes that particular object's state. `self` isn't a keyword (unlike `this` in Java/C++), which follows Python's rule "explicit is better than implicit".

`self` is a **reference to the current instance** of the class. It's the first parameter of every instance method and is passed automatically by Python when you call a method on an object.

```python
class Counter:
    def __init__(self):
        self.count = 0    # self refers to this specific instance

    def increment(self):
        self.count += 1   # Modifies this instance's count

    def reset(self):
        self.count = 0

c1 = Counter()
c2 = Counter()

c1.increment()
c1.increment()
c2.increment()

print(c1.count)  # 2 — c1's own count
print(c2.count)  # 1 — c2's own count

# self is just a convention — you could name it anything (but don't!)
class Weird:
    def method(this):   # 'this' works but is non-standard
        return this

# Under the hood: c1.increment() == Counter.increment(c1)
```

---

<a name="q5"></a>
## Q5. (Easy) What is the difference between class attributes and instance attributes?
**Answer:** A **class attribute** is defined on the class and shared by all instances; an **instance attribute** is set on `self` and belongs to one object. Reading `obj.x` checks the instance first, then the class. **Gotcha:** a *mutable* class attribute (list/dict) is shared — appending through one instance changes it for all.

```python
class Cart:
    tax_rate = 0.18          # class attribute — shared, fine (immutable)
    items = []               # ✘ shared list — bug

    def __init__(self):
        self.lines = []      # ✔ instance attribute — one per cart

a, b = Cart(), Cart()
a.items.append("pen")
print(b.items)               # ['pen']  ← b sees a's item
```

---

<a name="q6"></a>
## Q6. (Medium) What is the difference between `@staticmethod` and `@classmethod`?
**Answer:** Methods are functions stored on the class; the decorator decides what Python passes as the first argument. A normal **instance method** gets the instance (`self`) — use it when you need the object's state. A **`@classmethod`** gets the class (`cls`) — use it for alternative constructors (`from_json`, `from_fahrenheit`) and class-level logic; it works correctly for subclasses because `cls` is the subclass. A **`@staticmethod`** gets nothing — it's a plain function kept in the class because it logically belongs there.

- **Instance method** — receives `self` (the instance)
- `@classmethod` — receives `cls` (the class); used for factory methods, alternative constructors
- `@staticmethod` — receives neither; utility function logically grouped with the class

```python
class Temperature:
    unit = "Celsius"

    def __init__(self, value):
        self.value = value

    # Instance method — accesses instance data
    def to_fahrenheit(self):
        return self.value * 9/5 + 32

    # Class method — accesses class data, used as factory
    @classmethod
    def from_fahrenheit(cls, f_value):
        return cls((f_value - 32) * 5/9)

    @classmethod
    def set_unit(cls, unit):
        cls.unit = unit

    # Static method — no access to instance or class
    @staticmethod
    def is_valid(value):
        return -273.15 <= value  # absolute zero check

t1 = Temperature(100)
t2 = Temperature.from_fahrenheit(212)  # factory
print(Temperature.is_valid(-300))      # False
```

**Related:** [Functional · Q21](./03_Functional_and_Decorators.md#q21) — Which built-in / standard-library decorators should you know?

---

<a name="q7"></a>
## Q7. (Medium) What is the difference between `__str__` and `__repr__`?
**Answer:** Both return a string version of the object, for different audiences. `__repr__` is for **developers**: unambiguous, ideally looks like code that recreates the object (`Point(3, 4)`); it's used by the REPL, debuggers, `repr()` and when the object is inside a container. `__str__` is for **end users**: readable, used by `print()` and `str()`. If `__str__` isn't defined, Python falls back to `__repr__` — so always define `__repr__` first.

- `__str__` — **human-readable** string, used by `print()` and `str()`
- `__repr__` — **unambiguous** developer representation, used in REPL and `repr()`; should ideally be valid Python to recreate the object

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"  # Unambiguous

    def __str__(self):
        return f"({self.x}, {self.y})"            # Human-friendly

p = Point(3, 4)
print(str(p))    # (3, 4)       ← __str__
print(repr(p))   # Point(3, 4)  ← __repr__
print(p)         # (3, 4)       ← print() uses __str__

# In a list, __repr__ is used
print([p])       # [Point(3, 4)]

# Rule: always define __repr__; __str__ is optional
```

---

<a name="q8"></a>
## Q8. (Easy) What is the difference between public, protected, and private attributes?
**Answer:** Python has no `public` / `protected` / `private` keywords — everything is technically accessible, and developers follow naming conventions: no underscore = public API; `_name` = internal (tools and `from module import *` treat it as private); `__name` = name-mangled to `_ClassName__name` to avoid clashes in subclasses. The philosophy is "we are all consenting adults"; when you need controlled access, use `@property`.

Python uses **naming conventions** (not true access modifiers):

| Convention | Syntax | Meaning |
|-----------|--------|---------|
| Public | `self.name` | Accessible everywhere |
| Protected | `self._name` | Convention: "internal use", accessible but discouraged |
| Private | `self.__name` | Name mangling: `_ClassName__name`, harder to access |

```python
class Employee:
    def __init__(self, name, salary, ssn):
        self.name = name          # Public
        self._department = "IT"   # Protected — convention only
        self.__ssn = ssn          # Private — name mangled

    def get_ssn_last4(self):
        return self.__ssn[-4:]    # Access within class

emp = Employee("Alice", 90000, "123-45-6789")
print(emp.name)           # Alice — OK
print(emp._department)    # IT — works but discouraged
# print(emp.__ssn)        # AttributeError
print(emp._Employee__ssn) # 123-45-6789 — still accessible via mangled name
print(emp.get_ssn_last4()) # 6789 — proper way
```

---

## Part B — Inheritance & polymorphism

<a name="q9"></a>
## Q9. (Easy) What is inheritance? Single vs multiple?
**Answer:** Inheritance lets a **child class reuse and extend a parent class**: the child gets the parent's attributes and methods, can add new ones and override existing ones, and counts as an instance of the parent ("is-a"). **Single inheritance** = one parent. **Multiple inheritance** = several parents; Python supports it and decides which method wins using the MRO (C3 linearization). Multiple inheritance works best with small mixin classes; deep hierarchies make code fragile — prefer composition when it isn't a true "is-a".

Inheritance allows a class to **reuse and extend** the behavior of another class.

```python
# Single inheritance
class Vehicle:
    def __init__(self, speed: int):
        self.speed = speed

    def move(self) -> str:
        return f"Moving at {self.speed} km/h"

class Car(Vehicle):
    def __init__(self, speed: int, brand: str):
        super().__init__(speed)   # Call parent constructor
        self.brand = brand

    def honk(self) -> str:
        return "Beep!"

car = Car(120, "Toyota")
print(car.move())   # Moving at 120 km/h (inherited)
print(car.honk())   # Beep! (own method)

# Multiple inheritance
class Flyable:
    def fly(self) -> str:
        return "Flying!"

class Swimmable:
    def swim(self) -> str:
        return "Swimming!"

class Duck(Flyable, Swimmable):
    def quack(self) -> str:
        return "Quack!"

duck = Duck()
print(duck.fly())    # Flying!
print(duck.swim())   # Swimming!
print(duck.quack())  # Quack!
```

---

<a name="q10"></a>
## Q10. (Easy) What is method overriding?
**Answer:** Overriding means a subclass defines a method with the **same name** as one in its parent, so calls on subclass instances use the subclass version (it's found first in the MRO). This is how polymorphism works: code calls `shape.area()` without knowing the concrete type. The override can still reuse the parent's logic with `super().method()`. Keep the same signature and contract so the subclass stays substitutable (LSP). Python has no `override` keyword; `@typing.override` (3.12+) only helps type checkers.

Method overriding allows a **subclass to provide its own implementation** of a method defined in the parent class.

```python
class Shape:
    def area(self) -> float:
        raise NotImplementedError("Subclasses must implement area()")

    def describe(self) -> str:
        return f"I am a {self.__class__.__name__} with area {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:          # Override
        import math
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:          # Override
        return self.width * self.height

shapes = [Circle(5), Rectangle(4, 6)]
for shape in shapes:
    print(shape.describe())
# I am a Circle with area 78.54
# I am a Rectangle with area 24.00
```

---

<a name="q11"></a>
## Q11. (Medium) What is polymorphism? What is duck typing?
**Answer:** **Polymorphism** means the same operation works on different types, each doing the right thing for itself — `len()` on a list or a string, `animal.speak()` on a Dog or a Cat. In statically typed languages this usually needs a common base class or interface. Python uses **duck typing**: it doesn't check the type, only whether the object has the needed method at runtime ("if it walks like a duck and quacks like a duck…"). This keeps code flexible (file-like objects, iterables); `typing.Protocol` lets type checkers verify such interfaces.

- **Polymorphism** — objects of different types respond to the same interface
- **Duck typing** — "If it walks like a duck and quacks like a duck, it's a duck" — Python checks behavior, not type

```python
# Polymorphism via inheritance
class Dog:
    def speak(self): return "Woof!"

class Cat:
    def speak(self): return "Meow!"

class Robot:
    def speak(self): return "Beep boop!"

# Duck typing — no common base class needed!
def make_noise(thing):
    print(thing.speak())   # Works for any object with speak()

for creature in [Dog(), Cat(), Robot()]:
    make_noise(creature)

# Real-world duck typing: file-like objects
import io

def process_data(file_obj):
    """Works with any object that has .read()"""
    return file_obj.read()

# All of these work:
process_data(open("data.txt"))
process_data(io.StringIO("in-memory data"))
process_data(io.BytesIO(b"binary data"))

# isinstance() vs duck typing
# ❌ Rigid: isinstance(obj, list)
# ✅ Flexible: hasattr(obj, '__iter__')
```

---

<a name="q12"></a>
## Q12. (Medium) What is MRO (Method Resolution Order)?
**Answer:** The **Method Resolution Order** is the ordered list of classes Python searches when it looks up a method or attribute on an object; see it with `Class.__mro__` or `Class.mro()`. Python computes it with the **C3 linearization** algorithm, which guarantees that a class comes before its parents, the order of parents in the class definition is kept, and every class appears exactly once. `super()` follows this order, which is what makes cooperative multiple inheritance work.

MRO defines the **order in which Python searches for methods** in a class hierarchy. Python uses the **C3 linearization algorithm**.

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()

d = D()
d.method()
# D → B → C → A
# super() follows MRO, not just "parent"

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# C3 linearization rule:
# D's MRO = D + merge(MRO(B), MRO(C), [B, C])
# = D + merge([B,A,object], [C,A,object], [B,C])
# = D, B, C, A, object

# Practical implication: super() in B calls C.method(), not A.method()
# This is cooperative multiple inheritance
```

**Related:** [OOP · Q13](#q13) — What is `super()`? Why is it important? · [OOP · Q14](#q14) — What is the diamond problem? How does Python resolve it? · [OOP · Q15](#q15) — What is a mixin? When would you use one?

---

<a name="q13"></a>
## Q13. (Medium) What is `super()`? Why is it important?
**Answer:** `super()` returns a proxy that looks up methods in the **next class after the current one in the instance's MRO** — not simply "the parent". It's used to extend rather than replace inherited behaviour (`super().__init__(...)`). In multiple inheritance, if every class calls `super()`, each method in the chain runs exactly once in MRO order (cooperative inheritance); if one class skips it, the chain stops there. In Python 3, `super()` needs no arguments inside a method.

`super()` returns a proxy object that delegates method calls to the **next class in MRO**, enabling cooperative multiple inheritance.

```python
class LogMixin:
    def save(self):
        print(f"[LOG] Saving {self.__class__.__name__}")
        super().save()   # Delegates to next in MRO

class ValidationMixin:
    def save(self):
        print(f"[VALIDATE] Validating {self.__class__.__name__}")
        super().save()   # Delegates to next in MRO

class Model:
    def save(self):
        print(f"[DB] Saving to database")

class UserModel(LogMixin, ValidationMixin, Model):
    pass

user = UserModel()
user.save()
# [LOG] Saving UserModel
# [VALIDATE] Validating UserModel
# [DB] Saving to database

# MRO: UserModel → LogMixin → ValidationMixin → Model → object
# Each super() call goes to the NEXT class in MRO

# Without super() — breaks the chain
class BrokenMixin:
    def save(self):
        print("BrokenMixin.save")
        # No super() — ValidationMixin.save and Model.save never called!
```

**Related:** [OOP · Q12](#q12) — What is MRO (Method Resolution Order)?

---

<a name="q14"></a>
## Q14. (Hard) What is the diamond problem? How does Python resolve it?
**Answer:** The diamond problem appears when class D inherits from B and C, which both inherit from A: if B and C both override a method, which one does D use, and does A's version run twice? Python solves it with the **C3 MRO** — one consistent order (D → B → C → A → object) where A appears only once — plus `super()`, which walks along that order. As long as each class calls `super()` cooperatively, A's method runs exactly once.

The diamond problem occurs in multiple inheritance when a class inherits from two classes that both inherit from the same base class, creating ambiguity about which version of a method to use.

```
    A
   / \
  B   C
   \ /
    D
```

```python
class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        print("Hello from B")
        super().greet()

class C(A):
    def greet(self):
        print("Hello from C")
        super().greet()

class D(B, C):
    def greet(self):
        print("Hello from D")
        super().greet()

d = D()
d.greet()
# Hello from D
# Hello from B
# Hello from C
# Hello from A

# Python's C3 linearization ensures A.greet() is called ONCE
# MRO: D → B → C → A → object
# Without super(): A.greet() would be called twice (once from B, once from C)

# Key insight: super() doesn't mean "call parent"
# It means "call the next class in MRO"
# This enables cooperative multiple inheritance
```

**Related:** [OOP · Q12](#q12) — What is MRO (Method Resolution Order)?

---

<a name="q15"></a>
## Q15. (Hard) What is a mixin? When would you use one?
**Answer:** A **mixin** is a small class that adds one focused capability (JSON serialization, timestamps, logging, permission checks) to other classes through multiple inheritance. It isn't meant to be used on its own, usually has no state of its own (or cooperates through `super()`), and is listed **before** the main base class. Django's class-based views use this heavily (`LoginRequiredMixin`). Keep mixins small and independent to avoid MRO surprises.

A mixin is a class that provides **reusable methods** to be mixed into other classes via multiple inheritance. It's not meant to be instantiated on its own.

```python
# Mixins — reusable behavior modules
class JSONMixin:
    """Add JSON serialization to any class"""
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str: str):
        import json
        data = json.loads(json_str)
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj

class TimestampMixin:
    """Add created_at/updated_at to any model"""
    def __init__(self, *args, **kwargs):
        from datetime import datetime
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def touch(self):
        from datetime import datetime
        self.updated_at = datetime.now().isoformat()

class ValidationMixin:
    """Add validation to any model"""
    def validate(self) -> bool:
        for field, validator in getattr(self, '_validators', {}).items():
            if not validator(getattr(self, field, None)):
                raise ValueError(f"Validation failed for {field}")
        return True

# Compose mixins into a model
class User(JSONMixin, TimestampMixin, ValidationMixin):
    _validators = {
        'email': lambda x: x and '@' in x,
        'age': lambda x: x and 0 < x < 150,
    }

    def __init__(self, name: str, email: str, age: int):
        super().__init__()   # Calls TimestampMixin.__init__
        self.name = name
        self.email = email
        self.age = age

user = User("Alice", "alice@example.com", 30)
print(user.to_json())
user.validate()
user.touch()
```

**Related:** [OOP · Q12](#q12) — What is MRO (Method Resolution Order)?

---

<a name="q16"></a>
## Q16. (Medium) What is the difference between composition and inheritance?
**Answer:** Inheritance models an **is-a** relationship and reuses code by extending a parent; composition models a **has-a** relationship by holding other objects as attributes and delegating work to them. Inheritance couples the child tightly to the parent's internals (a change in the parent can break every child); composition keeps the parts independent, easy to replace (even at runtime) and easy to test. Rule of thumb: inherit for true subtypes and small mixins, compose for everything else ("favour composition over inheritance").

- **Inheritance** — "IS-A" relationship: `Dog IS-A Animal`
- **Composition** — "HAS-A" relationship: `Car HAS-A Engine`

> **Prefer composition over inheritance** — it's more flexible and avoids tight coupling.

```python
# ❌ Inheritance — tight coupling, fragile base class problem
class Animal:
    def breathe(self): return "breathing"
    def eat(self): return "eating"

class FlyingAnimal(Animal):
    def fly(self): return "flying"

class SwimmingAnimal(Animal):
    def swim(self): return "swimming"

# What about a duck that can both fly AND swim?
# Multiple inheritance gets messy...

# ✅ Composition — flexible, mix and match behaviors
class FlyBehavior:
    def fly(self): return "flying with wings"

class SwimBehavior:
    def swim(self): return "swimming with webbed feet"

class QuackBehavior:
    def quack(self): return "Quack!"

class Duck:
    def __init__(self):
        self.fly_behavior = FlyBehavior()
        self.swim_behavior = SwimBehavior()
        self.quack_behavior = QuackBehavior()

    def perform_fly(self): return self.fly_behavior.fly()
    def perform_swim(self): return self.swim_behavior.swim()
    def perform_quack(self): return self.quack_behavior.quack()

# Can swap behaviors at runtime!
class RocketFly:
    def fly(self): return "flying with rocket"

duck = Duck()
duck.fly_behavior = RocketFly()  # Change behavior without changing Duck class
print(duck.perform_fly())  # flying with rocket
```

---

## Part C — Encapsulation, abstraction & design

<a name="q17"></a>
## Q17. (Medium) What is encapsulation? How does Python achieve it?
**Answer:** Encapsulation means keeping an object's data together with the methods that operate on it, and **hiding the internal details** so the object itself controls how its state changes (e.g. a balance can never become negative). Benefits: invariants are protected and internals can change without breaking callers. Python achieves it through conventions (`_internal` attributes), name mangling and `@property` for validated access — not through enforced access modifiers.

Encapsulation bundles data and methods together and **controls access** to internal state. Python achieves it through naming conventions and `@property`.

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius   # Protected storage

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError(f"Temperature below absolute zero: {value}")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.celsius = (value - 32) * 5/9  # Validates via celsius setter

t = Temperature(25)
print(t.celsius)      # 25
print(t.fahrenheit)   # 77.0

t.fahrenheit = 32     # Sets celsius to 0
print(t.celsius)      # 0.0

# t.celsius = -300    # ValueError: Temperature below absolute zero
```

---

<a name="q18"></a>
## Q18. (Medium) What is abstraction? How do ABCs work?
**Answer:** Abstraction means exposing **what** an object does (its interface) while hiding **how** it does it. In Python an **Abstract Base Class** (`abc.ABC`) defines that interface: methods marked `@abstractmethod` must be implemented by subclasses, and Python refuses to instantiate any class that still has abstract methods (`TypeError`). An ABC can also contain shared concrete methods (the template-method pattern). Code then depends on the abstraction (`DataSource`), so implementations (PostgreSQL, BigQuery) can be swapped.

Abstraction hides implementation details and exposes only the **essential interface**. Python uses `ABC` (Abstract Base Class) to enforce that subclasses implement required methods.

```python
from abc import ABC, abstractmethod
from typing import List

class DataSource(ABC):
    """Abstract interface for all data sources"""

    @abstractmethod
    def connect(self) -> bool: ...

    @abstractmethod
    def fetch(self, query: str) -> List[dict]: ...

    @abstractmethod
    def close(self) -> None: ...

    # Concrete method — shared implementation
    def fetch_all(self, queries: List[str]) -> List[dict]:
        results = []
        for q in queries:
            results.extend(self.fetch(q))
        return results

# Concrete implementations
class PostgreSQLSource(DataSource):
    def connect(self) -> bool:
        print("Connecting to PostgreSQL...")
        return True

    def fetch(self, query: str) -> List[dict]:
        return [{"result": f"pg:{query}"}]

    def close(self) -> None:
        print("Closing PostgreSQL connection")

class BigQuerySource(DataSource):
    def connect(self) -> bool:
        print("Connecting to BigQuery...")
        return True

    def fetch(self, query: str) -> List[dict]:
        return [{"result": f"bq:{query}"}]

    def close(self) -> None:
        print("Closing BigQuery connection")

# Can't instantiate abstract class
# DataSource()  # TypeError: Can't instantiate abstract class

# Works with any concrete implementation
def run_pipeline(source: DataSource, queries: List[str]):
    source.connect()
    results = source.fetch_all(queries)
    source.close()
    return results
```

**Related:** [OOP · Q19](#q19) — What is the difference between an ABC and a Protocol?

---

<a name="q19"></a>
## Q19. (Medium) What is the difference between an ABC and a Protocol?
**Answer:** An **ABC** (`abc.ABC`, see [OOP · Q18](#q18)) is *nominal*: a class must **inherit** from it and implement the abstract methods. A **`typing.Protocol`** is *structural* ("static duck typing"): any class with matching methods satisfies it — no inheritance needed. Protocols are checked by type checkers (mypy), and at runtime only with `@runtime_checkable` + `isinstance`.

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, msg: str) -> None: ...

class EmailNotifier:                 # doesn't inherit anything
    def send(self, msg: str) -> None:
        print("email:", msg)

def alert(n: Notifier):              # mypy accepts EmailNotifier
    n.send("Disk full")
```
Use ABCs when you want to share base code and enforce implementation; Protocols for loose interfaces, especially with third-party classes.

**Related:** [OOP · Q18](#q18) — What is abstraction? How do ABCs work? · [Testing · Q7](./08_Testing_and_Tooling.md#q7) — What is type hinting in Python? What are its benefits?

---

<a name="q20"></a>
## Q20. (Medium) What are SOLID principles?
**Answer:**

| Principle | Full Name | Meaning |
|-----------|-----------|---------|
| **S** | Single Responsibility | A class should have only one reason to change |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | Subclasses must be substitutable for their base class |
| **I** | Interface Segregation | Many specific interfaces > one general interface |
| **D** | Dependency Inversion | Depend on abstractions, not concretions |

```python
from abc import ABC, abstractmethod

# S — Single Responsibility
class UserRepository:
    def save(self, user): pass      # Only handles DB operations

class EmailService:
    def send_welcome(self, user): pass  # Only handles emails

# O — Open/Closed
class Discount(ABC):
    @abstractmethod
    def apply(self, price: float) -> float: ...

class PercentDiscount(Discount):
    def __init__(self, percent): self.percent = percent
    def apply(self, price): return price * (1 - self.percent / 100)

class FlatDiscount(Discount):
    def __init__(self, amount): self.amount = amount
    def apply(self, price): return price - self.amount

# Add new discount types without modifying existing code ✅

# L — Liskov Substitution
class Bird:
    def move(self): return "moving"

class FlyingBird(Bird):
    def move(self): return "flying"   # Substitutable for Bird ✅

# ❌ Violation: Penguin can't fly but inherits from FlyingBird
# class Penguin(FlyingBird):
#     def move(self): raise NotImplementedError  # Breaks LSP!

# D — Dependency Inversion
class DataProcessor:
    def __init__(self, storage: 'Storage'):  # Depends on abstraction
        self.storage = storage

class Storage(ABC):
    @abstractmethod
    def save(self, data): ...

class S3Storage(Storage):
    def save(self, data): print(f"Saving to S3: {data}")

class LocalStorage(Storage):
    def save(self, data): print(f"Saving locally: {data}")

# Can swap storage without changing DataProcessor
processor = DataProcessor(S3Storage())
processor2 = DataProcessor(LocalStorage())
```

**Related:** [OOP · Q21](#q21) — What is the Liskov Substitution Principle (LSP)? · [OOP · Q22](#q22) — How do you implement dependency injection in Python?

---

<a name="q21"></a>
## Q21. (Hard) What is the Liskov Substitution Principle (LSP)?
**Answer:** The **Liskov Substitution Principle** (the L in SOLID) says: if S is a subclass of T, you must be able to use an S anywhere a T is expected without breaking the program. A subclass has to keep the parent's contract: accept the same inputs, not add stricter preconditions, not weaken guarantees, and not raise new unexpected errors. A violation usually means the "is-a" relationship is wrong (a Square with independent width/height setters, a Penguin that is a FlyingBird); fix it by changing the hierarchy or using composition.

LSP states that objects of a subclass must be **substitutable for objects of the superclass** without breaking the program.

```python
# ❌ LSP Violation — classic example
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def set_width(self, value):
        self.width = value

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def set_width(self, value):      # Square must keep sides equal...
        self.width = value
        self.height = value          # ...so it silently changes height too

# Code written for Rectangle:
def stretch(rect: Rectangle):
    old_height = rect.height
    rect.set_width(rect.width * 2)
    assert rect.height == old_height   # ✅ Rectangle — ❌ fails for Square: LSP broken

# ✅ LSP Fix — don't inherit Square from Rectangle
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self): return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self): return self.side ** 2
```

**Related:** [OOP · Q20](#q20) — What are SOLID principles?

---

<a name="q22"></a>
## Q22. (Medium) How do you implement dependency injection in Python?
**Answer:** Pass dependencies in (usually through `__init__`) instead of creating them inside the class. It makes code testable (inject a fake) and swappable (different DB/notifier per environment). Python rarely needs a DI framework — constructor injection with Protocols/ABCs is enough (FastAPI's `Depends` is a built-in DI system).

```python
class OrderService:
    def __init__(self, repo, notifier):        # injected, not created here
        self.repo, self.notifier = repo, notifier

    def place(self, order):
        self.repo.save(order)
        self.notifier.send(f"Order {order.id} placed")

service = OrderService(SqlOrderRepo(), EmailNotifier())          # production
test_service = OrderService(InMemoryRepo(), FakeNotifier())      # tests
```

**Related:** [OOP · Q20](#q20) — What are SOLID principles?

---

<a name="q23"></a>
## Q23. (Hard) What design patterns have you used? Explain Singleton, Factory, Observer.
**Answer:** Design patterns are reusable solutions to common design problems. **Singleton** — guarantee a single instance (in Python, a module-level object is usually the simplest singleton). **Factory** — a function or class decides which concrete class to create based on input, so callers depend only on the interface. **Observer** — a subject keeps a list of subscribers and notifies them when something happens (Django signals, event emitters, pub/sub). In interviews, explain the problem each pattern solves and where you used it.


```python
# 1. SINGLETON — ensure only one instance exists
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connected = False
        return cls._instance

    def connect(self, url: str):
        if not self._connected:
            print(f"Connecting to {url}")
            self._connected = True

db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True — same instance

# 2. FACTORY — create objects without specifying exact class
class Notification(ABC):
    @abstractmethod
    def send(self, message: str): ...

class EmailNotification(Notification):
    def send(self, message): print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message): print(f"SMS: {message}")

class SlackNotification(Notification):
    def send(self, message): print(f"Slack: {message}")

def notification_factory(channel: str) -> Notification:
    channels = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "slack": SlackNotification,
    }
    if channel not in channels:
        raise ValueError(f"Unknown channel: {channel}")
    return channels[channel]()

notif = notification_factory("email")
notif.send("Hello!")

# 3. OBSERVER — notify multiple objects when state changes
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event: str, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

emitter = EventEmitter()
emitter.on("data", lambda x: print(f"Handler 1: {x}"))
emitter.on("data", lambda x: print(f"Handler 2: {x}"))
emitter.emit("data", {"value": 42})
# Handler 1: {'value': 42}
# Handler 2: {'value': 42}
```

**Related:** [OOP · Q37](#q37) — What is the difference between `__new__` and `__init__`?

---

<a name="q24"></a>
## Q24. (Medium) Does Python support method overloading?
**Answer:** Not like Java — defining a method twice just replaces the first. Alternatives: default/keyword arguments, `*args`, checking types, or **`functools.singledispatch`** (choose the implementation by the type of the first argument; `singledispatchmethod` for methods). `typing.overload` only adds type hints, not runtime behaviour.

```python
from functools import singledispatch

@singledispatch
def to_json(value):
    raise TypeError(f"Unsupported: {type(value)}")

@to_json.register
def _(value: int):
    return str(value)

@to_json.register
def _(value: list):
    return "[" + ",".join(to_json(v) for v in value) + "]"

to_json([1, 2])     # '[1,2]'
```

---

<a name="q25"></a>
## Q25. (Easy) What are Enums and why use them?
**Answer:** `enum.Enum` defines a fixed set of named constants. Safer than raw strings/ints: typos fail loudly, values are grouped, you can iterate them, and comparisons are clear. `StrEnum`/`IntEnum` also behave like str/int (handy for JSON/DB).

```python
from enum import Enum, StrEnum

class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"

order_status = Status.PAID
order_status == "paid"            # True (StrEnum)
[s.value for s in Status]         # ['pending', 'paid']
```

---

## Part D — Data classes & special methods

<a name="q26"></a>
## Q26. (Easy) What are dataclasses and why use them?
**Answer:** `@dataclass` auto-generates `__init__`, `__repr__` and `__eq__` (and optionally ordering, hashing, `__slots__`) from type-annotated fields — less boilerplate for classes that mainly hold data. Use `field(default_factory=list)` for mutable defaults and `__post_init__` for extra validation. Options: `frozen=True` (immutable), `order=True`, `slots=True`.

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    id: int
    customer: str
    items: list[str] = field(default_factory=list)   # not items=[] (shared!)

    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("id must be positive")

Order(1, "Ann")   # Order(id=1, customer='Ann', items=[])
```

**Related:** [Memory · Q12](./05_Memory_Management.md#q12) — What are `__slots__` and how do they save memory?

---

<a name="q27"></a>
## Q27. (Medium) Dataclass vs NamedTuple vs Pydantic model — when to use which?
**Answer:**
| | `dataclass` | `NamedTuple` | Pydantic `BaseModel` |
|---|---|---|---|
| Mutable | Yes (unless `frozen`) | No | Yes (configurable) |
| Validation / type conversion | No (hints only) | No | **Yes** — validates and converts input |
| Speed / overhead | Light | Lightest, tuple-like | Heavier |
| Typical use | Internal data objects | Small immutable records | API input/output, config, parsing external data |

Rule: data from outside (requests, files, env) → Pydantic; internal objects → dataclass; tiny immutable records → NamedTuple.

---

<a name="q28"></a>
## Q28. (Medium) How are `__eq__` and `__hash__` related? Why does my object become unhashable?
**Answer:** Objects used as dict keys or in sets need `__hash__`, and **equal objects must have equal hashes**. If you define `__eq__` without `__hash__`, Python sets `__hash__ = None` → the object is unhashable (`TypeError: unhashable type`), to avoid broken dicts/sets. Define `__hash__` from the same **immutable** fields used in `__eq__`.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))

{Point(1, 2), Point(1, 2)}    # one element
```
(`@dataclass(frozen=True)` generates both correctly.)

**Related:** [Fundamentals · Q2](./01_Fundamentals.md#q2) — What are Python's mutable and immutable data types? · [DSA · Q5](./06_DSA.md#q5) — What is a hash table? How does Python's `dict` implement it?

---

<a name="q29"></a>
## Q29. (Medium) What are Python's dunder (magic) methods? Name 5 commonly used ones.
**Answer:**
Dunder methods (double underscore) allow classes to implement Python's built-in behaviors.

| Method | Triggered by | Purpose |
|--------|-------------|---------|
| `__init__` | `MyClass()` | Constructor |
| `__str__` | `str(obj)`, `print(obj)` | Human-readable string |
| `__repr__` | `repr(obj)`, REPL | Developer string |
| `__len__` | `len(obj)` | Length |
| `__getitem__` | `obj[key]` | Indexing/slicing |
| `__setitem__` | `obj[key] = val` | Assignment |
| `__contains__` | `x in obj` | Membership test |
| `__iter__` | `for x in obj` | Iteration |
| `__eq__` | `obj1 == obj2` | Equality |
| `__lt__` | `obj1 < obj2` | Less than |
| `__add__` | `obj1 + obj2` | Addition |
| `__enter__`/`__exit__` | `with obj:` | Context manager |

```python
class DataSet:
    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return f"DataSet({self._data!r})"

ds = DataSet([1, 2, 3, 4, 5])
print(len(ds))      # 5
print(ds[2])        # 3
print(3 in ds)      # True
for x in ds: print(x)
```

---

<a name="q30"></a>
## Q30. (Hard) What is the Python data model? How does operator overloading work?
**Answer:** The **data model** is the set of special (dunder) methods through which Python's syntax and built-ins talk to objects: `a + b` calls `a.__add__(b)`, `len(x)` calls `x.__len__()`, `x[i]` calls `__getitem__`, comparisons call `__eq__` / `__lt__`. **Operator overloading** means implementing these in your class so it behaves like a built-in type. If `a.__add__(b)` returns `NotImplemented`, Python tries the reflected `b.__radd__(a)`. `@functools.total_ordering` fills in the remaining comparison methods from `__eq__` plus one of `__lt__` / `__le__` / `__gt__` / `__ge__`.

The Python data model defines how objects interact with the language's built-in operations through dunder methods.

```python
from functools import total_ordering

@total_ordering  # Auto-generates missing comparison methods
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):  # scalar * vector
        return self.__mul__(scalar)

    def __abs__(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)    # Vector(4, 6)
print(v1 * 3)     # Vector(3, 6)
print(3 * v1)     # Vector(3, 6)
print(abs(v2))    # 5.0
print(v1 < v2)    # True
```

---

<a name="q31"></a>
## Q31. (Hard) What is the difference between `@property`, `@setter`, and `@deleter`?
**Answer:** `@property` turns a method into a **managed attribute**: callers use plain attribute syntax (`c.radius`) while your code runs on get/set/delete. That lets you start with a public attribute and later add validation or computation **without changing the API** — which is why Python doesn't need Java-style getters and setters. `@x.setter` and `@x.deleter` add write and delete behaviour; a property without a setter is read-only. Under the hood, `property` is a data descriptor.

`@property` creates a **managed attribute** — you can add validation, computation, or side effects to attribute access.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius  # Private storage

    @property
    def radius(self):
        """Getter — called on circle.radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter — called on circle.radius = 5"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @radius.deleter
    def radius(self):
        """Deleter — called on del circle.radius"""
        del self._radius

    @property
    def area(self):
        """Computed property — no setter needed"""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.radius)   # 5    — calls getter
c.radius = 10     # calls setter
print(c.area)     # 314.159...
# c.radius = -1   # ValueError
```

**Related:** [OOP · Q34](#q34) — What is a descriptor in Python? · [Functional · Q20](./03_Functional_and_Decorators.md#q20) — What is the difference between `@property`, `@functools.cached_property` and `@lru_cache` on a method?

---

<a name="q32"></a>
## Q32. (Hard) What is name mangling in Python?
**Answer:** Python has no truly private members — access control is by convention. A single underscore `_x` means "internal, don't use from outside". A double underscore `__x` (without trailing underscores) triggers **name mangling**: inside the class body the name is rewritten to `_ClassName__x`. The purpose is to avoid accidental name clashes with attributes in subclasses, **not** security — the mangled name is still reachable.

Name mangling transforms `__attr` (double underscore prefix) to `_ClassName__attr`, making it harder (but not impossible) to access from outside the class.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Stored as _BankAccount__balance

    def get_balance(self):
        return self.__balance

acc = BankAccount(1000)
# print(acc.__balance)          # AttributeError
print(acc._BankAccount__balance)  # 1000 — still accessible if you know the mangled name
print(acc.get_balance())          # 1000 — proper way

# Single underscore _ = convention for "internal use"
# Double underscore __ = name mangling (not truly private)
# Python has no true private attributes
```

---

<a name="q33"></a>
## Q33. (Hard) What is `__call__`? How can a class instance be made callable?
**Answer:** Calling `obj(args)` runs `type(obj).__call__(obj, args)`. Functions are callable because they implement `__call__`; defining it in your class makes instances behave like functions while keeping state in attributes. Useful for configurable function objects (a multiplier that remembers its factor), class-based decorators, strategy/callback objects and ML models (`model(x)`). `callable(obj)` tells you whether an object can be called.

`__call__` makes an instance **callable like a function** — `obj()` triggers `obj.__call__()`.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
print(callable(double))  # True

# Real-world use: stateful function objects, ML model inference
class TextClassifier:
    def __init__(self, model_path):
        self.model = self._load(model_path)

    def _load(self, path):
        return {}  # load model

    def __call__(self, text: str) -> str:
        # Preprocess → predict → postprocess
        return "positive"

classifier = TextClassifier("model.pkl")
result = classifier("This product is great!")  # Callable like a function
```

**Related:** [Functional · Q12](./03_Functional_and_Decorators.md#q12) — What is a Python decorator? What problem does it solve?

---

## Part E — Internals: descriptors, attribute lookup, metaclasses

<a name="q34"></a>
## Q34. (Hard) What is a descriptor in Python?
**Answer:** A descriptor is an object stored as a **class attribute** that controls what happens when that attribute is accessed on instances, by implementing `__get__` and optionally `__set__` / `__delete__`. If it defines `__set__` or `__delete__` it's a **data descriptor** and takes priority over the instance `__dict__`; otherwise it's a **non-data descriptor**. Descriptors power much of Python: `property`, methods (functions are non-data descriptors that bind `self`), `classmethod`, `staticmethod`, and Django model fields. `__set_name__` tells the descriptor which attribute name it was assigned to.

A descriptor is an object that defines `__get__`, `__set__`, or `__delete__` methods, controlling attribute access on another class.

```python
class Validator:
    """Descriptor that validates numeric values"""

    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name   # Called when class is created

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self   # Accessed on class, not instance
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be numeric")
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        obj.__dict__[self.name] = value

class Product:
    price = Validator(min_val=0)
    quantity = Validator(min_val=0, max_val=1000)

    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

p = Product(10.99, 50)
# p.price = -5    # ValueError: price must be >= 0
# p.quantity = "abc"  # TypeError: quantity must be numeric

# @property is a descriptor under the hood!
```

**Related:** [OOP · Q31](#q31) — What is the difference between `@property`, `@setter`, and `@deleter`? · [OOP · Q35](#q35) — How does Python look up an attribute on an object?

---

<a name="q35"></a>
## Q35. (Hard) How does Python look up an attribute on an object?
**Answer:** For `obj.name`, Python (in `object.__getattribute__`):
1. Looks for a **data descriptor** (e.g. `@property`) on the class and its MRO → uses it.
2. Else looks in the **instance `__dict__`**.
3. Else uses a non-data descriptor or plain class attribute (methods, class attributes) found along the **MRO**.
4. Else calls `__getattr__` if defined, otherwise raises `AttributeError`.
That's why a `@property` beats an instance attribute of the same name, and why methods bind `self` automatically. Related: [OOP · Q34](#q34), [OOP · Q36](#q36), [OOP · Q12](#q12).

**Related:** [OOP · Q34](#q34) — What is a descriptor in Python? · [OOP · Q36](#q36) — What is the difference between `__getattr__` and `__getattribute__`?

---

<a name="q36"></a>
## Q36. (Hard) What is the difference between `__getattr__` and `__getattribute__`?
**Answer:** When you read `obj.name`, Python **always** calls `type(obj).__getattribute__(obj, "name")`, which does the normal lookup (data descriptors, the instance `__dict__`, class attributes along the MRO). Only if that lookup raises `AttributeError` does Python call `__getattr__` as a **fallback**. So `__getattr__` is the safe hook for "missing" attributes (proxies, lazy loading, defaults); overriding `__getattribute__` intercepts every access, slows everything down, and must call `super().__getattribute__()` to avoid infinite recursion.

- `__getattribute__` — called on **every** attribute access (even existing ones)
- `__getattr__` — called only when the attribute is **not found** through normal means (fallback)

```python
class LazyLoader:
    """Load attributes on demand"""

    def __getattr__(self, name):
        # Only called when attribute doesn't exist
        print(f"Loading {name}...")
        value = self._load(name)
        setattr(self, name, value)  # Cache it
        return value

    def _load(self, name):
        return f"data_for_{name}"

obj = LazyLoader()
print(obj.config)   # Loading config... → data_for_config
print(obj.config)   # data_for_config (cached, __getattr__ not called again)

# __getattribute__ — intercepts ALL attribute access
class Logged:
    def __getattribute__(self, name):
        print(f"Accessing: {name}")
        return super().__getattribute__(name)  # Must call super() to avoid infinite recursion
```

**Related:** [OOP · Q35](#q35) — How does Python look up an attribute on an object?

---

<a name="q37"></a>
## Q37. (Hard) What is the difference between `__new__` and `__init__`?
**Answer:** Creating an object has two steps. `__new__(cls, ...)` **creates** and returns the new instance — it's the real constructor. Then, if it returned an instance of `cls`, Python calls `__init__(self, ...)` to **initialize** it; `__init__` must return `None`. You rarely override `__new__`: mainly when subclassing immutable types (`int`, `str`, `tuple` — their value must be set at creation), for singletons or instance caching, and in metaclasses.

- `__new__` — **creates** the instance (allocates memory), called first, returns the new object
- `__init__` — **initializes** the instance (sets attributes), called after `__new__`

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance  # Always return the same instance

    def __init__(self, value):
        self.value = value

s1 = Singleton(10)
s2 = Singleton(20)
print(s1 is s2)    # True — same object
print(s1.value)    # 20 — __init__ ran again on same object

# __new__ is also used for immutable types
class PositiveInt(int):
    def __new__(cls, value):
        if value <= 0:
            raise ValueError("Must be positive")
        return super().__new__(cls, value)

n = PositiveInt(5)   # OK
# PositiveInt(-1)    # ValueError
```

**Related:** [OOP · Q3](#q3) — What is a constructor? What is `__init__`? · [OOP · Q23](#q23) — What design patterns have you used? Explain Singleton, Factory, Observer.

---

<a name="q38"></a>
## Q38. (Hard) What is a metaclass in Python?
**Answer:** In Python, classes are objects too, and the class of a class is its **metaclass** — `type` by default. When Python runs a `class` statement, it executes the body into a namespace dict and then calls the metaclass — `type(name, bases, namespace)` — to build the class object. A custom metaclass (a subclass of `type`) can inspect or change classes at creation time: register them, enforce rules, add methods. Frameworks use this (Django models, ORMs, enums). For most needs simpler tools are enough: class decorators or `__init_subclass__`.

A metaclass is the **class of a class** — it controls how classes are created. `type` is the default metaclass.

```python
# type is the metaclass of all classes
print(type(int))    # <class 'type'>
print(type(str))    # <class 'type'>
print(type(list))   # <class 'type'>

# Creating a class dynamically with type
MyClass = type('MyClass', (object,), {'x': 10, 'greet': lambda self: "hello"})
obj = MyClass()
print(obj.x)        # 10
print(obj.greet())  # hello

# Custom metaclass — use case: auto-register subclasses
class PluginMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:  # Don't register the base class itself
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class CSVPlugin(Plugin): pass
class JSONPlugin(Plugin): pass

print(PluginMeta.registry)
# {'CSVPlugin': <class 'CSVPlugin'>, 'JSONPlugin': <class 'JSONPlugin'>}

# Modern alternative: __init_subclass__ (simpler, Python 3.6+)
class Plugin:
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin._registry[cls.__name__] = cls
```

**Related:** [Functional · Q15](./03_Functional_and_Decorators.md#q15) — What is a class decorator?

---

<a name="q39"></a>
## Q39. (Medium) What is monkey patching? When is it acceptable?
**Answer:** Changing a class, module or function **at runtime** — e.g. replacing a method. It's acceptable in **tests** (mocking: `unittest.mock.patch`) or as a temporary hotfix for a third-party bug. In application code it's risky: behaviour changes globally, it's hard to find, and it breaks on library upgrades.

```python
import requests
from unittest.mock import patch

with patch("requests.get") as fake_get:          # safe, scoped monkey patch in a test
    fake_get.return_value.status_code = 200
    assert requests.get("https://x").status_code == 200
```

**Related:** [Testing · Q3](./08_Testing_and_Tooling.md#q3) — What is a mock? When would you use `unittest.mock`?

---
