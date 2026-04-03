---
title: React Rendering Internals
category: concepts
tags: [web-frontend, react, virtual-dom, performance, reconciliation]
---

# React Rendering Internals

Understanding how React renders enables writing performant applications. React uses a Virtual DOM and Fiber architecture to minimize real DOM operations.

## Virtual DOM

1. Component returns JSX -> virtual DOM tree (lightweight JS objects)
2. State/props change -> new virtual DOM tree
3. **Diffing**: compare new tree with previous
4. **Reconciliation**: calculate minimal DOM operations
5. **Commit**: apply changes in batch

## Fiber Architecture

Each element has a Fiber node containing type, props, DOM reference, links to parent/child/sibling, state, and scheduling metadata.

### Two-Phase Rendering

**Render phase** (interruptible): traverses tree, calls components, diffs output. No DOM mutations. Can be paused/restarted.

**Commit phase** (synchronous): applies DOM mutations, runs `useLayoutEffect` (sync, blocks paint), browser paints, runs `useEffect` (async).

### Component Lifecycle (Hooks)
```
Mount:  render -> DOM update -> useLayoutEffect -> paint -> useEffect
Update: re-render -> diff -> DOM update -> layout cleanup/run -> paint -> effect cleanup/run
Unmount: layout cleanup -> effect cleanup -> DOM removal
```

## When Components Re-Render

1. Its **state** changes (setState)
2. Its **parent** re-renders (even if props unchanged!)
3. Its **context** value changes

A component does NOT re-render "because props changed" - it re-renders because parent re-rendered.

## Preventing Unnecessary Re-Renders

### React.memo
```jsx
const ExpensiveChild = React.memo(function({ data }) {
  return <div>{data.name}</div>;
});
// Only re-renders if 'data' prop changes (shallow comparison)
```

### useMemo (cache values)
```jsx
const sorted = useMemo(() =>
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### useCallback (cache functions)
```jsx
const handleClick = useCallback(() => {
  setCount(c => c + 1);
}, []);
// Same reference across renders -> memo'd child won't re-render
```

**When to use**: only when you've measured a problem. Profile first with React DevTools Profiler. Premature memoization adds complexity.

## key Prop Deep Dive

```jsx
// GOOD: stable unique ID
{items.map(item => <Item key={item.id} data={item} />)}

// BAD: index (breaks on reorder/delete)
{items.map((item, i) => <Item key={i} data={item} />)}
```

**Key reset trick**: changing key forces unmount + remount (resets all state):
```jsx
<UserForm key={userId} userId={userId} />
```

## Batch Updates (React 18)

React 18 batches ALL state updates, including async:
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

Force sync: `flushSync(() => setState(v))` (rare).

## React Frameworks

React is a library (view layer only). Choose routing, state, data fetching separately, or use a framework:

- **Next.js**: SSR, SSG, file-based routing, API routes (most popular)
- **Remix**: Nested routing, progressive enhancement
- **Gatsby**: Static generation, GraphQL

For production: use a framework. For learning/small SPAs: Vite + React.

## Class Components (Legacy)

```jsx
class Counter extends React.Component {
  state = { count: 0 };
  componentDidMount() { }
  componentDidUpdate() { }
  componentWillUnmount() { }
  render() { return <p>{this.state.count}</p>; }
}
```

All new code should use functional components with hooks.

## Gotchas

- **Parent re-render = child re-render**: even with unchanged props, unless wrapped in `React.memo`
- **Object/function props break memo**: `<Child data={{...}}/>` creates new reference each render
- **useMemo/useCallback not free**: memory overhead for memoization; measure first
- **StrictMode double-render**: development only, catches impure renders
- **Effect timing**: `useEffect` runs after paint, `useLayoutEffect` blocks paint (use for DOM measurements)
- **Index keys**: cause state to persist on wrong items when list reorders

## See Also

- [[react-components-and-jsx]] - Components, props, JSX basics
- [[react-state-and-hooks]] - State management, useEffect
- [[react-styling-approaches]] - CSS Modules, Tailwind
- [[frontend-build-systems]] - Vite, webpack for React apps
