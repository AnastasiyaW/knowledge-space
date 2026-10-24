---
title: "Fondamentaux de TypeScript"
category: concepts
tags: [web-frontend, typescript, types, generics, type-safety]
level: 3
source_sha256: 5834854c283c8ce7d0efc319b78a26fcc15b9db5d600e9c4861ec0bb1d5ed2e7
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de TypeScript {#typescript-fundamentals}

TypeScript est un surensemble typé de JavaScript qui se compile en JS standard. Tout code JS valide est du TS valide. La vérification statique des types détecte les erreurs à la compilation.

## Types de base {#basic-types}

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

## Alias de types et interfaces {#type-aliases-and-interfaces}

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

| Fonctionnalité | type | interface |
|----------------|------|-----------|
| Extension | `&` (intersection) | `extends` |
| Union | Oui | Non |
| Fusion de déclarations | Non | Oui |
| Primitifs/tuples | Oui | Non |

Convention : `interface` pour décrire la forme des objets, `type` pour les unions, les intersections et les utilitaires.

## Union et intersection {#union-and-intersection}

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

## Fonctions {#functions}

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

## Génériques {#generics}

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

## Restriction de type (type narrowing) {#type-narrowing}

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

## Typage structurel {#structural-typing}

Deux types sont compatibles si leur structure correspond, quel que soit leur nom :
```typescript
interface Point { x: number; y: number; }
interface Coord { x: number; y: number; }
const p: Point = { x: 1, y: 2 };
const c: Coord = p;  // OK - same structure
```

**Vérification des propriétés en excès** uniquement lors d'une affectation littérale :
```typescript
const p: Point = { x: 1, y: 2, z: 3 };  // Error
const obj = { x: 1, y: 2, z: 3 };
const p: Point = obj;                      // OK
```

## keyof et accès indexé {#keyof-and-indexed-access}

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

Rend les valeurs en lecture seule et restreint leur type à des types littéraux.

## Pièges à éviter {#gotchas}

- **`any` désactive toute vérification** : utilisez `unknown` puis restreignez le type
- **Coût à l'exécution des enums** : les enums émettent du code JS ; utilisez des objets `as const` pour un coût nul
- **Surprises du typage structurel** : les propriétés supplémentaires passent lors d'une affectation via une variable
- **Assertion de non-nullité `!`** : `value!.prop` est dangereux ; préférez la restriction de type
- **Type de tableau `T[]` vs `Array<T>`** : identiques, `T[]` est la forme conventionnelle
- **Vérification des propriétés en excès uniquement sur les littéraux** : un passage par variable la contourne

## Voir aussi {#see-also}

- [[typescript-advanced|Utilitaires, types conditionnels, types nominaux (branded types)]]
- [[react-components-and-jsx|Typage des composants React]]
- [[react-state-and-hooks|Typage des hooks]]
- [[js-variables-and-types|Bases du système de types JavaScript]]
