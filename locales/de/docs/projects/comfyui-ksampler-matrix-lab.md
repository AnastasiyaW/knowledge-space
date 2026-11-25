---
title: "ComfyUI KSampler Matrix Lab — Repository-Referenz"
category: projects
date: 2026-06-05
tags: [comfyui-ksampler-matrix-lab, comfyui_ksampler_matrix_lab, project, repository-reference]
aliases: ["ComfyUI KSampler Matrix Lab"]
level: 2
source_sha256: 58db1761192ab2ed7c2383768c0af73b5559958ebece342911c2d0d272268048
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI KSampler Matrix Lab — Repository-Referenz {#comfyui-ksampler-matrix-lab-repository-reference}

**Entwicklungslinie:** `project:comfyui-ksampler-matrix-lab` · Thread `repository-reference`  
**Letztes Ereignis:** 2026-06-05 · 1 datiertes Ereignis seit 2026-06-05 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI KSampler Matrix Lab — zwei ComfyUI-Nodes für Künstler und Modellevaluatoren: KSampler Matrix Lab vergleicht Sampler-/Scheduler-Kombinationen, Model Matrix Lab vergleicht installierte Checkpoints. Grenzen: bis zu 9 Sampler-Slots, 9 Scheduler-Slots und 20 Modell-Slots; die Generierung läuft sequenziell. Fazit: brauchbar für kontrollierte visuelle Tests, die Kompatibilität hängt jedoch weiterhin vom lokalen ComfyUI-Build, den Modellen und Custom Nodes ab.

## Entwicklungslinie {#development-line}

- **2026-06-05 — Repository von ComfyUI KSampler Matrix Lab referenziert.** Am 2026-06-05 wurde diese Entwicklungslinie mit dem GitHub-Repository für ComfyUI KSampler Matrix Lab verknüpft. Der datierte Link belegt eine öffentliche Repository-Referenz für das Projekt, Inhalte des Beitrags, Repository-Stand, Funktionsumfang und Release-Status wurden jedoch nicht recherchiert.

## Was sich geändert hat {#what-changed}

2026-06-05 — die Erweiterung war als Custom-Node-Paket für beschriftete Sampler-/Scheduler-Vergleichsraster verfügbar; der öffentliche Start des Erstellers ist auf 2026-06-04 datiert und beschrieb das Verhalten bei gleichem Seed, inkrementellem Seed, Metadaten-Header und Fehlerzellen.

## Anwendung {#how-to-use-this}

Stand 2026-06-05 sollten Anwender das verlinkte Repository prüfen, bevor sie ComfyUI KSampler Matrix Lab als einsatzfähige Workflow-Komponente betrachten; Installation, Verhalten und Reifegrad sind nicht verifiziert.

1. Das Repository nach `ComfyUI/custom_nodes` klonen und ComfyUI neu starten.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
2. `KSampler Matrix Lab` oder `Model Matrix Lab` aus der Erweiterungskategorie hinzufügen und mit einem normalen Generierungs-Workflow verbinden.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
3. Den einzelnen `IMAGE`-Ausgang des Nodes mit Preview Image oder Save Image verbinden; optional den mitgelieferten Workflow als JSON laden.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>

## Best Practices {#best-practices}

- Prompt, Modell, Latent und Seed konstant halten, wenn Sampler- und Scheduler-Einstellungen verglichen werden; inkrementellen Seed pro Zelle nur verwenden, wenn zusätzlich Variation getestet werden soll.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
- Die Matrix mit `max_combinations` begrenzen; vor einer Erhöhung des Limits zuerst die ausgewählten Sampler oder Scheduler reduzieren.
  — <https://www.runcomfy.com/comfyui-nodes/ComfyUI-KSampler-Matrix-Lab/k-sampler-matrix-lab>
- Beschriftungen und Laufheader aktiviert lassen, wenn Ergebnisse geprüft oder geteilt werden, und Fehlerzellen prüfen, wenn Fortsetzung aktiviert ist.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Das Repository hat keine getaggten Releases, und die zugängliche Übersicht des Erstanbieters enthält nach der ursprünglichen Veröffentlichung im Juni 2026 kein verlässliches, datiertes Commit-für-Commit-Änderungsprotokoll.
- Ein unabhängiger Laufzeittest auf einer aktuellen lokalen ComfyUI-Installation war nicht verfügbar; die aktuelle Kompatibilität ist daher dokumentiert, aber nicht durch Ausführung verifiziert.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab | GitHub — btitkin/ComfyUI-KSampler-Matrix-Lab | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1twjm31/comfyui_node_to_compare_multiple_samplers_and/ | ComfyUI-Node zum gleichzeitigen Vergleich mehrerer Sampler und Scheduler | 2026-09-05 |
| https://www.runcomfy.com/comfyui-nodes/ComfyUI-KSampler-Matrix-Lab/k-sampler-matrix-lab | KSampler Matrix Lab | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:comfyui-ksampler-matrix-lab`, Thread `repository-reference`, 1 datiertes Ereignis 2026-06-05 → 2026-06-05.
- **Praxishinweis:** Stand 2026-06-05 sollten Anwender das verlinkte Repository prüfen, bevor sie ComfyUI KSampler Matrix Lab als einsatzfähige Workflow-Komponente betrachten; Installation, Verhalten und Reifegrad sind nicht verifiziert.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
