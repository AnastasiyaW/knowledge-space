---
title: "Encodage vidéo et audio avec FFmpeg"
category: reference
tags: [linux-cli, ffmpeg, encoding, video, audio, nvenc, av1, h264, hevc]
level: 3
source_sha256: a6c11ff093bf53878c34792b9533bccdad74c73e8c32bce30a7d103f839f2670
translation: machine
translated_at: '2026-10-24'
---
# Encodage vidéo et audio avec FFmpeg {#ffmpeg-video-and-audio-encoding}

Encodeur multimédia en ligne de commande. Couvre le choix des codecs, l'accélération matérielle NVENC, l'encodage audio, la modification du tempo avec préservation des formants et les chemins rapides de concaténation. FFmpeg 7.x, NVENC Turing+.

## Points clés {#key-facts}

- `-vsync` est obsolète depuis FFmpeg 6+ ; utiliser `-fps_mode cfr` ou `-fps_mode vfr` à la place
- `libfaac` a été supprimé ; utiliser `aac` natif ou `libfdk_aac` installé via [[package-management]]
- `-rc constqp -qp X` fonctionne encore, mais `-rc vbr -cq X -b:v 0` est le schéma NVENC recommandé
- `-preset slow` n'existe plus pour NVENC ; utiliser les presets numériques `-preset p5/p6/p7` (p7 = le plus lent et le meilleur)
- `-tag:v hvc1` est requis pour HEVC dans MP4 lorsqu'on cible Apple QuickTime/Safari ; le `hev1` par défaut échoue
- NVENC Turing+ (RTX 2000+) est requis pour `spatial-aq`/`temporal-aq` ; Ada (RTX 4000+) pour `av1_nvenc`
- Le moteur Rubber Band R3 nécessite le CLI autonome de breakfastquay.com ; le `af_rubberband` intégré à ffmpeg utilise l'ancien moteur R2
- `yuv420p` est obligatoire pour la compatibilité avec les décodeurs matériels (téléphones, TV, systèmes embarqués) ; `yuv420p10le` est réservé à l'archivage
- `-movflags +faststart` déplace l'atome moov au début du fichier — requis pour le streaming HTTP et la navigation avant le téléchargement complet

## Choix du codec {#codec-selection}

| Codec | Encodeur | Vitesse (1080p, RTX 4090) | Qualité/débit | Compatibilité 2026 | À utiliser quand |
|---|---|---|---|---|---|
| H.264 | `libx264 -preset slow` | ~0,5x temps réel | Meilleure | Universelle | master d'archivage, petits lots |
| H.264 | `h264_nvenc -preset p6` | ~10x temps réel | Bonne (avec AQ) | Universelle | traitement par lots, distribution |
| HEVC | `libx265 -preset slow` | ~0,3x temps réel | Excellente | Large (pas WMP sans codec) | master d'archivage, 30-50 % plus petit que H.264 |
| HEVC | `hevc_nvenc -preset p6` | ~8x temps réel | Très bonne (avec `tune hq`) | Large | encodage HEVC par lots |
| AV1 | `libsvtav1 -preset 6` | ~0,5x temps réel | Meilleur AV1 sur CPU | Limitée (appareils récents) | archivage pérenne |
| AV1 | `av1_nvenc -preset p6` | ~8x temps réel | Bonne | Limitée | vitesse GPU quand le stockage est critique |

**Équivalence CRF/CQ (contenu peu dynamique : diapositives, enregistrement d'écran, tête parlante) :**

| Cible | CRF libx264 | CRF libx265 | CRF SVT-AV1 | CQ h264_nvenc | CQ hevc_nvenc |
|---|---|---|---|---|---|
| Visuellement sans perte | 18 | 16 | 20 | 18 | 18 |
| Compromis optimal pour la distribution | 22-23 | 22 | 28-32 | 24-25 | 26 |
| Agressif (surveiller les artefacts sur le texte) | 28+ | 26+ | 36+ | 28+ | 30+ |

Les contenus peu dynamiques (cours, screencasts, diapositives) tolèrent un CRF de 2 à 3 points plus élevé que la vidéo générale : les zones statiques profitent davantage de l'AQ que d'un débit supplémentaire.

**Choix de l'algorithme de mise à l'échelle :**

| Algorithme | Qualité | Vitesse | À utiliser quand |
|---|---|---|---|
| `lanczos` | Meilleur détail, légers halos (ringing) sur les contours du texte | Lent | Contenu photographique, tête parlante |
| `bicubic` | Bonne, moins de ringing | Rapide | Enregistrement d'écran, diapositives riches en texte |
| `bilinear` | La plus faible | La plus rapide | Jamais pour l'archivage |

## Recettes de commandes {#command-recipes}

### Copie de flux (réemballage du conteneur, sans perte de qualité) {#stream-copy-container-repack-no-quality-loss}

```bash
# MKV → MP4 repack, no re-encode
ffmpeg -i input.mkv -c copy -movflags +faststart output.mp4
```

### Master d'archivage libx264 {#libx264-archival-master}

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -preset slow -crf 20 \
  -profile:v high -level 4.1 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### Traitement par lots h264_nvenc (Turing+) {#h264_nvenc-bulk-batch-turing}

```bash
ffmpeg -i input.mp4 \
  -c:v h264_nvenc -preset p6 -tune hq \
  -rc vbr -cq 24 -b:v 0 -maxrate 6M -bufsize 12M \
  -bf 2 -spatial-aq 1 -temporal-aq 1 -rc-lookahead 32 \
  -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

`-bf 2` : images B pour une meilleure compression sur un contenu peu dynamique (NVENC peut utiliser 0 par défaut).  
`-rc-lookahead 32` : tampon de 32 images pour un meilleur contrôle de débit ; des valeurs plus élevées apportent des gains décroissants.  
`-multipass fullres` : apporte environ +10-15 % de qualité pour un temps d'encodage doublé ; intéressant pour l'archivage, à éviter pour le traitement par lots.

### Archivage HEVC (libx265, 10 bits pour les diapositives et le texte) {#hevc-archival-libx265-10-bit-for-slidetext-content}

```bash
ffmpeg -i input.mp4 \
  -c:v libx265 -preset slow -crf 22 \
  -pix_fmt yuv420p10le -tag:v hvc1 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

Le 10 bits réduit la posterisation et le banding sur les dégradés des diapositives ; le tag `hvc1` est requis pour la compatibilité Apple.

### hevc_nvenc par lots {#hevc_nvenc-bulk}

```bash
ffmpeg -i input.mp4 \
  -c:v hevc_nvenc -preset p6 -tune hq \
  -rc vbr -cq 26 -b:v 0 \
  -spatial-aq 1 -temporal-aq 1 -rc-lookahead 32 \
  -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### SVT-AV1 CPU (recommandé plutôt que libaom-av1) {#svt-av1-cpu-recommended-over-libaom-av1}

```bash
ffmpeg -i input.mp4 \
  -c:v libsvtav1 -preset 6 -crf 28 \
  -svtav1-params tune=0:lookahead=120 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

`tune=0` : mode de qualité VOD. `lookahead=120` : lookahead important pour la qualité ; le réduire à 32 pour gagner en vitesse.

### av1_nvenc (Ada, RTX 4000+) {#av1_nvenc-ada-rtx-4000}

```bash
ffmpeg -i input.mp4 \
  -c:v av1_nvenc -preset p6 -tune hq \
  -rc vbr -cq 30 -b:v 0 \
  -spatial-aq 1 -temporal-aq 1 \
  -c:a aac -b:a 128k -ac 1 -ar 48000 \
  -movflags +faststart \
  output.mp4
```

### Réduction de résolution (4K → 1080p) {#resolution-downscale-4k-1080p}

```bash
# Photographic / talking head — lanczos
ffmpeg -i input.mp4 -vf "scale=1920:-2:flags=lanczos" -c:v h264_nvenc ... output.mp4

# Screen recording / text slides — bicubic (less ringing)
ffmpeg -i input.mp4 -vf "scale=1920:-2:flags=bicubic" -c:v h264_nvenc ... output.mp4
```

`-2` : calcule la hauteur automatiquement en conservant le ratio ; garantit un nombre pair, requis par H.264.

### Audio : AAC pour la voix {#audio-aac-for-voice}

```bash
# Native AAC (universal builds) — adequate at 128k
-c:a aac -b:a 128k -ac 1 -ar 48000

# libfdk_aac (Fraunhofer, better quality especially <128k; requires non-free build)
-c:a libfdk_aac -b:a 96k -ac 1 -ar 48000 -afterburner 1

# Verify libfdk_aac availability
ffmpeg -encoders | grep fdk
```

Guide de débit AAC pour la voix en mono : 64k = streaming acceptable, 96k = minimum pour la distribution, 128k = compromis optimal pour l'archivage, 160k+ = gains décroissants.  
HE-AAC (`-profile:a aac_he`) est préférable en dessous de 64k, mais sa prise en charge par les lecteurs est moins bonne ; utiliser LC-AAC pour la compatibilité.

### Changement de tempo de la parole avec préservation des formants (Rubber Band R3) {#speech-tempo-change-with-formant-preservation-rubber-band-r3}

Pipeline en trois passes : extraction de l'audio, étirement R3, remultiplexage avec la vidéo accélérée :

```bash
# Pass 1: extract audio as lossless WAV
ffmpeg -y -i src.mp4 -vn -c:a pcm_s16le -ar 44100 -ac 1 audio.wav

# Pass 2: R3 time-stretch with formant preservation (-F mandatory for 3x speech)
rubberband-r3 -T 3 -F -q audio.wav audio_3x.wav
# -T 3   : 3x tempo (duration = original / 3)
# -F     : formant preserve — prevents gender-shift on extreme ratios
# -q     : quiet mode for batch

# Pass 3a: speed video only (no audio, use NVENC + AQ)
ffmpeg -y -i src.mp4 -an \
  -filter:v "setpts=PTS/3.0" \
  -c:v h264_nvenc -preset p6 -tune hq -cq 24 \
  -bf 2 -spatial-aq 1 -temporal-aq 1 \
  -movflags +faststart video_3x.mp4

# Pass 3b: mux speed-up video + R3 audio
ffmpeg -y -i video_3x.mp4 -i audio_3x.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy \
  -c:a aac -b:a 128k -ac 1 \
  -shortest \
  -movflags +faststart final_3x.mp4
```

`-shortest` aligne les durées des flux ; requis lorsque les longueurs vidéo et audio diffèrent de quelques millisecondes après l'étirement.

### Concaténation : chemin rapide (sans réencodage) {#concat-fast-path-no-re-encode}

Tous les clips doivent partager exactement le même codec, la même résolution, la même fréquence d'images, le même format de pixels et les mêmes paramètres audio :

```bash
# Build list file
printf "file '%s'\n" part1.mp4 part2.mp4 part3.mp4 > list.txt

# Demuxer concat — ~37x faster than re-encode
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# With regenerated timestamps (for speed-up outputs or AVI/MKV rips with corrupt PTS)
ffmpeg -fflags +genpts -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Concaténation : chemin par filtre (réencodage, paramètres mixtes) {#concat-filter-path-re-encode-mixed-params}

```bash
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v h264_nvenc -preset p6 -tune hq -cq 24 \
  -c:a aac -b:a 128k -ac 1 \
  -movflags +faststart output.mp4
```

À utiliser lorsque les clips diffèrent sur au moins un paramètre ; plus lent, mais gère toutes les combinaisons d'entrées.

## Référence de réglage NVENC {#nvenc-tuning-reference}

| Option | Valeurs | Effet |
|---|---|---|
| `-preset` | `p4` (à ignorer), `p5` lots, `p6` qualité, `p7` archivage | Compromis vitesse/qualité ; p7 reste plus rapide que libx264 medium |
| `-tune` | `hq` (toujours utiliser pour la qualité), `ll`/`ull` (latence uniquement) | `hq` obligatoire ; la valeur par défaut donne une qualité nettement inférieure |
| `-spatial-aq 1` | 0/1 | Plus de bits sur les zones spatiales complexes, moins sur les zones unies ; critique pour les diapositives |
| `-temporal-aq 1` | 0/1 | Plus de bits sur les images statiques (visage), moins sur le mouvement ; critique pour la tête parlante |
| `-rc-lookahead` | 32 (recommandé), 64 (gains décroissants) | Tampon d'images pour les décisions de contrôle de débit |
| `-bf` | 2-3 | Images B ; NVENC peut utiliser 0 par défaut, à définir explicitement pour les cours et contenus peu dynamiques |
| `-multipass fullres` | (option) | Deux passes en pleine résolution : +10-15 % de qualité, 2x le temps ; NVENC SDK 12+, archivage uniquement |

## Pièges {#gotchas}

- **Problème :** `af_rubberband=tempo=3.0` (intégré à ffmpeg) produit des artefacts métalliques ou robotiques à 3x sur la parole. **Solution :** Utiliser le CLI autonome Rubber Band R3 (`rubberband-r3 -T 3 -F`). La version intégrée utilise le moteur R2 ; même avec `formant=preserved`, R2 perd face à R3 sur la parole à des rapports élevés.

- **Problème :** `-movflags +faststart` omis : la vidéo met en tampon tout le fichier avant le début de la lecture, et la navigation échoue sur les flux HTTP. **Solution :** Toujours ajouter `-movflags +faststart` pour tout MP4 de distribution. Aucun inconvénient pour les fichiers locaux.

- **Problème :** la qualité NVENC déçoit sans `-tune hq` ; le tune par défaut équivaut à un mode non optimisé. **Solution :** Toujours spécifier `-tune hq` pour une cible de qualité ; l'omettre laisse une marge de qualité importante inexploitée, sans gain de vitesse.

- **Problème :** la sortie de `hevc_nvenc` refuse de se lire dans QuickTime/Safari (tag `hev1` non reconnu). **Solution :** Ajouter `-tag:v hvc1` pour forcer le bon tag ; cela s'applique à tout HEVC dans un MP4 destiné à Apple.

- **Problème :** `ffmpeg -f concat -c copy` produit une dérive de synchronisation audio/vidéo lorsque les fichiers sources ont un PTS de départ non nul (courant dans les sorties accélérées ou les extractions MKV). **Solution :** Ajouter `-fflags +genpts` pour régénérer les horodatages : `ffmpeg -fflags +genpts -f concat -safe 0 -i list.txt -c copy out.mp4`.

- **Problème :** une CQ trop basse (agressive) sur NVENC produit des blocs et du ringing visibles sur le texte et les dégradés des diapositives. **Solution :** Pour un contenu de cours ou de diapositives en 1080p, utiliser CQ 24-26 pour H.264 et CQ 26-28 pour HEVC. CQ 18 ou moins donne un résultat quasi sans perte, mais la taille du fichier croît de façon exponentielle ; c'est inutile pour du contenu d'écran.

- **Problème :** l'échelle CRF de `libsvtav1` n'est pas la même que celle de x264/x265 ; reporter directement une valeur CRF produit des résultats très différents. **Solution :** SVT-AV1 CRF 28-32 ≈ x265 CRF 22 ≈ x264 CRF 16-18 pour une qualité perceptuelle équivalente sur un contenu courant.

- **Problème :** `atempo=3.0` dans une chaîne de filtres audio ffmpeg produit une parole intelligible mais de faible qualité à 3x ; le lissage du vocodeur de phase est audible. **Solution :** Ne pas utiliser `atempo` au-delà de 2x pour la parole ; utiliser plutôt le pipeline autonome Rubber Band R3.

## Voir aussi {#see-also}

- [[bash-scripting]] - boucles de traitement par lots pour les tâches d'encodage multi-fichiers
- [[io-redirection-and-pipes]] - rediriger la sortie de ffmpeg, journaliser la progression de l'encodage
- [[monitoring-and-performance]] - surveillance de l'utilisation GPU pendant l'encodage NVENC (`nvidia-smi dmon`)
- [[disks-and-filesystems]] - organisation du stockage pour les grandes archives vidéo
- [Documentation FFmpeg sur les codecs](https://ffmpeg.org/ffmpeg-codecs.html)
- [Documentation FFmpeg sur le scaler](https://ffmpeg.org/ffmpeg-scaler.html)
- [Wiki FFmpeg : Encode/AV1](https://trac.ffmpeg.org/wiki/Encode/AV1)
- [Wiki FFmpeg : Encode/AAC](https://trac.ffmpeg.org/wiki/Encode/AAC)
- [Bibliothèque audio Rubber Band](https://breakfastquay.com/rubberband/)
- [Préréglages NVIDIA Video Codec SDK](https://developer.nvidia.com/blog/introducing-video-codec-sdk-10-presets/)
- [Analyse des presets SVT-AV1 — OTTVerse](https://ottverse.com/analysis-of-svt-av1-presets-and-crf-values/)
- [Guide CRF — slhck.info](https://slhck.info/video/2017/02/24/crf-guide.html)
