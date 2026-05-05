# Automated Video Production and Post-Production Toolkits

Modern video production workflows utilize AI-driven toolkits to automate scene generation, editing, and platform-specific exports. These systems integrate programmatic video frameworks with LLM-based directing and generative media tools.

## AI-Integrated Production Frameworks
Comprehensive toolkits allow for end-to-end automation from storyboard to final render.

### Multi-Skill Video Toolkits
Advanced production suites integrate several specialized libraries for complex media tasks:
- **Core Frameworks:** Integration with Remotion (React-based video), FFmpeg (encoding), and Playwright (automated screen recording).
- **Generative Media:** Support for LTX-2 (text-to-video), FLUX.2 (image generation), and SadTalker (AI talking heads).
- **Audio Synthesis:** ElevenLabs or Qwen3-TTS for voiceovers, and generative music via ACE-Step.
- **Transitions:** Custom GLSL-based effects including RGB split, glitch, zoom blur, and pixelate.

### Zero-Dependency Pipelines
Lightweight pipelines prioritize stability by using only standard utilities like FFmpeg and Whisper:
1. **Silence Removal:** Truncating pauses >0.5s to a natural 0.3s cadence.
2. **Transcription:** Timed transcription using OpenAI Whisper.
3. **Editorial Logic:** Classifying segments as normal, emphasis, or critical to drive visual changes.
4. **Dynamic Scaling:** Using OpenCV face detection to apply a 1.25x zoom on emphasized speech segments.
5. **Audio Mastering:** Highpass filtering followed by EQ, compression, and loudness normalization.

## Specialized Editing and Generative Workflows
Dedicated tools handle transcription cleanup, rough-cuts, and advanced generative lip-syncing.

### Transcription and Rough-Cut Automation
- **Refinement:** Deepgram Nova-2 combined with LLM processing for cleaned, speaker-identified transcripts.
- **NLE Export:** AI-generated rough-cuts can be exported as FCPXML for professional refinement in Final Cut Pro, Adobe Premiere, or DaVinci Resolve.
- **Analysis:** Frame extraction coupled with AI vision models allows for timestamped video summaries and scene-boundary detection.

### Generative Video Pipelines
- **High Resolution:** Support for LTX-2.3 4K video generation and Wan 2.6 for high-fidelity lip-syncing.
- **ComfyUI Integration:** Expert nodes for AnimateDiff and 4K upscaling within the ComfyUI ecosystem.

## Platform Export Specifications (2026)
Encoding parameters vary by platform to ensure optimal bitrate and playback compatibility.

### Social Media Presets
Universal requirements include MP4 container, H.264 codec, AAC-LC audio, and `yuv420p` pixel format.

| Platform | Resolution | Aspect Ratio | Target Bitrate |
| :--- | :--- | :--- | :--- |
| YouTube (4K) | 3840x2160 | 16:9 | 35-45 Mbps |
| Instagram Reels | 1080x1920 | 9:16 | 3500-4500 kbps |
| TikTok | 1080x1920 | 9:16 | 8000-12000 kbps |
| YouTube Shorts | 1080x1920 | 9:16 | 8-12 Mbps |

### Remotion Quality Settings
CRF (Constant Rate Factor) values determine the tradeoff between file size and visual fidelity:
- **High Master:** CRF 18 (final delivery).
- **Web Preview:** CRF 28 (rapid iteration).
- **Intermediates:** Apple ProRes (for further editing).

## Technical Implementation Snippets

### Automated Audio Mastering (FFmpeg)
```bash
ffmpeg -i input.wav -af \
"highpass=f=100, \
equalizer=f=1000:width_type=q:width=1:g=2, \
compand=attacks=0:points=-80/-80|-40/-15|-20/-10|0/-7, \
loudnorm=I=-16:TP=-1.5:LRA=11" \
output_mastered.wav
```

### Remotion Export via CLI
```bash
npx remotion render src/index.ts Main output.mp4 \
  --props='{"title": "Automated Title"}' \
  --codec=h264 \
  --crf=18
```

## Gotchas
- **Issue:** AI models frequently generate invalid syntax for complex FFmpeg `filter_complex` graphs. **Fix:** Chain simple filters sequentially or break the process into multiple render passes.
- **Issue:** Total silence removal (0s duration) sounds unnatural and "clipped." **Fix:** Configure thresholds to maintain a 0.3s minimum duration for natural breathing and cadence.
- **Issue:** Automated reformatting (e.g., 16:9 to 9:16) often crops the subject's head. **Fix:** Use OpenCV face tracking to dynamically adjust the crop center or focal point per frame.
- **Issue:** High CRF values (30+) in generative video cause severe macroblocking. **Fix:** Keep CRF below 22 for generative content, as AI-generated textures are highly sensitive to compression artifacts.

## See Also
- [[technical-article-structure]]
- [[publishing-platforms]]
- [[llm-writing-antipatterns]]
- [[natural-writing-style]]

