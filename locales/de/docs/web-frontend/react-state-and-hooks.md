---
title: "React-State und Hooks"
category: concepts
tags: [web-frontend, react, hooks, state-management, useEffect]
level: 3
source_sha256: 60eada7f368f55e1824ab5a05ec2ee3dcaa541edd46e82fc6a310538b36ce521
translation: machine
translated_at: '2026-10-24'
---
# React-State und Hooks {#react-state-and-hooks}

Hooks ermöglichen es funktionalen Komponenten, Zustand, Seiteneffekte und den Lebenszyklus ohne Klassen zu verwalten.

## useState {#usestate}

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

### Regeln {#rules}
- Auf oberster Ebene aufrufen (nicht in Bedingungen, Schleifen oder verschachtelten Funktionen)
- Nur in Komponenten oder eigenen Hooks aufrufen
- Aktualisierungen sind asynchron (gebündelt)

### Funktionale Aktualisierungen {#functional-updates}
```jsx
setCount(prev => prev + 1);   // Always correct (uses latest)
setCount(count + 1);           // May be stale in batched updates
```

### Objekt- und Array-Zustand {#object-and-array-state}
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

**Den Zustand niemals direkt mutieren. Immer neue Referenzen erzeugen.**

### Lazy Initialization {#lazy-initialization}
```jsx
const [data, setData] = useState(() => expensiveComputation());
// Function runs only on first render
```

## Ereignisbehandlung {#event-handling}

```jsx
<button onClick={() => handleDelete(id)}>Delete</button>
<form onSubmit={(e) => { e.preventDefault(); /* handle */ }}>
```

**Nicht aufrufen**: `onClick={handleClick}` (korrekt) vs. `onClick={handleClick()}` (ruft sofort auf).

## useEffect {#useeffect}

Seiteneffekte: Datenabruf, Subskriptionen, Timer, DOM-Manipulation.

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

### Abhängigkeitsarray {#dependency-array}
- **Kein Array**: bei jedem Render (meist falsch)
- **`[]`**: nur beim Mounten
- **`[dep1, dep2]`**: wenn sich eine der Abhängigkeiten ändert
- ALLE innerhalb verwendeten Werte müssen in den Abhängigkeiten stehen (ESLint `exhaustive-deps`)

### Muster für Datenabruf {#data-fetching-pattern}
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

### Gängige Muster {#common-patterns}
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

## useRef {#useref}

Veränderlicher Wert, der über Renderings hinweg erhalten bleibt, OHNE ein erneutes Rendern auszulösen.

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

| Merkmal | useRef | useState |
|---------|--------|---------|
| Bleibt erhalten | Ja | Ja |
| Rendert neu | Nein | Ja |
| Zugriff | `.current` | Direkt |
| Verwendung für | DOM, Timer, vorherige Werte | UI-Daten |

## Eigene Hooks {#custom-hooks}

Wiederverwendbare Logik auslagern. Der Name muss mit `use` beginnen.

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

## Fallstricke {#gotchas}

- **Zustandsaktualisierungen sind asynchron**: Direkt nach `set` kann der neue Wert noch nicht gelesen werden
- **Mutation von Objekten/Arrays**: React vergleicht Referenzen; gleiche Referenz = kein erneutes Rendern
- **Fehlende Abhängigkeiten in useEffect**: veraltete Closures führen zu Fehlern; `exhaustive-deps` beachten
- **useEffect für Datenabruf**: Cleanup muss behandelt werden, um das Setzen von Zustand in einer ausgehängten Komponente zu vermeiden
- **Reihenfolge der Hooks ist wichtig**: React verfolgt Hooks nach Aufrufreihenfolge; bedingte Hooks brechen dies
- **useRef löst kein erneutes Rendern aus**: Das Ändern von `.current` aktualisiert die UI nicht

## Siehe auch {#see-also}

- [[react-components-and-jsx]] - Komponenten, Props, JSX
- [[react-rendering-internals]] - Wann Re-Renderings stattfinden, memo, Keys
- [[js-async-and-fetch]] - Fetch-API zum Laden von Daten
- [[typescript-advanced]] - Typisierung von Hooks und Events
