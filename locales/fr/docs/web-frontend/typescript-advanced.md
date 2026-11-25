---
title: "TypeScript Advanced Types"
category: concepts
tags: [web-frontend, typescript, utility-types, conditional-types, type-level]
level: 4
source_sha256: f24dbdf063a477e91369e1036bc9ae54245a30a50db4fd13d850b2f41a340153
translation: machine
translated_at: '2026-10-24'
---
# Types avancés en TypeScript {#typescript-advanced-types}

Le système de types de TypeScript est lui-même un langage de programmation : les types peuvent être calculés, transformés et composés à l'aide de génériques, de types conditionnels, de types mappés et de récursion.

## Types utilitaires intégrés {#built-in-utility-types}

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

## Assertions de type {#type-assertions}

```typescript
const el = document.getElementById("input") as HTMLInputElement;
const value = someValue as unknown as TargetType;  // Double (rare)
```

## Types brandés {#branded-types}

Types nominalement distincts partageant la même structure sous-jacente :

```typescript
type USD = number & { __brand: "USD" };
type EUR = number & { __brand: "EUR" };

function usd(amount: number): USD { return amount as USD; }
const price: USD = usd(100);
// const wrong: EUR = price;  // Error!
```

Empêche le mélange accidentel de valeurs sémantiquement différentes.

## Gardes de type personnalisées {#custom-type-guards}

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

## Types conditionnels {#conditional-types}

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

## Types mappés avancés {#advanced-mapped-types}

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

## Types récursifs {#recursive-types}

```typescript
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type JSONValue = string | number | boolean | null | JSONValue[] | { [k: string]: JSONValue };
```

## Types littéraux de gabarit {#template-literal-types}

```typescript
type Color = "red" | "blue" | "green";
type DarkColor = `dark-${Color}`;  // "dark-red" | "dark-blue" | "dark-green"
```

## Zod (validation à l'exécution) {#zod-runtime-validation}

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

Fait le pont entre les types à la compilation et la validation à l'exécution : on définit une seule fois, on obtient les deux.

## TypeScript avec React {#typescript-with-react}

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

## Pièges courants {#gotchas}

- **Conditionnels distributifs** : `T extends U ? X : Y` se distribue sur l'union T ; l'envelopper dans un tuple `[T]` permet de l'éviter
- **`infer` uniquement dans un conditionnel** : `infer` ne peut être utilisé que dans la clause `extends` des types conditionnels
- **Limite de profondeur récursive** : TS impose une limite de récursion (~50) ; les types profonds peuvent échouer
- **`as` est non sûr** : les assertions de type contournent la vérification ; préférer les gardes de type
- **Remappage de clés dans les types mappés** : `as` dans un type mappé peut filtrer des clés en les associant à `never`

## Voir aussi {#see-also}

- [[typescript-fundamentals]] - Types de base, génériques, narrowing
- [[react-components-and-jsx]] - Patrons de typage des composants
- [[react-state-and-hooks]] - Typage des hooks
