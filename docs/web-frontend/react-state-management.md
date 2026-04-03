---
title: React State Management
category: react
tags: [react, state, redux, context, zustand, lifting-state, global-state]
---

# React State Management

## Key Facts

- **Local state** (`useState`) for component-specific data; simplest and preferred when possible
- **Lifting state up**: move shared state to nearest common ancestor, pass via props
- **Context** (`createContext` + `useContext`) for cross-cutting concerns (theme, auth, locale); not optimized for frequent updates
- **Redux** (Redux Toolkit): global store, actions, reducers, selectors; good for large apps with complex state flows
- **Redux Toolkit (RTK)**: `createSlice` simplifies reducers; `configureStore` adds middleware; RTK Query for data fetching
- State colocation: keep state as close to where it's used as possible; avoid premature global state
- **Derived state**: compute from existing state in render; don't store what you can calculate
- **Server state** (React Query / TanStack Query) is different from client state; caching, revalidation, deduplication
- `useReducer` for local complex state (multiple related values, state machine); alternative to `useState`
- Related: [[react-hooks]], [[react-components-and-jsx]], [[react-router-and-navigation]]

## Patterns

### Redux Toolkit Slice

```typescript
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface TodoState {
  items: Todo[];
  filter: "all" | "active" | "done";
}

const todoSlice = createSlice({
  name: "todos",
  initialState: { items: [], filter: "all" } as TodoState,
  reducers: {
    addTodo(state, action: PayloadAction<string>) {
      state.items.push({ id: Date.now(), text: action.payload, done: false });
      // Immer allows "mutation" syntax - produces immutable updates
    },
    toggleTodo(state, action: PayloadAction<number>) {
      const todo = state.items.find(t => t.id === action.payload);
      if (todo) todo.done = !todo.done;
    },
    setFilter(state, action: PayloadAction<TodoState["filter"]>) {
      state.filter = action.payload;
    },
  },
});

export const { addTodo, toggleTodo, setFilter } = todoSlice.actions;
export default todoSlice.reducer;
```

### Redux Store Setup

```typescript
import { configureStore } from "@reduxjs/toolkit";
import todoReducer from "./todoSlice";

export const store = configureStore({
  reducer: {
    todos: todoReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed hooks
import { useDispatch, useSelector, TypedUseSelectorHook } from "react-redux";
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Context for Theme

```tsx
const ThemeContext = createContext<{
  theme: "light" | "dark";
  toggle: () => void;
}>({ theme: "light", toggle: () => {} });

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const toggle = useCallback(
    () => setTheme(t => t === "light" ? "dark" : "light"),
    []
  );
  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

function useTheme() {
  return useContext(ThemeContext);
}
```

### State Decision Matrix

```
Local state (useState)     -> single component, UI state (open/closed, input value)
Lifted state               -> 2-3 siblings share data
Context                    -> many components need same data, infrequent updates (theme, locale, auth)
Redux / Zustand            -> complex client state, frequent updates, many consumers
React Query / TanStack     -> server/API data (caching, refetching, deduplication)
URL state (search params)  -> filters, pagination, shareable state
```

## Gotchas

- Context causes ALL consumers to re-render when value changes; split contexts or use `useMemo` on value object
- Redux state must be serializable (no functions, class instances, Promises); use plain objects/arrays
- Immer (used in RTK) allows "mutation" syntax in reducers but produces immutable updates; this ONLY works inside `createSlice` reducers
- Don't store derived data in state; compute it: `const activeTodos = todos.filter(t => !t.done)` in component or selector
- Prop drilling 2-3 levels deep is fine; don't reach for Context/Redux prematurely

## See Also

- [Redux Toolkit: Quick Start](https://redux-toolkit.js.org/tutorials/quick-start)
- [React: Managing State](https://react.dev/learn/managing-state)
