---
title: "C++20-Koroutinen"
description: "Kooperatives Multitasking mit co_yield, co_return und co_await für verzögerte Generatoren und asynchrone E/A"
level: 4
source_sha256: 58c633c9f018c9d0b963b088c0cb5a295b20091a0636f17c465bb2f04d2eef84
translation: machine
translated_at: '2026-10-24'
---
# C++20-Koroutinen {#c20-coroutines}

Koroutinen bieten in C++20 kooperatives Multitasking – eine Funktion, die die Ausführung unterbrechen, einen Wert liefern und später dort fortsetzen kann, wo sie aufgehört hat. Sie unterscheiden sich grundlegend von Threads: Es geht nicht um Parallelität, sondern um das verschachtelte Ausführen von Code ohne Blockieren.

## Kernmodell {#core-model}

Eine reguläre Funktion besitzt einen **Stack-Frame**, der beim Aufruf erzeugt und bei der Rückkehr zerstört wird. Eine Koroutine besitzt einen **Koroutinen-Frame**, der auf dem Heap angelegt wird und über Unterbrechungen hinweg bestehen bleibt.

Der zentrale Unterschied zu Threads:
- **Threads** nutzen präemptives Multitasking: Das Betriebssystem entscheidet, wann umgeschaltet wird
- **Koroutinen** nutzen kooperatives Multitasking: Die Koroutine gibt ihren Zug freiwillig ab

Wenn eine Koroutine unterbricht, signalisiert sie sinngemäß: „Ich habe ein wenig Arbeit erledigt und bin bereit, anderen nun den Vortritt zu lassen.“ Bei der Fortsetzung läuft die Ausführung genau dort weiter, wo sie aufgehört hat, mit allen lokalen Zuständen unverändert.

## Schlüsselwörter {#keywords}

C++20 führt drei Schlüsselwörter ein, durch die eine Funktion zur Koroutine wird:

| Schlüsselwort | Zweck |
|---------------|-------|
| `co_yield expr` | Unterbrechen und einen Wert liefern |
| `co_return expr` | Endgültige Rückgabe (Koroutine wird beendet) |
| `co_await expr` | Unterbrechen, bis ein Awaitable abgeschlossen ist |

Jede Funktion, die eines dieser Schlüsselwörter enthält, wird vom Compiler automatisch als Koroutine behandelt.

## Anwendungsfälle {#use-cases}

Koroutinen eignen sich besonders für:
- **Verzögerte Generatoren**: Werte einzeln erzeugen, ohne die gesamte Sequenz zu berechnen
- **Asynchrone E/A**: Lesevorgang einer Datei starten, Kontrolle abgeben, fortsetzen, sobald Daten bereitstehen
- **Stream-Verarbeitung**: Elemente verarbeiten, sobald sie eintreffen, ohne alles zwischenzuspeichern
- **Pipelines**: Erzeuger und Verbraucher ohne Threads verketten

Weniger geeignet sind sie für:
- CPU-gebundene Parallelität (dafür `std::thread` bzw. `std::async` verwenden)
- Das gleichzeitige Ausführen von N identischen Aufgaben (ein Thread-Pool ist besser geeignet)

## Generator-Muster {#generator-pattern}

Das häufigste Koroutinen-Muster – eine Funktion, die eine Sequenz von Werten verzögert erzeugt:

```cpp
#include <coroutine>
#include <iostream>

// Simplified generator (real implementation needs promise_type, etc.)
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// Usage: values computed on-demand
auto fib = fibonacci();
for (int i = 0; i < 10; ++i) {
    std::cout << fib.next() << " ";
}
// Output: 0 1 1 2 3 5 8 13 21 34
```

## Lebenszyklus des Koroutinen-Frames {#coroutine-frame-lifecycle}

1. Der Aufrufer ruft die Koroutinen-Funktion auf
2. Der Koroutinen-Frame wird angelegt (auf dem Heap, nicht auf dem Stack)
3. Parameter werden in den Frame kopiert
4. Das Promise-Objekt wird konstruiert
5. Die Ausführung beginnt
6. Bei `co_yield`/`co_await`: Zustand wird gesichert, die Kontrolle kehrt zum Aufrufer zurück
7. Bei der Fortsetzung: Die Ausführung läuft ab dem Unterbrechungspunkt weiter
8. Bei `co_return` oder dem Verlassen des Funktionsendes: Der Frame wird zerstört

## Verhältnis zu anderen Nebenläufigkeitsfunktionen {#relationship-to-other-concurrency-features}

| Funktion | Modell | Overhead | Geeignet für |
|----------|--------|----------|--------------|
| `std::thread` | Präemptiv, vom Betriebssystem verwaltet | Hoch (Betriebssystem-Thread) | CPU-Parallelität |
| `std::async` | Aufgabenbasiert, ggf. mit Thread-Pool | Mittel | Fire-and-forget-Aufgaben |
| Koroutinen | Kooperativ, single-threaded | Niedrig (Heap-Frame) | E/A, Generatoren, Pipelines |

## Fallstricke {#gotchas}

- **Kein Standard-Generatortyp in C++20.** Man muss einen eigenen `Generator<T>` mit passendem `promise_type` schreiben oder eine Bibliothek verwenden. C++23 bringt `std::generator`.
- **Der Koroutinen-Frame wird auf dem Heap angelegt.** Der Compiler kann dies unter Umständen wegoptimieren (HALO – Heap Allocation eLision Optimization), garantiert ist es jedoch nicht. Bei performancekritischen engen Schleifen sollte man messen.
- **Dangling References kommen leicht vor.** Erfasst eine Koroutine eine Referenz auf eine lokale Variable des Aufrufers, und endet der Gültigkeitsbereich des Aufrufers, bevor die Koroutine fortgesetzt wird, entsteht undefiniertes Verhalten.
- **Das Debuggen ist schwierig.** Das schrittweise Durchlaufen von Unterbrechung und Fortsetzung einer Koroutine im Debugger wird Stand 2024 von den meisten IDEs nur eingeschränkt unterstützt.

## Querverweise {#cross-references}

- [Concurrency - Threads, Async, Atomics](concurrency.md) - Threads, Mutexe, atomare Operationen
- [[modern-cpp-features]] - weitere Neuerungen in C++20
- [[lambda-expressions]] - wird bei Koroutinen häufig für Callbacks verwendet
