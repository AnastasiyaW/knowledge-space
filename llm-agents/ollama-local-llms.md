---
title: Ollama and Local LLMs
category: llm-agents/infrastructure
tags: [ollama, local-llm, self-hosted, open-source, llama, mistral, privacy, on-device]
---

# Ollama and Local LLMs

## Key Facts

- Ollama runs open-source LLMs locally on your machine via optimized C++ inference
- Zero API cost, full data privacy - nothing leaves your computer
- Supported models: Llama 3.x, Mistral, Qwen 2.5, Gemma 2, Phi-3, DeepSeek, CodeLlama, and 100+ more
- Hardware requirements: minimum 8GB RAM for 7B models, 16GB+ for 13B, 32GB+ for 70B (quantized)
- Apple Silicon Macs run local LLMs significantly faster than x86 due to unified memory architecture
- Ollama exposes an OpenAI-compatible API at `localhost:11434` - drop-in replacement for OpenAI SDK
- Trade-off: local models (2B-70B params) are less capable than frontier models (rumored 1T+ params) but free and private
- Can be used as workers in [[multi-agent-systems]] or for [[rag-pipeline]] with local embeddings

## Patterns

```bash
# Install and run
# Download from ollama.com, then:
ollama run llama3.2        # 3B model, fast
ollama run qwen2.5:7b      # Strong multilingual
ollama run mistral          # Good general purpose
ollama run codellama:13b    # Code-focused

# List downloaded models
ollama list

# Pull without running
ollama pull llama3.2:latest
```

```python
# Use Ollama with OpenAI SDK (compatible API)
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # required but unused
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain RAG in 3 sentences."}
    ]
)
print(response.choices[0].message.content)
```

```python
# Ollama with LangChain
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

llm = Ollama(model="llama3.2")
result = llm.invoke("What is machine learning?")

# Local embeddings (no API cost)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector = embeddings.embed_query("Hello world")
```

```python
# Ollama Python library (native)
import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response["message"]["content"])

# Streaming
for chunk in ollama.chat(model="llama3.2", messages=messages, stream=True):
    print(chunk["message"]["content"], end="")
```

## Gotchas

- **Quality gap**: local 7B model ~ GPT-3.5 level. For tasks requiring GPT-4 quality, use API
- **First run downloads**: `ollama run model` downloads the model weights first time (can be several GB)
- **VRAM limits**: model must fit in RAM/VRAM. 70B models need quantization (Q4) to fit in 32GB
- **Speed varies**: Apple M1/M2/M3 is fast. Older CPUs without AVX2 are very slow
- **Context window**: many local models have 4K-8K context by default. Check model card
- **Function calling support**: not all local models support tool use. Llama 3.1+ and Mistral do
- **No GPU fallback**: without GPU/Apple Silicon, inference on CPU is 5-20x slower

## See Also

- [[model-selection]] - when to use local vs API models
- [[api-integration]] - Ollama exposes OpenAI-compatible API
- [[rag-pipeline]] - building RAG with local models and embeddings
- [[fine-tuning]] - fine-tuning open-source models locally
- https://ollama.com/ - Ollama official site
- https://ollama.com/library - available models
- https://github.com/ollama/ollama - Ollama source code
