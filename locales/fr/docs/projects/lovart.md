---
title: "Lovart"
category: projects

tags: [lovart, lovart-development, project]
aliases: ["Lovart", "Lovart Vectorize"]
level: 3
source_sha256: b625187ad53600627dfcff06028fa0cec00e17dda710a3929163fccd457ab94e
translation: machine
translated_at: '2026-10-24'
---
# Lovart {#lovart}

**Ligne de développement :** `project:lovart` · fil `lovart-development`  
**Dernier événement :** - · 0 événement daté depuis · **Consulté le :** 2026-09-05 · confiance : medium

## Présentation {#what-it-is}

Lovart est un espace de travail web permettant de générer des images de marque, des vidéos et des graphiques, via un agent ou par sélection directe d'un modèle.

- Canvas : organise et modifie les ressources sur un espace de travail ouvert.
- Brand Kit : gère les logos, couleurs, polices et chartes graphiques, ou analyse des PDF de brand book.
- Édition ponctuelle : ajuste directement des éléments précis.
- Génération d'images et de vidéos : produit des médias via un agent ou par sélection directe d'un modèle.
- Vectorisation SVG : convertit des images matricielles PNG et JPG en SVG.
- Export PSD : exporte le contenu du canvas vers des fichiers PSD multicouches.

Canvas génère des fichiers SVG mais ne permet pas de modifier les tracés vectoriels ; l'édition des tracés nécessite Illustrator, Figma ou un autre éditeur vectoriel.
Il sert de couche de travail au-dessus de plusieurs modèles génératifs, et non de remplacement d'un éditeur de tracés vectoriels.

## Ligne de développement {#development-line}

- L'événement daté n'est pas encore documenté ; les informations connues figurent dans les sections ci-dessous.

## Évolutions {#what-changed}

- 2025-05-13 : Lovart fonctionnait en bêta fermée ; un message principal ultérieur confirme que la bêta a commencé en mai 2025.
- 2025-06-05 : ajout de l'intégration de Flux Kontext pour modifier des images par texte et par références.
- 2025-06-11 : ajout de Veo 3 pour la génération de vidéos.
- 2025-06-18 : ajout de Kling 2.1.
- 2025-07-23 : ajout de Chat with Canvas, permettant d'utiliser des commentaires sur une image ou une zone comme entrée de l'agent.
- 2025-07-28 : sortie de la bêta pour une publication publique avec ChatCanvas ; l'entreprise indique plus de 300 000 utilisateurs de la première heure.
- 2026-02-19 : ajout de Vectorize pour convertir des PNG et JPG en SVG.
- 2026-03-05 : ajout de préréglages de recadrage pour les plateformes sociales.
- 2026-03-09 : aucune information primaire vérifiée sur une version précise n'a été trouvée dans les liens accessibles.
- 2026-03-21 : ajout de la personnalisation de la barre d'outils.
- 2026-03-23 : ajout du déplacement des objets sélectionnés à l'intérieur d'une image, avec remplissage génératif pour la zone libérée.
- 2026-03-27 : aucune livraison autonome vérifiée pour cette date ; les évolutions confirmées les plus proches sont Move Object le 23 mars et l'export PSD le 29 mars.
- 2026-03-29 : ajout de l'export du contenu de Canvas au format PSD multicouche.
- État au 2026-09-05 : Lovart affiche des intégrations pour GPT Image 2, Seedance 2.0, Nano Banana Pro, Kling 3.0, Seedream 5, Veo 3.1, Midjourney, Luma Uni-1 et Flux 2 Pro ; la disponibilité et les réglages dépendent du modèle sélectionné et de l'offre souscrite.

## Mode d'emploi {#how-to-use-this}

Aucune action pratique n'est proposée : pour les dates 2025-05-13, 2026-03-09 et 2026-03-27, les liens datés seuls n'établissent pas de modification vérifiée du développement produit de Lovart.

1. Créez un nouveau projet ou lancez Quickstart ; décrivez la tâche en texte simple et vérifiez le résultat sur Canvas.
  — <https://www.lovart.ai/docs/getting-started/design-your-first-project>
2. Configurez d'abord le Brand Kit pour une marque existante : importez les logos, couleurs, polices et chartes, ou laissez le service analyser un PDF de brand book ; appliquez ensuite le kit au projet.
  — <https://www.lovart.ai/docs/getting-started/things-you-should-set-up-first>
3. Ouvrez Models pour une génération guidée : Auto sélectionne un modèle, Auto Off définit des préférences, et une mention @ fixe un modèle précis pour une seule invite.
  — <https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models>
4. Pour le SVG, sélectionnez un PNG ou JPG sur Canvas, choisissez Vectorize, téléchargez le SVG et ouvrez-le dans un éditeur vectoriel externe si nécessaire.
  — <https://www.lovart.ai/docs/edit-your-design/ai-transformation>
5. Exportez un objet unique ou plusieurs objets sélectionnés ; l'export par lot prend en charge le PSD.
  — <https://www.lovart.ai/docs/getting-started/design-your-first-project>

## Bonnes pratiques {#best-practices}

- Constituez le Brand Kit avant les premières générations pour une marque existante, et tenez un kit distinct pour chaque marque.
  — <https://www.lovart.ai/docs/getting-started/things-you-should-set-up-first>
- Considérez les préférences de modèle en sélection automatique comme des préférences et non comme des verrouillages stricts ; fixez un modèle précis avec @ si nécessaire.
  — <https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models>
- Supprimez les arrière-plans avant Vectorize pour que les logos et icônes se tracent proprement.
  — <https://www.lovart.ai/docs/edit-your-design/ai-transformation>
- Détourez précisément les objets pour les modifications Move Object : des sélections trop larges nuisent à la reconnaissance dans les scènes complexes.
  — <https://www.lovart.ai/docs/edit-your-design/ai-transformation>

## Remplacé par {#superseded-by-this}

- 2025-05-13 : les consignes sur l'accès à la bêta fermée ont été remplacées par le lancement public du 2025-07-28.
- Avant 2026-02-19 : l'hypothèse selon laquelle Lovart ne convertit pas le matriciel en SVG a été remplacée par Vectorize.
- 2026-02-19 : l'hypothèse selon laquelle Vectorize remplace un éditeur vectoriel n'est pas étayée ; Canvas ne permet pas encore de modifier les tracés SVG.

## Points inconnus {#still-unknown}

- Les dates 2026-03-09 et 2026-03-27 ne disposent pas de descriptions vérifiées de versions précises dans les liens accessibles ; il est impossible de les rattacher de façon fiable à Vectorize ou aux évolutions voisines.
- Les pages marketing de Lovart annoncent des capacités et un nombre d'utilisateurs ; aucun audit indépendant n'a vérifié la qualité, les limites de crédits ni la disponibilité des modèles.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.lovart.ai/ | Lovart – Premier agent de design IA au monde | 2026-09-05 |
| https://www.lovart.ai/changelog | Lovart AI Product Changelog & Latest Updates | 2026-09-05 |
| https://www.lovart.ai/news/lovart-design-agent-public-launch-chatcanvas | Lovart sort de la bêta et lance son agent de design public avec ChatCanvas | 2026-09-05 |
| https://www.lovart.ai/docs/getting-started/design-your-first-project | Design Your First Project | 2026-09-05 |
| https://www.lovart.ai/docs/getting-started/things-you-should-set-up-first | Things You Should Set Up First | 2026-09-05 |
| https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models | Selecting AI Models | 2026-09-05 |
| https://www.lovart.ai/docs/edit-your-design/ai-transformation | AI Transformation | 2026-09-05 |

## Brief d'agent {#agent-brief}

- **Sujet :** `project:lovart`, fil `lovart-development`, 0 événement daté - → -.
- **Note pratique :** Aucune action pratique n'est proposée : pour les dates 2025-05-13, 2026-03-09 et 2026-03-27, les liens datés seuls n'établissent pas de modification vérifiée du développement produit de Lovart.
- **Confiance :** medium. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
