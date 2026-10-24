---
title: "Modèles de conception d'agents"
description: "Choisir des modèles de flux de contrôle bornés pour les systèmes LLM : appels d'outils directs, ReAct, plans, machines à états et délégations à des spécialistes"
level: 3
source_sha256: 10ea5509dcc00d4f660247200511dced99b7128863072a7e6a83d210bcba895d
translation: machine
translated_at: '2026-10-24'
---
# Modèles de conception d'agents (septembre 2026) {#agent-design-patterns-september-2026}

Contexte de version : les modèles sont des choix d'architecture, non des fonctionnalités de framework. Figez le modèle, les schémas d'outils, la révision de politique et la suite d'évaluation utilisés par un flux déployé.

Un bon modèle d'agent rend la frontière de décision explicite : le modèle peut proposer la prochaine action, tandis que le code déterministe décide si cette action est autorisée, enregistre le résultat et choisit l'état terminal.

## Commencer en deçà de l'agentivité {#start-below-agency}

Utilisez la forme la moins dynamique qui répond à la tâche :

| Forme | Le modèle décide | Le système décide |
|---|---|---|
| Appel d'outil direct | Rien au-delà du contenu d'entrée | Outil, paramètres, autorisation, réponse |
| Workflow figé | Contenu à l'intérieur d'une étape connue | Ordre des étapes, nouvelles tentatives, transitions d'état |
| Boucle ReAct bornée | Prochaine étape de lecture/raisonnement autorisée | Liste blanche d'outils, budget, terminaison |
| Planifier puis exécuter | Plan candidat et demande de replanification | Validation du plan, exécution des étapes, approbation |
| Délégation à un spécialiste | Spécialiste approprié et autorisé | Identité, projection de l'historique, capacité |
| DAG | Proposition locale à chaque nœud | Dépendances, jointures, concurrence, reçus |

Un workflow figé est généralement plus simple à tester et plus sûr à exploiter. Ajoutez une boucle d'agent seulement lorsque la prochaine étape dépend réellement d'informations qui ne peuvent pas être énumérées à l'avance.

## ReAct borné {#bounded-react}

L'article ReAct décrit l'entrelacement de traces de raisonnement avec des actions et des observations. En production, ne traitez pas le raisonnement brut du modèle comme un journal d'audit ni comme une autorisation. Persistez plutôt des propositions d'action structurées et des reçus d'outils.

```text
input -> model proposes an allowed action -> policy validates
      -> tool executes -> receipt persists -> next state or terminal result
```

Chaque boucle doit avoir une condition d'arrêt : preuve suffisante, information insuffisante, action refusée, budget de tentatives, de coût ou de temps épuisé, ou approbation externe requise.

## Contrat de proposition d'action {#action-proposal-contract}

Exigez que le modèle émette un schéma indépendant de tout SDK de fournisseur :

```json
{
  "action": "search_documents",
  "arguments": {"query": "invoice INV-42"},
  "purpose": "find the authorized invoice record",
  "expected_receipt": "document-list-v1"
}
```

Le `purpose` est un résumé visible par l'opérateur, et non une chaîne de raisonnement cachée. La couche de politique valide le nom de l'action, le schéma des arguments, le périmètre de l'acteur et le budget restant avant l'exécution de tout outil.

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ActionProposal:
    action: str
    arguments: dict[str, Any]
    purpose: str


ALLOWED_ACTIONS = {"search_documents", "get_invoice"}


def authorize(proposal: ActionProposal, remaining_steps: int) -> None:
    if remaining_steps <= 0:
        raise RuntimeError("step budget exhausted")
    if proposal.action not in ALLOWED_ACTIONS:
        raise PermissionError(f"action is not allowed: {proposal.action}")
    if not proposal.purpose.strip():
        raise ValueError("operator-visible purpose is required")
```

## Planifier puis exécuter {#plan-and-execute}

Un plan est une hypothèse modifiable, non une commande. Utilisez un plan lorsque :

- la tâche comporte plusieurs objectifs dépendants ;
- un opérateur doit inspecter une approche proposée avant tout effet de bord ;
- les résultats intermédiaires peuvent déclencher une replanification autorisée ;
- chaque étape peut produire un reçu et un état d'échec défini.

Séparez la planification de l'exécution. Validez un plan au regard des permissions et des faits actuels, immédiatement avant chaque étape ; n'exécutez jamais aveuglément un ancien plan lorsque les outils, les données ou la politique ont changé.

## Réflexion et vérification {#reflection-and-verification}

Un appel de modèle d'autocritique peut produire des hypothèses utiles, mais ce n'est pas une vérification. Utilisez-le pour générer des contrôles candidats, puis exécutez des tests déterministes, une récupération de sources, une validation de schéma ou un évaluateur indépendant.

| Besoin | Mécanisme adapté |
|---|---|
| Valider un JSON / une sortie typée | Validateur de schéma |
| Vérifier un calcul | Code déterministe |
| Vérifier une affirmation sourcée | Source primaire récupérée, avec citation |
| Vérifier une modification de code | Tests/build et revue indépendante |
| Générer une stratégie alternative | Critique par le modèle ou planificateur |
| Approuver une action à fort impact | Humain autorisé ou service de politique |

## Découverte et composition d'outils {#tool-discovery-and-composition}

La découverte dynamique d'outils élargit la surface d'attaque et l'espace de décision du modèle. Privilégiez une petite liste blanche limitée à la tâche. Si la découverte est nécessaire, traitez les métadonnées d'outil comme non fiables tant que leur identité, leur schéma, leurs permissions et leur classe d'effets de bord n'ont pas été vérifiés.

La composition d'outils exige un contrat à chaque jonction : schéma de sortie, périmètre tenant/acteur, comportement en cas d'erreur, délai, clé d'idempotence et reçu. Une observation dont la provenance est absente ne doit pas déclencher une étape à effets de bord.

## Délégations {#handoffs}

Une délégation est appropriée lorsqu'une capacité ou une autorité distincte prend en charge la tâche suivante. Elle doit transporter une requête typée, une projection de contexte approuvée, un délai, une référence de trace et un responsable défini pour la réponse finale.

Ne transmettez pas par défaut l'intégralité d'une conversation à un spécialiste. Réduisez-la aux faits et artefacts que le spécialiste est autorisé à voir.

## Liste de contrôle pour le choix d'un modèle {#pattern-selection-checklist}

1. Décrivez le résultat terminal et les preuves requises pour le considérer comme complet.
2. Identifiez chaque effet de bord et chaque frontière d'autorisation.
3. Implémentez le workflow déterministe le plus court qui répond à la tâche.
4. Ajoutez une décision d'agent bornée uniquement là où la prochaine étape est réellement inconnue.
5. Instrumentez les propositions d'action, les décisions de politique, les reçus d'outils et la raison d'arrêt.
6. Évaluez l'ensemble du flux sur des cas représentatifs et adverses.

## Pièges {#gotchas}

- **Un plan généré par le modèle peut devenir obsolète.** Les sorties d'outils et les permissions évoluent après la planification. **Correctif :** autorisez et validez immédiatement avant chaque action, puis replanifiez à partir des reçus actuels.
- **Le raisonnement brut n'est pas un contrôle de sécurité.** Il peut être incomplet, sensible ou trompeur. **Correctif :** persistez des propositions structurées, des politiques et des reçus plutôt que de vous fier à un texte de raisonnement caché.
- **La réflexion peut amplifier la même erreur.** Le même modèle peut rationaliser une réponse incorrecte. **Correctif :** utilisez des contrôles déterministes indépendants ou un évaluateur calibré séparément.
- **La découverte dynamique n'est pas une autorisation.** Un outil annoncé peut être inadapté ou malveillant. **Correctif :** appliquez hors du modèle les contrôles d'identité, de schéma et de permission limitée à la tâche.

## Sources {#sources}

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [OpenAI Agents SDK: agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [OpenAI model guidance: tool orchestration](https://developers.openai.com/api/docs/guides/latest-model)

## Voir aussi {#see-also}

- [[agent-fundamentals]]
- [[agent-architectures]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-systems]]
