---
title: "Ollama and Local LLMs (September 2026)"
category: infrastructure
tags: [llm-agents, ollama, local-llm, structured-output, observability]
---

# Ollama and Local LLMs (September 2026)

Reviewed 2026-09-03. Ollama provides a local runtime and API surface for running compatible models. A local endpoint changes the deployment boundary; it does not by itself prove privacy, model provenance, license compliance, or sufficient quality for a workload.

## Runtime Contract

| Concern | What to record |
|---|---|
| Model | Exact tag and immutable artifact digest where available |
| Host | CPU/GPU, memory, driver, and runtime version |
| Endpoint | Local bind address, network exposure, authentication path |
| Data path | Prompts, files, tools, telemetry, and any cloud configuration |
| Quality | Evaluation set, tokenizer, quantization, and validation result |
| Operations | Load latency, generation latency, errors, and keep-alive policy |

Ollama documents its local API, streaming behavior, structured outputs, tool calling, and usage metrics. Treat the current official API reference as the authority for request fields and supported capabilities. [Ollama API](https://docs.ollama.com/) [Structured outputs](https://docs.ollama.com/capabilities/structured-outputs)

## Structured Local Call

This request asks for a non-streaming response constrained to a JSON schema. Use a model you have explicitly pulled and evaluated for the task.

```bash
ollama pull gemma3
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma3",
    "stream": false,
    "messages": [{"role": "user", "content": "Return one city and its country."}],
    "format": {
      "type": "object",
      "properties": {
        "city": {"type": "string"},
        "country": {"type": "string"}
      },
      "required": ["city", "country"]
    }
  }'
```

Validate the returned JSON in application code. A schema request reduces formatting failures; it does not verify factual accuracy.

## Streaming vs Non-Streaming

| Mode | Use when | Operator concern |
|---|---|---|
| Streaming | Long interactive output and progressive UI | Handle newline-delimited events and cancellation |
| Non-streaming | Short output, structured validation, or batch logic | Bound end-to-end timeout and response size |

The Ollama API documents streaming as the default for selected endpoints and non-streaming JSON responses when the request disables streaming. [Streaming](https://docs.ollama.com/api/streaming)

## Tool Calls and Metrics

Tool calls still need an application-controlled loop: inspect the request, validate the tool and arguments, execute under policy, then return the result. Ollama also documents response metrics such as load, prompt-evaluation, and evaluation durations. Use them with your run ID and model tag; a latency number without workload identity is not comparable. [Tool calling](https://docs.ollama.com/capabilities/tool-calling) [Usage metrics](https://docs.ollama.com/api/usage)

## Capacity Planning

- Measure a representative prompt and output length on the actual host.
- Set concurrency from observed memory and latency, not parameter-count folklore.
- Record the quantization and context configuration with every evaluation.
- Separate cold-start/load latency from token generation latency.
- Reject or queue work when capacity is exhausted; do not silently route private input to a different provider.

## Gotchas

- **Issue: Assuming localhost means all data stays local.** Cloud models, remote tools, telemetry, download sources, and network binding can alter the data path. **Fix:** review the complete deployment and network configuration.
- **Issue: Treating a model tag as immutable.** A tag can be updated or selected differently across hosts. **Fix:** record the evaluated artifact identity and deploy the same pinned artifact.
- **Issue: Using structured output without application validation.** A model can still return malformed or semantically invalid values. **Fix:** parse and validate against the same schema used for the request.
- **Issue: Comparing throughput without separating load time.** A warm model and a cold model answer different operational questions. **Fix:** record load and generation metrics separately.

## See Also

- [[function-calling]]
- [[tool-use-patterns]]
- [[frontier-models]]
- [[model-optimization]]
- [[agent-observability-dashboards]]

## Sources

- [Ollama documentation](https://docs.ollama.com/)
- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
- [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling)
- [Ollama usage metrics](https://docs.ollama.com/api/usage)
