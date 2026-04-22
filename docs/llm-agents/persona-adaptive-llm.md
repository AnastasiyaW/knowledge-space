# Persona-Adaptive LLM (PersonaVLM Pattern)

Modeling persona state intrinsically in the model rather than injecting it via context. PersonaVLM (MiG-NJU, 2026) embeds a learnable persona-memory directly in the model weights, bypassing the context-window bottleneck of prompt-based personalization.

## Core Concept

**Problem with prompt-based persona:** Injecting user history as context (RAG or stuffing) consumes tokens, degrades with history length, and doesn't persist between sessions without explicit retrieval.

**Intrinsic persona-memory approach:**
- Fine-tuned persona state lives in model parameters
- Per-user PEFT (LoRA/adapter) captures individual behavioral patterns
- Inference: model "is" the personalized version, no context injection needed
- Tradeoff: requires per-user fine-tuning infrastructure

## PersonaVLM Architecture

**Base:** Qwen2.5-VL-7B-Instruct (vision + language)  
**Variants:** GGUF quants (~6GB at Q4_K_M), suitable for consumer GPU inference  
**Training:** PEFT on persona-specific interaction data

```text
User interaction history
        ↓
   Persona extractor (student modeling)
        ↓
   LoRA adapter per user
        ↓
   Qwen2.5-VL-7B + LoRA → personalized responses
```

## When to Use

| Scenario | Recommended Approach |
|----------|---------------------|
| Short sessions, diverse users | Prompt injection (RAG) |
| Long-running users, >100 interactions | Intrinsic persona (PEFT adapter per user) |
| Fixed teacher persona | Baked into base fine-tune |
| Dynamic student modeling | Persona-adaptive PEFT |
| Multi-persona (teacher + student) | **Unsolved** — two-adapter composition not validated |

## PEFT Serving for Per-User Adapters

Hot-swap LoRA adapters at inference time using vLLM multi-LoRA serving:

```python
# vLLM multi-LoRA serving pattern
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

llm = LLM(
    model="qwen2.5-vl-7b-instruct",
    enable_lora=True,
    max_loras=64,           # hot-swap pool size
    max_lora_rank=32,
    gpu_memory_utilization=0.85,
)

# Per-user request with their LoRA adapter
response = llm.generate(
    prompts=["Your lesson question here"],
    sampling_params=SamplingParams(temperature=0.7, max_tokens=512),
    lora_request=LoRARequest(
        lora_name=f"user_{user_id}",
        lora_int_id=user_id,
        lora_local_path=f"/adapters/user_{user_id}",
    ),
)
```

**Cost:** Adapter hot-swap adds ~2ms latency. 64 concurrent adapters use ~4GB VRAM overhead (32-rank LoRA, 7B model).

## Memory Integration Stack

For long-term personalization beyond what LoRA can capture:

| Layer | What it stores | Implementation |
|-------|----------------|----------------|
| Intrinsic (LoRA) | Behavioral style, preferences, communication patterns | PEFT adapter, updated periodically |
| Session memory | Current conversation state | In-context |
| Long-term RAG | Factual history, past exercises | MemPalace / vector store |
| Scheduler | Spaced repetition state | FSRS-7 algorithm |

## Open Problems

- **Two-persona composition:** Paper covers single-persona adaptation (e.g. student-adaptive teacher). Using two simultaneous adapters (teacher style + student model) is unstested. Naive sum of LoRA weights degrades both.
- **Adapter staleness:** As user evolves, old adapter becomes less accurate. Requires periodic re-fine-tuning or online update strategy.
- **Cold-start:** New users have no adapter. Fallback to prompt injection until 50+ interactions collected.
- **Privacy:** Per-user LoRA weights encode behavioral patterns. Treat as PII for storage/deletion purposes.

## Gotchas

- **Issue:** GGUF quants lose LoRA compatibility — standard GGUF format bakes weights, can't hot-swap adapters. -> **Fix:** Use full-precision or GPTQ for adapter-serving deployment. GGUF only for single-user offline use.
- **Issue:** Qwen2.5-VL requires specific vision preprocessing — images must be padded to multiples of 28px before passing to ViT. -> **Fix:** Use the official `AutoProcessor` from HuggingFace, don't resize manually.

## See Also

- [[agent-memory]]
- [[llm-fine-tuning-practical]]
- [[kv-cache-compression]]
