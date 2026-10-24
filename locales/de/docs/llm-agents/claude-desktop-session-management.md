---
title: "Claude Desktop Daten- und Sitzungssicherheit"
description: "Unterstützte Export-, Konto- und Erweiterungssteuerungen verwenden, statt für die Wiederherstellung von Unterhaltungen oder die geräteübergreifende Synchronisierung auf unversionierte lokale Cache-Interna zu setzen."
tags: [claude-desktop, data-export, privacy, extensions, troubleshooting]
level: 3
source_sha256: b45629cca63517bdb3b0ca57da0693decce068c03455fae92e2f40ed547f9ba4
translation: machine
translated_at: '2026-10-24'
---
# Claude Desktop Daten- und Sitzungssicherheit {#claude-desktop-data-and-session-safety}

**Geprüft am Stand: 2026-09-04.** Claude Desktop ist eine kontogebundene Anwendung und keine unterstützte API für lokale Sitzungsdateien. Die öffentliche Dokumentation von Anthropic beschreibt unterstützte Steuerungen für den Export von Konto- und Chatdaten sowie für die Verwaltung von Desktop-Erweiterungen. Sie garantiert jedoch kein stabiles Schema für Unterhaltungen auf dem Datenträger, keinen festen Cache-Pfad, kein VM-Bundle und keinen kopierbasierten Wiederherstellungsablauf für die geräteübergreifende Nutzung. [Exportieren Sie Ihre Claude-Daten](https://support.claude.com/en/articles/9450526-export-your-claude-data) [Claude-Desktop-Erweiterungen](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)

## Zuerst unterstützte Steuerungen verwenden {#use-supported-controls-first}

| Bedarf | Unterstützter Weg | Nicht verlassen auf |
|---|---|---|
| Chatverlauf sichern oder einsehen | Datenexport anfordern unter Einstellungen → Datenschutz | Auslesen von Cache-Dateien der Anwendung |
| ein Code-Projekt zwischen Rechnern verschieben | Git, ein Repository-Remote und projekteigene Artefakte | Kopieren des Anwendungszustands von Desktop |
| eine bestimmte Unterhaltung teilen | die Teilen- und Freigabe-Aufhebung des Produkts | Senden roher Datenbank- oder Cache-Dateien |
| lokale Integrationen verwalten | Einstellungen → Erweiterungen oder freigegebene Erweiterungspakete | undokumentierte Konfigurationsordner |
| eine Erweiterung diagnostizieren | Erweiterungsstatus und Protokolle der Anwendung | Löschen nicht zugehöriger Anwendungsdaten |

Einzelnutzer können einen Export über die Web-App oder Claude Desktop anfordern. Inhaber von Team- und Enterprise-Konten verfügen über entsprechende organisatorische Exportsteuerungen. Der resultierende Download-Link wird per E-Mail zugestellt und läuft ab. Behandeln Sie ihn daher als sensible Daten. [Exportieren Sie Ihre Claude-Daten](https://support.claude.com/en/articles/9450526-export-your-claude-data)

## Projektkontinuität außerhalb des Chat-Clients sichern {#keep-project-continuity-outside-the-chat-client}

Bei Arbeiten, die Geräte-, Konto- oder Client-Wechsel überstehen müssen, persistieren Sie den tatsächlichen Projektzustand in dessen eigenem System:

```text
source and decisions     → Git-backed project files
running-job checkpoints  → service-owned durable storage
credentials              → approved secret store
chat history             → account export when needed
local extension settings → Claude Desktop or organization policy
```

Gehen Sie nicht davon aus, dass eine sichtbare Unterhaltung, die Seitenleiste der Anwendung und lokale temporäre Dateien dieselbe Aufbewahrungs- oder Synchronisierungslogik haben. Die Produktoberfläche und der Kontoexport sind der unterstützte Weg, Nutzerdaten aus Unterhaltungen abzurufen. Implementierungsdetails können sich ohne Kompatibilitätsgarantie ändern.

## Triage bei fehlender Unterhaltung {#a-safe-missing-conversation-triage}

Wenn der Verlauf fehlt oder ein Desktop-Client sich unerwartet verhält:

1. Anwendungsversion, Betriebssystem, Konto- bzw. Workspace-Kontext und das genaue, für Nutzer sichtbare Symptom festhalten;
2. prüfen, ob dasselbe Konto in der unterstützten Claude-Oberfläche den erwarteten Zustand zeigt;
3. das Projekt-Repository und unabhängige Aufgabenbelege sichern, bevor der Client untersucht wird;
4. für historische Daten den Produkt-Support, die Kontosteuerungen oder einen Datenexport nutzen;
5. eine geschwärzte Diagnose erfassen und vor dem Löschen oder Kopieren von Anwendungsdaten anhalten;
6. Neuinstallation, Zurücksetzen oder Datenlöschung nur nach den aktuellen Supportanweisungen des Produkts und erst nach Sicherung der erforderlichen Artefakte durchführen.

Diese Abfolge trennt ein Anzeigeproblem des Clients von einem Problem im Repository oder im externen Workflow, ohne ein Dateisystem-Wiederherstellungsverfahren zu erfinden.

## Desktop-Erweiterungen sind eine eigene Grenze {#desktop-extensions-are-a-separate-boundary}

Desktop-Erweiterungen können Claude Desktop mit lokalen Werkzeugen und Daten verbinden. Anthropic dokumentiert die Installation über Einstellungen → Erweiterungen, ein Erweiterungsverzeichnis und benutzerdefinierte Pakete. Aktuelle Hinweise beschreiben außerdem Organisationssteuerungen und Plattformrichtlinien. Behandeln Sie jede Erweiterung als Code mit Zugriff auf die Ressourcen, die ihre Konfiguration erlaubt. [Lokale MCP-Server auf Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)

Bevor Sie eine Erweiterung aktivieren:

1. Herausgeber, Version, Berechtigungen und Datenfluss ermitteln;
2. geprüfte oder organisatorisch freigegebene Pakete bevorzugen;
3. den engsten Dateisystem-, Netzwerk- und Geheimniszugriff verwenden, der nötig ist;
4. in einem Nicht-Produktions-Workspace testen;
5. Paket, Version und Freigabenachweis aufbewahren;
6. die Erweiterung über den unterstützten Verwaltungsweg entfernen oder widerrufen, sobald ihr Zweck entfällt.

Bei Team- und Enterprise-Bereitstellungen können Organisations- und Geräterichtlinien steuern, ob Desktop-Erweiterungen und Verzeichnisse verfügbar sind. Eine lokale Benutzereinstellung ist nicht zwingend die wirksame Richtlinie. [Verwaltung von Desktop-Erweiterungen](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)

## Datenschutz und Teilen {#privacy-and-sharing}

Chats sind standardmäßig privat. Ein Link zu einem geteilten Chat macht jedoch den zum Teilen ausgewählten Snapshot zugänglich. Prüfen und widerrufen Sie geteilte Links über die Datenschutzsteuerungen des Produkts, statt anzunehmen, dass das Löschen eines lokalen Artefakts eine geteilte Kopie verändert. [Chats teilen und Teilen aufheben](https://privacy.anthropic.com/en/articles/10593882-sharing-and-unsharing-chats)

Datenexporte und Diagnosepakete können sensible Unterhaltungen, Metadaten oder Kontoinformationen enthalten. Speichern Sie sie an einem freigegebenen, privaten Ort, beschränken Sie den Zugriff und legen Sie sie nicht in Repositories, Tickets, öffentlichen Issue-Trackern oder Modell-Prompts ab.

## Was diese Seite nicht behauptet {#what-this-page-does-not-claim}

Diese Seite schreibt bewusst keinen Verzeichnisnamen, keinen Datenbanktyp, kein VM-Image, keine verborgene Sitzungsregistrierung, keine Anleitung zum Leeren des Caches, keinen versionsspezifischen Fehler und kein Synchronisierungswerkzeug eines Drittanbieters vor. Solche Aussagen würden einen aktuellen unterstützten Vertrag oder eine reproduzierbare, eng begrenzte Untersuchung voraussetzen. Ohne beides wären sie unsichere Wiederherstellungsempfehlungen.

## Stolperfallen {#gotchas}

- **Ein Cache-Ordner wirkt wie ein Export.** Er kann unvollständig, verschlüsselt, transient oder privater Implementierungszustand sein. **Abhilfe:** den Exportmechanismus des Produkts für den Chatverlauf verwenden.
- **Das Kopieren von Anwendungsdaten scheint einen Rechner wiederherzustellen.** Dabei können Zugangsdaten kopiert werden, eine andere Installation beschädigt werden oder nicht unterstützter Zustand entstehen. **Abhilfe:** für Projektarbeit Git und für Chats die unterstützten Kontosteuerungen verwenden.
- **Ein Zurücksetzen dient als erste Diagnose.** Dabei können Belege für den Support verloren gehen. **Abhilfe:** zuerst das Symptom festhalten und unabhängige Projektartefakte sichern.
- **Einer Erweiterung wird vertraut, weil sie mit einem Klick installiert wird.** Installationskomfort ist keine Berechtigungsprüfung. **Abhilfe:** Herausgeber, Umfang und Organisationsrichtlinie prüfen, bevor die Erweiterung aktiviert wird.
- **Ein geteilter Chat wird für ein privates Backup gehalten.** Wer den Link besitzt, kann auf den Snapshot zugreifen. **Abhilfe:** Freigaben über die Datenschutzsteuerungen prüfen und widerrufen.

## Quellen {#sources}

- [Exportieren Sie Ihre Claude-Daten](https://support.claude.com/en/articles/9450526-export-your-claude-data)
- [Einstieg in lokale MCP-Server auf Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Wann Desktop- und Web-Connectors verwendet werden sollten](https://support.anthropic.com/en/articles/11725091-when-to-use-desktop-and-web-connectors)
- [Chats teilen und Teilen aufheben](https://privacy.anthropic.com/en/articles/10593882-sharing-and-unsharing-chats)

## Siehe auch {#see-also}

- [[claude-code-ecosystem]]
- [[agent-memory]]
- [[context-engineering]]
- [[agentic-security-2026]]
