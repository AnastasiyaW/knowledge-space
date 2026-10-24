---
title: "Calligrapher : personnalisation d'images de texte guidée par référence"
description: "Calligrapher personnalise des images de texte à partir de références de style via FLUX.1-Fill-dev, SigLIP, des masques et les poids du projet ; traitez la précision typographique et les licences comme des critères d'acceptation distincts."
category: models
tags: [text-editing, typography, style-reference, flux-fill, siglip, self-distillation, multilingual]
aliases: ["Calligrapher"]
level: 2
source_sha256: 4342e99b7c6144336d63a3e9d5fb3cf467bf06584b2058b3848f7264997501e7
translation: machine
translated_at: '2026-10-24'
---
# Calligrapher : personnalisation d'images de texte guidée par référence {#calligrapher-reference-guided-text-image-customization}

**Périmètre vérifié : 2026-09-04.** Calligrapher est un projet fondé sur la diffusion, destiné à générer ou éditer des images contenant du texte tout en transférant un style visuel depuis une référence. Ses modes documentés comprennent la référence interne (self-reference), la référence croisée (cross-reference) et la personnalisation à partir d'une référence non textuelle. Il est utile pour les expérimentations typographiques et les prototypes de direction artistique, mais l'orthographe générée, la composition et les droits doivent être vérifiés indépendamment.

## Ce que le flux de travail utilise {#what-the-workflow-uses}

La configuration publiée combine :

- une copie locale autorisée de `FLUX.1-Fill-dev` ;
- l'encodeur d'images SigLIP ;
- les poids du projet Calligrapher et les éléments de test ;
- une image d'entrée et un masque modifiable ;
- une instruction textuelle et une référence de style lorsque la tâche l'exige.

Le dépôt propose une démonstration Gradio de base avec un masque dessiné à la main, ainsi qu'une version acceptant un masque d'inpainting personnalisé. L'emplacement du masque et le rapport d'aspect influencent fortement le résultat : le modèle remplit la zone demandée et l'harmonise avec l'image environnante, sans se comporter comme un moteur de rendu de texte déterministe.

## Choisir délibérément le mode de référence {#choose-the-reference-mode-deliberately}

| Mode | Usage prévu | Points de contrôle |
|---|---|---|
| Référence interne (self-reference) | remplacer le texte en conservant le style de la même image | zone de texte source et préservation de l'arrière-plan local |
| Référence croisée (cross-reference) | appliquer une typographie issue d'une référence distincte | transfert de style sans copie involontaire de contenu |
| Référence non textuelle | dériver un traitement typographique à partir d'une référence visuelle | caractère reconnaissable du style et lisibilité du texte |
| Voie multilingue | utiliser la démonstration documentée assistée par TextFLUX | qualité des glyphes propre à chaque langue et orthographe |

La démonstration multilingue est facultative et repose sur une autre voie de modèle de base. Le projet signale que sa qualité peut varier ; ne réutilisez pas un résultat positif en anglais comme preuve pour un autre système d'écriture ou une autre langue.

## Résolution, texte et relecture humaine {#resolution-text-and-human-review}

Les auteurs entraînent le modèle à 512 pixels et recommandent 512 ou 768 pixels comme compromis pratique. Des résolutions très élevées peuvent introduire des erreurs d'orthographe. Considérez ce point comme une base de départ pour un banc d'essai, et non comme une exigence universelle de sortie.

Pour un élément destiné à la publication, évaluez séparément :

1. le texte exact et la ponctuation ;
2. l'ordre des glyphes, la prise en charge de la langue et du système d'écriture, ainsi que la lisibilité à la taille de livraison ;
3. la fidélité au style demandé, sans copie de contenu protégé ;
4. la limite du masque, l'arrière-plan, l'éclairage et les artefacts visuels ;
5. la source, le prompt, la révision du modèle, le masque et la sortie nécessaires pour reproduire une revue.

Utilisez un outil de mise en page et de typographie classique lorsque l'exigence porte sur un lettrage exact et déterministe. Une sortie de diffusion se traite au mieux comme une image candidate, susceptible de nécessiter une correction ou un montage.

## Accès et limites en matière de droits {#access-and-rights-boundary}

Le modèle FLUX de base requiert son propre accès et ses propres conditions, tandis que le projet Calligrapher et les éventuels poids auxiliaires ont leurs propres modalités de diffusion. Vérifiez chaque fiche de modèle et chaque licence en vigueur avant tout déploiement commercial, toute redistribution, ou toute utilisation d'une référence visuelle appartenant à un tiers. La disponibilité d'une démonstration n'accorde pas l'autorisation d'utiliser toutes les références ou toutes les sorties à toutes fins.

## Références {#references}

- [Dépôt officiel de Calligrapher](https://github.com/EzioBy/Calligrapher)
- [Article sur Calligrapher](https://arxiv.org/abs/2506.24123)
- [Poids et éléments de test de Calligrapher](https://huggingface.co/Calligrapher2025/Calligrapher)
