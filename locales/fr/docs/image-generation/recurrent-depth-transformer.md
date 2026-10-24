---
title: "Transformer à profondeur récurrente : contrat de preuves à l'exécution"
description: "Les transformers à profondeur récurrente réutilisent un bloc partagé propre à chaque version à travers les itérations ; associez l'architecture publiée, le checkpoint et le runtime, le budget de récurrence, le comportement du cache et de la terminaison, ainsi que la qualité et le coût mesurés, et n'inférez pas le raisonnement latent, la sortie anticipée, la stabilité ou la déployabilité à partir du nom de la famille."
category: techniques
tags: [recurrent-depth, transformers, recurrence, inference, evaluation, runtime, evidence]
aliases: ["Recurrent-Depth Transformer", "RDT Architecture", "Looped Transformer"]
level: 3
source_sha256: 40d8d9b1eb3e810e0c17f3dd0689061488ab91cc98471908fad6261f853fe260
translation: machine
translated_at: '2026-10-24'
---
# Transformer à profondeur récurrente : contrat de preuves à l'exécution {#recurrent-depth-transformer-runtime-evidence-contract}

Le « transformer à profondeur récurrente » est un nom de famille, et non un checkpoint normalisé ni une interface de service. L'idée qui le définit est la réutilisation d'un calcul partagé à travers plusieurs itérations, mais la disposition des blocs, l'injection d'entrée, le mécanisme de portes, la structure du cache, la condition d'arrêt, la procédure d'entraînement et les profondeurs de récurrence supportées dépendent d'une implémentation précise.

## Définir l'architecture avant d'en parler {#bind-the-architecture-before-discussing-it}

Une disposition publiée peut être résumée ainsi :

`input → prelude → cœur récurrent partagé répété r fois → coda → logits`

[Scaling up Test-Time Compute with Latent Reasoning](https://arxiv.org/abs/2502.05171)
décrit une conception prelude / cœur partagé / coda. Un article plus récent,
[Gated Recurrent Transformers](https://arxiv.org/abs/2608.15062), présente une autre conception récurrente à portes. Aucune de ces sources ne démontre que chaque modèle « RDT » possède la même règle de mise à jour, les mêmes adaptateurs, les mêmes couches de mélange d'experts, le même mécanisme d'attention, la même contrainte de stabilité ou le même comportement de sortie anticipée.

Pour une version concrète, conservez :

- la référence de l'article ou du code publié, le condensé (digest) du checkpoint, la licence, le tokenizer, la précision, le runtime ou backend, et tout correctif non par défaut ;
- la composition exacte prelude / cœur / coda, l'indication de partage ou non des poids du cœur, la politique d'injection d'entrée et de portes, ainsi que les valeurs de récurrence supportées ;
- le format du cache, la politique de regroupement par lots, le déterminisme, l'implémentation de la terminaison ou de la sortie anticipée, le comportement en cas d'erreur, et la source du budget de récurrence retenu ;
- le corpus et le découpage d'évaluation, la politique de prompt et de gabarit, les métriques de qualité, les tests de sécurité et la référence de comparaison ; et
- la latence, la mémoire, le débit et les variations de sortie mesurés à chaque réglage de récurrence publié, sur le matériel déployé.

## Traiter la récurrence comme une commande mesurée {#treat-recurrence-as-a-measured-control}

Davantage d'itérations ajoutent du calcul sans améliorer systématiquement toutes les tâches. Modifier `r` peut affecter la qualité, la latence, la pression mémoire, le regroupement des lots et la répartition des échecs. Un déploiement ne devrait exposer que les valeurs de profondeur pour lesquelles il a été entraîné et testé. N'extrapolez pas un nombre de boucles arbitraire à partir d'un schéma d'article, et ne supposez pas qu'un cœur partagé reste stable au-delà de la plage d'exécution documentée.

Comparez les réglages de récurrence sur un ensemble d'évaluation disjoint par source, et consignez la courbe complète qualité / coût. Signalez les échecs, et pas seulement le meilleur point. Si une sortie anticipée est revendiquée, évaluez sa décision de sortie et les sorties finales par rapport à la référence à profondeur complète pour la version nommée ; ne l'inférez pas du partage de poids récurrent.

## Ne pas surestimer le calcul latent {#do-not-overstate-latent-computation}

Les mises à jour répétées de l'état caché ne constituent ni une chaîne de pensée visible, ni une explication, ni une preuve de raisonnement, ni une interface d'inspection. Ne prétendez pas que les étapes latentes équivalent à un nombre d'étapes de raisonnement écrites, qu'elles sont interprétables, ni qu'un calcul caché rend le modèle sûr. Évaluez directement les sorties et les contrôles déclarés.

## Frontière de déploiement {#serving-boundary}

Ne déployez un modèle à profondeur récurrente qu'après avoir vérifié que le runtime réel peut charger l'artefact nommé, préserver le comportement de récurrence et de cache demandé, et produire les sorties mesurées sous charge de travail. Un serveur transformer générique, un checkpoint quantifié ou un chargeur d'adaptateurs ne doivent pas être considérés comme compatibles par défaut. Signalez une erreur si le budget de récurrence, la politique de cache ou l'identité de l'artefact ne peuvent pas être vérifiés ; ne lancez jamais silencieusement un substitut dense ni une profondeur non spécifiée.

## Pages connexes {#related-pages}

- [[low-vram-inference-strategies]]
- [[tiled-inference]]
- [[diffusion-lora-training]]
