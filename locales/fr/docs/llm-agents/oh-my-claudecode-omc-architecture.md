---
title: "Intégration d'Oh My ClaudeCode (OMC)"
description: "Comment adopter le plugin OMC, qui évolue rapidement, sans confondre les commandes tierces, le routage de modèles ou l'état généré avec une frontière de sécurité ou de publication stable."
tags: [claude-code, plugins, orchestration, omc, supply-chain, worktrees]
level: 3
source_sha256: 5e2e46d169e40e41451a6512b69f9abcc91879d6259254cd3c5180460e7aa5da
translation: machine
translated_at: '2026-10-24'
---
# Intégration d'Oh My ClaudeCode (OMC) {#oh-my-claudecode-omc-integration}

**Périmètre vérifié : 2026-09-04.** Oh My ClaudeCode (OMC) est une couche d'orchestration multi-agents tierce pour Claude Code. Son dépôt présente actuellement un chemin d'installation sous forme de plugin Claude Code ainsi qu'un paquet terminal publié séparément, mais ses commandes, son comportement de compatibilité et ses fichiers internes évoluent rapidement. Considérez le dépôt et la révision installée comme référence pour la version que vous exécutez ; ne vous fiez pas à des nombres d'agents fixes, à des noms de modèles, à des tarifs en jetons ni à d'anciens alias de commandes. [Dépôt OMC](https://github.com/Yeachan-Heo/oh-my-claudecode) [Plugins Claude Code](https://code.claude.com/docs/en/plugins)

## Choisir la surface d'installation {#choose-the-installation-surface}

Le dépôt OMC documente deux surfaces distinctes :

| Surface | Utilisation | Frontière |
|---|---|---|
| plugin Claude Code | compétences, hooks, agents et commandes slash en session | soumis à la politique des plugins Claude Code |
| paquet terminal | installation, mise à jour, diagnostics et workflows CLI documentés | exécutable local avec ses propres dépendances |

La procédure d'installation documentée du plugin est :

```text
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
```

Le dépôt documente également le paquet terminal, qui porte un nom distinct. Installez-le uniquement selon sa documentation actuelle et inspectez la version obtenue avant de considérer un exemple de CLI comme exécutable. En particulier, le projet distingue les compétences en session des commandes terminal ; n'inventez pas de sous-commande CLI OMC parce qu'une commande slash au nom similaire existe. [README OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)

## Considérer OMC comme une intégration, non comme une frontière de confiance {#treat-omc-as-an-integration-not-a-trust-boundary}

OMC peut coordonner la planification, la revue et plusieurs CLI de fournisseurs locaux, mais il ne remplace pas :

- les instructions du dépôt et la validation déterministe ;
- la revue de code et l'approbation de publication ;
- l'autorisation liée aux locataires, aux identifiants ou à la production ;
- l'historique Git, l'isolation par worktree et l'idempotence côté externe ;
- une revue de la chaîne d'approvisionnement des plugins et des dépendances locales.

Ses artefacts générés ne constituent des preuves opérationnelles utiles que s'ils identifient la révision d'entrée, la commande, la sortie et le responsable. Un plan, une boucle de consensus ou un libellé d'agent ne prouve pas qu'un build, une migration ou un effet de bord externe a réussi.

## Modèle d'adoption sûr {#safe-adoption-pattern}

Avant d'activer le plugin dans un dépôt de travail :

1. épinglez et consignez la révision du dépôt ou du paquet évaluée ;
2. inspectez le manifeste du plugin, les agents, compétences, hooks et la configuration MCP déclarés, ainsi que le script d'installation ;
3. identifiez chaque CLI ou fournisseur externe que le workflow est susceptible d'invoquer ;
4. testez dans un worktree isolé avec des identifiants et des données hors production ;
5. exécutez les contrôles propres au dépôt après que le plugin a modifié des fichiers ;
6. conservez une voie de retour arrière et retirez l'intégration par son mécanisme supporté si elle échoue à la revue.

Les plugins Claude Code regroupent des compétences, des agents, des hooks, des serveurs MCP et d'autres composants. La source d'installation mérite donc le même examen que toute autre dépendance exécutable. [Référence des plugins](https://code.claude.com/docs/en/plugins-reference)

## Routage vers l'équipe et les fournisseurs {#team-and-provider-routing}

Le dépôt OMC actuel présente Team comme sa surface d'orchestration canonique et documente la migration loin de la terminologie « swarm » héritée. Il s'agit d'un fait propre à une version du dépôt, non d'un standard général pour les systèmes multi-agents. Vérifiez la documentation installée avant d'automatiser une commande ou de former un opérateur à un raccourci. [README OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)

Lorsqu'un workflow achemine une tâche vers un autre fournisseur local ou distant :

1. classez l'entrée avant de la transmettre ;
2. gardez les identifiants, le contenu client, le code source privé et les secrets hors des prompts de tiers, sauf si un circuit de données approuvé existe ;
3. consignez le fournisseur, le modèle et la révision de CLI réellement exécutés ;
4. traitez le texte renvoyé comme non fiable tant que les contrôles du dépôt et une revue humaine ou indépendante ne l'ont pas validé ;
5. évitez le basculement automatique vers un autre fournisseur pour les mutations, sauf si le contrat de bascule est explicite.

La frontière utile n'est pas « multi-modèle » ; c'est un contrat de transfert revu, avec un résultat observable.

## Worktrees et état durable {#worktrees-and-durable-state}

Utilisez des worktrees Git ou des checkouts isolés équivalents pour les écrivains concurrents. Un coordinateur doit tenir un enregistrement de tâche unique contenant la propriété, la révision cible, les contrôles attendus, la clé de réservation/d'idempotence externe et un reçu terminal. Ne laissez jamais deux workers modifier le même ensemble de fichiers simplement parce qu'un outil d'orchestration les appelle une équipe.

L'état généré peut être un détail d'implémentation de la version OMC installée. Conservez les décisions du projet, les modifications de source, les preuves de publication et les enregistrements de passation dans des chemins gérés par le dépôt, dans des formats relisibles, plutôt que de vous fier au seul cache d'un plugin comme source de vérité.

## Procédure de mise à jour {#upgrade-procedure}

1. lisez les notes de version amont et les instructions d'installation actuelles ;
2. consignez la révision existante du plugin ou du paquet ainsi que sa configuration ;
3. mettez à jour d'abord dans un dépôt jetable ou isolé ;
4. exécutez la commande de diagnostic documentée si le projet en fournit une ;
5. comparez les composants installés et les modifications de configuration ;
6. exécutez des tâches représentatives hors production et la validation du dépôt ;
7. ne promouvez qu'avec une révision de retour arrière et un reçu.

Cette procédure détecte les alias supprimés, les changements d'accès aux outils, les migrations d'état généré et les changements de comportement avant qu'ils n'affectent les travaux de publication.

## Pièges fréquents {#gotchas}

- **Une commande OMC historique apparaît encore dans un article de blog.** Elle a pu être renommée ou supprimée. **Correctif :** utilisez la documentation actuelle du dépôt pour la révision installée.
- **Un plugin est installé directement dans un dépôt de production.** Des hooks ou le script d'installation peuvent modifier le comportement avant toute revue. **Correctif :** inspectez et testez d'abord dans un worktree isolé.
- **Un planificateur produit un artefact très détaillé.** Le détail n'est pas une vérification. **Correctif :** liez chaque tâche aux tests, builds et reçus de publication réels du dépôt.
- **Un fournisseur routé reçoit par défaut le code source privé.** Cela peut enfreindre la frontière des données. **Correctif :** classez et minimisez l'entrée avant tout transfert.
- **Des workers parallèles modifient les mêmes fichiers.** Un libellé d'orchestration ne sérialise pas les écritures. **Correctif :** attribuez une propriété exclusive des fichiers, ou utilisez des worktrees séparés et intégrez via la revue.

## Sources {#sources}

- [Dépôt Oh My ClaudeCode et README actuel](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Plugins Claude Code](https://code.claude.com/docs/en/plugins)
- [Référence des plugins Claude Code](https://code.claude.com/docs/en/plugins-reference)
- [Sous-agents Claude Code](https://code.claude.com/docs/en/subagents)

## Voir aussi {#see-also}

- [[claude-code-harness-patterns]]
- [[adaptive-patterns-for-autonomous-agents]]
- [[multi-session-coordination]]
- [[agent-orchestration]]
