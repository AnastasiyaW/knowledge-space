---
title: "Selene - Selenide pour Python"
category: tools
tags: [selene, selenide, ui-testing, browser-automation, fluent-api, auto-wait, css-selectors]
level: 3
source_sha256: 8df408d6778010f7cf7029905eeceaf74059d7b1ff72a3f0bc411a9e0d270b67
translation: machine
translated_at: '2026-10-24'
---
# Selene - Selenide pour Python {#selene-selenide-for-python}

Selene est un portage en Python de Selenide (Java), une surcouche concise et à attente automatique au-dessus de Selenium WebDriver. Elle réduit le code répétitif grâce à une API fluide et à des attentes intelligentes intégrées.

## Installation {#setup}

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

## Interactions de base {#basic-interactions}

```python
from selene import browser, have, be

def test_search():
    browser.open("/")
    browser.element("#search-input").type("python testing")
    browser.element("#search-button").click()
    browser.all(".search-result").should(have.size_greater_than(0))
    browser.element(".search-result").should(have.text("Python"))
```

Toutes les actions attendent automatiquement que l'élément soit visible et cliquable. Aucune attente explicite n'est nécessaire.

## Sélecteurs d'éléments {#element-selectors}

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

## Assertions (conditions) {#assertions-conditions}

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

Toutes les assertions sont réessayées automatiquement jusqu'à expiration du délai (4 s par défaut). Aucun `time.sleep()` ni attente explicite n'est nécessaire.

## Travailler avec les tableaux {#working-with-tables}

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

## Interactions avec les formulaires {#form-interactions}

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

## Configuration du navigateur par test {#browser-configuration-per-test}

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

## Selene et Selenium brut {#selene-vs-raw-selenium}

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

## Pièges {#gotchas}

- **Problème :** si `browser.quit()` n'est pas appelé après l'échec d'un test, le navigateur reste ouvert et consomme des ressources. **Correctif :** utilisez toujours une fixture avec `yield` et `quit` dans la phase de nettoyage. Vous pouvez aussi configurer `browser.config.hold_driver_at_exit = False`.

- **Problème :** `browser.all(".item").should(have.texts("A", "B"))` échoue, car la vérification porte sur l'ordre exact et le nombre exact d'éléments. **Correctif :** utilisez `have.size(N)` avec des vérifications `have.text()` individuelles lorsque l'ordre n'a pas d'importance. Vous pouvez aussi trier les valeurs attendues et obtenues avant la comparaison.

- **Problème :** Selene utilise Selenium en arrière-plan et nécessite toujours chromedriver. Une incompatibilité de version provoque une `SessionNotCreatedException`. **Correctif :** installez `webdriver-manager` ou utilisez Selenium 4.6+, qui télécharge automatiquement les pilotes via Selenium Manager.

## Voir aussi {#see-also}

- [[selenium-webdriver]]
- [[playwright-testing]]
- [[page-object-model]]
