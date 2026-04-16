---
description: "CWE vulnerability reference cards structured for AI-assisted code review. Root causes, trigger conditions, detection heuristics, and fix patterns for CWE Top 25."
date: 2026-04-16
tags:
  - security
  - cwe
  - vulnerability-detection
level: Advanced
---

# CWE Vulnerability Reference Cards

Structured knowledge entries for AI-assisted vulnerability detection, following the Vul-RAG approach (ACM TOSEM 2025). Each entry covers: functional semantics, root cause, trigger conditions, detection heuristics, and fixing patterns.

Designed for consumption by security review agents. Each card is self-contained - an agent reading one card has everything needed to detect that vulnerability class.

Based on CWE Top 25 Most Dangerous Software Weaknesses (2024).

## Entries

### Injection & Input Validation

- CWE-079: XSS - Cross-site Scripting (Rank 1)
- [[cwe-089-sql-injection]] - SQL Injection (Rank 3)
- [[cwe-918-ssrf]] - Server-Side Request Forgery (Rank 19)
- CWE-434: File Upload - Unrestricted File Upload (Rank 10)
- [[cwe-502-deserialization]] - Deserialization of Untrusted Data (Rank 16)

### Memory Safety

- [[cwe-787-oob-write]] - Out-of-bounds Write (Rank 2)
- CWE-125: Out-of-Bounds Read - Out-of-bounds Read (Rank 6)
- CWE-416: Use After Free - Use After Free (Rank 8)
- CWE-190: Integer Overflow - Integer Overflow (Rank 23)

### Resource Management

- [[cwe-400-resource-consumption]] - Uncontrolled Resource Consumption (Rank 24)

## Methodology

Each entry uses the Vul-RAG knowledge structure:

1. **Functional Semantics** - what the vulnerable code does (behavioral pattern, not syntax)
2. **Root Cause** - why the vulnerability exists (fundamental design flaw)
3. **Trigger Conditions** - when exploitable and when NOT (false positive indicators)
4. **Detection Heuristics** - what to look for during review (source-sink patterns, missing checks)
5. **Fixing Patterns** - how to fix (pattern templates) and anti-patterns (wrong fixes)

This structure outperforms code-example RAG by +16-24% accuracy (Vul-RAG, ACM TOSEM 2025).
