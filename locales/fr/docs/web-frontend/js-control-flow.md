---
title: "Structures de contrôle en JavaScript"
category: concepts
tags: [web-frontend, javascript, conditions, loops, operators]
level: 3
source_sha256: c07e5451ab2556251b7d5b1c1bf9a9985f5ad6cfb96cfa5da78059615ed67a4e
translation: machine
translated_at: '2026-10-24'
---
# Structures de contrôle en JavaScript {#javascript-control-flow}

Instructions conditionnelles, opérateurs de comparaison, opérateurs logiques et boucles pour contrôler l'exécution d'un programme.

## Instructions conditionnelles {#conditional-statements}

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

Utilise l'égalité stricte (`===`). Le fall-through sans `break` est parfois intentionnel pour regrouper des cas.

### Opérateur ternaire {#ternary}
```javascript
const status = age >= 18 ? "adult" : "minor";
```

## Opérateurs de comparaison {#comparison-operators}

```javascript
5 === "5"    // false (strict - no coercion)
5 == "5"     // true  (loose - type coercion!)
5 !== "5"    // true  (strict inequality)
```

**Utilisez toujours `===` et `!==`**. L'égalité non stricte réserve des surprises :
```javascript
0 == false       // true
"" == false      // true
null == undefined // true
null == 0        // false (special case!)
NaN == NaN       // false
```

## Opérateurs logiques {#logical-operators}

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

**`||` vs `??`** : `||` remplace TOUTE valeur falsy. `??` ne remplace que `null`/`undefined`. Utilisez `??` lorsque `0` ou `""` sont des valeurs valides.

### Court-circuit {#short-circuit}
```javascript
isLoggedIn && showDashboard();         // Conditional execution
const name = input || "Anonymous";      // Default for falsy
const port = config.port ?? 3000;       // Default for null/undefined
```

### Chaînage optionnel {#optional-chaining}
```javascript
const city = user?.address?.city;       // undefined if any part null/undefined
const first = arr?.[0];                  // Safe array access
const result = obj?.method?.();          // Safe method call
```

## Boucles {#loops}

### for {#for}
```javascript
for (let i = 0; i < 10; i++) { console.log(i); }
```

### for...of (valeurs - tableaux, chaînes, itérables) {#forof-values-arrays-strings-iterables}
```javascript
for (const fruit of ["apple", "banana"]) { console.log(fruit); }
for (const [i, v] of arr.entries()) { console.log(i, v); }
for (const char of "hello") { console.log(char); }
```

### for...in (clés - objets) {#forin-keys-objects}
```javascript
for (const key in { name: "Alice", age: 25 }) { console.log(key); }
```

**N'utilisez pas `for...in` sur les tableaux** : il parcourt toutes les propriétés énumérables, et l'ordre n'est pas garanti.

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

## Pièges courants {#gotchas}

- **Pièges de la coercition avec `==`** : `"" == false` vaut true, `null == 0` vaut false - utilisez `===`
- **`||` remplaçant un `0` valide** : `count || 10` renvoie `10` lorsque count vaut `0` ; utilisez `count ?? 10`
- **`for...in` sur les tableaux** : inclut les propriétés héritées, utilisez plutôt `for...of`
- **Switch sans break** : le passage au cas suivant se fait silencieusement
- **Chaînage optionnel + nullish** : `user?.name ?? "Anonymous"` combine les deux de manière sûre

## Voir aussi {#see-also}

- [[js-variables-and-types]] - Truthy/falsy, coercition de types
- [[js-arrays]] - Méthodes d'itération sur les tableaux (map, filter, forEach)
- [[js-functions]] - Callbacks et fonctions d'ordre supérieur
