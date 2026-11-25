---
title: "ComfyUI Flux2Klein Enhancer"
description: "Referenz für gepinnte Workflows zu Referenz-Conditioning und Identitäts-/Detailverbesserung mit FLUX.2 Klein in ComfyUI."
level: 3
source_sha256: 9129e484ed905eeac6bb09060cd39f594e06d2147e8738775282297408330e29
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Flux2Klein Enhancer {#comfyui-flux2klein-enhancer}

`ComfyUI-Flux2Klein-Enhancer` ist ein Custom-Node-Paket von Drittanbietern für ComfyUI zur Referenz-Konditionierung und zum Übertragen von Identität und Details. Es zielt auf das Verhalten von FLUX.2 Klein 9B ab und ist keine offizielle FLUX-Modellveröffentlichung. Der Status wurde am **27.08.2026** gegen das Projekt-Repository verifiziert.

## Aktueller Status {#current-status}

| Eigenschaft | Verifizierter Zustand |
|---|---|
| Repository | `capitan01R/ComfyUI-Flux2Klein-Enhancer` |
| Verifizierte Revision des Default-Branches | `6804643bff9a20926106427ff08d5b1bd2e49861` |
| Lizenz | MIT |
| Primärziel | FLUX.2 Klein 9B |
| Anzahl der Referenzen | Bis zu acht Referenzen im aktuellen Workflow |
| Neutrale Regler | Exakte neutrale Werte sind als Pass-through vorgesehen |
| Unabhängiger Identitäts-Benchmark | Im begrenzten Recherchedurchlauf nicht verfügbar |

Das Paket ist über die in der ersten Meldung beschriebene Form mit zwei Nodes hinausgewachsen. Aktuelle Workflow-Konzepte umfassen Referenz-Encoding, `Multi ReferenceLatent`, `Identity Feature Transfer Final` und optionale Masken.

## Entwicklungsverlauf {#development-history}

| Datum | Ereignis | Zeitlicher Status |
|---|---|---|
| 07.04.2026 | Erstes Enhancer-Paket/erster Bericht | Historische Grundlage |
| 24.06.2026 | Erweiterter Workflow/erweitertes Paket gemeldet | Aktuelles Nachfolgeereignis |
| 11.07.2026 | Datum der verifizierten Repository-Revision | Hier verwendeter aktueller Repository-Stand |

Der ursprüngliche Nachrichtentext bleibt unverändert. Spätere Paketerweiterungen und der aktuelle Repository-Stand werden als Nachfolgeknoten angefügt.

## Installation und Pinning {#installation-and-pinning}

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer.git
cd ComfyUI-Flux2Klein-Enhancer
git checkout 6804643bff9a20926106427ff08d5b1bd2e49861
git rev-parse HEAD
```

ComfyUI neu starten und einen Workflow laden, der zur gepinnten Revision passt. Die Workflow-JSON zusammen mit dem Laufprotokoll aufbewahren; Node-Namen und Sockets können sich zwischen Revisionen ändern.

## Evaluierungsprotokoll {#evaluation-protocol}

Einen Vergleich mit identischem Seed durchführen:

```yaml
comfyui_revision: <exact-revision>
plugin_revision: 6804643bff9a20926106427ff08d5b1bd2e49861
model: <exact-flux2-klein-artifact>
reference_count: <1-to-8>
reference_order: <ordered-list>
masks: <file-hashes-or-none>
seed: <integer>
dimensions: <width>x<height>
steps: <integer>
enhancer_controls: <all-values>
gpu_and_vram: <exact-device>
```

Einen Baseline-Workflow und einen Enhancer-Workflow vergleichen, dabei Modell, Prompt, Seed, Schritte, Auflösung und Sampler konstant halten. Identitätsähnlichkeit, ungewollte Detailübertragung, Prompt-Treue und maximalen VRAM-Bedarf erfassen. Neutrale Einstellungen sollten als exakte Pass-through-Invariante getestet werden.

## Grenzen der Evidenz {#evidence-boundaries}

- Das Repository belegt die Identität der Implementierung, die Node-Oberfläche, das Zielmodell und die Lizenz.
- „Kein LoRA nötig“, exakte Identitätserhaltung, Qualitätsgewinne und Verhalten bei wenig VRAM sind Aussagen von Autoren bzw. der Community, bis sie unabhängig gemessen wurden.
- Kleinere Conditioning-Modelle werden von der Implementierung möglicherweise erkannt, die Hook-Zeitpläne und die dokumentierte Zielsetzung konzentrieren sich jedoch auf Klein 9B.
- Im ersten begrenzten Durchlauf wurde keine qualifizierte chinesischsprachige Community-Quelle aufgenommen.

## Community- und Issue-Belege {#community-and-issue-evidence}

- [Issue #35](https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/35) zeigte, dass `Identity Feature Transfer Final` über `IS_CHANGED` den Wert `NaN` zurückgab, wodurch nachgelagerte Läufe mit festem Seed neu berechnet wurden. Der Maintainer hat am 12.06.2026 einen Fix gemergt. Dies ist ein historischer Fehler; Revisionen nach diesem Merge sollten die Umgehungslösung nicht übernehmen.
- [Issue #41](https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/41) meldet Identitätsänderungen nach ComfyUI `v0.28.0` mit zwei maskierten Referenzen. Der Melder isolierte `zero_unmasked_tokens` und verwendete `focus_only` als Workaround; das Issue blieb offen. Bei der Reproduktion ComfyUI-Version, Mask-Verdrahtung, Preset und Plugin-Revision festhalten.
- Der [Community-Showcase-Thread](https://www.reddit.com/r/StableDiffusion/comments/1t1mvyh/flux2klein_exact_preservation_no_lora_needed/) eignet sich, um die Methode kennenzulernen, doch „exakte Erhaltung“ bleibt eine Aussage von Autoren bzw. der Community ohne unabhängige Metrik.

## Stolperfallen {#gotchas}

- **Problem:** Das Plugin wird als offizielle FLUX-Funktion behandelt -> **Lösung:** Als Custom-Node-Paket eines Drittanbieters kennzeichnen und dessen Commit pinnen.
- **Problem:** Identitätserhaltung wird aus einem Showcase abgeleitet -> **Lösung:** Vergleiche mit Baseline und Enhancer bei gleichem Seed mit einer expliziten Bewertungsmetrik durchführen.
- **Problem:** Ein alter Workflow mit zwei Nodes wird mit dem erweiterten Paket geladen -> **Lösung:** Workflow-JSON an die exakte Plugin-Revision anpassen.
- **Problem:** Die Annahme, dass Unterstützung für kleinere Conditioning-Modelle volle 9B-Parität bedeutet -> **Lösung:** Exakten Modellpfad und Zeitpläne lokal überprüfen.
- **Problem:** `zero_unmasked_tokens` wird über ComfyUI-Versionen hinweg unverändert verwendet -> **Lösung:** mit dem gepinnten Mask-/Preset-Setup reproduzieren; `focus_only` ist ein gemeldeter Workaround für v0.28, kein universeller Standard.

## Zeitlicher Status {#temporal-status}

- **Aktuell:** erweiterter Multi-Referenz-Workflow in der gepinnten Revision vom Juli 2026.
- **Historisch:** ursprüngliche Beschreibung mit zwei Nodes vom April.
- **Gemeldet, nicht unabhängig verifiziert:** exakte Erhaltung, Ersetzung ohne LoRA, Qualitätsgewinn und Leistung bei geringem Speicherbedarf.

## Agent-Kurzfassung {#agent-brief}

Vor der Fehlersuche Plugin, ComfyUI, Workflow-JSON und Modell pinnen. Repository-Fakten getrennt von Wirksamkeitsbehauptungen aus Showcases und Community-Beiträgen betrachten. Für Aussagen zu Identität oder Details eine kontrollierte Baseline verlangen. Die ursprüngliche Meldung als Historie bewahren und den aktuellen Paketstand als Endpunkt anfügen, statt sie umzuschreiben.

## Quellen {#sources}

- Projekt-Repository: https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer
- Community-Diskussionsbereich: https://www.reddit.com/r/StableDiffusion/comments/1t1mvyh/flux2klein_exact_preservation_no_lora_needed/
- Behobener Cache-Invalidierungsfehler: https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/35
- Offenes Mask-Verhalten in ComfyUI v0.28: https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/41
