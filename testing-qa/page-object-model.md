---
title: Page Object Model
category: pattern
tags: [page-object, design-pattern, selenium, playwright, ui-testing, maintainability]
---
# Page Object Model

Design pattern that encapsulates page structure and interactions into classes - separates test logic from page details.

## Key Facts

- Each page/component = one class with locators and interaction methods
- Tests call page methods, never interact with raw selectors directly
- Locators are defined once in the page object, reused across tests
- Methods return `self` (for chaining) or another page object (for navigation)
- Benefits: single point of maintenance when UI changes, readable tests, DRY
- Base page class holds common methods: `click`, `fill`, `wait_for`, `get_text`
- Components (header, footer, modals) = separate classes composed into page objects
- Test reads like business scenario: `login_page.login("user", "pass")` not `driver.find_element(...).send_keys(...)`

## Patterns

```python
# Base page class
class BasePage:
    def __init__(self, page):  # Playwright Page or Selenium WebDriver
        self.page = page

    def open(self, path):
        self.page.goto(f"{BASE_URL}{path}")
        return self

    def find(self, selector):
        return self.page.locator(selector)

    def click(self, selector):
        self.find(selector).click()
        return self

    def fill(self, selector, value):
        self.find(selector).fill(value)
        return self

    def get_text(self, selector):
        return self.find(selector).text_content()


# Login page object
class LoginPage(BasePage):
    # Locators
    USERNAME = "[data-testid='username']"
    PASSWORD = "[data-testid='password']"
    SUBMIT = "[data-testid='login-btn']"
    ERROR_MSG = ".error-message"

    def open(self):
        return super().open("/login")

    def login(self, username, password):
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return DashboardPage(self.page)

    def get_error(self):
        return self.get_text(self.ERROR_MSG)


# Dashboard page object
class DashboardPage(BasePage):
    WELCOME_TEXT = "[data-testid='welcome']"
    LOGOUT_BTN = "[data-testid='logout']"

    def get_welcome_text(self):
        return self.get_text(self.WELCOME_TEXT)

    def logout(self):
        self.click(self.LOGOUT_BTN)
        return LoginPage(self.page)


# Component pattern
class HeaderComponent:
    def __init__(self, page):
        self.page = page

    NAV_MENU = "[data-testid='nav-menu']"

    def navigate_to(self, section):
        self.page.locator(f"{self.NAV_MENU} >> text={section}").click()


# Test using page objects
def test_successful_login(page):
    login_page = LoginPage(page).open()
    dashboard = login_page.login("admin", "password123")
    assert "Welcome" in dashboard.get_welcome_text()

def test_invalid_login(page):
    login_page = LoginPage(page).open()
    login_page.login("wrong", "wrong")
    assert login_page.get_error() == "Invalid credentials"
```

## Gotchas

- **Symptom**: page objects become too large - **Cause**: entire page in one class - **Fix**: extract components (header, sidebar, forms) into separate classes
- **Symptom**: tests break when element moves to different page section - **Cause**: locators too specific (full CSS path) - **Fix**: use `data-testid` attributes for stable selectors
- Don't put assertions in page objects - page objects describe capabilities, tests make assertions
- Don't duplicate checks: if `test_login` verifies redirect, other tests can assume login works and use it as a step
- Method chaining: `login_page.login("user", "pass")` should return the next page object, not the same page

## See Also

- [[css-xpath-selectors]] - writing stable locators
- [[playwright-testing]] - Playwright-specific page objects
- [[selenium-webdriver]] - Selenium-based page objects
- [[test-identifiers]] - data-testid best practices
