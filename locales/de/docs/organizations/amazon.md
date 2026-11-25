---
title: "Amazon — Generative-KI-Plattform und Modelle von Amazon"
category: organizations
tags: [amazon, amazon-generative-ai-platform-and-models, amazon-nova, amazon_bedrock_codewhisperer, organization]
aliases: ["Amazon"]
level: 3
source_sha256: 31178a9e3f54d82301179f59e97570cfb1c01c535d740578682af70ac51b232d
translation: machine
translated_at: '2026-10-24'
---
# Amazon — Generative-KI-Plattform und Modelle von Amazon {#amazon-amazon-generative-ai-platform-and-models}

**Entwicklungslinie:** `organization:amazon` · Thread `amazon-generative-ai-platform-and-models`  
**Ereignisse:** 2 datiert, 2023-04-13 → 2024-12-04 · **Recherchiert:** 2026-09-03 · Konfidenz: mittel

## Was es ist {#what-it-is}

Amazon — in dieser AWS-Linie gibt es zwei verschiedene Arbeitswege: Amazon Bedrock ist eine verwaltete Plattform für GenAI-Anwendungen und Agenten; Amazon Nova ist eine eigene Modellfamilie in Bedrock; Amazon Q Developer ist ein Assistent für Code, in den CodeWhisperer aufgegangen ist. Funktionen: - Modelle von AWS und Drittanbietern über Model Catalog und die Bedrock-API nutzen; - Nova 2 Lite und Sonic im Playground prototypisieren oder Nova 2 über Converse und InvokeModel aufrufen; - Q Developer in der IDE für Codevorschläge und Chat nutzen, solange die Plugin-Unterstützung besteht. Einschränkung: Eine Nova-Anfrage kann bis zu 60 Minuten dauern, und die Unterstützung der Q-Developer-IDE-Plugins endet am 2027-04-30. Fazit: Für einen neuen GenAI-Dienst sollten Sie Bedrock und das gewünschte Nova- oder Drittanbieter-Modell wählen; CodeWhisperer/Q Developer sollte nicht als langfristige Grundlage für eine neue IDE-Integration betrachtet werden.

## Entwicklungslinie {#development-line}

- **2023-04-13 — Amazon stellt Bedrock vor und erweitert sein Angebot für generative KI.** Am 2023-04-13 stellte Amazon Amazon Bedrock als Teil seines Einstiegs in den Markt für generative KI-Plattformen vor. Die verlinkten Materialien ordnen außerdem Amazon CodeWhisperer dieser entwicklerorientierten KI-Erweiterung zu, wodurch der Beitrag einen wesentlichen Schritt in der Entwicklung von Amazons generativer KI darstellt.
- **2024-12-04 — Amazon kündigt Amazon-Nova-Modelle für Bedrock an.** Am 2024-12-04 kündigte Amazon die Amazon-Nova-Familie von KI-Modellen zur Nutzung über Amazon Bedrock an. Das war eine wesentliche Entwicklung, weil Amazons Linie für generative KI damit von einer Plattform für den Modellzugriff hin zu benannten eigenen Modellangeboten erweitert wurde.

## Was sich geändert hat {#what-changed}

2023-04-13 — Amazon Bedrock erschien in einer begrenzten Preview als API zu Basismodellen von AWS und Drittanbietern. Am selben Tag wurde CodeWhisperer als allgemein verfügbarer Codeassistent für die IDE mit den Stufen individual und professional verfügbar. Von Anfang an handelte es sich um unterschiedliche Produkte: eine Inferenzplattform und ein Codeassistent. 2023-09-28 (heute geprüft) — Bedrock wurde allgemein verfügbar: AWS ergänzte eine verwaltete Modellauswahl, provisionierten Durchsatz sowie Integrationen mit CloudWatch und CloudTrail; der Preview-Status endete. 2024-04-30 (heute geprüft) — Amazon CodeWhisperer ging in Amazon Q Developer auf; die eigenständige Bezeichnung CodeWhisperer ist für das IDE-Produkt nicht mehr aktuell. 2024-12-04 — Amazon stellte Nova in Bedrock vor: die ersten Modelle Micro (nur Text), Lite und Pro (multimodal) sowie Canvas für Bilder und Reel für Video; Premier wurde als nächstes Modell angekündigt. 2026-08-17 (heute geprüft) — AWS dokumentierte, dass die Unterstützung der IDE-Plugins von Amazon Q Developer am 2027-04-30 endet, und nennt Kiro als Weg zu ähnlichen Funktionen. 2026-09-03 (heute geprüft) — der aktuelle Bedrock-Katalog und die Nova-Dokumentation zeigen die neuere Linie Nova 2, darunter Lite und Sonic; für die meisten Szenarien empfiehlt AWS die Converse API. Betrachten Sie die Modellauswahl aus der Ankündigung von 2024 nicht als vollständige aktuelle Liste.

## Wie Sie das nutzen {#how-to-use-this}

Seit 2023-04-13 sollten Praktiker, die Amazons KI-Stack bewerten, Bedrock als zentrale Plattformoption betrachten; seit 2024-12-04 sollten sie außerdem Amazon Nova neben Drittanbieter-Modellen in Bedrock für relevante Workloads prüfen.

1. Für eine neue GenAI-Anwendung öffnen Sie den Model Catalog von Amazon Bedrock, wählen ein Modell und prüfen die Berechtigungen für AWS Marketplace: Bei korrekten Berechtigungen sind die Modelle standardmäßig verfügbar; danach starten Sie den Playground oder rufen InvokeModel bzw. Converse auf.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html>
2. Für einen schnellen Prototyp von Amazon Nova 2 nutzen Sie den Chat- oder Text-Playground mit Nova 2 Lite bzw. Sonic; für eine Anwendung wechseln Sie zu Bedrock InvokeModel oder zur Converse API.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/getting-started-nova-2.html>
3. Im Code erstellen Sie einen Client bedrock-runtime und rufen Converse mit modelId und einem Array von Nachrichten auf; fügen Sie eine system-Anweisung, Inferenzparameter und eine gestreamte Antwort nur hinzu, wenn die Oberfläche sie benötigt.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-converse-api.html>
4. Für ein reguliertes Szenario binden Sie einen bestimmten Guardrail und seine numerische Version über die Bedingung bedrock:GuardrailIdentifier an eine IAM-Richtlinie, sodass eine Anfrage ohne die vorgeschriebene Schutzmaßnahme abgelehnt wird.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html>
5. Falls das Team Amazon Q Developer vorübergehend weiter nutzt, installieren Sie die Erweiterung für die IDE und melden sich über AWS Builder ID oder IAM Identity Center an; legen Sie zugleich einen separaten Migrationsplan bis 2027-04-30 an.
  — <https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html>

## Best Practices {#best-practices}

- Wählen Sie standardmäßig Converse: Die API bietet eine einheitliche Schnittstelle für verschiedene Modelle; die Invoke-API sollten Sie nur für Fälle verwenden, in denen das native Schema eines bestimmten Modells erforderlich ist.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html>
- Stellen Sie das Read-Timeout des Clients auf lange Nova-Anfragen ein: AWS warnt, dass eine einzelne Inferenz bis zu 60 Minuten dauern kann, und zeigt eine Konfiguration mit 3600 Sekunden.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html>
- Formulieren Sie eine einfache, eindeutige Anweisung nach dem Kontext, trennen Sie Eingabedaten durch Begrenzer, legen Sie das Ausgabeformat ausdrücklich fest und definieren Sie die Inferenzparameter; prüfen Sie Änderungen am Prompt an einem separaten Testset und nicht nur an Entwicklungsbeispielen.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html>
- Verlassen Sie sich nicht darauf, dass der aufrufende Code die Schutzmaßnahme freiwillig einbindet: IAM muss für jede Inferenzanfrage die konkrete Kennung und Version des Guardrails verlangen.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html>
- Prüfen Sie Vorschläge von CodeWhisperer/Q Developer vor der Übernahme auf Code, die URL des Ursprungsrepositorys und die Lizenz, wenn das System eine Ähnlichkeit mit öffentlichem Code gemeldet hat; das automatische Übernehmen einer Empfehlung ersetzt diese Prüfung nicht.
  — <https://aws.amazon.com/ru/codewhisperer/>

## Hiermit überholt {#superseded-by-this}

- 2023-04-13 — Der Status von Amazon Bedrock als limited preview ist überholt: Der Dienst wurde am 2023-09-28 allgemein verfügbar.
- 2023-04-13 — Die eigenständige Bezeichnung Amazon CodeWhisperer als aktuelles IDE-Produkt ist überholt: Seit dem 2024-04-30 gehört es zu Amazon Q Developer.
- 2024-12-04 — Die ursprünglichen Modelle Nova Micro, Lite, Pro, Canvas und Reel als vollständige aktuelle Modellauswahl zu betrachten, ist überholt: Der aktuelle Katalog umfasst die Linie Nova 2, darunter Lite und Sonic.
- Bis 2026-08-17 — Der Rat, eine neue langlebige IDE-Integration auf Amazon Q Developer ohne Migrationsfrist aufzubauen, ist überholt: Für genau die IDE-Plugins wurde das Ende der Unterstützung auf 2027-04-30 angekündigt.

## Weiterhin unbekannt {#still-unknown}

- Amazon Nova/Bedrock und CodeWhisperer/Amazon Q Developer sind zwei verschiedene Produktlinien von AWS, nicht ein Produkt und auch nicht aufeinanderfolgende Versionen; dieser Eintrag fasst sie nur auf Unternehmensebene zusammen.
- Die Mitteilung zum 2027-04-30 betrifft ausdrücklich die IDE-Plugins von Amazon Q Developer; aus den geprüften Quellen lässt sich der Status von Q Developer CLI, Konsole und der übrigen Komponenten nach diesem Datum nicht ableiten.
- Verfügbarkeit von Nova, Preise, Kontingente, Marketplace-Bedingungen und erforderliche Berechtigungen hängen von Region und AWS-Konto ab; bei dieser Prüfung gab es keinen Zugriff auf ein bestimmtes Konto oder eine bestimmte Region.
- Die Ankündigung von 2024 sah Nova Premier für das erste Quartal 2025 vor; ihre aktuelle regionale Verfügbarkeit und ihr Preis wurden nicht gesondert geprüft.
- Für Bedrock am 2023-04-13 wurde hier eine datierte Sekundärquelle verwendet; eine eigene primäre AWS-Ankündigung zur limited preview wurde nicht gefunden.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://techcrunch.com/2023/04/13/with-bedrock-amazon-enters-the-generative-ai-race/ | With Bedrock, Amazon enters the generative AI race | 2026-09-03 |
| https://aws.amazon.com/ru/codewhisperer/ | Генератор кода на основе искусственного интеллекта – Amazon CodeWhisperer – AWS | 2026-09-03 |
| https://aws.amazon.com/about-aws/whats-new/2023/04/amazon-codewhisperer-generally-available/ | Amazon CodeWhisperer is now generally available | 2026-09-03 |
| https://aws.amazon.com/about-aws/whats-new/2023/09/amazon-bedrock-generally-available/ | Amazon Bedrock is now generally available | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/doc-history.html | Document history for Amazon Q Developer User Guide | 2026-09-03 |
| https://www.aboutamazon.com/news/aws/amazon-nova-artificial-intelligence-bedrock-aws | Amazon Nova: Meet our new foundation models in Amazon Bedrock | 2026-09-03 |
| https://aws.amazon.com/bedrock | Amazon Bedrock – Build genAI applications and agents at production scale – AWS | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html | Models at a glance - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html | Request access to models - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/getting-started-nova-2.html | Getting started with Amazon Nova 2 - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-converse-api.html | Using the Converse API - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html | Core inference - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html | Design a prompt - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html | Enforce the use of specific guardrails in model inference requests - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html | Installing the Amazon Q Developer extension or plugin in your IDE - Amazon Q Developer | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html | Amazon Q Developer IDE plugins end of support - Amazon Q Developer | 2026-09-03 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `organization:amazon`, Thread `amazon-generative-ai-platform-and-models`, 2 datierte Ereignisse 2023-04-13 → 2024-12-04.
- **Praxishinweis:** Seit 2023-04-13 sollten Praktiker, die Amazons KI-Stack bewerten, Bedrock als zentrale Plattformoption betrachten; seit 2024-12-04 sollten sie außerdem Amazon Nova neben Drittanbieter-Modellen in Bedrock für relevante Workloads prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Überholungen oben.
