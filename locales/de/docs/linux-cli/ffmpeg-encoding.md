---
title: "FFmpeg-Video- und Audiokodierung"
category: reference
tags: [linux-cli, ffmpeg, encoding, video, audio, nvenc, av1, h264, hevc]
level: 3
source_sha256: a6c11ff093bf53878c34792b9533bccdad74c73e8c32bce30a7d103f839f2670
translation: machine
translated_at: '2026-10-24'
---
# FFmpeg-Video- und Audiokodierung {#ffmpeg-video-and-audio-encoding}

CLI-Medienencoder. Behandelt Codec-Auswahl, NVENC-Hardwarebeschleunigung, Audiokodierung, Tempoänderung mit Formant-Erhalt und Schnellpfade für Concat. FFmpeg 7.x, NVENC Turing+.

## Wichtige Fakten {#key-facts}

- `-vsync` ist in FFmpeg 6+ veraltet; stattdessen `-fps_mode cfr` oder `-fps_mode vfr` verwenden
- `libfaac` wurde entfernt; native `aac` oder über [[package-management]] installiertes `libfdk_aac` verwenden
- `-rc constqp -qp X` funktioniert weiterhin, aber `-rc vbr -cq X -b:v 0` ist das empfohlene NVENC-Muster
- `-preset slow` für NVENC ist entfallen; numerische `-preset p5/p6/p7` verwenden (p7 = langsamst/beste Qualität)
- `-tag:v hvc1` ist für HEVC in MP4 erforderlich, wenn Apple QuickTime/Safari adressiert werden; der Standardwert `hev1` schlägt fehl
- NVENC Turing+ (RTX 2000+) ist für `spatial-aq`/`temporal-aq` erforderlich; Ada (RTX 4000+) für `av1_nvenc`
- Die Rubber-Band-R3-Engine erfordert die eigenständige CLI von breakfastquay.com; der eingebaute `af_rubberband`-Filter von ffmpeg verwendet die ältere R2-Engine
- `yuv420p` ist für die Kompatibilität mit Hardware-Decodern (Telefone, Fernseher, Embedded-Geräte) zwingend; `yuv420p10le` nur für Archivierung
- `-movflags +faststart` verschiebt das moov-Atom an den Dateianfang – erforderlich für HTTP-Streaming und Spulen vor dem vollständigen Download

## Codec-Auswahl {#codec-selection}

| Codec | Encoder | Geschwindigkeit (1080p, RTX 4090) | Qualität/Bit | Kompatibilität 2026 | Verwendung, wenn |
|---|---|---|---|---|---|
| H.264 | `libx264 -preset slow` | ~0,5x Echtzeit | Am besten | Universell | Archiv-Master, kleine Stapel |
| H.264 | `h264_nvenc -preset p6` | ~10x Echtzeit | Gut (mit AQ) | Universell | Massenstapel, Verteilung |
| HEVC | `libx265 -preset slow` | ~0,3x Echtzeit | Ausgezeichnet | Breit (nicht WMP ohne Codec) | Archiv-Master, 30–50 % kleiner als H.264 |
| HEVC | `hevc_nvenc -preset p6` | ~8x Echtzeit | Sehr gut (mit `tune hq`) | Breit | HEVC-Massenkodierung |
| AV1 | `libsvtav1 -preset 6` | ~0,5x Echtzeit | Bestes CPU-AV1 | Eingeschränkt (neue Geräte) | zukunftssicheres Archiv |
| AV1 | `av1_nvenc -preset p6` | ~8x Echtzeit | Gut | Eingeschränkt | GPU-Geschwindigkeit bei knappem Speicher |

**CRF/CQ-Äquivalenz (wenig Bewegung: Folien, Bildschirmaufnahmen, Sprechkopf):**

| Ziel | libx264 CRF | libx265 CRF | SVT-AV1 CRF | h264_nvenc CQ | hevc_nvenc CQ |
|---|---|---|---|---|---|
| Visuell verlustfrei | 18 | 16 | 20 | 18 | 18 |
| Optimum für Verteilung | 22–23 | 22 | 28–32 | 24–25 | 26 |
| Aggressiv (auf Textartefakte achten) | 28+ | 26+ | 36+ | 28+ | 30+ |

Inhalte mit wenig Bewegung (Vorlesungen, Screencasts, Folien) vertragen einen um 2–3 höheren CRF-Wert als allgemeines Video – statische Bereiche profitieren mehr von AQ als von zusätzlicher Bitrate.

**Skalierungsalgorithmus:**

| Algorithmus | Qualität | Geschwindigkeit | Verwendung, wenn |
|---|---|---|---|
| `lanczos` | Beste Detailtreue, leichtes Ringing an Textkanten | Langsam | Fotografische Inhalte, Sprechkopf |
| `bicubic` | Gut, weniger Ringing | Schnell | Bildschirmaufnahmen, textlastige Folien |
| `bilinear` | Am schlechtesten | Am schnellsten | Niemals für Archivierung |

## Befehlsrezepte {#command-recipes}

### Stream-Kopie (Container-Neuverpackung, kein Qualitätsverlust) {#stream-copy-container-repack-no-quality-loss}

```bash
# MKV → MP4 repack, no re-encode
ffmpeg -i input.mkv -c copy -movflags +faststart output.mp4
```

### libx264-Archiv-Master {#libx264-archival-master}

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -preset slow -crf 20 \
  -profile:v high -level 4.1 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### h264_nvenc-Massenstapel (Turing+) {#h264_nvenc-bulk-batch-turing}

```bash
ffmpeg -i input.mp4 \
  -c:v h264_nvenc -preset p6 -tune hq \
  -rc vbr -cq 24 -b:v 0 -maxrate 6M -bufsize 12M \
  -bf 2 -spatial-aq 1 -temporal-aq 1 -rc-lookahead 32 \
  -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

`-bf 2`: B-Frames für bessere Kompression bei wenig Bewegung (NVENC steht möglicherweise standardmäßig auf 0).  
`-rc-lookahead 32`: 32-Frame-Puffer für bessere Ratensteuerung; höhere Werte bringen abnehmenden Nutzen.  
`-multipass fullres`: bringt ca. +10–15 % Qualität bei doppelter Kodierzeit – lohnt sich für Archivierung, für Massenstapel überspringen.

### HEVC-Archiv (libx265, 10-Bit für Folien-/Textinhalte) {#hevc-archival-libx265-10-bit-for-slidetext-content}

```bash
ffmpeg -i input.mp4 \
  -c:v libx265 -preset slow -crf 22 \
  -pix_fmt yuv420p10le -tag:v hvc1 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

10-Bit reduziert Posterisierung und Banding bei Verläufen in Folien; das Tag `hvc1` ist für die Apple-Kompatibilität erforderlich.

### hevc_nvenc-Massenkodierung {#hevc_nvenc-bulk}

```bash
ffmpeg -i input.mp4 \
  -c:v hevc_nvenc -preset p6 -tune hq \
  -rc vbr -cq 26 -b:v 0 \
  -spatial-aq 1 -temporal-aq 1 -rc-lookahead 32 \
  -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### SVT-AV1 CPU (gegenüber libaom-av1 empfohlen) {#svt-av1-cpu-recommended-over-libaom-av1}

```bash
ffmpeg -i input.mp4 \
  -c:v libsvtav1 -preset 6 -crf 28 \
  -svtav1-params tune=0:lookahead=120 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

`tune=0`: VOD-Qualitätsmodus. `lookahead=120`: großer Lookahead für Qualität; für Geschwindigkeit auf 32 reduzieren.

### av1_nvenc (Ada, RTX 4000+) {#av1_nvenc-ada-rtx-4000}

```bash
ffmpeg -i input.mp4 \
  -c:v av1_nvenc -preset p6 -tune hq \
  -rc vbr -cq 30 -b:v 0 \
  -spatial-aq 1 -temporal-aq 1 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### Auflösungsverkleinerung (4K → 1080p) {#resolution-downscale-4k-1080p}

```bash
# Photographic / talking head — lanczos
ffmpeg -i input.mp4 -vf "scale=1920:-2:flags=lanczos" -c:v h264_nvenc ... output.mp4

# Screen recording / text slides — bicubic (less ringing)
ffmpeg -i input.mp4 -vf "scale=1920:-2:flags=bicubic" -c:v h264_nvenc ... output.mp4
```

`-2`: berechnet die Höhe automatisch unter Beibehaltung des Seitenverhältnisses; sorgt für eine gerade Zahl, die H.264 voraussetzt.

### Audio: AAC für Sprache {#audio-aac-for-voice}

```bash
# Native AAC (universal builds) — adequate at 128k
-c:a aac -b:a 128k -ac 1 -ar 48000

# libfdk_aac (Fraunhofer, better quality especially <128k; requires non-free build)
-c:a libfdk_aac -b:a 96k -ac 1 -ar 48000 -afterburner 1

# Verify libfdk_aac availability
ffmpeg -encoders | grep fdk
```

AAC-Bitraten-Richtwerte für monophone Sprache: 64k = für Streaming akzeptabel, 96k = Minimum für Verteilung, 128k = Optimum für Archivierung, 160k+ = abnehmender Nutzen.  
HE-AAC (`-profile:a aac_he`) ist unterhalb von 64k besser, wird aber von Playern schlechter unterstützt; für Kompatibilität LC-AAC verwenden.

### Tempoänderung bei Sprache mit Formant-Erhalt (Rubber Band R3) {#speech-tempo-change-with-formant-preservation-rubber-band-r3}

Dreistufige Pipeline – Audio extrahieren, R3-Streckung, mit beschleunigtem Video neu muxen:

```bash
# Pass 1: extract audio as lossless WAV
ffmpeg -y -i src.mp4 -vn -c:a pcm_s16le -ar 44100 -ac 1 audio.wav

# Pass 2: R3 time-stretch with formant preservation (-F mandatory for 3x speech)
rubberband-r3 -T 3 -F -q audio.wav audio_3x.wav
# -T 3   : 3x tempo (duration = original / 3)
# -F     : formant preserve — prevents gender-shift on extreme ratios
# -q     : quiet mode for batch

# Pass 3a: speed video only (no audio, use NVENC + AQ)
ffmpeg -y -i src.mp4 -an \
  -filter:v "setpts=PTS/3.0" \
  -c:v h264_nvenc -preset p6 -tune hq -cq 24 \
  -bf 2 -spatial-aq 1 -temporal-aq 1 \
  -movflags +faststart video_3x.mp4

# Pass 3b: mux speed-up video + R3 audio
ffmpeg -y -i video_3x.mp4 -i audio_3x.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy \
  -c:a aac -b:a 128k -ac 1 \
  -shortest \
  -movflags +faststart final_3x.mp4
```

`-shortest` gleicht die Stream-Dauern an – erforderlich, wenn Video- und Audiolänge nach der Streckung um Millisekunden abweichen.

### Concat: Schnellpfad (ohne Neukodierung) {#concat-fast-path-no-re-encode}

Alle Clips müssen identische Codec-, Auflösungs-, Bildraten-, Pixelformat- und Audioparameter aufweisen:

```bash
# Build list file
printf "file '%s'\n" part1.mp4 part2.mp4 part3.mp4 > list.txt

# Demuxer concat — ~37x faster than re-encode
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# With regenerated timestamps (for speed-up outputs or AVI/MKV rips with corrupt PTS)
ffmpeg -fflags +genpts -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Concat: Filterpfad (Neukodierung, gemischte Parameter) {#concat-filter-path-re-encode-mixed-params}

```bash
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v h264_nvenc -preset p6 -tune hq -cq 24 \
  -c:a aac -b:a 128k -ac 1 \
  -movflags +faststart output.mp4
```

Verwenden, wenn sich Clips in einem beliebigen Parameter unterscheiden; langsamer, verarbeitet aber jede Eingabekombination.

## NVENC-Tuning-Referenz {#nvenc-tuning-reference}

| Flag | Werte | Wirkung |
|---|---|---|
| `-preset` | `p4` (überspringen), `p5` Massen, `p6` Qualität, `p7` Archiv | Geschwindigkeits-/Qualitätsabwägung; p7 ist immer noch schneller als libx264 medium |
| `-tune` | `hq` (immer für Qualität verwenden), `ll`/`ull` (nur Latenz) | `hq` ist zwingend – der Standardwert liefert deutlich geringere Qualität |
| `-spatial-aq 1` | 0/1 | Mehr Bits in komplexen räumlichen Bereichen, weniger in flachen – entscheidend für Folien |
| `-temporal-aq 1` | 0/1 | Mehr Bits in statischen Bildern (Gesicht), weniger bei Bewegung – entscheidend für Sprechkopf |
| `-rc-lookahead` | 32 (empfohlen), 64 (abnehmender Nutzen) | Framepuffer für Ratensteuerungsentscheidungen |
| `-bf` | 2–3 | B-Frames; NVENC steht möglicherweise standardmäßig auf 0, für Vorlesungen/wenig Bewegung explizit setzen |
| `-multipass fullres` | (Flag) | Zweipass bei voller Auflösung: +10–15 % Qualität, doppelte Zeit; NVENC SDK 12+, nur für Archivierung |

## Stolperfallen {#gotchas}

- **Problem:** `af_rubberband=tempo=3.0` (eingebauter ffmpeg-Filter) erzeugt metallische/roboterhafte Artefakte bei 3-facher Sprechgeschwindigkeit. **Lösung:** Eigenständige Rubber-Band-R3-CLI verwenden (`rubberband-r3 -T 3 -F`). Der eingebaute Filter nutzt die R2-Engine; selbst mit `formant=preserved` unterliegt R2 bei Sprache und hohen Verhältnissen der R3.

- **Problem:** `-movflags +faststart` fehlt – das Video puffert die gesamte Datei, bevor die Wiedergabe beginnt; Spulen bei HTTP-Streams schlägt fehl. **Lösung:** Bei jeder MP4 zur Verteilung immer `-movflags +faststart` anhängen. Bei lokalen Dateien entstehen keine Nachteile.

- **Problem:** NVENC-Qualität enttäuscht ohne `-tune hq`; der Standard-Tune entspricht einem nicht optimierten Modus. **Lösung:** Für ein Qualitätsziel immer `-tune hq` angeben; ohne dieses Flag bleibt erheblicher Qualitätsspielraum ungenutzt, ohne dass ein Geschwindigkeitsvorteil entsteht.

- **Problem:** Die Ausgabe von `hevc_nvenc` lässt sich in QuickTime/Safari nicht abspielen (`hev1`-Tag wird nicht erkannt). **Lösung:** `-tag:v hvc1` ergänzen, um das richtige Tag zu erzwingen; gilt für jedes HEVC-MP4, das auf Apple-Geräte abzielt.

- **Problem:** `ffmpeg -f concat -c copy` erzeugt Audio-/Video-Synchronisationsdrift, wenn Quelldateien einen von null verschiedenen Start-PTS haben (häufig bei beschleunigten Ausgaben oder MKV-Rips). **Lösung:** `-fflags +genpts` hinzufügen, um Zeitstempel neu zu erzeugen: `ffmpeg -fflags +genpts -f concat -safe 0 -i list.txt -c copy out.mp4`.

- **Problem:** Ein zu niedriger CQ-Wert (aggressiv) bei NVENC erzeugt sichtbare Blockbildung/Ringing an Text und Folienverläufen. **Lösung:** Für 1080p-Vorlesungs-/Folieninhalte CQ 24–26 bei H.264 bzw. CQ 26–28 bei HEVC verwenden. CQ 18 oder darunter ist nahezu verlustfrei, die Dateigröße wächst jedoch exponentiell; für Bildschirminhalte unnötig.

- **Problem:** Die CRF-Skala von `libsvtav1` entspricht nicht der von x264/x265; eine direkte Übertragung des CRF-Werts führt zu stark abweichenden Ergebnissen. **Lösung:** SVT-AV1 CRF 28–32 ≈ x265 CRF 22 ≈ x264 CRF 16–18 für vergleichbare wahrgenommene Qualität bei üblichen Inhalten.

- **Problem:** `atempo=3.0` in einer ffmpeg-Audiofilterkette erzeugt bei 3-facher Geschwindigkeit verständliche, aber qualitativ schlechte Sprache; Phase-Vocoder-Verschmierung ist hörbar. **Lösung:** `atempo` für Sprache nicht über 2x verwenden; stattdessen die eigenständige Rubber-Band-R3-Pipeline nutzen.

## Siehe auch {#see-also}

- [[bash-scripting]] - Batch-Schleifen für Multi-Datei-Kodierjobs
- [[io-redirection-and-pipes]] - Ausgabe von ffmpeg pipen, Kodierfortschritt protokollieren
- [[monitoring-and-performance]] - GPU-Auslastung während der NVENC-Kodierung überwachen (`nvidia-smi dmon`)
- [[disks-and-filesystems]] - Speicherlayout für große Videoarchive
- [FFmpeg Codecs Documentation](https://ffmpeg.org/ffmpeg-codecs.html)
- [FFmpeg Scaler Documentation](https://ffmpeg.org/ffmpeg-scaler.html)
- [FFmpeg Wiki: Encode/AV1](https://trac.ffmpeg.org/wiki/Encode/AV1)
- [FFmpeg Wiki: Encode/AAC](https://trac.ffmpeg.org/wiki/Encode/AAC)
- [Rubber Band Audio Library](https://breakfastquay.com/rubberband/)
- [NVIDIA Video Codec SDK Presets](https://developer.nvidia.com/blog/introducing-video-codec-sdk-10-presets/)
- [SVT-AV1 Preset Analysis — OTTVerse](https://ottverse.com/analysis-of-svt-av1-presets-and-crf-values/)
- [CRF Guide — slhck.info](https://slhck.info/video/2017/02/24/crf-guide.html)
