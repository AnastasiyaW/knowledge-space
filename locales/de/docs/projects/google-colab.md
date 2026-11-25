---
title: "Google Colab"
category: projects
date: 2023-05-19
tags: [colab_ai_codey, google-colab, google-colab-platform-evolution, google-colab:subscription-policy, project]
aliases: ["Google Colab"]
level: 3
source_sha256: 2509e165f739f1b50df56a84ec82beb2ff4accf9cba2a78bc659ed516d5e831d
translation: machine
translated_at: '2026-10-24'
---
# Google Colab {#google-colab}

**Entwicklungslinie:** `project:google-colab` · Strang `google-colab-platform-evolution`  
**Letztes Ereignis:** 2023-05-19 · 2 datierte seit 2022-08-31 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Google Colab ist gehostetes Jupyter für Python-Nutzer, die ein Browser-Notebook statt eines lokalen Jupyter-Setups benötigen.

- Dedizierte virtuelle Maschine, die Nutzercode ausführt.
- GPU- und TPU-Zugriff, sofern Rechenressourcen verfügbar sind.
- Integration mit Google Drive und GitHub, die `.ipynb`-Dateien speichert, teilt und lädt.
- Gemini-Integration, die für berechtigte Konten Chat, Code-Vervollständigung und einen Data-Science-Agenten ergänzt.

Die kostenlose Laufzeit ist nicht garantiert, dauert typischerweise höchstens 12 Stunden, und die Rechenkontingente ändern sich im Laufe der Zeit.

Die Plattform eignet sich für Tutorials, schnelle Prototypen und interaktive ML-Aufgaben, nicht aber für kontinuierliche oder fest geplante Rechenlasten.

## Entwicklungslinie {#development-line}

- **2022-08-31 — Änderung der Abonnementrichtlinie von Google Colab wurde öffentlich gemeldet.** Der verlinkte Eintrag ist zur Prüfung nicht verfügbar; die konkrete Abonnementänderung ist unbestätigt und kann nicht als aktive Regel gelten.
- **2023-05-19 — Google Colab führte KI-Codierungsfunktionen ein.** Google kündigte Codey-Funktionen an: Codegenerierung aus natürlicher Sprache, Code-Vervollständigung für berechtigte zahlende Abonnenten und einen Chat-Assistenten, zunächst für kostenpflichtige Konten in den USA.

## Was sich geändert hat {#what-changed}

Google Colab hat die Richtlinien für den Zugriff auf Rechenressourcen und den integrierten KI-Assistenten aktualisiert.

- 2022-08-31: Der verlinkte Eintrag ist zur Prüfung nicht verfügbar, daher ist die Abonnementänderung unbestätigt und kann nicht als aktive Regel gelten.
- 2023-05-19 (offizielle Ankündigung vom 2023-05-17): Google kündigte Codey-Funktionen an, darunter Codegenerierung aus natürlicher Sprache, Code-Vervollständigung für berechtigte zahlende Nutzer und einen Chat-Assistenten, zunächst für kostenpflichtige Tarife in den USA.
- 2026-04-08: Die Gemini-Integration erhielt in Notebooks gespeicherte Custom Instructions und den Learn Mode für schrittweise Anleitung.
- 2026-09-04: Die aktuelle Dokumentation beschreibt AI-First Colab mit Gemini-Chat, Code-Vervollständigung und einem Data Science Agent, der nach Prüfung durch den Nutzer einen Plan vorschlägt und ausführt; der Zugang variiert nach Alter und Region.
- 2026-09-04: Die Ressourcenzuteilung ist ausdrücklich dynamisch; weder kostenlose noch bezahlte Tarife garantieren Ressourcen, und Limits, Lebensdauer der VMs und Beschleunigertypen schwanken.

Der frühe Codey-Rollout spiegelt nicht die heutige Gemini-Oberfläche wider, und frühere Preisangaben ersetzen nicht die aktive Abonnementseite.

Colab bleibt ein einziger Dienst, Nutzer müssen verfügbare Compute-Laufzeiten und KI-Werkzeuge jedoch getrennt bewerten.

## So wird es eingesetzt {#how-to-use-this}

Nach dem 2023-05-19 sollten Praktiker Google Colab sowohl als gehostete Notebook-Umgebung als auch als KI-gestützte Coding-Umgebung betrachten und dabei die für ihre Arbeitslast geltende Abonnement- und Zugriffsrichtlinie prüfen.

1. Colab öffnen und über File ein neues Notebook erstellen oder über File > Upload notebook eine vorhandene `.ipynb`-Datei hochladen.
  — <https://research.google.com/colaboratory/faq.html>
2. Code- und Textzellen hinzufügen; wenn die Arbeitslast Hardwarebeschleunigung erfordert, über Runtime > Change runtime type eine GPU oder TPU auswählen.
  — <https://research.google.com/colaboratory/faq.html>
3. Notebooks in Google Drive speichern oder von GitHub laden; Notebooks über Share teilen, wobei zu beachten ist, dass die zugrunde liegende VM und lokale Dateien nicht übertragen werden.
  — <https://research.google.com/colaboratory/faq.html>
4. Den Gemini-Assistenten am unteren Rand des Notebooks öffnen, die Aufgabe beschreiben und jeden generierten Plan prüfen, bevor der Code ausgeführt wird.
  — <https://research.google.com/colaboratory/faq.html>
5. Für die Nutzung einer lokalen Maschine Jupyter oder eine unterstützte lokale Runtime ausführen, Connect > Connect to local runtime auswählen und die Backend-URL angeben.
  — <https://research.google.com/colaboratory/local-runtimes.html>

## Bewährte Praktiken {#best-practices}

- Verwaltete VMs als temporär behandeln: Abhängigkeiten direkt im Notebook installieren und Eingabedateien dort herunterladen, Ergebnisse jedoch außerhalb der Laufzeit speichern.
  — <https://research.google.com/colaboratory/faq.html>
- GPUs oder viel Speicher nicht unnötig anfordern und inaktive Tabs schließen, um das Rechenkontingent zu schonen.
  — <https://research.google.com/colaboratory/faq.html>
- Bibliotheksversionen für gemeinsam genutzte oder Lehr-Notebooks explizit festschreiben; bei Bedarf eine ältere Runtime-Version wählen, wobei zu beachten ist, dass frühere Runtimes nur begrenzte Lebensdauern haben.
  — <https://research.google.com/colaboratory/runtime-version-faq.html>
- Von Gemini generierten Code prüfen, testen und validieren; vertrauliche oder personenbezogene Daten nicht in KI-Prompts verwenden.
  — <https://research.google.com/colaboratory/faq.html>
- Lokale Runtimes nur mit vertrauenswürdigen Notebooks und geprüftem Code verbinden, da lokale Runtimes beliebige Shell-Befehle ausführen und lokale Dateien lesen können.
  — <https://research.google.com/colaboratory/local-runtimes.html>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2022-08-31: Ungeprüfte Behauptungen über Abonnementregeln sind veraltet; die aktuelle Richtlinie definiert alle Kontingente und Rechenressourcen als dynamisch.
- 2023-05-17/2023-05-19: Der Codey-Rollout für kostenpflichtige Konten in den USA wird durch AI-First Colab mit Gemini für berechtigte Nutzer ersetzt.
- 2025-03-21: Der Start von Colab über GCP-Marketplace-VMs ist veraltet; die Google-Dokumentation verweist auf Colab Enterprise oder lokale Runtimes.

## Noch unbekannt {#still-unknown}

- Der Quelltext vom 2022-08-31 ist nicht zugänglich, daher bleibt die genaue Änderung der Abonnementrichtlinie unbestätigt.
- Das erfasste Ereignisdatum 2023-05-19 weicht vom offiziellen Ankündigungsdatum 2023-05-17 ab.
- Rechenlimits und KI-Codierung gehören zum selben Dienst, Google hat jedoch keinen kausalen Zusammenhang zwischen den Richtlinienänderungen bestätigt.
- Genaue Preise, Recheneinheiten, GPU- und TPU-Modelle sowie die Verfügbarkeit von Gemini variieren je nach Konto, Tarif und Region und müssen direkt in der Abonnementoberfläche geprüft werden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://twitter.com/EMostaque/status/1564773589886320640 | Beitrag von @EMostaque — Inhalt während der Prüfung nicht verfügbar | 2026-09-04 |
| https://blog.google/technology/developers/google-colab-ai-coding-features/ | KI-gestütztes Programmieren, kostenlos mit Colab | 2026-09-04 |
| https://research.google.com/colaboratory/faq.html | Häufig gestellte Fragen | 2026-09-04 |
| https://blog.google/innovation-and-ai/technology/developers-tools/colab-updates/ | Einführung des Learn Mode: Ihr persönlicher Programmier-Tutor in Google Colab | 2026-09-04 |
| https://research.google.com/colaboratory/local-runtimes.html | Lokale Runtimes | 2026-09-04 |
| https://research.google.com/colaboratory/runtime-version-faq.html | Häufig gestellte Fragen – Frühere Runtime-Versionen | 2026-09-04 |
| https://research.google.com/colaboratory/marketplace.html | Anleitung zum Starten einer GCE-VM in Colab über den GCP Marketplace | 2026-09-04 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:google-colab`, Strang `google-colab-platform-evolution`, 2 datierte Ereignisse 2022-08-31 → 2023-05-19.
- **Praktischer Hinweis:** Nach dem 2023-05-19 sollten Praktiker Google Colab sowohl als gehostete Notebook-Umgebung als auch als KI-gestützte Coding-Umgebung betrachten und dabei die für ihre Arbeitslast geltende Abonnement- und Zugriffsrichtlinie prüfen.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
