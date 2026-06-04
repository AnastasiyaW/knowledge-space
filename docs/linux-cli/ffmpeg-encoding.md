---
title: FFmpeg Video and Audio Encoding
category: reference
tags: [linux-cli, ffmpeg, encoding, video, audio, nvenc, av1, h264, hevc]
---

# FFmpeg Video and Audio Encoding

CLI media encoder. Covers codec selection, NVENC hardware acceleration, audio encoding, tempo change with formant preservation, and concat fast paths. FFmpeg 7.x, NVENC Turing+.

## Key Facts

- `-vsync` deprecated in FFmpeg 6+; use `-fps_mode cfr` or `-fps_mode vfr` instead
- `libfaac` removed; use native `aac` or [[package-management]]-installed `libfdk_aac`
- `-rc constqp -qp X` still works but `-rc vbr -cq X -b:v 0` is the recommended NVENC pattern
- `-preset slow` for NVENC is gone; use numeric `-preset p5/p6/p7` (p7 = slowest/best)
- `-tag:v hvc1` required for HEVC in MP4 when targeting Apple QuickTime/Safari; default `hev1` fails
- NVENC Turing+ (RTX 2000+) required for `spatial-aq`/`temporal-aq`; Ada (RTX 4000+) for `av1_nvenc`
- Rubber Band R3 engine requires standalone CLI from breakfastquay.com; ffmpeg's built-in `af_rubberband` uses the older R2 engine
- `yuv420p` mandatory for hardware decoder compatibility (phones, TVs, embedded); `yuv420p10le` archival only
- `-movflags +faststart` moves moov atom to file start — required for HTTP streaming/seeking before full download

## Codec Selection

| Codec | Encoder | Speed (1080p, RTX 4090) | Quality/bit | Compat 2026 | Use when |
|---|---|---|---|---|---|
| H.264 | `libx264 -preset slow` | ~0.5x realtime | Best | Universal | archival master, small batch |
| H.264 | `h264_nvenc -preset p6` | ~10x realtime | Good (with AQ) | Universal | bulk batch, distribution |
| HEVC | `libx265 -preset slow` | ~0.3x realtime | Excellent | Wide (not WMP without codec) | archival master, 30-50% smaller than H.264 |
| HEVC | `hevc_nvenc -preset p6` | ~8x realtime | V.Good (with `tune hq`) | Wide | bulk HEVC encode |
| AV1 | `libsvtav1 -preset 6` | ~0.5x realtime | Best CPU AV1 | Limited (new devices) | future-proof archival |
| AV1 | `av1_nvenc -preset p6` | ~8x realtime | Good | Limited | GPU speed when storage critical |

**CRF/CQ equivalence (low-motion content: slides, screen recording, talking head):**

| Target | libx264 CRF | libx265 CRF | SVT-AV1 CRF | h264_nvenc CQ | hevc_nvenc CQ |
|---|---|---|---|---|---|
| Visually lossless | 18 | 16 | 20 | 18 | 18 |
| Distribution sweet spot | 22-23 | 22 | 28-32 | 24-25 | 26 |
| Aggressive (watch for text artifacts) | 28+ | 26+ | 36+ | 28+ | 30+ |

Low-motion content (lectures, screencasts, slides) tolerates CRF 2-3 higher than general video — static regions benefit more from AQ than extra bitrate.

**Scaler choice:**

| Algorithm | Quality | Speed | Use when |
|---|---|---|---|
| `lanczos` | Best detail, slight ringing on text edges | Slow | Photographic content, talking head |
| `bicubic` | Good, less ringing | Fast | Screen recording, text-heavy slides |
| `bilinear` | Worst | Fastest | Never for archival |

## Command Recipes

### Stream copy (container repack, no quality loss)

```bash
# MKV → MP4 repack, no re-encode
ffmpeg -i input.mkv -c copy -movflags +faststart output.mp4
```

### libx264 archival master

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -preset slow -crf 20 \
  -profile:v high -level 4.1 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### h264_nvenc bulk batch (Turing+)

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

`-bf 2`: B-frames for better compression on low-motion content (NVENC may default to 0).  
`-rc-lookahead 32`: 32-frame buffer for better rate control; higher values give diminishing returns.  
`-multipass fullres`: adds ~+10-15% quality at 2x encode time — worth it for archival, skip for bulk.

### HEVC archival (libx265, 10-bit for slide/text content)

```bash
ffmpeg -i input.mp4 \
  -c:v libx265 -preset slow -crf 22 \
  -pix_fmt yuv420p10le -tag:v hvc1 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

10-bit reduces posterization and banding on gradient slides; `hvc1` tag required for Apple compatibility.

### hevc_nvenc bulk

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

### SVT-AV1 CPU (recommended over libaom-av1)

```bash
ffmpeg -i input.mp4 \
  -c:v libsvtav1 -preset 6 -crf 28 \
  -svtav1-params tune=0:lookahead=120 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

`tune=0`: VOD quality mode. `lookahead=120`: large lookahead for quality; reduce to 32 for speed.

### av1_nvenc (Ada, RTX 4000+)

```bash
ffmpeg -i input.mp4 \
  -c:v av1_nvenc -preset p6 -tune hq \
  -rc vbr -cq 30 -b:v 0 \
  -spatial-aq 1 -temporal-aq 1 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### Resolution downscale (4K → 1080p)

```bash
# Photographic / talking head — lanczos
ffmpeg -i input.mp4 -vf "scale=1920:-2:flags=lanczos" -c:v h264_nvenc ... output.mp4

# Screen recording / text slides — bicubic (less ringing)
ffmpeg -i input.mp4 -vf "scale=1920:-2:flags=bicubic" -c:v h264_nvenc ... output.mp4
```

`-2`: computes height automatically while keeping aspect ratio; ensures even number required by H.264.

### Audio: AAC for voice

```bash
# Native AAC (universal builds) — adequate at 128k
-c:a aac -b:a 128k -ac 1 -ar 48000

# libfdk_aac (Fraunhofer, better quality especially <128k; requires non-free build)
-c:a libfdk_aac -b:a 96k -ac 1 -ar 48000 -afterburner 1

# Verify libfdk_aac availability
ffmpeg -encoders | grep fdk
```

AAC bitrate guide for mono voice: 64k = acceptable streaming, 96k = distribution minimum, 128k = archival sweet spot, 160k+ = diminishing returns.  
HE-AAC (`-profile:a aac_he`) better below 64k but has weaker player support; use LC-AAC for compatibility.

### Speech tempo change with formant preservation (Rubber Band R3)

Three-pass pipeline — extract audio, R3 stretch, re-mux with sped-up video:

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

`-shortest` aligns stream durations — required when video and audio lengths differ by milliseconds after stretch.

### Concat: fast path (no re-encode)

All clips must share identical codec, resolution, frame rate, pixel format, and audio parameters:

```bash
# Build list file
printf "file '%s'\n" part1.mp4 part2.mp4 part3.mp4 > list.txt

# Demuxer concat — ~37x faster than re-encode
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# With regenerated timestamps (for speed-up outputs or AVI/MKV rips with corrupt PTS)
ffmpeg -fflags +genpts -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Concat: filter path (re-encode, mixed params)

```bash
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v h264_nvenc -preset p6 -tune hq -cq 24 \
  -c:a aac -b:a 128k -ac 1 \
  -movflags +faststart output.mp4
```

Use when clips differ in any parameter; slower but handles any input combination.

## NVENC Tuning Reference

| Flag | Values | Effect |
|---|---|---|
| `-preset` | `p4` (skip), `p5` bulk, `p6` quality, `p7` archival | Speed/quality tradeoff; p7 still faster than libx264 medium |
| `-tune` | `hq` (use always for quality), `ll`/`ull` (latency only) | `hq` mandatory — default gives noticeably lower quality |
| `-spatial-aq 1` | 0/1 | More bits on complex spatial regions, fewer on flat — critical for slides |
| `-temporal-aq 1` | 0/1 | More bits on static frames (face), fewer on motion — critical for talking head |
| `-rc-lookahead` | 32 (recommended), 64 (diminishing) | Frame buffer for rate control decisions |
| `-bf` | 2-3 | B-frames; NVENC may default to 0, set explicitly for lecture/low-motion |
| `-multipass fullres` | (flag) | Two-pass full-res: +10-15% quality, 2x time; NVENC SDK 12+, archival only |

## Gotchas

- **Issue:** `af_rubberband=tempo=3.0` (ffmpeg built-in) produces metallic/robotic artifacts at 3x speech. **Fix:** Use Rubber Band R3 standalone CLI (`rubberband-r3 -T 3 -F`). Built-in uses R2 engine; even with `formant=preserved` R2 loses to R3 on speech at high ratios.

- **Issue:** `-movflags +faststart` omitted — video buffers entire file before play begins; seeking fails on HTTP streams. **Fix:** Always append `-movflags +faststart` for any distribution MP4. No downside for local files.

- **Issue:** NVENC quality disappoints without `-tune hq`; default tune is equivalent to unoptimized mode. **Fix:** Always specify `-tune hq` for quality target; omitting it leaves significant quality headroom unused with no speed benefit.

- **Issue:** `hevc_nvenc` output refuses to play in QuickTime/Safari (`hev1` tag not recognized). **Fix:** Add `-tag:v hvc1` to force correct tag; applies to any HEVC in MP4 targeting Apple.

- **Issue:** `ffmpeg -f concat -c copy` produces audio/video sync drift when source files have non-zero start PTS (common in speed-up outputs or MKV rips). **Fix:** Add `-fflags +genpts` to regenerate timestamps: `ffmpeg -fflags +genpts -f concat -safe 0 -i list.txt -c copy out.mp4`.

- **Issue:** CQ too low (aggressive) on NVENC produces visible blocking/ringing on text and slide gradients. **Fix:** For 1080p lecture/slide content use CQ 24-26 for H.264, CQ 26-28 for HEVC. CQ 18 or below = near-lossless but filesize grows exponentially; unnecessary for screen content.

- **Issue:** `libsvtav1` CRF scale is not the same as x264/x265; direct CRF transplant produces vastly different results. **Fix:** SVT-AV1 CRF 28-32 ≈ x265 CRF 22 ≈ x264 CRF 16-18 for equivalent perceptual quality on typical content.

- **Issue:** `atempo=3.0` in an ffmpeg audio filter chain produces intelligible but low-quality speech at 3x; phase-vocoder smearing is audible. **Fix:** Do not use `atempo` above 2x for speech; use Rubber Band R3 standalone pipeline instead.

## See Also

- [[bash-scripting]] - batch processing loops for multi-file encode jobs
- [[io-redirection-and-pipes]] - piping ffmpeg output, logging encode progress
- [[monitoring-and-performance]] - GPU utilization monitoring during NVENC encode (`nvidia-smi dmon`)
- [[disks-and-filesystems]] - storage layout for large video archives
- [FFmpeg Codecs Documentation](https://ffmpeg.org/ffmpeg-codecs.html)
- [FFmpeg Scaler Documentation](https://ffmpeg.org/ffmpeg-scaler.html)
- [FFmpeg Wiki: Encode/AV1](https://trac.ffmpeg.org/wiki/Encode/AV1)
- [FFmpeg Wiki: Encode/AAC](https://trac.ffmpeg.org/wiki/Encode/AAC)
- [Rubber Band Audio Library](https://breakfastquay.com/rubberband/)
- [NVIDIA Video Codec SDK Presets](https://developer.nvidia.com/blog/introducing-video-codec-sdk-10-presets/)
- [SVT-AV1 Preset Analysis — OTTVerse](https://ottverse.com/analysis-of-svt-av1-presets-and-crf-values/)
- [CRF Guide — slhck.info](https://slhck.info/video/2017/02/24/crf-guide.html)
