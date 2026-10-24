---
title: "C++20 Ranges und Views"
description: "Komponierbare, verzögerte Pipelines für die Sequenzverarbeitung mit dem Pipe-Operator und Range-Adaptoren"
level: 3
source_sha256: 94b917c8683ffd5d90dc1737024a26f008700e48d2119b97f6df3cc2f18ae3a4
translation: machine
translated_at: '2026-10-24'
---
# C++20 Ranges und Views {#c20-ranges-and-views}

C++20-Ranges bieten eine komponierbare, verzögerte (lazy) und pipeline-orientierte Art, mit Sequenzen zu arbeiten. Sie ersetzen ausführliche Iterator-Paar-Muster durch eine übersichtlichere Syntax und erreichen durch die verzögerte Auswertung häufig eine bessere Performance.

## Kernkonzepte {#core-concepts}

**Range**: jeder Typ, der `begin()` und `end()` bereitstellt. Alle Standardcontainer sind Ranges.

**View**: ein leichtgewichtiger, nicht besitzender, verzögerter Range-Adaptor. Views kopieren keine Daten, sondern beschreiben eine Transformation, die erst bei der Iteration bedarfsgesteuert ausgewertet wird.

**Range-Algorithmen**: direkte Ersatzfunktionen für die Funktionen aus `<algorithm>`, die statt Iterator-Paaren einen ganzen Container entgegennehmen.

```cpp
#include <ranges>
#include <vector>
#include <algorithm>

std::vector<int> nums = {32, 1, 26, 7, 10, 21};

// Old way: iterator pair
std::sort(nums.begin(), nums.end());

// C++20 ranges: pass entire container
std::ranges::sort(nums);
```

## View-Pipeline (Pipe-Operator) {#view-pipeline-pipe-operator}

Views werden über den `|`-Operator komponiert, ähnlich wie Unix-Pipes. Jede Stufe erzeugt eine verzögerte View – es werden keine Kopien angelegt, keine Allokationen durchgeführt und nichts berechnet, bis die Iteration beginnt.

```cpp
#include <ranges>
#include <vector>

struct PossibleValue {
    bool flag;
    int value;
};

std::vector<PossibleValue> values = {
    {true, 1}, {true, 2}, {false, 3}, {true, 4}, {false, 5}
};

auto flagged = [](const PossibleValue& pv) { return pv.flag; };

auto result = values
    | std::views::filter(flagged)           // keep only flagged
    | std::views::transform([](const PossibleValue& pv) { return pv.value; })  // extract int
    | std::views::reverse                   // reverse order
    | std::views::drop(1);                  // skip first element

// result is a lazy view: {4, 2} -> drop 1 -> {2}
// Nothing computed until iteration:
for (int v : result) {
    std::cout << v << " ";
}
```

Entscheidende Eigenschaft: Die gesamte Pipeline wird **verzögert ausgewertet**. Es werden keine CPU-Zyklen für die Auswertung des Lambdas oder die Filterung aufgewendet, bis mit der Iteration über das Ergebnis begonnen wird. Das ist sowohl einfacher als auch schneller als die entsprechende imperative Schleife.

## Gängige View-Adaptoren {#common-view-adaptors}

| Adaptor | Zweck |
|---------|-------|
| `std::views::filter(pred)` | Elemente behalten, die das Prädikat erfüllen |
| `std::views::transform(fn)` | Jedes Element durch eine Funktion abbilden |
| `std::views::take(n)` | Die ersten n Elemente |
| `std::views::drop(n)` | Die ersten n Elemente überspringen |
| `std::views::reverse` | Iterationsreihenfolge umkehren |
| `std::views::keys` / `std::views::values` | Für kartenartige Ranges |
| `std::views::split(delim)` | Aufteilen anhand eines Trennzeichens |
| `std::views::join` | Verschachtelte Ranges abflachen |

## Ranges: Sortieren und Suchen {#ranges-sorting-and-finding}

```cpp
#include <ranges>
#include <algorithm>
#include <vector>

std::vector<int> v = {5, 3, 8, 1, 9};

// Sort with ranges
std::ranges::sort(v);

// Find with ranges
auto it = std::ranges::find(v, 8);

// Find with predicate
auto it2 = std::ranges::find_if(v, [](int x) { return x > 6; });

// Partial sort: nth_element
// Puts the correct element at position n, partitions rest
std::ranges::nth_element(v, v.begin() + 2);
// v[2] is now what would be at index 2 if fully sorted
// Elements before are <= v[2], elements after are >= v[2]
// Neither half is necessarily sorted - faster than partial_sort
```

## Namenskonventionen der Algorithmen {#algorithm-naming-conventions}

Der Header `<algorithm>` folgt einheitlichen Konventionen, die den Aufwand beim Auswendiglernen verringern:

- Parameter folgen immer derselben Reihenfolge: Anfang vor Ende, Quelle vor Ziel
- Das Suffix `_if` kennzeichnet die Prädikat-Variante: `find` vs. `find_if`, `count` vs. `count_if`
- Das Suffix `_copy` bedeutet, dass das Ergebnis an einen Ausgabe-Iterator geschrieben wird
- Das Suffix `_n` bedeutet, dass auf einer Anzahl statt auf einem Range operiert wird
- Die `ranges::`-Varianten nehmen ganze Container entgegen, die `std::`-Varianten Iterator-Paare

## Compiler-Unterstützung {#compiler-support}

Nicht alle Compiler unterstützen C++20-Ranges vollständig. Möglicherweise benötigen Sie:
- die neueste Compilerversion
- den expliziten Schalter: `-std=c++20` oder `/std:c++latest`
- Online-Compiler (Compiler Explorer) zum Testen der Feature-Verfügbarkeit

## Fallstricke {#gotchas}

- **Views besitzen keine Daten.** Wird der zugrunde liegende Container zerstört oder verändert, wird die View ungültig (dangling). Views nie speichern, die länger leben als ihre Quelle.
- **Die Debugger-Unterstützung ist schwach.** Die meisten Debugger (Stand 2024) können den Inhalt von Views nicht gut darstellen. Zur Inspektion von Werten während des Debuggens hilft ein Ansatz mit einer Schleife, die die Werte in einen String schreibt.
- **Nicht alle View-Kombinationen kompilieren.** Manche Pipelines setzen voraus, dass der zugrunde liegende Range bestimmte Konzepte erfüllt (z. B. benötigt `reverse` einen bidirektionalen Range). Fehlermeldungen können kryptisch ausfallen.
- **`nth_element` ist KEIN partielles Sortieren.** Es partitioniert korrekt, sortiert die „Gewinner“ aber nicht. Verwenden Sie es, wenn Sie die Top-N-Elemente benötigen, ohne deren Reihenfolge zu beachten (schneller als `partial_sort`).

## Querverweise {#cross-references}

- [[stl-algorithms]] - klassische Algorithmusmuster
- [[stl-containers]] - Containertypen, die mit Ranges arbeiten
- [[lambda-expressions]] - Schreiben von Prädikaten für filter/transform
- [Performance Optimization](performance-optimization.md) - Vorteile der verzögerten Auswertung
