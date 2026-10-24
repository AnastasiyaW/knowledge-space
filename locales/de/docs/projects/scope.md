---
title: "SCoPE"
category: projects
date: 2026-08-14
tags: [project, scope, scope-public-resources]
aliases: ["SCoPE"]
level: 3
source_sha256: 17efd9309dcfb3ec57dc8c708a375ee635e829a8b269eb5803c4f432ec581e6f
translation: machine
translated_at: '2026-10-24'
---
# SCoPE {#scope}

**Entwicklungslinie:** `project:scope` · Thread `scope-public-resources`  
**Letztes Ereignis:** 2026-08-14 · 1 datiertes Ereignis seit 2026-08-14 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

SCoPE – ein Forschungsrelease für Bild-zu-Video-Generierung für Teams, die Kamerapfad-Steuerung auf Wan2.2-I2V-A14B benötigen.

- Eingaben: nimmt ein erstes Bild, einen Textprompt und eine Ziel-Kameratrajektorie entgegen.
- Positionskoordinate: fügt den Kamerastrahl jedes Tokens als zweite Koordinate hinzu, ohne einen separaten Steuerzweig.
- Inferenzgewichte: wird mit eigenständigen Gewichten für seine Wan2.2-I2V-A14B-Basis ausgeliefert.

Der Checkpoint ist etwa 67 GB groß. Lokale Inferenz erfordert Python 3.11 und eine CUDA-fähige GPU. Das dokumentierte Standardbeispiel erzeugt 81 Frames bei 480×832. Verwenden Sie es, wenn Sie kompatible Kameraposen bereitstellen können; ungenaue Geometrie, Pfade außerhalb der Verteilung, Verdeckung und schnelle Bewegung können die Qualität mindern.

## Entwicklungslinie {#development-line}

- **2026-08-14 — SCoPE-Projektressourcen wurden verlinkt.** Am 2026-08-14 verbanden öffentliche Links die SCoPE-Projektseite, das Quellcode-Repository von TencentARC und die Hugging-Face-Seite. Zusammen boten diese Links öffentliche Einstiegspunkte für Projektinformationen, Quellcode und Modell-Hosting-Materialien. Sie belegen kein Veröffentlichungsdatum, keine Version, keine Urheberschaft und keine Fähigkeiten.

## Was sich geändert hat {#what-changed}

- 2026-06-25 — SCoPE-Paper v1 etablierte ray-basierte Positionskodierung für Video-Diffusion-Transformer.
- 2026-08-12 — arXiv v3 wurde die neueste Paper-Revision vor den öffentlichen Links. Der initiale öffentliche Code-Upload fügte Inferenz- und Trainingscode, Beispiele, Dokumentation und eine Lizenz hinzu.
- 2026-08-14 — Die verlinkten Materialien beschrieben ein bereits öffentliches SCoPE-Release. Für dieses Datum wurde kein eigenständiges erstparteiliches Release oder keine Paper-Änderung gefunden.
- 2026-08-15 — Das README dokumentierte die offizielle Hugging-Face-Demo.
- 2026-08-16 — Das Repository verbesserte die Auswahl der Trajektorien und die Demo-Workflows.
- 2026-08-22 — Das Repository stellte fehlende vendorisierte DiffSynth-Modellquellen wieder her. Dadurch wurde das Quellverzeichnis repariert, es entstand aber keine neue Modellleistung.

## So verwenden Sie es {#how-to-use-this}

1. Nutzen Sie die offizielle Browser-Demo, um den Workflow zur Kamerasteuerung bei Bild-zu-Video zu prüfen, bevor Sie lokal einrichten.
  — <https://huggingface.co/TencentARC/SCoPE>
2. Für reproduzierbare lokale Inferenz klonen Sie das Repository und erstellen die fixierte Umgebung mit `uv sync`. Das dokumentierte Release verwendet Python 3.11, PyTorch 2.9.1 und CUDA 12.8.
  — <https://github.com/TencentARC/SCoPE>
3. Laden Sie `TencentARC/SCoPE` in ein lokales Checkpoint-Verzeichnis herunter. Planen Sie Platz für den etwa 67 GB großen Checkpoint und den Cache ein.
  — <https://huggingface.co/TencentARC/SCoPE>
4. Führen Sie einen mitgelieferten Fall mit einer expliziten Trajektorie aus, etwa `omni-misty-forest` und `truck_right`, als wiederholbare Ausgangsbasis.
  — <https://github.com/TencentARC/SCoPE>
5. Für einen eigenen Lauf stellen Sie ein erstes Bild, einen Prompt, ein OpenCV-Kamera-zu-Welt-Posen-Array und das horizontale Sichtfeld bereit.
  — <https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md>

## Best Practices {#best-practices}

- Halten Sie die dokumentierte Umgebung mit Python 3.11, PyTorch 2.9.1 und CUDA 12.8 ein, wenn Sie Ergebnisse reproduzieren. Das Projekt warnt, dass Änderungen der PyTorch-Version numerische Ergebnisse verändern können.
  — <https://github.com/TencentARC/SCoPE>
- Verwenden Sie eine explizite `--trajectory` für automatisierte oder wiederholbare Jobs, und kombinieren Sie sie nicht mit `--camera_path`.
  — <https://github.com/TencentARC/SCoPE>
- Validieren Sie eigene Posen als endliche OpenCV-Kamera-zu-Welt-Arrays mit der Form `[81, 3, 4]` oder `[81, 4, 4]`. Geben Sie `x_fov` in horizontalen Radiant an und verwenden Sie `xi=0` für eine Lochkamera.
  — <https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md>
- Speichern Sie sowohl den Checkpoint als auch den Hugging-Face-Cache auf lokalem Speicher. Verwenden Sie `--vram_limit_gb`, wenn VRAM-Verwaltung oder Offloading nötig ist.
  — <https://github.com/TencentARC/SCoPE>
- Verwenden Sie Quellcode ab Commit `449343d` oder neuer für lokale Checkout-Arbeiten, da er fehlende vendorisierte DiffSynth-Modellquellen wiederherstellt. Betrachten Sie diese Reparatur nicht als Nachweis für End-to-End-Inferenz.
  — <https://github.com/TencentARC/SCoPE/commit/449343d217c54b98cb182cbc00f318f892bfecef>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-08-22 — Hinweise, die auf einem Checkout vor 449343d beruhen, sind für ein vollständiges Quellverzeichnis überholt. Der spätere Commit stellt fehlende vendorisierte DiffSynth-Modellquellen wieder her. Dies ist eine Reparatur des Repositorys, kein neues Modell-Release.

## Weiterhin unbekannt {#still-unknown}

- Keine Seite des Projekts selbst belegt ein eigenständiges SCoPE-Release oder eine Paper-Änderung am 2026-08-14; der öffentliche Code-Release und die neueste Paper-Revision vor dem Ereignis sind auf 2026-08-12 datiert.
- Die aktuellen README-Anweisungen enthalten Verbesserungen nach dem 2026-08-14. Sie sind daher aktuelle Betriebshinweise und kein Beleg für den genauen ursprünglichen Workflow.
- Es gibt keinen unabhängigen Erfahrungsbericht von Betreibern auf Englisch oder vereinfachtem Chinesisch, der ausreicht, um die Setup-Empfehlungen über die offizielle Dokumentation hinaus zu stützen.
- SCoPE hat unverwandte Namenskollisionen in der Forschungs- und Modellsuche. Das genaue TencentARC-Repository, die Modell-ID und die arXiv-ID definieren diesen Eintrag.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://visual-ai.github.io/scope/ | SCoPE: Sightline-Coordinate Positional Encoding for Video Diffusion Transformers | 2026-09-07 |
| https://github.com/TencentARC/SCoPE | TencentARC/SCoPE-Repository und README | 2026-09-07 |
| https://huggingface.co/TencentARC/SCoPE | TencentARC/SCoPE-Modellkarte | 2026-09-07 |
| https://arxiv.org/abs/2606.27345 | SCoPE: Sightline-Coordinate Positional Encoding for Video Diffusion Transformers, arXiv:2606.27345 | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commits/main | TencentARC/SCoPE-Commit-Verlauf | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/30226072dd5314dc7c4d91a25cdf3771b485e13e | Release SCoPE: inference + training code, examples, docs, and license | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/69baf9815e10afcb44cf794f76cb80e1f5c4155b | Update README.md | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/6658d0e | Improve inference trajectory selection and README demos | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/449343d217c54b98cb182cbc00f318f892bfecef | Fix missing vendored DiffSynth model sources | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md | SCoPE for Wan2.2-I2V-A14B-Modellkarte | 2026-09-07 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:scope`, Thread `scope-public-resources`, 1 datiertes Ereignis vom 2026-08-14 bis 2026-08-14.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Verwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
