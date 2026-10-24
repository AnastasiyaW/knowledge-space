---
title: "TypeScript-Grundlagen"
category: concepts
tags: [web-frontend, typescript, types, generics, type-safety]
level: 3
source_sha256: 5834854c283c8ce7d0efc319b78a26fcc15b9db5d600e9c4861ec0bb1d5ed2e7
translation: machine
translated_at: '2026-10-24'
---
# TypeScript-Grundlagen {#typescript-fundamentals}

TypeScript ist eine typisierte Obermenge von JavaScript, die zu reinem JS kompiliert. Jedes gültige JS ist auch gültiges TS. Die statische Typprüfung erkennt Fehler bereits zur Kompilierzeit.

## Grundlegende Typen {#basic-types}

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

## Type-Aliase und Interfaces {#type-aliases-and-interfaces}

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

| Merkmal | type | interface |
|---------|------|-----------|
| Erweitern | `&` (Schnittmenge) | `extends` |
| Union | Ja | Nein |
| Deklarations-Merging | Nein | Ja |
| Primitive/Tupel | Ja | Nein |

Konvention: `interface` für Objektstrukturen, `type` für Unions, Schnittmengen und Utility-Typen.

## Union und Schnittmenge {#union-and-intersection}

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

## Funktionen {#functions}

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

## Generics {#generics}

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

## Typeingrenzung (Type Narrowing) {#type-narrowing}

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

## Strukturelle Typisierung {#structural-typing}

Typen sind kompatibel, wenn die Struktur übereinstimmt, unabhängig vom Namen:
```typescript
interface Point { x: number; y: number; }
interface Coord { x: number; y: number; }
const p: Point = { x: 1, y: 2 };
const c: Coord = p;  // OK - same structure
```

**Prüfung auf überzählige Eigenschaften** (Excess Property Checking) gilt nur bei literalen Zuweisungen:
```typescript
const p: Point = { x: 1, y: 2, z: 3 };  // Error
const obj = { x: 1, y: 2, z: 3 };
const p: Point = obj;                      // OK
```

## keyof und indizierter Zugriff {#keyof-and-indexed-access}

```typescript
type UserKeys = keyof User;          // "name" | "age" | "email"
type NameType = User["name"];        // string

function getProp<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## as const {#as-const}

```typescript
const colors = ["red", "green", "blue"] as const;
type Color = typeof colors[number];  // "red" | "green" | "blue"
```

Macht Werte readonly und verengt sie auf Literaltypen.

## Stolperfallen {#gotchas}

- **`any` deaktiviert jede Prüfung**: stattdessen `unknown` verwenden und per Narrowing eingrenzen
- **Laufzeitkosten von Enums**: Enums erzeugen JS-Code; für kostenfreie Alternativen `as const`-Objekte verwenden
- **Überraschungen durch strukturelle Typisierung**: zusätzliche Eigenschaften passieren die Zuweisung über eine Variable
- **`!` Non-Null-Assertion**: `value!.prop` ist unsicher – besser eingrenzen
- **Array-Typ `T[]` vs. `Array<T>`**: identisch, `T[]` ist üblich
- **Excess-Property-Prüfung nur bei Literalen**: Übergabe über eine Variable umgeht sie

## Siehe auch {#see-also}

- [[typescript-advanced]] - Utility-Typen, bedingte Typen, Branded Types
- [[react-components-and-jsx]] - Typisierung von React-Komponenten
- [[react-state-and-hooks]] - Typisierung von Hooks
- [[js-variables-and-types]] - Grundlagen des JavaScript-Typsystems
