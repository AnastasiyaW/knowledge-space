---
title: "UEmbed"
category: projects
date: 2026-08-05
tags: [project, uembed]
aliases: ["UEmbed"]
level: 2
source_sha256: 0b0c651112c74bbff7033a302689e783a3f2f33ef58f1f869714077e4bca9789
translation: machine
translated_at: '2026-10-24'
---
# UEmbed {#uembed}

**Ligne de développement :** `project:uembed` · fil `uembed`  
**Dernier événement :** 2026-08-05 · 1 événement daté depuis le 2026-08-05 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

UEmbed est une famille d'embeddings décodeur uniquement, basée sur Qwen3.5, destinée aux équipes qui devraient autrement exploiter des systèmes de recherche denses et épars séparés.

- Représentations denses et éparses : produit des vecteurs denses normalisés et des vecteurs lexicaux épars en une seule passe avant causale.
- Encodage multimodal : encode du texte, des images, des vidéos et des entrées mixtes pour la recherche et la recherche de documents visuels.
- Famille de modèles : distribuée sous forme de UEmbed-2B, UEmbed-4B et UEmbed-9B ; l'inférence épars nécessite les fichiers annexes `sparse_info.json` et `sparse_weights.pt`.

## Ligne de développement {#development-line}

- **2026-08-05 — Le projet public UEmbed, son code et les ressources UEmbed-9B ont été liés.** Le 2026-08-05, nous avons lié la page officielle du projet, son dépôt source GitHub et la page du modèle UEmbed-9B sur Hugging Face. Les liens datés établissent une étape de disponibilité publique du projet et du modèle, mais n'établissent ni une version précise, ni un benchmark, ni une affirmation de capacité.

## Ce qui a changé {#what-changed}

- 2026-08-05 — La version initiale d'UEmbed a été documentée comme une série de points de contrôle multimodaux à décodeur uniquement de 2B, 4B et 9B, produisant des représentations denses et éparses.
- 2026-08-13 — L'inférence est passée à un chargement natif avec Transformers, sans `trust_remote_code` ni correctif de processeur, et a ajouté un backend vLLM pour le service des représentations denses et éparses.
- 2026-08-15 — Le projet a annoncé la première place sur MMEB-v3 pour les pistes texte et agent, et la deuxième place parmi les modèles ouverts sur MMEB-v2, derrière Qwen3-VL-Embedding.
- 2026-08-17 — Le support du fine-tuning supervisé avec ms-swift a été ajouté.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-05, nous pouvons évaluer UEmbed via sa documentation officielle de projet, examiner son dépôt source et localiser la ressource du modèle UEmbed-9B. Ne pas déduire de performances ou de compatibilités non vérifiées.

1. Installer un environnement d'exécution à jour compatible Qwen3.5/Qwen3-VL : `transformers>=5.4.0`, PyTorch, qwen-vl-utils, tokenizers, Hugging Face Hub, Pillow et NumPy.
  — <https://github.com/Alibaba-NLP/UEmbed>
2. Choisir le point de contrôle 2B, 4B ou 9B et télécharger l'intégralité de son dépôt ; conserver les fichiers annexes épars à côté des poids.
  — <https://github.com/Alibaba-NLP/UEmbed>
3. Charger `Qwen35Embedder`, transmettre des dictionnaires contenant du texte, des images, des vidéos ou des entrées mixtes, et fournir une instruction de tâche pour les requêtes de recherche lorsque c'est approprié.
  — <https://huggingface.co/Alibaba-NLP/UEmbed-9B>
4. Sélectionner `pooling="last.normal"` pour les vecteurs denses ou `pooling="splade.last"` pour les vecteurs lexicaux épars, puis envoyer la représentation choisie à l'index de recherche correspondant.
  — <https://github.com/Alibaba-NLP/UEmbed>

## Bonnes pratiques {#best-practices}

- Télécharger l'intégralité du dépôt du point de contrôle ; le mode épars ne fonctionnera pas sans les deux fichiers annexes épars.
  — <https://github.com/Alibaba-NLP/UEmbed>
- Instancier uniquement le mode de pooling dense ou épars requis par le chemin de recherche, plutôt que de supposer qu'un seul format de sortie convient aux deux index.
  — <https://github.com/Alibaba-NLP/UEmbed>
- Utiliser des instructions de requête spécifiques à la tâche pour la recherche, et n'utiliser BF16 avec FlashAttention 2 que lorsque le GPU et l'environnement d'exécution déployés le prennent en charge.
  — <https://github.com/Alibaba-NLP/UEmbed>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-13 — Les anciennes consignes d'inférence exigeant `trust_remote_code` ou un correctif de processeur sont obsolètes pour le chemin natif officiel avec Transformers.

## Toujours inconnu {#still-unknown}

- Aucun instantané immuable du dépôt ou de la fiche du modèle n'a été trouvé pour prouver de manière indépendante que les trois fichiers de points de contrôle étaient téléchargeables le 2026-08-05 ; l'article indique qu'ils ont été publiés, tandis que les liens datés incluent la fiche du modèle 9B.
- Les affirmations de benchmark du 2026-08-15 sont rapportées par le projet et n'ont pas été reproduites de manière indépendante.
- La fiche Hugging Face désigne le point de contrôle comme UEmbed-9B mais affiche « Model size 8B params » ; les documents officiels n'expliquent pas cette différence.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://alibaba-nlp.github.io/UEmbed/ | UEmbed: Unified Sparse and Dense Multimodal Embeddings | 2026-09-05 |
| https://github.com/Alibaba-NLP/UEmbed | Alibaba-NLP/UEmbed | 2026-09-05 |
| https://huggingface.co/Alibaba-NLP/UEmbed-9B | Alibaba-NLP/UEmbed-9B | 2026-09-05 |
| https://arxiv.org/abs/2608.02583 | UEmbed: Unified Sparse and Dense Multimodal Embeddings | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:uembed`, fil `uembed`, 1 événement daté du 2026-08-05 au 2026-08-05.
- **Note pratique :** À partir du 2026-08-05, nous pouvons évaluer UEmbed via sa documentation officielle de projet, examiner son dépôt source et localiser la ressource du modèle UEmbed-9B. Ne pas déduire de performances ou de compatibilités non vérifiées.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
