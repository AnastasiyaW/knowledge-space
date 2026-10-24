---
title: "Fondamentaux de la POO"
category: concepts
tags: [python, oop, classes, inheritance, properties, encapsulation]
level: 3
source_sha256: b5572bedef7c8c929248123a26b05588bd141e4379b9ef400a941223c5d12ba4
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de la POO {#oop-fundamentals}

La programmation orientée objet en Python utilise des classes pour regrouper des données (attributs) et des comportements (méthodes). Les concepts clés comprennent l'héritage, les décorateurs `property` pour un accès contrôlé, et le MRO (Method Resolution Order) pour l'héritage multiple.

## Points clés {#key-facts}

- `__init__` est l'initialiseur (et non le constructeur) ; il est appelé automatiquement lors de l'instanciation
- `self` est toujours le premier paramètre des méthodes d'instance : il désigne l'instance courante
- Ordre de recherche d'un attribut : dictionnaire de l'instance -> dictionnaire de la classe -> dictionnaire de la classe parente (MRO)
- Python ne possède pas de véritables attributs privés : `_name` est une convention pour « protégé », tandis que `__name` déclenche le name mangling
- `property` fournit un getter, un setter et un deleter avec une syntaxe d'attribut
- `super()` suit le MRO, et pas seulement le parent immédiat

## Modèles {#patterns}

### Définition d'une classe {#class-definition}
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

### Attributs d'instance et attributs de classe {#instance-vs-class-attributes}
```python
class Counter:
    count = 0  # class attribute

    def increment(self):
        self.count += 1   # CREATES instance attribute, shadows class attr!
        # Use Counter.count += 1 to modify class attribute
```

### Types de méthodes {#method-types}
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

### Propriétés {#properties}
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

### Héritage {#inheritance}
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

### super() et MRO {#super-and-mro}
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

### isinstance() et issubclass() {#isinstance-and-issubclass}
```python
isinstance(obj, ClassName)      # respects inheritance
isinstance(obj, (A, B, C))     # any of these types
issubclass(Dog, Animal)         # True
```

### Conventions d'encapsulation {#encapsulation-conventions}
```python
class MyClass:
    def __init__(self):
        self.public = "anyone"
        self._protected = "convention: internal"
        self.__private = "name-mangled to _MyClass__private"
```

### Exemple : compte bancaire {#bankaccount-example}
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

## Pièges {#gotchas}

- `self.count += 1` crée un attribut d'instance si `count` est un attribut de classe ; utilisez `ClassName.count += 1` pour modifier l'attribut de classe
- N'utilisez jamais d'objets mutables (listes, dictionnaires) comme attributs de classe partagés par les instances, sauf intention délibérée
- `__init__` ne doit pas renvoyer de valeur
- Les attributs dunder comme `__name__` sont des noms spéciaux de Python : ne créez jamais vos propres dunders

## Voir aussi {#see-also}

- [[oop-advanced]] - ABC, descripteurs, métaclasses, dataclasses
- [[decorators]] - décorateurs de classes, patrons de décorateurs
- [[magic-methods]] - `__str__`, `__repr__`, `__eq__`, etc.
