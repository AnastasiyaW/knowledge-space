---
title: "Les fondamentaux de Figma"
category: concepts
tags: [web-frontend, figma, design, ui-design]
level: 2
source_sha256: cf16b35e3bc6cef1cb41897029ededf62782b7b271569803f3cb494fc7ef9e8b
translation: machine
translated_at: '2026-10-24'
---
# Les fondamentaux de Figma {#figma-fundamentals}

Figma est un outil de design collaboratif pour l'UI/UX. Il fonctionne dans le navigateur ou en application de bureau (fonctionnalités identiques). La version gratuite suffit pour apprendre.

## Interface {#interface}

- **Panneau de gauche** : arborescence des calques (hiérarchie)
- **Centre** : canevas infini
- **Panneau de droite** : propriétés (dimensions, couleurs, effets)
- **Barre d'outils supérieure** : outils (frame, forme, plume, texte)

### Navigation {#navigation}
| Action | Raccourci |
|--------|-----------|
| Zoom | Ctrl+défilement |
| Déplacer | Espace+glisser |
| Tout afficher | Ctrl+1 |
| Zoom 100 % | Ctrl+0 |
| Zoom sur la sélection | Maj+1 |
| Afficher/masquer la grille | Ctrl+Maj+4 |

## Frames {#frames}

Conteneurs principaux définissant les limites des écrans. Équivalents aux artboards dans d'autres outils.

| Appareil | Largeur |
|----------|---------|
| Bureau | 1440px |
| Portable | 1280px |
| Tablette | 768px |
| Mobile | 375px |

- Les frames peuvent être imbriqués (frame dans une frame pour les sections)
- « Clip content » contrôle la visibilité du débordement
- Maintenez Ctrl en faisant glisser les bords d'une frame pour la redimensionner sans redimensionner ses enfants

## Système de grille {#grid-system}

Sélectionner la frame -> Layout Grid -> « + » -> Columns :
- **Count** : 12 (standard pour le web, se divise en 2/3/4/6)
- **Type** : Stretch (s'adapte à la frame)
- **Margin** : 80-120px (bureau)
- **Gutter** : 20-30px

Plusieurs grilles peuvent se superposer (colonnes + lignes + ligne de base).

## Calques et sélection {#layers-and-selection}

- En haut du panneau = au premier plan sur le canevas (ordre z)
- **Groupe** (Ctrl+G) : regroupement visuel, sans clip, sans dimensions propres
- **Frame** (Ctrl+Alt+G) : conteneur avec clip, dimensions propres, compatible avec AutoLayout
- Clic = niveau supérieur ; double-clic = entrer dans l'élément ; Ctrl+clic = sélection profonde

## Formes et opérations booléennes {#shapes-and-boolean-operations}

Intégrées : Rectangle (R), Ellipse (O), Ligne (L), Polygone, Étoile.
- Maintenir Maj = contraint (carré/cercle)
- Maintenir Alt = dessiner depuis le centre

**Opérations booléennes** (sélectionner 2 formes ou plus) : Union, Soustraction, Intersection, Exclusion. Non destructives par défaut ; Aplatir (Ctrl+E) les rend permanentes.

## Outil plume (P) {#pen-tool-p}

- Clic = point d'ancrage droit
- Clic+glisser = courbe (poignées de Bézier)
- Fermer le tracé en cliquant sur le premier point
- Double-clic sur le tracé pour modifier les points

## Texte {#text}

- Touche T, clic pour une largeur automatique, clic+glisser pour une largeur fixe
- Propriétés : police, graisse, taille, interligne, espacement des lettres

## Export {#export}

- Sélectionner l'élément -> section Export -> « + »
- **SVG** : icônes, logos (vectoriel, mise à l'échelle parfaite)
- **PNG** : graphismes avec transparence
- **JPG** : photographies
- Échelles : 1x, 2x, 3x pour écrans Retina

## Partage {#sharing}

- Bouton « Share » -> copier le lien
- Autorisations : « can view » ou « can edit »
- « Duplicate to your drafts » pour obtenir une copie modifiable

## Frames et groupes {#frames-vs-groups}

| Caractéristique | Frame | Groupe |
|-----------------|-------|--------|
| Découpe le contenu | Oui | Non |
| Dimensions propres | Oui | Non |
| AutoLayout | Oui | Non |
| Remplissage/contour | Oui | Non |
| Équivalent CSS | `<div>` | Regroupement visuel |

**Règle** : frames pour les conteneurs de mise en page (correspondent au HTML). Groupes pour un regroupement visuel temporaire.

## Pièges courants {#gotchas}

- **La grille est purement visuelle** : elle n'impose pas de mise en page ; les éléments doivent être positionnés manuellement
- **Confusion groupe/frame** : utiliser une frame lorsque vous avez besoin de découpe, de dimensionnement ou d'AutoLayout
- **Polices locales dans le navigateur** : nécessitent le plugin Figma Font Helper ; l'application de bureau charge les polices locales
- **Dupliquer vers les brouillons** : le propriétaire du lien d'origine contrôle l'accès ; toujours dupliquer pour un travail modifiable

## Voir aussi {#see-also}

- [[figma-layout-and-components]] - AutoLayout, contraintes, composants, variantes
- [[figma-design-workflow]] - Typographie, couleur, prototypage
- [[css-grid]] - Implémentation CSS des concepts de grille de Figma
