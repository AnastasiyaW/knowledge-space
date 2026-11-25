---
title: "OOP-Grundlagen"
category: concepts
tags: [python, oop, classes, inheritance, properties, encapsulation]
level: 3
source_sha256: b5572bedef7c8c929248123a26b05588bd141e4379b9ef400a941223c5d12ba4
translation: machine
translated_at: '2026-10-24'
---
# OOP-Grundlagen {#oop-fundamentals}

Die objektorientierte Programmierung in Python verwendet Klassen, um Daten (Attribute) und Verhalten (Methoden) zu bündeln. Zentrale Konzepte sind Vererbung, Property-Dekoratoren für kontrollierten Zugriff und die MRO (Method Resolution Order) für Mehrfachvererbung.

## Wichtige Fakten {#key-facts}

- `__init__` ist der Initialisierer (kein Konstruktor); er wird bei der Instanziierung automatisch aufgerufen
- `self` ist immer der erste Parameter von Instanzmethoden - verweist auf die aktuelle Instanz
- Reihenfolge der Attributsuche: Instanz-Dict -> Klassen-Dict -> Dict der Elternklasse (MRO)
- Python kennt keine echten privaten Attribute - `_name` ist eine Konvention für „geschützt", `__name` löst Name Mangling aus
- `property` stellt Getter, Setter und Deleter mit attributartiger Syntax bereit
- `super()` folgt der MRO, nicht nur der unmittelbaren Elternklasse

## Muster {#patterns}

### Klassendefinition {#class-definition}
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

### Instanz- vs. Klassenattribute {#instance-vs-class-attributes}
```python
class Counter:
    count = 0  # class attribute

    def increment(self):
        self.count += 1   # CREATES instance attribute, shadows class attr!
        # Use Counter.count += 1 to modify class attribute
```

### Methodentypen {#method-types}
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

### Properties {#properties}
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

### Vererbung {#inheritance}
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

### super() und MRO {#super-and-mro}
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

### isinstance() und issubclass() {#isinstance-and-issubclass}
```python
isinstance(obj, ClassName)      # respects inheritance
isinstance(obj, (A, B, C))     # any of these types
issubclass(Dog, Animal)         # True
```

### Kapselungskonventionen {#encapsulation-conventions}
```python
class MyClass:
    def __init__(self):
        self.public = "anyone"
        self._protected = "convention: internal"
        self.__private = "name-mangled to _MyClass__private"
```

### Beispiel BankAccount {#bankaccount-example}
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

## Fallstricke {#gotchas}

- `self.count += 1` erzeugt ein Instanzattribut, wenn `count` ein Klassenattribut ist - verwende `ClassName.count += 1`, um das Klassenattribut zu ändern
- Verwende niemals veränderliche Objekte (Listen, Dicts) als Klassenattribute, die von Instanzen geteilt werden, es sei denn, dies ist beabsichtigt
- `__init__` darf keinen Wert zurückgeben
- `__name__`-Dunder-Attribute sind Python-Spezialnamen - erfinde niemals eigene Dunder-Namen

## Siehe auch {#see-also}

- [[oop-advanced]] - ABC, Descriptors, Metaklassen, Dataclasses
- [[decorators]] - Klassendekoratoren, Dekorator-Muster
- [[magic-methods]] - `__str__`, `__repr__`, `__eq__` usw.
