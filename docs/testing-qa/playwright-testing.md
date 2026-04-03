---
title: Playwright Testing
category: tool
tags: [playwright, browser-automation, ui-testing, auto-wait, codegen, trace, assertions, locators]
---

# Playwright Testing

Playwright is a modern browser automation framework by Microsoft. Key advantage over Selenium: auto-waiting for elements, built-in assertions with retry, trace viewer for debugging, and codegen for recording tests. Supports Chromium, Firefox, and WebKit from a single API.

## Key Facts

- **Auto-wait**: every action waits for element to be actionable (visible, stable, enabled)
- **Built-in assertions**: `expect(locator).to_have_text("...")` retries automatically with timeout
- **Codegen**: `playwright codegen URL` records actions as test code
- **Trace viewer**: records screenshots, DOM snapshots, network, console per action
- Supports Chromium, Firefox, WebKit; headless by default
- Multiple browser contexts = parallel independent sessions (different users, cookies)

## Patterns

### Pytest Integration

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

### Locators (Prefer Over CSS/XPath)

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

### Trace Viewer

```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
# ... test actions ...
context.tracing.stop(path="trace.zip")
# View: playwright show-trace trace.zip
```

### Multiple Contexts (Parallel Users)

```python
admin_ctx = browser.new_context()
user_ctx = browser.new_context()
admin_page = admin_ctx.new_page()
user_page = user_ctx.new_page()
# Independent sessions (separate cookies, storage)
```

## Gotchas

- Auto-wait is per-action, not per-assertion - use `expect()` for assertions (retries automatically)
- `page.wait_for_timeout(ms)` defeats the purpose - use `expect()` with custom timeout
- Codegen output is a starting point - refactor to use role/label locators and POM
- Browser contexts are isolated - state doesn't persist between contexts

## See Also

- [[selenium-webdriver]] - older alternative, wider ecosystem
- [[page-object-model]] - POM pattern applies to Playwright too
- [[allure-reporting]] - integrating Playwright results with Allure
