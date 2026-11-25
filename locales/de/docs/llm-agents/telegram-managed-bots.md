---
title: "Telegram Managed Bots"
description: "Ein produktionssicherer Leitfaden zum Manager-Bot-Modell von Telegram: Erstellung, Token-Rotation, Zugriffseinstellungen, Zustandsisolierung und Lebenszyklus-Belege."
tags: [telegram, bot-api, managed-bots, security, deployment]
level: 3
source_sha256: 8754df886567939fdadb542cba4bdace4b4a8a746ac0dac9e34f2dca2ae1d56c
translation: machine
translated_at: '2026-10-24'
---
# Telegram Managed Bots {#telegram-managed-bots}

**Geprüft am: 2026-09-04.** Mit Managed Bots kann ein Manager-Bot im Auftrag seines Besitzers einen Bot erstellen und betreiben. Die Funktion wurde in Bot API 9.6 eingeführt; die aktuelle API dokumentiert weiterhin den Erstellungsablauf, die Token-Methoden, die Zugriffseinstellungen und die Update-Typen. Es handelt sich um eine Kontrollebenen-Funktion von Telegram, nicht um ein vollständiges System für Mandantentrennung oder Datenisolation in Anwendungen. [Bot API changelog](https://core.telegram.org/bots/api-changelog) [Managed Bots guide](https://core.telegram.org/bots/features#managed-bots)

## Was Telegram bereitstellt {#what-telegram-provides}

Der Manager ist ein regulärer Bot, für den in BotFather Bot Management Mode aktiviert ist. Ein Nutzer folgt einem newbot-Deep-Link, bestätigt einen editierbaren vorgeschlagenen Bot-Namen und Benutzernamen, und Telegram sendet dem Manager ein **managed_bot**-Update. Das Update enthält ein **ManagedBotUpdated**-Objekt mit dem Besitzer und dem verwalteten Bot. Der Manager kann anschließend sein Token über **getManagedBotToken** abrufen. [Managed Bots guide](https://core.telegram.org/bots/features#managed-bots) [Bot API objects](https://core.telegram.org/bots/api#managedbotupdated)

Telegram dokumentiert außerdem:

- **replaceManagedBotToken**, das das alte Token widerruft und ein neues Token zurückgibt;
- **getManagedBotAccessSettings** und **setManagedBotAccessSettings**, die die Zugriffsrichtlinie des Bots anzeigen und ändern;
- nachfolgende managed-bot-Updates, wenn sich Token oder Besitzer eines verwalteten Bots ändern.

Diese Funktionen identifizieren den Telegram-Bot und steuern ihn. Sie partitionieren nicht Ihre Datenbank, Ihren Objektspeicher, Ihr Konto beim Modellanbieter, Ihre Analysen oder den Operator-Zugriff. Diese Grenzen müssen Sie explizit gestalten.

## Produktionstopologie {#production-topology}

Verwenden Sie eine Manager-/Kontrollebene und eine separate Mandantenlaufzeit:

```text
owner confirms bot creation
        |
manager bot receives managed_bot update
        |
control plane records owner, bot id, lifecycle version
        |
secret store retains the token; application reads it by bot id
        |
tenant runtime processes that bot's updates under an authenticated tenancy
```

Der Routing-Schlüssel sollte ein serverseitiger Bot-Datensatz sein, kein vom Nutzer gelieferter Chat-ID- oder Prompt-Wert. Binden Sie jedes eingehende Update an den verwalteten Bot, der es empfangen hat, und ermitteln Sie danach Besitzer und zulässige Ressourcen außerhalb des Modells.

## Erstellungsereignis registrieren {#register-the-creation-event}

Die Methodennamen von Bot-Bibliotheken unterscheiden sich, daher sollte der Lebenszyklus-Vertrag unabhängig von einem bestimmten SDK bleiben:

```python
# Pseudocode: validate the webhook before parsing an update.
def register_managed_bot(update, telegram_api, registry):
    managed = update.get("managed_bot")
    if not managed:
        return

    owner_id = managed["user"]["id"]
    bot_id = managed["bot"]["id"]
    token = telegram_api.get_managed_bot_token(user_id=owner_id)

    registry.upsert(
        bot_id=bot_id,
        owner_id=owner_id,
        token_secret_ref=store_secret(token),
        lifecycle_event_id=update["update_id"],
    )
```

Speichern Sie die Update-ID oder einen anderen Idempotenzschlüssel, bevor Sie einen Worker bereitstellen. Telegram weist darauf hin, dass Update-IDs nützlich sind, um Duplikate zu ignorieren und die Reihenfolge wiederherzustellen; außerdem kann Telegram einen Webhook erneut zustellen. [Update](https://core.telegram.org/bots/api#update) [Webhooks](https://core.telegram.org/bots/api#setwebhook)

Geben Sie ein Managed-Bot-Token niemals zurück, protokollieren, committen oder in ein Task-Transkript einfügen. Behandeln Sie den Abruf, den Austausch und das Bootstrapping eines Workers als Vorgänge mit Geheimnissen.

## Updates sicher empfangen {#receiving-updates-safely}

Wählen Sie für jeden verwalteten Bot einen Zustellungsmodus: Long Polling oder Webhook. Telegram dokumentiert beide als sich gegenseitig ausschließend. Ein Webhook sollte HTTPS und ein eindeutiges Secret-Token verwenden; Telegram sendet den passenden Wert im Header X-Telegram-Bot-Api-Secret-Token. [Getting updates](https://core.telegram.org/bots/api#getting-updates) [setWebhook](https://core.telegram.org/bots/api#setwebhook)

Bevor Sie ein Update verteilen:

1. prüfen Sie Transport und Webhook-Secret;
2. ermitteln Sie den Managed-Bot-Datensatz aus dem Ingress-Endpunkt oder der authentifizierten Laufzeit;
3. dedupizieren Sie die Update-ID und protokollieren Sie den Zustellungsbeleg;
4. laden Sie nur die Mandantenrichtlinie, den Konversationszustand, die Tools und die Geheimnisse dieses Bots;
5. wenden Sie Autorisierungs- und Ratenkontrollen an, bevor ein Modell oder ein externer Dienst aufgerufen wird;
6. speichern Sie ein geschwärztes Audit-Ereignis mit Bot-ID, Besitzerreferenz, Aktion und Ergebnis.

Behaupten Sie für ein Managed-Bot-Produkt keinen festen Durchsatzwert. Limits und Zustellungsverhalten richten sich nach der aktuellen Bot API und FAQ von Telegram und können sich ändern; testen Sie das konkrete ausgehende Muster und beobachten Sie die API-Antworten. [Bot API FAQ](https://core.telegram.org/bots/faq)

## Isolation ist ein Vertrag auf Anwendungsebene {#isolation-is-an-application-contract}

Verwenden Sie einen Managed Bot, wenn eine eigene Telegram-Identität und ein besitzergebundener Lebenszyklus nützlich sind. Erzwingen Sie die Anwendungsgrenze dennoch selbst:

| Ebene | Erforderliche Isolation |
|---|---|
| Telegram-Zugangsdaten | eine Secret-Referenz pro Managed Bot; Rotationsbeleg |
| Anwendungszustand | Mandanten- oder Bot-Schlüssel bei jedem Lesen und Schreiben |
| Dateien und Retrieval | namespacierter Speicher plus Autorisierung zum Zeitpunkt des Abrufs |
| Tools | Allowlist, ausgewählt über die authentifizierte Besitzerrichtlinie |
| Abrechnung und Kontingente | Metering mit demselben serverseitigen Mandantendatensatz |
| Betrieb | Audit-Trail und Incident-Rollback pro Bot |

Getrennte Token allein beweisen nicht, dass Worker A nicht auf die Daten von Worker B zugreifen kann.

## Lebenszyklus und Löschung {#lifecycle-and-deletion}

Behandeln Sie ein managed-bot-Update als Ereignis, das eine Erstellung, eine Rotation oder einen Besitzerwechsel auslösen kann. Rufen Sie das Secret nur über die dokumentierte API erneut ab und ersetzen Sie es nur dort; gleichen Sie den neuen Lebenszyklus-Zustand ab, bevor Sie die Zustellung wieder aufnehmen. **replaceManagedBotToken** widerruft das aktuelle Token, löscht aber weder Ihre Mandantendatensätze, Dateien noch den Modellverlauf. [Token methods](https://core.telegram.org/bots/api#getmanagedbottoken)

Ein vom Besitzer angefordertes Löschverfahren sollte einen eigenen Beleg erzeugen:

1. authentifizieren Sie den Besitzer über die aktuelle Bot- und Anwendungsrichtlinie;
2. deaktivieren Sie den Ingress und widerrufen oder rotieren Sie das Token, je nach Bedarf;
3. entziehen Sie dem Mandanten den Zugriff auf Daten, Jobs und Integrationen;
4. führen Sie die anwendbare Aufbewahrungs- und Löschrichtlinie für gespeicherte Inhalte aus;
5. protokollieren Sie die abgeschlossene Aktion, ohne das Token oder Nachrichteninhalte zu speichern.

Erfinden Sie keine Telegram-Funktion für gesetzliche Löschpflichten, Backup-Löschung oder systemübergreifenden Widerruf. Diese bleiben Verantwortung Ihres Systems.

## Fallstricke {#gotchas}

- **Ein Erstellungsupdate wird zweimal verarbeitet.** Wiederholungen können doppelte Worker bereitstellen. **Lösung:** Machen Sie die Registrierung idempotent über Update-ID und Managed-Bot-ID.
- **Ein Prompt wählt einen Bot oder Mandanten.** Dadurch kann die Datenauswahl mandantenübergreifend erfolgen. **Lösung:** Ermitteln Sie Bot und Besitzer aus dem authentifizierten Ingress, nicht aus der Modellausgabe.
- **Ein Token erscheint in einem Diagnoseprotokoll.** Es gewährt API-Zugriff. **Lösung:** Schwärzen Sie Geheimnisse, speichern Sie nur eine Referenz und rotieren Sie umgehend, wenn eine Offenlegung vermutet wird.
- **Ein Token wurde rotiert, der alte Worker bedient aber weiter.** Die lokale Konfiguration ist nun veraltet. **Lösung:** Stoppen Sie den alten Ingress, laden Sie das neue Secret neu und speichern Sie einen erfolgreichen Health-Beleg.
- **Ein Besitzer verliert den Zugriff.** Die Steuerung in Telegram kann sich ändern, während der Anwendungszustand bestehen bleibt. **Lösung:** Verarbeiten Sie Lebenszyklus-Updates und definieren Sie eine dokumentierte Richtlinie für Sperrung und Wiederherstellung.

## Quellen {#sources}

- [Telegram Bot API changelog](https://core.telegram.org/bots/api-changelog)
- [Telegram Managed Bots guide](https://core.telegram.org/bots/features#managed-bots)
- [Telegram Bot API: updates, webhooks, and managed-bot methods](https://core.telegram.org/bots/api)
- [Telegram Bot API FAQ](https://core.telegram.org/bots/faq)

## Siehe auch {#see-also}

- [[multi-agent-messaging]]
- [[agent-deployment]]
- [[tool-use-patterns]]
- [[agentic-security-2026]]
