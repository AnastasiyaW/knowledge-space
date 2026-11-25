---
title: "Mise en page et composants Figma"
category: concepts
tags: [web-frontend, figma, autolayout, components, variants, design-system]
level: 3
source_sha256: ecb01c0f84a704918373d8ae62767efb5711365fa82b21df9a54b5ebaa892d34
translation: machine
translated_at: '2026-10-24'
---
# Mise en page et composants Figma {#figma-layout-and-components}

AutoLayout (l'équivalent de Flexbox dans Figma), les contraintes de positionnement et les composants pour les éléments de design réutilisables.

## AutoLayout {#autolayout}

Fait se comporter les frames comme des conteneurs flex : les enfants s'agencent, s'espacent et se redimensionnent automatiquement.

**Créer** : sélectionner les éléments -> Maj+A (ou le « + » à côté d'Auto Layout dans le panneau de droite).

### Propriétés {#properties}
- **Direction** : Horizontal (row), Vertical (column), Wrap
- **Gap** : espace entre les enfants
- **Padding** : espacement interne (individuel ou uniforme)
- **Alignement** : grille à 9 points (du haut-gauche au bas-droite)

### Comportement de redimensionnement {#resizing-behavior}

| Mode | Comportement | Équivalent CSS |
|------|--------------|----------------|
| Fixed | Taille définie | `width: 200px` |
| Hug contents | Se réduit à la taille du contenu | `width: fit-content` |
| Fill container | S'étend pour remplir le conteneur | `flex: 1` / `width: 100%` |

### Modes d'espacement {#spacing-modes}
- **Packed** : les éléments se regroupent avec un gap défini (comme `gap` en CSS)
- **Space between** : les éléments se répartissent (comme `justify-content: space-between`)

### AutoLayout imbriqué (mises en page réelles) {#nested-autolayout-real-layouts}
```text
Page (vertical)
  ├── Header (horizontal)
  │     ├── Logo (fixed)
  │     ├── Nav (horizontal, gap: 24)
  │     └── CTA (fixed)
  ├── Hero (vertical, fill)
  └── Cards (horizontal, wrap)
        ├── Card 1 (vertical, fill)
        └── Card 2 (vertical, fill)
```

Reproduit la structure HTML/CSS pour faciliter la transmission aux développeurs.

### Contraintes min/max {#minmax-constraints}
Propriétés de l'élément -> « ... » sous W/H pour les largeur/hauteur min/max. Essentiel pour le comportement responsive.

### Positionnement absolu {#absolute-positioning}
Activer « Absolute position » sur un enfant pour le sortir du flux d'AutoLayout. Équivalent de `position: absolute` à l'intérieur d'un `position: relative`.

### Astuces {#tips}
1. Construire de l'intérieur vers l'extérieur : les plus petits éléments d'abord, puis les envelopper dans des AutoLayouts plus grands
2. Fill pour les zones flexibles, Hug pour un dimensionnement naturel (boutons, tags)
3. Grille de 8px : espacements de 8, 16, 24, 32, 40, 48px
4. Nommer les frames de manière descriptive (les développeurs les lisent)

## Contraintes {#constraints}

Pour les éléments à position fixe dans des frames sans AutoLayout. Contrôlent le comportement au redimensionnement.

| Horizontal | Comportement |
|-----------|--------------|
| Left | Fixé à gauche |
| Right | Fixé à droite |
| Left and Right | S'étire |
| Center | Centré |
| Scale | Proportionnel |

Mêmes options en vertical (Top, Bottom, etc.).

**Contraintes vs AutoLayout** : AutoLayout pour 90 % des mises en page (basé sur le flux). Contraintes pour les cas particuliers (éléments flottants, qui se chevauchent).

## Composants {#components}

Éléments réutilisables. Modifier le composant principal -> toutes les instances se mettent à jour.

### Création {#creating}
1. Sélectionner le ou les éléments
2. Ctrl+Alt+K -> composant créé (losange violet)
3. Le nommer avec une barre oblique : `button/primary`, `button/secondary`

### Principal vs instance {#main-vs-instance}
- **Principal** (losange violet plein) : définition source
- **Instance** (losange vide) : copie liée
- Les instances peuvent surcharger : le texte, le remplissage, la visibilité des enfants
- Détacher l'instance (clic droit) pour rompre le lien

## Variants {#variants}

Regrouper les états d'un même composant dans un ensemble de composants.

### Propriétés {#properties_1}
| Propriété | Valeurs | Usage |
|----------|---------|-------|
| State | default, hover, pressed, disabled | Interaction |
| Size | sm, md, lg | Responsive |
| Type | primary, secondary, ghost | Visuel |
| Icon | true, false | Avec/sans |

Nommage : `Button/Size=md, Type=primary, State=default`

### Propriétés de composant {#component-properties}
- **Boolean** : afficher/masquer un élément enfant
- **Instance swap** : remplacer un composant imbriqué
- **Text** : exposer un texte modifiable

## Page du design system {#design-system-page}

Page dédiée documentant toutes les décisions de design :
1. Palette de couleurs (nuanciers avec code hexadécimal)
2. Échelle typographique (toutes les tailles de titres et de corps de texte)
3. Échelle d'espacement (grille de 8px)
4. Bibliothèque de composants (boutons, champs de saisie, cartes)
5. Jeu d'icônes
6. Spécifications de grille

### Système de styles {#styles-system}
```text
Color styles:  primary/500, neutral/100, accent/success
Text styles:   heading/h1, heading/h2, body/regular
Effect styles: shadow/sm, shadow/md, blur/glass
Grid styles:   reusable grid configurations
```

La barre oblique crée une hiérarchie de dossiers. Modifier la définition d'un style -> toutes les instances se mettent à jour.

## Organisation du fichier {#file-organization}

| Page | Contenu |
|------|---------|
| Cover | Vignette du projet (1920x960) |
| Design System | Styles, couleurs, typographie, composants |
| Wireframes | Mises en page basse fidélité |
| Desktop | Haute fidélité desktop |
| Mobile | Haute fidélité mobile |
| Prototype | Écrans connectés |

## Pièges courants {#gotchas}

- **Contraintes ignorées dans AutoLayout** : AutoLayout contrôle le positionnement de tous les enfants
- **Nommage des variants** : le format doit être exactement `Property=Value` séparé par des virgules
- **Fill container uniquement dans AutoLayout** : impossible sur les enfants de frames sans AutoLayout
- **Hiérarchie des composants** : pas d'élément dans un élément dans le nommage ; garder une structure à plat
- **Instances détachées** : perdent tout lien avec le principal ; impossible de les rattacher

## Voir aussi {#see-also}

- [[figma-fundamentals]] - Interface, frames, export
- [[figma-design-workflow]] - Typographie, prototypage, responsive
- [[css-flexbox]] - Implémentation CSS des concepts d'AutoLayout
- [[css-responsive-design]] - Breakpoints et design adaptatif
