---
title: Selenium WebDriver
category: tool
tags: [selenium, webdriver, browser-automation, ui-testing, waits]
---
# Selenium WebDriver

Browser automation framework - controls real browsers via WebDriver protocol for UI testing.

## Key Facts

- Selenium 4+ uses WebDriver protocol (W3C standard) - no separate driver downloads needed with `selenium-manager`
- `webdriver.Chrome()`, `webdriver.Firefox()`, `webdriver.Edge()` - browser instances
- Locator strategies: `By.ID`, `By.CSS_SELECTOR`, `By.XPATH`, `By.CLASS_NAME`, `By.TAG_NAME`, `By.LINK_TEXT`
- Explicit waits (`WebDriverWait`) preferred over implicit waits or `time.sleep()`
- `ActionChains` for complex interactions: hover, drag-drop, right-click, double-click
- `Select` class for dropdown interactions
- Screenshots: `driver.save_screenshot("path.png")` or `driver.get_screenshot_as_png()`
- JavaScript execution: `driver.execute_script("return document.title")`
- Window/tab management: `driver.switch_to.window(handle)`, `driver.switch_to.frame()`
- For new projects, consider [[playwright-testing]] as a modern alternative

## Patterns

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# Setup with options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# Explicit wait (preferred)
wait = WebDriverWait(driver, timeout=10)
element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".result"))
)

# Common expected conditions
EC.presence_of_element_located((By.ID, "form"))
EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
EC.text_to_be_present_in_element((By.CLASS_NAME, "msg"), "Success")
EC.url_contains("/dashboard")
EC.invisibility_of_element_located((By.ID, "spinner"))

# Action chains
actions = ActionChains(driver)
actions.move_to_element(menu).click(submenu).perform()

# Dropdown
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.ID, "color"))
select.select_by_visible_text("Green")
select.select_by_value("green")

# Multiple windows/tabs
original = driver.current_window_handle
driver.find_element(By.LINK_TEXT, "Open").click()
for handle in driver.window_handles:
    if handle != original:
        driver.switch_to.window(handle)
        break

# iFrames
driver.switch_to.frame("iframe_name")
# ... interact with iframe content
driver.switch_to.default_content()

# Screenshot on failure (pytest fixture)
import pytest

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Cleanup
driver.quit()  # closes all windows and ends session
driver.close()  # closes current window only
```

## Gotchas

- **Symptom**: `StaleElementReferenceException` - **Cause**: DOM changed after element was found - **Fix**: re-find element or use explicit wait before interaction
- **Symptom**: `ElementClickInterceptedException` - **Cause**: overlay, modal, or another element blocking the target - **Fix**: wait for overlay to disappear, scroll element into view, or use JS click
- **Symptom**: tests pass locally, fail in CI - **Cause**: no display in CI - **Fix**: use `--headless` mode; add `--no-sandbox` and `--disable-dev-shm-usage` for Docker
- **Symptom**: `TimeoutException` on waits - **Cause**: element truly absent or wrong locator - **Fix**: verify locator in browser DevTools, increase timeout if page is slow
- Never use `time.sleep()` - use explicit `WebDriverWait` with appropriate expected conditions
- `driver.quit()` vs `driver.close()`: `quit()` ends entire session, `close()` only current window

## See Also

- [[css-xpath-selectors]] - locator strategies
- [[page-object-model]] - structuring Selenium tests
- [[playwright-testing]] - modern alternative to Selenium
- [Selenium Python docs](https://www.selenium.dev/documentation/webdriver/)
- [Selenium Python API](https://selenium-python.readthedocs.io/)
