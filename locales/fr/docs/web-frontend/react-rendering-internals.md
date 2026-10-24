---
title: "Fonctionnement interne du rendu React"
category: concepts
tags: [web-frontend, react, virtual-dom, performance, reconciliation]
level: 4
source_sha256: 7b34113fdf55b9bd51b0a542765540eb3489c5a5d5f7685bece7d45b635627be
translation: machine
translated_at: '2026-10-24'
---
# Fonctionnement interne du rendu React {#react-rendering-internals}

Comprendre le fonctionnement du rendu React permet d'écrire des applications performantes. React utilise un Virtual DOM et une architecture Fiber pour minimiser les opérations sur le DOM réel.

## Virtual DOM {#virtual-dom}

1. Le composant renvoie du JSX -> arbre du Virtual DOM (objets JS légers)
2. Changement d'état ou de props -> nouvel arbre du Virtual DOM
3. **Diffing** : comparaison du nouvel arbre avec le précédent
4. **Réconciliation** : calcul des opérations DOM minimales
5. **Commit** : application des changements par lot

## Architecture Fiber {#fiber-architecture}

Chaque élément possède un nœud Fiber contenant son type, ses props, une référence au DOM, des liens vers le parent, l'enfant et le frère, son état, ainsi que des métadonnées d'ordonnancement.

### Rendu en deux phases {#two-phase-rendering}

**Phase de rendu** (interruptible) : parcourt l'arbre, appelle les composants, compare les sorties. Aucune mutation du DOM. Peut être mise en pause puis relancée.

**Phase de commit** (synchrone) : applique les mutations du DOM, exécute `useLayoutEffect` (synchrone, bloque l'affichage), le navigateur affiche la page, puis exécute `useEffect` (asynchrone).

### Cycle de vie des composants (Hooks) {#component-lifecycle-hooks}
```sql
Mount:  render -> DOM update -> useLayoutEffect -> paint -> useEffect
Update: re-render -> diff -> DOM update -> layout cleanup/run -> paint -> effect cleanup/run
Unmount: layout cleanup -> effect cleanup -> DOM removal
```

## Quand les composants se re-rendent {#when-components-re-render}

1. Leur **état** change (setState)
2. Leur **parent** se re-rend (même si les props n'ont pas changé !)
3. La valeur de leur **contexte** change

Un composant ne se re-rend PAS « parce que les props ont changé » : il se re-rend parce que son parent s'est re-rendu.

## Éviter les re-rendus inutiles {#preventing-unnecessary-re-renders}

### React.memo {#reactmemo}
```jsx
const ExpensiveChild = React.memo(function({ data }) {
  return <div>{data.name}</div>;
});
// Only re-renders if 'data' prop changes (shallow comparison)
```

### useMemo (mise en cache de valeurs) {#usememo-cache-values}
```jsx
const sorted = useMemo(() =>
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### useCallback (mise en cache de fonctions) {#usecallback-cache-functions}
```jsx
const handleClick = useCallback(() => {
  setCount(c => c + 1);
}, []);
// Same reference across renders -> memo'd child won't re-render
```

**Quand l'utiliser** : uniquement lorsqu'un problème a été mesuré. Profilez d'abord avec le Profiler de React DevTools. Une mémoïsation prématurée ajoute de la complexité.

## Approfondissement de la prop key {#key-prop-deep-dive}

```jsx
// GOOD: stable unique ID
{items.map(item => <Item key={item.id} data={item} />)}

// BAD: index (breaks on reorder/delete)
{items.map((item, i) => <Item key={i} data={item} />)}
```

**Astuce de réinitialisation par key** : modifier la key force un démontage puis un remontage (réinitialise tout l'état) :
```jsx
<UserForm key={userId} userId={userId} />
```

## Mises à jour par lot (React 18) {#batch-updates-react-18}

React 18 regroupe TOUTES les mises à jour d'état, y compris les asynchrones :
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

Forcer la synchronisation : `flushSync(() => setState(v))` (rare).

## Frameworks React {#react-frameworks}

React est une bibliothèque (couche de vue uniquement). Choisissez séparément le routage, la gestion d'état et la récupération des données, ou utilisez un framework :

- **Next.js** : SSR, SSG, routage basé sur les fichiers, routes API (le plus populaire)
- **Remix** : routage imbriqué, amélioration progressive
- **Gatsby** : génération statique, GraphQL

En production : utilisez un framework. Pour l'apprentissage ou de petites SPA : Vite + React.

## Composants à classe (legacy) {#class-components-legacy}

```jsx
class Counter extends React.Component {
  state = { count: 0 };
  componentDidMount() { }
  componentDidUpdate() { }
  componentWillUnmount() { }
  render() { return <p>{this.state.count}</p>; }
}
```

Tout nouveau code devrait utiliser des composants fonctionnels avec des hooks.

## Pièges courants {#gotchas}

- **Re-rendu du parent = re-rendu de l'enfant** : même avec des props inchangées, sauf s'il est encapsulé dans `React.memo`
- **Les props objet ou fonction annulent le memo** : `<Child data={{...}}/>` crée une nouvelle référence à chaque rendu
- **useMemo/useCallback ne sont pas gratuits** : la mémoïsation consomme de la mémoire ; mesurez d'abord
- **Double rendu en StrictMode** : uniquement en développement, permet de détecter les rendus impurs
- **Moment d'exécution des effets** : `useEffect` s'exécute après l'affichage, `useLayoutEffect` bloque l'affichage (à utiliser pour les mesures du DOM)
- **Clés basées sur l'index** : l'état peut rester attaché aux mauvais éléments lorsque la liste est réordonnée

## Voir aussi {#see-also}

- [[react-components-and-jsx]] - Composants, props, bases du JSX
- [[react-state-and-hooks]] - Gestion d'état, useEffect
- [[react-styling-approaches]] - CSS Modules, Tailwind
- [[frontend-build-systems]] - Vite, webpack pour les applications React
