---
title: "KI-Texterkennung"
description: "Unterscheidung zwischen sprachwissenschaftlicher Korpusforschung auf Populationsebene, Einzelfallerkennung, Herkunftsnachweis und redaktioneller Qualität."
category: concepts
tags: [writing, ai-detection, nlp, research, evaluation]
level: 3
source_sha256: fb97cc3e7cca21e8c9dfeee7075524ceb2e0d93f46bd2a36aaea8206c7b0ffef
translation: machine
translated_at: '2026-10-24'
---
# KI-Texterkennung {#ai-text-detection}

Die Erkennung der Textherkunft, die inhaltliche Faktenprüfung und die redaktionelle
Qualität beantworten unterschiedliche Fragen. Ein klarer, korrekter Artikel kann
KI-unterstützt entstanden sein; ein von Menschen geschriebener Artikel kann falsch
sein. Der Geltungsbereich wurde am 2026-09-06 anhand der unten genannten Primärquellen geprüft.

Verwandle keine Wortliste, keine Heuristik zum Satzrhythmus und keinen unkalibrierten
Produktwert in eine sichere Aussage über den Arbeitsprozess einer bestimmten Autorin
oder eines bestimmten Autors.

## Die Fragen getrennt behandeln {#separate-the-questions}

| Frage | Relevante Evidenz | Was sie nicht beantwortet |
|---|---|---|
| Hat sich der Sprachgebrauch in einem Korpus verändert? | Korpusdesign, Zeitvergleich, gemessene Verschiebungen im Wortschatz | Ein auffälliges Wort in einem einzelnen Dokument |
| Unterscheidet ein Detektor in einem definierten Setting zuverlässig? | Beschriftete Stichproben außerhalb des Trainings, fester Schwellenwert, Fehlerraten | Eine Herstellerrangliste oder eine unversionierte Genauigkeitsangabe |
| Wie wurde dieses konkrete Dokument erstellt? | Verfügbare Quell- bzw. Entwurfshistorie und vertrauenswürdige Herkunftsnachweise | Gewöhnliche Grammatik oder das Fehlen von Anekdoten |
| Ist dieses Dokument korrekt und nützlich? | Quellen, gegebenenfalls lauffähige Beispiele, Aufgabe der Leserin bzw. des Lesers | Ein niedriger Wert für „KI-Wahrscheinlichkeit“ |

## Was die zitierte Forschung belegt {#what-the-cited-research-establishes}

[Delving into LLM-assisted writing in biomedical publications through excess vocabulary](https://arxiv.org/abs/2406.07016)
untersucht Veränderungen im Wortschatz biomedizinischer Zusammenfassungen. Die
Schätzungen auf Korpusebene sind weder ein Klassifikator für einzelne Dokumente noch
eine redaktionelle Sperrliste. Berücksichtige bei der Diskussion ihrer Schätzungen
die dort angegebene Grundgesamtheit und Revision; übertrage keinen Prozentwert auf
eine andere Sprache, Textgattung oder Zeitspanne.

[GPT detectors are biased against non-native English writers](https://arxiv.org/abs/2304.02819)
berichtet über Probleme mit falsch positiven Ergebnissen und mit der Robustheit bei
den untersuchten Detektoren und Stichproben. Die Studie spricht für Vorsicht bei
diesen Messungen, nicht für die Behauptung, dass jeder aktuelle Detektor gleichermaßen
ungenau sei.

Der [NIST-Bericht zur Transparenz synthetischer Inhalte](https://doi.org/10.6028/NIST.AI.100-4)
behandelt Herkunftsnachweise, Kennzeichnung, Erkennung und Evaluation als
unterschiedliche technische Ansätze. Herkunftsnachweise können Informationen über
Ursprung und Veränderungen liefern; sie garantieren jedoch nicht, dass eine Aussage
wahr ist oder im richtigen Kontext steht.

Quellenversionen: arXiv 2406.07016 v5 (2025-07-03), arXiv 2304.02819 v3
(2023-07-10) und NIST AI 100-4 (2024-11-20). Diese Daten kennzeichnen die Evidenz,
sie stellen keinen Benchmark für alle im September 2026 verfügbaren Modelle oder
Detektoren dar.

## Einen Detektor vor der Verwendung seines Werts bewerten {#evaluate-a-detector-before-using-its-score}

Lege für eine konkrete Erkennungsaufgabe die vorgesehene Grundgesamtheit und die
Kosten von Fehlentscheidungen fest. Halte Trainings- bzw. Material zur Schwellenwertwahl
von der Evaluation mit Testdaten getrennt.

Erfasse in der bereits verwendeten Evaluation mindestens Folgendes:

- Detektorversion, Vorverarbeitung, Schwellenwert und verfügbare Definition des Werts.
- Gruppen menschlicher und generierter Quellen, Sprache, Textgattung und Dokumentlänge.
- Generatoridentität und Einstellungen, sofern bekannt; unbekannte Herkunft ist explizit zu kennzeichnen.
- Anzahl der falsch positiven und falsch negativen Ergebnisse mit ihren Bezugsgrößen.
- Verhalten bei zulässiger Bearbeitung, Übersetzung und gemischter Urheberschaft, soweit für die Aufgabe relevant.

Berichte die Ergebnisse für die gemessenen Gruppen und nicht nur eine gepoolte
Genauigkeitszahl. Entscheide, ob die beobachteten Fehler für den vorgesehenen Zweck
tragbar sind. Ein unerklärter Wert darf niemals als Beweis für Fehlverhalten gelten.

## Die Erkennung aus dem Bearbeitungsziel heraushalten {#keep-detection-out-of-the-editing-objective}

Bearbeite auf belegte Bedeutung, nützliche Struktur und die gewünschte Tonalität hin.
Bewahre Datumsangaben, Zahlen, Versionen, Unsicherheiten und Zuschreibungen.

Eine feste Vorgabe für Meinungen, persönliche Misserfolgsgeschichten, ungewöhnliche
Wörter oder ungleichmäßige Absatzlängen kann ein sachliches Nachschlagewerk
beschädigen. Umgekehrt können formelle Prosa und parallele Listenpunkte für Verträge
und Anleitungen angemessen sein. Dies sind redaktionelle Entscheidungen, keine
gemessenen Urteile über die Urheberschaft.

Wenn ein Stilhinweis auf ein reales Problem hinweist, benenne es direkt: eine
mehrdeutige Bedingung, einen überflüssigen Absatz, eine nicht belegte Garantie oder
eine fehlende Quelle. Füge keine absichtlichen Fehler oder erfundene Aussagen hinzu,
um einen Detektorwert zu senken.

## Entscheidungsgrenzen {#decision-boundaries}

Verwende Erkennung nur für die Aufgabe, für die sie evaluiert wurde. Kann die
verfügbare Evidenz die Herkunft nicht feststellen, bleibt diese Schlussfolgerung
offen, statt sie durch stilistische Sicherheit zu ersetzen.

Für eine Aufgabe mit Veröffentlichungsanspruch können eine Quellenprüfung und eine
begrenzte redaktionelle Durchsicht die Arbeit abschließen, ohne die Urheberschaftsfrage
zu lösen. Bei einer Untersuchung der Urheberschaft ist saubere Prosa allein kein
abschließender Beleg.

## Fallstricke {#gotchas}

- **Sprung von der Korpus- auf die Dokumentebene:** Eine Verschiebung auf
  Populationsebene wird als Beweis gegen eine einzelne Person behandelt. Halte die
  Schätzung für die Population und die Aussage zum Einzelfall getrennt.
- **Ungemessener Schwellenwert:** „drei Warnzeichen“ werden zu hoher Sicherheit.
  Verwende eine evaluierte Entscheidungsregel oder halte fest, dass keine kalibrierte
  Regel verfügbar ist.
- **Detektoroptimierung schadet den Fakten:** Datumsangaben, Zahlen oder
  Unsicherheiten werden verändert, damit der Text weniger synthetisch klingt.
  Bewahre zuerst die Aussage, bevor du den Stil änderst.
- **Herkunftsnachweis wird mit Wahrheit verwechselt:** Eine authentische Historie
  wird genutzt, um eine falsche Aussage zu stützen. Prüfe die Aussage und ihren
  Kontext unabhängig davon.

## Siehe auch {#see-also}

- [[editing-checklist]]
- [[agent-evaluation]]
