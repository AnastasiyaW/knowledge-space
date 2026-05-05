# 4-Layer Content Quality Framework

A systematic approach to technical writing that filters linguistic noise, enforces informational density, aligns structure with reader outcomes, and codifies brand personality.

## Layer 1: Linguistic Anti-Slop
Linguistic "slop" refers to predictable patterns commonly found in synthetic or low-effort technical prose. Removing these markers increases perceived authority and human signal.

### Patterns for Removal
- **The Rule of Three:** Avoid clusters of three adjectives or nouns used to create a false sense of completeness (e.g., "fast, reliable, and scalable").
- **Merism / Fake Ranges:** Eliminate "from X to Y" phrases that cover the entire spectrum without adding specific data (e.g., "from simple scripts to complex architectures").
- **Tautological Synonyms:** Avoid repeating the subject via descriptive placeholders (e.g., using "this specialist" instead of the person's name to avoid repetition).
- **Vague Attribution:** Strip phrases like "according to experts" or "industry reports say" unless a specific, clickable citation is provided.
- **Problem-Future Structure:** Remove the narrative arc that starts with a generic negative and ends with vague optimism.
- **Title-as-Definition:** Do not start articles or sections with "X is a..." definitions for terms the reader is expected to know.
- **Promotional Adjective Clusters:** Remove "stunning," "powerful," "incredible," or "seamless."

## Layer 2: Informational Density (Infostyle)
Mechanical clarity ensures that every sentence provides a unique fact or necessary instruction.

- **The "So What?" Test:** Every statement must result in a concrete conclusion. If a sentence explains a feature without explaining its utility or trade-off, it is discarded.
- **Fact-over-Evaluation:** Replace qualitative assessments with quantitative data.
  - *Weak:* "High-performance data processing."
  - *Strong:* "99.2% of packets processed under 10ms."
- **Zero-Info Sentence Test:** If a sentence can be removed without losing technical meaning, it is deleted.
- **Single-Thought Syntax:** Restrict each sentence to one primary technical idea to prevent cognitive overload.

## Layer 3: Structural Strategy (JTBD)
Structure is determined by the "Job-to-be-Done" (JTBD) framework before the first draft is written.

### The Job Statement
Define the reader's transition using this template:
```text
When [technical situation], I want to [specific motivation/action], 
so I can [measurable outcome/state delta].
```

### Validation Checkpoints
- **Target State Delta:** Identify the specific difference between the reader's knowledge "Before" vs "After."
- **Competing Alternatives:** Address what the reader is currently doing (e.g., manual grep, StackOverflow search) and why this method "hires" the new solution.
- **Section-Level Utility:** Every H2 must move the reader one step closer to the target state. If a section is purely "contextual," it is merged or deleted.

## Layer 4: Tone of Voice (ToV) Codification
ToV is treated as a set of rules extracted from a validated corpus (20-30 high-performing posts) to ensure consistency across multiple authors or automated pipelines.

### Extraction Protocol
1. **Quantitative Metrics:** Measure average sentence length, paragraph depth, emoji frequency, and vocabulary richness (Type-Token Ratio).
2. **Qualitative Markers:** Identify recurring opening patterns, closure styles, and humor thresholds.
3. **Rule Specification:** Define ranges for variables to guide the writing process.

```json
{
  "tov_config": {
    "sentence_length_avg": 12,
    "max_paragraph_lines": 4,
    "formality_level": "technical_peer",
    "prohibited_openers": ["In the world of", "Imagine a scenario"],
    "required_elements": ["code_block", "gotcha_list"]
  }
}
```

## Gotchas
- **Issue:** Strict anti-slop editing can lead to "dry" or robotic text that lacks flow → **Fix:** Use Layer 4 (ToV) to re-introduce specific rhythmic patterns or signature phrasing that doesn't rely on generic AI markers.
- **Issue:** The "So What?" test results in overly long sentences as writers try to pack in utility → **Fix:** Force a hard break between the "Fact" and the "Utility" into two separate, short sentences.
- **Issue:** JTBD statements that are too broad (e.g., "I want to be better at Python") fail to guide the structure → **Fix:** Narrow the job to a single CLI command, a specific config change, or a single architectural decision.

## See Also
- [[llm-writing-antipatterns]]
- [[natural-writing-style]]
- [[technical-article-structure]]
- [[structural-antipatterns]]

