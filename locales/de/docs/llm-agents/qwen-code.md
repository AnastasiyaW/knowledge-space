---
title: "Qwen Code"
description: "Versionsbewusste Installation, Authentifizierung, Diagnose und Projekthistorie für den Terminal-Coding-Agenten Qwen Code."
level: 3
source_sha256: b5ecf6ff343817ce528c90b70edc049b0e81a83be45fe5ae50a1f9d08cd0caf4
translation: machine
translated_at: '2026-10-24'
---
# Qwen Code {#qwen-code}

Qwen Code ist ein Terminal-Coding-Agent und ein Provider- und Runtime-Client. Die Versionierung muss unabhängig von der Qwen-Modellfamilie erfolgen, die er aufrufen kann. Der Status wurde am **2026-08-27** gegen das offizielle Repository, die Releases und die chinesische Dokumentation geprüft.

## Aktueller Status {#current-status}

| Bereich | Geprüfter Zustand |
|---|---|
| CLI-Release | `v0.22.2`, veröffentlicht am 2026-08-26 |
| Quellcode | Offizielles Repository `QwenLM/qwen-code` |
| Laufzeitvoraussetzung | Node.js 22 oder neuer für die npm-Installation |
| Einstiegspunkt für Authentifizierung | `/auth` innerhalb der CLI |
| Einstiegspunkt für Diagnose | `/doctor` innerhalb der CLI |
| Qwen OAuth/kostenloser Login | Laut der aktuellen chinesischen Schnellstartanleitung am 2026-04-15 eingestellt |
| Aktuelle Zugangswege | Alibaba-Cloud-Tarif/API-Schlüssel, unterstützter Drittanbieter-Provider oder benutzerdefinierte Provider-Konfiguration |

Die CLI-Version ist keine Modellversion. Eine Aussage wie „das neueste Modell ist Qwen3.6“ muss separat anhand des Provider-/Modellkatalogs geprüft werden und darf niemals aus der Release-Nummer von Qwen Code abgeleitet werden.

## Entwicklungshistorie {#development-history}

| Datum | Ereignis | Zeitlicher Status |
|---|---|---|
| 2025-07-23 | Erster Bericht zu Qwen Code | Historische Grundlage |
| 2025-09-24 | Aktualisierung des Qwen-Modells im Projektumfeld diskutiert | Ereignis im Ökosystem, kein CLI-Release von Qwen Code |
| 2025-10-11 | Updates der CLI `v0.0.12` bis `v0.0.14` gemeldet | Historisch; das genaue Changelog erfordert eine Rekonstruktion auf Release-Ebene |
| 2025-11-17 | CLI `v0.2.1` gemeldet | Historisch |
| 2026-04-13 | Späterer Bericht zu Funktionen/Version von Qwen Code | Beibehalten, Modellbezeichnungen aber separat erneut prüfen |
| 2026-04-15 | Qwen-OAuth-Weg eingestellt | Aktuelle Grenze der Authentifizierung |
| 2026-08-26 | `v0.22.2` veröffentlicht | Zum Prüfzeitpunkt aktuelles Release |

## Installation und erste Prüfung {#installation-and-first-check}

```bash
node --version
npm install -g @qwen-code/qwen-code@latest
qwen --version
```

Node muss die Hauptversion 22 oder neuer melden. In der interaktiven CLI ausführen:

```text
/auth
/doctor
```

Mit `/auth` einen aktuell unterstützten Provider-Weg auswählen. Nach der Installation oder immer dann `/doctor` verwenden, wenn sich Tools, Zugangsdaten oder die Erreichbarkeit des Providers anders verhalten als in der erwarteten Konfiguration.

## Provider-Vertrag {#provider-contract}

Provider und Modell explizit festhalten:

```yaml
qwen_code_version: 0.22.2
node_version: 22.x
provider: <alibaba-cloud-or-third-party-or-custom>
model: <exact-provider-model-id>
auth_method: <api-key-or-supported-plan>
workspace_trust: <trusted-or-untrusted>
```

Nicht stillschweigend von einem Provider oder Modell auf ein anderes zurückfallen. Eine erfolgreiche Anfrage über einen Ersatz-Provider beweist nicht, dass der konfigurierte Weg funktioniert.

## Betriebliche Nutzung {#operational-use}

- In reproduzierbaren oder teamweiten Umgebungen die CLI-Version fixieren; `@latest` ist nur geeignet, wenn bewusste Upgrades akzeptabel sind.
- `/doctor` ausführen und dessen Ausgabe festhalten, wenn Probleme mit Authentifizierung, Modell, Tools oder Umgebung diagnostiziert werden.
- Repository-Dateien, MCP-Inhalte, Shell-Ausgaben und Webseiten als nicht vertrauenswürdige Eingaben behandeln; abgerufener Text darf die Tool-Berechtigungen nicht erweitern.
- Projektanweisungen im Repository ablegen und Geheimnisse über den konfigurierten Mechanismus für Zugangsdaten speichern, nicht in committeten Prompts.
- CLI- und Provider-Modellversion gemeinsam in den Belegen der Agentenläufe festhalten.

## Englische und chinesische Dokumentation {#english-and-chinese-documentation}

Die chinesische Schnellstartanleitung und die Seite mit den Befehlen sind Quellen des Anbieters selbst und enthalten derzeit wichtige Änderungen bei der Authentifizierung. Sprachvarianten können auseinanderlaufen; Veröffentlichungs- bzw. Aktualisierungsdatum vergleichen und die Seite bevorzugen, die den aktiven Provider-Vertrag ausdrücklich dokumentiert.

## Community-Berichte {#community-reports}

- [Issue #2907](https://github.com/QwenLM/qwen-code/issues/2907) dokumentiert Qwen Code `0.14.0` unter Windows mit Windows PowerShell, obwohl der Nutzer PowerShell 7 wollte. Für das Issue gab es keine akzeptierte Lösung. Es belegt daher eine versionsgebundene Lücke bei der Shell-Auswahl, aber kein unterstütztes Konfigurationsrezept.
- [Issue #7433](https://github.com/QwenLM/qwen-code/issues/7433) dokumentiert, dass Qwen Code `0.20.0` über ACP `coder-model(qwen-oauth)` als aktuelles Modell meldet, obwohl ein lokales OpenAI-kompatibles Modell konfiguriert ist. Mitwirkende konnten das Registry-Leck reproduzieren und meldeten die Behebung in `v0.21.12`/`v0.21.13`. Tritt dieses Symptom auf, auf eine Version nach `0.20.0` aktualisieren und anschließend `/about` sowie die ACP-Modell-Nutzlast prüfen, statt Provider-Einstellungen zu löschen.
- Das zweite Issue ist zugleich ein konkreter Grund, in Agenten-Belegen jeden stillen Provider- oder Modell-Fallback zu untersagen.

## Stolperfallen {#gotchas}

- **Problem:** Einer alten Anleitung zum Qwen-OAuth-Login folgen -> **Lösung:** einen aktuellen Weg über Alibaba Cloud, einen Drittanbieter oder einen benutzerdefinierten Provider verwenden; OAuth wurde am 2026-04-15 eingestellt.
- **Problem:** Das CLI-Release mit dem Modell-Release gleichsetzen -> **Lösung:** `qwen_code_version`, `provider` und exaktes `model` getrennt festhalten.
- **Problem:** Installation unter einer älteren Node-Laufzeit -> **Lösung:** vor der npm-Installation Node.js 22+ prüfen und danach `/doctor` ausführen.
- **Problem:** Provider-Fallback erlauben, der eine fehlerhafte Konfiguration verdeckt -> **Lösung:** sichtbar fehlschlagen lassen und den Provider-/Modellweg im Lauf-Beleg erhalten.
- **Problem:** Annehmen, `pwsh` werde verwendet, weil es installiert ist -> **Lösung:** die tatsächlich genutzte Shell der fixierten Qwen-Code-Version prüfen; Issue #2907 dokumentiert eine Windows-Abweichung ohne bestätigte Lösung.

## Zeitlicher Status {#temporal-status}

- **Aktuell:** `v0.22.2`, Node.js 22+, `/auth`, `/doctor`, Provider-Wege ohne OAuth.
- **Abgelöst:** Anleitungen zu Qwen OAuth/kostenlosem Login, die vor dem 2026-04-15 verfasst wurden.
- **Historisch/teilweise rekonstruiert:** Berichte zu `v0.0.12`-`v0.0.14` und `v0.2.1`.
- **Muss erneut geprüft werden:** jede Bezeichnung „neuestes Qwen-Modell“, Kontingente, Preise oder Liste der unterstützten Provider.

## Agent-Briefing {#agent-brief}

Vor der Unterstützung bei Qwen Code das aktuelle Release und die Schnellstartanleitung abrufen. In jeder Antwort CLI-Version, Provider, Modell-ID und Authentifizierungsweg getrennt angeben. Verlangt eine alte Anleitung Qwen OAuth, diese als abgelöst kennzeichnen. `/doctor` als ersten diagnostischen Beleg verwenden, Geheimnisse aber nicht in Berichten offenlegen. Die Verfügbarkeit eines Modells nicht aus einer Nachrichtenschlagzeile oder der CLI-Version ableiten.

## Quellen {#sources}

- Offizielles Repository: https://github.com/QwenLM/qwen-code
- Offizielle Releases: https://github.com/QwenLM/qwen-code/releases
- Chinesische Schnellstartanleitung: https://qwenlm.github.io/qwen-code-docs/zh/users/quickstart/
- Chinesische Befehlsreferenz: https://qwenlm.github.io/qwen-code-docs/zh/users/features/commands/
- Bericht zur Auswahl von Windows PowerShell 7: https://github.com/QwenLM/qwen-code/issues/2907
- Fehler beim lokalen Modell-Routing in ACP und Hinweis zur behobenen Version: https://github.com/QwenLM/qwen-code/issues/7433
