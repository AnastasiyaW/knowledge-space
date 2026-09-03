---
title: "Spring AI 2.0 (September 2026)"
category: frameworks
tags: [llm-agents, spring-ai, java, spring-boot, tool-calling, mcp]
---

# Spring AI 2.0 (September 2026)

Reviewed 2026-09-03 against Spring AI 2.0.1. Spring AI provides Spring-native abstractions for model calls, vector stores, tool calling, advisor chains, observability, and MCP integration. Use it when the application already owns Java/Spring operational concerns; do not treat provider portability as identical capability or behavior.

## Core Components

| Component | Responsibility |
|---|---|
| ChatClient | Fluent construction of model requests and synchronous/streaming calls |
| Advisor chain | Ordered request/response enrichment, including memory and retrieval patterns |
| ToolCallback / Tool annotation | Application-owned tool definition and dispatch |
| VectorStore | Provider-neutral vector-store abstraction with metadata filtering |
| MCP client/server | Consume MCP-server tools or expose Spring services to MCP clients |
| Observability | Micrometer observations for model, vector-store, and tool work |

The current Spring AI reference lists stable 2.0.1 and documents a first-class tool-calling loop in the ChatClient advisor chain. [Spring AI API](https://docs.spring.io/spring-ai/reference/api/) [Tool calling](https://docs.spring.io/spring-ai/reference/api/tools.html)

## ChatClient with an Explicit Tool

This Java example targets Spring AI 2.0.1 and requires a configured ChatModel bean. The application owns the actual tool implementation and therefore its authorization.

```java
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.tool.annotation.Tool;

final class WeatherTools {
    @Tool(description = "Get the current weather for a named city.")
    String getWeather(String city) {
        return "Weather lookup is not connected for " + city;
    }
}

public final class AgentService {
    private final ChatClient chatClient;
    private final WeatherTools weatherTools = new WeatherTools();

    public AgentService(ChatModel chatModel) {
        this.chatClient = ChatClient.create(chatModel);
    }

    public String answer(String question) {
        return this.chatClient.prompt()
                .user(question)
                .tools(this.weatherTools)
                .call()
                .content();
    }
}
```

Replace the illustrative string with a bounded application service. Do not expose a mutating method merely because it can be annotated as a tool.

## Advisor Ordering

Advisors can add context, retrieval, memory, logging, retries, or custom logic. Their order changes the request and response path, so record it in the deployment configuration and test it with representative conversations.

| Concern | Check |
|---|---|
| Memory | A conversation ID is provided on every call that uses memory |
| Retrieval | Source metadata and relevance are available to the final answer |
| Tool loop | Tool calls are allowed only through an explicit policy |
| Logging | Sensitive prompt and response fields are redacted |
| Streaming | The application uses the required reactive stack and cancellation policy |

Spring AI 2.0 uses ToolCallingAdvisor as the tool-loop owner. Older callback APIs and advisor names should be treated as migration work, not copied into new code. [Spring AI upgrade notes](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)

## MCP Boundary

Spring AI can consume MCP-server tools and expose Spring-based services. Keep MCP server configuration and tool exposure explicit: discovery does not authorize a tool for every ChatClient request. [Spring AI tool calling](https://docs.spring.io/spring-ai/reference/api/tools.html) [MCP Architecture](https://modelcontextprotocol.io/specification)

## Gotchas

- **Issue: Assuming a portable abstraction makes model behavior portable.** Providers differ in tool support, context limits, streaming, and error behavior. **Fix:** run the same evaluation suite for every provider/model configuration.
- **Issue: Forgetting advisor order.** Memory, retrieval, and tool execution can see different context depending on ordering. **Fix:** version the advisor chain and test the intended sequence.
- **Issue: Auto-executing a mutating Tool method.** Framework convenience is not approval. **Fix:** enforce authorization, idempotency, and explicit approval inside the tool service or gateway.
- **Issue: Logging ChatClient payloads in production.** Prompts and results may contain private data. **Fix:** redact at the logging/observability boundary and use minimal retention.

## See Also

- [[function-calling]]
- [[tool-use-patterns]]
- [[rag-pipeline]]
- [[llm-api-integration]]
- [[agent-observability-dashboards]]

## Sources

- [Spring AI API reference](https://docs.spring.io/spring-ai/reference/api/)
- [Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)
- [Spring AI ChatClient](https://docs.spring.io/spring-ai/reference/api/chatclient.html)
- [Spring AI Advisors](https://docs.spring.io/spring-ai/reference/api/advisors.html)
