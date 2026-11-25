---
title: "Concurrence en Go - Goroutines, channels et synchronisation"
category: concepts
tags: [go, golang, concurrency, goroutines, channels, mutex, scheduler]
level: 4
source_sha256: cae9d37fbb1021f273215e1fa2b588862c19a34c4f22eac0fafe5de781704ba1
translation: machine
translated_at: '2026-10-24'
---
# Concurrence en Go - Goroutines, channels et synchronisation {#go-concurrency-goroutines-channels-and-sync}

Le modèle de concurrence de Go : le scheduler GMP, les channels, select, les primitives de synchronisation et les patterns de production pour les programmes Go concurrents.

## Points clés {#key-facts}

- La pile d'une goroutine démarre à 2-8 Ko et croît dynamiquement : ~1 million de goroutines est réalisable
- Scheduler GMP : G (goroutine), M (thread OS), P (processeur/file d'exécution), nombre = GOMAXPROCS
- Ordonnancement coopératif-préemptif : cède la main lors des appels de fonction, et préemption asynchrone depuis Go 1.14
- Un channel non bufferisé synchronise l'émetteur et le récepteur ; un channel bufferisé ne bloque que lorsqu'il est plein
- Seul l'émetteur doit fermer un channel ; envoyer sur un channel fermé provoque une panique
- `go run -race` ou `go test -race` pour détecter les data races

## Patterns {#patterns}

### Canaux {#channels}

```go
ch := make(chan int)        // unbuffered: synchronizes sender and receiver
ch := make(chan int, 100)   // buffered: sender blocks only when full

ch <- value                 // send (blocks if full/no receiver)
value := <-ch               // receive (blocks if empty/no sender)
value, ok := <-ch           // ok=false if channel closed and empty

close(ch)                   // only sender should close
for v := range ch { ... }  // reads until closed
```

### Règles des canaux {#channel-rules}

| Opération | channel nil | channel fermé |
|-----------|-------------|----------------|
| Envoi | bloque indéfiniment | panique |
| Réception | bloque indéfiniment | renvoie la valeur zéro (ok=false) |

### Sémaphore via un channel bufferisé {#semaphore-via-buffered-channel}

```go
sem := make(chan struct{}, 10) // max 10 concurrent
for _, item := range items {
    sem <- struct{}{}           // acquire
    go func(x Item) {
        defer func() { <-sem }() // release
        process(x)
    }(item)
}
```

**Canal de signalisation** : `done := make(chan struct{})` - la structure de taille nulle n'utilise aucune mémoire.

### Instruction select {#select-statement}

```go
select {
case v := <-ch1:  ...
case ch2 <- val:  ...
case <-time.After(timeout): ...
default:          // non-blocking
}
```

Non déterministe : si plusieurs cas sont prêts, l'un d'eux est choisi au hasard.

### Primitives de synchronisation {#synchronization-primitives}

```go
var mu sync.Mutex
mu.Lock(); defer mu.Unlock()

var rw sync.RWMutex
rw.RLock(); defer rw.RUnlock()  // multiple concurrent readers
rw.Lock(); defer rw.Unlock()    // exclusive write

var wg sync.WaitGroup
wg.Add(n)
go func() { defer wg.Done(); ... }()
wg.Wait()

var once sync.Once
once.Do(func() { /* init */ }) // runs exactly once

var count int64
atomic.AddInt64(&count, 1)     // atomic increment
atomic.LoadInt64(&count)       // atomic read
```

### Arrêt gracieux {#graceful-shutdown}

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
<-ctx.Done()
// shutdown logic: close listeners, drain connections, flush buffers
```

### Fonctionnement interne du scheduler GMP {#gmp-scheduler-internals}

- **G** (Goroutine) : thread vert en espace utilisateur avec pile extensible
- **M** (Machine) : thread OS, limité par GOMAXPROCS
- **P** (Processor) : file d'exécution locale + contexte, nombre = GOMAXPROCS

Scheduler à vol de travail (work-stealing) : un P inactif vole des goroutines dans les files d'exécution des autres P.

`runtime.Gosched()` - cède explicitement la main ; rarement nécessaire. `runtime.GOMAXPROCS(n)` - définit le nombre de threads OS.

## Pièges {#gotchas}

- Envoyer sur un channel fermé provoque une panique : définissez toujours un modèle de propriété clair quant à celui qui ferme le channel
- Recevoir depuis un channel nil bloque indéfiniment (utile pour désactiver un cas d'un select)
- `sync.Map` ne remplace pas de manière générale `map + mutex` : elle est optimisée pour les charges à forte proportion de lectures ou pour des ensembles de clés disjoints
- Le détecteur de data races peut produire des faux négatifs, mais détecte la plupart des races : exécutez toujours les tests avec `-race`
- Un nombre élevé de goroutines ne dégrade les performances que lorsqu'elles se disputent simultanément les mêmes ressources
- `wg.Add(n)` doit être appelé avant de lancer les goroutines, et non à l'intérieur de celles-ci

## Voir aussi {#see-also}

- [[go/fundamentals]] - types, slices, maps, interfaces, gestion des erreurs
- [[microservices]] - services gRPC, tests, organisation du projet
- [[javascript-async-event-loop]] - comparaison : boucle d'événements vs goroutines
- [[kafka-messaging-fundamentals]] - les consumer groups sont souvent implémentés avec des goroutines
