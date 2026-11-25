---
title: "Hash-Tabellen"
category: concepts
tags: [data-structure, hashing, collision, lookup]
level: 3
source_sha256: 0ff214eb10bd93a1aaec216c97b005d567789583eb18ac0dd48ec8cf7e97d800
translation: machine
translated_at: '2026-10-24'
---
# Hash-Tabellen {#hash-tables}

Datenstruktur, die Schlüssel über eine Hash-Funktion auf Werte abbildet. Durchschnittlich O(1) für Suche, Einfügen und Löschen. Grundlage für Mengen, Wörterbücher, Caches und Zähl-Probleme.

## Wichtige Fakten {#key-facts}

- Die Hash-Funktion bildet einen Schlüssel auf einen Array-Index ab: `index = hash(key) % capacity`
- Durchschnittsfall: O(1) für get/set/delete
- Schlechtester Fall: O(N), wenn alle Schlüssel kollidieren (selten bei einer guten Hash-Funktion)
- Auslastungsfaktor = Einträge / Kapazität. Neu dimensionieren, wenn der Auslastungsfaktor > 0,7 (typisch)
- Pythons `dict` verwendet Open Addressing mit zufälligem Probing
- Pythons `dict` erhält die Einfügereihenfolge (seit 3.7)
- `collections.defaultdict`, `Counter` und `OrderedDict` sind spezialisierte Hash-Tabellen

## Kollisionsauflösung {#collision-resolution}

### Chaining (Separate Chaining) {#chaining-separate-chaining}

```php
index 0: -> [key1, val1] -> [key5, val5]
index 1: -> [key2, val2]
index 2: -> [key3, val3] -> [key7, val7] -> [key9, val9]
```

Jeder Bucket ist eine verkettete Liste. Einfach, aber mit schlechter Cache-Lokalität.

### Open Addressing (Linear Probing) {#open-addressing-linear-probing}

```text
If slot h(k) taken, try h(k)+1, h(k)+2, ...
```

Alle Einträge werden im Array gespeichert. Bessere Cache-Lokalität, aber Probleme durch Clustering.

### Robin-Hood-Hashing {#robin-hood-hashing}

Variante des Open Addressing: Von den Reichen (kurze Probe-Distanz) nehmen, den Armen (lange Probe-Distanz) geben. Gleichmäßigere Probe-Längen.

## Muster {#patterns}

### Two Sum (klassische Hash-Verwendung) {#two-sum-classic-hash-usage}

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### Group Anagrams {#group-anagrams}

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

### Häufigkeitszählung {#frequency-counting}

```python
from collections import Counter

def top_k_frequent(nums, k):
    return [x for x, _ in Counter(nums).most_common(k)]
```

### Subarray Sum Equals K (Präfixsumme mit HashMap) {#subarray-sum-equals-k-prefix-sum-hashmap}

```python
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}
    for num in nums:
        prefix += num
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count
```

### LRU-Cache (Hash + doppelt verkettete Liste) {#lru-cache-hash-doubly-linked-list}

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

## Komplexität {#complexity}

| Operation | Durchschnitt | Schlechtester Fall |
|-----------|--------------|--------------------|
| Einfügen | O(1) | O(N) |
| Suche | O(1) | O(N) |
| Löschen | O(1) | O(N) |
| Speicher | O(N) | O(N) |

## Eigenschaften von Hash-Funktionen {#hash-function-properties}

- **Deterministisch**: Dieselbe Eingabe erzeugt immer dieselbe Ausgabe
- **Gleichmäßige Verteilung**: Schlüssel gleichmäßig auf die Buckets verteilen
- **Schnelle Berechnung**: konstante Zeit pro Hash
- **Lawineneffekt**: kleine Eingabeänderung -> große Ausgabeänderung

## Python-Besonderheiten {#python-specifics}

```python
# Only immutable types are hashable by default
hash(42)          # int - OK
hash("hello")     # str - OK
hash((1, 2, 3))   # tuple of hashable - OK
# hash([1, 2])    # list - TypeError
# hash({1: 2})    # dict - TypeError

# Custom hashable objects
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

## Fallstricke {#gotchas}

- **Problem:** Veränderliche Objekte als dict-Schlüssel verwenden -> **Lösung:** Als Schlüssel nur unveränderliche, hashbare Typen verwenden. Listen in Tupel umwandeln.
- **Problem:** Sich auf die Reihenfolge von Hash-Tabellen verlassen in Sprachen, die diese nicht garantieren -> **Lösung:** Python-3.7+-dicts sind nach Einfügereihenfolge sortiert. In anderen Sprachen eine geordnete Map bzw. Baum-Map verwenden, wenn die Reihenfolge wichtig ist.
- **Problem:** Hash-Kollisionsangriffe (gezielt konstruierte Eingaben, die O(N)-Suchen auslösen) -> **Lösung:** Python randomisiert den Hash-Seed pro Prozess (seit 3.3). Für sicherheitskritische Anwendungen SipHash verwenden.

## Siehe auch {#see-also}

- [[searching-algorithms]] - Hash-Tabellen ermöglichen O(1)-Suche
- [[sorting-algorithms]] - Counting Sort verwendet eine hashähnliche Struktur
- [[complexity-analysis]] - Analyse des amortisierten O(1) für Hash-Tabellen
