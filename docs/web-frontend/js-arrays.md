---
title: JavaScript Arrays
category: concepts
tags: [web-frontend, javascript, arrays, functional-programming]
---

# JavaScript Arrays

Arrays are ordered collections with powerful built-in methods for searching, transforming, and reducing data.

## Creating and Accessing

```javascript
const arr = [1, 2, 3];
const arr = Array.from("hello");           // ['h','e','l','l','o']
const arr = Array.from({length: 5}, (_, i) => i);  // [0,1,2,3,4]
const arr = [...otherArray];               // Spread copy

arr[0]            // First
arr.at(-1)        // Last (modern)
arr.at(-2)        // Second from end
```

## Mutating Methods (change original)

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

**sort() gotcha**: default sort is lexicographic! `[10, 9, 80].sort()` = `[10, 80, 9]`. Always pass comparator for numbers.

## Non-Mutating Methods

### Slicing and Combining
```javascript
arr.slice(1, 3)         // New array [1..2]
arr.slice(-2)           // Last 2
arr.concat([4, 5])      // New merged array
[...arr, 4, 5]          // Spread concat
```

### Searching
```javascript
arr.indexOf("b")          // First index (-1 if not found)
arr.includes("b")         // true/false
arr.find(x => x > 3)     // First matching element
arr.findIndex(x => x > 3) // First matching index
arr.findLast(x => x > 3)  // Last matching (ES2023)
arr.some(x => x > 3)     // Any match?
arr.every(x => x > 0)    // All match?
```

### Transformation (Functional Core)

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

### reduce Examples
```javascript
// Max value
const max = arr.reduce((a, b) => Math.max(a, b));

// Group by category
const grouped = items.reduce((groups, item) => {
  (groups[item.category] ??= []).push(item);
  return groups;
}, {});
```

## Destructuring

```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
const [a, b] = [1, 2, 3];          // Skip: a=1, b=3
const [x = 0, y = 0] = [10];          // Defaults: x=10, y=0
[a, b] = [b, a];                       // Swap
```

## Spread and Rest

```javascript
// Spread: expand
const merged = [...arr1, ...arr2];
Math.max(...numbers);

// Rest: collect
function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }
const [head, ...tail] = [1, 2, 3];
```

## Method Chaining

```javascript
const result = users
  .filter(u => u.age >= 18)
  .map(u => u.name)
  .sort()
  .join(", ");
```

Each method returns a new array, enabling chains. Very common pattern.

## Array-like Conversion

```javascript
Array.from(nodeList);    // NodeList -> Array
[...nodeList];           // Spread works too
```

## Gotchas

- **sort() is lexicographic by default**: always pass comparator for numbers
- **splice mutates, slice doesn't**: easy to confuse
- **`const arr = []` is mutable**: `const` prevents reassignment, not mutation
- **`map`/`filter` create new arrays**: don't use `map` for side effects (use `forEach`)
- **Empty slots**: `new Array(5)` creates sparse array; `Array.from({length: 5})` fills with `undefined`
- **`indexOf` uses `===`**: can't find `NaN`; use `findIndex(x => Number.isNaN(x))`

## See Also

- [[js-objects-and-data]] - Object methods, destructuring
- [[js-functions]] - Higher-order functions, callbacks
- [[js-strings-and-numbers]] - String split/join
- [[typescript-fundamentals]] - Typed arrays
