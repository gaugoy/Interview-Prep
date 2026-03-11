# 🏗️ 03 — Object-Oriented Programming
### [← Back to Index](./00_INDEX.md)

---

## Table of Contents
- [🟢 Easy (Q1–Q7)](#easy)
- [🟡 Medium (Q8–Q14)](#medium)
- [🔴 Hard (Q15–Q19)](#hard)

---

<a name="easy"></a>
## 🟢 Easy

---

### Q1. What are the 4 pillars of OOP?

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

### Q2. What is the difference between a class and an object?

**Answer:**
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

---

### Q3. What is a constructor? What is `__init__`?

**Answer:**
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
        # Destructor — called when object is garbage collected
        Person.count -= 1

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"

p1 = Person("Alice", 30)
p2 = Person("Bob", 25)
print(Person.count)   # 2

del p1
print(Person.count)   # 1
```

---

### Q4. What is inheritance? Single vs multiple?

**Answer:**
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

### Q5. What is method overriding?

**Answer:**
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

### Q6. What is the difference between public, protected, and private attributes?

**Answer:**
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

### Q7. What is `self` in Python?

**Answer:**
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

<a name="medium"></a>
## 🟡 Medium

---

### Q8. What is polymorphism? What is duck typing?

**Answer:**
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

### Q9. What is encapsulation? How does Python achieve it?

**Answer:**
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

### Q10. What is abstraction? How do ABCs work?

**Answer:**
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

---

### Q11. What is the difference between composition and inheritance?

**Answer:**
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

### Q12. What is MRO (Method Resolution Order)?

**Answer:**
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

---

### Q13. What is `super()`? Why is it important?

**Answer:**
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

---

### Q14. What are SOLID principles?

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

---

<a name="hard"></a>
## 🔴 Hard

---

### Q15. What is the diamond problem? How does Python resolve it?

**Answer:**
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

---

### Q16. What is a descriptor in Python?

**Answer:**
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

---

### Q17. What design patterns have you used? Explain Singleton, Factory, Observer.

**Answer:**

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

---

### Q18. What is the Liskov Substitution Principle (LSP)?

**Answer:**
LSP states that objects of a subclass must be **substitutable for objects of the superclass** without breaking the program.

```python
# ❌ LSP Violation — classic example
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    @Rectangle.width.setter
    def width(self, value):
        self._width = value
        self._height = value   # Square must keep sides equal

    @Rectangle.height.setter
    def height(self, value):
        self._width = value
        self._height = value

# This breaks LSP:
def double_width(rect: Rectangle):
    rect.width *= 2
    assert rect.area() == rect.height * rect.width  # Fails for Square!

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

---

### Q19. What is a mixin? When would you use one?

**Answer:**
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

---

### [← Back to Index](./00_INDEX.md) | [Next: Functional & Advanced Python →](./04_Functional_Advanced_Python.md)
