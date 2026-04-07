---
title: Overused AI Words and Phrases
category: concepts
tags: [writing, ai-detection, vocabulary, reference]
---

# Overused AI Words and Phrases

Comprehensive reference of words and phrases that signal AI-generated text. Organized by detection strength (Tier 1 = immediate red flags, Tier 3 = academic research backing). Based on Liang et al. (2024, arxiv 2406.07016) analysis of 15M+ PubMed abstracts, GitHub compilations, and community resources.

**Core insight:** Unlike previous vocabulary shifts (COVID terms = content nouns), the 2024 excess was almost entirely STYLE words - verbs and adjectives. This is what makes them detectable and domain-independent.

## Tier 1: Immediate Red Flags

Sharpest frequency spikes post-ChatGPT. Any one of these in a short text raises suspicion.

| Word | Excess ratio | Notes |
|------|-------------|-------|
| delves | 25.2x | Poster child of AI slop. Dropped in 2025 after being called out |
| showcasing | 9.2x | |
| underscores | 9.1x | As a verb ("this underscores the importance") |
| crucial | high delta | One of 10 manually-selected marker words (Liang et al.) |
| comprehensive | high delta | Marker word |
| notably | high delta | Marker word |
| enhancing | high delta | Marker word |
| Additionally | high delta | Marker word - always capitalized, paragraph-opener |
| insights | high delta | Marker word |
| particularly | high delta | Marker word |

**The 10 most effective markers** (Liang et al.): across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within.

## Tier 2: Commonly Flagged

Source: GitHub compilations (chrisgherbert, swyxio gists), avoid-gpt-phrases repo.

### Verbs (66% of excess vocabulary)

**Power/action verbs (the worst offenders):**
- delve, dive (into), embark, navigate, uncover, unveil, unlock, unleash
- leverage, harness, foster, bolster, spearhead, champion
- resonate, reverberate, captivate, illuminate, elevate
- underscore, underpin, shed light (on)
- embrace, embody, explore, discover, revolutionize

**What to use instead:**

| AI word | Human alternatives |
|---------|-------------------|
| delve into | look at, examine, check |
| leverage | use |
| harness | use, apply |
| navigate | deal with, handle |
| foster | encourage, support |
| elevate | improve, raise |
| underscore | show, highlight |
| embark on | start, begin |
| unveil | show, release, announce |

### Adjectives

- vibrant, meticulous, intricate, multifaceted, nuanced, holistic
- comprehensive, compelling, profound, pivotal, paramount
- cutting-edge, transformative, unprecedented, remarkable, exceptional
- seamless, innovative, invaluable, noteworthy

**What to use instead:**

| AI word | Human alternatives |
|---------|-------------------|
| comprehensive | full, complete, thorough |
| pivotal | important, key |
| seamless | smooth, easy |
| unprecedented | new, first, unusual |
| invaluable | useful, helpful |
| meticulous | careful, detailed |
| transformative | big, significant (or just describe the change) |

### Nouns and Metaphors

- tapestry, landscape, realm, labyrinth, beacon, crucible
- journey, quest, symphony, treasure trove, mosaic
- interplay, synergy, zeitgeist, framework
- game changer, deep dive

### Transitions and Connectors

**Paragraph openers (high signal when every paragraph starts with one):**
- Moreover, Furthermore, Additionally, Notably
- In conclusion, In summary, It's worth noting that
- That being said, Nonetheless, Subsequently, Therefore
- Important to note, Important to understand

### Filler Phrases

- "A testament to..."
- "It's important to note..."
- "Fear not"
- "Let's dive in"
- "In the realm of..."
- "Little did [they] know"
- "At the end of the day"
- "This serves as a reminder..."
- "Consider a scenario where..."

## Tier 3: Research-Backed (Liang et al.)

Full list from the study analyzing 15M+ PubMed abstracts. These appear at statistically significant excess rates in post-LLM text:

commendable, versatile, profound, fascinating, intriguing, prevalent, proactive, vital, authentic, insightful, beneficial, strategic, instrumental, innovative, meticulous, intricate, notable, invaluable, pivotal, potent, ingenious, cogent, tangible, laudable, lucid, adaptable, admirable, proficient, exceptional, remarkable, seamless, comprehensive, pragmatic, unique, foundational, distinctive, holistic, substantial, compelling, unprecedented, inclusive, cohesive

## Pattern: Bad vs Good Text

**AI-generated:**
> This comprehensive guide delves into the multifaceted landscape of modern web development, showcasing pivotal frameworks that are transforming the industry. Additionally, it underscores the crucial role of performance optimization in delivering seamless user experiences.

**Human-written:**
> I spent three weeks benchmarking React, Vue, and Svelte for our dashboard rewrite. React won on ecosystem, Svelte on bundle size. Here's what I measured and why we picked React anyway.

**AI-generated:**
> Furthermore, it is important to note that leveraging cutting-edge AI technologies can foster innovation and unlock unprecedented opportunities for growth.

**Human-written:**
> We added GPT-4 to our support pipeline in January. Ticket resolution dropped from 4 hours to 40 minutes. The model hallucinates about 8% of the time, so a human still reviews every response.

## Gotchas

- **Issue:** Replacing individual AI words while keeping AI sentence structure produces text that still reads as AI - "the landscape of" becomes "the world of" but the problem is the construction, not the word. **Fix:** Rewrite the sentence from scratch. State the specific thing you mean instead of reaching for a metaphor.
- **Issue:** Some AI marker words are perfectly fine in context - "comprehensive" in "comprehensive test coverage" is normal technical usage. **Fix:** Words become markers when they appear in hedging/filler positions. "A comprehensive analysis reveals" = AI. "We need comprehensive test coverage" = human. Context matters more than the word itself.
- **Issue:** Word lists decay over time as models adapt (e.g., "delve" dropped after being called out). **Fix:** Focus on the underlying pattern - formal Latinate verbs where simple Anglo-Saxon ones work, superlative adjectives without evidence, metaphors instead of specifics.

## See Also

- [[ai-text-detection]]
- [[structural-antipatterns]]
- [[editing-checklist]]
