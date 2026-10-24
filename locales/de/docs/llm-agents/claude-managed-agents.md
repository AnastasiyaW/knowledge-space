---
title: "Organisationsverwaltete Claude-Code-Subagenten"
description: "Organisationsverwaltete Claude-Code-Subagenten mit explizitem Geltungsbereich, Rangfolge, Werkzeugbeschränkungen und Verifikation definieren, statt verwaltete Konfiguration als Cloud-Ausführungslaufzeit zu behandeln."
tags: [claude-code, subagents, managed-settings, governance, permissions]
level: 3
source_sha256: 521fa292162fc623c0ec94a1fc851ad30fb9a83f1f864aa73f7553905beae593
translation: machine
translated_at: '2026-10-24'
---
# Organisationsverwaltete Claude-Code-Subagenten {#organization-managed-claude-code-subagents}

**Stand der Prüfung: 2026-09-04.** Nach der aktuellen Claude-Code-Dokumentation ist ein verwalteter Subagent eine von der Organisation bereitgestellte Subagent-Definition, die über verwaltete Einstellungen verteilt wird. Er ist keine gehostete „Brain/Hands/Session“-Laufzeit, kein anbieterseitig abgerechnetes Sandbox-Produkt und keine Garantie für persistente Cloud-Ausführung. Verwaltete Definitionen verwenden dasselbe Markdown- und YAML-Frontmatter-Format wie benutzer- und projektbezogene Subagenten und haben Vorrang, wenn eine gleichnamige Definition auf einer niedrigeren Ebene existiert. [Claude Code subagents](https://code.claude.com/docs/en/subagents)

## Geltungsbereiche und Rangfolge {#definition-scopes-and-precedence}

| Geltungsbereich | Vorgesehene Verwendung | Eigentümer |
|---|---|---|
| user | persönliche, wiederverwendbare Workflows | einzelne Entwicklerin bzw. einzelner Entwickler |
| project | repositoryspezifische, gemeinsam genutzte Workflows | Repository-Team |
| managed | Organisationsrichtlinien und zentral gepflegte Agenten | Organisationsadministration |
| plugin | verteilbares Paket von Drittanbietern oder intern | Plugin-Herausgeber |

Wählen Sie den engsten Geltungsbereich, der den erforderlichen Eigentümer hat. Eine verwaltete Definition kann eine Projekt- oder Benutzerdefinition mit demselben Namen überschreiben. Namen sind daher als Teil der Organisationsrichtlinie zu behandeln. [Subagent configuration](https://code.claude.com/docs/en/configuration)

## Einen begrenzten Agenten definieren {#define-a-bounded-agent}

Eine Agentendefinition besteht aus Frontmatter, gefolgt von den Markdown-Anweisungen des Agenten. Das folgende Beispiel ist bewusst nur lesend angelegt. Passen Sie die genauen Felder und die zulässigen Werkzeuge vor dem Rollout an die aktuelle Claude-Code-Referenz an.

```markdown
---
name: policy-reviewer
description: "Read-only review of dependency and repository policy changes."
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---

Inspect the requested revision. Return findings with file references,
severity, evidence, and the smallest corrective action. Do not modify files.
```

Formulieren Sie die Beschreibung so präzise, dass die automatische Delegation vorhersehbar bleibt. Der Textkörper sollte festlegen, welche Nachweise relevant sind, welche Werkzeuge erlaubt sind, wann die Arbeit endet und welche Antwortstruktur erforderlich ist. Ein Rollentitel allein ist keine Sicherheitsgrenze. [Create custom subagents](https://code.claude.com/docs/en/subagents)

## Konfiguration und Ausführung trennen {#separate-configuration-from-execution}

Verwaltete Einstellungen können eine Definition verteilen, sie belegen aber nicht, dass eine Aufgabe in einem bestimmten Container, einer bestimmten Region, einem bestimmten Konto oder unter einem bestimmten Aufbewahrungsmodell ausgeführt wurde. Diese Fakten müssen auf der Ausführungsebene festgehalten werden:

1. Client-Version, wirksame Einstellungsquelle und Workspace-Revision protokollieren;
2. Werkzeuge und Berechtigungen einschränken, bevor die Aufgabe beginnt;
3. dem Agenten nur die minimal nötigen Daten und den minimal nötigen Repository-Umfang geben;
4. Belege für externe Seiteneffekte und Idempotenzschlüssel außerhalb des Chats speichern;
5. die deterministische Validierung der Aufgabe ausführen;
6. bei wesentlichen Änderungen eine unabhängige Prüfung verlangen.

Hängen Sie keine festen Latenz-, Kosten-, Sitzungspersistenz- oder Datenresidenzwerte an ein Konfigurationsmerkmal, solange der Anbieter keinen aktuellen Vertrag für genau diese Laufzeit veröffentlicht.

## Grenzen von Plugins {#plugin-boundaries}

Plugins können spezialisierte Agenten, Skills, Hooks, MCP-Server und verwandte Komponenten mitbringen. Claude Code dokumentiert eine wichtige Einschränkung: Von Plugins bereitgestellte Subagenten unterstützen keine Frontmatter-Felder für Hooks, MCP-Server oder Berechtigungsmodi; diese Felder werden ignoriert. Wenn ein Workflow solche Steuerungen benötigt, verwenden Sie die passende Ebene der Benutzer-, Projekt- oder verwalteten Einstellungen und prüfen Sie die wirksame Richtlinie. [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

Damit wird verhindert, dass eine Agentendeklaration in einem Plugin unbemerkt zu einer allgemeinen Vertrauensgrenze wird. Ein Plugin kann die Arbeit dennoch über seine Anweisungen und deklarierten Komponenten beeinflussen. Behandeln Sie Installation und Aktualisierung deshalb als Entscheidung zur Lieferkettensicherheit.

## Betriebsmuster {#operational-pattern}

Verwenden Sie für jeden zentral verwalteten Agenten einen klaren Vertrag:

| Vertragsfeld | Beispiel |
|---|---|
| Auslöser | eine Prüfung der Repository-Richtlinie wird angefordert |
| Eingabegrenze | ausgecheckte Revision und deklarierte Pfade ausschließlich |
| Werkzeuggrenze | Lese-, Such- und Testbefehle, keine Schreibzugriffe |
| Ausgabe | strukturierte Befunde mit Quell- bzw. Testbeleg |
| Eskalation | unklare Autorisierung oder Produktionsziel |
| Fehlersignal | fehlgeschlagene Prüfung, fehlende Belege oder expliziter Blockierungszustand |
| Eigentümer | Organisationsteam, das die Definition pflegt |

Protokollieren Sie, welche wirksame Definition ausgeführt wurde. Eine Änderung an einer verwalteten Richtlinie kann das Verhalten eines Agenten verändern, ohne dass sich das Repository ändert. Ein Freigabebeleg benötigt daher sowohl die Projektrevision als auch die Version oder Kennung der anwendbaren verwalteten Konfiguration.

## Rollout und Änderungskontrolle {#rollout-and-change-control}

1. Die Agentendefinition wie produktive Konfiguration prüfen;
2. sie in einem Wegwerf- oder isolierten Worktree testen;
3. bestätigen, dass Duplikate auf niedrigeren Ebenen die beabsichtigte Definition nicht verdecken;
4. repräsentative erlaubte und verbotene Werkzeugaufrufe ausführen;
5. den erwarteten Befund- bzw. Ausgabevertrag veröffentlichen;
6. eine Rollback-Version und ein datiertes Bereitstellungsprotokoll aufbewahren.

Bei einem Sicherheits- oder Compliance-Agenten darf derselbe Agent nicht zugleich eine Änderung verfassen und sie freigeben. Verwenden Sie einen separat berechtigten Prüfer oder ein deterministisches Gate.

## Fallstricke {#gotchas}

- **Ein Projektagent und ein verwalteter Agent tragen denselben Namen.** Das wirksame Verhalten kann von der verwalteten Definition bestimmt werden. **Abhilfe:** eindeutige Namen verwenden und die aktive Quelle vor der Freigabe prüfen.
- **Ein Plugin-Agent deklariert Berechtigungen im Frontmatter.** Diese Felder werden bei von Plugins bereitgestellten Agenten ignoriert. **Abhilfe:** erforderliche Steuerungen in eine unterstützte Einstellungsebene verlagern und dort prüfen.
- **Ein Agent kann ein Geheimnis lesen, wird aber angewiesen, es nicht preiszugeben.** Reine Textanweisungen sind keine Fähigkeitsgrenze. **Abhilfe:** keinen unnötigen Zugriff auf Geheimnisse gewähren.
- **Eine Prüfausgabe lautet PASS ohne Beleg.** Ein Ergebnis ist kein Freigabebeleg. **Abhilfe:** Befehlsergebnisse, Quellverweise oder beobachtete Artefakte verlangen.
- **Ein Update der Organisation ändert das Verhalten stillschweigend.** Reproduzierbarkeit wird schwierig. **Abhilfe:** die Identität der verwalteten Konfiguration im Aufgabenbeleg protokollieren.

## Quellen {#sources}

- [Claude Code subagents](https://code.claude.com/docs/en/subagents)
- [Claude Code settings and subagent configuration](https://code.claude.com/docs/en/configuration)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code extension overview](https://code.claude.com/docs/en/features-overview)

## Siehe auch {#see-also}

- [[claude-code-harness-patterns]]
- [[agent-orchestration]]
- [[agentic-security-2026]]
- [[multi-session-coordination]]
