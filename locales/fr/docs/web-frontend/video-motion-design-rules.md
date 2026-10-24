---
title: "Règles de design vidéo et motion design"
description: "Valeurs concrètes pour la durée, les courbes d'accélération, les niveaux audio, la composition et la narration dans les vidéos produit et les motion graphics."
level: 4
source_sha256: 8f3ccfecf037945120c3f8a345b3a23698345fe3338df0e347e9fdc39c21649d
translation: machine
translated_at: '2026-10-24'
---
# Règles de design vidéo et motion design {#video-motion-design-rules}

Référence pour les motion graphics, les vidéos produit et les présentations animées de qualité production. Toutes les valeurs sont précises et directement applicables.

## Timing des animations {#animation-timing}

### Durée selon le poids de l'élément {#duration-by-element-weight}

| Élément | Durée | Images @30 ips | Exemple |
|---------|-------|----------------|---------|
| Micro (icône, point) | 150-200 ms | 5-6 | Bascule, case à cocher |
| Petit (bouton, badge) | 200-300 ms | 6-9 | État au survol, infobulle |
| Moyen (carte, texte) | 300-500 ms | 9-15 | Glissement de panneau, liste déroulante |
| Grand (panneau, image) | 400-700 ms | 12-21 | Ouverture de modale |
| Héros (produit, scène) | 600-1200 ms | 18-36 | Révélation du produit |
| Cinématographique (arrière-plan) | 800-1500 ms | 24-45 | Transitions d'ambiance |

**Règle :** les animations d'interface restent sous 300 ms. 180 ms paraît plus réactif que 400 ms (observation empirique).

### Tokens de durée Material Design 3 {#material-design-3-duration-tokens}

| Token | Valeur | Usage |
|-------|--------|-------|
| short1 | 50 ms | Retour micro-interaction |
| short4 | 200 ms | Interactions standard |
| medium2 | 300 ms | Transitions standard |
| medium4 | 400 ms | Transitions complexes |
| long2 | 500 ms | Transitions de navigation |
| long4 | 600 ms | Transitions élaborées |
| extraLong1-4 | 700-1000 ms | Dramatique (rare) |

### Recommandations de durée des scènes {#scene-duration-guidelines}

| Type de scène | Durée |
|---------------|-------|
| Accroche/ouverture | 3-5 s |
| Chiffre clé (« 2x plus rapide ») | 4-6 s |
| Présentation de fonctionnalité | 5-8 s |
| Plan produit soigné | 3-5 s |
| Témoignage/citation | 4-6 s |
| Appel à l'action/conclusion | 4-6 s |
| Montage rapide | 2-3 s chacun |

**Rythme d'une vidéo de 60 secondes :**
```text
[0-5s]   Hook: bold statement, dark bg        — FAST
[5-15s]  Problem: 2-3 quick cuts              — MEDIUM
[15-25s] Solution reveal: product appears     — SLOW
[25-40s] Features: 3-4 staggered              — MEDIUM
[40-50s] Social proof: stats/logos/quotes     — MEDIUM-FAST
[50-60s] CTA: logo + URL + action             — SLOW, decisive
```

**Règle de respiration :** après chaque séquence rapide (3 coupes rapides ou plus), insérer un plan lent (5-8 s).

## Accélération {#easing}

### Référence cubic-bezier {#cubic-bezier-reference}

| Nom | Valeur | Usage |
|-----|--------|-------|
| ease (valeur par défaut du navigateur) | `(0.25, 0.1, 0.25, 1.0)` | Générique, acceptable |
| **Material Standard** | `(0.4, 0.0, 0.2, 1.0)` | Accélération principale de l'interface |
| Material Decelerate (entrée) | `(0.0, 0.0, 0.2, 1.0)` | Élément qui apparaît |
| Material Accelerate (sortie) | `(0.4, 0.0, 1.0, 1.0)` | Élément qui disparaît |
| Entrée accentuée | `(0.05, 0.7, 0.1, 1.0)` | Apparition spectaculaire |
| Sortie accentuée | `(0.3, 0.0, 0.8, 0.15)` | Départ spectaculaire |
| Rebond/dépassement | `(0.34, 1.56, 0.64, 1.0)` | Boutons et badges ludiques |
| Snappy | `(0.2, 0.0, 0.0, 1.0)` | Rapide, affirmé |
| Apple ease | `(0.25, 0.1, 0.25, 1.0)` | Style premium/Apple |

### Physique des ressorts {#spring-physics}

| Configuration | stiffness | damping | Effet |
|---------------|-----------|---------|-------|
| Interface réactive | 200 | 20 | Rebond minimal |
| Ludique | 120 | 10 | Rebond perceptible |
| Douce (grands éléments) | 50 | 200 | Lente, sans rebond |

**JAMAIS de linéaire pour l'interface** : l'effet est mécanique. Le linéaire est réservé aux barres de progression.

## Patterns de décalage (stagger) {#stagger-patterns}

**Nombre maximal d'éléments décalés : 8-10.** Au-delà, les derniers éléments attendent trop longtemps.

**Décalage linéaire :** 30-80 ms entre les éléments d'une liste.

**Cascade (accélérée) :** chaque délai est plus court que le précédent, ce qui crée un effet d'« écoulement ».

**Grille en diagonale :** délai = `(row + col) * baseDelay`. Le coin supérieur gauche s'anime en premier.

**Onde depuis le centre :** délai proportionnel à la distance au point central.

## Les 12 principes de Disney appliqués à la vidéo produit {#disneys-12-principles-applied-to-product-video}

| Principe | Application | À FAIRE / À ÉVITER |
|----------|-------------|--------------------|
| **Squash & Stretch** | Les boutons se réduisent à 0,95-0,97 à l'appui | À FAIRE : éléments souples. À ÉVITER : texte/lignes |
| **Anticipation** | Micro-mouvement de 30-50 ms dans le sens opposé au mouvement principal | À FAIRE : avant les transitions majeures. À ÉVITER : au survol |
| **Mise en scène** | Un seul point focal par scène | À FAIRE : arrêter les animations d'arrière-plan lorsque l'élément clé apparaît. À ÉVITER : 3 animations simultanées ou plus |
| **Continuité du mouvement** | Les éléments dépassent de 2-5 % puis se stabilisent | À FAIRE : décaler dans les listes/grilles. À ÉVITER : le même décalage pour 20 éléments ou plus |
| **Accélération entrée/sortie** | Jamais linéaire pour l'interface | Utiliser Material Standard par défaut |
| **Trajectoires courbes** | Trajectoires courbes naturelles entre deux positions | À FAIRE : éléments flottants. À ÉVITER : listes déroulantes (on attend une ligne droite) |
| **Action secondaire** | Les effets d'arrière-plan accompagnent sans rivaliser | À FAIRE : particules d'ambiance, pulsation lumineuse. À ÉVITER : rotation, clignotement |
| **Exagération** | Agrandir le produit de 5-15 % pour l'impact | À FAIRE : animations héros. À ÉVITER : animations utilitaires |
| **Profondeur** | 3-5 couches de parallaxe | Arrière-plan à 0,3x, premier plan à 1,0-1,3x |

## Typographie à l'écran {#typography-on-screen}

### Échelle de tailles pour 1920x1080 {#size-scale-for-1920x1080}

| Rôle | Taille | Graisse | Remarques |
|------|--------|---------|-----------|
| Chiffre clé | 120-200 px | 800-900 | « 10x plus rapide », statistiques clés |
| Titre de section | 64-80 px | 600 | Noms de fonctionnalités |
| Sous-titre | 36-48 px | 500 | Titres secondaires |
| Corps | 24-32 px | 400 | Descriptions |
| Légende | 16-20 px | 400 | Annotations courtes |
| **Minimum** | **16 px** | indifférent | En dessous : illisible en vidéo |

### Vitesse de lecture {#reading-speed}

| Format | Mots | Durée à l'écran |
|--------|------|-----------------|
| Ligne courte | 3-7 mots | 1,5-3 s |
| Ligne moyenne | 8-12 mots | 3-5 s |
| Phrase longue | 13-20 mots | 5-8 s |
| 30 mots et plus | à répartir sur 2-3 écrans | - |

Pour un public mixte, compter 150-180 mots par minute. Règle : 2,5-3,0 s par ligne courte (7-9 mots).

### Limites de mots par élément {#word-limits-per-element}

| Élément | Limite |
|---------|--------|
| Titre | 3-6 mots |
| Sous-titre/légende | 2 lignes maximum, 32-42 caractères par ligne |
| Bandeau inférieur | 2 lignes maximum (nom + fonction) |
| Écran avec voix off | 10-15 mots maximum |
| Écran sans voix off | 20-25 mots maximum |
| Vignette | 3-5 mots maximum |

### Animation du texte {#typography-animation}

- À FAIRE : fondu entrant + translation de 20-40 px depuis le bas
- À FAIRE : mise à l'échelle de 95 % à 100 % avec opacité de 0 à 1
- À FAIRE : décaler les mots de 4-8 images chacun
- À ÉVITER : faire pivoter le texte
- À ÉVITER : faire rebondir le texte (sauf marque ludique)
- À ÉVITER : déplacer le texte pendant que le spectateur le lit

**Le texte doit rester lisible au moins 2 s après la fin de l'animation.** Ne jamais animer un texte en attendant une lecture simultanée.

## Couleur {#color}

### Règles de palette {#palette-rules}

- 3 couleurs maximum par vidéo (+ noir, blanc, gris)
- 1 couleur de marque principale + 1 couleur d'accent + 1 couleur d'appel à l'action
- Contraste fond/texte minimum de 7:1 (WCAG AAA)
- Couleurs d'un dégradé : 120° maximum sur le cercle chromatique

### Recommandations pour les dégradés {#gradient-guidelines}

**Direction :** du haut-gauche vers le bas-droite (lumière naturelle). À ÉVITER : du bas vers le haut.

| Type | Usage |
|------|-------|
| Linéaire | Arrière-plans, superpositions |
| Radial | Projecteur, halo, focus au centre |
| Maillage (mesh) | Arrière-plans héros premium, écrans d'application |
| Conique | Horloges, graphiques circulaires, progression |

**Dégradés avec bruit (2025-2026) :** dégradé + superposition de bruit de 3-8 % = rendu organique premium.

### Mode sombre ou clair {#dark-vs-light-mode}

**Mode sombre préférable pour :** présentations de produits (le produit ressort), sensation premium/luxe, environnements de visionnage peu éclairés, photo/portfolio.

**Mode clair préférable pour :** texte dense, contextes corporate, salles de conférence, contenus proches de l'imprimé.

### Palettes tendance (2026) {#trending-palettes-2026}

**Tech/sombre :**
- Bleu marine profond `#0D1117` + bleu électrique `#58A6FF`
- Sarcelle sombre `#0F2027` + cyan `#00C9FF` + blanc doux

**Tech/clair :**
- Blanc cassé `#F8F9FA` + accents chauds
- Lavande douce `#F3E8FF` + violet profond `#7C3AED`

## Composition {#composition}

### Zones de sécurité par plateforme {#safe-zones-by-platform}

**YouTube 16:9 (1920x1080) :**
- Zone de sécurité pour le titre : 80 % intérieurs (marge de 10 % de chaque côté)
- Zone de sécurité pour l'action : 90 % intérieurs
- Zone des bandeaux inférieurs : 20-25 % du bas

**Vertical 9:16 (TikTok/Reels/Shorts, 1080x1920) :**
- 20 % du bas occupés par l'interface de la plateforme
- 10 % de droite occupés par l'interface de la plateforme
- Sujet/visage : 20-30 % supérieurs de l'image
- Zone de sécurité du texte : 15-75 % de la hauteur, largeur centrée

**Carré 1:1 (Instagram, 1080x1080) :**
- Zone de sécurité : 900x900 px intérieurs
- Une composition centrée est la plus efficace

### Hiérarchie visuelle par scène {#visual-hierarchy-per-scene}

- 3 niveaux de hiérarchie maximum par scène
- L'élément principal représente 40-60 % du poids visuel
- Jamais deux éléments principaux en concurrence dans une même scène
- Combiner taille, graisse, couleur et position (pas un seul de ces critères)

### Profondeur de parallaxe {#parallax-depth}

- Couche d'arrière-plan : vitesse de défilement de 0,2-0,4x
- Plan intermédiaire : 0,6-0,8x
- Premier plan : 1,0-1,3x

## Transitions entre scènes {#scene-transitions}

| Transition | Usage | Durée |
|-----------|-------|-------|
| **Coupe franche** | Même énergie, rythme rapide (80 % des coupes) | instantanée |
| Fondu enchaîné | Passage du temps, lien doux | 0,5-2 s |
| Fondu au noir | Fin de section, pause dramatique | 1-2 s |
| Balayage (wipe) | Changement de lieu, stylistique | 0,5-1,5 s |
| Zoom traversant | Énergie, modernité, dynamisme | 0,3-0,5 s |
| Match cut | Similitude visuelle (forme/couleur/mouvement) | instantanée |
| L-cut | Audio de la scène 1 sur les images de la scène 2 | chevauchement audio |
| J-cut | Audio de la scène 2 avant la fin de la scène 1 | l'audio devance |

**Par défaut : coupe franche.** Plus de 80 % des transitions de vidéo professionnelle sont des coupes.

2-3 types de transitions maximum par vidéo. À ÉVITER : les wipes en étoile, le damier, les fondus de plus de 2 s.

**Fondu audio croisé :** chevauchement de 100-300 ms pour des transitions audio fluides.

## Niveaux audio {#audio-levels}

### Référence en dB {#db-reference}

| Élément | Crête | Sonie (LUFS) |
|---------|-------|--------------|
| Voix off | -12 à -10 dB | -16 à -14 |
| Musique sous la voix off | -32 à -24 dB | -24 à -18 |
| Musique seule | -16 à -12 dB | -16 à -14 |
| Effets sonores | -18 à -10 dB | variable |
| Mixage global | -14 en moyenne, crêtes sous -6 dB | -16 à -14 |
| Plafond de vraie crête | -1 à -3 dB | - |

**Règle :** la voix off doit être environ 20 dB plus forte que la musique d'arrière-plan.

### BPM selon l'ambiance {#bpm-by-mood}

| BPM | Ambiance | Cas d'usage |
|-----|----------|-------------|
| 60-80 | Calme/ambiant | Luxe, méditation |
| 80-100 | Détendue | Art de vivre, interviews |
| 100-120 | Modérée | Corporate, démonstrations tech |
| 120-140 | Dynamique | Lancements de produits, fitness |
| 140+ | Haute énergie | Action, jeux vidéo |

120 BPM = tempo humain préféré (correspond à la cadence de la marche, valeur par défaut des DAW).

### Types d'effets sonores {#sound-effect-types}

| Effet | Durée | Usage |
|-------|-------|-------|
| Whoosh | 50-200 ms | Transitions par glissement |
| Clic/pop | 20-50 ms | Appui sur un bouton, sélection |
| Ding/carillon | - | États de succès, notifications |
| Swoosh | - | Transitions de page, révélations |

Les effets sonores doivent être 6-12 dB plus faibles que la voix off.

### Bibliothèques sonores gratuites {#free-sound-libraries}

- **Mixkit** (mixkit.co) : libre de droits, sans attribution, usage commercial autorisé
- **Pixabay** (pixabay.com/sound-effects) : libre de droits, sans inscription
- **Freesound** (freesound.org) : sous licence CC
- **SFX Engine** (sfxengine.com) : sons d'interface générés par IA

## Cadres narratifs {#storytelling-frameworks}

### PAS (Problème-Agitation-Solution) : meilleur taux de conversion {#pas-problem-agitation-solution-highest-converting}

```yaml
Problem:    3s — one clear pain point
Agitation:  5s — vivid consequence
Solution:   4s — your product/answer
CTA:        3s — direct call to action
Total: ~15s. Scale proportionally for 30-60s.
```

### Accroche-Valeur-CTA {#hook-value-cta}

```yaml
Hook:  2-5s  — pain point or question
Value: rest  — concise solution
CTA:   3-5s
```

### Accroche-Problème-Solution-Preuve-CTA (optimisé pour les vidéos courtes) {#hook-problem-solution-proof-cta-short-video-optimized}

| Section | Durée | Exemple |
|---------|-------|---------|
| Accroche | 3-5 s | « Et si vous pouviez créer une vidéo produit en 5 minutes ? » |
| Problème | 5-10 s | « Faire appel à une équipe vidéo coûte plus de 5 000 $. Les outils DIY font amateur. » |
| Solution | 10-20 s | Révélation du produit + 1 démonstration clé |
| Preuve | 5-10 s | Chiffres, logos, témoignages |
| CTA | 3-5 s | « Essayez gratuitement sur product.com » |

### Règle des premières secondes {#first-seconds-rule}

- Les 3 premières secondes déterminent la rétention (moment d'arrêt du défilement)
- Les 8 premières secondes comptent pour tout le format court
- À ÉVITER : commencer par le logo ou une intro (personne ne s'intéresse à votre logo)
- À FAIRE : commencer par l'accroche, le problème ou un élément visuel surprenant

## Spécifications des plateformes (2026) {#platform-specs-2026}

| Plateforme | Format | Résolution | Durée maximale | Format de fichier |
|------------|--------|------------|----------------|-------------------|
| YouTube | 16:9 | 1920x1080 (jusqu'à 4K) | 12 heures | MP4 H.264+AAC |
| YouTube Shorts | 9:16 | 1080x1920 | 3 min | MP4 |
| Instagram Reels | 9:16 | 1080x1920 | 20 min | MP4/MOV |
| Instagram Feed | 1:1 ou 4:5 | 1080x1080 ou 1080x1350 | 60 s | MP4/MOV |
| TikTok | 9:16 | 1080x1920 | 10 min dans l'application | MP4/MOV |
| Publicités TikTok | 9:16 | 1080x1920 | 9-60 s | MP4/MOV, moins de 500 Mo |
| LinkedIn | 16:9 ou 1:1 | 1920x1080 | 10 min | MP4 |

**Durées les plus efficaces :** TikTok 21-34 s, YouTube Shorts 30-60 s, Instagram Reels 15-30 s.

## Rédaction pour la vidéo {#copywriting-for-video}

- Des chiffres plutôt que des adjectifs : « 5x plus rapide » et non « beaucoup plus rapide »
- Le bénéfice plutôt que la fonctionnalité : « Gagnez 10 heures par semaine » et non « Dispose du traitement par lots »
- Vous plutôt que nous : « Vous allez adorer... » et non « Nous avons conçu... »
- 8-10 mots maximum par ligne à l'écran
- Supprimer : très, vraiment, en fait, réellement, juste

**Formules d'accroche :**
- « Et si vous pouviez [résultat souhaité] ? »
- « [Nombre] [nom] qui [bénéfice inattendu] »
- « Arrêtez [erreur courante]. Adoptez [meilleure approche]. »

## Conception de vignettes {#thumbnail-design}

Spécifications : 1280x720 px, 72 dpi, PNG/JPG de moins de 2 Mo.

**Règle des couleurs 60-30-10 :** 60 % pour l'arrière-plan, 30 % pour le sujet, 10 % pour l'accent/le texte.

- 3-5 mots maximum, lisibles sur mobile
- Visages expressifs = +20-30 % de CTR
- 1-2 éléments héros maximum, sans encombrement

## Pièges courants {#gotchas}

- **Une accélération linéaire paraît mécanique.** Utilisez toujours une courbe. Le linéaire n'est légitime que pour les barres de progression et les indicateurs de chargement, où un rythme constant est attendu.
- **Décaler 20 éléments ou plus casse l'expérience utilisateur.** Le dernier élément attend trop longtemps et l'attention du spectateur se disperse. Limitez-vous à 8-10 éléments décalés ; pour les listes plus longues, regroupez-les et décalez les groupes.
- **Ne commencez pas par un logo.** Les spectateurs passent les intros. L'accroche doit capter l'attention avant l'apparition de la marque.
- **BPM ≠ ambiance.** Deux morceaux à 120 BPM peuvent produire des impressions totalement différentes. Le BPM fixe le niveau d'énergie minimal, pas le caractère émotionnel.
- **Les 20 % du bas d'une vidéo verticale sont masqués par l'interface de la plateforme** (boutons J'aime/Commenter/Partager de TikTok). N'y placez jamais de texte ni d'appel à l'action.
- **Un fondu de plus de 2 secondes ressemble à une erreur.** Le fondu enchaîné sert à marquer le passage du temps, pas à faire du style. Gardez-le à 0,5-2 s maximum.

## Listes de contrôle de production {#production-checklists}

### Préproduction {#pre-production}

- [ ] Cadre narratif : PAS / 3 actes / Accroche-Valeur
- [ ] Plateforme et format défini
- [ ] Palette de couleurs : 3-4 couleurs maximum + neutres
- [ ] Polices : 2 maximum (titres + texte)
- [ ] Musique : BPM adapté à l'ambiance
- [ ] Bibliothèque d'effets sonores prête

### Animation {#animation}

- [ ] Accélération cohérente : 1-2 types de courbes maximum
- [ ] Durées dans les limites (micro <100 ms, standard 200-350 ms, complexe 350-500 ms)
- [ ] Décalage de 30-80 ms entre les éléments groupés
- [ ] 2 éléments animés simultanément maximum
- [ ] Continuité du mouvement à l'arrêt (dépassement + stabilisation)
- [ ] Anticipation avant les transitions majeures

### Post-production {#post-production}

- [ ] Niveaux audio : voix off -12 à -10 dB, musique -32 à -24 dB sous la voix off
- [ ] Texte lisible à la taille de l'appareil cible
- [ ] Zones de sécurité respectées pour la plateforme cible
- [ ] Transitions cohérentes (2-3 types maximum)
- [ ] Accroche dans les 3 premières secondes
- [ ] Appel à l'action clair et visible
- [ ] Vignette : règle 60-30-10, 5 mots maximum
- [ ] Sous-titres ajoutés
- [ ] Export aux spécifications de la plateforme

## Voir aussi {#see-also}

- [[css-animation-and-transforms]]
- [[remotion-programmatic-video]]
- [[3d-browser-libs-for-video]]
