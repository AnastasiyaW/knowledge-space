---
title: HuggingFace and Transformers
category: llm-agents/frameworks
tags: [huggingface, transformers, pipeline, model-hub, tokenizer, inference, open-source]
---

# HuggingFace and Transformers

## Key Facts

- HuggingFace is the central hub for open-source ML models, datasets, and tools
- The `transformers` library provides unified API to load and run 400K+ models
- Two API levels: **Pipeline** (simple, high-level) and **Model+Tokenizer** (fine-grained control)
- Model Hub: download pre-trained models by name (e.g., `meta-llama/Llama-3.2-3B-Instruct`)
- Key libraries: `transformers` (models), `datasets` (data), `peft` (efficient fine-tuning), `trl` (RL training), `accelerate` (multi-GPU)
- Inference API: run models in the cloud without local GPU via `huggingface_hub` client
- Model cards: documentation on each model's capabilities, limitations, and training data
- MTEB leaderboard: benchmark for [[embeddings]] model quality

## Patterns

```python
# Pipeline API (simplest - auto-downloads model)
from transformers import pipeline

# Text generation
generator = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
result = generator("Explain RAG:", max_new_tokens=200)

# Sentiment analysis
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
result = summarizer(long_text, max_length=130, min_length=30)
```

```python
# Model + Tokenizer (fine-grained control)
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "meta-llama/Llama-3.2-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"  # automatic GPU placement
)

inputs = tokenizer("Hello, how are you?", return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100, temperature=0.7)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

```python
# HuggingFace Inference API (cloud, no local GPU needed)
from huggingface_hub import InferenceClient

client = InferenceClient(model="meta-llama/Llama-3.2-3B-Instruct")
response = client.text_generation(
    "What is machine learning?",
    max_new_tokens=200
)

# Chat completion (OpenAI-compatible)
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=500
)
```

```python
# Sentence Transformers for embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(["cat", "dog", "car"])
similarity = model.similarity(embeddings[0], embeddings[1])
```

## Gotchas

- **Model access**: some models (Llama, Gemma) require accepting a license on HuggingFace before download
- **Disk space**: models range from 500MB (small) to 140GB+ (70B). Plan storage accordingly
- **GPU memory**: loading models in full precision requires significant VRAM. Use `torch_dtype=torch.bfloat16` or quantization
- **device_map="auto"**: automatically splits model across available GPUs. Essential for large models
- **Tokenizer padding**: batch inference requires padding. Set `tokenizer.pad_token = tokenizer.eos_token` if missing
- **Cache location**: models cache in `~/.cache/huggingface/`. Can fill disk fast. Set `HF_HOME` to redirect
- **Pipeline vs raw**: Pipeline is easy but hides important details. Use Model+Tokenizer for production

## See Also

- [[fine-tuning]] - training models with HuggingFace PEFT/TRL
- [[embeddings]] - sentence-transformers for vector representations
- [[ollama-local-llms]] - simpler alternative for running models locally
- [[model-selection]] - choosing models from the Hub
- https://huggingface.co/models - Model Hub
- https://huggingface.co/docs/transformers - Transformers documentation
- https://huggingface.co/docs/peft - PEFT (Parameter-Efficient Fine-Tuning)
