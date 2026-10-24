---
title: "Sicherheit und Ausrichtung von Agenten"
description: "Agentensicherheit als explizite Grenzen für Berechtigungen, Daten, Werkzeuge, Freigaben und Nachweise aufbauen statt als reines Versprechen im Prompt."
tags: [llm-agents, safety, alignment, guardrails, prompt-injection, sandboxing, approvals]
level: 5
source_sha256: c399383899c40f672c7e15c143344a9e5d3d43e5f27e9ebd55928224a707ca3c
translation: machine
translated_at: '2026-10-24'
---
# Sicherheit und Ausrichtung von Agenten (September 2026) {#agent-safety-and-alignment-september-2026}

Versionskontext: Modellverhalten, Werkzeugprotokolle, Sandbox-Produkte, Moderationsfunktionen und Richtlinienkontrollen der Anbieter ändern sich. Diese Seite beschreibt eine produktbezogene Sicherheitsarchitektur, die gegen das genaue Modell, die Werkzeuge, die Datenklassen und die Bereitstellungsumgebung bewertet werden muss.

Ein Agent kann zusammenfassen, planen, Werkzeuge aufrufen, Dateien schreiben oder externe Effekte anfordern. Formulierungen zur Ausrichtung im System-Prompt können das Verhalten lenken, sie erzeugen aber keine Autorisierung, isolieren keine Daten, validieren keine Zahlung und belegen nicht das Ergebnis einer Aktion. Sicherheit entsteht durch geschichtete technische und operative Kontrollen.

## Mit einem Bedrohungsmodell beginnen {#start-with-a-threat-model}

Lege fest, was vertrauenswürdig und was nicht vertrauenswürdig ist und welche Effekte eine eigene Autorisierungsentscheidung erfordern.

| Grenze | Beispiele | Erforderliche Kontrolle |
|---|---|---|
| Vertrauenswürdige Richtlinie | Anwendungskonfiguration, freigegebene Schemata, signierte Regeln | Versionierung, Zugriffskontrolle, Änderungsprüfung |
| Nicht vertrauenswürdige Inhalte | Benutzereingaben, Webseiten, E-Mails, abgerufene Dokumente, Werkzeugausgaben | als Daten behandeln; niemals als Autorität |
| Modellausgabe | vorgeschlagene Antwort, Werkzeugargumente, Routing-Entscheidung | Schema, fachliche Validierung, Autorisierung |
| Zugangsdaten und Identität | Dienstkonto, Mandantenscope, Benutzersitzung | minimale Berechtigungen, Ablauf, Audit |
| Externer Effekt | Senden, Veröffentlichen, Deployen, Kaufen, Löschen | Freigabe, Idempotenz, endgültige Quittung |

Ein Bedrohungsmodell sollte Assets, Akteure, Eintrittspunkte, Auswirkungen eines Fehlers, den Verantwortlichen für die Kontrolle und den Nachweis benennen, der belegt, dass die Kontrolle funktioniert.

## Prompt Injection ist ein Problem der Datengrenze {#prompt-injection-is-a-data-boundary-problem}

Anweisungen, die in einem Dokument, einer Webseite, einem Werkzeugergebnis oder einer Benutzernachricht eingebettet sind, gelten als nicht vertrauenswürdige Inhalte. Das bloße Entfernen von Textmustern macht sie nicht sicher: Angreifer können Anweisungen umformulieren, kodieren oder über einen Werkzeugablauf statt über eine bestimmte Formulierung ausnutzen.

Baue einen sichereren Pfad auf:

1. Vertrauenswürdige Anweisungen und nicht vertrauenswürdige Eingaben explizit kennzeichnen;
2. nur die minimal nötigen Daten für die Aufgabe übergeben;
3. das Modell auf einen engen, lokal freigegebenen Werkzeugsatz beschränken;
4. jeden vorgeschlagenen Werkzeugaufruf außerhalb des Modells validieren;
5. Autorisierung, Mandantenscope und externe Effekte im deterministischen Code belassen;
6. adversariale Inhalte in der tatsächlichen Abruf- und Werkzeugpipeline testen.

Die aktuellen Sicherheitsempfehlungen von OpenAI raten dazu, Ein- und Ausgaben einzuschränken und gegebenenfalls menschliche Prüfung einzusetzen. Dies sind Maßnahmen zur Risikominderung, keine Garantie, dass beliebige Inhalte sicher sind. [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)

## Fähigkeiten gewähren, nicht breite Absichten {#grant-capabilities-not-broad-intent}

Verwende für eine Aktion eine kurzlebige, unveränderliche Fähigkeit oder einen Freigabeverweis. Speichere sie serverseitig oder signiere sie; der Ausführende darf ihre Felder nicht ändern können:

```json
{
  "capability_id": "cap_01...",
  "capability_profile": "effect-capability/v1",
  "issuer": "policy-service",
  "issuer_key_id": "policy-service-key-2026-01",
  "subject": "workflow:research-review",
  "audience": "editorial-effect-service",
  "presenter_principal": "workload:research-reviewer@prod",
  "presenter_key_thumbprint": "sha256:...",
  "identity_source": "approved-workload-identity",
  "task_id": "publish-research-044",
  "action": "create_draft",
  "arguments_digest": "sha256:...",
  "resource_scope": "project:happyin-space",
  "data_classification": "public",
  "approval_decision_ref": "approval:appr_01...",
  "idempotency_key": "publish-research-044:v1",
  "expires_at": "2026-09-03T16:00:00Z",
  "policy_revision": "editorial-policy@6",
  "integrity_proof": "server-record-or-signature"
}
```

Der Agent darf eine Aktion anfordern, aber der Durchsetzungspunkt löst den unveränderlichen Datensatz auf bzw. verifiziert ihn und prüft vor der Ausführung Profil, Aussteller, an den Aussteller gebundenen Schlüssel, Subjekt, Aufgabe, Digest der Aktionsargumente, Scope, Ablauf, Freigabeentscheidung und Idempotenzschlüssel. Ein Serverdatensatz muss aus einem autorisierten Speicher stammen; eine signierte Fähigkeit muss gegen einen allowlisteten Aussteller und dessen konfigurierten Schlüssel verifiziert werden. Unbekannte Aussteller, falsche Profile und ungültige Signaturen schlagen geschlossen fehl (fail closed).

Der Effektdienst ist die Grenze für Empfänger und Beendigung der Identität. Er akzeptiert eine Präsenter-Identität nur von seinem konfigurierten Workload-Identity-Verifizierer, niemals aus einem weitergeleiteten Caller-Header. Er verlangt, dass der live authentifizierte Principal gleich `presenter_principal` ist, und den Nachweis des Besitzes des Credentials, das zu `presenter_key_thumbprint` passt; zusätzlich verlangt er, dass `audience` genau diesem lokalen Dienst entspricht. Fehlende oder ungleiche Werte lehnen die Aktion ab, sodass eine kopierte Fähigkeit nicht von einem anderen Principal wiederverwendet werden kann. Zertifikats- und schlüsselgebundene Token-Muster liefern Beispiele für diese Bindung und die Validierung des Empfängers. [RFC 8705](https://www.rfc-editor.org/rfc/rfc8705) [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725)

Jede geänderte Argument- oder Scope-Angabe erfordert eine neu ausgestellte Fähigkeit. Ein Agent kann seinen Scope nicht selbst erweitern, indem er behauptet, eine dringende Aufgabe brauche mehr Zugriff.

## Irreversible Effekte hinter ein Gate legen {#put-irreversible-effects-behind-a-gate}

Verwende einen Ablauf von Vorschlag zu Effekt:

```text
propose -> parse and validate -> authorize -> approve if required
       -> atomically reserve effect key -> execute -> reconcile -> terminal receipt
```

Die endgültige Quittung muss angeben, ob der externe Effekt eingetreten ist, nicht nur, dass das Modell eine Erfolgsmeldung erzeugt hat. Ein Timeout oder eine getrennte Browserverbindung ist ein unbekannter Zustand, bis der Effekt abgeglichen wurde.

Vor einem externen Effekt reserviere atomar das Tupel aus `capability_id`, `idempotency_key`, kanonischem `arguments_digest` und `resource_scope`. Ein identischer Wiederholungsversuch liefert die ursprüngliche endgültige Quittung zurück; ein laufendes Duplikat wartet oder löst einen Abgleich aus. Die Wiederverwendung eines Schlüssels mit geänderter Fähigkeit, geändertem Argument-Digest oder geändertem Scope ist eine Kollision und muss abgelehnt werden, bevor ein weiterer Effekt eintreten kann.

Bei Aktionen mit hoher Tragweite benötigen Prüfer vor der Freigabe die Quellenbelege und den genauen vorgeschlagenen Effekt. Die bloße Prüfung einer Modellzusammenfassung ist keine sinnvolle Aufsicht.

## Sandboxing reduziert eine Klasse von Risiken {#sandboxing-reduces-one-class-of-risk}

Ein isolierter Arbeitsbereich kann die Auswirkungen auf Dateisystem oder Prozesse begrenzen, beschränkt aber nicht automatisch den ausgehenden Netzwerkverkehr, Zugangsdaten, Datensichtbarkeit, Werkzeugfähigkeiten oder die Berechtigungen eines nachgelagerten Dienstes.

Definiere getrennt:

- Dateisystem-Scope und beschreibbare Pfade;
- Richtlinie für Prozesse, Pakete und Interpreter;
- Netzwerkziele und Anfragebudget;
- eingebundene Geheimnisse und Identität;
- in der Umgebung zulässige Datenklassifizierung;
- Exportpfad und Aufbewahrung von Artefakten;
- Nachweise für Abbruch und Bereinigung.

Die Host-Client-Server-Architektur von MCP legt Verbindungsberechtigungen, Benutzereinwilligung und Autorisierung beim Host fest. Betrachte dies als Protokollgrenze, die weiterhin anwendungsspezifische Sicherheitsrichtlinien erfordert. [MCP architecture](https://modelcontextprotocol.io/specification/latest/architecture)

## Ausgaben auf drei Ebenen validieren {#validate-output-at-three-levels}

| Ebene | Frage | Beispielnachweis |
|---|---|---|
| Strukturell | entspricht die Antwort dem deklarierten Schema? | Ergebnis von Parser und Schema-Validator |
| Fachlich | ist die angeforderte Aktion für dieses Konto und diesen Zustand gültig? | Richtlinien- und Datenbankvalidierung |
| Sicherheit und Herkunft | ist sie erlaubt, durch Quellen gestützt und angemessen klassifiziert? | Zitat, Freigabe- und Richtlinienquittung |

Ein gültiges JSON-Objekt oder ein syntaktisch korrekter Befehl ist keine sichere fachliche Aktion.

## Das tatsächliche System testen {#test-the-actual-system}

Eine Sicherheitsevaluierung sollte Folgendes umfassen:

- feindselige Anweisungen in Benutzereingaben, abgerufenen Dateien, Werkzeugergebnissen und Tickets;
- fehlende oder widersprüchliche Autorisierungsattribute;
- mandantenübergreifende und veraltete Abrufversuche;
- fehlerhafte oder gültige, aber unsichere Werkzeugargumente;
- Wiederholungs-, Abbruch- und Pfade mit verlorener Antwort bei realen Effekten;
- Tests zur Protokollierung und Schwärzung sowie Vorfallswiederholung aus kontrollierten Referenzen;
- unabhängige menschliche Prüfung bei Workflows mit hohen Einsätzen.

Halte die Klassifizierung der Testeingaben und geschwärzte Nachweise fest, damit die Sicherheitsaussage nach einer Änderung von Modell, Prompt, Werkzeug oder Richtlinie erneut überprüft werden kann.

## Stolperfallen {#gotchas}

- **Entfernen per Regex ist keine Abwehr gegen Prompt Injection.** Es erfasst nur Formulierungen, die jemand vorhergesehen hat. **Lösung:** Vertrauensgrenzen erhalten und Werkzeuge außerhalb des Modells autorisieren.
- **Ein Sicherheits-Prompt ist kein Berechtigungssystem.** Das Modell kann dennoch eine nicht autorisierte Aktion vorschlagen. **Lösung:** Fähigkeiten an Anwendungsidentität, Scope und Ablauf binden.
- **Eine Sandbox mit breiten Zugangsdaten bleibt hochriskant.** Isolation neutralisiert nicht die Berechtigungen, die darin eingebunden sind. **Lösung:** minimale Berechtigungen einsetzen und unnötigen ausgehenden Verkehr blockieren.
- **Eine Prüfung nach der Aktion ist kein Rollback-Plan.** Ein Prüfer kann nicht jede Nachricht, Löschung oder Veröffentlichung rückgängig machen. **Lösung:** irreversible Effekte vor der Ausführung absichern und Idempotenz bzw. Abgleich nutzen.
- **Protokolle können genau das preisgeben, was die Sandbox schützen sollte.** Vollständige Prompts und Werkzeugergebnisse können zu einem Schattendatenspeicher werden. **Lösung:** geschwärzte Referenzen ausgeben, Zugriff schützen und Aufbewahrung durchsetzen.
- **Eine Ablehnung nach dem Abruf kommt zu spät.** Daten haben möglicherweise bereits eine Autorisierungsgrenze überschritten. **Lösung:** Richtlinien durchsetzen, bevor Abrufkontext das Modell erreicht.

## Quellen {#sources}

- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 8725: JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)

## Siehe auch {#see-also}

- [[agent-security]]
- [[agent-orchestration]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[llmops]]
