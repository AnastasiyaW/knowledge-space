---
level: 3
source_sha256: 73ec683ba86c71539fe850da09b20d0cb603af76eaf07269c9850d43244a267b
translation: machine
translated_at: '2026-10-24'
---
# Berechnungsverschleierung: Split-Inference und Converter-Architekturen {#computation-obfuscation-split-inference-and-converter-architectures}

Datum: 2026-04-03
Kontext: Desktop-Produkt für ML-Inferenz. Schutz des Modell-IP, indem die rohen Gewichte für Piraterie nicht ausreichen: Die Ausgabe benötigt eine separate Transformation, um nutzbar zu sein.

---

## Kernproblem {#core-problem}

Die Verschlüsselung der Gewichte verhindert die Extraktion, aber sobald sie für die Inferenz entschlüsselt sind, läuft das Modell im Prozess des Angreifers. Ansätze zur Berechnungsverschleierung machen die Ausgabe des Modells selbst unbrauchbar, solange keine zweite Komponente vorhanden ist, die der Angreifer nicht kontrolliert.

---

## Variante A: Lokaler Converter-Dienst {#variant-a-local-converter-service}

Die letzte Schicht des Modells gibt einen nicht-RGB-kodierten Tensor aus (verwürfelte Kanäle, affine Transformation, XOR mit einem Schlüssel). Ein separater, signierter Prozess wandelt ihn in ein nutzbares Bild um.

**Architektur:**
```text
ONNX model -> encoded_tensor (not RGB) -> Converter.exe -> JPEG/PNG
```

**Eigenschaften des Converter-Binärs:**
- Separater Prozess, separate Signatur (Authenticode unter Windows, notarisiert unter macOS)
- Enthält die Dekodierungstransformation, verschleiert (LLVM-Passes, String-Verschlüsselung)
- Prüft regelmäßig den Lizenzserver; bei einem Fehler wird die Konvertierung gestoppt
- Prüft die eigene Integrität und erkennt Debugger

**Verschleierungs-Stack (C++):**
```text
LLVM passes:
  - Control Flow Flattening (CFF): state machine replaces conditional branches
  - Bogus Control Flow: dead code inserted with opaque predicates
  - String Encryption: all plaintext constants encrypted, decrypted at runtime
  
Binary protection (post-compile):
  - VMProtect / Themida: wraps critical functions in VM bytecode
  - Custom packer: compresses + encrypts PE/Mach-O sections
  - Anti-debug: TLS callbacks fire before main(), detect and exit
```

**Wirksamkeit: 5/10.** Sobald ein Angreifer die Transformation aus einer Binärversion rekonstruiert hat, sind alle bisherigen und aktuellen Kopien gebrochen. Die Transformation ist pro Modellversion fest. Sie verzögert gelegentliche Piraterie um Wochen bis Monate; motivierte Angreifer mit Reverse-Engineering-Kenntnissen werden sie extrahieren.

**Modellversionierung erzeugt natürlichen Neuschutz:**
- Jedes Modell-Update ändert das Ausgabeformat → erzwingt einen neuen Converter
- Der alte Converter funktioniert mit der neuen Modell-Binary nicht mehr
- Eine geknackte Version veraltet nach einem Update-Zyklus (2–4 Wochen)

---

## Variante B: Split-Inference (serverseitige Schichten) {#variant-b-split-inference-server-side-layers}

Kritische Schichten laufen auf einem entfernten Server. Der Client kann die Inferenz nicht ohne Beteiligung des Servers abschließen.

**Split-Strategien:**

| Strategie | Lokal | Server | Größe des Zwischentensors | Latenz-Overhead |
|-----------|-------|--------|---------------------------|-----------------|
| Früher Split | nur Encoder | Hauptverarbeitung | Groß (unkomprimierte Feature-Map) | 200–500 ms |
| Später Split | 95 % der Schichten | 1–2 Finalisierungsschichten | Klein (Bottleneck) | 50–150 ms |
| Mittlerer Split | Pre + Post | Bottleneck-Schicht | Minimal | 50–100 ms |

**Später Split wird für Desktop-Produkte bevorzugt:** Der Großteil der Berechnung bleibt lokal (unter Nutzung der GPU des Anwenders), es werden minimale Daten übertragen, und der Server übernimmt nur die Finalisierung.

```text
Client GPU: layers 0..N-2 -> intermediate_tensor [B, C, H/8, W/8]
HTTP POST /finalize:
  body: {tensor: base64(gzip(intermediate_tensor)), license_token: ...}
  response: {output_tensor: ...}
Client: postprocess + decode output
```

**Stärken:**
- Serverseitige Schichten fehlen auf dem Client physisch – nicht „umgehbar“, sondern buchstäblich nicht vorhanden
- Der Server kann unabhängig von der Client-Verteilung aktualisiert werden
- Serverseitige Nutzungsprotokolle ermöglichen die Erkennung von Anomalien

**Schwächen:**
- **Erfordert Internetverbindung.** Fotografen im Außeneinsatz, Offline-Workflows, China/Russland/Unternehmens-Proxys: alle blockiert.
- Latenz: 50–200 ms pro Inferenz sind für interaktive Werkzeuge spürbar.
- Infrastrukturkosten: serverseitige GPU-Inferenz.
- Single Point of Failure.

**Wirksamkeit: 8/10 Schutz, 4/10 UX** für ein Desktop-first-Produkt, das „auf schwacher GPU funktioniert“.

---

## Variante C: Hybrid – „Server-Enhancement“-Modell {#variant-c-hybrid-server-enhancement-model}

Das vollständige Modell läuft lokal in Standardqualität. 1–2 Enhancement-Schichten auf dem Server erzeugen Premium-Qualität. Kostenlose Stufe = nur lokal. Bezahlte Stufe = lokal + Server-Enhancement.

```text
Local inference -> "good" output (usable, watermarked)
         +
Server enhancement request (paid, requires active license)
         -> "premium" output (higher PSNR, finer detail, no visible watermark)
```

**Freemium über den Qualitätsunterschied:**
- Piraten nutzen die lokale Version – sie erhalten „gute“ Ausgaben mit sichtbarem Wasserzeichen
- Zahlende Nutzer erhalten serverseitig verbesserte Ausgaben – messbar besser, ohne Overlay
- Der Server-Endpunkt ist ohne gültiges Lizenz-Token nicht erreichbar
- Raubkopien können auf den Premium-Endpunkt nicht zugreifen, selbst wenn die lokale Binary geknackt wurde

**Anforderung an den Qualitätsunterschied:** Ist der Unterschied zwischen lokal und serverseitig verbessert in professioneller Ausgabe nicht sichtbar, gibt es keinen Kaufanreiz. Ziel: 2–3 dB PSNR-Verbesserung oder ein sichtbarer Detailunterschied bei 100 % Zoom auf druckgroßen Bildern.

**Wirksamkeit: 7/10.** Verhindert Piraterie nicht vollständig, macht aber das Bezahlen zur rationalen Wahl. Offline funktioniert immer. Ein Serverausfall führt zu „gut“ statt zu einem totalen Ausfall.

---

## Empfehlungsmatrix {#recommendation-matrix}

| Szenario | Empfohlene Variante |
|----------|---------------------|
| Desktop-first, Offline erforderlich, geringe Toleranz für Serverkosten | A (Converter) + C (Freemium-Qualität) |
| Cloud-first- oder API-Produkt, Latenz akzeptabel | B (Split-Inference) |
| SaaS mit Premium-Stufe | C (Hybrid-Enhancement) |
| Maximaler IP-Schutz unabhängig von der UX | B (Split-Inference) |

**Praktische Kombination für ein Desktop-Produkt:** Variante A als günstige erste Schicht (verzögert 80 % der gelegentlichen Piraten), Variante C zur Monetarisierung der verbleibenden Nutzer, die zwar piraten, aber für Qualität bezahlen würden.

---

## Referenz zur Binary-Härtung {#binary-hardening-reference}

### LLVM-Verschleierung (Ollvm / Hikari / O-MVLL) {#llvm-obfuscation-ollvm-hikari-o-mvll}

```cmake
# CMake: add obfuscation passes via Clang plugin
target_compile_options(converter PRIVATE
  -mllvm -fla          # Control Flow Flattening
  -mllvm -bcf          # Bogus Control Flow
  -mllvm -sub          # Instruction Substitution
  -mllvm -sobf         # String Obfuscation
)
```

**O-MVLL** (kommerziell, unterstützt Android NDK, iOS, macOS, Windows):
- VM-basierter Schutz: umschließt heiße Funktionen in interpretiertem Bytecode
- Trampolines verhindern die Auflösung von Symbolen
- Konstanten-Verschleierung: Konstanten werden zur Laufzeit aufgeteilt und rekonstruiert

### Anti-Debug im TLS-Callback (Windows) {#anti-debug-in-tls-callback-windows}

```cpp
// Fires before main() - attacker cannot skip
void NTAPI tls_callback(PVOID, DWORD reason, PVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        if (IsDebuggerPresent()) ExitProcess(0);
        BOOL remote = FALSE;
        CheckRemoteDebuggerPresent(GetCurrentProcess(), &remote);
        if (remote) ExitProcess(0);
    }
}
#pragma comment(linker, "/INCLUDE:_tls_used")
#pragma data_seg(".CRT$XLB")
PIMAGE_TLS_CALLBACK p_tls_callback = tls_callback;
#pragma data_seg()
```

---

## Stolperfallen {#gotchas}

- **Das Knacken des Converters ist eine einmalige, amortisierte Angelegenheit.** Sobald ein Cracker die Ausgabetransformation aus Version 2.1.3 rekonstruiert hat, ist diese Transformation öffentlich. Anders als bei der Verschlüsselung (Schlüssel pro Nutzer) ist die Converter-Transformation über alle Kopien hinweg identisch. Die einzige Verteidigung sind Modell-Updates, die das Format ändern.
- **VMProtect/Themida erhöhen die Startlatenz.** VM-geschützte Initialisierung kann beim ersten Start 0,5–3 Sekunden hinzufügen. Nutzer bemerken das und melden es. Profilieren Sie und schützen Sie nur das Minimum: die Lizenzprüfung und die Schlüsselextraktion, nicht das gesamte Binary.
- **Offline ist für professionelle Foto-Tools zwingend.** Variante B (Split-Inference) widerspricht grundsätzlich der Offline-Nutzung. Wenn Ihre Zielgruppe ein Hochzeitsfotograf vor Ort ohne Mobilfunkempfang ist, ist Variante B unabhängig von der Schutzstärke ausgeschlossen.
- **Der Split-Inference-Endpunkt kann wiedergegeben werden.** Ist der Zwischentensor nicht an ein Sitzungs-Token oder eine Nonce gebunden, kann ein Angreifer ihn abfangen und gegen den Server erneut einspielen. Binden Sie jede Inferenzanfrage an ein signiertes Sitzungs-Token mit Ablaufzeit.
- **Fehlalarme von Virenscannern durch starke Verschleierung.** Control-Flow-Flattening + String-Verschlüsselung + Packer lösen heuristische Erkennungen in Windows Defender, Kaspersky und BitDefender aus. Reichen Sie das Binary vor dem Versand bei den Antivirenherstellern ein oder nutzen Sie Codesignierung mit einem Extended-Validation-Zertifikat, um die Rate an Fehlalarmen zu senken.

## Siehe auch {#see-also}
- [[output-scrambling-antipiracy]]
- [[remote-kill-switch]]
- [[watermarking-encrypted-models]]
- [[model-weight-encryption]]
- [[licensing-implementation-cpp]]
