---
title: JavaScript Variables and Types
category: concepts
tags: [web-frontend, javascript, types, coercion]
---

# JavaScript Variables and Types

JavaScript is dynamic and weakly-typed. Types not declared explicitly, implicit conversions happen. Engine: V8 (Chrome, Node.js), SpiderMonkey (Firefox).

## Variable Declaration

```javascript
const age = 25;         // Block-scoped, NOT reassignable (default choice)
let name = "Alice";     // Block-scoped, reassignable
var legacy = true;      // Function-scoped, hoisted (NEVER use)
```

| Feature | const | let | var |
|---------|-------|-----|-----|
| Scope | Block | Block | Function |
| Reassign | No | Yes | Yes |
| Hoisting | TDZ | TDZ | Hoisted as `undefined` |

**Rule**: `const` by default, `let` when reassignment needed, never `var`.

### Temporal Dead Zone
```javascript
console.log(x); // ReferenceError (TDZ)
let x = 5;

console.log(y); // undefined (hoisted)
var y = 5;
```

## Primitive Types (7)

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

## Reference Types

```javascript
const user = { name: "Alice", age: 25 };   // Object
const items = [1, 2, 3];                     // Array (special object)
const greet = (name) => `Hi ${name}`;        // Function
```

## typeof

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

## Operators

```javascript
5 + 3    // 8     5 ** 3   // 125
5 / 3    // 1.666 (always float)
5 % 3    // 2 (remainder)
x++      // Post-increment (returns old, then increments)
++x      // Pre-increment (increments first)
```

### Precedence (high to low)
`()` > `**` > `* / %` > `+ -` > `< > <= >=` > `== != === !==` > `&&` > `||` > `??` > `=`

## Template Literals

```javascript
const message = `Hello, ${name}! Age: ${age}`;
const html = `
  <div>
    <h1>${name}</h1>
    <p>Total: $${(19.99 * 3).toFixed(2)}</p>
  </div>
`;
```

## Type Coercion

```javascript
"5" + 3       // "53"  (+ with string = concatenation)
"5" - 3       // 2     (- coerces to number)
"5" * 2       // 10
true + 1      // 2
null + 1      // 1
undefined + 1 // NaN
```

### Explicit Conversion
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

## Falsy and Truthy

### Falsy (7 values)
```javascript
false, 0, -0, "", null, undefined, NaN
```

### Truthy (everything else)
```javascript
true, 1, "hello", " ", [], {}, function(){}
```

**Gotcha**: `[]` and `{}` are truthy! Check empty array: `arr.length === 0`. Empty object: `Object.keys(obj).length === 0`.

## Gotchas

- **`typeof null === "object"`**: historical bug, never fixed
- **`NaN !== NaN`**: NaN is not equal to anything, use `Number.isNaN()`
- **`0.1 + 0.2 !== 0.3`**: floating point, compare with `Math.abs(a - b) < Number.EPSILON`
- **`[] == false` but `[] is truthy`**: abstract equality does coercion; `==` converts `[]` to `""` to `0`
- **String `+` wins**: any `+` with a string concatenates instead of adding

## See Also

- [[js-control-flow]] - Comparisons, logical operators, loops
- [[js-strings-and-numbers]] - String/Number methods, Math
- [[js-scope-closures-this]] - Variable scoping rules
- [[typescript-fundamentals]] - Static typing for JavaScript
