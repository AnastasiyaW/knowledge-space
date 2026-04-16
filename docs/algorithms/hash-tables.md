---
title: Hash Tables
category: concepts
tags: [data-structure, hashing, collision, lookup]
---

# Hash Tables

Data structure mapping keys to values via hash function. Average O(1) lookup, insert, delete. Foundation for sets, dictionaries, caches, and counting problems.

## Key Facts

- Hash function maps key to array index: `index = hash(key) % capacity`
- Average case: O(1) for get/set/delete
- Worst case: O(N) when all keys collide (rare with good hash function)
- Load factor = entries / capacity. Resize when load factor > 0.7 (typical)
- Python `dict` uses open addressing with random probing
- Python `dict` preserves insertion order (since 3.7)
- `collections.defaultdict`, `Counter`, `OrderedDict` are specialized hash tables

## Collision Resolution

### Chaining (Separate Chaining)

```php
index 0: -> [key1, val1] -> [key5, val5]
index 1: -> [key2, val2]
index 2: -> [key3, val3] -> [key7, val7] -> [key9, val9]
```

Each bucket is a linked list. Simple but poor cache locality.

### Open Addressing (Linear Probing)

```text
If slot h(k) taken, try h(k)+1, h(k)+2, ...
```

All entries stored in array. Better cache locality but clustering issues.

### Robin Hood Hashing

Variant of open addressing: steal from rich (short probe distance) give to poor (long probe distance). More uniform probe lengths.

## Patterns

### Two Sum (Classic Hash Usage)

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

### Group Anagrams

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

### Frequency Counting

```python
from collections import Counter

def top_k_frequent(nums, k):
    return [x for x, _ in Counter(nums).most_common(k)]
```

### Subarray Sum Equals K (Prefix Sum HashMap)

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

### LRU Cache (Hash + Doubly Linked List)

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

## Complexity

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(1) | O(N) |
| Lookup | O(1) | O(N) |
| Delete | O(1) | O(N) |
| Space | O(N) | O(N) |

## Hash Function Properties

- **Deterministic**: same input always produces same output
- **Uniform distribution**: spread keys evenly across buckets
- **Fast computation**: constant time per hash
- **Avalanche effect**: small input change -> large output change

## Python Specifics

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

## Gotchas

- **Issue:** Using mutable objects as dict keys -> **Fix:** Only use immutable, hashable types as keys. Convert lists to tuples.
- **Issue:** Relying on hash table order in languages that don't guarantee it -> **Fix:** Python 3.7+ dicts are insertion-ordered. In other languages, use ordered map/tree map if order matters.
- **Issue:** Hash collision attacks (adversarial input crafted to cause O(N) lookups) -> **Fix:** Python randomizes hash seed per process (since 3.3). For security-critical apps, use SipHash.

## See Also

- [[searching-algorithms]] - hash tables provide O(1) search
- [[sorting-algorithms]] - counting sort uses hash-like structure
- [[complexity-analysis]] - amortized O(1) analysis for hash tables
