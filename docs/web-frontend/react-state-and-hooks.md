---
title: React State and Hooks
category: concepts
tags: [web-frontend, react, hooks, state-management, useEffect]
---

# React State and Hooks

Hooks let functional components manage state, side effects, and lifecycle without classes.

## useState

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
      <button onClick={() => setCount(prev => prev - 1)}>-</button>
    </div>
  );
}
```

### Rules
- Call at TOP LEVEL (not in conditions/loops/nested functions)
- Call only in components or custom hooks
- Updates are async (batched)

### Functional Updates
```jsx
setCount(prev => prev + 1);   // Always correct (uses latest)
setCount(count + 1);           // May be stale in batched updates
```

### Object and Array State
```jsx
// WRONG: mutating directly (React won't detect change)
user.age = 26; setUser(user);

// CORRECT: new object/array
setUser({ ...user, age: 26 });
setUser(prev => ({ ...prev, age: prev.age + 1 }));
setItems([...items, newItem]);                      // Add
setItems(items.filter(i => i.id !== id));           // Remove
setItems(items.map(i => i.id === id ? { ...i, done: true } : i));  // Update
```

**Never mutate state directly. Always create new references.**

### Lazy Initialization
```jsx
const [data, setData] = useState(() => expensiveComputation());
// Function runs only on first render
```

## Event Handling

```jsx
<button onClick={() => handleDelete(id)}>Delete</button>
<form onSubmit={(e) => { e.preventDefault(); /* handle */ }}>
```

**Don't call**: `onClick={handleClick}` (correct) vs `onClick={handleClick()}` (calls immediately).

## useEffect

Side effects: data fetching, subscriptions, timers, DOM manipulation.

```jsx
// Every render
useEffect(() => { console.log("rendered"); });

// Mount only
useEffect(() => { fetchData(); }, []);

// When dependency changes
useEffect(() => { fetchUser(userId); }, [userId]);

// Cleanup (before re-run and on unmount)
useEffect(() => {
  const timer = setInterval(tick, 1000);
  return () => clearInterval(timer);
}, []);
```

### Dependency Array
- **No array**: every render (usually wrong)
- **`[]`**: mount only
- **`[dep1, dep2]`**: when any dep changes
- ALL values used inside must be in deps (ESLint `exhaustive-deps`)

### Data Fetching Pattern
```jsx
useEffect(() => {
  let cancelled = false;
  async function load() {
    const data = await fetchData();
    if (!cancelled) setData(data);
  }
  load();
  return () => { cancelled = true; };
}, []);
```

### Common Patterns
```jsx
// Event listener
useEffect(() => {
  const handler = () => setWidth(window.innerWidth);
  window.addEventListener("resize", handler);
  return () => window.removeEventListener("resize", handler);
}, []);

// Document title
useEffect(() => { document.title = `${count} items`; }, [count]);
```

## useRef

Mutable value that persists across renders WITHOUT causing re-render.

```jsx
// DOM access
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus();

// Persist values (no re-render)
const timerRef = useRef(null);
timerRef.current = setInterval(tick, 1000);
clearInterval(timerRef.current);
```

| Feature | useRef | useState |
|---------|--------|---------|
| Persists | Yes | Yes |
| Re-renders | No | Yes |
| Access | `.current` | Direct |
| For | DOM, timers, prev values | UI data |

## Custom Hooks

Extract reusable logic. Must start with `use`.

```jsx
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);
  return [value, setValue];
}

const [theme, setTheme] = useLocalStorage("theme", "light");
```

```jsx
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(url)
      .then(r => r.json())
      .then(d => { if (!cancelled) setData(d); })
      .catch(e => { if (!cancelled) setError(e); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [url]);

  return { data, loading, error };
}
```

## Gotchas

- **State updates are async**: can't read new value immediately after `set`
- **Object/array mutation**: React uses reference comparison; same reference = no re-render
- **Missing deps in useEffect**: stale closures lead to bugs; follow `exhaustive-deps`
- **useEffect for data fetching**: must handle cleanup to avoid setting state on unmounted component
- **Hooks order matters**: React tracks hooks by call order; conditional hooks break this
- **useRef doesn't trigger re-render**: changing `.current` won't update the UI

## See Also

- [[react-components-and-jsx]] - Components, props, JSX
- [[react-rendering-internals]] - When re-renders happen, memo, keys
- [[js-async-and-fetch]] - Fetch API for data loading
- [[typescript-advanced]] - Typing hooks and events
