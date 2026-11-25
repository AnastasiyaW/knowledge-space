---
title: "SenseNova U1 und ComfyUI"
description: "Grenzbewusste Referenz für offizielle SenseNova-U1/U1.5-Artefakte, offizielle ComfyUI-Nodes und den Drittanbieter-Wrapper ComfyUI_SenseNova_U1."
level: 3
source_sha256: 08fa2483f3d9b1c6a935a0e5d419d1324ec93767dabad05893d0ddf3c88a42b9
translation: machine
translated_at: '2026-10-24'
---
# SenseNova U1 und ComfyUI {#sensenova-u1-and-comfyui}

SenseNova U1 ist eine offizielle Modellfamilie für Bilderzeugung und Bildbearbeitung. `smthemex/ComfyUI_SenseNova_U1` ist ein separater Drittanbieter-Wrapper. Offizielle Nodes, offizielle Modellfähigkeiten und Wrapper-Fähigkeiten müssen unabhängig voneinander zugeordnet werden. Der Status wurde am **27.08.2026** anhand erstrangiger englischer und chinesischer Quellen sowie des Wrapper-Repositorys verifiziert.

## Aktuelle Artefakt-Übersicht {#current-artifact-map}

| Oberfläche | Verifizierter Stand |
|---|---|
| Offizielles Repository | `OpenSenseNova/SenseNova-U1`, Apache-2.0 |
| Offiziell verifizierte Revision | `022fa663d3f1a3c6822ec0b534e336a991bb7b0b` |
| Offizielle ComfyUI-Nodes | `OpenSenseNova/ComfyUI-SenseNova-U1` v0.3.0; Registry-Spiegel von `SenseNova-U1/apps/comfyui` |
| Revision des offiziellen ComfyUI-Spiegels | `fc90611ac6f9eecfbf0f6a5115b13f609683e202` |
| Drittanbieter-Wrapper | `smthemex/ComfyUI_SenseNova_U1`, Apache-2.0 |
| Verifizierte Wrapper-Revision | `35f930a349aa38a94100529fd1ec7dd8b31f9ec9` |
| Wrapper-Formate | U1.5 Preview/Formal sowie GGUF-, INT8-, FP8- und BF16-Pfade, wie im aktuellen README beschrieben |
| Älterer 8-Schritt-LoRA-Pfad | Im Wrapper-README durchgestrichen; als Verlauf erhalten, kein aktueller Standard |

Schreiben Sie nicht jede offizielle U1/U1.5-Funktion dem Drittanbieter-Wrapper zu. Werten Sie den quantisierten Pfad des Wrappers nicht als Beleg dafür, dass das offizielle Modell mit voller Genauigkeit auf dieselbe Hardware passt.

## Entwicklungsverlauf {#development-history}

| Datum | Strang | Ereignis | Zeitlicher Status |
|---|---|---|---|
| 2026-05-05 | Drittanbieter-Wrapper | Erster Bericht zum ComfyUI-Wrapper | Historische Grundlage |
| 2026-05-21 | offizielles Projekt | Code für Full Fine-Tuning veröffentlicht | Aktuelle offizielle Fähigkeit |
| 2026-06-19 | Wrapper/Adapter | Bericht zur 8-Schritt-LoRA für Infografiken | Ersetzt/durchgestrichen in der aktuellen Wrapper-Dokumentation |
| 2026-08-24 | offizielles ComfyUI | Registry-Spiegel v0.3.0 bereitgestellt | Aktuelle offizielle ComfyUI-Oberfläche |
| 2026-08-26 | Wrapper | Aktuelle Wrapper-Revision verifiziert | Aktueller Wrapper-Endpunkt |
| 2026-08-27 | offizielles Projekt | Aktuelle offizielle Revision verifiziert | Aktueller offizieller Endpunkt |

Die Entwicklung der offiziellen Modelle und die des Drittanbieter-Wrappers sind durch Integration verbunden, nicht durch Eigentum. Stellen Sie sie als getrennte Subjekte/Stränge mit expliziten `integrates_with`-Verknüpfungen dar, nicht als eine falsche Vorgängerkette.

## Hardware-Auswahl {#hardware-selection}

Die offizielle chinesische FAQ nennt für vollständiges BF16 etwa 36 GB und setzt für diesen Pfad mehr als 36 GB VRAM voraus. Für eingeschränkte Geräte empfiehlt sie niedrigere bzw. ausgewogene GGUF-Varianten.

Dieselbe FAQ warnt, dass ein vollständiger Q6-Pfad auf 8 GB unsicher ist und zu einem OOM führen kann. Machen Sie aus „GGUF verfügbar“ nicht „jede GGUF-Stufe passt in 8 GB“.

```yaml
surface: official-nodes-or-third-party-wrapper
official_revision: 022fa663d3f1a3c6822ec0b534e336a991bb7b0b
wrapper_revision: 35f930a349aa38a94100529fd1ec7dd8b31f9ec9
model: U1-or-exact-U1.5-artifact
format: BF16-or-FP8-or-INT8-or-exact-GGUF
adapter: <exact-hash-or-none>
comfyui_revision: <exact-revision>
gpu_and_vram: <exact-device>
steps: <integer>
resolution: <width>x<height>
peak_vram: <measured-value>
```

## Praktische Auswahl {#practical-selection}

- Bevorzugen Sie offizielle Registry-Nodes, wenn der offizielle Artefakt- bzw. Laufzeitvertrag die Aufgabe abdeckt. Das aktuelle offizielle Paket ist `ComfyUI-SenseNova-U1` v0.3.0 und setzt die v3-Node-API von ComfyUI voraus (`comfy_api.latest`).
- Installieren Sie das offizielle Paket über ComfyUI Manager/Registry oder fixieren Sie die Revision des Spiegels. Das README nennt `OpenSenseNova/SenseNova-U1/apps/comfyui` als maßgebliche Quelle.
- Verwenden Sie den Drittanbieter-Wrapper nur, wenn genau dessen Quantisierungs- bzw. Modellpfad benötigt wird, und fixieren Sie sowohl Wrapper als auch Modell.
- Entfernen oder deaktivieren Sie ein manuell kopiertes Legacy-Verzeichnis `ComfyUI_SenseNova_U1`, bevor Sie das offizielle Paket aktivieren. Beide Implementierungen registrieren überlappende Node-IDs; bleiben beide erhalten, entscheidet die Ladereihenfolge darüber, welcher Code läuft.
- Verwenden Sie vollständiges BF16 nur mit nachgewiesener Reserve über der dokumentierten Anforderung.
- Beginnen Sie auf 8 GB mit einer dokumentierten niedrigen bzw. ausgewogenen Quantisierung und validieren Sie einen minimalen Workflow; wählen Sie nicht allein anhand des Namens vollständiges Q6.
- Für die Generierung von Infografiken dokumentieren Sie Sprache, Fehler bei wiederholtem Text, Hintergrundverhalten, Adapter-Hash, Schrittzahl und Auflösung.

## Trainingsgrenze {#training-boundary}

Das offizielle Projekt hat am 21.05.2026 Code für Full Fine-Tuning veröffentlicht. Die offizielle FAQ beschreibt den LoRA-Trainingscode als geplant und nicht gleichwertig mit dem bereits veröffentlichten Full-Fine-Tuning-Pfad. Prüfen Sie diesen Status erneut, bevor Sie LoRA-Training als unterstützt darstellen, da er zeitlich instabil ist.

Lokale und API-Oberflächen können unterschiedliche Modelle, Standardwerte, Grenzen und Ausgabeverhalten zeigen. Halten Sie API-Ergebnisse aus lokalen Workflow-Benchmarks heraus, sofern nicht genau dieser Endpunkt Gegenstand der Untersuchung ist.

## Grenze der Community-Evidenz {#community-evidence-boundary}

Der ältere Bericht zur 8-Schritt-LoRA für Infografiken ist als Projektverlauf nützlich, aber kein aktueller Standard: Die eigene Wrapper-Dokumentation streicht diesen Pfad inzwischen durch. Konkrete Wrapper-Issues liefern zusätzlichen Kontext:

- [Issue #12](https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/12) berichtet von einer Bearbeitung mit `SenseNova-U1-8B-MoT-8step-Q8_0.gguf` (18,6 GB) auf einer NVIDIA-Karte mit 16 GB: Es wurden 4,92 GB GPU-Allokation protokolliert, und der 8-Schritt-Prompt benötigte 42,19 Sekunden, was auf starkes Offloading bzw. eine Unterauslastung hindeutet. Ein weiterer Berichterstatter maß für einen 2K-Lauf auf einer RTX 4090 insgesamt 37 GB kombinierten GPU- und geteilten Speicher und schlug vor, `prefetch_count=0` zu testen. Dies sind workflowspezifische Beobachtungen, keine Garantie für eine bestimmte Kapazität.
- [Issue #17](https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/17) berichtet von ausgebrannten Ergebnissen bei Interleaved-/Infographic-Feinabstimmungen unter Q4, während derselbe Berichterstatter Q6 als akzeptabel befand. Bewahren Sie die genaue GGUF-Quantisierung auf, bevor Sie die Adapterqualität diagnostizieren.
- Es existiert eine [Community-Modellkarte für U1.5 GGUF](https://huggingface.co/realrebelai/SenseNova-U1.5-8B_GGUFs), sie ist jedoch keine offizielle Modellkarte und kann die offizielle Warnung zu BF16 mit mehr als 36 GB bzw. Q6 auf 8 GB nicht außer Kraft setzen.

## Stolperfallen {#gotchas}

- **Problem:** Den Drittanbieter-Wrapper als „offizielles SenseNova ComfyUI“ bezeichnen -> **Lösung:** Nennen Sie den Repository-Eigentümer und halten Sie offizielle Registry-Nodes getrennt.
- **Problem:** Das offizielle Paket v0.3.0 neben dem Legacy-Verzeichnis des Drittanbieters installieren -> **Lösung:** Deaktivieren bzw. entfernen Sie zuerst die Legacy-Kopie; doppelte Node-IDs machen die aktive Implementierung von der Scan-Reihenfolge abhängig.
- **Problem:** Das offizielle Paket v0.3.0 auf einer älteren ComfyUI-Laufzeit mit v1-Nodes laden -> **Lösung:** Aktualisieren Sie auf einen Build, der `comfy_api.latest` bereitstellt, oder behalten Sie die fixierte, kompatible Drittanbieter-Oberfläche.
- **Problem:** Annahme, dass Q6 auf eine 8-GB-GPU passt -> **Lösung:** Folgen Sie der offiziellen Warnung und wählen und testen Sie eine niedriger dokumentierte Quantisierung.
- **Problem:** Empfehlung der alten 8-Schritt-LoRA, weil ein historischer Beitrag sie nannte -> **Lösung:** Markieren Sie sie als ersetzt/durchgestrichen und prüfen Sie den aktuellen Adapterpfad.
- **Problem:** Behauptung eines offiziellen LoRA-Trainings aus dem veröffentlichten Full-Fine-Tuning-Code -> **Lösung:** Behandeln Sie beides als getrennte Fähigkeiten und prüfen Sie die FAQ erneut.
- **Problem:** Diagnose der Infografik-Qualität ohne Kenntnis der GGUF-Stufe -> **Lösung:** Dokumentieren Sie Q4/Q6/Q8 und die Adapter-Revision; Issue #17 berichtet über deutlich unterschiedliche Ergebnisse zwischen Q4 und Q6.

## Zeitlicher Status {#temporal-status}

- **Aktuell:** offizielles U1-Repository und Registry-Nodes; aktuelle U1.5-/Quantisierungs-Oberfläche des Wrappers; veröffentlichter Code für Full Fine-Tuning.
- **Ersetzt, aber erhalten:** historische 8-Schritt-LoRA-Anleitung für Infografiken des Wrappers, nun durchgestrichen.
- **Geplant/instabil:** Status des offiziellen LoRA-Trainingscodes.
- **Unzulässige Verallgemeinerung:** vollständiges Q6 auf 8 GB.

## Agent-Kurzbeschreibung {#agent-brief}

Klären Sie zuerst die offiziellen v0.3.0-Nodes gegenüber dem Wrapper `smthemex`, dann U1 gegenüber dem genauen U1.5-Artefakt und der Quantisierung. Fixieren Sie beide Repositories, wenn der Wrapper verwendet wird, und laden Sie niemals beide Node-Implementierungen gemeinsam. Behandeln Sie historische Adapter-Anleitungen als ersetzt, wenn die aktuelle Dokumentation sie durchstreicht. Bewahren Sie die Zuordnung offiziell gegenüber Community und versprechen Sie niemals Kompatibilität mit 8 GB ohne eine exakt gemessene Konfiguration.

## Quellen {#sources}

- Offizielles Repository: https://github.com/OpenSenseNova/SenseNova-U1
- Offizielle chinesische FAQ: https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/FAQ_CN.md
- Offizieller ComfyUI-Registry-Spiegel: https://github.com/OpenSenseNova/ComfyUI-SenseNova-U1
- Offizielle Metadaten zu ComfyUI v0.3.0: https://github.com/OpenSenseNova/ComfyUI-SenseNova-U1/blob/main/pyproject.toml
- Drittanbieter-Wrapper: https://github.com/smthemex/ComfyUI_SenseNova_U1
- Offizielle Projektoberfläche: https://www.sensenova.cn/
- Paper: https://arxiv.org/abs/2605.12500
- Chinesischer Bericht zu VRAM/Offloading: https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/12
- Bericht zum Artefaktvergleich Q4 vs. Q6: https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/17
