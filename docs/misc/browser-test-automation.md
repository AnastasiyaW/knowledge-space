---
title: Browser Test Automation with Geb/Groovy (Selenium)
category: concepts
tags: [misc, testing, selenium, groovy, geb, browser-automation, webdriver]
---

# Browser Test Automation with Geb/Groovy (Selenium)

Geb is a Groovy library on top of Selenium WebDriver for browser test automation. Covers element finding, interaction, waiting, dialogs, iframes, drag-and-drop, and complete test flow patterns.

## Key Facts

- ChromeDriver version must match installed Chrome browser; SDK v25+ handles matching automatically
- Every script runs inside `Browser.drive { ... }` block
- `find()` locates elements by tag, attributes, or CSS selectors
- `<<` operator types text into inputs; `.click()` clicks elements
- `waitFor(timeout)` polls until condition is true - always prefer over `Thread.sleep`
- `withFrame(iframe) { ... }` and `withWindow(condition) { ... }` for context switching

## Patterns

### Basic Structure

```groovy
import geb.Browser

Browser.drive {
    go "https://example.com"
    assert page.title == "Expected Title"
    assert currentUrl.contains("/dashboard")
}
```

### Finding Elements

```groovy
find("a", text: "Link Text")            // by tag + text
find("input", placeholder: "Search")    // by placeholder
find("input", id: "username")           // by id
find("div", class: "container")         // by class
find("#main-content")                   // CSS selector
find(".btn-primary")                    // CSS class
find("table tr", 2)                    // nth match (0-indexed)
```

### Interaction

```groovy
find("a", text: "Click Me").click()
find("input", placeholder: "Name") << "John"   // type text
find("input", placeholder: "Name").value()      // read value
find("input", placeholder: "Name").value("New") // set value
```

### Keyboard Shortcuts

```groovy
import org.openqa.selenium.Keys

find("input") << Keys.chord(Keys.CONTROL, "A")  // select all
find("input") << Keys.BACK_SPACE                 // delete
find("input") << Keys.ENTER
find("input") << Keys.chord(Keys.CONTROL, "C")  // copy
```

### Form Elements

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

### Waiting

```groovy
// Prefer waitFor over Thread.sleep
waitFor(15) { find("button", text: "Done").size() == 1 }

// Multiple conditions
waitFor(15) {
    assert find("div", text: "Success").size() == 1
    find("div", class: "loading").size() == 0  // last line = return value
}
```

`waitFor` throws `WaitTimeoutException` if condition not met.

### Alert and Confirm Dialogs

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

### iFrames and Windows

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

### Scrolling, Hovering, Drag-and-Drop

```groovy
interact { moveToElement(find("div", id: "target")) }   // scroll into view
interact { moveToElement(find("div", class: "hover-trigger")) }  // hover

interact {
    dragAndDrop(find("div", id: "draggable"), find("div", id: "droptarget"))
}
```

### Complete Login Flow

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

## Gotchas

- **Stale element**: if DOM updates after `find()`, element reference becomes invalid - call `find()` again
- **Element not interactable**: element exists but hidden/overlapped - use `interact { moveToElement(...) }` first
- **ChromeDriver mismatch**: update driver when Chrome auto-updates
- **Alert blocking**: if an alert is open, all other WebDriver commands fail - handle alerts first
- **`Thread.sleep` vs `waitFor`**: `waitFor` exits as soon as condition is true (faster) and is more reliable

## See Also

- [[python-web-scraping]] - alternative scraping approach for non-JS pages
- [[ai-agent-ide-features]] - browser sub-agents for automated testing
