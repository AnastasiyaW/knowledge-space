---
title: Creational Design Patterns
category: patterns
tags: [java, design-patterns, singleton, factory, builder, prototype, creational]
---
# Creational Design Patterns

Creational patterns abstract the instantiation process - they help make a system independent of how its objects are created, composed, and represented.

## Key Facts

- **Singleton** - exactly one instance, global access point. Spring beans are singletons by default
- **Factory Method** - defines interface for creating objects, subclasses decide which class to instantiate
- **Abstract Factory** - creates families of related objects without specifying concrete classes
- **Builder** - constructs complex objects step by step, separates construction from representation
- **Prototype** - creates new objects by cloning existing ones (avoids expensive construction)
- Gang of Four (GoF) book defines 5 creational patterns; these are the most common in Java/Spring
- See [[spring-ioc-container]] for how Spring IoC replaces manual factory/singleton patterns
- See [[design-patterns-structural]] for patterns that compose objects

## Patterns

### Singleton

```java
// Thread-safe lazy initialization (Bill Pugh idiom)
public class DatabaseConnection {
    private DatabaseConnection() {}

    private static class Holder {
        private static final DatabaseConnection INSTANCE = new DatabaseConnection();
    }

    public static DatabaseConnection getInstance() {
        return Holder.INSTANCE;
    }
}

// Enum singleton (Joshua Bloch recommended)
public enum Logger {
    INSTANCE;
    public void log(String msg) { System.out.println(msg); }
}
Logger.INSTANCE.log("Hello");

// In Spring - just use @Component (singleton scope by default)
@Component
public class MyService { }
```

### Factory Method

```java
// Abstract creator
public interface NotificationFactory {
    Notification create(String type);
}

// Concrete factory
public class NotificationFactoryImpl implements NotificationFactory {
    @Override
    public Notification create(String type) {
        return switch (type) {
            case "email" -> new EmailNotification();
            case "sms"   -> new SmsNotification();
            case "push"  -> new PushNotification();
            default -> throw new IllegalArgumentException("Unknown: " + type);
        };
    }
}

// Usage
Notification n = factory.create("email");
n.send("Hello!");
```

### Abstract Factory

```java
// Families of related objects
public interface UIFactory {
    Button createButton();
    TextField createTextField();
}

public class DarkThemeFactory implements UIFactory {
    public Button createButton() { return new DarkButton(); }
    public TextField createTextField() { return new DarkTextField(); }
}

public class LightThemeFactory implements UIFactory {
    public Button createButton() { return new LightButton(); }
    public TextField createTextField() { return new LightTextField(); }
}
```

### Builder

```java
public class User {
    private final String name;
    private final String email;
    private final int age;
    private final String phone;

    private User(Builder builder) {
        this.name = builder.name;
        this.email = builder.email;
        this.age = builder.age;
        this.phone = builder.phone;
    }

    public static class Builder {
        private final String name;   // required
        private String email;        // optional
        private int age;
        private String phone;

        public Builder(String name) { this.name = name; }
        public Builder email(String email) { this.email = email; return this; }
        public Builder age(int age) { this.age = age; return this; }
        public Builder phone(String phone) { this.phone = phone; return this; }
        public User build() { return new User(this); }
    }
}

// Usage - readable, no telescoping constructors
User user = new User.Builder("Alice")
    .email("alice@example.com")
    .age(30)
    .build();
```

### Prototype

```java
public class Document implements Cloneable {
    private String title;
    private List<String> sections;

    @Override
    public Document clone() {
        try {
            Document copy = (Document) super.clone();
            copy.sections = new ArrayList<>(this.sections); // deep copy
            return copy;
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException(e);
        }
    }
}

// Usage - clone expensive-to-create objects
Document template = loadFromDatabase();
Document newDoc = template.clone();
newDoc.setTitle("New Document");
```

## Gotchas

- **Symptom**: Singleton via double-checked locking without `volatile` -> **Cause**: JVM can reorder instructions, returning partially constructed object -> **Fix**: Use enum singleton, Bill Pugh holder, or mark instance field `volatile`
- **Symptom**: `clone()` creates shared mutable state -> **Cause**: Shallow copy - nested objects are still shared references -> **Fix**: Deep copy mutable fields in `clone()` method
- **Symptom**: Builder allows building incomplete objects -> **Cause**: No validation in `build()` -> **Fix**: Validate required fields in `build()`, throw `IllegalStateException`
- **Symptom**: Reflection breaks singleton -> **Cause**: `Constructor.newInstance()` bypasses private constructor -> **Fix**: Use enum singleton (reflection-proof) or throw exception in constructor if instance exists

## See Also

- [[design-patterns-structural]] - Patterns for composing objects
- [[design-patterns-behavioral]] - Patterns for object communication
- [[spring-ioc-container]] - Spring DI as modern alternative to manual Factory/Singleton
- GoF Book: "Design Patterns: Elements of Reusable Object-Oriented Software"
- Refactoring.Guru: [Creational Patterns](https://refactoring.guru/design-patterns/creational-patterns)
