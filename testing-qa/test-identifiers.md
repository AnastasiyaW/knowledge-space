---
title: Test Identifiers (data-testid)
category: technique
tags: [data-testid, locators, frontend, react, test-stability, selectors]
---
# Test Identifiers (data-testid)

Adding `data-testid` attributes to frontend elements - the recommended strategy for stable, maintainable UI test locators.

## Key Facts

- `data-testid` = HTML attribute specifically for test automation, invisible to users
- Survives CSS refactors, text changes, layout redesigns - only changes intentionally
- QA automation engineers should know how to add them in frontend code (React, Vue, etc.)
- Naming convention: descriptive, kebab-case - e.g., `data-testid="login-submit-btn"`
- Component-based: add testid to the component root, find children via CSS within
- Playwright has native `page.get_by_test_id("name")` method
- Selenium: `[data-testid='name']` CSS selector
- Not a replacement for accessibility attributes (`aria-label`, `role`) - complementary
- Locale-independent: unlike text-based locators, works across all app languages

## Patterns

```html
<!-- HTML with test identifiers -->
<form data-testid="login-form">
  <input data-testid="username-input" type="text" />
  <input data-testid="password-input" type="password" />
  <button data-testid="login-submit-btn">Log In</button>
  <span data-testid="error-message" class="error"></span>
</form>
```

```jsx
// React component with data-testid
function LoginForm({ onSubmit }) {
  return (
    <form data-testid="login-form" onSubmit={onSubmit}>
      <input data-testid="username-input" name="username" />
      <input data-testid="password-input" name="password" type="password" />
      <button data-testid="login-submit-btn" type="submit">
        Log In
      </button>
    </form>
  );
}

// List items with dynamic testids
function UserList({ users }) {
  return (
    <ul data-testid="user-list">
      {users.map((user, index) => (
        <li key={user.id} data-testid={`user-item-${index}`}>
          <span data-testid={`user-name-${index}`}>{user.name}</span>
        </li>
      ))}
    </ul>
  );
}
```

```python
# Playwright usage
def test_login(page):
    page.get_by_test_id("username-input").fill("admin")
    page.get_by_test_id("password-input").fill("secret")
    page.get_by_test_id("login-submit-btn").click()

# Selenium usage
from selenium.webdriver.common.by import By

username = driver.find_element(By.CSS_SELECTOR, "[data-testid='username-input']")
username.send_keys("admin")

# Page Object with testids
class LoginPage:
    USERNAME = "[data-testid='username-input']"
    PASSWORD = "[data-testid='password-input']"
    SUBMIT = "[data-testid='login-submit-btn']"
    ERROR = "[data-testid='error-message']"
```

## Gotchas

- **Symptom**: `data-testid` on wrong element (container instead of input) - **Cause**: React component wraps input in div, testid goes to wrapper - **Fix**: find child element within the testid container: `[data-testid='wrapper'] input`
- **Symptom**: text-based test breaks when app is localized (translated) - **Cause**: text changes per locale - **Fix**: use `data-testid` which is locale-independent
- **Symptom**: dynamic list items hard to target - **Cause**: no index in testid - **Fix**: include index or unique ID: `data-testid={`item-${id}`}`
- Production stripping: some teams remove `data-testid` in production builds to reduce DOM size - configure bundler for this
- Don't overuse: add testids to elements that tests interact with, not every DOM element

## See Also

- [[css-xpath-selectors]] - fallback selectors when testids unavailable
- [[playwright-testing]] - Playwright's `get_by_test_id()` method
- [[page-object-model]] - organizing testid-based locators
