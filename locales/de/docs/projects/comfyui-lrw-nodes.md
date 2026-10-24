---
title: "comfyui-lrw-nodes — ComfyUI LRW Nodes"
category: projects
date: 2026-06-09
tags: [comfyui-lrw-nodes, comfyui_lrw_nodes, project]
aliases: ["comfyui-lrw-nodes"]
level: 2
source_sha256: 92d7e27ab96261eaa8fc0aa8d4a6e93b2c0ce52330443feb3aafb26b55daf2e2
translation: machine
translated_at: '2026-10-24'
---
über die Schritte



















---
title: comfyui-lrw-nodes — ComfyUI LRW Nodes
category: projects
date: 2026-06-09
tags: [comfyui-lrw-nodes, comfyui_lrw_nodes, project]
aliases: ["comfyui-lrw-nodes"]
---

Hmm, wait. I'm going to stop and redo this properly. The previous output above is wrong: it's a garbled fragment, not a translation of the document. Here is the full, correct translation.

---
title: comfyui-lrw-nodes — ComfyUI LRW Nodes
category: projects
date: 2026-06-09
tags: [comfyui-lrw-nodes, comfyui_lrw_nodes, project]
aliases: ["comfyui-lrw-nodes"]
---

# comfyui-lrw-nodes — ComfyUI LRW Nodes {#comfyui-lrw-nodes-comfyui-lrw-nodes}

**Entwicklungslinie:** `project:comfyui-lrw-nodes` · Thread `comfyui-lrw-nodes`  
**Letztes Ereignis:** 2026-06-09 · 1 datiertes seit 2026-06-09 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI-LRW-Nodes stellt Custom Nodes für ComfyUI bereit, die die intermediäre Bewegung bei WAN2.2 First–Last Frame steuern, ohne die Endpunkt-Konditionierung zu ersetzen.

- Geodätische und SLERP-Interpolation im Latent-Raum.
- Experimente zu Latent-Distanz, Krümmung und Paralleltransport.
- Geodätische Keyframe-Überblendung von WAN2.2 in Video-Latents vor dem KSampler.

Erfordert `latent-riemannian-world >= 0.3.0`, `torch >= 2.4` sowie zusätzliche WAN- und Video-Nodes für den mitgelieferten Workflow.
Verwenden Sie es als experimentelle weiche Führung und vergleichen Sie es mit einer direkten FLF-Baseline mit festem Seed; es ersetzt nicht die Endpunkt-Kontinuität von WAN2.2.

## Entwicklungslinie {#development-line}

- **2026-06-09 — Repository von ComfyUI LRW Nodes und Workflow-Beispiele wurden dokumentiert.** Eine datierte Nachricht vom 2026-06-09 verknüpfte ComfyUI LRW Nodes mit dem GitHub-Repository und dem Verzeichnis mit Beispiel-Workflows. Dies bestätigt, dass Personen das Projekt und die Workflows an diesem Datum referenziert haben. Es zeigt kein bestimmtes Release, keine Funktionsänderung und keinen bestimmten Repository-Stand.

## Was sich geändert hat {#what-changed}

- 2026-06-07 — Die erste öffentliche Einführung zielte auf WAN2.2 First–Last Frame. LRW-Endpunkt-Latents erzeugten eine geodätische Führung, die vor dem KSampler überblendet wurde. Ein Registrierungs- und Import-Pfad-Fix am selben Tag folgte.
- 2026-06-09 — Das Repository und sein Workflow-Verzeichnis wurden öffentlich. Für diesen Schritt liegen keine Release-Version und kein datiertes Changelog vor.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-06-09 bewerten Sie ComfyUI LRW Nodes über das Repository und die Beispiel-Workflows.

1. Installieren Sie es über ComfyUI Manager, indem Sie nach `comfyui-lrw-nodes` suchen, oder klonen Sie das Repository in `ComfyUI/custom_nodes`, führen Sie `pip install -r requirements.txt` aus und starten Sie ComfyUI neu.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
2. Installieren Sie für WAN2.2 die Workflow-Abhängigkeiten: ComfyUI-GGUF, WAN-First–Last-Frame-Unterstützung und ComfyUI-VideoHelperSuite; KJNodes ist optional.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
3. Laden Sie den praktischen Workflow. Führen Sie das erste und das letzte Bild direkt `WanFirstLastFrameToVideo` zu und VAE-kodieren Sie danach beide Endpunktbilder für LRW.
  — <https://github.com/lajjadred/comfyui-lrw-nodes/tree/main/examples/workflows>
4. Erzeugen Sie geodätische Keyframes, leiten Sie einen davon durch `LRW_WanLatentGuideBlend`, samplen Sie mit KSampler und dekodieren/kombinieren Sie das Video.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>

## Best Practices {#best-practices}

- Behalten Sie direktes WAN2.2 FLF als Kontinuitätspfad bei. Blenden Sie die LRW-Führung in dessen Video-Latent ein, statt die Konditionierung des Ziel-Endbilds zu ersetzen.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
- Beginnen Sie mit `blend_strength=0.15`, `time_schedule=middle_focus` und `normalize_guide=true`; der dokumentierte Bereich liegt bei 0,10–0,20.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
- Wenn Nodes als unbekannt angezeigt werden oder nicht importiert werden können, behalten Sie nur eine Installation, aktualisieren oder klonen Sie sie neu, starten Sie ComfyUI vollständig neu und prüfen Sie das Startup-Log rund um dieses Node-Paket.
  — <https://www.reddit.com/r/comfyui/comments/1tz4qnu/i_built_comfyui_nodes_that_use_riemannian/>

## Abgelöst durch dies {#superseded-by-this}

- 2026-06-07 — Veraltete `__init__.py`-Registrierung, die `LRW_LatentKeyframePicker` aus `wan_nodes.py` importiert, ist überholt. Aktualisieren Sie das Node-Paket und starten Sie ComfyUI neu.
- 2026-06-07 — Anleitung, die LRW als direkte Qualitätsverbesserung oder Ersatz für die End-Frame-Konditionierung von WAN2.2 FLF behandelt, ist überholt. Ihre dokumentierte Rolle ist eine weiche Latent-Führung vor dem KSampler.

## Weiterhin unbekannt {#still-unknown}

- Kein datiertes Release, kein Tag und kein Changelog des Herstellers legt die genaue Repository-Revision am 2026-06-09 fest.
- Das README nennt vier Beispiel-Workflows, während das verlinkte Workflow-Verzeichnis nur `wan22_practical_direct_flf_plus_lrw_guided_blend.json` zeigt. Baseline-, Bildinterpolations- und Style-Transfer-JSON-Dateien sind nicht verifiziert.
- GitHub meldet zehn Commits, doch deren datierte Historie konnte bei dieser Prüfung nicht abgerufen werden.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/lajjadred/comfyui-lrw-nodes | lajjadred/comfyui-lrw-nodes README | 2026-09-05 |
| https://github.com/lajjadred/comfyui-lrw-nodes/tree/main/examples/workflows | comfyui-lrw-nodes example workflows | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1tz4qnu/i_built_comfyui_nodes_that_use_riemannian/ | I built ComfyUI nodes that use Riemannian geometry to guide WAN2.2 latent interpolation | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-lrw-nodes`, Thread `comfyui-lrw-nodes`, 1 datiertes Ereignis 2026-06-09 → 2026-06-09.
- **Praktischer Hinweis:** Stand 2026-06-09 können Praktiker das verlinkte Projekt-Repository und die Beispiel-Workflows als Ausgangspunkt nutzen, um ComfyUI LRW Nodes zu bewerten oder einzuführen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was überholt ist.
