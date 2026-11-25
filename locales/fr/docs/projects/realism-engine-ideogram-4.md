---
title: "Realism_Engine_Ideogram_4 — LoRA Ideogram"
category: projects
date: 2026-06-11
tags: [ideogram-lora, project, realism-engine-ideogram-4]
aliases: ["Realism_Engine_Ideogram_4"]
level: 2
source_sha256: f3947eb20d075f351d0ce57ac77d32e7a13927f47267f960c59db44286ce8802
translation: machine
translated_at: '2026-10-24'
---
# Realism_Engine_Ideogram_4 — LoRA Ideogram {#realism_engine_ideogram_4-ideogram-lora}

**Ligne de développement :** `project:realism-engine-ideogram-4` · fil `ideogram-lora`  
**Dernier événement :** 2026-06-11 · 1 événement daté depuis le 2026-06-11 · **Recherche effectuée le :** 2026-09-07 · confiance : moyenne

## Description {#what-it-is}

Realism_Engine_Ideogram_4 est un ensemble de fichiers de poids LoRA et de workflows ComfyUI au format JSON, hébergé par un utilisateur, destiné à l'inférence locale d'Ideogram 4.

- comprend les fichiers safetensors V1, beta, V2, V3, V4 et V5 ;
- son workflow V2 applique le poids V2 via des chargeurs LoRA ne portant que sur le modèle (model-only) aux branches d'Ideogram 4.

Limite : le dépôt fait 21,5 Go, son README est vide, la licence de l'adaptateur est inconnue et aucun fournisseur d'inférence hébergé n'est proposé. Il faut le traiter comme un actif communautaire testé localement, et non comme une version d'Ideogram 4 documentée ou dont l'usage commercial est validé.

## Ligne de développement {#development-line}

- **2026-06-11 — Ressource de projet Hugging Face enregistrée pour Realism_Engine_Ideogram_4.** Le 2026-06-11, cette ligne de développement comprenait un lien vers une ressource Hugging Face pour Realism_Engine_Ideogram_4. Ce lien daté établit l'existence d'une ressource de projet identifiable, associée à la ligne à cette date. Les éléments disponibles n'établissent ni son statut de publication, ni son contenu, ni sa méthode d'entraînement, ni sa compatibilité.

## Modifications {#what-changed}

- 2026-06-09 — Le dépôt a été initialisé et les premiers actifs et workflows ont été téléversés.
- 2026-06-11 — Realism_Engine_Ideogram_V2.safetensors et rei4_v2_workflow.json ont été ajoutés.
- 2026-06-12 — Realism_Engine_Ideogram_V3.safetensors a été ajouté.
- 2026-06-14 — Realism_Engine_Ideogram_V4.safetensors a été ajouté.
- 2026-06-19 — Realism_Engine_Ideogram_V5.safetensors a été ajouté ; c'est le dernier poids nommé dans l'historique visible.

## Mode d'emploi {#how-to-use-this}

1. Consultez la page de l'adaptateur avant de télécharger : son README est vide et sa licence est inconnue, il n'est donc pas validé pour un usage commercial par sa propre documentation.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4>
2. Installez les composants ComfyUI d'Ideogram 4 dans les dossiers documentés diffusion_models, text_encoders et vae.
  — <https://huggingface.co/Comfy-Org/Ideogram-4>
3. Pour le parcours V2 documenté, téléchargez Realism_Engine_Ideogram_V2.safetensors, importez rei4_v2_workflow.json et faites pointer ses deux chargeurs LoRA ModelOnly vers ce poids exact.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json>
4. Épinglez ensemble le poids et le workflow testés : V3 à V5 sont des téléversements ultérieurs, mais le dépôt ne documente ni leurs modifications ni leur compatibilité avec le workflow.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/commits/main>

## Bonnes pratiques {#best-practices}

- Limitez le réglage de V2 à V2 : le workflow fourni indique que 0,50 à 0,90 est la plage optimale et déconseille de dépasser 0,90.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json>
- Utilisez à la fois les poids Ideogram conditionnels et inconditionnels pour le parcours de qualité visé : le responsable de Comfy-Org indique que l'omission de la branche inconditionnelle entraîne généralement une perte de qualité, tandis qu'un modèle inconditionnel en précision réduite peut diminuer la consommation de mémoire.
  — <https://huggingface.co/Comfy-Org/Ideogram-4/discussions/1>
- Utilisez les légendes JSON structurées d'Ideogram 4 pour les tests contrôlés et conservez la graine (seed) pour la reproductibilité.
  — <https://huggingface.co/docs/diffusers/main/api/pipelines/ideogram4>
- Suspendez l'usage commercial tant que les droits ne sont pas validés : le paquet de base ComfyUI relève de l'accord de non-commercialisation du modèle Ideogram.
  — <https://huggingface.co/Comfy-Org/Ideogram-4>

## Remplacé par {#superseded-by-this}

- Aucun remplacement documenté au 2026-09-07 : le téléversement V5 du 2026-06-19 n'indique pas qu'il remplace V1, beta, V2, V3 ou V4, qui restent disponibles.

## Points inconnus {#still-unknown}

- Les données d'entraînement, la méthode d'entraînement, l'usage prévu et la licence de l'adaptateur ne sont pas documentés.
- Aucune note de version, aucun benchmark ni aucune correspondance de workflow ne permettent d'établir lequel de V3 à V5 devrait remplacer V2.
- Aucune documentation de premier ordre en chinois et aucun retour indépendant exploitable en chinois sur l'exécution n'ont été trouvés.
- Aucune exécution locale indépendante n'a été réalisée ; les réglages V2 sont des recommandations de l'auteur du workflow, et non une recette vérifiée pour les poids ultérieurs.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4 | RazzzHF/Realism_Engine_Ideogram_4 — page du modèle | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/tree/main | RazzzHF/Realism_Engine_Ideogram_4 — arborescence actuelle des fichiers | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/commits/main | RazzzHF/Realism_Engine_Ideogram_4 — historique des commits, entrées datées du 2026-06-09 au 2026-06-19 | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json | rei4_v2_workflow.json — workflow V2, téléversé le 2026-06-11 | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Ideogram-4 | Comfy-Org/Ideogram-4 — paquet ComfyUI et licence | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Ideogram-4/discussions/1 | Discussion Comfy-Org Ideogram-4 — recommandations sur les modèles appariés et les échantillonneurs | 2026-09-07 |
| https://huggingface.co/docs/diffusers/main/api/pipelines/ideogram4 | Hugging Face Diffusers — documentation du pipeline Ideogram 4 | 2026-09-07 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:realism-engine-ideogram-4`, fil `ideogram-lora`, 1 événement daté du 2026-06-11 au 2026-06-11.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
