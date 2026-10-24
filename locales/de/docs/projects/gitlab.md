---
title: "Gitlab: gitlab-critical-vulnerability-patch-19-5-1 — Gitlab kritischer Schwachstellen-Patch 19 5 1"
category: "projects"
date: 2026-10-22
tags: ["gitlab", "gitlab-critical-vulnerability-patch-19-5-1", "project"]
aliases: ["Gitlab: gitlab-critical-vulnerability-patch-19-5-1"]
level: 2
source_sha256: 8adfa4680d5bd54ed043af0cd330c8563fd90e5d706bcac91ee4e134c533841e
translation: machine
translated_at: '2026-10-24'
---
# Gitlab: gitlab-critical-vulnerability-patch-19-5-1 — Gitlab kritischer Schwachstellen-Patch 19 5 1 {#gitlab-gitlab-critical-vulnerability-patch-19-5-1-gitlab-critical-vulnerability-patch-19-5-1}

**Entwicklungslinie:** project:gitlab · thread gitlab-critical-vulnerability-patch-19-5-1  
**Letztes Ereignis:** 2026-10-22 · 2 datierte Einträge seit 2026-10-22 · **Recherchiert:** 2026-10-23 · Konfidenz: hoch

## Worum es geht {#what-it-is}

GitLab 19.5.1 ist ein Notfall-Sicherheitsrelease für selbst gehostetes GitLab, die Plattform für Code-Zusammenarbeit und DevOps. Es behebt eine unauthentifizierte Remote-Code-Execution-Schwachstelle im Regular-Expression-Compiler und stellt die Speichersicherheit auf selbst gehosteten Installationen wieder her. Die Fixes werden in ältere Release-Branches zurückportiert, und die zentralen Git-Workflows ändern sich nicht.

Es gibt keinen Konfigurations-Workaround, daher ist das einzige Gegenmittel, das Binary bzw. Paket jetzt zu aktualisieren. Nach dem Update entfällt das Risiko einer Server-Übernahme, und bestehende Repositories und CI-Pipelines bleiben unverändert.

## Entwicklungslinie {#development-line}

- **2026-10-22 — GitLab behebt eine Remote-Code-Execution-Schwachstelle mit höchstem Schweregrad.** Die Schwachstelle wurde mit 10/10 bewertet und erlaubte es jedem, beliebigen Code auf dem Server auszuführen, ohne sich anzumelden. Sie betrifft Versionen ab 7.0. GitLab.com war bereits gepatcht, selbst verwaltete Nutzer wurden aufgefordert, sofort auf das Patch-Release GitLab 19.5.1 zu aktualisieren.
- **2026-10-22 — GitLab patcht eine kritische unauthentifizierte Code-Execution-Schwachstelle.** Mit 10/10 im Schweregrad bewertet, ermöglichte sie die Ausführung beliebigen Codes auf dem Server ohne Anmeldung, in Versionen ab 7.0. Die cloudgehostete Instanz GitLab.com war bereits gepatcht. Selbst verwaltete Nutzer wurden angewiesen, sofort mit dem Patch-Release 19.5.1 zu aktualisieren.
- **2026-10-22 — weitere Details vom selben Datum.**
  - Die Schwachstelle ist CVE-2026-110264, CVSS 10.0. Sie entsteht durch einen Integer-Overflow im Regular-Expression-Compiler (Onigmo) und wurde vom Forscher joaxcar über HackerOne gemeldet. Zurückportierte Releases sind 19.4.3, 19.3.6, 19.2.9, 19.1.9, 19.0.10 und 18.11.13; sie decken ältere Branches bis zurück zur Version 7.0 ab. (2026-10-22) — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
  - Der Code läuft als Benutzer git und benötigt keine Berechtigungen. Auslöser ist ein präparierter Ausdruck in einem Dokument-Rendering-Pfad wie Org-mode. Es gibt keinen Konfigurations-Workaround; nur ein Update hilft. (2026-10-22) — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Was sich geändert hat {#what-changed}

GitLab hat Notfall-Patches für aktive und ältere Release-Branches ausgeliefert, um einen Integer-Overflow im Regular-Expression-Compiler zu beheben. Der Hauptentwicklungsstrang hat das Sicherheitsupdate erhalten, und die Backports erreichen ältere Wartungszweige bis zur ersten betroffenen Version. Außerdem wurden automatisierte Testregeln und Signaturen zur Fehlererkennung veröffentlicht, damit Administratoren Worker-Prozesse auf Ausnutzungsversuche überwachen können.

## So wird es angewendet {#how-to-use-this}

1. Ermitteln Sie die Version Ihrer selbst verwalteten GitLab-Instanz im Admin-Dashboard oder führen Sie auf dem Host gitlab-rake gitlab:env:info aus.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
2. Wählen Sie den Patch für Ihre Versionslinie: 19.5.x auf 19.5.1, 19.4.x auf 19.4.3, 19.3.x auf 19.3.6, 19.2.x auf 19.2.9, 19.1.x auf 19.1.9, 19.0.x auf 19.0.10 sowie ältere Versionen von 7.0 bis 18.11.x auf 18.11.13.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
3. Führen Sie das Update über den Paketmanager aus oder ziehen Sie das Container-Image neu, und starten Sie anschließend die GitLab-Dienste neu, damit die neuen Binaries wirksam werden.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
4. Prüfen Sie die Puma-Worker-Logs und die Anwendungs-Fehlerlogs auf Fehler des Regular-Expression-Compilers oder auf ungewöhnliche Worker-Abbrüche. Diese deuten auf frühere Ausnutzungsversuche hin.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Bewährte Vorgehensweisen {#best-practices}

- Patchen Sie aus dem Internet erreichbare, selbst verwaltete Instanzen umgehend, da der Angriff keine Zugangsdaten und keine Benutzerinteraktion erfordert.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
- Aktualisieren Sie direkt auf das Patch-Release innerhalb Ihres aktuellen Minor-Branches, damit unnötige Datenbankmigrationen entfallen und die Ausfallzeit gering bleibt.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>
- Verlassen Sie sich nicht allein auf Firewall-Regeln am Perimeter oder auf Konfigurations-Workarounds, da schädliche reguläre Ausdrücke über viele Dokument-Rendering-Pfade eintreffen können.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Ungepatchte, selbst verwaltete GitLab-Instanzen der Versionen 7.0 bis 19.5.0 gelten als sicher gegen unauthentifizierte Remote-Code-Execution.
  — <https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/>

## Weiterhin unbekannt {#still-unknown}

- Sekundäre Medienberichterstattung und Community-Diskussionen sind nicht belegt. Ihre Suchlinks leiteten auf unklare Ziele weiter, und stabile direkte URLs konnten nicht bestätigt werden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/ | GitLab Critical Security Release: Patch Release 19.5.1 | 2026-10-23 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** project:gitlab, thread gitlab-critical-vulnerability-patch-19-5-1, 2 datierte Ereignisse vom 2026-10-22 bis 2026-10-22.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich deren Grenzen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
