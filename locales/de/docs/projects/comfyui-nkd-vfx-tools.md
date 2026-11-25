---
title: "ComfyUI-NKD-VFX-Tools"
category: projects

tags: [comfyui-nkd-vfx-tools, comfyui-nkd-vfx-tools-development, comfyui_nkd_vfx_tools, project]
aliases: ["ComfyUI-NKD-VFX-Tools"]
level: 2
source_sha256: 1a6d8b7968fb51bd60d2abdef3dda72a4d8ce039f463a7e0bf067e54b0222d6b
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI-NKD-VFX-Tools {#comfyui-nkd-vfx-tools}

**Entwicklungslinie:** `project:comfyui-nkd-vfx-tools` · Thread `comfyui-nkd-vfx-tools-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI-NKD-VFX-Tools stellt interaktive, VFX-orientierte Nodes bereit und kein Modell: Relight, Lens Blur, Preview 3D, fSpy Camera, Camera Delta Prompt, Perspective Unwarp/Rewarp, Lens Distort und Mask Scheduler. Die aktuellen Paketmetadaten nennen Version 1.7.4; das Paket benötigt ein aktuelles ComfyUI-Frontend und numpy, während seamless Perspective-Rewarp-Kanten zusätzlich OpenCV verwenden. Fazit: Einsetzen, um steuerbare Bildbedingungen zu erzeugen und diese an einen bestehenden ComfyUI-Generierungsworkflow zu übergeben, nicht als Ersatz für ein Diffusionsmodell.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

2026-07-24 — Das Paket befand sich in seiner ersten öffentlichen Release-Linie: Die Historie aus erster Hand verortet die erste öffentliche Veröffentlichung am 21. Juli und ergänzt am 23. Juli Nutzungsanleitungen; der Eintrag vom 24. Juli stellt daher einen frühen Schritt zur öffentlichen Verfügbarkeit dar, für den 24. Juli ist jedoch kein Commit aus erster Hand verzeichnet. 2026-07-27 — Lens Distort wurde als Version 1.4.0 dokumentiert, und Preview 3D erhielt direkten MESH-Eingang sowie Steuerungen für FOV, Roll und Hintergrundfarbe. 2026-07-30 — Preview 3D ergänzte Unterstützung für Hunyuan3D-/Output-Modell-Eingänge, viewport-gesteuerte Tiefenausgabe, automatisch geglättete Normalen und einen Pop-out-Viewer mit Tastatur-Gizmo-Kurzbefehlen. 2026-07-31 — Die Berechnung des Kontaktschattens wurde korrigiert, sodass nur tatsächlicher Bodenkontakt markiert wird; das Paket wurde auf 1.7.2 angehoben. Aktuell beobachteter Stand — Paketmetadaten nennen Version 1.7.4.

## So wird es eingesetzt {#how-to-use-this}

Stand 2026-07-24 kann keine praxisrelevante Änderung vorgeschlagen werden, da der Quellbeitrag, die Links und die Recherchebelege nicht verfügbar waren.

1. Über den ComfyUI Manager installieren, indem nach NKD VFX Tools gesucht wird, oder das Repository in ComfyUI/custom_nodes klonen; anschließend ComfyUI neu starten.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
2. Nodes im Menü NKD Nodes öffnen und zuerst das Steuerbild aufbauen: Kamera oder Perspektive lösen, 3D-Inhalte positionieren und Tiefen- oder Beleuchtungsbedingungen erzeugen, bevor die Ausgaben an den Generierungsgraphen übergeben werden.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
3. Für das Kamera-Matching zwei Paare von Fluchtlinien in NKD fSpy Camera zeichnen; für eine Perspektivbearbeitung die Fläche entzerren (unwarp), bearbeiten und anschließend wieder zurückentzerren (rewarp).
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
4. Preview 3D mit GLB/GLTF, Gaussian Splats oder unterstützten Mesh-Eingaben verwenden, um Composite, Objektebene, Maske, Tiefenkarte und Kamerainformationen für nachgelagerte Nodes zu erzeugen.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>

## Bewährte Vorgehensweisen {#best-practices}

- Die Nodes als Art Direction vor der Generierung behandeln: Licht, Kamera, Tiefe, Platzierung und Perspektive im Steuerbild explizit machen, statt sich allein auf den Prompt-Text zu verlassen.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
- Das ComfyUI-Frontend aktuell halten und numpy installieren; OpenCV nur dann installieren, wenn Perspective Rewarp Seamless Edges benötigt, da der übrige Node auch ohne OpenCV nutzbar bleibt.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
- Die interaktiven Viewports nutzen, um Steuerungen visuell zu prüfen, bevor ein aufwendiger Generierungsdurchlauf gestartet wird.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-07-23: Die frühe README beschrieb ihre Nutzungsanleitung als vorübergehend, bis Beispiel-Workflows fertig sind; die aktuelle Dokumentation aus erster Hand bietet weiterhin keine datierte Ersatz-Workflow-Sammlung, daher ist keine konkrete Ersatzempfehlung verifiziert.

## Weiterhin unbekannt {#still-unknown}

- Zum Ereignis vom 24. Juli gibt es keine extrahierte URL und keinen öffentlichen Quelltext. Belege aus erster Hand belegen benachbarte Release- und Dokumentationsdaten, identifizieren aber weder einen genauen Commit, eine Version noch eine Ankündigung für den 24. Juli.
- Für die aktuelle Paketmetadaten-Version 1.7.4 wurde kein datierter Release-Eintrag aus erster Hand gefunden; das genaue Veröffentlichungsdatum ist daher nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools | Nekodificador / ComfyUI-NKD-VFX-Tools Repository und README | 2026-09-05 |
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/commits/master/ | ComfyUI-NKD-VFX-Tools Commit-Historie | 2026-09-05 |
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/blob/master/pyproject.toml | ComfyUI-NKD-VFX-Tools Paketmetadaten | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-nkd-vfx-tools`, Thread `comfyui-nkd-vfx-tools-development`, 0 datierte Ereignisse - → -.
- **Praxishinweis:** Stand 2026-07-24 kann keine praxisrelevante Änderung vorgeschlagen werden, da der Quellbeitrag, die Links und die Recherchebelege nicht verfügbar waren.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich für das, was veraltet ist.
