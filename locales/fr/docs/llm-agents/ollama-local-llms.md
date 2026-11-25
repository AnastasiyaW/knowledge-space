---
title: "Ollama et les LLM locaux (septembre 2026)"
category: infrastructure
tags: [llm-agents, ollama, local-llm, structured-output, observability]
level: 3
source_sha256: 01f88dd0932a8c93e8a05117e8f053be0899ce327f3e59385d151377eaa40830
translation: machine
translated_at: '2026-10-24'
---
# Ollama et les LLM locaux (septembre 2026) {#ollama-and-local-llms-september-2026}

Relu le 2026-09-03. Ollama fournit un runtime local et une surface d'API pour exécuter des modèles compatibles. Un point de terminaison local modifie la frontière de déploiement ; il ne prouve pas, à lui seul, la confidentialité, la provenance du modèle, la conformité aux licences ni une qualité suffisante pour une charge de travail donnée.

## Contrat d'exécution {#runtime-contract}

| Préoccupation | Ce qu'il faut consigner |
|---|---|
| Modèle | Tag exact et digest d'artefact immuable lorsqu'il est disponible |
| Hôte | CPU/GPU, mémoire, pilote et version du runtime |
| Point de terminaison | Adresse d'écoute locale, exposition réseau, chemin d'authentification |
| Chemin des données | Prompts, fichiers, outils, télémétrie et toute configuration cloud |
| Qualité | Jeu d'évaluation, tokenizer, quantification et résultat de validation |
| Exploitation | Latence de chargement, latence de génération, erreurs et politique de keep-alive |

Ollama documente son API locale, le comportement de streaming, les sorties structurées, l'appel d'outils et les métriques d'utilisation. Considérez la référence API officielle actuelle comme l'autorité pour les champs de requête et les capacités prises en charge. [Ollama API](https://docs.ollama.com/) [Structured outputs](https://docs.ollama.com/capabilities/structured-outputs)

## Appel local structuré {#structured-local-call}

Cette requête demande une réponse sans streaming, contrainte par un schéma JSON. Utilisez un modèle que vous avez explicitement téléchargé et évalué pour la tâche.

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

Validez le JSON renvoyé dans le code applicatif. Une requête avec schéma réduit les erreurs de formatage ; elle ne vérifie pas l'exactitude factuelle.

## Streaming ou non-streaming {#streaming-vs-non-streaming}

| Mode | À utiliser quand | Préoccupation opérationnelle |
|---|---|---|
| Streaming | Sortie interactive longue et interface progressive | Gérer les événements délimités par des retours à la ligne et l'annulation |
| Non-streaming | Sortie courte, validation structurée ou logique par lots | Borner le délai de bout en bout et la taille de la réponse |

L'API Ollama documente le streaming comme comportement par défaut pour certains points de terminaison, et des réponses JSON non diffusées lorsque la requête désactive le streaming. [Streaming](https://docs.ollama.com/api/streaming)

## Appels d'outils et métriques {#tool-calls-and-metrics}

Les appels d'outils nécessitent toujours une boucle contrôlée par l'application : inspecter la requête, valider l'outil et ses arguments, l'exécuter selon la politique définie, puis renvoyer le résultat. Ollama documente aussi des métriques de réponse telles que les durées de chargement, d'évaluation du prompt et de génération. Utilisez-les avec votre identifiant d'exécution et le tag du modèle ; une latence sans identité de charge de travail n'est pas comparable. [Tool calling](https://docs.ollama.com/capabilities/tool-calling) [Usage metrics](https://docs.ollama.com/api/usage)

## Planification de capacité {#capacity-planning}

- Mesurez une longueur de prompt et de sortie représentative sur l'hôte réel.
- Définissez la concurrence à partir de la mémoire et de la latence observées, et non de règles empiriques sur le nombre de paramètres.
- Consignez la configuration de quantification et de contexte avec chaque évaluation.
- Séparez la latence de démarrage à froid (chargement) de la latence de génération des tokens.
- Rejetez ou mettez en file d'attente les requêtes lorsque la capacité est épuisée ; ne redirigez pas silencieusement une entrée privée vers un autre fournisseur.

## Pièges {#gotchas}

- **Problème : supposer que localhost signifie que toutes les données restent locales.** Les modèles cloud, les outils distants, la télémétrie, les sources de téléchargement et la liaison réseau peuvent modifier le chemin des données. **Correctif :** examiner la configuration complète du déploiement et du réseau.
- **Problème : considérer un tag de modèle comme immuable.** Un tag peut être mis à jour ou résolu différemment selon les hôtes. **Correctif :** consigner l'identité de l'artefact évalué et déployer ce même artefact épinglé.
- **Problème : utiliser une sortie structurée sans validation applicative.** Un modèle peut toujours renvoyer des valeurs malformées ou sémantiquement invalides. **Correctif :** analyser et valider selon le même schéma que celui envoyé dans la requête.
- **Problème : comparer le débit sans isoler le temps de chargement.** Un modèle chargé et un modèle à froid répondent à des questions opérationnelles différentes. **Correctif :** consigner séparément les métriques de chargement et de génération.

## Voir aussi {#see-also}

- [[function-calling]]
- [[tool-use-patterns]]
- [[frontier-models]]
- [[model-optimization]]
- [[agent-observability-dashboards]]

## Sources {#sources}

- [Documentation Ollama](https://docs.ollama.com/)
- [Sorties structurées Ollama](https://docs.ollama.com/capabilities/structured-outputs)
- [Appel d'outils Ollama](https://docs.ollama.com/capabilities/tool-calling)
- [Métriques d'utilisation Ollama](https://docs.ollama.com/api/usage)
