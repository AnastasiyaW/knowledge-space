---
title: "JavaScript-Kontrollfluss"
category: concepts
tags: [web-frontend, javascript, conditions, loops, operators]
level: 3
source_sha256: c07e5451ab2556251b7d5b1c1bf9a9985f5ad6cfb96cfa5da78059615ed67a4e
translation: machine
translated_at: '2026-10-24'
---
# JavaScript-Kontrollfluss {#javascript-control-flow}

Bedingte Anweisungen, Vergleichsoperatoren, logische Operatoren und Schleifen zur Steuerung der Programmausführung.

## Bedingte Anweisungen {#conditional-statements}

```javascript
if (condition) {
  // truthy
} else if (other) {
  // second check
} else {
  // fallback
}
```

### switch {#switch}
```javascript
switch (role) {
  case "admin":  console.log("Full access"); break;
  case "editor": console.log("Edit access"); break;
  default:       console.log("Unknown");
}
```

Verwendet strikte Gleichheit (`===`). Fall-through ohne `break` wird manchmal absichtlich zum Gruppieren genutzt.

### Ternärer Operator {#ternary}
```javascript
const status = age >= 18 ? "adult" : "minor";
```

## Vergleichsoperatoren {#comparison-operators}

```javascript
5 === "5"    // false (strict - no coercion)
5 == "5"     // true  (loose - type coercion!)
5 !== "5"    // true  (strict inequality)
```

**Immer `===` und `!==` verwenden**. Lose Gleichheit führt zu Überraschungen:
```javascript
0 == false       // true
"" == false      // true
null == undefined // true
null == 0        // false (special case!)
NaN == NaN       // false
```

## Logische Operatoren {#logical-operators}

```javascript
// AND: returns first falsy, or last if all truthy
"hello" && 42       // 42
0 && "hello"        // 0

// OR: returns first truthy, or last if all falsy
false || "hello"    // "hello"
0 || "" || null     // null

// NOT
!true               // false
!!value             // Convert to boolean

// Nullish Coalescing: right side only if left is null/undefined
null ?? "default"   // "default"
0 ?? "default"      // 0 (0 is NOT null/undefined!)
"" ?? "default"     // "" (empty string is NOT null/undefined!)
```

**`||` vs. `??`**: `||` ersetzt JEDEN falsy-Wert. `??` ersetzt nur `null`/`undefined`. Verwende `??`, wenn `0` oder `""` gültige Werte sind.

### Short-Circuit-Auswertung {#short-circuit}
```javascript
isLoggedIn && showDashboard();         // Conditional execution
const name = input || "Anonymous";      // Default for falsy
const port = config.port ?? 3000;       // Default for null/undefined
```

### Optional Chaining {#optional-chaining}
```javascript
const city = user?.address?.city;       // undefined if any part null/undefined
const first = arr?.[0];                  // Safe array access
const result = obj?.method?.();          // Safe method call
```

## Schleifen {#loops}

### for {#for}
```javascript
for (let i = 0; i < 10; i++) { console.log(i); }
```

### for...of (Werte – Arrays, Strings, Iterables) {#forof-values-arrays-strings-iterables}
```javascript
for (const fruit of ["apple", "banana"]) { console.log(fruit); }
for (const [i, v] of arr.entries()) { console.log(i, v); }
for (const char of "hello") { console.log(char); }
```

### for...in (Schlüssel – Objekte) {#forin-keys-objects}
```javascript
for (const key in { name: "Alice", age: 25 }) { console.log(key); }
```

**`for...in` nicht auf Arrays verwenden** – iteriert über alle aufzählbaren Eigenschaften, die Reihenfolge ist nicht garantiert.

### while / do...while {#while-dowhile}
```javascript
while (condition) { /* may never execute */ }
do { /* executes at least once */ } while (condition);
```

### break / continue {#break-continue}
```javascript
for (let i = 0; i < 100; i++) {
  if (i === 5) break;      // Exit loop
  if (i === 2) continue;   // Skip iteration
}

// Labeled break for nested loops
outer: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (i === 1 && j === 1) break outer;
  }
}
```

## Stolperfallen {#gotchas}

- **`==`-Typumwandlungsfallen**: `"" == false` ist true, `null == 0` ist false – verwende `===`
- **`||` ersetzt gültige 0**: `count || 10` liefert `10`, wenn `count` `0` ist; verwende stattdessen `count ?? 10`
- **`for...in` auf Arrays**: schließt geerbte Eigenschaften ein, verwende stattdessen `for...of`
- **switch ohne break**: Fall-through zum nächsten case erfolgt stillschweigend
- **Optional Chaining + Nullish**: `user?.name ?? "Anonymous"` kombiniert beides sicher

## Siehe auch {#see-also}

- [[js-variables-and-types]] - Truthy/Falsy, Typumwandlung
- [[js-arrays]] - Array-Iterationsmethoden (map, filter, forEach)
- [[js-functions]] - Callbacks und Funktionen höherer Ordnung
