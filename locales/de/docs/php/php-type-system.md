---
title: "PHP-Typsystem"
category: fundamentals
tags: [php, types, casting, strict-types, comparison, strings, type-juggling]
level: 3
source_sha256: 3c67b6ec50e018c7b909abf2e9bf2c34c3e8d3994c3e8ee23a1ce259f9e0625c
translation: machine
translated_at: '2026-10-24'
---
# PHP-Typsystem {#php-type-system}

PHP ist dynamisch typisiert mit optionalem Strict Mode. Acht primitive Typen: int, float, string, bool, array, object, null, resource. Type Juggling führt implizite Konvertierungen durch; `declare(strict_types=1)` deaktiviert dies pro Datei. Vergleichsoperatoren (`==` vs `===`) sind eine häufige Fehlerquelle - verwende immer den strikten Vergleich.

## Wichtige Fakten {#key-facts}

- `declare(strict_types=1)` am Dateianfang erzwingt Typhinweise (keine implizite Konvertierung)
- **Skalare Typen**: int, float, string, bool; **Zusammengesetzte Typen**: array, object; **Spezielle Typen**: null, resource
- `===` vergleicht Wert UND Typ; `==` verwendet Type Juggling (`"0" == false` ist true)
- String-Interpolation: nur mit doppelten Anführungszeichen (`"Hello $name"` oder `"Hello {$user->name}"`)
- Heredoc (`<<<EOT`) und Nowdoc (`<<<'EOT'`) für mehrzeilige Strings
- Union-Typen (PHP 8): `int|string`, nullable: `?string` = `string|null`
- `isset()` prüft Existenz UND Nicht-Null; `empty()` ist true für `0, "", null, false, []`

## Muster {#patterns}

### Typdeklarationen {#type-declarations}

```php
declare(strict_types=1);

function add(int $a, int $b): int {
    return $a + $b;
}

function find(int $id): ?User { /* ... */ }     // nullable return
function process(): int|false { /* ... */ }      // union type
function log(): void { /* ... */ }               // no return value
```

### Typprüfung und Casting {#type-checking-and-casting}

```php
gettype($var);      // "integer", "string", etc.
is_int($var);       // boolean type check

$int = (int)"42";       // 42
$float = (float)"3.14"; // 3.14
$bool = (bool)"";       // false

intval("0b1010", 2);    // 10 (binary)
intval("0xFF", 16);     // 255 (hex)
```

### String-Operationen {#string-operations}

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

## Stolperfallen {#gotchas}

- `"0" == false` und `"" == false` sind beide true beim losen Vergleich - verwende `===`
- `empty("0")` gibt true zurück - überraschend bei der Validierung von Formulareingaben
- Stringverkettung erfolgt mit `.` nicht `+`; `"3" + "5"` = `8` (Arithmetik!)
- `isset()` gibt false für null zurück, auch wenn die Variable existiert; `array_key_exists()` tut das nicht

## Siehe auch {#see-also}

- [[php-arrays]] - Array-Typ und Manipulation
- [[php-control-structures]] - match-Ausdruck, Vergleichsoperatoren
- [[php-oop-fundamentals]] - typisierte Eigenschaften und Rückgabetypen
