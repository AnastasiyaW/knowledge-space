---
title: "ComfyUI Flux2Klein Enhancer"
description: "Référence de workflow épinglé pour le conditionnement par référence et l'amélioration de l'identité et des détails avec FLUX.2 Klein dans ComfyUI."
level: 3
source_sha256: 9129e484ed905eeac6bb09060cd39f594e06d2147e8738775282297408330e29
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Flux2Klein Enhancer {#comfyui-flux2klein-enhancer}

`ComfyUI-Flux2Klein-Enhancer` est un package de nœuds personnalisés ComfyUI tiers, destiné au conditionnement par référence et au transfert d'identité et de détails. Il cible le comportement de FLUX.2 Klein 9B et n'est pas une version officielle de modèle FLUX. Statut vérifié sur le dépôt du projet le **27/08/2026**.

## Statut actuel {#current-status}

| Propriété | État vérifié |
|---|---|
| Dépôt | `capitan01R/ComfyUI-Flux2Klein-Enhancer` |
| Révision vérifiée de la branche par défaut | `6804643bff9a20926106427ff08d5b1bd2e49861` |
| Licence | MIT |
| Cible principale | FLUX.2 Klein 9B |
| Nombre de références | Jusqu'à huit références dans le workflow actuel |
| Contrôles neutres | Les valeurs neutres exactes sont destinées à un passage direct (pass-through) |
| Benchmark indépendant d'identité | Non disponible dans la passe de recherche bornée |

Le package a dépassé la forme à deux nœuds décrite dans la première annonce. Les concepts de workflow actuels incluent l'encodage des références, `Multi ReferenceLatent`, `Identity Feature Transfer Final` et des masques optionnels.

## Historique de développement {#development-history}

| Date | Événement | Statut temporel |
|---|---|---|
| 07/04/2026 | Premier package/rapport de l'enhancer | Fondation historique |
| 24/06/2026 | Workflow/package élargi signalé | Événement successeur actuel |
| 11/07/2026 | Date de révision vérifiée du dépôt | Instantané actuel du dépôt utilisé ici |

Conserver le texte d'origine de l'annonce sans modification. Rattacher l'extension ultérieure du package et l'état actuel du dépôt comme nœuds successeurs.

## Installation et épinglage {#installation-and-pinning}

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer.git
cd ComfyUI-Flux2Klein-Enhancer
git checkout 6804643bff9a20926106427ff08d5b1bd2e49861
git rev-parse HEAD
```

Redémarrer ComfyUI et charger un workflow correspondant à la révision épinglée. Conserver le JSON du workflow avec le reçu d'exécution : les noms de nœuds et les sockets peuvent changer d'une révision à l'autre.

## Protocole d'évaluation {#evaluation-protocol}

Exécuter une comparaison à graine identique :

```yaml
comfyui_revision: <exact-revision>
plugin_revision: 6804643bff9a20926106427ff08d5b1bd2e49861
model: <exact-flux2-klein-artifact>
reference_count: <1-to-8>
reference_order: <ordered-list>
masks: <file-hashes-or-none>
seed: <integer>
dimensions: <width>x<height>
steps: <integer>
enhancer_controls: <all-values>
gpu_and_vram: <exact-device>
```

Comparer un workflow de référence et un workflow avec enhancer en fixant le modèle, le prompt, la graine, les étapes, les dimensions et le sampler. Consigner la similarité d'identité, le transfert de détails non souhaités, le respect du prompt et le pic de VRAM. Les réglages neutres doivent être testés comme un invariant de passage direct exact.

## Limites des preuves {#evidence-boundaries}

- Le dépôt prouve l'identité de l'implémentation, la surface des nœuds, le modèle cible et la licence.
- « Pas besoin de LoRA », la préservation exacte de l'identité, les gains de qualité et le comportement à faible VRAM sont des affirmations de l'auteur ou de la communauté tant qu'elles n'ont pas été mesurées de façon indépendante.
- Des modèles de conditionnement plus petits peuvent être reconnus par l'implémentation, mais les calendriers de hooks et la cible documentée se concentrent sur Klein 9B.
- Aucune source communautaire chinoise qualifiée n'a été retenue dans la passe initiale bornée.

## Preuves issues de la communauté et des tickets {#community-and-issue-evidence}

- [Issue #35](https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/35) a montré que `Identity Feature Transfer Final` renvoyait `NaN` depuis `IS_CHANGED`, forçant des réexécutions en aval à graine fixe. Le mainteneur a fusionné une correction le 12/06/2026. Il s'agit d'un bug historique : les révisions postérieures à cette fusion ne devraient pas reprendre le contournement.
- [Issue #41](https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/41) signale des changements d'identité après ComfyUI `v0.28.0` avec deux références masquées. L'auteur du signalement a isolé `zero_unmasked_tokens` et utilisé `focus_only` comme contournement ; le ticket est resté ouvert. Conserver la version de ComfyUI, le câblage des masques, le preset et la révision du plugin lors de la reproduction.
- Le [fil de présentation communautaire](https://www.reddit.com/r/StableDiffusion/comments/1t1mvyh/flux2klein_exact_preservation_no_lora_needed/) est utile pour découvrir la méthode, mais « préservation exacte » reste une affirmation de l'auteur ou de la communauté sans métrique indépendante.

## Pièges {#gotchas}

- **Problème :** traiter le plugin comme une fonctionnalité officielle de FLUX → **Correction :** l'identifier comme package ComfyUI tiers et épingler son commit.
- **Problème :** affirmer la préservation de l'identité à partir d'une présentation → **Correction :** exécuter des comparaisons baseline/enhancer à graine identique avec une métrique d'évaluation explicite.
- **Problème :** charger un ancien workflow à deux nœuds avec le package élargi → **Correction :** faire correspondre le JSON du workflow à la révision exacte du plugin.
- **Problème :** supposer que la prise en charge d'un modèle de conditionnement plus petit équivaut à la parité avec le 9B complet → **Correction :** vérifier localement le chemin exact du modèle et les calendriers.
- **Problème :** réutiliser `zero_unmasked_tokens` entre versions de ComfyUI → **Correction :** reproduire avec la configuration de masque/preset épinglée ; `focus_only` est un contournement signalé pour la v0.28, pas une valeur par défaut universelle.

## Statut temporel {#temporal-status}

- **Actuel :** workflow multi-références élargi, à la révision épinglée de juillet 2026.
- **Historique :** description initiale à deux nœuds d'avril.
- **Signalé, non vérifié de façon indépendante :** préservation exacte, remplacement sans LoRA, gain de qualité et performances à faible mémoire.

## Brief pour agents {#agent-brief}

Épingler le plugin, ComfyUI, le JSON du workflow et le modèle avant tout dépannage. Séparer les faits du dépôt des affirmations d'efficacité issues de présentations et de la communauté. Exiger une baseline contrôlée pour toute affirmation sur l'identité ou les détails. Conserver l'annonce initiale comme historique et rattacher l'état actuel du package comme point d'arrivée, sans la réécrire.

## Sources {#sources}

- Dépôt du projet : https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer
- Espace de discussion communautaire : https://www.reddit.com/r/StableDiffusion/comments/1t1mvyh/flux2klein_exact_preservation_no_lora_needed/
- Bug corrigé d'invalidation de cache : https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/35
- Comportement ouvert des masques ComfyUI v0.28 : https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/41
