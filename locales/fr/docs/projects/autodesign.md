---
title: "AutoDesign"
category: projects

tags: [autodesign, autodesign-development, project, yaxin9luo/autodesign]
aliases: ["AutoDesign"]
level: 2
source_sha256: 2f3e360e6403e9bd73a35791d92fdec022fe6ceb0717af8011095fc1fb9583df
translation: machine
translated_at: '2026-10-24'
---
# AutoDesign {#autodesign}

**Ligne de développement :** `project:autodesign` · fil `autodesign-development`  
**Dernier événement :** - · 0 daté depuis - · **Consulté le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

AutoDesign est un projet sous licence MIT destiné aux chercheurs et aux équipes qui ont besoin de supports éditables à partir d'un PDF d'article, à l'aide d'un agent de codage et d'un fournisseur de LLM au choix.

- Génération : produit un poster HTML, des diapositives, une page d'accueil et une vidéo sous-titrée.
- Stockage local : enregistre localement les manifestes, les événements d'exécution, les candidats et les sorties.
- Optimisation du harnais : ajuste le harnais d'agent qui entoure le modèle plutôt que les poids du modèle de base.

L'évaluation formelle PosterBench ne couvre que les posters académiques ; les diapositives, les pages web et les vidéos restent des pistes pilotes.
Nous pouvons l'utiliser pour un flux de travail reproductible article-vers-poster ; testez les autres formats sur vos propres exemples.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-08-13 — L'article a présenté AutoDesign comme un méta-harnais pour le passage article-vers-poster et PosterBench : 100 articles dans le jeu principal et 10 dans le mini-jeu contrôlé ; les auteurs ont rapporté 78,32 points sur la piste principale et 253 appels d'outils sur 40 minutes d'exécution autonome.
- 2026-08-14 — Première publication publique du dépôt.
- 2026-08-16 — AutoDesign est devenu disponible en tant que projet public, avec code source et interface web ; le périmètre confirmé est la conversion de sources multimodales en posters académiques, et non un générateur d'interfaces général.
- 2026-08-17 — Des Agent Skills autonomes sont devenues disponibles pour les posters, les présentations, les pages web et les vidéos.
- 2026-08-18 — Le Poster Skill est passé à la v2 orientée agent : gestion directe des PDF, tentatives liées à une révision et contrôle QA du DOM en lecture seule.
- 2026-08-19 — L'interface web a ajouté des contrôles du canevas de poster : modèles, ratios d'aspect, dimensions exactes et préréglages académiques.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-16, les praticiens peuvent considérer le site web et le dépôt AutoDesign liés comme des sources à examiner, mais ne doivent pas en déduire une version, une capacité ou une évolution de flux de travail vérifiée à partir de cet enregistrement qui ne repose que sur un lien.

1. Installez Node.js 22+ et ffmpeg/ffprobe, lancez le lanceur local, et vérifiez l'environnement avec `autodesign doctor`.
  — <https://github.com/Yaxin9Luo/AutoDesign>
2. Pour une exécution depuis les sources, installez les dépendances avec `uv sync`, installez les navigateurs Playwright, et configurez l'environnement d'exécution vidéo ainsi que les dépendances du client web.
  — <https://github.com/Yaxin9Luo/AutoDesign>
3. Téléversez un PDF et lancez Paper All-in-One, ou appelez `python -m autodesign run` avec le PDF et le modèle de poster.
  — <https://github.com/Yaxin9Luo/AutoDesign>
4. Vérifiez `final/poster.html`, l'aperçu, le manifeste final et `run_events.jsonl` ; la simple présence de fichiers ne garantit pas la réussite de la validation.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Bonnes pratiques {#best-practices}

- Utilisez les posters de référence uniquement pour le système visuel : leur texte, logos, QR codes, tableaux et liens ne doivent pas devenir des éléments de preuve pour de nouveaux travaux.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Consultez le statut du terminal et les retours du manifeste plutôt que de considérer un fichier généré comme une preuve de réussite.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Utilisez `autodesign` et les variables `AUTODESIGN_*` pour toute nouvelle automatisation : les anciens noms `design_anything` et `DESIGN_ANYTHING_*` sont des alias obsolètes.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Remplacé par {#superseded-by-this}

- 2026-08-17 — L'usage monolithique, uniquement côté serveur, n'est plus obligatoire : des Agent Skills autonomes et installables sont disponibles.
- 2026-08-18 — Le Poster Skill précédent a été remplacé par la v2 orientée agent pour les flux de travail centrés sur les PDF et le contrôle QA du DOM.
- La documentation actuelle marque `design_anything`, `design-anything`, `designanything` et `DESIGN_ANYTHING_*` comme alias de compatibilité obsolètes ; les nouvelles configurations utilisent `autodesign` et `AUTODESIGN_*`.

## Toujours inconnu {#still-unknown}

- Les résultats de benchmark et les scores d'évaluation humaine publiés par les auteurs n'ont pas été reproduits de manière indépendante dans cette revue.
- La stabilité de la démo hébergée et la maturité en production des intégrations fournies restent non vérifiées.
- L'événement du 2026-08-16 n'a pas de source primaire datée distincte ; les détails reposent sur l'article du 2026-08-13 et la publication publique du 2026-08-14.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/Yaxin9Luo/AutoDesign | Yaxin9Luo/AutoDesign | 2026-09-05 |
| https://arxiv.org/abs/2608.13560 | AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design | 2026-09-05 |

## Agent brief {#agent-brief}

- **Sujet :** `project:autodesign`, fil `autodesign-development`, 0 événement daté - → -.
- **Note pratique :** Au 2026-08-16, les praticiens peuvent considérer le site web et le dépôt AutoDesign liés comme des sources à examiner, mais ne doivent pas en déduire une version, une capacité ou une évolution de flux de travail vérifiée à partir de cet enregistrement qui ne repose que sur un lien.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
