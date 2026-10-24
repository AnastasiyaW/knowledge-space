---
title: "Lois d'échelle des LLM et benchmarks"
description: "Utiliser la recherche sur les lois d'échelle et les suites de benchmarks sans transformer des ajustements historiques ou des instantanés de classements en décisions produit"
level: 3
source_sha256: efcfe64bc1a45ba02f60b1777b897c3e3105e6f96e776aa0bcc6da500db3062d
translation: machine
translated_at: '2026-10-24'
---
# Lois d'échelle des LLM et benchmarks (septembre 2026) {#llm-scaling-laws-and-benchmarks-september-2026}

Contexte de version : les ajustements de lois d'échelle et les scores de benchmarks sont des résultats empiriques obtenus avec des jeux de données, des budgets de calcul, des architectures, des prompts et des harnais d'évaluation précis. Ce ne sont ni des règles de dimensionnement universelles, ni des classements durables de modèles.

## À quelle question répondent les lois d'échelle {#what-scaling-laws-answer}

La recherche sur les lois d'échelle étudie comment une perte ou une capacité mesurée évolue lorsque le calcul d'entraînement, la taille du modèle, les données et les variables associées augmentent. Elle est utile pour :

- planifier un programme de pré-entraînement ou de pré-entraînement continu contrôlé ;
- choisir les expériences coûteuses à mener ensuite ;
- détecter des configurations candidates manifestement sous-entraînées ;
- cadrer un compromis calcul/données dans une méthodologie figée.

Elle ne permet pas à elle seule de choisir un modèle en production, de prouver la sécurité en aval, ni de prédire la latence et le coût sous une charge de service réelle.

L'étude Chinchilla a rapporté que, pour son réglage optimal en calcul, la taille du modèle et le nombre de tokens d'entraînement doivent croître proportionnellement. Ce résultat est un ajustement historique sur un régime expérimental particulier. Ne l'utilisez comme règle d'approvisionnement `tokens-per-parameter` qu'après validation sur l'architecture, les données et l'objectif réels.

## Séparer trois décisions {#separate-three-decisions}

| Décision | Preuves qui la tranchent |
|---|---|
| Allocation du pré-entraînement | Expériences contrôlées de perte et de capacité, provenance du calcul et des données |
| Conception du service | Latence, débit, mémoire, disponibilité et coût unitaire mesurés |
| Acceptation produit | Suite de tâches figée, contrôles de sécurité et revue des erreurs pertinentes pour l'utilisateur |

Confondre ces décisions mène à de fausses conclusions : un modèle plus grand peut être un moins bon choix produit s'il échoue sur le flux de travail visé, ne respecte pas un SLO ou ne peut pas être exploité en toute sécurité.

## Inventaire des benchmarks {#benchmark-inventory}

Un benchmark n'est utile que si sa tâche, sa version, son prompt, sa méthode de notation et son risque de contamination sont connus.

| Catégorie | Exemple d'usage | Question de mise en production |
|---|---|---|
| Connaissances/raisonnement généraux | Suite de type MMLU | Le candidat régresse-t-il sur une capacité générale pertinente pour le produit ? |
| Ensemble de tâches métier | Corpus interne annoté | Résout-il correctement le travail réel ? |
| Jeu de robustesse / adversarial | Injection de prompt, refus, entrée malformée | Échoue-t-il de manière sûre ? |
| Évaluation de l'usage d'outils | Contrats d'outils enregistrés | Sélectionne-t-il les actions permises et respecte-t-il les schémas ? |
| Test opérationnel | Exercice de charge et de pannes | Peut-il respecter les bornes de latence, d'erreur et de coût ? |

MMLU est un benchmark académique largement cité, mais un score agrégé unique ne constitue pas une preuve qu'un agent est fiable sur la tâche d'une organisation. Conservez les résultats de benchmarks comme signaux de diagnostic, à côté d'une évaluation spécifique au produit.

## Fiche d'évaluation {#evaluation-record}

Chaque comparaison nécessite un récépissé immuable. Cela évite qu'un chiffre de classement perde les paramètres qui l'ont produit.

```json
{
  "evaluation_id": "support-routing-2026-09-03",
  "candidate": {"model": "candidate-id", "revision": "immutable-revision"},
  "baseline": {"model": "baseline-id", "revision": "immutable-revision"},
  "suite": {"name": "support-routing-v4", "digest": "sha256:..."},
  "harness": {"commit": "git-sha", "prompt_policy": "prompt-v7"},
  "metrics": {
    "route_accuracy": 0.0,
    "schema_valid_rate": 0.0,
    "p95_latency_ms": 0,
    "cost_per_accepted_output": 0.0
  },
  "verdict": "hold"
}
```

Utilisez le même ensemble d'entrées, la même politique de décodage, la même disponibilité des outils et la même méthode de notation pour la référence et le candidat. Si l'un de ces éléments change, lancez une nouvelle comparaison plutôt que de fusionner les chiffres.

## Contamination et reproductibilité {#contamination-and-reproducibility}

Les benchmarks publics peuvent être présents dans les données de pré-entraînement ou de réglage par instructions. Un score élevé peut indiquer une mémorisation, une sensibilité au prompt ou une optimisation propre au test, plutôt qu'une performance transférable.

Mesures d'atténuation :

1. Suivre la révision du benchmark et la licence de sa source.
2. Conserver une suite de tâches privée, nouvellement collectée, qui n'est jamais utilisée pour le réglage.
3. Renouveler les cas cachés tout en préservant des cas de régression stables.
4. Consigner les prompts, les graines aléatoires, les paramètres d'échantillonnage et la politique d'outils.
5. Inspecter manuellement des succès et des échecs représentatifs.

## Procédure de sélection du modèle {#model-selection-procedure}

1. Définir un contrat d'acceptation : qualité des résultats, sécurité, latence, disponibilité et budget.
2. Établir une référence avec la politique de prompt et d'outils déployée.
3. Tester un petit ensemble de niveaux de candidats sur la même suite figée.
4. Examiner les tranches d'erreurs, et pas seulement la moyenne.
5. Retenir le candidat le moins coûteux qui satisfait tous les seuils requis.
6. Conserver le récépissé et planifier une réévaluation lorsque le modèle, les prompts, les outils ou le corpus changent.

## Pièges {#gotchas}

- **Un coefficient de loi d'échelle n'est pas un paramètre de déploiement.** Il a été estimé sous des hypothèses précises. **Correction :** utilisez-le pour choisir les expériences, puis mesurez la charge de travail qui sera réellement servie.
- **Les scores agrégés masquent les tranches inacceptables.** Un modèle peut améliorer la moyenne tout en échouant sur une langue réglementée, une cohorte difficile ou une condition de sécurité. **Correction :** fixer des seuils de mise en production explicites par tranche.
- **Les instantanés de classements dérivent.** Harnais, prompts, jeux de données et révisions de modèles changent. **Correction :** publier le récépissé d'évaluation complet plutôt qu'un score sans source.
- **Le succès à un benchmark ne prouve pas la sécurité des outils.** La précision à choix multiples ne permet pas de vérifier les effets de bord, les permissions ou les nouvelles tentatives. **Correction :** tester séparément les contrats d'outils enregistrés et les scénarios opérationnels adversariaux.

## Sources {#sources}

- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)
- [Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300)
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)

## Voir aussi {#see-also}

- [[frontier-models]]
- [[model-optimization]]
- [[agent-evaluation]]
- [[llm-fine-tuning-practical]]
