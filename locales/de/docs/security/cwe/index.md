---
description: "CWE-Schwachstellen-Referenzkarten, strukturiert für KI-gestützte Code-Reviews. Grundursachen, Auslösebedingungen, Erkennungsheuristiken und Fix-Muster für die CWE Top 25."
date: 2026-04-16
tags:
  - security
  - cwe
  - vulnerability-detection
level: Advanced
source_sha256: d234d6cf5ac564a188dd03e276355497a028e9bdb47dcd6279f0863c196c7653
translation: machine
translated_at: '2026-10-24'
---
# CWE-Schwachstellen-Referenzkarten {#cwe-vulnerability-reference-cards}

Strukturierte Wissenseinträge für die KI-gestützte Schwachstellenerkennung, basierend auf dem Vul-RAG-Ansatz (ACM TOSEM 2025). Jeder Eintrag umfasst: funktionale Semantik, Grundursache, Auslösebedingungen, Erkennungsheuristiken und Fix-Muster.

Für die Verwendung durch Security-Review-Agenten konzipiert. Jede Karte ist in sich geschlossen – ein Agent, der eine Karte liest, hat alles, was er zur Erkennung dieser Schwachstellenklasse benötigt.

Basierend auf den CWE Top 25 Most Dangerous Software Weaknesses (2024).

## Einträge {#entries}

### Injection & Eingabevalidierung {#injection-input-validation}

- CWE-079: XSS - Cross-Site Scripting (Rang 1)
- [[cwe-089-sql-injection]] - SQL-Injection (Rang 3)
- [[cwe-918-ssrf]] - Server-Side Request Forgery (Rang 19)
- CWE-434: File Upload - Unrestricted File Upload (Rang 10)
- [[cwe-502-deserialization]] - Deserialisierung nicht vertrauenswürdiger Daten (Rang 16)

### Speichersicherheit {#memory-safety}

- [[cwe-787-oob-write]] - Out-of-Bounds Write (Rang 2)
- CWE-125: Out-of-Bounds Read - Out-of-Bounds Read (Rang 6)
- CWE-416: Use After Free - Use After Free (Rang 8)
- CWE-190: Integer Overflow - Integer Overflow (Rang 23)

### Ressourcenverwaltung {#resource-management}

- [[cwe-400-resource-consumption]] - Unkontrollierter Ressourcenverbrauch (Rang 24)

## Methodik {#methodology}

Jeder Eintrag folgt der Wissensstruktur von Vul-RAG:

1. **Funktionale Semantik** - was der verwundbare Code tut (Verhaltensmuster, nicht Syntax)
2. **Grundursache** - warum die Schwachstelle existiert (grundlegender Designfehler)
3. **Auslösebedingungen** - wann ausnutzbar und wann NICHT (Indikatoren für Fehlalarme)
4. **Erkennungsheuristiken** - worauf beim Review zu achten ist (Source-Sink-Muster, fehlende Prüfungen)
5. **Fix-Muster** - wie behoben wird (Mustervorlagen) und Anti-Muster (falsche Fixes)

Diese Struktur übertrifft codebasiertes RAG um +16–24 % Genauigkeit (Vul-RAG, ACM TOSEM 2025).
