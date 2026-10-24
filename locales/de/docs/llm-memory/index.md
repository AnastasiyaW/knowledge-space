---
title: "LLM-Gedächtnis & Wissenspersistenz"
type: MOC
level: 2
source_sha256: 71474d6e69cb1bff2d843d384162e84d85f59ebb1f7c776c939ada4f3422499c
translation: machine
translated_at: '2026-10-24'
---
# LLM-Gedächtnis & Wissenspersistenz {#llm-memory-knowledge-persistence}

Muster und Architekturen für die Organisation persistenten Wissens bei der Arbeit mit LLM-Agenten. Nicht über den Aufbau von RAG-Systemen (siehe [[agent-fundamentals]]) – sondern darüber, wie Agenten sich über Sitzungen hinweg erinnern, vergessen und Wissen verwalten.

## Memory-Architektur {#memory-architecture}
- [[memory-architectures]] - Flache Dateien, hierarchische Graphen, Vektorspeicher, Wissensgraphen, hybride Ansätze
- [[verbatim-vs-extraction]] - Warum Rohtext LLM-Extraktion schlägt (96,6 % vs. 85 %), wann welcher Ansatz sinnvoll ist

## Kontext- & Fenstermanagement {#context-window-management}
- [[context-window-management]] - Schichtweises Laden (L0–L3), Token-Budgets, Compaction, Re-Injection-Muster

## Wissensorganisation {#knowledge-organization}
- [[knowledge-base-as-memory]] - Raw->Wiki->Schema-Pipeline, reines Markdown vs. RAG, Ingest-/Query-/Lint-Operationen
- [[session-persistence]] - Handoff-Dateien, Memory-Dateien, Zustandsdateien, Journal-Muster

## Zeitlichkeit & Retrieval {#temporal-retrieval}
- [[temporal-memory]] - Gültigkeitszeiträume, Erkennung veralteter Inhalte, Zeitverfall, Auflösung von Widersprüchen
- [[memory-retrieval-patterns]] - Index-Navigation, BM25, Vektorsuche, hybride Suche, Reranking, Kostenvergleich

## Memory-Lebenszyklus {#memory-lifecycle}
- [[forgetting-strategies]] - Compaction, Archivierung, TTL, Relevanzbewertung, Verwaltung der Memory-Größe

## Weitere Referenzen {#additional-references}

- [[knowledge-graph-memory]] - Persistente Wissensgraph-Muster für KI-Agenten: Entitätsauflösung, Pipeline-Stufen, Agentennotizen
- [[memory-priority-enforcement]] - Muster zur Strukturierung des Agenten-Gedächtnisses in Stufen mit ständigem Laden (kritisch) und bedarfsgesteuertem Laden (Referenz)
- [[memory-transfer-learning]] - Domänenübergreifender Memory-Transfer für Coding-Agenten
- [[shared-knowledge-layers]] - Wenn mehrere Agenten parallel arbeiten, benötigen sie einen strukturierten Weg, Erkenntnisse zu teilen, ohne
- [[verbatim-retrieval-vs-extraction]] - Warum die Speicherung im Originalwortlaut die LLM-Extraktion für das Memory-Retrieval von Agenten schlägt – Benchmarks, MemPalace
