---
title: Java Concurrency and Threading
category: concepts
tags: [java-spring, java, threads, concurrency, executors, completable-future, synchronization]
---

# Java Concurrency and Threading

Java threading model, synchronization primitives, thread pools, CompletableFuture, and concurrent collections. Foundation for building thread-safe applications.

## Key Facts

- Threads are heavyweight (~1MB stack each), limited by memory
- `start()` creates a new thread; calling `run()` directly executes on current thread
- `synchronized` provides mutual exclusion; `volatile` provides visibility only (no atomicity)
- Prefer `ReentrantLock` over `synchronized` for complex locking (tryLock, fairness)
- `ExecutorService` manages thread pools - never create raw threads in production
- `CompletableFuture` enables non-blocking async composition
- Deadlock: two threads waiting for each other's locks - prevent by consistent lock ordering

## Patterns

### Thread Creation
```java
// Runnable (preferred - allows extending other class)
new Thread(() -> System.out.println("Running")).start();

// Callable (returns value)
Callable<String> task = () -> { return "Result"; };
```

### Thread Lifecycle States
`NEW` -> `RUNNABLE` -> `RUNNING` -> `BLOCKED/WAITING/TIMED_WAITING` -> `TERMINATED`

### Synchronization
```java
// synchronized method
public synchronized void increment() { count++; }

// synchronized block (finer granularity)
public void update() {
    synchronized (this) { count++; }
}

// Atomic classes - lock-free thread safety
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();
count.compareAndSet(5, 10);  // CAS operation
```

### ReentrantLock and ReadWriteLock
```java
private final ReentrantLock lock = new ReentrantLock();
public void update() {
    lock.lock();
    try { /* critical section */ }
    finally { lock.unlock(); }  // ALWAYS in finally
}

// ReadWriteLock - concurrent reads, exclusive writes
ReadWriteLock rwLock = new ReentrantReadWriteLock();
rwLock.readLock().lock();   // multiple readers OK
rwLock.writeLock().lock();  // exclusive writer
```

### ExecutorService Thread Pools
```java
ExecutorService fixed = Executors.newFixedThreadPool(4);
ExecutorService single = Executors.newSingleThreadExecutor();
ExecutorService cached = Executors.newCachedThreadPool();
ScheduledExecutorService sched = Executors.newScheduledThreadPool(2);

Future<String> future = fixed.submit(() -> { return "Result"; });
String result = future.get();           // blocks
String timed = future.get(5, TimeUnit.SECONDS);  // with timeout
fixed.shutdown();
```

### CompletableFuture (Async Composition)
```java
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> fetchData())
    .thenApply(data -> process(data))
    .thenAccept(result -> display(result))
    .exceptionally(e -> handleError(e));

// Combine multiple
CompletableFuture<String> users = CompletableFuture.supplyAsync(() -> getUsers());
CompletableFuture<String> orders = CompletableFuture.supplyAsync(() -> getOrders());
CompletableFuture.allOf(users, orders).thenRun(() -> {
    combineResults(users.join(), orders.join());
});
```

### Concurrent Collections
```java
Map<String, Integer> map = new ConcurrentHashMap<>();
List<String> list = new CopyOnWriteArrayList<>();
BlockingQueue<Task> queue = new LinkedBlockingQueue<>();
queue.put(task);       // blocks if full
Task t = queue.take(); // blocks if empty
```

### Producer-Consumer Pattern
```java
BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(10);
// Producer: queue.put(item);   // blocks if full
// Consumer: queue.take();      // blocks if empty
```

## Gotchas

- `count++` is NOT atomic (read-increment-write) - use `AtomicInteger` or `synchronized`
- `volatile` ensures visibility but NOT atomicity - `volatile int count; count++` is still unsafe
- `ReentrantLock.unlock()` must be in `finally` block - forgetting it causes permanent lock
- Deadlock prevention: always acquire locks in the same global order
- `Thread.sleep()` holds locks; `Object.wait()` releases them
- `ConcurrentHashMap` does not allow null keys or values (unlike `HashMap`)

## See Also

- [[kotlin-coroutines]] - Lightweight alternative to threads
- [[spring-ioc-beans]] - Bean scopes and thread safety (singleton caution)
- [[algorithms-data-structures]] - Concurrent data structure internals
