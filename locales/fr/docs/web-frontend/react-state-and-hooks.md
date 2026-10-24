---
title: "État et hooks React"
category: concepts
tags: [web-frontend, react, hooks, state-management, useEffect]
level: 3
source_sha256: 60eada7f368f55e1824ab5a05ec2ee3dcaa541edd46e82fc6a310538b36ce521
translation: machine
translated_at: '2026-10-24'
---
# État et hooks React {#react-state-and-hooks}

Les hooks permettent aux composants fonctionnels de gérer l'état, les effets de bord et le cycle de vie sans recourir aux classes.

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

### Règles {#rules}
- Appeler au NIVEAU SUPÉRIEUR (pas dans des conditions, des boucles ou des fonctions imbriquées)
- Appeler uniquement dans des composants ou des hooks personnalisés
- Les mises à jour sont asynchrones (regroupées par lots)

### Mises à jour fonctionnelles {#functional-updates}
```jsx
setCount(prev => prev + 1);   // Always correct (uses latest)
setCount(count + 1);           // May be stale in batched updates
```

### État objet et tableau {#object-and-array-state}
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

**Ne jamais muter l'état directement. Toujours créer de nouvelles références.**

### Initialisation paresseuse {#lazy-initialization}
```jsx
const [data, setData] = useState(() => expensiveComputation());
// Function runs only on first render
```

## Gestion des événements {#event-handling}

```jsx
<button onClick={() => handleDelete(id)}>Delete</button>
<form onSubmit={(e) => { e.preventDefault(); /* handle */ }}>
```

**Ne pas appeler** : `onClick={handleClick}` (correct) contre `onClick={handleClick()}` (appelle immédiatement).

## useEffect {#useeffect}

Effets de bord : récupération de données, abonnements, minuteurs, manipulation du DOM.

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

### Tableau de dépendances {#dependency-array}
- **Pas de tableau** : à chaque rendu (généralement une erreur)
- **`[]`** : uniquement au montage
- **`[dep1, dep2]`** : lorsqu'une des dépendances change
- TOUTES les valeurs utilisées à l'intérieur doivent figurer dans les dépendances (règle ESLint `exhaustive-deps`)

### Schéma de récupération de données {#data-fetching-pattern}
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

### Schémas courants {#common-patterns}
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

Valeur mutable qui persiste entre les rendus SANS provoquer de nouveau rendu.

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

| Caractéristique | useRef | useState |
|---------|--------|---------|
| Persiste | Oui | Oui |
| Provoque un rendu | Non | Oui |
| Accès | `.current` | Direct |
| Usage | DOM, minuteurs, valeurs précédentes | Données d'interface |

## Hooks personnalisés {#custom-hooks}

Extraire la logique réutilisable. Doivent commencer par `use`.

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

## Pièges {#gotchas}

- **Les mises à jour d'état sont asynchrones** : impossible de lire la nouvelle valeur immédiatement après `set`
- **Mutation d'objets et de tableaux** : React utilise une comparaison par référence ; même référence = pas de nouveau rendu
- **Dépendances manquantes dans useEffect** : les closures obsolètes provoquent des bugs ; suivre `exhaustive-deps`
- **useEffect pour la récupération de données** : il faut gérer le nettoyage pour éviter de mettre à jour l'état d'un composant démonté
- **L'ordre des hooks compte** : React suit les hooks selon l'ordre d'appel ; les hooks conditionnels cassent ce mécanisme
- **useRef ne déclenche pas de rendu** : modifier `.current` ne met pas à jour l'interface

## Voir aussi {#see-also}

- [[react-components-and-jsx]] - Composants, props, JSX
- [[react-rendering-internals]] - Quand les rendus surviennent, memo, clés
- [[js-async-and-fetch]] - API Fetch pour le chargement de données
- [[typescript-advanced]] - Typer les hooks et les événements
