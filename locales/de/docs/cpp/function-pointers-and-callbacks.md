---
title: "Funktionszeiger und Callbacks in C++"
description: "Funktionszeiger im C-Stil, std::function und Lambdas für indirekte Aufrufe und Callback-Muster"
level: 3
source_sha256: d96b61d5bb5f83c7e7079207a54517a928750a88c65c1de59ce5e9182e5415e2
translation: machine
translated_at: '2026-10-24'
---
# Funktionszeiger und Callbacks in C++ {#function-pointers-and-callbacks-in-c}

Funktionen in C++ haben Adressen im Speicher. Ein Funktionszeiger enthält die Adresse einer Funktion und kann sie indirekt aufrufen. Modernes C++ bietet `std::function` und Lambdas als sicherere und flexiblere Alternativen.

## Funktionszeiger im C-Stil (Legacy) {#legacy-c-style-function-pointers}

Jede Funktion liegt im Speicher. Der Funktionsname ohne Klammern ergibt ihre Adresse:

```cpp
int sum(int a, int b) { return a + b; }

// Print function address
std::cout << reinterpret_cast<void*>(sum);  // some hex address

// Declare function pointer (C-style syntax)
int (*func_ptr)(int, int) = sum;

// Call through pointer
int result = func_ptr(3, 4);          // result = 7
int result2 = (*func_ptr)(3, 4);      // equivalent, explicit dereference
```

Die Syntax `int (*name)(int, int)` liest sich so: `name` ist ein Zeiger auf eine Funktion, die zwei `int`-Werte entgegennimmt und einen `int` zurückgibt.

## auto für eine einfachere Syntax {#auto-for-simpler-syntax}

```cpp
auto* func_ptr = sum;   // compiler deduces the type
func_ptr(3, 4);         // works identically
```

## Funktionen als Parameter {#functions-as-parameters}

Die eigentliche Stärke: Verhalten als Argument übergeben.

```cpp
// Legacy: function pointer parameter
int calculate(int* arr, int size, int (*operation)(int, int)) {
    int result = arr[0];
    for (int i = 1; i < size; ++i) {
        result = operation(result, arr[i]);
    }
    return result;
}

int sum(int a, int b) { return a + b; }
int product(int a, int b) { return a * b; }

int arr[] = {1, 2, 3, 4, 5};
calculate(arr, 5, sum);      // 15
calculate(arr, 5, product);  // 120
```

## Lambdas als Inline-Funktionen {#lambdas-as-inline-functions}

Anstatt benannte Funktionen für einmalig verwendete Callbacks zu definieren, verwendet man Lambdas:

```cpp
// Lambda: anonymous function
calculate(arr, 5, [](int a, int b) { return a + b; });
calculate(arr, 5, [](int a, int b) { return a * b; });
```

Lambdas, die nichts erfassen (leeres `[]`), lassen sich implizit in Funktionszeiger im C-Stil umwandeln.

## std::function (modernes C++) {#stdfunction-modern-c}

`std::function` aus `<functional>` ist ein universeller, typgelöschter Funktionswrapper. Er funktioniert mit Funktionszeigern, Lambdas (auch solchen mit Captures) und Funktionsobjekten.

```cpp
#include <functional>

// Accepts any callable with matching signature
int calculate(int* arr, int size, const std::function<int(int, int)>& op) {
    int result = arr[0];
    for (int i = 1; i < size; ++i) {
        result = op(result, arr[i]);
    }
    return result;
}

// Works with capturing lambda (function pointer cannot do this)
int offset = 10;
calculate(arr, 5, [offset](int a, int b) { return a + b + offset; });
```

## Welches Mittel wann? {#when-to-use-which}

| Mechanismus | Overhead | Captures | Type Erasure |
|-----------|----------|----------|-------------|
| C-Funktionszeiger | Null | Nein | Nein |
| `auto` + Lambda | Null (inline) | Ja | Nein |
| `std::function` | Gering (Heap möglich) | Ja | Ja |
| Template-Parameter | Null (zur Compilezeit) | Ja | Nein |

**Standardwahl**: `std::function` für API-Grenzen, Templates für interne bzw. performancekritische Codeabschnitte. Rohe Funktionszeiger nur für die C-Interoperabilität.

```cpp
// Best for library APIs: flexible, clear interface
void register_callback(std::function<void(int)> cb);

// Best for hot paths: zero overhead, inlined
template <typename F>
void hot_loop(F&& callback) { /* ... */ }
```

## Fallstricke {#gotchas}

- **Lambdas mit Captures lassen sich nicht in rohe Funktionszeiger umwandeln.** Nur Lambdas ohne Captures (`[]`) sind konvertierbar. Für capturende Lambdas `std::function` verwenden.
- **`std::function` verursacht Overhead.** Bei großen Captures kann Heap-Allokation erfolgen, intern wird außerdem virtueller Dispatch genutzt. Für performancekritischen Code in engen Schleifen sind Template-Parameter vorzuziehen.
- **`std::function` per `const&` übergeben**, nicht per Wert, um unnötiges Kopieren des internen Callables zu vermeiden.
- **Der Aufruf einer leeren `std::function` wirft `std::bad_function_call`.** Falls die Funktion leer sein könnte, immer vorher mit `if (func)` prüfen.

## Querverweise {#cross-references}

- [[lambda-expressions]] - Lambda-Syntax, Captures, generische Lambdas
- [[templates-and-concepts]] - Templates für kostenlose Callbacks (Zero-Cost)
- [[design-patterns-cpp]] - das Strategy-Pattern verwendet intensiv Funktionsobjekte
- [[stl-algorithms]] - Algorithmen akzeptieren Callables als Parameter
