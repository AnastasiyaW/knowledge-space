---
title: "Tokenisierung für LLM-Systeme (September 2026)"
category: concepts
tags: [llm-agents, tokenization, bpe, wordpiece, sentencepiece, context-window]
level: 3
source_sha256: 01b13f5bd9f2f9317815d08a15c842b141219023754c66f860b45cbd0ed02c95
translation: machine
translated_at: '2026-10-24'
---
# Tokenisierung für LLM-Systeme (September 2026) {#tokenization-for-llm-systems-september-2026}

Geprüft am 2026-09-03. Tokenisierung bildet Eingabetext auf die ganzzahligen Sequenzen ab, die ein Modell verarbeitet. Token-Anzahlen, Spezial-Tokens, Kürzung und Chat-Formatierung sind modellspezifisch. Verwende für Budgets oder harte Grenzen niemals eine generische Schätzung über Zeichen pro Token.

## Tokenisierungs-Pipeline {#tokenization-pipeline}

| Stufe | Zweck |
|---|---|
| Normalisierung | Wendet konfigurierte Transformationen auf die Roheingabe an |
| Pre-Tokenisierung | Zerlegt Text in mögliche Einheiten |
| Modell | Bildet Einheiten bzw. Subwörter auf Token-IDs ab |
| Nachverarbeitung | Fügt Spezial-Tokens und Sequenzstruktur hinzu |
| Encoding | Enthält IDs, Offsets, Masken und verwandte Metadaten |

Die Hugging Face Tokenizers API dokumentiert diese Pipeline und die Tokenizer-Komponenten. [Tokenizer API](https://huggingface.co/docs/tokenizers/main/api/tokenizer)

## Algorithmusfamilien {#algorithm-families}

| Familie | Typische Eigenschaft | Mit Vorsicht verwenden |
|---|---|---|
| BPE | Häufige Merges erzeugen wiederverwendbare Subwörter | Vokabular- und Byte-Behandlung unterscheiden sich je nach Implementierung |
| WordPiece | Subwort-Bewertung mit Fortsetzungskonventionen | Die Token-Repräsentation ist tokenizerspezifisch |
| Unigram / SentencePiece | Probabilistisches Subwort-Vokabular und Behandlung von Rohtext | Whitespace- und Normalisierungsrichtlinien sind relevant |
| Zeichen-/Byte-Fallback | Abdeckung ungewöhnlicher Texte | Längere Sequenzen können Kosten und Latenz verändern |

Der Algorithmusname bestimmt weder Kosten noch Kontextverhalten. Maßgeblich sind das tatsächliche Tokenizer-Artefakt, das Chat-Template und die Serialisierung der Anfrage.

## Mit dem exakten Tokenizer zählen {#count-with-the-exact-tokenizer}

Dieses Python-Beispiel verwendet ein benanntes Tokenizer-Artefakt und liefert die exakten IDs für dieses Artefakt.

```python
from tokenizers import Tokenizer


tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
encoding = tokenizer.encode("A token budget must use the deployment tokenizer.")

print("token_count=", len(encoding.ids))
print("tokens=", encoding.tokens)
```

Verwende bei gehosteten APIs die vom Anbieter dokumentierte Tokenizer- bzw. Zählmethode für das genaue Modell und Anfrageformat. Berücksichtige im Budget Systemnachrichten, Tool-Definitionen, abgerufenen Kontext, Anhänge und die Reservierung für die erwartete Ausgabe.

## Kontextbudget {#context-budget}

```text
context_limit
  - fixed instructions
  - tool schemas
  - conversation state
  - retrieved evidence
  - current user input
  - output reservation
  = remaining input budget
```

Kürze nicht stillschweigend. Lege fest, welche Inhalte zusammengefasst, erneut abgerufen, verworfen oder für eine kleinere Aufgabe zurückgehalten werden können.

## Unicode und strukturierte Daten {#unicode-and-structured-data}

- Sprachen, Code, JSON, URLs und Base64-Nutzlasten können sehr unterschiedliche Token-Dichten aufweisen.
- Eine sichtbare Zeichenfolge kann je nach Tokenizer unterschiedlich normalisiert oder zerlegt werden.
- Tool-Definitionen und große Tool-Ergebnisse können Kontext verbrauchen, bevor die Benutzereingabe verarbeitet wird.
- Die Abrechnung multimodaler Anfragen ist anbieterspezifisch. Halte dich an die aktuellen Vorgaben des Anbieters, statt Medien als Text-Token zu behandeln.

## Stolperfallen {#gotchas}

- **Problem: Kosten mit einer festen Regel für Zeichen pro Token schätzen.** Die Schätzung kann bei nicht-englischem Text, Code oder strukturierten Daten falsch sein. **Lösung:** Zähle mit dem exakten Deployment-Tokenizer und der vollständigen Serialisierung der Anfrage.
- **Problem: Den Tokenizer des Basistexts verwenden, aber Chat- bzw. Tool-Formatierung weglassen.** Die Anfrage kann das tatsächliche Kontextlimit überschreiten. **Lösung:** Berücksichtige Systemanweisungen, Tool-Schemata, abgerufene Chunks und die Ausgabereserve.
- **Problem: Versehentliches Abschneiden der neuesten Evidenz.** Ein simpler Zuschnitt kann irrelevante Historie erhalten und die Aufgabe verlieren. **Lösung:** Definiere eine zustandsbewusste Kürzungs- oder Retrieval-Strategie.
- **Problem: Tokenizer-Artefakte ohne Evaluation wechseln.** Token-Grenzen können Retrieval, Prompt-Länge und Modellverhalten beeinflussen. **Lösung:** Versioniere den Tokenizer zusammen mit der Modellkonfiguration.

## Siehe auch {#see-also}

- [[chunking-strategies]]
- [[context-engineering]]
- [[rag-pipeline]]
- [[model-optimization]]

## Quellen {#sources}

- [Hugging Face Tokenizers API](https://huggingface.co/docs/tokenizers/main/api/tokenizer)
- [Hugging Face Transformers Tokenizer-Referenz](https://huggingface.co/docs/transformers/main_classes/tokenizer)
