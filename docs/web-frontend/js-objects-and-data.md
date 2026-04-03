---
title: JavaScript Objects and Data
category: concepts
tags: [web-frontend, javascript, objects, json, date]
---

# JavaScript Objects and Data

Objects are key-value collections. Along with JSON, Date, and Symbol, they form JavaScript's data handling foundation.

## Creating and Accessing Objects

```javascript
const user = {
  name: "Alice",
  age: 25,
  skills: ["JS", "CSS"],
  address: { city: "New York" },
  greet() { return `Hi, I'm ${this.name}`; }
};

user.name              // "Alice" (dot notation)
user["name"]           // "Alice" (bracket - for dynamic keys)
user?.address?.city    // "New York" (safe with optional chaining)
```

## Modifying

```javascript
user.email = "a@b.com";    // Add
user.age = 26;              // Update
delete user.age;            // Delete

const obj = { a: 1 };
obj.a = 2;    // OK (property mutable)
obj = {};     // Error (const prevents reassignment)
```

## Shorthand and Computed Keys

```javascript
const name = "Alice", age = 25;
const user = { name, age };                  // Shorthand
const key = "email";
const obj = { [key]: "a@b.com" };           // Computed key
const obj = { [`${key}Count`]: 5 };         // { emailCount: 5 }
```

## Destructuring

```javascript
const { name, age } = user;
const { name: userName } = user;            // Rename
const { role = "user" } = user;             // Default
const { address: { city } } = user;         // Nested

function greet({ name, age = 0 }) { }      // In parameters
```

## Spread

```javascript
const copy = { ...user };                    // Shallow copy
const merged = { ...defaults, ...overrides }; // Merge (right wins)
const updated = { ...user, age: 26 };       // Copy + update
```

**Shallow only**: nested objects are still references. Use `structuredClone(obj)` for deep copy.

## Object Static Methods

```javascript
Object.keys(user)       // ["name", "age", ...]
Object.values(user)     // ["Alice", 25, ...]
Object.entries(user)    // [["name","Alice"], ["age",25], ...]

for (const [key, value] of Object.entries(user)) {
  console.log(`${key}: ${value}`);
}

Object.assign(target, source)     // Merge (mutates target)
Object.freeze(obj)                // Shallow immutable
Object.seal(obj)                  // Can modify, can't add/delete

"name" in user                    // true (includes inherited)
Object.hasOwn(user, "name")      // true (own only, ES2022)
```

## null vs undefined

```javascript
undefined  // Not assigned, missing param, missing property
null       // Intentional "no value"

typeof undefined  // "undefined"
typeof null       // "object" (historical bug)
null == undefined  // true (loose)
null === undefined // false (strict)
```

Convention: use `null` for explicit "no value", `undefined` = "not yet assigned".

## JSON

```javascript
JSON.stringify(user)              // Object -> JSON string
JSON.stringify(user, null, 2)     // Pretty-printed
JSON.parse('{"name":"Alice"}')    // JSON string -> Object

// Deep clone (simple objects only)
const clone = JSON.parse(JSON.stringify(original));
// Modern deep clone (handles more types)
const clone = structuredClone(original);
```

**JSON rules**: double-quoted keys, no functions/undefined/Symbol, no trailing commas, no comments.

## Date

```javascript
const now = new Date();
const d = new Date(2024, 0, 15);        // Jan 15 (month is 0-indexed!)
const d = new Date("2024-01-15");

now.getFullYear()    // 2024
now.getMonth()       // 0-11 (January = 0!)
now.getDate()        // 1-31
now.getDay()         // 0-6 (Sunday = 0!)
now.getTime()        // Milliseconds since epoch

now.toLocaleDateString()  // Locale-dependent
now.toISOString()         // "2024-01-15T00:00:00.000Z"
Date.now()                // Timestamp (no object)
```

## Symbol

```javascript
const id = Symbol("description");
Symbol("x") === Symbol("x")  // false (always unique)

const SECRET = Symbol("secret");
const obj = { [SECRET]: "hidden", name: "visible" };
Object.keys(obj)   // ["name"] (Symbols not enumerable)
```

Used for truly private properties and avoiding name collisions.

## Gotchas

- **Month is 0-indexed**: January = 0, December = 11 (most common Date bug)
- **Object spread is shallow**: nested objects/arrays are still shared references
- **`typeof null === "object"`**: historical bug, never fixed
- **`JSON.stringify` drops functions**: and undefined, Symbol
- **`for...in` includes inherited**: use `Object.keys()` or `Object.hasOwn()`
- **Object comparison by reference**: `{} === {}` is `false`

## See Also

- [[js-arrays]] - Array methods, destructuring, spread
- [[js-dom-and-events]] - localStorage (JSON serialization)
- [[js-async-and-fetch]] - Fetch returns JSON
- [[typescript-fundamentals]] - Type interfaces for objects
