---
title: TypeScript Integration
category: tooling
tags: [typescript, types, generics, interfaces, discriminated-unions, tsconfig, strict, type-safety]
---
# TypeScript Integration

TypeScript adds static typing to JavaScript, catching errors at compile time. In Node.js, TypeScript is used for type-safe APIs, domain modeling with discriminated unions, and ensuring interface contracts across modules.

## Key Facts

- TypeScript compiles to JavaScript; types are erased at runtime (no runtime overhead)
- `tsconfig.json` configures the compiler: `strict: true` enables all strict checks (recommended)
- Key strict flags: `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `noUncheckedIndexedAccess`
- **Discriminated unions**: `type Shape = { kind: 'circle', radius: number } | { kind: 'rect', w: number, h: number }` - TypeScript narrows type in `switch(shape.kind)`
- **Generics**: `function first<T>(arr: T[]): T | undefined` - type parameters for reusable code
- **Utility types**: `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `Readonly<T>`
- **Type guards**: `function isUser(x: unknown): x is User` - custom runtime checks that narrow types
- `as const` makes literals/objects deeply readonly and preserves literal types
- `satisfies` operator (TS 5.0): validates type without widening: `const cfg = { port: 3000 } satisfies Config`
- For Node.js: use `@types/node` for built-in module types; `tsx` or `ts-node` for direct execution
- Module resolution: `"moduleResolution": "node16"` or `"bundler"` for modern projects
- **Declaration files** (`.d.ts`): type definitions without implementation; `@types/*` packages on npm

## Patterns

```typescript
// Strict domain types (branded types)
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

function createUserId(id: string): UserId {
  return id as UserId;
}
// Cannot accidentally pass OrderId where UserId expected

// Discriminated union for API responses
type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; code: string; message: string };

function handleResponse<T>(res: ApiResponse<T>): T {
  switch (res.status) {
    case 'success': return res.data;
    case 'error': throw new Error(`${res.code}: ${res.message}`);
    // TypeScript error if a variant is missing (exhaustive check)
  }
}

// Generic repository interface
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findAll(filter?: Partial<T>): Promise<T[]>;
  create(data: Omit<T, 'id' | 'createdAt'>): Promise<T>;
  update(id: ID, data: Partial<T>): Promise<T>;
  delete(id: ID): Promise<boolean>;
}

class UserRepository implements Repository<User> {
  constructor(private db: Pool) {}

  async findById(id: string): Promise<User | null> {
    const { rows } = await this.db.query(
      'SELECT * FROM users WHERE id = $1', [id]
    );
    return rows[0] ?? null;
  }
  // ...
}

// Type-safe event emitter
interface AppEvents {
  'user:created': [user: User];
  'user:deleted': [userId: string];
  'order:placed': [order: Order, user: User];
}

class TypedEmitter<Events extends Record<string, unknown[]>> {
  private listeners = new Map<string, Function[]>();

  on<K extends keyof Events>(
    event: K,
    listener: (...args: Events[K]) => void
  ): void {
    const list = this.listeners.get(event as string) || [];
    list.push(listener);
    this.listeners.set(event as string, list);
  }

  emit<K extends keyof Events>(event: K, ...args: Events[K]): void {
    const list = this.listeners.get(event as string) || [];
    for (const fn of list) fn(...args);
  }
}

const bus = new TypedEmitter<AppEvents>();
bus.on('user:created', (user) => {
  // user is typed as User
});

// Zod for runtime validation + type inference
import { z } from 'zod';
const UserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});
type User = z.infer<typeof UserSchema>; // derived type

function validateInput(raw: unknown): User {
  return UserSchema.parse(raw); // throws ZodError on invalid
}

// satisfies for config
const config = {
  port: 3000,
  host: 'localhost',
  db: { host: 'db', port: 5432 },
} satisfies AppConfig;
// config.port is narrowed to 3000, not number

// Type-safe middleware
type Middleware<Ctx> = (ctx: Ctx, next: () => Promise<void>) => Promise<void>;

function compose<Ctx>(middlewares: Middleware<Ctx>[]): Middleware<Ctx> {
  return async (ctx, next) => {
    let index = -1;
    async function dispatch(i: number): Promise<void> {
      if (i <= index) throw new Error('next() called multiple times');
      index = i;
      const fn = middlewares[i] ?? next;
      await fn(ctx, () => dispatch(i + 1));
    }
    await dispatch(0);
  };
}
```

## Gotchas

- **Symptom**: type says it's safe but crashes at runtime - **Cause**: `as` type assertion bypasses checks; external data not validated - **Fix**: validate external input with Zod/Ajv; minimize `as` usage; prefer type guards
- **Symptom**: `any` spreading through the codebase - **Cause**: `strict: false` or liberal use of `any` - **Fix**: enable `strict: true`; use `unknown` instead of `any` and narrow with type guards
- **Symptom**: import resolves at compile time but fails at runtime - **Cause**: mismatch between `moduleResolution` in tsconfig and actual module format - **Fix**: use `"moduleResolution": "node16"` with `"module": "node16"` for proper CJS/ESM support
- **Symptom**: `Object.keys()` returns `string[]` not `(keyof T)[]` - **Cause**: TypeScript's structural typing means objects can have extra properties - **Fix**: use type assertion `Object.keys(obj) as (keyof typeof obj)[]` when you control the object shape

## See Also

- [[modules-and-packages]] - ESM/CJS interop with TypeScript
- [[algebraic-types]] - discriminated unions as TypeScript-native sum types
- [[solid-and-grasp]] - interfaces for dependency inversion
- [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/)
- [Node.js TypeScript guide](https://nodejs.org/en/learn/getting-started/nodejs-with-typescript)
