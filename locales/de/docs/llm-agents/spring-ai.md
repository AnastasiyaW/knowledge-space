---
title: "Spring AI 2.0 (September 2026)"
category: frameworks
tags: [llm-agents, spring-ai, java, spring-boot, tool-calling, mcp]
level: 3
source_sha256: 1a916bc881efdfbe83e8c693b5cd38161da0ec1bb184d3fbc19c8931ad79b716
translation: machine
translated_at: '2026-10-24'
---
# Spring AI 2.0 (September 2026) {#spring-ai-20-september-2026}

Geprüft am 03.09.2026 gegen Spring AI 2.0.1. Spring AI stellt Spring-native Abstraktionen für Modellaufrufe, Vektorspeicher, Tool-Calling, Advisor-Ketten, Observability und MCP-Integration bereit. Setzen Sie es ein, wenn die Anwendung ohnehin Java-/Spring-Betriebsaspekte verantwortet. Behandeln Sie Provider-Portabilität nicht als identische Funktionalität oder identisches Verhalten.

## Kernkomponenten {#core-components}

| Komponente | Verantwortung |
|---|---|
| ChatClient | Fluent-Aufbau von Modellanfragen sowie synchrone und Streaming-Aufrufe |
| Advisor-Kette | Geordnete Anreicherung von Anfrage und Antwort, einschließlich Memory- und Retrieval-Mustern |
| ToolCallback / Tool-Annotation | Von der Anwendung definierte Tool-Beschreibung und Dispatch |
| VectorStore | Provider-neutrale Vektorspeicher-Abstraktion mit Metadatenfilterung |
| MCP-Client/Server | Nutzung von Tools aus MCP-Servern oder Bereitstellung von Spring-Services für MCP-Clients |
| Observability | Micrometer-Observations für Modell-, Vektorspeicher- und Tool-Arbeit |

Die aktuelle Spring-AI-Referenz führt 2.0.1 als stabile Version auf und dokumentiert eine erstklassige Tool-Calling-Schleife in der Advisor-Kette des ChatClient. [Spring AI API](https://docs.spring.io/spring-ai/reference/api/) [Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)

## ChatClient mit einem expliziten Tool {#chatclient-with-an-explicit-tool}

Dieses Java-Beispiel zielt auf Spring AI 2.0.1 und benötigt eine konfigurierte ChatModel-Bean. Die Anwendung verantwortet die eigentliche Tool-Implementierung und damit deren Autorisierung.

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

Ersetzen Sie die illustrative Zeichenkette durch einen begrenzten Anwendungsservice. Machen Sie eine Methode, die Daten verändert, nicht allein deshalb zum Tool, weil sie sich annotieren lässt.

## Reihenfolge der Advisors {#advisor-ordering}

Advisors können Kontext, Retrieval, Memory, Logging, Wiederholungsversuche oder eigene Logik hinzufügen. Ihre Reihenfolge verändert den Anfrage- und Antwortpfad. Dokumentieren Sie sie daher in der Deployment-Konfiguration und testen Sie sie mit repräsentativen Konversationen.

| Belang | Prüfung |
|---|---|
| Memory | Bei jedem Aufruf, der Memory nutzt, wird eine Konversations-ID übergeben |
| Retrieval | Quellenmetadaten und Relevanz stehen der finalen Antwort zur Verfügung |
| Tool-Schleife | Tool-Aufrufe sind nur über eine explizite Richtlinie erlaubt |
| Logging | Sensible Prompt- und Antwortfelder werden geschwärzt |
| Streaming | Die Anwendung nutzt den erforderlichen reaktiven Stack und die Abbruchrichtlinie |

Spring AI 2.0 verwendet ToolCallingAdvisor als Verantwortlichen für die Tool-Schleife. Ältere Callback-APIs und Advisor-Namen sollten als Migrationsaufgabe behandelt und nicht in neuen Code übernommen werden. [Spring AI Upgrade-Hinweise](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)

## MCP-Grenze {#mcp-boundary}

Spring AI kann Tools aus MCP-Servern nutzen und Spring-basierte Services bereitstellen. Halten Sie die MCP-Server-Konfiguration und die Tool-Freigabe explizit: Eine Erkennung autorisiert ein Tool nicht für jede ChatClient-Anfrage. [Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html) [MCP-Architektur](https://modelcontextprotocol.io/specification)

## Fallstricke {#gotchas}

- **Problem: Annahme, dass eine portable Abstraktion portables Modellverhalten erzeugt.** Provider unterscheiden sich in Tool-Unterstützung, Kontextlimits, Streaming und Fehlerverhalten. **Lösung:** Führen Sie dieselbe Evaluierungssuite für jede Kombination aus Provider und Modell aus.
- **Problem: Vergessene Reihenfolge der Advisors.** Memory, Retrieval und Tool-Ausführung können je nach Reihenfolge unterschiedlichen Kontext sehen. **Lösung:** Versionieren Sie die Advisor-Kette und testen Sie die beabsichtigte Abfolge.
- **Problem: Automatische Ausführung einer datenverändernden Tool-Methode.** Die Bequemlichkeit des Frameworks ersetzt keine Freigabe. **Lösung:** Erzwingen Sie Autorisierung, Idempotenz und explizite Freigabe innerhalb des Tool-Services oder des Gateways.
- **Problem: Protokollierung von ChatClient-Payloads in der Produktion.** Prompts und Ergebnisse können private Daten enthalten. **Lösung:** Schwärzen Sie Daten an der Grenze von Logging und Observability und begrenzen Sie die Aufbewahrungsdauer.

## Siehe auch {#see-also}

- [[function-calling]]
- [[tool-use-patterns]]
- [[rag-pipeline]]
- [[llm-api-integration]]
- [[agent-observability-dashboards]]

## Quellen {#sources}

- [Spring AI API-Referenz](https://docs.spring.io/spring-ai/reference/api/)
- [Spring AI Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)
- [Spring AI ChatClient](https://docs.spring.io/spring-ai/reference/api/chatclient.html)
- [Spring AI Advisors](https://docs.spring.io/spring-ai/reference/api/advisors.html)
