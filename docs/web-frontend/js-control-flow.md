---
title: JavaScript Control Flow
category: concepts
tags: [web-frontend, javascript, conditions, loops, operators]
---

# JavaScript Control Flow

Conditional statements, comparison operators, logical operators, and loops for controlling program execution.

## Conditional Statements

```javascript
if (condition) {
  // truthy
} else if (other) {
  // second check
} else {
  // fallback
}
```

### switch
```javascript
switch (role) {
  case "admin":  console.log("Full access"); break;
  case "editor": console.log("Edit access"); break;
  default:       console.log("Unknown");
}
```

Uses strict equality (`===`). Fall-through without `break` is sometimes intentional for grouping.

### Ternary
```javascript
const status = age >= 18 ? "adult" : "minor";
```

## Comparison Operators

```javascript
5 === "5"    // false (strict - no coercion)
5 == "5"     // true  (loose - type coercion!)
5 !== "5"    // true  (strict inequality)
```

**Always use `===` and `!==`**. Loose equality surprises:
```javascript
0 == false       // true
"" == false      // true
null == undefined // true
null == 0        // false (special case!)
NaN == NaN       // false
```

## Logical Operators

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

**`||` vs `??`**: `||` replaces ANY falsy value. `??` only replaces `null`/`undefined`. Use `??` when `0` or `""` are valid.

### Short-circuit
```javascript
isLoggedIn && showDashboard();         // Conditional execution
const name = input || "Anonymous";      // Default for falsy
const port = config.port ?? 3000;       // Default for null/undefined
```

### Optional Chaining
```javascript
const city = user?.address?.city;       // undefined if any part null/undefined
const first = arr?.[0];                  // Safe array access
const result = obj?.method?.();          // Safe method call
```

## Loops

### for
```javascript
for (let i = 0; i < 10; i++) { console.log(i); }
```

### for...of (values - arrays, strings, iterables)
```javascript
for (const fruit of ["apple", "banana"]) { console.log(fruit); }
for (const [i, v] of arr.entries()) { console.log(i, v); }
for (const char of "hello") { console.log(char); }
```

### for...in (keys - objects)
```javascript
for (const key in { name: "Alice", age: 25 }) { console.log(key); }
```

**Don't use `for...in` on arrays** - iterates all enumerable properties, order not guaranteed.

### while / do...while
```javascript
while (condition) { /* may never execute */ }
do { /* executes at least once */ } while (condition);
```

### break / continue
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

## Gotchas

- **`==` coercion traps**: `"" == false` is true, `null == 0` is false - use `===`
- **`||` replacing valid 0**: `count || 10` returns `10` when count is `0`; use `count ?? 10`
- **`for...in` on arrays**: includes inherited properties, use `for...of` instead
- **Switch without break**: fall-through to next case silently
- **Optional chaining + nullish**: `user?.name ?? "Anonymous"` combines both safely

## See Also

- [[js-variables-and-types]] - Truthy/falsy, type coercion
- [[js-arrays]] - Array iteration methods (map, filter, forEach)
- [[js-functions]] - Callbacks and higher-order functions
