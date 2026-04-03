---
title: HTML Tables and Forms
category: concepts
tags: [web-frontend, html, forms, accessibility, validation]
---

# HTML Tables and Forms

Tables display tabular data; forms collect user input. Both require proper semantics for accessibility.

## Tables

```html
<table>
  <caption>Q4 Sales by Region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North</th>
      <td>$50,000</td>
    </tr>
  </tbody>
  <tfoot>
    <tr><td colspan="2">Total: $50,000</td></tr>
  </tfoot>
</table>
```

- `<th>` for headers (screen readers announce column/row names)
- `scope="col"` / `scope="row"` clarifies direction
- `<caption>` describes table purpose (accessibility)
- `colspan` / `rowspan` for spanning cells
- Never use tables for page layout

```css
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
tbody tr:nth-child(even) { background-color: #fafafa; }
```

`border-collapse: collapse` is almost always needed - without it, cells have separate borders with gaps.

## Form Element

```html
<form action="/submit" method="POST" enctype="multipart/form-data">
  <!-- form controls -->
</form>
```

| Attribute | Purpose |
|-----------|---------|
| `action` | URL where data is sent |
| `method` | `GET` (data in URL) or `POST` (data in body) |
| `enctype` | `multipart/form-data` required for file uploads |
| `novalidate` | Disables built-in validation |

**GET vs POST**: GET for search/filters (bookmarkable, visible in URL). POST for sensitive data (login, registration, file upload).

## Input Types

```html
<!-- Text -->
<input type="text" placeholder="Name">
<input type="email" placeholder="user@example.com">
<input type="password">
<input type="tel" placeholder="+1-234-567-8900">
<input type="url" placeholder="https://...">
<input type="search">
<input type="number" min="0" max="100" step="1">

<!-- Date/Time -->
<input type="date">
<input type="time">
<input type="datetime-local">

<!-- Selection -->
<input type="checkbox">
<input type="radio" name="group">
<input type="range" min="0" max="100">
<input type="color">

<!-- File -->
<input type="file" accept=".jpg,.png,.pdf" multiple>
<input type="hidden" name="csrf" value="token">
```

## Input Attributes

| Attribute | Purpose |
|-----------|---------|
| `name` | Key for submitted data (required) |
| `value` | Default/current value |
| `placeholder` | Hint text (disappears on focus) |
| `required` | Must be filled |
| `disabled` | Cannot interact, NOT submitted |
| `readonly` | Cannot edit, IS submitted |
| `autofocus` | Focus on page load |
| `maxlength` / `minlength` | Character limits |
| `pattern` | Regex validation |
| `min` / `max` / `step` | Number/date range |
| `multiple` | Allow multiple values |
| `autocomplete` | Browser autofill hint |

## Labels

Every input MUST have a label. Screen readers read them; clicking labels focuses the input.

```html
<!-- Method 1: for/id (preferred) -->
<label for="email-input">Email:</label>
<input type="email" id="email-input" name="email">

<!-- Method 2: wrapping -->
<label>Email: <input type="email" name="email"></label>
```

## Select and Textarea

```html
<select name="country">
  <option value="">-- Select --</option>
  <option value="us">United States</option>
  <option value="uk" selected>United Kingdom</option>
  <optgroup label="European">
    <option value="de">Germany</option>
  </optgroup>
</select>

<textarea name="message" rows="5" cols="40" placeholder="Write here..."></textarea>
```

## Radio and Checkboxes

```html
<fieldset>
  <legend>Payment Method</legend>
  <label><input type="radio" name="payment" value="card" checked> Card</label>
  <label><input type="radio" name="payment" value="paypal"> PayPal</label>
</fieldset>

<fieldset>
  <legend>Interests</legend>
  <label><input type="checkbox" name="interests" value="sports"> Sports</label>
  <label><input type="checkbox" name="interests" value="music" checked> Music</label>
</fieldset>
```

Radio buttons with same `name` allow only one selection. `<fieldset>` + `<legend>` groups controls semantically.

## Datalist (Autocomplete Suggestions)

```html
<input list="browsers" name="browser">
<datalist id="browsers">
  <option value="Chrome">
  <option value="Firefox">
  <option value="Safari">
</datalist>
```

Unlike `<select>`, allows custom input while suggesting options.

## Built-in Validation

```html
<form>
  <input type="email" required>
  <input type="text" minlength="3" maxlength="20" required>
  <input type="number" min="18" max="99">
  <input type="text" pattern="[A-Za-z]{3}" title="Three letters">
  <button type="submit">Submit</button>
</form>
```

- `:valid` / `:invalid` CSS pseudo-classes for styling validation state
- `novalidate` on `<form>` disables all built-in validation
- Disabled inputs are NOT submitted

## Buttons

```html
<button type="submit">Submit Form</button>    <!-- Default inside form -->
<button type="reset">Reset Form</button>
<button type="button">Regular Button</button> <!-- No form action -->
```

Prefer `<button>` over `<input type="submit">` - buttons can contain HTML (icons, spans). A `<button>` inside `<form>` defaults to `type="submit"`.

## Gotchas

- **Missing labels**: screen readers cannot identify input purpose
- **No `name` attribute**: data won't be submitted to server
- **Button default type**: `<button>` inside form defaults to `submit`, not `button`
- **`disabled` vs `readonly`**: disabled inputs are excluded from form submission
- **Radio without shared name**: each radio acts independently instead of as a group
- **`border-collapse`**: forgetting it on tables creates double borders

## See Also

- [[html-fundamentals]] - Document structure, semantics
- [[js-dom-and-events]] - Form handling with JavaScript
- [[js-async-and-fetch]] - Submitting forms via fetch API
- [[react-state-and-hooks]] - Controlled form inputs in React
