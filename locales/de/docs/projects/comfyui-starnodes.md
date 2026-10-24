---
title: "ComfyUI_StarNodes"
category: projects
date: 2026-07-18
tags: [comfyui-starnodes, project]
aliases: ["ComfyUI_StarNodes"]
level: 3
source_sha256: 91b9704ed78359f74eed1503cf5d90ec1b00e3469a586a1557f6d0be38d17364
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI_StarNodes {#comfyui_starnodes}

**Entwicklungslinie:** `project:comfyui-starnodes` · Thread `comfyui-starnodes`  
**Letztes Ereignis:** 2026-07-18 · 1 datiertes seit 2026-07-18 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI_StarNodes ist eine MIT-lizenzierte Suite benutzerdefinierter Nodes für ComfyUI-Anwender, die Starter-Workflows, Sampling, Bildverarbeitung und Video in einer Erweiterung benötigen.

- Starter-Einstellungen für Flux, SDXL und Qwen
- Sampler, LoRAs, Inpainting, Upscaling, PSD-Speicherung, Wildcards und Debugging-Werkzeuge
- Video-Werkzeuge, einschließlich LTX-Workflows

Das README nennt 100 Nodes, `pyproject.toml` führt die Version 2.7.1 auf, und GitHub Releases enthält keine Releases. Das Paket deckt ein breites Feld ab, reproduzierbare Workflows erfordern jedoch das Festlegen (Pinnen) einer Revision und das separate Testen einzelner Nodes.

## Entwicklungslinie {#development-line}

- **2026-07-18 — Auf das GitHub-Repository von ComfyUI_StarNodes wurde verwiesen.** Am 2026-07-18 haben wir auf den Link zum GitHub-Repository von ComfyUI_StarNodes verwiesen. Die verfügbaren Belege identifizieren das Projekt-Repository, belegen aber weder ein Release, eine Funktionsänderung, eine Version noch den Installationsstatus. Dieser Verlaufseintrag vermerkt nur den datierten Repository-Verweis.

## Was sich geändert hat {#what-changed}

- **2024-11-20** — v1.7.0 übernahm verifizierte StarBetaNodes in das Hauptpaket, einschließlich Qwen/WAN-Bearbeitung und Hilfsfunktionen.
- **2026-04-10** — v2.0.0 ergänzte neun integrierte Nodes für LTX-Video und ACE Step, entfernte acht Legacy-Nodes und reduzierte die Abhängigkeiten.
- **2026-07-10** — Ein öffentlicher Beitrag behauptete v2.1.1 mit einem 360-Grad-Panorama-Viewer und einem aktualisierten Workflow; Commit- oder Registry-Artefakte fehlen.
- **2026-07-18** — Für dieses Datum ist nur der Repository-Link dokumentiert, ohne bestätigte Änderung, Version oder SHA.
- **2026-07-19** — Ein öffentlicher Beitrag behauptete Updates v2.3.6 und v2.3.7 mit Leistungsverbesserungen, neuen Nodes, UI-Aktualisierungen und Kompatibilitätskorrekturen; primäre Release-Artefakte fehlen.

## So verwenden Sie dies {#how-to-use-this}

Behandeln Sie das verlinkte ComfyUI_StarNodes-Repository als Projektquelle, die zum Stand 2026-07-18 zu prüfen ist, nicht als Nachweis eines verifizierten Releases oder eines Installationsverfahrens.

1. Suchen Sie in ComfyUI Manager nach `Starnodes`, installieren Sie das Paket und starten Sie ComfyUI neu. Wird das Paket nicht aufgelistet, fahren Sie mit der manuellen Installation fort.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>
2. Für die manuelle Installation klonen Sie das Repository in `ComfyUI/custom_nodes`, installieren `requirements.txt` und starten ComfyUI neu.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>
3. Installieren Sie die Abhängigkeiten direkt in der Python-Umgebung des aktiven ComfyUI-Setups und prüfen Sie nach dem Neustart das Startup-Log auf Importfehler.
  — <https://docs.comfy.org/installation/install_custom_node>
4. Suchen Sie Nodes nach `star` und beginnen Sie mit einem passenden Beispiel: Start(t) Settings, um einen Graphen zu starten, Save Image+ oder PSD Saver für die Ausgabe sowie Star Wildcards Advanced für Prompt-Daten.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Prüfen Sie das Repository und seine Anforderungen vor der Installation. ComfyUI empfiehlt, benutzerdefinierte Nodes nur aus vertrauenswürdigen Quellen zu installieren und zu verstehen, was sie tun.
  — <https://docs.comfy.org/installation/install_custom_node>
- Speichern Sie vor einem Update einen Snapshot, damit Manager das Node-Setup nach dem nächsten Start wiederherstellen kann.
  — <https://docs.comfy.org/manager/legacy-ui>
- Verwenden Sie für Produktions-Graphen eine paketierte Version statt Nightly, da die Manager-Dokumentation Nightly als weniger stabil kennzeichnet.
  — <https://docs.comfy.org/manager/legacy-ui>
- Beginnen Sie mit dem mitgelieferten JSON-Beispiel für die Zielaufgabe, anstatt den gesamten Produktions-Graphen auf einmal umzuziehen.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>

## Hiermit ersetzt {#superseded-by-this}

- :{
- claim
- obsolete_since
- source_url
- claim

## Noch unbekannt {#still-unknown}

- Keine zweite datierte Primärquelle verknüpft den 2026-07-18 mit einer bestimmten Änderung, einem Commit, Tag oder einer Version.
- Der Wert 2.7.1 in `pyproject.toml` ist eine Manifest-Version, kein bestätigtes GitHub-Release und keine verifizierte Veröffentlichung in einer Registry.
- Die zugängliche GitHub-Historie endet mit einem Snapshot vom April 2026, während aktuelle Repository-Dateien spätere Metadaten tragen; die genaue Commit-Chronologie nach April ist nicht bestätigt.
- Die Beiträge vom 10. und 19. Juli verweisen auf dasselbe Repository, unabhängige Primärartefakte bestätigen jedoch weder deren Urheberschaft noch die behaupteten Versionen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/Starnodes2024/ComfyUI_StarNodes | ComfyUI_StarNodes-Repository | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md | ComfyUI_StarNodes README | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/pyproject.toml | ComfyUI_StarNodes pyproject.toml | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/CHANGELOG.md | ComfyUI_StarNodes-Changelog | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/commits/main | ComfyUI_StarNodes-Commit-Historie | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/releases | ComfyUI_StarNodes-Releases | 2026-09-06 |
| https://www.reddit.com/r/comfyui/comments/1usx5f3/starnodes_211_panorama_update/ | Starnodes 2.1.1 Panorama Update | 2026-09-06 |
| https://www.reddit.com/r/comfyui/comments/1v0u5mt/starnodes_double_feature_updates_v236_v237_are/ | STARNODES Double Feature: Updates v2.3.6 & v2.3.7 are LIVE! | 2026-09-06 |
| https://docs.comfy.org/installation/install_custom_node | So installieren Sie benutzerdefinierte Nodes in ComfyUI | 2026-09-06 |
| https://docs.comfy.org/manager/legacy-ui | Verwalten benutzerdefinierter Nodes mit ComfyUI-Manager (Legacy-UI) | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-starnodes`, Thread `comfyui-starnodes`, 1 datiertes Ereignis 2026-07-18 → 2026-07-18.
- **Praktischer Hinweis:** Zum Stand 2026-07-18 sollten Anwender das verlinkte ComfyUI_StarNodes-Repository als zu untersuchende Projektquelle behandeln, nicht als Nachweis eines verifizierten Releases oder eines Installationsverfahrens.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
