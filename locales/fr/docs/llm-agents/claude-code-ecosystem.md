---
title: "Surfaces d'extension et de gouvernance de Claude Code"
description: "Utiliser les plugins, skills, hooks, instructions de projet et subagents de Claude Code comme surfaces de gouvernance explicites et versionnées ; vérifier leur schéma actuel et leur portée effective avant déploiement."
tags: [claude-code, plugins, skills, hooks, subagents, governance]
level: 3
source_sha256: ac26a4cb1674052c821758614a66d72ab5acb94f7b69a08c2b2dcd1869182d89
translation: machine
translated_at: '2026-10-24'
---
# Surfaces d'extension et de gouvernance de Claude Code {#claude-code-extension-and-governance-surfaces}

**Périmètre vérifié : 2026-09-04.** Claude Code peut étendre une session via des instructions de projet, des plugins, des skills, des hooks et des subagents. Ce sont des surfaces de contrôle distinctes, avec des cycles de vie et des niveaux d'autorité différents. Ne considérez pas qu'une extension pratique prouve qu'une tâche s'est exécutée dans un environnement cloud donné, qu'une politique est appliquée partout, ou qu'un plugin peut être installé sans risque.

## Choisir la surface de contrôle la plus petite {#choose-the-smallest-control-surface}

| Besoin | Surface appropriée | Preuves à conserver |
|---|---|---|
| directives stables pour le dépôt | fichier d'instructions de projet | révision source relue et instructions effectives |
| playbook de tâche réutilisable | skill | déclencheur, périmètre et résultat de validation |
| réaction déterministe à un événement du cycle de vie | hook | schéma de l'événement, source du gestionnaire, enregistrement de sortie ou de décision |
| ensemble distribuable d'extensions liées | plugin | source, version, composants déclarés et approbation d'installation |
| investigation ou implémentation déléguée et bornée | subagent | frontière des outils, révision des entrées, preuves de sortie et résultat du vérificateur |

Une instruction courte ne peut pas, de manière fiable, faire respecter une politique sur les opérations destructrices. Un hook ne peut pas trancher une exigence produit qui demande un jugement humain. La description d'un subagent n'est pas une délégation d'autorisation. Placez chaque contrôle au niveau qui peut réellement le prouver ou l'appliquer.

## Les instructions de projet forment une couche de politique {#project-instructions-are-a-policy-layer}

Gardez les directives du dépôt concises, pertinentes pour la tâche et relisibles. Elles doivent nommer la commande de validation habituelle, les frontières d'architecture importantes, les données protégées et les règles d'escalade. Elles ne doivent pas dupliquer un linter ni prétendre qu'une instruction en langage naturel est un bac à sable.

Claude Code documente son système de mémoire de projet et le chargement des fichiers d'instructions séparément des plugins et des hooks. Inspectez les sources d'instructions effectives actuelles dans le client cible avant de vous appuyer sur la priorité ou l'inclusion automatique. [Comment Claude se souvient de votre projet](https://code.claude.com/docs/en/memory)

Une instruction utile répond à quatre questions :

1. quel dépôt ou quel chemin est dans le périmètre ;
2. ce que l'agent peut lire, modifier ou exécuter ;
3. quelles preuves déterminent le succès ;
4. quand il doit s'arrêter et demander à un responsable.

## Les plugins sont des entrées de la chaîne d'approvisionnement {#plugins-are-supply-chain-inputs}

Un plugin peut regrouper des capacités telles que des commandes, des agents, des skills, des hooks et une configuration liée à MCP. Sa forme de paquet et ses champs pris en charge évoluent : utilisez la référence actuelle des plugins au lieu de copier un ancien manifeste depuis un blog ou un dépôt. [Créer des plugins](https://code.claude.com/docs/en/plugins)

Avant toute installation ou mise à jour, consignez :

- l'éditeur et la révision source immuable ;
- les composants déclarés et leur comportement vis-à-vis des outils et du réseau ;
- les secrets requis, les chemins de données et les points de terminaison externes ;
- les preuves de compatibilité avec la version cible de Claude Code ;
- la procédure de retour arrière ou de désactivation ;
- le résultat de la validation dans un espace de travail jetable ou hors production.

N'approuvez pas un plugin simplement parce que le nom de sa commande semble familier. Un hook ou une intégration MCP embarqués peuvent affecter une frontière de confiance bien plus large qu'un skill en Markdown.

## Les hooks nécessitent un contrat déterministe {#hooks-need-a-deterministic-contract}

Les hooks actuels de Claude Code peuvent réagir à des événements du cycle de vie via des gestionnaires de type commande, HTTP, MCP, prompt ou agent. La référence des hooks documente le schéma des événements, le comportement des matchers, les formats d'entrée et de sortie, les contrôles de décision et les emplacements de configuration pris en charge. [Référence des hooks de Claude Code](https://code.claude.com/docs/en/hooks)

Pour chaque hook, déclarez :

| Champ | Exemple |
|---|---|
| déclencheur | un événement du cycle de vie nommé et un matcher étroit |
| entrée | champs JSON documentés utilisés par le gestionnaire |
| effet de bord | validation en lecture seule, écriture d'un artefact local ou notification |
| décision | aucune décision, autoriser, refuser ou différer, lorsque l'événement actuel le permet |
| politique d'échec | un timeout ou une erreur est visible et ne peut pas approuver silencieusement une action protégée |
| reçu | version du gestionnaire, résultat de sortie et révision concernée |

Utilisez les hooks pour des règles mécaniques évaluables à partir d'entrées déclarées. Évitez les hooks shell larges qui inspectent chaque commande, récupèrent des variables d'environnement non déclarées ou effectuent des appels réseau sans liste d'autorisation explicite ni timeout. Une sortie réussie sans sortie n'équivaut pas à une revue de sécurité.

## Déléguer avec des frontières de subagent {#delegate-with-subagent-boundaries}

Un subagent est utile lorsque ses entrées, ses outils et les preuves requises peuvent être bornés. Les définitions de subagents de Claude Code peuvent délimiter un rôle, ses instructions et les outils autorisés ; consultez la référence actuelle pour l'emplacement, les champs, la priorité et les limites propres au produit. [Créer des subagents personnalisés](https://code.claude.com/docs/en/subagents)

Utilisez un brief de tâche qui nomme :

```yaml
goal: verify the changed authentication paths
input: immutable revision and declared files
tools: read, search, and named test command only
writes: none
output: findings with file, evidence, and severity
stop_when: evidence is missing or the task exceeds the declared scope
```

Le workflow principal doit malgré tout inspecter les artefacts référencés et exécuter la porte de publication. Le texte produit par un subagent est une évaluation candidate, non un substitut au test, à la source ou au reçu de déploiement sous-jacent.

## Déployer les extensions en toute sécurité {#roll-out-extensions-safely}

1. relire la source de l'extension et son propriétaire ;
2. la tester dans un dépôt jetable ou un worktree isolé ;
3. consigner la configuration effective et les outils autorisés ;
4. exécuter une tâche à périmètre volontairement restreint ;
5. vérifier les artefacts produits et les effets externes éventuels ;
6. ne promouvoir qu'après qu'un relecteur a pu reproduire le résultat ;
7. conserver un chemin de désactivation pour les hooks, les plugins et les changements de politique.

Traitez une incompatibilité de schéma, un composant indisponible ou un reçu manquant comme un échec visible. Ne substituez pas silencieusement un autre plugin, une autre commande, un autre fournisseur ou un autre mode de permission.

## Modes de défaillance courants {#common-failure-modes}

- **Folklore de version :** nombres d'événements, options CLI ou champs de manifeste statiques recopiés d'une ancienne version.
- **Politique par la prose :** une règle de sécurité critique n'existe que dans un long fichier d'instructions.
- **Hook non borné :** un gestionnaire de commande accède à des données ou à des cibles réseau sans rapport avec son déclencheur.
- **Confiance dans le nom du plugin :** l'installation intervient sans revue de la source, des composants ou des permissions.
- **Délégation sans preuve :** un subagent affirme qu'un changement fonctionne, mais aucun test ni reçu de cible n'existe.
- **Repli caché :** une extension indisponible entraîne l'exécution d'une autre capacité, sans que l'opérateur en soit informé.

## Références {#references}

- [Référence des hooks de Claude Code](https://code.claude.com/docs/en/hooks)
- [Créer des plugins](https://code.claude.com/docs/en/plugins)
- [Créer des subagents personnalisés](https://code.claude.com/docs/en/subagents)
- [Comment Claude se souvient de votre projet](https://code.claude.com/docs/en/memory)
