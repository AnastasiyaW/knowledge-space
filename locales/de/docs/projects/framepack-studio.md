---
title: "FramePack Studio"
category: projects
date: 2025-07-04
tags: [framepack-studio, framepack-studio-development, framepack_studio, project]
aliases: ["FramePack Studio", "Framepack Studio"]
level: 3
source_sha256: 949bc07b72fdda500f02dbac84078e58d165fd5f90a89da25a43c8ce69888152
translation: machine
translated_at: '2026-10-24'
---
# FramePack Studio {#framepack-studio}

**Entwicklungslinie:** `project:framepack-studio` · Thread `framepack-studio-development`  
**Letztes Ereignis:** 2025-07-04 · 2 datierte seit 2025-05-05 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

FramePack Studio ist eine lokale Anwendung auf Basis von FramePack für Kreative, die Original- und F1-Bild-zu-Video-Generierung sowie Videoverlängerung benötigen, ohne einen eigenen Workflow zusammenzustellen.

- Generierung mit Original und Endframe, F1-Generierung und Videoverlängerung;
- Eingaben für Text, Bild, Video, LoRA, zeitgestempelte Prompts und Prompt-Blending;
- Job-Queues, Presets, reproduzierbare Metadaten, Upscaling, Interpolation, Filter und Looping.

Die Hardware-Untergrenze ist eine CUDA-GPU mit mindestens 8 GB VRAM, empfohlen 16 GB, 16 GB Systemspeicher und 80 GB Speicherplatz. Der erste Start lädt rund 30 GB Modelle herunter.

Für einen lokalen GPU-Workflow sollten das FP-Studio-Repository und die Dokumentation verwendet werden. Nicht verwechseln mit dem nicht verwandten Browser-Dienst unter framepack.studio.

## Entwicklungslinie {#development-line}

- **2025-05-05 — Das FramePack-Studio-Repository wurde verlinkt.** Am 2025-05-05 verknüpften Links FramePack Studio mit dem GitHub-Repository colinurbs/FramePack-Studio und einem GreenNeuralRobots-Eintrag. Die Belege identifizieren weder ein Release, eine Version noch eine konkrete Funktion.
- **2025-07-04 — Dokumentation und Projekt-Repository von FramePack Studio wurden verlinkt.** Am 2025-07-04 verbanden Links FramePack Studio mit dem GitHub-Repository FP-Studio/FramePack-Studio und dessen Dokumentationsseite. Die Links belegen nicht, ob damit ein Release, eine Migration oder eine Funktionsänderung angekündigt wurde.

## Was sich geändert hat {#what-changed}

FramePack Studio hat seinen öffentlichen Pfad von einer URL im persönlichen Repository auf das FP-Studio-Projekt und seine Dokumentation verlagert; das neueste gefundene formale Release bleibt 0.5.1.

- 2025-05-05 — der Projektlink war colinurbs/FramePack-Studio; er leitet nun auf FP-Studio/framepack-studio weiter. Der Ankündigungstext ist nicht verfügbar, daher wird an diesem Datum keine Funktionsänderung zugeordnet.
- 2025-06-30 (heute gefunden) — v0.5.0 machte MagCache zum Standard-Cache, ergänzte die Granite-Prompt-Verbesserung und die Florence2-Bildbeschriftung, veröffentlichte Docker-Images und kündigte die Dokumentationsseite an.
- 2025-07-04 — die Projektlinks verweisen auf das FP-Studio-Repository und die offizielle Dokumentation, was dieselbe Projektidentität bestätigt und kein zweites FramePack Studio belegt.
- 2025-07-14 (heute gefunden) — v0.5.1 machte, dass Original das Eingabebild als erstes Frame verwendet, und behob die Reihenfolge der FFmpeg-Argumente für Video-Loops.
- 2025-11-14 (heute gefunden) — main erhielt Aktualisierungen der Paketversionen; ein neueres Release ist nicht aufgeführt.
- 2026-03-07 (heute gefunden) — eine Logging-Änderung im develop-Branch löste einen Docker-Publish-Workflow aus, der bei der Installation der Requirements fehlschlug. Dies ist eine Warnung zum Docker-Pfad der Entwicklungsversion; es beweist nicht, dass Release 0.5.1 nicht lauffähig ist.

Die öffentliche Release-Seite kennzeichnet 0.5.1 weiterhin als neueste Version.

Das Projekt blieb nach seinem letzten Release aktiv, aber ein aktuelles Deployment sollte einen gepinnten, getesteten Build verwenden und nicht davon ausgehen, dass develop veröffentlichbar ist.

## Anwendung {#how-to-use-this}

Ab 2025-07-04 sollte bei der Bewertung oder Nutzung des Projekts das verlinkte FramePack-Studio-Repository zusammen mit der Dokumentationsseite herangezogen werden; die datierten Links allein belegen keinen versionsspezifischen Workflow.

1. Prüfen, dass GPU, CUDA-/Torch-Build, Speicher und Festplatte die dokumentierten Anforderungen erfüllen; für den Host zwischen Pinokio, Docker, automatischer Windows-Installation oder manuellem Setup wählen.
  — <https://docs.framepackstudio.com/docs/get_started/>
2. Die Anwendung installieren und starten. Für Docker das Repository klonen und `docker compose` ausführen; für die manuelle Installation eine virtuelle Umgebung anlegen, die Requirements und den CUDA-passenden Torch-Build installieren und anschließend `studio.py` ausführen.
  — <https://docs.framepackstudio.com/docs/get_started/>
3. Nach Abschluss des initialen Modell-Downloads die lokale Oberfläche unter http://localhost:7860 öffnen.
  — <https://docs.framepackstudio.com/docs/get_started/>
4. Original für stärkere Konsistenz, Original with Endframe, wenn das letzte Frame wichtig ist, F1 für dynamischere Bewegung oder einen Video-Modus wählen, um einen vorhandenen Clip zu verlängern; das passende Bild- oder Videoinput bereitstellen.
  — <https://docs.framepackstudio.com/docs/user_guide/>
5. Einen konkreten Prompt mit Motiv, Szene, Aktion, Kamera, Licht und Bildausschnitt formulieren; zeitgestempelte Prompt-Segmente verwenden, wenn sich die Aktion im Verlauf ändern soll.
  — <https://docs.framepackstudio.com/docs/prompting_guide/>
6. Jobs zur Queue hinzufügen, Ausgaben und gespeicherte Metadaten prüfen und anschließend ausgewählte Clips für Nachbearbeitung wie Upscaling, Interpolation, Filter oder Loops weiterleiten.
  — <https://docs.framepackstudio.com/docs/user_guide/>

## Best Practices {#best-practices}

- Den Torch-CUDA-Build auf die GPU abstimmen und den dokumentierten Installationsweg für den Host verwenden. Pinokio ist für eine Installation ohne technischen Hintergrund am einfachsten, wird in der Dokumentation aber ausdrücklich als schwerer zu debuggen beschrieben.
  — <https://docs.framepackstudio.com/docs/get_started/>
- Höchstens eine Attention-Bibliothek installieren und SageAttention, FlashAttention oder xFormers auf GPUs der Serien RTX 1000/2000 nicht installieren, da die Dokumentation vor daraus resultierenden Generierungsfehlern warnt.
  — <https://docs.framepackstudio.com/docs/get_started/>
- Das Modell anhand des Zielkonflikts wählen: Original hält in der Regel die Konsistenz besser, während F1 in der Regel dynamischere Bewegung erzeugt, aber zwischen Abschnitten pulsieren kann.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Den Prompt konkret, aber begrenzt halten: Motiv, Szene, Aktion, Kamera, Licht und Einstellungsgröße nennen; der offizielle Leitfaden empfiehlt 60–100 Wörter und eine logische Abfolge.
  — <https://docs.framepackstudio.com/docs/prompting_guide/>
- Metadaten als JSON speichern und bei vielversprechenden Läufen den Seed beibehalten, damit Parameter wiederhergestellt und verglichen werden können, statt sie aus dem Gedächtnis neu zu erstellen.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Höheres CFG und aggressiveres Caching als Abwägung zwischen Qualität und Geschwindigkeit behandeln: CFG über 1 verdoppelt die Generierungszeit und kann Artefakte hinzufügen; niedrigere MagCache-Schwellenwerte oder eine kürzere Retention können schneller sein, weichen aber stärker von der ungecachten Ausgabe ab.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Nicht davon ausgehen, dass der develop-Docker-Pfad veröffentlichbar ist: Der letzte beobachtete Veröffentlichungs-Workflow von develop ist bei der Installation der Requirements fehlgeschlagen. Den gewählten Build pinnen und testen.
  — <https://github.com/FP-Studio/framepack-studio/actions/runs/22808835350>

## Durch dieses ersetzt {#superseded-by-this}

- 2025-05-05 — colinurbs/FramePack-Studio als eigene aktuelle Projektadresse zu behandeln; die Adresse leitet auf FP-Studio/framepack-studio weiter.
- 2025-06-30 — Annahmen aus der Zeit vor v0.5, MagCache sei nicht der Standard-Cache gewesen oder es habe keine Dokumentationsseite gegeben.
- 2025-07-14 — Annahmen aus der Zeit von v0.5.0 zur Verarbeitung des Eingabebilds bei Original; v0.5.1 verwendet das Eingabebild als erstes Frame.
- 2026-03-07 — ein Docker-Image des neuesten develop-Stands als verifizierten Deployment-Weg zu behandeln; der beobachtete Veröffentlichungslauf ist fehlgeschlagen.

## Weiterhin unbekannt {#still-unknown}

- Der genaue Text und die Funktionsaussagen der Ankündigungen vom 2025-05-05 und 2025-07-04 sind nicht verfügbar; ihre Links belegen Identität, aber keine präzise Release-Notiz.
- Die beiden datierten GitHub-Links führen zum selben FP-Studio-Projekt, sie deuten also nicht auf zwei verschiedene Gegenstände hin. Ein separater browserorientierter Dienst unter framepack.studio verwendet denselben Namen und sollte nicht als FP-Studio behandelt werden.
- In den beobachteten Suchen wurde keine offizielle vereinfacht-chinesische Dokumentation und keine bestätigte chinesischsprachige Quelle mit Betriebsberichten gefunden; die zurückgegebenen chinesischsprachigen Ergebnisse zeigten vor allem die Namenskollision mit dem nicht verwandten Dienst.
- Hier liegt kein sauberer Neuinstallations- oder erfolgreicher aktueller Docker-Deployment-Nachweis vor. Die Dokumentation, die Release-Historie, ein offener Installationsbericht vom Mai 2026 und der fehlgeschlagene develop-Publish-Job vom März 2026 zeigen, dass sich Installations- und Paketierungszustand nach v0.5.1 möglicherweise verschoben haben.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/colinurbs/FramePack-Studio/ | GitHub - FP-Studio/framepack-studio: Expanding FramePack into a multifunction video creation tool | 2026-09-04 |
| https://github.com/FP-Studio/FramePack-Studio/ | FP-Studio/framepack-studio repository | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio | GitHub - FP-Studio/framepack-studio: Expanding FramePack into a multifunction video creation tool | 2026-09-04 |
| https://github.com/FP-Studio/FramePack-Studio/releases | Releases · FP-Studio/framepack-studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/get_started/ | Erste Schritte | FP-Studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/user_guide/ | Benutzerhandbuch | FP-Studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/prompting_guide/ | Prompt-Leitfaden | FP-Studio | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/commits/main/ | Commits · FP-Studio/framepack-studio | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/actions/runs/22808835350 | finish logging implementation · FP-Studio/framepack-studio@648e34a | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/issues/382 | Installation Fail for FP-Studio · Issue #382 | 2026-09-04 |
| https://framepack.studio/zh | FramePack Studio | FramePack AI、FramePack Studio 及图像转视频工作流程 | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:framepack-studio`, Thread `framepack-studio-development`, 2 datierte Ereignisse vom 2025-05-05 bis 2025-07-04.
- **Praktischer Hinweis:** Ab 2025-07-04 sollten Anwender das verlinkte FramePack-Studio-Repository zusammen mit der Dokumentationsseite heranziehen, wenn sie das Projekt bewerten oder nutzen; die datierten Links allein belegen keinen versionsspezifischen Workflow.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.
