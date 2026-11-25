---
title: "ToonComposer"
category: projects
date: 2025-08-19
tags: [project, tooncomposer, tooncomposer-public-availability]
aliases: ["ToonComposer"]
level: 2
source_sha256: 76c6a34798916fa6367bb5f5f15d9488e47b2b73b4df3c082fc88a74bc4b8fab
translation: machine
translated_at: '2026-10-24'
---
# ToonComposer {#tooncomposer}

**Ligne de développement :** `project:tooncomposer` · fil `tooncomposer-public-availability`  
**Dernier événement :** 2025-08-19 · 2 événements datés depuis 2025-08-16 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

ToonComposer est un modèle de post-keyframing de TencentARC, construit sur Wan2.1-I2V-14B-480P. Il prend en entrée une image de référence colorée, un prompt textuel et un ou plusieurs croquis à des images choisies. Il génère une séquence de dessin animé, prend en charge des masques de mouvement par région et propose des points de contrôle en 480p ou 608p. Une génération de 61 images en 480p nécessite environ 57 Go de VRAM. Nous l'utilisons pour des plans courts de dessin animé contrôlés, lorsque des indications de mouvement sous forme de croquis épars dessinés par des artistes sont disponibles. Nous ne l'utilisons pas comme générateur vidéo général et léger.

## Ligne de développement {#development-line}

- **2025-08-16 — La page projet publique et les ressources source de ToonComposer ont été recensées.** Le 2025-08-16, ToonComposer a obtenu une page projet publique et le dépôt GitHub de TencentARC. Ces éléments établissent à ce moment de la chronologie la présentation publique du projet et son code source. Ils n'établissent pas de version, de capacité ou de date de publication originale précises.
- **2025-08-19 — Un Space Hugging Face hébergeant ToonComposer a été recensé.** Le 2025-08-19, ToonComposer a obtenu le Space Hugging Face TencentARC/ToonComposer. Cela ajoute une interface publique hébergée à la présentation publique du projet et à son code source. Ces liens n'établissent pas les fonctions exactes du Space, sa révision de modèle ni de nouvelles capacités.

## Évolutions {#what-changed}

- 2025-08-14 — L'article a présenté ToonComposer, l'injection de croquis épars, l'adaptation spatiale de bas rang (spatial low-rank adaptation) et PKBench, avant les annonces de publication listées.
- 2025-08-16 — TencentARC a publié le projet et le code, établissant un flux de travail unifié de post-keyframing au lieu d'une chaîne séparée d'interpolation puis de colorisation.
- 2025-08-19 — Le Space Hugging Face officiel a rendu le flux de travail disponible sous forme de démonstration hébergée, aux côtés du modèle publié.
- 2026-03-24 — L'auteur du projet a signalé que la démonstration Hugging Face officielle avait redémarré après une panne temporaire du Space.

## Mode d'emploi {#how-to-use-this}

Au 2025-08-19, nous recherchons ToonComposer via sa page projet publique, son dépôt source et son Space Hugging Face hébergé. Nous vérifions directement la capacité exacte et la révision, car cette ligne n'a pas fait l'objet de recherches.

1. Clonez le dépôt officiel, créez un environnement Conda Python 3.10 et installez ses dépendances épinglées.
  — <https://github.com/TencentARC/ToonComposer>
2. Exécutez `python app.py` ; il utilise d'abord les poids en cache, sinon il récupère le modèle de fondation Wan2.1 et le point de contrôle ToonComposer.
  — <https://github.com/TencentARC/ToonComposer>
3. Dans l'interface Gradio, définissez le prompt, le nombre d'images de sortie et la résolution ; fournissez une image clé colorée et des croquis épars aux images que vous souhaitez contrôler.
  — <https://github.com/TencentARC/ToonComposer>
4. Utilisez le Space officiel hébergé lorsque la mémoire GPU locale est insuffisante.
  — <https://huggingface.co/spaces/TencentARC/ToonComposer>

## Bonnes pratiques {#best-practices}

- Commencez avec une image de référence colorée et un croquis, puis ajoutez des croquis uniquement là où un contrôle de mouvement supplémentaire est nécessaire.
  — <https://arxiv.org/abs/2508.10881>
- Utilisez le masque de croquis pour les régions où vous souhaitez un mouvement guidé par le contexte, plutôt que de laisser ces régions non marquées.
  — <https://github.com/TencentARC/ToonComposer>
- Pour faire varier la sortie ou en cas d'échec, ajustez la graine, le nombre d'étapes d'échantillonnage, l'échelle CFG, l'échelle du résiduel sensible à la position, ainsi que les entrées de croquis ou de masque.
  — <https://github.com/TencentARC/ToonComposer>
- Considérez le Space officiel comme solution de repli pour la charge locale documentée de 57 Go de VRAM en 480p/61 images ; ne supposez pas qu'un déploiement chez un fournisseur d'inférence existe.
  — <https://huggingface.co/TencentARC/ToonComposer>

## Remplacé par la présente {#superseded-by-this}

- 2026-03-24 — La consigne selon laquelle la démonstration Hugging Face officielle était indisponible est obsolète : l'auteur du projet a signalé qu'elle fonctionnait après un redémarrage.

## Points toujours inconnus {#still-unknown}

- Les champs demandés event_findings et new_events ne figuraient pas dans le schéma ; leurs preuves sont conservées dans what_changed.
- Aucun journal des modifications ni historique de publication daté de première main documentant des évolutions du modèle après la version d'août 2025 n'a été trouvé ; le redémarrage de la démonstration en mars 2026 constitue un changement de disponibilité, et non une preuve d'une nouvelle version du modèle.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/TencentARC/ToonComposer | GitHub — TencentARC/ToonComposer | 2026-09-05 |
| https://huggingface.co/spaces/TencentARC/ToonComposer | Space Hugging Face — TencentARC/ToonComposer | 2026-09-05 |
| https://huggingface.co/TencentARC/ToonComposer | Fiche de modèle Hugging Face — TencentARC/ToonComposer | 2026-09-05 |
| https://arxiv.org/abs/2508.10881 | ToonComposer: Streamlining Cartoon Production with Generative Post-Keyframing | 2026-09-05 |
| https://huggingface.co/TencentARC/ToonComposer/discussions/2 | Discussion ToonComposer : Availability? | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:tooncomposer`, fil `tooncomposer-public-availability`, 2 événements datés du 2025-08-16 au 2025-08-19.
- **Note pratique :** Au 2025-08-19, les praticiens doivent rechercher ToonComposer via sa page projet publique, son dépôt source et son Space Hugging Face hébergé, tout en vérifiant directement la capacité exacte et la révision, car cette ligne n'a pas fait l'objet de recherches.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
