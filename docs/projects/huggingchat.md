---
title: HuggingChat
category: projects
tags: [huggingchat, huggingchat-launch, project]
aliases: ["HuggingChat"]
---

# HuggingChat

**Development line:** `project:huggingchat` · thread `huggingchat-launch`  
**Events:** 1 dated, 2023-04-25 → 2023-04-25 · **Researched:** 2026-09-04 · confidence: medium

## What it is

HuggingChat is a ChatGPT-style web chat for Hugging Face users who run open-source models. We can also self-host its Chat UI codebase.

- Hosted use: Omni routes a prompt automatically, or a user selects a model directly.
- Deployment: Chat UI connects to an OpenAI-compatible API and its `/models` endpoint.

## Development line

- **2023-04-25 — HuggingChat was introduced with an OpenAssistant model link.** The chat link pointed to `OpenAssistant/oasst-sft-6-llama-30b-xor`, which the card names OpenAssistant LLaMA 30B SFT 6. This shows an early model context, not a single hosted backend.

## What changed

HuggingChat moved from an OpenAssistant chat interface to a multi-provider routed service.

- 2023-04-25: the chat link pointed to `OpenAssistant/oasst-sft-6-llama-30b-xor`, whose card identifies it as OpenAssistant LLaMA 30B SFT 6. This shows an early model context, not a single hosted backend.
- 2023-06-11: web search was already running by this date. A first-party post from 2023-06-02 says the toggle had just launched and was still early. The generic chat link shows no separate June 11 change.
- 2025-07-01: HuggingChat announced that the old hosted service was closing and offered conversation export, while keeping Chat UI maintained.
- 2025-10-16: HuggingChat returned with Omni, a policy router across 115+ models and 15+ providers. It shows which model handled each routed request.
- Found today: the live page offers Omni and direct model choice across 138 models. The current Chat UI README uses OpenAI-compatible APIs; its web-search documentation and README conflict on whether legacy web-search helpers remain.

## How to use this

From 2023-04-25, we could use the public HuggingChat entry point as an early interface to an OpenAssistant-linked model.

1. Open the hosted app, sign in with a Hugging Face account if prompted, and select Start chatting.
  — <https://huggingface.co/chat/>
2. Choose Omni for automatic routing, or choose a named model for a direct comparison; when Omni routes, note the model shown during streaming.
  — <https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764>
3. For a controlled deployment, clone Chat UI, configure `MONGODB_URL`, `OPENAI_API_KEY`, and `OPENAI_BASE_URL`, then run it against an OpenAI-compatible provider.
  — <https://github.com/huggingface/chat-ui>

## Best practices

- Verify factual or high-stakes output against primary sources. The hosted UI warns that generated content may be inaccurate or false.
  — <https://huggingface.co/chat/>
- Select a named model or log Omni's displayed model for reproducible evaluation. Omni routes each request by policy and falls back when a primary model is unavailable.
  — <https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764>
- Review provider terms before sending sensitive data. HuggingChat routes across external providers, and each provider handles its own data security.
  — <https://github.com/huggingface/chat-ui/blob/main/PRIVACY.md>
- Pin the Chat UI revision for self-hosting. Test needed features directly instead of assuming old web-search behavior persists in current code.
  — <https://github.com/huggingface/chat-ui>

## Superseded by this

- 2023-04-25: treat HuggingChat as a dynamic router, not a fixed OpenAssistant LLaMA 30B endpoint. The current product provides Omni routing and direct choice from a changing catalogue.
- 2023-06-02 / 2023-06-11: early web-search toggle guidance is obsolete. The current README states legacy web-search helpers were removed, though Chat UI documentation still describes web search.
- 2025-07-01: the closure notice no longer applies. HuggingChat announced its return on 2025-10-16, and the hosted page was live when checked.

## Still unknown

- The 2023-04-25 source could not be retrieved, so its exact wording and intent stay unverified. Its model-card link does not prove a sole production backend.
- The 2023-06-11 link gives only the generic chat URL. The 2023-06-02 post confirms when web search launched, but not whether 2023-06-11 was a separate rollout, fix, or repost.
- Current hosted web-search status is unresolved. Official Chat UI documentation describes web search, but the current GitHub README says legacy web-search helpers were removed. Neither source confirms what runs on the hosted page.
- HuggingChat and self-hosted Chat UI are not identical setups. Public Chat UI source code does not prove the hosted instance's exact models, features, or provider configuration.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/chat/ | HuggingChat - Chat with AI models | 2026-09-04 |
| https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor | OpenAssistant/oasst-sft-6-llama-30b-xor · Hugging Face | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/185 | huggingchat/chat-ui · Feedback on the web search feature | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/747 | huggingchat/chat-ui · [ANNOUNCEMENT] HuggingChat is closing for now | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764 | huggingchat/chat-ui · [NEW] HuggingChat Omni | 2026-09-04 |
| https://github.com/huggingface/chat-ui | GitHub - huggingface/chat-ui: The open source codebase powering HuggingChat | 2026-09-04 |
| https://github.com/huggingface/chat-ui/blob/main/PRIVACY.md | chat-ui/PRIVACY.md at main · huggingface/chat-ui · GitHub | 2026-09-04 |
| https://huggingface.co/docs/chat-ui/en/configuration/web-search | Web Search · Hugging Face | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:huggingchat`, thread `huggingchat-launch`, 1 dated events 2023-04-25 → 2023-04-25.
- **Practical note:** From 2023-04-25, practitioners could use the public HuggingChat entry point as an early interface to an OpenAssistant-linked conversational model.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
