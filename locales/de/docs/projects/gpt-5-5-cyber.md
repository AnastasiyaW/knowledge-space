---
title: "GPT-5.5-Cyber"
category: projects
date: 2026-06-23
tags: [gpt-5-5-cyber, project]
aliases: ["GPT-5.5-Cyber"]
level: 3
source_sha256: a94bfd08719dc09208677cd08108ed54276dc7dca9133143c401b354962db7f1
translation: machine
translated_at: '2026-10-24'
---
# GPT-5.5-Cyber {#gpt-55-cyber}

**Entwicklungslinie:** `project:gpt-5-5-cyber` · Thread `gpt-5-5-cyber`  
**Letztes Ereignis:** 2026-06-23 · 1 datiertes seit 2026-06-23 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

GPT-5.5-Cyber ist ein Legacy-Modell von OpenAI für genehmigte Verteidiger, die autorisiertes Red Teaming, Exploit-Validierung, Penetrationstests und kontrollierte Schwachstellenforschung durchführen.

Fähigkeiten:

- Cyber-Workflows: führt spezialisierte, autorisierte Sicherheitsoperationen aus.
- Ablehnungen: für risikoreichere defensive Aufgaben reduziert.
- API-Kennung: verwendet `gpt-5.5-cyber-preview` in der Responses API.

Eine frühere Genehmigung für GPT-5.5-Cyber gewährt keinen Zugang zu Daybreak Red. Neuer erweiterter Zugang erfordert eine separate Genehmigung.

Für übliche defensive Arbeit nutzen wir Daybreak Blue. Für neue erweiterte Deployments nutzen wir Daybreak Red mit GPT-5.6-Cyber. GPT-5.5-Cyber behalten wir nur dort, wo ein bestehender Anspruch erforderlich ist.

## Entwicklungslinie {#development-line}

- **2026-06-23 — OpenAI-Daybreak-Sicherheitsmitteilung zu GPT-5.5-Cyber.** Am 2026-06-23 verlinkte der GPT-5.5-Cyber-Thread auf eine offizielle OpenAI-Daybreak-Seite. Der Link verweist auf eine offizielle Sicherheitsseite in der Projekthistorie. Die technischen Aussagen wurden nicht recherchiert.

## Was sich geändert hat {#what-changed}

- 2026-05-07 — GPT-5.5-Cyber wurde in eine eingeschränkte Vorschau für Verteidiger kritischer Infrastruktur aufgenommen. Es reduzierte Ablehnungen, statt gegenüber GPT-5.5 wesentliche Cyber-Fähigkeiten hinzuzufügen.
- 2026-06-23 — die vollständige Veröffentlichung von GPT-5.5-Cyber erreichte vertrauenswürdige Verteidiger im begrenzten Rollout. Sie brachte verbesserte Leistung bei der Schwachstellenerkennung und beim Patchen.
- 2026-08-10 — Daybreak Red führte GPT-5.6-Cyber als aktuelles spezialisiertes Modell für erweiterte autorisierte Arbeit ein. GPT-5.5-Cyber wechselte zu Legacy-Zugangsbedingungen.

## Wie damit umzugehen ist {#how-to-use-this}

Seit 2026-06-23 behandeln wir diese Mitteilung als Prüfanlass für GPT-5.5-Cyber. Wir ändern Implementierung und Deployment-Praxis nicht, bis wir die verlinkte Quelle recherchiert und verifiziert haben.

1. Definieren Sie einen internen Sicherheitsbereich, der Systeme umfasst, die Sie besitzen oder für die Sie eine ausdrückliche Testerlaubnis haben. Beantragen Sie den Daybreak-Zugang als Einzelperson oder Organisation.
  — <https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview>
2. Beginnen Sie übliche AppSec-, Incident-Response-, Malware-Analyse- und Patch-Validierungsarbeit mit Daybreak Blue statt mit dem Legacy-Modell.
  — <https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/>
3. Holen Sie eine separate Daybreak-Red-Genehmigung für autorisierte Exploit-Entwicklung, Red Teaming oder Penetrationstests ein. Verwenden Sie `gpt-daybreak-red-latest` oder `gpt-5.6-cyber` über das genehmigte API-Projekt.
  — <https://developers.openai.com/api/docs/models/gpt-daybreak-red-latest>
4. Prüfen Sie bestehende GPT-5.5-Cyber-Ansprüche mit einer direkten Responses-API-Anfrage unter Verwendung von `gpt-5.5-cyber-preview`. Die Sichtbarkeit in der Modellliste belegt keinen Zugriff.
  — <https://help.openai.com/en/articles/20001259-trusted-access-for-cyber-common-issues-and-troubleshooting>

## Bewährte Praktiken {#best-practices}

- Betreiben Sie Trusted Access innerhalb eines internen Workspaces. Leiten Sie niemals kundenseitigen, nachgelagerten oder Drittanbieter-Traffic darüber.
  — <https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview>
- Verwenden Sie Daybreak Blue als Standardstufe. Eskalieren Sie zu Daybreak Red nur für erweiterte autorisierte Arbeit, die spezialisierte Fähigkeiten erfordert.
  — <https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/>
- Führen Sie Sicherheits-Workflows in isolierten Umgebungen aus. Prüfen Sie erhöhte Tool-Aktionen mit Auto-Review und behalten Sie bei Hochrisikoaufgaben die menschliche Aufsicht.
  — <https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/>
- Behandeln Sie Zugang als begrenzt und Schutzmaßnahmen als aktiv. Eine Genehmigung entfernt nicht alle Ablehnungen, und sie autorisiert niemals Tests an Systemen ohne ausdrückliche Erlaubnis.
  — <https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview>

## Durch dies ersetzt {#superseded-by-this}

- 2026-08-10 — GPT-5.5-Cyber ist nicht mehr die aktuelle spezialisierte Wahl für neue erweiterte Cyber-Deployments. GPT-5.6-Cyber ist das Daybreak-Red-Modell.
- 2026-09-05 — Daybreak Blue mit GPT-5.6 Sol ersetzt frühere Empfehlungen, Teams mit GPT-5.5 und Trusted Access zu starten. Bestehende GPT-5.5-Cyber-Genehmigungen bleiben unter ihren ursprünglichen Bedingungen bestehen und wechseln nicht zu Daybreak Red.

## Noch unbekannt {#still-unknown}

- Der Ereignisdatensatz ist auf 2026-06-23 datiert, während die verlinkte Ankündigung der Originalquelle auf 2026-06-22 datiert ist. Wir behalten das Ereignisdatum 2026-06-23 bei und verfolgen das Quellendatum separat.
- OpenAI kennzeichnet GPT-5.5-Cyber in der aktuellen Support-Dokumentation als Legacy. Sie veröffentlichen kein allgemeines Abkündigungsdatum und garantieren die weitere Verfügbarkeit für bereits genehmigte Konten nicht.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://openai.com/index/daybreak-securing-the-world/ | Daybreak: Tools for securing every organization in the world | 2026-09-05 |
| https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber/ | Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber | 2026-09-05 |
| https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/ | Expanding Daybreak as the Cyber Defense Window Narrows | 2026-09-05 |
| https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview | OpenAI Daybreak - Trusted Access for Cyber Overview | 2026-09-05 |
| https://help.openai.com/en/articles/20001259-trusted-access-for-cyber-common-issues-and-troubleshooting | OpenAI Daybreak - Common Issues and Troubleshooting | 2026-09-05 |
| https://developers.openai.com/api/docs/models/gpt-daybreak-red-latest | Daybreak Red Model | 2026-09-05 |
| https://openai.com/zh-Hans-CN/index/daybreak-securing-the-world/ | Daybreak: Sicherheitsschutz für Organisationen weltweit | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:gpt-5-5-cyber`, Thread `gpt-5-5-cyber`, 1 datiertes Ereignis 2026-06-23 → 2026-06-23.
- **Praktischer Hinweis:** Seit 2026-06-23 behandeln Sie diese sicherheitsbezogene offizielle Mitteilung als Prüfanlass für GPT-5.5-Cyber; ändern Sie Implementierung und Deployment-Praxis nicht, bis die verlinkte Quelle recherchiert und verifiziert ist.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
