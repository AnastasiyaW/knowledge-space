---
title: "Optimisation des tokens pour les agents"
description: "Réduire le coût et la latence mesurés des workflows d'agents sans sacrifier la qualité des tâches, la sécurité, la provenance ou la fiabilité de l'achèvement."
tags: [llm-agents, token-optimization, cost-optimization, context-engineering, prompt-caching, evaluation]
level: 4
source_sha256: 4cd0e8e28f08884e718af2d1d1629a58e0a4169b7e946f73981ab62041f95c7e
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des tokens pour les agents (septembre 2026) {#token-optimization-for-agents-september-2026}

Contexte de version : les tokenizers, les limites de contexte des modèles, les catégories de facturation, le comportement du cache et les niveaux de traitement par lots ou de priorité dépendent du fournisseur et du modèle. Utilisez les données d'usage actuelles du fournisseur et sa grille tarifaire pour le déploiement résolu ; ne reprenez pas une table de prix statique ni un ratio universel de tokens.

L'objectif n'est pas « utiliser le moins de tokens possible ». L'objectif est de minimiser le coût et la latence mesurés du workflow tout en respectant les exigences de qualité, de sécurité et d'achèvement de la tâche. Une réponse laconique qui déclenche des nouvelles tentatives, omet une réserve juridique ou exécute la mauvaise action d'outil constitue un échec coûteux.

## Établir une frontière de mesure {#establish-a-measurement-boundary}

Mesurez une tâche ou un workflow à la fois. Enregistrez la révision de release, la classe de tâche, le résultat terminal, l'usage rapporté par le fournisseur, la latence, les nouvelles tentatives, les signaux de cache lorsqu'ils sont disponibles, les appels d'outils et le résultat du validateur.

```json
{
  "trace_id": "tr_01...",
  "release_id": "research-summarizer@18",
  "task_class": "source-grounded-summary",
  "usage": {
    "input": 0,
    "output": 0,
    "cache_read": 0
  },
  "latency_ms": 0,
  "retry_count": 0,
  "tool_call_count": 0,
  "validator_outcome": "pass",
  "terminal_state": "completed"
}
```

Les catégories ci-dessus sont volontairement génériques. Les objets de réponse des fournisseurs peuvent utiliser d'autres noms ou exposer des champs d'usage supplémentaires. Conservez la réponse typée d'origine dans un journal contrôlé si l'audit l'exige, et ne normalisez que les données dont l'opérateur a besoin.

## Optimiser d'abord le contexte à plus fort levier {#optimize-the-highest-leverage-context-first}

Les améliorations les plus durables suppriment le travail inutile plutôt que de compresser le langage au point de le rendre ambigu.

| Levier | Mise en œuvre sûre | Mesure à conserver |
|---|---|---|
| Routage des tâches | n'orienter que les classes de tâches bien distinctes vers des configurations approuvées | précision du routage, taux de repli, taux de réussite des tâches |
| Sélection du contexte | ne récupérer ou charger que les preuves pertinentes pour la tâche déclarée | couverture des citations, taux de preuves manquantes |
| Surface des outils | n'exposer que les outils nécessaires à la tâche | erreurs de sélection d'outils, refus d'autorisation |
| Résultats d'outils | renvoyer des champs structurés et bornés, ainsi que des références durables vers les artefacts | taux d'appels répétés, résultat du validateur |
| Contrat de sortie | spécifier un schéma court ou un maximum uniquement lorsque l'exhaustivité est préservée | exhaustivité, taux de correction, résultat pour l'utilisateur |
| Instructions répétées | réutiliser un préfixe stable et relu lorsque le fournisseur prend en charge le cache | signal de cache, test confidentialité/locataire, révision de release |
| Politique de nouvelle tentative | corriger les causes récurrentes d'échec de validation ou de délai d'attente au lieu de réessayer aveuglément | nombre de nouvelles tentatives, taux d'effets en double |

N'utilisez pas une sortie « mots-clés uniquement » ou agrammaticale comme optimisation par défaut. Elle peut détruire des noms, des qualificatifs, des dates et des instructions qu'un autre système ou une personne doit interpréter correctement.

## Le contexte est un problème de recherche et de politique {#context-is-a-retrieval-and-policy-problem}

Avant d'ajouter un document, un résultat d'outil ou un tour de conversation à un prompt, demandez-vous :

1. Cet élément répond-il à une partie requise du contrat de la tâche ?
2. Est-il suffisamment fiable pour la décision à prendre ?
3. Est-il à jour, dans la frontière du locataire et autorisé par la politique de données ?
4. Une petite référence ou une extraction structurée peut-elle remplacer le contenu brut ?
5. Le relecteur en aval peut-il retrouver la source d'origine à partir de la sortie ?

Privilégiez un identifiant de source, une révision et un extrait pertinent plutôt qu'une transcription complète. Préservez la provenance : un contexte plus court qui perd la source d'origine constitue généralement une régression de qualité.

## Utiliser le cache comme optimisation contrôlée {#use-caching-as-a-controlled-optimization}

Lorsqu'un fournisseur prend en charge le cache de prompts, placez en premier les instructions partagées stables et les descriptions d'outils relues, avant de modifier les données propres à la tâche. Suivez les règles de cache actuelles du fournisseur plutôt que de supposer un seuil, une remise ou une durée de conservation fixes.

Incluez ces valeurs dans la clé de cache ou de release lorsque c'est pertinent :

```text
prompt_revision + policy_revision + tool_schema_revision
+ model/configuration + tenant or trust boundary
```

Le cache n'est pas un mécanisme d'autorisation. Ne réutilisez pas un contexte mis en cache entre utilisateurs, locataires ou classifications, sauf si le contrat avec le fournisseur et votre politique de données l'autorisent explicitement. [Cache de prompts OpenAI](https://developers.openai.com/api/docs/guides/prompt-caching) et [cache de prompts Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) décrivent le comportement propre à chaque fournisseur, qui doit être revérifié au moment du déploiement.

## Décisions de coût et de capacité {#cost-and-capacity-decisions}

Calculez le coût d'une requête à partir de l'usage rapporté par le fournisseur et de la grille tarifaire actuelle pour le modèle résolu exact et le niveau de traitement :

```text
request cost = sum(reported usage category × current unit price)
workflow cost = request costs + tool costs + retries + human review cost
```

Conservez ce calcul dans la configuration de déploiement ou de facturation, et non copié dans un article durable. La décision pertinente est de savoir si le workflow complet reste dans son budget approuvé tout en réussissant son évaluation de qualité et de sécurité.

Un modèle plus petit, un contexte plus court, une fonctionnalité de cache ou un niveau asynchrone sont des configurations candidates. Ne les mettez en production qu'après qu'ils ont satisfait les mêmes critères d'acceptation propres à la tâche que la configuration de référence.

## Mener une boucle d'optimisation fondée sur des preuves {#run-an-evidence-based-optimization-loop}

| Étape | Justificatif requis |
|---|---|
| Référence | échantillon de tâches figé, révision de configuration, distribution de l'usage et de la qualité |
| Hypothèse | une modification proposée et le compromis attendu |
| Exécution candidate | même échantillon, mêmes critères d'évaluation, usage normalisé |
| Revue des erreurs | échecs, nouvelles tentatives, lacunes de citations et tentatives d'actions non sûres |
| Décision | conserver, revenir en arrière ou investiguer, avec responsable et preuves |
| Contrôle en production | déploiement progressif et borné, avec résultats terminaux vérifiés |

Cette boucle empêche une baisse apparente des tokens d'entrée de masquer une hausse des coûts de correction, d'outils ou de support.

## Pièges courants {#gotchas}

- **Les économies de tokens d'entrée peuvent déplacer le coût ailleurs.** Un contexte manquant peut provoquer de nouvelles tentatives, des recherches web ou une escalade vers un humain. **Correctif :** mesurez le coût du workflow complet et le taux de réussite terminal de la tâche.
- **Les comptages de tokens des fournisseurs ne sont pas interchangeables.** Les caractères, les mots et le tokenizer d'un fournisseur ne permettent pas de prédire exactement la facturation d'un autre. **Correctif :** utilisez l'usage rapporté par le fournisseur pour la comptabilité.
- **Un contexte mis en cache conserve une frontière de confiance.** La réutilisation peut être dangereuse lorsqu'elle franchit une frontière de locataire, de politique ou de révision. **Correctif :** intégrez ces frontières dans la conception du cache et de la release, et testez l'isolation.
- **Un routeur peut devenir une nouvelle source d'échecs.** Des erreurs de routage bon marché peuvent envoyer des tâches à fort enjeu vers une configuration inadaptée. **Correctif :** évaluez la précision du routage et définissez un repli sûr.
- **Une compression trop agressive peut effacer la provenance.** Un résumé peut être plus court tout en ne montrant plus d'où provient une affirmation. **Correctif :** conservez les références aux sources et validez la couverture des citations.
- **Les nouvelles tentatives sont souvent le coût caché dominant.** Une requête moins chère ne sert à rien si elle échoue plus souvent. **Correctif :** enregistrez les nouvelles tentatives et corrigez leur cause avant d'optimiser la formulation.

## Sources {#sources}

- [OpenAI : sélection de modèle](https://developers.openai.com/api/docs/guides/model-selection)
- [OpenAI : cache de prompts](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenAI : référence de l'API Responses](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [Anthropic : cache de prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

## Voir aussi {#see-also}

- [[tokenization]]
- [[context-engineering]]
- [[prompt-engineering]]
- [[llmops]]
- [[llm-api-integration]]
- [[agent-observability-dashboards]]
