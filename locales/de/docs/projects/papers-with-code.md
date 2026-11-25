---
title: "Papers with Code"
category: projects

tags: [papers-with-code, papers-with-code-development, project]
aliases: ["Papers with Code"]
level: 2
source_sha256: 6d2d5beaf4244b95a151a1b750ea90ecab45916dbbc0f6cf4deb66c5d2b3a6a0
translation: machine
translated_at: '2026-10-24'
---
# Papers with Code {#papers-with-code}

**Entwicklungslinie:** `project:papers-with-code` · Thread `papers-with-code-development`  
**Letztes Ereignis:** - · 0 datierte seitdem - · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Papers with Code ist eine von Hugging Face betriebene Neuauflage des früheren Forschungsindex für Praktiker, die Paper, Implementierungen, Tasks, Datensätze und Evaluationsergebnisse finden müssen.

- Paper-Suche, um Publikationen und verknüpfte Implementierungen zu finden.
- Task- und Benchmark-Seiten, um Datensätze und Metriken zu navigieren.
- Leaderboards mit mehreren Metriken, um die Modellleistung zu vergleichen.
- Code-Links, um Referenzimplementierungen zu prüfen.
- Ergebniseinreichungen, um Paper und Code dem Index hinzuzufügen.

Der Katalog wächst kontinuierlich, für Teile des Index gibt es eine automatisierte Anreicherung. Ein Rang im Leaderboard engt die Kandidatenmenge ein, belegt aber nicht, dass sich ein Ergebnis in einer Zielumgebung reproduzieren lässt.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; was bekannt ist, steht in den folgenden Abschnitten.

## Was sich geändert hat {#what-changed}

- 2026-05-19: Papers with Code war kurz nach seiner Neuauflage unter der neuen Domain paperswithcode.co verfügbar. Ein Update des Maintainers vom 24. Mai datiert den Start eine Woche früher. Der datierte Link allein konserviert die ursprüngliche Aussage nicht, aber die verfügbaren Belege deuten auf den neu aufgelegten Dienst hin und nicht auf ein Update der älteren .com-Seite.
- 2026-05-24: Mehrmetrische Benchmark-Tabellen, Einreichung externer Paper, Paper-Herkunft (Lineage), Methodenseiten, Export von Leaderboard-Bildern und rund 3.000 Evaluationen hinzugefügt.
- 2026-06-22: SOTA-Abzeichen für die drei besten Benchmark-Werte, Ergebnisse von Drittanbieter-Evaluationen sowie zusätzliche Tasks und Benchmarks hinzugefügt. Der Trend-Score berücksichtigt nun außerdem die Aktivität auf verknüpften Hugging-Face-Artefakten.

## So wird es verwendet {#how-to-use-this}

Stand 2026-05-19 lässt sich allein über den datierten Papers-with-Code-Homepage-Link keine Änderung der Praxis begründen.

1. Homepage öffnen, nach Forschungsaufgabe suchen oder browsen, anschließend Kandidaten-Paper-Seiten und deren verknüpfte Implementierungen öffnen.
  — <https://paperswithcode.co/>
2. Modelle auf dem relevanten Task oder Benchmark vergleichen; jede Metrik lesen, statt sich auf einen einzelnen Rang zu verlassen.
  — <https://huggingface.co/blog/nielsr/paperswithcode-launch>
3. Beim Ergänzen des Index ein arXiv-Paper, ein Repository, einen Blogbeitrag oder ein anderes unterstütztes externes Paper über die Einreichungsseite einreichen.
  — <https://paperswithcode.co/submit>
4. Den Task-Katalog nutzen, um Benchmarks zu finden, und prüfen, ob ein berichtetes Ergebnis eines Papers eine Eigenevaluation oder eine externe Evaluation ist.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>

## Best Practices {#best-practices}

- Genauigkeit zusammen mit der begleitenden Effizienzmetrik vergleichen, sofern der Benchmark mehr als eine Metrik ausweist; zum Beispiel WER mit RTFx oder mAP mit FPS.
  — <https://huggingface.co/blog/nielsr/paperswithcode-launch>
- Den Trending-Feed als Discovery-Werkzeug behandeln, nicht als Qualitätsranking: Sein Score berücksichtigt GitHub-Star-Geschwindigkeit und Aktivität auf verknüpften Hugging-Face-Artefakten.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>
- Vor einer technischen Entscheidung auf Basis einer Leaderboard-Zahl Ergebnisse der Paper-Autoren von Drittanbieter-Evaluationen trennen.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>

## Durch dies überholt {#superseded-by-this}

- Vor 2026-05-24: Hinweise, die den alten Papers-with-Code-Katalog als einzige aktuelle Oberfläche behandeln, sind veraltet; der aktive Dienst ist paperswithcode.co und unterstützt Einreichungen über arXiv hinaus.
- Vor 2026-06-22: Hinweise, die nur vom Paper eingeführte Evaluationen erwarten, sind unvollständig, da der neu aufgelegte Dienst auch externe Evaluationen anzeigt.

## Noch unbekannt {#still-unknown}

- Der Text des Eintrags vom 2026-05-19 ist nicht verfügbar, daher lässt sich die genaue Aussage von diesem Datum allein aus seiner URL nicht rekonstruieren.
- Die gepflegte Website bestätigt, dass die Neuauflage etwa eine Woche vor dem 2026-05-24 stattfand, während ein Launch-Beitrag in erster Person auf 2026-05-18 datiert ist; das verfügbare Update des Anbieters selbst legt keinen exakten Starttermin fest.
- Keine hier geprüfte Primärquelle nennt eine formale Verifikationsrichtlinie oder eine Abdeckungsgarantie für jeden automatisch angereicherten Datensatz.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://paperswithcode.co/ | Papers with Code — Trending research and open source | 2026-09-05 |
| https://huggingface.co/blog/nielsr/paperswithcode-launch | Relaunching PapersWithCode with new features | 2026-09-05 |
| https://huggingface.co/blog/nielsr/updates-to-pwc | New updates to Papers with Code | 2026-09-05 |
| https://paperswithcode.co/submit | Papers with Code submission page | 2026-09-05 |

## Agenten-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:papers-with-code`, Thread `papers-with-code-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-05-19 lässt sich allein über den datierten Papers-with-Code-Homepage-Link keine Änderung der Praxis begründen.
- **Konfidenz:** mittel. Die datierten Einträge unter „Durch dies überholt“ sind maßgeblich dafür, was veraltet ist.
