---
title: Selene - Selenide for Python
category: tools
tags: [selene, selenide, ui-testing, browser-automation, fluent-api, auto-wait, css-selectors]
---

# Selene - Selenide for Python

Selene is a Python port of Selenide (Java) - a concise, auto-waiting wrapper over Selenium WebDriver. Reduces boilerplate with fluent API and built-in smart waits.

## Setup

```bash
pip install selene
```

```python
from selene import browser, have, be, by

browser.config.base_url = "https://example.com"
browser.config.timeout = 10  # seconds for all waits
browser.config.window_width = 1920
browser.config.window_height = 1080
```

## Basic Interactions

```python
from selene import browser, have, be

def test_search():
    browser.open("/")
    browser.element("#search-input").type("python testing")
    browser.element("#search-button").click()
    browser.all(".search-result").should(have.size_greater_than(0))
    browser.element(".search-result").should(have.text("Python"))
```

All actions auto-wait for element to be visible/clickable. No explicit waits needed.

## Element Selectors

```python
# CSS selector (default)
browser.element("#id")
browser.element(".class")
browser.element("[data-testid='login']")

# XPath
browser.element(by.xpath("//button[contains(text(), 'Submit')]"))

# By text
browser.element(by.text("Sign In"))
browser.element(by.partial_text("Sign"))

# Collections
browser.all(".item")                    # all matching elements
browser.all(".item").first              # first element
browser.all(".item")[2]                 # third element (0-indexed)
browser.all(".item").element_by(have.text("Special"))  # find by condition
```

## Assertions (Conditions)

```python
# Element conditions
browser.element("#name").should(have.value("John"))
browser.element("#status").should(have.text("Active"))
browser.element("#status").should(have.exact_text("Active User"))
browser.element("#error").should(have.css_class("alert-danger"))
browser.element("#modal").should(be.visible)
browser.element("#loader").should(be.not_.visible)
browser.element("#input").should(be.enabled)

# Collection conditions
browser.all(".row").should(have.size(10))
browser.all(".tag").should(have.texts("Python", "Testing", "QA"))
browser.all(".option").should(have.size_greater_than(3))
```

All assertions auto-retry until timeout (default 4s). No `time.sleep()` or explicit waits.

## Working with Tables

```python
def test_table_data():
    rows = browser.all("table tbody tr")
    rows.should(have.size(5))

    # Check specific cell
    rows[0].all("td")[1].should(have.text("John Doe"))

    # Find row by content
    target_row = rows.element_by(have.text("admin@example.com"))
    target_row.element(".delete-btn").click()
```

## Form Interactions

```python
def test_registration_form():
    browser.open("/register")
    browser.element("#name").type("Jane Doe")
    browser.element("#email").type("jane@example.com")
    browser.element("#password").type("secure123")

    # Dropdown
    browser.element("#country").click()
    browser.all(".dropdown-option").element_by(have.text("Germany")).click()

    # Checkbox
    browser.element("#agree-terms").click()

    # Submit
    browser.element("button[type=submit]").click()
    browser.element(".success-message").should(have.text("Welcome"))
```

## Browser Configuration per Test

```python
@pytest.fixture
def setup_browser():
    browser.config.base_url = "https://staging.example.com"
    browser.config.timeout = 15
    yield
    browser.quit()

@pytest.fixture
def headless_browser():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--headless")
    browser.config.driver_options = options
    yield
    browser.quit()
```

## Selene vs Raw Selenium

```python
# Selenium (verbose)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#search")))
element.send_keys("python")
driver.find_element(By.CSS_SELECTOR, "#btn").click()

# Selene (concise)
browser.element("#search").type("python")
browser.element("#btn").click()
```

## Gotchas

- **Issue:** Selene's `browser.quit()` not called after test failure leaves browser open, consuming resources. **Fix:** Always use a fixture with yield + quit in teardown. Or configure `browser.config.hold_driver_at_exit = False`.

- **Issue:** `browser.all(".item").should(have.texts("A", "B"))` fails because it checks exact order and exact count. **Fix:** Use `have.size(N)` + individual `have.text()` checks when order doesn't matter. Or sort expected/actual before comparison.

- **Issue:** Selene uses Selenium under the hood - still needs chromedriver. Version mismatch causes `SessionNotCreatedException`. **Fix:** Install `webdriver-manager` or use Selenium 4.6+ which auto-downloads drivers via Selenium Manager.

## See Also

- [[selenium-webdriver]]
- [[playwright-testing]]
- [[page-object-model]]
