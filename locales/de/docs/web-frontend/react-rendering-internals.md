---
title: "React-Rendering-Interna"
category: concepts
tags: [web-frontend, react, virtual-dom, performance, reconciliation]
level: 4
source_sha256: 7b34113fdf55b9bd51b0a542765540eb3489c5a5d5f7685bece7d45b635627be
translation: machine
translated_at: '2026-10-24'
---
# React-Rendering-Interna {#react-rendering-internals}

Das Verständnis, wie React rendert, ist die Grundlage für performante Anwendungen. React verwendet ein Virtual DOM und die Fiber-Architektur, um Operationen auf dem echten DOM zu minimieren.

## Virtual DOM {#virtual-dom}

1. Komponente gibt JSX zurück -> Virtual-DOM-Baum (leichtgewichtige JS-Objekte)
2. State/Props ändern sich -> neuer Virtual-DOM-Baum
3. **Diffing**: neuen Baum mit dem vorherigen vergleichen
4. **Reconciliation**: minimale DOM-Operationen berechnen
5. **Commit**: Änderungen gebündelt anwenden

## Fiber-Architektur {#fiber-architecture}

Jedes Element besitzt einen Fiber-Knoten, der Typ, Props, DOM-Referenz, Verknüpfungen zu Eltern-, Kind- und Geschwisterknoten, State und Scheduling-Metadaten enthält.

### Zweiphasiges Rendering {#two-phase-rendering}

**Render-Phase** (unterbrechbar): durchläuft den Baum, ruft Komponenten auf und diffed die Ausgabe. Keine DOM-Mutationen. Kann pausiert und neu gestartet werden.

**Commit-Phase** (synchron): wendet DOM-Mutationen an, führt `useLayoutEffect` aus (synchron, blockiert das Painting), der Browser zeichnet, danach wird `useEffect` ausgeführt (asynchron).

### Komponenten-Lebenszyklus (Hooks) {#component-lifecycle-hooks}
```sql
Mount:  render -> DOM update -> useLayoutEffect -> paint -> useEffect
Update: re-render -> diff -> DOM update -> layout cleanup/run -> paint -> effect cleanup/run
Unmount: layout cleanup -> effect cleanup -> DOM removal
```

## Wann Komponenten neu rendern {#when-components-re-render}

1. Ihr **State** ändert sich (setState)
2. Ihr **Parent** rendert neu (auch wenn sich die Props nicht geändert haben!)
3. Ihr **Context**-Wert ändert sich

Eine Komponente rendert **nicht** neu, weil sich "die Props geändert haben", sondern weil der Parent neu gerendert hat.

## Unnötige Re-Renders vermeiden {#preventing-unnecessary-re-renders}

### React.memo {#reactmemo}
```jsx
const ExpensiveChild = React.memo(function({ data }) {
  return <div>{data.name}</div>;
});
// Only re-renders if 'data' prop changes (shallow comparison)
```

### useMemo (Werte cachen) {#usememo-cache-values}
```jsx
const sorted = useMemo(() =>
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### useCallback (Funktionen cachen) {#usecallback-cache-functions}
```jsx
const handleClick = useCallback(() => {
  setCount(c => c + 1);
}, []);
// Same reference across renders -> memo'd child won't re-render
```

**Wann verwenden**: nur dann, wenn ein Problem gemessen wurde. Zuerst mit dem React DevTools Profiler profilieren. Verfrühtes Memoizing erhöht die Komplexität.

## Vertiefung: key-Prop {#key-prop-deep-dive}

```jsx
// GOOD: stable unique ID
{items.map(item => <Item key={item.id} data={item} />)}

// BAD: index (breaks on reorder/delete)
{items.map((item, i) => <Item key={i} data={item} />)}
```

**Key-Reset-Trick**: Das Ändern des Keys erzwingt Unmount und Remount (setzt den gesamten State zurück):
```jsx
<UserForm key={userId} userId={userId} />
```

## Batch-Updates (React 18) {#batch-updates-react-18}

React 18 fasst ALLE State-Updates zusammen, auch asynchrone:
```jsx
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  // ONE re-render
}

setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Still ONE re-render (React 18+)
}, 1000);
```

Synchron erzwingen: `flushSync(() => setState(v))` (selten).

## React-Frameworks {#react-frameworks}

React ist eine Bibliothek (nur die View-Schicht). Routing, State und Datenabruf wählt man separat aus oder nutzt ein Framework:

- **Next.js**: SSR, SSG, dateibasiertes Routing, API-Routen (am weitesten verbreitet)
- **Remix**: verschachteltes Routing, progressive Enhancement
- **Gatsby**: statische Generierung, GraphQL

Für Produktivbetrieb: ein Framework verwenden. Zum Lernen oder für kleine SPAs: Vite + React.

## Klassenkomponenten (Legacy) {#class-components-legacy}

```jsx
class Counter extends React.Component {
  state = { count: 0 };
  componentDidMount() { }
  componentDidUpdate() { }
  componentWillUnmount() { }
  render() { return <p>{this.state.count}</p>; }
}
```

Neuer Code sollte durchgängig funktionale Komponenten mit Hooks verwenden.

## Fallstricke {#gotchas}

- **Parent-Re-Render = Kind-Re-Render**: auch bei unveränderten Props, sofern nicht in `React.memo` gekapselt
- **Objekt- bzw. Funktions-Props brechen memo**: `<Child data={{...}}/>` erzeugt bei jedem Render eine neue Referenz
- **useMemo/useCallback sind nicht kostenlos**: Speicheraufwand für das Memoizing; zuerst messen
- **StrictMode-Doppel-Render**: nur in der Entwicklung aktiv, erkennt unreine Renders
- **Effect-Timing**: `useEffect` läuft nach dem Painting, `useLayoutEffect` blockiert das Painting (für DOM-Messungen verwenden)
- **Index-Keys**: führen dazu, dass State bei Umordnung einer Liste an falschen Elementen hängen bleibt

## Siehe auch {#see-also}

- [[react-components-and-jsx]] - Komponenten, Props, JSX-Grundlagen
- [[react-state-and-hooks]] - State-Management, useEffect
- [[react-styling-approaches]] - CSS Modules, Tailwind
- [[frontend-build-systems]] - Vite, webpack für React-Anwendungen
