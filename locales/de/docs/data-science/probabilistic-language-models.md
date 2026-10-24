---
title: "Probabilistische Sprachmodelle"
description: "N-Gramm-Modelle, Glättungsverfahren und Perplexitätsbewertung für Textgenerierung und NLP-Grundlagen"
level: 3
source_sha256: 6d700379aa37a3a7e90e9c100a55b7f513f602fd9ab1d3b2e70a005899808a16
translation: machine
translated_at: '2026-10-24'
---
# Probabilistische Sprachmodelle {#probabilistic-language-models}

Statistische Modelle, die Wortfolgen Wahrscheinlichkeiten zuweisen. Grundlage für Textgenerierung, Rechtschreibkorrektur, Spracherkennung und das Brechen von Chiffren. Das Verständnis von N-Gramm-Modellen ist Voraussetzung, um zu verstehen, warum Transformer so einen grundlegenden Wandel gebracht haben.

## N-Gramm-Modelle {#n-gram-models}

Ein N-Gramm-Sprachmodell schätzt die Wahrscheinlichkeit des nächsten Wortes gegeben die vorherigen (n-1) Wörter:

- **Unigramm**: P(w) – Worthäufigkeit, ohne Kontext
- **Bigramm**: P(w_i | w_{i-1}) – ein Wort Kontext
- **Trigramm**: P(w_i | w_{i-2}, w_{i-1}) – zwei Wörter Kontext

```python
from collections import Counter, defaultdict

def build_bigram_model(corpus):
    """Build bigram probabilities from tokenized corpus."""
    bigram_counts = Counter()
    unigram_counts = Counter()

    for sentence in corpus:
        tokens = sentence.lower().split()
        for i in range(len(tokens)):
            unigram_counts[tokens[i]] += 1
            if i > 0:
                bigram_counts[(tokens[i-1], tokens[i])] += 1

    # P(w2 | w1) = count(w1, w2) / count(w1)
    model = defaultdict(dict)
    for (w1, w2), count in bigram_counts.items():
        model[w1][w2] = count / unigram_counts[w1]

    return model
```

## Satzwahrscheinlichkeit {#sentence-probability}

Die Wahrscheinlichkeit eines Satzes ist das Produkt der bedingten Wahrscheinlichkeiten:

```bash
P("the cat sat") = P(the) * P(cat|the) * P(sat|cat)
```

In der Praxis verwendet man Logarithmen der Wahrscheinlichkeiten, um Underflow zu vermeiden:

```python
import math

def sentence_log_prob(sentence, model):
    tokens = sentence.lower().split()
    log_prob = 0
    for i in range(1, len(tokens)):
        prev, curr = tokens[i-1], tokens[i]
        prob = model.get(prev, {}).get(curr, 1e-10)  # smoothing
        log_prob += math.log(prob)
    return log_prob
```

Höhere Log-Wahrscheinlichkeit = Satz ist wahrscheinlicher echtes Englisch. Diese Erkenntnis ist der Kern der Chiffre-Entschlüsselung und der Erkennung von Artikel-Spinning.

## Chiffre-Entschlüsselung mit Sprachmodellen {#cipher-decryption-with-language-models}

Eine Substitutionschiffre ersetzt jeden Buchstaben durch einen anderen. Um sie ohne Schlüssel zu brechen:

1. Ein Sprachmodell der Zielsprache erstellen (Bigramme oder Trigramme auf Zeichenebene)
2. Einen genetischen/evolutionären Algorithmus verwenden, um Kandidaten für Entschlüsselungsschlüssel weiterzuentwickeln
3. Jeden Kandidaten anhand der Sprachmodell-Wahrscheinlichkeit des entschlüsselten Textes bewerten
4. Die besten Kandidaten auswählen und mutieren, dann wiederholen

```python
import random
import string

def fitness(decrypted_text, language_model):
    """Score how 'English-like' the decrypted text is."""
    return sentence_log_prob(decrypted_text, language_model)

def mutate(key):
    """Swap two random letter mappings."""
    key = list(key)
    i, j = random.sample(range(26), 2)
    key[i], key[j] = key[j], key[i]
    return ''.join(key)

# Evolutionary loop
population = [random_key() for _ in range(pool_size)]
for epoch in range(num_epochs):
    scored = [(fitness(decrypt(cipher, k), lm), k) for k in population]
    scored.sort(reverse=True)
    parents = [k for _, k in scored[:top_n]]
    population = [mutate(random.choice(parents)) for _ in range(pool_size)]
```

Der genetische Algorithmus durchsucht den Schlüsselraum (26! Permutationen) mittels Mutation und Selektion, geleitet durch den Bewertungswert des Sprachmodells.

## Artikel-Spinning und seine Erkennung {#article-spinning-and-detection}

Artikel-Spinning ersetzt Wörter durch Synonyme, um „einzigartige“ Inhalte zu erzeugen. Eine Kontextprüfung auf Trigrammbasis erkennt schlechte Ersetzungen:

| Original | Naive Ersetzung | Problem |
|----------|-----------|---------|
| quantum **gate** | quantum **door** | „gate“ = Logikgatter, nicht physisches Gatter |
| complex **Hilbert space** | complicated **Hilbert space** | „complex“ = komplexe Zahlen, nicht Schwierigkeit |

Einfache Synonymersetzung ohne Kontext scheitert, weil viele Wörter domänenspezifische Bedeutungen haben. Kontextbewusste Modelle (Deep Learning) schneiden besser ab, doch selbst eine Prüfung auf Trigrammebene fängt die gravierendsten Fehler ab.

## Von Markow-Modellen zu PageRank {#markov-models-to-pagerank}

N-Gramm-Sprachmodelle sind Markow-Ketten: Der nächste Zustand hängt nur von den vorherigen N-1 Zuständen ab. Dasselbe Prinzip liegt zugrunde:

- **PageRank**: Webseiten als Zustände, Links als Übergänge. Stationäre Verteilung = Seitenbedeutung
- **TextRank**: Sätze als Zustände, Ähnlichkeit als Übergangswahrscheinlichkeit
- **Hidden Markov Models (HMM)**: für Spracherkennung, POS-Tagging, Analyse biologischer Sequenzen

## Historischer Kontext {#historical-context}

- 1900er: Andrei Markow wendete Kettenmodelle auf Vokal-/Konsonantenmuster im russischen Text an
- 1948: Claude Shannon nutzte Markow-Modelle zur Textgenerierung in seiner grundlegenden Arbeit zur Informationstheorie
- 2000er: HMMs dominierten die Spracherkennung, bis Deep Learning sie ablöste
- Heute: Transformer haben N-Gramm-Modelle für die meisten NLP-Aufgaben ersetzt, doch N-Gramm-Modelle bleiben nützlich für:
  - Tastatur-Vorhersage (mobil)
  - Rechtschreibkorrektur
  - Spracherkennung (Language Detection)
  - Umgebungen mit geringen Ressourcen

## Fallstricke {#gotchas}

- **Glättung ist unverzichtbar.** Ungesehene N-Gramme erhalten Wahrscheinlichkeit null, wodurch die Wahrscheinlichkeit des gesamten Satzes null wird. Laplace-Glättung (Add-1), Kneser-Ney oder Backoff sind gängige Lösungen.
- **Zeichenbasierte Modelle sind für die Chiffre-Entschlüsselung besser** als wortbasierte Modelle. Wortbasierte Modelle haben eine dünne Abdeckung; zeichenbasierte Bigramm- oder Trigramm-Modelle erfassen die Struktur der Sprache für diese Aufgabe robuster.
- **Artikel-Spinning IST erkennbar.** Schon einfache Bigramm-Analysen markieren unnatürliche Wortkombinationen. Ausgereiftere Plagiatswerkzeuge nutzen Dokumentähnlichkeit in Kombination mit Perplexitätsanalyse.

## Querverweise {#cross-references}

- [[nlp-text-processing]] - Tokenisierung, TF-IDF, Textvorverarbeitung
- [[text-summarization]] - TextRank verwendet Markow-ketten-ähnliche Bewertung
- [[bayesian-methods]] - probabilistische Grundlagen
- [[monte-carlo-simulation]] - Stichproben aus Wahrscheinlichkeitsverteilungen
