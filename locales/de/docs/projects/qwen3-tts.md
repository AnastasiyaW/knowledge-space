---
title: "Qwen3-TTS"
category: projects
date: 2026-08-06
tags: [project, qwen3-tts, qwen3-tts-release-and-distribution, qwen3_tts]
aliases: ["Qwen3-TTS"]
level: 3
source_sha256: 2de0a05c6be6e522decb06701a4117cc07268732337af8a14af29ba6d41762f7
translation: machine
translated_at: '2026-10-24'
---
# Qwen3-TTS {#qwen3-tts}

**Entwicklungslinie:** `project:qwen3-tts` · Thread `qwen3-tts-release-and-distribution`  
**Letztes Ereignis:** 2026-08-06 · 2 datierte seit 2025-09-23 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Qwen3-TTS ist eine Open-Weight-Serie zur Sprachsynthese für Entwickler, die cloudbasierte TTS-APIs wie ElevenLabs ersetzen soll. Sie bietet CustomVoice für voreingestellte Klangfarben, VoiceDesign für Textbeschreibungen und Base für das Klonen anhand eines Audio-Referenzbeispiels.

- 10 Sprachen bei der Sprachsynthese
- Base: 3-Sekunden-Klonen aus einem Referenz-Audio
- Generierung: Streaming- und Batch-Modi
- CustomVoice: bis zu 9 voreingestellte Klangfarben

Die angegebene minimale End-to-End-Latenz beträgt 97 ms; als Open-Weight-Varianten stehen 0.6B und 1.7B zur Verfügung. Es ist eine praktikable Wahl für lokale mehrsprachige TTS, wenn wir Python und PyTorch ausführen oder das Base-Modell über eine kompatible GGUF-Laufzeitumgebung betreiben können.

## Entwicklungslinie {#development-line}

- **2025-09-23 — Qwen verlinkte eine offizielle Qwen3-TTS-Demo und die Qwen-TTS-Dokumentation.** Mehrere Klangfarben, mehrsprachige und dialektale Sprachsynthese; die primäre offizielle Veröffentlichung ist auf 2025-09-21 datiert.
- **2026-08-06 — ggml-org veröffentlichte eine GGUF-Distribution von Qwen3-TTS-12Hz-1.7B-Base.** Am 2026-08-06 verzeichnete der datierte Link eine GGUF-Distribution von Qwen3-TTS-12Hz-1.7B-Base auf Hugging Face. Dabei handelte es sich um einen nachgelagerten Distributionsschritt und nicht um eine upstream veröffentlichte Qwen-Modellversion, er erweiterte jedoch den Pfad für lokale Laufzeit-Deployments des Projekts erheblich.

## Was sich geändert hat {#what-changed}

- **2025-09-23** — Qwen3-TTS-Flash legte die API-Richtung für mehrere Klangfarben, mehrsprachige und dialektale Sprachsynthese fest; die erste offizielle Veröffentlichung ist auf 2025-09-21 datiert.
- **2025-12-04** — Flash wurde auf 49 Klangfarben, 10 Sprachen und 9 Dialekte erweitert; dies war ein API-Update und keine lokale Gewichtsveröffentlichung.
- **2025-12-22** — Qwen fügte die API-Modelle Qwen3-TTS-VD-Flash für Voice Design und Qwen3-TTS-VC-Flash für das Klonen anhand einer dreisekündigen Probe hinzu.
- **2026-01-22** — Qwen veröffentlichte die Open-Weight-Serie unter Apache-2.0 mit Tokenizer-12Hz, 0.6B Base/CustomVoice und 1.7B Base/CustomVoice/VoiceDesign; damit wurden lokales Deployment und Fine-Tuning in den upstream unterstützten Workflows möglich.
- **2026-08-06** — ggml-org veröffentlichte GGUF-Quantisierungen von Qwen3-TTS-12Hz-1.7B-Base für lokale Laufzeitumgebungen, die mit llama.cpp kompatibel sind; dies ist nachgelagerte Paketierung des Base-Modells und keine neue upstream Qwen-Variante.

## Anwendung {#how-to-use-this}

Ab 2025-09-23 sollten Praktiker, die Qwen3-TTS evaluieren, mit der verlinkten offiziellen Demo und der Qwen-TTS-Dokumentation beginnen; ab 2026-08-06 können Praktiker, die ein lokales Deployment anstreben, zusätzlich das verlinkte GGUF-Distributionspaket evaluieren.

1. Wähle CustomVoice für eine voreingestellte Klangfarbe, VoiceDesign für eine promptbasierte Klangfarbe oder Base für das Stimmklonen; für lokale Ausführung wähle 0.6B für geringere Anforderungen oder 1.7B für höhere Qualität.
  — <https://github.com/QwenLM/Qwen3-TTS>
2. Lege eine saubere Python-3.12-Umgebung an, installiere `qwen-tts` und lade das Modell mit `Qwen3TTSModel.from_pretrained`.
  — <https://github.com/QwenLM/Qwen3-TTS>
3. Für CustomVoice übergibst du Text, Sprache, Sprecher und optional instruct; für VoiceDesign lieferst du Text und eine natürlichsprachige Stimmbeschreibung; für Base stellst du Referenz-Audio und dessen Transkript bereit.
  — <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base>
4. Für einen leichteren lokalen Pfad nur für 1.7B Base führst du das GGUF-Release über llama.cpp aus, z. B. `llama serve -hf ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF:Q4_K_M`.
  — <https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF>

## Best Practices {#best-practices}

- Verwende eine saubere Python-Umgebung, damit sich TTS-Abhängigkeiten nicht mit bestehenden Projekten überschneiden; aktiviere FlashAttention 2 nur auf kompatibler Hardware mit float16/bfloat16.
  — <https://github.com/QwenLM/Qwen3-TTS>
- Setze die bekannte Sprache explizit statt Auto; verwende für die beste CustomVoice-Qualität die Muttersprache der gewählten Klangfarbe.
  — <https://github.com/QwenLM/Qwen3-TTS>
- Stelle die Base-Web-UI und das Mikrofon nicht über unverschlüsseltes HTTP bereit: Verlange für Remote-Zugriff in Produktion HTTPS und ein gültiges Zertifikat.
  — <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base>
- Behandle GGUF nicht als gleichwertigen Ersatz für die gesamte Familie: Das veröffentlichte Paket umfasst nur Base und liefert separate Quantisierungen Q4_K_M, Q8_0 und BF16.
  — <https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF>

## Abgelöst durch {#superseded-by-this}

- 2026-01-22: Qwen3-TTS ausschließlich als Qwen3-TTS-Flash-API zu behandeln, ist für die lokale Nutzung überholt; Apache-2.0-Gewichte für 0.6B/1.7B und der Quellcode sind veröffentlicht.
- 2026-08-06: GGUF Base ersetzt nicht die upstream CustomVoice- oder VoiceDesign-Modelle; für diese Aufgaben das Paket `qwen-tts` und die offiziellen Checkpoints verwenden.

## Weiterhin unbekannt {#still-unknown}

- Die Antwortstruktur enthält keine eigenen Felder `event_findings` und `new_events`; wir haben deren Fakten in die datierte Zeile `what_changed` übernommen.
- Das genaue Erstellungsdatum des GGUF-Repositorys war auf der Modellseite nicht ersichtlich; 2026-08-06 bleibt das erfasste Datum des verlinkten Ereignisses, die Paketdetails wurden anhand der Model Card geprüft.
- Wir haben DashScope-API-Preise, regionale Verfügbarkeit und aktuelle Ratenlimits nicht verifiziert; diese können unabhängig von der Open-Weight-Veröffentlichung abweichen.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://qwen.ai/blog?from=home.latest-research-list | Qwen3-TTS-Flash: Multi-timbre, Multi-lingual and Multi-dialect Speech Synthesis | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3-tts-1128 | Qwen3-TTS Update! 49 Timbres + 10 Languages + 9 Dialects | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign | Qwen3-TTS Steps Up: Voice Cloning and Voice Design! | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3tts-0115 | Qwen3-TTS Family Is Now Open Sourced: Voice Design, Clone, and Generation | 2026-09-05 |
| https://github.com/QwenLM/Qwen3-TTS | QwenLM/Qwen3-TTS | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base | Qwen/Qwen3-TTS-12Hz-1.7B-Base | 2026-09-05 |
| https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF | ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:qwen3-tts`, Thread `qwen3-tts-release-and-distribution`, 2 datierte Ereignisse 2025-09-23 → 2026-08-06.
- **Praxishinweis:** Ab 2025-09-23 sollten Praktiker, die Qwen3-TTS evaluieren, mit der verlinkten offiziellen Demo und der Qwen-TTS-Dokumentation beginnen; ab 2026-08-06 können Praktiker, die ein lokales Deployment anstreben, zusätzlich das verlinkte GGUF-Distributionspaket evaluieren.
- **Konfidenz:** hoch. Die datierten Abschnitte „Abgelöst durch“ sind maßgeblich dafür, was veraltet ist.
