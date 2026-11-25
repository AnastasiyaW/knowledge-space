---
title: "Automatisation de tests navigateur avec Geb/Groovy (Selenium)"
category: concepts
tags: [testing, selenium, groovy, geb, browser-automation, webdriver]
level: 3
source_sha256: 70418b16b38ae85b62d6bf6a39abd040fa32464842644b2fed066c7c0116a615
translation: machine
translated_at: '2026-10-24'
---
# Automatisation de tests navigateur avec Geb/Groovy (Selenium) {#browser-test-automation-with-gebgroovy-selenium}

Geb est une bibliothèque Groovy construite au-dessus de Selenium WebDriver pour l'automatisation des tests navigateur. Elle couvre la recherche d'éléments, les interactions, l'attente, les boîtes de dialogue, les iframes, le glisser-déposer et les schémas complets de flux de test.

## Points clés {#key-facts}

- La version de ChromeDriver doit correspondre au navigateur Chrome installé ; le SDK v25+ gère cette correspondance automatiquement
- Chaque script s'exécute dans un bloc `Browser.drive { ... }`
- `find()` localise les éléments par balise, attributs ou sélecteurs CSS
- L'opérateur `<<` saisit du texte dans les champs ; `.click()` clique sur les éléments
- `waitFor(timeout)` interroge jusqu'à ce que la condition soit vraie - toujours privilégier cette méthode à `Thread.sleep`
- `withFrame(iframe) { ... }` et `withWindow(condition) { ... }` pour changer de contexte

## Modèles {#patterns}

### Structure de base {#basic-structure}

```groovy
import geb.Browser

Browser.drive {
    go "https://example.com"
    assert page.title == "Expected Title"
    assert currentUrl.contains("/dashboard")
}
```

### Recherche d'éléments {#finding-elements}

```groovy
find("a", text: "Link Text")            // by tag + text
find("input", placeholder: "Search")    // by placeholder
find("input", id: "username")           // by id
find("div", class: "container")         // by class
find("#main-content")                   // CSS selector
find(".btn-primary")                    // CSS class
find("table tr", 2)                    // nth match (0-indexed)
```

### Interaction {#interaction}

```groovy
find("a", text: "Click Me").click()
find("input", placeholder: "Name") << "John"   // type text
find("input", placeholder: "Name").value()      // read value
find("input", placeholder: "Name").value("New") // set value
```

### Raccourcis clavier {#keyboard-shortcuts}

```groovy
import org.openqa.selenium.Keys

find("input") << Keys.chord(Keys.CONTROL, "A")  // select all
find("input") << Keys.BACK_SPACE                 // delete
find("input") << Keys.ENTER
find("input") << Keys.chord(Keys.CONTROL, "C")  // copy
```

### Éléments de formulaire {#form-elements}

```groovy
import geb.module.Checkbox
import geb.module.Select
import geb.module.FileInput

// Checkbox
def cb = find("input", type: "checkbox").module(Checkbox)
cb.check()        // tick
cb.uncheck()      // untick
cb.checked        // true if checked

// Radio button (click label, more reliable)
find("label", for: "radioButtonId").click()

// Dropdown
def dd = find("select", id: "country").module(Select)
dd.selected = "United States"
dd.selectedText   // current display text

// File upload
find("input", type: "file").module(FileInput).file = new File("/path/to/file.png")
```

### Attente {#waiting}

```groovy
// Prefer waitFor over Thread.sleep
waitFor(15) { find("button", text: "Done").size() == 1 }

// Multiple conditions
waitFor(15) {
    assert find("div", text: "Success").size() == 1
    find("div", class: "loading").size() == 0  // last line = return value
}
```

`waitFor` lève une exception `WaitTimeoutException` si la condition n'est pas remplie.

### Boîtes de dialogue alert et confirm {#alert-and-confirm-dialogs}

```groovy
// Alert (OK only)
def msg = withAlert(wait: true) {
    find("button", id: "trigger-alert").click()
}

// Confirm - accept (true) or dismiss (false)
def msg = withConfirm(true, wait: true) {
    find("button", id: "trigger-confirm").click()
}
```

### iFrames et fenêtres {#iframes-and-windows}

```groovy
// iFrame
withFrame(find("iframe", id: "frame-id")) {
    find("button", text: "Inside Frame").click()
}

// New window/tab
withWindow({ getDriver().windowHandles.size() == 2 }) {
    assert page.title == "New Window Title"
}
```

### Défilement, survol, glisser-déposer {#scrolling-hovering-drag-and-drop}

```groovy
interact { moveToElement(find("div", id: "target")) }   // scroll into view
interact { moveToElement(find("div", class: "hover-trigger")) }  // hover

interact {
    dragAndDrop(find("div", id: "draggable"), find("div", id: "droptarget"))
}
```

### Flux de connexion complet {#complete-login-flow}

```groovy
Browser.drive {
    go "https://app.example.com/login"
    find("input", id: "email") << "user@example.com"
    find("input", id: "password") << "securepassword"
    find("button", text: "Sign In").click()
    waitFor(10) { currentUrl.contains("/dashboard") }
    assert find("h1", text: "Dashboard").size() == 1
}
```

## Pièges courants {#gotchas}

- **Élément obsolète (stale element)** : si le DOM est mis à jour après `find()`, la référence à l'élément devient invalide - rappeler `find()`
- **Élément non interactif** : l'élément existe mais est masqué ou recouvert - utiliser d'abord `interact { moveToElement(...) }`
- **Incompatibilité de ChromeDriver** : mettre à jour le pilote lorsque Chrome se met à jour automatiquement
- **Blocage par une alerte** : si une alerte est ouverte, toutes les autres commandes WebDriver échouent - traiter les alertes en premier
- **`Thread.sleep` vs `waitFor`** : `waitFor` se termine dès que la condition est vraie (plus rapide) et est plus fiable

## Voir aussi {#see-also}

- [[web-scraping]] - approche alternative de scraping pour les pages sans JavaScript
- [[ai-agent-ide-features]] - sous-agents navigateur pour les tests automatisés
