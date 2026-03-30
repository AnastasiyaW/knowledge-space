---
title: Middleware and HTTP
category: concepts
tags: [middleware, http, express, koa, router, request, response, rest-api, cors]
---
# Middleware and HTTP

The middleware pattern is the core architectural concept in Node.js HTTP frameworks. A middleware is a function that receives a request, optionally modifies it, and either responds or passes control to the next middleware. Express, Koa, Fastify, and Hapi all use variations of this pattern.

## Key Facts

- Express middleware signature: `(req, res, next) => {}` - call `next()` to pass to next middleware, or respond
- Error middleware: `(err, req, res, next) => {}` - four arguments; Express routes errors here when `next(err)` is called
- Koa middleware uses async functions and `ctx` object: `async (ctx, next) => { await next(); }`
- Koa's "onion model": middleware wraps around the next; code before `await next()` runs on the way in, after on the way out
- `http.createServer()` is the foundation; frameworks are abstractions over it
- `req` (IncomingMessage) is a [[streams|Readable stream]]; `res` (ServerResponse) is a Writable stream
- Middleware ordering matters: auth before route handlers, error handler last
- Middleware types: application-level, router-level, error-handling, built-in, third-party
- Common middleware: body parsing, CORS, compression, rate limiting, logging, authentication
- Fastify uses a plugin system instead of traditional middleware; plugins are encapsulated and can share decorators
- `http.Agent` manages connection pooling; `keepAlive: true` reuses TCP connections

## Patterns

```javascript
// Raw Node.js HTTP server
const http = require('http');
const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok' }));
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});
server.listen(3000);

// Express middleware chain
const express = require('express');
const app = express();

// Built-in body parsing
app.use(express.json({ limit: '10mb' }));

// Custom logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    console.log(`${req.method} ${req.url} ${res.statusCode} ${Date.now() - start}ms`);
  });
  next();
});

// Auth middleware (reusable)
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try {
    req.user = jwt.verify(token, SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
}

// Router
const router = express.Router();
router.get('/users', requireAuth, async (req, res, next) => {
  try {
    const users = await userService.list();
    res.json(users);
  } catch (err) { next(err); }
});
app.use('/api', router);

// Error handler (must be last, must have 4 params)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({
    error: err.code || 'INTERNAL',
    message: process.env.NODE_ENV === 'production'
      ? 'Something went wrong'
      : err.message,
  });
});

// Koa onion model
const Koa = require('koa');
const koa = new Koa();

koa.use(async (ctx, next) => {
  const start = Date.now();
  await next(); // wait for downstream
  const ms = Date.now() - start;
  ctx.set('X-Response-Time', `${ms}ms`);
});

koa.use(async (ctx) => {
  ctx.body = { hello: 'world' };
});

// Graceful shutdown
const server2 = app.listen(3000);
process.on('SIGTERM', () => {
  server2.close(() => {
    db.end();
    process.exit(0);
  });
  // Force exit after timeout
  setTimeout(() => process.exit(1), 10000);
});
```

## Gotchas

- **Symptom**: request hangs, no response sent - **Cause**: middleware neither calls `next()` nor sends a response - **Fix**: ensure every middleware path either responds or calls `next()`
- **Symptom**: error handler not triggered - **Cause**: error handler has 3 params instead of 4, or is registered before routes - **Fix**: error middleware MUST have exactly 4 params `(err, req, res, next)` and be registered last
- **Symptom**: `req.body` is undefined - **Cause**: body parsing middleware not added, or added after the route - **Fix**: add `express.json()` before route definitions
- **Symptom**: CORS errors in browser - **Cause**: no CORS headers set for cross-origin requests - **Fix**: add `cors()` middleware before routes; configure allowed origins

## See Also

- [[design-patterns-gof]] - middleware is Chain of Responsibility pattern
- [[nodejs/error-handling]] - async error propagation in middleware
- [[streams]] - req/res are Node.js streams
- [Express docs](https://expressjs.com/en/guide/using-middleware.html)
- [Node.js HTTP](https://nodejs.org/api/http.html)
