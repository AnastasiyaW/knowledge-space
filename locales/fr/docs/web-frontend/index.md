---
title: "Développement web frontend"
type: MOC
level: 2
source_sha256: d74a8da3833c91c5825b91fd822554b25f350cd8a67a1c203426f760d1d7952c
translation: machine
translated_at: '2026-10-24'
---
# Développement web frontend {#web-frontend}

Base de connaissances de référence pour HTML, CSS, JavaScript, TypeScript, React, les outils de build et le design Figma.

## HTML {#html}

La fondation structurelle du contenu web, de la structure du document aux formulaires et à l'accessibilité.

- [[html-fundamentals]] - Structure du document, éléments sémantiques, images, liens, bloc vs inline
- [[html-tables-and-forms]] - Tableaux, champs de formulaire, validation, labels, patterns d'accessibilité

## CSS Core {#css-core}

Mise en forme, mise en page et présentation visuelle du contenu web.

- [[css-selectors-and-cascade]] - Sélecteurs, spécificité, héritage, couleurs, typographie, propriétés personnalisées
- [[css-box-model-and-layout]] - Box model, border-box, display, position, z-index, unités, arrière-plans
- [[css-flexbox]] - Layout 1D : direction, justify, align, grow/shrink/basis, patterns courants
- [[css-grid]] - Layout 2D : template columns/rows, areas, auto-fit/fill, minmax, subgrid
- [[css-responsive-design]] - Media queries, unités viewport, clamp(), images responsives, mobile-first
- [[css-animation-and-transforms]] - Transitions, transformations, keyframes, filtres, performance GPU
- [[css-sass-and-methodology]] - Nommage BEM, SMACSS, prétraitement SASS/SCSS, organisation des fichiers

## JavaScript {#javascript}

Fonctionnalités核心 du langage, depuis les variables et les types jusqu'à la programmation asynchrone.

- [[js-variables-and-types]] - let/const/var, types primitifs, typeof, coercition, truthy/falsy
- [[js-control-flow]] - Conditions, égalité stricte, opérateurs logiques, optional chaining, boucles
- [[js-strings-and-numbers]] - Méthodes String/Number, Math, virgule flottante, bases des expressions régulières
- [[js-functions]] - Déclarations, fonctions fléchées, paramètres, fonctions d'ordre supérieur, callbacks, fonctions pures
- [[js-scope-closures-this]] - Chaîne de portée, hoisting, closures, règles de liaison de this, mode strict
- [[js-arrays]] - Méthodes mutantes et non mutantes, map/filter/reduce, déstructuration, spread, chaînage
- [[js-objects-and-data]] - Objets, déstructuration, spread, JSON, Date, Symbol
- [[js-dom-and-events]] - Sélection et modification du DOM, événements, délégation, localStorage, FormData
- [[js-async-and-fetch]] - Event loop, Promises, async/await, API Fetch, gestion des erreurs

## TypeScript {#typescript}

Système de types statique pour JavaScript, des bases à la programmation avancée au niveau des types.

- [[typescript-fundamentals]] - Types de base, interfaces, unions, génériques, narrowing, typage structurel
- [[typescript-advanced]] - Utility types, types conditionnels, types mappés, branded types, Zod, typage React

## React {#react}

Bibliothèque d'interfaces basée sur des composants, avec des hooks pour la gestion d'état et les effets de bord.

- [[react-components-and-jsx]] - Règles JSX, composants, props, children, composition, rendu conditionnel
- [[react-state-and-hooks]] - useState, useEffect, useRef, hooks personnalisés, gestion des événements
- [[react-rendering-internals]] - Virtual DOM, Fiber, déclencheurs de re-rendu, memo/useMemo/useCallback, keys
- [[react-styling-approaches]] - CSS Modules (styles scopés), Tailwind CSS (utility-first)

## Build Tooling {#build-tooling}

Gestion de paquets, bundling et optimisation pour la production.

- [[npm-and-task-runners]] - npm, package.json, node_modules, Gulp, CLI SASS
- [[frontend-build-systems]] - Webpack/Vite/Rollup, transpilation, tree-shaking, code splitting, source maps
- [[git-and-github]] - Gestion de versions, branchement, fusion, PRs, workflows de collaboration

## Figma Design {#figma-design}

Outil de design UI/UX pour créer des maquettes, prototypes et design systems.

- [[figma-fundamentals]] - Interface, frames, grilles, calques, formes, export, partage
- [[figma-layout-and-components]] - AutoLayout, contraintes, composants, variants, design systems
- [[figma-design-workflow]] - Typographie, couleur, effets, prototypage, design responsive, wireframes

## Additional References {#additional-references}

- [[3d-browser-libs-for-video]] - Comparaison de Three.js, React Three Fiber, Spline, Lottie et d'autres bibliothèques 3D/animation pour
- [[dom-free-text-layout]] - Mesure et mise en page du texte sans déclencher de reflow du DOM par le navigateur
- [[javascript-async-event-loop]] - Référence complète de la programmation asynchrone en JavaScript - des callbacks jusqu'à
- [[javascript-concurrency-primitives]] - Coordination asynchrone avancée en JavaScript - sémaphores, mutex, files/pools asynchrones, workers
- [[remotion-programmatic-video]] - Créer des démos produit, vidéos marketing et pitch decks sous forme de composants React - rendu en MP4 avec
- [[video-motion-design-rules]] - Valeurs concrètes pour le timing, les easings, les niveaux audio, la composition et le storytelling dans les vidéos produit
