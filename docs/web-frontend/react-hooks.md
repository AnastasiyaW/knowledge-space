---
title: React Hooks
category: react
tags: [react, hooks, useState, useEffect, useRef, useMemo, useCallback, custom-hooks]
---

# React Hooks

## Key Facts

- **Hooks** allow function components to use state, effects, refs, context, and more
- `useState(initial)` - returns `[value, setter]`; setter triggers re-render; can accept updater function
- `useEffect(fn, deps)` - side effects after render; return cleanup function; empty deps `[]` = mount only
- `useRef(initial)` - mutable ref that persists across renders without causing re-render; `.current` access
- `useMemo(fn, deps)` - memoize expensive computation; recomputes only when deps change
- `useCallback(fn, deps)` - memoize function reference; equivalent to `useMemo(() => fn, deps)`
- `useContext(Context)` - read context value; re-renders when context changes
- `useReducer(reducer, initial)` - state machine pattern; `dispatch({ type, payload })`
- **Rules of Hooks**: only call at top level (not inside loops/conditions), only in function components or custom hooks
- Custom hooks extract reusable stateful logic; name must start with `use`
- Related: [[react-components-and-jsx]], [[react-state-management]]

## Patterns

### useState with Updater Function

```tsx
const [count, setCount] = useState(0);

// Direct value
setCount(5);

// Updater function - safe for batched updates
setCount(prev => prev + 1);

// Object state - spread previous
const [form, setForm] = useState({ name: "", email: "" });
setForm(prev => ({ ...prev, name: "Ana" }));
```

### useEffect Patterns

```tsx
// Mount only (fetch data)
useEffect(() => {
  fetchData().then(setData);
}, []); // empty deps

// Dependency tracking
useEffect(() => {
  const ws = new WebSocket(`wss://api.example.com/${roomId}`);
  ws.onmessage = (e) => setMessages(prev => [...prev, e.data]);
  return () => ws.close(); // cleanup on unmount or roomId change
}, [roomId]);

// Cleanup pattern (event listener)
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    if (e.key === "Escape") setOpen(false);
  };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, []);
```

### useRef for DOM Access and Persistent Values

```tsx
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focus = () => inputRef.current?.focus();

  return <input ref={inputRef} />;
}

// Persistent value (no re-render)
function Timer() {
  const intervalRef = useRef<number | null>(null);

  const start = () => {
    intervalRef.current = window.setInterval(() => { /* tick */ }, 1000);
  };
  const stop = () => {
    if (intervalRef.current) clearInterval(intervalRef.current);
  };

  return /* ... */;
}
```

### Custom Hook

```tsx
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

// Usage
const [theme, setTheme] = useLocalStorage("theme", "light");
```

### useReducer for Complex State

```tsx
type Action =
  | { type: "increment" }
  | { type: "decrement" }
  | { type: "reset"; payload: number };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "increment": return state + 1;
    case "decrement": return state - 1;
    case "reset": return action.payload;
  }
}

const [count, dispatch] = useReducer(reducer, 0);
dispatch({ type: "increment" });
```

## Gotchas

- `useEffect` with missing deps causes stale closures; ESLint `exhaustive-deps` rule catches this
- `useEffect` runs AFTER render + paint; for DOM measurements before paint, use `useLayoutEffect`
- `useMemo`/`useCallback` are performance optimizations, not semantic guarantees; React may discard cache
- Setting state during render causes infinite loop; `useEffect` or event handler is the correct place
- `useState` initializer function runs only on first render: `useState(() => expensiveInit())` - don't call directly as `useState(expensiveInit())`

## See Also

- [React: Hooks Reference](https://react.dev/reference/react/hooks)
- [React: Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
