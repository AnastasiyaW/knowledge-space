---
level: 4
source_sha256: f75f0f677ff3f2bc162c4d05ddac1ee39b2ca83732930d936d48159f44a3e268
translation: machine
translated_at: '2026-10-24'
---
# Surveillance externe par heartbeat pour les crashs de processus natifs {#external-heartbeat-monitoring-for-native-process-crashes}

Les gestionnaires d'exceptions intégrés au processus échouent souvent à capturer les crashs « silencieux » provoqués par des terminaisons bas niveau du système ou par des défaillances critiques de sécurité. La surveillance externe, reposant sur des heartbeats et le traçage noyau, permet de diagnostiquer ces défaillances de manière fiable.

## Limites des gestionnaires intégrés au processus {#limitations-of-in-process-handlers}
Windows peut terminer un processus par des chemins qui contournent les filtres d'exceptions en mode utilisateur :

- **`__fastfail` (FAST_FAIL_FATAL_APP_EXIT) :** Utilise `int 0x29`. Le noyau gère directement cet appel, en contournant `SetUnhandledExceptionFilter` sous Windows 8 et versions ultérieures.
- **`TerminateProcess` initié par le noyau :** Une terminaison directe par un pilote ou par un autre processus ne laisse aucune possibilité de dérouler la pile ni d'exécuter un gestionnaire.
- **`ExitProcess` au niveau pilote :** Les pilotes en mode utilisateur (par ex. DirectX/DirectML) peuvent détecter une faute interne et appeler `ExitProcess` directement depuis leurs propres chemins de crash.
- **Clauses `__except` internes :** Le code de bibliothèque (par ex. ONNX Runtime, Qt) peut intercepter une faute en interne et quitter volontairement le processus avant que les gestionnaires globaux ne soient atteints.

## Architecture de détection des interruptions de heartbeat {#heartbeat-gap-detection-architecture}
Un processus de surveillance externe (watchdog) suit l'état de santé de l'application cible en observant un flux d'événements de trace structurés ou de heartbeats.

- **Surveillance de la cadence :** La cible émet des événements (par ex. `system.stats`) à une fréquence fixe (1 Hz).
- **Détection des interruptions :** Si `now - last_heartbeat > threshold` alors que le processus est toujours en vie, le moniteur signale un « blocage ».
- **Corrélation avec le crash :** Si le processus se termine et que le dernier heartbeat est plus ancien que le seuil, un crash silencieux est enregistré par rapport au dernier état valide connu.

### Modèle d'implémentation (C++) {#implementation-pattern-c}
```cpp
// Target process heartbeat thread
void heartbeat_loop() {
    while (running) {
        emit_trace_event("heartbeat", get_timestamp());
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}
```

## Collecte externe de vidages mémoire {#external-dump-collection}
Lorsqu'une interruption est détectée ou qu'une sortie silencieuse survient, le moniteur peut capturer l'état du processus avant que le système d'exploitation ne termine l'arrêt, en utilisant la bibliothèque `DbgHelp` depuis un processus indépendant.

### Déclenchement externe de MiniDump {#external-minidump-trigger}
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

## Traçage au niveau noyau (ETW) {#kernel-level-tracing-etw}
L'utilisation d'Event Tracing for Windows (ETW) permet de capturer le code de sortie exact, même pour les processus tués par le noyau ou par `__fastfail`.

- **Fournisseur :** `Microsoft-Windows-Kernel-Process` (`{22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}`)
- **Événement :** `ProcessStop` (ID 2)
- **Données :** Contient `ExitStatus`, `ImageName` et `ProcessID`.
- **Signification :** Un `0xC0000409` (STATUS_STACK_BUFFER_OVERRUN) avec le sous-code 7 indique généralement une terminaison par `__fastfail`.

## Pièges courants {#gotchas}
- **Effet d'observateur :** L'attachement d'un débogueur ou l'utilisation d'outils comme ProcDump (`DebugActiveProcess`) déclenche `IsDebuggerPresent` et d'autres vérifications anti-débogage, ce qui peut modifier le chemin d'exécution et masquer le crash d'origine.
- **Droits d'accès aux handles :** `MiniDumpWriteDump` requiert `PROCESS_QUERY_INFORMATION` et `PROCESS_VM_READ`. Si la cible s'exécute à un niveau d'intégrité supérieur (Administrateur) à celui du moniteur, l'ouverture du handle échouera.
- **Conflit WER :** Si Windows Error Reporting (WER) traite déjà un crash, les appels externes à `MiniDumpWriteDump` peuvent renvoyer des erreurs ou produire des fichiers corrompus en raison de la contention sur les ressources.

## Voir aussi {#see-also}
- [Gestion des erreurs - Exceptions et alternatives](error-handling.md)
- [Concurrence - Threads, Async, Atomics](concurrency.md)
- [[object-lifetime]]
- [Optimisation des performances](performance-optimization.md)
