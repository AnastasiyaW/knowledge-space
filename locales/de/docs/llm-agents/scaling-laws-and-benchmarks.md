---
title: "LLM-Skalierungsgesetze und Benchmarks"
description: "Skalierungsgesetz-Forschung und Benchmark-Suiten nutzen, ohne historische Anpassungen oder Leaderboard-Momentaufnahmen in Produktentscheidungen zu verwandeln"
level: 3
source_sha256: efcfe64bc1a45ba02f60b1777b897c3e3105e6f96e776aa0bcc6da500db3062d
translation: machine
translated_at: '2026-10-24'
---
# LLM-Skalierungsgesetze und Benchmarks (September 2026) {#llm-scaling-laws-and-benchmarks-september-2026}

Versionskontext: Anpassungen von Skalierungsgesetzen und Benchmark-Ergebnisse sind empirische Resultate unter angegebenen Datensätzen, Rechenbudgets, Architekturen, Prompts und Evaluierungsumgebungen. Sie sind weder universelle Dimensionierungsregeln noch dauerhafte Modellrankings.

## Was Skalierungsgesetze beantworten {#what-scaling-laws-answer}

Die Forschung zu Skalierungsgesetzen untersucht, wie sich ein gemessener Verlust oder eine gemessene Fähigkeit verändert, wenn Trainings-Rechenaufwand, Modellgröße, Datenmenge und verwandte Größen zunehmen. Sie ist nützlich für:

- die Planung eines kontrollierten Pretraining- oder Continued-Pretraining-Programms;
- die Auswahl der als Nächstes durchzuführenden kostspieligen Experimente;
- das Erkennen offensichtlich untertrainierter Kandidatenkonfigurationen;
- die Einordnung eines Rechenaufwand-/Daten-Trade-offs innerhalb einer festen Methodik.

Allein entscheidet sie nicht, welches Modell in die Produktion geht, beweist keine nachgelagerte Sicherheit und sagt keine Latenz und Kosten unter einer realen Serving-Last voraus.

Die Chinchilla-Studie berichtete, dass für ihre rechenoptimale Einstellung Modellgröße und Trainingstokens proportional skaliert werden sollten. Dieses Ergebnis ist eine historische Anpassung an ein bestimmtes experimentelles Regime. Verwenden Sie es als Beschaffungsregel `tokens-per-parameter` erst, nachdem Sie es an der tatsächlichen Architektur, den Daten und der Zielfunktion validiert haben.

## Drei Entscheidungen getrennt betrachten {#separate-three-decisions}

| Entscheidung | Evidenz, die sie entscheidet |
|---|---|
| Zuteilung beim Pretraining | Kontrollierte Experimente zu Verlust/Fähigkeit, Herkunft von Rechenaufwand und Daten |
| Serving-Design | Gemessene Latenz, Durchsatz, Speicherbedarf, Verfügbarkeit und Stückkosten |
| Produktabnahme | Eingefrorene Aufgabensuite, Sicherheitsprüfungen und Überprüfung nutzerrelevanter Fehler |

Wer diese vermischt, zieht falsche Schlüsse: Ein größeres Modell kann die schlechtere Produktwahl sein, wenn es den Ziel-Workflow nicht erfüllt, ein SLO verfehlt oder sich nicht sicher betreiben lässt.

## Benchmark-Inventar {#benchmark-inventory}

Ein Benchmark ist nur dann nützlich, wenn seine Aufgabe, Version, sein Prompt, seine Bewertungsmethode und sein Kontaminationsrisiko bekannt sind.

| Kategorie | Beispielhafte Verwendung | Freigabefrage |
|---|---|---|
| Breites Wissen/Schlussfolgern | MMLU-artige Suite | Verschlechtert sich der Kandidat bei der für das Produkt relevanten allgemeinen Fähigkeit? |
| Domänen-Aufgabenset | Internes gelabeltes Korpus | Löst er die tatsächliche Arbeit korrekt? |
| Robustheits- / Adversarial-Set | Prompt-Injection, Verweigerung, fehlerhafte Eingaben | Scheitert er sicher? |
| Tool-Nutzung | Aufgezeichnete Tool-Verträge | Wählt er erlaubte Aktionen aus und hält er Schemas ein? |
| Betriebstest | Last- und Fehlerprüfung | Kann er Latenz-, Fehler- und Kostengrenzen einhalten? |

MMLU ist ein häufig zitierter akademischer Benchmark, aber ein einzelner aggregierter Wert ist kein Nachweis, dass ein Agent bei der Aufgabe einer Organisation zuverlässig arbeitet. Behandeln Sie Benchmark-Ergebnisse als diagnostische Signale neben einer produktspezifischen Evaluierung.

## Evaluierungsprotokoll {#evaluation-record}

Jeder Vergleich braucht einen unveränderlichen Nachweis. So geht eine Leaderboard-Zahl nicht die Einstellungen verloren, die sie hervorgebracht haben.

```json
{
  "evaluation_id": "support-routing-2026-09-03",
  "candidate": {"model": "candidate-id", "revision": "immutable-revision"},
  "baseline": {"model": "baseline-id", "revision": "immutable-revision"},
  "suite": {"name": "support-routing-v4", "digest": "sha256:..."},
  "harness": {"commit": "git-sha", "prompt_policy": "prompt-v7"},
  "metrics": {
    "route_accuracy": 0.0,
    "schema_valid_rate": 0.0,
    "p95_latency_ms": 0,
    "cost_per_accepted_output": 0.0
  },
  "verdict": "hold"
}
```

Verwenden Sie für Basislinie und Kandidat dieselbe Eingabemenge, dieselbe Decoding-Richtlinie, dieselbe Tool-Verfügbarkeit und dieselbe Bewertungsmethode. Wenn sich etwas ändert, beginnen Sie einen neuen Vergleich, statt Zahlen zusammenzuführen.

## Kontamination und Reproduzierbarkeit {#contamination-and-reproducibility}

Öffentliche Benchmarks können in Pretraining- oder Instruction-Tuning-Daten enthalten sein. Ein hoher Wert kann auf Auswendiglernen, Prompt-Empfindlichkeit oder testspezifische Optimierung hindeuten statt auf übertragbare Leistung.

Gegenmaßnahmen:

1. Benchmark-Revision und Quelllizenz nachverfolgen.
2. Eine private, neu erhobene Aufgabensuite führen, die niemals zum Tuning verwendet wird.
3. Verborgene Fälle rotieren, dabei stabile Regressionsfälle beibehalten.
4. Prompts, Zufallsseeds, Sampling-Parameter und Tool-Richtlinie protokollieren.
5. Repräsentative Erfolge und Fehlschläge manuell prüfen.

## Verfahren zur Modellauswahl {#model-selection-procedure}

1. Einen Abnahmevertrag definieren: Ergebnisqualität, Sicherheit, Latenz, Verfügbarkeit und Budget.
2. Eine Basislinie mit der eingesetzten Prompt-/Tool-Richtlinie etablieren.
3. Eine kleine Menge an Kandidatenstufen auf derselben eingefrorenen Suite testen.
4. Fehlerausschnitte prüfen, nicht nur den Durchschnitt.
5. Den günstigsten Kandidaten auswählen, der jede erforderliche Schwelle erfüllt.
6. Den Nachweis aufbewahren und eine Neubewertung einplanen, wenn sich Modell, Prompts, Tools oder Korpus ändern.

## Fallstricke {#gotchas}

- **Ein Koeffizient eines Skalierungsgesetzes ist kein Deployment-Parameter.** Er wurde unter bestimmten Annahmen geschätzt. **Lösung:** Verwenden Sie ihn, um Experimente auszuwählen, und messen Sie dann die Last, die tatsächlich bereitgestellt wird.
- **Aggregierte Werte verbergen inakzeptable Ausschnitte.** Ein Modell kann den Durchschnitt verbessern und dabei an einer regulierten Sprache, einer schwierigen Kohorte oder einer Sicherheitsbedingung scheitern. **Lösung:** Explizite Freigabeschwellen pro Ausschnitt festlegen.
- **Leaderboard-Momentaufnahmen veralten.** Harnesses, Prompts, Datensätze und Modellrevisionen ändern sich. **Lösung:** Den vollständigen Evaluierungsnachweis veröffentlichen statt einer unbelegten Zahl.
- **Benchmark-Erfolg beweist keine Tool-Sicherheit.** Multiple-Choice-Genauigkeit kann Seiteneffekte, Berechtigungen oder Wiederholungen nicht überprüfen. **Lösung:** Aufgezeichnete Tool-Verträge und adversariale Betriebsszenarien separat testen.

## Quellen {#sources}

- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)
- [Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300)
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)

## Siehe auch {#see-also}

- [[frontier-models]]
- [[model-optimization]]
- [[agent-evaluation]]
- [[llm-fine-tuning-practical]]
