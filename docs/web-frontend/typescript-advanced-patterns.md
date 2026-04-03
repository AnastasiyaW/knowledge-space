---
title: TypeScript Advanced Patterns
category: typescript
tags: [typescript, mapped-types, conditional-types, template-literals, infer, branded-types]
---

# TypeScript Advanced Patterns

## Key Facts

- **Mapped types** transform properties of existing types: `{ [K in keyof T]: ... }`
- **Conditional types**: `T extends U ? X : Y` - type-level if/else
- **`infer`** keyword extracts types within conditional types: `T extends Promise<infer U> ? U : T`
- **Template literal types**: `` `on${Capitalize<string>}` `` creates typed event names
- **Index access types**: `T["key"]` or `T[number]` to extract element type from array
- **Branded types** use intersection with unique symbol to prevent type confusion (e.g., UserId vs PostId)
- `satisfies` operator (TS 5.0+) validates type without widening: `config satisfies Config` keeps literal types
- `const` type parameters (TS 5.0+): `function foo<const T>(arg: T)` infers literals instead of widening
- **Variadic tuple types**: `[...T, string]` for typed spread in tuples
- Related: [[typescript-type-system]], [[react-components-and-jsx]]

## Patterns

### Mapped Types

```typescript
// Make all properties nullable
type Nullable<T> = { [K in keyof T]: T[K] | null };

// Deep readonly
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// Create getters
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
// Getters<{ name: string }> = { getName: () => string }
```

### Conditional Types

```typescript
// Unwrap Promise
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
// Awaited<Promise<Promise<string>>> = string

// Extract function return type
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

// Filter union members
type OnlyStrings<T> = T extends string ? T : never;
// OnlyStrings<string | number | boolean> = string
```

### Template Literal Types

```typescript
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

type CSSProperty = "margin" | "padding";
type CSSDirection = "top" | "right" | "bottom" | "left";
type CSSDecl = `${CSSProperty}-${CSSDirection}`;
// "margin-top" | "margin-right" | ... (8 combinations)
```

### Discriminated Unions with Exhaustive Check

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rect": return shape.width * shape.height;
    case "triangle": return 0.5 * shape.base * shape.height;
    default: {
      const _exhaustive: never = shape; // compile error if case missing
      throw new Error(`Unknown shape: ${_exhaustive}`);
    }
  }
}
```

### Branded Types

```typescript
type UserId = number & { __brand: "UserId" };
type PostId = number & { __brand: "PostId" };

function createUserId(id: number): UserId { return id as UserId; }
function createPostId(id: number): PostId { return id as PostId; }

function getUser(id: UserId) { /* ... */ }

const uid = createUserId(1);
const pid = createPostId(1);
getUser(uid); // OK
// getUser(pid); // Error: PostId not assignable to UserId
```

### `satisfies` Operator

```typescript
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
} satisfies Record<string, string | number[]>;

// palette.green is still typed as string (not string | number[])
palette.green.toUpperCase(); // OK - type is narrowed
```

## Gotchas

- Conditional type distribution: `T extends U ? X : Y` distributes over unions when `T` is a bare type parameter; wrap in `[T]` to prevent
- Mapped type modifiers: `+readonly` adds, `-?` removes optional; `-readonly` makes mutable
- `infer` only works inside conditional types; cannot be used standalone
- Recursive conditional types have a depth limit (~50 levels); use tail-call optimization pattern for deep recursion
- Template literal types can create huge union explosions; `${string}` is fine but `${string}${string}` = `string`

## See Also

- [TypeScript: Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)
- [TypeScript: Conditional Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)
