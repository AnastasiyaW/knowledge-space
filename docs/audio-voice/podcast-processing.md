---
title: Podcast Processing
category: patterns
tags: [podcast, diarization, transcription, speaker-separation, editing, sommelier, nemo]
---

# Podcast Processing

End-to-end podcast processing pipelines handle speaker diarization (who spoke when), transcription, music/noise removal, and structured output generation. The Sommelier pipeline demonstrates a modern open-source approach combining multiple specialized models.

## Key Facts

- Speaker diarization identifies and labels distinct speakers in multi-speaker audio
- Modern diarization uses neural speaker embeddings + clustering (spectral, agglomerative, or NME-SC)
- Sommelier pipeline combines: NeMo Sortformer (diarization) + Whisper/Parakeet (ASR) + Canary (translation)
- Source separation (Demucs, UVR5) isolates vocals from music/noise before transcription
- pyannote.audio is the most popular open-source diarization framework
- Typical podcast pipeline: separate sources -> diarize -> transcribe -> align -> format

## Full Processing Pipeline

```text
Raw podcast audio (mixed speakers, music, ads)
  |
  v
1. Source Separation (Demucs / UVR5)
   -> vocals_track.wav (speech only)
   -> music_track.wav (background music, jingles)
   -> noise_track.wav (ambient noise)
  |
  v
2. Voice Activity Detection (Silero VAD / pyannote VAD)
   -> speech segments with timestamps
   -> silence regions marked for potential cuts
  |
  v
3. Speaker Diarization (pyannote / NeMo Sortformer)
   -> speaker labels: Speaker_A [0:00-0:15], Speaker_B [0:15-0:32], ...
   -> overlap regions detected
  |
  v
4. ASR Transcription (Whisper / Parakeet)
   -> text aligned to speaker segments
   -> word-level timestamps via forced alignment
  |
  v
5. Post-Processing
   -> Merge same-speaker consecutive segments
   -> Remove filler words (configurable)
   -> Generate: SRT subtitles, JSON transcript, show notes
```

## Speaker Diarization

### pyannote.audio Pipeline

```python
from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="HF_TOKEN"
)

diarization = pipeline("podcast.wav", num_speakers=2)  # or min/max_speakers

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"[{turn.start:.1f}s - {turn.end:.1f}s] {speaker}")
```

### NeMo Sortformer

```text
NeMo Sortformer (used in Sommelier):
  - Sort-based diarization: predicts speaker order, not just clusters
  - Handles overlapping speech better than clustering approaches
  - Integrates with NeMo ASR models for joint optimization
  - Scales to 10+ speakers without predefined count
```

## Sommelier Pipeline

Open-source podcast processing combining best-in-class models.

```text
Sommelier components:
  1. Source separation - remove music/jingles from speech
  2. NeMo Sortformer - speaker diarization with overlap handling
  3. Whisper / Parakeet - transcription (Parakeet for EN, Whisper for multilingual)
  4. Canary - optional translation to other languages
  5. Post-processor - format output as transcript with speaker labels

Key advantage: each component is replaceable. 
Swap Whisper for Parakeet for better English WER.
Swap pyannote for Sortformer for better overlap handling.
```

## Source Separation

```text
Models for vocal isolation:
  Demucs (Meta) - 4-stem separation (vocals, drums, bass, other)
  UVR5 - multiple architectures, strong vocal isolation
  MDX-Net - competitive with Demucs, different architecture
  
For podcasts, only vocal stem is needed.
Run before ASR to remove background music/jingles.
```

## Output Formats

### SRT Subtitles with Speakers

```text
1
00:00:01,200 --> 00:00:04,800
[Host] Welcome to the show. Today we're 
talking about machine learning.

2
00:00:05,100 --> 00:00:08,900
[Guest] Thanks for having me. I've been 
working on transformer architectures.
```

### Structured JSON Transcript

```json
{
  "speakers": ["Host", "Guest"],
  "segments": [
    {
      "speaker": "Host",
      "start": 1.2,
      "end": 4.8,
      "text": "Welcome to the show. Today we're talking about machine learning.",
      "words": [
        {"word": "Welcome", "start": 1.2, "end": 1.6, "confidence": 0.98},
        {"word": "to", "start": 1.6, "end": 1.7, "confidence": 0.99}
      ]
    }
  ],
  "metadata": {
    "duration": 3600.0,
    "language": "en",
    "num_speakers": 2
  }
}
```

## Editing Pipeline

After transcription, text-based editing allows cutting audio by editing text:

```text
Text-based audio editing workflow:
  1. Transcribe with word-level timestamps
  2. Display transcript in editor UI
  3. User deletes/rearranges text
  4. Map text edits back to audio timestamps
  5. Apply non-destructive audio cuts
  6. Crossfade at edit points (10-50ms) to avoid clicks
  
Tools: Descript (commercial), audapolis (open source)
```

## Gotchas

- **Diarization fails on similar voices** - when two speakers have similar vocal characteristics (same gender, age, accent), clustering-based diarization frequently merges them into one speaker. Providing `num_speakers` explicitly or using NeMo Sortformer (order-based, not clustering-based) helps significantly
- **Source separation introduces artifacts in speech** - Demucs vocal isolation can create slight metallic coloring in speech. For ASR-only pipelines, this is acceptable (WER stays similar). For published audio, apply light equalization after separation
- **Overlapping speech destroys transcription accuracy** - when two speakers talk simultaneously, ASR accuracy drops to 30-50%. Detect overlaps in diarization, flag them in output, and consider separate channel recording for critical content

## See Also

- [[speech-recognition]] - ASR models and Whisper usage details
- [[voice-cloning]] - reference audio preparation techniques overlap with podcast preprocessing
- [[audio-generation]] - music generation for podcast intros/outros
