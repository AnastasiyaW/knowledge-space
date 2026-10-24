---
title: "Workflow de design dans Figma"
category: concepts
tags: [web-frontend, figma, typography, color, prototyping, responsive]
level: 3
source_sha256: aef298d42b151b49fb52b9b2174e163bc5404cc8e871ef31f307750d127f6e77
translation: machine
translated_at: '2026-10-24'
---
# Workflow de design dans Figma {#figma-design-workflow}

Typographie, théorie des couleurs, effets, prototypage et workflow de design responsive dans Figma.

## Typographie {#typography}

### Classification des polices {#font-classification}
- **Serif** (Times, Playfair) : classique, formel, titres dans le luxe et l'édition
- **Sans-serif** (Roboto, Inter, Open Sans) : épuré, moderne, choix par défaut pour le corps de texte web
- **Monospace** (Fira Code) : blocs de code uniquement
- **Display/Script** : titres ou accents uniquement, jamais pour le corps de texte

### Échelle typographique {#typography-scale}

| Élément | Taille | Graisse | Hauteur de ligne |
|---------|--------|---------|------------------|
| H1 | 48-64px | Bold 700 | 110-120 % |
| H2 | 36-48px | Bold 700 | 120-130 % |
| H3 | 24-32px | SemiBold 600 | 120-130 % |
| Corps | 16-18px | Regular 400 | 150-160 % |
| Légende | 12-14px | Regular 400 | 140-150 % |
| Bouton | 14-16px | Medium 500 | 100 % |

### Règles {#rules}
- Maximum 2 familles de polices par projet
- 45 à 75 caractères par ligne pour une bonne lisibilité
- Minimum 14px sur le web, 16px recommandé pour le corps de texte
- Majuscules : uniquement pour les libellés courts, avec un interlettrage augmenté de 2 à 5 %

## Grille d'espacement de 8px {#8px-spacing-grid}

Tous les espacements sont des multiples de 8 : 8, 16, 24, 32, 40, 48, 64, 80px. Une sous-grille de 4px sert aux ajustements fins.

| Contexte | Valeurs typiques |
|----------|------------------|
| Marges de page (mobile) | 16-24px |
| Marges de page (desktop) | 80-120px |
| Padding de section | 64-120px |
| Padding de carte | 16-32px |
| Espace entre les cartes | 16-32px |
| Padding de bouton | 12-16px vertical, 24-32px horizontal |

## Couleur {#color}

### Modèle HSB {#hsb-model}
- **H** (Hue, teinte) : roue chromatique de 0 à 360
- **S** (Saturation) : 0-100 % (du gris au vif)
- **B** (Brightness, luminosité) : 0-100 % (du noir au maximum)

### Construire une palette {#building-a-palette}
1. **Primaire** : couleur de marque (CTA, liens)
2. **Secondaire** : couleur complémentaire
3. **Neutres** : 5 à 7 nuances de gris
4. **Sémantiques** : succès, erreur, avertissement, information

### Règle 60-30-10 {#60-30-10-rule}
- 60 % dominant (généralement neutre/blanc)
- 30 % secondaire (sections, cartes)
- 10 % accent (CTA, mises en évidence)

### Contraste {#contrast}
Minimum 4,5:1 pour le corps de texte, 3:1 pour les grands textes (WCAG AA). Utiliser les plugins Stark ou Contrast pour vérifier.

## Effets {#effects}

### Ombre portée {#drop-shadow}
Valeur courante : `X:0 Y:4 Blur:12 Color:#000 à 10-15 %`. Plusieurs ombres peuvent être superposées.

### Flou d'arrière-plan (glassmorphism) {#background-blur-glassmorphism}
Flou d'arrière-plan de 10 à 20px + remplissage #FFF à 30-60 % d'opacité.

### Modes de fusion {#blend-modes}
Multiply (assombrir), Screen (éclaircir), Overlay (contraste). À utiliser pour harmoniser les images.

### Masques {#masks}
Placer la forme au-dessus de l'image → sélectionner les deux → « Utiliser comme masque » (Ctrl+Alt+M). La forme définit la zone visible.

## Prototypage {#prototyping}

### Connexions {#connections}
1. Sélectionner l'élément déclencheur (bouton, carte)
2. Glisser le cercle bleu vers le cadre cible
3. Configurer : déclencheur, action, animation, durée, courbe d'accélération

### Types de transition {#transition-types}
- **Instant** : aucune animation
- **Dissolve** : fondu enchaîné
- **Smart Animate** : interpole les calques correspondants (même nom requis)
- **Move/Push/Slide** : transitions directionnelles

### Smart Animate {#smart-animate}
1. Créer le cadre A (état de départ)
2. Dupliquer → modifier dans le cadre B (position, taille, couleur, opacité)
3. Relier A → B avec Smart Animate
4. Les calques DOIVENT porter des noms identiques pour être mis en correspondance

Interpole : position, taille, rotation, opacité, remplissage, rayon de bordure, contour.

### Overlays {#overlays}
Relier le déclencheur à « Open overlay » → sélectionner le cadre d'overlay. Configurer la position, l'assombrissement de l'arrière-plan et la fermeture au clic.

### Composants interactifs {#interactive-components}
Définir les interactions DANS les variantes du composant (survol, appui). Chaque instance en hérite automatiquement.

### Recommandations de durée {#duration-guidelines}
| Animation | Durée |
|-----------|-------|
| État de bouton | 100-200ms |
| Infobulle | 150-200ms |
| Modale | 200-300ms |
| Transition de page | 300-500ms |

### Courbes d'accélération (easing) {#easing}
- **Ease out** : éléments qui entrent (le plus courant)
- **Ease in** : éléments qui sortent
- **Ease in-out** : éléments qui se déplacent à l'intérieur de la vue
- Material Design : `cubic-bezier(0.4, 0.0, 0.2, 1.0)`

## Workflow de design responsive {#responsive-design-workflow}

### Points de rupture {#breakpoints}
Concevoir au moins 3 tailles : Mobile (375px), Tablette (768px), Desktop (1440px).

### Schémas d'adaptation {#adaptation-patterns}
1. **Reflow** : horizontal → pile verticale
2. **Hide** : retirer les éléments non essentiels sur petit écran
3. **Resize** : réduire proportionnellement les polices et les paddings
4. **Replace** : le menu hamburger remplace la navigation horizontale

### Processus {#process}
1. Commencer par le desktop (plus d'espace pour planifier la mise en page)
2. Dupliquer → redimensionner pour la tablette → ajuster
3. Dupliquer → redimensionner pour le mobile → ajuster
4. Garder les composants cohérents d'un point de rupture à l'autre

### Export pour écrans Retina {#export-for-retina}
- 1x (standard), 2x (Retina), 3x (iPhone Plus/Max)
- Le SVG n'a pas besoin d'exports multiples (vectoriel)

## Principes de design {#design-principles}

- **Espace blanc** : plus d'espace = sensation premium ; moins d'espace = information dense
- **Proximité** : éléments liés rapprochés, éléments non liés éloignés
- **Répétition** : styles cohérents pour les éléments de même niveau
- **Contraste** : les différences de taille, de graisse, de couleur et d'espace créent la hiérarchie
- **Alignement** : des axes partagés créent l'ordre

## Wireframes {#wireframes}

Planification de structure en basse fidélité : niveaux de gris, rectangles simples, texte basique. Tester auprès des parties prenantes avant d'investir dans la haute fidélité.

## Plugins essentiels {#essential-plugins}

| Plugin | Usage |
|--------|-------|
| Iconify | Plus de 100 000 icônes |
| Unsplash | Photos d'illustration |
| Contrast/Stark | Vérification de l'accessibilité |
| Content Reel | Données de substitution |

## Pièges courants {#gotchas}

- **Décalage de noms dans Smart Animate** : les calques aux noms différents subissent un fondu enchaîné au lieu d'être interpolés
- **Overlay sans fermeture** : l'utilisateur reste bloqué ; toujours activer la fermeture au clic extérieur
- **Trop de polices** : plus de 2 familles crée un chaos visuel
- **Ignorer le contraste** : un texte beau mais illisible échoue en accessibilité
- **Raisonner en maquette statique** : ne pas tester le redimensionnement tôt mène à des designs non responsives

## Voir aussi {#see-also}

- [[figma-fundamentals]] - Interface, cadres, export
- [[figma-layout-and-components]] - AutoLayout, composants, variantes
- [[css-animation-and-transforms]] - Implémentation des animations conçues
- [[css-responsive-design]] - Media queries CSS pour les points de rupture
