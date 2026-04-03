---
title: PHP Arrays
category: fundamentals
tags: [php, arrays, array-functions, associative, multidimensional, sorting, destructuring]
---

# PHP Arrays

PHP arrays are ordered maps - they serve as arrays, lists, hash tables, dictionaries, stacks, and queues. Three types: indexed (numeric keys), associative (string keys), and multidimensional (nested). Rich standard library with 70+ functions. Short syntax `[]` replaced `array()` in modern PHP.

## Key Facts

- All PHP arrays are ordered hash maps internally (preserve insertion order)
- Short syntax: `$a = [1, 2, 3]` or `$a = ['key' => 'value']`
- Array unpacking: `[...$a, ...$b]` merges arrays (PHP 7.4+)
- `array_map`, `array_filter`, `array_reduce` for functional operations
- `list()` or `[$a, $b] = $arr` for destructuring assignment
- Arrays are passed by value (copy-on-write); use `&$arr` for reference

## Patterns

### Creation and Access

```php
$fruits = ['apple', 'banana', 'cherry'];
$user = ['name' => 'Alice', 'age' => 30];
$matrix = [[1, 2], [3, 4]];

$fruits[] = 'date';  // append
echo $user['name'];  // Alice
```

### Key Functions

```php
in_array($needle, $haystack, strict: true);  // value search
array_key_exists('name', $user);             // key check
array_search('banana', $fruits);             // returns key

// Functional
array_map(fn($x) => $x * 2, [1, 2, 3]);           // [2, 4, 6]
array_filter([1, 0, 2, ''], fn($x) => $x > 0);    // [1, 2]
array_reduce([1, 2, 3], fn($c, $x) => $c + $x, 0); // 6

// Merge
array_merge($a, $b);              // reindex numeric keys
$a + $b;                          // union (first wins for duplicates)
array_column($records, 'name');   // extract column from 2D

// Destructuring
[$first, $second] = [10, 20];
['name' => $name, 'age' => $age] = $user;
```

### Sorting

```php
sort($arr);      // by value ascending, reindex
asort($arr);     // by value, preserve keys
ksort($arr);     // by key
usort($arr, fn($a, $b) => $a <=> $b);  // custom
```

## Gotchas

- `array_merge` reindexes numeric keys; `+` preserves them (first value wins for duplicates)
- `in_array` uses loose comparison by default - pass `true` as third arg
- `array_filter` without callback removes all falsy values including `0` and `"0"`
- `foreach ($arr as &$value)` modifies in place - `unset($value)` after or last element gets overwritten

## See Also

- [[php-type-system]] - array as fundamental PHP type
- [[php-control-structures]] - foreach loops and array iteration
