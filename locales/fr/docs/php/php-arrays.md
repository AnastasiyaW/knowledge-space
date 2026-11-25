---
title: "Tableaux PHP"
category: fundamentals
tags: [php, arrays, array-functions, associative, multidimensional, sorting, destructuring]
level: 3
source_sha256: 80159d82672ac05369271c16ae0279c52cd4b333b708135fc9abb370dc25f830
translation: machine
translated_at: '2026-10-24'
---
# Tableaux PHP {#php-arrays}

Les tableaux PHP sont des tables de hachage ordonnées : ils servent à la fois de tableaux, de listes, de tables de hachage, de dictionnaires, de piles et de files. Trois types existent : indexés (clés numériques), associatifs (clés chaînes) et multidimensionnels (imbriqués). La bibliothèque standard propose plus de 70 fonctions. La syntaxe courte `[]` a remplacé `array()` dans le PHP moderne.

## Points clés {#key-facts}

- Tous les tableaux PHP sont en interne des tables de hachage ordonnées (l'ordre d'insertion est conservé)
- Syntaxe courte : `$a = [1, 2, 3]` ou `$a = ['key' => 'value']`
- Déballage de tableaux : `[...$a, ...$b]` fusionne des tableaux (PHP 7.4+)
- `array_map`, `array_filter`, `array_reduce` pour les opérations fonctionnelles
- `list()` ou `[$a, $b] = $arr` pour l'affectation par déstructuration
- Les tableaux sont passés par valeur (copie à l'écriture) ; utiliser `&$arr` pour une référence

## Modèles {#patterns}

### Création et accès {#creation-and-access}

```php
$fruits = ['apple', 'banana', 'cherry'];
$user = ['name' => 'Alice', 'age' => 30];
$matrix = [[1, 2], [3, 4]];

$fruits[] = 'date';  // append
echo $user['name'];  // Alice
```

### Fonctions clés {#key-functions}

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

### Tri {#sorting}

```php
sort($arr);      // by value ascending, reindex
asort($arr);     // by value, preserve keys
ksort($arr);     // by key
usort($arr, fn($a, $b) => $a <=> $b);  // custom
```

## Pièges {#gotchas}

- `array_merge` réindexe les clés numériques ; `+` les conserve (en cas de doublons, la première valeur l'emporte)
- `in_array` utilise une comparaison souple par défaut : passer `true` comme troisième argument
- `array_filter` sans fonction de rappel supprime toutes les valeurs falsy, y compris `0` et `"0"`
- `foreach ($arr as &$value)` modifie en place : faire `unset($value)` après, sinon le dernier élément sera écrasé

## Voir aussi {#see-also}

- [[php-type-system]] - le tableau comme type fondamental de PHP
- [[php-control-structures]] - boucles foreach et itération sur les tableaux
