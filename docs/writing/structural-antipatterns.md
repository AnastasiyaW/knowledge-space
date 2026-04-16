---
title: Structural Anti-Patterns in AI Text
category: patterns
tags: [writing, ai-detection, structure, antipatterns]
---

# Structural Anti-Patterns in AI Text

AI-generated text has a recognizable "shape" independent of vocabulary. Even after replacing marker words, the structure betrays machine origin. These patterns are harder to fix than word substitution because they require rethinking how content is organized.

## The "AI Shape"

### Symmetrical Paragraph Structure

Every paragraph roughly the same length (4-6 sentences). Every section has 3-5 bullet points. No paragraph is a single sentence. No paragraph runs for 10+ sentences.

**AI text (uniform):**
> Machine learning has transformed many industries. Companies are adopting neural networks for various tasks. These models require significant computational resources. Training typically involves large datasets and specialized hardware. The results can be impressive when properly implemented.
>
> Natural language processing is another key area. Researchers have developed sophisticated models for text analysis. These systems can understand context and generate coherent responses. Applications range from chatbots to translation services. The field continues to evolve rapidly.

Every paragraph: 5 sentences, ~20 words each, same rhythm.

**Human text (uneven):**
> We tried three different architectures before anything worked.
>
> The first attempt used a basic LSTM. Training took 14 hours on a single GPU and the model couldn't handle inputs longer than 512 tokens - which was 60% of our dataset. We burned a week on this before admitting it was a dead end. The attention-based approach that replaced it trained in 3 hours and handled arbitrary lengths, which honestly felt unfair given how much time we'd spent on the LSTM.
>
> Third try: fine-tuned BERT. Worked immediately.

Paragraphs: 1 sentence, 4 sentences, 1 sentence. Rhythm changes. Short paragraphs for emphasis.

### Predictable Transitions

Every paragraph opens with a transition word. The pattern is visible without reading the content:

```text
Moreover, [paragraph]...
Furthermore, [paragraph]...
Additionally, [paragraph]...
In conclusion, [paragraph]...
```

Human text does not need mechanical transitions. Context and flow carry the reader. When transitions appear in human text, they are varied, informal, and infrequent ("But here's the thing," "So," "Turns out," or no transition at all).

### List-ification

AI converts everything into numbered lists or bullet points:
- Each item roughly the same length (10-15 words)
- Items that could be prose but are forced into list format
- Lists where order doesn't matter presented as numbered
- Nested bullets that add no value

**When lists are appropriate:** genuinely parallel items, steps in a sequence, configuration options, comparison tables.

**When they're not:** arguments that build on each other, narratives, explanations where context accumulates.

### The Sandwich Pattern

Every paragraph follows: **broad claim -> supporting detail -> restatement of claim.**

> Machine learning is transforming healthcare. [claim]
> Recent studies show that AI can detect cancer in medical images with 95% accuracy. [detail]
> This demonstrates the significant impact of machine learning on the healthcare industry. [restatement]

Repeated identically across all paragraphs. Human writers state something, develop it, and move on. They don't return to restate the opening claim in each paragraph.

### Header Patterns

AI headers follow predictable templates:
- "Understanding X"
- "The Role of Y"
- "Why Z Matters"
- "Exploring the Power of W"
- "A Comprehensive Guide to V"

Human headers tend to be specific and action-oriented:
- "LSTM Failed, BERT Worked"
- "The 512-Token Limit Problem"
- "Training Costs: $47 vs $3"

## Burstiness Deficit

**Burstiness** = variation in sentence length and structure. The strongest structural signal for detection.

**Human writing burstiness:**
```yaml
Sentence lengths: 5, 23, 8, 41, 12, 3, 28, 15, 6, 35
SD: ~13 words
```

**AI writing burstiness:**
```yaml
Sentence lengths: 18, 22, 19, 21, 17, 20, 23, 18, 21, 19
SD: ~2 words
```

Human text has rhythm. Short sentences punch. Long sentences develop complex ideas with subordinate clauses, digressions, and qualifications that mirror actual thought. AI text runs at a constant 18-22 words per sentence.

## Perplexity Deficit

**Perplexity** = how unpredictable word choices are. The second key metric after burstiness.

- **Human writing**: unexpected verbs, surprising metaphors, unusual word pairings. Spikes of high perplexity (creative choices) mixed with low perplexity (common phrases).
- **AI writing**: consistently low perplexity. Every word is the "safest statistical choice." Technically correct but predictable. No surprises.

Burstiness measures rhythm variation. Perplexity measures vocabulary unpredictability. Both are low in AI text; both need to be high for natural reading.

## Missing Human Markers

What human text has that AI text lacks:

- **Tangential asides** that don't perfectly serve the thesis
- **Strong opinions** stated without hedging ("This approach is wrong")
- **Self-correction** ("Actually, that's not quite right...")
- **Register shifts** - formal to informal and back ("the algorithm converges - or at least it did on my laptop")
- **Incomplete thoughts** left for the reader to complete
- **Emotional inconsistency** - enthusiasm followed by frustration
- **Specific errors and corrections** that show thinking process
- **Personal shortcuts** - assuming reader knowledge without explaining basics

## Tone Anti-Patterns

### Excessive Enthusiasm
Everything is "fascinating," "remarkable," "exciting." Generic superlatives applied to mundane topics. No human is genuinely excited about every aspect of a technical topic equally.

### Hedge-Heavy Writing
- "It's worth noting that..."
- "While it may seem..."
- "One could argue that..."
- Never taking a definitive position. Human experts have opinions and state them directly.

### Balanced-to-a-Fault
"On the one hand... On the other hand..." for every topic, even when one side is clearly stronger. Non-committal conclusions: "It depends on your specific needs and requirements."

### Surface Polish, Nothing Underneath
Per Northeastern/Khoury research on "AI slop" (arxiv 2509.19163) - three defining properties:
1. **Superficial competence** - reads smoothly but says nothing specific
2. **Asymmetric effort** - easy to produce, hard to verify
3. **Mass producibility** - text could apply to any similar topic with minimal changes

## Gotchas

- **Issue:** Fixing individual structural problems (e.g., varying paragraph length) while keeping others (sandwich pattern, no opinions) produces text that still reads as AI. **Fix:** Structure follows thought. Write what you actually think in the order you thought it, then edit for clarity. Don't retrofit human-like variation onto AI structure.
- **Issue:** Adding bullet points to break up AI prose makes it worse, not better - it creates list-ification on top of existing structural problems. **Fix:** If the content is an argument or narrative, keep it as prose. Lists are for genuinely parallel items only.
- **Issue:** "Let me add some humor" produces forced jokes that are another AI tell. **Fix:** Humor in technical writing comes from honest observations, not from inserted quips. "The docs say this takes 5 minutes. It took us three days." is funnier than any constructed joke.

## See Also

- [[ai-text-detection]]
- [[overused-words-phrases]]
- [[natural-writing-style]]
- [[editing-checklist]]
