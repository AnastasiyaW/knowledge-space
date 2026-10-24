---
title: "Agent-Speicher und Zustand (September 2026)"
category: concepts
tags: [llm-agents, memory, state, context-management, persistence, authorization]
level: 3
source_sha256: 8efb020906623767e800af791b840523b4a2c1e8d4dbe186f8255b21fc6a7ee9
translation: machine
translated_at: '2026-10-24'
---
# Agent-Speicher und Zustand (September 2026) {#agent-memory-and-state-september-2026}

Überprüft am 2026-09-03. „Memory“ beschreibt mehrere verschiedene Mechanismen. Halten Sie Ausführungszustand, benutzerspezifischen Speicher, organisatorisches Wissen und maßgebliches Quellmaterial auseinander: Sie haben unterschiedliche Verantwortliche, Aufbewahrungsregeln, Zugriffsbereiche und Fehlermuster.

## Vier Dinge, die oft als Speicher bezeichnet werden {#four-things-often-called-memory}

| Typ | Geltungsbereich | Typischer Inhalt | Erforderliche Steuerung |
|---|---|---|---|
| Laufzustand | Eine Workflow-Ausführung | Schritte, Tool-Belege, ausstehende Freigabe | Checkpointing und idempotentes Fortsetzen |
| Thread-Kontext | Eine Konversation oder Aufgabe | Aktuelle Nachrichten und ausgewählte Artefakte | Token-Budget und Komprimierungsrichtlinie |
| Langzeitspeicher | Benutzer-, Agent- oder Organisations-Namespace | Präferenzen, Fakten, frühere Ergebnisse | Schreibrichtlinie, Herkunftsnachweis, Isolation, Ablauf |
| Wissenskorpus | Viele Benutzer/Aufgaben | Versionierte Quelldokumente | Autorität, Zitate, Retrieval, Veröffentlichungsrichtlinie |

Ein Chat-Verlauf ist keine Datenbank, und ein Vektorspeicher ist keine Erlaubnis, abgerufenen Text als erinnerten Fakt zu behandeln.

## Vertrag für Speichereinträge {#memory-record-contract}

```json
{
  "memory_id": "user-193:preference-7",
  "namespace": ["user", "193"],
  "kind": "preference",
  "value": "Prefers concise weekly summaries",
  "source": "explicit-user-statement",
  "written_by": "memory-policy-v2",
  "created_at": "2026-09-03T12:00:00Z",
  "expires_at": null,
  "confidence": "confirmed",
  "access_policy": "user-193-only"
}
```

Der Eintrag muss festhalten, warum er geschrieben wurde und wer ihn lesen darf. Lassen Sie nicht zu, dass ein Modell beliebigen, nicht vertrauenswürdigen Text ohne deterministische Regel und Prüfgrenze in dauerhafte Richtlinien oder benutzerübergreifenden Speicher überführt.

## Lese- und Schreibpfad {#read-and-write-path}

```text
incoming request
    -> authenticate and establish namespace
    -> retrieve only scoped, unexpired records
    -> select a bounded context slice
    -> run the workflow with checkpointed state
    -> propose memory candidates
    -> validate/provenance-check/approve writes
```

LangGraph unterscheidet thread-gebundenen, checkpointed Zustand von threadübergreifenden Stores. Die Dokumentation behandelt Kurzzeit- und Langzeitspeicher als getrennte Konzepte; übernehmen Sie diese Unterscheidung auch dann, wenn ein anderes Framework andere API-Namen verwendet. [Memory overview](https://docs.langchain.com/oss/python/concepts/memory) [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## Kontext-Komprimierung ist eine Richtlinie {#context-compaction-is-a-policy}

Wenn eine Konversation wächst, legen Sie fest, was zusammengefasst, verworfen, erneut abgerufen oder als strukturiertes Zustandsfeld erhalten werden kann. Bewahren Sie offene Freigaben, Tool-Belege, für Benutzer sichtbare Zusagen und Verweise auf maßgebliche Quellen. Zusammenfassungen in Freitextform sollten nicht die einzige Aufzeichnung einer wesentlichen Aktion werden.

## Evaluierung {#evaluation}

Testen Sie das Speichersystem mit getrennten Szenarien für:

1. korrektes Erinnern innerhalb eines Benutzer-Namespace;
2. kein Retrieval über Benutzer, Mandanten oder entzogene Berechtigungen hinweg;
3. Ablauf, Korrektur und Löschung eines veralteten Eintrags;
4. Widerstandsfähigkeit gegenüber Prompt-Injection beim Schreiben in den Speicher;
5. Wiederherstellung nach einer Unterbrechung an einem Checkpoint.

Messen Sie sowohl hilfreiches als auch schädliches Erinnern. Ein System, das mehr behält, ist nicht zwingend besser.

## Fallstricke {#gotchas}

- **Problem: Eine Präferenz wird geschrieben, weil eine nicht vertrauenswürdige Webseite sie vorgegeben hat.** Externer Text kann dauerhaftes Verhalten steuern. **Lösung:** Schreibvorgänge auf explizite Aussagen des Benutzers oder validierte Anwendungsereignisse mit Herkunftsnachweis beschränken.
- **Problem: Standardmäßig ein agentenweiter Namespace geteilt.** Die Daten eines Benutzers können andere Workflows beeinflussen. **Lösung:** Geltungsbereich explizit machen und standardmäßig den engsten Namespace wählen.
- **Problem: Eine ausstehende Freigabe oder ein Beleg wird in der Zusammenfassung weggelassen.** Der Workflow verliert seine Wiederherstellungsgrenze. **Lösung:** Diese als typisierte Zustandsfelder speichern, nicht nur als Fließtext.
- **Problem: Alten Speicher als maßgebliche Wahrheit behandeln.** Präferenzen und Fakten können sich ändern. **Lösung:** Zeitstempel, Herkunft, Konfidenz sowie eine Ablauf- und Prüfrichtlinie hinterlegen.

## Siehe auch {#see-also}

- [[context-engineering]]
- [[agent-architectures]]
- [[production-patterns]]
- [[tokenization]]

## Quellen {#sources}

- [LangChain memory overview](https://docs.langchain.com/oss/python/concepts/memory)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph add memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
