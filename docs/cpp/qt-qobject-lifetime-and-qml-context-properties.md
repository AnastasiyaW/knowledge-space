---
title: Qt QObject Lifetime and QML Context Properties
description: Thread-affinity deletion rules and a bounded migration policy for QML context properties in Qt 6.
tags: [cpp, qt, qml, qobject, lifetime]
---

# Qt QObject Lifetime and QML Context Properties

Qt 6 object lifetime is governed by QObject ownership, thread affinity, and event-loop state. QML context exposure adds a separate lifetime contract: the context does not own an injected QObject.

## Review the lifetime, not just `deleteLater()`

Before accepting a cleanup path, identify the object's owner, its current affinity, whether the owning thread can process deferred events, and what ends that thread.

| Situation | Correct review conclusion |
| --- | --- |
| Parent and child live in one thread | The parent owns and deletes the child. Parent and child cannot have different thread affinities. |
| Object receives queued work | Its event handler runs in the thread of its affinity, not necessarily the caller's thread. |
| Another thread needs cleanup | Direct deletion is unsafe unless lifetime and event processing are synchronized. Prefer the documented teardown path in the object's affinity thread. |
| `deleteLater()` before an event loop starts | Qt deletes the object after that event loop starts. |
| `deleteLater()` after the main event loop stops | Qt does not delete the object. Shutdown needs an earlier cleanup decision. |
| Object lives in a worker thread without a running loop | A `deleteLater()` object is destroyed when that thread finishes. |

The blanket rule “no event loop means no deletion” is wrong. The lifecycle phase matters: Qt documents different outcomes before startup, after main-loop shutdown, and at worker-thread finish. [QObject](https://doc.qt.io/qt-6/qobject.html) and [Threads and QObjects](https://doc.qt.io/qt-6/threads-qobject.html) define those cases.

### Worker-object teardown

Keep the QThread object and its worker separate. The QThread object has the affinity of the thread that created it; it is not the worker thread itself.

The documented worker-object pattern connects `QThread::finished()` to the worker's `QObject::deleteLater()`. It is not a substitute for cancellation, a completion protocol, or correct sequencing: request completion through the worker's own delivery path, let the thread finish, and wait before destroying objects that own or depend on that thread. Do not block the creator thread in a way that prevents its queued completion path from running.

## QML context exposure has two separate mutations

`QQmlContext` properties are names held by the context. They are not `QObject` properties. Adding or replacing such a name with `setContextProperty()` changes the context and can force bindings in that context to re-evaluate after objects exist.

An injected context QObject is different. Its `Q_PROPERTY` values can change through their `NOTIFY` signals without adding or replacing a context property. Treat these as distinct review questions:

| Change | Review question |
| --- | --- |
| Add, replace, or change the context object/property | Was all context setup completed before QML objects were created? |
| Update a property of an existing injected QObject | Does the `Q_PROPERTY` have the correct `NOTIFY` signal, thread affinity, and owner lifetime? |

`QQmlContext` reports that a context object's property updates are observed via the property's notify signal, while setting the context object or adding context properties after creation forces binding re-evaluation. [QQmlContext](https://doc.qt.io/qt-6/qqmlcontext.html) documents both behaviors.

### Bounded compatibility exposure

Existing pre-load context exposure can be a compatibility boundary rather than an automatic rewrite trigger. Keep it bounded: inject before `setSource()` or component creation, document the names expected by the QML root, make the injected object's owner outlive the QML engine, and do not mutate the context shape after startup.

`setContextProperty()` does not transfer ownership of the injected QObject; its C++ owner must outlive QML use. For new reusable APIs, prefer root-object properties, registered types, or singletons. Context properties create undeclared dependencies and are invisible to ahead-of-time QML tooling. See [Embedding C++ Objects into QML with Context Properties](https://doc.qt.io/qt-6/qtqml-cppintegration-contextproperties.html).

## Review checklist

- Record the affinity and owner of every long-lived QObject, including its children.
- For each deferred deletion, state whether the relevant loop has not started, is running, has stopped, or ends with a worker thread.
- Trace completion, cancellation, thread finish, and destruction in that order; a connection line alone is not a shutdown protocol.
- Treat every QML context name as an implicit API dependency. Record its provider, owner, and the point before QML object creation at which it is injected.
- Use a `NOTIFY`-backed QObject property for stable live state; do not replace a context name to deliver ordinary state changes.

## Gotchas

- **Calling `deleteLater()` during shutdown:** The main event loop may already be stopped, so the deferred deletion will never occur. Decide ownership and teardown before the loop exits.
- **Deleting a moved QObject from the creator thread:** Affinity moved with the QObject; a cross-thread direct `delete` can race event delivery. Use the worker's lifecycle and an owner-thread-safe deletion path.
- **Replacing a context property for normal state updates:** This changes the context and can re-evaluate every binding. Expose a QObject with `Q_PROPERTY` and `NOTIFY` when the shape is stable and only values change.
- **Assuming QML owns an injected pointer:** `QQmlContext` does not take ownership. A stack object is valid only while its C++ scope outlives the view or engine that uses it.
- **Treating context injection as invisible harmless glue:** The QML file has an undeclared dependency that `qmllint`, the QML language server, and the Quick Compiler cannot resolve ahead of time.

## Limitations

This is a review reference, not runtime proof for any application. It does not choose an application's cancellation protocol, QML module boundary, or shutdown ordering. Verify the actual affinity graph, signal connections, event-loop ownership, and startup/shutdown behavior in the target build.

## See Also

- [[object-lifetime]]
- [[scope-and-lifetime]]
- [[concurrency]]
- [[smart-pointers]]
