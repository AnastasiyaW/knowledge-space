---
title: "Selenium WebDriver"
category: tool
tags: [selenium, webdriver, browser-automation, ui-testing, waits, css-selectors, xpath, data-testid, locators]
level: 3
source_sha256: 8e293d9d96272b637d9f17875a7bfbff8bf677d5930b785037297337cd97a056
translation: machine
translated_at: '2026-10-24'
---
# Selenium WebDriver {#selenium-webdriver}

Selenium steuert Browser über das W3C-WebDriver-Protokoll. Die Architektur besteht aus drei Ebenen: Python-Client -> WebDriver (ChromeDriver) -> Browser. Die größten Herausforderungen sind Element-Locator, Waits und die Verwaltung der Treiberversionen. Verwende `webdriver-manager` für die automatische Versionsauflösung und explizite Waits für Stabilität.

## Wichtige Fakten {#key-facts}

- Architektur: Client (selenium-Bibliothek) -> WebDriver-Binary -> Browser (HTTP-Protokoll)
- Die Version von ChromeDriver MUSS zur Chrome-Version passen; `webdriver-manager` löst sie automatisch auf
- Locator-Strategien: CSS-Selektoren, XPath, ID, name, data-testid (am stabilsten)
- **Verwende niemals `time.sleep()`** - explizite Waits mit Bedingungen sind zuverlässig und schnell
- Implizite Waits gelten global; explizite Waits gelten pro Element (explizite bevorzugen)
- `data-testid`-Attribute liefern stabile Locator, die unabhängig von CSS-Änderungen und Styling sind

## Muster {#patterns}

### Einrichtung mit automatischer Versionierung {#setup-with-auto-versioning}

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Locator-Strategien {#locator-strategies}

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

**CSS vs. XPath**: CSS ist für einfache Fälle kürzer und schneller. XPath kann nach Textinhalt suchen und im DOM nach oben navigieren (Parent- und Ancestor-Achsen).

### Explizite Waits (immer bevorzugen) {#explicit-waits-always-prefer}

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#result")))
element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button")))
```

### Häufige Interaktionen {#common-interactions}

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

### Headless- und CI-Optionen {#headless-and-ci-options}

```python
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")  # required in Docker
driver = webdriver.Chrome(options=options)
```

## Stolperfallen {#gotchas}

- `find_element` löst `NoSuchElementException` aus, wenn das Element nicht gefunden wird - verwende Waits oder try/except
- Veraltete Element-Referenzen nach DOM-Änderungen (AJAX, Navigation) - das Element neu suchen
- iFrame-Elemente sind aus dem Hauptkontext unsichtbar - zuerst `switch_to.frame()` aufrufen
- Selenium Grid ist schwergewichtig; Selenoid (Docker-basiert, leichter, mit integrierter Videoaufzeichnung) ist vorzuziehen

## Siehe auch {#see-also}

- [[playwright-testing]] - moderne Alternative mit automatischen Waits
- [[page-object-model]] - Organisation von Locators und Aktionen in Klassen
- [[ci-cd-test-automation]] - Selenoid für Browser-Tests in CI
