---
title: "GLM-5.2 — Modellverfügbarkeit"
category: projects
date: 2026-06-14
tags: [glm-5-2, glm_models, model-availability, project]
aliases: ["GLM-5.2"]
level: 3
source_sha256: 5086941fae00f3f982651b1c4ec2ee8af80723337a1fb344c739901f60a01fc3
translation: machine
translated_at: '2026-10-24'
---
# GLM-5.2 — Modellverfügbarkeit {#glm-52-model-availability}

**Entwicklungslinie:** `project:glm-5-2` · Thread `model-availability`  
**Letztes Ereignis:** 2026-06-14 · 1 datiertes Ereignis seit 2026-06-14 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

GLM-5.2 ist ein weiterhin gelistetes Z.ai-Modell für Software-Engineering-Agenten.

- Reasoning
- Streaming
- Funktionsaufrufe
- Context Caching
- Strukturiertes JSON
- MCP

1M Kontext und 128K Output.

GLM-5.2 für Kompatibilität oder einen kontrollierten Vergleich beibehalten, für neue Coding-Aufgaben jedoch GLM-5.3 verwenden.

## Entwicklungslinie {#development-line}

- **2026-06-14 — Die Z.ai-Dokumentation identifizierte GLM-5.2 als ihr neuestes Modell.** Am 2026-06-14 verlinkte Z.ai DevPack-Dokumentation für das neueste Modell innerhalb der GLM-5.2-Entwicklungslinie. Das markiert einen Meilenstein der Verfügbarkeit, wir haben den Beitrag bzw. die Dokumentation jedoch nicht recherchiert. Wir behaupten keine Release-Details, Fähigkeiten oder Zugangsbedingungen.

## Was sich geändert hat {#what-changed}

- 2026-06-14 — Die verlinkte URL „latest model“ verweist auf einen Umstiegsleitfaden für GLM-5.3 und belegt daher keinen Launch von GLM-5.2.
- 2026-06-16 — Z.ai hat GLM-5.2 veröffentlicht und unter MIT als Open Source bereitgestellt; hinzu kam ein verlustfreies Modell mit 1M Kontext für langlaufende Coding-Aufgaben.
- 2026-07-08 — Eine unabhängige CAISI-Bewertung ergänzte einen Sicherheitshinweis: Schutzmaßnahmen beim Deployment verhinderten nicht die Unterstützung bei der agentischen Entwicklung von Exploits, und Betreiber können Schutzmaßnahmen bei selbst gehosteten Open Weights entfernen.
- 2026-08-18 — GLM-5.3 hat GLM-5.2 als aktuelles Flaggschiff von Z.ai abgelöst, mit einem vom Anbieter gemeldeten Coding-Zuwachs von 50 % auf Z.ai Code Bench.

## Anwendung {#how-to-use-this}

Stand 2026-06-14 die DevPack-Dokumentation von Z.ai zum neuesten Modell prüfen, bevor GLM-5.2 ausgewählt wird. Nicht davon ausgehen, dass ein früheres GLM-Modell weiterhin die aktuell dokumentierte Option ist.

1. Einen Z.ai-API-Client anlegen und eine Bearer-authentifizierte Anfrage an `https://api.z.ai/api/paas/v4/chat/completions` mit `model: "glm-5.2"` und mindestens einer Nutzernachricht senden.
  — <https://docs.z.ai/guides/llm/glm-5.2>
2. Bei einer schwierigen Coding-Aufgabe Thinking aktivieren und `reasoning_effort` auf `max` setzen. `max_tokens` auf den tatsächlich benötigten Output begrenzen.
  — <https://docs.z.ai/guides/llm/glm-5.2>
3. `stream: true` verwenden, wenn der Aufrufer Server-Sent-Event-Chunks verarbeiten kann. Den Parameter weglassen oder auf false setzen, wenn eine synchrone Antwort gewünscht ist.
  — <https://docs.z.ai/api-reference/llm/chat-completion>
4. Zurückgegebene Argumente von Funktionsaufrufen als nicht vertrauenswürdige Eingaben behandeln. Sie vor der Ausführung gegen das deklarierte Schema validieren.
  — <https://docs.z.ai/api-reference/llm/chat-completion>

## Best Practices {#best-practices}

- Einer Refactoring-Aufgabe explizite Grenzen für Geschäftslogik, API, Laufzeit, Abhängigkeiten und Verifikation geben. Vor der Übernahme der Änderung einen Plan und die relevanten Testergebnisse verlangen.
  — <https://docs.z.ai/guides/llm/glm-5.2>
- `thinking.clear_thinking` bei gewöhnlichen Chats aktiviert lassen. Frühere Reasoning-Inhalte nur erhalten, wenn der vollständige, unveränderte und korrekt geordnete Verlauf verfügbar ist.
  — <https://docs.z.ai/api-reference/llm/chat-completion>
- Für neue Coding-Deployments zuerst GLM-5.3 evaluieren. GLM-5.2 nur dort beibehalten, wo seine Modell-ID eine bewusste Kompatibilitätsvorgabe ist.
  — <https://docs.z.ai/guides/llm/glm-5.3>

## Hierdurch ersetzt {#superseded-by-this}

- :

## Weiterhin unbekannt {#still-unknown}

- Das Ereignis vom 2026-06-14 liegt vor dem von Z.ai bestätigten Release vom 2026-06-16. Verfügbares Material von Z.ai bestätigt einen früheren Zugang zum Coding Plan vor dem Release, datiert diese Vorschau jedoch nicht auf den 14. Juni.
- Die offiziellen Seiten von Z.ai widersprechen sich beim Zeitpunkt von GLM-5.3. Der Forschungsindex nennt 2026-08-14, die Release Notes 2026-08-18; für das Datum der Ablösung verwenden wir letzteres.
- Wir haben keine authentifizierte API-Anfrage durchgeführt. Kontospezifische Verfügbarkeit, Kontingente und regionaler Zugang sind nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://docs.z.ai/devpack/latest-model | Modelle wechseln - Überblick - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://docs.z.ai/release-notes/new-released | Neu veröffentlicht - Überblick - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.zhipuai.cn/zh/research/161 | GLM-5.2 online und Open Source: Fokus auf Coding und langlaufende Aufgaben | 2026-09-05 |
| https://docs.z.ai/guides/llm/glm-5.2 | GLM-5.2 - Überblick - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://docs.z.ai/api-reference/llm/chat-completion | Chat Completion - Überblick - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.nist.gov/document/caisi-assessment-zais-glm-52 | Bewertung von Z.ai’s GLM-5.2 | 2026-09-05 |
| https://docs.z.ai/guides/llm/glm-5.3 | GLM-5.3 - Überblick - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.zhipuai.cn/en/research | Research - Z.ai | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:glm-5-2`, Thread `model-availability`, 1 datiertes Ereignis 2026-06-14 → 2026-06-14.
- **Praktischer Hinweis:** Stand 2026-06-14 die DevPack-Dokumentation von Z.ai zum neuesten Modell prüfen, bevor GLM-5.2 ausgewählt wird. Nicht davon ausgehen, dass ein früheres GLM-Modell weiterhin die aktuell dokumentierte Option ist.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
