---
title: "GenMM"
category: projects
date: 2023-06-02
tags: [genmm, genmm-development, project]
aliases: ["GenMM"]
level: 2
source_sha256: a13baecfc849b590a051ba38845647dc36fca6de36407b1f4e2bff34b4411bd4
translation: machine
translated_at: '2026-10-24'
---
# GenMM {#genmm}

**Entwicklungslinie:** `project:genmm` · Thread `genmm-development`  
**Letztes Ereignis:** 2023-06-02 · 1 datiertes Ereignis seit 2023-06-02 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

GenMM ist eine Forschungscodebasis zur SIGGRAPH 2023 für technische Animatoren, die neue skelettale Bewegungssequenzen aus einem oder wenigen Beispielclips benötigen. Es handelt sich nicht um ein Text-zu-Bewegung-Modell.

- Erzeugt diverse Varianten, vervollständigt Bewegungen, folgt Keyframe-Posen, erstellt Schleifen, setzt Bewegungen über heterogene Skelette hinweg neu zusammen und verändert Fortbewegungstrajektorien.
- Der dokumentierte lokale Stack ist Python 3.8, PyTorch 1.12.1 und CUDA 11.3. Die Autoren berichten von etwa 0,05 s pro Bewegung auf einer Tesla V100 und 0,2 s auf einem Apple M1.

## Entwicklungslinie {#development-line}

- **2023-06-02 — Öffentliche GenMM-Projektmaterialien verlinkt.** Am 2023-06-02 veröffentlichte das Projekt seine Projektseite, das Quell-Repository und einen Demo-Link. Dieser Meilenstein eröffnete Einstiegspunkte für die Evaluation des Projekts, wobei der nicht verfügbare Quelltext die genaue Release-Aussage und die technischen Details unbelegt lässt.

## Was sich geändert hat {#what-changed}

2023-06-02 — GenMM ging mit einer Projektseite, einem Quell-Repository und einer Browser-Demo als beispielbasiertes, trainingsfreies System zur Bewegungssynthese online. Die Seite dokumentiert Bewegungsvervollständigung, Keyframe-Steuerung, Schleifenbildung, Neuzusammensetzung und Fortbewegung. 2023-07-13 — der Eintrag nennt nur den bestehenden Endpunkt der Browser-Demo. Er identifiziert kein neues Modell, keine Paketversion und kein neues Feature, daher handelt es sich nicht um einen bestätigten Software-Release. 2026-09-04 — die ursprüngliche GitHub-URL leitet auf liyuuuu98/GenMM weiter; die aktuelle Releases-Seite zeigt ein einziges Blender-Add-on-Pre-Release, v0.0.1. Die abgerufene Release-Seite gibt nur "29 Jul 12:48" an, nicht aber ein Jahr, daher wird kein vollständiges Veröffentlichungsdatum zugeordnet.

## Anwendung {#how-to-use-this}

Ab 2023-06-02 konnten wir die öffentliche GenMM-Projektseite, das Quell-Repository und die Demo als Einstiegspunkte für die Evaluation nutzen. Der Demo-Link vom 2023-07-13 allein belegt keine weitere praktische Änderung.

1. Klonen Sie das Repository und reproduzieren Sie die dokumentierte Umgebung: Python 3.8, PyTorch 1.12.1, CUDA 11.3, docker/requirements.txt und torch-scatter==2.1.1.
  — <https://github.com/wyysf-98/GenMM>
2. Stellen Sie einen BVH-Bewegungsclip bereit und führen Sie `python run_random_generation.py -i <clip.bvh>` aus; für weitere Konfiguration der Synthese verwenden Sie `run_random_generation.py`.
  — <https://github.com/wyysf-98/GenMM>
3. Für Blender installieren Sie die aufgelisteten Python-Pakete in den mitgelieferten Python-Interpreter von Blender und installieren die Add-on-ZIP über Preferences > Add-ons > Install. Anschließend wählen Sie ein Armature aus und öffnen das GenMM-Panel.
  — <https://github.com/wyysf-98/GenMM>
4. Für die Web-Demo wählen Sie ein Beispiel mit Next, verwenden Generate und Controls und setzen dann frames, noise_sigma, loop, patch_size, coarse_ratio, pyr_factor und Optimierungsschritte.
  — <https://github.com/wyysf-98/GenMM_demo>
5. Wartet die geteilte Demo unbegrenzt, duplizieren Sie deren Hugging-Face-Space, beziehen Ihre eigene API-URL und ersetzen `api_url` in Controls.
  — <https://github.com/wyysf-98/GenMM_demo>

## Best Practices {#best-practices}

- Fixieren oder containerisieren Sie die dokumentierten Python-, PyTorch- und CUDA-Versionen, bevor Sie Abhängigkeiten ändern. Die offiziellen Anweisungen enthalten keine neuere Kompatibilitätsmatrix.
  — <https://github.com/wyysf-98/GenMM>
- Validieren Sie die finale Bewegung in einem riggbewussten Workflow und nicht nur im Browser-Viewer. Die Projektseite warnt, dass dem Three.js-FBX-Parser eine Fußkontakt-Korrektur fehlt und er Artefakte erzeugen kann.
  — <https://weiyuli.xyz/GenMM/>
- Wenn die geteilte Demo langsam ist, verwenden Sie einen duplizierten Space mit Ihrer eigenen API-URL, statt den CPU-basierten geteilten Endpunkt wiederholt neu anzufragen.
  — <https://github.com/wyysf-98/GenMM_demo>

## Abgelöst durch dies {#superseded-by-this}

- 2023-06-02 — Die README-Release-Checkliste ist als Verfügbarkeitsaussage veraltet: Das Repository enthält nun den lokalen Runner, und GitHub listet das Blender-Add-on v0.0.1 als Pre-Release.
- 2023-07-13 — Ein reiner Browser-Demo-Workflow ist für wiederholte Arbeit veraltet: Die Erstanbieter-Dokumentation beschreibt nun einen Wiederherstellungspfad über einen kopierten Space mit privater API und warnt vor Viewer-Artefakten und Stillständen der geteilten CPU.

## Weiterhin unbekannt {#still-unknown}

- Keine heute gelesene Primärquelle liefert eine 2026 getestete Kompatibilitätsmatrix für Python, PyTorch, CUDA oder Blender.
- Der Eintrag vom 2023-07-13 liefert nur die bestehende Demo-URL. Ohne seinen Quelltext können wir diesem Datum keine eigene Fähigkeit oder Version zuordnen.
- Die aktuelle Releases-Seite zeigt v0.0.1 als Pre-Release und gibt 29 Jul 12:48 an, die abgerufene Ansicht legt jedoch kein Jahr offen.
- Die Browser-Demo benötigt JavaScript; eine durchgängige Live-Generierung wurde in dieser Recherche nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://weiyuli.xyz/GenMM/ | Example-based Motion Synthesis via Generative Motion Matching | 2026-09-04 |
| https://github.com/wyysf-98/GenMM | GitHub — liyuuuu98/GenMM | 2026-09-04 |
| https://weiyuli.xyz/GenMM_demo/ | patch-based_motion_synthesis | 2026-09-04 |
| https://github.com/wyysf-98/GenMM_demo | GitHub — liyuuuu98/GenMM_demo | 2026-09-04 |
| https://github.com/wyysf-98/GenMM/releases | GitHub — GenMM-Releases | 2026-09-04 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:genmm`, Thread `genmm-development`, 1 datiertes Ereignis, 2023-06-02 → 2023-06-02.
- **Praktischer Hinweis:** Ab 2023-06-02 konnten Praktiker die öffentliche GenMM-Projektseite, das Quell-Repository und die Demo als Einstiegspunkte für die Evaluation nutzen. Der Demo-Link vom 2023-07-13 allein belegt keine weitere praktische Änderung.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
