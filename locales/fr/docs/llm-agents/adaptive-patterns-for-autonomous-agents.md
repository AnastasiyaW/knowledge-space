---
title: "Modèles adaptatifs pour agents autonomes"
description: "Utiliser un état de tâche explicite, des hooks bornés, des sous-agents à capacités restreintes et des portes de validation fondées sur des preuves, plutôt que des déclencheurs par mots-clés opaques ou des scores d'ambiguïté arbitraires."
tags: [agents, orchestration, hooks, subagents, task-state, verification]
level: 3
source_sha256: 738a2f89a78e98f8f22921f17616444542f2a1087a38edc94f4d6845748d170f
translation: machine
translated_at: '2026-10-24'
---
# Modèles adaptatifs pour agents autonomes {#adaptive-patterns-for-autonomous-agents}

**Périmètre vérifié : 2026-09-04.** Un système d'agents adaptatif doit modifier son comportement parce qu'une condition observable et une politique déclarée l'exigent, et non parce qu'un mot-clé vague ou une supposition du modèle s'est déclenché. Les points d'extension actuels de Claude Code fournissent des skills, des hooks, des sous-agents, des équipes d'agents et des plugins ; ils ne rendent pas l'automatisation arbitraire sûre par défaut. [Extension overview](https://code.claude.com/docs/en/features-overview) [Hooks guide](https://code.claude.com/docs/en/hooks-guide)

## Adapter le mécanisme au besoin {#match-the-mechanism-to-the-need}

| Besoin | Mécanisme utile le plus simple | Preuve de réussite |
|---|---|---|
| contraintes récurrentes du projet | fichier d'instructions ou de règles versionné | une tâche respecte l'invariant déclaré |
| procédure réutilisable | skill avec un déclencheur précis | la procédure produit l'artefact attendu |
| pré/post-condition déterministe | hook de commande | code de sortie ou reçu structuré |
| tâche annexe ciblée | sous-agent à capacités restreintes | résultat borné et preuves issues des sources/tests |
| travail indépendant en parallèle | équipe d'agents ou worktree isolé | aucune collision sur l'état partagé et revue conjointe |
| livraison de longue durée | enregistrement de tâche durable | chaque élément atteint un reçu terminal |

N'introduisez pas un hook simplement parce qu'un comportement pourrait être utile. Un hook de cycle de vie est approprié lorsque le déclencheur, l'action autorisée, la sortie, le signal d'échec et le responsable sont tous connus.

## Privilégier l'activation déclarée plutôt que la devinette par mots-clés {#prefer-declared-activation-over-keyword-guessing}

Claude Code peut charger des skills lorsqu'ils sont pertinents et exécuter des hooks pour des événements de cycle de vie tels que UserPromptSubmit, PreToolUse, PostToolUse et SubagentStop. Un hook peut exécuter une commande, une requête HTTP, un outil MCP, un prompt ou un vérificateur agentique. Les hooks de commande sont le choix stable pour l'application déterministe ; les hooks d'agent sont documentés comme expérimentaux. [Hooks reference](https://code.claude.com/docs/en/hooks) [Agent-based hooks](https://code.claude.com/docs/en/hooks-guide)

Utilisez une petite table de politique plutôt qu'une expression régulière qui modifie silencieusement les permissions :

```json
{
  "event": "PreToolUse",
  "condition": "requested action writes to a production target",
  "action": "require approved change record",
  "on_unknown": "block with a visible reason",
  "receipt": "change-record id and tool outcome"
}
```

La correspondance par mots-clés peut être utile uniquement pour la sélection de contexte sans effet de bord. Elle ne doit jamais accorder des identifiants, choisir un locataire, étendre l'accès aux outils ou déclencher à elle seule un effet externe.

## Utiliser les questions comme porte de risque, non comme rituel de score {#use-questions-as-a-risk-gate-not-a-score-ritual}

Un seuil arbitraire tel que « 20 % d'ambiguïté » n'est ni une preuve de sûreté ni une exigence produit. Demandez une clarification lorsqu'une réponse est nécessaire pour choisir une cible irréversible, interpréter une frontière d'autorisation ou définir le critère d'acceptation. Sinon, exécutez l'action réversible suivante, dans le périmètre, et rapportez les preuves.

| Observation | Réponse sûre |
|---|---|
| la cible ou le périmètre de suppression est inconnu | s'arrêter avant toute modification et demander la cible exacte |
| l'intention de l'utilisateur est claire mais l'implémentation offre des choix | sélectionner l'implémentation réversible la plus simple et la vérifier |
| test ou reçu manquant | créer ou exécuter la validation réelle de la tâche avant de déclarer le succès |
| affirmation de source sensible au temps | récupérer la documentation primaire et dater le résultat |
| sous-tâche qui surchargerait le contexte principal | la déléguer avec des outils, un périmètre et un reçu attendu explicites |

Cela évite à la fois la supposition silencieuse et la boucle d'interrogation sans fin.

## État de tâche durable {#durable-task-state}

L'historique de conversation n'est pas un journal de transactions fiable. Conservez les éléments de travail dans un enregistrement visible depuis le dépôt, avec un identifiant stable, la révision de la source, le responsable, le statut terminal et la référence de preuve :

```json
{
  "task_id": "DOC-042",
  "source_revision": "immutable-git-sha",
  "status": "RUNNING",
  "acceptance": ["strict build passes", "fresh review passes"],
  "attempt": 1,
  "idempotency_key": "docs:la051-055:revision",
  "evidence": ["reports/doc-042/links.txt"],
  "next_recheck": "named command or external event"
}
```

Les transitions d'état valides doivent être explicites, par exemple PENDING vers RUNNING vers PASS, BLOCKED_EXTERNAL ou FAILED_RETRYABLE. Un message de chat d'apparence verte n'est pas un état terminal sans le reçu nommé.

## Lier l'état à l'espace de travail réel {#couple-state-to-the-actual-workspace}

Enregistrez la révision Git, le worktree et la commande de validation qui ont produit un résultat. Si une branche change, un ancien succès peut ne plus s'appliquer. Pour les modifications parallèles :

1. donner à chaque rédacteur un worktree isolé ou la propriété exclusive des fichiers ;
2. placer les ressources partagées modifiables derrière un verrou visible et une vérification de santé externe ;
3. réserver les identifiants ou URL externes avant le début du travail lorsque les doublons sont nuisibles ;
4. relancer la validation causale après une intégration ou un rebase ;
5. faire appel à un relecteur neuf pour les travaux importants touchant au public, à la sécurité ou aux publications.

Les sous-agents sont utiles parce que chacun dispose d'un contexte indépendant, d'instructions personnalisées et d'outils restreints. Ils ne remplacent pas une porte de fusion et leurs conclusions ne font pas autorité par elles-mêmes. [Subagents](https://code.claude.com/docs/en/subagents)

## La mémoire est une entrée publiable {#memory-is-a-publishable-input}

Gardez les connaissances opérationnelles faciles à parcourir :

- indexer les décisions durables du projet et son état courant ;
- rattacher les affirmations aux révisions de sources, journaux, tests ou reçus externes ;
- distinguer une observation datée d'une règle réutilisable ;
- rendre visibles les enregistrements périmés plutôt que de les traiter silencieusement comme actuels ;
- valider les liens et la propriété des documents sur lesquels l'automatisation va s'appuyer.

Un agent ne peut pas agir en toute sécurité sur une information qu'il ne peut ni récupérer ni valider avec les outils dont il dispose.

## Pièges courants {#gotchas}

- **Un mot-clé active un outil puissant.** Le langage naturel est ambigu et peut être contrôlé par un attaquant. **Correctif :** réserver les mots-clés au routage sans effet de bord ; rendre explicites les permissions et les effets externes.
- **Un hook de prompt fait appeler un LLM pour décider d'un invariant.** Le résultat peut varier et être difficile à auditer. **Correctif :** utiliser des hooks déterministes pour les politiques strictes ; garder le jugement du modèle à titre consultatif.
- **Un fichier de tâche indique « terminé » après une exécution partielle.** Un processus peut s'être arrêté avant l'effet de bord final. **Correctif :** exiger un reçu terminal qui prouve le résultat demandé.
- **Un sous-agent rapporte une revue positive de sa propre sortie.** Ce n'est pas une vérification indépendante. **Correctif :** faire appel à un relecteur distinct et neuf pour les travaux importants.
- **Un verrou périmé est récupéré sur la seule base de son horodatage.** Le processus d'origine peut encore détenir la ressource. **Correctif :** vérifier le processus réel ou le service externe avant de récupérer le verrou.

## Sources {#sources}

- [Claude Code extension overview](https://code.claude.com/docs/en/features-overview)
- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
- [Claude Code subagents](https://code.claude.com/docs/en/subagents)

## Voir aussi {#see-also}

- [[agent-design-patterns]]
- [[context-engineering]]
- [[agent-memory]]
- [[agent-orchestration]]
