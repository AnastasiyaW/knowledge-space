---
title: "NexVid — Distribution d'extension de navigateur"
category: projects
date: 2026-04-17
tags: [browser-extension-distribution, nexvid, project]
aliases: ["NexVid"]
level: 3
source_sha256: 69700292e2d23129b7207b3946e34436e87a6c0816666eb8fd3b1cd26e6b786c
translation: machine
translated_at: '2026-10-24'
---
# NexVid — Distribution d'extension de navigateur {#nexvid-browser-extension-distribution}

**Ligne de développement :** `project:nexvid` · fil `browser-extension-distribution`  
**Dernier événement :** 2026-04-17 · 1 événement daté depuis le 2026-04-17 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

NexVid est une extension de navigateur destinée aux personnes qui regardent des animés, des dessins animés et des vidéos web dans Chrome ou Firefox.
- Mise à l'échelle GPU Anime4K pour la lecture vidéo en temps réel.
- Profils de qualité et de FPS adaptés aux performances matérielles.
- Filtres et shaders WebGL pour l'ajustement de l'image.
- Préréglages permettant de sauvegarder les chaînes de shaders et de filtres.
- Lecteur local pour les fichiers vidéo du bureau.

Le traitement s'exécute pendant la lecture et nécessite un accès aux données de tous les sites web ; la version v1.1.9 du 2026-08-20 est la version actuelle.
Elle ajuste la lecture, mais ne remplace pas l'export vidéo avec mise à l'échelle par réseau de neurones.

## Ligne de développement {#development-line}

- **2026-04-17 — Les fiches de l'extension de navigateur NexVid apparaissent pour Chrome et Firefox.** Le 2026-04-17, les fiches de l'extension NexVid sont apparues sur le Chrome Web Store et sur Firefox Add-ons. Cette étape a étendu la distribution à Chrome et Firefox. Les fiches sources n'indiquent ni version, ni ensemble de fonctionnalités, ni état de disponibilité, ni modifications apportées à cette date.

## Évolutions {#what-changed}

- 2025-10-27 — Firefox 1.0.2 devient la plus ancienne version publiquement visible dans l'historique AMO.
- 2025-11-10 — Firefox 1.0.5 ajoute la prise en charge des vidéos locales et des effets supplémentaires.
- 2025-12-01 — Firefox 1.1.0 ajoute les thèmes sombre et minimaliste, relève le FPS maximal et corrige Twitch ; la 1.1.1, publiée le même jour, corrige la sélection des profils dans l'interface minimale.
- 2026-01-20 — Firefox 1.1.2 ajoute un seuil de résolution permettant d'ignorer les sources de haute qualité, ainsi que des shaders expérimentaux.
- 2026-03-08 — Firefox 1.1.3 ajoute une liste blanche de sites web.
- 2026-04-17 — Chrome 1.1.6 est mise à jour ; cela confirme une version Chrome, et non une version Firefox identique à cette date.
- 2026-08-20 — Chrome et Firefox proposent la 1.1.9 ; les descriptions actuelles des stores mentionnent Anime4K, les profils de performance, les shaders, les préréglages et un lecteur local.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-04-17, les praticiens qui évaluent NexVid doivent vérifier sa disponibilité en tant qu'extension de navigateur via le Chrome Web Store et Firefox Add-ons, en vérifiant par eux-mêmes la compatibilité et les capacités actuelles.

1. Installez NexVid depuis le Chrome Web Store ou Firefox Add-ons, puis ouvrez la vidéo web visée.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
2. Sélectionnez un profil Anime4K et un FPS cible adaptés aux performances de l'ordinateur, puis définissez un seuil de résolution pour ignorer les sources de haute qualité.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>
3. Construisez, si nécessaire, une chaîne de filtres et de shaders WebGL, puis enregistrez-la comme préréglage.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
4. Ouvrez les fichiers locaux avec le lecteur intégré plutôt que d'attendre un export de vidéo mise à l'échelle.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Bonnes pratiques {#best-practices}

- Commencez par les animés et les dessins animés ; l'auteur les présente comme les meilleures sources.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Ne dépassez pas le FPS de la source. Le curseur plafonne les images traitées au lieu d'en générer de nouvelles ; une limite de 30 FPS sur une source à 60 FPS peut provoquer des pertes d'images.
  — <https://www.reddit.com/r/SideProject/comments/1okqhgx/i_made_a_browser_extension_that_let_you_upscale/>
- Sélectionnez un profil en fonction de la charge matérielle, puis réglez les filtres séparément. L'auteur recommande le masque flou (unsharp mask) et le passe-haut pour la netteté avant d'enregistrer un préréglage.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Vérifiez la permission d'accès aux données de tous les sites avant l'installation, et limitez l'extension à une liste blanche de sites lorsque cette option est disponible.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Remplacé par {#superseded-by-this}

- 2025-10-31 — L'indication selon laquelle les fichiers locaux ne peuvent pas être ouverts dans NexVid est obsolète depuis l'arrivée de la prise en charge des vidéos locales dans Firefox 1.0.5, le 2025-11-10.
- 2026-04-17 — Chrome 1.1.6 n'est plus la version recommandée : la fiche actuelle du store indique la 1.1.9 du 2026-08-20.

## Points non élucidés {#still-unknown}

- L'historique public des versions Firefox s'arrête à la 1.1.3 du 2026-03-08, alors que la fiche actuelle affiche la 1.1.9 ; aucun journal des modifications entre les deux n'est disponible.
- La version Chrome 1.1.6 et son instantané de statistiques sont confirmés pour le 2026-04-17, mais aucun journal des modifications primaire n'explique le contenu de cette mise à jour.
- Le store Chrome indique une collecte de données de localisation et d'activité utilisateur, tandis que la fiche Firefox exige un accès aux données de tous les sites web ; une ventilation comparable des permissions sur les deux plateformes n'est pas établie.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim | NexVid - Real-time Video Upscaler & Enhancer - Chrome Web Store | 2026-09-05 |
| https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/ | NexVid - Real-time Video Upscaler & Enhancer – Firefox Add-ons | 2026-09-05 |
| https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/versions/ | Historique de versions de NexVid - Real-time Video Upscaler & Enhancer | 2026-09-05 |
| https://chrome-stats.com/d/hiocbajaikpcckgeagcngaeoioncmbim | NexVid: Real-time Video Upscaler & Enhancer | 2026-09-05 |
| https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/ | I made a browser extension that let you upscale and enhance videos from your browser in real-time: NexVid | 2026-09-05 |
| https://www.reddit.com/r/SideProject/comments/1okqhgx/i_made_a_browser_extension_that_let_you_upscale/ | I made a browser extension that let you upscale and enhance videos from your browser in real-time: NexVid | 2026-09-05 |
| https://www.reddit.com/r/chrome_extensions/comments/1okqerj/i_made_an_extension_that_let_you_upscale_and/ | I made an extension that let you upscale and enhance videos from your browser in real-time: NexVid | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:nexvid`, fil `browser-extension-distribution`, 1 événement daté du 2026-04-17 au 2026-04-17.
- **Note pratique :** À partir du 2026-04-17, les praticiens qui évaluent NexVid doivent vérifier sa disponibilité en tant qu'extension de navigateur via le Chrome Web Store et Firefox Add-ons, en vérifiant par eux-mêmes la compatibilité et les capacités actuelles.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
