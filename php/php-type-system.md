---
title: PHP Type System
category: fundamentals
tags: [php, types, casting, strict-types, comparison]
---

# PHP Type System

PHP is dynamically typed with optional type declarations (since PHP 7.0+). Understanding type juggling, strict comparisons, and type declarations is critical for avoiding subtle bugs - especially in conditionals, database queries, and API responses.

## Key Facts

- PHP has 10 primitive types: `int`, `float`, `string`, `bool`, `array`, `object`, `callable`, `iterable`, `null`, `never` (8.1+)
- Variables are not declared with a type - type is determined by the assigned value
- `declare(strict_types=1)` enables strict mode per-file (no implicit coercion for scalar type declarations)
- Type declarations work on function params, return types, and class properties (7.4+)
- Union types (`int|string`) since PHP 8.0, intersection types (`Countable&Iterator`) since 8.1
- `mixed` type (8.0+) explicitly allows any type
- `null` is its own type; nullable syntax: `?string` or `string|null`
- See [[php-control-structures]] for how types affect conditionals

## Patterns

```php
<?php
declare(strict_types=1); // must be first statement in file

// Type declarations
function calculateTotal(float $price, int $quantity): float {
    return $price * $quantity;
}

// Union types (PHP 8.0+)
function processId(int|string $id): string {
    return (string) $id;
}

// Nullable types
function findUser(?int $id): ?User {
    if ($id === null) return null;
    return User::find($id);
}

// Type casting
$val = "42abc";
$int = (int) $val;       // 42 (truncates at first non-numeric)
$float = (float) $val;   // 42.0
$bool = (bool) $val;     // true (non-empty string)
$arr = (array) $obj;     // object properties become array keys
```

### Comparison operators

```php
<?php
// Loose comparison (==) - type juggling
0 == "foo"     // true in PHP 7, false in PHP 8+
"" == null     // true
"0" == false   // true
[] == false    // true

// Strict comparison (===) - no type juggling
0 === "0"      // false (different types)
null === false // false

// Spaceship operator (<=>)
1 <=> 2        // -1
1 <=> 1        // 0
2 <=> 1        // 1

// Always prefer === over == to avoid type juggling bugs
```

### Type checking functions

```php
<?php
is_int($val);       // true if integer
is_string($val);    // true if string
is_array($val);     // true if array
is_null($val);      // true if null
isset($val);        // true if set AND not null
empty($val);        // true if "", 0, "0", null, false, []
gettype($val);      // returns type as string
$val instanceof Foo // true if $val is instance of Foo
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `0 == "foo"` returns true (PHP 7) | Loose comparison coerces string to int 0 | Use `===` strict comparison |
| Function accepts wrong type silently | `strict_types` not declared | Add `declare(strict_types=1)` at file top |
| `empty("0")` returns true | `"0"` is considered empty in PHP | Use `$val !== ""` or `strlen($val) > 0` |
| `(int) "12abc"` silently gives 12 | PHP truncates at first non-numeric char | Validate with `is_numeric()` or `filter_var()` |
| `null` vs `false` vs `""` confusion | Three distinct falsy values | Use `===` and be explicit about expected types |

## See Also

- [[php-control-structures]] - conditionals, loops, match expression
- [[php-arrays]] - array types and operations
- https://www.php.net/manual/en/language.types.php
- https://www.php.net/manual/en/language.types.type-juggling.php
- https://www.php.net/manual/en/language.types.declarations.php
