---
title: "WinHTTP-Client im asynchronen Modus"
description: "Abschlussbenachrichtigungen im Vergleich zu Fortschrittsbenachrichtigungen, begrenzte Wartezeiten und Abbruchsemantik für WinHTTP im WINHTTP_FLAG_ASYNC-Modus. Warum ein asynchroner Client endlos hängt und wie sich feststellen lässt, welchen von drei Defekten man hat."
level: 4
source_sha256: a19669f19678837aebd796ac935a3e0ceb304511e3d52d7b4c173bf6db006496
translation: machine
translated_at: '2026-10-24'
---
# WinHTTP-Client im asynchronen Modus {#winhttp-asynchronous-client}

Ein asynchroner WinHTTP-Client, der „hängt“, hat fast immer einen von drei voneinander unabhängigen
Defekten: Er hat die Abschlussbenachrichtigung, auf die er wartet, nie abonniert, er wartet ohne
Zeitgrenze, oder er bricht seine eigene, intakte Anfrage ab. Jeder hat eine eigene Signatur, und jeder
lässt sich isoliert nachweisen. Geprüft gegen `winhttp.h` aus dem Windows SDK 10.0.26100.0 und die
aktuelle Dokumentation des Herstellers.

## Benachrichtigungsmodell: Fortschritt ist nicht Abschluss {#notification-model-progress-is-not-completion}

`WinHttpSetStatusCallback` nimmt eine Bitmaske `dwNotificationFlags` entgegen. Die Namen sind die Falle:
Mehrere Flags klingen, als deckten sie den Abschluss ab, expandieren aber nur zu *Fortschritts*-
Benachrichtigungen. Aus dem SDK-Header:

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

Es gibt genau sechs Abschlussbenachrichtigungen, und jede gehört zu dem Aufruf, den sie beendet:

| Abschlussbenachrichtigung | Beendet |
|---|---|
| `WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE` | `WinHttpSendRequest` |
| `WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE` | `WinHttpReceiveResponse` |
| `WINHTTP_CALLBACK_STATUS_DATA_AVAILABLE` | `WinHttpQueryDataAvailable` |
| `WINHTTP_CALLBACK_STATUS_READ_COMPLETE` | `WinHttpReadData` |
| `WINHTTP_CALLBACK_STATUS_WRITE_COMPLETE` | `WinHttpWriteData` |
| `WINHTTP_CALLBACK_STATUS_REQUEST_ERROR` | jeden der obigen Aufrufe bei einem Fehler |

`WINHTTP_CALLBACK_STATUS_REQUEST_ERROR` ist die einzige Abschlussbenachrichtigung, die Fehler bedeutet;
jede andere Abschlussbenachrichtigung bedeutet, dass der zugehörige Aufruf erfolgreich war.

**Gemessene Signatur einer falschen Subskription:** Ein Client, der mit `SEND_REQUEST | RECEIVE_RESPONSE`
abonniert war, protokollierte Fortschrittsbenachrichtigungen normal und erhielt **0 Abschlüsse in
120 000 ms**. Derselbe Client mit ergänzten Abschlussflags schloss dieselbe Anfrage in **78 ms** ab.
Fortschrittsbenachrichtigungen laufen weiter, das Protokoll wirkt also lebendig, weshalb dieser Defekt
einer oberflächlichen Prüfung standhält.

### Korrekte Subskription {#correct-subscription}

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

Verwenden Sie während der Fehlersuche `WINHTTP_CALLBACK_FLAG_ALL_NOTIFICATIONS` (0xffffffff): WinHTTP
ist beim eigenen Zustandsautomaten ausführlich, und die zusätzliche Ablaufverfolgung lohnt sich.
Danach einschränken.

`WinHttpSetStatusCallback` selbst ist auch im `WINHTTP_FLAG_ASYNC`-Modus synchron; sein Rückgabewert ist
das Ergebnis. Der auf einem Session-Handle gesetzte Callback wird an daraus erzeugte Request-Handles
vererbt, eine spätere Änderung wirkt sich jedoch nicht auf bereits abgeleitete Handles aus. Setzen Sie
ihn auf jeder Ebene, die Ihnen wichtig ist.

### Subskription zur Compilezeit an die Behandlung binden {#bind-subscription-to-handling-at-compile-time}

Die Defektklasse lautet „der Switch behandelt eine Benachrichtigung, die niemand abonniert hat“ (toter
Zweig) oder „die Subskription enthält eine Benachrichtigung, die niemand behandelt“ (stille
Verwerfung). Beides sind statische Fakten, also prüfen Sie sie statisch:

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

Das ist der günstigste mögliche Schutz: Er kostet zur Laufzeit nichts und lässt den Build fehlschlagen,
sobald jemand die Flag-Liste „aufräumt“.

## Warten mit Zeitgrenze {#waiting-with-a-bound}

Eine Abschlussbenachrichtigung, die nie eintrifft, muss die Operation trotzdem beenden. `INFINITE`
verwandelt einen Subskriptionsfehler, eine abgebrochene Verbindung oder einen hängenden Proxy in einen
nicht beendbaren Thread.

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

Timeout ist ein dritter Zustand, weder Fehler noch Erfolg – dieselbe Drei-Zustände-Disziplin, die für
jede Zustandsprüfung gilt. Siehe [[three-state-check-aggregation]].

## Abbruch: Das Schließen des Handles ist der Abbruch {#cancellation-closing-the-handle-is-the-cancel}

Es gibt kein `WinHttpCancel`. Eine laufende asynchrone Anfrage wird abgebrochen, indem man ihr
Request-Handle schließt, und die Regeln dafür sind unnachgiebig:

- Nach `WinHttpCloseHandle` darf das Handle von keinem Thread mehr an irgendeine WinHTTP-Funktion übergeben
  werden – auch nicht an `WinHttpCloseHandle` selbst. WinHTTP verwendet Handle-Werte wieder, daher kann
  ein doppeltes Schließen die Anfrage eines anderen treffen.
- Callbacks können noch eintreffen, nachdem das Schließen zurückgekehrt ist; WinHTTP baut Handles
  asynchron ab. Eine abgebrochene Operation erscheint als
  `WINHTTP_CALLBACK_STATUS_REQUEST_ERROR`.
- Das Schließen eines **übergeordneten** Handles (Session, Connection) bricht keine ausstehende Operation
  auf einem **untergeordneten** Request-Handle ab. Brechen Sie das Handle ab, das die Operation besitzt.
- Selbst wenn das Handle geschlossen wird, kann die Operation erfolgreich abgeschlossen werden, statt
  abgebrochen zu werden. Beide Ausgänge sind zulässig; behandeln Sie beide.
- Halten Sie das Kontextobjekt am Leben, bis `WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING` eintrifft.
  Den Callback auf `NULL` zu setzen macht dies nicht sicher: WinHTTP synchronisiert
  `WinHttpSetStatusCallback` nicht mit Callbacks, die bereits auf Worker-Threads laufen.

**Gemessene Signatur der Selbstabschaltung:** Ein Retry-Close-Aufruf innerhalb der Wartschleife wurde beim
ersten 50-ms-Tick ausgelöst und schloss eine völlig intakte Anfrage. Der Fehler erschien als
`ERROR_WINHTTP_OPERATION_CANCELLED` (12017), gemeldet für `WinHttpSendRequest` – einen Aufruf, der bereits
erfolgreich abgesetzt worden war. 12017 bedeutet „das Handle, auf dem die Anfrage arbeitete, wurde
geschlossen, bevor die Operation abgeschlossen war“; tritt dies ohne externen Abbruch auf, hat der Aufrufer
sein eigenes Handle geschlossen.

```cpp
// Close exactly once, from one place, and only when a cancel is actually intended.
std::atomic<bool> closed{false};
if (!closed.exchange(true)) {
    WinHttpCloseHandle(hRequest);   // the only close for this handle
}
// Do NOT put a close/retry-close inside the poll loop that is waiting for the completion.
```

## Puffer- und Thread-Regeln, die später beißen {#buffer-and-thread-rules-that-bite-later}

- WinHTTP kopiert Ihre Puffer nicht. Ein Sendepuffer muss von `WinHttpSendRequest` bis
  `SENDREQUEST_COMPLETE` gültig bleiben, ein Empfangspuffer von `WinHttpReadData` bis `READ_COMPLETE`.
  Stack-Puffer in einer Funktion, die vor dem Abschluss zurückkehrt, sind ein Use-after-free mit einem
  netzwerkzeitabhängigen Auslöser. Siehe [[object-lifetime]] und [[raii-resource-management]].
- Verwenden Sie einen Empfangspuffer von mindestens 8 KB. Kleine Puffer treiben den Zyklus aus
  `WinHttpQueryDataAvailable` / `WinHttpReadData` in tiefe Rekursion und können den Stack erschöpfen.
- WinHTTP liefert Benachrichtigungen für den gesamten Prozess über einen einzigen Thread. Blockieren
  innerhalb eines Callbacks hält jede HTTP-Anfrage im Prozess an und lässt den Kernelspeicher wachsen.
  Kopieren Sie, was Sie brauchen, signalisieren Sie und kehren Sie zurück.
- Der Callback läuft auf einem Thread, der nicht derjenige ist, der den Aufruf abgesetzt hat, und er kann
  für eine andere Anfrage erneut betreten werden. Er muss threadsicher sein. Die einzige Ausnahme ist
  `HANDLE_CLOSING`, das für dieses Handle garantiert als letzte Benachrichtigung eintrifft.
- Eine Benachrichtigung kann **vor** dem Setzen des Kontextwerts eintreffen, da der Kontext erst von
  `WinHttpSendRequest` / `WinHttpSetOption` übergeben wird. Behandeln Sie `dwContext == NULL`.

## Diagnose: Welchen Defekt haben Sie? {#diagnosing-which-defect-you-have}

Führen Sie den Client einmal mit vollständiger Benachrichtigungsverfolgung aus und zählen Sie, was eintrifft:

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

| Beobachtung | Defekt |
|---|---|
| Fortschrittsbenachrichtigungen laufen, null Abschlüsse, Wartezeit kehrt nie zurück | Abschlussflags nicht abonniert |
| Abschluss erscheint in der Ablaufverfolgung, aber der Aufrufer bleibt blockiert | Warten nicht an diese Benachrichtigung gebunden, oder `INFINITE` auf dem falschen Objekt |
| `REQUEST_ERROR` mit `dwError == 12017` ohne externen Abbruch | Der Client hat sein eigenes Handle geschlossen |
| Gar nichts, nicht einmal `HANDLE_CREATED` | Callback nie installiert, oder auf der falschen Handle-Ebene installiert |

## Fallstricke {#gotchas}

- **Problem:** `WINHTTP_CALLBACK_FLAG_SEND_REQUEST` liest sich wie „Anfrage-Senden abgeschlossen“, und die
  Dokumentationsformulierung „Beginn und Abschluss des Sendens eines Anfrage-Headers“ bestärkt dies. Das
  Flag expandiert zu `SENDING_REQUEST | REQUEST_SENT` – zwei Fortschrittsbenachrichtigungen, kein
  Abschlussbit. → **Lösung:** `WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS` abonnieren (oder die expliziten
  Abschlussflags plus `REQUEST_ERROR`) und mit `static_assert` absichern.
- **Problem:** Ein Retry- oder Aufräumpfad ruft `WinHttpCloseHandle` aus der Schleife auf, die auf den
  Abschluss wartet, sodass der erste Tick die laufende Anfrage tötet; das Symptom ist 12017, zugeordnet
  einem Aufruf, der bereits erfolgreich war. → **Lösung:** Nur an genau einer Stelle schließen, durch ein
  atomares Flag abgesichert, und niemals durch einen Timer, der nebenläufig zum Warten läuft.
- **Problem:** `WaitForSingleObject(hEvent, INFINITE)` macht jede fehlende Abschlussbenachrichtigung zu
  einem dauerhaften Hang ohne Diagnose. → **Lösung:** Immer eine endliche Zeitgrenze übergeben und den
  Timeout als eigenes Ergebnis behandeln, getrennt von Erfolg und Fehler.
- **Problem:** Kontext oder Puffer wird nach der Rückkehr von `WinHttpCloseHandle` freigegeben, in der
  Annahme, das Handle sei tot. Callbacks können auf einem Worker-Thread noch laufen. → **Lösung:** Erst
  nach `WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING` freigeben; dafür muss `WINHTTP_CALLBACK_FLAG_HANDLES`
  abonniert werden.
- **Problem:** Abbruch durch Schließen des Session-Handles, während eine Anfrage aussteht. Die
  untergeordnete Operation wird nicht abgebrochen, und der Code fährt so fort, als wäre sie es. →
  **Lösung:** Das Request-Handle schließen, das die Operation besitzt.
- **Problem:** Der Callback erledigt echte Arbeit (Parsen, Plattenzugriffe, Logging in eine langsame
  Senke), sodass jede HTTP-Anfrage im Prozess gemeinsam langsamer wird oder stehen bleibt. → **Lösung:**
  Der Callback kopiert den Zustand und signalisiert; die Arbeit geschieht im Thread des Aufrufers.

## Siehe auch {#see-also}

- [Fehlerbehandlung – Ausnahmen und Alternativen](error-handling.md) – Fehlerweitergabe über eine C-API-Grenze
- [[object-lifetime]] – Lebensdauerregeln für Puffer und Kontext
- [[raii-resource-management]] – Handle-Wrapper mit einem einzigen Besitzer
- [Nebenläufigkeit – Threads, Async, Atomics](concurrency.md) – Anforderungen an die Threadsicherheit von Callbacks
- [[external-heartbeat-monitoring-for-native-process-crashes]] – Erkennung des Hangs von außen
- [[three-state-check-aggregation]] – Timeout als eigenständiges Urteil
- [WinHttpSetStatusCallback](https://learn.microsoft.com/windows/win32/api/winhttp/nf-winhttp-winhttpsetstatuscallback)
- [WINHTTP_STATUS_CALLBACK](https://learn.microsoft.com/windows/win32/api/winhttp/nc-winhttp-winhttp_status_callback)
- [WinHttpCloseHandle](https://learn.microsoft.com/windows/win32/api/winhttp/nf-winhttp-winhttpclosehandle)
- [Nebenläufigkeit in WinHTTP](https://learn.microsoft.com/windows/win32/winhttp/concurrency-in-winhttp)
- [WinHTTP-Fehlermeldungen](https://learn.microsoft.com/windows/win32/winhttp/error-messages)
