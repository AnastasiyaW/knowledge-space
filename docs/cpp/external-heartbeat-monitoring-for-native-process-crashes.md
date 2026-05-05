# External Heartbeat Monitoring for Native Process Crashes

Standard in-process exception handlers often fail to capture "silent" crashes caused by low-level system terminations or critical security failures. External monitoring via heartbeats and kernel tracing provides a reliable way to diagnose these failures.

## Limitations of In-Process Handlers
Windows can terminate a process through paths that bypass user-mode exception filters:

- **`__fastfail` (FAST_FAIL_FATAL_APP_EXIT):** Uses `int 0x29`. The kernel handles this directly, bypassing `SetUnhandledExceptionFilter` on Windows 8 and later.
- **Kernel-initiated `TerminateProcess`:** Direct termination by drivers or other processes provides no opportunity for stack unwinding or handler execution.
- **Driver-level `ExitProcess`:** User-mode drivers (e.g., DirectX/DirectML) may detect internal faults and call `ExitProcess` directly from their own crash paths.
- **Internal `__except` clauses:** Library code (e.g., ONNX Runtime, Qt) may catch a fault internally and exit the process voluntarily before global handlers are reached.

## Heartbeat Gap Detection Architecture
An external monitor process (watchdog) tracks the health of the target application by monitoring a stream of structured trace events or heartbeats.

- **Cadence Monitoring:** Target emits events (e.g., `system.stats`) at a fixed frequency (1 Hz).
- **Gap Detection:** If `now - last_heartbeat > threshold` while the process is still alive, the monitor flags a "hang".
- **Crash Correlation:** If the process terminates and the last heartbeat is older than the threshold, a silent crash is recorded relative to the last known valid state.

### Implementation Pattern (C++)
```cpp
// Target process heartbeat thread
void heartbeat_loop() {
    while (running) {
        emit_trace_event("heartbeat", get_timestamp());
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}
```

## External Dump Collection
When a gap is detected or a silent exit occurs, the monitor can capture the process state before the OS completes termination by using the `DbgHelp` library from an independent process.

### External MiniDump Trigger
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

## Kernel-Level Tracing (ETW)
Using Event Tracing for Windows (ETW) allows capturing the exact exit code even for processes killed by the kernel or `__fastfail`.

- **Provider:** `Microsoft-Windows-Kernel-Process` (`{22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}`)
- **Event:** `ProcessStop` (ID 2)
- **Data:** Contains `ExitStatus`, `ImageName`, and `ProcessID`.
- **Significance:** A `0xC0000409` (STATUS_STACK_BUFFER_OVERRUN) with subcode 7 typically indicates a `__fastfail` termination.

## Gotchas
- **Observer Effect:** Attaching debuggers or using tools like ProcDump (`DebugActiveProcess`) triggers `IsDebuggerPresent` and other anti-debug checks, which can change the execution path and mask the original crash.
- **Handle Access Rights:** `MiniDumpWriteDump` requires `PROCESS_QUERY_INFORMATION` and `PROCESS_VM_READ`. If the target is running at a higher integrity level (Admin) than the monitor, handle opening will fail.
- **WER Collision:** If Windows Error Reporting (WER) is already processing a crash, external `MiniDumpWriteDump` calls may return errors or produce corrupted files due to resource contention.

## See Also
- [[error-handling]]
- [[concurrency]]
- [[object-lifetime]]
- [[performance-optimization]]

