---
title: PHP Control Structures and Functions
category: fundamentals
tags: [php, conditionals, loops, match, switch, operators, functions, closures, arrow-functions, named-arguments]
---

# PHP Control Structures and Functions

PHP control structures include if/elseif/else, switch, match (PHP 8), for/foreach/while. The `match` expression uses strict comparison and returns values - preferred over switch. Functions support type hints, default values, variadic params, named arguments (PHP 8), closures (`use`), and arrow functions (`fn`).

## Key Facts

- `match` (PHP 8) = strict comparison, returns value, no fallthrough (replaces switch)
- `foreach ($arr as $key => $value)` - primary array loop
- Ternary: `$x ?: 'default'` (falsy); null coalescing: `$x ?? 'default'` (null only)
- Spaceship `<=>` returns -1, 0, 1 - used in `usort`
- Named arguments (PHP 8): `htmlspecialchars(string: $s, double_encode: false)`
- Arrow functions (PHP 7.4): `fn($x) => $x * 2` - auto-capture, single expression

## Patterns

### Match Expression

```php
$result = match($status) {
    'active', 'verified' => 'Access granted',
    'pending'            => 'Awaiting approval',
    'banned'             => 'Access denied',
    default              => 'Unknown',
};
```

### Functions and Closures

```php
// Typed function
function greet(string $name, string $greeting = "Hello"): string {
    return "$greeting, $name!";
}

// Variadic
function sum(int ...$nums): int { return array_sum($nums); }

// Closure (captures via use)
$tax = 0.2;
$calc = function(float $price) use ($tax): float {
    return $price * (1 + $tax);
};

// Arrow function (auto-captures, single expression)
$calc = fn(float $price): float => $price * (1 + $tax);
```

### Null Handling

```php
$name = $_GET['name'] ?? 'Guest';    // null coalescing
$name ??= 'Guest';                    // null coalescing assignment
$len = $user?->profile?->name;        // nullsafe operator (PHP 8)
```

### String Functions and Dates

```php
// String manipulation
strtolower($s); strtoupper($s);
trim($s); ltrim($s); rtrim($s);
str_replace('old', 'new', $s);
explode(',', $csv);   // string -> array
implode(', ', $arr);  // array -> string
substr($s, 0, 5);
sprintf("Price: $%.2f", 9.99);

// Dates
echo date('Y-m-d H:i:s');           // 2026-04-03 12:00:00
echo date('D, M jS Y', $timestamp); // Thu, Apr 3rd 2026
$dt = new DateTime('2026-01-01');
$dt->modify('+30 days');
$diff = $dt->diff(new DateTime());
```

## Gotchas

- `switch` uses loose comparison and falls through without break - prefer `match`
- Arrow functions capture by value, not reference - mutations don't affect outer scope
- `foreach ($arr as &$value)` - unset `$value` after loop to avoid last-element bugs
- `date()` uses server timezone; `date_default_timezone_set('UTC')` for consistency

## See Also

- [[php-type-system]] - type declarations and strict_types
- [[php-arrays]] - array iteration and functional operations
- [[php-oop-fundamentals]] - methods as functions on objects
