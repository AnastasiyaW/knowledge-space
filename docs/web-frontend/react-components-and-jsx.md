---
title: React Components and JSX
category: concepts
tags: [web-frontend, react, jsx, components, props]
---

# React Components and JSX

React builds UIs from composable components. Each component is a function that returns JSX describing what to render.

## Project Setup (Vite)

```bash
npm create vite@latest my-app -- --template react
cd my-app && npm install && npm run dev
```

```text
src/
  components/     # Reusable components
  pages/          # Page-level components
  App.jsx         # Root component
  main.jsx        # Entry (renders App into DOM)
```

### Entry Point
```jsx
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

`StrictMode` double-renders in dev to detect side effects. No effect in production.

## JSX Rules

```jsx
// 1. Single root element (or Fragment)
return (
  <>
    <h1>Title</h1>
    <p>Text</p>
  </>
);

// 2. All tags must close
<img src="photo.jpg" alt="" />
<input type="text" />

// 3. HTML differences
<div className="card">          {/* className, not class */}
<label htmlFor="email">         {/* htmlFor, not for */}
<div onClick={fn} tabIndex={0}> {/* camelCase attributes */}

// 4. JS expressions in {}
<h1>{user.name}</h1>
<p>{isActive ? "Active" : "Inactive"}</p>
<p>{items.length > 0 && "Has items"}</p>

// 5. Inline styles as objects
<div style={{ backgroundColor: "blue", fontSize: "16px" }}>
```

### Rendering Lists
```jsx
{items.map(item => (
  <li key={item.id}>{item.name}</li>
))}
```

**key prop**: must be unique among siblings. Use stable IDs, not array index (breaks on reorder). React uses keys for efficient DOM updates.

## Functional Components

```jsx
function Card({ title, description }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}
```

Rules: name starts uppercase, returns JSX (or null), one component per file (convention).

## Props

Props are read-only data passed parent -> child.

```jsx
// Parent
<Card
  title="React"
  description="Learn components"
  isNew={true}
  tags={["react", "frontend"]}
  onClick={() => console.log("clicked")}
/>

// Child (destructured)
function Card({ title, description, isNew, tags, onClick }) {
  return (
    <div onClick={onClick}>
      <h2>{title}</h2>
      <p>{description}</p>
      {isNew && <span className="badge">New</span>}
    </div>
  );
}
```

### Default Props
```jsx
function Button({ variant = "primary", size = "md", children }) {
  return <button className={`btn-${variant} btn-${size}`}>{children}</button>;
}
```

### children Prop
```jsx
function Container({ children }) {
  return <div className="container">{children}</div>;
}

<Container>
  <h1>Title</h1>
  <p>Content between tags becomes children</p>
</Container>
```

### Props are Read-Only
Never modify props. Data flows one direction: parent -> child. To change data, use state and pass callbacks.

## Component Composition

```jsx
function PageLayout({ header, sidebar, children }) {
  return (
    <div className="layout">
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{children}</main>
    </div>
  );
}

<PageLayout header={<Nav />} sidebar={<Filters />}>
  <ProductList />
</PageLayout>
```

Composition over inheritance - React components compose by nesting, not extending.

## Conditional Rendering

```jsx
// Ternary
{isLoggedIn ? <Dashboard /> : <Login />}

// Logical AND
{hasItems && <ItemList items={items} />}

// Early return
function Profile({ user }) {
  if (!user) return <p>Loading...</p>;
  return <h1>{user.name}</h1>;
}
```

**Gotcha with `&&`**: `{0 && <Component />}` renders `0`. Use `{count > 0 && ...}` or ternary.

## Gotchas

- **Uppercase names required**: `<card />` is HTML element, `<Card />` is component
- **key in lists**: missing or index-based keys cause rendering bugs
- **`&&` with 0**: falsy number 0 renders in JSX, unlike other falsy values
- **Props are immutable**: never `props.value = newValue`
- **Spread props carefully**: `<div {...props}>` may pass unexpected attributes to DOM

## See Also

- [[react-state-and-hooks]] - useState, useEffect, custom hooks
- [[react-rendering-internals]] - Virtual DOM, reconciliation, keys
- [[react-styling-approaches]] - CSS Modules, Tailwind in React
- [[typescript-advanced]] - Typing React components
