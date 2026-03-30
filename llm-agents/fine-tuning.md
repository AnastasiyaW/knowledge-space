---
title: Fine-Tuning LLMs
category: llm-agents/training
tags: [fine-tuning, lora, qlora, peft, sft, rlhf, training, model-customization]
---

# Fine-Tuning LLMs

## Key Facts

- Fine-tuning adjusts model weights on task-specific data to change model **behavior**, not just add knowledge
- Three training phases: **pre-training** (massive text corpus, expensive) -> **fine-tuning/SFT** (question-answer pairs, cheaper) -> **RLHF** (human preference feedback)
- Pre-training: 10TB+ text, requires massive GPU clusters. Creates the base model (e.g., Llama base)
- SFT (Supervised Fine-Tuning): ~100K+ Q&A examples teaching response style. Much cheaper than pre-training
- RLHF: human raters score outputs, model learns preferences. Final polish step
- **LoRA** (Low-Rank Adaptation): trains only small adapter matrices, not full model weights. ~1% of parameters
- **QLoRA**: LoRA + 4-bit quantization. Fine-tune 70B models on a single GPU
- RAG adds knowledge, fine-tuning changes behavior. [[rag-pipeline]] is usually tried first due to lower cost

## Patterns

```python
# OpenAI fine-tuning (API, simplest approach)
from openai import OpenAI
client = OpenAI()

# Prepare JSONL training data
# {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}

# Upload training file
file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={"n_epochs": 3}
)

# Use fine-tuned model
response = client.chat.completions.create(
    model="ft:gpt-4o-mini:my-org::abc123",  # fine-tuned model ID
    messages=[{"role": "user", "content": "..."}]
)
```

```python
# LoRA fine-tuning with HuggingFace PEFT
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,              # rank (lower = fewer params, less expressive)
    lora_alpha=32,     # scaling factor
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"]  # which layers to adapt
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: ~0.5% of total

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=TrainingArguments(
        output_dir="./lora_output",
        per_device_train_batch_size=4,
        num_train_epochs=3,
        learning_rate=2e-4,
    )
)
trainer.train()
```

```python
# QLoRA - 4-bit quantized LoRA (fit large models on consumer GPU)
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"
)
# Now apply LoRA config as above
```

## Gotchas

- **RAG first, fine-tune second**: fine-tuning is more expensive and harder to iterate on. Try RAG first
- **Data quality > quantity**: 1000 high-quality examples beat 100K noisy ones
- **Catastrophic forgetting**: fine-tuning can degrade model's general capabilities. Use LoRA to minimize this
- **Evaluation is critical**: always hold out test data and measure with [[llm-evaluation]] before deploying
- **LoRA rank tradeoff**: higher r = more expressive but more memory/compute. Start with r=8 or r=16
- **OpenAI fine-tuning costs**: training + per-token inference surcharge. Can get expensive at scale
- **Merging adapters**: LoRA adapters can be merged back into the base model for inference speed

## See Also

- [[rag-pipeline]] - alternative approach to adding knowledge
- [[huggingface-transformers]] - HuggingFace ecosystem for training
- [[model-selection]] - choosing the right base model
- [[llm-evaluation]] - measuring fine-tuned model quality
- https://huggingface.co/docs/peft - PEFT library documentation
- https://platform.openai.com/docs/guides/fine-tuning - OpenAI fine-tuning guide
- https://huggingface.co/docs/trl - TRL (Transformer Reinforcement Learning)
