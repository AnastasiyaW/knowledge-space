---
title: "Manuelle Speicherverwaltung in C++"
description: "Rohes new/delete, Stack vs. Heap und die drei Fehlerklassen, die intelligente Zeiger und RAII motivieren"
level: 3
source_sha256: fe1a627336ab59da854461b93a8bd897a1a05a88c7301ebab7d0610c2462524e
translation: machine
translated_at: '2026-10-24'
---
# Manuelle Speicherverwaltung in C++ {#manual-memory-management-in-c}

Das Verständnis von rohem `new`/`delete` ist unerlässlich, um zu begreifen, warum [Smart Pointers and Memory Management](smart-pointers.md) und [[raii-resource-management]] existieren. Manuelle Speicherverwaltung ist fehleranfällig und sollte im modernen C++ vermieden werden, doch die Kenntnis der Fehlerfälle ist entscheidend.

## Stack vs. Heap (Free Store) {#stack-vs-heap-free-store}

**Stack**: automatische Speicherdauer. Objekte werden beim Betreten des Gültigkeitsbereichs erzeugt und beim Verlassen zerstört. Keine manuelle Verwaltung nötig.

**Heap (Free Store)**: dynamische Speicherdauer. Objekte werden mit `new` erzeugt und bestehen fort, bis sie explizit mit `delete` zerstört werden. Der Programmierer ist vollständig für die Lebensdauer verantwortlich.

```cpp
void example() {
    Resource local("local");     // stack: automatic cleanup at }

    Resource* p = new Resource("heap");  // heap: manual cleanup
    p->getName();
    delete p;                    // must explicitly destroy
}  // local destroyed here automatically, p's memory was freed above
```

## Drei Fehlerklassen {#three-failure-modes}

### 1. Zugriff nach delete (Dangling Pointer) {#1-use-after-delete-dangling-pointer}

```cpp
Resource* p = new Resource("data");
delete p;
p->getName();  // UNDEFINED BEHAVIOR: p points to freed memory
// Crash, garbage data, or silent corruption
```

### 2. Doppeltes delete {#2-double-delete}

```cpp
Resource* p = new Resource("data");
Resource* p2 = p;    // copy the pointer, not the object
delete p2;           // frees the memory
delete p;            // CRASH: same memory freed twice
```

Das Kopieren roher Zeiger ist gefährlich, weil mehrere Zeiger auf dasselbe Objekt Unklarheit darüber schaffen, wer für die Freigabe verantwortlich ist.

### 3. Speicherleck (Memory Leak) {#3-memory-leak}

```cpp
Resource* p = new Resource("data");
if (someCondition) {
    return;  // early return: delete never reached
}
delete p;    // never executes when condition is true
```

Die Regel „jedes `new` braucht genau ein `delete`“ klingt einfach, versagt aber bei:
- frühen Rückgaben (Early Returns)
- Exceptions, die zwischen `new` und `delete` geworfen werden
- komplexem Kontrollfluss
- Zeigerkopien, die Eigentumsunklarheit erzeugen

## Überladen von new und delete {#overloading-new-and-delete}

`new` und `delete` sind Operatoren, die für benutzerdefiniertes Verhalten überladen werden können. Die Überladung betrifft nur den Teil der Speicherallokation bzw. -freigabe – Konstruktion und Destruktion bleiben unverändert.

```cpp
#include <cstdlib>
#include <cstddef>

// Track allocations globally
static std::size_t allocated_mem = 0;

void* operator new(std::size_t size) {
    allocated_mem += size;
    std::cout << "Allocating " << size << " bytes\n";
    return std::malloc(size);
}

void operator delete(void* ptr, std::size_t size) noexcept {
    allocated_mem -= size;
    std::cout << "Deallocating " << size << " bytes\n";
    std::free(ptr);
}

// At program end: if allocated_mem != 0, there is a leak
```

Anwendungsfälle für Überladungen:
- **Benutzerdefinierte Erkennung von Speicherlecks** – Bilanz von Allokationen und Freigaben verfolgen
- **Memory Pooling** – große Blöcke vorab allokieren und Objekte zusammenlegen, um Fragmentierung zu reduzieren
- **Eingebettete Systeme** – eigenen Heap implementieren, wenn das Betriebssystem keinen bereitstellt
- **Performance-Profiling** – Allokationsmuster über die Zeit darstellen
- **Klassenspezifische Überladungen** – Allokation für eine bestimmte Klasse optimieren

## Globale vs. klassenbezogene Überladungen {#global-vs-class-scoped-overloads}

```cpp
// Global: affects ALL allocations in the program
void* operator new(std::size_t size) { /* ... */ }

// Class-scoped: affects only this class
class MyObject {
    static void* operator new(std::size_t size) { /* ... */ }
    static void operator delete(void* ptr) { /* ... */ }
};
```

## Vector: Größe vs. Kapazität {#vector-size-vs-capacity}

So verwaltet `std::vector` seinen Speicher intern:

```cpp
std::vector<Subject> v;
// size=0, capacity=0

v.reserve(3);
// size=0, capacity=3 (memory allocated, no objects constructed)

v.emplace_back("Math", 95);
// size=1, capacity=3 (one object constructed in-place)

v.push_back(Subject("History", 80));
// size=2, capacity=3 (temporary created then moved)

v.clear();
// size=0, capacity=3 (objects destroyed but memory NOT freed)
```

Wichtige Unterscheidungen:
- `reserve(n)`: reserviert Kapazität, ohne Objekte zu konstruieren
- `resize(n)`: ändert die Größe und konstruiert/zerstört Objekte bei Bedarf
- `emplace_back(args...)`: konstruiert das Objekt direkt an Ort und Stelle (kein Temporary, kein Move)
- `push_back(obj)`: kopiert bzw. verschiebt ein bestehendes Objekt in den Vector
- `clear()`: zerstört alle Objekte, verkleinert die Kapazität aber NICHT
- `shrink_to_fit()`: fordert eine (nicht bindende) Reduzierung der Kapazität an

**Bevorzugen Sie `emplace_back` gegenüber `push_back`**, wenn neue Objekte konstruiert werden – das vermeidet den Aufwand für Temporary und Move-Konstruktor.

## Die Antwort des modernen C++ {#the-modern-c-answer}

Die gesamte Klasse manueller Speicherverwaltungsfehler wird gelöst durch:
1. **RAII** – Lebensdauer der Ressource an den Gültigkeitsbereich des Objekts binden
2. **`std::unique_ptr`** – exklusives Eigentum, kein Mehraufwand
3. **`std::shared_ptr`** – geteiltes Eigentum mit Referenzzählung
4. Rohes `new`/`delete` im Anwendungscode niemals verwenden

## Stolpersteine {#gotchas}

- **`delete` auf einem Nullzeiger ist sicher** (laut Standard eine No-Op), `delete` auf einen bereits gelöschten Zeiger hingegen ist undefiniertes Verhalten.
- **`clear()` gibt den Speicher des Vectors nicht frei.** Nur der Destruktor oder `shrink_to_fit()` können die Kapazität reduzieren. Dies ist aus Performancegründen so vorgesehen – es vermeidet Reallokationen, wenn der Vector erneut befüllt wird.
- **Globale `operator new`-Überladungen wirken sich auf das gesamte Programm aus**, einschließlich Bibliothekscode. Verwenden Sie klassenbezogene Überladungen für gezieltes Verhalten.
- **`malloc`/`free` rufen KEINE Konstruktoren/Destruktoren auf.** Verwenden Sie sie nur innerhalb von `operator new`-/`operator delete`-Überladungen, niemals direkt im C++-Code.

## Querverweise {#cross-references}

- [Smart Pointers and Memory Management](smart-pointers.md) - `unique_ptr`, `shared_ptr`, `weak_ptr`
- [[raii-resource-management]] - das Muster, das manuelle Verwaltung ersetzt
- [[object-lifetime]] - Gültigkeitsbereich, Speicherdauer, Reihenfolge der Destruktion
- [[move-semantics]] - effiziente Übertragung von Ressourcen
