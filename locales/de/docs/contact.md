---
title: Kontakt
description: "So erreichen Sie die Betreuer der Happyin Knowledge Space: GitHub-Issues für Korrekturen und Anfragen, Telegram für Neuigkeiten und Fragen."
---
# Kontakt {#contact}

## Korrekturen, Fragen und Artikelwünsche {#corrections-questions-and-article-requests}

Eröffnen Sie ein Issue im öffentlichen GitHub-Repository: [github.com/AnastasiyaW/knowledge-space/issues](https://github.com/AnastasiyaW/knowledge-space/issues). Das ist der schnellste Weg, eine falsche oder veraltete Seite zu melden, ein Thema anzufragen oder eine Datenschutzfrage zu stellen. Issues sind öffentlich. Bitte nehmen Sie daher keine personenbezogenen Daten auf. Wenn Sie etwas Vertrauliches mitteilen möchten, schreiben Sie das im Issue, und wir richten einen privaten Kanal ein.

Pull Requests sind ebenfalls willkommen: [Wie Sie beitragen können](contributing/index.md).

## Telegram {#telegram}

Neuigkeiten zur Wissensdatenbank und ein Ort für Fragen: [t.me/happyin_space](https://t.me/happyin_space).

## Meldungen von KI-Assistenten und Skripten {#reports-from-ai-assistants-and-scripts}

Ein KI-Assistent oder ein Skript kann einen veralteten Artikel oder ein fehlendes Thema mit einer einzigen Anfrage melden, ohne Konto. Ein einfacher GET genügt, daher kann jedes Fetch-Werkzeug sie senden:

```text
https://happyin.space/api/feedback/report?kind=gap&topic=<what you looked for>&agent=<your client name>
https://happyin.space/api/feedback/report?kind=outdated&article=<domain/slug>&detail=<what changed>
```

Skripte können dieselben Felder auch als JSON per POST an `https://happyin.space/api/feedback` senden; ein GET auf diese Adresse liefert die vollständige Feldliste. Die Antwort enthält einen Status-Link, der zeigt, was mit der Meldung geschieht. Senden Sie nur, was Sie auch in ein öffentliches Issue schreiben würden: keine personenbezogenen Daten, keinen privaten Code und keine Geheimnisse.

## Werbung und Partnerschaften {#advertising-and-partnerships}

Anzeigen auf dieser Website werden über Google AdSense ausgespielt; Werbeplätze verkaufen wir nicht direkt. Für andere Partnerschaftsanfragen eröffnen Sie bitte ein GitHub-Issue oder schreiben Sie uns in Telegram.
