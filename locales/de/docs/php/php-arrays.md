---
title: "PHP-Arrays"
category: fundamentals
tags: [php, arrays, array-functions, associative, multidimensional, sorting, destructuring]
level: 3
source_sha256: 80159d82672ac05369271c16ae0279c52cd4b333b708135fc9abb370dc25f830
translation: machine
translated_at: '2026-10-24'
---
# PHP-Arrays {#php-arrays}

PHP-Arrays sind geordnete Maps – sie dienen als Arrays, Listen, Hash-Tabellen, Dictionaries, Stacks und Queues. Drei Typen: indizierte (numerische Schlüssel), assoziative (String-Schlüssel) und mehrdimensionale (verschachtelte). Umfangreiche Standardbibliothek mit über 70 Funktionen. Die Kurzsyntax `[]` hat in modernem PHP `array()` ersetzt.

## Wichtige Fakten {#key-facts}

- Alle PHP-Arrays sind intern geordnete Hash-Maps (die Einfügereihenfolge bleibt erhalten)
- Kurzsyntax: `$a = [1, 2, 3]` oder `$a = ['key' => 'value']`
- Array-Entpackung: `[...$a, ...$b]` führt Arrays zusammen (PHP 7.4+)
- `array_map`, `array_filter`, `array_reduce` für funktionale Operationen
- `list()` oder `[$a, $b] = $arr` für Destrukturierungszuweisung
- Arrays werden per Wert übergeben (Copy-on-Write); für Referenzen `&$arr` verwenden

## Muster {#patterns}

### Erstellung und Zugriff {#creation-and-access}

```php
$fruits = ['apple', 'banana', 'cherry'];
$user = ['name' => 'Alice', 'age' => 30];
$matrix = [[1, 2], [3, 4]];

$fruits[] = 'date';  // append
echo $user['name'];  // Alice
```

### Wichtige Funktionen {#key-functions}

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

### Sortierung {#sorting}

```php
sort($arr);      // by value ascending, reindex
asort($arr);     // by value, preserve keys
ksort($arr);     // by key
usort($arr, fn($a, $b) => $a <=> $b);  // custom
```

## Fallstricke {#gotchas}

- `array_merge` indiziert numerische Schlüssel neu; `+` behält sie bei (bei Duplikaten gewinnt der erste Wert)
- `in_array` verwendet standardmäßig einen lockeren Vergleich – als dritten Parameter `true` übergeben
- `array_filter` ohne Callback entfernt alle falsy-Werte einschließlich `0` und `"0"`
- `foreach ($arr as &$value)` ändert in place – `unset($value)` danach verwenden, sonst wird das letzte Element überschrieben

## Siehe auch {#see-also}

- [[php-type-system]] – Array als grundlegender PHP-Typ
- [[php-control-structures]] – foreach-Schleifen und Array-Iteration
