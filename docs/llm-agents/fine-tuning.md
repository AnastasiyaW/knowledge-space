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

```yaml
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

### QLoRA Training with SFTTrainer

```python
from trl import SFTTrainer, SFTConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
import torch

# 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
tokenizer = AutoTokenizer.from_pretrained(model_name)

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
                         lora_dropout=0.05, task_type="CAUSAL_LM")

sft_config = SFTConfig(
    output_dir="./qlora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    report_to="wandb",  # Weights & Biases integration
)

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=dataset,
    peft_config=lora_config,
    processing_class=tokenizer
)
trainer.train()
```

**TRL library** (Transformers Reinforcement Learning) provides `SFTTrainer` which wraps HuggingFace `Trainer` with fine-tuning-specific features: chat template handling, dataset formatting, LoRA integration.

### GPU Selection for QLoRA

| GPU | VRAM | QLoRA 7B | QLoRA 13B | Notes |
|-----|------|----------|-----------|-------|
| T4 | 16GB | Comfortable | Tight | Free tier on Colab |
| A100 40GB | 40GB | Fast | Comfortable | ~$1/hr on Colab Pro |
| RTX 4090 | 24GB | Good | Possible with small batch | Consumer option |

For T4: reduce `per_device_train_batch_size` to 1-2 and increase `gradient_accumulation_steps`.

### Monitoring with Weights & Biases

```python
import wandb
wandb.login()  # or set WANDB_API_KEY environment variable

# In TrainingArguments / SFTConfig:
# report_to="wandb"
# run_name="qlora-llama3-experiment-1"
```

W&B automatically tracks: loss curves, learning rate schedule, GPU utilization, gradient norms. For OpenAI fine-tuning: link your W&B API key in the OpenAI dashboard Settings -> Integrations section to visualize training progress.

## PEFT Methods Comparison

| Method | Approach | Trainable Params |
|--------|----------|-----------------|
| **LoRA** | Low-rank weight update decomposition | 0.1-1% |
| **QLoRA** | LoRA + 4-bit quantization | 0.1-1% |
| **Prefix Tuning** | Trainable prefix tokens per layer | Very small |
| **Prompt Tuning** | Trainable soft prompt vectors | Tiny |
| **Adapter Layers** | Small trainable layers between frozen layers | 1-5% |

## LoRA Hyperparameter Tuning

### Rank (r)
Controls the capacity of LoRA adaptation. Higher rank = more expressiveness but more memory and risk of overfitting.

| Rank | Use Case | Notes |
|------|----------|-------|
| 4-8 | Simple task adaptation (classification, formatting) | Start here |
| 16 | General-purpose fine-tuning | Good default |
| 32-64 | Complex domain adaptation, multi-task | When lower ranks underperform |
| 128+ | Rarely needed | Diminishing returns |

### Alpha (lora_alpha)
Scaling factor for LoRA updates. Effective scaling = alpha / r. Common practice: set alpha = 2 * r (e.g., r=16, alpha=32).

### Dropout (lora_dropout)
Regularization for LoRA layers. Typical: 0.05-0.1. Helps prevent overfitting on small datasets.

### Target Module Selection Strategy
- **Minimum viable**: `q_proj`, `v_proj` - attention queries and values only. Good starting point
- **More capacity**: add `k_proj`, `o_proj` - full attention adaptation
- **Maximum**: add `gate_proj`, `up_proj`, `down_proj` - adapts FFN layers too. Use when attention-only is insufficient

## Quantization Impact on Fine-Tuning Quality

Quantization reduces model precision to save memory, but impacts performance differently across tasks:

- **Full precision (FP32/BF16)**: baseline quality, highest memory
- **8-bit quantization**: ~1-2% quality drop, 2x memory reduction
- **4-bit (NF4/GPTQ)**: ~3-5% quality drop, 4x memory reduction
- **Impact varies by task**: simple classification barely affected, complex reasoning shows more degradation

Run your evaluation suite across quantization levels to find the sweet spot:

```python
from transformers import BitsAndBytesConfig

# 4-bit quantization config for QLoRA
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True  # nested quantization saves extra memory
)

model = AutoModelForCausalLM.from_pretrained(
    model_name, quantization_config=bnb_config
)
```

## Dataset Preparation for Fine-Tuning

### Finding and Crafting Datasets
- **Existing datasets**: HuggingFace Hub, Kaggle. Filter for task-specific quality
- **Synthetic generation**: use a stronger model (GPT-4) to generate training data for a smaller model
- **Manual curation**: highest quality, most expensive. Even 100 expert-curated examples can be transformative
- **Format consistency**: every example must follow the exact format expected during inference

### Conversation Format
```json
{"messages": [
  {"role": "system", "content": "You are a pricing assistant..."},
  {"role": "user", "content": "Price for item X?"},
  {"role": "assistant", "content": "$42.99"}
]}
```

System prompt should be identical across all training examples and match inference-time system prompt.

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
- **Quantization affects tasks unevenly** - always benchmark YOUR specific task at each precision level, not just overall perplexity
- **lora_alpha/r ratio matters more than absolute values** - alpha=32/r=16 and alpha=64/r=32 behave similarly
- **System prompt mismatch** - if training uses a system prompt but inference doesn't (or vice versa), quality drops significantly
- **Double quantization** (`bnb_4bit_use_double_quant=True`) provides additional memory savings with minimal quality impact

## See Also
- [[model-optimization]] - Quantization, distillation, pruning
- [[frontier-models]] - Base models available for fine-tuning
- [[ollama-local-llms]] - Running fine-tuned models locally
- [[rag-pipeline]] - Alternative to fine-tuning for knowledge
- [[prompt-engineering]] - Establish baseline before fine-tuning
