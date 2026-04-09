---
title: "Gradio for LLM Interfaces"
description: "Rapid prototyping of chat UIs with streaming, markdown rendering, and multi-model comparison dashboards"
---

# Gradio for LLM Interfaces

Gradio provides rapid prototyping of web UIs for LLM applications. From simple chat interfaces to multi-model comparison dashboards, it handles streaming, markdown rendering, and model switching with minimal code.

## Minimal Chat Interface

```python
import gradio as gr
from openai import OpenAI

client = OpenAI()

def chat(message, history):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content

demo = gr.ChatInterface(fn=chat)
demo.launch()
```

## Streaming Responses

Gradio detects generator functions and automatically renders streaming typewriter-style output.

```python
def stream_gpt(message, history):
    messages = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    result = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            result += content
            yield result  # MUST yield cumulative result, not individual chunks

demo = gr.ChatInterface(fn=stream_gpt)
demo.launch()
```

**Critical**: yield the cumulative string, not individual chunks. If you yield only the current chunk, Gradio replaces the previous text instead of appending.

## Markdown Rendering

Replace `gr.Textbox` output with `gr.Markdown` for formatted responses:

```python
def ask_llm(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Respond in well-formatted Markdown."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

demo = gr.Interface(fn=ask_llm, inputs="text", outputs=gr.Markdown())
demo.launch()
```

## Multi-Model Comparison

```python
import anthropic

anthropic_client = anthropic.Anthropic()

def stream_claude(message, history):
    result = ""
    with anthropic_client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": message}]
    ) as stream:
        for text in stream.text_stream:
            result += text
            yield result

def chat_with_model(message, history, model_choice):
    if model_choice == "GPT-4o":
        yield from stream_gpt(message, history)
    else:
        yield from stream_claude(message, history)

demo = gr.ChatInterface(
    fn=chat_with_model,
    additional_inputs=[
        gr.Dropdown(["GPT-4o", "Claude"], label="Model", value="GPT-4o")
    ]
)
demo.launch()
```

## Key Differences: OpenAI vs Anthropic Streaming

| Feature | OpenAI | Anthropic |
|---------|--------|-----------|
| Stream parameter | `stream=True` in create() | Use `.stream()` instead of `.create()` |
| Max tokens | Optional (has default) | **Required** parameter |
| System message | In messages list | Separate `system=` parameter |
| Chunk access | `chunk.choices[0].delta.content` | Context manager + `.text_stream` |

## Advanced: Log Viewer and Plots

```python
import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        chatbot = gr.Chatbot()
        log_output = gr.Textbox(label="Agent Logs", lines=10)

    with gr.Row():
        msg = gr.Textbox(label="Message")
        send = gr.Button("Send")

    # Optional: add plots, tables, images
    plot = gr.Plot(label="Vector Space")
    table = gr.Dataframe(label="Results")

    send.click(fn=process, inputs=[msg], outputs=[chatbot, log_output, table])
```

## Gotchas

- **Streaming must yield cumulative text.** Yielding individual chunks causes flickering - each yield replaces the entire output, so you must yield the full text so far.
- **Gradio auto-detects generators.** If your function uses `yield`, Gradio treats it as streaming. If it uses `return`, it waits for the full response. No configuration needed.
- **Long-running operations blank interactive components.** While a Gradio callback is running, other components may not update. For agent workflows with multiple stages, use background threads or async to keep the UI responsive.
- **Anthropic max_tokens is required.** Unlike OpenAI which defaults to a reasonable max, Anthropic raises an error if `max_tokens` is not explicitly set.

## Cross-References

- [[llm-api-integration]] - API setup and authentication
- [[prompt-engineering]] - system prompts for better output
- [[agent-architectures]] - building agent UIs
- [[production-patterns]] - deploying Gradio apps
