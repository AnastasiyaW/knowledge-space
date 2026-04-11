---
title: "Video & Motion Design Rules"
description: "Concrete numbers for timing, easing, audio levels, composition, and storytelling in product videos and motion graphics."
---

# Video & Motion Design Rules

Reference for production-quality motion graphics, product videos, and animated presentations. All values are specific and actionable.

## Animation Timing

### Duration by element weight

| Element | Duration | Frames @30fps | Example |
|---------|----------|---------------|---------|
| Micro (icon, dot) | 150-200ms | 5-6 | Toggle, checkbox |
| Small (button, badge) | 200-300ms | 6-9 | Hover state, tooltip |
| Medium (card, text) | 300-500ms | 9-15 | Panel slide, dropdown |
| Large (panel, image) | 400-700ms | 12-21 | Modal open |
| Hero (product, scene) | 600-1200ms | 18-36 | Product reveal |
| Cinematic (background) | 800-1500ms | 24-45 | Ambient transitions |

**Rule:** UI animations stay under 300ms. 180ms feels more responsive than 400ms (empirical).

### Material Design 3 duration tokens

| Token | Value | When |
|-------|-------|------|
| short1 | 50ms | Micro-feedback |
| short4 | 200ms | Standard interactions |
| medium2 | 300ms | Standard transitions |
| medium4 | 400ms | Complex transitions |
| long2 | 500ms | Navigation transitions |
| long4 | 600ms | Elaborate transitions |
| extraLong1-4 | 700-1000ms | Dramatic (rare) |

### Scene duration guidelines

| Scene type | Duration |
|------------|----------|
| Hook/opener | 3-5s |
| Hero stat ("2x faster") | 4-6s |
| Feature showcase | 5-8s |
| Product beauty shot | 3-5s |
| Testimonial/quote | 4-6s |
| CTA/closer | 4-6s |
| Fast-cut montage | 2-3s each |

**60-second video rhythm:**
```
[0-5s]   Hook: bold statement, dark bg        — FAST
[5-15s]  Problem: 2-3 quick cuts              — MEDIUM
[15-25s] Solution reveal: product appears     — SLOW
[25-40s] Features: 3-4 staggered              — MEDIUM
[40-50s] Social proof: stats/logos/quotes     — MEDIUM-FAST
[50-60s] CTA: logo + URL + action             — SLOW, decisive
```

**Breathing rule:** after every fast section (3+ quick cuts), include one slow shot (5-8s).

## Easing

### Cubic-bezier reference

| Name | Value | When |
|------|-------|------|
| ease (browser default) | `(0.25, 0.1, 0.25, 1.0)` | Generic, acceptable |
| **Material Standard** | `(0.4, 0.0, 0.2, 1.0)` | Primary UI easing |
| Material Decelerate (enter) | `(0.0, 0.0, 0.2, 1.0)` | Element appearing |
| Material Accelerate (exit) | `(0.4, 0.0, 1.0, 1.0)` | Element leaving |
| Emphasized enter | `(0.05, 0.7, 0.1, 1.0)` | Dramatic appearance |
| Emphasized exit | `(0.3, 0.0, 0.8, 0.15)` | Dramatic departure |
| Bounce/overshoot | `(0.34, 1.56, 0.64, 1.0)` | Playful buttons/badges |
| Snappy | `(0.2, 0.0, 0.0, 1.0)` | Fast, confident |
| Apple ease | `(0.25, 0.1, 0.25, 1.0)` | Premium/Apple style |

### Spring physics

| Config | stiffness | damping | Effect |
|--------|-----------|---------|--------|
| Responsive UI | 200 | 20 | Minimal bounce |
| Playful | 120 | 10 | Noticeable bounce |
| Gentle (large elements) | 50 | 200 | Slow, no bounce |

**NEVER linear for UI** - looks mechanical. Linear is for progress bars only.

## Stagger Patterns

**Max staggered items: 8-10.** Beyond that, last items wait too long.

**Linear stagger:** 30-80ms between items in a list.

**Cascade (accelerating):** each delay is shorter than previous - creates "pouring in" effect.

**Grid diagonal:** delay = `(row + col) * baseDelay`. Top-left animates first.

**Ripple from center:** delay proportional to distance from center point.

## Disney's 12 Principles Applied to Product Video

| Principle | Application | DO / DON'T |
|-----------|-------------|------------|
| **Squash & Stretch** | Buttons scale 0.95-0.97 on press | DO: soft elements. DON'T: text/lines |
| **Anticipation** | 30-50ms micro-movement opposite to main direction | DO: before major transitions. DON'T: on hover |
| **Staging** | One focal point per scene | DO: stop bg animations when showing key element. DON'T: 3+ simultaneous animations |
| **Follow Through** | Elements overshoot 2-5% then settle | DO: stagger in lists/grids. DON'T: same stagger for 20+ items |
| **Ease In/Out** | Never linear for UI | Use Material Standard as default |
| **Arcs** | Natural curved paths between positions | DO: floating elements. DON'T: dropdowns (expect straight line) |
| **Secondary Action** | Background effects support, not compete | DO: ambient particles, glow pulse. DON'T: spinning, flashing |
| **Exaggeration** | Scale product 5-15% larger for impact | DO: hero animations. DON'T: utility animations |
| **Depth** | 3-5 parallax layers | Background 0.3x speed, foreground 1.0-1.3x |

## Typography on Screen

### Size scale for 1920x1080

| Role | Size | Weight | Notes |
|------|------|--------|-------|
| Hero number | 120-200px | 800-900 | "10x faster", key stats |
| Section title | 64-80px | 600 | Feature names |
| Subtitle | 36-48px | 500 | Supporting headlines |
| Body | 24-32px | 400 | Descriptions |
| Caption | 16-20px | 400 | Small annotations |
| **Minimum** | **16px** | any | Below = illegible on video |

### Reading speed

| Format | Words | Time on screen |
|--------|-------|----------------|
| Short line | 3-7 words | 1.5-3s |
| Medium line | 8-12 words | 3-5s |
| Long sentence | 13-20 words | 5-8s |
| 30+ words | split into 2-3 screens | - |

Assume 150-180 WPM for mixed audience. Rule: 2.5-3.0s per short line (7-9 words).

### Word limits per element

| Element | Limit |
|---------|-------|
| Headline | 3-6 words |
| Subtitle/caption | max 2 lines, 32-42 chars/line |
| Lower third | 2 lines max (name + title) |
| Screen with VO | max 10-15 words |
| Screen without VO | max 20-25 words |
| Thumbnail | max 3-5 words |

### Typography animation

- DO: fade in + translate 20-40px from bottom
- DO: scale from 95% to 100% with opacity 0→1
- DO: stagger words 4-8 frames each
- DON'T: rotate text
- DON'T: bounce text (unless playful brand)
- DON'T: move text while viewer is reading it

**Text must be readable for minimum 2s after animation completes.** Never animate text AND expect reading simultaneously.

## Color

### Palette rules

- Max 3 colors per video (+ black/white/gray)
- 1 primary brand color + 1 accent + 1 CTA color
- Background:text contrast minimum 7:1 (WCAG AAA)
- Gradient colors: max 120° apart on color wheel

### Gradient guidelines

**Direction:** top-left→bottom-right (natural light). DON'T bottom-to-top.

| Type | When |
|------|------|
| Linear | Backgrounds, overlays |
| Radial | Spotlight, glow, focus on center |
| Mesh | Premium hero backgrounds, app screens |
| Conic | Clocks, pie charts, progress |

**Noise gradients (2025-2026):** gradient + 3-8% noise overlay = organic premium feel.

### Dark vs light mode

**Dark mode better for:** product showcases (product pops), premium/luxury feel, dim viewing environments, photo/portfolio.

**Light mode better for:** dense text, corporate, conference rooms, print-adjacent.

### Trending palettes (2026)

**Tech/dark:**
- Deep navy `#0D1117` + electric blue `#58A6FF`
- Dark teal `#0F2027` + cyan `#00C9FF` + soft white

**Tech/light:**
- Off-white `#F8F9FA` + warm accents
- Soft lavender `#F3E8FF` + deep purple `#7C3AED`

## Composition

### Safe zones by platform

**16:9 YouTube (1920x1080):**
- Title-safe: inner 80% (10% padding each side)
- Action-safe: inner 90%
- Lower thirds zone: bottom 20-25%

**9:16 Vertical (TikTok/Reels/Shorts, 1080x1920):**
- Bottom 20% occupied by platform UI
- Right 10% occupied by platform UI
- Subject/face: upper 20-30% of frame
- Text safe zone: 15-75% height, centered width

**1:1 Square (Instagram, 1080x1080):**
- Safe zone: inner 900x900px
- Center composition works best

### Visual hierarchy per scene

- Maximum 3 hierarchy levels per scene
- Primary element = 40-60% of visual weight
- Never two primary elements competing in one scene
- Use size + weight + color + position together (not just one)

### Parallax depth

- Background layer: 0.2-0.4x scroll speed
- Midground: 0.6-0.8x
- Foreground: 1.0-1.3x

## Scene Transitions

| Transition | When | Duration |
|-----------|------|----------|
| **Hard cut** | Same energy, fast pacing (80% of cuts) | instant |
| Cross dissolve | Passage of time, soft connection | 0.5-2s |
| Fade to black | End of section, dramatic pause | 1-2s |
| Wipe | Location change, stylistic | 0.5-1.5s |
| Zoom through | Energy, modern, dynamic | 0.3-0.5s |
| Match cut | Visual similarity (shape/color/motion) | instant |
| L-cut | Audio from scene 1 over scene 2 visuals | audio overlap |
| J-cut | Audio from scene 2 before scene 1 ends | audio leads |

**Default = hard cut.** 80%+ of professional video transitions are cuts.

Max 2-3 transition types per video. DON'T: star wipes, checkerboard, dissolve >2s.

**Audio crossfade:** 100-300ms overlap for smooth audio transitions.

## Audio Levels

### dB reference

| Element | Peak | Loudness (LUFS) |
|---------|------|-----------------|
| Voiceover | -12 to -10 dB | -16 to -14 |
| Music under VO | -32 to -24 dB | -24 to -18 |
| Music standalone | -16 to -12 dB | -16 to -14 |
| Sound effects | -18 to -10 dB | varies |
| Overall mix | -14 avg, peaks < -6 dB | -16 to -14 |
| True peak ceiling | -1 to -3 dB | - |

**Rule:** VO should be ~20 dB louder than background music.

### BPM by mood

| BPM | Mood | Use case |
|-----|------|---------|
| 60-80 | Calm/ambient | Luxury, meditation |
| 80-100 | Relaxed | Lifestyle, interviews |
| 100-120 | Moderate | Corporate, tech demos |
| 120-140 | Energetic | Product launches, fitness |
| 140+ | High energy | Action, gaming |

120 BPM = preferred human tempo (matches walking pace, DAW default).

### Sound effect types

| SFX | Duration | When |
|-----|----------|------|
| Whoosh | 50-200ms | Slide-in transitions |
| Click/pop | 20-50ms | Button press, selection |
| Ding/chime | - | Success states, notifications |
| Swoosh | - | Page transitions, reveals |

SFX should be 6-12 dB quieter than VO.

### Free sound libraries

- **Mixkit** (mixkit.co) - royalty-free, no attribution, commercial OK
- **Pixabay** (pixabay.com/sound-effects) - royalty-free, no signup
- **Freesound** (freesound.org) - CC-licensed
- **SFX Engine** (sfxengine.com) - AI-generated UI sounds

## Storytelling Frameworks

### PAS (Problem-Agitation-Solution) - highest converting

```
Problem:    3s — one clear pain point
Agitation:  5s — vivid consequence
Solution:   4s — your product/answer
CTA:        3s — direct call to action
Total: ~15s. Scale proportionally for 30-60s.
```

### Hook-Value-CTA

```
Hook:  2-5s  — pain point or question
Value: rest  — concise solution
CTA:   3-5s
```

### Hook-Problem-Solution-Proof-CTA (short video optimized)

| Section | Duration | Example |
|---------|----------|---------|
| Hook | 3-5s | "What if you could make product videos in 5 minutes?" |
| Problem | 5-10s | "Hiring a video team costs $5000+. DIY tools look amateur." |
| Solution | 10-20s | Product reveal + 1 key demo |
| Proof | 5-10s | Stats, logos, testimonials |
| CTA | 3-5s | "Start free at product.com" |

### First seconds rule

- First 3 seconds determine retention (scroll-stop moment)
- First 8 seconds = everything for short-form
- DON'T: logo/intro first (nobody cares about your logo)
- DO: start with hook/problem/visual surprise

## Platform Specs (2026)

| Platform | Ratio | Resolution | Max Duration | Format |
|----------|-------|-----------|-------------|--------|
| YouTube | 16:9 | 1920x1080 (up to 4K) | 12 hours | MP4 H.264+AAC |
| YouTube Shorts | 9:16 | 1080x1920 | 3 min | MP4 |
| Instagram Reels | 9:16 | 1080x1920 | 20 min | MP4/MOV |
| Instagram Feed | 1:1 or 4:5 | 1080x1080 or 1080x1350 | 60s | MP4/MOV |
| TikTok | 9:16 | 1080x1920 | 10 min in-app | MP4/MOV |
| TikTok ads | 9:16 | 1080x1920 | 9-60s | MP4/MOV <500MB |
| LinkedIn | 16:9 or 1:1 | 1920x1080 | 10 min | MP4 |

**Engagement sweet spots:** TikTok 21-34s, YouTube Shorts 30-60s, Instagram Reels 15-30s.

## Copywriting for Video

- Numbers > adjectives: "5x faster" not "much faster"
- Benefit > feature: "Save 10 hours/week" not "Has batch processing"
- You > We: "You'll love..." not "We built..."
- Max 8-10 words per line on screen
- Remove: Very, Really, Basically, Actually, Just

**Hook formulas:**
- "What if you could [desired outcome]?"
- "[Number] [noun] that [unexpected benefit]"
- "Stop [common mistake]. Start [better approach]."

## Thumbnail Design

Spec: 1280x720px, 72dpi, PNG/JPG <2MB.

**60-30-10 color rule:** 60% background, 30% subject, 10% accent/text.

- Max 3-5 words, readable at mobile size
- Faces with emotion = +20-30% CTR
- 1-2 hero elements max, no clutter

## Gotchas

- **Linear easing looks mechanical.** Always use a curve. The only legitimate use for linear is progress bars and spinners where constant rate is expected.
- **Staggering 20+ items breaks UX.** The last item waits too long - viewer attention drifts. Max 8-10 staggered items; for longer lists, group them and stagger groups.
- **Don't start with a logo.** Viewers skip intros. The hook must earn attention before branding appears.
- **Music BPM ≠ mood.** Two tracks at 120 BPM can feel completely different. BPM sets energy floor, not emotional character.
- **Bottom 20% of vertical video is covered by platform UI** (TikTok Like/Comment/Share buttons). Never place text or CTAs there.
- **Dissolve longer than 2 seconds looks like a mistake.** Cross dissolve is for passage of time, not style. Keep it 0.5-2s max.

## Production Checklists

### Pre-production

- [ ] Story framework: PAS / 3-Act / Hook-Value
- [ ] Platform + aspect ratio defined
- [ ] Color palette: max 3-4 colors + neutrals
- [ ] Fonts: max 2 (heading + body)
- [ ] Music: BPM matched to mood
- [ ] Sound effects library ready

### Animation

- [ ] Consistent easing: 1-2 curve types max
- [ ] Timing within bounds (micro <100ms, standard 200-350ms, complex 350-500ms)
- [ ] Stagger 30-80ms between grouped items
- [ ] Max 2 elements animated simultaneously
- [ ] Follow-through on stops (overshoot + settle)
- [ ] Anticipation before major transitions

### Post-production

- [ ] Audio levels: VO -12 to -10 dB, music -32 to -24 dB under VO
- [ ] Text readable at target device size
- [ ] Safe zones respected for target platform
- [ ] Transitions consistent (max 2-3 types)
- [ ] Hook in first 3 seconds
- [ ] CTA clear and visible
- [ ] Thumbnail: 60-30-10 rule, max 5 words
- [ ] Captions/subtitles added
- [ ] Exported at correct platform specs

## See Also

- [[css-animation-and-transforms]]
- [[remotion-programmatic-video]]
- [[3d-browser-libs-for-video]]
