---
title: "xAI — Grok-Modellentwicklung"
category: organizations
tags: [grok-model-development, grok_4, grok_release, organization, xai]
aliases: ["xAI"]
level: 3
source_sha256: 492f986f56cf04ebed559de76b26664e1fabaf1c7d7d0ea04d849d19f7211519
translation: machine
translated_at: '2026-10-24'
---
# xAI — Grok-Modellentwicklung {#xai-grok-model-development}

**Entwicklungslinie:** `organization:xai` · Thread `grok-model-development`  
**Ereignisse:** 1 datiertes Ereignis, 2025-07-08 → 2025-07-08 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

xAI entwickelt Grok und stellt eine API für Teams bereit, die Chat-, Coding- und Agent-Workflows bauen.

Funktionen:

- Grok 4.6 akzeptiert Text und Bilder und gibt Text zurück;
- Grok 4.6 unterstützt konfigurierbares Reasoning;
- Grok unterstützt Function Calling, Web/X Search und Code-Ausführung;
- Voice- und Imagine-APIs sind separat.

Einschränkung: Grok 4.6 hat ein Kontextfenster von 500k Token; bei weniger als 200k Input-Token kostet die API pro 1M Input-/Cached-Input-/Output-Token $2 / $0.50 / $6.

Für eine neue Text- oder Coding-Integration sollte das aktuelle Modell verwendet werden, nicht der ursprüngliche Grok-4-Slug.

## Entwicklungslinie {#development-line}

- **2025-07-08 — Meilenstein der Grok-4-Entwicklung bei xAI.** Grok 4 und Grok 4 Heavy wurden für Abonnenten und die xAI-API mit nativer Tool-Nutzung und Echtzeit-Websuche/X-Suche verfügbar.

## Was sich geändert hat {#what-changed}

2024-08-15 — „uncensored“ ist eine unbestätigte Positionierungsbezeichnung. Kein offizieller Release-Eintrag verbindet sie mit einer Grok-Version, einem Endpoint, einer Richtlinie oder einer Verfügbarkeitsänderung.

2025-07-08 — Der verlinkte Social-Media-Beitrag war nicht abrufbar. Die erste bestätigte Produktänderung ist vom 2025-07-09: Grok 4 und Grok 4 Heavy wurden für Abonnenten und die xAI-API mit nativer Tool-Nutzung und Echtzeit-Websuche/X-Suche verfügbar.

2026-05-15 — `grok-4-0709` und mehrere ältere Grok-Slugs wurden außer Betrieb genommen; Aufrufe des alten Grok-4-Slugs werden auf `grok-4.3` umgeleitet.

Stand 2026-09-04 ist Grok 4.6 seit 2026-08-12 in der API verfügbar und ist das aktuelle Standardmodell für Code- und allgemeine Textarbeit.

## Anwendung {#how-to-use-this}

Stand 2025-07-08 sollten Praktiker, die xAIs Grok evaluieren, ihre Annahmen zur Modellauswahl am Grok-4-Meilenstein überprüfen. Aktuelle Fähigkeiten und Zugangsdetails sollten vor einer Einführung anhand primärer Quellen verifiziert werden.

1. Ein xAI-Console-Konto anlegen und Guthaben hinzufügen.
  — <https://docs.x.ai/developers/quickstart>
2. Einen API-Schlüssel erstellen und über `XAI_API_KEY` laden.
  — <https://docs.x.ai/developers/quickstart>
3. Für eine neue allgemeine Text- oder Coding-Integration `grok-4.6` auswählen; wenn Ausgabekonsistenz wichtig ist, einen datierten Slug verwenden.
  — <https://docs.x.ai/developers/models>
4. Die erste Anfrage mit dem xAI SDK oder einem OpenAI-Client, der auf `https://api.x.ai/v1` zeigt, an die Responses API senden.
  — <https://docs.x.ai/developers/quickstart>
5. Web Search oder X Search aktivieren, wenn eine Antwort auf aktuellen Informationen beruht.
  — <https://docs.x.ai/developers/models>

## Best Practices {#best-practices}

- Für reproduzierbares Produktionsverhalten einen datierten Modell-Slug festlegen. `-latest` nur verwenden, wenn automatische Modellaktualisierungen gewünscht sind.
  — <https://docs.x.ai/developers/models>
- Fragen zu aktuellen Ereignissen als Tool-Nutzungsfall behandeln. Serverseitige Suche aktivieren, statt sich auf den Trainingsstand des Modells zu verlassen.
  — <https://docs.x.ai/developers/models>
- Bei wiederkehrenden Konversationen einen stabilen `prompt_cache_key` oder `x-grok-conv-id` verwenden. Das Präfix nur anhängend gestalten und `cached_tokens` überwachen.
  — <https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices>
- Budgets sowohl für RPS als auch für TPM planen. HTTP 429 mit begrenztem exponentiellem Backoff behandeln.
  — <https://docs.x.ai/developers/rate-limits>

## Durch dies abgelöst {#superseded-by-this}

- 2026-05-15 — Das Deployment-Ziel `grok-4-0709` aus der Ära 2025 ist veraltet: xAI nimmt es außer Betrieb und leitet Aufrufe auf `grok-4.3` um; ein Ersatz sollte explizit gewählt werden, um Reasoning und Preis zu steuern.
- 2026-08-12 — Die Standardempfehlung für neue allgemeine Text- und Coding-Arbeiten wechselte zu `grok-4.6`; `grok-4.3` wird dadurch selbst nicht außer Betrieb genommen.

## Weiterhin unbekannt {#still-unknown}

- Die Referenz vom 2024-08-15 ist eine X-Suche-URL und keine archivierte Release-Notiz; sie hat den behaupteten „uncensored“-Zustand nicht belegt.
- Die x.com-Status-URL vom 2025-07-08 war zum Zeitpunkt der Prüfung nicht erreichbar, daher wurde ihr Wortlaut nicht verwendet.
- Es wurde keine offizielle, modellspezifische Veröffentlichung oder Dokumentationsseite auf Vereinfachtem Chinesisch gefunden. Die faktenliefernden Quellen sind englischsprachig.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://x.ai/news/grok-4 | Grok 4 | SpaceXAI | 2026-09-04 |
| https://docs.x.ai/developers/migration/may-15-retirement | Grok Model Retirement on May 15, 2026 | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/release-notes | Versionshinweise | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/models | Grok Models & Pricing | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/grok-4-6 | Grok 4.6 | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/quickstart | Grok API Quickstart: Get Your API Key | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices | Best Practices & FAQ | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/rate-limits | Rate Limits | SpaceXAI Docs | 2026-09-04 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `organization:xai`, Thread `grok-model-development`, 1 datiertes Ereignis 2025-07-08 → 2025-07-08.
- **Praktischer Hinweis:** Stand 2025-07-08 sollten Praktiker, die xAIs Grok evaluieren, ihre Annahmen zur Modellauswahl am Grok-4-Meilenstein überprüfen. Aktuelle Fähigkeiten und Zugangsdetails sollten vor einer Einführung anhand primärer Quellen verifiziert werden.
- **Konfidenz:** mittel. Die datierten, abgelösten Einträge oben sind maßgeblich dafür, was veraltet ist.
