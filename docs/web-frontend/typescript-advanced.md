---
title: TypeScript Advanced Types
category: concepts
tags: [web-frontend, typescript, utility-types, conditional-types, type-level]
---

# TypeScript Advanced Types

TypeScript's type system is a programming language itself - types can be computed, transformed, and composed using generics, conditional types, mapped types, and recursion.

## Built-in Utility Types

```typescript
// Object
Partial<T>          // All optional
Required<T>         // All required
Readonly<T>         // All readonly
Pick<T, K>          // Subset of properties
Omit<T, K>          // Exclude properties
Record<K, V>        // Object with keys K, values V

// Union
Exclude<T, U>       // Remove types from union
Extract<T, U>       // Keep only assignable to U
NonNullable<T>      // Remove null/undefined

// Function
ReturnType<T>       // Return type
Parameters<T>       // Param types as tuple

// String
Uppercase<T>  Lowercase<T>  Capitalize<T>  Uncapitalize<T>

// Promise
Awaited<T>          // Unwrap Promise recursively
```

## Type Assertions

```typescript
const el = document.getElementById("input") as HTMLInputElement;
const value = someValue as unknown as TargetType;  // Double (rare)
```

## Branded Types

Nominally distinct types with same underlying structure:

```typescript
type USD = number & { __brand: "USD" };
type EUR = number & { __brand: "EUR" };

function usd(amount: number): USD { return amount as USD; }
const price: USD = usd(100);
// const wrong: EUR = price;  // Error!
```

Prevents accidental mixing of semantically different values.

## Custom Type Guards

```typescript
function isString(v: unknown): v is string {
  return typeof v === "string";
}

function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null && "name" in v;
}

// Assertion function
function assertString(v: unknown): asserts v is string {
  if (typeof v !== "string") throw new Error("Not string");
}
// After call, TS narrows the type
assertString(value);
value.toUpperCase();  // OK
```

## Conditional Types

```typescript
type IsString<T> = T extends string ? true : false;

// Distributive over unions
type ToArray<T> = T extends any ? T[] : never;
type R = ToArray<string | number>;  // string[] | number[]

// Prevent distribution with tuple wrapper
type ToArray<T> = [T] extends [any] ? T[] : never;

// infer: extract types
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type ElementType<T> = T extends (infer E)[] ? E : T;
type UnwrapPromise<T> = T extends Promise<infer V> ? V : T;
```

## Advanced Mapped Types

```typescript
// Remap keys
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

// Filter by value type
type StringKeys<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
```

## Recursive Types

```typescript
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type JSONValue = string | number | boolean | null | JSONValue[] | { [k: string]: JSONValue };
```

## Template Literal Types

```typescript
type Color = "red" | "blue" | "green";
type DarkColor = `dark-${Color}`;  // "dark-red" | "dark-blue" | "dark-green"
```

## Zod (Runtime Validation)

```typescript
import { z } from "zod";

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  age: z.number().int().positive(),
  email: z.string().email(),
  role: z.enum(["admin", "user"])
});

type User = z.infer<typeof UserSchema>;  // TS type from schema

const result = UserSchema.safeParse(unknownData);
if (result.success) result.data;  // Fully typed
else result.error;                 // Validation errors
```

Bridges compile-time types and runtime validation - define once, get both.

## TypeScript with React

```typescript
interface ButtonProps {
  label: string;
  variant?: "primary" | "secondary";
  onClick: () => void;
  children?: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ label, variant = "primary", onClick }) => (
  <button className={`btn-${variant}`} onClick={onClick}>{label}</button>
);

// Event types
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {};
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {};
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {};

// useState
const [user, setUser] = useState<User | null>(null);

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}
function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

## Gotchas

- **Distributive conditionals**: `T extends U ? X : Y` distributes over union T; wrap in tuple `[T]` to prevent
- **`infer` only in conditional**: can only use `infer` in the extends clause of conditional types
- **Recursive depth limit**: TS has a recursion depth limit (~50); deep types may fail
- **`as` is unsafe**: type assertions bypass checking; prefer type guards
- **Mapped type key remapping**: `as` in mapped types can filter keys by mapping to `never`

## See Also

- [[typescript-fundamentals]] - Basic types, generics, narrowing
- [[react-components-and-jsx]] - Component typing patterns
- [[react-state-and-hooks]] - Hook typing
