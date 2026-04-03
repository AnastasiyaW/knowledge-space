---
title: OOP Fundamentals
category: concepts
tags: [python, oop, classes, inheritance, properties, encapsulation]
---

# OOP Fundamentals

Python's object-oriented programming uses classes to bundle data (attributes) and behavior (methods). Key concepts include inheritance, property decorators for controlled access, and the MRO (Method Resolution Order) for multiple inheritance.

## Key Facts

- `__init__` is the initializer (not constructor); called automatically on instantiation
- `self` is always the first parameter of instance methods - refers to current instance
- Attribute lookup order: instance dict -> class dict -> parent class dict (MRO)
- Python has no true private attributes - `_name` is convention for "protected", `__name` triggers name mangling
- `property` provides getter/setter/deleter with attribute-like syntax
- `super()` follows MRO, not just the immediate parent

## Patterns

### Class Definition
```python
class Dog:
    species = "Canis familiaris"  # class attribute (shared)

    def __init__(self, name, age):
        self.name = name    # instance attribute (unique)
        self.age = age

    def bark(self):
        return f"{self.name} says Woof!"

    def __str__(self):
        return f"Dog({self.name}, {self.age})"

my_dog = Dog("Rex", 5)
```

### Instance vs Class Attributes
```python
class Counter:
    count = 0  # class attribute

    def increment(self):
        self.count += 1   # CREATES instance attribute, shadows class attr!
        # Use Counter.count += 1 to modify class attribute
```

### Method Types
```python
class Employee:
    raise_amount = 1.04

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    # Instance method - operates on instance data
    def apply_raise(self):
        self.salary *= self.raise_amount

    # Class method - operates on class data, alternative constructor
    @classmethod
    def from_string(cls, emp_str):
        name, salary = emp_str.split('-')
        return cls(name, int(salary))

    # Static method - no access to instance or class
    @staticmethod
    def is_workday(day):
        return day.weekday() < 5

emp = Employee.from_string("John-50000")
```

### Properties
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):  # read-only computed property
        return self._celsius * 9/5 + 32

t = Temperature(25)
t.celsius = 30        # uses setter
print(t.fahrenheit)   # 86.0 (computed)
```

### Inheritance
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement")

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"
```

### super() and MRO
```python
class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)  # calls parent __init__
        self.department = department

# MRO for multiple inheritance (C3 linearization)
class D(B, C):
    pass

print(D.__mro__)  # (D, B, C, A, object)
```

### isinstance() and issubclass()
```python
isinstance(obj, ClassName)      # respects inheritance
isinstance(obj, (A, B, C))     # any of these types
issubclass(Dog, Animal)         # True
```

### Encapsulation Conventions
```python
class MyClass:
    def __init__(self):
        self.public = "anyone"
        self._protected = "convention: internal"
        self.__private = "name-mangled to _MyClass__private"
```

### BankAccount Example
```python
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
```

## Gotchas

- `self.count += 1` creates an instance attribute if `count` is a class attribute - use `ClassName.count += 1` to modify the class attribute
- Never use mutable objects as class attributes shared by instances (lists, dicts) unless intentional
- `__init__` must not return a value
- `__name__` dunder attributes are Python special names - never invent your own dunders

## See Also

- [[oop-advanced]] - ABC, descriptors, metaclasses, dataclasses
- [[decorators]] - class decorators, decorator patterns
- [[magic-methods]] - `__str__`, `__repr__`, `__eq__`, etc.
