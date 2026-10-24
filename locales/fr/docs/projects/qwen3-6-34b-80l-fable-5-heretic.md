---
title: "Qwen3.6-34B-80L-Fable-5-Heretic"
category: projects
date: 2026-06-29
tags: [project, qwen3-6-34b-80l-fable-5-heretic]
aliases: ["Qwen3.6-34B-80L-Fable-5-Heretic"]
level: 2
source_sha256: fd7289b5b7966a4a09c8b06db2662a70ccb669307e0dbc1cd4b1cd8e9f3988e0
translation: machine
translated_at: '2026-10-24'
---
# Qwen3.6-34B-80L-Fable-5-Heretic {#qwen36-34b-80l-fable-5-heretic}

**Ligne de développement :** `project:qwen3-6-34b-80l-fable-5-heretic` · fil `qwen3-6-34b-80l-fable-5-heretic`  
**Dernier événement :** 2026-06-29 · 1 événement daté depuis le 2026-06-29 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Qwen3.6-34B-80L-Fable-5-Heretic est un dérivé en BF16 de Qwen3.6-27B, destiné à un auto-hébergement avec Transformers ou vLLM.

- 80 couches, environ 34 B de paramètres, et un contexte annoncé pouvant atteindre 256K.
- Entraînement QLoRA sur 4 665 traces CoT agentiques Fable-5.
- Poids MTP présents dans le dépôt pour le décodage spéculatif.

## Ligne de développement {#development-line}

- **2026-06-29 — Page du modèle Qwen3.6-34B-80L-Fable-5-Heretic enregistrée sur Hugging Face.** Un dérivé de Qwen3.6-27B étendu de 64 à 80 couches, annonçant environ 34 B de paramètres, des poids BF16, 4 665 traces QLoRA et 15 poids MTP. Nous n'avons trouvé aucune confirmation indépendante et datée de la publication le 2026-06-29.

## Ce qui a changé {#what-changed}

2026-06-29 — Nous avons enregistré le lien vers hiebo/Qwen3.6-34B-80L-Fable-5-Heretic. La fiche du modèle détaille cette étape : le dérivé de Qwen3.6-27B passe de 64 à 80 couches, annonce environ 34 B de paramètres, des poids BF16, 4 665 traces QLoRA et 15 poids MTP. Nous n'avons trouvé aucune confirmation indépendante et datée de la publication le 2026-06-29.

Après le 2026-06-29 — Nous n'avons trouvé aucune modification datée et vérifiée du modèle. Les miroirs sur Hugging Face redistribuent les mêmes artefacts plutôt qu'une nouvelle version.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-29, repérez l'entrée Qwen3.6-34B-80L-Fable-5-Heretic sur Hugging Face et vérifiez la fiche du modèle, les fichiers, la licence, la provenance et la compatibilité avant de l'adopter.

1. Chargez l'identifiant exact `hiebo/Qwen3.6-34B-80L-Fable-5-Heretic` avec Transformers en utilisant `device_map="auto"`, puis testez une requête courte avant de charger le contexte complet.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
2. Servez le modèle avec la commande vLLM indiquée dans la fiche du modèle, en BF16 et avec un `--max-model-len` explicite. Commencez par une limite basse, le temps de mesurer le cache KV et la mémoire GPU.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>

## Bonnes pratiques {#best-practices}

- Ne reprenez pas automatiquement les réglages du modèle de base : le dérivé personnalisé modifie le nombre de couches et ajoute des poids MTP. Vérifiez donc d'abord la compatibilité du chargeur, du tokenizer et du pipeline de génération avec un test de fumée local.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- Considérez le taux d'acceptation de 78 % et le débit 2× annoncés comme une hypothèse de la fiche du modèle : mesurez l'acceptation, la latence et la qualité sur votre propre jeu de tâches.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- Le modèle Qwen de base recommande une limite de génération élevée pour les tâches complexes ; traitez cela comme un réglage expérimental, et non comme une preuve de la qualité du dérivé.
  — <https://huggingface.co/Qwen/Qwen3.6-27B>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- La fiche du modèle est une affirmation de l'auteur, publiée depuis un dépôt personnel ; nous n'avons trouvé ni évaluations indépendantes, ni entraînements reproductibles, ni accélérations vérifiées.
- Les sources primaires ne donnent ni date exacte de publication ni dates de mise à jour ; nous ne pouvons donc pas confirmer que la publication a eu lieu le 2026-06-29.
- Le schéma ne comporte pas les champs `event_findings` et `new_events` ; nous avons consigné les constats pertinents dans `what_changed` et `unknowns`.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic | hiebo/Qwen3.6-34B-80L-Fable-5-Heretic — fiche du modèle | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.6-27B | Qwen/Qwen3.6-27B — fiche officielle du modèle | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:qwen3-6-34b-80l-fable-5-heretic`, fil `qwen3-6-34b-80l-fable-5-heretic`, 1 événement daté du 2026-06-29 au 2026-06-29.
- **Note pratique :** À partir du 2026-06-29, les praticiens peuvent repérer l'entrée Hugging Face de Qwen3.6-34B-80L-Fable-5-Heretic et doivent vérifier la fiche du modèle, les fichiers, la licence, la provenance et la compatibilité avant de l'adopter.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
