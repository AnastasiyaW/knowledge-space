---
title: "Persona-Policy-Design für LLM-Systeme"
description: "Gestalten Sie eine LLM-Persona als versionierte Verhaltensrichtlinie mit explizit definierten Grenzen für Autorität, Datenschutz, Eskalation und Evaluation, statt als angenommene Modellpersönlichkeit."
tags: [llm-agents, persona, policy, safety, evaluation, privacy]
level: 3
source_sha256: 1b586484cead5814f647a72196f160fab2676062abbe7bc970833ffab51e71ef
translation: machine
translated_at: '2026-10-24'
---
# Persona-Policy-Design für LLM-Systeme {#persona-policy-design-for-llm-systems}

**Stand der Prüfung: 2026-09-04.** Eine Persona ist dann nützlich, wenn sie das Verhalten eines Agenten für eine definierte Zielgruppe und Aufgabe vorhersehbarer macht. Sie ist weder ein Persönlichkeitstest noch eine Aussage über den inneren Zustand des Modells, und sie ersetzt keine Sicherheitsmaßnahmen, Zugriffskontrolle und Verifikation.

## Verhalten definieren, nicht Adjektive {#define-behavior-not-adjectives}

Begriffe wie „freundlich“, „streng“ oder „kreativ“ sind zu vage, um eine konkrete Entscheidung zu steuern. Übersetzen Sie jede gewünschte Eigenschaft in beobachtbares Verhalten, eine Ausnahmeregel und einen Eskalationspfad.

| Absicht | Operative Richtlinie |
|---|---|
| unterstützendes Lehren | den Lösungsversuch einer lernenden Person anerkennen; den konkreten Fehler benennen; die nächste passende Übung anbieten |
| prägnante Fachunterstützung | mit Entscheidung und Belegen beginnen; nicht angeforderten Hintergrund weglassen; Unsicherheit offenlegen |
| sichere Unterstützung im Gesundheits- oder Rechtsbereich | nur allgemeine Informationen geben; keine individuellen Schlussfolgerungen ziehen; die Person an eine geeignete Fachperson verweisen |
| datenschutzorientierter Assistent | nur deklarierte Felder erheben; Zweck und Aufbewahrung erklären; Löschung und Änderungen der Einwilligung respektieren |

Stimme, Tonfall und Register beeinflussen die Darstellung. Sie dürfen weder sachliche Richtigkeit, Vertraulichkeit, eine Anweisung mit höherer Priorität noch eine Freigabegrenze außer Kraft setzen.

## Persona-Vertrag {#persona-contract}

Speichern Sie die wirksame Persona als kleine, versionierte Richtlinie. Das Beispiel ist bewusst produktneutral.

```yaml
persona_id: learning-coach
version: 2026-09-04
purpose: guide practice without inventing learner progress
audience: opted-in adult learners
voice: direct, respectful, plain language
allowed:
  - explain supplied learning material
  - ask a clarifying question when the task is ambiguous
prohibited:
  - infer sensitive traits from conversation
  - promise outcomes or credentials
  - bypass a teacher or owner approval
memory:
  allowed_fields: [declared_goal, opted_in_preference]
  retention: documented service policy
escalate_when:
  - safety risk
  - conflicting instructions
  - requested action exceeds declared authority
```

Ein Richtlinienvertrag ermöglicht es Engineering, Redaktion und Datenschutzverantwortlichen, ein konkretes Artefakt zu prüfen. Er macht Änderungen außerdem umkehrbar: Stellen Sie eine neue Version bewusst bereit, bewahren Sie die vorherige Version und die Evaluationsergebnisse auf, und widerrufen Sie die Richtlinie, sobald ihr Zweck nicht mehr gilt.

## Nutzerinhalte als Daten behandeln, nicht als Autorität {#treat-user-content-as-data-not-authority}

Eine Persona sollte die Autoritätsreihenfolge des Systems auch dann einhalten, wenn sie auf Anweisungen in Nachrichten, Dateien, Tool-Ausgaben, Webseiten, Tickets oder abgerufenem Speicher stößt. Nicht vertrauenswürdige Inhalte können einen Stilwechsel verlangen, aber sie können keinen Zugriff autorisieren, keine Aufbewahrungsregel ändern und den Agenten nicht dazu bringen, die Validierung zu ignorieren.

Machen Sie bei toolnutzenden Systemen die Grenze explizit: Die Persona darf eine Erklärung prägen, während Tool-Berechtigungen und Freigaben festlegen, was das System tun darf. Dadurch sinkt das Risiko, dass ein überzeugender „Charakter“ eine unsichere Aktion verdeckt.

## Zustand, Einwilligung und Widerruf {#state-consent-and-revocation}

Wenn sich eine Persona an eine Person anpasst, dokumentieren Sie den Lebenszyklus jedes Zustandsfeldes:

1. Benennen Sie Feld, Zweck, Quelle und verantwortliche Stelle;
2. holen Sie die Einwilligung oder die sonstige rechtliche Grundlage ein, die für diese Nutzung erforderlich ist;
3. beschränken Sie den Abruf auf die Aufgabe, die das Feld benötigt;
4. stellen Sie Wege für Korrektur, Löschung und Widerruf bereit;
5. testen Sie das System nach Änderungen der Einwilligung, nicht nur beim erstmaligen Onboarding.

Machen Sie aus einer Stilpräferenz durch Schlussfolgerung kein sensibles Profil. Wenn ein Dienst aus Gesprächen abgeleitete Daten speichert, gehören Aufbewahrungs- und Löschverhalten in die dokumentierte Datenrichtlinie des Produkts – nicht in einen informellen Prompt.

## Die Richtlinie in Szenarien evaluieren {#evaluate-the-policy-in-scenarios}

Evaluieren Sie eine Persona mit Szenario-Fixtures, nicht anhand eines vagen Eindrucks, sie wirke „in der Rolle“.

| Szenario | Was zu prüfen ist |
|---|---|
| Routineaufgabe | die Stimme ist klar, und die Antwort erledigt die erlaubte Aufgabe |
| mehrdeutige Anfrage | der Agent fragt nach oder eskaliert, statt eine Annahme zu erfinden |
| widersprüchliche Anweisung | die Richtlinie mit höherer Priorität bleibt in Kraft |
| Anfrage nach sensiblen Daten | der Agent minimiert die Offenlegung und hält die Einwilligungsgrenzen ein |
| Tool- oder externe Aktion | die Persona erteilt sich selbst keine Berechtigung |
| Richtlinienaktualisierung | das beabsichtigte Verhalten ändert sich, während nicht zusammenhängendes Sicherheitsverhalten stabil bleibt |

Verwenden Sie deterministische Prüfungen für bekannte verbotene Formulierungen, Tool-Aufrufe und Schema-Felder. Ergänzen Sie unabhängige menschliche Prüfungen für Qualitäts-, Fairness- oder Sicherheitsurteile, die sich nicht auf einen binären Validator reduzieren lassen. Protokollieren Sie Persona-Version, Fixture-Revision, Modell-/Tool-Konfiguration und Ergebnis.

## Persona-Änderungen klein und prüfbar halten {#keep-persona-changes-small-and-reviewable}

Eine Persona-Richtlinie wird fragil, wenn sie eine Biografie, mehrere widersprüchliche Zielgruppen und nicht testbare Tonregeln ansammelt. Bevorzugen Sie pro Produktoberfläche eine klar abgegrenzte Richtlinie. Benötigt dasselbe System eine andere Rolle – etwa Tutor, Redakteur oder Support-Triage –, machen Sie den Wechsel explizit und protokollieren Sie, welche Richtlinie aktiv ist.

Vermeiden Sie es, dieselbe Regel an vielen Stellen umzuformulieren. Eine maßgebliche Richtlinie mit sichtbarer Vorrangreihenfolge lässt sich leichter testen als verstreute Prompt-Fragmente.

## Typische Fehlerbilder {#common-failure-modes}

- **Adjektivstapel:** Das System kann nicht erkennen, was eine Eigenschaft in einer konkreten Entscheidung verändert.
- **Persona überstimmt Sicherheit:** Eine warme oder bestimmte Stimme wird fälschlich als Autorität behandelt.
- **Implizites Profiling:** Abgeleitete Merkmale werden ohne Einwilligung oder deklarierten Zweck gespeichert.
- **Unversionierte Änderungen:** Das Verhalten ändert sich, aber kein Prüfer kann die aktive Richtlinie identifizieren.
- **Nur Stiltests:** Antworten klingen richtig, während Tool-, Datenschutz- oder Eskalationsverhalten falsch ist.
- **Dauerhafter Speicher als Standard:** Nutzerpräferenzen überdauern ihren dokumentierten Zweck.

## Referenzen {#references}

- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — Risikomanagement-Kontext für generative KI-Systeme.
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) — Prompt-Injection, Missbrauch von Tools und Risiken an Datengrenzen.
- [[persona-adaptive-llm]] — ein verwandter Gestaltungsleitfaden zu Profilfeldern, Abrufspeicher, Einwilligung und Löschgrenzen.
