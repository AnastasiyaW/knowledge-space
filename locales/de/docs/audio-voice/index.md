---
title: "Audio & Stimme"
description: "Spracherkennung, Text-to-Speech, Voice Cloning und Voice-Agent-Pipelines: Modellvergleiche, Latenz-Benchmarks und Integrationsmuster für den Produktivbetrieb."
type: MOC
level: 2
source_sha256: 2da8cd2ffe7b18c38fe935ad2667933a39ebbd983382de863a5aa5d05e815c44
translation: machine
translated_at: '2026-10-24'
---
# Audio & Stimme {#audio-voice}

Moderne Sprachsysteme umfassen drei Kernbereiche: die Erkennung gesprochener Sprache (ASR), die Synthese von Stimmen (TTS) sowie die Umwandlung oder das Klonen einer Sprecheridentität. Die Artikel hier behandeln aktuelle Modellfamilien (Whisper, Qwen3-ASR, NVIDIA Canary, F5-TTS, CosyVoice), Latenzbudgets für Echtzeit-Voice-Agents, Fine-Tuning-Infrastruktur auf gemieteten GPUs sowie Kompromisse beim mehrsprachigen Deployment. Jeder Beitrag ist eine dichte Referenz mit Architekturdiagrammen, Befehlen, Benchmarks und Integrationsfallen, keine Tutorials.

## Sprache & Erkennung {#speech-recognition}
- [[speech-recognition]] - ASR-Modelle, Transkription, Aussprachebewertung

## Text-to-Speech {#text-to-speech}
- [[tts-models]] - Vergleich von TTS-Modellen, Latenz-Benchmarks, mehrsprachige Unterstützung
- [[voice-cloning]] - Voice Cloning, Stimmmischung, Natürlichkeits-Benchmarks
- [[voice-conversion]] - Techniken und Pipelines für Voice Conversion
- [[audio-generation]] - Modelle und Workflows zur Audiogenerierung
- [[audio-flamingo]] - Audio Flamingo 3, Music Flamingo und die Verständnis-Artefakte von AF-Next
- [[ace-step-1-5]] - ACE-Step 1.5 Base/SFT/Turbo und Hardware-Grenzen von XL

## Voice-Anwendungen {#voice-applications}
- [[voice-agent-pipelines]] - Voice-Agent-Pipelines und Frameworks für Echtzeitanwendungen
- [[podcast-processing]] - Podcast-Verarbeitung, Transkription und Analyse

## Weitere Referenzen {#additional-references}

- [[asr-stt-compression]] - KV-Cache-Kompressionsverfahren für die ASR/TTS-Inferenz und LLM-Kontext im Jahr 2026: TriAttention
- [[audio-omni-unified-model]] - Ein einziges Modell für Audioverständnis, -generierung und -bearbeitung durch eingefrorenes LLM-Reasoning + trainierbare
- [[lemas-tts-and-speech-editing]] - LEMAS, quelloffene mehrsprachige TTS- und Wortebenen-Sprachbearbeitungsmodelle: Architektur
- [[tts-fine-tuning-infrastructure]] - Vergleich von GPU-Mietplattformen und Deployment-Muster für Fine-Tuning und Serving von 2B-4B-TTS-Modellen
- [[voice-design]] - Erzeugung einzigartiger synthetischer Stimmen aus Textbeschreibungen, Stimm-Morphing, Natürlichkeits-Benchmarks
