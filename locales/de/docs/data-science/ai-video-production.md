---
title: "KI-gestützte Videoproduktion"
category: applications
tags: [data-science, generative-ai, video, production, tools]
level: 2
source_sha256: 37aaa4559931fe6bdacda7e32233050bd3a6e3a88f33aa370152a10e6ccedceb
translation: machine
translated_at: '2026-10-24'
---
# KI-gestützte Videoproduktion {#ai-powered-video-production}

Durchgängige Pipeline zur Erstellung kommerzieller Videos mit KI-Werkzeugen. Verkettet LLM-basiertes Scripting, Bildgenerierung, Videosynthese und Audiogenerierung.

## Werkzeugkette {#tool-chain}

| Tool | Rolle | Ideal für |
|------|-------|-----------|
| GPT-5 | Skript, Prompts, Iteration | Ein Projekt pro Video, ein Chat pro Sitzung |
| Seedream 4 | Bildgenerierung von Grund auf | Fotorealistische Personen/Szenen |
| NanoBanana Pro | Bearbeitung/Stilisierung bestehender Frames | Referenzreproduktion, Erhalt der Geometrie |
| Kling 2.5 | Videogenerierung | Entwurf in 720p (kostenlos), finale Fassung in 1080p |
| ElevenLabs | Sprachgenerierung | Voiceover, Figurenstimmen |
| Suno | Musikgenerierung | Hintergrundmusik |

## Pipeline-Stufen {#pipeline-stages}

### 1. Skript & Storyboard {#1-script-storyboard}
- GPT mit Konzept, Figuren, Schauplatz und visuellen Referenzen briefen
- In ca. 6 Szenen mit insgesamt ca. 25 Sekunden gliedern
- Einstellungsarten zuweisen: Totale / Halbnah / Nah / Detail
- Dieselbe Einstellungsart nie zweimal hintereinander verwenden
- KI-Einschränkungen berücksichtigen: Gesichter in Weitaufnahmen werden schlecht gerendert

### 2. Generierung der Standbilder {#2-still-frame-generation}
- Seedream: Stil „Fashion Photo“, 16:9, Unlimited Mode
- „AI Prompt / Improve short prompts“ deaktivieren
- Zuerst ohne Referenzen generieren, dann mit Referenzen verfeinern
- Geometrieerhaltende Korrekturen mit NanoBanana bearbeiten

### 3. Entwurfs-Animatic {#3-draft-animatic}
- Kling 2.5 in 720p Unlimited (0 Credits) zum Testen
- Prüfen: Bewegungsgeschwindigkeit, Proportionen, Konsistenz des Hintergrunds
- Korrektur durch erneute Generierung mit verfeinerten Prompts

### 4. Aufbau der Video-Prompts {#4-video-prompt-structure}
```text
1. Scene description: "wide shot of a lone man walking..."
2. Character movement: "takes 2-3 small steps then stops"
3. Camera movement: "camera slowly dollies forward, no shaking"
4. Atmosphere: "cold, dramatic grading, blue haze"
5. Negative: "no extra limbs, no face blur, no acid colors"
```

### 5. Audio & Lipsync {#5-audio-lipsync}
- ElevenLabs zur Erzeugung der Voiceovers
- Lipsync in Higgsfield (Abgleich von Video und Audio)
- Englischer Lipsync ist stabiler als in anderen Sprachen
- Dauerabgleich ist entscheidend: Video und Audio müssen übereinstimmen

## Seedream vs. NanoBanana {#seedream-vs-nanobanana}

| Aspekt | Seedream 4 | NanoBanana Pro |
|--------|-----------|----------------|
| Von Grund auf | Ausgezeichnet | Gut |
| Referenzreproduktion | Schwach | Ausgezeichnet |
| Nahaufnahmen-Details | Kontrastreich, hart | Weich, realistisch |
| Text/Branding | Schwach | Deutlich besser |

## Credit-Verwaltung {#credit-management}
- Alle Standbilder und Experimente: Unlimited-Modus (kostenlos)
- Entwurfsvideos: 720p Unlimited (0 Credits)
- Nur finale Generierung: 1080p (500 Credits/Generierung, 3–5 Versuche pro Szene)

## Stolperfallen {#gotchas}
- Lange, „poetische“ Prompts verwirren Videomodelle – knapp strukturiert und konkret halten
- Kamerabewegung immer angeben (Standard = zufälliges „Fliegen“)
- Weit von der Kamera entfernt = schlechtere Gesichtsqualität – separate Ganzkörperreferenz verwenden
- Farbgestaltung: GPTs Standardvorgabe „Golden Hour“ für dramatische Looks überschreiben
- Zähne/Zunge/Mund = Hauptzone für Artefakte beim Lipsync

## Siehe auch {#see-also}
- [[generative-models]] – zugrunde liegende Generierungstechnologie
- [[nlp-text-processing]] – Prompt-Engineering
