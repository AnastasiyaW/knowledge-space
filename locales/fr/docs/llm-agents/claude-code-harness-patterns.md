---
title: "Schémas de harnais pour agents de codage"
description: "Une frontière pratique entre instructions, outils, contrôles déterministes, revue et preuves durables pour le travail des agents de codage."
tags: [coding-agents, harness, hooks, skills, testing, verification]
level: 4
source_sha256: 3b35b2430962d068196f086c208501b2594cf3bb077e895259cb7646a5cbeb7d
translation: machine
translated_at: '2026-10-24'
---
# Schémas de harnais pour agents de codage {#coding-agent-harness-patterns}

**Périmètre vérifié : 2026-09-03.** Un harnais est l'environnement d'exécution qui entoure un agent de codage. Son rôle n'est pas de donner à l'agent une apparence de rigueur : il rend le workflow voulu inspectable et permet à des contrôles déterministes de rejeter une modification invalide.

Ce guide évite les gains de vitesse universels revendiqués, les classements de produits et les recommandations d'outils tiers codées en dur. Mesurez un harnais dans son propre dépôt, par rapport à un critère de livraison déclaré.

## Cinq frontières {#five-boundaries}

| Frontière | Responsabilités | Ne doit pas gérer |
|---|---|---|
| contrat de tâche | critères d'acceptation, périmètre, autorité | décisions d'implémentation cachées |
| instructions | conventions du projet et routage | un substitut à une politique exécutable |
| outils et skills | workflows métier reproductibles | approbation finale de leur propre sortie |
| contrôles déterministes | build, tests, schéma, formatage, vérification des liens | jugement sur une intention produit non explicite |
| revue indépendante | risque sémantique et risque de mise en production | une réécriture sans limite d'une tâche déjà arrêtée |

Lorsqu'une couche ne peut pas être inspectée, invoquée ou vérifiée par l'agent, elle ne constitue pas un contrôle opérationnel.

## Commencer par un contrat de livraison {#start-with-a-delivery-contract}

Rédigez les critères d'acceptation avant toute modification :

1. nommez les chemins ou le comportement externe concernés ;
2. indiquez la commande de vérification exacte ou le justificatif observable ;
3. listez les actions irréversibles ou soumises à approbation ;
4. identifiez le responsable de chaque ressource modifiable ;
5. nommez le relecteur requis lorsque l'auto-revue ne suffit pas.

Conservez l'état de la tâche dans un artefact durable, et non uniquement dans l'historique du chat. Un manifeste concis peut suivre `PENDING`, `RUNNING`, `PASS` et `BLOCKED`, ainsi que le justificatif qui étaye un état terminal.

## Les instructions sont une configuration délimitée {#instructions-are-scoped-configuration}

Claude Code distingue actuellement les paramètres partagés du projet, les paramètres locaux au projet, les paramètres utilisateur et la politique gérée. Placez la configuration versionnée et sûre pour l'équipe dans le périmètre partagé du projet ; gardez les surcharges personnelles et les identifiants hors du dépôt. `/status` indique les sources chargées par la session active. [Paramètres de Claude Code](https://code.claude.com/docs/en/settings)

Le fichier d'instructions du projet ne doit répondre qu'aux questions qui ne peuvent pas être déduites à faible coût du code :

- où se trouvent la documentation d'architecture et de déploiement faisant autorité ;
- comment exécuter les vérifications requises ;
- les fichiers protégés, les limites concernant les secrets et les règles d'approbation ;
- les artefacts attendus de passation et de revue.

Ne transformez pas le fichier d'instructions en journal des modifications ni en vidage de prompts. Renvoyez vers des documents durables pour les connaissances détaillées.

## Les contrôles déterministes passent avant le jugement du modèle {#deterministic-controls-come-before-model-judgment}

Exécutez directement les vérifications mécaniques peu coûteuses :

| Risque de modification | Exemple de contrôle | Preuve |
|---|---|---|
| syntaxe ou format | formateur, parseur, vérificateur de types | code de sortie du processus et rapport |
| contrat modifié | test ciblé ou validation de schéma | sortie des assertions |
| documentation | vérifications des liens et du frontmatter | reçu de lint |
| artefact de publication | vérification du build ou du paquet | référence d'artefact immuable |
| comportement à risque | test d'intégration ou visible par l'utilisateur | trace, capture d'écran ou reçu de service |

Un LLM peut interpréter un rapport d'échec et proposer une correction. Il ne doit pas transformer un contrôle échoué en succès par simple explication.

## Hooks et skills ont des rôles différents {#hooks-and-skills-have-different-roles}

Claude Code prend en charge des hooks autour des événements du cycle de vie et des outils, et les subagents personnalisés peuvent porter un contexte ciblé ainsi que des permissions d'outils. Ce sont des points d'intégration, et non une preuve qu'un workflow a bien été suivi. [Référence des hooks](https://code.claude.com/docs/en/hooks) [Subagents personnalisés](https://code.claude.com/docs/en/sub-agents)

| Mécanisme | Bon usage | Garde-fou requis |
|---|---|---|
| skill | procédure métier ou checklist réutilisable | conditions de déclenchement et vérification exécutable |
| hook | enregistrer un événement ou bloquer une action interdite | entrées/sorties stables et comportement fail-closed lors de la publication |
| subagent | exploration bornée ou revue indépendante | propriété des fichiers, pas d'auto-certification, format de retour clair |
| script | inventaire ou validation déterministe | source versionnée, code de sortie, rapport conservé |

Ne faites pas d'un résultat d'outil non fiable une autorité exécutable. Analysez-le, validez-le et faites-le passer par la même frontière d'approbation que toute autre entrée.

## Une boucle de modification minimale {#a-minimal-change-loop}

```text
freeze acceptance criteria
        ↓
inspect code and relevant documentation
        ↓
make the smallest coherent change
        ↓
run the named deterministic checks
        ↓
collect receipts and inspect the diff
        ↓
independent review for material risk
        ↓
publish only after every required gate passes
```

La boucle devient utile lorsque chaque flèche correspond à un artefact durable. Un message de statut sans sortie de test, sans diff ni reçu d'exécution n'est pas une preuve.

## Isolation du worktree et du relecteur {#worktree-and-reviewer-isolation}

Utilisez un worktree Git séparé lorsque des travaux concurrents partageraient autrement une copie de travail modifiable. Git documente les worktrees liés comme des arbres de travail distincts rattachés à un même dépôt, ce qui permet d'avoir plusieurs branches extraites à la fois. [git-worktree](https://git-scm.com/docs/git-worktree)

Pour une modification publique importante, le relecteur doit lire le diff final de façon indépendante et renvoyer soit `PASS`, soit un constat précis avec le fichier, la ligne, l'impact et la correction minimale. L'auteur applique les corrections ; le relecteur ne certifie pas silencieusement, de mémoire, une implémentation modifiée.

## Mesurer localement, pas à partir du marketing {#measure-locally-not-by-marketing}

Si une équipe veut comparer des variantes de harnais, définissez :

- un corpus de tâches fixe et des révisions de dépôt figées ;
- le même modèle, les mêmes permissions et la même disponibilité des outils ;
- une métrique de qualité principale, comme les tests acceptés ou les constats de revue ;
- une mesure du coût et du temps écoulé ;
- une règle pour conserver, annuler ou répéter une expérience.

Sans ce cadre, un pourcentage publié relève de l'anecdote et non d'un résultat d'ingénierie.

## Pièges courants {#gotchas}

- **Un skill demande d'exécuter une vérification, mais aucun script n'existe.** La règle n'est pas applicable. **Correction :** ajoutez ou référencez la vérification exécutable la plus simple avant de la traiter comme un contrôle.
- **Un hook dispose d'un large droit d'écriture.** Il peut devenir un chemin de déploiement caché. **Correction :** limitez les hooks, journalisez-les et empêchez-les de contourner l'approbation normale de publication.
- **Le même agent écrit et approuve une modification risquée.** Il a les mêmes angles morts dans les deux rôles. **Correction :** exigez un relecteur neuf ou un contrôle externe déterministe.
- **Une suite de tests passe alors que la tâche a changé de forme.** Elle peut ne pas tester le comportement demandé. **Correction :** associez chaque critère d'acceptation à sa propre preuve.
- **Des agents parallèles partagent une copie de travail.** Les conflits sur les fichiers effacent l'intention. **Correction :** utilisez des worktrees ou des frontières de propriété explicites avant de modifier.

## Sources {#sources}

- [Paramètres de Claude Code](https://code.claude.com/docs/en/settings)
- [Hooks de Claude Code](https://code.claude.com/docs/en/hooks)
- [Subagents personnalisés de Claude Code](https://code.claude.com/docs/en/sub-agents)
- [Worktrees Git](https://git-scm.com/docs/git-worktree)

## Voir aussi {#see-also}

- [[agent-design-patterns]]
- [[agent-orchestration]]
- [[multi-session-coordination]]
- [[handoff-rollup-pattern]]
- [[production-patterns]]
