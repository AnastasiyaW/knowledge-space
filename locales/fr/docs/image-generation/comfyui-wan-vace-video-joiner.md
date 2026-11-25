---
title: "Joiner vidéo Wan VACE pour ComfyUI : contrat de workflow lié à une version"
description: "Une jointure vidéo Wan VACE dans ComfyUI est un workflow communautaire lié à une version précise, et non un simple nœud de transition générique ; figez la révision du workflow, les dépendances ComfyUI, custom-nodes et modèles, les contrats d'images, de timestamps et de couleur des entrées, la politique de génération des images de liaison et de bouclage, les artefacts intermédiaires, ainsi que la revue visuelle et audio avant publication d'un clip assemblé."
category: workflows
tags: [comfyui, wan-vace, video, transitions, provenance, review]
aliases: ["ComfyUI Wan VACE Video Joiner", "Wan VACE Video Joiner"]
level: 2
source_sha256: cd04f963ee940b295ad7c11ea7165fb0e467d19f1139291027288c33c4cfcdbc
translation: machine
translated_at: '2026-10-24'
---
# Joiner vidéo Wan VACE pour ComfyUI : contrat de workflow lié à une version {#comfyui-wan-vace-video-joiner-release-bound-workflow-contract}

Une jointure Wan VACE doit être traitée comme une version particulière d'un
workflow ComfyUI, et non comme un nœud de transition générique. Le
[dépôt communautaire ComfyUI Wan VACE Video Joiner](https://github.com/stuttlepress/ComfyUI-Wan-VACE-Video-Joiner)
publie des workflows qui génèrent des images de liaison à partir du contexte
situé de part et d'autre de la frontière entre deux clips. Il documente
également les dépendances sensibles à la version et les modes de défaillance
connus. C'est un bon point de départ, mais cela ne garantit pas que toute
paire de clips source se joindra correctement.

## Figer le workflow exécutable {#pin-the-executable-workflow}

Pour chaque exécution, consignez :

- le fichier de workflow et la révision du dépôt, ainsi que toute modification locale ;
- les versions du backend et du frontend ComfyUI, les révisions des custom-nodes et leur source d'installation ;
- le modèle, les poids et la précision compatibles VACE, ainsi que le sous-graphe d'échantillonnage utilisé ;
- les clips d'entrée, la règle d'ordonnancement, le conteneur et le codec, le nombre d'images, les timestamps, la fréquence d'images, les dimensions, l'interprétation des couleurs, la politique de canal alpha et tout rééchantillonnage ;
- le contexte de transition, la politique de remplacement ou de génération, la politique de bouclage, la graine (seed) et les identifiants de file d'attente et d'exécution ; et
- les images ou fichiers intermédiaires avec leurs empreintes, les paramètres d'encodage finaux et l'empreinte de la sortie.

Le workflow amont identifie actuellement Wan 2.1 VACE et Wan 2.2 Fun VACE
comme chemin de modèles de diffusion compatible. Ne supposez pas qu'un modèle
non VACE, un autre fichier JSON de workflow ou une installation ComfyUI non
figée présente le même contrat.

## Traiter les images de liaison générées comme un contenu dérivé {#treat-generated-bridge-frames-as-derived-content}

Consignez quelles images sont des images source conservées et lesquelles sont
générées, remplacées, fusionnées, interpolées, alignées en couleur ou
réencodées. Une transition qui paraît continue peut tout de même modifier
l'exposition, la couleur, la géométrie, le texte, le mouvement ou des détails
factuels. Si un bouclage est demandé, évaluez séparément la frontière entre la
dernière et la première image ; un interrupteur de bouclage ne constitue pas
une preuve de boucle sans raccord.

Conservez les droits sur la source et le périmètre des modifications autorisées
dans la fiche du clip. Vérifiez la synchronisation et la continuité audio
indépendamment des images, car un alignement visuel n'établit pas la justesse
de l'audio.

## Valider la condition de livraison cible {#validate-the-target-delivery-condition}

Exécutez une jointure représentative de petite taille dans l'environnement figé
avant de traiter un lot. Examinez chaque frontière à la fréquence d'images et
à la résolution de livraison, en recherchant images perdues ou répétées,
effet fantôme, discontinuité de mouvement, décalages de luminosité ou de
couleur, sujets ou objets modifiés, et erreurs d'encodage ou de conteneur.
Conservez une procédure de relance pour une seule frontière défaillante plutôt
que de remplacer un lot sans preuve.

Si une dépendance requise, un modèle, une forme d'entrée ou une validation de
workflow échoue, arrêtez-vous explicitement en conservant l'environnement
capturé et l'erreur. Ne substituez ni un fondu enchaîné, ni un autre modèle,
ni une fréquence d'images modifiée, ni un autre nœud comme résultat équivalent.

## Pages liées {#related-pages}

- [[temporal-tiling]]
- [[tiled-inference]]
- [[diffusion-inference-acceleration]]
- [[flow-matching]]
