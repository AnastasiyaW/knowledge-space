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
