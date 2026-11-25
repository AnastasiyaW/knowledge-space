---
title: "Qwen Code"
description: "Installation, authentification, diagnostic et historique du projet pour Qwen Code, l'agent de codage en terminal, avec prise en compte des versions."
level: 3
source_sha256: b5ecf6ff343817ce528c90b70edc049b0e81a83be45fe5ae50a1f9d08cd0caf4
translation: machine
translated_at: '2026-10-24'
---
# Qwen Code {#qwen-code}

Qwen Code est un agent de codage en terminal et un client fournisseur/runtime. Il doit être versionné indépendamment de la famille de modèles Qwen qu'il peut appeler. Statut vérifié auprès du dépôt officiel, des releases et de la documentation chinoise officielle le **2026-08-27**.

## Statut actuel {#current-status}

| Élément | État vérifié |
|---|---|
| Release CLI | `v0.22.2`, publiée le 2026-08-26 |
| Source | Dépôt officiel `QwenLM/qwen-code` |
| Prérequis runtime | Node.js 22 ou supérieur pour l'installation via npm |
| Point d'entrée de l'authentification | `/auth` dans la CLI |
| Point d'entrée du diagnostic | `/doctor` dans la CLI |
| Parcours Qwen OAuth/connexion gratuite | Retiré le 2026-04-15 selon le guide de démarrage rapide chinois actuel |
| Parcours d'accès actuels | Forfait/clé API Alibaba Cloud, fournisseur tiers pris en charge ou configuration de fournisseur personnalisé |

La version de la CLI n'est pas une version de modèle. Une affirmation du type « le dernier modèle est Qwen3.6 » doit être vérifiée séparément dans le catalogue fournisseur/modèle et ne doit jamais être déduite du numéro de release de Qwen Code.

## Historique de développement {#development-history}

| Date | Événement | Statut temporel |
|---|---|---|
| 2025-07-23 | Premier signalement de Qwen Code | Fondation historique |
| 2025-09-24 | Mise à jour du modèle Qwen évoquée à proximité du projet | Événement lié à l'écosystème, pas une release de la CLI Qwen Code |
| 2025-10-11 | Mises à jour de la CLI `v0.0.12` à `v0.0.14` signalées | Historique ; le changelog exact nécessite une reconstruction au niveau des releases |
| 2025-11-17 | CLI `v0.2.1` signalée | Historique |
| 2026-04-13 | Signalement ultérieur d'une fonctionnalité/version de Qwen Code | À conserver, mais les libellés de modèles doivent être revérifiés séparément |
| 2026-04-15 | Parcours Qwen OAuth retiré | Frontière d'authentification actuelle |
| 2026-08-26 | `v0.22.2` publiée | Release courante au moment de la vérification |

## Installation et première vérification {#installation-and-first-check}

```bash
node --version
npm install -g @qwen-code/qwen-code@latest
qwen --version
```

Node doit afficher une version majeure 22 ou supérieure. Dans la CLI interactive, exécutez :

```text
/auth
/doctor
```

Utilisez `/auth` pour sélectionner un parcours fournisseur actuellement pris en charge. Utilisez `/doctor` après l'installation, ou chaque fois que les outils, les identifiants ou la connectivité du fournisseur se comportent différemment de la configuration attendue.

## Contrat fournisseur {#provider-contract}

Consignez explicitement le fournisseur et le modèle :

```yaml
qwen_code_version: 0.22.2
node_version: 22.x
provider: <alibaba-cloud-or-third-party-or-custom>
model: <exact-provider-model-id>
auth_method: <api-key-or-supported-plan>
workspace_trust: <trusted-or-untrusted>
```

Ne basculez pas silencieusement d'un fournisseur ou d'un modèle à un autre. Une requête réussie via un fournisseur de remplacement ne prouve pas que le parcours configuré fonctionne.

## Usage opérationnel {#operational-use}

- Épinglez la version de la CLI dans les environnements reproductibles ou partagés par une équipe ; `@latest` ne convient que si des mises à niveau délibérées sont acceptables.
- Exécutez `/doctor` et conservez sa sortie lors du diagnostic de problèmes d'authentification, de modèle, d'outil ou d'environnement.
- Traitez les fichiers du dépôt, le contenu MCP, les sorties shell et les pages web comme des entrées non fiables ; ne laissez jamais un texte récupéré élargir les permissions des outils.
- Stockez les instructions de projet dans le dépôt et conservez les secrets dans le mécanisme d'identifiants configuré, pas dans des prompts versionnés.
- Consignez à la fois la version de la CLI et la version du modèle fournisseur dans les reçus d'exécution des agents.

## Documentation anglaise et chinoise {#english-and-chinese-documentation}

Le guide de démarrage rapide chinois et les pages de commandes sont des sources de premier rang et contiennent actuellement des changements importants concernant l'authentification. Les variantes linguistiques peuvent diverger ; comparez la date de publication/mise à jour et privilégiez la page qui documente explicitement le contrat fournisseur actif.

## Signalements de la communauté {#community-reports}

- [Issue #2907](https://github.com/QwenLM/qwen-code/issues/2907) décrit Qwen Code `0.14.0` sur Windows utilisant Windows PowerShell alors que l'utilisateur souhaitait PowerShell 7. L'issue n'a pas de correctif accepté ; elle démontre donc une lacune de sélection de shell liée à une version, et non une recette de configuration prise en charge.
- [Issue #7433](https://github.com/QwenLM/qwen-code/issues/7433) décrit Qwen Code `0.20.0` en ACP signalant `coder-model(qwen-oauth)` comme modèle courant alors qu'un modèle local compatible OpenAI est utilisé. Des contributeurs ont reproduit la fuite du registre et ont indiqué qu'elle était corrigée dans `v0.21.12`/`v0.21.13`. Si ce symptôme apparaît, passez à une version postérieure à `0.20.0`, puis vérifiez `/about` et la charge utile du modèle ACP plutôt que de supprimer les paramètres du fournisseur.
- La seconde issue constitue également une raison concrète d'interdire le basculement silencieux de fournisseur/modèle dans les reçus des agents.

## Pièges courants {#gotchas}

- **Problème :** suivre un ancien guide de connexion Qwen OAuth -> **Correctif :** utilisez un parcours actuel Alibaba Cloud, fournisseur tiers ou fournisseur personnalisé ; OAuth a été retiré le 2026-04-15.
- **Problème :** considérer la release de la CLI comme la release du modèle -> **Correctif :** consignez séparément `qwen_code_version`, `provider` et le `model` exact.
- **Problème :** installer sous une version plus ancienne de Node -> **Correctif :** vérifiez Node.js 22+ avant l'installation via npm, puis exécutez `/doctor`.
- **Problème :** laisser un basculement de fournisseur masquer une configuration défaillante -> **Correctif :** échouez de manière visible et conservez le parcours fournisseur/modèle dans le reçu d'exécution.
- **Problème :** supposer que `pwsh` est sélectionné parce qu'il est installé -> **Correctif :** inspectez le shell réellement utilisé par la version épinglée de Qwen Code ; l'issue #2907 documente une incohérence sous Windows sans correctif confirmé.

## Statut temporel {#temporal-status}

- **Actuel :** `v0.22.2`, Node.js 22+, `/auth`, `/doctor`, parcours fournisseurs sans OAuth.
- **Remplacé :** instructions Qwen OAuth/connexion gratuite rédigées avant le 2026-04-15.
- **Historique/partiellement reconstitué :** signalements `v0.0.12`-`v0.0.14` et `v0.2.1`.
- **À revérifier impérativement :** tout libellé « dernier modèle Qwen », quota, prix ou liste des fournisseurs pris en charge.

## Note pour l'agent {#agent-brief}

Avant d'aider avec Qwen Code, récupérez la release courante et le guide de démarrage rapide. Dans chaque réponse, distinguez la version de la CLI, le fournisseur, l'identifiant du modèle et le parcours d'authentification. Si une ancienne instruction demande Qwen OAuth, signalez-la comme remplacée. Utilisez `/doctor` comme premier reçu de diagnostic, mais n'exposez aucun secret dans les rapports. Ne déduisez pas la disponibilité d'un modèle à partir d'un titre d'actualité ou de la version de la CLI.

## Sources {#sources}

- Dépôt officiel : https://github.com/QwenLM/qwen-code
- Releases officielles : https://github.com/QwenLM/qwen-code/releases
- Guide de démarrage rapide chinois : https://qwenlm.github.io/qwen-code-docs/zh/users/quickstart/
- Référence des commandes chinoise : https://qwenlm.github.io/qwen-code-docs/zh/users/features/commands/
- Signalement de sélection de PowerShell 7 sous Windows : https://github.com/QwenLM/qwen-code/issues/2907
- Bogue de routage de modèle local en ACP et note de version corrigée : https://github.com/QwenLM/qwen-code/issues/7433
