---
title: Spring AI (Java)
category: frameworks
tags: [llm-agents, spring-ai, java, spring-boot, enterprise]
---

# Spring AI (Java)

Spring AI brings LLM integration to the Java/Spring Boot ecosystem. Provides Spring-native abstractions for AI providers, RAG, function calling, and vector stores with familiar dependency injection and auto-configuration.

## Key Facts
- Unified API for OpenAI, Anthropic, Ollama, Google, and other providers
- Spring Boot auto-configuration for minimal setup
- RAG support with vector store advisors
- Function calling support
- Best choice when building on existing Java/Spring infrastructure

## Basic Usage

```java
@RestController
public class ChatController {

    private final ChatClient chatClient;

    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @GetMapping("/chat")
    public String chat(@RequestParam String message) {
        return chatClient.prompt()
            .user(message)
            .call()
            .content();
    }
}
```

## Configuration

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      chat:
        options:
          model: gpt-4
          temperature: 0.7
```

## RAG Integration

```java
@Bean
public ChatClient chatClient(ChatClient.Builder builder, VectorStore vectorStore) {
    return builder
        .defaultAdvisors(new QuestionAnswerAdvisor(vectorStore))
        .build();
}
```

## When to Use

- Existing Java/Spring ecosystem
- Enterprise applications already on Spring Boot
- Team expertise in Java rather than Python
- Integration with Spring Security, Spring Data, etc.
- Organizations with Java-centric infrastructure

## Gotchas
- Smaller community and fewer examples compared to Python LangChain ecosystem
- Provider support may lag behind Python SDKs for new features
- Most AI/ML tutorials and examples are Python-first - need to adapt patterns
- Spring AI is relatively new - API surface may change between versions

## See Also
- [[langchain-framework]] - Python equivalent framework
- [[llm-api-integration]] - Provider API patterns (applicable to any language)
- [[rag-pipeline]] - RAG concepts implemented in Spring AI
- [[function-calling]] - Tool use concepts applicable to Spring AI
