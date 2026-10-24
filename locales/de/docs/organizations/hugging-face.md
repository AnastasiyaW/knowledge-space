---
title: "Hugging Face"
category: organizations
date: 2025-02-03
tags: [dreambooth-hackathon, hf-inference-providers, hugging-face, hugging-face-mcp, hugging-face-platform-evolution, huggingface-local-apps, organization]
aliases: ["Hugging Face"]
level: 3
source_sha256: 74a2012891ccb9a486731a5e3d1bfb98e702762311b1a0513b0caeb956f3a7ea
translation: machine
translated_at: '2026-10-24'
---
# Hugging Face {#hugging-face}

**Entwicklungslinie:** `organization:hugging-face` · Strang `hugging-face-platform-evolution`  
**Letztes Ereignis:** 2025-02-03 · 4 datierte seit 2022-12-28 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Hugging Face ist eine GitHub-artige ML-Plattform für Teams, die Modelle, Datensätze und KI-Apps veröffentlichen, evaluieren, ausführen oder anbinden.

- Hub-Repositories für Modelle, Datensätze und Spaces.
- Inference Providers für kompatible Serverless-Modelle über eine einzige API.
- MCP-Zugriff auf Hub-Suche, Dokumentation, ausgewählte Spaces, Jobs und Sandboxes.

## Entwicklungslinie {#development-line}

- **2022-12-28 — Hugging Face veröffentlichte Materialien für einen DreamBooth-Hackathon.** Hugging Face verlinkte eine DreamBooth-Hackathon-Seite und ein Colab-Notebook für Diffusion-Workflows.
- **2024-05-24 — Hugging Face ergänzte einen Local-Apps-Produktpfad.** Hugging Face verlinkte Task-Code für Local Apps und eine Einstellungsseite, um lokale Anwendungs-Workflows zu unterstützen.
- **2024-06-05 — Hugging Face veröffentlichte eine Offenlegung zu Spaces-Secrets.** Hugging Face legte offen, dass Secrets in Spaces offengelegt worden waren. Damit wurde die Sicherheit von Zugangsdaten in Spaces zu einem öffentlichen Anliegen für Maintainer und Nutzer.
- **2025-02-03 — Hugging Face kündigte Inference Providers an.** Hugging Face kündigte Inference Providers als Plattformweg an, um Inferenz über integrierte Provider zu nutzen.

## Was sich geändert hat {#what-changed}

Hugging Face entwickelte sich von gehosteter Modellzusammenarbeit zu einer Plattform mit lokalen, gerouteten und agentenorientierten Ausführungspfaden.

- 2022-12-28 — Der DreamBooth-Hackathon bot einen Notebook-Pfad, um Stable Diffusion anhand weniger Bilder zu personalisieren und Modelle im Hub zu veröffentlichen. Der Wettbewerb endete im Januar 2023.
- 2024-05-24 — Local Apps ergänzte auf Modellseiten lauffähige Snippets für lokale Laufzeitumgebungen. Die verlinkte, veränderliche Quelle deckt llama.cpp, vLLM, SGLang und MLX ab, die Implementierung vom Mai 2024 ist jedoch nicht fixiert.
- 2024-06-05 — Nach der Offenlegung der Space-Secrets vom 31. Mai rotierte Hugging Face betroffene Tokens, entfernte Organisations-Tokens aus Spaces, ergänzte KMS-gestützte Secrets und stellte Nutzer auf Fine-grained Tokens um.
- 2025-02-03 — Kurz nach dem Start am 28. Januar festgehalten: Inference Providers verlagerten die Serverless-Nutzung von einem einzigen Hub-Endpunkt zu einer providergerouteten API mit kompatiblen Modellseiten, SDK-Unterstützung, persönlichen Provider-Schlüsseln und einer über Hugging Face abgerechneten Abrechnung.
- 2025-06-07 — Im Einklang mit dem offiziellen MCP-Server-Start vom 6. Juni konnten MCP-kompatible Assistenten Hub-Ressourcen durchsuchen und ausgewählte Gradio-Apps aufrufen. Der Start erfolgte als experimentell.
- 2026-07-22 (heute gefunden) — MCP ergänzte das Navigationswerkzeug hf_fs für Repositories, Speicher, Dokumentation und Papers sowie Sandboxes, die an Buckets und Repositories angehängt werden.

## Anwendung {#how-to-use-this}

Prüfen und beheben Sie Secrets, die in Hugging Face Spaces verwendet werden, nach der Offenlegung der Spaces-Secrets vom 2024-06-05. Bewerten Sie Hugging Face Inference Providers als providervermittelten Inferenzzugriff ab 2025-02-03, wenn Sie Deployment-Workflows auswählen.

1. Erstellen Sie einen Fine-grained Access Token, der auf das Repository oder die Inferenzaufgabe beschränkt ist, und authentifizieren Sie danach einen Entwicklungsrechner mit hf auth login.
  — <https://huggingface.co/docs/hub/en/security-tokens>
2. Legen Sie ein Modell-, Datensatz- oder Space-Repository an; setzen Sie Eigentümer, Sichtbarkeit und Lizenz; laden Sie anschließend mit hf upload oder über Git/Xet hoch.
  — <https://huggingface.co/docs/hub/en/repositories-getting-started>
3. Veröffentlichen Sie eine Model Card in der README des Repositories mit vorgesehenen Einsatzzwecken, Einschränkungen, Trainingsinformationen, Datensätzen und Evaluationsergebnissen.
  — <https://huggingface.co/docs/hub/en/model-cards>
4. Für gehostete Inferenz wählen Sie ein kompatibles Hub-Modell aus und rufen es über InferenceClient auf, mit explizitem Modell und Provider, wenn die Workload vorhersagbares Routing benötigt.
  — <https://huggingface.co/docs/huggingface_hub/guides/inference>
5. Für einen Agenten-Workflow öffnen Sie bei angemeldetem Zustand die MCP Settings, verwenden die generierte Client-Konfiguration, starten den Client neu und fügen danach nur die Hub- oder Space-Werkzeuge hinzu, die die Aufgabe benötigt.
  — <https://huggingface.co/docs/hub/en/agents-mcp>
6. Wählen Sie für einen Space bewusst die Sichtbarkeit public, protected oder private und legen Sie Zugangsdaten in den Space Secrets ab, nicht im Quellcode oder in öffentlichen Variables.
  — <https://huggingface.co/docs/hub/en/spaces-overview>

## Bewährte Praktiken {#best-practices}

- Verwenden Sie pro Anwendung oder Nutzungsfall einen eigenen Fine-grained Token; verwenden Sie für CI, wo verfügbar, OIDC Trusted Publishers, statt ein langlebiges Token zu speichern.
  — <https://huggingface.co/docs/hub/en/security-tokens>
- Behandeln Sie die Model Card als Anforderung für jede Veröffentlichung: Nennen Sie vorgesehene Verwendung, bekannte Grenzen, Trainingseingaben und Parameter sowie Nachweise der Evaluation.
  — <https://huggingface.co/docs/hub/en/model-cards>
- Legen Sie in der Produktion eine explizite Hub-Modell-ID und einen benannten Provider fest; empfohlene Modelle und die automatische Providerauswahl können sich ändern.
  — <https://huggingface.co/docs/huggingface_hub/guides/inference>
- Prüfen Sie vor dem Deployment die Kompatibilität von Modell, Aufgabe und Provider; ein im Hub gehostetes Modell ist nicht automatisch bei jedem Inference Provider verfügbar.
  — <https://huggingface.co/docs/inference-providers/index>
- Halten Sie Space-Secrets aus Code und Variables heraus; Secrets sind privat, Variables dagegen öffentlich einsehbar und werden beim Duplizieren von Spaces mitkopiert.
  — <https://huggingface.co/docs/hub/en/spaces-overview>
- Verwenden Sie die von MCP Settings generierte Konfiguration und lassen Sie schreibfähige Repository-Werkzeuge, Jobs, Sandboxes und Community-Spaces nur bewusst aktivierbar.
  — <https://huggingface.co/docs/hub/en/agents-mcp>

## Durch diesen Stand überholt {#superseded-by-this}

- 2022-12-28 — Preis-, Zertifikats- und Leaderboard-Einreichungsabläufe des DreamBooth-Hackathons sind veraltet, weil das Event im Januar 2023 endete.
- 2024-06-05 — Empfehlungen auf Basis breiter klassischer Lese-/Schreib-Tokens sind durch Fine-grained Tokens pro Anwendung und kurzlebige, per OIDC ausgestellte Tokens für CI ersetzt.
- 2025-02-03 — Die Annahme einer einzigen statischen gehosteten Inference API für jedes Hub-Modell ist durch Provider-Kompatibilität und explizite Providerauswahl überholt.
- 2025-06-07 — Handgeschriebene feste MCP-Client-Konfigurationen sind durch die generierte Settings-Konfiguration und die Navigation mit hf_fs ersetzt.

## Weiterhin unklar {#still-unknown}

- Hugging Face vereint ein Repository-Plattform-, eine Integrationsschicht für lokale Laufzeitumgebungen, ein Inferenz-Gateway, die Spaces-Plattform und einen MCP-Connector. Diese Ereignisse bilden eine Plattform-Chronologie ab, keine einzelne Produktmigration.
- Der Beitrag vom 2025-06-07 lieferte während der Recherche keinen lesbaren Inhalt. Der Changelog von Hugging Face vom 6. Juni bestätigt den MCP-Start unabhängig, nicht aber den genauen Wortlaut des Beitrags.
- Der Verweis auf Local Apps zeigt auf veränderliche Repository-Quellen statt auf eine unveränderliche Revision vom Mai 2024; das genaue historische Verhalten ist daher nicht verifiziert.
- Aktuelle Preise, Kontingente, Bedingungen zur Datenverarbeitung und Verfügbarkeit wurden nicht angegeben, da sie je nach Tarif, Modell und Provider variieren.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/dreambooth-hackathon | DreamBooth Hackathon | 2026-09-04 |
| https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/local-apps.ts | local-apps.ts — huggingface.js | 2026-09-04 |
| https://raw.githubusercontent.com/huggingface/huggingface.js/main/packages/tasks/src/local-apps.ts | local-apps.ts raw source | 2026-09-04 |
| https://huggingface.co/blog/space-secrets-disclosure | Space secrets leak disclosure | 2026-09-04 |
| https://huggingface.co/blog/inference-providers | Welcome to Inference Providers on the Hub | 2026-09-04 |
| https://x.com/_akhaliq/status/1931013733406445702 | x.com status 1931013733406445702 | 2026-09-04 |
| https://huggingface.co/changelog/hf-mcp-server | Connect Your MCP Client to the Hugging Face Hub | 2026-09-04 |
| https://huggingface.co/changelog/mcp-improvements-jul-26 | MCP Server Enhancements | 2026-09-04 |
| https://huggingface.co/docs/hub/en/index | Hugging Face Hub documentation | 2026-09-04 |
| https://huggingface.co/docs/hub/en/repositories-getting-started | Getting Started with Repositories | 2026-09-04 |
| https://huggingface.co/docs/hub/en/model-cards | Model Cards | 2026-09-04 |
| https://huggingface.co/docs/hub/en/security-tokens | User access tokens | 2026-09-04 |
| https://huggingface.co/docs/inference-providers/index | Inference Providers | 2026-09-04 |
| https://huggingface.co/docs/huggingface_hub/guides/inference | Run Inference on servers | 2026-09-04 |
| https://huggingface.co/docs/hub/en/agents-mcp | Hugging Face MCP Server | 2026-09-04 |
| https://huggingface.co/docs/hub/en/spaces-overview | Spaces Overview | 2026-09-04 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `organization:hugging-face`, Strang `hugging-face-platform-evolution`, 4 datierte Ereignisse 2022-12-28 → 2025-02-03.
- **Praxishinweis:** Nach der Offenlegung der Spaces-Secrets vom 2024-06-05 prüfen und beheben Sie alle Secrets, die in Hugging Face Spaces verwendet werden; ab 2025-02-03 bewerten Sie Hugging Face Inference Providers als providervermittelten Inferenzzugriff, wenn Sie Deployment-Workflows auswählen.
- **Konfidenz:** mittel. Die datierten Überholungsvermerke oben sind maßgeblich dafür, was veraltet ist.
