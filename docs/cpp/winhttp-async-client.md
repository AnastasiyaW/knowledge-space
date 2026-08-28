---
title: "WinHTTP Asynchronous Client"
description: "Completion vs progress notifications, bounded waits, and cancellation semantics for WinHTTP in WINHTTP_FLAG_ASYNC mode. Why an async client hangs forever and how to prove which of the three defects you have."
---

# WinHTTP Asynchronous Client

An asynchronous WinHTTP client that "hangs" almost always has one of three independent
defects: it never subscribed to the completion it waits for, it waits without a bound, or
it cancels its own healthy request. Each has a distinct signature and each is provable in
isolation. Verified against `winhttp.h` from Windows SDK 10.0.26100.0 and current
first-party documentation.

## Notification model: progress is not completion

`WinHttpSetStatusCallback` takes a `dwNotificationFlags` bitmask. The names are the trap:
several flags read as though they cover completion, but expand to *progress* notifications
only. From the SDK header:

```c
/* progress only - fires while the header is going out */
#define WINHTTP_CALLBACK_FLAG_SEND_REQUEST \
    (WINHTTP_CALLBACK_STATUS_SENDING_REQUEST | WINHTTP_CALLBACK_STATUS_REQUEST_SENT)

#define WINHTTP_CALLBACK_FLAG_RECEIVE_RESPONSE \
    (WINHTTP_CALLBACK_STATUS_RECEIVING_RESPONSE | WINHTTP_CALLBACK_STATUS_RESPONSE_RECEIVED)

/* the actual completions */
#define WINHTTP_CALLBACK_FLAG_SENDREQUEST_COMPLETE  WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE
#define WINHTTP_CALLBACK_FLAG_READ_COMPLETE         WINHTTP_CALLBACK_STATUS_READ_COMPLETE
#define WINHTTP_CALLBACK_FLAG_WRITE_COMPLETE        WINHTTP_CALLBACK_STATUS_WRITE_COMPLETE
#define WINHTTP_CALLBACK_FLAG_REQUEST_ERROR         WINHTTP_CALLBACK_STATUS_REQUEST_ERROR

#define WINHTTP_CALLBACK_FLAG_HANDLES \
    (WINHTTP_CALLBACK_STATUS_HANDLE_CREATED | WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING)
```

There are exactly six completion notifications, and each one maps to the call it finishes:

| Completion notification | Finishes |
|---|---|
| `WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE` | `WinHttpSendRequest` |
| `WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE` | `WinHttpReceiveResponse` |
| `WINHTTP_CALLBACK_STATUS_DATA_AVAILABLE` | `WinHttpQueryDataAvailable` |
| `WINHTTP_CALLBACK_STATUS_READ_COMPLETE` | `WinHttpReadData` |
| `WINHTTP_CALLBACK_STATUS_WRITE_COMPLETE` | `WinHttpWriteData` |
| `WINHTTP_CALLBACK_STATUS_REQUEST_ERROR` | any of the above, on failure |

`WINHTTP_CALLBACK_STATUS_REQUEST_ERROR` is the only completion that means failure; every
other completion means the corresponding call succeeded.

**Measured signature of a wrong subscription:** a client subscribed with
`SEND_REQUEST | RECEIVE_RESPONSE` logged progress notifications normally and received
**0 completions in 120 000 ms**. The same client with the completion flags added
completed the same request in **78 ms**. Progress notifications keep flowing, so the log
looks alive - which is why this defect survives casual inspection.

### Correct subscription

```cpp
// Subscribe to every completion plus handle lifetime. ALL_COMPLETIONS covers the six
// completions above; HANDLES adds HANDLE_CREATED / HANDLE_CLOSING for context lifetime.
const DWORD kFlags = WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS
                   | WINHTTP_CALLBACK_FLAG_HANDLES;

if (WinHttpSetStatusCallback(hSession, &OnWinHttpStatus, kFlags, 0)
        == WINHTTP_INVALID_STATUS_CALLBACK) {
    return HRESULT_FROM_WIN32(GetLastError());
}
```

Use `WINHTTP_CALLBACK_FLAG_ALL_NOTIFICATIONS` (0xffffffff) while debugging: WinHTTP is
verbose about its own state machine and the extra trace pays for itself. Narrow it
afterwards.

`WinHttpSetStatusCallback` itself is synchronous even under `WINHTTP_FLAG_ASYNC`; its
return value is the verdict. The callback set on a session handle is inherited by request
handles created from it, but changing it later does not propagate to already-derived
handles - set it at each level you care about.

### Bind subscription to handling at compile time

The defect class is "the switch handles a notification nobody subscribed to" (dead branch)
or "the subscription includes a notification nobody handles" (silent drop). Both are
static facts, so assert them statically:

```cpp
constexpr DWORD kSubscribed = WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS
                            | WINHTTP_CALLBACK_FLAG_HANDLES;

// Every notification the dispatcher has a case for must be subscribed.
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE, "no send completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE,   "no headers completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_DATA_AVAILABLE,      "no data completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_READ_COMPLETE,       "no read completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_REQUEST_ERROR,       "no error completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING,      "no closing notice");
```

This is the cheapest possible guard: it costs nothing at runtime and it fails the build
the moment somebody "cleans up" the flag list.

## Waiting with a bound

A completion that never arrives must still end the operation. `INFINITE` turns a
subscription bug, a dropped connection, or a stalled proxy into an unkillable thread.

```cpp
// Bounded wait. Distinguish the three outcomes; never collapse timeout into failure.
enum class WaitResult { Completed, TimedOut, Abandoned };

WaitResult WaitForCompletion(HANDLE hEvent, DWORD timeoutMs) {
    const DWORD rc = WaitForSingleObject(hEvent, timeoutMs);  // never INFINITE
    switch (rc) {
        case WAIT_OBJECT_0: return WaitResult::Completed;
        case WAIT_TIMEOUT:  return WaitResult::TimedOut;
        default:            return WaitResult::Abandoned;     // WAIT_ABANDONED / WAIT_FAILED
    }
}
```

Timeout is a third state, not a failure and not a success - the same three-state discipline
that applies to any health check. See [[three-state-check-aggregation]].

## Cancellation: closing the handle is the cancel

There is no `WinHttpCancel`. An in-flight asynchronous request is cancelled by closing its
request handle, and the rules around that are unforgiving:

- After `WinHttpCloseHandle`, the handle must never be passed to any WinHTTP function
  again from any thread - including `WinHttpCloseHandle` itself. WinHTTP reuses handle
  values, so a double close can land on somebody else's request.
- Callbacks can still arrive after the close returns; WinHTTP tears handles down
  asynchronously. A cancelled operation surfaces as
  `WINHTTP_CALLBACK_STATUS_REQUEST_ERROR`.
- Closing a **parent** handle (session, connection) does not cancel a pending operation on
  a **child** request handle. Cancel the handle that owns the operation.
- Even when the handle is closed, the operation may still complete successfully rather
  than being cancelled. Both outcomes are legal; handle both.
- Keep the context object alive until `WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING` arrives.
  Setting the callback to `NULL` does not make this safe: WinHTTP does not synchronize
  `WinHttpSetStatusCallback` against callbacks already running on worker threads.

**Measured signature of self-cancellation:** a retry-close call placed inside the wait loop
fired on the first 50 ms tick and closed a perfectly healthy request. The failure surfaced
as `ERROR_WINHTTP_OPERATION_CANCELLED` (12017) reported against `WinHttpSendRequest` -
a call that had already been issued successfully. 12017 means "the handle the request was
operating on was closed before the operation completed"; when it appears without any
external cancel, the caller closed its own handle.

```cpp
// Close exactly once, from one place, and only when a cancel is actually intended.
std::atomic<bool> closed{false};
if (!closed.exchange(true)) {
    WinHttpCloseHandle(hRequest);   // the only close for this handle
}
// Do NOT put a close/retry-close inside the poll loop that is waiting for the completion.
```

## Buffer and thread rules that bite later

- WinHTTP does not copy your buffers. A send buffer must stay valid from
  `WinHttpSendRequest` until `SENDREQUEST_COMPLETE`; a receive buffer from
  `WinHttpReadData` until `READ_COMPLETE`. Stack buffers in a function that returns before
  the completion are a use-after-free with a network-timing trigger. See
  [[object-lifetime]] and [[raii-resource-management]].
- Use a receive buffer of at least 8 KB. Small buffers drive the
  `WinHttpQueryDataAvailable` / `WinHttpReadData` cycle into deep recursion and can exhaust
  the stack.
- WinHTTP delivers notifications on a single thread for the whole process. Blocking inside
  a callback stalls every HTTP request in the process and grows kernel-mode memory. Copy
  what you need, signal, and return.
- The callback runs on a thread that is not the one that issued the call, and it can be
  re-entered for a different request. It must be thread-safe. The one exception is
  `HANDLE_CLOSING`, which is guaranteed to be last for that handle.
- A notification can arrive **before** the context value is set, because the context is
  only supplied by `WinHttpSendRequest` / `WinHttpSetOption`. Handle `dwContext == NULL`.

## Diagnosing which defect you have

Run the client once with full notification tracing and count what arrives:

```cpp
void CALLBACK OnWinHttpStatus(HINTERNET, DWORD_PTR ctx, DWORD status,
                              LPVOID info, DWORD infoLen) {
    // Trace every notification id; completions are the six ids listed above.
    Trace("winhttp status=0x%08X ctx=%p len=%u", status, (void*)ctx, infoLen);
    if (status == WINHTTP_CALLBACK_STATUS_REQUEST_ERROR && info) {
        auto* r = static_cast<WINHTTP_ASYNC_RESULT*>(info);
        Trace("  request_error api=%lu code=%lu", r->dwResult, r->dwError);
    }
}
```

| Observation | Defect |
|---|---|
| Progress notifications flow, zero completions, wait never returns | Completion flags not subscribed |
| Completion arrives in the trace but the caller stays blocked | Wait not tied to that notification, or `INFINITE` on the wrong object |
| `REQUEST_ERROR` with `dwError == 12017` and no external cancel | The client closed its own handle |
| Nothing at all, not even `HANDLE_CREATED` | Callback never installed, or installed on the wrong handle level |

## Gotchas

- **Issue:** `WINHTTP_CALLBACK_FLAG_SEND_REQUEST` reads like "send request completed", and
  the documentation phrase "beginning and completing the sending of a request header"
  reinforces it. It expands to `SENDING_REQUEST | REQUEST_SENT` - two progress
  notifications, no completion bit. -> **Fix:** subscribe
  `WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS` (or the explicit completion flags plus
  `REQUEST_ERROR`) and pin it with `static_assert`.
- **Issue:** a retry or cleanup path calls `WinHttpCloseHandle` from inside the loop that
  is waiting for the completion, so the first tick kills the live request; the symptom is
  12017 attributed to a call that already succeeded. -> **Fix:** close from exactly one
  place, guarded by an atomic flag, and never on a timer that runs concurrently with the
  wait.
- **Issue:** `WaitForSingleObject(hEvent, INFINITE)` converts any missing completion into
  a permanent hang with no diagnostic. -> **Fix:** always pass a finite timeout and treat
  timeout as its own outcome, distinct from success and failure.
- **Issue:** context or buffer freed after `WinHttpCloseHandle` returns, on the assumption
  that the handle is dead. Callbacks can still be in flight on a worker thread. -> **Fix:**
  free only after `WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING`, which requires subscribing
  `WINHTTP_CALLBACK_FLAG_HANDLES`.
- **Issue:** cancelling by closing the session handle while a request is pending. The
  child operation is not cancelled and the code proceeds as if it were. -> **Fix:** close
  the request handle that owns the operation.
- **Issue:** the callback does real work (parsing, disk I/O, logging to a slow sink), so
  every HTTP request in the process slows down or stalls together. -> **Fix:** the callback
  copies state and signals; work happens on the caller's thread.

## See Also

- [[error-handling]] - error propagation across a C API boundary
- [[object-lifetime]] - buffer and context lifetime rules
- [[raii-resource-management]] - one-owner handle wrappers
- [[concurrency]] - thread-safety requirements for callbacks
- [[external-heartbeat-monitoring-for-native-process-crashes]] - detecting the hang from outside
- [[three-state-check-aggregation]] - timeout as a distinct verdict
- [WinHttpSetStatusCallback](https://learn.microsoft.com/windows/win32/api/winhttp/nf-winhttp-winhttpsetstatuscallback)
- [WINHTTP_STATUS_CALLBACK](https://learn.microsoft.com/windows/win32/api/winhttp/nc-winhttp-winhttp_status_callback)
- [WinHttpCloseHandle](https://learn.microsoft.com/windows/win32/api/winhttp/nf-winhttp-winhttpclosehandle)
- [Concurrency in WinHTTP](https://learn.microsoft.com/windows/win32/winhttp/concurrency-in-winhttp)
- [WinHTTP error messages](https://learn.microsoft.com/windows/win32/winhttp/error-messages)
