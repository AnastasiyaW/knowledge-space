---
title: "Inférence à faible VRAM : contrat d'exécution mesuré"
description: "L'inférence à faible VRAM est une configuration d'exécution mesurée, et non une promesse liée à une gamme de matériel ; figez le modèle et le backend, ne sélectionnez que des chemins de quantification, de déchargement ou de tuilage documentés, et consignez la mémoire de pointe, la latence, la fidélité des sorties et le comportement en cas d'échec sur le périphérique réel."
category: techniques
tags: [memory, offloading, quantization, tiling, onnx, inference, evaluation]
aliases: ["Memory-Efficient Inference", "GPU Memory Optimization"]
level: 3
source_sha256: a86ffae0861b9b672ec6963a86470333863d217d76e6d1443263cbe7a56d1cfc
translation: machine
translated_at: '2026-10-24'
---
# Inférence à faible VRAM : contrat d'exécution mesuré {#low-vram-inference-measured-runtime-contract}

Le support de la faible VRAM ne se résume pas à un tableau de noms de GPU ni à un chiffre de mémoire annoncé.
Il s'agit d'une configuration d'exécution versionnée, qui doit s'adapter au modèle réel, à la résolution, au lot, au périphérique, au pilote, au backend et à la charge de travail concurrente, tout en préservant le contrat de sortie visé.

## Établir une référence {#establish-a-baseline}

Mesurez d'abord le chemin non optimisé pris en charge sur le périphérique cible. Consignez :

- l'empreinte (digest) du modèle ou du point de contrôle, les versions du runtime, du backend et du fournisseur, le périphérique et le pilote, le type de données, la forme d'entrée, le lot et la concurrence ;
- la mémoire périphérique allouée et réservée au pic, la mémoire hôte, le temps d'exécution, le comportement de la première exécution, ainsi que la sortie des nouvelles tentatives et des échecs ;
- les empreintes des sorties ou un résultat de fidélité ou de relecture propre à la tâche ; et
- le budget de mémoire périphérique qui reste disponible pour les activations, le décodage, l'interface et les autres processus.

N'estimez pas un budget mémoire utilisable à partir de la VRAM nominale. La mémoire d'activation et l'espace de travail du runtime peuvent dépasser la taille des poids du modèle, et un périphérique qui démarre une tâche peut néanmoins échouer en cours de route.

## Choisir des stratégies documentées {#choose-documented-strategies}

La [documentation Diffusers sur la mémoire](https://huggingface.co/docs/diffusers/optimization/memory) décrit le placement sur périphérique ainsi que le déchargement CPU de modèle, séquentiel et par groupes.
Ces opérations présentent des compromis mémoire/latence différents et peuvent installer des hooks à état. Leur compatibilité dépend du pipeline et de la version.

| Stratégie | Valable uniquement si | Mesure requise |
|---|---|---|
| Quantification | le point de contrôle ou le runtime nommé prend en charge ce format exact | fidélité des sorties, mémoire de pointe, échecs de chargement et débit |
| Déchargement du modèle ou séquentiel | le pipeline documente le chemin de déchargement et l'ordre des appels | mémoire périphérique et hôte au pic, latence lors d'appels répétés |
| Placement par groupes ou par périphérique | le modèle et le runtime prennent en charge le mappage sélectionné | ordre des composants, réinitialisations et comportement en cas de manque de mémoire |
| Tuilage spatial ou latent | le chemin d'encodage/décodage ou d'inférence du modèle le prend en charge | raccords, comportement de remplissage et de recadrage, préservation des détails protégés |
| Liaison d'E/S ONNX (I/O binding) | les tenseurs sont placés sur le périphérique cible du fournisseur d'exécution | compatibilité du fournisseur, comportement des copies de données et gestion des formes dynamiques |

La [liaison d'E/S d'ONNX Runtime](https://onnxruntime.ai/docs/performance/tune-performance/iobinding.html)
peut éviter des transferts inutiles lorsque les tenseurs résident déjà sur le périphérique cible. Ce n'est pas une accélération générique : le fournisseur, la propriété des tenseurs, les formes et la durée de vie de la mémoire doivent être validés ensemble.

## Politique en cas d'échec {#failure-policy}

Sélectionnez un chemin explicite et pris en charge par profil de périphérique mesuré. Si la référence ne tient pas en mémoire, choisissez une alternative documentée et mesurez à nouveau. Si aucune configuration prise en charge ne convient, renvoyez un état visible de capacité ou d'erreur, ou un chemin CPU ou distant explicitement approuvé ; ne remplacez jamais silencieusement le modèle, la précision, le fournisseur ou la qualité de sortie.

Le comportement des caches et des moteurs compilés relève également du contrat. Liez les caches aux hypothèses de modèle, de runtime, de périphérique et de pilote dont ils dépendent, et mesurez séparément les exécutions à froid et à chaud.

## Critères d'acceptation {#acceptance}

Une configuration à faible mémoire ne peut être livrée que si elle :

1. reste dans le budget mémoire mesuré sur des exécutions répétées ;
2. renvoie la sortie attendue, sans artefacts de tuilage ou de quantification non relus ;
3. signale un échec exploitable lorsque les entrées dépassent sa forme ou son enveloppe mémoire validées ; et
4. consigne la configuration utilisée pour chaque résultat.

Cela transforme une optimisation mémoire en capacité produit observable, plutôt qu'en promesse matérielle impossible à tester.

## Pages connexes {#related-pages}

- [[tiled-inference]]
- [[diffusion-inference-acceleration]]
- [[upscaler-evaluation]]
