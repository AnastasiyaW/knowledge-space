---
title: "Probabilistic Language Models"
description: "N-gram models, smoothing techniques, and perplexity evaluation for text generation and NLP foundations"
---

# Probabilistic Language Models

Statistical models that assign probabilities to sequences of words. Foundation for text generation, spelling correction, speech recognition, and cipher breaking. Understanding n-gram models is prerequisite for appreciating why transformers were transformative.

## N-gram Models

An n-gram language model estimates the probability of the next word given the previous (n-1) words:

- **Unigram**: P(w) - word frequency, no context
- **Bigram**: P(w_i | w_{i-1}) - one word of context
- **Trigram**: P(w_i | w_{i-2}, w_{i-1}) - two words of context

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

## Sentence Probability

The probability of a sentence is the product of conditional probabilities:

```
P("the cat sat") = P(the) * P(cat|the) * P(sat|cat)
```

In practice, use log probabilities to avoid underflow:

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

Higher log probability = sentence is more likely to be real English. This is the core insight used in cipher decryption and article spinning detection.

## Cipher Decryption with Language Models

A substitution cipher replaces each letter with another. To break it without the key:

1. Build a language model of the target language (character-level bigrams or trigrams)
2. Use a genetic/evolutionary algorithm to evolve candidate decryption keys
3. Score each candidate by the language model probability of the decrypted text
4. Select and mutate top candidates, repeat

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

The genetic algorithm explores the key space (26! permutations) using mutation + selection guided by the language model score.

## Article Spinning and Detection

Article spinning replaces words with synonyms to create "unique" content. Trigram-based context checking catches bad replacements:

| Original | Naive Spin | Problem |
|----------|-----------|---------|
| quantum **gate** | quantum **door** | "gate" = logic gate, not physical gate |
| complex **Hilbert space** | complicated **Hilbert space** | "complex" = complex numbers, not difficulty |

Simple synonym replacement without context fails because many words have domain-specific meanings. Context-aware models (deep learning) perform better, but even trigram-level checking catches the worst errors.

## Markov Models to PageRank

N-gram language models are Markov chains: the next state depends only on the previous N-1 states. This same principle underlies:

- **PageRank**: web pages as states, links as transitions. Stationary distribution = page importance
- **TextRank**: sentences as states, similarity as transition probability
- **Hidden Markov Models (HMM)**: for speech recognition, POS tagging, biological sequence analysis

## Historical Context

- 1900s: Andrei Markov applied chain models to vowel/consonant patterns in Russian text
- 1948: Claude Shannon used Markov models for text generation in his foundational information theory paper
- 2000s: HMMs dominated speech recognition until deep learning
- Modern: transformers replaced n-grams for most NLP tasks, but n-gram models remain useful for:
  - Keyboard prediction (mobile)
  - Spelling correction
  - Language detection
  - Low-resource environments

## Gotchas

- **Smoothing is essential.** Unseen n-grams get zero probability, making entire sentence probability zero. Laplace smoothing (add-1), Kneser-Ney, or backoff are standard solutions.
- **Character-level models are better for cipher decryption** than word-level models. Word-level models have sparse coverage; character-level bigram/trigram models capture the structure of the language more robustly for this task.
- **Article spinning IS detectable.** Even simple bigram analysis flags unnatural word combinations. More sophisticated plagiarism tools use document similarity + perplexity analysis.

## Cross-References

- [[nlp-text-processing]] - tokenization, TF-IDF, text preprocessing
- [[text-summarization]] - TextRank uses Markov-chain-like scoring
- [[bayesian-methods]] - probabilistic foundations
- [[monte-carlo-simulation]] - sampling from probability distributions
