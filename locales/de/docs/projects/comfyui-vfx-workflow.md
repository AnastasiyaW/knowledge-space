---
title: "heydoughogan ComfyUI VFX Workflow — ComfyUI-VFX-Passes"
category: projects
date: 2026-06-12
tags: [comfyui-vfx-passes, comfyui-vfx-workflow, project]
aliases: ["heydoughogan ComfyUI VFX Workflow"]
level: 2
source_sha256: f2619a3c10cd3836bac86198d670c0137c36b6a93afeec8d3557329749b1f577
translation: machine
translated_at: '2026-10-24'
---
# heydoughogan ComfyUI VFX Workflow — ComfyUI-VFX-Passes {#heydoughogan-comfyui-vfx-workflow-comfyui-vfx-passes}

**Entwicklungslinie:** `project:comfyui-vfx-workflow` · Thread `comfyui-vfx-passes`  
**Letztes Ereignis:** 2026-06-12 · 1 datiertes seit 2026-06-12 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

VFX Utilities ist ein ComfyUI-Workflow von Doug Hogan für Compositor und VFX-Artists. Er erzeugt Passes für Relighting, Compositing und Look-Development, ohne separates CG-Rendering.

- Alpha- und Matte-Extraktion mit RMBG und SAM3
- Textprompt- und Punktsegmentierung
- Gesichtssegmentierung
- Erzeugung von Tiefen- und Normal-Passes

Die Karte stellt derzeit 1 herunterladbaren JSON-Graphen bereit.

## Entwicklungslinie {#development-line}

- **2026-06-12 — Datierte Comfy-Workflow-Referenz für VFX-Passes.** Der Graph kombiniert Quellvideo-Import, RMBG, SAM3-Prompts und -Punkte, Gesichtssegmentierung, Tiefe und Normals in 1 ComfyUI-Graphen. Die aktuelle Karte listet Alpha-, Tiefen- und Normal-Maps als Ausgaben. Zum Stand des Graphen am Veröffentlichungstag liegt uns keine Bestätigung vor.

## Was sich geändert hat {#what-changed}

2026-06-12 — Veröffentlichung des VFX-Utilities-Workflows. Er kombiniert Quellvideo-Import, RMBG, SAM3-Prompts und -Punkte, Gesichtssegmentierung, Tiefe und Normals in 1 ComfyUI-Graphen. Die aktuelle Karte listet Alpha-, Tiefen- und Normal-Maps als Ausgaben. Die historische Version des Graphen zum Veröffentlichungsdatum ist nicht bestätigt.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-06-12 sollten Sie den verlinkten Comfy-Workflow als Referenz behandeln, die für VFX-Pass-Arbeiten manuell zu prüfen ist, nicht als verifiziertes oder vollständig dokumentiertes Rezept.

1. Öffnen Sie die Karte und laden Sie das Workflow-JSON herunter.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>
2. Laden Sie das JSON in ComfyUI, stellen Sie eine Bild- oder Videoplatte bereit und setzen Sie Prompt-Text oder Segmentierungspunkte.
  — <https://comfy.org/workflows/download/be0889296f65.json?filename=be0889296f65>
3. Führen Sie die benötigten Pfade aus und verwenden Sie die Alpha-, Tiefen- und Normal-Ausgaben als Passes für Compositing, Relighting oder Look-Development.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>

## Hiermit ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Das Ereignis nennt eine Konto-URL für heydoughogan, die wir nicht verifizieren konnten. Der bestätigte Kartenautor ist Doug Hogan (@doughogan).
- Die Karte zeigt das aktuelle JSON mit einem relativen Erstellungsdatum, daher ist das genaue Node- und Modell-Setup vom 2026-06-12 nicht bestätigt.
- Wir haben keine datierte Primärquelle gefunden, die spätere Änderungen an diesem Workflow bestätigt, daher werden keine neuen datierten Ereignisse ergänzt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://comfy.org/workflows/be0889296f65-be0889296f65/ | VFX Utilities - ComfyUI Workflow | 2026-09-05 |
| https://comfy.org/workflows/download/be0889296f65.json?filename=be0889296f65 | be0889296f65 workflow JSON | 2026-09-05 |
| https://comfy.org/workflows/doughogan/ | Doug Hogan - ComfyUI Workflow Templates | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-vfx-workflow`, Thread `comfyui-vfx-passes`, 1 datiertes Ereignis 2026-06-12 → 2026-06-12.
- **Praktischer Hinweis:** Stand 2026-06-12 sollten Praktiker den verlinkten Comfy-Workflow als Referenz behandeln, die für VFX-Pass-Arbeiten manuell zu prüfen ist, nicht als verifiziertes oder vollständig dokumentiertes Rezept.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
