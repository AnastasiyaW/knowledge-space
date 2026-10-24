---
title: "Claude Code-Erweiterungs- und Governance-Oberflächen"
description: "Claude Code-Plugins, Skills, Hooks, Projektanweisungen und Subagenten als explizite, versionierte Governance-Oberflächen nutzen; deren aktuelles Schema und den effektiven Geltungsbereich vor dem Rollout prüfen."
tags: [claude-code, plugins, skills, hooks, subagents, governance]
level: 3
source_sha256: ac26a4cb1674052c821758614a66d72ab5acb94f7b69a08c2b2dcd1869182d89
translation: machine
translated_at: '2026-10-24'
---
# Claude Code-Erweiterungs- und Governance-Oberflächen {#claude-code-extension-and-governance-surfaces}

**Stand der Prüfung: 2026-09-04.** Claude Code kann eine Sitzung über Projektanweisungen, Plugins, Skills, Hooks und Subagenten erweitern. Dabei handelt es sich um getrennte Steuerungsoberflächen mit unterschiedlichen Lebenszyklen und Berechtigungen. Eine bequeme Erweiterung ist kein Nachweis dafür, dass eine Aufgabe in einer bestimmten Cloud-Umgebung ausgeführt wurde, dass eine Richtlinie überall durchgesetzt wird oder dass ein Plugin sicher zu installieren ist.

## Die kleinste geeignete Steuerungsoberfläche wählen {#choose-the-smallest-control-surface}

| Bedarf | Geeignete Oberfläche | Aufzubewahrende Nachweise |
|---|---|---|
| stabile Repository-Vorgaben | Projektanweisungsdatei | geprüfte Quellrevision und effektive Anweisungen |
| wiederverwendbares Aufgabenvorgehen | Skill | Auslöser, Geltungsbereich und Validierungsergebnis |
| deterministische Reaktion auf ein Lebenszyklusereignis | Hook | Ereignisschema, Handler-Quelle, Exit-/Entscheidungsprotokoll |
| verteilbares Paket zusammengehöriger Erweiterungen | Plugin | Quelle, Version, deklarierte Komponenten und Installationsfreigabe |
| begrenzte delegierte Analyse oder Implementierung | Subagent | Werkzeuggrenze, Eingaberevision, Ausgabenachweise und Prüfergebnis |

Eine kurze Anweisung kann eine Richtlinie für destruktive Operationen nicht zuverlässig durchsetzen. Ein Hook kann keine Produktanforderung entscheiden, die menschliches Urteilsvermögen erfordert. Eine Subagenten-Beschreibung ist keine Berechtigung. Jede Kontrolle gehört in die Schicht, die sie tatsächlich nachweisen oder durchsetzen kann.

## Projektanweisungen sind eine Richtlinienebene {#project-instructions-are-a-policy-layer}

Repository-Vorgaben sollten knapp, aufgabenrelevant und überprüfbar sein. Sie sollten den üblichen Validierungsbefehl, wichtige Architekturgrenzen, geschützte Daten und Eskalationsregeln nennen. Sie sollten keinen Linter duplizieren und nicht so tun, als wäre eine natürlichsprachliche Anweisung eine Sandbox.

Claude Code dokumentiert sein Projektgedächtnis und das Laden von Anweisungsdateien getrennt von Plugins und Hooks. Prüfen Sie die aktuell wirksamen Anweisungsquellen im Zielclient, bevor Sie sich auf Rangfolge oder automatische Einbindung verlassen. [How Claude remembers your project](https://code.claude.com/docs/en/memory)

Eine brauchbare Anweisung beantwortet vier Fragen:

1. welches Repository oder welcher Pfad in den Geltungsbereich fällt;
2. was der Agent lesen, ändern oder ausführen darf;
3. welche Nachweise über Erfolg entscheiden;
4. wann er anhalten und einen Verantwortlichen fragen muss.

## Plugins sind Eingaben der Lieferkette {#plugins-are-supply-chain-inputs}

Ein Plugin kann Fähigkeiten bündeln, etwa Befehle, Agenten, Skills, Hooks und MCP-bezogene Konfiguration. Sein Paketaufbau und die unterstützten Felder entwickeln sich weiter. Verwenden Sie deshalb die aktuelle Plugin-Referenz und kopieren Sie kein altes Manifest aus einem Blog oder Repository. [Create plugins](https://code.claude.com/docs/en/plugins)

Vor Installation oder Aktualisierung festhalten:

- Herausgeber und unveränderliche Quellrevision;
- deklarierte Komponenten und deren Werkzeug- und Netzwerkverhalten;
- benötigte Geheimnisse, Datenpfade und externe Endpunkte;
- Kompatibilitätsnachweis für die Zielversion von Claude Code;
- Rollback- oder Deaktivierungsverfahren;
- Validierungsergebnis in einem Wegwerf- oder Nicht-Produktions-Arbeitsbereich.

Genehmigen Sie ein Plugin nicht allein deshalb, weil sein Befehlsname vertraut klingt. Ein mitgeliefcollter Hook oder eine MCP-Integration kann eine deutlich größere Vertrauensgrenze berühren als ein Markdown-Skill.

## Hooks brauchen einen deterministischen Vertrag {#hooks-need-a-deterministic-contract}

Aktuelle Hooks in Claude Code können auf Lebenszyklusereignisse über Command-, HTTP-, MCP-, Prompt- oder Agent-Handler reagieren. Die Hook-Referenz dokumentiert das Ereignisschema, das Matcher-Verhalten, Ein- und Ausgabeformate, Entscheidungssteuerungen und die unterstützten Konfigurationsorte. [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)

Deklarieren Sie für jeden Hook:

| Feld | Beispiel |
|---|---|
| Auslöser | ein benanntes Lebenszyklusereignis und ein eng gefasster Matcher |
| Eingabe | dokumentierte JSON-Felder, die der Handler verwendet |
| Nebenwirkung | rein lesende Validierung, Schreiben lokaler Artefakte oder Benachrichtigung |
| Entscheidung | keine Entscheidung, erlauben, verweigern oder aufschieben, soweit das aktuelle Ereignis dies unterstützt |
| Fehlerverhalten | Timeout oder Fehler ist sichtbar und kann eine geschützte Aktion nicht stillschweigend freigeben |
| Beleg | Handler-Version, Exit-Ergebnis und betroffene Revision |

Verwenden Sie Hooks für mechanische Regeln, die sich anhand deklarierter Eingaben auswerten lassen. Vermeiden Sie breite Shell-Hooks, die jeden Befehl prüfen, nicht deklarierte Umgebungsvariablen auslesen oder ohne explizite Allowlist und Timeout Netzwerkaufrufe ausführen. Ein erfolgreicher Exit ohne Ausgabe ist nicht gleichbedeutend mit einer Sicherheitsprüfung.

## Delegation mit Subagenten-Grenzen {#delegate-with-subagent-boundaries}

Ein Subagent ist nützlich, wenn Eingabe, Werkzeuge und erforderliche Nachweise begrenzt werden können. Subagenten-Definitionen in Claude Code können eine Rolle, deren Anweisungen und erlaubte Werkzeuge festlegen. Für Speicherort, Felder, Rangfolge und produktspezifische Einschränkungen konsultieren Sie die aktuelle Referenz. [Create custom subagents](https://code.claude.com/docs/en/subagents)

Verwenden Sie ein Aufgabenbriefing, das Folgendes benennt:

```yaml
goal: verify the changed authentication paths
input: immutable revision and declared files
tools: read, search, and named test command only
writes: none
output: findings with file, evidence, and severity
stop_when: evidence is missing or the task exceeds the declared scope
```

Der Hauptworkflow muss referenzierte Artefakte trotzdem prüfen und das Release-Gate ausführen. Die Textausgabe eines Subagenten ist eine Kandidatenbewertung, kein Ersatz für den zugrunde liegenden Test-, Quell- oder Deployment-Nachweis.

## Erweiterungen sicher ausrollen {#roll-out-extensions-safely}

1. Quelle und Verantwortlichkeit der Erweiterung prüfen;
2. sie in einem Wegwerf-Repository oder einem isolierten Worktree testen;
3. die effektive Konfiguration und die erlaubten Werkzeuge festhalten;
4. eine Aufgabe mit bewusst kleinem Geltungsbereich ausführen;
5. erzeugte Artefakte und alle externen Wirkungen verifizieren;
6. erst befördern, wenn ein Prüfer das Ergebnis reproduzieren kann;
7. für Hooks, Plugins und Richtlinienänderungen einen Deaktivierungspfad vorhalten.

Behandeln Sie eine Schemaabweichung, eine nicht verfügbare Komponente oder einen fehlenden Beleg als sichtbaren Fehler. Ersetzen Sie nicht stillschweigend ein Plugin, einen Befehl, einen Provider oder einen Berechtigungsmodus durch eine andere Variante.

## Häufige Fehlermuster {#common-failure-modes}

- **Versionsfolklore:** statische Ereigniszahlen, CLI-Flags oder Manifestfelder aus einer alten Version übernommen.
- **Richtlinie nur als Prosa:** eine kritische Sicherheitsregel existiert nur in einer langen Anweisungsdatei.
- **Unbegrenzter Hook:** ein Befehls-Handler erhält Zugriff auf Daten oder Netzwerkziele, die mit seinem Auslöser nichts zu tun haben.
- **Vertrauen auf den Plugin-Namen:** Installation ohne Prüfung von Quelle, Komponenten oder Berechtigungen.
- **Delegation ohne Nachweis:** ein Subagent behauptet, eine Änderung funktioniere, doch es existiert kein Test- oder Zielbeleg.
- **Verdeckter Fallback:** eine nicht verfügbare Erweiterung führt dazu, dass ohne Sichtbarkeit für den Operator eine andere Fähigkeit läuft.

## Referenzen {#references}

- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Create custom subagents](https://code.claude.com/docs/en/subagents)
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
