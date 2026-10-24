---
title: "Accélération de l'inférence de diffusion"
description: "L'accélération de la diffusion est un compromis propre à chaque modèle et à chaque runtime ; mesurez la latence à chaud et en régime permanent, la mémoire, la fidélité des sorties et la reproductibilité pour le checkpoint et le workflow exacts."
category: techniques
tags: [inference, acceleration, quantization, torch-compile, attention, scheduler, reproducibility]
aliases: ["Inference Speedup", "Diffusion Optimization"]
level: 3
source_sha256: 025a8fb34335f120c077d4e24e71d385b9e6c1619843cf6fb5885cbed48e0715
translation: machine
translated_at: '2026-10-24'
---
# Accélération de l'inférence de diffusion {#diffusion-inference-acceleration}

Il n'existe pas de « facteur d'accélération » portable pour l'inférence de
diffusion. Une technique peut améliorer le débit pour un checkpoint, une
résolution, une cible matérielle et un pipeline donnés, tout en ralentissant
un autre workflow, en le rendant moins stable ou en modifiant visuellement le
résultat. Traitez l'accélération comme une expérience contrôlée, et non comme
une liste de nœuds interchangeables.

## Établir un relevé de référence {#establish-a-baseline-receipt}

Avant de modifier le runtime, consignez :

- la révision exacte du modèle/checkpoint, la version du pipeline, le
  scheduler et les adaptateurs ;
- le prompt ou la fixture d'entrée, la graine, les dimensions, la taille de
  lot et le nombre d'étapes ;
- le GPU, le pilote, les versions CUDA/PyTorch/runtime et la précision ;
- le temps de démarrage à froid, la latence en régime permanent à chaud, le
  pic de mémoire du périphérique, ainsi que les fichiers de sortie ou leurs
  empreintes ; et
- un contrôle de fidélité propre à la tâche, incluant une relecture humaine
  lorsque la justesse visuelle est en jeu.

Présentez séparément le comportement à froid et à chaud. La compilation et la
mise en cache déplacent souvent du temps vers la première requête, ce qui peut
être inacceptable pour une édition interactive, même si les travaux répétés
deviennent plus rapides.

## Familles d'optimisation compatibles {#compatible-optimization-families}

N'utilisez qu'un mécanisme documenté pour le couple modèle/runtime exact, et
ajoutez une famille à la fois.

### Compilation {#compilation}

Le [guide d'accélération de Diffusers](https://huggingface.co/docs/diffusers/optimization/fp16)
documente torch.compile pour les composants de modèle gourmands en calcul.
La compilation peut être rentable pour des travaux répétés et à formes
stables, mais un changement de taille d'image ou de condition d'exécution peut
déclencher une recompilation. Diffusers documente également la compilation
régionale pour les blocs répétés ; sa disponibilité dépend de l'implémentation
du modèle.

### Précision et quantification {#precision-and-quantization}

La précision réduite ou les poids quantifiés peuvent modifier l'utilisation
mémoire, la latence, le comportement numérique et les détails de l'image.
Mesurez le résultat sur des entrées représentatives ; ne déduisez pas la
fidélité de l'étiquette de précision. Consignez le quantificateur, le
checkpoint de base, le chemin de calibration le cas échéant, ainsi que la
version du chargeur et du runtime.

### Attention et placement mémoire {#attention-and-memory-placement}

Les backends d'attention peuvent modifier la vitesse et le comportement mémoire
sur une pile matérielle donnée. Le déchargement CPU ou disque résout
principalement une contrainte de mémoire, et non un problème de latence
systématique : le
[guide mémoire](https://huggingface.co/docs/diffusers/optimization/memory)
indique que le déchargement CPU séquentiel peut être extrêmement lent.
Traitez le déchargement, le tuilage du VAE et le sharding comme des choix de
capacité, et évaluez-les indépendamment.

### Scheduler, nombre d'étapes et mise en cache {#scheduler-step-count-and-caching}

Changer de scheduler ou réduire le nombre d'étapes modifie la procédure
d'échantillonnage. Utilisez la voie prise en charge par l'éditeur du
checkpoint, puis évaluez la tâche demandée plutôt que de supposer qu'un
scheduler arbitraire est compatible. Les schémas de cache sont souvent
spécifiques à l'architecture et à l'implémentation ; vérifiez leur coût
mémoire, leur comportement d'invalidation et leur effet sur les sorties du
pipeline cible.

## Contrôler le flux aléatoire, et pas seulement l'étiquette de graine {#control-the-random-stream-not-just-the-seed-label}

Pour les comparaisons Diffusers sensibles à la reproductibilité, utilisez un
`torch.Generator(device="cpu")` sur CPU et initialisez-le explicitement. Un
générateur est mutable : réutiliser un objet déjà consommé fait avancer son
flux aléatoire. Recréez-le avec la même graine pour chaque comparaison
contrôlée, ou sauvegardez puis restaurez son état. Cela ne garantit pas des
images identiques entre versions, plateformes ou backends numériques.
[Guide de reproductibilité de Diffusers](https://huggingface.co/docs/diffusers/using-diffusers/reusing_seeds).

Rattachez le résultat au triplet modèle/runtime/matériel consigné. Lorsqu'un
benchmark modifie un backend d'attention, la précision, le scheduler ou le
nombre d'étapes, comparez la sortie autant que la vitesse ; une graine entière
identique n'isole pas ces changements. Utilisez les réglages de guidage pris
en charge par le checkpoint, et non une plage CFG universelle copiée depuis
une autre famille de modèles.

## Protocole de mesure {#measurement-protocol}

1. Exécutez une référence fixe après un préchauffage suffisant et conservez le
   relevé brut.
2. Modifiez une famille d'optimisation et répétez la même fixture.
3. Comparez la latence médiane et de queue, le pic de mémoire, la
   reproductibilité des sorties et la fidélité visuelle/liée à la tâche.
4. Ne conservez le changement que si le compromis mesuré satisfait la
   contrainte de déploiement ; sinon, revenez en arrière.
5. Recommencez après toute modification du checkpoint, des adaptateurs, du
   régime de résolution, du pilote ou du runtime.

Pour un workflow public, publiez le tuple de versions compatible et la fixture
de benchmark, et non une affirmation générique de performance. Ne combinez pas
les gains en pourcentage issus d'expériences séparées comme s'ils se
multipliaient.

## Pièges courants {#gotchas}

- **Même objet générateur, résultat différent :** son état a été consommé ;
  recréez-le ou restaurez-le pour la comparaison contrôlée.
- **Une inférence plus rapide est déclarée équivalente sur la seule base de la
  latence :** conservez la comparaison des sorties et de la fidélité à la tâche
  pour le runtime exact modifié.
- **Le déchargement est présenté comme une accélération inconditionnelle :**
  mesurez séparément les transferts vers l'hôte et la latence en régime
  permanent, au-delà du bénéfice en capacité mémoire.

## Pages connexes {#related-pages}

- [[flow-matching]]
- [[low-vram-inference-strategies]]
- [[tiled-inference]]
- [[flux-klein-9b-inference]]
