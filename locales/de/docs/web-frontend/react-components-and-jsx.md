---
title: "React-Komponenten und JSX"
category: concepts
tags: [web-frontend, react, jsx, components, props]
level: 3
source_sha256: 7fc879b174e02898c5ed2ed8d97e875b2127641d1cd9c3b7be29bc833bcfe443
translation: machine
translated_at: '2026-10-24'
---
# React-Komponenten und JSX {#react-components-and-jsx}

React baut UIs aus kombinierbaren Komponenten. Jede Komponente ist eine Funktion, die JSX zurückgibt, das beschreibt, was gerendert werden soll.

## Projekteinrichtung (Vite) {#project-setup-vite}

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

### Einstiegspunkt {#entry-point}
```jsx
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

`StrictMode` rendert im Entwicklungsmodus doppelt, um Seiteneffekte aufzudecken. In der Produktion hat dies keine Auswirkung.

## JSX-Regeln {#jsx-rules}

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

### Listen rendern {#rendering-lists}
```jsx
{items.map(item => (
  <li key={item.id}>{item.name}</li>
))}
```

**key-Prop**: muss unter Geschwistern eindeutig sein. Verwende stabile IDs statt Array-Indizes (diese brechen bei Umsortierung). React nutzt Keys für effiziente DOM-Aktualisierungen.

## Funktionale Komponenten {#functional-components}

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

Regeln: Der Name beginnt mit einem Großbuchstaben, die Komponente gibt JSX (oder `null`) zurück, eine Komponente pro Datei (Konvention).

## Props {#props}

Props sind schreibgeschützte Daten, die von Eltern- an Kindkomponenten übergeben werden.

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

### Standard-Props {#default-props}
```jsx
function Button({ variant = "primary", size = "md", children }) {
  return <button className={`btn-${variant} btn-${size}`}>{children}</button>;
}
```

### children-Prop {#children-prop}
```jsx
function Container({ children }) {
  return <div className="container">{children}</div>;
}

<Container>
  <h1>Title</h1>
  <p>Content between tags becomes children</p>
</Container>
```

### Props sind schreibgeschützt {#props-are-read-only}
Props dürfen niemals verändert werden. Daten fließen in eine Richtung: von der Elternkomponente zur Kindkomponente. Um Daten zu ändern, verwende State und übergib Callbacks.

## Komponenten-Komposition {#component-composition}

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

Komposition statt Vererbung: React-Komponenten werden durch Verschachtelung kombiniert, nicht durch Erweiterung.

## Bedingtes Rendern {#conditional-rendering}

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

**Stolperfalle bei `&&`**: `{0 && <Component />}` rendert `0`. Verwende stattdessen `{count > 0 && ...}` oder einen ternären Operator.

## Stolperfallen {#gotchas}

- **Großgeschriebene Namen erforderlich**: `<card />` ist ein HTML-Element, `<Card />` ist eine Komponente
- **key in Listen**: fehlende oder indexbasierte Keys führen zu Rendering-Fehlern
- **`&&` mit 0**: Die falsy Zahl 0 wird in JSX gerendert, anders als andere falsy Werte
- **Props sind unveränderlich**: niemals `props.value = newValue`
- **Spread-Props mit Bedacht einsetzen**: `<div {...props}>` kann unerwartete Attribute an das DOM weitergeben

## Siehe auch {#see-also}

- [[react-state-and-hooks]] - useState, useEffect, eigene Hooks
- [[react-rendering-internals]] - Virtual DOM, Reconciliation, Keys
- [[react-styling-approaches]] - CSS Modules, Tailwind in React
- [[typescript-advanced]] - Typisierung von React-Komponenten
