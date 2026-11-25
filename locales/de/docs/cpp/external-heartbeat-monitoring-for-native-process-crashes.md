---
level: 4
source_sha256: f75f0f677ff3f2bc162c4d05ddac1ee39b2ca83732930d936d48159f44a3e268
translation: machine
translated_at: '2026-10-24'
---
# Externe Heartbeat-Überwachung für Absstürze nativer Prozesse {#external-heartbeat-monitoring-for-native-process-crashes}

Herkömmliche In-Process-Exception-Handler erfassen oft keine „stillen“ Abstürze, die durch systemnahe Prozessbeendigungen oder kritische Sicherheitsfehler verursacht werden. Eine externe Überwachung über Heartbeats und Kernel-Tracing bietet eine zuverlässige Möglichkeit, solche Fehler zu diagnostizieren.

## Grenzen von In-Process-Handlern {#limitations-of-in-process-handlers}
Windows kann einen Prozess über Pfade beenden, die User-Mode-Exception-Filter umgehen:

- **`__fastfail` (FAST_FAIL_FATAL_APP_EXIT):** Verwendet `int 0x29`. Der Kernel behandelt dies direkt und umgeht ab Windows 8 `SetUnhandledExceptionFilter`.
- **Kernel-initiiertes `TerminateProcess`:** Eine direkte Beendigung durch Treiber oder andere Prozesse lässt weder Stack-Unwinding noch die Ausführung eines Handlers zu.
- **Treiberseitiges `ExitProcess`:** User-Mode-Treiber (z. B. DirectX/DirectML) können interne Fehler erkennen und `ExitProcess` direkt aus ihren eigenen Crash-Pfaden aufrufen.
- **Interne `__except`-Klauseln:** Bibliothekscode (z. B. ONNX Runtime, Qt) kann einen Fehler intern abfangen und den Prozess freiwillig beenden, bevor globale Handler erreicht werden.

## Architektur der Heartbeat-Lückenerkennung {#heartbeat-gap-detection-architecture}
Ein externer Überwachungsprozess (Watchdog) verfolgt den Zustand der Zielanwendung, indem er einen Strom strukturierter Trace-Events bzw. Heartbeats überwacht.

- **Takt-Überwachung:** Das Ziel sendet Events (z. B. `system.stats`) in einer festen Frequenz (1 Hz).
- **Lückenerkennung:** Ist `now - last_heartbeat > threshold`, während der Prozess noch läuft, meldet der Monitor einen „Hang“.
- **Absturz-Korrelation:** Beendet sich der Prozess und ist der letzte Heartbeat älter als der Schwellenwert, wird ein stiller Absturz relativ zum letzten bekannten gültigen Zustand erfasst.

### Implementierungsmuster (C++) {#implementation-pattern-c}
```cpp
// Target process heartbeat thread
void heartbeat_loop() {
    while (running) {
        emit_trace_event("heartbeat", get_timestamp());
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}
```

## Externe Dump-Erfassung {#external-dump-collection}
Wird eine Lücke erkannt oder endet der Prozess still, kann der Monitor den Prozesszustand erfassen, bevor das Betriebssystem die Beendigung abschließt. Dazu verwendet er aus einem unabhängigen Prozess heraus die Bibliothek `DbgHelp`.

### Externer MiniDump-Auslöser {#external-minidump-trigger}
```cpp
#include <windows.h>
#include <DbgHelp.h>

void trigger_external_dump(DWORD process_id, const char* file_path) {
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, process_id);
    if (hProcess != NULL) {
        HANDLE hFile = CreateFileA(file_path, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hFile != INVALID_HANDLE_VALUE) {
            // Write full memory dump from external process
            MiniDumpWriteDump(hProcess, process_id, hFile, MiniDumpWithFullMemory, NULL, NULL, NULL);
            CloseHandle(hFile);
        }
        CloseHandle(hProcess);
    }
}
```

## Kernel-Level-Tracing (ETW) {#kernel-level-tracing-etw}
Mit Event Tracing for Windows (ETW) lässt sich auch bei Prozessen, die vom Kernel oder durch `__fastfail` beendet wurden, der genaue Exit-Code erfassen.

- **Provider:** `Microsoft-Windows-Kernel-Process` (`{22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}`)
- **Event:** `ProcessStop` (ID 2)
- **Daten:** Enthält `ExitStatus`, `ImageName` und `ProcessID`.
- **Bedeutung:** Ein `0xC0000409` (STATUS_STACK_BUFFER_OVERRUN) mit Subcode 7 deutet typischerweise auf eine Beendigung durch `__fastfail` hin.

## Fallstricke {#gotchas}
- **Beobachtereffekt:** Das Anhängen von Debuggern oder Werkzeugen wie ProcDump (`DebugActiveProcess`) löst `IsDebuggerPresent` und andere Anti-Debug-Prüfungen aus. Dadurch kann sich der Ausführungspfad ändern und der ursprüngliche Absturz verschleiert werden.
- **Zugriffsrechte auf Handles:** `MiniDumpWriteDump` benötigt `PROCESS_QUERY_INFORMATION` und `PROCESS_VM_READ`. Läuft das Ziel mit einer höheren Integritätsstufe (Administrator) als der Monitor, schlägt das Öffnen des Handles fehl.
- **Kollision mit WER:** Verarbeitet Windows Error Reporting (WER) bereits einen Absturz, können externe `MiniDumpWriteDump`-Aufrufe aufgrund von Ressourcenkonflikten Fehler zurückgeben oder beschädigte Dateien erzeugen.

## Siehe auch {#see-also}
- [Fehlerbehandlung – Exceptions und Alternativen](error-handling.md)
- [Nebenläufigkeit – Threads, Async, Atomics](concurrency.md)
- [[object-lifetime]]
- [Performance-Optimierung](performance-optimization.md)
