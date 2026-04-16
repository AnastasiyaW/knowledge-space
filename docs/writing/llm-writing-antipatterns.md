---
title: "LLM Writing Anti-Patterns"
description: "Detectable AI text patterns - overused vocabulary, structural anti-patterns, burstiness/perplexity metrics, Russian-specific markers, and humanization checklist."
---

# LLM Writing Anti-Patterns

How to detect and avoid AI-generated text patterns. Covers English vocabulary markers, structural signatures, the burstiness metric, Russian-specific patterns, and practical editing checklist.

## High-Signal English Vocabulary

From analysis of 15M+ PubMed abstracts (Liang et al., arXiv 2406.07016):

### Tier 1: Immediate Red Flags

| Word | Excess ratio | Note |
|------|-------------|------|
| delves | 25.2x | Canonical AI marker, dropped after wide exposure |
| showcasing | 9.2x | |
| underscores | 9.1x | |
| across, additionally, comprehensive | High | Among 10 most effective detection markers |
| crucial, enhancing, insights | High | |
| notably, particularly, within | High | |

**66% of excess AI vocabulary are verbs and adjectives** - not content nouns. This is why AI text is detectable as *style*, not *content*.

### Tier 2: Common Flagged Terms

**Verbs:** delve, dive into, embark, navigate, uncover, unveil, unlock, unleash, leverage, harness, foster, bolster, spearhead, champion, resonate, captivate, illuminate, elevate, underscore, shed light on

**Adjectives:** vibrant, meticulous, intricate, multifaceted, nuanced, holistic, comprehensive, compelling, profound, pivotal, paramount, cutting-edge, transformative, seamless, innovative

**Nouns/Metaphors:** tapestry, landscape, realm, labyrinth, beacon, crucible, interplay, synergy, zeitgeist, game changer, deep dive

**Transitions:** Moreover, Furthermore, Additionally, Notably, In conclusion, In summary, That being said, Subsequently

**Filler:** "A testament to...", "It's important to note...", "Let's dive in", "In the realm of..."

## Structural Anti-Patterns

### The "AI Shape"

- Every paragraph roughly the same length
- Every section has 3-5 bullet points
- Predictable header pattern: "Understanding X", "The Role of Y", "Why Z Matters"
- Every paragraph starts with a transition word
- "In conclusion..." as the inevitable closer

### Burstiness (Most Detectable Metric)

Burstiness = variation in sentence length and structure.

**Human writing:** naturally mixes short punchy sentences with long complex ones. A paragraph might have a 5-word sentence followed by a 40-word one.

**AI writing:** sentences cluster around medium length (15-25 words). Monotonous tempo. Every sentence runs at the same pace.

Burstiness is computable: measure std dev of sentence lengths. AI text has low std dev, human text has high std dev.

### Perplexity

Low perplexity = every word is the "safest statistical choice."

Human writing has spikes of high perplexity (creative choices, unexpected metaphors, unusual word pairings) mixed with low perplexity stretches. AI text is uniformly low-perplexity - technically correct, boring.

### The Core Signature

"Surface polish, nothing underneath" (Northeastern/Khoury research):
- Reads smoothly but says nothing specific
- Verbose yet information-sparse
- Generic frameworks instead of concrete examples
- Could apply to any similar topic

## Tone Anti-Patterns

- **Excessive enthusiasm:** "Fascinating!", "Remarkable!" - every topic treated as equally exciting
- **Hedge-heavy:** "It's worth noting that...", "One could argue that..." - never takes a definitive position
- **Balanced-to-a-fault:** "On the one hand... on the other hand..." even when one side is clearly correct
- **Missing markers:** No personal opinions, no uncertainty expressed naturally, no humor, no self-correction

## Russian-Specific Markers

### Word Markers

**Overused copula verbs:**
- "является" (is) - humans rarely use this in informal/semi-formal writing
- "выступает" / "служит" (serves as)
- "играет важную роль" (plays an important role)

**Favorite constructions:**
- "не просто..., а..." (not just... but...) - ChatGPT's signature Russian phrase
- "мощный" (powerful) - overused adjective
- Deverbal nouns everywhere: привлечение, обеспечение, тестирование

**English calques:** Word order unnatural for Russian, copied from English syntax. Russian allows much freer SVO order - overly rigid word order is suspicious.

### Structural Signs

- Every paragraph starts with a deverbal noun + colon
- Subject-Predicate order everywhere (Russian has freer word order)
- Paragraphs can be rearranged without damage - no logical chain
- Perfect punctuation, zero grammatical irregularities

### Indicator Phrases

- "Я надеюсь, это помогло Вам" (I hope this helped you)
- "Конечно" / "Безусловно" in opening position
- "Вы абсолютно правы" (You are absolutely right)
- "По состоянию на [дата]" (As of [date])

## What Human Writing Actually Looks Like

- **Uneven paragraph lengths** (some 1 sentence, some 10)
- **Strong opinions** stated without hedging
- **Specific examples** with names, dates, numbers - not "consider a scenario where..."
- **Self-correction** ("Actually, that's not quite right...")
- **Register shifts** (formal to informal and back)
- **Tangential asides** that don't perfectly serve the thesis
- **Errors and corrections** that show the thinking process

## Editing Checklist

Before publishing:
- [ ] No Tier 1 words (delve, crucial, comprehensive, etc.)
- [ ] Sentence lengths vary significantly (measure shortest vs longest)
- [ ] At least one personal opinion per 500 words
- [ ] No symmetrical paragraph structure
- [ ] Specific examples with names/numbers/dates
- [ ] At least one admission of uncertainty or limitation
- [ ] No more than 2 transition words per page (Moreover, Furthermore)
- [ ] At least one place where you disagree or take a stance
- [ ] No generic conclusions ("In conclusion, X is important for Y")

**For technical articles specifically:**
1. Lead with the problem you actually had, not a topic overview
2. Include dead ends - "I tried X but it failed because..."
3. Show specific error messages, stack traces, version numbers
4. Use your actual numbers - "took 47 minutes on my M1 MacBook"
5. Disagree with something - take a stance
6. Mention time - "at 2am I realized..."

## Fundamental Difference

**Specificity vs generality.**

Human text is specific: references exact things, takes positions, makes mistakes, shows personality.  
AI text is general: covers all bases, hedges everything, uses the most common phrasings, produces text that could apply to any similar topic.

The specific/general axis is the most reliable single dimension for detection.

## Gotchas

- **AI patterns change after exposure.** "Delve" dropped sharply after being widely called out. LLMs and humans co-evolve - the specific word list will change. The structural and burstiness patterns are more stable.
- **"500 AI words to avoid" blog posts often use the same patterns.** Most lists are AI-generated content about AI-generated content. The academic sources (Liang et al., Northeastern) are more reliable.
- **Russian AI detection differs from English.** The copula verb signal ("является") is much stronger in Russian than "is" in English, because Russian rarely needs a copula. English calque word order is a unique Russian AI signal with no direct English equivalent.

## See Also

- [[natural-writing-style]]
- [[overused-words-phrases]]
- [[ai-text-detection]]
- [[structural-antipatterns]]
