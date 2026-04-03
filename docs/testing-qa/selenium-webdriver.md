---
title: Selenium WebDriver
category: tool
tags: [selenium, webdriver, browser-automation, ui-testing, waits, css-selectors, xpath, data-testid, locators]
---

# Selenium WebDriver

Selenium automates browsers via the W3C WebDriver protocol. Three-tier architecture: Python client -> WebDriver (ChromeDriver) -> Browser. The main challenges are element locators, waits, and driver version management. Use `webdriver-manager` for auto-versioning and explicit waits for stability.

## Key Facts

- Architecture: client (selenium lib) -> WebDriver binary -> browser (HTTP protocol)
- ChromeDriver version MUST match Chrome version; `webdriver-manager` auto-resolves
- Locator strategies: CSS selectors, XPath, ID, name, data-testid (most stable)
- **Never use `time.sleep()`** - explicit waits with conditions are reliable and fast
- Implicit waits are global; explicit waits are per-element (prefer explicit)
- `data-testid` attributes provide stable locators independent of CSS/styling changes

## Patterns

### Setup with Auto-Versioning

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Locator Strategies

```python
from selenium.webdriver.common.by import By

# CSS Selectors (fast, familiar)
driver.find_element(By.CSS_SELECTOR, "#username")           # by ID
driver.find_element(By.CSS_SELECTOR, ".login-form")         # by class
driver.find_element(By.CSS_SELECTOR, "input[name='email']") # by attribute
driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-btn']")  # test ID

# XPath (more powerful, can search by text and traverse up)
driver.find_element(By.XPATH, "//h1[text()='Welcome']")
driver.find_element(By.XPATH, "//div[contains(@class, 'error')]")
driver.find_element(By.XPATH, "//input[@type='text'][2]")  # 1-indexed!
```

**CSS vs XPath**: CSS is shorter and faster for simple cases. XPath can search by text content and traverse up the DOM (parent/ancestor axes).

### Explicit Waits (Always Prefer)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#result")))
element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button")))
```

### Common Interactions

```python
# Navigation
driver.get("https://example.com")
driver.back(); driver.forward(); driver.refresh()

# Elements
element.clear(); element.send_keys("text"); element.click()
element.text; element.get_attribute("value")

# Select dropdown
from selenium.webdriver.support.select import Select
Select(driver.find_element(By.CSS_SELECTOR, "#menu")).select_by_visible_text("Option")

# File upload
driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys("/path/to/file.png")

# Alerts
alert = driver.switch_to.alert
alert.accept()   # OK
alert.dismiss()  # Cancel

# iFrames
driver.switch_to.frame("frameName")
driver.switch_to.default_content()  # back to main
```

### Headless and CI Options

```python
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")  # required in Docker
driver = webdriver.Chrome(options=options)
```

## Gotchas

- `find_element` raises `NoSuchElementException` if not found - use waits or try/except
- Stale element references after DOM changes (AJAX, navigation) - re-find the element
- iFrame elements are invisible from main context - must `switch_to.frame()` first
- Selenium Grid is heavyweight; prefer Selenoid (Docker-based, lighter, built-in video recording)

## See Also

- [[playwright-testing]] - modern alternative with auto-waits
- [[page-object-model]] - organizing locators and actions into classes
- [[ci-cd-test-automation]] - Selenoid for browser tests in CI
