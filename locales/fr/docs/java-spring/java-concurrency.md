---
title: "Concurrence et multithreading en Java"
category: concepts
tags: [java-spring, java, threads, concurrency, executors, completable-future, synchronization]
level: 4
source_sha256: d4071f148f8368152598efc712a1a15af4c098c116b0c2e52033595857e90d97
translation: machine
translated_at: '2026-10-24'
---
# Concurrence et multithreading en Java {#java-concurrency-and-threading}

Modèle de threads Java, primitives de synchronisation, pools de threads, CompletableFuture et collections concurrentes. Base pour la construction d'applications thread-safe.

## Points clés {#key-facts}

- Les threads sont coûteux (~1 Mo de pile chacun) et limités par la mémoire
- `start()` crée un nouveau thread ; appeler `run()` directement exécute le code sur le thread courant
- `synchronized` assure l'exclusion mutuelle ; `volatile` garantit uniquement la visibilité (pas l'atomicité)
- Préférer `ReentrantLock` à `synchronized` pour les verrouillages complexes (tryLock, équité)
- `ExecutorService` gère les pools de threads : ne jamais créer de threads bruts en production
- `CompletableFuture` permet la composition asynchrone non bloquante
- Interblocage (deadlock) : deux threads attendent mutuellement leurs verrous ; prévention par un ordre d'acquisition cohérent des verrous

## Modèles {#patterns}

### Création de threads {#thread-creation}
```java
// Runnable (preferred - allows extending other class)
new Thread(() -> System.out.println("Running")).start();

// Callable (returns value)
Callable<String> task = () -> { return "Result"; };
```

### États du cycle de vie d'un thread {#thread-lifecycle-states}
`NEW` -> `RUNNABLE` -> `RUNNING` -> `BLOCKED/WAITING/TIMED_WAITING` -> `TERMINATED`

### Synchronisation {#synchronization}
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

### ReentrantLock et ReadWriteLock {#reentrantlock-and-readwritelock}
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

### Pools de threads avec ExecutorService {#executorservice-thread-pools}
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

### CompletableFuture (composition asynchrone) {#completablefuture-async-composition}
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

### Collections concurrentes {#concurrent-collections}
```java
Map<String, Integer> map = new ConcurrentHashMap<>();
List<String> list = new CopyOnWriteArrayList<>();
BlockingQueue<Task> queue = new LinkedBlockingQueue<>();
queue.put(task);       // blocks if full
Task t = queue.take(); // blocks if empty
```

### Patron producteur-consommateur {#producer-consumer-pattern}
```java
BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(10);
// Producer: queue.put(item);   // blocks if full
// Consumer: queue.take();      // blocks if empty
```

## Pièges courants {#gotchas}

- `count++` n'est PAS atomique (lecture, incrémentation, écriture) : utiliser `AtomicInteger` ou `synchronized`
- `volatile` garantit la visibilité mais PAS l'atomicité : `volatile int count; count++` reste non sûr
- `ReentrantLock.unlock()` doit être placé dans un bloc `finally` : l'oublier provoque un verrou définitivement bloqué
- Prévention des interblocages : toujours acquérir les verrous dans le même ordre global
- `Thread.sleep()` conserve les verrous ; `Object.wait()` les libère
- `ConcurrentHashMap` n'accepte ni clés ni valeurs nulles (contrairement à `HashMap`)

## Voir aussi {#see-also}

- [[kotlin-coroutines]] - Alternative légère aux threads
- [[spring-ioc-beans]] - Portées des beans et thread safety (prudence avec les singletons)
- [[algorithms-data-structures]] - Fonctionnement interne des structures de données concurrentes
