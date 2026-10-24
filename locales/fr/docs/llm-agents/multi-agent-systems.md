---
title: "Coordination des systèmes multi-agents"
description: "Coordonner plusieurs agents au moyen de contrats de tâche, de propriété, d'autorité, d'état et de frontières de preuve ; n'ajouter des agents que lorsqu'une décomposition mesurée les rend nécessaires."
tags: [llm-agents, multi-agent, orchestration, delegation, governance, evidence]
level: 4
source_sha256: 1ffe0801345085a3b71865858c3efce0d6e973d2e1859490fc38255358443c3f
translation: machine
translated_at: '2026-10-24'
---
# Coordination des systèmes multi-agents {#multi-agent-system-coordination}

**Périmètre vérifié : 2026-09-04.** Un système multi-agents est un workflow comportant plus d'un décideur autonome ou d'un rôle d'exécution. Il n'est pas automatiquement plus capable qu'un agent unique. N'ajouter un rôle que lorsque la tâche admet une décomposition claire, une frontière d'autorité ou d'outillage distincte, et un moyen d'évaluer le coût supplémentaire de coordination.

## Commencer par le contrat de travail {#start-with-the-work-contract}

Chaque tâche déléguée a besoin d'un enregistrement qui survit aux messages et aux redémarrages.

```json
{
  "task_id": "docs-review-001",
  "input_revision": "immutable source revision",
  "owner": "named coordinator",
  "acceptance": ["named checks pass", "evidence is attached"],
  "authority": "read-only review",
  "allowed_tools": ["read", "search", "named test"],
  "side_effect_policy": "no external actions",
  "handoff": "structured findings with source references"
}
```

Le contrat empêche un rôle spécialisé de devenir une persona vague. Il permet au coordinateur de distinguer une tâche réellement terminée d'un message qui se contente de paraître complet.

## Utiliser la forme de coordination la plus simple {#use-the-simplest-coordination-shape}

| Forme | Cas d'usage adapté | Risque principal |
|---|---|---|
| agent unique avec outils déterministes | une tâche cohérente et une seule frontière d'autorité | une délégation inutile dilue la responsabilité |
| pipeline séquentiel | chaque artefact est l'entrée de l'étape suivante bien définie | une erreur précoce devient un contexte aval non contrôlé |
| investigation parallèle | sources, tests ou conceptions candidates indépendants | travail dupliqué et hypothèses corrélées |
| superviseur avec travailleurs bornés | plusieurs contrats de tâche distincts nécessitent un responsable final | le superviseur devient un goulot d'étranglement non testable |
| relecteur indépendant | un changement significatif requiert une évaluation neuve | le relecteur est invité à approuver sans accès aux preuves |

Ne pas choisir un nombre d'agents à partir d'un modèle. Mesurer si le goulot d'étranglement actuel est un manque de preuves, un accès insuffisant aux outils, ou un besoin réel de relecture indépendante. Une transformation déterministe doit rester du code, même si un agent peut la décrire.

## Séparer l'état selon le modèle de concurrence {#separate-state-by-concurrency-model}

| Type d'état | Schéma de coordination sûr |
|---|---|
| entrée ou preuve immuable | empreinte de contenu et références en lecture seule |
| constats ou accusés de réception en ajout seul | un enregistrement par producteur, avec identifiants stables |
| propriété mutable d'une tâche | un bail ou un unique rédacteur explicite |
| artefact partagé en cours de modification | worktree ou branche isolé, puis fusion relue |
| question adressée | message avec expéditeur, destinataire et enregistrement de la réponse |
| effet de bord externe | clé d'idempotence, responsable nommé et accusé de réception de la cible |

Éviter un bloc-notes partagé unique que tout agent peut réécrire. Il rend la perte, le conflit et l'injection accidentelle d'instructions difficiles à attribuer. Si un agent a besoin d'un verrou, enregistrer la ressource, le détenteur, le battement de cœur, l'expiration et la vérification de reprise.

## L'autorité ne transite pas par un transfert {#authority-does-not-flow-through-a-handoff}

Un coordinateur peut demander à un agent d'investiguer un incident de production sans lui accorder de droits de déploiement. Les permissions d'outils, l'accès aux données, la politique d'approbation et l'environnement cible doivent être attribués par rôle. Un message transmis, un résumé ou un score de confiance d'agent ne peut pas élever l'autorité.

Les sous-agents de Claude Code constituent un exemple concret de système où des rôles délégués peuvent être définis avec des instructions et des limites d'outils circonscrites ; consulter la documentation produit actuelle pour les champs exacts et leur ordre de priorité. [Create custom subagents](https://code.claude.com/docs/en/subagents)

Pour un système ayant des effets externes, utiliser une porte de publication située hors de la boucle de débat :

1. le travailleur produit un candidat et ses preuves ;
2. un vérificateur compare les preuves au contrat d'acceptation ;
3. un responsable nommé fournit toute approbation requise ;
4. l'exécutant autorisé réalise l'action, avec une clé d'idempotence le cas échéant ;
5. le workflow enregistre l'accusé de réception effectif de la cible.

## Revue et agrégation {#review-and-aggregation}

Le travail parallèle doit converger par les preuves, et non par le décompte des votes. Le coordinateur peut comparer des sources collectées indépendamment, des résultats de tests déterministes et des compromis bornés. Il doit pouvoir répondre « non démontré » lorsqu'aucun candidat ne satisfait le contrat.

Pour les préoccupations de sécurité ou de sûreté, conserver l'union des constats comme tri initial, et vérifier chaque constat avant de le traiter comme un défaut ou de modifier une cible. Le profil de risque de l'IA générative du NIST constitue un cadre utile pour maintenir les preuves de risque et de gouvernance tout au long du cycle de vie d'un système. [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## Évaluer la décomposition {#evaluate-the-decomposition}

Un workflow multi-agents doit être évalué à deux niveaux :

| Niveau | Question |
|---|---|
| rôle | chaque travailleur produit-il l'artefact requis dans le cadre de son autorité ? |
| système | le transfert préserve-t-il les entrées, les contraintes et les preuves jusqu'à la complétion ? |
| opérationnel | les nouvelles tentatives, les échecs, les verrous et les effets de bord restent-ils visibles et récupérables ? |
| comparatif | l'équipe améliore-t-elle le résultat d'acceptation de la tâche par rapport à une base plus simple ? |

Conserver l'agencement le plus simple qui satisfait le contrat d'acceptation. Davantage de messages, de rôles et d'appels de modèle peuvent augmenter la latence, le coût et les incohérences d'état sans apporter de nouvelles preuves.

## Modes de défaillance courants {#common-failure-modes}

- **Théâtre des rôles :** des noms comme « chercheur » ou « critique » remplacent un contrat concret d'entrée et de sortie.
- **Mémoire partagée mutable :** des agents écrasent mutuellement leur état ou traitent des notes comme une autorité.
- **Permission déléguée :** un transfert est pris pour une approbation d'utilisation d'un secret ou d'une cible de production.
- **Consensus comme preuve :** plusieurs agents répètent la même affirmation non étayée.
- **Nouvelles tentatives sans limite :** un travailleur en échec est relancé sans limite de tentatives ni condition de reprise.
- **Absence de preuve d'intégration :** chaque rôle réussit localement, mais le workflow combiné ne dispose d'aucun accusé de réception de la cible.

## Références {#references}

- [Create custom subagents](https://code.claude.com/docs/en/subagents)
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
