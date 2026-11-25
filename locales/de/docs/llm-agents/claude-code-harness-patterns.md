---
title: "Muster für Coding-Agent-Harnesses"
description: "Eine praxisnahe Abgrenzung zwischen Anweisungen, Werkzeugen, deterministischen Kontrollpunkten, Review und dauerhaften Nachweisen für die Arbeit von Coding-Agents."
tags: [coding-agents, harness, hooks, skills, testing, verification]
level: 4
source_sha256: 3b35b2430962d068196f086c208501b2594cf3bb077e895259cb7646a5cbeb7d
translation: machine
translated_at: '2026-10-24'
---
# Muster für Coding-Agent-Harnesses {#coding-agent-harness-patterns}

**Stand der Prüfung: 2026-09-03.** Ein Harness ist die Betriebsumgebung rund um einen Coding-Agent. Seine Aufgabe besteht nicht darin, einen Agent diszipliniert klingen zu lassen; er macht den beabsichtigten Arbeitsablauf überprüfbar und erlaubt deterministischen Prüfungen, eine ungültige Änderung abzulehnen.

Dieser Leitfaden verzichtet auf behauptete allgemeingültige Beschleunigungen, Produktrankings und fest verdrahtete Empfehlungen für Werkzeuge von Drittanbietern. Messen Sie ein Harness im eigenen Repository gegen ein festgelegtes Lieferkriterium.

## Fünf Grenzen {#five-boundaries}

| Grenze | Verantwortet | Darf nicht verantworten |
|---|---|---|
| Aufgabenvertrag | Abnahmekriterien, Umfang, Befugnisse | verborgene Implementierungsentscheidungen |
| Anweisungen | Projektkonventionen und Routing | Ersatz für ausführbare Richtlinien |
| Werkzeuge und Skills | wiederholbare fachliche Arbeitsabläufe | die endgültige Freigabe der eigenen Ausgabe |
| deterministische Kontrollpunkte | Build, Tests, Schema, Formatierung, Linkprüfungen | Urteile über nicht genannte Produktabsichten |
| unabhängiges Review | semantisches und Release-Risiko | eine unbegrenzte Neufassung einer abgeschlossenen Aufgabe |

Ist eine Schicht vom Agent weder prüfbar, aufrufbar noch verifizierbar, ist sie keine operative Kontrolle.

## Mit einem Liefervertrag beginnen {#start-with-a-delivery-contract}

Formulieren Sie die Abnahmekriterien vor der Bearbeitung:

1. Benennen Sie die betroffenen Pfade oder das extern beobachtbare Verhalten im Umfang;
2. nennen Sie den genauen Verifikationsbefehl oder einen beobachtbaren Nachweis;
3. listen Sie irreversible oder freigabepflichtige Aktionen auf;
4. bestimmen Sie den Eigentümer jeder veränderlichen Ressource;
5. benennen Sie den erforderlichen Reviewer, wenn Selbstprüfung nicht ausreicht.

Halten Sie den Aufgabenstatus in einem dauerhaften Artefakt fest, nicht nur im Chatverlauf. Ein knappes Manifest kann `PENDING`, `RUNNING`, `PASS` und `BLOCKED` sowie den Nachweis verfolgen, der einen Endzustand begründet.

## Anweisungen sind bereichsbezogene Konfiguration {#instructions-are-scoped-configuration}

Das aktuelle Claude Code unterscheidet gemeinsame Projekteinstellungen, projektlokale Einstellungen, Benutzereinstellungen und verwaltete Richtlinien. Legen Sie team-taugliche, versionierte Konfiguration im gemeinsamen Projektbereich ab; halten Sie persönliche Überschreibungen und Zugangsdaten aus dem Repository heraus. `/status` zeigt die Quellen, die die aktive Sitzung geladen hat. [Claude Code settings](https://code.claude.com/docs/en/settings)

Projektanweisungen sollten nur Fragen beantworten, die sich nicht günstig aus dem Code ableiten lassen:

- wo die maßgebliche Architektur- und Deployment-Dokumentation liegt;
- wie die erforderlichen Prüfungen ausgeführt werden;
- geschützte Dateien, Grenzen für Geheimnisse und Freigaberegeln;
- die erwarteten Übergabe- und Review-Artefakte.

Machen Sie aus einer Anweisungsdatei weder ein Änderungsprotokoll noch eine Prompt-Sammlung. Verweisen Sie für ausführliches Wissen auf dauerhafte Dokumente.

## Deterministische Kontrollen kommen vor dem Urteil des Modells {#deterministic-controls-come-before-model-judgment}

Führen Sie günstige mechanische Prüfungen direkt aus:

| Änderungsrisiko | Beispielkontrolle | Nachweis |
|---|---|---|
| Syntax oder Format | Formatierer, Parser, Typprüfer | Prozess-Exitcode und Bericht |
| geänderter Vertrag | gezielter Test oder Schema-Validierung | Assertion-Ausgabe |
| Dokumentation | Link- und Frontmatter-Prüfungen | Lint-Nachweis |
| Release-Artefakt | Build- oder Paketverifikation | Referenz auf unveränderliches Artefakt |
| riskantes Verhalten | Integrations- oder nutzersichtbarer Test | Trace, Screenshot oder Dienstnachweis |

Ein LLM kann einen fehlgeschlagenen Bericht interpretieren und eine Korrektur vorschlagen. Es darf eine fehlgeschlagene Prüfung nicht allein durch eine Erklärung in ein Bestanden verwandeln.

## Hooks und Skills haben unterschiedliche Rollen {#hooks-and-skills-have-different-roles}

Claude Code unterstützt Hooks rund um Lebenszyklus- und Werkzeugereignisse, und benutzerdefinierte Subagents können fokussierten Kontext und Werkzeugberechtigungen mitführen. Dabei handelt es sich um Integrationspunkte, nicht um einen Beweis, dass ein Arbeitsablauf eingehalten wurde. [Hooks reference](https://code.claude.com/docs/en/hooks) [Custom subagents](https://code.claude.com/docs/en/sub-agents)

| Mechanismus | Gute Verwendung | Erforderliche Absicherung |
|---|---|---|
| Skill | fachliche Vorgehensweise oder wiederverwendbare Checkliste | Auslösebedingungen und eine ausführbare Verifikation |
| Hook | Ereignis protokollieren oder eine verbotene Aktion blockieren | stabile Ein- und Ausgabe sowie Fail-Closed-Verhalten bei der Freigabe |
| Subagent | begrenzte Erkundung oder unabhängiges Review | Dateizuständigkeit, keine Selbstbestätigung, klares Rückgabeformat |
| Skript | deterministische Inventarisierung oder Validierung | versionierte Quelle, Exitstatus, aufbewahrter Bericht |

Machen Sie ein nicht vertrauenswürdiges Werkzeugergebnis nicht zu ausführbarer Autorität. Parsen, validieren und leiten Sie es über dieselbe Freigabegrenze wie jede andere Eingabe.

## Eine minimale Änderungsschleife {#a-minimal-change-loop}

```text
freeze acceptance criteria
        ↓
inspect code and relevant documentation
        ↓
make the smallest coherent change
        ↓
run the named deterministic checks
        ↓
collect receipts and inspect the diff
        ↓
independent review for material risk
        ↓
publish only after every required gate passes
```

Die Schleife wird nützlich, wenn jeder Pfeil ein dauerhaftes Artefakt hat. Eine Statusmeldung ohne Testausgabe, Diff oder Laufzeitnachweis ist kein Beleg.

## Isolation von Worktree und Reviewer {#worktree-and-reviewer-isolation}

Verwenden Sie einen separaten Git-Worktree, wenn parallele Arbeit sonst einen veränderlichen Checkout teilen würde. Git beschreibt verknüpfte Worktrees als separate Arbeitsverzeichnisse, die an ein Repository angebunden sind und es erlauben, mehr als einen Branch gleichzeitig auszuchecken. [git-worktree](https://git-scm.com/docs/git-worktree)

Bei einer wesentlichen öffentlichen Änderung sollte der Reviewer den endgültigen Diff unabhängig lesen und entweder `PASS` oder einen konkreten Befund mit Datei, Zeile, Auswirkung und minimaler Korrektur zurückgeben. Der Autor wendet die Korrekturen an; der Reviewer bestätigt eine geänderte Implementierung nicht stillschweigend aus dem Gedächtnis.

## Lokal messen, nicht nach Marketingaussagen {#measure-locally-not-by-marketing}

Wenn ein Team Harness-Varianten vergleichen will, legen Sie fest:

- ein festes Aufgabenkorpus und feste Repository-Revisionen;
- dasselbe Modell, dieselben Berechtigungen und dieselbe Werkzeugverfügbarkeit;
- eine primäre Qualitätsmetrik, etwa akzeptierte Tests oder Reviewer-Befunde;
- die Erfassung von Kosten und verstrichener Zeit;
- eine Regel, wann ein Experiment beibehalten, zurückgerollt oder wiederholt wird.

Ohne diese Gestaltung ist ein berichteter Prozentwert eine Anekdote und kein technisches Ergebnis.

## Fallstricke {#gotchas}

- **Ein Skill fordert eine Prüfung, aber es gibt kein Skript.** Die Regel ist nicht durchsetzbar. **Abhilfe:** Ergänzen oder referenzieren Sie die kleinste ausführbare Prüfung, bevor Sie sie als Kontrollpunkt behandeln.
- **Ein Hook hat weitreichende Schreibrechte.** Er kann zu einem verborgenen Deployment-Pfad werden. **Abhilfe:** Halten Sie Hooks eng gefasst, protokolliert und ohne Möglichkeit, die normale Freigabe zu umgehen.
- **Derselbe Agent schreibt und genehmigt eine riskante Änderung.** Er hat in beiden Rollen dieselben blinden Flecken. **Abhilfe:** Verlangen Sie einen frischen Reviewer oder eine deterministische externe Prüfung.
- **Eine Testsuite läuft durch, nachdem sich die Aufgabe verändert hat.** Sie prüft unter Umständen nicht das angeforderte Verhalten. **Abhilfe:** Ordnen Sie jedes Abnahmekriterium einem eigenen Nachweis zu.
- **Parallele Agents teilen sich einen Checkout.** Dateikonflikte zerstören die Absicht. **Abhilfe:** Verwenden Sie Worktrees oder explizite Zuständigkeitsgrenzen, bevor Sie bearbeiten.

## Quellen {#sources}

- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Git worktrees](https://git-scm.com/docs/git-worktree)

## Siehe auch {#see-also}

- [[agent-design-patterns]]
- [[agent-orchestration]]
- [[multi-session-coordination]]
- [[handoff-rollup-pattern]]
- [[production-patterns]]
