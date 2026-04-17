---
title: Editing Checklist for Text Quality
category: tools
tags: [writing, editing, checklist, ai-detection, quality]
---

# Editing Checklist for Text Quality

Practical checklist for reviewing text before publication. Covers AI marker detection, structural quality, style, and readability. Use sequentially - fix earlier items first because they affect later ones.

## Phase 1: AI Marker Scan

Run through these first. If multiple items fail, consider rewriting from scratch rather than patching.

- [ ] **No Tier 1 words**: delve, showcase, underscore, crucial, comprehensive, notably, enhancing, Additionally, insights, particularly (see [[overused-words-phrases]])
- [ ] **Max 2 transition openers per page**: Moreover, Furthermore, Additionally, Notably, In conclusion
- [ ] **No filler phrases**: "It's important to note," "A testament to," "In the realm of," "Let's dive in"
- [ ] **No generic metaphors**: tapestry, landscape, realm, journey, beacon, symphony
- [ ] **No unearned superlatives**: transformative, unprecedented, revolutionary, game-changing (unless backed by specific evidence)

### Quick Word Frequency Check

Count per 1000 words:
- Tier 1 markers: **0 is ideal**, 1 is acceptable in long text
- Tier 2 markers: **< 3** total across the piece
- Transition words opening paragraphs: **< 20%** of paragraphs

## Phase 2: Structure Check

- [ ] **Paragraph lengths vary**: at least one 1-2 sentence paragraph AND one 5+ sentence paragraph per 500 words
- [ ] **Sentence lengths vary**: shortest sentence < 8 words, longest > 30 words (measure by counting)
- [ ] **No sandwich pattern**: paragraphs don't follow claim-detail-restatement structure repeatedly
- [ ] **Headers are specific**: no "Understanding X," "The Role of Y," "Why Z Matters" templates
- [ ] **Lists are justified**: bulleted items are genuinely parallel (not prose forced into list format)
- [ ] **Sections are unequal**: the most important section is noticeably longer than others
- [ ] **No symmetric bullet points**: list items vary in length (not all 10-15 words)

## Phase 3: Voice and Authenticity

- [ ] **At least one opinion per 500 words**: the author takes a position, not just presents "both sides"
- [ ] **At least one specific example**: names, numbers, dates, tool versions (not "consider a scenario")
- [ ] **At least one admission**: uncertainty, limitation, something the author doesn't know or got wrong
- [ ] **No hedge stacking**: "It should be noted that while some might argue" = 3 hedges in one sentence
- [ ] **Register is consistent but not uniform**: occasional informal touches in technical writing
- [ ] **Enthusiasm is earned**: superlatives attached to specific evidence, not sprinkled on every topic
- [ ] **No generic conclusions**: "In conclusion, X is important for Y" -> delete or replace with specific next steps

## Phase 4: Content Quality

- [ ] **First paragraph hooks**: reader learns what the article delivers in the first 3 sentences
- [ ] **Code appears early**: first code example within the first 1/3 of the article
- [ ] **Code is complete**: at least one code example is copy-paste runnable (not pseudocode)
- [ ] **Code blocks are language-tagged**: every fence has a language identifier
- [ ] **Links are specific**: point to exact resources, not "learn more about X"
- [ ] **No orphan sections**: every section has >= 2 sentences of content
- [ ] **No redundant summary**: conclusion adds information, doesn't restate the introduction

## Phase 5: Readability

- [ ] **Read aloud**: does it sound like something you'd say to a colleague?
- [ ] **Contractions present**: "it's," "don't," "won't" (unless formal context requires otherwise)
- [ ] **No noun stacking**: "the machine learning model training pipeline optimization process" -> break it up
- [ ] **Active voice dominates**: "We measured" not "Measurements were taken"
- [ ] **Paragraph breaks at topic changes**: no paragraph covers two unrelated points
- [ ] **Subheads every 200-400 words**: a reader skimming can follow the structure

## Automated Checks

Tools that can catch some of these mechanically:

| Check | Tool | What it catches |
|-------|------|----------------|
| AI markers | Custom script / regex | Tier 1-2 word presence |
| Sentence variation | Hemingway Editor | Long/complex sentences, passive voice |
| Readability score | Flesch-Kincaid | Grade level, sentence length average |
| AI detection | GPTZero | Perplexity + burstiness scores |
| Word frequency | Custom script | Repeated words, AI markers per 1000 words |

### Minimal Regex Check

```python
import re

TIER1_MARKERS = [
    r'\bdelves?\b', r'\bshowcas(?:e|ing|es|ed)\b', r'\bunderscore[sd]?\b',
    r'\bcrucial\b', r'\bcomprehensive\b', r'\bnotably\b',
    r'\benhancing\b', r'\badditionally\b', r'\binsights?\b',
    r'\bparticularly\b'
]

FILLER_PHRASES = [
    r"it'?s important to note",
    r"a testament to",
    r"in the realm of",
    r"let'?s dive in",
    r"in today'?s (?:rapidly )?\w+ (?:landscape|world)"]

def scan_text(text: str) -> list[str]:
    findings = []
    for pattern in TIER1_MARKERS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            findings.append(f"Tier 1 marker: {matches[0]} ({len(matches)}x)")
    for pattern in FILLER_PHRASES:
        if re.search(pattern, text, re.IGNORECASE):
            findings.append(f"Filler phrase: {pattern}")
    return findings
```

## Priority by Impact

If you can only do 3 things:

1. **Remove Tier 1 marker words** - highest single-item impact on AI detection scores
2. **Vary sentence length** - strongest structural signal. Read aloud and break monotony
3. **Add one specific example** - a real number, name, or date transforms a paragraph from generic to authentic

## Gotchas

- **Issue:** Running through the checklist mechanically produces "checklist-optimized" text that passes all checks but reads as artificial because the changes are superficial patches. **Fix:** Use the checklist to identify problems, then rewrite the flagged sections from scratch. The checklist diagnoses; you fix by rewriting, not by search-and-replace.
- **Issue:** Editing someone else's text (or your own AI-assisted draft) for authenticity markers while preserving their voice is much harder than writing from scratch. **Fix:** Keep the structure and key points from the draft, but rewrite each section in your own words from memory. If you can't rewrite it from memory, you don't understand it well enough to publish it.
- **Issue:** Checklist fatigue - checking 25+ items per article becomes a chore and items get skipped. **Fix:** Do Phase 1 (AI markers) on every piece. Phases 2-5 only on important publications. Phase 1 alone catches 80% of obvious AI tells.

## See Also

- [[ai-text-detection]]
- [[overused-words-phrases]]
- [[structural-antipatterns]]
- [[natural-writing-style]]
