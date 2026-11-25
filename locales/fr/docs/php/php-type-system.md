---
title: "Système de types PHP"
category: fundamentals
tags: [php, types, casting, strict-types, comparison, strings, type-juggling]
level: 3
source_sha256: 3c67b6ec50e018c7b909abf2e9bf2c34c3e8d3994c3e8ee23a1ce259f9e0625c
translation: machine
translated_at: '2026-10-24'
---
# Système de types PHP {#php-type-system}

PHP est typé dynamiquement, avec un mode strict optionnel. Huit types primitifs : int, float, string, bool, array, object, null, resource. La conversion implicite de type (type juggling) effectue des conversions automatiques ; `declare(strict_types=1)` la désactive fichier par fichier. Les opérateurs de comparaison (`==` vs `===`) sont une source majeure de bugs – privilégiez toujours la comparaison stricte.

## Faits clés {#key-facts}

- `declare(strict_types=1)` en haut de fichier impose les indications de type (aucune conversion implicite)
- **Types scalaires** : int, float, string, bool ; **composés** : array, object ; **spéciaux** : null, resource
- `===` compare la valeur ET le type ; `==` utilise la conversion implicite de type (`"0" == false` est vrai)
- Interpolation de chaînes : guillemets doubles uniquement (`"Hello $name"` ou `"Hello {$user->name}"`)
- Heredoc (`<<<EOT`) et Nowdoc (`<<<'EOT'`) pour les chaînes multilignes
- Types union (PHP 8) : `int|string`, nullable : `?string` = `string|null`
- `isset()` vérifie l'existence ET la non-nullité ; `empty()` est vrai pour `0, "", null, false, []`

## Modèles {#patterns}

### Déclarations de types {#type-declarations}

```php
declare(strict_types=1);

function add(int $a, int $b): int {
    return $a + $b;
}

function find(int $id): ?User { /* ... */ }     // nullable return
function process(): int|false { /* ... */ }      // union type
function log(): void { /* ... */ }               // no return value
```

### Vérification et conversion de types {#type-checking-and-casting}

```php
gettype($var);      // "integer", "string", etc.
is_int($var);       // boolean type check

$int = (int)"42";       // 42
$float = (float)"3.14"; // 3.14
$bool = (bool)"";       // false

intval("0b1010", 2);    // 10 (binary)
intval("0xFF", 16);     // 255 (hex)
```

### Opérations sur les chaînes {#string-operations}

```php
$name = "World";
echo "Hello $name";           // interpolation (double quotes)
echo "Value: {$arr['key']}";  // complex expressions need braces

// Heredoc (interpolates) and Nowdoc (literal)
$html = <<<HTML
<div class="$class">$content</div>
HTML;

// Key string functions
strlen($s);                         // byte length
mb_strlen($s);                      // character length (multibyte-safe)
str_contains($haystack, $needle);   // PHP 8
str_starts_with($s, 'prefix');      // PHP 8
```

## Pièges courants {#gotchas}

- `"0" == false` et `"" == false` sont tous deux vrais avec la comparaison lâche – utilisez `===`
- `empty("0")` renvoie vrai – surprenant pour la validation de saisies de formulaire
- La concaténation de chaînes utilise `.` et non `+` ; `"3" + "5"` = `8` (arithmétique !)
- `isset()` renvoie faux pour null même si la variable existe ; `array_key_exists()` non

## Voir aussi {#see-also}

- [[php-arrays]] - type array et manipulation de tableaux
- [[php-control-structures]] - expression match, opérateurs de comparaison
- [[php-oop-fundamentals]] - propriétés typées et types de retour
