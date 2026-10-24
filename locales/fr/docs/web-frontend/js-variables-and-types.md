---
title: "Variables et types en JavaScript"
category: concepts
tags: [web-frontend, javascript, types, coercion]
level: 3
source_sha256: 99e1ca517052c4ddb11f4ca11fa4e0adca4ee6bd07fab02b10e0aa22bf4bf116
translation: machine
translated_at: '2026-10-24'
---
# Variables et types en JavaScript {#javascript-variables-and-types}

JavaScript est dynamique et faiblement typé. Les types ne sont pas déclarés explicitement, et des conversions implicites ont lieu. Moteur : V8 (Chrome, Node.js), SpiderMonkey (Firefox).

## Déclaration des variables {#variable-declaration}

```javascript
const age = 25;         // Block-scoped, NOT reassignable (default choice)
let name = "Alice";     // Block-scoped, reassignable
var legacy = true;      // Function-scoped, hoisted (NEVER use)
```

| Caractéristique | const | let | var |
|---------|-------|-----|-----|
| Portée | Bloc | Bloc | Fonction |
| Réassignation | Non | Oui | Oui |
| Hoisting | TDZ | TDZ | Hissée avec `undefined` |

**Règle** : `const` par défaut, `let` lorsqu'une réassignation est nécessaire, jamais `var`.

### Zone morte temporelle {#temporal-dead-zone}
```javascript
console.log(x); // ReferenceError (TDZ)
let x = 5;

console.log(y); // undefined (hoisted)
var y = 5;
```

## Types primitifs (7) {#primitive-types-7}

```javascript
const str = "Alice";                    // String
const tmpl = `Hello, ${str}!`;         // Template literal
const num = 42;                         // Number (int and float share type)
const price = 19.99;
const big = 9007199254740991n;          // BigInt
const active = true;                    // Boolean
let x;                                  // undefined
const data = null;                      // null (intentional absence)
const id = Symbol('unique');            // Symbol
```

## Types référence {#reference-types}

```javascript
const user = { name: "Alice", age: 25 };   // Object
const items = [1, 2, 3];                     // Array (special object)
const greet = (name) => `Hi ${name}`;        // Function
```

## typeof {#typeof}

```javascript
typeof "hello"      // "string"
typeof 42           // "number"
typeof true         // "boolean"
typeof undefined    // "undefined"
typeof null         // "object"    // Historical bug!
typeof {}           // "object"
typeof []           // "object"    // Use Array.isArray()
typeof function(){} // "function"
```

## Opérateurs {#operators}

```javascript
5 + 3    // 8     5 ** 3   // 125
5 / 3    // 1.666 (always float)
5 % 3    // 2 (remainder)
x++      // Post-increment (returns old, then increments)
++x      // Pre-increment (increments first)
```

### Priorité (de la plus haute à la plus basse) {#precedence-high-to-low}
`()` > `**` > `* / %` > `+ -` > `< > <= >=` > `== != === !==` > `&&` > `||` > `??` > `=`

## Template literals {#template-literals}

```javascript
const message = `Hello, ${name}! Age: ${age}`;
const html = `
  <div>
    <h1>${name}</h1>
    <p>Total: $${(19.99 * 3).toFixed(2)}</p>
  </div>
`;
```

## Coercition de types {#type-coercion}

```javascript
"5" + 3       // "53"  (+ with string = concatenation)
"5" - 3       // 2     (- coerces to number)
"5" * 2       // 10
true + 1      // 2
null + 1      // 1
undefined + 1 // NaN
```

### Conversion explicite {#explicit-conversion}
```javascript
Number("42")         // 42
Number("")           // 0
Number(null)         // 0
Number(undefined)    // NaN
String(42)           // "42"
Boolean(0)           // false
parseInt("42px")     // 42 (parses until non-digit)
parseFloat("3.14em") // 3.14
+"42"                // 42 (unary plus shortcut)
```

## Falsy et truthy {#falsy-and-truthy}

### Falsy (7 valeurs) {#falsy-7-values}
```javascript
false, 0, -0, "", null, undefined, NaN
```

### Truthy (tout le reste) {#truthy-everything-else}
```javascript
true, 1, "hello", " ", [], {}, function(){}
```

**Piège** : `[]` et `{}` sont truthy ! Pour vérifier un tableau vide : `arr.length === 0`. Pour un objet vide : `Object.keys(obj).length === 0`.

## Pièges {#gotchas}

- **`typeof null === "object"`** : bug historique, jamais corrigé
- **`NaN !== NaN`** : NaN n'est égal à aucune valeur, utiliser `Number.isNaN()`
- **`0.1 + 0.2 !== 0.3`** : virgule flottante, comparer avec `Math.abs(a - b) < Number.EPSILON`
- **`[] == false` mais `[] est truthy`** : l'égalité abstraite effectue une coercition ; `==` convertit `[]` en `""` puis en `0`
- **Le `+` avec une chaîne l'emporte** : tout `+` impliquant une chaîne effectue une concaténation au lieu d'une addition

## Voir aussi {#see-also}

- [[js-control-flow]] - Comparaisons, opérateurs logiques, boucles
- [[js-strings-and-numbers]] - Méthodes de String/Number, Math
- [[js-scope-closures-this]] - Règles de portée des variables
- [[typescript-fundamentals]] - Typage statique pour JavaScript
