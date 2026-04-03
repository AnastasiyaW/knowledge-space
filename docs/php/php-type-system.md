---
title: PHP Type System
category: fundamentals
tags: [php, types, casting, strict-types, comparison, strings, type-juggling]
---

# PHP Type System

PHP is dynamically typed with optional strict mode. Eight primitive types: int, float, string, bool, array, object, null, resource. Type juggling performs implicit conversions; `declare(strict_types=1)` disables this per-file. Comparison operators (`==` vs `===`) are a major source of bugs - always prefer strict comparison.

## Key Facts

- `declare(strict_types=1)` at file top enforces type hints (no implicit conversion)
- **Scalar types**: int, float, string, bool; **Compound**: array, object; **Special**: null, resource
- `===` compares value AND type; `==` uses type juggling (`"0" == false` is true)
- String interpolation: double quotes only (`"Hello $name"` or `"Hello {$user->name}"`)
- Heredoc (`<<<EOT`) and Nowdoc (`<<<'EOT'`) for multiline strings
- Union types (PHP 8): `int|string`, nullable: `?string` = `string|null`
- `isset()` checks existence AND non-null; `empty()` is true for `0, "", null, false, []`

## Patterns

### Type Declarations

```php
declare(strict_types=1);

function add(int $a, int $b): int {
    return $a + $b;
}

function find(int $id): ?User { /* ... */ }     // nullable return
function process(): int|false { /* ... */ }      // union type
function log(): void { /* ... */ }               // no return value
```

### Type Checking and Casting

```php
gettype($var);      // "integer", "string", etc.
is_int($var);       // boolean type check

$int = (int)"42";       // 42
$float = (float)"3.14"; // 3.14
$bool = (bool)"";       // false

intval("0b1010", 2);    // 10 (binary)
intval("0xFF", 16);     // 255 (hex)
```

### String Operations

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

## Gotchas

- `"0" == false` and `"" == false` are both true with loose comparison - use `===`
- `empty("0")` returns true - surprising for form input validation
- String concatenation uses `.` not `+`; `"3" + "5"` = `8` (arithmetic!)
- `isset()` returns false for null even if variable exists; `array_key_exists()` doesn't

## See Also

- [[php-arrays]] - array type and manipulation
- [[php-control-structures]] - match expression, comparison operators
- [[php-oop-fundamentals]] - typed properties and return types
