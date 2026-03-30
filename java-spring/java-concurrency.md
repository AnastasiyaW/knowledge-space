---
title: Java Concurrency
category: concepts
tags: [java, threads, concurrency, synchronized, executor-service, locks, atomic]
---
# Java Concurrency

## Key Facts

- Two ways to create threads: extend `Thread` class or implement `Runnable` interface (preferred)
- `synchronized` keyword ensures only one thread executes a block/method at a time using intrinsic lock
- `volatile` guarantees visibility of variable changes across threads but does NOT ensure atomicity
- `java.util.concurrent` package provides higher-level concurrency utilities since Java 5
- `AtomicInteger`, `AtomicLong`, `AtomicReference` - lock-free thread-safe operations via CAS
- `ExecutorService` manages thread pools - never create raw threads in production code
- `ReentrantLock` provides explicit lock/unlock with tryLock, fairness, and multiple conditions
- `CountDownLatch` - one-time barrier; `CyclicBarrier` - reusable barrier; `Phaser` - flexible phasing
- `Exchanger<V>` allows two threads to swap objects at a synchronization point
- See [[java-collections]] for base collection types
- See [[spring-ioc-container]] for how Spring manages bean scopes in concurrent contexts

## Patterns

### Thread creation

```java
// Option 1: Runnable (preferred - separates task from thread)
Runnable task = () -> {
    System.out.println("Running in: " + Thread.currentThread().getName());
};
Thread t = new Thread(task);
t.start();  // start(), NOT run()!

// Option 2: Extend Thread
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Custom thread");
    }
}
new MyThread().start();
```

### Synchronized and thread safety

```java
public class BankAccount {
    private int balance;

    // Synchronized method - intrinsic lock on 'this'
    public synchronized void transferFunds(BankAccount target, int amount) {
        if (this.balance >= amount) {
            this.balance -= amount;
            target.balance += amount;
        }
    }

    // Synchronized block - finer granularity
    public void deposit(int amount) {
        synchronized (this) {
            balance += amount;
        }
    }
}
```

### Atomic operations

```java
import java.util.concurrent.atomic.AtomicInteger;

AtomicInteger counter = new AtomicInteger(0);

// Thread-safe without synchronized
counter.incrementAndGet();    // ++counter
counter.getAndIncrement();    // counter++
counter.addAndGet(10);        // counter += 10
counter.compareAndSet(10, 0); // CAS: if 10 then set 0
```

### ExecutorService and thread pools

```java
import java.util.concurrent.*;

// Fixed pool - reuses N threads
ExecutorService pool = Executors.newFixedThreadPool(4);

// Submit tasks
Future<String> future = pool.submit(() -> {
    Thread.sleep(1000);
    return "Result";
});

String result = future.get();  // blocks until complete
String result2 = future.get(5, TimeUnit.SECONDS); // with timeout

// Shutdown
pool.shutdown();               // finish pending, reject new
pool.awaitTermination(10, TimeUnit.SECONDS);

// Other pool types
Executors.newCachedThreadPool();       // grows/shrinks dynamically
Executors.newSingleThreadExecutor();   // single worker, ordered
Executors.newScheduledThreadPool(2);   // delayed/periodic tasks
```

### ReentrantLock

```java
import java.util.concurrent.locks.ReentrantLock;

ReentrantLock lock = new ReentrantLock();

public void safeOperation() {
    lock.lock();
    try {
        // critical section
    } finally {
        lock.unlock();  // ALWAYS in finally
    }
}

// tryLock - non-blocking attempt
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try { /* work */ }
    finally { lock.unlock(); }
} else {
    // handle lock not acquired
}
```

### CountDownLatch

```java
CountDownLatch latch = new CountDownLatch(3);

// Worker threads count down
for (int i = 0; i < 3; i++) {
    new Thread(() -> {
        doWork();
        latch.countDown();  // decrement
    }).start();
}

latch.await();  // blocks until count reaches 0
System.out.println("All workers finished");
```

### Concurrent collections

```java
// Thread-safe map - no need for external synchronization
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("key", 1);
map.compute("key", (k, v) -> v + 1);  // atomic compute

// Thread-safe list - snapshot iterator (no CME)
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

// Blocking queue - producer/consumer
BlockingQueue<String> queue = new LinkedBlockingQueue<>(100);
queue.put("item");        // blocks if full
String item = queue.take(); // blocks if empty
```

## Gotchas

- **Symptom**: Deadlock - two threads hang forever -> **Cause**: Thread A locks X then waits for Y, Thread B locks Y then waits for X -> **Fix**: Always acquire locks in consistent global order; use `tryLock` with timeout
- **Symptom**: Thread sees stale value of shared variable -> **Cause**: Missing `volatile` or synchronization; CPU cache not flushed -> **Fix**: Use `volatile`, `synchronized`, or `Atomic*` classes
- **Symptom**: Thread.start() vs Thread.run() confusion -> **Cause**: Calling `run()` executes on current thread, not new thread -> **Fix**: Always call `start()` to create actual OS thread
- **Symptom**: `interrupt()` doesn't stop the thread -> **Cause**: Thread doesn't check `Thread.interrupted()` or catch `InterruptedException` -> **Fix**: Check `isInterrupted()` in loops, handle `InterruptedException` properly

## See Also

- [[java-collections]] - Non-thread-safe collections that need wrapping
- [[kotlin-fundamentals]] - Kotlin coroutines as alternative to Java threads
- [[spring-ioc-container]] - Singleton beans in concurrent web application contexts
- Oracle Tutorial: [Concurrency](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- Java API: [java.util.concurrent](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/package-summary.html)
