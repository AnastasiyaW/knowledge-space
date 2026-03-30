---
title: Web Browser Automation with Groovy and Geb
category: misc/test-automation
tags: [groovy, geb, browser-automation, web-testing, chromedriver, selenium, scripting]
---

# Web Browser Automation with Groovy and Geb

## Key Facts

- **Geb** is a browser automation framework built on top of [[selenium-webdriver]] for the Groovy language
- Uses `Browser.drive { }` block to launch and control a browser instance
- Scripts are `.groovy` files executed via `groovy/bin/groovy script.groovy`
- Requires **ChromeDriver** matching the installed Chrome version - version mismatch causes errors
- Core commands: `go` (navigate), `find` (locate elements), `click`, `assert` (verify conditions), `println` (logging)
- Elements are found using CSS selectors: `find("tag", attribute: "value")` - e.g., `find("a", text: "Home")`
- `find().size()` returns element count on the page - used for assertions
- `find().click()` triggers a click on the found element - element must be unique or the click fails
- Assertions use Groovy's `assert` keyword - if the condition is false, the script stops with an error message

### Common Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `go "url"` | Navigate to URL | `go "https://example.com"` |
| `find("tag")` | Find elements by tag | `find("a")` - all links |
| `find("tag", text: "X")` | Find by tag + text | `find("button", text: "Submit")` |
| `.size()` | Count matching elements | `find("a").size() == 3` |
| `.click()` | Click an element | `find("button", text: "OK").click()` |
| `assert` | Verify condition | `assert find("p", text: "Success").size() == 1` |
| `println` | Log message to console | `println "test passed"` |

## Patterns

```groovy
// Basic navigation and assertion script
import geb.Browser

Browser.drive {
    // Navigate to page
    go "https://demoqa.com/buttons"

    // Click a button
    find("button", text: "Click Me").click()

    // Verify expected result appeared
    assert find("p", text: "You have done a dynamic click").size() == 1

    println "test passed"
}
```

```groovy
// Link verification script
import geb.Browser

Browser.drive {
    go "https://example.com/links"

    // Verify specific link exists
    assert find("a", text: "Home").size() == 1

    // Verify total link count
    assert find("a").size() >= 5

    println "all links verified"
}
```

```bash
# Running scripts
# Windows:
groovy\bin\groovy script.groovy

# Linux/macOS:
groovy/bin/groovy script.groovy

# ChromeDriver update (when Chrome updates):
# 1. Check Chrome version: chrome://version
# 2. Download matching driver from googlechromelabs.github.io
# 3. Replace driver in tat/driver/ directory
```

## Gotchas

- ChromeDriver version MUST match Chrome browser version - update driver when Chrome auto-updates
- Error "this version of ChromeDriver only supports Chrome version X" means version mismatch
- `find().click()` fails if multiple elements match the selector - make selectors specific enough to match exactly one element
- Scripts execute fast - some actions happen too quickly to observe visually, but the assertions still run
- File encoding must be **UTF-8** - especially important when scripts contain non-ASCII characters (Cyrillic, etc.)
- The browser opens and closes automatically during script execution - don't interact with it while a script runs
- `assert` failures stop script execution immediately - `println` after a failed assert never runs

## See Also

- [[browser-sub-agents]] - AI-driven browser automation (non-scripted alternative)
- [[ai-ide-workflow-modes]] - browser verification in AI coding workflows
