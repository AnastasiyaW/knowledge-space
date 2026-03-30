---
title: Playwright Testing
category: tool
tags: [playwright, browser-automation, ui-testing, auto-wait, codegen, trace]
---
# Playwright Testing

Modern browser automation library by Microsoft - auto-waiting, multi-browser, trace viewer, codegen.

## Key Facts

- `pip install playwright && playwright install` - installs browsers (Chromium, Firefox, WebKit)
- Auto-waiting built in - no explicit waits needed for most actions (click, fill, assert)
- Locators: `page.locator()`, `page.get_by_role()`, `page.get_by_test_id()`, `page.get_by_text()`
- `data-testid` attribute is the preferred locator strategy for stable tests
- `playwright codegen URL` - records browser actions and generates test code
- Trace viewer: `playwright show-trace trace.zip` - time-travel debugging with screenshots
- pytest-playwright plugin: `page` fixture provides a fresh browser page per test
- Network interception: `page.route()` for mocking API responses
- Multiple browser contexts for parallel isolated sessions
- Assertions: `expect(locator).to_have_text()`, `expect(locator).to_be_visible()`, etc.

## Patterns

```python
# pytest-playwright setup
# pip install pytest-playwright
# pytest --browser chromium --headed

import pytest
from playwright.sync_api import Page, expect

# Basic test with auto-wait
def test_login(page: Page):
    page.goto("https://example.com/login")
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("secret")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_text("Welcome")).to_be_visible()

# data-testid locator (preferred)
def test_form_submit(page: Page):
    page.goto("/form")
    page.get_by_test_id("email-input").fill("test@example.com")
    page.get_by_test_id("submit-btn").click()
    expect(page.get_by_test_id("success-msg")).to_have_text("Submitted")

# Network mocking
def test_with_mock_api(page: Page):
    page.route("**/api/users", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='[{"id": 1, "name": "Mock User"}]'
    ))
    page.goto("/users")
    expect(page.get_by_text("Mock User")).to_be_visible()

# Screenshot and trace
def test_with_trace(page: Page, context):
    context.tracing.start(screenshots=True, snapshots=True)
    page.goto("/dashboard")
    # ... test actions
    context.tracing.stop(path="trace.zip")

# Multiple tabs
def test_new_tab(page: Page, context):
    page.goto("/")
    with context.expect_page() as new_page_info:
        page.get_by_text("Open link").click()
    new_page = new_page_info.value
    expect(new_page).to_have_url("/new-page")

# Page Object with Playwright
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.submit = page.get_by_role("button", name="Login")

    def login(self, user: str, pwd: str):
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()

# conftest.py - browser config
@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
    }
```

## Gotchas

- **Symptom**: `get_by_test_id` not finding elements - **Cause**: default attribute is `data-testid`, app uses different attr - **Fix**: configure `playwright.selectors.set_test_id_attribute("data-test")`
- **Symptom**: test flaky with network requests - **Cause**: real API responses vary - **Fix**: use `page.route()` to mock API or `page.wait_for_load_state("networkidle")`
- **Symptom**: `page.goto()` timeout - **Cause**: slow page load or network issues - **Fix**: increase timeout `page.goto(url, timeout=60000)` or wait for specific element
- Playwright locators are lazy - they don't search the DOM until an action is performed
- `expect()` assertions auto-retry (up to 5 seconds by default) - different from Python `assert`
- Codegen (`playwright codegen`) is useful for learning locators but generates non-ideal code - refactor into page objects

## See Also

- [[page-object-model]] - structuring Playwright tests
- [[test-identifiers]] - setting up data-testid in frontend apps
- [[css-xpath-selectors]] - fallback locator strategies
- [Playwright Python docs](https://playwright.dev/python/docs/intro)
- [Playwright locators](https://playwright.dev/python/docs/locators)
- [Playwright assertions](https://playwright.dev/python/docs/test-assertions)
