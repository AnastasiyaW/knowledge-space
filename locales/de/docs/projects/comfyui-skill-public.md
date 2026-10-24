---
title: "ComfyUI Skill Public — öffentliches Repository"
category: projects
date: 2026-05-14
tags: [comfyui-skill-public, comfyui_skill_public, project, public-repository]
aliases: ["ComfyUI Skill Public", "comfyui-skill-public"]
level: 3
source_sha256: ef9c3871e674d1af70cd0d254cf0c42307f1aab7df0e889adefd67a61b21c2a7
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Skill Public — öffentliches Repository {#comfyui-skill-public-public-repository}

**Entwicklungslinie:** `project:comfyui-skill-public` · Thread `public-repository`  
**Letztes Ereignis:** 2026-05-14 · 1 datiertes Ereignis seit 2026-05-14 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

comfyui-skill-public: ein portabler ComfyUI-Skill für Agenten und Operatoren, die mit unbekannten lokalen, entfernten oder Cloud-Installationen arbeiten.

- Ermittelt Node-Klassen und Modellwerte, bevor ein Workflow aufgebaut wird.
- Deckt FLUX-2-Bildarbeit, LTX-2.3- und WAN-2.2-Video, JoyCaption-Prompting, LoRA-Training, Batches und Wiederherstellung ab.
- Nutzt REST plus WebSocket-Jobverfolgung statt einer GUI.

## Entwicklungslinie {#development-line}

- **2026-05-14 — GitHub-Repository von ComfyUI Skill Public referenziert.** Am 2026-05-14 hat der Eintrag einen Link zum GitHub-Repository von ComfyUI Skill Public erfasst. Die verfügbaren Belege belegen den Repository-Verweis, aber nicht ein bestimmtes Release, Feature oder eine bestimmte Code-Änderung.

## Was sich geändert hat {#what-changed}

2026-03-28 — comfyui-skill-public: Das erste öffentliche portable Paket trennte Hinweise zu Trigger und Routing von maschinenspezifischer Einrichtung. 2026-04-11 — LTX-2.3-Hinweise, Batch-Zustand und Wiederherstellung, Referenzimplementierungen, Hinweise zu Abhängigkeiten, Demo-Workflows und ein LoRA-Trainingspfad wurden ergänzt. 2026-04-12 — Prompting-Anleitungen für FLUX 2 und WAN 2.2 sowie ein Entscheidungsablauf für die Ersteinrichtung wurden ergänzt. 2026-04-25 — Eine SOP für Batch-Überwachung und Wiederherstellung wurde ergänzt. 2026-04-26 — Dokumentation zu Einrichtung und Cron wurde abgeglichen. 2026-05-14 — Eine dokumentierte öffentliche Erwähnung beschrieb die Steuerung über OpenClaw in natürlicher Sprache; für dieses Datum ist keine Änderung der GitHub-Implementierung erkennbar. 2026-06-03 — v1.4.0 ergänzte einen portablen API-Helper, einen Batch-Starter, eine JoyCaption-Konvention, Cold-Start-Anweisungen für Agenten und weitere Node-Maps; v1.4.1 erweiterte die Unterstützung ausdrücklich über OpenClaw hinaus und ersetzte die Anleitung „Demo als Drop-in“ durch Workflows mit eigener API.

## Wie Sie das nutzen {#how-to-use-this}

Stand 2026-05-14 können Praktiker das verlinkte GitHub-Repository als möglichen öffentlichen Referenzpunkt für den ComfyUI-Skill verwenden, sollten dessen Inhalte aber prüfen, bevor sie sich auf eine bestimmte Fähigkeit oder ein bestimmtes Release verlassen.

1. Klonen Sie das Repository und lassen Sie einen KI-Agenten AGENTS.md oder SKILL.md als Operator lesen; installieren Sie die aufgelisteten Python-Abhängigkeiten, wenn Sie dessen Hilfscode verwenden.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
2. Erheben Sie bei einem unbekannten ComfyUI-Ziel URL, Version, Node-Pakete, Modellfamilie, Hardwaregrenzen und Ausgaberegeln; prüfen Sie zuerst system_stats, object_info, queue, WebSocket und einen kleinen abgeschlossenen Prompt.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/setup.md>
3. Exportieren Sie einen bestehenden Workflow im ComfyUI-API-Format und prüfen Sie anschließend über object_info die benötigten Nodes, Modelle, Encoder und VAEs.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
4. Kopieren Sie den Workflow tief, patchen Sie nur die jobspezifischen Eingaben, senden Sie ihn an prompt, behalten Sie die Prompt-ID, warten Sie auf den WebSocket-Abschluss und verifizieren Sie die Ausgaben über history.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/api.md>
5. Verwenden Sie bei einem Batch eine gemeinsame Client-ID und eine WebSocket-Verbindung, speichern Sie den Zustand jedes Jobs und setzen Sie nur Jobs fort, für die keine verifizierte Ausgabe vorliegt.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md>

## Best Practices {#best-practices}

- Ermitteln Sie Node-Klassen, Modelldateinamen und installationsspezifische Werte zur Laufzeit; behandeln Sie Beispiele nicht als Fakten über die Zielmaschine.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/SKILL.md>
- Bearbeiten Sie einen Basis-Workflow nicht direkt; kopieren Sie ihn tief und patchen Sie die Kopie.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
- Senden Sie Batch-Prompts nicht ohne Rückmeldung ab: Warten Sie auf den WebSocket-Abschluss und verifizieren Sie jede Prompt-ID über history.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md>
- Behandeln Sie mitgelieferte Demo-Graphen nur als Beispiele; verwenden Sie bevorzugt einen Workflow, der aus der Zielinstallation von ComfyUI exportiert wurde.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/755d3f66f4ebb1072a75fc7d8d616489c97bacce>

## Durch Neueres abgelöst {#superseded-by-this}

- 2026-06-03 — Demo-Workflows als installationsfertige Drop-ins: abgelöst durch die Anleitung aus v1.4.1, den eigenen Workflow im API-Format zu exportieren und anzupassen.
- 2026-06-03 — OpenClaw- und Discord-spezifische, fest codierte Annahmen zum Controller: abgelöst durch die scheduler-neutrale, umgebungskonfigurierte Anleitung aus v1.4.0.

## Weiterhin unbekannt {#still-unknown}

- Für 2026-05-14 ist kein Commit des Projekts selbst und kein GitHub-Release erkennbar; das Ereignis ist als öffentliche Erwähnung am selben Tag belegt, nicht als nachgewiesene Code-Veröffentlichung.
- Die ursprüngliche URL leitet nun auf ComfyUI-Agent-Toolkit weiter, aber das Datum und die Begründung der Umbenennung sind nicht offengelegt.
- GitHub hat keine veröffentlichten Releases; die Versionsbezeichnungen im Changelog sind Dokumentation, kein Nachweis für Release-Assets.
- Die GitHub-API war bei dieser Prüfung nicht erreichbar, daher wurden created_at und pushed_at des Repositories nicht unabhängig verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/Zambav/comfyui-skill-public | GitHub - Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |
| https://nnets.ru/news/openclaw-skill-upravlenie-comfyui-komandami-na-estestvennom-yazyke | OpenClaw Skill: управление ComfyUI командами на естественном языке. | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commits/main | Commits · Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/95fe0bc5ee9cdf9b64db983ea8983d68905dbc9c | v1.4.0: port controller improvements + new hero README | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/755d3f66f4ebb1072a75fc7d8d616489c97bacce | v1.4.1: broaden README to 'any agent' + 'bring your own workflows' | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md | README.md | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/SKILL.md | SKILL.md | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/setup.md | setup.md | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/api.md | ComfyUI-Agent-Toolkit/api.md at main | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md | ComfyUI-Agent-Toolkit/batch-operations.md at main | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/changelog.md | changelog.md | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/releases | Releases · Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:comfyui-skill-public`, Thread `public-repository`, 1 datiertes Ereignis vom 2026-05-14 bis 2026-05-14.
- **Praktischer Hinweis:** Stand 2026-05-14 können Praktiker das verlinkte GitHub-Repository als möglichen öffentlichen Referenzpunkt für den ComfyUI-Skill verwenden, sollten dessen Inhalte aber prüfen, bevor sie sich auf eine bestimmte Fähigkeit oder ein bestimmtes Release verlassen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Ablösungen oben.
