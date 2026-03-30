---
title: Streams
category: concepts
tags: [streams, readable, writable, transform, duplex, backpressure, pipe, pipeline]
---
# Streams

Streams are Node.js's abstraction for processing data piece-by-piece without loading entire payloads into memory. They implement the `EventEmitter` interface and are the backbone of file I/O, HTTP, compression, and crypto.

## Key Facts

- Four stream types: **Readable**, **Writable**, **Duplex** (both), **Transform** (Duplex that modifies data)
- Streams operate in two modes: **flowing** (data emitted automatically) and **paused** (must call `.read()`)
- `pipe()` connects Readable to Writable and handles [[producer-patterns]] automatically
- `pipeline()` from `stream/promises` is the modern replacement: handles errors and cleanup
- **Backpressure**: when the consumer is slower than the producer, `.write()` returns `false`; producer must wait for `drain` event
- `Readable.from(iterable)` creates a Readable from any sync/async iterable
- Streams are async iterables: `for await (const chunk of readable) {}`
- `objectMode: true` allows streaming JS objects instead of Buffers/strings
- `highWaterMark` controls internal buffer size (default 16KB for byte streams, 16 objects for object mode)
- `stream.compose()` (Node 16+) chains transforms declaratively
- HTTP request (`req`) is a Readable stream; response (`res`) is a Writable stream

## Patterns

```javascript
const { pipeline } = require('stream/promises');
const { createReadStream, createWriteStream } = require('fs');
const { createGzip, createGunzip } = require('zlib');
const { Transform } = require('stream');

// File compression with pipeline (handles errors + cleanup)
await pipeline(
  createReadStream('input.log'),
  createGzip(),
  createWriteStream('input.log.gz')
);

// Custom Transform stream
class UpperCase extends Transform {
  _transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
}

// Transform with pipeline
await pipeline(
  createReadStream('input.txt'),
  new UpperCase(),
  createWriteStream('output.txt')
);

// Readable from async generator
const { Readable } = require('stream');
async function* generateData() {
  for (let i = 0; i < 1000; i++) {
    yield JSON.stringify({ id: i }) + '\n';
  }
}
const readable = Readable.from(generateData());

// Async iteration over stream
const rl = require('readline').createInterface({
  input: createReadStream('data.csv'),
  crlfDelay: Infinity
});
for await (const line of rl) {
  const [name, value] = line.split(',');
  // process line by line, constant memory
}

// Object mode stream
const objectTransform = new Transform({
  objectMode: true,
  transform(record, enc, cb) {
    record.processed = true;
    cb(null, record);
  }
});

// Handling backpressure manually
function writeMany(writable, data) {
  return new Promise((resolve, reject) => {
    let i = 0;
    write();
    function write() {
      let ok = true;
      while (i < data.length && ok) {
        ok = writable.write(data[i]);
        i++;
      }
      if (i < data.length) {
        writable.once('drain', write);
      } else {
        resolve();
      }
    }
    writable.on('error', reject);
  });
}

// HTTP streaming response
const http = require('http');
http.createServer(async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  const fileStream = createReadStream('large-data.json');
  await pipeline(fileStream, res);
}).listen(3000);
```

## Gotchas

- **Symptom**: piped stream silently swallows errors - **Cause**: `.pipe()` does not forward errors - **Fix**: use `pipeline()` from `stream/promises` which propagates errors and destroys streams on failure
- **Symptom**: memory grows unbounded when writing fast - **Cause**: ignoring backpressure (not checking `.write()` return value) - **Fix**: check the boolean return of `.write()`; wait for `drain` event before continuing
- **Symptom**: stream hangs, never finishes - **Cause**: Transform `_transform` callback never called, or `_flush` not implemented - **Fix**: always call `callback()` in Transform; implement `_flush(cb)` if buffering data
- **Symptom**: "Cannot pipe, not readable" - **Cause**: trying to pipe a Writable stream - **Fix**: check stream type; Writable can only be a pipe destination

## See Also

- [[event-loop]] - streams are driven by the event loop's poll phase
- [[producer-patterns]] - flow control between fast producers and slow consumers
- [[nodejs/error-handling]] - stream error patterns
- [Node.js Streams API](https://nodejs.org/api/stream.html)
- [Node.js stream/promises](https://nodejs.org/api/stream.html#streampipelinestreams-options)
