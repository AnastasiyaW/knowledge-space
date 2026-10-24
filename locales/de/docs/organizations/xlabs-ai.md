---
title: "XLabs AI — FLUX-Konditionierung und ComfyUI-Integrationen"
category: organizations
date: 2024-08-21
tags: [flux-conditioning-and-comfyui-integrations, organization, xlabs-ai, xlabs_flux_controlnet, xlabs_flux_ip_adapter]
aliases: ["XLabs AI"]
level: 3
source_sha256: 3998dee9731d8ffbe4018d96e9059fb85240bba983396d73467827175ce04c96
translation: machine
translated_at: '2026-10-24'
---
# XLabs AI — FLUX-Konditionierung und ComfyUI-Integrationen {#xlabs-ai-flux-conditioning-and-comfyui-integrations}

**Entwicklungslinie:** `organization:xlabs-ai` · Thread `flux-conditioning-and-comfyui-integrations`  
**Letztes Ereignis:** 2024-08-21 · 3 datierte seit 2024-08-14 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

XLabs AI veröffentlicht Add-ons für FLUX.1-dev für ComfyUI. Sie bieten strukturelle Steuerung und Steuerung über Referenzbilder, wenn Prompting allein nicht ausreicht.

- ControlNet: Canny-Kanten, Midas-Tiefe und HED-Linienkarten.
- IP-Adapter v2: Konditionierung über Referenzbilder.
- x-flux-comfyui: Nodes und Beispiel-Workflows.

## Entwicklungslinie {#development-line}

- **2024-08-14 — XLabs AI verband eine FLUX-ControlNet-Sammlung mit ComfyUI.** Am 2024-08-14 kombinierte XLabs AI eine FLUX-ControlNet-Sammlung auf Hugging Face mit seiner x-flux-comfyui-Codebasis. Damit entstand ein ControlNet-Integrationspfad für FLUX in ComfyUI. Die Links beschreiben einzelne Modelle und Release Notes nicht näher.
- **2024-08-19 — XLabs AI dokumentierte drei FLUX-ControlNet-v3-Varianten.** Am 2024-08-19 verlinkte XLabs AI die Modellseiten für FLUX ControlNet HED v3, Depth v3 und Canny v3. Die Sammlung wurde dadurch um drei benannte Konditionierungsvarianten erweitert. Die Seiten enthalten keine Benchmarks, keine Versionshistorie und keine Angaben zum Workflow.
- **2024-08-21 — XLabs AI ergänzte einen FLUX-IP-Adapter-Integrationspfad.** Am 2024-08-21 kombinierte XLabs AI eine Modellseite für den FLUX-IP-Adapter, das x-flux-comfyui-Repository und einen OpenArt-Workflow. Damit kam Konditionierung über Referenzbilder neben ControlNet hinzu. Die Belege bestätigen weder Laufzeiteinstellungen noch Betriebsergebnisse.

## Was sich geändert hat {#what-changed}

Am 2024-08-14 ergänzte XLabs AI eine FLUX.1-dev-ControlNet-Sammlung und Custom Nodes für ComfyUI.
Am 2024-08-19 teilte sich die Linie in eigene Checkpoints für Canny v3, Depth v3 und HED v3 für ComfyUI bei 1024×1024.
Am 2024-08-21 ergänzte XLabs AI FLUX IP-Adapter v1 für Konditionierung über Referenzbilder im selben Stack.
Wir haben die Repositories am 2026-09-04 geprüft. Die v1-Karte verweist auf flux-ip-adapter-v2 als neuere Version. Dieses v2-Modell hat mehr Trainingsschritte, behält das Seitenverhältnis bei und ist der aktuelle Ausgangspunkt bei XLabs. Das Custom-Node-Repository zeigt keine Änderungen am Main-Branch nach 2024-10-30.

## Anwendung {#how-to-use-this}

Behandeln Sie ControlNet-Varianten und IP-Adapter-Konditionierung über Referenzbilder ab 2024-08-21 als getrennte Pfade. Starten Sie bei der ComfyUI-Integration, statt einen gemeinsamen Workflow zu erwarten.

1. Installieren Sie x-flux-comfyui über ComfyUI Manager oder klonen Sie es unter ComfyUI/custom_nodes, führen Sie python setup.py aus und starten Sie ComfyUI neu.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>
2. Für strukturelle Konditionierung installieren Sie die Abhängigkeit des ControlNet-Preprocessors. Legen Sie die gewählten Canny-, Depth- oder HED-v3-Gewichte in ComfyUI/models/xlabs/controlnets ab und aktualisieren Sie die Modellliste.
  — <https://github.com/XLabs-AI/x-flux-comfyui>
3. Beginnen Sie mit canny_workflow.json, depth_workflow.json oder hed_workflow.json bei 1024×1024.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
4. Für Referenzbilder verwenden Sie flux-ip-adapter-v2. Legen Sie Clip-L in ComfyUI/models/clip_vision und den Adapter in ComfyUI/models/xlabs/ipadapters ab und verwenden Sie dann Load Flux IPAdapter und Apply Flux IPAdapter.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
5. Passen Sie die IP-Stärke an, wenn die Einhaltung der Referenz schwach ist. Verwenden Sie CUDA für den CLIP-ViT-Loader nur, wenn der VRAM es zulässt.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>

## Best Practices {#best-practices}

- Passen Sie die Konditionierung an die Aufgabe an: Canny für Kanten, Depth für Geometrie und HED für Linienstruktur. Behandeln Sie sie nicht als austauschbare generische ControlNets.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
- Testen Sie ControlNet zuerst bei 1024×1024, der dokumentierten Trainings- und Arbeitsauflösung der v3-Modelle.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3>
- Bauen Sie neue Workflows mit Referenzbildern auf IP-Adapter v2 statt v1 auf. Die v1-Karte kennzeichnet v2 als neuere Version.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter>
- Behandeln Sie IP-Adapter als Tuning-Workflow und nicht als feste Übertragung. Die v2-Karte kennzeichnet ihn weiterhin als Beta und empfiehlt, die IP-Stärke anzupassen, wenn die Ergebnisse schwach sind.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
- Fixieren und testen Sie Custom Nodes vor dem Produktiveinsatz. Die Historie des Main-Branch endet am 2024-10-30, daher garantieren Setup-Anleitungen keine aktuelle Kompatibilität.
  — <https://github.com/XLabs-AI/x-flux-comfyui/commits/main>

## Abgelöst durch {#superseded-by-this}

- 2024-08-14 — Für neue ComfyUI-ControlNet-Arbeiten ist die ursprüngliche Sammlung durch die Checkpoints und Workflows Canny v3, Depth v3 und HED v3 vom 2024-08-19 abgelöst.
- 2024-08-21 — Beginnen Sie keine neuen Arbeiten mit flux-ip-adapter v1. Dessen Karte kennzeichnet flux-ip-adapter-v2 als neuer.
- Installationshinweise aus der Zeit 2024 garantieren keine aktuelle Kompatibilität. Die Historie des x-flux-comfyui-Main-Branch endet am 2024-10-30. Testen Sie es daher gegen Ihre installierte ComfyUI-Version.

## Weiterhin ungeklärt {#still-unknown}

- ControlNet und IP-Adapter sind getrennte Linien von XLabs AI. Die eine konditioniert FLUX mit strukturellen Karten, die andere mit Referenzbildern; keine ersetzt die andere.
- Im chinesischsprachigen Rechercheweg haben wir keine Dokumentation oder Release Notes in vereinfachtem Chinesa von Erstanbietern gefunden.
- Keine heute geprüfte Quelle belegt die Kompatibilität von x-flux-comfyui mit aktuellem ComfyUI oder einem Nachfolger von FLUX.
- Kommerzielle Bedingungen sind weiterhin unbestätigt. Die v2-Seite zeigt Apache-2.0-Metadaten, der Lizenztext beschränkt die Gewichte jedoch auf die FLUX.1-dev Non-Commercial License.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/XLabs-AI/flux-controlnet-collections | XLabs-AI/flux-controlnet-collections · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-hed-v3 | XLabs-AI/flux-controlnet-hed-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3 | XLabs-AI/flux-controlnet-depth-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-canny-v3 | XLabs-AI/flux-controlnet-canny-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-ip-adapter | XLabs-AI/flux-ip-adapter · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-ip-adapter-v2 | XLabs-AI/flux-ip-adapter-v2 · Hugging Face | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui | GitHub - XLabs-AI/x-flux-comfyui | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md | x-flux-comfyui Guide.md · GitHub | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui/commits/main | Commits · XLabs-AI/x-flux-comfyui · GitHub | 2026-09-04 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `organization:xlabs-ai`, Thread `flux-conditioning-and-comfyui-integrations`, 3 datierte Ereignisse 2024-08-14 → 2024-08-21.
- **Praktischer Hinweis:** Behandeln Sie ControlNet-Konditionierung und IP-Adapter-Konditionierung über Referenzbilder ab 2024-08-21 als getrennte Pfade. Starten Sie bei der verlinkten ComfyUI-Integration, statt einen einzigen gemeinsamen Workflow vorauszusetzen.
- **Konfidenz:** mittel. Die datierte Liste der Ablösungen oben markiert, was veraltet ist.
