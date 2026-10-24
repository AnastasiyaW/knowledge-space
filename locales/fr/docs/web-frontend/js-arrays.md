---
title: "Tableaux JavaScript"
category: concepts
tags: [web-frontend, javascript, arrays, functional-programming]
level: 3
source_sha256: fe69957c29fd835f8da6674e94a385b6ad9373874c69cae51b88ad6e1d00d341
translation: machine
translated_at: '2026-10-24'
---
# Tableaux JavaScript {#javascript-arrays}

Les tableaux sont des collections ordonnées dotées de méthodes intégrées puissantes pour rechercher, transformer et réduire des données.

## Création et accès {#creating-and-accessing}

```javascript
const arr = [1, 2, 3];
const arr = Array.from("hello");           // ['h','e','l','l','o']
const arr = Array.from({length: 5}, (_, i) => i);  // [0,1,2,3,4]
const arr = [...otherArray];               // Spread copy

arr[0]            // First
arr.at(-1)        // Last (modern)
arr.at(-2)        // Second from end
```

## Méthodes mutantes (modifient le tableau d'origine) {#mutating-methods-change-original}

```javascript
arr.push("e");          // Add to end
arr.pop();              // Remove from end
arr.unshift("z");       // Add to beginning
arr.shift();            // Remove from beginning

arr.splice(1, 2);           // Remove 2 at index 1
arr.splice(1, 0, "x", "y"); // Insert at index 1
arr.splice(1, 1, "x");      // Replace at index 1

arr.reverse();
arr.sort((a, b) => a - b);         // Numeric ascending
arr.sort((a, b) => b - a);         // Numeric descending
arr.sort((a, b) => a.localeCompare(b));  // String (locale)
arr.fill(0, 1, 3);                 // Fill indexes 1-2
```

**Piège de sort()** : le tri par défaut est lexicographique ! `[10, 9, 80].sort()` donne `[10, 80, 9]`. Toujours passer un comparateur pour les nombres.

## Méthodes non mutantes {#non-mutating-methods}

### Découpage et combinaison {#slicing-and-combining}
```javascript
arr.slice(1, 3)         // New array [1..2]
arr.slice(-2)           // Last 2
arr.concat([4, 5])      // New merged array
[...arr, 4, 5]          // Spread concat
```

### Recherche {#searching}
```javascript
arr.indexOf("b")          // First index (-1 if not found)
arr.includes("b")         // true/false
arr.find(x => x > 3)     // First matching element
arr.findIndex(x => x > 3) // First matching index
arr.findLast(x => x > 3)  // Last matching (ES2023)
arr.some(x => x > 3)     // Any match?
arr.every(x => x > 0)    // All match?
```

### Transformation (cœur fonctionnel) {#transformation-functional-core}

```javascript
// map: transform each element
[1, 2, 3].map(x => x * 2)            // [2, 4, 6]

// filter: keep matching
[1, 2, 3, 4, 5].filter(x => x > 3)   // [4, 5]

// reduce: accumulate to single value
[1, 2, 3, 4].reduce((sum, x) => sum + x, 0)  // 10

// flat: flatten nested
[[1, 2], [3, 4]].flat()              // [1, 2, 3, 4]
[1, [2, [3]]].flat(Infinity)         // [1, 2, 3]

// flatMap: map + flat(1)
["hello world", "foo"].flatMap(s => s.split(" "))  // ["hello","world","foo"]

// forEach: side-effect iteration (no return value)
arr.forEach((el, i) => console.log(i, el));
```

### Exemples avec reduce {#reduce-examples}
```javascript
// Max value
const max = arr.reduce((a, b) => Math.max(a, b));

// Group by category
const grouped = items.reduce((groups, item) => {
  (groups[item.category] ??= []).push(item);
  return groups;
}, {});
```

## Déstructuration {#destructuring}

```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
const [a, b] = [1, 2, 3];          // Skip: a=1, b=3
const [x = 0, y = 0] = [10];          // Defaults: x=10, y=0
[a, b] = [b, a];                       // Swap
```

## Spread et rest {#spread-and-rest}

```javascript
// Spread: expand
const merged = [...arr1, ...arr2];
Math.max(...numbers);

// Rest: collect
function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }
const [head, ...tail] = [1, 2, 3];
```

## Chaînage de méthodes {#method-chaining}

```javascript
const result = users
  .filter(u => u.age >= 18)
  .map(u => u.name)
  .sort()
  .join(", ");
```

Chaque méthode renvoie un nouveau tableau, ce qui permet d'enchaîner les appels. Motif très courant.

## Conversion depuis des objets semblables à des tableaux {#array-like-conversion}

```javascript
Array.from(nodeList);    // NodeList -> Array
[...nodeList];           // Spread works too
```

## Pièges courants {#gotchas}

- **sort() est lexicographique par défaut** : toujours passer un comparateur pour les nombres
- **splice modifie le tableau, slice non** : facile à confondre
- **`const arr = []` reste mutable** : `const` empêche la réaffectation, pas la mutation
- **`map`/`filter` créent de nouveaux tableaux** : ne pas utiliser `map` pour les effets de bord (utiliser `forEach`)
- **Cases vides** : `new Array(5)` crée un tableau creux ; `Array.from({length: 5})` le remplit avec `undefined`
- **`indexOf` utilise `===`** : ne peut pas trouver `NaN` ; utiliser `findIndex(x => Number.isNaN(x))`

## Voir aussi {#see-also}

- [[js-objects-and-data]] - Méthodes des objets, déstructuration
- [[js-functions]] - Fonctions d'ordre supérieur, callbacks
- [[js-strings-and-numbers]] - Découpage et jointure de chaînes (split/join)
- [[typescript-fundamentals]] - Tableaux typés
