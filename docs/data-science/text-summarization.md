---
title: "Text Summarization"
description: "Extractive and abstractive summarization techniques using TF-IDF scoring and transformer models"
---

# Text Summarization

Automatic generation of condensed versions of documents. Two fundamental approaches: extractive (select existing sentences) and abstractive (generate new text). Extractive methods require no training data and work from a single document.

## Extractive vs Abstractive

| Approach | Method | Pros | Cons |
|----------|--------|------|------|
| **Extractive** | Select top-scoring sentences from document | Simple, no training data, faithful to source | Limited to existing sentences, may lack coherence |
| **Abstractive** | Generate new text expressing main ideas | More natural, can paraphrase | Requires seq2seq/transformer models, may hallucinate |

## TF-IDF Sentence Scoring

The simplest extractive method: score sentences by the importance of their words.

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

**Why mean of non-zero values, not sum?**
- Sum biases toward longer sentences (more terms = higher sum)
- Mean normalizes for sentence length
- Non-zero only: the TF-IDF matrix is very sparse. Including zeros would dilute meaningful scores with zero-valued (absent) terms

**Why not mean of the whole vector?**
- Sentences with large vocabulary variety would score low (many zeros dilute the mean)
- We want the sentence with the most important words on average, not the most diverse vocabulary

## TextRank (PageRank for Sentences)

Treats sentences as nodes in a graph. Edge weight = similarity between sentences. High-scoring sentences are those similar to many other important sentences.

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

TextRank is based on Google's PageRank: a sentence is important if it is similar to many other important sentences (recursive definition solved by eigenvector computation / power iteration).

## Selection Strategies

After scoring, multiple ways to select which sentences appear in the summary:

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Top-N sentences | Take N highest-scoring | Fixed-length summaries |
| Top-N words/chars | Take sentences until word/char budget met | Search engine snippets |
| Percentage | Top X% of sentences | Proportional to document length |
| Threshold | Sentences scoring above mean * factor | Variable length, adapts to content |

## Libraries

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

## Gotchas

- **Extractive summaries can be incoherent.** Selected sentences may reference entities introduced in skipped sentences. Post-processing (pronoun resolution) can help but adds complexity.
- **TF-IDF scoring requires enough sentences.** With fewer than 5-6 sentences, the IDF component becomes unstable. For very short texts, simple sentence length + keyword overlap works better.
- **TextRank can select redundant sentences.** Two very similar sentences may both score high. Apply MMR (Maximal Marginal Relevance) to penalize selecting sentences too similar to already-selected ones.

## Cross-References

- [[nlp-text-processing]] - tokenization, TF-IDF fundamentals
- [[attention-mechanisms]] - abstractive summarization uses attention
- [[rnn-sequences]] - seq2seq abstractive models
