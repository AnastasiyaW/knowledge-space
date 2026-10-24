---
title: "Audio Flamingo"
description: "Référence tenant compte des versions pour les points de contrôle de compréhension Audio Flamingo 3, Music Flamingo et Audio Flamingo Next."
level: 4
source_sha256: faaf08c64e3a7f268c48caeca723319d73b4aee5d546e6b4a35d49bfdf9e5c7a
translation: machine
translated_at: '2026-10-24'
---
# Audio Flamingo {#audio-flamingo}

Audio Flamingo est une famille de recherche de NVIDIA sur la compréhension audio. Audio Flamingo 3 (AF3), Music Flamingo et Audio Flamingo Next (AF-Next) sont des branches apparentées mais distinctes. Statut vérifié à partir des sources officielles du projet, de l'article, du dépôt et des fiches de modèle, à la date du **2026-08-27**.

## Carte actuelle de la famille {#current-family-map}

| Branche | Objectif | Périmètre de l'artefact actuel |
|---|---|---|
| Audio Flamingo 3 | Compréhension générale du langage audio | Branche de recherche publiée antérieurement |
| Music Flamingo | Compréhension et raisonnement centrés sur la musique | Branche musicale distincte ; ne pas la traiter comme une version corrective d'AF3 |
| Audio Flamingo Next | Famille actuelle de compréhension de longs fichiers audio | Points de contrôle Hugging Face 8B BF16 : variantes instruction, thinking et captioning |

La fiche de modèle officielle `nvidia/audio-flamingo-next-hf` fait autorité pour l'inférence d'AF-Next. Le dépôt plus ancien `NVIDIA/audio-flamingo` précède AF-Next et ne doit pas servir à déduire l'ensemble des fonctionnalités ou des détails d'installation actuels.

## Contrat d'entrée d'AF-Next {#af-next-input-contract}

| Propriété | Valeur vérifiée sur la fiche de modèle |
|---|---|
| Famille de points de contrôle | 8B BF16 |
| Variantes | instruction, thinking, captioner |
| Format audio | 16 kHz mono |
| Fenêtre de traitement | 30 secondes |
| Durée maximale documentée | 1 800 secondes / 30 minutes |
| Environnement d'exécution | Exemple de fiche de modèle Transformers |
| Fournisseur d'inférence hébergée | Aucun affiché au moment de la vérification |
| Licence | Non commerciale ; consulter la licence exacte de la fiche de modèle avant utilisation |

La prise en charge des longs fichiers audio repose sur un traitement par fenêtres. « Prend en charge 30 minutes » ne signifie pas un tenseur de contexte unique et illimité, un streaming en temps réel ni une inférence à faible consommation mémoire.

Le point de contrôle AF-Next publié est un modèle de compréhension audio. Le projet de recherche plus large évoque la synthèse vocale en streaming (TTS) et les capacités voix-à-voix, mais ces capacités ne sont **pas incluses dans le point de contrôle Hugging Face publié**.

## Historique de développement {#development-history}

| Date | Fil | Événement | Statut temporel |
|---|---|---|---|
| 2025-10-27 | langage audio général | Audio Flamingo 3 présenté | Fondation historique |
| 2025-11-15 | compréhension musicale | Music Flamingo présenté | Branche distincte actuelle |
| 2026-04-15 | langage audio général | Audio Flamingo Next présenté | Branche successeur actuelle |

AF3 peut être le prédécesseur d'AF-Next dans le fil du langage audio général. Music Flamingo reste une branche de projet distincte, car sa spécialisation et ses artefacts diffèrent.

## Utilisation pratique {#practical-use}

Choisissez la variante d'AF-Next en fonction du comportement attendu en sortie :

- **Point de contrôle instruction :** analyse audio directe suivant des instructions.
- **Point de contrôle thinking :** tâches orientées raisonnement, lorsque le contrat de la fiche de modèle prend explicitement en charge ce mode.
- **Captioner :** description audio dense ou structurée.

Normalisez l'entrée avant l'évaluation :

```yaml
sample_rate_hz: 16000
channels: 1
duration_seconds: <0-to-1800>
checkpoint: nvidia/audio-flamingo-next-hf
checkpoint_revision: <immutable-revision>
variant: instruction-or-thinking-or-captioner
dtype: bfloat16
device: <exact-gpu>
transformers_version: <exact-version>
```

Pour les longs enregistrements, conservez les décalages temporels de chaque fenêtre de 30 secondes afin de pouvoir remonter des réponses jusqu'à l'audio source. Testez le comportement de recouvrement et d'agrégation sur la tâche cible plutôt que de supposer que les frontières de fenêtres sont sémantiquement neutres.

## Quand l'utiliser {#when-to-use}

- Questions-réponses audio, description et analyse sémantique dans le cadre du contrat de tâche de la fiche de modèle.
- Longs enregistrements pour lesquels le parcours documenté par fenêtres de 30 minutes est utile.
- Évaluation de recherche lorsque la licence non commerciale est acceptable.

Ne présentez pas le point de contrôle AF-Next publié comme une preuve de synthèse vocale en streaming, de conversion de voix ou de droits de déploiement commercial.

## Limites des retours de la communauté {#community-evidence-boundary}

Aucune source chinoise qualifiée ni aucune recette reproductible de consommation de mémoire sur matériel grand public n'a été retenue lors de la passe limitée. Un écart d'implémentation précis a été conservé :

- [Issue #104](https://github.com/NVIDIA/audio-flamingo/issues/104) montre que `audio-flamingo-3-hf` sous Transformers rejette une conversation multi-tours à deux fichiers audio avec une `ValueError` due à une correspondance 1:1 entre le nombre de textes et d'audios. Le ticket est ouvert, sans réponse des mainteneurs. Il concerne AF3 et non AF-Next, et rend l'affirmation générale de « dialogue multi-audio » inadaptée comme recette Transformers générique.
- [Issue #106](https://github.com/NVIDIA/audio-flamingo/issues/106) documente des ambiguïtés non résolues dans la chronologie du jeu de données LongAudio (écarts de raccordement de 1 seconde contre 10 ms, et segments hors d'ordre). Cela affecte la reproduction des résultats de questions-réponses temporelles, et non l'inférence courante du point de contrôle.

## Pièges courants {#gotchas}

- **Problème :** combiner les résultats d'AF3, de Music Flamingo et d'AF-Next -> **Correction :** nommer la branche et la variante de point de contrôle dans chaque affirmation.
- **Problème :** lire « prise en charge de 30 minutes » comme un streaming ou un contexte en une seule passe -> **Correction :** respecter le contrat de fenêtrage documenté de 30 secondes et tester l'agrégation.
- **Problème :** revendiquer la TTS ou la conversion voix-à-voix à partir du point de contrôle HF d'AF-Next -> **Correction :** limiter les affirmations sur le point de contrôle aux capacités de compréhension audio publiées.
- **Problème :** ignorer la licence non commerciale -> **Correction :** consulter et consigner la licence exacte du point de contrôle avant toute utilisation produit.
- **Problème :** supposer que des résultats de recherche multi-audio se transposent directement au modèle de conversation Transformers d'AF3 -> **Correction :** tester le contrat exact du processeur ; le ticket #104 signale une non-correspondance 1:1 actuelle.

## Statut temporel {#temporal-status}

- **Actuel :** variantes de la fiche de modèle AF-Next 8B BF16 et leur contrat de 16 kHz mono, fenêtres de 30 secondes, maximum de 30 minutes.
- **Historique :** branche audio générale AF3.
- **Parallèle :** branche de compréhension musicale Music Flamingo.
- **Non publié dans le point de contrôle cité :** fonctionnalités de TTS en streaming et de voix-à-voix.

## Brief pour agents {#agent-brief}

Identifiez `AF3`, `Music Flamingo` ou `AF-Next` avant de répondre. Pour AF-Next, consultez la fiche de modèle actuelle et identifiez la variante exacte. Conservez le format audio, la durée et le fenêtrage, le dtype, le matériel, la révision et la licence. Ne transformez jamais des démonstrations de recherche plus larges en capacités d'un point de contrôle publié, et distinguez explicitement les observations de la communauté des faits issus des artefacts officiels.

## Sources {#sources}

- Dépôt Audio Flamingo : https://github.com/NVIDIA/audio-flamingo
- Projet Audio Flamingo 3 : https://research.nvidia.com/labs/adlr/AF3/
- Point de contrôle Audio Flamingo Next : https://huggingface.co/nvidia/audio-flamingo-next-hf
- Article Audio Flamingo Next : https://arxiv.org/abs/2604.10905
- Écart multi-audio Transformers d'AF3 : https://github.com/NVIDIA/audio-flamingo/issues/104
- Écart de reproduction de la chronologie LongAudio : https://github.com/NVIDIA/audio-flamingo/issues/106
