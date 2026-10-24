---
title: "DOM et événements en JavaScript"
category: concepts
tags: [web-frontend, javascript, dom, events, localstorage]
level: 3
source_sha256: 331caa20fd06d4d326418226279ba3b24d8fd81b793779c57b779e7d176e6c23
translation: machine
translated_at: '2026-10-24'
---
# DOM et événements en JavaScript {#javascript-dom-and-events}

Le DOM (Document Object Model) est une représentation arborescente du HTML. JavaScript le lit et le modifie pour créer des pages dynamiques et interactives.

## Sélection d'éléments {#selecting-elements}

```javascript
document.getElementById("header")                   // Single or null
document.querySelector(".card")                      // First match (any CSS selector)
document.querySelectorAll(".card")                   // Static NodeList of all matches
document.getElementsByClassName("card")              // Live HTMLCollection
```

`querySelector` est la méthode la plus souple (n'importe quel sélecteur CSS). `getElementsBy...` renvoie des collections dynamiques (live).

### Parcours de l'arbre {#traversing}
```javascript
element.parentElement
element.children                   // Direct children (HTMLCollection)
element.firstElementChild
element.lastElementChild
element.nextElementSibling
element.previousElementSibling
element.closest(".container")      // Nearest ancestor matching selector
```

## Modification des éléments {#modifying-elements}

### Texte et HTML {#text-and-html}
```javascript
element.textContent = "Text";         // Safe (no HTML parsing)
element.innerHTML = "<b>Bold</b>";    // Parses HTML (XSS risk with user input!)
```

### Attributs {#attributes}
```javascript
element.getAttribute("href")
element.setAttribute("href", "/new")
element.removeAttribute("href")
element.dataset.userId                // data-user-id (camelCase)
```

### Classes {#classes}
```javascript
element.classList.add("active")
element.classList.remove("active")
element.classList.toggle("active")
element.classList.contains("active")
element.classList.replace("old", "new")
```

### Styles en ligne {#inline-styles}
```javascript
element.style.backgroundColor = "red";
element.style.display = "none";
getComputedStyle(element).fontSize     // Computed value
```

**Privilégiez `classList` à `style`** pour basculer entre des états. Définissez les styles en CSS et basculez les classes en JS.

## Création et suppression {#creating-and-removing}

```javascript
const div = document.createElement("div");
div.textContent = "Hello";
div.classList.add("card");

parent.appendChild(child)              // Last child
parent.prepend(child)                   // First child
element.after(newEl)                    // After
element.before(newEl)                   // Before
parent.insertAdjacentHTML("beforeend", "<div>HTML</div>")

element.remove()                        // Remove from DOM
const clone = element.cloneNode(true)  // Deep clone
```

### Positions de insertAdjacentHTML {#insertadjacenthtml-positions}
```php
beforebegin -> [element] -> afterbegin ... beforeend -> [/element] -> afterend
```

## Événements {#events}

```javascript
element.addEventListener("click", (event) => {
  event.target           // Element that triggered
  event.currentTarget    // Element listener is on
  event.preventDefault() // Stop default (link, form submit)
  event.stopPropagation() // Stop bubbling
});

// Remove (must reference same function)
const handler = (e) => console.log(e);
element.addEventListener("click", handler);
element.removeEventListener("click", handler);
```

### Événements courants {#common-events}
| Événement | Quand |
|-------|------|
| `click`, `dblclick` | Clic de souris |
| `mouseenter`/`mouseleave` | Entrée/sortie (sans bubbling) |
| `keydown`/`keyup` | Clavier |
| `input` | Changement de valeur (en temps réel) |
| `change` | Changement de valeur (à la perte du focus ou à la validation) |
| `submit` | Formulaire soumis |
| `focus`/`blur` | Focus obtenu/perdu |
| `scroll`, `resize` | Défilement/redimensionnement |
| `DOMContentLoaded` | HTML analysé |
| `load` | Tout chargé |

### Événements clavier {#keyboard-events}
```javascript
document.addEventListener("keydown", (e) => {
  e.key       // "Enter", "Escape", "a"
  e.code      // "KeyA", "Space" (physical key)
  e.ctrlKey   // Ctrl held?
  e.shiftKey  // Shift held?
});
```

## Propagation et délégation d'événements {#event-bubbling-and-delegation}

Les événements se propagent : **capture** (de haut en bas) -> **cible** -> **bubbling** (de bas en haut, par défaut).

### Délégation d'événements {#event-delegation}
Un seul écouteur sur le parent plutôt qu'un écouteur par enfant :

```javascript
document.querySelector(".list").addEventListener("click", (e) => {
  if (e.target.matches(".list-item")) {
    console.log("Item:", e.target.textContent);
  }
});
```

**Avantages** : fonctionne pour les éléments ajoutés dynamiquement, moins d'écouteurs, code plus simple.

## localStorage et sessionStorage {#localstorage-and-sessionstorage}

```javascript
localStorage.setItem("theme", "dark");
localStorage.setItem("user", JSON.stringify({ name: "Alice" }));

localStorage.getItem("theme")                    // "dark"
JSON.parse(localStorage.getItem("user"))         // { name: "Alice" }

localStorage.removeItem("theme");
localStorage.clear();
```

| Fonctionnalité | localStorage | sessionStorage |
|---------|-------------|----------------|
| Persistance | Jusqu'à effacement | Jusqu'à la fermeture de l'onglet |
| Portée | Tous les onglets (même origine) | Uniquement l'onglet courant |
| Taille | ~5 Mo | ~5 Mo |

Sérialisez toujours les objets avec `JSON.stringify()` lors de l'enregistrement, et désérialisez-les avec `JSON.parse()` lors de la lecture.

## FormData API {#formdata-api}

```javascript
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  fd.get("email");
  const data = Object.fromEntries(fd);

  fetch("/api", { method: "POST", body: fd });
});
```

## Pièges courants {#gotchas}

- **XSS via `innerHTML`** : n'insérez jamais de saisie utilisateur avec `innerHTML` ; utilisez `textContent`
- **Collections dynamiques ou statiques** : `getElementsBy...` est dynamique (mise à jour automatique), `querySelectorAll` est statique
- **`DOMContentLoaded` vs `load`** : le premier se déclenche lorsque le HTML est analysé, le second lorsque toutes les ressources sont chargées
- **`event.target` vs `currentTarget`** : target = l'élément cliqué, currentTarget = l'élément auquel l'écouteur est attaché
- **`innerHTML = ""` détruit les écouteurs** : les écouteurs des enfants sont perdus ; rattachez-les ou utilisez la délégation
- **localStorage est synchrone** : il bloque le thread principal pour les volumes de données importants

## Voir aussi {#see-also}

- [[html-tables-and-forms]] - Éléments de formulaire et validation
- [[js-async-and-fetch]] - API Fetch pour les requêtes réseau
- [[react-components-and-jsx]] - L'approche DOM virtuel de React
- [[js-scope-closures-this]] - Liaison de `this` dans les gestionnaires d'événements
