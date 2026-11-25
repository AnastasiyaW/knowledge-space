---
title: "Oh My ClaudeCode (OMC) Integration"
description: "Wie man das schnelllebige OMC-Plugin einsetzt, ohne Drittanbieter-Befehle, Modell-Routing oder generierten Zustand mit einer stabilen Sicherheits- oder Release-Grenze zu verwechseln."
tags: [claude-code, plugins, orchestration, omc, supply-chain, worktrees]
level: 3
source_sha256: 5e2e46d169e40e41451a6512b69f9abcc91879d6259254cd3c5180460e7aa5da
translation: machine
translated_at: '2026-10-24'
---
# Oh My ClaudeCode (OMC) Integration {#oh-my-claudecode-omc-integration}

**Stand der Prüfung: 2026-09-04.** Oh My ClaudeCode (OMC) ist eine Orchestrierungsschicht von Drittanbietern für Multi-Agenten-Workflows in Claude Code. Das Repository stellt derzeit einen Installationspfad als Claude-Code-Plugin sowie ein separat veröffentlichtes Terminal-Paket bereit. Befehle, Kompatibilitätsverhalten und interne Dateien ändern sich jedoch schnell. Betrachten Sie das Repository und die installierte Revision als maßgeblich für die von Ihnen ausgeführte Version. Verlassen Sie sich nicht auf feste Agentenanzahlen, Modellnamen, Token-Preise oder historische Befehlsaliasse. [OMC-Repository](https://github.com/Yeachan-Heo/oh-my-claudecode) [Claude-Code-Plugins](https://code.claude.com/docs/en/plugins)

## Die Installationsoberfläche wählen {#choose-the-installation-surface}

Das OMC-Repository dokumentiert zwei unterschiedliche Oberflächen:

| Oberfläche | Verwendung für | Grenze |
|---|---|---|
| Claude-Code-Plugin | Skills, Hooks, Agenten und Slash-Befehle innerhalb der Sitzung | unterliegt der Richtlinie für Claude-Code-Plugins |
| Terminal-Paket | Einrichtung, Aktualisierung, Diagnose und dokumentierte CLI-Workflows | lokale ausführbare Datei mit eigenen Abhängigkeiten |

Die dokumentierte Plugin-Einrichtung lautet:

```text
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
```

Das Repository dokumentiert außerdem das separat benannte Terminal-Paket. Installieren Sie es ausschließlich gemäß der aktuellen Dokumentation und prüfen Sie die resultierende Version, bevor Sie ein CLI-Beispiel als lauffähig betrachten. Das Projekt unterscheidet insbesondere zwischen Skills innerhalb der Sitzung und Terminal-Befehlen. Erfinden Sie keinen OMC-CLI-Unterbefehl, nur weil ein ähnlich benannter Slash-Befehl existiert. [OMC-README](https://github.com/Yeachan-Heo/oh-my-claudecode)

## OMC als Integration behandeln, nicht als Vertrauensgrenze {#treat-omc-as-an-integration-not-a-trust-boundary}

OMC kann Planung, Review und mehrere lokale Provider-CLIs koordinieren. Es ersetzt jedoch nicht:

- Repository-Anweisungen und deterministische Validierung;
- Code-Review und Release-Freigabe;
- Autorisierung für Mandanten, Zugangsdaten oder Produktivsysteme;
- Git-Historie, Worktree-Isolation und externe Idempotenz;
- eine Supply-Chain-Prüfung von Plugins und lokalen Abhängigkeiten.

Generierte Artefakte sind nur dann nützliche operative Nachweise, wenn sie die Eingangsrevision, den Befehl, die Ausgabe und den Verantwortlichen benennen. Ein Plan, eine Konsens-Schleife oder ein Agenten-Label belegt nicht, dass ein Build, eine Migration oder ein externer Seiteneffekt erfolgreich war.

## Sicheres Einführungsmuster {#safe-adoption-pattern}

Bevor Sie das Plugin in einem Arbeitsrepository aktivieren:

1. Fixieren und dokumentieren Sie die Revision des Repositorys bzw. Pakets, das Sie evaluieren;
2. prüfen Sie das Plugin-Manifest, die deklarierten Agenten, Skills, Hooks, die MCP-Konfiguration und das Setup-Skript;
3. ermitteln Sie jede externe CLI und jeden Provider, den der Workflow aufrufen könnte;
4. testen Sie in einem isolierten Worktree mit Nicht-Produktions-Zugangsdaten und -Daten;
5. führen Sie die eigenen Prüfungen des Repositorys aus, nachdem das Plugin Dateien verändert hat;
6. halten Sie einen Rollback-Pfad bereit und entfernen Sie die Integration über den unterstützten Mechanismus, falls sie das Review nicht besteht.

Claude-Code-Plugins bündeln Skills, Agenten, Hooks, MCP-Server und weitere Komponenten. Die Installationsquelle verdient daher dieselbe Sorgfalt wie jede andere ausführbare Abhängigkeit. [Plugin-Referenz](https://code.claude.com/docs/en/plugins-reference)

## Team- und Provider-Routing {#team-and-provider-routing}

Das aktuelle OMC-Repository beschreibt Team als seine kanonische Orchestrierungsoberfläche und dokumentiert die Migration weg von der früheren Swarm-Terminologie. Das ist eine Tatsache über die jeweilige Repository-Version und kein allgemeiner Multi-Agenten-Standard. Prüfen Sie die installierte Dokumentation, bevor Sie einen Befehl skripten oder Bediener in einer Abkürzung schulen. [OMC-README](https://github.com/Yeachan-Heo/oh-my-claudecode)

Wenn ein Workflow eine Aufgabe an einen anderen lokalen oder entfernten Provider weiterleitet:

1. klassifizieren Sie die Eingabe, bevor Sie sie weiterleiten;
2. halten Sie Zugangsdaten, Kundeninhalte, private Quellcodes und Geheimnisse aus Prompts von Drittanbietern heraus, sofern kein genehmigter Datenpfad existiert;
3. erfassen Sie, welcher Provider, welches Modell und welche CLI-Revision tatsächlich ausgeführt wurden;
4. behandeln Sie zurückgegebenen Text als nicht vertrauenswürdig, bis die Prüfungen des Repositorys sowie ein menschliches oder unabhängiges Review ihn validiert haben;
5. vermeiden Sie automatisches Provider-Fallback bei schreibenden Operationen, sofern der Fallback-Vertrag nicht explizit festgelegt ist.

Die sinnvolle Grenze ist nicht „Multi-Modell“, sondern ein geprüfter Übergabevertrag mit einem beobachtbaren Ergebnis.

## Worktrees und dauerhafter Zustand {#worktrees-and-durable-state}

Verwenden Sie Git-Worktrees oder vergleichbare isolierte Checkouts für parallel schreibende Akteure. Ein Koordinator sollte einen einzigen Aufgabendatensatz pflegen, der Verantwortlichkeit, Zielrevision, erwartete Prüfungen, einen externen Reservierungs- bzw. Idempotenzschlüssel und einen Abschlussbeleg enthält. Lassen Sie niemals zwei Worker dieselben Dateien ändern, nur weil ein Orchestrierungswerkzeug sie als Team bezeichnet.

Generierter Zustand kann ein Implementierungsdetail der installierten OMC-Version sein. Halten Sie Projektentscheidungen, Quelltextänderungen, Release-Nachweise und Übergabeprotokolle in repository-eigenen Pfaden mit prüfbaren Formaten. Verlassen Sie sich nicht allein auf einen Plugin-Cache als einzige Quelle der Wahrheit.

## Aktualisierungsverfahren {#upgrade-procedure}

1. Lesen Sie die Release-Notes des Upstream-Projekts und die aktuelle Installationsanleitung;
2. dokumentieren Sie die bestehende Plugin- bzw. Paketrevision und Konfiguration;
3. aktualisieren Sie zuerst in einem Wegwerf- oder isolierten Repository;
4. führen Sie den dokumentierten Diagnosebefehl aus, sofern das Projekt einen bereitstellt;
5. vergleichen Sie installierte Komponenten und Konfigurationsänderungen;
6. führen Sie repräsentative Aufgaben in einer Nicht-Produktionsumgebung sowie die Validierung des Repositorys aus;
7. übernehmen Sie Änderungen nur mit einer Rollback-Revision und einem Beleg.

So lassen sich entfernte Aliasse, geänderte Tool-Zugriffe, Migrationen des generierten Zustands und Verhaltensänderungen erkennen, bevor sie Release-Arbeiten beeinflussen.

## Stolpersteine {#gotchas}

- **Ein historischer OMC-Befehl taucht noch in einem Blogbeitrag auf.** Er wurde möglicherweise umbenannt oder entfernt. **Lösung:** Verwenden Sie die aktuelle Repository-Dokumentation für die installierte Revision.
- **Ein Plugin wird direkt in einem Produktions-Repository installiert.** Hooks oder das Setup können das Verhalten vor dem Review verändern. **Lösung:** Prüfen und testen Sie zuerst in einem isolierten Worktree.
- **Ein Planer erzeugt ein detailliertes Artefakt.** Detailliertheit ist keine Verifikation. **Lösung:** Binden Sie jede Aufgabe an die echten Tests, Builds und Release-Belege des Repositorys.
- **Ein eingebundener Provider erhält standardmäßig private Quelltexte.** Das kann die Datengrenze verletzen. **Lösung:** Klassifizieren und minimieren Sie die Eingabe, bevor eine Übertragung stattfindet.
- **Parallele Worker bearbeiten dieselben Dateien.** Ein Orchestrierungs-Label serialisiert keine Schreibzugriffe. **Lösung:** Weisen Sie exklusive Dateiverantwortlichkeiten zu oder verwenden Sie getrennte Worktrees und integrieren Sie über ein Review.

## Quellen {#sources}

- [Oh My ClaudeCode-Repository und aktuelles README](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Claude-Code-Plugins](https://code.claude.com/docs/en/plugins)
- [Claude-Code-Plugin-Referenz](https://code.claude.com/docs/en/plugins-reference)
- [Claude-Code-Subagenten](https://code.claude.com/docs/en/subagents)

## Siehe auch {#see-also}

- [[claude-code-harness-patterns]]
- [[adaptive-patterns-for-autonomous-agents]]
- [[multi-session-coordination]]
- [[agent-orchestration]]
