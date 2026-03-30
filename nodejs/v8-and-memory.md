---
title: V8 Engine and Memory Management
category: internals
tags: [v8, garbage-collection, heap, memory-leak, hidden-class, jit, optimization, profiling]
---
# V8 Engine and Memory Management

V8 is the JavaScript engine powering Node.js. Understanding its JIT compilation, hidden classes, and garbage collection is essential for writing performant code and diagnosing memory leaks.

## Key Facts

- V8 compiles JavaScript to machine code using JIT (Just-In-Time) compilation
- Compilation pipeline: Parser -> AST -> Ignition (bytecode interpreter) -> TurboFan (optimizing compiler)
- **Hidden classes** (Maps): V8 assigns internal type information to objects; adding properties in different order creates different hidden classes (deoptimization)
- **Inline caching**: V8 caches property access patterns; polymorphic/megamorphic access is slower
- Garbage collection: **generational** - young generation (Scavenger, frequent, fast) and old generation (Mark-Sweep-Compact, infrequent, slower)
- Default heap limit: ~1.5GB on 64-bit; increase with `--max-old-space-size=4096`
- **Memory leak causes**: forgotten closures, growing arrays/maps, event listeners not removed, global variables, circular references with weak refs
- `WeakMap`/`WeakSet`/`WeakRef` allow GC to collect entries when keys are no longer referenced elsewhere
- `--expose-gc` flag enables `global.gc()` for manual GC (debugging only)
- `process.memoryUsage()` returns `{ rss, heapTotal, heapUsed, external, arrayBuffers }`
- Chrome DevTools (via `--inspect`) for heap snapshots, allocation timeline, and CPU profiling
- `Buffer` and `TypedArray` memory is counted as `external` (outside V8 heap, managed by V8's ArrayBuffer allocator)

## Patterns

```javascript
// Monitor memory usage
function logMemory(label) {
  const { heapUsed, heapTotal, rss } = process.memoryUsage();
  console.log(`${label}: heap=${(heapUsed/1e6).toFixed(1)}MB / ${(heapTotal/1e6).toFixed(1)}MB, rss=${(rss/1e6).toFixed(1)}MB`);
}

// Hidden class optimization: always initialize properties in same order
// Good: consistent shape
class Point {
  constructor(x, y) {
    this.x = x; // always x first
    this.y = y; // always y second
  }
}

// Bad: different property order = different hidden class
function createBad(a, b, flag) {
  const obj = {};
  if (flag) { obj.x = a; obj.y = b; }
  else { obj.y = b; obj.x = a; } // different order!
  return obj;
}

// WeakMap for metadata without preventing GC
const metadata = new WeakMap();
function process(obj) {
  metadata.set(obj, { processedAt: Date.now() });
  // When obj is GC'd, the metadata entry is also cleaned up
}

// WeakRef for optional caching
class WeakCache {
  #cache = new Map();

  get(key) {
    const ref = this.#cache.get(key);
    if (!ref) return undefined;
    const value = ref.deref();
    if (!value) {
      this.#cache.delete(key); // ref expired
      return undefined;
    }
    return value;
  }

  set(key, value) {
    this.#cache.set(key, new WeakRef(value));
  }
}

// Detecting memory leaks with heap snapshots
// Start: node --inspect app.js
// 1. Open chrome://inspect
// 2. Take heap snapshot before operation
// 3. Perform suspected leaking operation N times
// 4. Take another snapshot
// 5. Compare: objects with growing count = leak

// Memory-efficient large data processing
const { pipeline } = require('stream/promises');
const { createReadStream } = require('fs');
const { Transform } = require('stream');

// Stream processing: constant memory regardless of file size
await pipeline(
  createReadStream('huge.json'),
  new Transform({
    transform(chunk, enc, cb) {
      // Process chunk, don't accumulate
      cb(null, processChunk(chunk));
    }
  }),
  createWriteStream('output.json')
);

// FinalizationRegistry for cleanup
const registry = new FinalizationRegistry((heldValue) => {
  console.log(`Object with key ${heldValue} was GC'd`);
  // cleanup: close file handles, remove temp files, etc.
});
function trackObject(key, obj) {
  registry.register(obj, key);
}

// Avoid deoptimization: monomorphic functions
function add(a, b) { return a + b; }
add(1, 2);      // number + number: V8 optimizes
add('a', 'b');   // string + string: different types = deoptimization
// Fix: separate functions for different types
```

## Gotchas

- **Symptom**: heap keeps growing, never shrinks - **Cause**: accumulating data in closures, event listeners, or global arrays - **Fix**: use heap snapshots to identify retained objects; remove listeners; use WeakMap/WeakRef
- **Symptom**: "JavaScript heap out of memory" - **Cause**: exceeded default heap limit processing large data - **Fix**: increase `--max-old-space-size`; or better, use [[streams]] for large data
- **Symptom**: function performance degrades over time - **Cause**: V8 deoptimizes due to changing object shapes or polymorphic calls - **Fix**: initialize all properties in constructors; keep function argument types consistent
- **Symptom**: `external` memory high but `heapUsed` low - **Cause**: large Buffers or native addons allocating outside V8 heap - **Fix**: track Buffer allocations; ensure native addons release memory

## See Also

- [[event-loop]] - GC pauses can block the event loop
- [[streams]] - streaming prevents heap exhaustion on large data
- [[worker-threads]] - separate V8 isolate per worker
- [V8 blog](https://v8.dev/blog)
- [Node.js debugging guide](https://nodejs.org/en/learn/getting-started/debugging)
- [Node.js --inspect](https://nodejs.org/en/learn/getting-started/debugging#inspector-clients)
