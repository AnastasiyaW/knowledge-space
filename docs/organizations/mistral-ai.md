---
title: Mistral AI — Product and model releases
category: organizations
tags: [mistral-ai, mistral_ai, model_releases, organization, product-and-model-releases]
aliases: ["Mistral AI"]
---

# Mistral AI — Product and model releases

**Development line:** `organization:mistral-ai` · thread `product-and-model-releases`  
**Events:** 2 dated, 2024-02-29 → 2026-02-05 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Mistral AI is a hosted model platform for developers, with Vibe as its interactive Work, Code and Chat surface.

- Studio: APIs and a console for text generation, agents, document AI, RAG, audio, keys and usage.
- Vibe: interactive work in the browser, terminal and IDE.
- Voxtral: batch transcription, live transcription and speech-to-speech building blocks.

## Development line

- **2024-02-29 — Mistral AI referenced its developer console and chat services.** On 2024-02-29, Mistral AI referenced both its developer console and chat service through the supplied official URLs. This is a visible product-access step in the company's history, covering a builder-facing console and an end-user chat interface. The supplied links establish no specific launch date or feature set beyond those services.
- **2026-02-05 — Mistral AI published Voxtral transcription and realtime model resources.** Mini Transcribe V2 covers batch work with diarization, context biasing and timestamps, while 4B Realtime covers live streams. The linked official announcement is dated 2026-02-04.

## What changed

2024-02-29 — Mistral AI exposed a developer-console URL and a separate chat URL.

2026-02-05 — Voxtral Transcribe 2 added a two-path speech-to-text release. Mini Transcribe V2 covers batch work with diarization, context biasing and timestamps; 4B Realtime covers live streams. The linked official announcement is dated 2026-02-04.

2026-09-04 (found today) — The console is now documented as Studio, a developer platform for API, agents, document AI, RAG and audio. chat.mistral.ai now opens Vibe with Work, Code and Chat modes.

2026-09-04 (found today) — The current audio surface also includes TTS and a composable speech-to-speech pipeline.

Choose an explicit surface—Studio, Vibe, batch audio or streaming audio—instead of treating Mistral as one generic chat endpoint.

## How to use this

From 2026-02-05, practitioners evaluating Mistral AI for speech workflows should consider its official Voxtral transcription and realtime resources, including the console speech-to-text path, rather than treating the company solely as a text-model provider.

1. Choose a surface: use Vibe for interactive Chat, Work or Code tasks, and Studio when building an application.  
   — [Le Chat is now Vibe](https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe)
2. Activate Studio, create a named API key, set an expiration and choose the smallest connector scope that fits the integration.  
   — [Activate Studio and generate an API key](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key)
3. Store MISTRAL_API_KEY in the environment, install the Python or TypeScript SDK (or use HTTP), send one chat-completion request, then verify the returned response.  
   — [Send your first API request](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request)
4. Use Studio Playground to test prompts, compare models and parameters, then review usage before moving the prompt into application code.  
   — [Studio](https://docs.mistral.ai/studio)
5. For audio, use Voxtral Mini Transcribe 2 for files, meetings and archives; use Voxtral Realtime only for low-latency streams. Test a representative file in the speech-to-text playground before integration.  
   — [Audio](https://docs.mistral.ai/studio/audio/overview)
6. If a local streaming deployment is required, follow the official Voxtral Mini 4B Realtime model card and its documented vLLM or Transformers path.  
   — [Voxtral Mini 4B Realtime model card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

## Best practices

- Start in Playground. Compare prompts and parameters without code, then make the tested configuration the integration baseline.  
  — [Studio](https://docs.mistral.ai/studio)
- Use expiring, named API keys. Grant the smallest connector scope, store the key once in a secret store, and rotate it regularly.  
  — [Activate Studio and generate an API key](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key)
- Treat Free mode as rate-limited. Implement exponential backoff for 429 responses.  
  — [Send your first API request](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request)
- Pick audio mode by workload. Batch Mini Transcribe 2 supports diarization, timestamps and up to 100 context terms; Realtime is for live streaming and cannot use diarization.  
  — [Audio](https://docs.mistral.ai/studio/audio/overview)
- For names and specialist vocabulary, use batch context biasing and evaluate it on your language. The release notes say the feature is optimized for English, while other-language support is experimental.  
  — [Voxtral Transcribe 2 release notes](https://mistral.ai/news/voxtral-transcribe-2)
- Self-host Realtime only against the documented backend and hardware envelope. The official BF16 card names a single GPU with at least 16 GB for vLLM serving and marks some alternatives untested.  
  — [Voxtral Mini 4B Realtime model card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

## Superseded by this

- 2024-02-29 — The chat surface is no longer described as Le Chat. chat.mistral.ai now opens Vibe with the same URL, login and existing conversations.
- 2026-02-05 — New audio integrations should not treat batch transcription and live streaming as interchangeable. Current guidance selects Mini Transcribe 2 for recordings and Realtime for streams, and Realtime cannot use diarization.
- 2026-02-05 — Use the current streaming model identifier, `voxtral-mini-transcribe-realtime-2602`, rather than relying on the family name alone.

## Still unknown

- The 2024-02-29 record preserves only entry-point URLs; it does not give the exact console or chat feature set at that date.
- The listed event is dated 2026-02-05, while Mistral's announcement is dated 2026-02-04. The source does not resolve the timezone or ingestion difference.
- `model_releases` is a shared release bucket, not a Mistral-only chronology. Only the linked Voxtral event is safely attached to this company page.
- A bounded Simplified-Chinese search found no first-party Chinese Mistral page to support a Chinese-specific operating recommendation.
- These operating practices come from current official documentation and the official model card; no independent production report was used.

## Sources

| source | title | read |
|---|---|---|
| https://console.mistral.ai/ | Mistral Console | 2026-09-04 |
| https://chat.mistral.ai/ | Vibe Chat | 2026-09-04 |
| https://mistral.ai/news/voxtral-transcribe-2 | Voxtral transcribes at the speed of sound. | Mistral AI | 2026-09-04 |
| https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602 | mistralai/Voxtral-Mini-4B-Realtime-2602 · Hugging Face | 2026-09-04 |
| https://console.mistral.ai/build/audio/speech-to-text | Mistral Studio speech-to-text playground | 2026-09-04 |
| https://docs.mistral.ai/studio | Studio | Mistral Docs | 2026-09-04 |
| https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request | Send your first API request | Mistral Docs | 2026-09-04 |
| https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key | Activate Studio and generate an API key | Mistral Docs | 2026-09-04 |
| https://docs.mistral.ai/studio/audio/overview | Audio | Mistral Docs | 2026-09-04 |
| https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe | Le Chat is now Vibe | Mistral Help Center | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:mistral-ai`, thread `product-and-model-releases`, 2 dated events 2024-02-29 → 2026-02-05.
- **Practical note:** From 2026-02-05, practitioners evaluating Mistral AI for speech workflows should consider its official Voxtral transcription and realtime resources, including the console speech-to-text path, rather than treating the company solely as a text-model provider.
- **Confidence:** medium. The dated supersedes above are the authority for what is obsolete.
