---
title: "Playwright-Tests"
category: tool
tags: [playwright, browser-automation, ui-testing, auto-wait, codegen, trace, assertions, locators]
level: 3
source_sha256: f512a341abed0654ba43a842640eaa570a2864376457fcadf46083d6a25c8abc
translation: machine
translated_at: '2026-10-24'
---
# Playwright-Tests {#playwright-testing}

Playwright ist ein modernes Browser-Automatisierungs-Framework von Microsoft. Der wesentliche Vorteil gegenüber Selenium: automatisches Warten auf Elemente, eingebaute Assertions mit Wiederholungsversuchen, ein Trace-Viewer zum Debuggen und Codegen zum Aufzeichnen von Tests. Unterstützt Chromium, Firefox und WebKit über eine einzige API.

## Wichtige Fakten {#key-facts}

- **Auto-Wait**: jede Aktion wartet, bis das Element bedienbar ist (sichtbar, stabil, aktiviert)
- **Eingebaute Assertions**: `expect(locator).to_have_text("...")` wiederholt sich automatisch bis zum Timeout
- **Codegen**: `playwright codegen URL` zeichnet Aktionen als Testcode auf
- **Trace-Viewer**: zeichnet Screenshots, DOM-Snapshots, Netzwerk und Konsole pro Aktion auf
- Unterstützt Chromium, Firefox, WebKit; standardmäßig headless
- Mehrere Browser-Kontexte = parallele, unabhängige Sitzungen (verschiedene Benutzer, Cookies)

## Muster {#patterns}

### Pytest-Integration {#pytest-integration}

```python
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
```

### Locators (Bevorzugt gegenüber CSS/XPath) {#locators-prefer-over-cssxpath}

```python
# Role-based (most stable, accessibility-first)
page.get_by_role("button", name="Submit")
page.get_by_role("textbox", name="Email")

# Text and label
page.get_by_text("Welcome")
page.get_by_label("Password")
page.get_by_placeholder("Enter email")

# Test ID
page.get_by_test_id("submit-btn")

# CSS/XPath still available
page.locator("css=#username")
```

### Trace-Viewer {#trace-viewer}

```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
# ... test actions ...
context.tracing.stop(path="trace.zip")
# View: playwright show-trace trace.zip
```

### Mehrere Kontexte (parallele Benutzer) {#multiple-contexts-parallel-users}

```python
admin_ctx = browser.new_context()
user_ctx = browser.new_context()
admin_page = admin_ctx.new_page()
user_page = user_ctx.new_page()
# Independent sessions (separate cookies, storage)
```

## Stolperfallen {#gotchas}

- Auto-Wait gilt pro Aktion, nicht pro Assertion - für Assertions `expect()` verwenden (wiederholt sich automatisch)
- `page.wait_for_timeout(ms)` untergräbt den Zweck - stattdessen `expect()` mit eigenem Timeout verwenden
- Die Ausgabe von Codegen ist ein Ausgangspunkt - auf Rollen- und Label-Locators sowie POM umstellen
- Browser-Kontexte sind isoliert - Zustand bleibt zwischen Kontexten nicht erhalten

## Siehe auch {#see-also}

- [[selenium-webdriver]] - älterer Alternativ, breiteres Ökosystem
- [[page-object-model]] - das POM-Muster gilt auch für Playwright
- [[allure-reporting]] - Integration von Playwright-Ergebnissen mit Allure
