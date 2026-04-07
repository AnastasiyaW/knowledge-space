---
title: AI Text Detection
category: concepts
tags: [writing, ai-detection, nlp, research]
---

# AI Text Detection

Methods and research for identifying AI-generated text. Detection relies on statistical markers (word frequency shifts), structural patterns (low burstiness), and stylistic tells (hedge-heavy, opinion-free prose). No single method is foolproof - but combining signals yields high accuracy.

## Key Research: Liang et al. (2024)

Study: "Delving into LLM-assisted writing in biomedical publications through excess vocabulary" (arxiv 2406.07016). Analyzed 15M+ PubMed abstracts.

**Findings:**
- 280 excess style words identified in 2024 publications
- 10-13.5% of abstracts showed LLM processing markers, up to 40% in some subfields
- The excess was almost entirely **style words** (verbs, adjectives) - not content nouns
- Previous vocabulary shifts (e.g., COVID-related) were content nouns - this shift is qualitatively different
- Makes detection feasible because style words are content-independent

**The 10 most effective marker words** (Liang et al.): across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within.

**Top excess ratios:**

| Word | Excess ratio |
|------|-------------|
| delves | 25.2x |
| showcasing | 9.2x |
| underscores | 9.1x |
| crucial | high delta |
| comprehensive | high delta |
| notably | high delta |

## Detection Dimensions

### 1. Vocabulary Analysis

Count frequency of known AI marker words per 1000 words. Compare against pre-2023 baselines for the same genre. High concentration of Tier 1 markers (see [[overused-words-phrases]]) is the strongest single signal.

**Key finding from Liang et al.:** 66% of excess vocabulary were verbs. Adjectives were the second largest category. This is because LLMs default to the statistically safest word choices, which tend to be formal, Latinate verbs and superlative adjectives.

### 2. Burstiness (Sentence Length Variation)

**Burstiness** = variation in sentence length and complexity across a text.

- **Human writing**: naturally mixes short punchy sentences (5 words) with long complex ones (40+ words). Rhythm changes based on emotion, emphasis, pacing
- **AI writing**: sentences cluster around medium length (15-25 words). Monotonous tempo throughout

Measure: standard deviation of sentence word counts. Human text: high SD. AI text: low SD.

### 3. Perplexity (Word Predictability)

**Perplexity** = how unpredictable word choices are when measured against a language model.

- **Human writing**: spikes of high perplexity (creative, unexpected choices) mixed with low perplexity (common phrases)
- **AI writing**: consistently low perplexity. Every word is the "safest statistical choice." Technically correct but flat

Tools like GPTZero use perplexity and burstiness together as primary signals.

### 4. Structural Fingerprinting

AI text has a recognizable "shape" (see [[structural-antipatterns]]):
- Symmetrical paragraph lengths
- Predictable transition words opening each paragraph
- Every section follows introduction-body-conclusion
- Lists with uniform item lengths

### 5. Voice and Tone Markers

- No personal opinions or first-person experience
- Excessive hedging ("It's worth noting that...")
- Balanced-to-a-fault ("On one hand... on the other hand...")
- Perfect grammar throughout (humans make strategic informal choices)
- Generic enthusiasm without specific cause

## Detection Tools

| Tool | Method | Notes |
|------|--------|-------|
| GPTZero | Perplexity + burstiness | Most widely used, per-sentence scoring |
| Originality.ai | ML classifier | Subscription, batch scanning |
| Turnitin AI | Integrated with plagiarism check | Academic institutions |
| Binoculars | Zero-shot, cross-model perplexity | Research tool, no fine-tuning needed |
| Sber GigaCheck | Russian-focused, 94.7% accuracy | Best for Russian text |

## Co-Evolution Effect

From arxiv 2502.09606: "delve" dropped sharply in LLM output after being publicly called out as an AI marker. LLMs and humans co-evolve - as detection patterns are identified, model outputs shift. Detection must track moving targets.

**Implication:** Static word lists decay in effectiveness. Structural and statistical methods (burstiness, perplexity) are more durable than vocabulary lists.

## Practical Detection Workflow

1. **Scan vocabulary** - count Tier 1/2 marker words per 1000 words (see [[overused-words-phrases]])
2. **Measure burstiness** - calculate SD of sentence lengths. SD < 5 words is suspicious
3. **Check structure** - uniform paragraph lengths, predictable transitions, list-heavy
4. **Read for specificity** - AI text lacks names, dates, exact numbers, personal anecdotes
5. **Verify tone** - no opinions, no humor, no self-correction, no emotional shifts

**Threshold heuristic:** 3+ signals from different dimensions = high confidence AI-generated.

## Gotchas

- **Issue:** Heavily edited AI text passes vocabulary checks because marker words are replaced. **Fix:** Structural analysis (burstiness, paragraph symmetry) survives surface editing. A text can have zero "delves" and still read as AI due to uniform rhythm.
- **Issue:** Non-native English speakers sometimes trigger false positives because their writing has low burstiness and formal vocabulary. **Fix:** Look for specificity - non-native human writers include personal details, opinions, and domain knowledge that AI text lacks.
- **Issue:** Detection tools give confidence scores, not binary verdicts - a 60% score is not meaningful. **Fix:** Use tools as one input among several. Manual structural + vocabulary analysis is more reliable than any single automated score.

## See Also

- [[overused-words-phrases]]
- [[structural-antipatterns]]
- [[natural-writing-style]]
- [[editing-checklist]]
