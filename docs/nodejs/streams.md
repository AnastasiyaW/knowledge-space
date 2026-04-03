---
title: Streams
category: concepts
tags: [nodejs, streams, readable, writable, transform, duplex, backpressure]
---

# Streams

Node.js streams provide an interface for working with data that arrives or is consumed incrementally. Instead of loading entire datasets into memory, streams process data in chunks, enabling handling of files and network data larger than available RAM.

## Key Facts

- **Readable** - data source (file read, HTTP request body)
- **Writable** - data sink (file write, HTTP response)
- **Transform** - reads and writes, modifying data in between (compression, encryption)
- **Duplex** - both readable and writable independently (WebSocket, TCP socket)
- Streams implement backpressure automatically: when a writable is slower than a readable, the readable pauses
- When a socket is paused, the OS kernel buffers incoming data - the main thread event loop still processes other events

## Patterns

### Stream Backpressure Flow

1. Readable pushes data faster than writable can consume
2. Internal buffer fills up
3. Readable pauses automatically (backpressure signal)
4. When writable drains buffer, readable resumes

### Optimized Chunk Streaming

```js
// Optimized: single buffer allocation for streaming over WebSocket
const sendChunk = (streamId, data) => {
  const packet = Buffer.allocUnsafe(8 + data.length);
  packet.writeInt32BE(streamId, 0);
  packet.writeInt32BE(data.length, 4);
  data.copy(packet, 8);
  return packet;
};

// Before optimization: two typed arrays, copied into one
// const header = new Uint8Array(8);
// const body = new Uint8Array(data);
// const packet = Buffer.concat([header, body]); // 2 allocations
```

### Cursor Pattern (Stream-like In-Memory)

```js
class Cursor {
  constructor(data) { this.data = data; }

  select(fields) {
    return new Cursor(this.data.map(row =>
      fields.reduce((obj, f) => ({ ...obj, [f]: row[f] }), {})
    ));
  }

  order(field) {
    return new Cursor([...this.data].sort((a, b) =>
      a[field] > b[field] ? 1 : -1
    ));
  }

  union(other) {
    return new Cursor([...this.data, ...other.data]);
  }

  intersect(other) {
    const keys = new Set(other.data.map(r => JSON.stringify(r)));
    return new Cursor(this.data.filter(r => keys.has(JSON.stringify(r))));
  }

  fetch() { return this.data; }
}

// Chaining mimics SQL:
// cursor.select(['name', 'age']).order('name').fetch()
```

Advanced: implement `Symbol.iterator` for `for...of`, `Symbol.asyncIterator` for async iteration, stream interface for `.pipe()`.

## Gotchas

- `Buffer.allocUnsafe()` is faster but contains uninitialized memory - always write to all bytes before sending
- Understanding backpressure requires knowing both Node.js internals and OS networking (kernel buffers)
- Streaming file chunks over WebSocket needs IDs for multiplexing multiple streams over the same connection

## See Also

- [[async-patterns]] - async iterators and generators as stream alternatives
- [[performance-optimization]] - buffer optimization techniques
- [[event-loop-and-architecture]] - how libuv handles I/O in the thread pool
