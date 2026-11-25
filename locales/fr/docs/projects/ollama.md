---
title: "Ollama — Développement produit"
category: projects
date: 2026-01-22
tags: [ollama, product-development, project]
aliases: ["Ollama"]
level: 2
source_sha256: ea28751ddad14f28a58e16889bae3832622d517d7d31f7a3650ec259df555845
translation: machine
translated_at: '2026-10-24'
---
# Ollama — Développement produit {#ollama-product-development}

**Ligne de développement :** `project:ollama` · fil `product-development`  
**Dernier événement :** 2026-01-22 · 2 événements datés depuis 2025-05-19 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Ollama est un environnement d'exécution local destiné aux développeurs qui font tourner des modèles de langage, de vision et d'embedding sur leur propre matériel ou via une API compatible.

- Exécuteur de modèles : télécharge les modèles et fournit une CLI interactive, une API HTTP et des bibliothèques Python et JavaScript.
- Processeur de vision : traite les images en complément des prompts textuels.

La vitesse, la taille du contexte et la concurrence dépendent de la RAM et de la VRAM disponibles.

Une alternative pratique à l'inférence dans le cloud pour le développement local et la maîtrise du lieu de stockage des données.

## Ligne de développement {#development-line}

- **2025-05-19 — Ollama a publié une mise à jour sur les modèles multimodaux.** Le 2025-05-19, Ollama a renvoyé vers sa page de blog officielle consacrée aux modèles multimodaux et vers sa page de téléchargement, sans détails sur des modèles spécifiques ni sur la configuration matérielle requise.
- **2026-01-22 — Ollama a partagé une mise à jour de version logicielle.** Le 2026-01-22, Ollama a orienté les utilisateurs vers la page des releases GitHub sans préciser la version ni la liste des modifications.

## Changements {#what-changed}

- 2025-05-19 — Ollama a déplacé les modèles de vision vers un nouveau moteur multimodal et ajouté la prise en charge de Llama 4, Gemma 3, Qwen 2.5 VL et Mistral Small 3.1.
- 2026-01-22 — Un lien vers GitHub Releases confirme le canal de publication, mais l'URL ne comporte aucune étiquette de version ; le contenu de la release ne peut donc pas être reconstitué de manière fiable.

## Mode d'emploi {#how-to-use-this}

À la date du 2025-05-19, évaluez le workflow multimodal officiel lorsque vous choisissez des modèles locaux. À la date du 2026-01-22, consultez les notes de version GitHub du projet avant toute mise à niveau.

1. Installez Ollama sur macOS, Windows ou Linux.
  — <https://docs.ollama.com/quickstart>
2. Lancez un modèle dans le terminal, par exemple `ollama run gemma4`, pour tester la première session.
  — <https://docs.ollama.com/quickstart>
3. Envoyez les requêtes depuis vos applications vers l'API locale à l'adresse `http://localhost:11434/api`, ou utilisez les bibliothèques officielles Python et JavaScript.
  — <https://docs.ollama.com/api/introduction>
4. Joignez une image au texte dans la CLI ou dans le champ `images` de la requête API pour les tâches de vision.
  — <https://docs.ollama.com/capabilities/vision>

## Bonnes pratiques {#best-practices}

- Vérifiez le placement des modèles avec `ollama ps` pour savoir s'ils tournent sur GPU, sur CPU ou en mode mixte.
  — <https://docs.ollama.com/faq>
- Ajustez `OLLAMA_CONTEXT_LENGTH` et la concurrence à la mémoire disponible : la consommation augmente avec le nombre de requêtes parallèles multiplié par la taille du contexte.
  — <https://docs.ollama.com/faq>
- Conservez le service sur l'interface de boucle locale (loopback) par défaut ; modifiez `OLLAMA_HOST` en connaissance de cause et utilisez un reverse proxy si vous l'exposez.
  — <https://docs.ollama.com/faq>
- Désactivez les fonctionnalités cloud avec `OLLAMA_NO_CLOUD=1` ou `disable_ollama_cloud` pour une configuration entièrement locale.
  — <https://docs.ollama.com/faq>

## Remplacé par ce qui suit {#superseded-by-this}

- 2025-05-15 — L'ancienne intégration, reposant sur du code multimodal partagé dans llama.cpp, a été remplacée par des implémentations de modèles isolées dans le nouveau moteur.
- 2026-01-20 — La génération d'images, limitée à macOS, a été marquée comme expérimentale ; Windows et Linux n'étaient pas encore pris en charge.

## Points encore inconnus {#still-unknown}

- Le lien GitHub Releases de l'événement du 2026-01-22 pointe vers un flux de releases modifiable, sans étiquette ; nous ne pouvons donc pas rattacher une version ou un changelog précis à cette date.
- La documentation actuelle inclut des modèles cloud, mais les 2 liens datés ne permettent pas de savoir si l'exécution dans le cloud faisait partie de l'annonce initiale.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ollama.com/blog/multimodal-models | Le nouveau moteur d'Ollama pour les modèles multimodaux | 2026-09-05 |
| https://ollama.com/download | Télécharger Ollama | 2026-09-05 |
| https://github.com/ollama/ollama/releases | Releases · ollama/ollama | 2026-09-05 |
| https://github.com/ollama/ollama/releases/tag/v0.14.3 | Release v0.14.3 · ollama/ollama | 2026-09-05 |
| https://ollama.com/blog/image-generation | Génération d'images (expérimental) | 2026-09-05 |
| https://docs.ollama.com/quickstart | Démarrage rapide | 2026-09-05 |
| https://docs.ollama.com/api/introduction | Introduction - API Ollama | 2026-09-05 |
| https://docs.ollama.com/capabilities/vision | Vision | 2026-09-05 |
| https://docs.ollama.com/faq | FAQ | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:ollama`, fil `product-development`, 2 événements datés du 2025-05-19 au 2026-01-22.
- **Note pratique :** À la date du 2025-05-19, évaluez le workflow multimodal officiel d'Ollama lors du choix de modèles locaux ; à la date du 2026-01-22, examinez les notes de version GitHub du projet avant toute mise à niveau.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
