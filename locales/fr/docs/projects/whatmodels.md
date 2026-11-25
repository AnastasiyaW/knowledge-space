---
title: "WhatModels — Site public"
category: projects
date: 2026-05-15
tags: [project, public-website, whatmodels]
aliases: ["WhatModels"]
level: 2
source_sha256: 85187382ea7faecedce3c6be6ff706959f25d4844fe4396c72eb9d591f6959f5
translation: machine
translated_at: '2026-10-24'
---
# WhatModels — Site public {#whatmodels-public-website}

**Ligne de développement :** `project:whatmodels` · fil `public-website`  
**Dernier événement :** 2026-05-15 · 1 événement daté depuis le 2026-05-15 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

WhatModels est un sélecteur de modèles destiné aux utilisateurs d'Ollama, de llama.cpp et d'autres runtimes locaux, permettant de choisir des modèles selon le GPU ou une VRAM saisie manuellement, en estimant le contexte maximal et la vitesse de génération.

- Catalogue de GPU pour choisir des configurations matérielles prédéfinies.
- Saisie manuelle de la VRAM pour spécifier des limites de mémoire personnalisées.
- Filtres de contexte minimal pour écarter les configurations insuffisantes.
- Comparaison des quantifications pour évaluer la taille par rapport à la mémoire.
- Catégories d'adéquation pour regrouper les modèles en « fonctionne bien », « ajustement serré » et « ne tient pas ».

La vitesse de génération n'apparaît que pour les GPU du catalogue et reste une estimation, et non un benchmark d'exécution.

L'outil convient à la sélection initiale d'un modèle et du matériel, mais l'inférence en production nécessite une vérification sur le matériel local.

## Ligne de développement {#development-line}

- **2026-05-15 — Site public de WhatModels documenté.** Le 2026-05-15, un message du fil WhatModels renvoyait vers le site public du projet. Cela établit une référence publique datée pour WhatModels, mais les éléments disponibles n'identifient ni lancement, ni version publiée, ni modification de fonctionnalité.

## Ce qui a changé {#what-changed}

2026-05-15 — WhatModels fonctionnait comme un calculateur de compatibilité web pour les LLM locaux. L'exemple publié configurait deux cartes RTX 5060 Ti 16 Go, un contexte de 16K, un minimum de 10 tokens/s et 64 Go de RAM.

Après le 2026-05-15 — Nous n'avons trouvé aucune version datée confirmée au-delà de l'événement initial. La documentation actuelle du dépôt décrit un calcul statique dans le navigateur, sans backend ni API : la VRAM combine les poids du modèle et le KV-cache, et la vitesse de génération dérive de la bande passante mémoire et de la taille des poids.

## Comment l'utiliser {#how-to-use-this}

Au 2026-05-15, les praticiens peuvent utiliser le site public documenté de WhatModels comme point de découverte du projet ; ses capacités spécifiques et son statut de publication nécessitent encore une vérification séparée.

1. Ouvrez le calculateur et choisissez un GPU dans la liste ou saisissez la VRAM disponible manuellement.
  — <https://whatmodelscanirun.com/>
2. Définissez le contexte minimal acceptable ; lorsque vous sélectionnez un GPU dans la liste, comparez les tokens par seconde estimés.
  — <https://github.com/BenD10/whatmodels>
3. Commencez par les résultats « Runs well » ; vérifiez localement les options « Tight fit » avec le contexte et la quantification requis.
  — <https://github.com/BenD10/whatmodels>

## Bonnes pratiques {#best-practices}

- Incluez le KV-cache en plus des poids : un modèle qui tient selon la taille du fichier GGUF peut manquer de mémoire au contexte visé.
  — <https://github.com/BenD10/whatmodels>
- Considérez les estimations de vitesse comme préliminaires : la vitesse de génération dépend de la bande passante mémoire, de la quantification, du contexte et de la surcharge du moteur d'exécution.
  — <https://github.com/BenD10/whatmodels>
- Comparez les configurations sur le même modèle et la même quantification, au même contexte requis, puis confirmez le résultat dans le runtime cible.
  — <https://habr.com/ru/articles/1035862/>

## Remplacé par {#superseded-by-this}

- 2026-05-16 — Choisir un LLM local uniquement selon le nombre de paramètres ou la taille du fichier est obsolète pour les tâches à long contexte : le calcul doit inclure le KV-cache et la quantification.

## Inconnues {#still-unknown}

- Il n'existe pas de journal des modifications daté et primaire pour WhatModels pour le 2026-05-15 ou les changements ultérieurs ; le dépôt GitHub montre le code actuel mais ne fournit aucune étape de version datée dans les éléments disponibles.
- Le schéma initial a enregistré l'événement du 2026-05-15 sans champs de constat dédiés ; en dehors de cet événement, aucune étape de développement datée ultérieure n'est confirmée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://whatmodelscanirun.com/ | What Models? — Pick the right model for your GPU in seconds | 2026-09-05 |
| https://github.com/BenD10/whatmodels | BenD10/whatmodels — Figure out what models you can run locally | 2026-09-05 |
| https://www.forum.mista.ru/topic/901896 | Confaster — ИИ-агент для 1С Конфигуратора с MCP сервером | 2026-09-05 |
| https://habr.com/ru/articles/1035862/ | Калькулятор VRAM для локальных LLM: Какие модели ИИ запустятся у вас на компьютере? | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:whatmodels`, fil `public-website`, 1 événement daté du 2026-05-15 au 2026-05-15.
- **Note pratique :** Au 2026-05-15, les praticiens peuvent utiliser le site public documenté de WhatModels comme point de découverte du projet ; ses capacités spécifiques et son statut de publication nécessitent encore une vérification séparée.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
