---
title: "Calibration de perspective pour l'incrustation d'objets"
description: "Un cadre de décision local pour estimer la géométrie de la caméra, la valider à l'aide des indices de la scène, et en dériver une transformation de placement stable avant d'incruster un objet."
level: 3
source_sha256: 75f29b17bd86bc31ac8fcd60ade7e681d996d708768f391c4e34d4856bedd7da
translation: machine
translated_at: '2026-10-24'
---
# Calibration de perspective pour l'incrustation d'objets {#perspective-calibration-for-object-compositing}

La calibration de perspective est l'étape géométrique qui précède l'incrustation d'objets. Son résultat est une hypothèse défendable sur la caméra et le plan d'appui : paramètres intrinsèques `K`, orientation de la caméra, horizon et application plane. Elle ne fait pas correspondre un détourage à la scène ; elle empêche un compositeur ultérieur d'essayer de masquer une échelle, une inclinaison ou un point de contact impossibles.

Utilisez la calibration lorsque l'objet inséré doit reposer sur une surface plane, partager des arêtes convergentes ou rester plausible après un léger repositionnement. Pour un graphique plat placé parallèlement au plan image, utilisez plutôt une transformation 2D. Pour un objet qui doit être vu sous un angle sensiblement différent, acquérez ou rendez une vue correspondante ; une calibration à partir d'une seule image ne permet pas de retrouver une géométrie cachée.

## Déterminer ce qui doit être estimé {#decide-what-must-be-estimated}

Partez du montage, et non du modèle :

- **Placement uniquement sur un plan connu :** estimez `K`, l'orientation et une homographie du plan d'appui. C'est le cas courant du produit posé au sol, de l'enseigne sur un mur ou du meuble posé sur le sol.
- **Architecture visible ou marquages routiers :** extrayez les lignes et exigez une concordance entre leurs directions de fuite et l'estimation de la caméra.
- **Contexte faible, courbe ou uniquement texturé :** utilisez une estimation apprise à partir d'une seule image comme proposition, mais exigez un horizon ou des ancrages manuels, ou une seconde image, avant de valider un placement à forts enjeux.
- **Besoin de l'orientation locale des surfaces ou de l'occlusion :** ajoutez une profondeur ou des normales monoculaires après la calibration de la caméra. Considérez leur échelle comme incertaine, sauf si la source fournit des contraintes métriques compatibles avec la scène.
- **Distorsion en barillet ou fisheye marquée :** rectifiez d'abord l'image ou choisissez un modèle de caméra qui la représente. Une estimation sténopé sur une image visiblement déformée n'est pas un échec de calibration qu'un compositeur pourrait réparer.

Le livrable minimal n'est pas une valeur de distance focale. Conservez les dimensions de l'image, le modèle de caméra, `K`, la convention de rotation, l'horizon, la définition du plan d'appui, les ancrages et une superposition de validation. Ces artefacts rendent la transformation de l'objet reproductible et signalent quand un recadrage ou un redimensionnement ultérieur la rend invalide.

## Choix des outils et frontière juridique {#tool-selection-and-legal-boundary}

Le tableau est volontairement court : choisissez un estimateur pour l'inconnue, puis une source de preuves distincte pour la validation. Le « dernier signe d'activité » est la valeur `pushed_at` du dépôt GitHub, vérifiée le **21 août 2026** ; elle indique la récence de la maintenance, et non la précision. Les conditions du code et celles des points de contrôle (checkpoints) sont des éléments distincts et doivent être consignées séparément dans un manifeste de publication.

| Rôle | Utiliser lorsque | Interface ou sortie locale | Licence du code | Conditions des poids ou points de contrôle | Activité vérifiée le 21 août 2026 |
|---|---|---|---|---|---|
| [GeoCalib](https://github.com/cvg/GeoCalib) | Proposition par défaut d'intrinsèques et de gravité à partir d'une seule image | `GeoCalib().calibrate(image)` renvoie la caméra, la gravité et des champs de covariance ou de confiance ; modèles sténopé et de la famille radiale | Apache-2.0 | Le dépôt officiel télécharge les artefacts `pinhole`/`distorted` depuis sa version publiée sur GitHub. Aucune licence distincte pour les points de contrôle n'était indiquée dans le README ou le fichier LICENSE du dépôt au moment de la vérification ; examinez l'artefact exact de la version avant toute redistribution. | 16 août 2026 |
| [DeepLSD](https://github.com/cvg/DeepLSD) | Segments de droites précis de la scène et preuves indépendantes de points de fuite | segments de droites ; l'export du dépôt prend en charge `--pred_vps` | MIT | Les points de contrôle officiels sont hébergés sur `cvg-data.inf.ethz.ch` ; aucune licence distincte pour les poids n'est indiquée dans le README. | 9 janvier 2025 |
| [CTRL-C](https://github.com/jwlee-vcl/CTRL-C) | Proposition de calibration indépendante conditionnée par les lignes | points de fuite, distance focale, ligne d'horizon à partir de l'image et de segments de droites | Apache-2.0 | Les points de contrôle officiels sont liés depuis Google Drive ; la licence du dépôt couvre le code, mais des conditions distinctes pour les points de contrôle n'y sont pas indiquées. | 25 juin 2024 |
| [MoGe](https://github.com/microsoft/MoGe) | Besoin de profondeur, de normales, d'intrinsèques et de champ de vision pour construire les preuves de support et d'occlusion | carte de points, profondeur, normales, intrinsèques normalisés | MIT ; le sous-arbre DINOv2 inclus est sous Apache-2.0 | La fiche modèle officielle `Ruicheng/moge-2-vitl-normal` déclare `mit` à la date de vérification. Revérifiez la fiche modèle précise et chaque dépendance pour la révision choisie. | 19 août 2026 |

Pour un pipeline distribuable commercialement, ne retenez un outil qu'après avoir rattaché la **révision exacte du code et le point de contrôle exact téléchargé** à leurs conditions applicables respectives. « Dépôt ouvert » et « point de contrôle téléchargeable » ne constituent pas des classifications de licence.

## Pipeline de calibration {#calibration-pipeline}

1. **Normaliser la source.** Conservez séparément les pixels d'origine et les métadonnées EXIF. Consignez tout recadrage, redimensionnement, rotation ou correction d'objectif. Exécutez l'inférence sur la même matrice de pixels que celle utilisée pour le placement ; sinon, transformez `K` et tous les ancrages selon la même transformation d'image.
2. **Choisir le modèle de caméra.** Commencez par le modèle sténopé pour les images rectilignes. Passez à un modèle radial uniquement lorsque les arêtes droites de la scène se courbent visiblement ; n'utilisez pas un paramètre de distorsion supplémentaire simplement pour absorber de mauvais ancrages.
3. **Générer une proposition de caméra.** Estimez les intrinsèques et la gravité avec GeoCalib, en enregistrant les paramètres de la caméra ainsi que les sorties de covariance ou de confiance. GeoCalib suppose que le point principal est centré et ne l'optimise pas ; traitez donc les images fortement recadrées ou décentrées comme un cas à examiner.
4. **Extraire une géométrie indépendante.** Exécutez DeepLSD, regroupez les longues lignes cohérentes par direction, puis comparez les directions de fuite obtenues à l'horizon et à la rotation prédits. Sur les scènes structurées, exécutez CTRL-C comme proposition indépendante plutôt que de moyenner aveuglément les sorties.
5. **Accepter, réviser ou arrêter.** N'acceptez que si les familles d'arêtes parallèles visibles, l'horizon et les verticales connues concordent dans la tolérance de l'image retenue pour le montage. Si les indices sont contradictoires, examinez la distorsion de l'objectif, l'historique de recadrage, les arêtes « de référence » non planes et le choix des lignes avant de changer de modèle.
6. **Construire le plan d'appui.** Définissez un système de coordonnées local au plan à partir d'au moins trois ancrages visibles, puis dérivez une homographie plan-vers-image. Un rendu utilise la projection de la caméra ; un gauchissement 2D utilise la même homographie du plan. Conservez les dimensions physiques de l'objet dans le système de coordonnées du plan, plutôt que d'ajuster une échelle dans l'espace image à l'œil.
7. **Placer et valider.** Projetez une boîte, une empreinte ou un fil de fer avant de rendre les pixels. Vérifiez le point de contact, la hauteur, la direction verticale, l'ordre d'occlusion et la direction de l'ombre portée par rapport à la source. Ce n'est qu'ensuite que l'élément placé peut passer à la composition alpha, au détourage, au ré-éclairage ou à l'harmonisation générative.

Pour un plan `Z = 0` en coordonnées monde, un placement projectif s'écrit :

```text
p ~ K [r1 r2 t] [X Y 1]^T
H_plane = K [r1 r2 t]
```

`~` signifie égalité à un facteur d'échelle près. L'équation n'est valable que pour les points du plan déclaré. Elle ne doit pas servir à « faire pivoter » un objet volumétrique vers une nouvelle vue.

## Contrat de configuration pratique {#practical-configuration-contract}

Il s'agit d'une configuration au niveau de l'application, et non d'une ligne de commande acceptée par les projets amont. Elle rend explicite chaque décision ainsi que la revue ultérieure.

```yaml
source:
  image: scene.png
  raster_size_px: [4032, 3024]
  image_transform: identity          # crop/resize/rectification chain; never implicit
camera:
  estimator: geocalib
  camera_model: pinhole              # use simple_radial only after visible-distortion review
  principal_point: image_center_assumed
  save: camera.json                  # K, orientation, gravity, covariance, source hash
evidence:
  lines:
    detector: deeplsd
    minimum_length_px: 160
    use_for: [horizon_check, vanishing_direction_check]
  independent_estimate:
    estimator: ctrl-c
    required_for: high_value_structured_scene
acceptance:
  horizon_residual_px_max: 12        # edit-specific; compare at final raster size
  vertical_edge_angle_error_deg_max: 2
  require_two_consistent_edge_families: true
placement:
  support_plane: floor
  anchors_px: [[491, 2210], [2108, 2160], [2999, 1894]]
  object_size_m: [0.42, 0.18, 0.12]
  export: [placement.json, validation-overlay.png]
```

Les seuils sont des points de contrôle de revue, et non des affirmations universelles de précision. Resserrez-les pour une arête architecturale proéminente ; ne les relâchez que moyennant une justification écrite pour une image à faible saillance. Stockez une superposition montrant l'horizon, les directions de fuite ajustées, les ancrages, l'empreinte de l'objet et les verticales de référence, afin qu'un opérateur puisse rejeter un résultat invraisemblable sans avoir à interpréter les matrices brutes.

## Logique de validation {#validation-logic}

Utilisez des observations indépendantes plutôt qu'une unique « confiance » scalaire :

- **Test de l'horizon :** l'horizon projeté suit au moins deux longues familles d'arêtes parallèles dans le monde, lorsqu'elles sont visibles.
- **Test de la verticale :** la direction verticale du monde se projette dans le même sens que les verticales fiables ; excluez les objets penchés et le roulis dû à une caméra tenue à la main, sauf si leur pose est intentionnelle.
- **Test de l'empreinte :** tous les points de contact se situent sur le plan déclaré, et la variation d'échelle est monotone avec la profondeur.
- **Test d'occlusion :** une frontière de scène au premier plan masque l'objet avant le début de la synthèse de couleur, d'ombre ou de texture.
- **Test d'éclairage :** l'ombre de contact part de l'empreinte et suit une direction cohérente avec la source. La cohérence de l'éclairage est distincte de la calibration de la caméra.

Lorsqu'une estimation projective est légèrement erronée, réajustez-la sur des repères explicites en gardant le modèle de caméra fixe. Lorsque le résidu présente une courbure systématique, revoyez la distorsion ou le prétraitement de la source ; ne compensez pas en déplaçant uniquement l'objet.

## Pièges {#gotchas}

- **Le recadrage invalide les intrinsèques :** `K` appartient à un système de coordonnées pixel donné. Un recadrage modifie le point principal ; un redimensionnement met à l'échelle les distances focales et le point principal. **Correction :** conservez la chaîne des transformations d'image et mettez à jour l'ensemble des artefacts de calibration simultanément.
- **Fausses lignes parallèles :** les arêtes d'étagères, les lignes de toit et les joints de chaussée peuvent ne pas être parallèles en 3D, ou se courber sous l'effet de la distorsion de l'objectif. **Correction :** utilisez plusieurs longues familles d'arêtes et rejetez les groupes qui contredisent la structure connue de la scène.
- **Hypothèse sur le point principal :** l'hypothèse documentée de GeoCalib, à savoir un point principal centré, peut biaiser un recadrage décentré. **Correction :** utilisez l'image non recadrée lorsqu'elle est disponible, contraignez manuellement la géométrie, ou signalez le résultat comme une proposition plutôt que comme une caméra définitive.
- **La profondeur n'est pas une règle par défaut :** une carte de profondeur monoculaire peut fournir un ordre et des normales utiles sans fixer l'échelle absolue de l'objet. **Correction :** ancrez l'échelle sur une dimension connue de la scène ou sur un plan calibré.
- **Un bon détourage ne corrige pas la parallaxe :** des bords alpha propres, le remplissage ou l'harmonisation ne peuvent pas faire apparaître une vue de profil à partir d'un élément conçu de face. **Correction :** acquérez une vue compatible ou utilisez un actif 3D et effectuez le rendu avec la caméra ajustée.
- **Les conditions peuvent diverger :** les conditions du code du dépôt ne licencient pas automatiquement les points de contrôle, les données d'entraînement ou un backbone inclus. **Correction :** consignez chaque artefact téléchargé, sa révision et l'URL de sa licence ou de sa fiche modèle dans le manifeste de publication.

## Limites {#limitations}

La calibration à partir d'une seule image est sous-contrainte. Les motifs répétitifs, un champ de vision limité, une faible résolution, l'obturateur déroulant, un flou important, les reflets et les scènes sans lignes droites fiables peuvent donner lieu à plusieurs caméras plausibles. Les estimations apprises peuvent constituer des propositions utiles, mais elles n'établissent pas de vérité terrain. Ni une homographie ni la profondeur ou les normales ne permettent de retrouver les surfaces cachées, la réponse matérielle propre à l'objet, ni une source lumineuse physiquement correcte.

Ce pipeline sépare également délibérément la géométrie de la finition. Utilisez [[intrinsic-decomposition]] pour le raisonnement sur l'éclairage et l'albédo, [[color-checker-and-white-balance]] pour la mesure de couleur, [[videomama-diffusion-based-video-matting]] pour l'affinement alpha, et [[spatialedit-16b-geometric-control-for-diffusion-based-image-editing]] lorsqu'un modèle d'édition d'image est envisagé une fois le placement géométrique fixé.

## Sources primaires {#primary-sources}

- [Dépôt et API d'inférence de GeoCalib](https://github.com/cvg/GeoCalib), [licence Apache-2.0](https://github.com/cvg/GeoCalib/blob/main/LICENSE) et [publication des points de contrôle v1.0](https://github.com/cvg/GeoCalib/releases/tag/v1.0).
- [Dépôt DeepLSD](https://github.com/cvg/DeepLSD) et [licence MIT](https://github.com/cvg/DeepLSD/blob/main/LICENSE).
- [Dépôt CTRL-C](https://github.com/jwlee-vcl/CTRL-C) et [licence Apache-2.0](https://github.com/jwlee-vcl/CTRL-C/blob/main/LICENSE).
- [Dépôt MoGe](https://github.com/microsoft/MoGe), [licence du code](https://github.com/microsoft/MoGe/blob/main/LICENSE) et [fiche modèle MoGe-2 ViT-L normal](https://huggingface.co/Ruicheng/moge-2-vitl-normal).
