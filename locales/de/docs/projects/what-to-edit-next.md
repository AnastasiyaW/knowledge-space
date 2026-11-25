---
title: "Was als Nächstes bearbeiten — Referenz der öffentlichen Website"
category: projects
date: 2026-08-17
tags: [alibaba/what-to-edit-next, project, public-site-reference, what-to-edit-next]
aliases: ["What to Edit Next"]
level: 2
source_sha256: ff3092ba99717b66d4bad1fc645e9e2c015c9d5403103929f3660fdfe43f5f0f
translation: machine
translated_at: '2026-10-24'
---
# Was als Nächstes bearbeiten — Referenz der öffentlichen Website {#what-to-edit-next-public-site-reference}

**Entwicklungslinie:** `project:what-to-edit-next` · Thread `public-site-reference`  
**Letztes Ereignis:** 2026-08-17 · 1 datiertes seit 2026-08-17 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

What to Edit Next ist eine Methode der Qwen App, die aus dem neuesten Bild, der aktuellen Anfrage und der Bearbeitungsabsicht die nächste Bearbeitung vorschlägt.

- Qwen3-VL-8B-Policy, feinabgestimmt mit kuratierten Absichten und Klick-Feedback.
- Bildorientierter Qwen3-VL-30B-A3B-Verifier, der während des Trainings nicht unterstützte oder redundante Bearbeitungen verwirft.

## Entwicklungslinie {#development-line}

- **2026-08-17 — Auf die öffentliche Website von What to Edit Next wurde verwiesen.** Die Projektseite von What to Edit Next wurde verlinkt, um eine Referenz zur Website herzustellen. Dokumentiert ist nur dieser Verweis, nicht ein Start, eine Funktionsveröffentlichung, eine Code-Veröffentlichung oder eine Änderung des öffentlichen Zugangs.

## Was sich geändert hat {#what-changed}

- 2026-08-03: What to Edit Next v1 wurde bei arXiv eingereicht und dokumentiert die dreistufige Methode der Qwen App.
- 2026-08-17: Die Projektseite von What to Edit Next wurde verlinkt; dies stellt nur eine Referenz zur Website her, keinen dokumentierten Start, keine Funktionsveröffentlichung, keine Code-Veröffentlichung und keine Änderung des öffentlichen Zugangs.
- 2026-08-18: What to Edit Next arXiv v2 wurde eingereicht; deren Versionsverlauf enthält kein Änderungsprotokoll.

## So wird es verwendet {#how-to-use-this}

Stand 2026-08-17 sollte man zur Bewertung von What to Edit Next zunächst die verlinkte öffentliche Projektseite heranziehen. Quellenmaterial direkt prüfen, bevor Funktionen oder Veröffentlichungsstand angenommen werden.

1. Mit der Projektseite beginnen, um die Methode zu beurteilen, nicht um sie zu installieren. Ihre sichtbare Navigation verweist auf Paper-, arXiv- und Methodenmaterial, nicht auf einen öffentlichen Integrationseinstieg.
  — <https://what-to-edit-next.github.io/>
2. Für eine vergleichbare Implementierung jede Eingabe aus dem neuesten Bild, der umformulierten aktuellen Anfrage und der Bearbeitungsabsicht bilden. Fünf bis sieben Vorschläge erzeugen und drei davon zufällig zur Anzeige auswählen.
  — <https://arxiv.org/html/2608.07565v1>
3. Bearbeitungen bildorientiert validieren. Das Bild inventarisieren, jeden Kandidaten in benötigte Quellen und gewünschte Zielzustände zerlegen und dann fehlende Quellen sowie bereits erfüllte Ziele verwerfen. Ein hinzugefügtes Objekt ist ein Ziel und muss nicht bereits sichtbar sein.
  — <https://arxiv.org/html/2608.07565v1>

## Bewährte Vorgehensweisen {#best-practices}

- Nicht allein auf Klicks optimieren. Die Autoren berichten, dass die visuelle Inkonsistenz von 3,0 % nach SFT auf 3,7 % nach Klick-RL steigt und dann mit der Grounding-Belohnung auf 0,9 % sinkt.
  — <https://arxiv.org/html/2608.07565v1>
- Das Bild betrachten, bevor Kandidatenanweisungen interpretiert werden. Prüfungen auf Existenz der Quelle getrennt von Prüfungen des Zielzustands halten.
  — <https://arxiv.org/html/2608.07565v1>
- Das Paper als Entscheidungsvertrag behandeln, nicht als reproduzierbares Produktionspaket. Es lässt wörtliche Produktionsprompts, produktspezifische Lexika und genaue Auslöser der Nachverarbeitung weg.
  — <https://arxiv.org/html/2608.07565v1>

## Ersetzt durch dieses {#superseded-by-this}

- 2026-08-18: arXiv v1 (2026-08-03) war nicht mehr die neueste Paper-Version, als v2 eingereicht wurde. Material, das spezifisch für v2 ist, nicht dem 2026-08-17 zuschreiben.

## Weiterhin unbekannt {#still-unknown}

- Die Projektseite hat keinen Veröffentlichungszeitstempel. Ihr Inhalt und ihre Verfügbarkeit am 2026-08-17 lassen sich von der aktuellen Seite aus nicht feststellen.
- Sichtbare Links belegen nicht, dass Code, Gewichte, eine API oder eine Demo nicht anderswo existieren.
- arXiv v2 hat keinen Revisionshinweis, daher sind die inhaltlichen Unterschiede zu v1 unbekannt.
- In den geprüften Quellen wurde keine datierte Ankündigung des Herstellers auf Chinesisch und kein öffentlicher Implementierungsleitfaden gefunden.
- Der einzelne datierte Eintrag und das passende Preprint beziehen sich auf einen einzigen Gegenstand; ein zweites Projekt mit demselben Namen wurde nicht gefunden.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://what-to-edit-next.github.io/ | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems | 2026-09-05 |
| https://arxiv.org/abs/2608.07565v1 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv v1 | 2026-09-05 |
| https://arxiv.org/html/2608.07565v1 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv HTML v1 | 2026-09-05 |
| https://arxiv.org/abs/2608.07565 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv version history | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:what-to-edit-next`, Thread `public-site-reference`, 1 datiertes Ereignis 2026-08-17 → 2026-08-17.
- **Praktischer Hinweis:** Stand 2026-08-17 die Bewertung bei der verlinkten öffentlichen Projektseite beginnen. Quellenmaterial direkt prüfen, bevor Funktionen oder Veröffentlichungsstatus angenommen werden.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, sind die datierten Ersetzungshinweise maßgeblich.
