---
title: "Spring AI 2.0 (septembre 2026)"
category: frameworks
tags: [llm-agents, spring-ai, java, spring-boot, tool-calling, mcp]
level: 3
source_sha256: 1a916bc881efdfbe83e8c693b5cd38161da0ec1bb184d3fbc19c8931ad79b716
translation: machine
translated_at: '2026-10-24'
---
# Spring AI 2.0 (septembre 2026) {#spring-ai-20-september-2026}

Relu le 2026-09-03 par rapport à Spring AI 2.0.1. Spring AI fournit des abstractions natives de Spring pour les appels de modèles, les vector stores, le tool calling, les chaînes d'advisors, l'observabilité et l'intégration MCP. Utilisez-le lorsque l'application gère déjà les contraintes opérationnelles Java/Spring ; ne considérez pas la portabilité entre fournisseurs comme une capacité ou un comportement identique.

## Composants principaux {#core-components}

| Composant | Responsabilité |
|---|---|
| ChatClient | Construction fluide des requêtes de modèle et des appels synchrones/en flux |
| Advisor chain | Enrichissement ordonné des requêtes et des réponses, incluant les patterns de mémoire et de récupération |
| ToolCallback / annotation Tool | Définition et répartition des outils, sous le contrôle de l'application |
| VectorStore | Abstraction de vector store indépendante du fournisseur, avec filtrage sur les métadonnées |
| Client/serveur MCP | Consommation des outils de serveurs MCP ou exposition des services Spring aux clients MCP |
| Observabilité | Observations Micrometer pour les traitements de modèle, de vector store et d'outils |

La référence actuelle de Spring AI indique que la version 2.0.1 est stable et documente une boucle de tool calling de première classe dans la chaîne d'advisors du ChatClient. [Spring AI API](https://docs.spring.io/spring-ai/reference/api/) [Tool calling](https://docs.spring.io/spring-ai/reference/api/tools.html)

## ChatClient avec un outil explicite {#chatclient-with-an-explicit-tool}

Cet exemple Java cible Spring AI 2.0.1 et nécessite un bean ChatModel configuré. L'application est responsable de l'implémentation réelle de l'outil, et donc de son autorisation.

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

Remplacez la chaîne illustrative par un service applicatif borné. N'exposez pas une méthode modifiant des données simplement parce qu'elle peut être annotée comme outil.

## Ordre des advisors {#advisor-ordering}

Les advisors peuvent ajouter du contexte, de la récupération, de la mémoire, de la journalisation, des tentatives de reprise ou une logique personnalisée. Leur ordre modifie le chemin de la requête et de la réponse : consignez-le dans la configuration de déploiement et testez-le avec des conversations représentatives.

| Préoccupation | Point à vérifier |
|---|---|
| Mémoire | Un identifiant de conversation est fourni à chaque appel qui utilise la mémoire |
| Récupération | Les métadonnées des sources et leur pertinence sont disponibles pour la réponse finale |
| Boucle d'outils | Les appels d'outils ne sont autorisés que par une politique explicite |
| Journalisation | Les champs sensibles des prompts et des réponses sont masqués |
| Streaming | L'application utilise la pile réactive requise et une politique d'annulation |

Spring AI 2.0 utilise ToolCallingAdvisor comme responsable de la boucle d'outils. Les anciennes API de callbacks et les anciens noms d'advisors doivent être traités comme du travail de migration, et non recopiés dans le nouveau code. [Notes de mise à niveau de Spring AI](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)

## Frontière MCP {#mcp-boundary}

Spring AI peut consommer les outils de serveurs MCP et exposer des services basés sur Spring. Gardez la configuration du serveur MCP et l'exposition des outils explicites : la découverte n'autorise pas un outil pour chaque requête ChatClient. [Tool calling Spring AI](https://docs.spring.io/spring-ai/reference/api/tools.html) [Architecture MCP](https://modelcontextprotocol.io/specification)

## Pièges {#gotchas}

- **Problème : supposer qu'une abstraction portable rend le comportement des modèles portable.** Les fournisseurs diffèrent par le support des outils, les limites de contexte, le streaming et le comportement en cas d'erreur. **Correctif :** exécutez la même suite d'évaluation pour chaque configuration fournisseur/modèle.
- **Problème : oublier l'ordre des advisors.** La mémoire, la récupération et l'exécution des outils peuvent voir des contextes différents selon l'ordre. **Correctif :** versionnez la chaîne d'advisors et testez la séquence prévue.
- **Problème : exécuter automatiquement une méthode Tool qui modifie des données.** La commodité du framework ne vaut pas approbation. **Correctif :** appliquez l'autorisation, l'idempotence et une approbation explicite dans le service d'outil ou la passerelle.
- **Problème : journaliser les payloads du ChatClient en production.** Les prompts et les résultats peuvent contenir des données privées. **Correctif :** masquez les données au niveau de la journalisation/observabilité et limitez la durée de conservation.

## Voir aussi {#see-also}

- [[function-calling]]
- [[tool-use-patterns]]
- [[rag-pipeline]]
- [[llm-api-integration]]
- [[agent-observability-dashboards]]

## Sources {#sources}

- [Référence de l'API Spring AI](https://docs.spring.io/spring-ai/reference/api/)
- [Tool Calling Spring AI](https://docs.spring.io/spring-ai/reference/api/tools.html)
- [ChatClient Spring AI](https://docs.spring.io/spring-ai/reference/api/chatclient.html)
- [Advisors Spring AI](https://docs.spring.io/spring-ai/reference/api/advisors.html)
