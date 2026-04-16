---
title: JavaScript DOM and Events
category: concepts
tags: [web-frontend, javascript, dom, events, localstorage]
---

# JavaScript DOM and Events

The DOM (Document Object Model) is a tree representation of HTML. JavaScript reads and modifies it to create dynamic, interactive pages.

## Selecting Elements

```javascript
document.getElementById("header")                   // Single or null
document.querySelector(".card")                      // First match (any CSS selector)
document.querySelectorAll(".card")                   // Static NodeList of all matches
document.getElementsByClassName("card")              // Live HTMLCollection
```

`querySelector` is most flexible (any CSS selector). `getElementsBy...` returns live collections.

### Traversing
```javascript
element.parentElement
element.children                   // Direct children (HTMLCollection)
element.firstElementChild
element.lastElementChild
element.nextElementSibling
element.previousElementSibling
element.closest(".container")      // Nearest ancestor matching selector
```

## Modifying Elements

### Text and HTML
```javascript
element.textContent = "Text";         // Safe (no HTML parsing)
element.innerHTML = "<b>Bold</b>";    // Parses HTML (XSS risk with user input!)
```

### Attributes
```javascript
element.getAttribute("href")
element.setAttribute("href", "/new")
element.removeAttribute("href")
element.dataset.userId                // data-user-id (camelCase)
```

### Classes
```javascript
element.classList.add("active")
element.classList.remove("active")
element.classList.toggle("active")
element.classList.contains("active")
element.classList.replace("old", "new")
```

### Inline Styles
```javascript
element.style.backgroundColor = "red";
element.style.display = "none";
getComputedStyle(element).fontSize     // Computed value
```

**Prefer `classList` over `style`** for toggling states. Define styles in CSS, toggle classes in JS.

## Creating and Removing

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

### insertAdjacentHTML Positions
```php
beforebegin -> [element] -> afterbegin ... beforeend -> [/element] -> afterend
```

## Events

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

### Common Events
| Event | When |
|-------|------|
| `click`, `dblclick` | Mouse click |
| `mouseenter`/`mouseleave` | Enter/leave (no bubble) |
| `keydown`/`keyup` | Keyboard |
| `input` | Value changes (real-time) |
| `change` | Value changes (on blur/commit) |
| `submit` | Form submitted |
| `focus`/`blur` | Focus gained/lost |
| `scroll`, `resize` | Scroll/resize |
| `DOMContentLoaded` | HTML parsed |
| `load` | Everything loaded |

### Keyboard Events
```javascript
document.addEventListener("keydown", (e) => {
  e.key       // "Enter", "Escape", "a"
  e.code      // "KeyA", "Space" (physical key)
  e.ctrlKey   // Ctrl held?
  e.shiftKey  // Shift held?
});
```

## Event Bubbling and Delegation

Events propagate: **Capturing** (top-down) -> **Target** -> **Bubbling** (bottom-up, default).

### Event Delegation
One listener on parent instead of many on children:

```javascript
document.querySelector(".list").addEventListener("click", (e) => {
  if (e.target.matches(".list-item")) {
    console.log("Item:", e.target.textContent);
  }
});
```

**Benefits**: works for dynamically added elements, fewer listeners, simpler code.

## localStorage and sessionStorage

```javascript
localStorage.setItem("theme", "dark");
localStorage.setItem("user", JSON.stringify({ name: "Alice" }));

localStorage.getItem("theme")                    // "dark"
JSON.parse(localStorage.getItem("user"))         // { name: "Alice" }

localStorage.removeItem("theme");
localStorage.clear();
```

| Feature | localStorage | sessionStorage |
|---------|-------------|----------------|
| Persists | Until cleared | Until tab closes |
| Scope | All tabs (same origin) | Same tab only |
| Size | ~5MB | ~5MB |

Always `JSON.stringify()` objects when storing, `JSON.parse()` when retrieving.

## FormData API

```javascript
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  fd.get("email");
  const data = Object.fromEntries(fd);

  fetch("/api", { method: "POST", body: fd });
});
```

## Gotchas

- **`innerHTML` XSS**: never insert user input via `innerHTML`; use `textContent`
- **Live vs static collections**: `getElementsBy...` is live (auto-updates), `querySelectorAll` is static
- **`DOMContentLoaded` vs `load`**: first fires when HTML parsed, second when all resources loaded
- **`event.target` vs `currentTarget`**: target = what was clicked, currentTarget = where listener is
- **`innerHTML = ""` destroys listeners**: child event listeners are lost; re-attach or use delegation
- **localStorage is synchronous**: blocks main thread for large data

## See Also

- [[html-tables-and-forms]] - Form elements and validation
- [[js-async-and-fetch]] - Fetch API for network requests
- [[react-components-and-jsx]] - React's virtual DOM approach
- [[js-scope-closures-this]] - Event handler `this` binding
