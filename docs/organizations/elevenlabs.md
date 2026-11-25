---
title: ElevenLabs — Voice Platform Development
category: organizations
tags: [elevenlabs, organization, voice-platform-development]
aliases: ["ElevenLabs"]
---

# ElevenLabs — Voice Platform Development

**Development line:** `organization:elevenlabs` · thread `voice-platform-development`  
**Events:** 1 dated, 2025-11-12 → 2025-11-12 · **Researched:** 2026-09-03 · confidence: high

## What it is

ElevenLabs — AI audio platform for product teams and creators who need generated speech, transcription, voice cloning, dubbing, or a voice layer for an LLM. Capabilities: - Text to Speech, Speech to Text, voice cloning, dubbing, and voice agents. - Hosted ElevenAgents, or Speech Engine when a team keeps the LLM and conversation logic on its own server. Limit: Eleven v3 supports 70+ languages but does not support SSML break tags; generated audio is nondeterministic. Verdict: a practical single-platform choice for voice product work, provided each selected voice, language, and rights path is tested before release.

## Development line

- **2025-11-12 — ElevenLabs linked its Iconic Voices program to celebrity AI-voice partnerships.** On 2025-11-12, the dated links connected ElevenLabs’ Iconic Voices offering with a Variety report on AI-voice partnerships involving Matthew McConaughey and Michael Caine. This is a material development because it records an official celebrity-voice program within ElevenLabs’ voice platform.

## What changed

2023-01-30 — At the beta stage, ElevenLabs offered long-form text-to-speech, voice cloning, voice design, and API access; AI dubbing was still described as a future release. 2024-02-13 — Voice Library expanded from designed synthetic voices to verified Professional Voice Clones that could be shared and earn payouts from paid-subscriber usage, with verification, review, withdrawal, and moderation controls. 2024-02-19 — No product change is assigned: the linked Typeform page cannot be identified from its currently retrievable content. 2025-11-12 — The Iconic Marketplace introduced a request-and-licensing route for companies seeking approved iconic voices; it is not an ordinary self-serve cloning path. Found today, 2026-09-04 — current documentation describes a broader platform: TTS, STT, cloned or designed voices, dubbing, and two agent routes: hosted ElevenAgents or bring-your-own-LLM Speech Engine.

## How to use this

From 2025-11-12, practitioners should distinguish officially licensed voices offered through ElevenLabs’ Iconic Voices program from unlicensed celebrity-voice imitation, and verify the applicable rights before use.

1. For narration, open Text to Speech, enter or paste the script, select a voice, adjust the model and settings if needed, then generate and download the audio.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
2. For transcription, send audio to the Speech-to-Text API and use the returned text, timestamps, and speaker information supported by the selected Scribe model.
  — <https://elevenlabs.io/docs/overview/capabilities/speech-to-text/>
3. For a voice agent, choose hosted ElevenAgents when you want the platform to provide the LLM, knowledge base, and tools; choose Speech Engine when your backend owns the LLM and conversation flow.
  — <https://elevenlabs.io/docs/overview/capabilities/speech-engine>
4. For a high-fidelity clone of your own voice, create a Professional Voice Clone, upload clean samples, complete voice verification, wait for fine-tuning, then select it from My Voices.
  — <https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning>
5. To share and monetize an approved Professional Voice Clone, enable Voice Library sharing, complete Stripe Connect setup, and review usage in My Voices and Payouts.
  — <https://elevenlabs.io/docs/eleven-creative/voices/payouts>
6. For an iconic or estate-managed voice, use Iconic Marketplace and submit a Request Voice; access is a licensing request.
  — <https://elevenlabs.io/iconic-voices>

## Best practices

- Choose the voice before fine-tuning settings, and match its language, accent, and baseline delivery to the actual script.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
- Write numbers and ambiguous symbols out as words, and use deliberate punctuation so the model receives an unambiguous script.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
- For Eleven v3, match the base voice to the intended delivery; use audio tags, punctuation, and text structure for pacing instead of SSML break tags, then test the chosen voice-tag combination.
  — <https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices>
- Treat output as probabilistic: use stability to trade expressiveness for repeatability and approve the actual generated take rather than assuming identical repeats.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
- Clone only a voice you have the right and consent to use. For a Professional Voice Clone, use clean single-speaker recordings in the intended language and delivery style; PVC is restricted to the account holder's own verified voice.
  — <https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning>

## Superseded by this

- 2023-01-30 — Guidance that treats ElevenLabs only as a beta long-form TTS and narration tool is obsolete; the current platform also documents STT, dubbing, voices, and agent workflows.
- 2024-02-13 — Guidance that treats Voice Library as a catalog only of designed synthetic voices is obsolete; verified Professional Voice Clones can now be shared and monetized through the payout flow.
- 2025-11-12 — Guidance to obtain a famous or estate-managed voice through ordinary self-serve cloning is obsolete; the current route is an Iconic Marketplace licensing request.
- 2026-09-04, found today — Guidance to use SSML break tags for pauses in Eleven v3 is obsolete; v3 uses audio tags, punctuation, and text structure instead.

## Still unknown

- The 2024-02-19 Typeform URL, https://form.typeform.com/to/gg0xzZW4, could not be retrieved or independently identified, so it is not used to assert a product change.
- Pricing, regional availability, and approval of an individual marketplace or iconic-voice request depend on the account, plan, and rights-holder review; they were not compared here.
- This is first-party product and workflow evidence, not an independent benchmark of output quality, uptime, or commercial suitability.

## Sources

| source | title | read |
|---|---|---|
| https://elevenlabs.io/docs/overview | Documentation | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech | Text to Speech (product guide) | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/overview/capabilities/speech-to-text/ | Transcription | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/overview/capabilities/speech-engine | Speech Engine | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning | Professional Voice Cloning | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/eleven-creative/voices/payouts | Payouts | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices | Best practices | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/blog/elevenlabs-raises-2m-pre-seed-and-announces-ai-speech-platform-promising-to-revolutionize-audio-storytelling | ElevenLabs Raises $2M and Announces AI Speech Platform | 2026-09-04 |
| https://elevenlabs.io/blog/introducing-voice-actor-payouts | Introducing Voice Actor Payouts | 2026-09-04 |
| https://elevenlabs.io/blog/announcing-partnership-with-sir-michael-caine-to-newly-launched-iconic-marketplace | Sir Michael Caine partners with ElevenLabs and joins new Iconic Marketplace | 2026-09-04 |
| https://elevenlabs.io/iconic-voices | ElevenLabs — License Legendary Voices - Iconic Marketplace | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:elevenlabs`, thread `voice-platform-development`, 1 dated events 2025-11-12 → 2025-11-12.
- **Practical note:** From 2025-11-12, practitioners should distinguish officially licensed voices offered through ElevenLabs’ Iconic Voices program from unlicensed celebrity-voice imitation, and verify the applicable rights before use.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:463d2c76338193a3159f2c71777af49ca92383d8f02ad28090db53d1eafdb2b7 -->
## 2026-10-17 — ElevenLabs adds Instant Soundtracks for uploaded video

Instant Soundtracks creates a score and timestamped sound effects from uploaded video. It keeps effects as editable layers and can return separate music and sound-effect files through the API.

### Usage and practices

- Open the ElevenCreative Music Video Editor, upload video, and generate a soundtrack with sound effects. The video’s existing audio can serve as a score reference. [Source](https://elevenlabs.io/blog/introducing-instant-soundtracks)
- Review sound effects on separate timeline layers. Adjust timing or replace music, then export the result. [Source](https://elevenlabs.io/blog/introducing-instant-soundtracks)
- For music outside the video workflow, describe the genre, mood, instrumentation, structure, and intended use in a natural-language prompt. Then edit sections or regenerate. [Source](https://elevenlabs.io/docs/eleven-creative/products/music)
- Combine genre, mood, instrumentation, tempo, and use case in a detailed prompt instead of using a broad genre label. [Source](https://elevenlabs.io/docs/eleven-creative/products/music)
- For longer compositions, generate and approve the intro first. Build the next sections one at a time, refining prompts instead of restarting the whole track. [Source](https://elevenlabs.io/docs/eleven-creative/products/music)
- Use separate sound-effect layers to check cue timing and revise individual moments before export. [Source](https://elevenlabs.io/blog/introducing-instant-soundtracks)

### Additional evidence

- 2026-10-17: The release documents the API controls as add\_sfx, separate\_tracks, and use\_audio\_as\_reference. With separate\_tracks=true, the API returns a ZIP containing separate music and sound-effect files. Requests support up to 10 videos totaling 200 MB and 10 minutes. [Source](https://elevenlabs.io/blog/introducing-instant-soundtracks)

### Limits and open questions

- The reviewed public material does not state a minimum subscription tier for the full Instant Soundtracks workflow.
- The public release does not name a distinct model for Instant Soundtracks.
- No qualifying independent practitioner discussion specifically about Instant Soundtracks was found in the reviewed results.

<!-- Retained base: fa3cccdfbdd5ddca7a3b01f3b752c0fa59966afe; article blob: fe6aa94482f605160178e07ded1bc76ca5ad03de -->

<!-- live-update:c8ce4024a7948cdb529aa05d26690a24bbae6d3aad2f4a65d8d0503d6ce199ef -->
## 2026-10-22 — ElevenLabs Chimera in ElevenCreative

ElevenLabs introduced Chimera, a character system inside ElevenCreative. It pairs the Eleven v4 emotive speech engine with the Seedance 2.5 video generation model. From a text script, emotion tags and a reference image, it produces a talking character with speech and face in sync.

### Usage and practices

- Open ElevenCreative and pick the character generation studio. [Source](https://elevenlabs.io/creative)
- Upload a reference image of the character, or generate one from a text prompt. [Source](https://elevenlabs.io/creative)
- Pick an Eleven v4 voice, or assign a cloned voice profile. [Source](https://elevenlabs.io/creative)
- Type the dialogue in the script editor. Add bracketed emotion tags such as \[whispers\] or \[laughs\] to steer the voice and the facial expression. [Source](https://elevenlabs.io/creative)
- Render the generation pass to export the lip-synced video. [Source](https://elevenlabs.io/creative)
- Put each emotion tag right before the sentence or word it applies to, so the speech model and the video model match the expression to the tone. [Source](https://elevenlabs.io/creative)
- Use a high-resolution, forward-facing portrait with clear features, so lip sync does not distort during complex emotional lines. [Source](https://elevenlabs.io/creative)
- Keep each dialogue segment short, so the face stays consistent and does not drift over long renders. [Source](https://elevenlabs.io/creative)

### Additional evidence

- 2026-10-22: Chimera combines ByteDance's Seedance 2.5 video architecture with Eleven v4 speech synthesis inside ElevenCreative. The stated aim is to remove dubbing sync lag and drive facial movement from emotion, across more than ninety languages. [Source](https://elevenlabs.io/creative)

### Superseded guidance (retained for history)

- 2026-10-22: The old workflow split the job in two: synthesize the voiceover first, then lip-sync it with a separate post-processing tool. [Source](https://elevenlabs.io/creative)

### Limits and open questions

- "Voice Platform Development" is a general category, not a product name. This entry covers ElevenLabs Chimera within ElevenCreative only.
- Third-party benchmarks and community discussion on Reddit, YouTube and Medium turned up, but without verifiable direct page links, so none of it is cited here.
- Credit cost per render, batch API endpoints and export resolution caps for Chimera are not given on the main ElevenCreative page.

<!-- Retained base: dfb3de9ab54eb4b0ebd0dce739bcda6b6bd59c78; article blob: 52948543a1ace86d5aefeb5f2fb50994000b8d6c -->
