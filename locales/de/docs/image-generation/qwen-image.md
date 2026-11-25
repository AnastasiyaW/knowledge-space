---
title: "Qwen-Image"
description: "Versionsbezogene Referenz für Qwen-Image-Generierung und -Bearbeitung, die Checkpoints 2511/2512 sowie die separate Service-Oberfläche von Qwen-Image 2.0."
level: 3
source_sha256: d1f97016e48185c7fccd93691baf57684ffc3d729c310339f9c4b45f110f631d
translation: machine
translated_at: '2026-10-24'
---
# Qwen-Image {#qwen-image}

Qwen-Image ist eine Projektfamilie mit getrennten Checkpoints für Generierung und Bearbeitung. Diese Seite unterscheidet offene lokale Artefakte von späteren Ankündigungen gehosteter Produkte. Der Status wurde am **27.08.2026** anhand erstparteilicher Quellen überprüft.

## Aktuelle Artefaktübersicht {#current-artifact-map}

| Artefakt | Status laut Erstquelle | Verwendung |
|---|---|---|
| Qwen-Image | Im offiziellen Repository am 04.08.2025 veröffentlicht | Basis für Text-zu-Bild-Generierung |
| Qwen-Image-Edit | Veröffentlicht am 18.08.2025 | Anweisungsbasierte Bildbearbeitung |
| Qwen-Image-Edit-2511 | Gewichte am 23.12.2025 angekündigt | Späterer Bearbeitungs-Checkpoint |
| Qwen-Image-2512 | Gewichte am 31.12.2025 angekündigt | Späterer Generierungs-Checkpoint |
| Qwen-Image 2.0 | Am 10.02.2026 über den offiziellen Blog bzw. die Qwen-Chat-Oberfläche angekündigt | Gehostetes/aktuelles Produkt zur Generierung; keine offenen 2.0-Gewichte im offiziellen Repository gefunden |
| Qwen-Image 2.0 Pro | Als gehostete Produkt-/Nachrichtenbezeichnung im Laufe des Jahres 2026 beobachtet | Nicht als Alias für offene 2512-Gewichte behandeln |

Der sichere Standard für einen lokalen, offenen Generierungs-Workflow ist das offizielle **2512**-Beispiel. Der sichere Standard für einen lokalen, offenen Bearbeitungs-Workflow ist das offizielle **Edit-2511**-Beispiel. Vor der Annahme, dass Qwen-Image 2.0 herunterladbar ist, sollte das Repository erneut geprüft werden.

## Entwicklungsverlauf {#development-history}

| Datum | Strang | Ereignis | Zeitlicher Status |
|---|---|---|---|
| 04.08.2025 | generation | Erste Veröffentlichung von Qwen-Image | Für aktuelle lokale Beispiele durch 2512 abgelöst |
| 18.08.2025 | editing | Veröffentlichung von Qwen-Image-Edit | Für aktuelle lokale Beispiele durch Edit-2511 abgelöst |
| 23.12.2025 | editing | Gewichte von Edit-2511 veröffentlicht | Aktueller offener Bearbeitungs-Checkpoint in den offiziellen Beispielen |
| 31.12.2025 | generation | Gewichte von 2512 veröffentlicht | Aktueller offener Generierungs-Checkpoint in den offiziellen Beispielen |
| 10.02.2026 | generation/product | Qwen-Image 2.0 angekündigt | Aktueller Zweig gehosteter Produkte; Status offener Artefakte nicht verifiziert |
| 26.04.2026 | generation/product | Bericht zu Qwen-Image 2.0 Pro beobachtet | Späteres Produktereignis, kein Beleg für offene Gewichte |

Generierung und Bearbeitung sind verwandte Projektzweige und keine einzelne Vorgängerkette. Beide Verläufe sollten erhalten bleiben. Beim Aufbau eines Nachrichtengraphen sollten nur Ereignisse innerhalb desselben Zweigs miteinander verknüpft werden.

## Praktische Anwendung {#practical-use}

### Lokale Generierung {#local-generation}

```bash
git clone https://github.com/QwenLM/Qwen-Image.git
cd Qwen-Image
git rev-parse HEAD
```

Anschließend das 2512-Generierungsbeispiel aus dieser fixierten Revision verwenden. Modell-ID, Repository-Revision, Diffusers-/Laufzeitversionen, dtype, GPU, Seed, Abmessungen, Schrittzahl sowie eventuelle Quantisierung oder Offloading dokumentieren.

### Lokale Bearbeitung {#local-editing}

Das Edit-2511-Beispiel aus demselben fixierten Repository verwenden. Ausgangsbild und Bearbeitungsanweisung gemeinsam im Ausführungsprotokoll festhalten. Bei Bearbeitung mit mehreren Bildern auch die Eingabereihenfolge dokumentieren, da positionsbezogene Referenzen die Interpretation beeinflussen können.

### Gehostetes 2.0 {#hosted-20}

Die aktuelle erstparteiliche Dokumentation von Qwen Chat/API verwenden und den genauen Endpunkt bzw. das genaue Modell nennen. Gehostete Latenz, Grenzwerte oder Ausgabeverhalten nicht als Eigenschaften des lokalen 2512-Checkpoints darstellen.

## Laufzeit- und Integrationsoberfläche {#runtime-and-integration-surface}

Das offizielle Repository dokumentiert Integrationspfade für Diffusers und nennt Unterstützung in LightX2V, vLLM-Omni und SGLang. Dabei handelt es sich um getrennte Laufzeitumgebungen mit unterschiedlichen Batching-, Quantisierungs- und API-Verträgen.

Für jede Bereitstellung festhalten:

```yaml
artifact: Qwen-Image-2512-or-Qwen-Image-Edit-2511
source_revision: <40-character-commit>
runtime: <diffusers-or-serving-runtime>
runtime_version: <exact-version>
dtype: <bf16-fp16-fp8-int8-other>
gpu: <exact-model-and-vram>
resolution: <width>x<height>
steps: <integer>
seed: <integer>
```

Im begrenzten Rechercheschritt wurde keine aktuelle, versionierte und erstparteiliche VRAM-/Latenz-Übersicht akzeptiert. Den lokalen Ressourcenverbrauch messen, statt eine Community-Angabe zu übernehmen.

## Grenzen der Belege {#evidence-boundaries}

- Das offizielle Repository ist maßgeblich für herunterladbare Artefakte und lokale Beispiele.
- Der offizielle 2.0-Blog ist maßgeblich für die Ankündigung, belegt aber allein keinen offenen Checkpoint.
- Die chinesischsprachige erstparteiliche API-Dokumentation ist nützlich für das Verhalten gehosteter Bearbeitung; sie belegt keine Kompatibilität mit dem lokalen 2512.
- Community-Beispiele eignen sich zum Auffinden von Fehlern, nicht zur Bestimmung der Artefaktidentität oder allgemeingültiger Einstellungen.

## Community-Berichte {#community-reports}

- [Issue #26](https://github.com/QwenLM/Qwen-Image/issues/26) dokumentiert einen ersten Diffusers-Lauf von Qwen-Image, der 44,24 GiB belegte und auf einer nominell 48-GB-Karte fehlschlug. Community-Antworten nennen `enable_model_cpu_offload()` als funktionierende Speicherreduzierung mit Geschwindigkeitseinbuße; VAE-Tiling allein überschritt bei einem Berichtenden weiterhin 50 GB. Diese Messungen stammen vom Basisartefakt von 2025, nicht von 2512/Edit-2511.
- [Issue #54](https://github.com/QwenLM/Qwen-Image/issues/54) vergleicht einen offiziellen Infografik-Prompt über gehostetes Qwen, Diffusers und ComfyUI BF16. Mehrere Nutzer berichteten, dass der Standard von ComfyUI mit 20 Schritten hinter dem 50-Schritte-Beispiel des Repositorys zurückblieb; 50 Schritte verbesserten die Lesbarkeit, garantierten aber keinen prompt-perfekten Text. Ausgaben von Diffusers und ComfyUI waren auch bei nominell ähnlichen Gewichten nicht austauschbar.
- Die betriebliche Lehre lautet, Laufzeitumgebung und Schrittzahl bei Vergleichen festzuhalten. Ein gehostetes Beispiel nicht als Garantie für den lokalen Checkpoint darstellen.

## Fallstricke {#gotchas}

- **Problem:** Jedes Artefakt als „Qwen-Image 2.0“ bezeichnen -> **Lösung:** Die genaue Modell-ID beibehalten: Basis, Edit, Edit-2511, 2512 oder gehostetes 2.0/2.0 Pro.
- **Problem:** Annahme, dass ein Blog- oder Qwen-Chat-Start offene Gewichte bedeutet -> **Lösung:** Vor der Beschreibung von 2.0 als lokal herunterladbar ein erstparteiliches Repository- bzw. Model-Card-Artefakt verlangen.
- **Problem:** Bearbeitungsereignisse als Vorgänger von Generierungsereignissen verknüpfen -> **Lösung:** `generation`- und `editing`-Entwicklungsstränge getrennt führen.
- **Problem:** Community-VRAM- oder Geschwindigkeitswerte als allgemeingültig veröffentlichen -> **Lösung:** Laufzeitumgebung, dtype, Quantisierung, Abmessungen, Schrittzahl und GPU festlegen und dann messen.
- **Problem:** Einen 20-Schritte-ComfyUI-Lauf mit dem 50-Schritte-Diffusers-Beispiel des Repositorys vergleichen -> **Lösung:** Zuerst die Laufzeitsteuerung angleichen und trotzdem mit backendspezifischen Ausgabeunterschieden rechnen.

## Zeitlicher Status {#temporal-status}

- **Aktuell:** lokales 2512-Generierungsbeispiel; lokales Edit-2511-Bearbeitungsbeispiel; gehostete Produktoberfläche Qwen-Image 2.0.
- **Abgelöst, aber beibehalten:** ursprüngliche Basis-Generierungs- und Bearbeitungsbeispiele von 2025, sofern es spätere offizielle Checkpoints gibt.
- **Unbekannt:** Verfügbarkeit, Lizenz und lokaler Laufzeitvertrag eines offenen Qwen-Image-2.0-Checkpoints.

## Hinweise für Agenten {#agent-brief}

Vor jeder Empfehlung die Absicht der Nutzerin bzw. des Nutzers auf `local generation`, `local editing` oder `hosted 2.0` abbilden. Für lokale Arbeit das aktuelle offizielle Repository abrufen und eine unveränderliche Revision sowie die genaue Modell-ID zitieren. Für gehostete Arbeit die aktuelle Endpunkt-Dokumentation zitieren. „2.0 Pro“ niemals ohne primären Beleg auf `2512` abbilden. Ältere Ereignisse mit ihrem zeitlichen Status zurückgeben, statt sie zu löschen.

## Quellen {#sources}

- Offizielles Repository: https://github.com/QwenLM/Qwen-Image
- Ankündigung von Qwen-Image 2.0: https://qwen.ai/blog?id=qwen-image-2.0
- Chinesischsprachige Dokumentation zur gehosteten Bildbearbeitung: https://docs.qwencloud.com/developer-guides/image-generation/image-editing
- Forschungsarbeit: https://arxiv.org/abs/2605.10730
- Diskussion zum Speicherbedarf des Basismodells (zh-CN/EN): https://github.com/QwenLM/Qwen-Image/issues/26
- Diskussion zur Reproduktion gehostet/Diffusers/ComfyUI: https://github.com/QwenLM/Qwen-Image/issues/54
