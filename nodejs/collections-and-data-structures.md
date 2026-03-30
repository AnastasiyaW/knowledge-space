---
title: Collections and Data Structures
category: language
tags: [map, set, weakmap, weakset, array, buffer, typed-array, data-structures]
---
# Collections and Data Structures

JavaScript built-in collections beyond plain objects and arrays. Map, Set, WeakMap, WeakSet, Buffer, and TypedArray provide specialized storage with different performance characteristics and memory semantics.

## Key Facts

- **Map**: key-value pairs with any key type (objects, functions, primitives); ordered by insertion; O(1) lookup
- **Set**: unique values collection; O(1) membership check (`has`); ordered by insertion
- **WeakMap**: keys must be objects/symbols; entries are GC'd when key has no other references; not iterable
- **WeakSet**: like WeakMap but for presence checks only; not iterable; entries auto-GC'd
- **Buffer**: Node.js-specific, fixed-size byte array for binary data; backed by `ArrayBuffer`
- **TypedArray**: `Uint8Array`, `Int32Array`, `Float64Array`, etc. - fixed-type arrays for binary/numeric data
- Map vs Object: Map has better performance for frequent additions/deletions; any key type; has `.size`
- Object literal is faster for static string-keyed config; Map is better for dynamic lookups
- `Array.from()`, spread `[...iterable]`, destructuring work with any iterable (Map, Set, generators)
- `structuredClone(obj)` (Node 17+) deep-clones objects, Maps, Sets, Dates, ArrayBuffers, etc.
- `Buffer.alloc(size)` zero-fills (safe); `Buffer.allocUnsafe(size)` does not (fast but may contain old data)
- `SharedArrayBuffer` enables shared memory between [[worker-threads]]; requires `Atomics` for safe access

## Patterns

```javascript
// Map for flexible key-value storage
const cache = new Map();
cache.set(userObj, { lastAccess: Date.now() }); // object as key
cache.set('/api/users', responseData);           // string as key

// Map from entries, and back
const map = new Map([['a', 1], ['b', 2]]);
const obj = Object.fromEntries(map);
const arr = [...map]; // [['a', 1], ['b', 2]]

// Set for deduplication
const unique = [...new Set([1, 2, 2, 3, 3, 3])]; // [1, 2, 3]

// Set operations
function union(a, b) { return new Set([...a, ...b]); }
function intersection(a, b) { return new Set([...a].filter(x => b.has(x))); }
function difference(a, b) { return new Set([...a].filter(x => !b.has(x))); }

// WeakMap for private data / metadata
const privateData = new WeakMap();
class SecureUser {
  constructor(name, secret) {
    privateData.set(this, { secret });
    this.name = name;
  }
  getSecret() {
    return privateData.get(this).secret;
  }
}
// When SecureUser instance is GC'd, privateData entry is also freed

// WeakSet for tracking processed objects
const processed = new WeakSet();
function processOnce(obj) {
  if (processed.has(obj)) return; // skip duplicates
  processed.add(obj);
  // ... process obj
}

// Buffer operations
const buf = Buffer.from('Hello', 'utf8');
console.log(buf.length);           // 5 bytes
console.log(buf.toString('hex'));   // 48656c6c6f
console.log(buf.toString('base64')); // SGVsbG8=

// Buffer for binary protocols
const header = Buffer.alloc(8);
header.writeUInt32BE(0x01020304, 0); // 4-byte magic
header.writeUInt32BE(payload.length, 4); // 4-byte length

// TypedArray for numeric computation
const float64 = new Float64Array(1000);
for (let i = 0; i < float64.length; i++) {
  float64[i] = Math.sin(i * 0.01);
}

// structuredClone for deep copy
const original = { date: new Date(), map: new Map([['a', 1]]), nested: { x: 1 } };
const clone = structuredClone(original);
clone.nested.x = 99; // does not affect original

// LRU Cache implementation
class LRUCache {
  #max;
  #cache;
  constructor(max = 100) {
    this.#max = max;
    this.#cache = new Map();
  }
  get(key) {
    if (!this.#cache.has(key)) return undefined;
    const value = this.#cache.get(key);
    this.#cache.delete(key);     // remove
    this.#cache.set(key, value); // re-insert (moves to end)
    return value;
  }
  set(key, value) {
    this.#cache.delete(key);
    this.#cache.set(key, value);
    if (this.#cache.size > this.#max) {
      const oldest = this.#cache.keys().next().value;
      this.#cache.delete(oldest);
    }
  }
}
```

## Gotchas

- **Symptom**: Map lookup fails for object keys - **Cause**: looking up by a different object instance (reference equality) - **Fix**: use the same reference; or use string/number keys; or use serialized key
- **Symptom**: WeakMap entries not being GC'd - **Cause**: another reference to the key still exists somewhere - **Fix**: ensure all references to the key are removed; check closures holding references
- **Symptom**: `Buffer.allocUnsafe()` contains sensitive data from previous allocations - **Cause**: uninitialized memory reuse - **Fix**: use `Buffer.alloc()` for sensitive contexts; or `.fill(0)` after `allocUnsafe()`
- **Symptom**: `JSON.stringify()` drops Map/Set - **Cause**: Map and Set are not JSON-serializable by default - **Fix**: convert to array first: `JSON.stringify([...map])`, or use a replacer function

## See Also

- [[v8-and-memory]] - how V8 manages collection memory; WeakRef and FinalizationRegistry
- [[worker-threads]] - SharedArrayBuffer for inter-thread collections
- [[closures-and-scope]] - WeakMap for private class data
- [MDN Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
- [Node.js Buffer](https://nodejs.org/api/buffer.html)
