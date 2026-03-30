---
title: Hash Tables
category: data-structures
tags: [hash-table, hash-map, dictionary, hash-set, collision-resolution]
---

# Hash Tables

## Key Facts

- **Hash table** maps keys to values via a hash function; Python `dict`/`set`, Java `HashMap`/`HashSet`
- Average case: Insert O(1), Lookup O(1), Delete O(1)
- Worst case (all collisions): Insert O(n), Lookup O(n), Delete O(n)
- **Hash function** converts key to integer index; must be deterministic and distribute keys uniformly
- **Collision resolution**: chaining (linked lists at each bucket) or open addressing (linear/quadratic probing)
- **Load factor** = n_elements / n_buckets; resize (rehash) when load factor exceeds threshold (typically 0.75)
- Python `dict` preserves insertion order (CPython 3.6+, language spec 3.7+)
- Related: [[arrays-and-strings]], [[binary-tree-traversal]]

## Patterns

### Two Sum (Classic Hash Table Pattern)

```python
# O(n) time, O(n) space
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
        key = tuple(sorted(s))  # or frequency tuple
        groups[key].append(s)
    return list(groups.values())
```

### Frequency Counter

```python
from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)
    return [x for x, _ in count.most_common(k)]
```

### Hash Set for Cycle Detection

```python
# Detect duplicate in O(n) time, O(n) space
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

```java
// Java HashMap pattern
import java.util.*;

public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{};
}
```

### Implementing a Simple Hash Table

```python
class HashTable:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))
        self.size += 1

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        raise KeyError(key)
```

## Gotchas

- **Unhashable types** - Python lists and dicts cannot be dictionary keys; use tuples instead
- **Hash collisions are inevitable** - even good hash functions have collisions; worst case is O(n) per operation
- **Mutable keys** - if an object's hash changes after insertion, it becomes unfindable. Never use mutable objects as keys
- **Order guarantees** - Python dict preserves insertion order; Java `HashMap` does not (use `LinkedHashMap` for order)
- **`defaultdict` vs `dict.get()`** - `defaultdict(int)` auto-creates missing keys; `dict.get(key, 0)` does not modify the dict
- **Set operations are O(1) average** but `in` on a list is O(n) - always prefer sets for membership testing

## See Also

- [[arrays-and-strings]] - frequency counting, anagram problems
- [[binary-tree-traversal]] - ordered alternative to hash tables
- [[graph-representations]] - adjacency list uses hash maps
