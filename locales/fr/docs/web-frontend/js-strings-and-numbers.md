---
title: "Chaînes et nombres en JavaScript"
category: concepts
tags: [web-frontend, javascript, strings, numbers, math, regex]
level: 3
source_sha256: 4765d8ca50e7d7f4f61cf07ce3aa2c5f4e1a93cc64394c0459ff17a23bac112a
translation: machine
translated_at: '2026-10-24'
---
# Chaînes et nombres en JavaScript {#javascript-strings-and-numbers}

Méthodes des chaînes et des nombres, objet Math et bases des expressions régulières.

## Méthodes des chaînes {#string-methods}

```javascript
const str = "Hello, World!";

// Access
str[0]                    // "H"
str.length                // 13

// Search
str.indexOf("World")      // 7 (-1 if not found)
str.includes("World")     // true
str.startsWith("Hello")   // true
str.endsWith("!")         // true

// Extract
str.slice(7, 12)          // "World" (start, end exclusive)
str.slice(-6)             // "orld!" (from end)

// Transform
str.toUpperCase()         // "HELLO, WORLD!"
str.toLowerCase()         // "hello, world!"
str.trim()                // Remove whitespace both ends
str.trimStart()           // Start only
str.padStart(20, "*")     // "*******Hello, World!"
str.repeat(2)             // "Hello, World!Hello, World!"

// Replace
str.replace("World", "JS")       // First occurrence
str.replaceAll("l", "L")         // All occurrences
str.replace(/l/g, "L")           // All via regex

// Split / Join
"a,b,c".split(",")       // ["a", "b", "c"]
"hello".split("")         // ["h", "e", "l", "l", "o"]
["a", "b"].join(", ")    // "a, b"
```

### Comparaison de chaînes {#string-comparison}
```javascript
"apple" < "banana"              // true (lexicographic)
"a".localeCompare("b")          // -1 (locale-aware)
```

### Piège des emoji {#emoji-gotcha}
```javascript
"emoji".length                   // May be > 1 (surrogate pairs)
[..."emoji"]                     // Spread correctly splits by codepoint
```

## Méthodes des nombres {#number-methods}

```javascript
Number("42")               // 42
parseInt("42px")           // 42
parseFloat("3.14em")       // 3.14
+"42"                      // 42 (unary plus)

Number.isInteger(42)       // true
Number.isFinite(42)        // true
Number.isNaN(NaN)          // true (use this, not global isNaN)
Number.isSafeInteger(42)   // true (within 2^53)

(3.14159).toFixed(2)       // "3.14" (returns string!)
(1234567).toLocaleString() // "1,234,567"

Number.MAX_SAFE_INTEGER    // 9007199254740991
```

### Virgule flottante {#floating-point}
```javascript
0.1 + 0.2 === 0.3              // false! (0.30000000000000004)
Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON  // true

// Work in integers (cents, not dollars)
const cents = 10 + 20;         // 30 (exact)
```

## Objet Math {#math-object}

```javascript
Math.round(4.5)    // 5
Math.ceil(4.1)     // 5
Math.floor(4.9)    // 4
Math.trunc(4.9)    // 4 (remove decimal)
Math.abs(-5)       // 5
Math.max(1, 5, 3)  // 5
Math.min(1, 5, 3)  // 1
Math.sqrt(16)      // 4
Math.random()      // [0, 1)

// Random integer in [min, max]
const randomInt = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;
```

## Expressions régulières {#regular-expressions}

```javascript
const regex = /pattern/flags;
// Flags: g (global), i (case-insensitive), m (multiline)

/\d+/.test("abc123")                    // true
"hello 123 world 456".match(/\d+/g)    // ["123", "456"]
"a1b2".replace(/\d/g, "")              // "ab"

// Common patterns
/^\d+$/             // Only digits
/^[a-zA-Z]+$/       // Only letters
/\S+@\S+\.\S+/     // Basic email
/^https?:\/\//      // URL prefix
```

## Pièges à éviter {#gotchas}

- **`.toFixed()` renvoie une chaîne** : `(3.14).toFixed(2)` vaut `"3.14"`, et non `3.14`
- **La fonction globale `isNaN("hello")` vaut true** : elle effectue d'abord une coercition ; utilisez `Number.isNaN()`
- **Base de `parseInt`** : `parseInt("08")` donne désormais le bon résultat, mais `parseInt("0x10")` vaut 16 ; passez toujours la base explicitement : `parseInt(str, 10)`
- **Le tri est lexicographique** : `[10, 9, 80].sort()` donne `[10, 80, 9]` ; utilisez une fonction de comparaison
- **Virgule flottante** : ne comparez jamais des flottants avec `===` ; utilisez un epsilon ou travaillez avec des entiers

## Voir aussi {#see-also}

- [[js-variables-and-types]] - Système de types, coercition
- [[js-arrays]] - Méthodes de transformation des tableaux
- [[js-objects-and-data]] - JSON, Date, données structurées
