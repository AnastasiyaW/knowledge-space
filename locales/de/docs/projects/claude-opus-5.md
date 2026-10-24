---
title: "Claude Opus 5"
category: projects
date: 2026-07-24
tags: [claude-opus-5, claude-opus-5-development, claude_opus_5, project]
aliases: ["Claude Opus 5"]
level: 3
source_sha256: a6eadfd07a1d2dbd72793f6dc9c14186c76d74fc4974758fa3566deb8fa875a9
translation: machine
translated_at: '2026-10-24'
---
# Claude Opus 5 {#claude-opus-5}

**Entwicklungslinie:** `project:claude-opus-5` · Thread `claude-opus-5-development`  
**Letztes Ereignis:** 2026-07-24 · 1 datiertes seit 2026-07-24 · **Recherchiert:** 2026-09-07 · Konfidenz: hoch

## Was es ist {#what-it-is}

Anthropics aktuelles Modell der Opus-Klasse für Teams, die langlaufende Coding-Agenten und Enterprise-Workflows entwickeln.

- Komplexes Coding, Tool-Nutzung, Long-Context, Vision und Dokumentenaufgaben.
- 1M-Token-Kontext und 128K maximale Standard-Ausgabe; die 300K-Obergrenze der Batch API ist nur in der Beta verfügbar.
- 5 $ pro Million Input-Token und 25 $ pro Million Output-Token.

Verwenden Sie es, wenn Ihre eigene Evaluierung die Kosten für Output-Token und Latenz rechtfertigt.

## Entwicklungslinie {#development-line}

- **2026-07-24 — Anthropic veröffentlichte eine Ankündigung zu Claude Opus 5.** Am 2026-07-24 veröffentlichte Anthropic einen offiziellen Nachrichtenbeitrag, dessen Link auf Claude Opus 5 verweist. Die verfügbaren Belege belegen nicht die Fähigkeiten, Verfügbarkeit, Preise oder technischen Details der Ankündigung, daher erfasst dieser Verlaufseintrag nur den datierten Entwicklungsmeilenstein.

## Was sich geändert hat {#what-changed}

2026-07-24 — Claude Opus 5 wurde als `claude-opus-5` veröffentlicht, mit 1M-Token-Kontext, 128K maximaler Ausgabe, standardmäßig aktiviertem adaptivem Denken, 5 Effort-Stufen und Tool-Änderungen mitten in der Konversation (Beta).  
2026-08-01 — Claude Opus 5 wurde in der Dreams-Research-Preview unterstützt.  
2026-08-05 — Claude Opus 4.1 wurde eingestellt; Anthropic nannte Claude Opus 5 als Upgrade-Pfad.  
2026-08-19 — Claude Opus 5 wurde in der Claude API mit dem GA-Computer-Use-Toolset und dem neu eingeführten Browser-Use-Client-Toolset kompatibel.  
2026-08-20 — Diese Toolsets wurden für Claude Opus 5 in Google Cloud verfügbar.  
2026-09-01 — Die Claude API ergänzte für Claude Opus 5 Effort-Änderungen pro Nachricht (Beta) unter Erhalt des Prompt-Caches.

## So verwenden Sie es {#how-to-use-this}

1. Erstellen Sie eine Messages-API-Anfrage mit `model="claude-opus-5"`, setzen Sie `max_tokens` und senden Sie für eine mehrstufige Konversation den vollständigen Nachrichtenverlauf.
  — <https://platform.claude.com/docs/en/claude_api_primer>
2. Wenn Sie eine Opus-4.8-Integration migrieren, wählen Sie Antwortblöcke anhand von `type` aus, geben Sie Thinking-Blöcke nach Tool-Aufrufen unverändert zurück und entfernen Sie `thinking.disabled` bei `xhigh` oder `max`.
  — <https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5>
3. Beginnen Sie mit dem Standard-Effort `high`, führen Sie anschließend einen Effort-Sweep über Ihre eigenen Evaluierungen durch und wählen Sie dann `low`, `medium`, `xhigh` oder `max`; setzen Sie bei `xhigh` oder `max` einen großzügigen `max_tokens`-Wert.
  — <https://platform.claude.com/docs/en/build-with-claude/effort>
4. Für eine Claude-Code-Sitzung starten Sie `claude --model claude-opus-5`.
  — <https://support.claude.com/en/articles/11940350-claude-code-model-configuration>

## Best Practices {#best-practices}

- Geben Sie komplexen Aufgaben von Anfang an die vollständige Aufgabenspezifikation und begrenzen Sie den Umfang bei eng umrissenen Aufgaben ausdrücklich.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- Fordern Sie die sichtbare Antwortlänge an, die Sie benötigen; Effort steuert den Umfang des Denkens, nicht verlässlich die Länge der Antwort.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- Beginnen Sie mit `high` und ändern Sie den Effort erst nach einem Effort-Sweep über Ihre eigenen Evaluierungen; senken Sie ihn dort, wo die Qualität erhalten bleibt, und reservieren Sie `xhigh` oder `max` für fähigkeitskritische Aufgaben.
  — <https://platform.claude.com/docs/en/build-with-claude/effort>
- Entfernen Sie übernommene Anweisungen zur abschließenden Verifikation oder zu Verifier-Subagenten, sofern die Aufgabe sie nicht wirklich erfordert; bei Opus 5 können sie zu übermäßiger Verifikation und verschwendeten Tokens führen.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2026-07-24 — Die Annahme aus Opus 4.8, dass adaptives Denken Opt-in ist und `content[0]` Text ist, ist für Claude Opus 5 überholt; Antwortblöcke müssen anhand ihres Typs behandelt werden.
- 2026-07-24 — `thinking: {"type": "disabled"}` bei `xhigh` oder `max` ist für Claude Opus 5 keine gültige Anfrage mehr; sie liefert HTTP 400.
- 2026-08-05 — `claude-opus-4-1-20250805` ist eingestellt und liefert nun Fehler; Anthropics genannter Upgrade-Zielwert ist Claude Opus 5.
- 2026-08-19 — Die Annahme, dass `computer_toolset_20260801` in der Claude API nur in der Beta verfügbar ist, ist überholt; das Toolset ist GA, frühere Beta-Versionen bleiben verfügbar.

## Weiterhin unbekannt {#still-unknown}

- Keine Quelle in diesem Satz belegt kontospezifische Kontingente, regionale Kapazitäten oder Vertragspreise; prüfen Sie vor dem Rollout die Zielkonsole bzw. den Cloud-Katalog.
- Die Benchmark- und Early-Access-Aussagen der Launch-Ankündigung wurden hier nicht unabhängig reproduziert.
- Keine offizielle Quelle aus dieser Recherche besagt, dass Fable 5.1 Claude Opus 5 ablöst oder einstellt; die aktuelle Modellseite führt Opus 5 weiterhin als aktiv.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.anthropic.com/news/claude-opus-5 | Introducing Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/release-notes/overview | Claude-Platform-Versionshinweise | 2026-09-07 |
| https://platform.claude.com/docs/en/models/opus-5/overview | Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5 | Neuerungen in Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/claude_api_primer | API-Nutzungseinführung für Claude | 2026-09-07 |
| https://platform.claude.com/docs/en/build-with-claude/effort | Effort | 2026-09-07 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | Prompting Claude Opus 5 | 2026-09-07 |
| https://support.claude.com/en/articles/11940350-claude-code-model-configuration | Claude-Code-Modellkonfiguration | 2026-09-07 |
| https://platform.claude.com/docs/zh-CN/release-notes/overview | Claude-Platform-Versionshinweise (zh-CN) | 2026-09-07 |

## Agent-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:claude-opus-5`, Thread `claude-opus-5-development`, 1 datiertes Ereignis 2026-07-24 → 2026-07-24.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Die datierten Ablösungshinweise oben sind maßgeblich dafür, was veraltet ist.
