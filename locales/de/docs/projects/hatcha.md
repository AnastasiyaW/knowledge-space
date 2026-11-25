---
title: "HATCHA — Referenz zum öffentlichen Repository"
category: projects
date: 2026-06-27
tags: [hatcha, project, public-repository-reference]
aliases: ["HATCHA"]
level: 2
source_sha256: b7f3dcb2c0a3bb9f437c160f094637a6c155916d1aa7b55836cd5a9f8a521b12
translation: machine
translated_at: '2026-10-24'
---
# HATCHA — Referenz zum öffentlichen Repository {#hatcha-public-repository-reference}

**Entwicklungslinie:** `project:hatcha` · Thread `public-repository-reference`  
**Letztes Ereignis:** 2026-06-27 · 1 datiertes seit 2026-06-27 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

HATCHA ist ein Open-Source-Reverse-CAPTCHA von monday.com für Next.js und Express. Es stellt eine Rechenaufgabe, speichert die Antwort ausschließlich auf dem Server, signiert Hash und Ablaufzeit mit einem HMAC-Token und gibt ein Verifizierungstoken zurück.

- Fünf eingebaute Challenges: Ausführung von Rechenaufgaben zur Verifizierung von Agenten.
- React-Komponenten: Bereitstellung der Client-Integration und von Provider-Wrappern.
- Server-Handler: Weiterleitung von Verifizierungsanfragen in Next.js und Express.
- Eigene Generatoren: Registrierung nicht standardisierter Challenges.

Eingebaute Challenges sind auf 30 Sekunden begrenzt.

Damit ist HATCHA eine zusätzliche Sperre für risikoarme, rein agentenbasierte Szenarien, kein Nachweis von Identität, Berechtigung oder Sicherheit eines Agenten.

## Entwicklungslinie {#development-line}

- **2026-06-27 — Auf das GitHub-Repository von HATCHA wurde verwiesen.** Das Monorepo gliedert sich in die Pakete Core, React und Server, mit Adaptern für Next.js und Express.

## Was sich geändert hat {#what-changed}

2026-06-27 — monday.com hat HATCHA als öffentliches MIT-Projekt veröffentlicht. Das Monorepo gliedert sich in die Pakete Core, React und Server, mit Adaptern für Next.js und Express.

## So wird es verwendet {#how-to-use-this}

Nach dem Repository-Verweis vom 2026-06-27 können wir das GitHub-Repository von HATCHA als Implementierungsquelle behandeln. Prüfen Sie Inhalte und Release-Status, bevor Sie sich auf ein bestimmtes Feature verlassen.

1. Installieren Sie die React- und Server-Pakete: `npm install @mondaycom/hatcha-react @mondaycom/hatcha-server`.
  — <https://github.com/mondaycom/HATCHA>
2. Legen Sie mit `createHatchaHandler` einen Route-Handler für Next.js an und übergeben Sie einen eindeutigen serverseitigen `HATCHA_SECRET`.
  — <https://github.com/mondaycom/HATCHA>
3. Umschließen Sie die Anwendung mit `HatchaProvider`, importieren Sie die Styles und rufen Sie `requestVerification` vor der Ziel-Aktion für Agenten auf.
  — <https://usehatcha.dev/>
4. Verifizieren Sie das ausgestellte Verifizierungstoken auf dem Server, bevor Sie die geschützte Aktion zulassen; Challenge und Antwort dürfen nicht als clientseitige Geheimnisse offengelegt werden.
  — <https://github.com/mondaycom/HATCHA>

## Bewährte Praktiken {#best-practices}

- Setzen Sie HATCHA vor risikoarme, rein agentenbasierte Workflows, Demos oder Sandboxes, behalten Sie aber für Daten- oder Finanzaktionen separate Authentifizierung, Autorisierung, Audit-Logs, Schutzmaßnahmen gegen Missbrauch und Ausgabenlimits bei.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Halten Sie `HATCHA_SECRET` strikt auf dem Server, verwenden Sie einen starken Wert und setzen Sie Rate Limits zusammen mit einem explizit dokumentierten Bedrohungsmodell.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Registrieren Sie einen eigenen Challenge-Generator für nicht standardisierte Anwendungsfälle, behalten Sie aber die serverseitige Verifizierung und eine begrenzte TTL bei.
  — <https://github.com/mondaycom/HATCHA>

## Durch dieses ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Das Repository hat keine veröffentlichten GitHub Releases; die Primärquellen nennen weder den genauen Commit noch die Version, die dem 2026-06-27 entspricht.
- Es gibt keinen primären Changelog-Eintrag mit dem Datum 2026-06-27; die Details stützen sich auf eine Veröffentlichung vom 2026-06-26 und die aktuelle Dokumentation, sodass spätere Änderungen unbestätigt bleiben.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/mondaycom/HATCHA | GitHub — mondaycom/HATCHA | 2026-09-05 |
| https://usehatcha.dev/ | HATCHA — Reverse CAPTCHA für KI-Agenten | 2026-09-05 |
| https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents | Monday.com veröffentlicht HATCHA, ein Reverse CAPTCHA für KI-Agenten | 2026-09-05 |
| https://developer-community.monday.com/ai-category-25/welcoming-agents-to-the-ecosystem-5206 | Willkommen Agenten im Ökosystem | 2026-09-05 |
| https://developer.monday.com/api-reference/docs/build-on-monday-with-ai | Auf monday.com mit KI aufbauen | 2026-09-05 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:hatcha`, Thread `public-repository-reference`, 1 datiertes Ereignis 2026-06-27 → 2026-06-27.
- **Praktischer Hinweis:** Nach dem Repository-Verweis vom 2026-06-27 können wir das GitHub-Repository von HATCHA als Implementierungsquelle behandeln; Inhalte und Release-Status sind vor dem Verlassen auf ein bestimmtes Feature zu prüfen.
- **Konfidenz:** mittel. Datierte Ersetzungen oberhalb sind maßgeblich dafür, was veraltet ist.
