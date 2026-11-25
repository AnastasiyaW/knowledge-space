---
title: "Claude Mythos"
category: projects

tags: [claude-mythos, claude-mythos-security-findings, claude_mythos_security_findings, project]
aliases: ["Claude Mythos"]
level: 3
source_sha256: 881b9c435411d28add32e46b68dc44d222dd0e249fa83bbdb00721871cd684cf
translation: machine
translated_at: '2026-10-24'
---
# Claude Mythos {#claude-mythos}

**Entwicklungslinie:** `project:claude-mythos` · Thread `claude-mythos-security-findings`  
**Letztes Ereignis:** - · 0 datierte Einträge seither · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Anthropics Modelllinie mit Einladungsprinzip für ausgewählte Cyberabwehr-Teams und Teams für kritische Software.

- Scannt eigene Codebasen auf kontextbezogene Schwachstellenbefunde und vorgeschlagene Korrekturen.
- Direkter Zugriff nur für zugelassene Partner von Project Glasswing.
- Stellt die Scans von Claude Security bereit, ohne direkten Modellzugriff offenzulegen.

## Entwicklungslinie {#development-line}

- Die datierte Entwicklungslinie ist noch nicht aufbereitet; der aktuelle Kenntnisstand steht in den folgenden Abschnitten.

## Was sich geändert hat {#what-changed}

- 2026-04-07 — Anthropic kündigte Claude Mythos Preview und Project Glasswing an. Die Preview ging an Launch-Partner und mehr als 40 Organisationen der kritischen Infrastruktur, und zwar für defensive Arbeit statt für eine allgemeine Veröffentlichung.
- 2026-04-10 — Die datierte Anleitung von Anthropic identifiziert das Modell als Claude Mythos Preview und ordnet diesen Schritt als operative Anleitung nach dem Launch ein, nicht als zweite Modellveröffentlichung. KI verkürzt die Zeiträume für das Auffinden von Schwachstellen und für Exploits; Anthropic empfiehlt, die Patch-Lücke zu schließen und KEV-Einträge dringend zu beheben.
- 2026-06-09 — Claude Mythos 5 (`claude-mythos-5`) ersetzte die Preview für berechtigte Glasswing-Teilnehmer. Es teilt sich das Basismodell von Fable 5 und entfernt für zugelassene Nutzer die Cyber-Schutzmaßnahmen; dokumentierte Grenzen waren 1M Kontext, 128K Ausgabe und $10/$50 pro Million Eingabe-/Ausgabe-Token.
- 2026-08-21 — Die öffentliche Beta von Claude Security für Enterprise begann, Repository-Scans auf Mythos 5 auszuführen und Befunde sowie vorgeschlagene Korrekturen zurückzugeben, ohne dass direkte Mythos-Prompts nötig sind.
- 2026-08-31 — Claude Mythos 5.1 wurde für zugelassene Partner als Covered Model mit begrenzter Verfügbarkeit ausgewiesen.
- 2026-09-01 — Claude Mythos 5.1 wurde das aktuelle Mythos-Modell mit direktem Zugriff, weiterhin nur auf Einladung über Project Glasswing.

## Wie das zu verwenden ist {#how-to-use-this}

Stand 2026-04-10 sollte auf Basis dieser Entwicklungslinie keine operative Änderung vorgenommen werden, bis der zugrunde liegende Beitrag oder die Quelle abgerufen und geprüft wurde.

1. Aktivieren Sie Claude Security in den Organisationseinstellungen unter Claude Enterprise.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
2. Verbinden Sie ein berechtigtes GitHub-Konto und wählen Sie dann in Claude Security ein eigenes Repository auf GitHub.com oder GitHub Enterprise Server aus.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
3. Starten Sie den Scan und prüfen Sie anschließend für jeden Befund die CWE-Kategorie, den Schweregrad, die Konfidenz, den Reproduktionspfad und die vorgeschlagene Korrektur.
  — <https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders>
4. Öffnen Sie eine vorgeschlagene Korrektur in Claude Code und lassen Sie sie vor der Umsetzung von einem Menschen prüfen, testen und freigeben.
  — <https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders>
5. Für die direkte Nutzung von Mythos 5.1 holen Sie die Freigabe von Project Glasswing über ein Account-Team von Anthropic, AWS oder Google Cloud ein; verwenden Sie die Modell-ID `claude-mythos-5-1` erst, wenn der Zugang gewährt wurde.
  — <https://platform.claude.com/docs/en/models/mythos-5-1/overview>

## Bewährte Praktiken {#best-practices}

- Scannen Sie nur Code, den die Organisation besitzt oder für den sie Scanrechte hat.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
- Behandeln Sie Scans als stochastische Evidenz und nicht als Ersatz für Validierung; Schweregradeinstellungen sind nicht konfigurierbar.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
- Patchen Sie internetexponierte Systeme innerhalb von 24 Stunden, nachdem ein Exploit verfügbar ist; beheben Sie zuerst KEV-Einträge und priorisieren Sie die übrige Warteschlange mit EPSS.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>
- Senden Sie einen Schwachstellenbericht erst nach menschlicher Verifizierung; fügen Sie den verwundbaren Codepfad, eine lauffähige Reproduktion und einen vorgeschlagenen Patch bei und legen Sie offen, dass KI beteiligt war.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>
- Beginnen Sie die KI-gestützte Alarmtriage mit reinem Lesezugriff und messen Sie die Übereinstimmung mit einem menschlichen Prüfer, bevor Sie die Automatisierung ausweiten.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>

## Durch Folgendes ersetzt {#superseded-by-this}

- 2026-06-09 — Claude Mythos Preview ist veraltet; berechtigte Nutzer wurden auf Claude Mythos 5 umgestellt.
- 2026-09-01 — Claude Mythos 5 ist nicht mehr das aktuelle Ziel für direkten Zugriff; berechtigte Partner sollten auf Claude Mythos 5.1 migrieren.
- 2026-08-21 — Direkte Prompts sind für Mythos nicht mehr erforderlich: Claude Security liefert begrenzte defensive Befunde, ohne das Modell offenzulegen.

## Weiterhin unbekannt {#still-unknown}

- Der Eintrag vom 2026-04-10 hat weder eine URL noch einen Text, daher lässt sich seine genaue Aussage nicht eindeutig mit der datierten Anleitung von Anthropic abgleichen.
- Die aktuelle Dokumentation nennt Mythos 5 für Claude-Security-Scans und Mythos 5.1 für den direkten Partnerzugriff; sie bestätigt nicht, dass Claude Security auf 5.1 umgestellt wurde.
- Ein öffentlicher Self-Service-Weg zum direkten Zugriff auf Mythos 5.1 ist nicht dokumentiert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.anthropic.com/research/mythos-preview | Assessing Claude Mythos Preview’s cybersecurity capabilities | 2026-09-05 |
| https://www.anthropic.com/glasswing | Project Glasswing: Securing critical software for the AI era | 2026-09-05 |
| https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense | Preparing your security program for AI-accelerated offense | 2026-09-05 |
| https://www.anthropic.com/news/claude-fable-5-mythos-5 | Claude Fable 5 and Claude Mythos 5 | 2026-09-05 |
| https://platform.claude.com/docs/en/models/mythos-5/overview | Claude Mythos 5 - Claude Platform Docs | 2026-09-05 |
| https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders | Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders | 2026-09-05 |
| https://platform.claude.com/docs/en/models/mythos-5-1/overview | Claude Mythos 5.1 - Claude Platform Docs | 2026-09-05 |
| https://support.claude.com/en/articles/14661296-use-claude-security | Use Claude Security | 2026-09-05 |
| https://support.claude.com/en/articles/15425695-covered-models | Covered Models | 2026-09-05 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Model deprecations - Claude Platform Docs | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:claude-mythos`, Thread `claude-mythos-security-findings`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-04-10 sollte auf Basis dieser Entwicklungslinie keine operative Änderung vorgenommen werden, bis der zugrunde liegende Beitrag oder die Quelle abgerufen und geprüft werden kann.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
