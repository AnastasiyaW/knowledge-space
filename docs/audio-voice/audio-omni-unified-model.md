# Audio-Omni: Unified Audio Understanding, Generation, and Editing

Single model for audio understanding, generation, and editing via frozen LLM reasoning + trainable Diffusion Transformer synthesis. [arxiv 2604.10708] SIGGRAPH 2026.

## Architecture

Two-component design: a frozen multimodal LLM handles reasoning and conditioning; a trainable DiT handles high-fidelity audio synthesis.

```text
Text / Audio / Video input
         ↓
  ┌─────────────────────────────────────┐
  │  FROZEN Qwen2.5-Omni (multimodal)   │  ← reasoning, context, knowledge
  │  - Audio encoder                    │
  │  - Text encoder                     │
  │  - Cross-modal reasoning            │
  └─────────────────────────────────────┘
         ↓  semantic conditioning
  ┌─────────────────────────────────────┐
  │  TRAINABLE Diffusion Transformer    │  ← high-fidelity synthesis
  │  - Audio latent diffusion           │
  │  - Conditioned on LLM embeddings    │
  └─────────────────────────────────────┘
         ↓
  Generated / edited audio
```

**Why freeze the LLM:** preserves general knowledge, reduces training compute, enables zero-shot adaptation via prompting rather than per-task fine-tuning.

Video-to-audio tasks use an additional Synchformer checkpoint for visual-audio temporal alignment.

## Capabilities

### Understanding
- Audio captioning and QA
- Speech analysis: gender, speaker count, sarcasm detection
- Sound classification and source identification
- Background scene recognition

### Generation
- Text-to-Audio (environmental sounds, foley)
- Text-to-Music (from video or text)
- Video-to-Audio
- Video-to-Music (soundtrack)
- Text-to-Speech
- Zero-shot voice conversion

### Editing (word/segment level)
Audio editing is the differentiating capability — no comparable open model provides all four operations:

```python
# Add a sound element to existing audio
model.edit("Add", "input.wav", desc="skateboarding sounds")

# Remove a specific element
model.edit("Remove", "input.mp3", desc="female singing")

# Extract a specific element
model.edit("Extract", "input.wav", desc="piano melody")

# Apply style transfer
model.edit("Style", "input.wav", desc="lo-fi hip hop")

# Replace a word/phrase in speech
model.edit("Speech", "input.wav", desc="replace 'hello' with 'goodbye'")
```

## Technical Specs

| Parameter | Value |
|---|---|
| Base LLM | Qwen2.5-Omni (frozen) |
| Checkpoint size | ~21 GB |
| Estimated parameters | ~8–14B (bf16) |
| License | **CC-BY-NC-4.0** (non-commercial) |
| Languages | EN, CN, JA, FR, DE |
| Russian | Not supported |
| VRAM (inference) | 24 GB minimum; 40+ GB recommended |
| Python | 3.11 |
| Reference audio (voice cloning) | Zero-shot (no minimum length specified) |
| Fine-tune / LoRA recipe | Not provided |
| Commercial license | On request only |

## Training Data

**AudioEdit** dataset: 1M+ curated editing pairs created specifically for audio editing tasks. Availability as a standalone open dataset is unconfirmed at time of writing. If released, it would be valuable for training editing capabilities on top of commercially-licensed TTS bases.

## Comparison: Audio-Omni vs Specialized TTS

| Aspect | Audio-Omni | VoxCPM2 | OmniVoice | Fish S2 Pro |
|---|---|---|---|---|
| Architecture | Frozen LLM + DiT | Tokenizer-free diffusion-AR | Attention-based | Dual-AR + RLHF |
| Parameters | ~8–14B | 2B | Not disclosed | 4.4B |
| Languages | 5 | 30+ | 600+ | 80+ |
| Russian | No | Yes | Yes | Yes |
| Voice cloning | Zero-shot | Zero-shot + fine-tune | Zero-shot cross-lang | 10–30s ref |
| Word-level editing | **Yes** | No | No | No |
| Audio understanding | **Yes** | No | No | No |
| Fine-tune / LoRA | No recipe | Yes | Unclear | Yes |
| License | CC-BY-NC-4.0 | Apache 2.0 | Open | Open weights |
| Commercial use | No (without agreement) | Yes | Yes | Yes |

Audio-Omni trades language coverage and commercial usability for breadth of capabilities. Specialized TTS models outperform it on single-language TTS quality and multilingual support.

## Architectural Pattern: Frozen Reasoning + Trainable Synthesis

This design pattern — shared frozen LLM as reasoning backbone over a trainable synthesis module — generalizes beyond this model:

- New tasks = new prompts to the frozen LLM, not retraining
- Reasoning and generation can be updated independently
- The frozen LLM provides grounded pedagogical feedback (e.g., explaining phoneme-level errors in speech)

**Word-level speech editing implementation alternatives** (for commercially-licensed systems):
1. Diffusion-based inpainting with a prompt (requires diffusion architecture like VoxCPM2)
2. Phoneme alignment + AudioSep extraction → TTS inpaint in target voice → re-splice
3. Train editing LoRA on open-commercial base using AudioEdit dataset (if released)

## Unified API Pattern

```python
# Demonstrates clean interface separation between tasks
model.understand("transcribe", audio_path)          # understanding
model.generate("tts", text="Hello world", ref=ref_audio)  # generation
model.edit("Add", audio_path, desc="rain sounds")  # editing
```

This three-namespace API design (understand / generate / edit) cleanly separates intent and is worth replicating in audio worker services.

## Gotchas

- **Issue:** 21 GB checkpoint requires 24+ GB VRAM for inference → **Fix:** Use A100 80GB or H100; consumer 24 GB cards (RTX 4090/3090) are at the absolute limit with no headroom for batching
- **Issue:** CC-BY-NC-4.0 blocks commercial use → **Fix:** Contact authors for commercial licensing (`ztianad@connect.ust.hk`); for production commercial systems, use Apache 2.0 alternatives (VoxCPM2, Fish S2 Pro)
- **Issue:** No Russian language support despite 600-language alternatives existing → **Fix:** For RU production, use OmniVoice (600+ langs) or Fish S2 Pro with fine-tuning
- **Issue:** No LoRA / fine-tune recipe provided → **Fix:** Cannot adapt to custom voices or domains without implementing custom training pipeline; specialized models (Fish S2 Pro, VoxCPM2) offer documented fine-tune paths

## See Also

- [[tts-models]]
- [[voice-cloning]]
- [[voice-conversion]]
