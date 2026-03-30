---
title: PHP Arrays
category: fundamentals
tags: [php, arrays, array-functions, associative, multidimensional]
---

# PHP Arrays

PHP arrays are ordered maps that serve as arrays, lists, hash tables, dictionaries, collections, stacks, and queues. They are the most versatile and heavily-used data structure in PHP. Understanding array manipulation is essential for working with database results, API payloads, form data, and [[laravel-eloquent-orm]] collections.

## Key Facts

- PHP has one array type that handles both indexed (numeric keys) and associative (string keys) arrays
- Arrays are copy-on-write (assigning to a new variable creates a shallow copy)
- Short array syntax `[]` replaces `array()` since PHP 5.4
- Array unpacking with spread operator: `[...$arr1, ...$arr2]` (PHP 7.4+ for indexed, 8.1+ for string keys)
- Array destructuring: `[$a, $b] = [1, 2]` or `['name' => $name] = $user`
- `count()` returns number of elements; `empty()` checks if array has no elements
- Named arguments + arrays: `array_map(callback: fn($x) => $x * 2, array: $items)` (PHP 8.0+)
- Maximum practical array size limited by available memory (`memory_limit` in php.ini)

## Patterns

### Creating and accessing arrays

```php
<?php
// Indexed array
$fruits = ['apple', 'banana', 'cherry'];
echo $fruits[0]; // 'apple'

// Associative array
$user = [
    'name'  => 'Admin',
    'email' => 'admin@mail.com',
    'role'  => 'admin',
];

// Multidimensional
$matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
];
echo $matrix[1][2]; // 6

// Adding elements
$fruits[] = 'date';               // append
$user['age'] = 30;                // add key

// Destructuring
['name' => $name, 'email' => $email] = $user;
[$first, , $third] = $fruits;     // skip second element
```

### Essential array functions

```php
<?php
// Searching
in_array('banana', $fruits);              // true (loose)
in_array('banana', $fruits, true);        // true (strict)
array_search('banana', $fruits);          // 1 (key)
array_key_exists('name', $user);          // true

// Transforming
$upper = array_map('strtoupper', $fruits);
$even = array_filter($nums, fn($n) => $n % 2 === 0);
$sum = array_reduce($nums, fn($carry, $n) => $carry + $n, 0);

// Sorting (modifies in place, returns bool)
sort($fruits);          // by value, reindex
asort($user);           // by value, keep keys
ksort($user);           // by key
usort($items, fn($a, $b) => $a['price'] <=> $b['price']); // custom

// Merging
$merged = array_merge($arr1, $arr2);      // reindex numeric keys
$merged = [...$arr1, ...$arr2];            // spread operator (PHP 7.4+)
$combined = $arr1 + $arr2;                 // union (keeps first key)

// Slicing and chunking
$slice = array_slice($fruits, 1, 2);       // ['banana', 'cherry']
$chunks = array_chunk($items, 10);         // split into groups of 10

// Keys and values
$keys = array_keys($user);                 // ['name', 'email', 'role']
$values = array_values($user);             // ['Admin', 'admin@...', 'admin']
$flipped = array_flip($user);              // swap keys/values
```

### Iteration patterns

```php
<?php
// Counting sum (manual approach)
$sum = 0;
foreach ($numbers as $num) {
    $sum += $num;
}

// Average
$avg = array_sum($numbers) / count($numbers);

// Building string from array
$str = implode(' ', $words);  // join with separator

// String to array
$parts = explode(',', 'a,b,c'); // ['a', 'b', 'c']
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `in_array(0, ['foo'])` returns true | Loose comparison (type juggling) | Use `in_array($val, $arr, true)` for strict |
| `array_merge` reindexes numeric keys | By design - numeric keys are renumbered | Use `+` operator or spread to preserve keys |
| `foreach` reference variable persists | `&$item` stays bound after loop | `unset($item)` after `foreach` |
| `count(null)` returns 0 (with warning in 8.0+) | `count()` expects array or Countable | Check `is_array()` first or use `??` |
| Sorting returns `true` not the array | `sort()`/`usort()` etc. modify in place | Do not chain: `sort($arr); return $arr;` |
| `array_filter` preserves keys | By design - keys are not re-indexed | Wrap with `array_values()` if needed |

## See Also

- [[php-functions]] - closures used with array_map/filter/reduce
- [[laravel-eloquent-orm]] - Collections extend array functionality
- https://www.php.net/manual/en/language.types.array.php
- https://www.php.net/manual/en/ref.array.php
