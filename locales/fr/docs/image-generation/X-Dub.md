---
title: "X-Dub : doublage visuel public sans masque"
description: "X-Dub est une version publique de doublage visuel basée sur Wan2.2-TI2V-5B ; validez le recadrage sur une seule personne, l'identité, la stabilité temporelle, les droits audio et les conditions du modèle pour chaque vidéo cible."
category: models
tags: [visual-dubbing, lip-sync, video-editing, wan2.2, audio-driven, generative-bootstrapping, synthetic-media]
aliases: ["X-Dub Wan-5B"]
level: 2
source_sha256: 2a5a84f96014f1d39f81709e61aa2c2e1fce870f70a5fb728e4111331768796d
translation: machine
translated_at: '2026-10-24'
---
# X-Dub : doublage visuel public sans masque {#x-dub-public-mask-free-visual-dubbing}

**Périmètre vérifié : 2026-09-04.** X-Dub est l'implémentation publique d'une méthode de doublage visuel qui synchronise une vidéo avec un audio de remplacement. La méthode en amont présente la tâche comme une édition sans masque entraînée par amorçage génératif (*generative bootstrapping*). Elle vise à modifier les mouvements liés à la parole tout en conservant le reste de la vidéo, mais cette conservation est un objectif d'acceptation, et non une garantie.

## Version publique et modèle de l'article {#public-release-versus-the-paper-model}

Les mainteneurs distinguent explicitement la version publique X-Dub (Wan-5B) du modèle interne évalué dans l'article. La version publique repose sur une pile basée sur Wan2.2-TI2V-5B et un affinage supervisé en plusieurs étapes ; le modèle interne et son réglage LoRA ne sont pas publiés.

Ne transférez pas les résultats quantitatifs, les attentes de qualité ou les paramètres du modèle interne de l'article vers le point de contrôle public. Le dépôt public lui-même signale des limites persistantes en matière de cohérence temporelle et de sujet, et indique qu'une comparaison quantitative reste à réaliser.

## Limites actuelles d'exécution {#current-runtime-boundary}

Le dépôt officiel fournit un pipeline d'inférence, un ensemble de modèles, des composants audio et une prise en charge du recadrage de visage. Son chemin de recadrage en ligne actuel est destiné aux vidéos à **une seule personne**. Il recadre le visage, applique le doublage sur ce recadrage, puis reporte le résultat sur la vidéo d'origine.

Ce chemin pratique n'est pas un suivi multi-personnes. Un mouvement rapide de la tête, une occlusion ou un suivi de recadrage peu fiable peuvent provoquer des tremblements, une dérive d'identité, une dérive colorimétrique ou des images défaillantes. Considérez chaque sortie comme un extrait candidat nécessitant une relecture.

## Flux de travail sûr en production {#safe-production-workflow}

1. Vérifiez les droits et le consentement pour la vidéo source, l'audio de remplacement et toute personne ou tout personnage représenté.
2. Figez la révision exacte du dépôt, les poids, les dépendances, la vidéo d'entrée, l'audio d'entrée et les paramètres d'inférence.
3. Exécutez un court segment représentatif avant de traiter un actif complet.
4. Relisez la sortie image par image autour de la parole, des coupures, des occlusions, des mouvements rapides et de la frontière de recadrage.
5. Comparez l'identité, l'éclairage, la colorimétrie, l'arrière-plan et les mouvements hors bouche par rapport à la source.
6. Conservez la source, la sortie, la configuration, les journaux et une mention claire de contenu synthétique le cas échéant.

N'utilisez jamais un résultat de doublage généré comme preuve qu'une personne réelle a dit quelque chose. Pour les contenus publics, commerciaux ou sensibles, ajoutez une étape d'approbation humaine et respectez les règles applicables en matière de consentement, de divulgation et de plateforme.

## Matrice de validation {#validation-matrix}

| Risque | Preuve requise |
|---|---|
| Alignement lèvres/audio | relire plusieurs segments de parole avec l'audio prévu |
| Identité et apparence | comparaison source/sortie à la résolution de livraison |
| Stabilité temporelle | relecture séquentielle au niveau des coupures, des virages rapides et des occlusions |
| Exactitude du recadrage | vérifier que seul le visage visé a été sélectionné |
| Reproductibilité | empreintes de la source et de l'audio, révision du modèle, paramètres et accusé de réception de la sortie |

## Conditions de licence et des artefacts {#licensing-and-artifact-terms}

Le code du dépôt, le backbone Wan, l'ensemble des points de contrôle, les composants du modèle audio et toute intégration communautaire peuvent relever de conditions distinctes. Examinez les conditions actuelles et les conditions de redistribution de chaque artefact téléchargé ; ne déduisez pas l'autorisation de déploiement de l'étiquette d'un seul dépôt.

## Références {#references}

- [Dépôt officiel de X-Dub](https://github.com/KlingAIResearch/X-Dub)
- [Page du projet X-Dub](https://hjrphoebus.github.io/X-Dub/)
- [Article X-Dub](https://arxiv.org/abs/2512.25066)
- [Collection de modèles X-Dub](https://huggingface.co/KlingTeam/X-Dub)
