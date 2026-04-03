---
title: TypeScript Type System
category: typescript
tags: [typescript, types, interfaces, generics, type-guards, utility-types]
---

# TypeScript Type System

## Key Facts

- TypeScript adds **static type checking** to JavaScript; compiles to plain JS at runtime
- `interface` defines object shape (extendable with `extends`); `type` defines any type (unions, intersections, primitives)
- **Union types**: `string | number` - value can be either type; narrow with type guards
- **Intersection types**: `A & B` - value must satisfy both types (merge objects)
- **Generics**: `<T>` for type parameters; enable reusable, type-safe functions and classes
- **Literal types**: `type Direction = "up" | "down" | "left" | "right"` - exact values
- `as const` makes values deeply readonly with literal types: `[1, 2] as const` = `readonly [1, 2]`
- `unknown` is type-safe alternative to `any`; must narrow before use
- `never` type represents values that never occur (exhaustive checks, impossible states)
- TypeScript uses **structural typing** (duck typing), not nominal; compatible shapes are assignable
- Related: [[typescript-advanced-patterns]], [[react-components-and-jsx]]

## Patterns

### Interface vs Type

```typescript
// Interface - extendable, declaration merging
interface User {
  id: number;
  name: string;
  email?: string; // optional
}

interface Admin extends User {
  role: "admin";
  permissions: string[];
}

// Type - unions, intersections, mapped types
type Status = "active" | "inactive" | "banned";
type UserWithStatus = User & { status: Status };
type ID = string | number;
```

### Generics

```typescript
// Generic function
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Generic with constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic interface
interface ApiResponse<T> {
  data: T;
  error: string | null;
  status: number;
}

const response: ApiResponse<User[]> = await fetchUsers();
```

### Type Guards and Narrowing

```typescript
// typeof guard
function format(value: string | number): string {
  if (typeof value === "number") {
    return value.toFixed(2); // TS knows: number
  }
  return value.toUpperCase(); // TS knows: string
}

// Discriminated union
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function handle<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data);  // TS narrows to { success: true; data: T }
  } else {
    console.error(result.error); // TS narrows to { success: false; error: string }
  }
}

// Custom type guard
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null && "id" in value;
}
```

### Utility Types

```typescript
Partial<User>        // all properties optional
Required<User>       // all properties required
Readonly<User>       // all properties readonly
Pick<User, "id" | "name">  // subset of properties
Omit<User, "email">        // all except specified
Record<string, number>     // { [key: string]: number }
Extract<Status, "active" | "inactive">  // "active" | "inactive"
Exclude<Status, "banned">              // "active" | "inactive"
ReturnType<typeof fetchUser>           // infer return type of function
Parameters<typeof fetchUser>           // infer parameter types as tuple
```

## Gotchas

- TypeScript types are **erased at runtime**; you cannot use `typeof T` or `instanceof` on type parameters
- `interface` supports declaration merging (same name = merged); `type` does not - use `interface` for libraries/APIs
- `object` type = any non-primitive; `Object` type = almost everything; `{}` = any non-null; use specific types instead
- `!` non-null assertion (`value!.prop`) suppresses null checks but doesn't validate at runtime; prefer optional chaining + guard
- `enum` generates runtime JavaScript object; use `const enum` for inlining or union of string literals for zero runtime cost

## See Also

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [TypeScript Playground](https://www.typescriptlang.org/play)
