---
title: "PHP-Kontrollstrukturen und Funktionen"
category: fundamentals
tags: [php, conditionals, loops, match, switch, operators, functions, closures, arrow-functions, named-arguments]
level: 3
source_sha256: df7df2ffb2a0319f9ef4820dd8e88682d8b7e3477f799b5389500c26926d256a
translation: machine
translated_at: '2026-10-24'
---
# PHP-Kontrollstrukturen und Funktionen {#php-control-structures-and-functions}

PHP-Kontrollstrukturen umfassen if/elseif/else, switch, match (PHP 8) sowie for/foreach/while. Der `match`-Ausdruck verwendet strikten Vergleich und gibt Werte zurück – er wird gegenüber switch bevorzugt. Funktionen unterstützen Typhinweise, Standardwerte, variadische Parameter, benannte Argumente (PHP 8), Closures (`use`) und Arrow-Funktionen (`fn`).

## Key Facts {#key-facts}

- `match` (PHP 8) = strikter Vergleich, gibt einen Wert zurück, kein Fallthrough (ersetzt switch)
- `foreach ($arr as $key => $value)` - primäre Array-Schleife
- Ternäroperator: `$x ?: 'default'` (falsy); Null-Coalescing: `$x ?? 'default'` (nur null)
- Spaceship `<=>` gibt -1, 0, 1 zurück – wird in `usort` verwendet
- Benannte Argumente (PHP 8): `htmlspecialchars(string: $s, double_encode: false)`
- Arrow-Funktionen (PHP 7.4): `fn($x) => $x * 2` – automatische Übernahme (auto-capture), genau ein Ausdruck

## Patterns {#patterns}

### Match Expression {#match-expression}

```php
$result = match($status) {
    'active', 'verified' => 'Access granted',
    'pending'            => 'Awaiting approval',
    'banned'             => 'Access denied',
    default              => 'Unknown',
};
```

### Functions and Closures {#functions-and-closures}

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

### Null Handling {#null-handling}

```php
$name = $_GET['name'] ?? 'Guest';    // null coalescing
$name ??= 'Guest';                    // null coalescing assignment
$len = $user?->profile?->name;        // nullsafe operator (PHP 8)
```

### String Functions and Dates {#string-functions-and-dates}

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

## Gotchas {#gotchas}

- `switch` verwendet lockeren Vergleich und fällt ohne `break` durch – `match` bevorzugen
- Arrow-Funktionen übernehmen Variablen per Wert, nicht per Referenz – Änderungen wirken sich nicht auf den äußeren Gültigkeitsbereich aus
- `foreach ($arr as &$value)` – `$value` nach der Schleife mit `unset` entfernen, um Fehler mit dem letzten Element zu vermeiden
- `date()` verwendet die Zeitzone des Servers; `date_default_timezone_set('UTC')` sorgt für Konsistenz

## See Also {#see-also}

- [[php-type-system]] - Typdeklarationen und strict_types
- [[php-arrays]] - Array-Iteration und funktionale Operationen
- [[php-oop-fundamentals]] - Methoden als Funktionen auf Objekten
