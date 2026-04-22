# Recurrent-Depth Transformer (RDT) Architecture

Looped transformer architecture that reuses a single block T times to simulate multi-step reasoning without generating visible tokens. 770M looped ≈ 1.3B standard quality (Parcae, arxiv 2604.12946).

## Three-Stage Forward Pass

```text
Input → Prelude (N layers, once) → Recurrent Block (× T loops) → Coda (N layers, once) → Logits
```

**Prelude:** Standard transformer layers (default 2). Encodes input to hidden state `e`.

**Recurrent Block update rule:**
```text
h_{t+1} = A * h_t + B * e + Transformer(h_t, e)
```
- `e` = Prelude output, injected every iteration
- `A`, `B` = diagonal LTI injection parameters, constrained to spectral radius < 1
- Ensures convergence: `rho(A) < 1` prevents hidden state explosion

**Coda:** Final layers (default 2) run once, produce logits.

## Key Components

| Component | Purpose | Source |
|-----------|---------|--------|
| **MoE FFN** | Expert routing (DeepSeek-style: shared + routed) | arxiv 2401.06066 |
| **Depth-wise LoRA** | Per-iteration rank-r adapters → each loop is functionally distinct despite weight sharing | arxiv 2410.20672 |
| **ACT halting** | Per-token variable loop depth (easy tokens exit early) | arxiv 1807.03819 |
| **MLA attention** | Multi-Latent Attention, compresses KV cache to latent vectors | DeepSeek-V2 |
| **LTI stability** | Spectral radius < 1 via diagonal parameterization, solves training instability | arxiv 2604.12946 |

## Scaling Properties (Parcae 2604.12946)

- **Param efficiency:** 770M looped = quality of 1.3B standard transformer
- **Optimal depth:** power-law relationship between loop count T and token count N
- **Grokking stages** (arxiv 2604.07822): memorization → in-distribution generalization → systematic OOD generalization (train 5-hop, test 10-hop)
- Training instability solved by spectral constraint on A matrix

## Latent Reasoning vs Chain-of-Thought

Formal equivalence: T loop iterations simulate T steps of CoT in continuous latent space (Saunshi et al., arxiv 2502.17416).

| Property | Latent Reasoning (RDT loops) | Chain-of-Thought (token generation) |
|----------|------------------------------|--------------------------------------|
| Thinking cost | Add compute per loop, no token overhead | Autoregressive token generation |
| Context consumed | Zero thinking tokens | Thinking tokens fill context |
| Interpretability | None (hidden state) | Full trace visible |
| Hypotheses | Multiple simultaneously (breadth-first) | Sequential (depth-first) |
| Variable compute | ACT halting per token | Fixed or budget-based |

## Inference Implications

**If deployed at scale:**
- Inference cost = f(loop_count), not f(param_count). Simple queries = fewer loops = cheaper.
- Context window: 200K tokens = 200K user content, no thinking token budget.
- MLA compression: KV cache stores only latent vectors, not full K/V matrices.
- Continuous depth-wise batching: process easy/hard requests at different loop depths in the same batch → ~2-3x throughput (theoretical).

## Gotchas

- **Issue:** Spectral radius constraint is necessary, not optional. Without `rho(A) < 1`, looped models diverge during training. -> **Fix:** Parameterize A as a diagonal matrix and apply `tanh` or clamp to enforce stability. See Parcae for exact implementation.
- **Issue:** ACT halting required to prevent "overthinking." More loops eventually hurts due to composition bias — the model memorizes rather than generalizing. -> **Fix:** Adaptive Computation Time mechanism (Graves 2016, arxiv 1807.03819) adds a halting probability per token per loop.
- **Issue:** Depth-wise LoRA adapters are needed per loop iteration. Without them, all loops are identical: `h_{t+1} = Transformer(h_t, e)` with the same weights produces decreasing marginal utility. -> **Fix:** Small rank-r LoRA (r=4-16) added to each loop iteration's attention and/or MLP.
- **Issue:** KV cache management unclear for variable-depth batching in production. Tokens in the same batch may exit at different loop counts. -> **Fix:** Known open problem; current implementations pad to max T for simplicity.

## Paper Reference Map

| arxiv ID | Title | Key claim |
|----------|-------|-----------|
| 2604.12946 | Parcae | 770M looped = 1.3B standard; spectral stability |
| 2604.07822 | Loop, Think & Generalize | 3-stage grokking, depth extrapolation |
| 2502.17416 | Reasoning with Latent Thoughts | T loops ≡ T CoT steps formally |
| 2412.06769 | COCONUT | Practical latent-space reasoning (Meta AI) |
| 2410.20672 | Relaxed Recursive Transformers | Depth-wise LoRA |
| 1807.03819 | Universal Transformers | ACT halting mechanism |

## See Also

- [[diffusion-inference-acceleration]]
- [[kv-cache-compression]]
- [[llm-fine-tuning-practical]]
