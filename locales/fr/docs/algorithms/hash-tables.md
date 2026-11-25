---
title: "Tables de hachage"
category: concepts
tags: [data-structure, hashing, collision, lookup]
level: 3
source_sha256: 0ff214eb10bd93a1aaec216c97b005d567789583eb18ac0dd48ec8cf7e97d800
translation: machine
translated_at: '2026-10-24'
---
# Tables de hachage {#hash-tables}

Structure de données associant des clés à des valeurs via une fonction de hachage. Recherche, insertion et suppression en O(1) en moyenne. Fondation des ensembles, dictionnaires, caches et problèmes de comptage.

## Points clés {#key-facts}

- La fonction de hachage associe une clé à un indice de tableau : `index = hash(key) % capacity`
- Cas moyen : O(1) pour get/set/delete
- Pire cas : O(N) lorsque toutes les clés entrent en collision (rare avec une bonne fonction de hachage)
- Facteur de charge = entrées / capacité. Redimensionnement lorsque le facteur de charge dépasse 0,7 (valeur typique)
- Le `dict` Python utilise un adressage ouvert avec sondage aléatoire
- Le `dict` Python préserve l'ordre d'insertion (depuis la 3.7)
- `collections.defaultdict`, `Counter` et `OrderedDict` sont des tables de hachage spécialisées

## Résolution des collisions {#collision-resolution}

### Chaînage (chaînage séparé) {#chaining-separate-chaining}

```php
index 0: -> [key1, val1] -> [key5, val5]
index 1: -> [key2, val2]
index 2: -> [key3, val3] -> [key7, val7] -> [key9, val9]
```

Chaque case est une liste chaînée. Simple, mais à faible localité de cache.

### Adressage ouvert (sondage linéaire) {#open-addressing-linear-probing}

```text
If slot h(k) taken, try h(k)+1, h(k)+2, ...
```

Toutes les entrées sont stockées dans le tableau. Meilleure localité de cache, mais problèmes de regroupement (clustering).

### Robin Hood Hashing {#robin-hood-hashing}

Variante de l'adressage ouvert : « prendre aux riches » (faible distance de sondage) pour « donner aux pauvres » (longue distance de sondage). Les longueurs de sondage sont plus uniformes.

## Schémas d'utilisation {#patterns}

### Two Sum (usage classique de la table de hachage) {#two-sum-classic-hash-usage}

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

### Comptage de fréquences {#frequency-counting}

```python
from collections import Counter

def top_k_frequent(nums, k):
    return [x for x, _ in Counter(nums).most_common(k)]
```

### Subarray Sum Equals K (HashMap de sommes préfixes) {#subarray-sum-equals-k-prefix-sum-hashmap}

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

### LRU Cache (table de hachage + liste doublement chaînée) {#lru-cache-hash-doubly-linked-list}

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

## Complexité {#complexity}

| Opération | Moyenne | Pire cas |
|-----------|---------|-------|
| Insertion | O(1) | O(N) |
| Recherche | O(1) | O(N) |
| Suppression | O(1) | O(N) |
| Espace | O(N) | O(N) |

## Propriétés de la fonction de hachage {#hash-function-properties}

- **Déterministe** : une même entrée produit toujours la même sortie
- **Distribution uniforme** : répartir les clés équitablement entre les cases
- **Calcul rapide** : temps constant par hachage
- **Effet avalanche** : une petite modification de l'entrée entraîne une grande modification de la sortie

## Spécificités Python {#python-specifics}

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

## Pièges {#gotchas}

- **Problème :** utiliser des objets mutables comme clés de dictionnaire -> **Solution :** n'utiliser comme clés que des types immuables et hachables. Convertir les listes en tuples.
- **Problème :** se fier à l'ordre d'une table de hachage dans les langages qui ne le garantissent pas -> **Solution :** depuis Python 3.7, les dictionnaires conservent l'ordre d'insertion. Dans les autres langages, utiliser une map ordonnée ou une tree map si l'ordre importe.
- **Problème :** attaques par collisions de hachage (entrées conçues pour provoquer des recherches en O(N)) -> **Solution :** Python randomise la graine de hachage à chaque processus (depuis la 3.3). Pour les applications critiques en sécurité, utiliser SipHash.

## Voir aussi {#see-also}

- [[searching-algorithms]] - les tables de hachage offrent une recherche en O(1)
- [[sorting-algorithms]] - le tri par comptage utilise une structure similaire à une table de hachage
- [[complexity-analysis]] - analyse en O(1) amorti pour les tables de hachage
