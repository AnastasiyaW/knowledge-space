---
title: "Empfehlungssysteme"
category: techniques
tags: [data-science, ml, recommendations, collaborative-filtering, ranking]
level: 2
source_sha256: 5789620a610091e73e84a8e05e94b7093ad7aed0bf8d6d408faf4ccb09dbed2c
translation: machine
translated_at: '2026-10-24'
---
# Empfehlungssysteme {#recommender-systems}

Vorhersage von Nutzerpräferenzen und Ranking von Objekten. Von einfachem Collaborative Filtering bis zu Deep-Learning-Ansätzen. Die Evaluation erfolgt anders als bei Standard-Klassifikation/Regression.

## Ansätze {#approaches}

### Collaborative Filtering {#collaborative-filtering}
Basiert auf Nutzerverhaltensmustern. „Nutzer, die X mochten, mochten auch Y."

**User-based**: ähnliche Nutzer finden und empfehlen, was diese mochten.
**Item-based**: Objekte finden, die denen ähnlich sind, die der Nutzer bereits mochte.

**Matrix Factorization**: Zerlegung der Nutzer-Objekt-Interaktionsmatrix in latente Faktoren.
```yaml
R ~ U * V^T
R: user-item matrix (sparse)
U: user latent factors (n_users x k)
V: item latent factors (n_items x k)
```

### Content-Based {#content-based}
Empfiehlt Objekte, die denen ähneln, mit denen der Nutzer zuvor interagiert hat, basierend auf Objektmerkmalen (Genre, Beschreibung, Tags).

### Hybrid {#hybrid}
Kombiniert Collaborative und Content-Based Ansätze. Die meisten Produktivsysteme verwenden hybride Ansätze.

## Evaluation {#evaluation}

### Offline-Metriken {#offline-metrics}

| Metrik | Beschreibung |
|--------|-------------|
| precision@k | Anteil relevanter Objekte in den Top-k-Empfehlungen |
| recall@k | Anteil aller relevanten Objekte, die in den Top-k gefunden wurden |
| mAP@k | Mittlere Average Precision über alle Nutzer |
| nDCG@k | Positionsgewichtete Relevanz |
| Hit Rate | Anteil der Nutzer, die mindestens eine relevante Empfehlung erhielten |

**nDCG-Formel:**
DCG@k = sum_i (2^relevance_i - 1) / log2(i + 1)
nDCG = DCG / ideal_DCG

### Online-Metriken (A/B-Test) {#online-metrics-ab-test}
- CTR (Click-through-Rate)
- Sitzungsdauer
- Anzahl konsumierter Objekte
- Retention (Rückkehr am nächsten Tag?)
- Umsatz pro Nutzer

### Evaluationspipeline {#evaluation-pipeline}
1. **Offline**: Train/Test-Split, Berechnung der Ranking-Metriken
2. **A/B-Test**: Deployment auf eine Nutzerteilmenge, Messung der Geschäftsmetriken
3. **Analyse**: Prüfung der Gültigkeit der Gruppenaufteilung, Berechnung der Hitrate

**Gotcha**: Empfehlungslogs und Klicklogs liegen in getrennten Tabellen. Das Verknüpfen erfordert eine Zeitnähe-Zuordnung (Klicks innerhalb von ca. 1 Stunde, passende user_id und item_id).

## Cold-Start-Problem {#cold-start-problem}

- **Neuer Nutzer**: keine Interaktionshistorie. Verwenden: beliebte Objekte, demografiebasiert, inhaltsbasiert
- **Neues Objekt**: keine Nutzerinteraktionen. Verwenden: Inhaltsmerkmale, Ähnlichkeit der Metadaten

## Implizites vs. explizites Feedback {#implicit-vs-explicit-feedback}

- **Explizit**: Bewertungen, Likes (selten, verzerrt hin zu starken Meinungen)
- **Implizit**: Klicks, Aufrufe, Käufe, Verweildauer (reichlich vorhanden, verrauscht)

Die meisten realen Systeme nutzen implizites Feedback. „Keine Interaktion" sollte sorgfältig interpretiert werden – sie ist nicht zwingend negativ.

## Gotchas {#gotchas}
- Offline-Metriken korrelieren nicht immer mit Online-Geschäftsmetriken – immer per A/B-Test prüfen
- Popularitätsbias: Beliebte Objekte sind leicht zu empfehlen, Long-Tail-Objekte nur schwer sichtbar zu machen
- Filterblasen: Empfehlungen werden zunehmend eng ohne gezielte Diversitätsinjektion
- Evaluation mit implizitem Feedback ist heikel – fehlende Daten ≠ negative Präferenz

## Siehe auch {#see-also}
- [[model-evaluation]] - allgemeines Metrik-Framework
- [[unsupervised-learning]] - Matrix Factorization, SVD
- [[hypothesis-testing]] - A/B-Tests für Empfehlungen
- [[math-linear-algebra]] - SVD für Matrix Factorization
