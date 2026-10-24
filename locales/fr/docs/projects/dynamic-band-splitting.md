---
title: "Séparation dynamique de bandes : dynamic-band-splitting-release — Publication de Dynamic Band Splitting"
category: "projects"
date: 2026-10-18
tags: ["dynamic-band-splitting", "dynamic-band-splitting-release", "project"]
aliases: ["Dynamic Band Splitting: dynamic-band-splitting-release"]
level: 2
source_sha256: 6b030239ef8de211469f1f7d70fb18e54f7f422b33f594fc74d67313ccb8424b
translation: machine
translated_at: '2026-10-24'
---
# Séparation dynamique de bandes : dynamic-band-splitting-release — Publication de Dynamic Band Splitting {#dynamic-band-splitting-dynamic-band-splitting-release-dynamic-band-splitting-release}

**Ligne de développement :** project:dynamic-band-splitting · fil dynamic-band-splitting-release  
**Dernier événement :** 2026-10-18 · 3 événements datés depuis 2026-10-10 · **Recherche effectuée le :** 2026-10-18 · niveau de confiance : élevé

## Présentation {#what-it-is}

Dynamic Band Splitting est un framework de séparation de sources audio destiné aux chercheurs et aux développeurs. Il modifie les frontières des bandes de fréquences pour chaque mélange et prend en charge les architectures BSRNN et TIGER.

Il produit des estimations pour la musique, les effets sonores et la parole. Sa recette d'inférence DnR publiée utilise de l'audio monophonique à 44,1 kHz.

Utilisez-le pour évaluer le découpage adaptatif en bandes. Les pistes séparées peuvent encore contenir des fuites et des artefacts.

## Ligne de développement {#development-line}

- **2026-10-10 — Dynamic Band Splitting : mise à jour dynamic-band-splitting-release.** Le dépôt officiel enregistre la publication du code, des modèles pré-entraînés DBS-BSRNN et DBS-TIGER, ainsi qu'un studio d'écoute interactif.
- **2026-10-15 — Dynamic Band Splitting : mise à jour dynamic-band-splitting-release.** Le dépôt officiel indique que l'article est disponible sur arXiv.
- **2026-10-18 — Tsinghua publie la méthode de séparation de sources audio DBS \(Dynamic Band Splitting\).** Tsinghua a publié la méthode DBS \(Dynamic Band Splitting\) pour la séparation de sources audio. Elle adapte les frontières des bandes de fréquences à chaque mélange avec un budget de jetons fixe.

  Deux versions ont été publiées :

  - DBS-BSRNN : 4,7 M de paramètres et fenêtres de 3 secondes.
  - DBS-TIGER : 1 M de paramètres et fenêtres de 6 secondes.

  Les deux séparent des pistes monophoniques à 44,1 kHz en musique, effets sonores et parole.
  - L'implémentation indique que la version comprend le code, les modèles pré-entraînés DBS-BSRNN et DBS-TIGER, ainsi qu'un studio interactif. Sa note de publication datée est le 10 octobre, et non le 18 octobre. (2026-10-10) — <https://github.com/JusperLee/Dynamic-Band-Splitting>
  - L'article indique que DBS prédit des frontières conditionnées par le mélange à l'intérieur de blocs de fréquences grossiers et fixes. Il utilise une sélection Top-K dure sous un budget de jetons fixe. L'article rapporte des évaluations sur DnR v2, MUSDB18-HQ et EchoSet. (2026-10-10) — <https://arxiv.org/abs/2610.14993>
  - Une synthèse chinoise de recherche audio décrit quatre blocs de fréquences fixes avec des budgets de bandes fixes par bloc. Les positions et largeurs des frontières varient selon le mélange en entrée. (2026-10-15) — <https://nanless.github.io/audio-paper-digest-blog/posts/2026-10-15/>

## Ce qui a changé {#what-changed}

Dynamic Band Splitting a rendu disponible un partitionnement fréquentiel adaptatif grâce aux points de contrôle DBS-BSRNN et DBS-TIGER publiés, au code source et à un studio d'écoute interactif.

## Comment l'utiliser {#how-to-use-this}

1. Clonez le dépôt. Installez une version de PyTorch adaptée à votre machine, puis installez les dépendances documentées et le paquet en mode éditable.
   — <https://github.com/JusperLee/Dynamic-Band-Splitting>
2. Chargez DBS-BSRNN pour la recette publiée de 3 secondes avec un saut de 1,5 seconde, ou DBS-TIGER pour la recette de 6 secondes avec un saut de 3 secondes.
   — <https://github.com/JusperLee/Dynamic-Band-Splitting>
3. Fournissez de l'audio à 44,1 kHz. Convertissez une entrée multicanal en mono si vous suivez l'exemple documenté, puis appelez l'API de séparation pour obtenir les estimations de musique, d'effets sonores et de parole.
   — <https://github.com/JusperLee/Dynamic-Band-Splitting>

## Bonnes pratiques {#best-practices}

- Faites correspondre l'architecture du point de contrôle à sa recette de découpage en segments : utilisez des fenêtres de 3 secondes avec DBS-BSRNN et des fenêtres de 6 secondes avec DBS-TIGER.
  — <https://github.com/JusperLee/Dynamic-Band-Splitting>
- Considérez les pistes issues de la démo et de l'inférence comme des estimations, et non comme une vérité de référence. Inspectez-les pour détecter les fuites entre sources et les artefacts avant toute utilisation en aval.
  — <https://cslikai.cn/Dynamic-Band-Splitting/>

## Retours de la pratique {#what-practitioners-say}

- Un rapport de la communauté indique que DBS-TIGER est plus clair pour la parole dans son test, mais plus lent que DBS-BSRNN. Il signale aussi une isolation plus faible des bruits non vocaux, comme le ronronnement d'un ventilateur. (2026-10-18)
  — <https://www.artofsm.art/t/1m-parameter-ai-pulls-speech-out-of-music-fan-noise/26189>

## Remplacé par cette version {#superseded-by-this}

- Rien d'obsolète n'a encore été signalé.

## Points encore inconnus {#still-unknown}

- Les URL fournies du modèle Hugging Face et de la démo n'ont pas pu être consultées pendant cette session de recherche. Leurs fiches et leur comportement à l'exécution n'ont pas été vérifiés de manière indépendante.
- Aucune donnée publique n'établit la fiabilité en production sur des domaines audio arbitraires au-delà des benchmarks et exemples rapportés.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/JusperLee/Dynamic-Band-Splitting | JusperLee/Dynamic-Band-Splitting | 2026-10-19 |
| https://arxiv.org/abs/2610.14993 | Learning Where to Split: Dynamic Band Splitting for Audio Source Separation | 2026-10-19 |
| https://cslikai.cn/Dynamic-Band-Splitting/ | Dynamic Band Splitting | 2026-10-19 |
| https://nanless.github.io/audio-paper-digest-blog/posts/2026-10-15/ | 语音/音乐/音频论文速递 2026-10-15 | 2026-10-19 |
| https://www.artofsm.art/t/1m-parameter-ai-pulls-speech-out-of-music-fan-noise/26189 | 1M Parameter AI Pulls Speech Out of Music \+ Fan Noise | 2026-10-19 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** project:dynamic-band-splitting, fil dynamic-band-splitting-release, 3 événements datés du 2026-10-10 au 2026-10-18.
- **Remarque pratique :** Voir les sections d'usage et de pratique sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
