---
title: JavaScript DOM and Events
category: javascript
tags: [javascript, dom, events, event-delegation, event-bubbling, dom-manipulation]
---

# JavaScript DOM and Events

## Key Facts

- **DOM** (Document Object Model) is a tree of nodes representing the HTML document
- `document.querySelector(css)` returns first match; `querySelectorAll(css)` returns `NodeList`
- `element.textContent` for text (escapes HTML); `element.innerHTML` for HTML (XSS risk with user input)
- `element.classList.add/remove/toggle/contains()` for CSS class manipulation
- **Event bubbling**: events propagate from target element up to `document`; capture phase goes top-down
- **Event delegation**: attach single listener to parent, use `event.target` to identify source
- `event.preventDefault()` stops default behavior (form submit, link navigation)
- `event.stopPropagation()` stops event from bubbling up
- `addEventListener(type, fn, { once: true })` auto-removes listener after first fire
- `MutationObserver` watches DOM changes without polling; `IntersectionObserver` detects visibility
- Related: [[javascript-fundamentals]], [[javascript-async-and-promises]]

## Patterns

### Selecting and Modifying Elements

```javascript
const btn = document.querySelector(".submit-btn");
const items = document.querySelectorAll(".item");

// Modify
btn.textContent = "Submit";
btn.setAttribute("disabled", "");
btn.style.setProperty("--color", "blue"); // CSS custom property

// Create and append
const div = document.createElement("div");
div.className = "card";
div.innerHTML = `<h3>${title}</h3><p>${text}</p>`;
document.querySelector(".container").append(div);
```

### Event Delegation

```javascript
// Instead of adding listener to each <li>
document.querySelector("ul").addEventListener("click", (e) => {
  const li = e.target.closest("li"); // find nearest <li> ancestor
  if (!li) return;
  li.classList.toggle("selected");
});
```

### Form Handling

```javascript
const form = document.querySelector("form");
form.addEventListener("submit", (e) => {
  e.preventDefault(); // stop page reload

  const formData = new FormData(form);
  const data = Object.fromEntries(formData);
  // { name: "Ana", email: "ana@..." }

  fetch("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
});
```

### IntersectionObserver (Lazy Loading / Animations)

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target); // stop observing after trigger
      }
    });
  },
  { threshold: 0.1 } // trigger when 10% visible
);

document.querySelectorAll(".animate-on-scroll").forEach((el) => {
  observer.observe(el);
});
```

### Debounce and Throttle

```javascript
function debounce(fn, ms = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

const handleSearch = debounce((query) => {
  fetch(`/api/search?q=${encodeURIComponent(query)}`);
}, 300);

input.addEventListener("input", (e) => handleSearch(e.target.value));
```

## Gotchas

- `querySelectorAll` returns a static `NodeList`, not live; `getElementsByClassName` returns live `HTMLCollection`
- `innerHTML = userInput` is an XSS vector; use `textContent` or sanitize with DOMPurify
- Event listeners on removed DOM elements can cause memory leaks; use `AbortController` signal or `removeEventListener`
- `click` event on touch devices has 300ms delay (for double-tap zoom); use `touchend` or `pointer` events for instant response
- `event.currentTarget` is the element with the listener; `event.target` is the actual clicked element (different with delegation)

## See Also

- [MDN: DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)
- [MDN: Event reference](https://developer.mozilla.org/en-US/docs/Web/Events)
