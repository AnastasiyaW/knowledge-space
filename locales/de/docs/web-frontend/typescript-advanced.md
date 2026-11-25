---
title: "TypeScript fortgeschrittene Typen"
category: concepts
tags: [web-frontend, typescript, utility-types, conditional-types, type-level]
level: 4
source_sha256: f24dbdf063a477e91369e1036bc9ae54245a30a50db4fd13d850b2f41a340153
translation: machine
translated_at: '2026-10-24'
---
# TypeScript fortgeschrittene Typen {#typescript-advanced-types}

Das Typsystem von TypeScript ist selbst eine Programmiersprache: Typen können mit Generics, bedingten Typen, Mapped Types und Rekursion berechnet, transformiert und zusammengesetzt werden.

## Eingebaute Utility-Typen {#built-in-utility-types}

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

## Typ-Assertions {#type-assertions}

```typescript
const el = document.getElementById("input") as HTMLInputElement;
const value = someValue as unknown as TargetType;  // Double (rare)
```

## Branded Types {#branded-types}

Nominell unterschiedliche Typen mit gleicher zugrunde liegender Struktur:

```typescript
type USD = number & { __brand: "USD" };
type EUR = number & { __brand: "EUR" };

function usd(amount: number): USD { return amount as USD; }
const price: USD = usd(100);
// const wrong: EUR = price;  // Error!
```

Verhindert die versehentliche Vermischung semantisch unterschiedlicher Werte.

## Eigene Type Guards {#custom-type-guards}

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

## Bedingte Typen {#conditional-types}

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

## Fortgeschrittene Mapped Types {#advanced-mapped-types}

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

## Rekursive Typen {#recursive-types}

```typescript
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type JSONValue = string | number | boolean | null | JSONValue[] | { [k: string]: JSONValue };
```

## Template Literal Types {#template-literal-types}

```typescript
type Color = "red" | "blue" | "green";
type DarkColor = `dark-${Color}`;  // "dark-red" | "dark-blue" | "dark-green"
```

## Zod (Laufzeitvalidierung) {#zod-runtime-validation}

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

Verbindet Typen zur Compile-Zeit mit Validierung zur Laufzeit: einmal definieren, beides erhalten.

## TypeScript mit React {#typescript-with-react}

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

## Fallstricke {#gotchas}

- **Distributive Conditionals**: `T extends U ? X : Y` verteilt sich über den Union-Typ T; mit einem Tupel `[T]` lässt sich das verhindern
- **`infer` nur in Conditionals**: `infer` kann nur in der extends-Klausel bedingter Typen verwendet werden
- **Tiefenlimit für Rekursion**: TS hat ein Rekursionslimit (etwa 50); tief verschachtelte Typen können fehlschlagen
- **`as` ist unsicher**: Typ-Assertions umgehen die Prüfung; Type Guards sind vorzuziehen
- **Key Remapping in Mapped Types**: `as` in Mapped Types kann Schlüssel herausfiltern, indem sie auf `never` abgebildet werden

## Siehe auch {#see-also}

- [[typescript-fundamentals]] - Grundlegende Typen, Generics, Narrowing
- [[react-components-and-jsx]] - Muster zur Typisierung von Komponenten
- [[react-state-and-hooks]] - Typisierung von Hooks
