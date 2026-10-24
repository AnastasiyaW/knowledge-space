---
title: "Production vidéo assistée par IA"
category: applications
tags: [data-science, generative-ai, video, production, tools]
level: 2
source_sha256: 37aaa4559931fe6bdacda7e32233050bd3a6e3a88f33aa370152a10e6ccedceb
translation: machine
translated_at: '2026-10-24'
---
# Production vidéo assistée par IA {#ai-powered-video-production}

Pipeline complet de création de vidéos commerciales à l'aide d'outils d'IA. Enchaîne la rédaction de scénario par LLM, la génération d'images, la synthèse vidéo et la génération audio.

## Chaîne d'outils {#tool-chain}

| Outil | Rôle | Idéal pour |
|-------|------|------------|
| GPT-5 | Scénario, prompts, itérations | Un projet par vidéo, un chat par session |
| Seedream 4 | Génération d'images à partir de zéro | Personnes et scènes photoréalistes |
| NanoBanana Pro | Édition et stylisation d'images existantes | Reproduction de références, préservation de la géométrie |
| Kling 2.5 | Génération vidéo | Brouillon en 720p (gratuit), version finale en 1080p |
| ElevenLabs | Génération vocale | Voix off, dialogues de personnages |
| Suno | Génération musicale | Musique de fond |

## Étapes du pipeline {#pipeline-stages}

### 1. Scénario et storyboard {#1-script-storyboard}
- Transmettre à GPT le concept, les personnages, le cadre et les références visuelles
- Structurer en environ 6 scènes, pour une durée totale d'environ 25 secondes
- Attribuer les types de plans : large / moyen / gros plan / détail
- Ne jamais répéter deux fois de suite le même type de plan
- Tenir compte des limites de l'IA : les plans éloignés restituent mal les visages

### 2. Génération des images fixes {#2-still-frame-generation}
- Seedream : style Fashion Photo, 16:9, mode Unlimited
- Désactiver « AI Prompt / Improve short prompts »
- Générer d'abord sans références, puis affiner avec des références
- Corriger avec NanoBanana les modifications qui doivent préserver la géométrie

### 3. Animatique de brouillon {#3-draft-animatic}
- Kling 2.5 en 720p Unlimited (0 crédit) pour les tests
- Vérifier : vitesse des mouvements, proportions, cohérence de l'arrière-plan
- Corriger par régénération avec des prompts affinés

### 4. Structure du prompt vidéo {#4-video-prompt-structure}
```text
1. Scene description: "wide shot of a lone man walking..."
2. Character movement: "takes 2-3 small steps then stops"
3. Camera movement: "camera slowly dollies forward, no shaking"
4. Atmosphere: "cold, dramatic grading, blue haze"
5. Negative: "no extra limbs, no face blur, no acid colors"
```

### 5. Audio et synchronisation labiale {#5-audio-lipsync}
- ElevenLabs pour la génération des voix off
- Synchronisation labiale dans Higgsfield (alignement vidéo et audio)
- La synchronisation labiale en anglais est plus stable que dans les autres langues
- Adéquation des durées essentielle : la vidéo et l'audio doivent être alignés

## Seedream et NanoBanana {#seedream-vs-nanobanana}

| Critère | Seedream 4 | NanoBanana Pro |
|---------|-----------|----------------|
| À partir de zéro | Excellent | Bon |
| Reproduction de références | Médiocre | Excellent |
| Détails en gros plan | Contrasté, dur | Doux, réaliste |
| Texte et image de marque | Médiocre | Nettement meilleur |

## Gestion des crédits {#credit-management}
- Toutes les images fixes et expérimentations : mode Unlimited (gratuit)
- Vidéos de brouillon : 720p Unlimited (0 crédit)
- Génération finale uniquement : 1080p (500 crédits par génération, 3 à 5 tentatives par scène)

## Pièges à éviter {#gotchas}
- Les prompts longs et « poétiques » déroutent les modèles vidéo : rester structuré et précis
- Toujours préciser le comportement de la caméra (par défaut, un mouvement « flottant » aléatoire)
- Loin de la caméra, la qualité du visage se dégrade : utiliser une référence séparée en pied
- Étalonnage des couleurs : remplacer le « golden hour » par défaut de GPT pour des rendus dramatiques
- Dents, langue et bouche sont les principales zones d'artefacts en synchronisation labiale

## Voir aussi {#see-also}
- [[generative-models]] - technologie de génération sous-jacente
- [[nlp-text-processing]] - ingénierie des prompts
