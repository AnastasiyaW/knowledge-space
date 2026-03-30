---
title: Worker Threads and Child Processes
category: internals
tags: [worker-threads, child-process, cluster, multicore, cpu-bound, parallelism, shared-memory]
---
# Worker Threads and Child Processes

Node.js is single-threaded for JavaScript execution but provides `worker_threads` for CPU-bound work and `child_process`/`cluster` for process-level parallelism. Choosing the right approach depends on whether you need shared memory, isolation level, or multi-core HTTP scaling.

## Key Facts

- **worker_threads**: threads within the same process; share memory via `SharedArrayBuffer` and `Atomics`
- **child_process**: separate OS processes; communicate via IPC (serialized messages), full isolation
- **cluster**: forks multiple copies of the main process to handle HTTP on multiple cores
- Worker threads have their own event loop but share the same V8 isolate address space
- Data transfer to workers: **structured clone** (copy), **transfer** (zero-copy, original becomes unusable), or **SharedArrayBuffer** (true shared memory)
- `worker_threads` are cheaper than `child_process` (no full process overhead) but share memory = shared bugs
- CPU-bound tasks in the main thread block the [[event-loop]]; offload to workers
- `worker.postMessage(data)` sends data; `worker.on('message', handler)` receives
- `Atomics.wait()` / `Atomics.notify()` for thread synchronization on SharedArrayBuffer
- `cluster.fork()` uses `child_process.fork()` under the hood; the primary distributes connections to workers
- Alternative: use `child_process.exec/spawn` for running external commands (ffmpeg, ImageMagick, etc.)
- `os.availableParallelism()` (Node 19+) returns number of CPU cores for optimal pool sizing

## Patterns

```javascript
// Worker thread: CPU-intensive task
// main.js
const { Worker, isMainThread } = require('worker_threads');

if (isMainThread) {
  function runInWorker(data) {
    return new Promise((resolve, reject) => {
      const worker = new Worker(__filename, { workerData: data });
      worker.on('message', resolve);
      worker.on('error', reject);
    });
  }
  const result = await runInWorker({ iterations: 1e8 });
} else {
  // Worker code
  const { workerData, parentPort } = require('worker_threads');
  let sum = 0;
  for (let i = 0; i < workerData.iterations; i++) sum += Math.random();
  parentPort.postMessage(sum);
}

// Worker pool pattern
const { availableParallelism } = require('os');
class WorkerPool {
  #workers = [];
  #queue = [];
  #available = [];

  constructor(script, size = availableParallelism()) {
    for (let i = 0; i < size; i++) {
      const worker = new Worker(script);
      this.#workers.push(worker);
      this.#available.push(worker);
    }
  }

  run(data) {
    return new Promise((resolve, reject) => {
      const worker = this.#available.pop();
      if (worker) {
        this.#dispatch(worker, data, resolve, reject);
      } else {
        this.#queue.push({ data, resolve, reject });
      }
    });
  }

  #dispatch(worker, data, resolve, reject) {
    const cleanup = () => {
      worker.removeAllListeners('message');
      worker.removeAllListeners('error');
      this.#available.push(worker);
      const next = this.#queue.shift();
      if (next) this.#dispatch(worker, next.data, next.resolve, next.reject);
    };
    worker.once('message', (result) => { cleanup(); resolve(result); });
    worker.once('error', (err) => { cleanup(); reject(err); });
    worker.postMessage(data);
  }

  terminate() {
    return Promise.all(this.#workers.map(w => w.terminate()));
  }
}

// SharedArrayBuffer for shared state
const { Worker } = require('worker_threads');
const sharedBuf = new SharedArrayBuffer(4);
const view = new Int32Array(sharedBuf);
const worker = new Worker('./counter-worker.js', {
  workerData: { buffer: sharedBuf }
});
// counter-worker.js
const { workerData } = require('worker_threads');
const view = new Int32Array(workerData.buffer);
Atomics.add(view, 0, 1); // thread-safe increment

// Child process: run external command
const { execFile } = require('child_process');
const { promisify } = require('util');
const execFileAsync = promisify(execFile);
const { stdout } = await execFileAsync('ffprobe', [
  '-v', 'error', '-show_entries', 'format=duration',
  '-of', 'csv=p=0', inputPath
]);

// Cluster for multi-core HTTP
const cluster = require('cluster');
const http = require('http');
if (cluster.isPrimary) {
  const numCPUs = availableParallelism();
  for (let i = 0; i < numCPUs; i++) cluster.fork();
  cluster.on('exit', (worker) => {
    console.log(`Worker ${worker.process.pid} died, restarting`);
    cluster.fork();
  });
} else {
  http.createServer((req, res) => {
    res.end('Hello from worker ' + process.pid);
  }).listen(3000);
}
```

## Gotchas

- **Symptom**: worker thread throws "not serializable" error - **Cause**: trying to send functions, WeakMaps, or other non-transferable types via `postMessage` - **Fix**: only send structured-cloneable data (plain objects, arrays, ArrayBuffer, Date, RegExp, Map, Set)
- **Symptom**: shared memory race condition - **Cause**: multiple threads read/write SharedArrayBuffer without synchronization - **Fix**: use `Atomics` operations for all shared memory access
- **Symptom**: cluster workers crash on port conflict - **Cause**: each worker tries to listen on the same port independently - **Fix**: let the primary distribute connections (default `cluster` behavior); don't call `.listen()` in primary
- **Symptom**: child process hangs - **Cause**: stdout/stderr buffers full; process waits for pipe to drain - **Fix**: consume stdout/stderr streams, or use `{ stdio: 'ignore' }` if output not needed

## See Also

- [[event-loop]] - why CPU work blocks the main thread
- [[async-patterns]] - async for I/O, workers for CPU
- [Node.js worker_threads](https://nodejs.org/api/worker_threads.html)
- [Node.js child_process](https://nodejs.org/api/child_process.html)
- [Node.js cluster](https://nodejs.org/api/cluster.html)
