---
title: AI-Powered Video Production
category: applications
tags: [data-science, generative-ai, video, production, tools]
---

# AI-Powered Video Production

Full pipeline for creating commercial video using AI tools. Chains LLM scripting, image generation, video synthesis, and audio generation.

## Tool Chain

| Tool | Role | Best For |
|------|------|----------|
| GPT-5 | Script, prompts, iteration | One project per video, one chat per session |
| Seedream 4 | Image generation from scratch | Photorealistic people/scenes |
| NanoBanana Pro | Edit/stylize existing frames | Reference reproduction, geometry preservation |
| Kling 2.5 | Video generation | Draft at 720p (free), final at 1080p |
| ElevenLabs | Voice generation | Voiceovers, character speech |
| Suno | Music generation | Background music |

## Pipeline Stages

### 1. Script & Storyboard
- Brief GPT with concept, characters, setting, visual references
- Structure into ~6 scenes, ~25 sec total
- Assign shot types: wide / medium / close-up / detail
- Never repeat same shot type consecutively
- Account for AI limitations: far shots render faces poorly

### 2. Still Frame Generation
- Seedream: Fashion Photo style, 16:9, Unlimited Mode
- Disable "AI Prompt / Improve short prompts"
- Generate without references first, then refine with references
- Edit with NanoBanana for geometry-preserving corrections

### 3. Draft Animatic
- Kling 2.5 at 720p Unlimited (0 credits) for testing
- Review: movement speed, proportions, background consistency
- Fix via re-generation with refined prompts

### 4. Video Prompt Structure
```
1. Scene description: "wide shot of a lone man walking..."
2. Character movement: "takes 2-3 small steps then stops"
3. Camera movement: "camera slowly dollies forward, no shaking"
4. Atmosphere: "cold, dramatic grading, blue haze"
5. Negative: "no extra limbs, no face blur, no acid colors"
```

### 5. Audio & Lipsync
- ElevenLabs for voiceover generation
- Lipsync in Higgsfield (video + audio alignment)
- English lipsync more stable than other languages
- Duration matching critical: video and audio must align

## Seedream vs NanoBanana

| Aspect | Seedream 4 | NanoBanana Pro |
|--------|-----------|----------------|
| From scratch | Excellent | Good |
| Reference reproduction | Poor | Excellent |
| Close-up details | Contrasty, hard | Soft, realistic |
| Text/branding | Poor | Much better |

## Credit Management
- All stills and experiments: Unlimited mode (free)
- Draft videos: 720p Unlimited (0 credits)
- Final generation only: 1080p (500 credits/gen, 3-5 attempts per scene)

## Gotchas
- Long "poetic" prompts confuse video models - keep structured and specific
- Always specify camera behavior (default = random "flying")
- Far from camera = worse face quality - use separate full-body reference
- Color grading: override GPT's default "golden hour" for dramatic looks
- Teeth/tongue/mouth = main artifact zones in lipsync

## See Also
- [[generative-models]] - underlying generation technology
- [[nlp-text-processing]] - prompt engineering
