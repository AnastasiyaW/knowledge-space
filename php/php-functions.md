---
title: PHP Functions
category: fundamentals
tags: [php, functions, closures, arrow-functions, scope, callbacks]
---

# PHP Functions

Functions encapsulate reusable logic. PHP supports named functions, anonymous functions (closures), arrow functions (PHP 7.4+), and first-class callable syntax (PHP 8.1+). Understanding scope rules and closure binding is essential for working with [[php-arrays]] callbacks and [[laravel-routing]] route definitions.

## Key Facts

- Functions are not hoisted in conditionals but are in global scope (can call before definition in same file)
- Parameters can have type declarations, default values, and variadic (`...$args`) syntax
- Return types declared with `: type` after parameter list
- Variables are function-scoped by default (no access to outer variables without `global` or `use`)
- Closures: `function() use ($var) { ... }` captures outer variables by value
- Arrow functions: `fn($x) => $x * 2` - auto-capture outer scope by value, single expression only
- Named arguments (PHP 8.0+): `str_pad(string: 'hi', length: 10, pad_type: STR_PAD_LEFT)`
- First-class callable: `$fn = strlen(...)` creates Closure from function name (PHP 8.1+)

## Patterns

### Function declarations

```php
<?php
// Basic function with type declarations
function calculateDiscount(float $price, int $percent = 10): float {
    return $price * (1 - $percent / 100);
}

// Variadic parameters
function sum(int|float ...$numbers): int|float {
    return array_sum($numbers);
}
echo sum(1, 2, 3, 4); // 10

// Spread operator for argument unpacking
$args = [10, 20, 30];
echo sum(...$args); // 60

// Named arguments (PHP 8.0+)
$result = calculateDiscount(percent: 15, price: 100.0);
```

### Closures and arrow functions

```php
<?php
// Closure - captures $tax by value
$tax = 0.2;
$addTax = function(float $price) use ($tax): float {
    return $price * (1 + $tax);
};
echo $addTax(100); // 120

// Capture by reference
$counter = 0;
$increment = function() use (&$counter) {
    $counter++;
};
$increment();
echo $counter; // 1

// Arrow function (PHP 7.4+) - auto-captures, single expression
$addTax = fn(float $price): float => $price * (1 + $tax);

// Used with array functions
$prices = [10, 20, 30];
$withTax = array_map(fn($p) => $p * 1.2, $prices);
$expensive = array_filter($prices, fn($p) => $p > 15);
```

### Callbacks and callables

```php
<?php
// String function name
$result = array_map('strtoupper', $names);

// Static method
$result = array_map([MyClass::class, 'process'], $items);

// First-class callable syntax (PHP 8.1+)
$result = array_map(strtoupper(...), $names);
$result = array_map($object->method(...), $items);

// Callable type hint
function apply(callable $fn, array $items): array {
    return array_map($fn, $items);
}
```

### Scope and global

```php
<?php
$config = 'production';

function getConfig(): string {
    // $config is NOT accessible here (function scope)
    global $config; // pulls from global scope (avoid this pattern)
    return $config;
}

// Better: pass as parameter or use dependency injection
function getConfig(string $config): string {
    return $config;
}
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| Variable undefined inside function | PHP has function scope, not block scope | Pass as parameter or `use ($var)` in closure |
| Closure captures stale value | `use ($var)` captures by value at definition time | Use `use (&$var)` for reference capture |
| Arrow function can't have statements | Arrow functions support only single expression | Use full closure `function() use () { ... }` |
| `callable` type hint doesn't work on class property | Limitation in PHP - `callable` not allowed for properties | Use `Closure` type or `\Closure` instead |
| Named argument breaks after rename | Named args bind to parameter names | Treat parameter names as API surface |

## See Also

- [[php-oop-fundamentals]] - methods are functions on classes
- [[php-arrays]] - callbacks with array_map, array_filter, array_reduce
- https://www.php.net/manual/en/language.functions.php
- https://www.php.net/manual/en/functions.arrow.php
- https://www.php.net/manual/en/functions.first_class_callable_syntax.php
