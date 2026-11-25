---
title: "Transformers v5 : migration liée à une version précise"
description: "Transformers v5 déplace la conversion des checkpoints dans le loader, mais chaque intégration doit être épinglée sur une version installée, un contrat d'exécution, un checkpoint et un test d'adaptateur ; les API de la branche principale actuelle ne constituent pas une compatibilité universelle."
category: infrastructure
tags: [huggingface, transformers, weight-converter, migration, checkpoint-loading, compatibility]
level: 2
source_sha256: 6820230129d9c490e660cb795a8c6574b56133a26611f687a69af8686cf1f820
translation: machine
translated_at: '2026-10-24'
---
# Transformers v5 : migration liée à une version précise {#transformers-v5-version-bound-migration}

Transformers v5 est une ligne de version majeure en évolution, et non un instantané d'API figé. Une migration commence par l'enregistrement de la version du paquet installée ainsi que des révisions exactes du modèle, du checkpoint et des bibliothèques associées. Ne déduisez pas le comportement d'un article de blog, d'un exemple de la branche `main` ou d'une version corrective sans rapport.

La [liste des releases](https://github.com/huggingface/transformers/releases) officielle et la [documentation v5](https://huggingface.co/docs/transformers/) font foi pour la version du paquet que vous installez réellement.

## Conversion dynamique des checkpoints {#dynamic-checkpoint-conversion}

La [documentation de WeightConverter](https://github.com/huggingface/transformers/blob/main/docs/source/en/weightconverter.md) actuelle décrit un loader capable de renommer, découper, fusionner, transposer, fragmenter et quantifier des tenseurs de checkpoint compatibles pendant le chargement. Il est utile lorsque la disposition sérialisée d'un modèle pris en charge diffère de sa disposition de paramètres à l'exécution.

Ce mécanisme a des limites claires :

- une correspondance de conversion doit exister pour le modèle ou la classe native visée ;
- les modèles à code personnalisé ne sont pas couverts automatiquement par une correspondance ;
- un chargement réussi ne prouve ni la parité des sorties, ni la compatibilité des adaptateurs, ni l'aptitude à un autre framework ; et
- un loader Transformers ne convertit pas automatiquement un pipeline Diffusers, un fork personnalisé ou un checkpoint tiers arbitraire.

Traitez les correspondances manquantes, les clés inattendues, les changements de dtype et les erreurs d'adaptateur comme des échecs de compatibilité visibles. Ne sélectionnez pas silencieusement un autre loader ou un autre checkpoint.

## Contrat de migration {#migration-contract}

Avant de modifier un environnement de génération d'images, consignez la matrice suivante :

| Périmètre | À enregistrer |
|---|---|
| Paquet | version installée de Transformers, Python, PyTorch et versions de l'accélérateur ou du runtime |
| Modèle | révision du dépôt, configuration, fichiers et empreintes du checkpoint, dtype et device map |
| Intégration | Diffusers, PEFT/adaptateurs, code personnalisé et toutes les révisions de patchs locaux |
| Référence | un chargement épinglé avant migration et une vérification structurelle ou de sortie propre à la tâche |
| Candidat | le nouvel environnement, le rapport du loader, les avertissements et la vérification de tâche correspondante |

Exécutez le chemin de chargement en conservant intacts les journaux. Vérifiez ensuite ce dont l'application a réellement besoin : par exemple la forme et le dtype des sorties de l'encodeur de texte, l'attachement des adaptateurs, l'appel de génération, le comportement mémoire et une sortie relue. Le succès de l'import ou de `from_pretrained` seul ne constitue pas une preuve de mise en production.

## Intégrations de génération d'images {#image-generation-integrations}

Les piles de génération d'images couvrent souvent plusieurs paquets. Un modèle peut utiliser Transformers pour un encodeur de texte, tandis que son débruiteur, son scheduler, son VAE ou son runtime d'adaptateurs relève d'une autre bibliothèque. Épinglez et testez l'ensemble de la pile conjointement.

Pour un projet utilisant [[SANA]], [[PixelSmile]] ou une autre intégration propre à un modèle :

1. lisez la dépendance et le contrat de patch déclarés dans le dépôt amont ;
2. reproduisez un chargement minimal pris en charge par l'amont ;
3. ajoutez le chemin d'adaptateur ou d'édition du projet ;
4. comparez avec la référence épinglée ; et
5. conservez la matrice de versions et les sorties d'échec avec le résultat.

Cette démarche fait de la conversion dynamique une fonctionnalité de compatibilité traçable, et non une raison de supposer que chaque modèle historique se charge désormais sans modification.

## Sources et pages associées {#sources-and-related-pages}

- [Vue d'ensemble de Transformers v5](https://huggingface.co/blog/transformers-v5)
- [Releases de Transformers](https://github.com/huggingface/transformers/releases)
- [Documentation du chargement dynamique des poids](https://github.com/huggingface/transformers/blob/main/docs/source/en/weightconverter.md)
- [[SANA]]
- [[PixelSmile]]
- [[flux-klein-9b-inference]]
