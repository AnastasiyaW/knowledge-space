---
title: Ollama and Local LLMs
category: infrastructure
tags: [llm-agents, ollama, local-llm, open-source, llama, mistral, privacy, quantization]
---

# Ollama and Local LLMs

Ollama provides a simple way to run open-source LLMs locally. Complete data privacy, no API costs after download, offline capability, and full customization. The tradeoff is hardware requirements and lower capability than frontier closed-source models.

## Key Facts
- Full data privacy - nothing leaves your machine
- No cost after download - free forever
- Works offline - no internet required
- Server endpoint: `http://localhost:11434`
- Start with Q4 8B model - if it runs smoothly, try larger
- Open-source models are not yet at GPT-4/Claude level but the gap is narrowing rapidly

## Setup

```bash
# Install from ollama.com, then:
ollama run llama3.1:8b          # Download + run interactively
ollama list                      # Show downloaded models
ollama serve                     # Start API server (port 11434)
/bye                             # Exit interactive session
```

## Hardware Requirements

| Model Size | VRAM Needed | Hardware |
|------------|-------------|----------|
| 8B params | 8-16 GB | Consumer GPUs (RTX 4060+) |
| 70B params | 40+ GB | Professional workstations |
| 405B params | Multiple H100s | Impractical for local use |

## Quantization Levels

| Quant | Quality | Size (8B) | Recommendation |
|-------|---------|-----------|----------------|
| Q2 | Very low | Smallest | Not recommended |
| Q4 | Good | ~4GB | Best starting point |
| Q5 | Better | ~5GB | If Q4 runs well |
| Q6 | High | ~6GB | Strong GPU |
| Q8 | Near-original | ~8GB | RTX 4060+ |
| fp16 | Original | ~16GB | Needs >= 16GB VRAM |

```bash
ollama run llama3.1:8b-instruct-q4_0  # Q4 quantized
ollama run llama3.1:8b-instruct-q8_0  # Q8 quantized
```

## Recommended Models

| Model | Strength |
|-------|----------|
| **Llama 3.1 8B** | Best open-source for local use, competitive with GPT-3.5 |
| **Llama 3.1 70B** | Beats GPT-3.5 in benchmarks |
| **Gemma 2** | Strong alternative from Google |
| **Mistral** | Good general-purpose |
| **Qwen 2** | Strong multilingual |
| **DeepSeek Coder** | Specialized for code |
| **Phi-3** | Small but capable (Microsoft) |
| **Dolphin-Llama3** | Uncensored variant |

**Dolphin models**: fine-tuned to remove alignment/censorship. Useful for unrestricted local use.

## Groq API - Fast Inference Alternative

When local hardware is insufficient, Groq provides fast inference via LPU (Language Processing Unit):
- Much faster than GPU-based inference
- Works with open-source models (Llama 3.1, etc.)
- Free tier available, cheap paid pricing
- OpenAI-compatible API format

## Integration Patterns

### FlowWise
1. Add "Chat Ollama" node
2. Set base URL: `http://localhost:11434`
3. Set model name (e.g., `llama3.1:8b`)
4. Connect to supervisor/chain as usual

### LangChain
```python
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3.1:8b", temperature=0)
response = llm.invoke("Hello, world!")
```

### Local RAG Stack
- **Chat model**: Chat Ollama
- **Embeddings**: Ollama Embeddings (same server)
- **Vector store**: In-memory or Chroma
- **Document loader**: PDFs, text files, web scraper
- **Text splitter**: Recursive character (chunk 700-1000, overlap 50-100)
- **Memory**: Buffer memory for conversation context

Entirely local, free, private.

### Local Email Agent
Three-agent pipeline on Ollama:
1. **Email Summarizer** - reads email, produces summary
2. **Email Responder** - generates reply in user's style (via RAG on sample emails)
3. **Email Formatter** - formats and saves to file

Complete privacy for email processing.

## Gotchas
- Small quantized models produce errors with complex agent workflows - use capable models for agents
- Must upsert documents into vector store before RAG works - the #1 FlowWise mistake
- Local models are significantly slower than API models without GPU acceleration
- CPU-only inference works but is very slow for models > 3B parameters
- Ollama downloads models on first use - plan for download time on slow connections
- Quality degrades noticeably below Q4 quantization for most tasks
- Function calling is less reliable with local models than with GPT-4 or Claude

## See Also
- [[frontier-models]] - Comparing local vs cloud model capabilities
- [[model-optimization]] - Quantization formats and techniques
- [[no-code-platforms]] - FlowWise integration with Ollama
- [[rag-pipeline]] - Building local RAG with Ollama
- [[fine-tuning]] - Customizing local models
