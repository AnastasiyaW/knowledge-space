---
title: "Auto-amélioration des agents"
description: "Une boucle d'expérimentation sûre pour améliorer les prompts, outils, code et politiques des agents grâce à des évaluations figées et un retour arrière"
level: 3
source_sha256: 3008cdc49d8be7a88fe016b21d0ee35a8ed0ef617c4e2fe4196150360e7d58ba
translation: machine
translated_at: '2026-10-24'
---
# Auto-amélioration des agents (septembre 2026) {#agent-self-improvement-september-2026}

Contexte de version : traitez une boucle d'amélioration comme un système expérimental. Sa métrique, son ensemble d'évaluation, ses conditions de garde, sa révision candidate et sa règle de retour arrière sont des entrées versionnées ; modifier l'une d'elles lance une nouvelle série d'expériences.

Un agent ne doit pas se déclarer lui-même amélioré. L'amélioration est une comparaison mesurée par rapport à une référence, sur une évaluation tenue à l'écart, avec des contrôles de garde pour la sécurité et l'exploitation.

## Ce qui peut être amélioré {#what-may-improve}

| Cible | Méthode initiale sûre | Preuves requises |
|---|---|---|
| Prompt/instructions | Une modification circonscrite | Évaluation de tâches figée et revue des sorties |
| Descriptions des outils/liste d'autorisation | Réduire ou clarifier l'ensemble des outils | Exactitude de l'usage des outils et tests d'actions refusées |
| Politique de récupération | Une modification de la récupération/du reranking | Évaluation des réponses ancrées dans les sources et des citations |
| Code du workflow | Modification isolée dans une branche/un worktree | Tests, build, revue indépendante |
| Sélection/configuration du modèle | Comparer des candidats | Même suite, relevé latence/coût/sécurité |
| Politique de mémoire à long terme | Essai contrôlé en bac à sable | Tests d'empoisonnement, d'expiration, de provenance et de confidentialité |

Ne modifiez ni le code source de production, ni les outils globaux, ni les identifiants, ni la mémoire uniquement sur la base de la réflexion du modèle. Utilisez un environnement isolé et ne promouvez que des artefacts vérifiés.

## Contrat minimal d'expérience {#minimal-experiment-contract}

```json
{
  "experiment_id": "agent-routing-2026-09-03-001",
  "baseline_revision": "git:abc123",
  "candidate_revision": "git:def456",
  "suite_digest": "sha256:...",
  "primary_metric": "accepted_task_rate",
  "guard_metrics": {
    "policy_violations_max": 0,
    "p95_latency_ms_max": 3000,
    "cost_per_task_max": 0.05
  },
  "decision": "pending"
}
```

Une métrique sans garde est vulnérable à une optimisation qui dégrade la sécurité, le coût, la latence ou la fiabilité. Un candidat sans référence fixe ni suite figée ne peut pas prouver un changement causal.

## Règle de conservation et de rejet {#keepreject-rule}

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    primary: float
    policy_violations: int
    p95_latency_ms: int
    cost_per_task: float


def accept(
    baseline: Evaluation,
    candidate: Evaluation,
    *,
    latency_limit: int,
    cost_limit: float,
) -> bool:
    return (
        candidate.primary > baseline.primary
        and candidate.policy_violations == 0
        and candidate.p95_latency_ms <= latency_limit
        and candidate.cost_per_task <= cost_limit
    )
```

Une évaluation réelle nécessite aussi des intervalles de confiance ou des exécutions répétées lorsque la variance d'échantillonnage est significative. La valeur par défaut prudente consiste à rejeter les égalités et les régressions.

## Boucle d'amélioration contrôlée {#controlled-improvement-loop}

1. Figez les critères d'acceptation, la suite de tests et le reçu de référence.
2. Générez ou sélectionnez une seule modification candidate.
3. Appliquez-la uniquement dans une branche/un worktree isolé ou un bac à sable.
4. Exécutez les tests déterministes ainsi que la même suite d'évaluation de l'agent.
5. Faites examiner les preuves et les cas défavorables par un évaluateur indépendant.
6. Ne conservez le candidat que s'il améliore la métrique principale et passe tous les contrôles de garde.
7. Conservez le candidat rejeté et son reçu ; n'écrasez jamais l'historique en silence.

L'idée centrale des projets expérimentaux pilotés par des agents, comme autoresearch, n'est utile que si l'évaluation est réelle et si le périmètre des modifications est contrôlé. Ce n'est pas une autorisation d'auto-modification illimitée.

## Réflexion et données de trajectoire {#reflection-and-trajectory-data}

La réflexion du modèle peut aider à formuler des hypothèses : une tâche échouée peut suggérer un contexte d'outil manquant, un prompt ambigu, un analyseur défaillant ou une condition d'arrêt incomplète. Ce n'est pas une vérité de référence.

Stockez un enregistrement structuré de l'échec :

```json
{
  "task_id": "eval_431",
  "revision": "git:def456",
  "terminal_state": "failed",
  "evidence": ["tool receipt: timeout", "output schema: invalid"],
  "hypothesis": "retry policy is missing an eligible timeout branch",
  "review_state": "unverified"
}
```

Utilisez ces éléments pour produire un candidat testable. N'entraînez pas le modèle sur des explications rédigées par le modèle et ne les promouvez pas tant que les faits sous-jacents n'ont pas été vérifiés.

## Conception de l'évaluation {#evaluation-design}

Une suite utile contient :

- des tâches courantes représentatives ;
- des tâches difficiles aux limites et de récupération après erreur ;
- des cas d'entrées malformées et de résultats d'outils ;
- des refus de politique et des tentatives d'injection adverses ;
- des cas de régression découverts en production ;
- des mesures de coût, de latence et de nouvelles tentatives.

Conservez un jeu de validation (holdout) qu'aucun optimiseur ni aucune boucle de réglage de prompts ne peut consulter. Faites entrer de nouveaux exemples cachés dans ce jeu après chaque version majeure.

## Frontière de promotion {#promotion-boundary}

Un candidat peut progresser selon les étapes suivantes :

```text
sandbox experiment -> local validation -> independent review
                   -> staged/canary evaluation -> production release
```

Les retours de production constituent une preuve, mais ils ne constituent pas une autorisation pour un système de se réécrire lui-même. Toute promotion reste soumise à la gestion des changements et à la capacité de retour arrière.

## Pièges {#gotchas}

- **L'agent peut optimiser la métrique plutôt que le résultat.** Un scoreur étroit peut être contourné. **Correctif :** utilisez plusieurs gardes, des cas adverses et une revue manuelle de sorties représentatives.
- **La fuite de données de test crée une fausse amélioration.** Une optimisation répétée sur le même ensemble visible finit par le sur-ajuster. **Correctif :** conservez un jeu de validation caché et réservez-le à la preuve de mise en production.
- **Les modifications multiples détruisent la causalité.** Un meilleur score ne permet pas d'identifier quelle modification a aidé. **Correctif :** modifiez une seule variable circonscrite par expérience et conservez le reçu complet.
- **Les réflexions du modèle peuvent inventer des causes.** Des explications plausibles ne sont pas des diagnostics. **Correctif :** reliez les hypothèses à des journaux, des reçus ou des tests reproductibles avant toute modification.
- **Un retour arrière sans intégrité des artefacts n'en est pas un.** Des branches mutables et des fichiers écrasés font perdre le dernier état connu comme bon. **Correctif :** utilisez des identifiants de commit immuables et des enregistrements d'évaluation versionnés.

## Sources {#sources}

- [OpenAI API : working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)

## Voir aussi {#see-also}

- [[agent-evaluation]]
- [[agent-design-patterns]]
- [[autonomous-agent-evolution]]
- [[production-patterns]]
- [[llm-fine-tuning-practical]]
