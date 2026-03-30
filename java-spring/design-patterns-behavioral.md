---
title: Behavioral Design Patterns
category: patterns
tags: [java, design-patterns, strategy, observer, iterator, behavioral]
---
# Behavioral Design Patterns

Behavioral patterns are concerned with algorithms and the assignment of responsibilities between objects - how objects communicate and distribute work.

## Key Facts

- **Strategy** - defines family of algorithms, encapsulates each one, makes them interchangeable at runtime
- **Observer** - defines one-to-many dependency; when subject changes state, all observers are notified
- **Iterator** - provides sequential access to collection elements without exposing internal structure
- Observer is the foundation of event systems, reactive programming, and Spring's `ApplicationEvent`
- Iterator is built into Java: `Iterable`/`Iterator` interfaces, for-each loop uses them
- Strategy eliminates conditional statements by delegating to interchangeable algorithm objects
- See [[design-patterns-creational]] and [[design-patterns-structural]] for other pattern categories
- See [[spring-ioc-container]] for how Spring DI naturally implements Strategy pattern

## Patterns

### Strategy

```java
// Strategy interface
public interface SortStrategy {
    void sort(int[] array);
}

// Concrete strategies
public class BubbleSort implements SortStrategy {
    public void sort(int[] array) { /* bubble sort impl */ }
}
public class QuickSort implements SortStrategy {
    public void sort(int[] array) { /* quicksort impl */ }
}
public class MergeSort implements SortStrategy {
    public void sort(int[] array) { /* merge sort impl */ }
}

// Context - uses strategy
public class Sorter {
    private SortStrategy strategy;

    public Sorter(SortStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(SortStrategy strategy) {
        this.strategy = strategy;  // swap at runtime
    }

    public void performSort(int[] data) {
        strategy.sort(data);
    }
}

// Usage
Sorter sorter = new Sorter(new QuickSort());
sorter.performSort(data);
sorter.setStrategy(new MergeSort()); // switch algorithm
sorter.performSort(otherData);

// Java 8+ functional approach
public class Sorter {
    public void sort(int[] data, Consumer<int[]> strategy) {
        strategy.accept(data);
    }
}
```

### Observer

```java
import java.util.*;

// Subject (Observable)
public class EventManager {
    private final Map<String, List<EventListener>> listeners = new HashMap<>();

    public void subscribe(String eventType, EventListener listener) {
        listeners.computeIfAbsent(eventType, k -> new ArrayList<>()).add(listener);
    }

    public void unsubscribe(String eventType, EventListener listener) {
        listeners.getOrDefault(eventType, List.of()).remove(listener);
    }

    public void notify(String eventType, String data) {
        for (EventListener listener : listeners.getOrDefault(eventType, List.of())) {
            listener.update(eventType, data);
        }
    }
}

// Observer interface
public interface EventListener {
    void update(String eventType, String data);
}

// Concrete observers
public class EmailNotifier implements EventListener {
    public void update(String eventType, String data) {
        sendEmail("Event: " + eventType + ", Data: " + data);
    }
}

public class LogNotifier implements EventListener {
    public void update(String eventType, String data) {
        log.info("Event: {} Data: {}", eventType, data);
    }
}

// Usage
EventManager events = new EventManager();
events.subscribe("order.created", new EmailNotifier());
events.subscribe("order.created", new LogNotifier());
events.notify("order.created", "Order #123");
```

### Iterator

```java
// Custom iterable collection
public class NumberRange implements Iterable<Integer> {
    private final int start;
    private final int end;

    public NumberRange(int start, int end) {
        this.start = start;
        this.end = end;
    }

    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<>() {
            private int current = start;

            @Override
            public boolean hasNext() { return current <= end; }

            @Override
            public Integer next() {
                if (!hasNext()) throw new NoSuchElementException();
                return current++;
            }
        };
    }
}

// Usage - works with for-each
for (int n : new NumberRange(1, 10)) {
    System.out.println(n);
}
```

### Spring ApplicationEvent (Observer in Spring)

```java
// Event class
public class OrderCreatedEvent extends ApplicationEvent {
    private final String orderId;
    public OrderCreatedEvent(Object source, String orderId) {
        super(source);
        this.orderId = orderId;
    }
    public String getOrderId() { return orderId; }
}

// Publisher
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher publisher;

    public void createOrder(Order order) {
        orderRepo.save(order);
        publisher.publishEvent(new OrderCreatedEvent(this, order.getId()));
    }
}

// Listener
@Component
public class NotificationListener {
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        sendNotification(event.getOrderId());
    }
}
```

## Gotchas

- **Symptom**: Observer memory leak -> **Cause**: Observers never unsubscribed, held by subject reference -> **Fix**: Use WeakReference for observers, or ensure cleanup on lifecycle end
- **Symptom**: Observer notification order matters but is unpredictable -> **Cause**: HashMap/Set iteration order is undefined -> **Fix**: Use LinkedHashSet or priority-based notification
- **Symptom**: Strategy pattern with many implementations becomes hard to manage -> **Cause**: Too many concrete strategy classes -> **Fix**: Use lambdas (Java 8+) or a Strategy registry Map

## See Also

- [[design-patterns-creational]] - Object creation patterns
- [[design-patterns-structural]] - Object composition patterns
- [[spring-ioc-container]] - DI naturally enables Strategy; ApplicationEvent enables Observer
- [[android-architecture]] - Observer pattern underpins LiveData and StateFlow
- Refactoring.Guru: [Behavioral Patterns](https://refactoring.guru/design-patterns/behavioral-patterns)
