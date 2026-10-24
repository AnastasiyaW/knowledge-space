---
title: "Java-Concurrency und Threading"
category: concepts
tags: [java-spring, java, threads, concurrency, executors, completable-future, synchronization]
level: 4
source_sha256: d4071f148f8368152598efc712a1a15af4c098c116b0c2e52033595857e90d97
translation: machine
translated_at: '2026-10-24'
---
# Java-Concurrency und Threading {#java-concurrency-and-threading}

Das Java-Threading-Modell, Synchronisationsprimitive, Thread-Pools, CompletableFuture und nebenläufige Collections. Grundlage für den Bau thread-sicherer Anwendungen.

## Key Facts {#key-facts}

- Threads sind schwergewichtig (ca. 1 MB Stack pro Thread) und durch den Speicher begrenzt
- `start()` erzeugt einen neuen Thread; ein direkter Aufruf von `run()` führt den Code im aktuellen Thread aus
- `synchronized` sorgt für gegenseitigen Ausschluss; `volatile` garantiert nur Sichtbarkeit (keine Atomarität)
- `ReentrantLock` gegenüber `synchronized` bevorzugen, wenn komplexe Sperrlogik nötig ist (tryLock, Fairness)
- `ExecutorService` verwaltet Thread-Pools - in Produktivsystemen niemals rohe Threads erzeugen
- `CompletableFuture` ermöglicht nicht-blockierende asynchrone Komposition
- Deadlock: Zwei Threads warten auf die Sperren des jeweils anderen - Vermeidung durch konsistente Reihenfolge beim Sperren

## Patterns {#patterns}

### Thread Creation {#thread-creation}
```java
// Runnable (preferred - allows extending other class)
new Thread(() -> System.out.println("Running")).start();

// Callable (returns value)
Callable<String> task = () -> { return "Result"; };
```

### Thread Lifecycle States {#thread-lifecycle-states}
`NEW` -> `RUNNABLE` -> `RUNNING` -> `BLOCKED/WAITING/TIMED_WAITING` -> `TERMINATED`

### Synchronization {#synchronization}
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

### ReentrantLock and ReadWriteLock {#reentrantlock-and-readwritelock}
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

### ExecutorService Thread Pools {#executorservice-thread-pools}
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

### CompletableFuture (Async Composition) {#completablefuture-async-composition}
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

### Concurrent Collections {#concurrent-collections}
```java
Map<String, Integer> map = new ConcurrentHashMap<>();
List<String> list = new CopyOnWriteArrayList<>();
BlockingQueue<Task> queue = new LinkedBlockingQueue<>();
queue.put(task);       // blocks if full
Task t = queue.take(); // blocks if empty
```

### Producer-Consumer Pattern {#producer-consumer-pattern}
```java
BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(10);
// Producer: queue.put(item);   // blocks if full
// Consumer: queue.take();      // blocks if empty
```

## Gotchas {#gotchas}

- `count++` ist NICHT atomar (Lesen, Erhöhen, Schreiben) - `AtomicInteger` oder `synchronized` verwenden
- `volatile` garantiert Sichtbarkeit, aber NICHT Atomarität - `volatile int count; count++` ist weiterhin unsicher
- `ReentrantLock.unlock()` muss in einem `finally`-Block stehen - wird er vergessen, bleibt die Sperre dauerhaft belegt
- Deadlock-Vermeidung: Sperren immer in derselben globalen Reihenfolge erwerben
- `Thread.sleep()` hält Sperren; `Object.wait()` gibt sie frei
- `ConcurrentHashMap` erlaubt weder `null`-Schlüssel noch `null`-Werte (anders als `HashMap`)

## See Also {#see-also}

- [[kotlin-coroutines]] - Leichtgewichtige Alternative zu Threads
- [[spring-ioc-beans]] - Bean-Scopes und Thread-Sicherheit (Vorsicht bei Singletons)
- [[algorithms-data-structures]] - Interna nebenläufiger Datenstrukturen
