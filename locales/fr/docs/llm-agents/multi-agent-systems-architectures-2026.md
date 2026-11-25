---
title: "Architectures de systèmes multi-agents (septembre 2026)"
description: "Patterns de production pour le routage, le fan-out, l'évaluation et la reprise durable dans les systèmes multi-agents ; revu le 2026-09-03."
level: 3
source_sha256: b7005cf447c53216b8c991e861c08394b23f0d92f90ca874cb8aebd67f41c583
translation: machine
translated_at: '2026-10-24'
---
# Architectures de systèmes multi-agents (septembre 2026) {#multi-agent-systems-architectures-september-2026}

Revu le 2026-09-03. Un système multi-agents est un workflow comportant plus d'un worker piloté par modèle. Son architecture se définit par l'autorité, l'état, le flux de données et la validation, et non par des intitulés de poste anthropomorphiques.

## Choisir un pattern selon le flux de contrôle {#choose-a-pattern-by-control-flow}

| Pattern | Contrôleur | Idéal pour | Risque principal |
|---|---|---|---|
| Manager avec spécialistes exposés comme outils | Manager | Une réponse finale assemblée à partir de sous-résultats bornés | Le prompt du manager devient un moteur de politiques non testable |
| Handoff explicite | Routeur puis spécialiste sélectionné | Un spécialiste doit prendre en charge l'interaction active avec l'utilisateur | Responsabilité ambiguë après le routage |
| Fan-out / fan-in | Ordonnanceur déterministe | Partitions indépendantes, recherche ou dimensions de revue | Travail dupliqué et fusion non déterministe |
| Générateur / évaluateur | Contrôleur de workflow | Sorties coûteuses avec critères d'acceptation explicites | Auto-revue dans le même contexte |
| Workflow durable | Contrôleur de machine à états | Tâches qui peuvent survivre à un processus ou appeler des systèmes externes | Relancer un effet de bord sans réconciliation |

Dans le SDK Agents d'OpenAI, un agent utilisé comme outil laisse le manager aux commandes ; un handoff transfère la conversation active au spécialiste choisi. La distinction est architecturale, même si les deux reposent sur des appels de modèle. [Orchestration d'agents](https://openai.github.io/openai-agents-js/guides/multi-agent/)

## Contrat de travail partagé {#shared-work-contract}

Chaque worker reçoit un élément de travail borné et produit une seule enveloppe de résultat. Évitez de partager une transcription libre et modifiable comme système de référence.

```json
{
  "work_item_id": "research:chunk-07",
  "run_id": "run_01J...",
  "parent_run_id": "run_01J-parent",
  "objective": "extract claims from this source set",
  "input_refs": ["source:42", "source:43"],
  "allowed_tools": ["fetch_source", "quote_locator"],
  "deadline_at": "2026-09-03T16:00:00Z",
  "output_schema": "claim-set/v1",
  "idempotency_key": "research:chunk-07:v1"
}
```

Le résultat doit contenir un statut terminal, des références aux sources et aux preuves, ainsi qu'une catégorie d'erreur. Par défaut, un synthétiseur doit recevoir des enveloppes de résultat validées, et non les traces brutes des workers.

## Fan-out / fan-in déterministe {#deterministic-fan-out-fan-in}

Utilisez le fan-out uniquement lorsque chaque partition est indépendante et que la règle de fusion est déterministe. Cet exemple Python 3.11+ est indépendant du fournisseur ; remplacez le corps du worker par un appel de modèle qui renvoie le schéma de résultat déclaré.

```python
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass(frozen=True)
class Result:
    item_id: str
    status: str
    value: str


async def run_partition(item_id: str) -> Result:
    # Replace with a bounded model/tool invocation.
    await asyncio.sleep(0)
    return Result(item_id=item_id, status="passed", value=item_id.upper())


async def run_all(
    item_ids: list[str],
    worker: Callable[[str], Awaitable[Result]],
    concurrency: int = 4,
) -> list[Result]:
    semaphore = asyncio.Semaphore(concurrency)

    async def guarded(item_id: str) -> Result:
        async with semaphore:
            return await worker(item_id)

    results = await asyncio.gather(*(guarded(item_id) for item_id in item_ids))
    failures = [result for result in results if result.status != "passed"]
    if failures:
        raise RuntimeError(f"partition failures: {[item.item_id for item in failures]}")
    return sorted(results, key=lambda result: result.item_id)


async def main() -> None:
    results = await run_all(["a", "b", "c"], run_partition, concurrency=2)
    print([result.value for result in results])


if __name__ == "__main__":
    asyncio.run(main())
```

Le réducteur doit définir, avant le démarrage du travail, comment il traite les revendications en double, les réponses contradictoires, les partitions manquantes et les échecs de l'évaluateur.

## Évaluation indépendante {#independent-evaluation}

Utilisez une séparation générateur/évaluateur lorsqu'une sortie requiert une décision de qualité ou de sûreté que le générateur ne peut pas certifier lui-même.

| Étape | Entrée | Sortie | Autorité |
|---|---|---|---|
| Générer | Contrat de travail et sources | Artefact candidat | Générateur |
| Valider | Candidat et critères figés | Constats réussite/échec | Validateur déterministe |
| Évaluer | Candidat, sources, critères | Verdict de revue | Évaluateur à portée indépendante |
| Décider | Reçus du validateur et de l'évaluateur | Publier, relancer ou suspendre | Contrôleur de workflow |

L'évaluateur ne doit pas hériter du raisonnement privé du générateur comme preuve. Fournissez-lui l'artefact, les critères acceptés et les sources primaires pertinentes. Cela réduit les défaillances corrélées ; cela ne garantit pas l'exactitude.

## Frontière du workflow durable {#durable-workflow-boundary}

Persistez l'état avant tout appel externe et réconciliez après un délai d'attente.

```text
PENDING -> RUNNING -> VALIDATING -> PASSED
                    |               |
                    v               v
                 RETRYABLE        PUBLISHED
                    |
                    v
                 FAILED
```

Règles de la machine à états :

- Un contrôleur, et non un worker, possède les transitions terminales.
- Chaque appel externe porte une clé d'idempotence stable.
- Un délai d'attente est un état inconnu, non un échec. Interrogez le reçu externe avant de relancer.
- La publication exige un état d'approbation distinct lorsqu'une revue éditoriale ou juridique est nécessaire.
- Un redémarrage reprend à partir du dernier état persisté et ne rejoue pas les effets de bord déjà accomplis.

## Agents inter-services {#cross-service-agents}

Utilisez un protocole inter-services uniquement lorsque les agents sont déployés ou détenus de manière indépendante. A2A fournit une frontière d'interopérabilité pour la communication entre agents ; MCP fournit une frontière gérée par l'hôte pour les outils et le contexte. [Protocole A2A](https://a2a-protocol.org/latest/) [Architecture MCP](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

Pour des agents au sein d'une même application, une API interne typée est généralement plus simple. N'introduisez un protocole public qu'après avoir défini les règles de compatibilité, d'authentification, de découverte, de délai d'attente et de versionnement.

## Les rôles sont de la documentation, pas de l'architecture {#roles-are-documentation-not-architecture}

Des noms comme chercheur, relecteur ou coordinateur ne sont utiles que lorsqu'ils correspondent à un contrat différent :

- **Chercheur :** accès en lecture seule aux sources et sortie structurée à la manière de citations.
- **Relecteur :** aucune autorité de modification et une grille de réussite/échec.
- **Coordinateur :** possède l'ordonnancement, les budgets et les transitions d'état.
- **Éditeur de publication :** peut écrire une sortie publique uniquement après un reçu d'approbation.

Si deux rôles partagent les mêmes outils, les mêmes données, le même budget et le même validateur, fusionnez-les jusqu'à ce qu'une séparation concrète soit nécessaire.

## Pièges {#gotchas}

- **Problème : des workers parallèles modifient le même enregistrement.** Une corruption de type « le dernier écrit gagne » peut ressembler à une fusion réussie. **Correctif :** partitionnez les entrées immuables et donnez à un seul réducteur la propriété exclusive de la sortie modifiable.
- **Problème : l'évaluateur n'est que le générateur invité à se louer ou à se critiquer lui-même.** Il hérite des mêmes angles morts et peut optimiser sa propre formulation. **Correctif :** utilisez un contexte séparé, des critères figés et des vérifications ancrées dans les sources.
- **Problème : un handoff fait perdre la responsabilité de la réponse finale.** L'utilisateur reçoit une réponse, mais le système n'a aucun propriétaire responsable. **Correctif :** enregistrez le propriétaire courant, la raison du routage et la règle de clôture après le handoff.
- **Problème : un délai d'attente est relancé comme un échec simple.** La première requête a pu déjà produire son effet. **Correctif :** réconciliez par clé d'idempotence ou par reçu du fournisseur avant d'émettre un nouvel appel.

## Limites {#limitations}

Les systèmes multi-agents augmentent le coût, la latence et la surface opérationnelle. Le parallélisme n'améliore le débit que pour un travail réellement indépendant. Un agent supplémentaire ne peut pas compenser une autorité des sources insuffisante, un critère d'acceptation flou ou un effet de bord sans contrat d'idempotence.

## Voir aussi {#see-also}

- [[agent-architectures]]
- [[agent-orchestration]]
- [[managed-agents]]
- [[multi-agent-messaging]]
- [[multi-session-coordination]]

## Sources {#sources}

- [SDK Agents d'OpenAI : orchestration d'agents](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [Protocole A2A](https://a2a-protocol.org/latest/)
- [Architecture du Model Context Protocol](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
