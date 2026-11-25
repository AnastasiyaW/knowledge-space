---
title: "Subagents Claude Code gérés par l'organisation"
description: "Définir des subagents Claude Code gérés par l'organisation avec un périmètre explicite, une priorité, des limites d'outils et une vérification, plutôt que de traiter la configuration gérée comme un runtime d'exécution cloud."
tags: [claude-code, subagents, managed-settings, governance, permissions]
level: 3
source_sha256: 521fa292162fc623c0ec94a1fc851ad30fb9a83f1f864aa73f7553905beae593
translation: machine
translated_at: '2026-10-24'
---
# Subagents Claude Code gérés par l'organisation {#organization-managed-claude-code-subagents}

**Périmètre vérifié : 2026-09-04.** Dans la documentation actuelle de Claude Code, un subagent géré est une définition de subagent fournie par l'organisation et distribuée via les paramètres gérés (managed settings). Ce n'est pas un runtime hébergé de type « Brain/Hands/Session », ni un produit de bac à sable facturé par le fournisseur, ni une garantie d'exécution persistante dans le cloud. Les définitions gérées utilisent le même format Markdown avec frontmatter YAML que les subagents utilisateur et projet, et prennent le pas lorsqu'une définition portant le même nom existe à un niveau de portée inférieur. [Subagents Claude Code](https://code.claude.com/docs/en/subagents)

## Portées de définition et priorité {#definition-scopes-and-precedence}

| Portée | Usage prévu | Responsable |
|---|---|---|
| user | workflows personnels réutilisables | développeur individuel |
| project | workflow partagé propre à un dépôt | équipe du dépôt |
| managed | politique de l'organisation et agents maintenus centralement | administrateur de l'organisation |
| plugin | paquet distribuable, tiers ou interne | éditeur du plugin |

Choisissez la portée la plus étroite compatible avec le responsable requis. Une définition gérée peut remplacer une définition project ou user portant le même nom : les noms doivent donc être traités comme faisant partie de la surface de la politique de l'organisation. [Configuration des subagents](https://code.claude.com/docs/en/configuration)

## Définir un agent borné {#define-a-bounded-agent}

Une définition d'agent se compose d'un frontmatter suivi des instructions Markdown de l'agent. L'exemple ci-dessous est volontairement en lecture seule ; adaptez les champs exacts et les outils autorisés à la référence Claude Code en vigueur avant le déploiement.

```markdown
---
name: policy-reviewer
description: "Read-only review of dependency and repository policy changes."
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---

Inspect the requested revision. Return findings with file references,
severity, evidence, and the smallest corrective action. Do not modify files.
```

Rédigez une description suffisamment précise pour que la délégation automatique soit prévisible. Le corps doit définir les éléments de preuve pertinents, les outils autorisés, la condition d'arrêt et la structure de réponse attendue. Un simple intitulé de rôle ne constitue pas une frontière de sécurité. [Créer des subagents personnalisés](https://code.claude.com/docs/en/subagents)

## Séparer la configuration de l'exécution {#separate-configuration-from-execution}

Les paramètres gérés peuvent distribuer une définition, mais ils ne prouvent pas qu'une tâche s'est exécutée dans un conteneur, une région, un compte ou un modèle de rétention donné. Établissez ces faits au niveau de l'exécution :

1. enregistrer la version du client, la source effective des paramètres et la révision de l'espace de travail ;
2. contraindre les outils et les permissions avant le début de la tâche ;
3. donner à l'agent le plus petit périmètre de données et de dépôts nécessaire ;
4. stocker en dehors du chat les reçus des effets de bord externes et les clés d'idempotence ;
5. exécuter la validation déterministe de la tâche ;
6. exiger une revue indépendante lorsque la modification est significative.

N'associez pas de chiffres fixes de latence, de coût, de persistance de session ou de résidence des données à une fonctionnalité de configuration, sauf si le fournisseur publie un contrat actuel pour le runtime exact.

## Frontières des plugins {#plugin-boundaries}

Les plugins peuvent embarquer des agents spécialisés, des skills, des hooks, des serveurs MCP et d'autres composants associés. Claude Code documente une restriction importante : les subagents fournis par un plugin ne prennent pas en charge les champs de frontmatter relatifs aux hooks, aux serveurs MCP ou au mode de permission ; ces champs sont ignorés. Si un workflow nécessite de tels contrôles, utilisez la couche user, project ou managed appropriée, et vérifiez la politique effective. [Référence des plugins](https://code.claude.com/docs/en/plugins-reference)

Cela empêche qu'une déclaration d'agent dans un plugin devienne silencieusement une frontière de confiance universelle. Un plugin peut tout de même influencer le travail à travers ses instructions et ses composants déclarés ; traitez donc l'installation et les mises à jour comme une décision relative à la chaîne d'approvisionnement.

## Schéma opérationnel {#operational-pattern}

Utilisez un contrat clair pour chaque agent géré centralement :

| Champ du contrat | Exemple |
|---|---|
| déclencheur | une revue de politique du dépôt est demandée |
| périmètre d'entrée | révision extraite et chemins déclarés uniquement |
| périmètre des outils | commandes de lecture, recherche et test, aucune écriture |
| sortie | constats structurés avec reçu source/test |
| escalade | autorisation inconnue ou cible de production |
| signal d'échec | vérification en échec, preuve manquante ou état bloqué explicite |
| responsable | équipe de l'organisation qui maintient la définition |

Enregistrez quelle définition effective a été exécutée. Une modification de politique gérée peut changer le comportement d'un agent sans toucher au dépôt ; un reçu de publication doit donc contenir à la fois la révision du projet et la version ou l'identifiant de la configuration gérée applicable.

## Déploiement et gestion des changements {#rollout-and-change-control}

1. relire la définition de l'agent comme une configuration de production ;
2. la tester sur un worktree jetable ou isolé ;
3. confirmer que les doublons de portée inférieure ne masquent pas la définition visée ;
4. exécuter des appels d'outils représentatifs autorisés et refusés ;
5. publier le contrat attendu pour les constats et la sortie ;
6. conserver une version de retour arrière et un enregistrement daté du déploiement.

Pour un agent de sécurité ou de conformité, ne laissez pas le même agent rédiger une modification et la certifier. Utilisez un relecteur à périmètre distinct ou une porte de contrôle déterministe.

## Pièges {#gotchas}

- **Un agent project et un agent managed partagent le même nom.** Le comportement effectif peut être celui de la définition gérée. **Correctif :** utiliser des noms explicites et vérifier la source active avant la publication.
- **Un agent de plugin déclare des permissions dans le frontmatter.** Ces champs sont ignorés pour les agents fournis par un plugin. **Correctif :** déplacer les contrôles requis vers une portée de paramètres prise en charge et les vérifier à cet endroit.
- **Un agent peut lire un secret mais on lui demande de ne pas le révéler.** Les seules instructions textuelles ne constituent pas une frontière de capacité. **Correctif :** ne pas fournir d'accès inutile aux secrets.
- **Une sortie de revue indique PASS sans preuve.** Une conclusion n'est pas un reçu de publication. **Correctif :** exiger les résultats de commandes, les références aux sources ou les artefacts observés.
- **Une mise à jour de l'organisation modifie le comportement silencieusement.** La reproduction devient difficile. **Correctif :** consigner l'identité de la configuration gérée dans le reçu de la tâche.

## Sources {#sources}

- [Subagents Claude Code](https://code.claude.com/docs/en/subagents)
- [Paramètres Claude Code et configuration des subagents](https://code.claude.com/docs/en/configuration)
- [Référence des plugins Claude Code](https://code.claude.com/docs/en/plugins-reference)
- [Vue d'ensemble des extensions Claude Code](https://code.claude.com/docs/en/features-overview)

## Voir aussi {#see-also}

- [[claude-code-harness-patterns]]
- [[agent-orchestration]]
- [[agentic-security-2026]]
- [[multi-session-coordination]]
