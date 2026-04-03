---
title: No-Code Agent Platforms
category: frameworks
tags: [llm-agents, n8n, flowise, gradio, no-code, automation, visual-builder]
---

# No-Code Agent Platforms

Visual and low-code platforms for building LLM agents, chatbots, and automation workflows. Enable building AI applications without deep programming, connecting to hundreds of services via drag-and-drop interfaces.

## Key Facts
- n8n: workflow automation with AI nodes, connects 400+ services
- FlowWise: visual LangChain/LangGraph builder, drag-and-drop agents
- Gradio: Python library for quick ML model UIs
- All three are open-source and self-hostable
- No-code tools are excellent for prototyping but may need code for production edge cases

## n8n - Workflow Automation

### Core Concepts
- **Workflow**: sequence of connected nodes
- **Node**: single operation (HTTP request, LLM call, database query)
- **Trigger**: starts workflow (webhook, schedule, email, chat message)
- **Credentials**: stored API keys

### AI Nodes
- **AI Agent node**: creates ReAct agent with tools
- **LLM Chat node**: simple chat completion
- **Embeddings node**: generate embeddings
- **Vector Store node**: Pinecone, Qdrant, etc.
- **Memory node**: conversation buffer
- **Tool nodes**: calculator, code execution, HTTP

### Building AI Agents
1. Chat Trigger (webhook for incoming messages)
2. AI Agent node with LLM (OpenAI, Anthropic, Ollama)
3. Tools (web search, calculator, custom HTTP)
4. Memory for conversation context
5. Output to webhook response, email, Slack

Can connect to Make/Zapier via webhooks for extended integrations.

## FlowWise - Visual LLM Builder

### Installation
```bash
npm install -g flowise
npx flowise start
# Or: docker pull flowiseai/flowise && docker run -d -p 3000:3000 flowiseai/flowise
```

### Building Blocks
- **Chat Models**: OpenAI, Anthropic, Ollama, Gemini
- **Chains**: Conversational Retrieval QA, LLM Chain, Sequential Chain
- **Agents**: Supervisor, Worker, OpenAI Function Agent, ReAct
- **Tools**: Search API, Calculator, Retriever, Custom (JavaScript), Write/Read File
- **Vector Stores**: In-Memory, Chroma, Pinecone, Qdrant
- **Embeddings**: OpenAI, Ollama, HuggingFace
- **Document Loaders**: PDF, Text, Web Scraper (Cheerio), CSV
- **Text Splitters**: Recursive Character, Token-based

### Supervisor Agent Pattern
1. Create Agent Flow
2. Add Supervisor + 2-3 Worker nodes
3. Connect Chat Model to Supervisor
4. Set worker system prompts and tools
5. Configure supervisor: "Start with Worker1, pass to Worker2"
6. Test

### Deployment
- Embed in websites via iframe or JavaScript widget
- REST API for programmatic access
- Deploy to Render, Railway, or any Node.js host

```html
<script type="module">
  import Chatbot from "https://cdn.jsdelivr.net/npm/flowise-embed/dist/web.js"
  Chatbot.init({
    chatflowid: "your-chatflow-id",
    apiHost: "https://your-flowise.com",
    theme: { button: { backgroundColor: "#3B81F6" } }
  })
</script>
```

### REST API
```bash
curl -X POST https://your-flowise.com/api/v1/prediction/{chatflow-id} \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, how can you help?"}'
```

## Gradio - Python ML UIs

### Quick Chatbot
```python
import gradio as gr

def chat(message, history):
    response = llm.invoke(message)
    return response

demo = gr.ChatInterface(fn=chat, title="AI Assistant")
demo.launch()
```

### Blocks Layout
```python
with gr.Blocks() as demo:
    gr.Markdown("# My AI App")
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="Question")
            temperature = gr.Slider(0, 2, value=0.7, label="Temperature")
            submit_btn = gr.Button("Ask")
        with gr.Column():
            output_text = gr.Textbox(label="Answer")
    submit_btn.click(fn=process, inputs=[input_text, temperature], outputs=output_text)
demo.launch(share=True)  # share=True creates public URL
```

### Key Features
- `launch(share=True)`: temporary public URL
- `launch(server_name="0.0.0.0")`: network accessible
- Streaming via `yield`
- `gr.State()` for persisting data
- `gr.Tab()` for multi-page interfaces
- Basic auth: `launch(auth=("user", "pass"))`

### HuggingFace Spaces
Free hosting for Gradio apps. Push code to HuggingFace Space for automatic deployment.

## Gotchas
- FlowWise: MUST click "Upsert" to index documents - without this, RAG returns garbage
- n8n credentials are stored locally - back them up before migration
- Gradio `share=True` URLs are temporary and insecure - not for production
- No-code platforms add abstraction layers that can mask debugging information
- FlowWise marketplace templates may use outdated node versions
- Token costs are the same whether you use no-code or code - track usage

## See Also
- [[langchain-framework]] - Code-first alternative to FlowWise
- [[ollama-local-llms]] - Local models for FlowWise/n8n
- [[rag-pipeline]] - RAG concepts that FlowWise implements visually
- [[multi-agent-systems]] - Agent patterns built visually
- [[agent-fundamentals]] - Concepts behind the visual abstractions
