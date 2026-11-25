---
title: "ACE-Step 1.5"
description: "Artefakt- und hardwarebewusste Referenz für die Musikgenerierung mit ACE-Step 1.5 (base/SFT/turbo) sowie die XL-Ausführung."
level: 3
source_sha256: 41b142fc4ff664e57772a73c242bbb8f00516a383f01fb62abe8bbee03d2cc40
translation: machine
translated_at: '2026-10-24'
---
# ACE-Step 1.5 {#ace-step-15}

ACE-Step 1.5 ist ein Open-Source-Projekt zur Musikgenerierung mit den Artefakten base, SFT, turbo und XL. Schrittzahl, CFG-Verhalten, Speicherbedarf und Dauerbegrenzungen hängen vom gewählten Artefakt und vom Laufzeitmodus ab. Der Status wurde am **27.08.2026** anhand der offiziellen Release-Informationen, Model Cards, Tutorials und GPU-Richtlinien überprüft.

## Aktueller Status {#current-status}

| Bereich | Verifizierter Stand |
|---|---|
| Aktuelles Repository-Release | `v0.1.8`, veröffentlicht am 18.05.2026 |
| Lizenz | MIT auf der offiziellen Projekt-/Modelloberfläche; jedes heruntergeladene Artefakt einzeln prüfen |
| Base-1.5-Anspruch zum niedrigen Speicherbedarf | Lauffähig unter 4 GB im dokumentierten Base-Pfad; kein XL-Anspruch |
| Base/SFT-Sampling | 50 Schritte mit CFG laut dokumentierter Tabelle |
| Turbo-Sampling | 8 Schritte ohne CFG laut dokumentierter Tabelle |
| XL ab 12 GB | Laut offizieller GPU-Anleitung nicht empfohlen/unterstützt |

Die Aussage „ACE-Step 1.5 läuft unter 4 GB“ darf nicht mit den Anforderungen von ACE-Step 1.5 XL vermischt werden. Beide beziehen sich auf unterschiedliche Artefaktpfade.

## Artefakt-Auswahl {#artifact-selector}

| Artefakt | Schritte | CFG | Auswahlregel |
|---|---:|---|---|
| base | 50 | aktiviert | Basispfad für Qualität und Steuerung |
| SFT | 50 | aktiviert | Nur auswählen, wenn das feinabgestimmte Verhalten benötigt wird |
| turbo | 8 | deaktiviert | Schneller Pfad; CFG-Einstellungen von base nicht übernehmen |
| XL-Varianten | Versionsspezifisch | Versionsspezifisch | Die genaue Release-Tabelle und die GPU-Vorabprüfung verwenden |

Das vollständige Modellverzeichnis bzw. die vollständige Revision in den Lauf-Protokollen festhalten. Eine UI-Bezeichnung wie „XL“ reicht nicht aus, wenn mehrere base-/SFT-/turbo-Dateien installiert sind.

## GPU- und Speicherplanung für XL {#gpu-and-memory-planning-for-xl}

| Verfügbarer VRAM | Grenze laut offizieller Empfehlung |
|---|---|
| 12 GB oder weniger | XL nicht verwenden |
| 12–16 GB | Eingeschränkter XL-Pfad mit CPU-Offloading und INT8 |
| 16–20 GB | XL mit Offloading |
| 20 GB oder mehr | Vollständiger XL-Pfad |
| 24 GB oder mehr | Alle LM-Optionen ohne Offloading/Quantisierung laut Anleitung |

Für 12–16 GB begrenzt die Anleitung die maximale Dauer auf etwa 8 Minuten mit LM und 10 Minuten ohne LM. Dies nicht als „10 Minuten mit LM“ wiedergeben. Dauer, LM-Status, Offloading, Quantisierung und GPU müssen immer gemeinsam dokumentiert werden.

## Entwicklungsverlauf {#development-history}

| Datum | Ereignis | Zeitlicher Status |
|---|---|---|
| 03.02.2026 | Bericht zum initialen Release von ACE-Step 1.5 | Historische Grundlage |
| 04.02.2026 | Verfügbarkeit der Demo wiederhergestellt/gemeldet | Unterstützendes Ereignis; kein eigener Projektmeilenstein |
| 07.04.2026 | ACE-Step 1.5 XL gemeldet | Grundlage des aktuellen XL-Zweigs |
| 18.05.2026 | Repository-Release `v0.1.8` | Aktuelles Release zum Zeitpunkt der Überprüfung |

Die Wiederherstellung der Demo gilt als unterstützender Beleg für das initiale Ereignis, nicht als eigener neuer Entwicklungszweig.

## Reproduzierbares Lauf-Protokoll {#reproducible-run-record}

```yaml
ace_step_version: 0.1.8
artifact: base-or-sft-or-turbo-or-exact-xl-name
artifact_revision: <immutable-revision>
steps: 50-or-8
cfg_enabled: <true-or-false>
lm_enabled: <true-or-false>
duration_seconds: <integer>
dtype_or_quantization: <exact-value>
cpu_offload: <true-or-false>
gpu: <exact-model-and-vram>
peak_vram: <measured-value>
seed: <integer>
```

Vor der Generierung langer Stücke eine kurze Probe validieren. Liegt der Speicherbedarf nahe am Hardwarelimit, die Artefaktgröße reduzieren oder den dokumentierten Offloading-/INT8-Pfad verwenden, statt mehrere Parameter stillschweigend zu ändern.

## Grenzen der Community-Evidenz {#community-evidence-boundary}

Berichte der Community zu Qualität und Speicherbedarf sind nur dann nützlich, wenn sie Artefakt, Release, Dauer, LM-Status, Offloading, Quantisierung, Schrittzahl und GPU angeben. Zwei aktuelle Fehlerberichte liefern begrenzte betriebliche Hinweise:

- [Issue #1274](https://github.com/ace-step/ACE-Step-1.5/issues/1274) reproduziert NaN/Inf-Latents auf einer Quadro RTX 6000 (Turing) mit 24 GB für turbo und XL-turbo. Das Umstellen nur des Haupt-DiT-Fallbacks von FP16 auf FP32 löste den Fall des Meldenden, erhöhte aber den VRAM-Bedarf. Ein Beitragender bestätigte, dass der Dtype-Pfad einen Code-Fix benötigt. FP32 ist daher als diagnostische Umgehung zu behandeln, bis ein Release das Issue ausdrücklich schließt.
- [Issue #1271](https://github.com/ace-step/ACE-Step-1.5/issues/1271) zeigt, dass `cover_noise_strength=0.2` aus Cover/Remix in Text-zu-Musik übernommen wird und dort eine vollständig lange statische Ausgabe erzeugt. Ein Beitragender bestätigte den Backend-Pfad und empfahl, `cover_noise_strength` vor der Rückkehr zu Text-zu-Musik auf `0` zurückzusetzen, bis der Fehler behoben ist.

## Fallstricke {#gotchas}

- **Problem:** Den Base-Anspruch „unter 4 GB“ auf XL übertragen → **Lösung:** die XL-VRAM-Matrix verwenden; 12 GB oder weniger ist kein XL-Ziel.
- **Problem:** CFG für turbo aktivieren, weil base es verwendet → **Lösung:** für den dokumentierten turbo-Pfad 8 Schritte mit deaktiviertem CFG verwenden.
- **Problem:** Behaupten, 12–16 GB unterstütze 10 Minuten mit LM → **Lösung:** die Unterscheidung der Anleitung zwischen 8 Minuten mit LM und 10 Minuten ohne LM beibehalten.
- **Problem:** „ACE-Step 1.5“ ohne Artefakt/Release melden → **Lösung:** base/SFT/turbo/XL sowie die genaue Revision dokumentieren.
- **Problem:** Text-zu-Musik wird nach dem Cover-Modus plötzlich zu einer vollständig langen statischen Ausgabe → **Lösung:** die gespeicherten Lauf-Parameter prüfen und `cover_noise_strength` auf `0` zurücksetzen; Issue #1271 als versionsgebundenen Beleg festhalten.

## Zeitlicher Status {#temporal-status}

- **Aktuell:** `v0.1.8` zum Zeitpunkt der Überprüfung; artefaktspezifische Regeln für Schritte und CFG; offizielle GPU-Matrix für XL.
- **Historisch:** initiales Release im Februar und Wiederherstellung der Demo.
- **Abgelöst:** generische frühe Speicheraussagen, sofern sie auf XL angewendet werden.
- **Offen:** reproduzierbarer Qualitätsvergleich über Consumer-GPUs hinweg.

## Briefing für Agenten {#agent-brief}

Vor der Erstellung eines Rezepts das exakte ACE-Step-Artefakt und die GPU erfragen. Das aktuelle Release und die GPU-Anleitung abrufen und Schritte, CFG, LM, Dauer, Quantisierung und Offloading an dieses Artefakt binden. Jeden Versuch ablehnen, die Base-Aussage „unter 4 GB“ auf XL zu verallgemeinern oder Base-Sampling-Einstellungen für turbo wiederzuverwenden.

## Quellen {#sources}

- Offizielles Repository/Releases: https://github.com/ace-step/ACE-Step-1.5/releases
- Offizielle Model Card: https://huggingface.co/ACE-Step/Ace-Step1.5
- Chinesisches Tutorial: https://ace-step.github.io/ACE-Step-1.5/zh/Tutorial
- Paper: https://arxiv.org/abs/2602.00744
- Bericht zu NaN/FP32-Fallback bei Pre-Ampere-GPUs: https://github.com/ace-step/ACE-Step-1.5/issues/1274
- Bericht zum Leck der Cover-Parameter: https://github.com/ace-step/ACE-Step-1.5/issues/1271
