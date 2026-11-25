---
title: "Architectures de débruitage : contrat de dégradation et de preuve"
description: "Une architecture de débruitage se choisit en fonction d'une dégradation déclarée et d'un objectif de fidélité, et non d'un classement ou du nom d'une famille ; il faut associer les hypothèses de capture et de bruit, le modèle et son checkpoint, le chemin de prétraitement, de découpage en tuiles et de couleur, les découpages d'entraînement et d'évaluation autorisés, les métriques de tâche et de préservation, ainsi qu'une revue visuelle avant d'accepter des détails générés ou restaurés."
category: reference
tags: [denoising, restoration, degradation, evaluation, fidelity, provenance]
aliases: ["Denoise Architectures 2026", "Image Denoising Architectures"]
level: 2
source_sha256: 5aa1d877cc8bdd49fb2705094c356294238c13462f227d5bf11dcaa3599751c7
translation: machine
translated_at: '2026-10-24'
---
# Architectures de débruitage : contrat de dégradation et de preuve {#denoising-architectures-degradation-and-evidence-contract}

Les noms d'architectures n'identifient ni la dégradation à supprimer, ni les
détails à préserver. Un débruiteur peut estimer du bruit de capteur, des
artefacts de compression, du flou, de la pluie, une perturbation synthétique
ou un mélange de ces éléments ; chaque tâche requiert un contrat distinct
d'entrée, de fidélité et d'évaluation.

Le [rapport du défi NTIRE 2025 sur le débruitage d'images](https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/html/Sun_The_Tenth_NTIRE_2025_Image_Denoising_Challenge_Report_CVPRW_2025_paper.html)
présente les méthodes et les scores obtenus pour son défi AWGN à sigma 50.
Ses résultats constituent des éléments utiles pour ce benchmark précis. Ils ne
permettent pas de classer les architectures de manière universelle selon les
chaînes de traitement des caméras, les mélanges de bruit, les retouches
artistiques, la récupération en contexte forensique, les limites d'exécution
ou les exigences de préservation des détails protégés.

## Déclarer la cible de restauration {#declare-the-restoration-target}

Pour chaque évaluation ou déploiement de modèle, consigner :

- la provenance de l'actif source ou de la capture, l'orientation, le profil
  colorimétrique, la plage dynamique, l'historique de compression, la politique
  alpha/masque et le modèle de dégradation déclaré ;
- le modèle/checkpoint, le code/runtime/version, la plage d'entrée compatible,
  le domaine colorimétrique, le prétraitement, le padding, la politique de
  découpage/tuilage/fusion et la transformation de sortie ;
- les données appariées ou de référence normale autorisées, la politique
  d'annotation/de vérité terrain, les découpages disjoints par groupe, et tout
  générateur de dégradation synthétique ;
- les métriques de tâche et les métriques de préservation, évaluées sur un
  ensemble disjoint par source ; et
- la revue visuelle de la suppression du bruit, de la texture, du texte, des
  contours, de la géométrie des produits, des visages, des ombres, des dégradés,
  des couleurs et des zones protégées à la taille de livraison.

Changer la caméra, le codec, la distribution du bruit, le recadrage, l'espace
colorimétrique de travail, le plan de tuilage ou le checkpoint crée une
nouvelle configuration. Un score obtenu avec une autre dégradation ou un autre
découpage de sources ne constitue pas une preuve pour celle-ci.

## Choisir selon le comportement d'échec mesuré {#choose-by-measured-failure-behavior}

Les approches convolutives, transformeurs, à espace d'états, de Fourier et
fondées sur la diffusion font des hypothèses différentes sur la localité, le
conditionnement et la génération. N'utiliser la version documentée que lorsque
ses hypothèses correspondent à la tâche déclarée, puis la comparer à une
référence nommée, avec des entrées et un chemin d'export identiques.

Mesurer la latence et la mémoire de pointe séparément de la qualité de
récupération. Si une méthode génère une texture ou un détail plausible non
étayé par l'entrée, qualifier cette sortie de dérivée/générée plutôt que de
signal source récupéré. Pour une correction masquée, consigner le masque et
vérifier séparément que les zones hors masque sont inchangées ; une absence
apparente de modification hors masque n'est pas démontrée sans comparaison.

## Limite d'échec {#failure-boundary}

Si les hypothèses de dégradation, la compatibilité du modèle, l'autorité de la
vérité terrain, l'évaluation disjointe par source ou la revue des détails
protégés font défaut, retourner un état visible de revue ou d'échec. Ne pas
sélectionner un modèle parce qu'il domine un autre classement, ne pas basculer
silencieusement vers un a priori génératif, et ne pas présenter un détail
plausible comme une restauration factuelle.

## Pages connexes {#related-pages}

- [[image-restoration-survey]]
- [[paired-training-for-restoration]]
- [[tiled-inference]]
- [[frequency-decomposition-editing]]
