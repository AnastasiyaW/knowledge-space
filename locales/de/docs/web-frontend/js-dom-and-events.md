---
title: "JavaScript DOM und Events"
category: concepts
tags: [web-frontend, javascript, dom, events, localstorage]
level: 3
source_sha256: 331caa20fd06d4d326418226279ba3b24d8fd81b793779c57b779e7d176e6c23
translation: machine
translated_at: '2026-10-24'
---
# JavaScript DOM und Events {#javascript-dom-and-events}

Das DOM (Document Object Model) ist eine Baumdarstellung von HTML. JavaScript liest und verändert diesen Baum, um dynamische, interaktive Seiten zu erstellen.

## Elemente auswählen {#selecting-elements}

```javascript
document.getElementById("header")                   // Single or null
document.querySelector(".card")                      // First match (any CSS selector)
document.querySelectorAll(".card")                   // Static NodeList of all matches
document.getElementsByClassName("card")              // Live HTMLCollection
```

`querySelector` ist am flexibelsten (beliebiger CSS-Selektor). `getElementsBy...` liefert Live-Collections zurück.

### Traversieren {#traversing}
```javascript
element.parentElement
element.children                   // Direct children (HTMLCollection)
element.firstElementChild
element.lastElementChild
element.nextElementSibling
element.previousElementSibling
element.closest(".container")      // Nearest ancestor matching selector
```

## Elemente verändern {#modifying-elements}

### Text und HTML {#text-and-html}
```javascript
element.textContent = "Text";         // Safe (no HTML parsing)
element.innerHTML = "<b>Bold</b>";    // Parses HTML (XSS risk with user input!)
```

### Attribute {#attributes}
```javascript
element.getAttribute("href")
element.setAttribute("href", "/new")
element.removeAttribute("href")
element.dataset.userId                // data-user-id (camelCase)
```

### Klassen {#classes}
```javascript
element.classList.add("active")
element.classList.remove("active")
element.classList.toggle("active")
element.classList.contains("active")
element.classList.replace("old", "new")
```

### Inline-Styles {#inline-styles}
```javascript
element.style.backgroundColor = "red";
element.style.display = "none";
getComputedStyle(element).fontSize     // Computed value
```

**Bevorzuge `classList` gegenüber `style`** beim Umschalten von Zuständen. Definiere Styles in CSS und schalte Klassen in JS um.

## Erstellen und Entfernen {#creating-and-removing}

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

### insertAdjacentHTML-Positionen {#insertadjacenthtml-positions}
```php
beforebegin -> [element] -> afterbegin ... beforeend -> [/element] -> afterend
```

## Events {#events}

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

### Häufige Events {#common-events}
| Event | Wann |
|-------|------|
| `click`, `dblclick` | Mausklick |
| `mouseenter`/`mouseleave` | Betreten/Verlassen (ohne Bubbling) |
| `keydown`/`keyup` | Tastatur |
| `input` | Wertänderung (in Echtzeit) |
| `change` | Wertänderung (bei Blur/Bestätigung) |
| `submit` | Formular abgeschickt |
| `focus`/`blur` | Fokus erhalten/verloren |
| `scroll`, `resize` | Scrollen/Größenänderung |
| `DOMContentLoaded` | HTML geparst |
| `load` | Alles geladen |

### Tastatur-Events {#keyboard-events}
```javascript
document.addEventListener("keydown", (e) => {
  e.key       // "Enter", "Escape", "a"
  e.code      // "KeyA", "Space" (physical key)
  e.ctrlKey   // Ctrl held?
  e.shiftKey  // Shift held?
});
```

## Event-Bubbling und Delegation {#event-bubbling-and-delegation}

Events werden weitergeleitet: **Capturing** (von oben nach unten) -> **Target** -> **Bubbling** (von unten nach oben, Standard).

### Event-Delegation {#event-delegation}
Ein Listener am Elternelement statt vieler an den Kindelementen:

```javascript
document.querySelector(".list").addEventListener("click", (e) => {
  if (e.target.matches(".list-item")) {
    console.log("Item:", e.target.textContent);
  }
});
```

**Vorteile**: funktioniert für dynamisch hinzugefügte Elemente, weniger Listener, einfacherer Code.

## localStorage und sessionStorage {#localstorage-and-sessionstorage}

```javascript
localStorage.setItem("theme", "dark");
localStorage.setItem("user", JSON.stringify({ name: "Alice" }));

localStorage.getItem("theme")                    // "dark"
JSON.parse(localStorage.getItem("user"))         // { name: "Alice" }

localStorage.removeItem("theme");
localStorage.clear();
```

| Merkmal | localStorage | sessionStorage |
|---------|-------------|----------------|
| Persistenz | Bis zum Löschen | Bis der Tab geschlossen wird |
| Geltungsbereich | Alle Tabs (gleicher Origin) | Nur derselbe Tab |
| Größe | ~5 MB | ~5 MB |

Objekte immer mit `JSON.stringify()` speichern und mit `JSON.parse()` auslesen.

## FormData-API {#formdata-api}

```javascript
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  fd.get("email");
  const data = Object.fromEntries(fd);

  fetch("/api", { method: "POST", body: fd });
});
```

## Stolperfallen {#gotchas}

- **`innerHTML` und XSS**: Benutzereingaben niemals über `innerHTML` einfügen; stattdessen `textContent` verwenden
- **Live- vs. statische Collections**: `getElementsBy...` ist live (aktualisiert sich automatisch), `querySelectorAll` ist statisch
- **`DOMContentLoaded` vs. `load`**: Ersteres feuert, sobald das HTML geparst ist, Letzteres, wenn alle Ressourcen geladen sind
- **`event.target` vs. `currentTarget`**: target = das, was angeklickt wurde; currentTarget = das Element, an dem der Listener hängt
- **`innerHTML = ""` entfernt Listener**: Event-Listener der Kindelemente gehen verloren; neu anhängen oder Delegation verwenden
- **localStorage ist synchron**: blockiert den Hauptthread bei großen Datenmengen

## Siehe auch {#see-also}

- [[html-tables-and-forms]] - Formularelemente und Validierung
- [[js-async-and-fetch]] - Fetch-API für Netzwerkanfragen
- [[react-components-and-jsx]] - Reacts Ansatz mit dem Virtual DOM
- [[js-scope-closures-this]] - Bindung von `this` in Event-Handlern
