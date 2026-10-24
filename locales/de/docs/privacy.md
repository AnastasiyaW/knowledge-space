---
title: Datenschutz
description: "Welche Daten, Cookies und Werbung Happyin Knowledge Space verwendet."
---
# Datenschutz {#_1}

Der russische Zweig fügt kein eigenes Datenerfassungssystem hinzu: Er läuft auf denselben Seiten und nach denselben Regeln wie die englische Wissensdatenbank.

## Zählung ohne Cookies {#cookie}

Seitenaufrufe zählt Cloudflare Web Analytics: ohne Cookies und ohne Browser-Fingerprints. Der anonyme Zähler für Wiederkehrende und für „Stern“-Schaltflächen speichert Einträge nur im lokalen Speicher des Browsers; Einzelheiten und den Schalter finden Sie in der [englischen Datenschutzerklärung](https://happyin.space/privacy/).

## Google Analytics und Google-Werbung {#google-analytics-google}

Sofern die Betreiberin sie eingerichtet hat, laden die Seiten Google Analytics 4, auf Artikelseiten zusätzlich Google-AdSense-Werbung. Wie Google diese Daten nutzt, ist im Dokument [„Wie Google Informationen von Websites und aus Apps nutzt, auf denen Google-Dienste verwendet werden“](https://policies.google.com/technologies/partner-sites?hl=ru) sowie im Abschnitt zu [Werbe-Cookies von Google](https://policies.google.com/technologies/ads?hl=ru) beschrieben.

**Consent Mode v2** wird gesetzt, bevor Google-Skripte geladen werden:

- **Im EWR, im Vereinigten Königreich und in der Schweiz** ist die Speicherung für Analyse und Werbung standardmäßig untersagt. Sie sehen eine Abfrage, und Cookies von Google Analytics werden erst nach Auswahl von „Zulassen“ verwendet. Bis dahin kann Google Signale ohne Cookies und ohne Werbe-IDs erhalten (z. B. über den Seitenaufruf). Die Einwilligung in personalisierte Werbung erfasst in diesen Ländern die zertifizierte Nachricht von Google, sofern Werbung aktiviert ist; ohne sie wird keine personalisierte Werbung ausgespielt.
- **In den übrigen Ländern** sind diese Einstellungen standardmäßig aktiviert, und Google kann Analyse- und Werbe-Cookies setzen. Sie können sie jederzeit deaktivieren.
- **Global Privacy Control oder Do Not Track** deaktivieren alles: Das Google-Analytics-Tag wird nicht geladen, Werbung wird ohne cookiebasierte Personalisierung angezeigt.

**Ihre Auswahl.** Der Link „Datenschutzeinstellungen“ am Ende jeder Seite und die Schaltfläche unten öffnen die Abfrage erneut. „Ablehnen“ untersagt alle vier Consent-Mode-Signale in diesem Browser, stoppt unsere Analyseereignisse und löscht die Google-Cookies dieser Website (`_ga`, `_ga_*`, `__gads`, `__gpi`, `__eoi`). Die Auswahl wird im lokalen Speicher des Browsers gespeichert (`ks_consent_v2`). Um zu entscheiden, ob die Abfrage nötig ist, ruft die Seite `/api/consent-region` dieser Website auf; die Antwort lautet nur „nötig / nicht nötig“ anhand des Landes, das Cloudflare anhand der IP-Adresse ermittelt, und das Land wird nicht gespeichert.

**Was wir messen.** Nur aggregierte Aktionen: Aufrufe von Seiten und Artikeln, Nutzung der Suche und Öffnen von Ergebnissen, Kopieren von Code, Wechsel zu GitHub sowie erfolgreiche Anmeldungen zum Newsletter. Wir übermitteln in den Ereignissen keine Suchbegriffe, Prompts, E-Mail-Adressen, Texte aus Rückmeldungen, Query-Strings von URLs und Werbe-IDs; Google-Signale und Personalisierung der Werbung sind für unsere Analyse deaktiviert.

**Werbung** erscheint nur auf Artikelseiten: nie auf der Startseite, auf dieser Seite sowie auf den Seiten „Über das Projekt“ und „Kontakt“. Personalisierte Werbung können Sie im [„Meine Werbeeinstellungen“-Bereich von Google](https://myadcenter.google.com/) anpassen. Werbung ist mit dem Wort „Werbung“ gekennzeichnet und beeinflusst den Inhalt der Artikel nicht.

<p class="ks-counter-switch"><span data-ks-analytics-state>Für diesen Schalter wird JavaScript benötigt.</span> <button type="button" class="md-button" data-ks-analytics-preferences hidden>Datenschutzeinstellungen</button></p>

## Cookies {#cookie_1}

- **Google Analytics** (`_ga`, `_ga_*`, bis zu 2 Jahre) und **Werbe-Cookies von Google** (`__gads`, `__gpi`, `__eoi` auf dieser Domain sowie eigene Google-Cookies auf Google-Domains) — nur wie oben beschrieben.
- **Cloudflare** kann notwendige Sicherheits-Cookies setzen.
- Im **lokalen Speicher** (kein Cookie): Zähler für Wiederkehrende, Ihre Einwilligungsauswahl und ob das Abo-Fenster geschlossen wurde.

## Kontakt {#_2}

Fragen zu Daten stellen Sie in den [GitHub Issues](https://github.com/AnastasiyaW/knowledge-space/issues) oder im [Telegram-Kanal](https://t.me/happyin_space); Einzelheiten finden Sie auf der Seite [„Kontakt“](contact.md). Veröffentlichen Sie keine personenbezogenen Daten in einem öffentlichen Issue.

## Vollständige Richtlinie {#_3}

Die vollständige maßgebliche Richtlinie (Abo, Fehlerberichte, Drittanbieterdienste) finden Sie [auf Englisch](https://happyin.space/privacy/). Bei Abweichungen gilt bis zu einer gesonderten rechtlichen Prüfung der Übersetzung der englische Text.
