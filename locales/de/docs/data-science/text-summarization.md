---
title: "Textzusammenfassung"
description: "Extraktive und abstraktive Zusammenfassungsverfahren mit TF-IDF-Bewertung und Transformer-Modellen"
level: 4
source_sha256: 08186e83314c09af32c4c1cec4fe7ef3e4f032392779d1b8919d6df03dd7f6b4
translation: machine
translated_at: '2026-10-24'
---
# Textzusammenfassung {#text-summarization}

Automatische Erzeugung verdichteter Versionen von Dokumenten. Zwei grundlegende Ansätze: extraktiv (bestehende Sätze auswählen) und abstraktiv (neuen Text erzeugen). Extraktive Verfahren benötigen keine Trainingsdaten und arbeiten auf Basis eines einzelnen Dokuments.

## Extraktiv vs. Abstraktiv {#extractive-vs-abstractive}

| Ansatz | Methode | Vorteile | Nachteile |
|--------|---------|----------|-----------|
| **Extraktiv** | Hochbewertete Sätze aus dem Dokument auswählen | Einfach, keine Trainingsdaten, treu zur Quelle | Auf bestehende Sätze beschränkt, kann an Kohärenz fehlen |
| **Abstraktiv** | Neuen Text erzeugen, der die Kernaussagen wiedergibt | Natürlicher, kann paraphrasieren | Erfordert Seq2seq-/Transformer-Modelle, kann halluzinieren |

## TF-IDF-Bewertung von Sätzen {#tf-idf-sentence-scoring}

Die einfachste extraktive Methode: Sätze werden anhand der Bedeutung ihrer Wörter bewertet.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk

def summarize_tfidf(text, top_n=3):
    # Step 1: Split into sentences
    sentences = nltk.sent_tokenize(text)

    # Step 2: Build TF-IDF matrix (sentences = documents)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Step 3: Score each sentence = mean of non-zero TF-IDF values
    scores = []
    for i in range(tfidf_matrix.shape[0]):
        row = tfidf_matrix[i].toarray().flatten()
        non_zero = row[row > 0]
        score = non_zero.mean() if len(non_zero) > 0 else 0
        scores.append(score)

    # Step 4: Select top sentences (maintain original order)
    ranked_idx = np.argsort(scores)[-top_n:]
    ranked_idx = sorted(ranked_idx)  # preserve document order

    return ' '.join([sentences[i] for i in ranked_idx])
```

**Warum Mittelwert der Nicht-Null-Werte statt Summe?**
- Die Summe begünstigt längere Sätze (mehr Terme = höhere Summe)
- Der Mittelwert normalisiert nach Satzlänge
- Nur Nicht-Null-Werte: Die TF-IDF-Matrix ist sehr dünn besetzt. Null-Werte einzubeziehen würde aussagekräftige Bewertungen mit Null-Werten (nicht vorhandenen Termen) verwässern

**Warum nicht der Mittelwert des gesamten Vektors?**
- Sätze mit großer Vokabularvielfalt würden niedrig bewertet (viele Nullen verwässern den Mittelwert)
- Gesucht ist der Satz mit im Durchschnitt wichtigsten Wörtern, nicht der mit der vielfältigsten Wortwahl

## TextRank (PageRank für Sätze) {#textrank-pagerank-for-sentences}

Sätze werden als Knoten eines Graphen betrachtet. Kantengewicht = Ähnlichkeit zwischen Sätzen. Hoch bewertete Sätze sind solche, die vielen anderen wichtigen Sätzen ähneln.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk

def textrank_summarize(text, top_n=3, damping=0.85, iterations=50):
    sentences = nltk.sent_tokenize(text)
    n = len(sentences)

    # Build similarity matrix
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(sentences)
    sim_matrix = cosine_similarity(tfidf)

    # Normalize rows (transition probabilities)
    for i in range(n):
        row_sum = sim_matrix[i].sum()
        if row_sum > 0:
            sim_matrix[i] /= row_sum

    # Power iteration (PageRank)
    scores = np.ones(n) / n
    for _ in range(iterations):
        scores = (1 - damping) / n + damping * sim_matrix.T @ scores

    # Top sentences in original order
    top_idx = sorted(np.argsort(scores)[-top_n:])
    return ' '.join([sentences[i] for i in top_idx])
```

TextRank basiert auf Googles PageRank: Ein Satz ist wichtig, wenn er vielen anderen wichtigen Sätzen ähnelt (rekursive Definition, gelöst über Eigenvektorberechnung bzw. Power Iteration).

## Auswahlstrategien {#selection-strategies}

Nach der Bewertung gibt es mehrere Möglichkeiten, auszuwählen, welche Sätze in der Zusammenfassung erscheinen:

| Strategie | Beschreibung | Anwendungsfall |
|-----------|--------------|----------------|
| Top-N-Sätze | N höchstbewertete Sätze übernehmen | Zusammenfassungen fester Länge |
| Top-N-Wörter/Zeichen | Sätze übernehmen, bis das Wort- bzw. Zeichenbudget erreicht ist | Snippets in Suchmaschinen |
| Prozentsatz | Oberste X % der Sätze | Proportional zur Dokumentlänge |
| Schwellenwert | Sätze mit Bewertung über Mittelwert * Faktor | Variable Länge, passt sich dem Inhalt an |

## Bibliotheken {#libraries}

```python
# sumy: multiple algorithms
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

parser = PlaintextParser.from_string(text, Tokenizer("english"))
summarizer = TextRankSummarizer()
summary = summarizer(parser.document, sentences_count=3)

# gensim (older versions)
from gensim.summarization import summarize  # deprecated in gensim 4+
summary = summarize(text, word_count=100)
```

## Stolpersteine {#gotchas}

- **Extraktive Zusammenfassungen können inkohärent sein.** Ausgewählte Sätze können sich auf Entitäten beziehen, die in übersprungenen Sätzen eingeführt wurden. Nachbearbeitung (Pronomenauflösung) kann helfen, erhöht aber die Komplexität.
- **TF-IDF-Bewertung benötigt genügend Sätze.** Bei weniger als 5–6 Sätzen wird die IDF-Komponente instabil. Für sehr kurze Texte funktionieren einfache Satzlänge und Schlüsselwortüberlappung besser.
- **TextRank kann redundante Sätze auswählen.** Zwei sehr ähnliche Sätze können beide hoch bewertet werden. MMR (Maximal Marginal Relevance) anwenden, um die Auswahl von Sätzen zu bestrafen, die bereits gewählten zu ähnlich sind.

## Querverweise {#cross-references}

- [[nlp-text-processing]] - Tokenisierung, TF-IDF-Grundlagen
- [[attention-mechanisms]] - Abstraktive Zusammenfassung nutzt Attention
- [[rnn-sequences]] - Seq2seq-Modelle für abstraktive Zusammenfassung
