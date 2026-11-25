---
title: "RL agentique pour la programmation compétitive"
category: patterns
tags: [llm-agents, reinforcement-learning, competitive-programming, code-generation, self-improvement, verification]
level: 3
source_sha256: e67f496f86cf2f4875d6113004431ee337dad7bc78f59e02200bff3811367288
translation: machine
translated_at: '2026-10-24'
---
# RL agentique pour la programmation compétitive {#agentic-rl-for-competitive-programming}

GrandCode (2026) atteint un niveau de grand maître sur les problèmes de programmation compétitive en combinant une boucle agentique et l'apprentissage par renforcement. L'idée clé : le RL classique entraîne une politique sur des trajectoires, alors que la programmation compétitive exige un raisonnement en plusieurs étapes, une autocorrection et une vérification externe, soit exactement le motif agentique. L'approche atteint le rang d'IGM (Grand Maître international) sur Codeforces, dépassant tous les systèmes d'IA précédents.

## Architecture principale {#core-architecture}

L'agent fonctionne selon une boucle **générer → exécuter → évaluer → améliorer** plutôt qu'en une seule passe de génération :

```python
# Simplified agentic RL loop (pseudocode)
def solve(problem: str, time_budget: int) -> str:
    solution = initial_draft(problem)
    for step in range(time_budget):
        result = run_tests(solution)           # external verifier
        if result.all_pass:
            return solution
        feedback = analyze_failures(result)    # step-level reward signal
        solution = refine(solution, feedback)  # policy update via RL
    return best_so_far
```

La politique est entraînée avec une **récompense de processus** (correction à chaque étape) plutôt qu'avec une **récompense de résultat** (succès ou échec final uniquement). C'est essentiel au niveau de difficulté grand maître, où une seule étape erronée dans une dérivation de 50 étapes produit un signal nul avec des récompenses éparses.

## Pourquoi le RL agentique surpasse la génération en une seule passe {#why-agentic-rl-beats-one-shot-generation}

| Approche | Pass@1 sur les problèmes difficiles | Benchmark IGM |
|---|---|---|
| GPT-4o (direct) | ~8 % | Non |
| o3-mini (chaîne de pensée) | ~23 % | Non |
| GrandCode (RL agentique) | ~61 % | Oui |

L'écart s'explique par le fait que les problèmes compétitifs difficiles exigent :

- **Itération guidée par les tests** : soumettre des solutions partielles et observer quels tests échouent
- **Découverte de cas limites** : le juge externe révèle des entrées que le modèle n'avait pas imaginées
- **Recherche multi-hypothèses** : essayer différentes approches algorithmiques en parallèle

La génération en une seule passe ne peut pas se rattraper après un mauvais choix d'algorithme. Une boucle agentique peut revenir en arrière.

## La vérification comme signal d'entraînement {#verification-as-the-training-signal}

Le composant d'infrastructure crucial : des **vérificateurs peu coûteux et déterministes**. La programmation compétitive dispose de vérificateurs parfaits (les cas de test du juge). La boucle de RL ne fonctionne que parce que :

1. Chaque solution intermédiaire peut être évaluée exactement
2. L'évaluation est rapide (quelques millisecondes par cas de test)
3. Le crédit partiel est significatif (% de tests réussis = récompense)

```python
# Process reward model
def step_reward(partial_solution: str, test_cases: list) -> float:
    passed = sum(run_test(partial_solution, t) for t in test_cases)
    return passed / len(test_cases)   # 0.0 → 1.0 dense signal
```

C'est pourquoi la programmation compétitive est un domaine d'entraînement RL idéal : le signal de récompense qui rend le RL difficile dans les tâches ouvertes est fourni gratuitement.

## Motif Memory Intelligence Agent (MIA) {#memory-intelligence-agent-mia-pattern}

Une autre piste de travaux (ECNU-SII/MIA) s'attaque à un goulot d'étranglement apparenté : dans les tâches de **recherche approfondie**, l'agent doit synthétiser des informations issues de dizaines d'appels d'outils. Sans gestion explicite de la mémoire, il perd les découvertes antérieures à mesure que le contexte se remplit.

MIA introduit une mémoire de travail structurée que l'agent lit et écrit explicitement :

```python
# MIA-style memory operations (conceptual)
memory = WorkingMemory()

# During research loop
finding = web_search(query)
memory.store(key=topic_hash(finding), value=summarize(finding))

# When forming final answer
relevant = memory.retrieve(query=current_subtask, top_k=5)
answer = synthesize(relevant + current_context)
```

L'amélioration mesurée : une réduction d'environ 40 % des « recherches répétées » (l'agent redécouvrant des informations déjà trouvées), ainsi que des gains de précision notables sur les benchmarks de recherche multi-sauts.

## Lien avec le motif Proof Loop {#connecting-to-proof-loop-pattern}

GrandCode et MIA mettent tous deux en œuvre le même motif sous-jacent :

```text
spec_freeze → build → evidence → fresh_verify → fix → verify_again
```

- **GrandCode** : spécification = énoncé du problème ; preuves = résultats des tests ; vérificateur indépendant = juge
- **MIA** : spécification = question de recherche ; preuves = contenu de la mémoire ; vérificateur indépendant = étape de synthèse

La différence avec les techniques de réflexion de [[agent-self-improvement]] : GrandCode s'appuie sur une **vérité terrain externe** (les tests du juge), et non sur une qualité auto-évaluée. Le vérificateur est extérieur à la politique optimisée. Cela empêche le modèle de manipuler sa propre métrique d'évaluation.

## Contraintes d'implémentation {#implementation-constraints}

- **La disponibilité des vérificateurs est le goulot d'étranglement** : cette approche se transpose directement à tout domaine disposant d'une vérification déterministe peu coûteuse (tests unitaires, prouveurs formels, validateurs de requêtes SQL). Elle ne se transpose pas aux tâches de génération ouverte sans modèle de récompense séparé.
- **Le coût d'exploration croît avec la difficulté du problème** : les problèmes de niveau grand maître nécessitent 50 à 200 étapes de raffinement ; les problèmes faciles en demandent 1 à 3. Dimensionnez le budget en conséquence.
- **Le RL nécessite des données de trajectoires** : atteindre le niveau grand maître a exigé un entraînement sur environ 500 000 trajectoires de programmation compétitive annotées de récompenses intermédiaires. Il ne s'agit pas d'un simple fine-tuning sur des solutions, mais d'un entraînement sur l'intégralité du processus de résolution.

## Pièges courants {#gotchas}

- **Une récompense éparse fait échouer le RL sur les problèmes difficiles** : si vous ne notez que la soumission finale, le signal de gradient pour une solution correcte à 90 % est identique à celui d'une solution correcte à 0 %. Utilisez le taux de réussite de la suite de tests comme récompense dense.
- **La fuite de tests invalide les résultats** : si les trajectoires d'entraînement incluent des problèmes de l'ensemble d'évaluation, les performances rapportées sont surestimées. Vérifiez la séparation entraînement/évaluation au niveau du problème, et non seulement au niveau de la solution.
- **Les cas de test générés par le modèle sont faibles** : les modèles tendent à générer des tests que leurs propres solutions réussissent. Utilisez des juges externes non utilisés pour l'entraînement ou des cas limites générés de manière adversariale.
- **Une mémoire sans oubli se dégrade** : la mémoire de type MIA accumule du bruit au fil des longues sessions. Mettez en place une décroissance de l'ancienneté ou une consolidation périodique pour éviter que la qualité de la recherche ne chute après plus de 50 écritures.

## Voir aussi {#see-also}

- [[agent-self-improvement]]
- [[agent-memory]]
- [[swarm-based-review-and-multisampling-in-agentic-workflows]]
- [[adaptive-patterns-for-autonomous-agents]]
