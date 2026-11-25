---
title: "ACE-Step 1.5"
description: "Référence tenant compte des artefacts et du matériel pour la génération musicale ACE-Step 1.5, base/SFT/turbo, et l'exécution XL."
level: 3
source_sha256: 41b142fc4ff664e57772a73c242bbb8f00516a383f01fb62abe8bbee03d2cc40
translation: machine
translated_at: '2026-10-24'
---
# ACE-Step 1.5 {#ace-step-15}

ACE-Step 1.5 est un projet open source de génération musicale proposant les artefacts base, SFT, turbo et XL. Le nombre d'étapes, le comportement du CFG, la mémoire et les limites de durée dépendent de l'artefact sélectionné et du mode d'exécution. Statut vérifié à partir des documents de publication, de la fiche modèle, du tutoriel et du guide GPU de première partie, à la date du **2026-08-27**.

## Statut actuel {#current-status}

| Élément | État vérifié |
|---|---|
| Version actuelle du dépôt | `v0.1.8`, publiée le 2026-05-18 |
| Licence | MIT sur le périmètre officiel du projet et du modèle ; vérifier chaque artefact téléchargé |
| Affirmation de faible mémoire pour base 1.5 | Peut fonctionner sous 4 Go sur le chemin base documenté ; ce n'est pas une affirmation concernant XL |
| Échantillonnage base/SFT | 50 étapes avec CFG dans le tableau documenté |
| Échantillonnage turbo | 8 étapes sans CFG dans le tableau documenté |
| XL <=12 Go | Non recommandé ni pris en charge par le guide GPU officiel |

Ne pas fusionner « ACE-Step 1.5 fonctionne sous 4 Go » avec les exigences d'ACE-Step 1.5 XL. Ces deux affirmations concernent des chemins d'artefacts différents.

## Sélecteur d'artefact {#artifact-selector}

| Artefact | Étapes | CFG | Règle de sélection |
|---|---:|---|---|
| base | 50 | activé | Chemin de référence en qualité et en contrôle |
| SFT | 50 | activé | À sélectionner uniquement lorsque son comportement affiné est requis |
| turbo | 8 | désactivé | Chemin rapide ; ne pas reprendre les paramètres CFG de base |
| Variantes XL | Dépendant de la version | Dépendant de la version | Utiliser le tableau exact de la version et la vérification préalable du GPU |

Conserver le répertoire complet du modèle et sa révision dans les justificatifs d'exécution. Un libellé d'interface tel que « XL » est insuffisant lorsque plusieurs fichiers base/SFT/turbo sont installés.

## Planification GPU et mémoire pour XL {#gpu-and-memory-planning-for-xl}

| VRAM disponible | Limite indiquée par le guide officiel |
|---|---|
| 12 Go ou moins | Ne pas utiliser XL |
| 12-16 Go | Chemin XL limité avec déchargement CPU et INT8 |
| 16-20 Go | XL avec déchargement |
| 20 Go ou plus | Chemin XL complet |
| 24 Go ou plus | Toutes les options LM sans déchargement ni quantification, selon le guide |

Pour 12-16 Go, le guide limite la durée maximale à environ 8 minutes avec LM et à 10 minutes sans LM. Ne pas reformuler cela en « 10 minutes avec LM ». La durée, l'état LM, le déchargement, la quantification et le GPU doivent être documentés ensemble.

## Historique de développement {#development-history}

| Date | Événement | Statut temporel |
|---|---|---|
| 2026-02-03 | Rapport de publication initiale d'ACE-Step 1.5 | Fondation historique |
| 2026-02-04 | Disponibilité de la démo rétablie/signalée | Événement d'appui ; pas un jalon distinct du projet |
| 2026-04-07 | ACE-Step 1.5 XL annoncé | Fondation de la branche XL actuelle |
| 2026-05-18 | Dépôt `v0.1.8` | Version actuelle au moment de la vérification |

Le rétablissement de la démo sert de preuve complémentaire à l'événement initial, et non de nouvelle branche de développement.

## Journal d'exécution reproductible {#reproducible-run-record}

```yaml
ace_step_version: 0.1.8
artifact: base-or-sft-or-turbo-or-exact-xl-name
artifact_revision: <immutable-revision>
steps: 50-or-8
cfg_enabled: <true-or-false>
lm_enabled: <true-or-false>
duration_seconds: <integer>
dtype_or_quantization: <exact-value>
cpu_offload: <true-or-false>
gpu: <exact-model-and-vram>
peak_vram: <measured-value>
seed: <integer>
```

Valider un échantillon court avant toute génération de longue durée. Si la mémoire approche la limite matérielle, réduire la taille de l'artefact ou utiliser le chemin documenté de déchargement/INT8, plutôt que de modifier silencieusement plusieurs paramètres.

## Limites des retours de la communauté {#community-evidence-boundary}

Les rapports communautaires sur la qualité et la mémoire ne sont utiles que s'ils conservent l'artefact, la version, la durée, l'état LM, le déchargement, la quantification, le nombre d'étapes et le GPU. Deux rapports d'incident actuels fournissent des indications opérationnelles limitées :

- [Issue #1274](https://github.com/ace-step/ACE-Step-1.5/issues/1274) reproduit des latents NaN/Inf sur un Quadro RTX 6000 de 24 Go (Turing) pour turbo et XL-turbo. Le passage du seul repli du DiT principal de FP16 à FP32 a résolu le cas du rapporteur, mais a augmenté la VRAM utilisée ; un contributeur a confirmé que le chemin de type de données nécessite une correction de code. Considérer FP32 comme un contournement de diagnostic jusqu'à ce qu'une version ferme explicitement ce ticket.
- [Issue #1271](https://github.com/ace-step/ACE-Step-1.5/issues/1271) isole la fuite de `cover_noise_strength=0.2` depuis Cover/Remix vers la génération texte-vers-musique, qui produit un bruit statique sur toute la durée. Un contributeur a confirmé le chemin côté backend et recommande de remettre `cover_noise_strength` à `0` avant de revenir à la génération texte-vers-musique, jusqu'à correction.

## Pièges {#gotchas}

- **Problème :** Appliquer l'affirmation de moins de 4 Go du modèle base à XL -> **Correction :** utiliser la matrice VRAM de XL ; <=12 Go n'est pas une cible XL.
- **Problème :** Activer le CFG pour turbo parce que base l'utilise -> **Correction :** utiliser 8 étapes avec CFG désactivé, comme indiqué dans le chemin turbo documenté.
- **Problème :** Affirmer que 12-16 Go prennent en charge 10 minutes avec LM -> **Correction :** conserver la distinction du guide entre 8 minutes avec LM et 10 minutes sans LM.
- **Problème :** Signaler « ACE-Step 1.5 » sans artefact ni version -> **Correction :** indiquer base/SFT/turbo/XL ainsi que la révision exacte.
- **Problème :** La génération texte-vers-musique devient soudainement un bruit statique sur toute la durée après le mode Cover -> **Correction :** inspecter les paramètres d'exécution sauvegardés et remettre `cover_noise_strength` à `0` ; conserver le ticket #1271 comme preuve liée à la version.

## Statut temporel {#temporal-status}

- **Actuel :** `v0.1.8` au moment de la vérification ; règles d'étapes et de CFG propres à chaque artefact ; matrice GPU officielle pour XL.
- **Historique :** publication initiale de février et rétablissement de la démo.
- **Remplacé :** les affirmations générales et anciennes sur la mémoire, lorsqu'elles sont appliquées à XL.
- **Ouvert :** comparaison reproductible de la qualité sur les GPU grand public.

## Consigne pour agents {#agent-brief}

Demander l'artefact ACE-Step exact et le GPU avant de générer une recette. Consulter la version actuelle et le guide GPU, puis lier étapes, CFG, LM, durée, quantification et déchargement à cet artefact. Rejeter toute tentative de généraliser l'affirmation « moins de 4 Go » du modèle base à XL, ou de réutiliser les paramètres d'échantillonnage de base pour turbo.

## Sources {#sources}

- Dépôt et versions officiels : https://github.com/ace-step/ACE-Step-1.5/releases
- Fiche modèle officielle : https://huggingface.co/ACE-Step/Ace-Step1.5
- Tutoriel en chinois : https://ace-step.github.io/ACE-Step-1.5/zh/Tutorial
- Article : https://arxiv.org/abs/2602.00744
- Rapport NaN/repli FP32 sur architectures antérieures à Ampere : https://github.com/ace-step/ACE-Step-1.5/issues/1274
- Rapport de fuite de paramètres Cover : https://github.com/ace-step/ACE-Step-1.5/issues/1271
