---
title: "Browser-Testautomatisierung mit Geb/Groovy (Selenium)"
category: concepts
tags: [testing, selenium, groovy, geb, browser-automation, webdriver]
level: 3
source_sha256: 70418b16b38ae85b62d6bf6a39abd040fa32464842644b2fed066c7c0116a615
translation: machine
translated_at: '2026-10-24'
---
# Browser-Testautomatisierung mit Geb/Groovy (Selenium) {#browser-test-automation-with-gebgroovy-selenium}

Geb ist eine Groovy-Bibliothek auf Basis von Selenium WebDriver für die Browser-Testautomatisierung. Behandelt werden das Finden von Elementen, Interaktion, Warten, Dialoge, iFrames, Drag-and-Drop und vollständige Testablaufmuster.

## Wichtige Fakten {#key-facts}

- Die ChromeDriver-Version muss zum installierten Chrome-Browser passen; ab SDK v25 erfolgt die Zuordnung automatisch
- Jedes Skript läuft innerhalb eines `Browser.drive { ... }`-Blocks
- `find()` lokalisiert Elemente anhand von Tag, Attributen oder CSS-Selektoren
- Der `<<`-Operator gibt Text in Eingabefelder ein; `.click()` klickt Elemente an
- `waitFor(timeout)` fragt wiederholt ab, bis die Bedingung erfüllt ist – immer `Thread.sleep` vorziehen
- `withFrame(iframe) { ... }` und `withWindow(condition) { ... }` zum Wechseln des Kontexts

## Muster {#patterns}

### Grundstruktur {#basic-structure}

```groovy
import geb.Browser

Browser.drive {
    go "https://example.com"
    assert page.title == "Expected Title"
    assert currentUrl.contains("/dashboard")
}
```

### Elemente finden {#finding-elements}

```groovy
find("a", text: "Link Text")            // by tag + text
find("input", placeholder: "Search")    // by placeholder
find("input", id: "username")           // by id
find("div", class: "container")         // by class
find("#main-content")                   // CSS selector
find(".btn-primary")                    // CSS class
find("table tr", 2)                    // nth match (0-indexed)
```

### Interaktion {#interaction}

```groovy
find("a", text: "Click Me").click()
find("input", placeholder: "Name") << "John"   // type text
find("input", placeholder: "Name").value()      // read value
find("input", placeholder: "Name").value("New") // set value
```

### Tastenkombinationen {#keyboard-shortcuts}

```groovy
import org.openqa.selenium.Keys

find("input") << Keys.chord(Keys.CONTROL, "A")  // select all
find("input") << Keys.BACK_SPACE                 // delete
find("input") << Keys.ENTER
find("input") << Keys.chord(Keys.CONTROL, "C")  // copy
```

### Formularelemente {#form-elements}

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

### Warten {#waiting}

```groovy
// Prefer waitFor over Thread.sleep
waitFor(15) { find("button", text: "Done").size() == 1 }

// Multiple conditions
waitFor(15) {
    assert find("div", text: "Success").size() == 1
    find("div", class: "loading").size() == 0  // last line = return value
}
```

`waitFor` wirft eine `WaitTimeoutException`, wenn die Bedingung nicht erfüllt wird.

### Alert- und Confirm-Dialoge {#alert-and-confirm-dialogs}

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

### iFrames und Fenster {#iframes-and-windows}

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

### Scrollen, Hovern, Drag-and-Drop {#scrolling-hovering-drag-and-drop}

```groovy
interact { moveToElement(find("div", id: "target")) }   // scroll into view
interact { moveToElement(find("div", class: "hover-trigger")) }  // hover

interact {
    dragAndDrop(find("div", id: "draggable"), find("div", id: "droptarget"))
}
```

### Vollständiger Login-Ablauf {#complete-login-flow}

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

## Stolpersteine {#gotchas}

- **Stale Element**: Wenn das DOM nach `find()` aktualisiert wird, wird die Element-Referenz ungültig – `find()` erneut aufrufen
- **Element not interactable**: Das Element existiert, ist aber verborgen oder überlagert – zuerst `interact { moveToElement(...) }` verwenden
- **ChromeDriver-Versionskonflikt**: Den Treiber aktualisieren, wenn Chrome automatisch aktualisiert wird
- **Alert blockiert**: Ist ein Alert geöffnet, schlagen alle anderen WebDriver-Befehle fehl – Alerts zuerst behandeln
- **`Thread.sleep` vs. `waitFor`**: `waitFor` endet, sobald die Bedingung erfüllt ist (schneller), und ist zuverlässiger

## Siehe auch {#see-also}

- [[web-scraping]] - alternativer Scraping-Ansatz für nicht-JavaScript-Seiten
- [[ai-agent-ide-features]] - Browser-Subagenten für automatisierte Tests
