# Practical LLM Fine-Tuning

End-to-end guide for fine-tuning LLMs on custom tasks. Covers both frontier model fine-tuning (via API) and open-source model fine-tuning with QLoRA. Includes the failure modes - fine-tuning does NOT always help.

## When Fine-Tuning Helps vs Hurts

Fine-tuning is most effective when:
- Task requires consistent output FORMAT (JSON, specific schema)
- Domain has specialized vocabulary not well-represented in pre-training
- You have high-quality examples of desired behavior (hundreds to thousands)
- You need to reduce prompt length (bake instructions into weights)

Fine-tuning often DOES NOT help when:
- The task requires broad reasoning (better to use a bigger base model)
- Training data is small (<100 examples) or noisy
- The task is already well-served by few-shot prompting
- You are trying to add factual knowledge (RAG is usually better)

## Frontier Model Fine-Tuning (OpenAI API)

Training data format - JSONL with chat messages:

```json
{"messages": [{"role": "system", "content": "You are a price estimator."}, {"role": "user", "content": "Estimate the price of: Sony WH-1000XM5 headphones"}, {"role": "assistant", "content": "349.99"}]}
{"messages": [{"role": "system", "content": "You are a price estimator."}, {"role": "user", "content": "Estimate the price of: Apple AirPods Pro 2"}, {"role": "assistant", "content": "249.00"}]}
```

```python
from openai import OpenAI
client = OpenAI()

# Upload training file
file = client.files.create(file=open("train.jsonl", "rb"), purpose="fine-tune")

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={"n_epochs": 3}
)

# Monitor progress
client.fine_tuning.jobs.retrieve(job.id)

# Use fine-tuned model
response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:org-id::job-id",
    messages=[{"role": "user", "content": "Price of MacBook Air M3?"}]
)
```

## Open-Source Fine-Tuning with QLoRA

QLoRA: quantize base model to 4-bit, train small LoRA adapters. Dramatically reduces GPU memory requirements.

### Key Hyperparameters

| Parameter | Typical Value | Effect |
|-----------|--------------|--------|
| **Learning rate** | 1e-4 to 2e-4 | How much weights shift per step. Lower = more stable |
| **LoRA rank (r)** | 8-64 | Adapter capacity. Higher = more expressive, more memory |
| **LoRA alpha** | 16-128 | Scaling factor, usually 2x rank |
| **LoRA dropout** | 0.05-0.1 | Regularization within adapter |
| **Batch size** | 4-16 | Samples per step. Larger = more stable gradients |
| **Gradient accumulation** | 1-8 | Simulates larger batch size without more memory |
| **Epochs** | 1-5 | Full passes through training data |
| **Optimizer** | adamw_8bit | Memory-efficient Adam. Good default |

### Learning Rate Scheduling

Start with a learning rate, then gradually reduce:
- As the model gets better, want smaller adjustments (fine-tuning, not wholesale changes)
- Cosine schedule is standard: warm up for ~10% of steps, then decay
- If training loss oscillates wildly, learning rate is too high
- If training loss decreases very slowly, learning rate is too low

### Gradient Accumulation

Instead of forward pass -> backward pass -> update weights on every sample:
1. Forward pass -> compute gradients (don't update)
2. Repeat for N steps, accumulating gradients
3. Update weights once using accumulated gradients

Effect: simulates a batch size of N * actual_batch_size. Speeds up training at the cost of slightly less granular updates.

```python
from transformers import TrainingArguments
from trl import SFTTrainer
from peft import LoraConfig

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # effective batch = 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    args=training_args,
    max_seq_length=512
)
trainer.train()
```

## Monitoring with Weights & Biases

```python
import wandb
wandb.init(project="my-finetune", name="run-1")

# TrainingArguments automatically logs to W&B if installed
training_args = TrainingArguments(
    report_to="wandb",
    # ...
)
```

Key metrics to watch:
- **Training loss** should decrease steadily
- **Eval loss** should decrease then plateau (overfitting if it rises)
- **Learning rate** curve should show warmup then decay

## Loading a Fine-Tuned LoRA Model

The LoRA adapter is separate from the base model. Loading requires both:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Apply LoRA weights on top
model = PeftModel.from_pretrained(base_model, "./lora-adapter-path")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
```

## Five-Step Problem-Solving Strategy

1. **Define the business problem** and success metric
2. **Collect and prepare data** - quality > quantity
3. **Establish baseline** - test the base model without fine-tuning
4. **Fine-tune** frontier model (API) AND/OR open-source model (QLoRA)
5. **Evaluate** against baseline on your business metric, not generic benchmarks

## Gotchas

- **Fine-tuning can make things worse.** If training data is noisy or the task does not benefit from specialization, the fine-tuned model may underperform the base model on your actual metric.
- **Biggest outlier reduction != better average.** A fine-tuned model may fix extreme errors while slightly worsening average performance. Always measure the metric you actually care about.
- **LoRA target modules matter.** Different modules have different effects. `q_proj` + `v_proj` is the minimum viable set; adding `k_proj`, `o_proj`, and MLP layers increases capacity but also memory and training time.
- **You cannot just load a LoRA model directly.** You must first load the base model, then apply the LoRA adapter. Forgetting this step is a common source of confusion.

## Cross-References

- [[fine-tuning]] - general fine-tuning concepts
- [[model-optimization]] - quantization techniques (4-bit, 8-bit)
- [[scaling-laws-and-benchmarks]] - when bigger models vs fine-tuning
- [[rag-pipeline]] - alternative to fine-tuning for adding knowledge
