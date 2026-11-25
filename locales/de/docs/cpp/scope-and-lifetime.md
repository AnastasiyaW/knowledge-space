---
title: "Variablen-Gültigkeitsbereich und Lebensdauer in C++"
description: "Regeln für Gültigkeitsbereiche auf Blockebene, Namensverdeckung und deterministische Reihenfolge der Destruktion als Voraussetzung für RAII"
level: 4
source_sha256: cc71320356236c667198f8b1cb0ab13afa2bf1ae3baae1deff7395656012e1e1
translation: machine
translated_at: '2026-10-24'
---
# Variablen-Gültigkeitsbereich und Lebensdauer in C++ {#variable-scope-and-lifetime-in-c}

C++ kennt Gültigkeitsbereiche auf Blockebene mit strikten Regeln dafür, wo Variablen sichtbar sind und wann sie zerstört werden. Das Verständnis des Gültigkeitsbereichs verhindert Fehler durch Namensverdeckung und ist Voraussetzung für [[raii-resource-management]].

## Ebenen des Gültigkeitsbereichs {#scope-levels}

C++ unterstützt drei Ebenen des Gültigkeitsbereichs:

1. **Globaler Gültigkeitsbereich** – außerhalb aller Funktionen deklariert, überall zugänglich
2. **Funktions- bzw. lokaler Gültigkeitsbereich** – innerhalb einer Funktion deklariert, nur innerhalb dieser Funktion zugänglich
3. **Blockbezogener Gültigkeitsbereich** – innerhalb von `{}` deklariert, nur innerhalb dieses Blocks zugänglich

```cpp
int x = 10;  // global scope

int main() {
    int x = 20;  // local scope (shadows global x)

    {
        int x = 30;  // block scope (shadows local x)
        std::cout << x;  // prints 30 (nearest scope)
    }

    std::cout << x;  // prints 20 (block x is gone)

    // Access global x despite local shadow:
    std::cout << ::x;  // prints 10 (scope resolution operator)
}
```

## Regeln zur Namensauflösung {#name-lookup-rules}

Wird ein Name verwendet, durchsucht der Compiler die Gültigkeitsbereiche von innen nach außen:
1. Aktueller Block
2. Umschließende Blöcke
3. Funktionsbereich
4. Namensraumbereich
5. Globaler Gültigkeitsbereich

Der **erste Treffer gewinnt**. Innere Deklarationen verdecken äußere.

## Bereichsauflösungsoperator {#scope-resolution-operator}

Der Operator `::` greift auf einen bestimmten Gültigkeitsbereich zu:

```cpp
int x = 10;  // global

int main() {
    int x = 20;  // local shadows global
    std::cout << x;    // 20 (local)
    std::cout << ::x;  // 10 (global, bypassing shadow)
}
```

Er wird auch für den Zugriff auf Namensräume und Klassenmitglieder verwendet: `std::cout`, `MyClass::method`.

## Speicherdauer {#storage-duration}

| Dauer | Erzeugt | Zerstört | Beispiel |
|-------|---------|----------|----------|
| Automatisch | Blockeintritt | Blockaustritt | Lokale Variablen |
| Statisch | Programmstart | Programmende | `static`-Lokalvariablen, globale Variablen |
| Dynamisch | `new` | `delete` | Auf dem Heap angelegt |
| Thread | Threadstart | Threadende | `thread_local` |

## const als Dokumentation {#const-as-documentation}

Variablen als `const` zu markieren, dient als Dokumentation des Gültigkeitsbereichs:

```cpp
void process() {
    const int max_retries = 3;  // documents: this will not change
    int attempts = 0;           // documents: this WILL change

    // Technique for exploring unfamiliar code:
    // 1. Mark everything const
    // 2. Compile
    // 3. Remove const where compiler complains
    // Result: map of which variables actually vary
}
```

Regeln für `const`:
- Muss bei der Deklaration initialisiert werden (kein „später const machen“)
- Der Compiler erzwingt dies: Versuche, den Wert zu ändern, führen zu einem Kompilierfehler
- Macht die Absicht für andere Entwickler, die den Code lesen, deutlich

## Globale Variablen {#global-variables}

Globale Variablen:
- Werden beim Programmstart erzeugt und beim Programmende zerstört
- Liegen weder auf dem Stack noch auf dem Heap (eigenes Speichersegment)
- Sind aus jeder Funktion zugänglich (schlecht für die Kapselung)
- Die Initialisierungsreihenfolge über Übersetzungseinheiten hinweg ist **undefiniert** (Static Initialization Order Fiasco)

**Allgemeine Regel**: Globalen veränderlichen Zustand vermeiden. `const`- bzw. `constexpr`-Globals nur für echte Konstanten verwenden; für alles andere Zustand über Parameter übergeben.

## Stolperfallen {#gotchas}

- **Namensverdeckung erfolgt standardmäßig stillschweigend.** Eine Variable mit demselben Namen in einem inneren Gültigkeitsbereich zu deklarieren, ist gültiges C++ und erzeugt keine Warnung, solange `-Wshadow` nicht aktiviert ist. Immer mit aktivierten Warnungen kompilieren.
- **Variablen in der Initialisierung einer `for`-Schleife sind auf die Schleife beschränkt.** Bei `for (int i = 0; ...)` existiert `i` nach dem Schleifenkörper nicht mehr.
- **`if`-Initialisierungsanweisungen (C++17) sind blockbezogen.** Bei `if (auto it = map.find(key); it != map.end())` existiert `it` nur innerhalb von `if`/`else`.
- **Statische lokale Variablen werden beim ersten Funktionsaufruf einmalig initialisiert** und bleiben danach erhalten. Bei späteren Aufrufen werden sie **nicht** erneut initialisiert – das ist nützlich für Muster der verzögerten Initialisierung.

## Querverweise {#cross-references}

- [[raii-resource-management]] – Bindung der Bereinigung an das Verlassen des Gültigkeitsbereichs
- [[object-lifetime]] – Reihenfolge von Konstruktion und Destruktion
- [[const-and-type-safety]] – Const-Korrektheit
- [Smart Pointers and Memory Management](smart-pointers.md) – Speicherverwaltung über den Gültigkeitsbereich
