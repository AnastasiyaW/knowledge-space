---
title: JavaScript Array Methods
category: javascript
tags: [javascript, array, map, filter, reduce, spread, iteration]
---

# JavaScript Array Methods

## Key Facts

- `map(fn)` - returns new array with `fn` applied to each element; does NOT mutate original
- `filter(fn)` - returns new array with elements where `fn` returns truthy
- `reduce(fn, initial)` - accumulates array to single value; `fn(accumulator, current, index, array)`
- `find(fn)` / `findIndex(fn)` - first match or -1; `includes(value)` for simple existence check
- `forEach(fn)` - side effects only, returns `undefined`; cannot `break` (use `for...of` instead)
- `some(fn)` - true if ANY element passes; `every(fn)` - true if ALL pass (short-circuit)
- `flat(depth)` - flattens nested arrays; `flatMap(fn)` = `map` + `flat(1)`
- `sort(fn)` - **mutates** original array; `toSorted(fn)` (ES2023) returns new sorted array
- `structuredClone(arr)` for deep copy; `[...arr]` / `Array.from(arr)` for shallow copy
- Related: [[javascript-fundamentals]], [[javascript-async-and-promises]]

## Patterns

### Chain: Filter + Map + Reduce

```javascript
const total = orders
  .filter(o => o.status === "completed")
  .map(o => o.amount)
  .reduce((sum, amount) => sum + amount, 0);
```

### Group By (Object.groupBy - ES2024)

```javascript
// Modern
const grouped = Object.groupBy(users, user => user.role);
// { admin: [...], editor: [...], viewer: [...] }

// Classic fallback
const grouped = users.reduce((acc, user) => {
  (acc[user.role] ??= []).push(user);
  return acc;
}, {});
```

### Array Creation Patterns

```javascript
// Range [0, 1, 2, ..., n-1]
const range = Array.from({ length: n }, (_, i) => i);

// Fill with value
const zeros = new Array(5).fill(0);

// Unique values
const unique = [...new Set(arr)];

// Chunk array
function chunk(arr, size) {
  return Array.from(
    { length: Math.ceil(arr.length / size) },
    (_, i) => arr.slice(i * size, i * size + size)
  );
}
```

### Non-Mutating Alternatives (ES2023)

```javascript
const sorted = arr.toSorted((a, b) => a - b);     // new sorted array
const reversed = arr.toReversed();                  // new reversed array
const spliced = arr.toSpliced(1, 1, "new");        // new array with splice
const changed = arr.with(2, "replacement");         // new array, index 2 replaced
```

### Searching and Testing

```javascript
arr.includes(value);           // boolean, strict equality
arr.indexOf(value);            // index or -1
arr.find(x => x.id === 42);   // first matching element or undefined
arr.findLast(x => x > 5);     // last matching (ES2023)
arr.some(x => x > 10);        // true if any > 10
arr.every(x => x > 0);        // true if all > 0
```

## Gotchas

- `sort()` without comparator sorts as strings: `[10, 2, 1].sort()` = `[1, 10, 2]`; always pass `(a, b) => a - b` for numbers
- `map`/`filter`/`reduce` return NEW arrays; `sort`/`reverse`/`splice` MUTATE in place
- `Array(5)` creates sparse array with 5 empty slots; `Array(5).fill(0)` or `Array.from({length: 5})` for actual elements
- `reduce` without initial value uses first element as accumulator; throws on empty array - always provide initial value
- `delete arr[i]` creates a sparse slot (not a real deletion); use `splice(i, 1)` or `toSpliced()`

## See Also

- [MDN: Array methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)
- [MDN: Object.groupBy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy)
