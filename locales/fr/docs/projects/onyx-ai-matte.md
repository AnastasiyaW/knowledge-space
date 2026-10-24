---
title: "ONYX Ai Matte"
category: projects
date: 2026-03-10
tags: [onyx-ai-matte, project]
aliases: ["ONYX Ai Matte"]
level: 2
source_sha256: 08536999395bc015895c0b8c358e3283104c5cd05c6b46857d5d0e2ae9ca06c2
translation: machine
translated_at: '2026-10-24'
---
# ONYX Ai Matte {#onyx-ai-matte}

**Ligne de développement :** `project:onyx-ai-matte` · fil `onyx-ai-matte`  
**Dernier événement :** 2026-03-10 · 1 événement daté depuis le 2026-03-10 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ONYX Ai Matte est un outil OFX local de rotoscopie et d'extraction d'alpha pour Nuke, DaVinci Resolve, Fusion, Flame et Natron. Fonctionnalités : prompts box/point/text/mask, suivi jusqu'à 16 objets, affinage du bord avec VitMatte/MeMatte, export des masques cuits. Limites : Windows requiert une carte NVIDIA RTX série 20 ou supérieure et 6 Go de VRAM ; macOS requiert Apple Silicon et macOS 15 ou supérieur ; le résultat couvre généralement 60 à 80 % du matte, la finition étant laissée au compositeur. Verdict : une alternative pratique à Magic Mask pour un pipeline OFX local, mais qui ne remplace pas le contrôle qualité du masque final.

## Ligne de développement {#development-line}

- **2026-03-10 — Les ressources du projet ONYX Ai Matte ont été liées.** Le 2026-03-10, la ligne de développement ONYX Ai Matte a été associée à son site de projet et à un lien de ressource Hugging Face. Ces liens datés établissent une référence de projet accessible de l'extérieur, mais n'établissent pas une version, un modèle, une capacité ou une modification précise sans le billet original ou une recherche complémentaire.

## Ce qui a changé {#what-changed}

2026-03-10 — le lien de l'événement renvoyait au site officiel d'ONYX ; aucune confirmation datée indépendante d'une modification précise survenue ce jour-là n'a été trouvée. 2026-03-24 — publication d'ONYX Ai Matte v2.5 : cinq modes de fonctionnement, suivi automatique, prompts text/mask et segmentation multi-objets. 2026-07-17 — la v3.1.0 a ajouté la gestion de l'espace couleur d'entrée pour ACES/OCIO, l'activation des proxys et des corrections de stabilité. 2026-08-03 — la v3.2.0 a ajouté la prise en charge d'Apple Silicon/macOS et de Flame. 2026-08-12 — la v3.3.0 a porté le cache des masques suivis à environ 12 000 images en 6K. 2026-08-31 — la v3.4.0 a ajouté des canaux séparés pour le object mask et la unknown zone dans Refiner Direct.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-10, les praticiens doivent traiter ONYX Ai Matte comme une ligne projet/ressource liée séparément et vérifier la disponibilité actuelle ainsi que les conditions d'usage sur le site officiel et la ressource Hugging Face avant toute adoption.

1. Fermez l'hôte, installez le paquet à jour, puis redémarrez l'hôte et ajoutez l'effet OFX ONYX Ai Matte v3 ; la période d'essai de 7 jours démarre à l'ajout du premier nœud.
  — <https://onyxofx.com/docs/>
2. Connectez le clip à Source, sélectionnez l'objet avec un prompt box/point/text/mask sur l'image de départ, puis lancez une lecture en un seul passage pour un suivi séquentiel.
  — <https://onyxofx.com/docs/>
3. Vérifiez le masque, ajustez le bord avec VitMatte/MeMatte et, si nécessaire, cuisez la séquence PNG/EXR dans un dossier séparé.
  — <https://onyxofx.com/docs/>

## Bonnes pratiques {#best-practices}

- Désactivez Loop pour le suivi ; pour une passe complète depuis l'image de départ dans les deux sens, utilisez Bounce/Ping-Pong.
  — <https://onyxofx.com/docs/>
- Pour un suivi instable ou coupé lors de mouvements rapides, augmentez Crop Padding ou désactivez Crop Mode.
  — <https://onyxofx.com/docs/>
- N'acceptez pas le matte IA sans vérification : l'outil est conçu pour fournir environ 60 à 80 % du résultat, la finition revenant au compositeur.
  — <https://onyxofx.com/docs/>

## Remplacé par {#superseded-by-this}

- 2026-08-31 — Le Refiner Direct Mode a été remplacé par l'affectation de object mask et unknown zone à des canaux d'entrée distincts dans la v3.4.0.
- 2026-08-12 — L'ancien petit cache de suivi a été remplacé par le cache compressé de la v3.3.0.
- 2026-08-03 — L'état antérieur à la prise en charge macOS/Flame est obsolète depuis la v3.2.0.

## Points inconnus {#still-unknown}

- Les notes de version officielles ne contiennent aucune entrée datée du 2026-03-10 ; il est donc impossible d'attribuer de façon fiable à ce jour une version ou une fonctionnalité précise.
- Le schéma JSON fourni ne comporte pas de champs event_findings ni new_events ; les dates supplémentaires confirmées figurent dans what_changed, et le rattachement à l'événement du 2026-03-10 est conservé comme incertitude.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://onyxofx.com/ | ONYX Ai Matte — AI Roto for Nuke & Resolve. No Subscription | 2026-09-05 |
| https://onyxofx.com/docs/ | ONYX Ai Matte Documentation \| Install and Parameters | 2026-09-05 |
| https://onyxofx.com/release-notes/ | Release Notes — ONYX Ai Matte | 2026-09-05 |
| https://www.cgchannel.com/2026/03/onyx-ai-matte-automatically-generates-masks-from-video-footage/ | ONYX Ai Matte automatically generates masks from video | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:onyx-ai-matte`, fil `onyx-ai-matte`, 1 événement daté du 2026-03-10 au 2026-03-10.
- **Note pratique :** À partir du 2026-03-10, les praticiens doivent traiter ONYX Ai Matte comme une ligne projet/ressource liée séparément et vérifier la disponibilité actuelle ainsi que les conditions d'usage sur le site officiel et la ressource Hugging Face avant toute adoption.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
