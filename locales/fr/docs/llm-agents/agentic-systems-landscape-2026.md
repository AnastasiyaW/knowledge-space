---
title: "Paysage des systèmes agentiques (septembre 2026)"
description: "Frontières de protocoles, choix de runtimes et patterns de plan de contrôle en production pour les systèmes agentiques ; revu le 2026-09-03."
level: 3
source_sha256: 7f059e9e0243ea8b32639b80fb3be82ed0567e293498b354e9632cf021d89a77
translation: machine
translated_at: '2026-10-24'
---
# Paysage des systèmes agentiques (septembre 2026) {#agentic-systems-landscape-september-2026}

Revu le 2026-09-03. Considérez un système agentique comme un plan de contrôle applicatif autour d'appels probabilistes à des modèles, et non comme un ensemble de personas autonomes. Les unités durables sont les contrats, l'état, les permissions, les preuves et les frontières de retour arrière.

## Frontières de protocoles {#protocol-boundaries}

| Frontière | Usage | Possède le cycle de vie | Ne pas utiliser comme |
|---|---|---|---|
| MCP | Connecter un agent hébergé par une application à des outils, des données et des fournisseurs de contexte | L'application hôte | Un moteur générique de workflow entre agents |
| A2A | Échanger des tâches et des résultats entre agents exploités séparément | Chaque agent/service participant | Un remplacement de l'autorisation d'outils ou des appels de fonctions locales |
| API applicative | Appels internes entre composants que vous déployez ensemble | Votre application | Un protocole public d'interopérabilité sans contrat de compatibilité |

MCP définit une architecture hôte-client-serveur : l'hôte crée les clients, contrôle les permissions et gère le cycle de vie. [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

A2A est un protocole d'interopérabilité pour la communication entre agents. Il complète MCP plutôt que de le remplacer : un agent peut utiliser MCP pour accéder à ses outils et A2A pour confier du travail à un autre agent. [A2A specification](https://a2a-protocol.org/latest/)

## Choix du runtime {#runtime-choice}

Choisissez le runtime le plus petit qui expose le contrôle dont vous avez besoin.

| Besoin | Point de départ adapté | Contrôle requis |
|---|---|---|
| Une tâche bornée avec quelques outils | Une boucle agentique dans le code applicatif | Schémas d'outils, délais, sortie finale structurée |
| Un spécialiste aide un manager | Le manager appelle le spécialiste comme un outil | Le manager reste l'unique autorité sur la sortie finale |
| L'utilisateur doit poursuivre avec un spécialiste | Transfert explicite (handoff) | Règle de routage, propriété visible par l'utilisateur, contrat de contexte |
| Éléments de travail indépendants | Fan-out et fan-in déterministes | Clé d'idempotence, plafond de concurrence, réducteur |
| Travail long ou redémarrable | Workflow durable / magasin d'état | Points de contrôle, bail, politique de relance, reçu terminal |

Le OpenAI Agents SDK documente deux modes de composition distincts : les spécialistes utilisés comme outils laissent le manager aux commandes, tandis que les transferts (handoffs) cèdent la conversation active à un spécialiste. Ses recommandations distinguent aussi l'orchestration choisie par le modèle de celle choisie par le code. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)

Les runtimes gérés peuvent réduire la charge d'infrastructure, mais ils ne dispensent pas de définir l'accès aux données, l'approbation, la validation des sorties et la gestion des incidents. Par exemple, Claude Managed Agents modélise un agent comme une configuration versionnée, associée à un environnement et à une session. [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/quickstart)

## Plan de contrôle en production {#production-control-plane}

Une invocation d'agent doit disposer d'un seul enregistrement durable. Stockez des références vers les entrées et sorties volumineuses plutôt que de les copier dans chaque prompt.

```json
{
  "run_id": "run_01J...",
  "work_item_id": "news-2026-09-03-001",
  "parent_run_id": null,
  "attempt": 1,
  "input_ref": "s3://private-bucket/intake/001.json",
  "agent_version": "news-curator@2026-09-03",
  "tool_policy_id": "news-read-only-v3",
  "status": "running",
  "output_ref": null,
  "evidence": [],
  "idempotency_key": "news-2026-09-03-001:curate:v3"
}
```

### Invariants requis {#required-invariants}

- Un seul composant possède chaque enregistrement modifiable. Les workers peuvent ajouter des preuves, mais seul le contrôleur de workflow modifie le statut terminal.
- Une nouvelle tentative réutilise le même élément de travail et un nouveau numéro de tentative. Elle ne crée jamais silencieusement un second candidat de publication.
- Un appel d'outil dispose d'une capacité figurant dans une liste d'autorisation, d'un délai, d'une identité d'appelant et d'un reçu. Les issues inconnues d'un appel d'outil échouent en mode fermé (fail closed).
- Une réponse générée n'est pas un reçu. Un reçu identifie l'entrée, la version de l'agent ou de sa configuration, les résultats des outils, le résultat du validateur et l'horodatage.
- La publication publique est une transition d'état distincte, intervenant après revue. N'assimilez pas une extraction réussie à une approbation.

## Ordre de construction {#build-order}

1. Implémentez un chemin à agent unique avec une entrée et une sortie typées.
2. Ajoutez une validation déterministe avant d'ajouter un autre agent.
3. Ajoutez un évaluateur à portée séparée lorsqu'une mauvaise sortie a un coût important.
4. Ajoutez des workers parallèles uniquement pour des éléments de travail indépendants et partitionnés.
5. Ajoutez une reprise durable uniquement lorsque le travail peut survivre à un processus unique.
6. Ajoutez A2A inter-services uniquement lorsque des agents possédés indépendamment nécessitent une frontière d'interopérabilité stable.

Cet ordre permet de garder la surface de défaillance observable. Une conception multi-agents se justifie par un besoin concret de travail indépendant, de séparation des autorités ou d'une frontière de confiance différente, et non par un nom de rôle.

## Routage des modèles et des outils {#model-and-tool-routing}

Routez selon le contrat, et non selon une étiquette de produit.

| Classe de travail | Critère de routage | Exemple de validateur |
|---|---|---|
| Extraction | Le schéma est connu | Vérifications de schéma JSON et des références aux sources |
| Classification | Les étiquettes autorisées sont finies | Validation par énumération et politique de confiance |
| Rédaction | Une relecture humaine est requise | Grille éditoriale et enregistrement d'approbation |
| Modification de code | L'état du dépôt fait autorité | Test ciblé et revue du diff |
| Action externe | L'effet de bord est significatif | Approbation explicite et clé d'idempotence |

Ne utilisez un routage choisi par le modèle que lorsque le routage lui-même constitue une tâche de raisonnement ouverte. Utilisez du code applicatif lorsque le routage relève d'une décision de politique, d'une frontière d'autorisation ou d'une limite de budget.

## Quand ne pas ajouter d'agent {#when-not-to-add-an-agent}

N'ajoutez pas un spécialiste simplement pour renommer un prompt. Conservez un agent unique lorsque :

- la tâche est séquentielle et les mêmes permissions s'appliquent du début à la fin ;
- le résultat dispose d'un unique validateur déterministe ;
- partager le contexte complet est moins coûteux et plus sûr que de le sérialiser entre agents ;
- aucun relecteur indépendant ni aucune frontière de confiance externe n'est nécessaire.

Découper le travail introduit une perte de contexte, un surcoût, davantage de traces à inspecter, et un mode de défaillance supplémentaire à chaque transfert.

## Pièges courants {#gotchas}

- **Problème : traiter MCP et A2A comme interchangeables.** L'autorisation MCP relève de la frontière hôte/outil ; A2A concerne la communication entre agents. **Correctif :** documentez séparément les deux frontières et utilisez le protocole qui gouverne la relation.
- **Problème : laisser un modèle décider d'un routage soumis à une politique.** Une instruction en langage naturel n'est pas un système d'autorisation. **Correctif :** conservez les budgets, l'approbation de publication et les portes de contrôle des actions destructrices dans du code applicatif déterministe.
- **Problème : relancer avec une nouvelle identité.** Un délai d'attente peut laisser un effet de bord externe incertain. **Correctif :** persistez une clé d'idempotence et réconciliez la tentative précédente avant de renvoyer la requête.
- **Problème : considérer une réponse du modèle comme une achèvement.** Une réponse fluide peut omettre les preuves requises. **Correctif :** faites en sorte que le workflow ne se termine qu'après que le validateur a enregistré un reçu PASS.

## Limites {#limitations}

Les protocoles rendent les frontières explicites ; ils ne rendent pas les agents fiables, sûrs ni mutuellement dignes de confiance. Le comportement des outils, la qualité des sources, le caractère non déterministe des modèles et la politique de relecture restent de la responsabilité de l'application. Testez le workflow réel avec des défaillances représentatives avant d'augmenter l'autonomie.

## Voir aussi {#see-also}

- [[agent-orchestration]]
- [[managed-agents]]
- [[multi-agent-systems]]
- [[multi-session-coordination]]
- [[llmops]]

## Sources {#sources}

- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [A2A Protocol](https://a2a-protocol.org/latest/)
- [OpenAI Agents SDK: Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [Claude Managed Agents Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
