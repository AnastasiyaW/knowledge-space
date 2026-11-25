---
title: "Qwen-MM-Plugins — Développement"
category: projects
date: 2026-08-10
tags: [development, project, qwen, qwen-mm-plugins]
aliases: ["Qwen-MM-Plugins"]
level: 3
source_sha256: 545fc7adbc4f2498695184293619f99bd37edd7d6eb1ca84a783fa94300a8366
translation: machine
translated_at: '2026-10-24'
---
# Qwen-MM-Plugins — Développement {#qwen-mm-plugins-development}

**Ligne de développement :** `project:qwen-mm-plugins` · fil `development`  
**Dernier événement :** 2026-08-10 · 1 événement daté depuis le 2026-08-10 · **Recherche effectuée le :** 2026-09-08 · niveau de confiance : moyen

## Présentation {#what-it-is}

Qwen-MM-Plugins regroupe des Skills spécialisés par capacité et des serveurs MCP optionnels pour les harness d'agents. Il connecte un agent existant à des tâches de vision, d'audio, de documents, de recherche et de 3D/CAO.

- `core` : lecture et visualisation locales d'images, de vidéos, de documents, de données, de fichiers 3D et de NIfTI.
- `api` et `search` : tâches de vision, d'OCR, de grounding, d'audio, de recherche web et de recherche d'image inversée via modèles et API.
- `video-memory`, `video-edit`, `blender`, `freecad`, `edu-agent` et `omni-memory` : flux de travail pour vidéos longues, montage médias, pilotage d'applications, enseignement et mémoire audiovisuelle.

`core` ne nécessite aucune clé API en mode image native par défaut. Les chemins cloud, recherche, légendage texte seul et mémoire exigent des identifiants ou des dépendances système. Windows natif n'est pas validé. Commencez par `core` sur un harness multimodal. N'ajoutez des capacités que lorsque les exigences de transfert de données et d'exécution le justifient.

## Ligne de développement {#development-line}

- **2026-08-10 — Dépôt Qwen-MM-Plugins référencé.** Le 2026-08-10, le fil Qwen a référencé le dépôt GitHub Qwen-MM-Plugins. La source ne fournit que la date et le lien du dépôt, sans affirmer de version, de fonctionnalité ou de changement de modèle.

## Modifications {#what-changed}

- 2026-08-10 — Qwen-MM-Plugins a été mentionné dans une source datée ; le dépôt de première partie accessible n'établit pas de date de lancement, de création ni de premier commit.
- 2026-08-11 — Un mode audio Base64 brut, activé sur option, pour les endpoints compatibles OpenAI a été fusionné, tandis que la valeur par défaut DashScope est restée inchangée.
- 2026-08-18 — `video-memory` v1.0.2 a normalisé les URI de fichiers locaux pour l'ensemble des capacités, dans le cadre de corrections de chemins multiplateformes.
- 2026-08-20 — Les mises à jour de capacités étiquetées ont ajouté un repli texte pour les résultats d'images MCP.
- 2026-08-24 — `core` v1.0.5 a ajouté la visualisation de volumes NIfTI et la sélection de volumes 4D.
- 2026-09-03 — `omni-memory` v1.0.0 a ajouté une mémoire audiovisuelle pour les travaux sur vidéos longues.

## Mode d'emploi {#how-to-use-this}

1. Choisissez une capacité pour la tâche, puis utilisez l'installateur guidé pour le harness cible. Sous Windows, utilisez Ubuntu WSL2 et conservez le checkout dans le répertoire personnel Linux.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
2. Configurez uniquement les identifiants et les outils système requis. Exécutez l'action Verify de l'installateur ou testez l'entrée MCP avec `--check-system`.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
3. Référencez un fichier dans le harness et formulez la tâche en langage courant. Le Skill installé sélectionne l'outil MCP pertinent.
  — <https://github.com/QwenLM/Qwen-MM-Plugins>
4. Sur un hôte texte seul, définissez `QWEN_MM_NATIVE_MODE=0` uniquement après avoir configuré un endpoint VL et approuvé les envois d'images.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
5. Pour un flux vidéo `omni-memory`, interrogez d'abord `get_memory_status`. Ne construisez ou ne reprenez la mémoire que si la durée des clips et leur statut le justifient.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md>

## Bonnes pratiques {#best-practices}

- Épinglez les installations durables sur des tags immuables par capacité. Réservez `main` et le mode checkout local au développement.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
- Mettez à jour le Skill et l'enregistrement MCP d'une capacité ensemble, puis rechargez ou redémarrez le harness.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
- Conservez la sortie d'image native pour un hôte multimodal. Le repli texte seul envoie les images renvoyées et les captures d'écran à l'endpoint VL configuré.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
- Épinglez `QWEN_MM_SEARCH_BACKEND` lorsque la sélection du fournisseur doit rester reproductible. Le mode auto choisit le premier backend configuré.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
- Activez `QWEN_MM_AUDIO_RAW_B64` uniquement pour les endpoints Omni conformes à la spécification OpenAI qui exigent du Base64 brut. Laissez DashScope sur son format par défaut.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/pull/9>
- Après une construction omni-memory interrompue, vérifiez la couverture des clips avec `get_memory_status`. Reprenez la construction plutôt que de faire confiance à une mémoire partielle.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-11 — Supposer que tout endpoint compatible OpenAI accepte l'audio en data URL DashScope. Le chemin Base64 brut activé sur option couvre des endpoints comme vLLM, tandis que DashScope conserve la valeur par défaut.
- 2026-08-18 — URI de fichiers locaux non normalisés entre capacités. `video-memory` v1.0.2 a normalisé les URI et corrigé les chemins multiplateformes.
- 2026-08-20 — Blocs d'images MCP natifs comme seul format documenté pour les hôtes texte seul. Les mises à jour ont ajouté un repli texte.
- 2026-08-24 — `core` sans visualisation NIfTI ni sélection de volumes 4D. `core` v1.0.5 a ajouté les deux.

## Points inconnus {#still-unknown}

- La publication officielle de Qwen du 10 août a renvoyé une erreur HTTP 403 pendant la recherche. Les détails de l'événement reposent sur des archives secondaires plutôt que sur un justificatif du dépôt de première partie.
- Les pages du dépôt GitHub et des Releases n'établissent ni date de création, ni premier commit, ni Release GitHub au 2026-08-10.
- La ligne de développement plus large de Qwen comprend des projets distincts. Nous n'avons trouvé aucun lien technique, de compatibilité ou de propriété avec Qwen-MM-Plugins.
- Nous n'avons trouvé aucune matrice de compatibilité primaire couvrant les fournisseurs compatibles OpenAI. Testez l'endpoint et la capacité retenus avant de vous y fier.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/QwenLM/Qwen-MM-Plugins | README du dépôt QwenLM/Qwen-MM-Plugins | 2026-09-08 |
| https://easyvibecoding.app/curated/2887-alibaba-qwen-shares-qwen-mm-plugins-native-multimodal-agent | Archive EasyVibeCoding de la publication Qwen sur Qwen-MM-Plugins | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/pull/9 | PR #9 : audio d'entrée Base64 brut, activé sur option, pour serveurs conformes à OpenAI | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/tags | Tags des capacités Qwen-MM-Plugins | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md | Guide d'installation de Qwen-MM-Plugins | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md | Référence de configuration de Qwen-MM-Plugins | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md | Cookbook d'utilisation omni-memory de Qwen-MM-Plugins | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/releases | Page GitHub Releases de Qwen-MM-Plugins | 2026-09-08 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:qwen-mm-plugins`, fil `development`, 1 événement daté, du 2026-08-10 au 2026-08-10.
- **Remarque pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
