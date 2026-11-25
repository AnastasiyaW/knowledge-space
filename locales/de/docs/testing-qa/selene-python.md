---
title: "Selene - Selenide für Python"
category: tools
tags: [selene, selenide, ui-testing, browser-automation, fluent-api, auto-wait, css-selectors]
level: 3
source_sha256: 8df408d6778010f7cf7029905eeceaf74059d7b1ff72a3f0bc411a9e0d270b67
translation: machine
translated_at: '2026-10-24'
---
# Selene - Selenide für Python {#selene-selenide-for-python}

Selene ist eine Python-Portierung von Selenide (Java), ein knapper Wrapper über Selenium WebDriver mit automatischem Warten. Durch die Fluent API und die integrierten intelligenten Waits wird der Boilerplate-Code reduziert.

## Einrichtung {#setup}

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

## Grundlegende Interaktionen {#basic-interactions}

```python
from selene import browser, have, be

def test_search():
    browser.open("/")
    browser.element("#search-input").type("python testing")
    browser.element("#search-button").click()
    browser.all(".search-result").should(have.size_greater_than(0))
    browser.element(".search-result").should(have.text("Python"))
```

Alle Aktionen warten automatisch, bis das Element sichtbar bzw. klickbar ist. Explizite Waits sind nicht nötig.

## Element-Selektoren {#element-selectors}

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

## Assertions (Conditions) {#assertions-conditions}

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

Alle Assertions wiederholen sich automatisch bis zum Timeout (Standard: 4s). Kein `time.sleep()` und keine expliziten Waits.

## Arbeiten mit Tabellen {#working-with-tables}

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

## Formular-Interaktionen {#form-interactions}

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

## Browser-Konfiguration pro Test {#browser-configuration-per-test}

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

## Selene vs. reines Selenium {#selene-vs-raw-selenium}

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

## Stolpersteine {#gotchas}

- **Problem:** Wird `browser.quit()` nach einem Testfehler nicht aufgerufen, bleibt der Browser geöffnet und verbraucht Ressourcen. **Lösung:** Immer ein Fixture mit yield und quit im Teardown verwenden. Alternativ `browser.config.hold_driver_at_exit = False` setzen.

- **Problem:** `browser.all(".item").should(have.texts("A", "B"))` schlägt fehl, weil Reihenfolge und exakte Anzahl geprüft werden. **Lösung:** Wenn die Reihenfolge keine Rolle spielt, `have.size(N)` zusammen mit einzelnen `have.text()`-Prüfungen verwenden. Alternativ Erwartungs- und Istwerte vor dem Vergleich sortieren.

- **Problem:** Selene nutzt intern Selenium und benötigt weiterhin chromedriver. Eine nicht passende Version führt zu `SessionNotCreatedException`. **Lösung:** `webdriver-manager` installieren oder Selenium 4.6+ verwenden, das Treiber über Selenium Manager automatisch herunterlädt.

## Siehe auch {#see-also}

- [[selenium-webdriver]]
- [[playwright-testing]]
- [[page-object-model]]
