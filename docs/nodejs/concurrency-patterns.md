---
title: Concurrency Patterns
category: patterns
tags: [nodejs, actor-model, crdt, blockchain, webrtc, shared-worker, concurrency]
---

# Concurrency Patterns

Node.js concurrency extends beyond async/await to Actor model, CRDT for distributed state, SharedWorker for browser tab coordination, and custom protocols for real-time applications. These patterns address coordination between independent execution contexts.

## Actor Model (Single-threaded)

According to Alan Kay, all OOP was supposed to look like the Actor pattern: isolated state, message-based communication.

```js
class Actor {
  #queue = [];
  #processing = false;

  send(message) {
    this.#queue.push(message);
    if (!this.#processing) this.#process();
  }

  async #process() {
    this.#processing = true;
    while (this.#queue.length > 0) {
      const msg = this.#queue.shift();
      await this.handle(msg);
    }
    this.#processing = false;
  }
}
```

Single-threaded version uses async queue instead of `process.send()` / `MessagePort`. Same API works for single-thread, multi-thread, and multi-process by swapping the message transport.

**Reactor pattern**: event loop model for cooperative multitasking within a single thread - the foundation of Node.js.

## CRDT (Conflict-free Replicated Data Types)

### Synchronization Methods

- **State-based:** full state sent (larger payloads, simpler)
- **Operation-based:** only operations transmitted (smaller payloads, more complex)
- **Delta-based:** only changes transmitted (best for network efficiency)

### Available Data Structures

- G-Counter (grow-only), PN-Counter (positive-negative)
- G-Set (grow-only), 2P-Set (two-phase), OR-Set (observed-remove)
- Graphs, ordered lists, registers

### Schema-Driven CRDT

```js
const schema = {
  likes: { type: 'g-counter' },
  tags: { type: '2p-set' },
  inventory: { type: 'pn-counter' },
};
```

## SharedWorker WebSocket

Share one WebSocket across multiple browser tabs:

- 50 tabs open but only 1 WebSocket connection to server
- Service Worker acts as message broker between tabs
- All tabs synchronize state through the Service Worker
- Saves server resources and client memory

## Custom Binary Protocol (Metacom)

- Packet format with IDs: positive = client-to-server, negative = server-to-client events
- Stream IDs for file upload/download multiplexed over same connection
- Binary serialization outperforms JSON in size and speed
- Version 3: merged serializer functions, single buffer allocation for stream chunks

### Dynamic API Client (scaffold)

```js
const scaffold = (url, structure) => {
  const api = {};
  for (const [entity, methods] of Object.entries(structure)) {
    api[entity] = {};
    for (const method of methods) {
      api[entity][method] = (...args) =>
        fetch(`${url}/${entity}/${method}`, {
          method: 'POST', body: JSON.stringify(args),
        }).then(r => r.json());
    }
  }
  return api;
};
```

## Deployment Patterns

### Blue-Green Deployment
Two identical clusters. Deploy new version to one, switch traffic instantly if needed.

### Canary Release
Route subset of users to new version. Detect problems before full rollout.

### Feature Toggles
Enable/disable features dynamically without redeployment: command-line flags, remote control via admin panel, kill switch for error spikes.

## Gotchas

- Single-threaded Actor in JS still needs to handle race conditions in the message handler (multiple awaits can interleave)
- CRDT eventually converges but may show stale data temporarily - not suitable for strong consistency requirements
- SharedWorker is not available in all browsers - check compatibility

## See Also

- [[async-patterns]] - async/await, EventEmitter as concurrency primitives
- [[event-loop-and-architecture]] - single-threaded execution model
- [[data-access-patterns]] - transactions as serialized access pattern
- [[streams]] - stream-based data processing concurrency
