---
title: "Fizgig : fizgig-v6-0-1-refmod-support — Prise en charge de Fizgig V6 0 1 Refmod"
category: "projects"
date: 2026-10-17
tags: ["fizgig", "fizgig-v6-0-1-refmod-support", "project"]
aliases: ["Fizgig: fizgig-v6-0-1-refmod-support"]
level: 2
source_sha256: 6f9b45474dd30454c1c4092917adaa6f02f522c2bc2179577997bf952ea38b1d
translation: machine
translated_at: '2026-10-24'
---
# Fizgig : fizgig-v6-0-1-refmod-support — Prise en charge de Fizgig V6 0 1 Refmod {#fizgig-fizgig-v6-0-1-refmod-support-fizgig-v6-0-1-refmod-support}

**Ligne de développement :** project:fizgig · fil fizgig-v6-0-1-refmod-support  
**Dernier événement :** 2026-10-17 · 1 événement daté depuis le 2026-10-17 · **Recherche effectuée le :** 2026-10-19 · confiance : moyenne

## Présentation {#what-it-is}

Fizgig est une suite open source pour l'entraînement de LoRA et le fine-tuning de modèles sur des GPU locaux et dans le cloud. Elle entraîne des adaptateurs LoRA de personnages grâce à une méthode d'isolation, afin que chaque identité reste distincte lorsque plusieurs personnes figurent sur la même image.

- Entraînement multi-identités : plusieurs personnages dans un seul fichier d'adaptateur
- Differential Output Preservation : adaptée depuis les fondations d'AI-Toolkit
- Découplage des classes par tokens fusionnés : sépare les déclencheurs uniques des sujets des mots de classe de base
- Paires négatives synthétiques : protègent les inconnus en arrière-plan
- Prise en charge des modèles de base : compatible avec les architectures flow-matching et de diffusion

Elle nécessite au moins deux sujets distincts pendant l'entraînement. Dans ces conditions, les identités ne se contaminent pas mutuellement et aucune retouche manuelle par inpainting n'est nécessaire après la génération.

## Ligne de développement {#development-line}

- **2026-10-17 — Fizgig publie LoRA Isolation pour l'entraînement de LoRA multi-identités.** Le 2026-10-17, un développeur de Fizgig a annoncé LoRA Isolation. Cette fonctionnalité entraîne deux identités dans une même LoRA et maintient les autres personnes de l'image distinctes. Lors d'un test rapporté sur Krea 2, la propagation des visages d'inconnus est passée de 48 sur 50 à 0 sur 50. L'annonce renvoie vers les notes de version de la v8.4.0 et vers le dépôt GitHub.
  - Le développeur de Fizgig Peter Neill (@shootthesound) a décrit la construction de LoRA Isolation. Elle combine Differential Output Preservation (DOP), adaptée depuis Ostris AI-Toolkit, le découplage des classes par tokens fusionnés et les paires négatives synthétiques d'inconnus. Sur 50 générations de test réalisées sur Krea 2, il n'a constaté aucune fuite de visage d'inconnu. (2026-10-17) — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
  - La version v8.4.0 ajoute la configuration de dossiers multi-sujets à la carte Subjects de l'onglet Training. Elle automatise la fusion des tokens de déclencheur et de classe ainsi que la mise en place de l'entraînement par paires négatives. (2026-10-17) — <https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0>
  - Une vidéo explicative montre la création de deux dossiers de sujets distincts sur la carte Subjects. Elle formate les légendes avec des déclencheurs uniques et des descripteurs de classe, de sorte que les tokens fusionnés sont générés automatiquement. (2026-10-17) — <https://youtu.be/CNh4sN5vN_8>

## Évolutions {#what-changed}

Le travail est passé du simple fine-tuning de personnages à la séparation d'identités multi-sujets, fondée sur la préservation différentielle des sorties et l'entraînement par paires négatives. La fusion automatique des légendes en tokens est venue ensuite, accompagnée de la prise en charge de nouveaux backends d'images à poids ouverts.

## Mode d'emploi {#how-to-use-this}

1. Placez les jeux de données d'au moins deux identités distinctes dans des dossiers séparés sur la carte Subjects de l'onglet Training de Fizgig.
  — <https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0>
2. Commencez chaque légende par le token de déclencheur unique, suivi d'une virgule, puis du descripteur de classe (par exemple, « zwxem, a woman smiling »). Fizgig utilise cette structure pour construire les tokens fusionnés internes.
  — <https://github.com/shootthesound/Fizgig>
3. Activez LoRA Isolation dans la configuration d'entraînement. Elle combine Differential Output Preservation et l'appariement automatique d'images synthétiques d'inconnus.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
4. À l'inférence, utilisez le token de déclencheur fusionné et décrivez les autres sujets de la scène. Les frontières d'identité sont respectées et les visages ne fuient pas.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Bonnes pratiques {#best-practices}

- Entraînez au moins deux personnages distincts ensemble, même si vous n'en voulez qu'un seul. Cela oblige le réseau à séparer les tokens d'identité des tokens de classe humaine de base.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
- N'incluez pas le token de déclencheur lorsque vous décrivez des personnages d'arrière-plan ou des foules. Le modèle de base génère alors ses visages variés par défaut, sans fuite.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
- Lorsque vous associez des composites négatifs multi-personnes à l'entraînement, rédigez les légendes dans un ordre causal, avec les descripteurs des inconnus en premier.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Ce que disent les praticiens {#what-practitioners-say}

- Des praticiens rapportent que l'isolation multi-identités résout un problème courant : les LoRA de personnages qui écrasent les visages d'arrière-plan et les personnages secondaires dans les scènes de groupe. (2026-10-17)
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Remplacé par ce qui précède {#superseded-by-this}

- La recommandation précédente était l'entraînement de LoRA sur un sujet unique avec des tokens de classe génériques comme « man » ou « woman ». Dans les prompts multi-personnes, cela provoquait une forte fuite des visages sur les inconnus.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Points encore inconnus {#still-unknown}

- Le fil s'appelle fizgig-v6-0-1-refmod-support, mais l'événement et les notes de version que nous avons consultés concernent la v8.4.0. La date de publication et les détails de mise en œuvre de la prise en charge de refmod dans la version 6.0.1 n'ont pas pu être déterminés à partir des résultats de recherche disponibles.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/ | Fizgig LoRA Isolation : un nouveau procédé pour l'entraînement multi-identités sans fuite de visages | 2026-10-19 |
| https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0 | Release v8.4.0 : prise en charge de LoRA Isolation · shootthesound/Fizgig | 2026-10-19 |
| https://github.com/shootthesound/Fizgig | shootthesound/Fizgig : studio LoRA et fine-tuning | 2026-10-19 |
| https://youtu.be/CNh4sN5vN_8 | Fizgig LoRA Isolation : tutoriel et workflow multi-sujets | 2026-10-19 |
| https://youtu.be/8uW5NdL5b20 | Tutoriel d'entraînement LoRA Fizgig : prévenir la fuite de visages | 2026-10-19 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** project:fizgig, fil fizgig-v6-0-1-refmod-support, 1 événement daté du 2026-10-17 au 2026-10-17.
- **Remarque pratique :** utilisez les sections d'usage et de pratiques sourcées ci-dessus, avec leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus déterminent ce qui est obsolète.
