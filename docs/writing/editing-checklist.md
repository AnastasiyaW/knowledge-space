---
title: Editing Checklist for Text Quality
description: Preserve facts and technical meaning while improving clarity, structure, and publication readiness.
category: tools
tags: [writing, editing, checklist, verification, quality]
---

# Editing Checklist for Text Quality

Use this checklist to improve a document without changing what its evidence
supports. Scope checked 2026-09-06: technical references, tutorials, analyses,
and incident narratives, including AI-assisted drafts.

An unfamiliar word or an even sentence rhythm is not a factual defect.
Prioritize correctness and the reader's task over detector scores or style quotas.

## Preserve the Claim Before Editing Its Wording

Keep the original source and draft available during revision. For material
claims, identify the evidence and the exact boundary of the statement.

| Protected element | Unsafe edit | Required check |
|---|---|---|
| Count and denominator | Turn 12 of 40 checked records into 12 successful records | Preserve what was counted and what remains unchecked |
| Historical date | Replace a dated observation with “currently” | Retain the date unless new evidence supports an update |
| Modality | Turn “may recover” into “will recover” | Preserve uncertainty and conditions |
| Negation | Drop “not” while shortening a sentence | Compare the proposition, not only matching keywords |
| Units and versions | Remove a unit or version as visual clutter | Keep the conditions needed to interpret the result |
| Quotation or personal experience | Invent “we tested” to make prose sound authentic | Use only supplied testimony, clearly attributed |
| Technical identifier | Rename an API or flag for smoother prose | Check the exact spelling against the relevant source |

Unknown quantities remain unknown. A labeled hypothetical example is acceptable
when it serves the reader, but it must not masquerade as an observed result.

## Choose the Structure for the Reader's Task

| Document | What must be easy to find | What is not compulsory |
|---|---|---|
| Reference | Contract, parameters, constraints, version, failure modes | Anecdote, dramatic opening, personal opinion |
| Tutorial | Prerequisites, runnable sequence, expected result, recovery | A benchmark or invented project history |
| Analysis | Question, evidence, comparison criteria, limitations | Equal-sized sections or a predetermined verdict |
| Incident narrative | Observed failure, cause, intervention, verification | A tidy success story when recovery is incomplete |

Remove repetition when it obscures these elements. Do not stretch a paragraph
or add a rhetorical question merely to make the document appear less regular.
The [Google developer documentation tone guide](https://developers.google.com/style/tone)
supports clear, direct prose suited to the reader; it does not prescribe such quotas.

## Review in Order of Consequence

1. Check unsupported or contradictory claims and material omissions.
2. Check whether the reader can carry out the intended task.
3. Check examples, identifiers, links and relevant version conditions.
4. Improve ambiguous wording and unnecessary repetition.
5. Apply the requested house style without altering the first four results.

A useful editorial finding identifies the passage, explains its consequence,
and gives a correction consistent with the available evidence. “Sounds like AI”
does not specify an actionable technical defect.

## Verify Examples and Completion Claims

If a document includes code, test the stated runnable boundary with the named
runtime and dependencies. Label an illustrative fragment as such; do not imply
that an omitted service, fixture, credential or model has been exercised.

Keep these different claims separate:

- Source inspection: a recommendation or code path was reviewed.
- Fixture check: the supplied example passed a bounded test.
- Installation check: the intended files or configuration reached the target.
- Consumer check: the intended tool or reader loaded the delivered result.
- Product result: the requested real workflow completed under its actual conditions.

A green fixture does not upgrade the final item. Likewise, a valid article
source or successful Git push is not proof that readers can see the new page.

## Use Automation for Narrow Assertions

Automated checks can identify broken links, malformed markup, changed numbers,
or missing protected identifiers. Their result is limited to those assertions.

A number comparison cannot detect every change of meaning: “12 failed” and
“12 passed” share a number. Retain a semantic review of the claim and its source.
A prose linter's flag should prompt inspection, not automatic word replacement.

Do not use a detector score as an editorial acceptance condition. The primary
study on [non-native English detector bias](https://arxiv.org/abs/2304.02819)
documents limitations in its evaluated detectors and samples; it does not
establish a universal test of current authorship.

## Stop When the Requested Document Is Ready

Once material defects are resolved and the requested checks pass, stop
cosmetic revision. Record a no-change review when appropriate. Continue any
remaining requested publication or delivery step; reviewing the text alone
does not finish a request to publish it.

## Gotchas

- **Invented specificity:** a quota for numbers or anecdotes creates pressure to
  supply unsupported facts. Remove the quota, not the uncertainty.
- **Historical claims become current:** replacing a date with “now” silently
  changes its truth conditions. Retain the source date or obtain new evidence.
- **Endless editorial passes:** each pass finds a new personal preference.
  Reopen only a material defect or a changed acceptance condition.
- **Rewriting from memory:** source conditions disappear during a fluent rewrite.
  Compare the edited claim with the actual source, not recollection.

## See Also

- [[ai-text-detection]]
- [[technical-article-structure]]
- [[agent-evaluation]]
