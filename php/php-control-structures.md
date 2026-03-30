---
title: PHP Control Structures
category: fundamentals
tags: [php, conditionals, loops, match, switch, operators]
---

# PHP Control Structures

Branching and looping constructs that control program execution flow. Includes if/else/elseif, switch, match (PHP 8.0+), for, foreach, while, and logical operators. Every non-trivial PHP program uses these for conditional rendering, data processing, and request handling.

## Key Facts

- `if`/`elseif`/`else` - standard branching; `elseif` should be written as one word (not `else if`) for compatibility with alternative syntax
- `switch` - loose comparison (`==`) against cases; falls through without `break`
- `match` (PHP 8.0+) - strict comparison (`===`), returns a value, no fall-through, throws `UnhandledMatchError` if no match
- Logical operators: `&&` / `and`, `||` / `or`, `!` (negation), `xor`
- `&&` and `||` have higher precedence than `and`/`or` - mixing them causes bugs
- Ternary: `$x ? $y : $z`; null coalescing: `$x ?? $default` (returns `$x` if not null)
- Alternative syntax for templates: `if(): ... endif;` used in [[laravel-blade-templates]]

## Patterns

### if / elseif / else

```php
<?php
$color = 'red';

if ($color === 'red') {
    echo 'stop';
} elseif ($color === 'yellow' || $color === 'orange') {
    echo 'ready';
} else {
    echo 'go';
}

// Negation operator (!) inverts boolean result
if (!$isAuthenticated) {
    redirect('/login');
}
```

### match expression (PHP 8.0+)

```php
<?php
$status = 200;

$text = match(true) {
    $status >= 200 && $status < 300 => 'Success',
    $status >= 300 && $status < 400 => 'Redirect',
    $status >= 400 && $status < 500 => 'Client Error',
    $status >= 500                  => 'Server Error',
    default                         => 'Unknown',
};

// match with simple value comparison (strict ===)
$label = match($role) {
    'admin'  => 'Administrator',
    'editor' => 'Content Editor',
    'user'   => 'Regular User',
    default  => 'Guest',
};
```

### Loops

```php
<?php
// foreach - primary loop for arrays
$items = ['apple', 'banana', 'cherry'];
foreach ($items as $index => $item) {
    echo "$index: $item\n";
}

// foreach with reference (modify in place)
foreach ($prices as &$price) {
    $price *= 1.1; // increase by 10%
}
unset($price); // always unset reference after loop!

// for - counter-based
for ($i = 0; $i < count($items); $i++) {
    echo $items[$i];
}

// while / do-while
while ($row = $stmt->fetch()) {
    processRow($row);
}
```

### Null coalescing and ternary

```php
<?php
// Null coalescing (??) - returns left if not null
$name = $_GET['name'] ?? 'Anonymous';

// Null coalescing assignment (??=) PHP 7.4+
$config['timeout'] ??= 30;

// Ternary
$label = $count > 0 ? "$count items" : 'empty';

// Short ternary (Elvis operator)
$display = $username ?: 'Guest'; // uses $username if truthy
```

### Logical operators

```php
<?php
// && (AND) - both must be true
if ($age >= 18 && $hasLicense) { /* allowed */ }

// || (OR) - at least one must be true
if ($isAdmin || $isEditor) { /* can edit */ }

// Precedence: && binds tighter than ||
// a || b && c means a || (b && c)
// Use parentheses for clarity:
if (($isAdmin || $isEditor) && $isActive) { /* ... */ }
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `switch` executes multiple cases | Missing `break` after case | Always add `break` or use `match` |
| `else if` error in alternative syntax | `else if` (two words) invalid with `endif` | Write `elseif` as one word |
| Reference variable leaks after `foreach` | `&$item` reference persists after loop | `unset($item)` immediately after loop |
| `$a or $b` behaves unexpectedly | `or` has lower precedence than `=` | Use `||` instead of `or` |
| Infinite loop in `while` | Forgetting to update loop variable | Ensure exit condition changes each iteration |
| `match` throws `UnhandledMatchError` | No matching arm and no `default` | Always include `default` arm |

## See Also

- [[php-type-system]] - type juggling affects conditionals
- [[php-functions]] - functions called within control structures
- https://www.php.net/manual/en/language.control-structures.php
- https://www.php.net/manual/en/control-structures.match.php
