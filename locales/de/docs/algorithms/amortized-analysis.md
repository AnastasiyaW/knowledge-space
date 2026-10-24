---
title: "Amortisierte Analyse"
category: concepts
tags: [algorithms, complexity, amortized, dynamic-array]
level: 2
source_sha256: 1547f9a73a9a1cb72135ead4367c23d37aae2a754436459e29c15be551ccec8e
translation: machine
translated_at: '2026-10-24'
---
Hmm, that was a stray output. Let me actually produce the translation now.

---
title: Amortisierte Analyse
category: concepts
tags: [algorithms, complexity, amortized, dynamic-array]
---

# Amortisierte Analyse {#amortized-analysis}

Die amortisierte Analyse berechnet die durchschnittlichen Kosten pro Operation über eine Folge von Operationen und liefert so eine garantierte Schranke, unabhängig von der Eingabe. Anders als die Average-Case-Analyse (die von der Eingabeverteilung abhängt) gilt die amortisierte Komplexität für alle möglichen Operationsfolgen.

## Key Facts {#key-facts}

- Amortisierte Kosten = Gesamtkosten von n Operationen / n
- NICHT abhängig von Eingabewahrscheinlichkeiten – garantierte Schranke über alle Folgen
- Einzelne Operationen können teuer sein, der Durchschnitt ist aber günstig
- Häufigstes Beispiel: Anhängen an ein dynamisches Array (Python-Liste)

## Patterns {#patterns}

### Einfügen in ein dynamisches Array (Python-Liste) {#dynamic-array-python-list-insertion}

Ist das Array voll, wird die Kapazität verdoppelt und alle Elemente werden kopiert. Ein Resize findet bei den Größen 1, 2, 4, 8, 16, 32, ... statt.

```text
Cost of n insertions without resize: n
Cost of resize operations: 1 + 2 + 4 + 8 + ... + n = 2n - 1

Total cost of n insertions = n + (2n - 1) ~ 3n
Amortized cost per insertion = 3n / n = O(1)
```

Obwohl ein einzelner Resize O(n) kostet, geschieht er so selten, dass die amortisierten Kosten pro `append()` O(1) betragen.

### Wichtige Unterscheidung {#key-distinction}

| Konzept | Abhängig von | Garantie |
|---------|-----------|-----------|
| Worst Case | Einzelne ungünstigste Eingabe | Pro Operation |
| Average Case | Eingabe-Wahrscheinlichkeitsverteilung | Erwartungswert über zufällige Eingaben |
| Amortisiert | Folge von Operationen | Durchschnitt pro Operation, beliebige Folge |

## Gotchas {#gotchas}

- Amortisiertes O(1) bedeutet NICHT, dass jede Operation O(1) ist – einzelne Operationen können O(n) kosten
- Nicht geeignet für Echtzeitsysteme, in denen jede einzelne Operation schnell sein muss
- Die Garantie gilt für die gesamte Folge, nicht pro Operation
- Python `list.append()` ist amortisiert O(1), aber ein einzelnes Append kann eine O(n)-Kopie auslösen

## See Also {#see-also}

- [[complexity-analysis]] – grundlegende Komplexitätskonzepte
- [[data-structures]] – Interna der Python-Liste
