---
title: "DiffIR2VR-Zero"
category: projects
date: 2024-07-14
tags: [diffir2vr-zero, diffir2vr-zero-development, diffir2vr_zero, project]
aliases: ["DiffIR2VR-Zero"]
level: 2
source_sha256: 9898f04564ea07a3478fb68400b8d6f445eb317ba40f1c5dc63146be7c791dbf
translation: machine
translated_at: '2026-10-24'
---
# DiffIR2VR-Zero {#diffir2vr-zero}

**Entwicklungslinie:** `project:diffir2vr-zero` · Thread `diffir2vr-zero-development`  
**Letztes Ereignis:** 2024-07-14 · 2 datierte seit 2024-07-01 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

DiffIR2VR-Zero — Forschungscode, der vortrainierte Diffusionsmodelle zur Bildrestaurierung auf zeitlich konsistente Videorestaurierung anpasst. — Blindes Entrauschen (`dn`) und Super-Resolution (`sr`). — Beansprucht bis zu 8× Super-Resolution ohne aufgabenspezifisches Nachtraining. — Hierarchisches Latent-Warping sowie flow- und ähnlichkeitsbasiertes Token-Merging. Einschränkung: Der Launcher verwendet standardmäßig CUDA, es gibt kein getaggtes GitHub-Release, und die gehostete Demo meldet einen Build-Fehler. Für kontrollierte Experimente das Repository verwenden, die Demo nicht als produktiven Endpunkt.

## Entwicklungslinie {#development-line}

- **2024-07-01 — Projektseite und interaktive Demo von DiffIR2VR-Zero wurden öffentlich dokumentiert.** Am 2024-07-01 wurde die DiffIR2VR-Zero-Entwicklungslinie mit einer Projektwebsite und einem Hugging-Face-Space verknüpft. Dies ist eine wesentliche öffentliche Projekt- und Demo-Präsenz in der historischen Dokumentation. Das gesicherte Belegmaterial stellt Modellversion, Fähigkeiten oder Veröffentlichungsstatus hinter diesen Links nicht fest.
- **2024-07-14 — Das GitHub-Repository von DiffIR2VR-Zero wurde in der Entwicklungslinie verlinkt.** Am 2024-07-14 verknüpfte die DiffIR2VR-Zero-Entwicklungslinie einen früheren Eintrag zusammen mit dem GitHub-Repository des Projekts. Dies wird als wesentlicher Meilenstein beim Quellcodezugang in der öffentlichen Historie gewertet. Die gesicherten Links allein zeigen nicht, ob es sich um eine neue Code-Veröffentlichung oder um einen Verweis auf bereits zuvor verfügbaren Code handelt.

## Was sich geändert hat {#what-changed}

DiffIR2VR-Zero — Methode und Quellcode erschienen im Juli 2024; spätere Belege zeigen Überarbeitungen des Papers, eine Reparatur eines Checkpoint-Links und eine nicht verfügbare gehostete Demo, aber keine neue Produktgeneration. — 2024-07-01: arXiv v1 und der erste Commit des Repositorys etablierten die trainingsfreie Methode zur Videorestaurierung, die Projektseite und den lokalen Codepfad. — 2024-07-14: Der GitHub-Weg machte den Quellcode-Checkout explizit. Die Repository-Historie, heute geprüft, verortet den initialen Commit auf 2024-07-01; dies ist daher nicht als zweites algorithmisches Release belegt. — 2025-12-31 (heute gefunden): arXiv v5 wurde veröffentlicht. Seine Metadaten beschreiben keine entsprechende lauffähige Code-Änderung. — 2026-01-22 (heute gefunden): Commit `2cf4737` ersetzte die nicht mehr verfügbare offizielle URL des SD-2.1-Checkpoints durch einen Mirror; die Inferenzmethode blieb unverändert. — 2026-09-04 (heute gefunden): Der öffentliche Hugging-Face-Space meldet einen Build-Fehler, sodass das lokale Repository der praktische Einstiegspunkt bleibt. Einschränkung: In dieser Prüfung wurde keine frische Installation von Anfang bis Ende durchgeführt. Es ist als leicht gepflegter Forschungscode mit einem funktionierenden Quellpfad, aber einer fragilen Abhängigkeitskette zu behandeln.

## Anwendung {#how-to-use-this}

Ab 2024-07-01 konnten Praktiker DiffIR2VR-Zero über die öffentlichen Projekt- und Demo-Links untersuchen; ab 2024-07-14 konnten sie zusätzlich das verlinkte GitHub-Repository für den Implementierungszugang heranziehen, wobei die genaue Revision und die Nutzungsbedingungen eigenständig zu überprüfen sind.

1. Repository klonen, eine Python-3.10-Conda-Umgebung anlegen und `requirements.txt` installieren.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
2. `weights/` anlegen und `gmflow_sintel-0c07dcb3.pth` manuell hinzufügen; der dokumentierte Inferenzpfad lädt die übrigen DiffBIR-v2- und SD-2.1-Gewichte bei Bedarf nach.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
3. Mit der dokumentierten Entrauschungs-Baseline beginnen: `--version v2 --task dn --upscale 1 --cfg_scale 4.0 --batch_size 10`, mit der mitgelieferten Konfiguration, den Ein- und Ausgabepfaden, `final_size` und dem Merge-Verhältnis.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
4. Für Super-Resolution auf `--task sr` umstellen und mit dem dokumentierten 4×-Befehl beginnen, bevor der vom Projekt beanspruchte 8×-Bereich versucht wird.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
5. Für vergleichbare Läufe ein explizites `--seed` setzen und prüfen, ob CUDA tatsächlich verfügbar ist; andernfalls weicht der Launcher auf die CPU aus.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero/blob/main/inference.py>

## Best Practices {#best-practices}

- Das lokale Repository statt des gehosteten Space verwenden, bis dessen Build-Fehler behoben ist.
  — <https://huggingface.co/spaces/Koi953215/DiffIR2VR>
- Heruntergeladene Checkpoints fixieren und eigenständig verifizieren: Der Maintainer ersetzte den offiziellen SD-2.1-Download durch einen Mirror, nachdem die offizielle URL nicht mehr verfügbar war.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero/commit/2cf4737bfc8319abd8ca399d70cc49a3aaf097a6>
- Mit der dokumentierten Baseline 480×854, CFG 4.0, Batch-Größe 10 und Merge-Verhältnis beginnen; jeweils nur eine Parametergruppe ändern und dabei Detailtreue gegen zeitliche Stabilität abwägen.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
- Die Behauptungen zu bis zu 8× und ohne Nachtraining als Forschungsergebnisse behandeln und restaurierte Clips anschließend auf zeitliche Kohärenz und erfundene Details im Zielmaterial prüfen.
  — <https://jimmycv07.github.io/DiffIR2VR_web/>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2024-07-01–2024-07-14: Die Hugging-Face-Demo als operativen Einstiegspunkt nutzen — als praktische Anleitung überholt; der zugängliche Space meldet nun einen Build-Fehler.
- Vor 2026-01-22: Sich auf den automatischen Download von der offiziellen URL des Stable-Diffusion-2.1-Checkpoints verlassen — überholt; der Maintainer wechselte die Quelle, weil diese offizielle URL nicht verfügbar war.
- 2024-07-14: Den GitHub-Link als zweites Code-Release interpretieren — durch die Repository-Historie nicht gestützt, die den ersten Commit auf 2024-07-01 verzeichnet.

## Noch unbekannt {#still-unknown}

- Keine aktuelle CUDA-/PyTorch-Installation und kein vollständiger Inferenzlauf wurden unabhängig verifiziert; die Repository-Anleitungen sind Quellbelege, kein Laufzeitnachweis.
- Der zugängliche Hugging-Face-Space meldet einen Build-Fehler, sein Seiten-Snapshot wurde jedoch zwei Wochen vor dieser Prüfung gecrawlt; seine tatsächliche Live-Laufzeit wurde nicht im Browser ausgeführt.
- Der Space-Quellcode verlinkt `arXiv:2406.06523`, das eigenständige Videobearbeitungs-Paper NaRCan. Dies können veraltete Metadaten oder eine historische Verwechslung sein. Projektseite, Repository und `arXiv:2407.01519` identifizieren übereinstimmend DiffIR2VR-Zero; zwei unterschiedliche DiffIR2VR-Zero-Gegenstände sind daher nicht belegt.
- In einer separaten Suche nach vereinfachtem Chinesisch wurde keine chinesischsprachige Erstdokumentation gefunden; daher wurde keine chinesischspezifische Betriebsanleitung ergänzt.
- Die Metadaten von arXiv v2–v5 erklären ihre inhaltlichen Änderungen nicht; diese Revisionsdaten sollten nicht als Implementierungs-Releases gelesen werden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/abs/2407.01519 | DiffIR2VR-Zero: Zero-Shot Video Restoration with Diffusion-based Image Restoration Models | 2026-09-04 |
| https://jimmycv07.github.io/DiffIR2VR_web/ | DiffIR2VR-Zero Projektseite | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero | GitHub — jimmycv07/DiffIR2VR-Zero | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/commits/main | Commit-Historie — jimmycv07/DiffIR2VR-Zero | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/blob/main/inference.py | DiffIR2VR-Zero inference.py | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/commit/2cf4737bfc8319abd8ca399d70cc49a3aaf097a6 | Änderung der sd_v21-Modell-Checkpoint-URL | 2026-09-04 |
| https://huggingface.co/spaces/Koi953215/DiffIR2VR | DiffIR2VR — Hugging-Face-Space | 2026-09-04 |
| https://arxiv.org/abs/2406.06523 | NaRCan: Natural Refined Canonical Image with Integration of Diffusion Prior for Video Editing | 2026-09-04 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:diffir2vr-zero`, Thread `diffir2vr-zero-development`, 2 datierte Ereignisse 2024-07-01 → 2024-07-14.
- **Praktische Anmerkung:** Ab 2024-07-01 konnten Praktiker DiffIR2VR-Zero über die öffentlichen Projekt- und Demo-Links untersuchen; ab 2024-07-14 konnten sie zusätzlich das verlinkte GitHub-Repository für den Implementierungszugang heranziehen, wobei die genaue Revision und die Nutzungsbedingungen eigenständig zu überprüfen sind.
- **Konfidenz:** mittel. Die datierten Abschnitte „Abgelöst durch diesen Eintrag“ sind maßgeblich dafür, was veraltet ist.
