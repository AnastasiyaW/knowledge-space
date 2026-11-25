---
title: "HTML-Tabellen und Formulare"
category: concepts
tags: [web-frontend, html, forms, accessibility, validation]
level: 3
source_sha256: db6926b6d3b1d6c5a206c7a9f0329c4b4a869303c7d6bdf04e8c4a33953f43bf
translation: machine
translated_at: '2026-10-24'
---
# HTML-Tabellen und Formulare {#html-tables-and-forms}

Tabellen stellen tabellarische Daten dar; Formulare erfassen Benutzereingaben. Beide erfordern korrekte Semantik für die Barrierefreiheit.

## Tabellen {#tables}

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

- `<th>` für Kopfzellen (Screenreader kündigen Spalten- bzw. Zeilennamen an)
- `scope="col"` / `scope="row"` verdeutlicht die Richtung
- `<caption>` beschreibt den Zweck der Tabelle (Barrierefreiheit)
- `colspan` / `rowspan` für zusammengeführte Zellen
- Tabellen niemals für das Seitenlayout verwenden

```css
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
tbody tr:nth-child(even) { background-color: #fafafa; }
```

`border-collapse: collapse` ist fast immer nötig – ohne diese Eigenschaft haben Zellen getrennte Rahmen mit Lücken.

## Formularelement {#form-element}

```html
<form action="/submit" method="POST" enctype="multipart/form-data">
  <!-- form controls -->
</form>
```

| Attribut | Zweck |
|-----------|---------|
| `action` | URL, an die die Daten gesendet werden |
| `method` | `GET` (Daten in der URL) oder `POST` (Daten im Body) |
| `enctype` | `multipart/form-data` ist für Datei-Uploads erforderlich |
| `novalidate` | Deaktiviert die integrierte Validierung |

**GET vs. POST**: GET für Suche und Filter (als Lesezeichen speicherbar, in der URL sichtbar). POST für sensible Daten (Login, Registrierung, Datei-Upload).

## Eingabetypen {#input-types}

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

## Eingabeattribute {#input-attributes}

| Attribut | Zweck |
|-----------|---------|
| `name` | Schlüssel für die übermittelten Daten (erforderlich) |
| `value` | Standard- bzw. aktueller Wert |
| `placeholder` | Hinweistext (verschwindet beim Fokussieren) |
| `required` | Muss ausgefüllt werden |
| `disabled` | Keine Interaktion möglich, wird NICHT übermittelt |
| `readonly` | Nicht editierbar, wird übermittelt |
| `autofocus` | Fokus beim Laden der Seite |
| `maxlength` / `minlength` | Zeichenbegrenzungen |
| `pattern` | Validierung per Regex |
| `min` / `max` / `step` | Zahlen- bzw. Datumsbereich |
| `multiple` | Mehrere Werte erlauben |
| `autocomplete` | Hinweis für die Browser-Autovervollständigung |

## Labels {#labels}

Jede Eingabe MUSS ein Label haben. Screenreader lesen sie vor; ein Klick auf das Label setzt den Fokus auf die Eingabe.

```html
<!-- Method 1: for/id (preferred) -->
<label for="email-input">Email:</label>
<input type="email" id="email-input" name="email">

<!-- Method 2: wrapping -->
<label>Email: <input type="email" name="email"></label>
```

## Select und Textarea {#select-and-textarea}

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

## Radio-Buttons und Checkboxen {#radio-and-checkboxes}

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

Radio-Buttons mit gleichem `name` erlauben nur eine Auswahl. `<fieldset>` + `<legend>` gruppiert Steuerelemente semantisch.

## Datalist (Autovervollständigungsvorschläge) {#datalist-autocomplete-suggestions}

```html
<input list="browsers" name="browser">
<datalist id="browsers">
  <option value="Chrome">
  <option value="Firefox">
  <option value="Safari">
</datalist>
```

Anders als bei `<select>` ist eine eigene Eingabe möglich, während Optionen vorgeschlagen werden.

## Integrierte Validierung {#built-in-validation}

```html
<form>
  <input type="email" required>
  <input type="text" minlength="3" maxlength="20" required>
  <input type="number" min="18" max="99">
  <input type="text" pattern="[A-Za-z]{3}" title="Three letters">
  <button type="submit">Submit</button>
</form>
```

- CSS-Pseudoklassen `:valid` / `:invalid` zur Gestaltung des Validierungszustands
- `novalidate` auf `<form>` deaktiviert die gesamte integrierte Validierung
- Deaktivierte Eingaben werden NICHT übermittelt

## Schaltflächen {#buttons}

```html
<button type="submit">Submit Form</button>    <!-- Default inside form -->
<button type="reset">Reset Form</button>
<button type="button">Regular Button</button> <!-- No form action -->
```

`<button>` ist `<input type="submit">` vorzuziehen – Buttons können HTML enthalten (Icons, spans). Ein `<button>` innerhalb von `<form>` hat standardmäßig `type="submit"`.

## Fallstricke {#gotchas}

- **Fehlende Labels**: Screenreader können den Zweck einer Eingabe nicht erkennen
- **Kein `name`-Attribut**: Daten werden nicht an den Server übermittelt
- **Standardtyp von Buttons**: `<button>` innerhalb eines Formulars ist standardmäßig `submit`, nicht `button`
- **`disabled` vs. `readonly`**: Deaktivierte Eingaben werden vom Formularversand ausgeschlossen
- **Radio-Buttons ohne gemeinsamen Namen**: Jeder Radio-Button verhält sich unabhängig statt als Gruppe
- **`border-collapse`**: Wer es bei Tabellen vergisst, erzeugt doppelte Rahmen

## Siehe auch {#see-also}

- [[html-fundamentals]] - Dokumentstruktur, Semantik
- [[js-dom-and-events]] - Formularverarbeitung mit JavaScript
- [[js-async-and-fetch]] - Formulare über die Fetch-API absenden
- [[react-state-and-hooks]] - Kontrollierte Formulareingaben in React
