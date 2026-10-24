---
title: "Tableaux et formulaires HTML"
category: concepts
tags: [web-frontend, html, forms, accessibility, validation]
level: 3
source_sha256: db6926b6d3b1d6c5a206c7a9f0329c4b4a869303c7d6bdf04e8c4a33953f43bf
translation: machine
translated_at: '2026-10-24'
---
# Tableaux et formulaires HTML {#html-tables-and-forms}

Les tableaux affichent des données tabulaires ; les formulaires collectent les saisies des utilisateurs. Les deux nécessitent une sémantique correcte pour l'accessibilité.

## Tableaux {#tables}

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

- `<th>` pour les en-têtes (les lecteurs d'écran annoncent les noms des colonnes/lignes)
- `scope="col"` / `scope="row"` précise le sens
- `<caption>` décrit la finalité du tableau (accessibilité)
- `colspan` / `rowspan` pour les cellules fusionnées
- Ne jamais utiliser les tableaux pour la mise en page

```css
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
tbody tr:nth-child(even) { background-color: #fafafa; }
```

`border-collapse: collapse` est presque toujours nécessaire : sans lui, les cellules ont des bordures séparées avec des espaces.

## Élément Form {#form-element}

```html
<form action="/submit" method="POST" enctype="multipart/form-data">
  <!-- form controls -->
</form>
```

| Attribut | Rôle |
|-----------|---------|
| `action` | URL vers laquelle les données sont envoyées |
| `method` | `GET` (données dans l'URL) ou `POST` (données dans le corps) |
| `enctype` | `multipart/form-data` requis pour l'envoi de fichiers |
| `novalidate` | Désactive la validation intégrée |

**GET vs POST** : GET pour les recherches/filtres (ajoutable en favori, visible dans l'URL). POST pour les données sensibles (connexion, inscription, envoi de fichiers).

## Types d'input {#input-types}

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

## Attributs des inputs {#input-attributes}

| Attribut | Rôle |
|-----------|---------|
| `name` | Clé des données envoyées (obligatoire) |
| `value` | Valeur par défaut/actuelle |
| `placeholder` | Texte d'indication (disparaît au focus) |
| `required` | Champ obligatoire |
| `disabled` | Non interactif, NON envoyé |
| `readonly` | Non modifiable, EST envoyé |
| `autofocus` | Focus au chargement de la page |
| `maxlength` / `minlength` | Limites de caractères |
| `pattern` | Validation par expression régulière |
| `min` / `max` / `step` | Plage de nombres/dates |
| `multiple` | Autorise plusieurs valeurs |
| `autocomplete` | Indication de remplissage automatique du navigateur |

## Labels {#labels}

Chaque input DOIT avoir un label. Les lecteurs d'écran les lisent ; cliquer sur un label donne le focus à l'input.

```html
<!-- Method 1: for/id (preferred) -->
<label for="email-input">Email:</label>
<input type="email" id="email-input" name="email">

<!-- Method 2: wrapping -->
<label>Email: <input type="email" name="email"></label>
```

## Select et Textarea {#select-and-textarea}

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

## Radio et checkboxes {#radio-and-checkboxes}

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

Les boutons radio ayant le même `name` n'autorisent qu'une seule sélection. `<fieldset>` + `<legend>` regroupe les contrôles de façon sémantique.

## Datalist (suggestions de saisie) {#datalist-autocomplete-suggestions}

```html
<input list="browsers" name="browser">
<datalist id="browsers">
  <option value="Chrome">
  <option value="Firefox">
  <option value="Safari">
</datalist>
```

Contrairement à `<select>`, permet une saisie libre tout en proposant des options.

## Validation intégrée {#built-in-validation}

```html
<form>
  <input type="email" required>
  <input type="text" minlength="3" maxlength="20" required>
  <input type="number" min="18" max="99">
  <input type="text" pattern="[A-Za-z]{3}" title="Three letters">
  <button type="submit">Submit</button>
</form>
```

- Pseudo-classes CSS `:valid` / `:invalid` pour styliser l'état de validation
- `novalidate` sur `<form>` désactive toute la validation intégrée
- Les inputs désactivés ne sont PAS envoyés

## Boutons {#buttons}

```html
<button type="submit">Submit Form</button>    <!-- Default inside form -->
<button type="reset">Reset Form</button>
<button type="button">Regular Button</button> <!-- No form action -->
```

Préférer `<button>` à `<input type="submit">` : les boutons peuvent contenir du HTML (icônes, spans). Un `<button>` à l'intérieur d'un `<form>` a par défaut `type="submit"`.

## Pièges courants {#gotchas}

- **Labels manquants** : les lecteurs d'écran ne peuvent pas identifier le rôle de l'input
- **Absence d'attribut `name`** : les données ne seront pas envoyées au serveur
- **Type par défaut du bouton** : un `<button>` dans un formulaire vaut `submit` par défaut, et non `button`
- **`disabled` vs `readonly`** : les inputs désactivés sont exclus de l'envoi du formulaire
- **Radio sans name commun** : chaque radio agit indépendamment au lieu de former un groupe
- **`border-collapse`** : l'oublier sur les tableaux crée des bordures doubles

## Voir aussi {#see-also}

- [[html-fundamentals]] - Structure du document, sémantique
- [[js-dom-and-events]] - Gestion des formulaires en JavaScript
- [[js-async-and-fetch]] - Envoi de formulaires via l'API fetch
- [[react-state-and-hooks]] - Champs de formulaire contrôlés en React
