---
title: Technical Article Structure
category: patterns
tags: [writing, technical-writing, article-structure, publishing]
---

# Technical Article Structure

How to structure technical articles that get read, shared, and bookmarked. Based on patterns from high-engagement technical content across platforms. The core principle: lead with the problem you actually had, not a topic overview.

## The Hook-Problem-Solution Pattern

The highest-performing structure for technical articles:

1. **Hook** (1-3 sentences) - the specific situation that made you write this
2. **Context** - what you were trying to do and why existing solutions didn't work
3. **Solution** - what you did, with code and specifics
4. **Results** - what happened, with numbers
5. **Caveats** - what doesn't work, edge cases, limitations
6. **Next steps** - what you'd do differently or what's left to explore

This is NOT the standard "Introduction -> Background -> Method -> Conclusion" academic structure. Technical blog readers want the payoff early and details later.

## Opening Patterns That Work

**Lead with the problem:**
> Our CI pipeline took 47 minutes. Deploys happened twice a day, which meant engineers spent 90+ minutes daily waiting for builds.

**Lead with a surprising result:**
> We deleted 60% of our microservices and reliability improved. Here's why.

**Lead with a failure:**
> I mass-migrated 2M rows to the new schema on Friday at 4pm. The rollback took until Sunday.

**What doesn't work:**
> In today's fast-paced world of software development, continuous integration and continuous deployment (CI/CD) have become essential practices for modern engineering teams. This article explores...

## Code Examples Placement

**Rules:**
- First code example within the first 1/3 of the article
- Use code from your actual project, not generic examples
- Include version numbers, OS, and runtime details
- Show the error/output, not just the input
- Keep individual code blocks under 30 lines - split longer examples

**Good placement pattern:**
```ini
[2-3 paragraphs of context]
[code block showing the problem]
[1-2 paragraphs explaining]
[code block showing the solution]
[paragraph on results]
[code block showing results/benchmarks]
```

**Bad placement pattern:**
```ini
[10 paragraphs of theory]
[massive code block with everything]
[brief conclusion]
```

## Section Breakdown

### For Tutorial/How-To Articles

```ini
# [Specific outcome] with [specific tool]

## The Problem
[2-3 sentences - what wasn't working]
[Error message or screenshot]

## What I Tried First
[Brief dead-end descriptions - shows real experience]

## The Solution
[Step-by-step with code blocks]
[Each step: what to do, why, expected output]

## Gotchas
[Things that broke during implementation]
[Edge cases discovered in production]

## Results
[Before/after metrics]
[Timeline: how long the migration/implementation took]
```

### For Investigation/Debug Articles

```bash
# How We Fixed [specific problem]

## Symptoms
[What was observed - exact error messages, metrics]

## Initial Hypotheses
[What we thought was wrong and why]

## Investigation
[Tools used, commands run, what each revealed]
[Include dead ends - "we checked X but it was fine"]

## Root Cause
[What actually happened]

## Fix
[What we changed, with code diff]

## Prevention
[What we changed to catch this earlier]
```

### For Comparison/Evaluation Articles

```sql
# [Tool A] vs [Tool B] for [specific use case]

## Our Requirements
[Specific criteria, not generic "performance and scalability"]

## Test Setup
[Exact versions, hardware, dataset size]

## Results
[Table with numbers]
[One section per criterion with details]

## Our Choice
[What we picked and why - take a position]

## What We'd Choose Differently For
[Other use cases where the other tool wins]
```

## Optimal Length

- **Sweet spot**: 1200-2000 words (7-10 minute read)
- Short articles (<5 min): high completion rate but less engagement
- Medium articles (5-10 min): best balance of completion and depth
- Long articles (10+ min): lower completion, higher bookmarks
- "Evergreen" tutorials get steady long-term traffic regardless of length

## Formatting Essentials

- **Headers**: H2 for major sections, H3 for subsections. No H4+ in blog posts
- **Code blocks**: always language-tagged, < 30 lines each
- **Images/diagrams**: every 300-500 words for engagement
- **Bold** for key terms on first use, not for emphasis in every paragraph
- **Links**: to specific relevant resources, not "read more about X here"
- **TL;DR**: at the top for long articles, not at the bottom

## Techniques for Authenticity

From analysis of highest-rated technical articles:

1. **Include dead ends** - "I tried X but it failed because..."
2. **Show specific error messages**, stack traces, version numbers
3. **Use your actual numbers** - "took 47 minutes on my M1 MacBook"
4. **Reference specific tools by version** - not "a popular framework"
5. **Disagree with something** - take a stance on a tool or approach
6. **Admit what you don't understand** - "I still don't know why this works"
7. **Use code from your actual project**, not sanitized examples
8. **Mention time** - "at 2am I realized the problem was..."
9. **Include screenshots** of your actual terminal/IDE
10. **Show the before/after** - concrete proof the solution works

## Anti-Patterns

- Starting with "In today's world..." or "X has become increasingly important"
- Explaining basics your audience already knows (know your reader's level)
- Equal space to every section regardless of value
- No code until the second half of the article
- Generic conclusion restating the introduction
- "I hope this was helpful" as a closing

## Gotchas

- **Issue:** Structuring a debug story chronologically ("first I checked A, then B, then C") can be tedious if A and B were dead ends. **Fix:** Lead with the root cause and fix, then explain the investigation. Readers want the answer first, the journey second.
- **Issue:** Including every detail about the setup makes the article inaccessible to readers with different environments. **Fix:** State your exact environment (OS, versions, hardware) once at the top, then focus on the concepts. Link to setup guides rather than embedding them.
- **Issue:** Code examples that work in isolation but not in real projects because imports, configuration, and error handling are omitted. **Fix:** Show complete, runnable code for at least one key example. Mark simplified examples explicitly: "// simplified - see full version at [link]."

## Content Frameworks

### Story Spine (Pixar-adapted)

Maps well to debugging stories and architecture decisions. The "Man in Hole" narrative shape (problem → worse → solved):

```rust
"Once upon a time..." → project context, how things worked
"Every day..."        → the normal state before the problem
"One day..."          → the triggering problem or discovery
"Because of that..."  → failed attempt #1 (include this - it builds trust)
"Because of that..."  → deeper understanding
"Until finally..."    → solution and what changed permanently
```

The "failed attempt" beat is where most technical articles win or lose. Skip it and you get a press release. Include it and you have a story worth reading.

### Problem-Discovery-Solution with Dead Ends

Critical differentiator: failed approaches build trust, save readers time, add narrative tension.

```rust
"We tried X and it failed because Y" > clean success story
```

Readers won't trust an article that has no dead ends. Real engineering has dead ends. If your draft has none, you've edited them out - put them back.

### Learning in Public (Swyx pattern)

Write about what you learn **as** you learn it. Not "expert tutorial" voice - honest process documentation including mistakes. 80% of developers never publish. Just by publishing you're ahead.

Format: write the confusion and the moment it cleared, not just the final answer.

### Practitioner Chronicle

Written from what you **do**, not what you **read**. Reference: Simon Willison (rapid experiments, documents everything), Chip Huyen (bridges research/production), Lilian Weng (deep explainers).

The test: could this article have been written without doing the actual work? If yes, it's a tutorial. If no, it's a chronicle.

### Findings Taxonomy as Article Seeds

During work, tag raw notes with:

- `[DECISION]` → becomes an "Architecture Decisions" article
- `[GOTCHA]` → becomes a "Things I Wish I Knew" article
- `[REUSE]` → becomes a tutorial or guide
- `[STORY]` → becomes a chronicle with narrative arc

### Journalistic SEO

Write answers to specific practitioner questions, not generic topic introductions.

```text
"Why does my RAG pipeline hallucinate on long documents?" ← specific, gets search traffic
"Introduction to RAG"                                     ← no one searches this
```

## Platform-Specific Notes

### Habr

- Audience detects filler instantly
- Headlines: concrete numbers + technical terminology → higher CTR
- Highest engagement: personal experience + technical depth
- **Bookmarks** are the real metric - practical evergreen content
- Anti-patterns: AI-generated text, subtle advertising (flagged by mods)
- First-hour momentum (1000+ views) triggers trending algorithm
- Google Discover is a major traffic source for Habr articles

### Medium / dev.to

- Medium: "sense-making" (explaining WHY something works) > step-by-step tutorials
- dev.to: beginner-friendly, tutorial-heavy, different audience
- Both: show real messy code first, then explain

## Chronicle → Article Pipeline

```text
1. Capture  (during work): tag [DECISION], [GOTCHA], [REUSE], [STORY], screenshot outputs
2. Triage   (weekly): scan for narrative arc (problem → struggle → solution)
3. Outline  (Story Spine): identify the lowest point - that's the article center
4. Draft    write the problem first (hook), then solution (payoff), fill middle
5. Polish   cut ruthlessly, add code blocks/screenshots, write headline LAST
```

## See Also

- [[natural-writing-style]]
- [[publishing-platforms]]
- [[editing-checklist]]
- [[seo-for-articles]]
