---
title: "LLM & KI-Agenten"
type: MOC
level: 3
source_sha256: 0a84593682152b5363e36cfa851da3818a5a1b2782d89ed934ee033081fd1693
translation: machine
translated_at: '2026-10-24'
---
# LLM & KI-Agenten {#llm-ai-agents}

## Grundlagen {#foundations}
- [[transformer-architecture]] - Ein praxisnaher, versionsbewusster Leitfaden zu aufmerksamkeitsbasierter Transformer-Struktur, autoregressiver Dekodierung, Positionsinformationen und Grenzen der Produktionskonfiguration.
- [[tokenization]] - BPE, WordPiece, SentencePiece, Kontextfenster, Token-Zählung
- [[embeddings]] - Vektorrepräsentationen, Ähnlichkeitsmaße, Embedding-Modelle, bekannte Probleme
- [[frontier-models]] - Vergleich und Auswahlleitfaden für GPT, Claude, Llama, Mistral, Gemini

## Prompting und Generierung {#prompting-and-generation}
- [[prompt-engineering]] - System-Prompts, Few-Shot, Chain-of-Thought, Checklisten-Muster, Destillation von Anweisungen
- [[function-calling]] - Tool-Use-APIs von OpenAI und Anthropic, Tool-Beschreibungen, Validierung
- [[llm-api-integration]] - Chat Completions, Nachrichtenrollen, Streaming, Parameter, Kostenmanagement

## Retrieval-Augmented Generation {#retrieval-augmented-generation}
- [[rag-pipeline]] - RAG-Architektur, Halluzinationsproblem, Verbesserungsstrategien, Evaluation
- [[chunking-strategies]] - Textaufteilung, Chunk-Größen, semantisches Chunking, Document Loader
- [[vector-databases]] - Vektorsuche um versionierte Embeddings, autorisierte Metadatenfilter, Herkunftsnachweise, Recall-Evaluation und sichere Migration aufbauen statt sich auf statische Produkt-Rankings zu stützen.

## KI-Agenten {#ai-agents}
- [[agent-fundamentals]] - ReAct-Schleife, Agentenkomponenten, Typen, Agent vs. Workflow
- [[agent-design-patterns]] - Plan-and-Execute, Reflexion, MRKL, Scratchpad, Entwurfsprinzipien
- [[multi-agent-systems]] - Mehrere Agenten über Aufgabenverträge, Verantwortlichkeiten, Befugnisse, Zustand und Nachweisgrenzen koordinieren; Agenten nur hinzufügen, wenn eine gemessene Zerlegung sie erfordert.
- [[agent-memory]] - Kurz- und Langzeitgedächtnis, HITL, Copilot-Muster, Konversationsmanagement
- [[agent-security]] - Jailbreaks, Prompt Injection, Data Poisoning, Verteidigungsstrategien

## Frameworks und Tools {#frameworks-and-tools}
- [[langchain-framework]] - Ein versionsbewusster Leitfaden zum aktuellen Agent-Harness von LangChain, zu Provider-Integrationen, Middleware, Zustand und Grenzen für den Produktionseinsatz.
- [[langgraph]] - Zustandsbehaftete Graphen, bedingtes Routing, Human-in-the-Loop, Orchestrierung mehrerer Agenten
- [[no-code-platforms]] - n8n, FlowWise, Gradio-UI-Erstellung, Deployment
- [[spring-ai]] - LLM-Integration mit Java/Spring Boot
- [[ai-coding-assistants]] - KI-Coding-Assistenten über explizite Grenzen für Umfang, Daten, Tools, Freigaben und Nachweise betreiben, statt auf Produkt-Rankings oder Vertrauen in generierten Code zu setzen.
- [[qwen-code]] - Installation der Qwen-Code-CLI, Provider-Vertrag und Authentifizierungsverlauf
- [[unsloth]] - Unsloth Core, Studio, Desktop und modellspezifische Grenzen beim Fine-Tuning

## Modellbetrieb {#model-operations}
- [[fine-tuning]] - LoRA, QLoRA, PEFT, Fine-Tuning bei OpenAI, Datenqualität
- [[model-optimization]] - Quantisierung (GGUF, GPTQ, AWQ), Destillation, Pruning
- [[ollama-local-llms]] - Einrichtung lokaler Inferenz, Quantisierungsstufen, Modellauswahl
- [[llmops]] - Evaluation, Monitoring, Kostenoptimierung, CI/CD für LLM-Anwendungen
- [[production-patterns]] - Deterministische Kontextinjektion, Copilot, Workflow-Zerlegung, Logging

## Weiterführende Referenzen {#additional-references}

- [[adaptive-learning-systems]] - Architekturmuster für KI-gestützte Bildungssysteme, die sich an einzelne Lernende anpassen
- [[adaptive-patterns-for-autonomous-agents]] - Explizite Aufgabenzustände, begrenzte Hooks, auf Fähigkeiten beschränkte Subagenten und nachweisbasierte Freigabeprüfungen verwenden statt undurchsichtiger Schlüsselwort-Trigger oder willkürlicher Mehrdeutigkeitswerte.
- [[agent-architectures]] - Wie sich der Kontrollfluss und die Zustandsverwaltung eines LLM-Agenten über einzelne Muster hinaus strukturieren lassen
- [[agent-deployment]] - Agenten vom Prototyp in den Produktionsbetrieb überführen
- [[agent-evaluation]] - Agentenverhalten mit versionierten Aufgabenfixtures, deterministischen Validatoren, kontrollierten Prüfungen von Seiteneffekten und reproduzierbaren Nachweisen evaluieren, statt sich auf einen einzelnen Benchmark-Wert zu verlassen.
- [[agent-observability-dashboards]] - Echtzeit-Observability für Multi-Agenten- und Subagenten-Systeme: hookbasierte Telemetrie, Ereignisse
- [[agent-orchestration]] - Modellaufrufe, Tools, Übergaben, Freigaben, Wiederholungen und Nachweise über expliziten Aufgabenzustand koordinieren, statt eine frameworkspezifische Agentenschleife zu verwenden.
- [[agent-safety-alignment]] - Agentensicherheit als explizite Grenzen für Befugnisse, Daten, Tools, Freigaben und Nachweise aufbauen, statt sie als reines Prompt-Versprechen zu behandeln.
- [[agent-scope-evasion]] - Coding-Agenten, die auf die Reduzierung von Sykophanz trainiert wurden, zeigen einen dokumentierten Fehlermodus: beim Auftreten von
- [[agent-self-improvement]] - Techniken, mit denen Agenten ihre eigene Leistung durch Reflexion, Belohnung auf Schrittebene verbessern
- [[agentic-rl-competitive-programming]] - GrandCode (2026) erreicht Großmeister-Niveau bei Wettbewerbsprogrammierungsaufgaben durch
- [[agentic-security-2026]] - Ein Bedrohungsmodell und Kontrollleitfaden für werkzeugnutzende Agenten, MCP-Integrationen, persistenten Speicher und irreversible Effekte. Stand der Prüfung: 2026-09-03.
- [[agentic-systems-landscape-2026]] - Protokolle für Multi-Agenten-Systeme, SDK-Vergleich, Orchestrierungsmuster und reale Coding-Agenten
- [[ai-adaptive-learning-systems]] - Eine versionsbewusste Architektur für Lernendendaten, deterministische Terminplanung, eingeschränktes LLM-Tutoring, Evaluation und Schutzmaßnahmen für Lernendendaten.
- [[ai-agent-ide-features]] - KI-gestützte Coding-Umgebungen entlang von Workspace-Isolation, expliziten Berechtigungen, dauerhaften Aufgabenartefakten, Verifikation und Review gestalten und bewerten.
- [[autonomous-agent-evolution]] - Ersetzen der festen evolutionären Suche (Agenten als zustandslose Worker) durch langlebige autonome Agenten
- [[chinese-ai-coding-ecosystem]] - Chinesische KI-Coding-Werkzeuge, Muster und Community-Praktiken: Trae, OpenSpec, MetaGPT, GLM-5
- [[claude-adaptive-thinking]] - Den Reasoning-Aufwand von Claude konfigurieren und bewerten, ohne sich auf feste, modellspezifische Faustregeln zu verlassen.
- [[claude-code-degradation-2026]] - Eine belegbasierte Methode zur Diagnose von Qualitäts-, Konfigurations-, Kosten- und Verfügbarkeitsänderungen bei Coding-Agenten, ohne einen Vorfall beim Anbieter zu erfinden.
- [[claude-code-ecosystem]] - Claude-Code-Plugins, Skills, Hooks, Projektanweisungen und Subagenten als explizite, versionierte Governance-Oberflächen nutzen; vor dem Rollout das aktuelle Schema und den effektiven Geltungsbereich prüfen.
- [[claude-code-harness-patterns]] - Eine praxisnahe Abgrenzung zwischen Anweisungen, Tools, deterministischen Gates, Review und dauerhaften Nachweisen für die Arbeit mit Coding-Agenten.
- [[claude-desktop-session-management]] - Unterstützte Export-, Konto- und Erweiterungsfunktionen nutzen, statt sich für die Wiederherstellung von Unterhaltungen oder die geräteübergreifende Synchronisation auf nicht versionierte interne Caches zu verlassen.
- [[claude-managed-agents]] - Organisationsweit verwaltete Claude-Code-Subagenten mit explizitem Geltungsbereich, Vorrangregeln, Tool-Beschränkungen und Verifikation definieren, statt verwaltete Konfiguration als Cloud-Ausführungsumgebung zu behandeln.
- [[context-engineering]] - Modellkontext als begrenzte Arbeitseingabe behandeln und Aufgabenzustand, Nachweise, Befugnisse und Retrieval-Herkunft in versionierten Artefakten erhalten, statt feste Token-Budgets zu verwenden.
- [[gradio-llm-interfaces]] - Schnelles Prototyping von Chat-Oberflächen mit Streaming, Markdown-Darstellung und Vergleich mehrerer Modelle
- [[handoff-rollup-pattern]] - Wie man eine begrenzte, nachvollziehbare Zusammenfassung langlaufender Agentenarbeit erstellt, ohne so zu tun, als wäre eine Zusammenfassung verlustfrei.
- [[kv-cache-compression]] - Reduzierung des KV-Cache-Speichers bei der LLM-Inferenz, um längere Kontexte und mehr gleichzeitige Anfragen zu ermöglichen
- [[llm-fine-tuning-practical]] - End-to-End-Leitfaden für Fine-Tuning über Frontier-APIs und QLoRA mit einem Entscheidungsrahmen für den Einsatzzeitpunkt
- [[llm-persona-design-and-engineering]] - Eine LLM-Persona als versionierte Verhaltensrichtlinie mit expliziten Befugnissen, Datenschutzregeln, Eskalations- und Evaluationsgrenzen entwerfen, statt eine vorausgesetzte Modellpersönlichkeit anzunehmen.
- [[managed-agents]] - Ein versionsbewusster Leitfaden zum verwalteten Agent-Harness von Anthropic: Agentenkonfiguration, Umgebungen, Sitzungen, Ereignisse, Berechtigungsrichtlinien und Datengrenzen.
- [[multi-agent-messaging]] - Kommunikationsmuster zwischen Agenten für Claude-Code-Sitzungen: integrierte Agent Teams, hookbasiert
- [[multi-agent-systems-architectures-2026]] - Multi-Agenten-Systeme (MAS) haben sich in zwei Hauptarchitekturschulen aufgespalten: rollenbasiert
- [[multi-session-coordination]] - Dauerhafte Koordinationsmuster für mehrere Coding-Agenten-Sitzungen: isolierte Worktrees, Manifeste, nur anhängbare Nachweise, Leases für exklusive Ressourcen und verifizierte Integration.
- [[notebooklm-integration]] - Google NotebookLM als kostenloses Recherche-Backend für Claude Code nutzen – token-sparende Workflows
- [[oh-my-claudecode-omc-architecture]] - Wie man das sich schnell weiterentwickelnde OMC-Plugin einsetzt, ohne Drittanbieter-Befehle, Modell-Routing oder erzeugten Zustand mit einer stabilen Sicherheits- oder Release-Grenze zu verwechseln.
- [[persona-adaptive-llm]] - Ein Entscheidungsrahmen für Profilfelder, Retrieval-Speicher und adapterbasierte Personalisierung mit Mandantenisolation, Evaluation, Einwilligung und Löschgrenzen.
- [[scaling-laws-and-benchmarks]] - Chinchilla-Skalierungsgesetz, Standard-Benchmarks (ARC, DROP, HellaSwag) und Richtlinien zur Modellauswahl
- [[social-media-mcp-tools]] - Ein anbieterneutraler, freigabeorientierter Entwurf für die Nutzung von MCP, um Social-Media-Inhalte zu entwerfen, zu validieren und zu veröffentlichen, ohne einen Social-Media-Beitrag als umkehrbare Chat-Aktion zu behandeln.
- [[swarm-based-review-and-multisampling-in-agentic-workflows]] - Unabhängige Kandidaten erzeugen, Nachweise validieren und Agentenausgaben über explizite Akzeptanzkriterien auswählen, statt über feste Stimmenzahlen oder Modellkonfidenz.
- [[telegram-managed-bots]] - Ein produktionssicherer Leitfaden zum Manager-Bot-Modell von Telegram: Erstellung, Token-Rotation, Zugriffseinstellungen, Zustandsisolation und Lebenszyklus-Nachweise.
- [[token-optimization]] - Reduzierung des Token-Verbrauchs in Agentensystemen, ohne die Aufgabenleistung zu beeinträchtigen
- [[tool-use-patterns]] - Wie man Tools für LLM-Agenten entwirft, bereitstellt und verwaltet
- [[uml-driven-agent-development]] - Kleine, versionierte Sequenz-, Zustands- und Vertrauensgrenzen-Diagramme verwenden, um Agenten-Workflows zu verdeutlichen, und sie anschließend in dem Renderer und CI-Ziel validieren, das sie veröffentlichen wird.
