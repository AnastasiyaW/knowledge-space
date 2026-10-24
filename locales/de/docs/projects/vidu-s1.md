---
title: "Vidu S1"
category: projects

tags: [project, vidu-s1]
aliases: ["Vidu S1"]
level: 3
source_sha256: e583e53e3229ab76e6a40d1d27c7bfb600deb999cc282db4f63b9aab21c2314b
translation: machine
translated_at: '2026-10-24'
---
# Vidu S1 {#vidu-s1}

**Entwicklungslinie:** `project:vidu-s1` · Thread `vidu-s1`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Vidu S1 ist ShengShus gehostetes Echtzeit-Videomodell für Kreative und Produktteams, die sprechende, interaktive digitale Charaktere entwickeln. Vidu führt es separat von den Clip-Generierungsmodellen Q1/Q2/Q3 auf.

- Charaktererstellung: erstellt einen Charakter aus einer Persona, einem initialen Mensch-, Anime- oder Haustierbild und einer ausgewählten oder geklonten Stimme.
- Dynamische Steuerung: ändert Charakteraktionen anhand gesprochener Eingaben während einer Audio- oder Videositzung.
- Client-Zugang: bietet Vidu Stream und eine derzeit dokumentierte Vidu S1 API (Beta), die einen Steuerungs-WebSocket zusammen mit AliRTC-Medien nutzt.

Die Produktseite nennt 540p bei 25 fps, bis zu 42 fps. Sitzungsdauer und Abrechnung müssen aus der Antwort der Live-Sitzung abgelesen werden, da die Herstellerdokumentation widersprüchlich ist. Verwenden Sie das Modell für reaktionsschnelle Avatar-Interaktionen, nicht für eine lokale Modellinstallation oder einen konventionellen, fertigen Clip.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

2026-07-10 — Die öffentliche GitHub-Präsentation von Vidu S1 erhielt drei Änderungen an den Erfahrungs-GIFs. Die formale Veröffentlichung war bereits auf 2026-07-03 datiert. Dabei handelte es sich also um eine Verfeinerung von Demo und Dokumentation und nicht um eine neue Modellveröffentlichung.

## So wird es verwendet {#how-to-use-this}

1. Für eine Testnutzung ohne Code öffnen Sie Vidu Stream, melden sich an und verifizieren das Konto, dann wählen Sie einen Charakter aus oder erstellen einen.
  — <https://www.vidu.com/vidu-stream>
2. Legen Sie die Persona fest, laden Sie ein initiales Bild hoch und wählen, laden oder klonen Sie anschließend eine Stimme, bevor Sie die Unterhaltung starten.
  — <https://www.vidu.com/vidu-stream>
3. Verwenden Sie gesprochene Anweisungen während der Unterhaltung, um die Aktionen des Charakters zu steuern.
  — <https://www.vidu.com/vidu-stream>
4. Für eine Anwendung beschaffen Sie einen API-Schlüssel und erstellen eine Live-Sitzung mit `POST /live/v1/lives`; bewahren Sie `live.id` und die zurückgegebenen RTC-Zugangsdaten auf.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
5. Treten Sie dem Aliyun-RTC-Kanal bei und etablieren den authentifizierten Steuerungs-WebSocket, warten auf `conn_init_ack.success=true`, beenden dann das Gespräch, schließen den WebSocket und verlassen den RTC-Kanal.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>

## Best Practices {#best-practices}

- Bei Browser-Clients bewahren Sie den rohen Vidu-API-Schlüssel in einem vertrauenswürdigen Backend auf und leiten den authentifizierten WebSocket darüber weiter. Native Browser-WebSockets können den erforderlichen Autorisierungs-Header nicht setzen.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Behandeln Sie das zurückgegebene `live_duration` und die final abgerechnete Nutzung als maßgeblich. Hart codieren Sie keine „unbegrenzte“ oder feste Sitzungsobergrenze.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/api-reference.md>
- Im Videomodus implementieren Sie für `NOT_READY` eine Behandlung nach dem Muster Schließen–Backoff–Wiederverbinden. Für `LIVE_CONN_INIT_FAILED` erstellen Sie eine neue Live-Sitzung.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Integrieren Sie Aliyun RTC als eigenständige Medienschicht und abonnieren den aktiven Remote-Stream genau einmal. Ignorieren Sie veraltete RTC- oder WebSocket-Ereignisse aus einer vorherigen Sitzung.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Behandeln Sie sowohl serverseitige `type:6`-Hangups als auch abnormale WebSocket-Schließungen. Nach einem aktiven Hangup schließen Sie den WebSocket, bevor Sie `leaveChannel()` aufrufen.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/websocket-protocol.md>

## Abgelöst durch dieses {#superseded-by-this}

- 2026-07-03 — Die Behandlung von Vidu S1 als standardmäßigen Generator nach dem Muster „Prompt absenden, dann warten“ oder als Variante der Vidu-Q-Reihe ist überholt. Es wurde als eigene Echtzeit-Linie für interaktive digitale Charaktere eingeführt.
- 2026-07-03 — Die Bezeichnung des 2026-07-10 als Start von Vidu S1 ist überholt. ShengShu hat es formal am 2026-07-03 veröffentlicht.

## Weiterhin unbekannt {#still-unknown}

- Die öffentliche Plattform-API nennt für `live_duration` ein Maximum von 600 Sekunden, während der herstellereigene Integrationsleitfaden auf einen richtlinienspezifischen zurückgegebenen Wert verweist und 7200 Sekunden angibt. Es stand keine Antwort eines Live-Kontos zur Verfügung, um beide abzugleichen.
- Aktuelle Herstellerquellen widersprechen sich außerdem bei den Credit-Einheiten und den Zusatzkosten für Stimmklone. Verwenden Sie eine authentifizierte Konsole oder eine finale Abrechnungsantwort, bevor Sie ein Budget freigeben.
- Das verlinkte Vidu-S1-Repository stellt Dokumentation und Bilder bereit, keine öffentlichen Modellgewichte und kein lauffähiges Inferenzpaket. Lokale Bereitstellung und Modelllizenzrechte sind nicht verifiziert.
- Die Angaben zu 42 fps und langen Sitzungsdauern sind Herstellerangaben und Preprint-Behauptungen, keine unabhängige Garantie für Latenz oder Qualität in jeder Bereitstellung.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/shengshu-ai/Vidu-S1 | Vidu S1: Ein Echtzeit-interaktives Videogenerierungsmodell | 2026-09-06 |
| https://github.com/shengshu-ai/Vidu-S1/commits/main | Commits · shengshu-ai/Vidu-S1 · GitHub | 2026-09-06 |
| https://www.vidu.com/vidu-stream | Vidu S1 AI Video Model | Vidu AI | 2026-09-06 |
| https://platform.vidu.com/docs/vidu-s1 | Vidu S1 API (Beta) | Vidu API | 2026-09-06 |
| https://platform.vidu.com/docs/model-map | Modellübersicht | Vidu API | 2026-09-06 |
| https://platform.vidu.com/docs/pricing | Preise | Vidu API | 2026-09-06 |
| https://www.genspi.com/zh/news/vidu-s1-realtime-interactive-model/ | ShengShu veröffentlicht Vidu S1 und leitet die Ära der „Echtzeit-Interaktion“ in der Videogenerierung ein | 2026-09-06 |
| https://arxiv.org/html/2607.03118v1 | Vidu S1: Ein Echtzeit-interaktives Videogenerierungsmodell | 2026-09-06 |
| https://www.genspi.com/zh/news/vidu-s1-zhenhuan-digital-human/ | Technik stärkt IP-Erlebnisse: Vidu S1 hilft 360 bei einem neuen digitalen Menschen-Konzept für „Zhen Huan“ | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md | Vidu S1 Live API Integration | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/api-reference.md | Vidu S1 Live API — HTTP-Referenz | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/websocket-protocol.md | Vidu S1 Live API — WebSocket-Steuerprotokoll | 2026-09-06 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:vidu-s1`, Thread `vidu-s1`, 0 datierte Ereignisse - → -.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was überholt ist.
