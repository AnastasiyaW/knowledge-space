---
title: Structural Design Patterns
category: patterns
tags: [java, design-patterns, decorator, adapter, bridge, facade, flyweight, proxy, structural]
---
# Structural Design Patterns

Structural patterns deal with object composition - how classes and objects are composed to form larger structures while keeping the structure flexible and efficient.

## Key Facts

- **Decorator** - dynamically adds behavior to objects by wrapping them (used in Java I/O streams)
- **Adapter** - converts one interface to another that clients expect (like USB-to-outlet adapter)
- **Bridge** - separates abstraction from implementation so both can vary independently
- **Facade** - provides simplified interface to a complex subsystem
- **Flyweight** - shares common state between many objects to reduce memory (e.g., String pool)
- **Proxy** - controls access to another object (used in Spring AOP, lazy loading, security)
- Java I/O is a textbook Decorator example: `new BufferedReader(new InputStreamReader(new FileInputStream("f")))`
- See [[design-patterns-creational]] for patterns that create objects
- See [[spring-ioc-container]] for how Spring uses Proxy pattern extensively

## Patterns

### Decorator

```java
// Base interface
public interface Coffee {
    double getCost();
    String getDescription();
}

// Concrete component
public class SimpleCoffee implements Coffee {
    public double getCost() { return 1.0; }
    public String getDescription() { return "Simple coffee"; }
}

// Decorator base
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee decorated;
    public CoffeeDecorator(Coffee coffee) { this.decorated = coffee; }
}

// Concrete decorators
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }
    public double getCost() { return decorated.getCost() + 0.5; }
    public String getDescription() { return decorated.getDescription() + ", milk"; }
}

// Usage - stack decorators
Coffee order = new MilkDecorator(new SugarDecorator(new SimpleCoffee()));
// "Simple coffee, sugar, milk" - $2.0
```

### Adapter

```java
// Existing interface (what client uses)
public interface MediaPlayer {
    void play(String filename);
}

// Incompatible interface (what we have)
public interface AdvancedPlayer {
    void playMp4(String filename);
    void playVlc(String filename);
}

// Adapter - bridges the gap
public class MediaAdapter implements MediaPlayer {
    private final AdvancedPlayer advancedPlayer;

    public MediaAdapter(AdvancedPlayer player) {
        this.advancedPlayer = player;
    }

    @Override
    public void play(String filename) {
        if (filename.endsWith(".mp4")) {
            advancedPlayer.playMp4(filename);
        } else if (filename.endsWith(".vlc")) {
            advancedPlayer.playVlc(filename);
        }
    }
}
```

### Bridge

```java
// Implementation hierarchy
public interface AccountType {
    String getType();
    double getInterestRate();
}

public class SavingsAccount implements AccountType {
    public String getType() { return "Savings"; }
    public double getInterestRate() { return 0.04; }
}

public class DebitAccount implements AccountType {
    public String getType() { return "Debit"; }
    public double getInterestRate() { return 0.01; }
}

// Abstraction hierarchy (uses AccountType via composition, not inheritance)
public abstract class Currency {
    protected AccountType accountType; // bridge
    public Currency(AccountType type) { this.accountType = type; }
    abstract String getCurrency();
}

public class Dollar extends Currency {
    public Dollar(AccountType type) { super(type); }
    public String getCurrency() { return "USD"; }
}

// Any Currency x Any AccountType - no class explosion
Currency account = new Dollar(new SavingsAccount());
```

### Facade

```java
// Complex subsystem
class VideoDecoder { byte[] decode(String file) { /* ... */ } }
class AudioDecoder { byte[] decode(String file) { /* ... */ } }
class SubtitleParser { String parse(String file) { /* ... */ } }
class Renderer { void render(byte[] video, byte[] audio, String subs) { /* ... */ } }

// Facade - simple interface
public class VideoPlayerFacade {
    private final VideoDecoder video = new VideoDecoder();
    private final AudioDecoder audio = new AudioDecoder();
    private final SubtitleParser subs = new SubtitleParser();
    private final Renderer renderer = new Renderer();

    public void play(String file) {
        renderer.render(
            video.decode(file),
            audio.decode(file),
            subs.parse(file)
        );
    }
}

// Client: one method instead of four
new VideoPlayerFacade().play("movie.mp4");
```

### Proxy

```java
// Real subject
public class ExpensiveDatabase implements Database {
    public ExpensiveDatabase() {
        connectToRemoteServer(); // slow
    }
    public String query(String sql) { return executeQuery(sql); }
}

// Proxy - lazy initialization + access control
public class DatabaseProxy implements Database {
    private ExpensiveDatabase real;
    private final String userRole;

    public DatabaseProxy(String role) { this.userRole = role; }

    public String query(String sql) {
        if (!userRole.equals("ADMIN") && sql.startsWith("DROP")) {
            throw new SecurityException("Insufficient privileges");
        }
        if (real == null) {
            real = new ExpensiveDatabase(); // lazy init
        }
        return real.query(sql);
    }
}
```

## Gotchas

- **Symptom**: Decorator ordering matters but isn't documented -> **Cause**: Decorators wrap in sequence; `A(B(x))` != `B(A(x))` -> **Fix**: Document decoration order, consider Builder pattern for complex decoration chains
- **Symptom**: Too many adapter classes -> **Cause**: One adapter per incompatible interface pair -> **Fix**: Use generic adapter with functional interface, or refactor to common interface
- **Symptom**: Facade becomes a God Object -> **Cause**: Adding too many methods to facade -> **Fix**: Create multiple focused facades for different use cases

## See Also

- [[design-patterns-creational]] - Object creation patterns
- [[design-patterns-behavioral]] - Object communication patterns
- [[spring-ioc-container]] - Spring AOP uses dynamic proxies extensively
- Refactoring.Guru: [Structural Patterns](https://refactoring.guru/design-patterns/structural-patterns)
