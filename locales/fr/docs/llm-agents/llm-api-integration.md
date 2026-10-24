---
title: "Intégration de l'API LLM"
description: "Construire des intégrations de fournisseurs autour de contrats typés, d'une configuration sécurisée, d'un état explicite, de nouvelles tentatives et de portes de publication observables."
tags: [llm-agents, api, openai, anthropic, streaming, function-calling, llmops]
level: 5
source_sha256: 0a36fa4575d393cecff4202e9354046cf1205f33ce141d1bfbf9defa4cbf8322
translation: machine
translated_at: '2026-10-24'
---
# Intégration de l'API LLM (septembre 2026) {#llm-api-integration-september-2026}

Contexte de version : les identifiants de modèles, les points de terminaison, les formes de réponse, les limites de débit, les options de conservation des données, la sémantique des outils et la tarification évoluent indépendamment les uns des autres. Conservez-les dans une configuration relue et validez le contrat exact du fournisseur au moment du déploiement. Cette page n'utilise ni tableau de prix statique ni recommandation de modèle permanente.

Une intégration LLM en production est une frontière applicative, et non un simple appel au SDK. Elle nécessite des entrées et sorties typées, des contrôles d'identité et de données, une configuration des modèles, des délais d'expiration, une sémantique de nouvelle tentative, une télémétrie d'usage, ainsi qu'un moyen de reproduire ou d'annuler un changement de comportement.

## Commencer par un contrat indépendant du fournisseur {#start-with-a-provider-neutral-contract}

Gardez la logique applicative indépendante de l'objet de réponse du SDK.

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    task_id: str
    model_key: str
    input_text: str
    max_output_tokens: int


@dataclass(frozen=True)
class LLMResult:
    text: str
    provider_request_id: str
    model_revision: str
    usage: dict[str, int]
    finish_state: str


class LLMProvider(Protocol):
    def complete(self, request: LLMRequest) -> LLMResult: ...
```

L'adaptateur prend en charge la construction des requêtes propres au fournisseur, les événements de streaming, les boucles d'appels d'outils, les erreurs et l'extraction de l'usage. L'application gère l'autorisation, la validation métier, l'idempotence et la politique visible par l'utilisateur.

## Configuration sécurisée {#secure-configuration}

Utilisez un gestionnaire de secrets, une identité de charge de travail ou une injection de variables d'environnement gérée par le système de déploiement. Ne placez jamais de clés d'API dans les fichiers sources, le code côté navigateur, les captures d'écran, les documents, les prompts, les journaux ni les outils accessibles au modèle.

Séparez la configuration du code :

```json
{
  "provider": "approved_provider",
  "model_key": "support_triage_v4",
  "model_id": "reviewed-at-deploy",
  "timeout_seconds": 45,
  "max_output_tokens": 300,
  "data_policy_revision": "policy@12",
  "tool_policy_revision": "tools@7"
}
```

Une clé de modèle permet à l'application de demander une capacité relue, tandis que la configuration de déploiement fait correspondre cette clé à un modèle du fournisseur actuellement approuvé. Consignez la révision de modèle résolue dans le reçu du résultat.

## API Responses d'OpenAI {#openai-responses-api}

L'API Responses d'OpenAI actuelle accepte des entrées textuelles, d'images et de fichiers, expose les données de statut et d'usage, et peut renvoyer des appels d'outils. N'utilisez le champ de commodité du SDK pour le texte qu'après avoir vérifié le statut terminal.

```python
import os
from openai import OpenAI


def run_openai(prompt: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=os.environ["OPENAI_MODEL"],
        input=prompt,
        max_output_tokens=300,
    )
    if response.status != "completed":
        raise RuntimeError(f"response did not complete: {response.status}")
    return response.output_text
```

Ne codez jamais en dur un nom de modèle dans un article réutilisable ou un module applicatif. Restreignez la variable d'environnement à une liste d'autorisations approuvée dans la configuration de déploiement.

## API Messages d'Anthropic {#anthropic-messages-api}

L'API Messages accepte une conversation structurée et génère le message suivant. Conservez l'état de la conversation dans un enregistrement géré par l'application lorsque votre produit exige de la reproductibilité, des contrôles de conservation ou une portabilité entre fournisseurs.

```python
import os
import anthropic


def run_anthropic(prompt: str) -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=os.environ["ANTHROPIC_MODEL"],
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(
        block.text for block in message.content if block.type == "text"
    )
```

Les blocs de réponse d'un fournisseur peuvent contenir plus que du texte visible. Conservez la réponse typée jusqu'à la fin du traitement de la politique et des outils ; ne supposez pas que le premier bloc de contenu est le seul résultat.

## L'état est une décision produit {#state-is-a-product-decision}

Les différentes API offrent différents mécanismes de conversation et de conservation. Les Responses d'OpenAI peuvent lier des appels grâce à un identifiant de conversation ou de réponse précédente ; l'API Messages d'Anthropic s'utilise avec une liste de messages explicite. Un adaptateur générique ne doit traiter aucun de ces comportements comme un modèle universel de mémoire.

Pour chaque requête, enregistrez :

- l'identifiant applicatif de la conversation ou de la tâche ;
- la configuration et la révision du modèle ;
- la classification de la politique d'entrée et de contenu ;
- les identifiants de requête et de réponse du fournisseur ;
- les décisions d'appels d'outils et d'approbations ;
- le statut terminal, l'usage et le nombre de nouvelles tentatives ;
- la référence de trace expurgée et la politique de conservation.

Cela donne à un opérateur une frontière de tâche reproductible, sans conserver plus de contenu que la politique ne le permet.

## Le streaming exige un contrat d'événements {#streaming-needs-an-event-contract}

Les flux des fournisseurs sont des séquences d'événements, et non de simples fragments de texte. Faites-les passer par un analyseur qui reconnaît les événements de début, de delta, d'entrée d'outil, d'usage, d'erreur, de fin et d'annulation.

```text
stream event -> provider parser -> typed application event
             -> validation / UI update -> durable terminal receipt
```

N'exécutez jamais un outil à partir d'un fragment JSON partiel. Accumulez et validez une entrée d'outil complète, autorisez-la côté serveur, exécutez-la avec une clé d'idempotence, puis renvoyez un résultat d'outil structuré. Certains fournisseurs autorisent délibérément le streaming d'outils à granularité fine, où le JSON peut être incomplet pendant son arrivée.

## Sortie structurée et appels d'outils {#structured-output-and-tool-calls}

Utilisez des schémas aux deux frontières :

1. Donnez au modèle un schéma de sortie ou d'outil restreint.
2. Analysez la sortie avec un véritable validateur JSON/schéma.
3. Vérifiez les invariants métier, le périmètre du locataire et l'autorisation dans le code applicatif.
4. Liez les identifiants à l'action effectuée, et non au processus du modèle de manière générale.
5. Renvoyez une erreur typée ou une demande de correction ; ne forcez jamais silencieusement une valeur dangereuse.
6. Stockez un reçu qui identifie les révisions de politique et de schéma.

Un objet JSON valide n'est pas automatiquement une action métier valide.

## Nouvelles tentatives, idempotence et limites de débit {#retries-idempotency-and-rate-limits}

Ne relancez que les échecs dont on sait qu'ils peuvent être rejoués sans risque. Utilisez un backoff exponentiel borné avec gigue pour les échecs transitoires de réseau, de capacité ou de limite de débit, conformément aux recommandations actuelles du fournisseur. Ne répétez pas un effet de bord externe simplement parce qu'une réponse du LLM est manquante.

Pour un flux de travail à effets, créez la clé d'idempotence avant l'appel au fournisseur et conservez-la pendant l'exécution des outils :

```json
{
  "task_id": "invoice-summary-003",
  "idempotency_key": "task:invoice-summary-003:v1",
  "effect": "send_draft_only",
  "retry_budget": 3,
  "terminal_state": "pending"
}
```

Utilisez une file d'attente ou une tâche en arrière-plan pour les requêtes de longue durée. La fermeture de la connexion du navigateur ne prouve ni l'échec ni la réussite de la tâche sous-jacente.

## Observabilité et maîtrise des coûts {#observability-and-cost-control}

Suivez l'usage déclaré par le fournisseur, la latence, le statut, les erreurs, la révision du modèle, les signaux de cache lorsqu'ils sont disponibles, le nombre d'appels d'outils et le résultat de la tâche. Reliez les alertes aux échecs visibles par l'utilisateur et aux budgets approuvés, et non à un prix codé en dur, copié d'une version précédente.

Testez chaque adaptateur de fournisseur avec :

- une réponse ordinaire et une réponse incomplète ou en erreur ;
- un délai d'expiration et une nouvelle tentative bornée ;
- une violation de la sortie structurée ;
- un flux partiel ou une entrée d'outil partielle ;
- une livraison en double de la même tâche ;
- une requête d'outil inter-locataires ou non autorisée ;
- un changement de modèle ou de configuration avec la suite d'évaluation de publication.

## Pièges courants {#gotchas}

- **Les objets du SDK sont propres à chaque fournisseur.** Les laisser fuir dans le code applicatif rend la migration et les tests fragiles. **Correction :** normalisez-les dans un petit contrat de résultat interne.
- **Un identifiant de conversation n'est pas une politique de conservation des données.** L'état côté fournisseur et l'état côté application peuvent avoir des sémantiques de conservation différentes. **Correction :** définissez où vit l'historique et ce qui est supprimé ou expurgé.
- **Les données de flux partielles ne sont pas une entrée exécutable.** Le JSON d'un outil peut être incomplet ou invalide pendant le streaming. **Correction :** tamponnez, analysez, validez, autorisez, puis exécutez.
- **Les nouvelles tentatives peuvent dupliquer des effets de bord.** Un délai d'expiration ne prouve pas que la première requête a échoué. **Correction :** utilisez des clés d'idempotence et réconciliez l'état terminal.
- **Les exemples de prix statiques deviennent vite obsolètes.** Les coûts dépendent du modèle, du palier, du comportement du cache et de la sortie. **Correction :** utilisez l'usage déclaré par le fournisseur et les tarifs en vigueur au moment de la planification.

## Sources {#sources}

- [Référence de l'API Responses d'OpenAI](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [Guide d'appel de fonctions d'OpenAI](https://developers.openai.com/api/docs/guides/function-calling)
- [Bonnes pratiques de sécurité d'OpenAI](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [Référence de l'API Messages d'Anthropic](https://platform.claude.com/docs/en/api/messages/create)
- [Messages en streaming d'Anthropic](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Streaming d'outils à granularité fine d'Anthropic](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming)

## Voir aussi {#see-also}

- [[prompt-engineering]]
- [[function-calling]]
- [[tokenization]]
- [[llmops]]
- [[frontier-models]]
- [[agent-security]]
