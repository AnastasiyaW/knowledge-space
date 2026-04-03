---
title: TypeScript Fundamentals
category: concepts
tags: [web-frontend, typescript, types, generics, type-safety]
---

# TypeScript Fundamentals

TypeScript is a typed superset of JavaScript that compiles to plain JS. All valid JS is valid TS. Static type checking catches errors at compile time.

## Basic Types

```typescript
let name: string = "Alice";
let age: number = 25;
let active: boolean = true;
let data: null = null;
let value: undefined = undefined;

let nums: number[] = [1, 2, 3];
let strs: Array<string> = ["a", "b"];

let pair: [string, number] = ["Alice", 25];  // Tuple

enum Status { Active = "ACTIVE", Inactive = "INACTIVE" }

let anything: any = "hello";        // Disables checking (avoid!)
let value: unknown = "hello";       // Must narrow before use
function log(msg: string): void { } // No return
function fail(msg: string): never { throw new Error(msg); } // Never returns
```

## Type Aliases and Interfaces

```typescript
type User = {
  name: string;
  age: number;
  email?: string;          // Optional
  readonly id: number;     // Cannot modify after creation
};

interface User {
  name: string;
  age: number;
  email?: string;
  readonly id: number;
}

// Extension
interface Admin extends User { role: string; }
type Admin = User & { role: string; };
```

| Feature | type | interface |
|---------|------|-----------|
| Extend | `&` (intersection) | `extends` |
| Union | Yes | No |
| Declaration merging | No | Yes |
| Primitives/tuples | Yes | No |

Convention: `interface` for object shapes, `type` for unions/intersections/utilities.

## Union and Intersection

```typescript
type StringOrNumber = string | number;

// Discriminated union (most useful pattern)
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
  }
}

// Intersection
type WithTimestamp = { createdAt: Date };
type UserWithTime = User & WithTimestamp;
```

## Functions

```typescript
function add(a: number, b: number): number { return a + b; }
const add = (a: number, b: number): number => a + b;

function greet(name: string, greeting = "Hello"): string { }
function sum(...numbers: number[]): number { }

type MathFn = (a: number, b: number) => number;

// Overloads
function process(input: string): string;
function process(input: number): number;
function process(input: string | number) {
  return typeof input === "string" ? input.toUpperCase() : input * 2;
}
```

## Generics

```typescript
function identity<T>(value: T): T { return value; }
identity<string>("hello");
identity("hello");                // Inferred

// With constraint
function getLength<T extends { length: number }>(value: T): number {
  return value.length;
}

// Generic interface
interface ApiResponse<T> { data: T; status: number; error?: string; }
const r: ApiResponse<User[]> = { data: users, status: 200 };

// Default type
type Container<T = string> = { value: T };
```

## Type Narrowing

```typescript
// typeof
if (typeof value === "string") { value.toUpperCase(); }

// instanceof
if (error instanceof TypeError) { }

// in operator
if ("email" in user) { }

// Discriminated union
switch (shape.kind) { case "circle": /* TS narrows */ }

// Custom type guard
function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null && "name" in v;
}
```

## Structural Typing

Types compatible if structure matches, regardless of name:
```typescript
interface Point { x: number; y: number; }
interface Coord { x: number; y: number; }
const p: Point = { x: 1, y: 2 };
const c: Coord = p;  // OK - same structure
```

**Excess property checking** only on literal assignment:
```typescript
const p: Point = { x: 1, y: 2, z: 3 };  // Error
const obj = { x: 1, y: 2, z: 3 };
const p: Point = obj;                      // OK
```

## keyof and Indexed Access

```typescript
type UserKeys = keyof User;          // "name" | "age" | "email"
type NameType = User["name"];        // string

function getProp<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## as const

```typescript
const colors = ["red", "green", "blue"] as const;
type Color = typeof colors[number];  // "red" | "green" | "blue"
```

Makes values readonly and narrows to literal types.

## Gotchas

- **`any` disables all checking**: use `unknown` and narrow instead
- **Enum runtime cost**: enums emit JS code; use `as const` objects for zero-cost
- **Structural typing surprises**: extra properties pass through variable assignment
- **`!` non-null assertion**: `value!.prop` is unsafe - prefer narrowing
- **Array type `T[]` vs `Array<T>`**: identical, `T[]` is conventional
- **Excess property check only on literals**: passing via variable bypasses it

## See Also

- [[typescript-advanced]] - Utility types, conditional types, branded types
- [[react-components-and-jsx]] - Typing React components
- [[react-state-and-hooks]] - Typing hooks
- [[js-variables-and-types]] - JavaScript type system basics
