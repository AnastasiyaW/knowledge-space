---
title: "Composants React et JSX"
category: concepts
tags: [web-frontend, react, jsx, components, props]
level: 3
source_sha256: 7fc879b174e02898c5ed2ed8d97e875b2127641d1cd9c3b7be29bc833bcfe443
translation: machine
translated_at: '2026-10-24'
---
# Composants React et JSX {#react-components-and-jsx}

React construit des interfaces utilisateur à partir de composants composables. Chaque composant est une fonction qui renvoie du JSX décrivant ce qui doit être rendu.

## Mise en place du projet (Vite) {#project-setup-vite}

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

### Point d'entrée {#entry-point}
```jsx
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

`StrictMode` effectue un double rendu en développement pour détecter les effets de bord. Sans effet en production.

## Règles du JSX {#jsx-rules}

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

### Rendu de listes {#rendering-lists}
```jsx
{items.map(item => (
  <li key={item.id}>{item.name}</li>
))}
```

**Prop key** : doit être unique parmi les éléments frères. Utilisez des identifiants stables, et non l'index du tableau (cela pose problème lors d'un réordonnancement). React utilise les clés pour mettre à jour le DOM de manière efficace.

## Composants fonctionnels {#functional-components}

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

Règles : le nom commence par une majuscule, le composant renvoie du JSX (ou `null`), un composant par fichier (convention).

## Props {#props}

Les props sont des données en lecture seule transmises du parent vers l'enfant.

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

### Valeurs par défaut des props {#default-props}
```jsx
function Button({ variant = "primary", size = "md", children }) {
  return <button className={`btn-${variant} btn-${size}`}>{children}</button>;
}
```

### Prop children {#children-prop}
```jsx
function Container({ children }) {
  return <div className="container">{children}</div>;
}

<Container>
  <h1>Title</h1>
  <p>Content between tags becomes children</p>
</Container>
```

### Les props sont en lecture seule {#props-are-read-only}
Ne modifiez jamais les props. Les données circulent dans un seul sens : du parent vers l'enfant. Pour modifier des données, utilisez l'état (state) et transmettez des callbacks.

## Composition de composants {#component-composition}

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

Composition plutôt qu'héritage : les composants React se composent par imbrication, et non par extension.

## Rendu conditionnel {#conditional-rendering}

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

**Piège avec `&&`** : `{0 && <Component />}` affiche `0`. Utilisez `{count > 0 && ...}` ou un opérateur ternaire.

## Pièges à éviter {#gotchas}

- **Noms en majuscule obligatoires** : `<card />` est un élément HTML, `<Card />` est un composant
- **key dans les listes** : des clés absentes ou basées sur l'index provoquent des bugs de rendu
- **`&&` avec 0** : le nombre 0 est affiché dans le JSX, contrairement à d'autres valeurs falsy
- **Props immuables** : ne jamais écrire `props.value = newValue`
- **Spread des props avec précaution** : `<div {...props}>` peut transmettre des attributs inattendus au DOM

## Voir aussi {#see-also}

- [[react-state-and-hooks]] - useState, useEffect, hooks personnalisés
- [[react-rendering-internals]] - DOM virtuel, réconciliation, clés
- [[react-styling-approaches]] - CSS Modules, Tailwind dans React
- [[typescript-advanced]] - Typer les composants React
