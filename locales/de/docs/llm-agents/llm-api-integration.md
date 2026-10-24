---
title: "LLM-API-Integration"
description: "Providerintegrationen auf Basis typisierter Verträge, sicherer Konfiguration, expliziten Zustands, Wiederholungslogik und beobachtbaren Release-Gates aufbauen."
tags: [llm-agents, api, openai, anthropic, streaming, function-calling, llmops]
level: 5
source_sha256: 0a36fa4575d393cecff4202e9354046cf1205f33ce141d1bfbf9defa4cbf8322
translation: machine
translated_at: '2026-10-24'
---
# LLM-API-Integration (September 2026) {#llm-api-integration-september-2026}

Versionskontext: Modell-IDs, Endpunkte, Antwortstrukturen, Rate Limits, Aufbewahrungsoptionen, Tool-Semantik und Preise ändern sich unabhängig voneinander. Halte sie in geprüfter Konfiguration und validiere den genauen Provider-Vertrag zum Zeitpunkt des Deployments. Diese Seite verwendet keine statische Preistabelle und keine dauerhafte Modellempfehlung.

Eine produktive LLM-Integration ist eine Anwendungsgrenze und nicht bloß ein einzelner SDK-Aufruf. Sie benötigt typisierte Ein- und Ausgaben, Identitäts- und Datenkontrollen, Modellkonfiguration, Timeouts, Wiederholungssemantik, Nutzungstelemetrie sowie eine Möglichkeit, eine Verhaltensänderung nachzuvollziehen oder zurückzurollen.

## Mit einem providerneutralen Vertrag beginnen {#start-with-a-provider-neutral-contract}

Halte die Anwendungslogik unabhängig von einem SDK-Antwortobjekt.

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    task_id: str
    model_key: str
    input_text: str
    max_output_tokens: int


@dataclass(frozen=True)
class LLMResult:
    text: str
    provider_request_id: str
    model_revision: str
    usage: dict[str, int]
    finish_state: str


class LLMProvider(Protocol):
    def complete(self, request: LLMRequest) -> LLMResult: ...
```

Der Adapter verantwortet die providerspezifische Request-Konstruktion, Streaming-Ereignisse, Tool-Call-Schleifen, Fehler und die Extraktion der Nutzungsdaten. Die Anwendung verantwortet Autorisierung, fachliche Validierung, Idempotenz und die für Nutzer sichtbaren Richtlinien.

## Sichere Konfiguration {#secure-configuration}

Verwende einen Secret Manager, Workload Identity oder eine vom Deployment-System verwaltete Umgebungsinjektion. Lege API-Schlüssel nicht in Quelldateien, Browser-Code, Screenshots, Dokumenten, Prompts, Logs oder für das Modell zugänglichen Tools ab.

Halte Konfiguration getrennt vom Code:

```json
{
  "provider": "approved_provider",
  "model_key": "support_triage_v4",
  "model_id": "reviewed-at-deploy",
  "timeout_seconds": 45,
  "max_output_tokens": 300,
  "data_policy_revision": "policy@12",
  "tool_policy_revision": "tools@7"
}
```

Ein Modellschlüssel erlaubt der Anwendung, eine geprüfte Fähigkeit anzufordern, während die Deployment-Konfiguration ihn auf ein aktuell freigegebenes Provider-Modell abbildet. Protokolliere die aufgelöste Modellrevision im Ergebnisbeleg.

## OpenAI Responses API {#openai-responses-api}

Die aktuelle OpenAI Responses API akzeptiert Text-, Bild- und Dateieingaben, stellt Status- und Nutzungsdaten bereit und kann Tool-Calls zurückgeben. Verwende das SDK-Komfortfeld nur für Text, nachdem der terminale Status geprüft wurde.

```python
import os
from openai import OpenAI


def run_openai(prompt: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=os.environ["OPENAI_MODEL"],
        input=prompt,
        max_output_tokens=300,
    )
    if response.status != "completed":
        raise RuntimeError(f"response did not complete: {response.status}")
    return response.output_text
```

Schreibe keinen Modellnamen fest in einen wiederverwendbaren Artikel oder ein Anwendungsmodul. Beschränke die Umgebungsvariable in der Deployment-Konfiguration auf eine freigegebene Allowlist.

## Anthropic Messages API {#anthropic-messages-api}

Die Messages API nimmt eine strukturierte Konversation entgegen und erzeugt die nächste Nachricht. Wenn dein Produkt Reproduzierbarkeit, Aufbewahrungskontrollen oder providerübergreifende Portabilität benötigt, halte den Konversationszustand in einem anwendungseigenen Datensatz.

```python
import os
import anthropic


def run_anthropic(prompt: str) -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=os.environ["ANTHROPIC_MODEL"],
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(
        block.text for block in message.content if block.type == "text"
    )
```

Antwortblöcke des Providers können mehr als sichtbaren Text enthalten. Bewahre die typisierte Antwort auf, bis Richtlinienprüfung und Tool-Verarbeitung abgeschlossen sind; nimm nicht an, dass der erste Inhaltsblock das einzige Ergebnis ist.

## Zustand ist eine Produktentscheidung {#state-is-a-product-decision}

Verschiedene APIs bieten unterschiedliche Mechanismen für Konversation und Aufbewahrung. OpenAI Responses kann Aufrufe über eine Konversations- oder Kennung der vorherigen Antwort verknüpfen; die Anthropic Messages API lässt sich mit einer expliziten Nachrichtenliste verwenden. Ein generischer Adapter sollte keines dieser Verhalten als universelles Speichermodell behandeln.

Protokolliere für jede Anfrage:

- anwendungseigene Konversations- oder Task-ID;
- Konfiguration und Modellrevision;
- Klassifizierung der Eingabe- bzw. Inhaltsrichtlinie;
- Request- und Response-Kennungen des Providers;
- Entscheidungen zu Tool-Calls und Freigaben;
- terminalen Status, Nutzung und Anzahl der Wiederholungen;
- Referenz auf den bereinigten Trace und die Aufbewahrungsrichtlinie.

Damit erhält ein Operator eine reproduzierbare Task-Grenze, ohne mehr Inhalte zu speichern, als die Richtlinie erlaubt.

## Streaming braucht einen Ereignisvertrag {#streaming-needs-an-event-contract}

Provider-Streams sind Ereignisfolgen und nicht bloß Textfragmente. Leite sie durch einen Parser, der Start-, Delta-, Tool-Input-, Nutzungs-, Fehler-, Abschluss- und Abbruchereignisse erkennt.

```text
stream event -> provider parser -> typed application event
             -> validation / UI update -> durable terminal receipt
```

Führe kein Tool auf Basis eines unvollständigen JSON-Fragments aus. Sammle und validiere die vollständige Tool-Eingabe, autorisiere sie serverseitig, führe sie mit einem Idempotenzschlüssel aus und gib anschließend ein strukturiertes Tool-Ergebnis zurück. Einige Provider erlauben bewusst feingranulares Tool-Streaming, bei dem JSON während der Übertragung unvollständig sein kann.

## Strukturierte Ausgabe und Tool-Calls {#structured-output-and-tool-calls}

Verwende Schemata an beiden Grenzen:

1. Gib dem Modell ein enges Ausgabe- oder Tool-Schema vor.
2. Parse mit einem echten JSON-/Schema-Validator.
3. Prüfe fachliche Invarianten, Mandantenbezug und Autorisierung im Anwendungscode.
4. Binde Berechtigungsnachweise an die jeweils auszuführende Aktion, nicht breit an den Modellprozess.
5. Gib einen typisierten Fehler oder eine Korrekturanforderung zurück; erzwinge niemals stillschweigend einen unsicheren Wert.
6. Speichere einen Beleg, der die Richtlinien- und Schema-Revisionen identifiziert.

Ein gültiges JSON-Objekt ist nicht automatisch eine gültige fachliche Aktion.

## Wiederholungen, Idempotenz und Rate Limits {#retries-idempotency-and-rate-limits}

Wiederhole nur Fehler, die nachweislich gefahrlos wiederholbar sind. Verwende für vorübergehende Netzwerk-, Kapazitäts- oder Rate-Limit-Fehler ein begrenztes exponentielles Backoff mit Jitter gemäß der aktuellen Empfehlung des Providers. Wiederhole keine externe Seiteneffekte allein deshalb, weil eine LLM-Antwort fehlt.

Erstelle bei einem Workflow mit Seiteneffekten den Idempotenzschlüssel vor dem Provider-Aufruf und führe ihn durch die Tool-Ausführung weiter:

```json
{
  "task_id": "invoice-summary-003",
  "idempotency_key": "task:invoice-summary-003:v1",
  "effect": "send_draft_only",
  "retry_budget": 3,
  "terminal_state": "pending"
}
```

Verwende für lang laufende Anfragen eine Warteschlange oder einen Hintergrundjob. Ein geschlossene Browserverbindung ist kein Beweis dafür, dass die zugrunde liegende Aufgabe fehlgeschlagen oder erfolgreich war.

## Observability und Kostenkontrolle {#observability-and-cost-control}

Erfasse die vom Provider gemeldete Nutzung, Latenz, Status, Fehler, Modellrevision, Cache-Signale sofern verfügbar, Anzahl der Tool-Calls und das Task-Ergebnis. Binde Alarme an für Nutzer sichtbare Fehler und genehmigte Budgets, nicht an einen fest codierten Preis aus einem früheren Release.

Teste jeden Provider-Adapter mit:

- einer regulären Antwort sowie einer unvollständigen bzw. fehlerhaften Antwort;
- einem Timeout und einem begrenzten Wiederholungsversuch;
- einer Verletzung der strukturierten Ausgabe;
- einem partiellen Stream oder partieller Tool-Eingabe;
- einer doppelten Zustellung derselben Aufgabe;
- einer mandantenübergreifenden oder nicht autorisierten Tool-Anfrage;
- einem Modell- bzw. Konfigurationswechsel mit der Release-Evaluierungssuite.

## Stolperfallen {#gotchas}

- **SDK-Objekte sind providerspezifisch.** Wenn sie direkt in den Anwendungscode gelangen, werden Migration und Tests fragil. **Lösung:** In einen kleinen internen Ergebnisvertrag normalisieren.
- **Eine Konversations-ID ist keine Aufbewahrungsrichtlinie.** Provider- und Anwendungszustand können unterschiedliche Aufbewahrungsregeln haben. **Lösung:** Lege fest, wo der Verlauf liegt und was gelöscht oder bereinigt wird.
- **Partielle Streamdaten sind keine ausführbare Eingabe.** Tool-JSON kann während des Streamings unvollständig oder ungültig sein. **Lösung:** Puffern, parsen, validieren, autorisieren und erst dann ausführen.
- **Wiederholungen können Seiteneffekte duplizieren.** Ein Timeout beweist nicht, dass die erste Anfrage fehlgeschlagen ist. **Lösung:** Idempotenzschlüssel verwenden und den terminalen Zustand abgleichen.
- **Statische Preisbeispiele veralten schnell.** Kosten hängen von Modell, Tarif, Cache-Verhalten und Ausgabe ab. **Lösung:** Vom Provider gemeldete Nutzung und die aktuellen Preise zum Planungszeitpunkt verwenden.

## Quellen {#sources}

- [OpenAI Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [Anthropic Messages API reference](https://platform.claude.com/docs/en/api/messages/create)
- [Anthropic streaming messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Anthropic fine-grained tool streaming](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming)

## Siehe auch {#see-also}

- [[prompt-engineering]]
- [[function-calling]]
- [[tokenization]]
- [[llmops]]
- [[frontier-models]]
- [[agent-security]]
