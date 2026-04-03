---
title: Fine-Tuning and LoRA
category: techniques
tags: [llm-agents, fine-tuning, lora, qlora, peft, training, model-customization]
---

# Fine-Tuning and LoRA

Fine-tuning adapts a pre-trained model to specific tasks, domains, or output styles. LoRA and PEFT methods make this practical on consumer hardware by training only a tiny fraction of parameters.

## Key Facts
- RAG for adding knowledge, fine-tuning for changing behavior/style - often combined in production
- Before fine-tuning, establish baselines: zero-shot, few-shot, RAG performance
- 100 high-quality examples > 10,000 noisy examples (quality >> quantity)
- LoRA trains 0.1-1% of total parameters, reducing GPU memory by 4-8x
- QLoRA combines LoRA with 4-bit quantization: 7B model fine-tuning on ~6GB VRAM

## When to Fine-Tune vs RAG

| Approach | Best For | Not For |
|----------|----------|---------|
| **RAG** | Domain knowledge, frequently updated data | Changing model behavior/style |
| **Fine-tuning** | Behavior, output format, domain adaptation | Real-time knowledge updates |
| **Both** | Complex production systems needing both |

## OpenAI Fine-Tuning

```python
# 1. Prepare JSONL training data
# Each line: {"messages": [{"role": "system",...}, {"role": "user",...}, {"role": "assistant",...}]}

# 2. Upload training file
file = client.files.create(file=open("training.jsonl"), purpose="fine-tune")

# 3. Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={"n_epochs": 3}
)

# 4. Use fine-tuned model
response = client.chat.completions.create(
    model="ft:gpt-4o-mini:my-org::abc123",
    messages=[...]
)
```

**Data requirements**: minimum 10 examples (50-100+ recommended), diverse, consistent format.

## LoRA (Low-Rank Adaptation)

Full fine-tuning updates ALL parameters. For a 7B model, that's 7 billion weights requiring massive GPU memory. LoRA decomposes weight updates into two small matrices:

```
W_new = W_original + A * B

W_original: frozen (e.g., 4096 x 4096)
A: trainable (e.g., 4096 x 16) - rank=16
B: trainable (e.g., 16 x 4096)
```

Result: ~130K trainable parameters per layer instead of 16M. 99% fewer parameters.

**Rank (r)**: controls expressiveness. Typical: 8, 16, 32, 64. Higher = more capacity, more memory.

### LoRA with HuggingFace PEFT

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable: 4,194,304 || all: 8,030,261,248 || trainable%: 0.05
```

### Target Modules
- `q_proj`, `v_proj` (attention queries/values) - most common, good default
- `k_proj` (attention keys) - added for more expressiveness
- `o_proj` (attention output)
- `gate_proj`, `up_proj`, `down_proj` (FFN) - for deeper adaptation

### Training Configuration
```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./lora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)
```

## QLoRA (Quantized LoRA)

Combines LoRA with quantization:
1. Quantize base model to 4-bit (NF4 format)
2. Add LoRA adapters in FP16
3. Train only LoRA parameters

**Memory savings**: 7B model goes from ~28GB (full) to ~6GB (QLoRA). Enables fine-tuning on consumer GPUs.

## PEFT Methods Comparison

| Method | Approach | Trainable Params |
|--------|----------|-----------------|
| **LoRA** | Low-rank weight update decomposition | 0.1-1% |
| **QLoRA** | LoRA + 4-bit quantization | 0.1-1% |
| **Prefix Tuning** | Trainable prefix tokens per layer | Very small |
| **Prompt Tuning** | Trainable soft prompt vectors | Tiny |
| **Adapter Layers** | Small trainable layers between frozen layers | 1-5% |

## Data Quality Guidelines

- Each example should demonstrate the exact behavior you want
- Remove duplicates, contradictions, low-quality samples
- Hold out 10-20% as test set
- Measure task-specific metrics (accuracy, BLEU, F1)
- Compare against baseline to verify improvement
- Check for overfitting (training metric improves but test doesn't)

## Gotchas
- Fine-tuning on small datasets risks overfitting - always validate on held-out set
- Fine-tuned models inherit the base model's limitations (hallucination, reasoning failures)
- LoRA adapters can be composed (merge multiple LoRA) but quality may degrade
- Hyperparameter tuning (rank, learning rate, epochs) significantly affects results
- Fine-tuned model quality degrades if training data format doesn't match inference format
- Always measure: sometimes prompt engineering + RAG outperforms fine-tuning

## See Also
- [[model-optimization]] - Quantization, distillation, pruning
- [[frontier-models]] - Base models available for fine-tuning
- [[ollama-local-llms]] - Running fine-tuned models locally
- [[rag-pipeline]] - Alternative to fine-tuning for knowledge
- [[prompt-engineering]] - Establish baseline before fine-tuning
