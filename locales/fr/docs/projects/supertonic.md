---
title: "Supertonic — Référence de projet public"
category: projects
date: 2026-05-18
tags: [project, public-project-reference, supertonic]
aliases: ["Supertonic"]
level: 2
source_sha256: b8209c813e5a50c276e7949bddc5586982a8dba4bc95aeb80ba9058573b0761b
translation: machine
translated_at: '2026-10-24'
---
# Supertonic — Référence de projet public {#supertonic-public-project-reference}

**Ligne de développement :** `project:supertonic` · fil `public-project-reference`  
**Dernier événement :** 2026-05-18 · 1 événement daté depuis le 2026-05-18 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Supertonic — une pile de synthèse vocale basée sur ONNX Runtime, destinée aux développeurs qui ont besoin d'une alternative auto-hébergée aux API TTS hébergées.

- SDK Python, CLI et serveur HTTP en boucle locale (loopback)
- Supertonic-3 avec 31 codes de langue plus le repli `na`
- dix styles de voix intégrés et import JSON de Voice Builder

## Ligne de développement {#development-line}

- **2026-05-18 — Référence au dépôt public de Supertonic.** Le 2026-05-18, le fil Supertonic a renvoyé vers le dépôt GitHub public du projet, accompagné d'une référence à la source. Cela établit un point de référence public daté pour le projet, sans affirmer de version, de fonctionnalité ou de modification de code particulière.

## Ce qui a changé {#what-changed}

- 2025-12-10 — le paquet Python et six styles de voix intégrés supplémentaires ont été ajoutés.
- 2026-01-06 — Supertonic 2 a étendu le modèle de l'anglais à cinq langues ; sa voie de code est restée sur une branche de publication.
- 2026-01-22 — Voice Builder a été mis en service pour des profils de voix personnalisés persistants.
- 2026-04-29 — Sortie de Supertonic 3 avec la prise en charge de 31 langues, des améliorations de la stabilité de lecture et une interface ONNX publique compatible avec la v2.
- 2026-05-18 — Le SDK Python 1.3.1 a ajouté l'interface HTTP locale `supertonic serve` ; Voice Builder a ajouté les profils JSON de Supertonic-3.
- 2026-05-20 — Supertonic 3 est devenu disponible dans Supertone Play et dans l'API Supertone.

## Comment l'utiliser {#how-to-use-this}

Commencez par le dépôt GitHub public référencé à la date du 2026-05-18. Nous ne disposons d'aucune preuve justifiant des recommandations d'adoption propres à une version.

1. Installez `supertonic` ; utilisez Python 3.9 ou une version ultérieure.
  — <https://pypi.org/project/supertonic/>
2. Créez `TTS(auto_download=True)`, sélectionnez une voix intégrée, synthétisez le texte et enregistrez la sortie WAV.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
3. Transmettez un code de langue ISO pris en charge lorsque celui-ci est connu, ou `na` pour un traitement indépendant de la langue.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
4. Pour les clients HTTP, installez `supertonic[serve]`, exécutez `supertonic serve --host 127.0.0.1 --port 7788`, puis appelez `/v1/tts` ou `/v1/audio/speech`.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>

## Bonnes pratiques {#best-practices}

- Commencez avec la valeur par défaut de huit étapes de synthèse, puis mesurez le compromis entre qualité et latence. Les réglages vont de 5 à 12 étapes, et la vitesse de 0,7 à 2,0.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Téléchargez à l'avance le fichier de modèle d'environ 400 Mo lors de la configuration de l'intégration continue ou du déploiement, afin que la première requête en production ne subisse pas le coût du téléchargement.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Gardez `supertonic serve` sur la boucle locale par défaut. Ne l'exposez que derrière un reverse proxy.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Distinguez les obligations de licence et de consentement liées au modèle de la licence MIT du code source Python, en particulier lors de l'import d'un profil de voix personnalisé.
  — <https://github.com/supertone-inc/supertonic-py/blob/main/llms.txt>
- Testez la latence avec les lecteurs d'écran ainsi que la lecture des nombres propre à chaque langue avant tout déploiement en accessibilité. Un utilisateur turc de NVDA a signalé des retards et des échecs de prononciation des chiffres après la sortie de la v3.
  — <https://github.com/supertone-inc/supertonic/issues/144>

## Remplacé par {#superseded-by-this}

- 2026-04-29 — Supertonic 3 remplace la recommandation Supertonic 2 à cinq langues pour les nouveaux déploiements multilingues. Il prend en charge 31 langues et conserve l'interface ONNX publique compatible avec la v2. Supertonic 2 reste utilisé pour les intégrations existantes sur sa branche de publication.
- 2026-05-18 — L'intégration Python embarquée n'est plus la seule voie d'intégration officielle. Le SDK 1.3.1 a ajouté une façade HTTP locale, tandis que l'usage embarqué reste valable là où il est plus simple.

## Points toujours inconnus {#still-unknown}

- Nous n'avons trouvé aucune documentation de première main en chinois simplifié dans la piste de recherche chinoise consultée. Les documents de première main examinés étaient en anglais ou en coréen, ce qui n'exclut pas l'existence d'une telle page.
- PyPI répertorie à la fois les versions 1.3.0 et 1.3.1 au 2026-05-18. Nous n'avons trouvé aucune note de version permettant de considérer la 1.3.0 comme un événement de développement distinct.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/supertone-inc/supertonic | GitHub - supertone-inc/supertonic: Lightning-Fast, On-Device, Multilingual TTS — running natively via ONNX. | 2026-09-05 |
| https://pypi.org/project/supertonic/ | supertonic · PyPI | 2026-09-05 |
| https://supertone-inc.github.io/supertonic-py/quickstart/ | Quick Start - supertonic-py | 2026-09-05 |
| https://github.com/supertone-inc/supertonic-py/blob/main/llms.txt | supertonic-py/llms.txt at main · supertone-inc/supertonic-py | 2026-09-05 |
| https://www.supertone.ai/en/work/faster-and-more-accurate-across-31-languages----introducing-supertonic-3 | Faster and more accurate across 31 languages — introducing Supertonic 3! | Supertone | 2026-09-05 |
| https://supertonic3.github.io/ | Supertonic 3 — Lightning-Fast, On-Device, Multilingual TTS | 2026-09-05 |
| https://github.com/supertone-inc/supertonic/issues/144 | supertonic tts turkish language and screen readers · Issue #144 | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:supertonic`, fil `public-project-reference`, 1 événement daté du 2026-05-18 au 2026-05-18.
- **Remarque pratique :** Commencez par le dépôt GitHub public référencé à la date du 2026-05-18. Nous ne disposons d'aucune preuve justifiant des recommandations d'adoption propres à une version.
- **Confiance :** élevée. Les mentions de remplacement datées ci-dessus font foi pour ce qui est devenu obsolète.
