---
title: "LocateAnything — Publication du modèle"
category: projects
date: 2026-05-29
tags: [locateanything, model-release, project]
aliases: ["LocateAnything"]
level: 2
source_sha256: 13716cd93545597bbd693144635af28a8b822c3b2717b86df01e60a9a3c50880
translation: machine
translated_at: '2026-10-24'
---
# LocateAnything — Publication du modèle {#locateanything-model-release}

**Ligne de développement :** `project:locateanything` · fil `model-release`  
**Dernier événement :** 2026-05-29 · 1 événement daté depuis le 2026-05-29 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

LocateAnything est un modèle de recherche NVIDIA de 3B paramètres, issu de la famille Eagle, dédié au visual grounding : détection d'objets, grounding par expression référentielle, GUI grounding, OCR/localisation de texte, layout grounding et pointing. Il prédit une bounding box complète en parallèle, plutôt que des coordonnées token par token ; le débit annoncé est de 12.7 boxes/s sur un seul H100 en Hybrid Mode. Verdict : adapté à la R&D et à l'intégration locale de tâches de localisation, mais les poids publiés sont soumis à une licence non commerciale.

## Ligne de développement {#development-line}

- **2026-05-29 — NVIDIA a publié les ressources LocateAnything et la page du modèle LocateAnything-3B.** Le 2026-05-29, la page de recherche LocateAnything de NVIDIA et la page du modèle NVIDIA LocateAnything-3B sur Hugging Face associée ont été partagées. Cela marque une étape de mise à disposition publique du projet et du modèle dans l'historique de développement de LocateAnything.

## Ce qui a changé {#what-changed}

2026-05-29 — LocateAnything est devenu disponible sous la forme LocateAnything-3B ; les sources primaires précisent que la publication du code, des poids, de la démo, de la page web et du rapport est datée du 2026-05-26, et non du 29 mai. Le modèle combine MoonViT-SO-400M, Qwen2.5-3B-Instruct et un projecteur MLP ; le Parallel Box Decoding prédit x1,y1,x2,y2 en un seul bloc. Données d'entraînement : 12M d'images, plus de 138M de requêtes et 785M de boîtes. 2026-06 — Eagle a ajouté l'inférence par lots basée sur FlashAttention pour A100/RTX 4090 ainsi qu'un script LoRA pour le fine-tuning en visual-prompt ; cependant, le checkpoint public de base ne prend toujours pas en charge l'inférence en visual-prompt sans fine-tuning.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-05-29, les praticiens peuvent évaluer LocateAnything via la ressource de recherche publique de NVIDIA et la page du modèle LocateAnything-3B associée, avant de le retenir pour des flux de travail de localisation d'objets.

1. Clonez NVlabs/Eagle, rendez-vous dans Embodied et installez le paquet avec la commande pip install -e .
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
2. Chargez nvidia/LocateAnything-3B via LocateAnythingWorker, transmettez une image RGB et appelez detect, ground_multi, detect_text, ground_gui ou point.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
3. Analysez la réponse : les coordonnées des boîtes sont dans la plage 0–1000, il faut donc les mettre à l'échelle de la largeur et de la hauteur de l'image source.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
4. Pour le traitement par lots, téléchargez le dépôt du modèle et lancez batch_infer.py avec --attn la_flash et une taille de lot adaptée.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>

## Bonnes pratiques {#best-practices}

- Pour une exécution standard, utilisez le Hybrid Mode : le Fast Mode est appliqué par défaut, et les blocs problématiques sont retraités en Slow Mode.
  — <https://research.nvidia.com/labs/lpr/locate-anything/>
- Pour obtenir une réponse complète, fixez max_new_tokens=8192 ; la fiche du modèle recommande le Hybrid Mode comme compromis entre vitesse et précision.
  — <https://huggingface.co/nvidia/LocateAnything-3B>
- Sur A100 et autres GPU autres que Hopper/Blackwell, utilisez le runtime par lots la_flash plutôt que le SDPA dense ; l'exemple publié sur A100 fait passer la mémoire réservée maximale de 35.12 GB à 11.71 GB.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
- Ne comptez pas sur l'inférence en visual-prompt avec le nvidia/LocateAnything-3B d'origine : cette tâche nécessite un fine-tuning propre, à partir du code publié.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points non résolus {#still-unknown}

- Les sources primaires datent la publication initiale du 2026-05-26, alors que l'événement est enregistré au 2026-05-29 ; les éléments disponibles n'expliquent pas cet écart de trois jours.
- Pour les mises à jour de juin, Eagle ne publie que le mois et non les jours exacts ; elles ne peuvent donc pas être rattachées de façon fiable à des événements datés précis.
- Aucune confirmation primaire n'a été trouvée indiquant que les poids publics ont obtenu une autorisation commerciale ; la fiche du modèle continue de les limiter à la recherche académique et non commerciale.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://research.nvidia.com/labs/lpr/locate-anything/ | LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding | 2026-09-05 |
| https://huggingface.co/nvidia/LocateAnything-3B | nvidia/LocateAnything-3B model card | 2026-09-05 |
| https://github.com/NVlabs/EAGLE | NVlabs/Eagle repository | 2026-09-05 |
| https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md | LocateAnything implementation and usage guide | 2026-09-05 |
| https://arxiv.org/abs/2605.27365 | LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:locateanything`, fil `model-release`, 1 événement daté du 2026-05-29 au 2026-05-29.
- **Note pratique :** À partir du 2026-05-29, les praticiens peuvent évaluer LocateAnything via la ressource de recherche publique de NVIDIA et la page du modèle LocateAnything-3B associée, avant de le retenir pour des flux de travail de localisation d'objets.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
