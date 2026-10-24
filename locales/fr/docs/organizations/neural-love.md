---
title: "neural.love — génération d'images par IA et entraînement de modèles"
category: organizations
date: 2022-11-15
tags: [ai-creation-and-model-training, neural-love, neural_love, organization]
aliases: ["Neural.love", "neural.love"]
level: 3
source_sha256: bd99f44ea59b755ec2c80f34ee1e2bf50003f515578dba761cd572fac0bbec3c
translation: machine
translated_at: '2026-10-24'
---
# neural.love — création par IA et entraînement de modèles {#neurallove-ai-creation-and-model-training}

**Ligne de développement :** `organization:neural-love` · fil `ai-creation-and-model-training`  
**Dernier événement :** 2022-11-15 · 2 événements datés depuis 2022-08-17 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

neural.love est une plateforme web et API destinée aux créateurs qui ont besoin de génération d'images par IA, d'amélioration ou de restauration d'images, d'outils liés à la vidéo et de transformations photo.

- AI Art Generator : génération avec options de modèle, de style, de prompt, de mise en page, de HD et d'image en entrée.
- AI Photo Studio : transformations d'une seule photo.
- API d'entraînement de modèles personnalisés : flux de travail pour entraîner des modèles de génération d'art par IA personnalisés.

La limite par défaut documentée de l'API est de 300 requêtes par cinq minutes, et la génération consomme des crédits.

La plateforme sert un usage créatif actuel et des intégrations délimitées, mais il faut vérifier la propriété et le support avant d'en faire une nouvelle dépendance de production à long terme.

## Ligne de développement {#development-line}

- **2022-08-17 — neural.love marque une étape sur le générateur d'art par IA.** Le 2022-08-17, neural.love a publié un lien vers son générateur d'art par IA, ce qui constitue une étape publique de développement produit pour son offre de création d'images par IA.
- **2022-11-15 — neural.love marque une étape sur l'entraînement de modèles.** Le 2022-11-15, neural.love a publié un lien vers sa page d'entraînement de modèles, étendant sa gamme publique de la génération d'art par IA à un flux de travail d'entraînement de modèles.

## Ce qui a changé {#what-changed}

neural.love — les liens datés établissent des routes produit, et non des annonces de lancement vérifiées.

2022-08-17 — la route AI Art Generator était présente.

2022-11-15 — la route Train a Model était présente ; les éléments disponibles n'établissent pas ses entrées, son type de modèle ni ses sorties historiques.

Constaté aujourd'hui (2026-09-04) — la route AI Art Generator reste active. Train a Model redirige vers AI Photo Studio, tandis que l'entraînement de modèles personnalisés reste documenté via l'API. Un avis daté du 12 mars 2026 indique que les actifs sont à vendre et que le propriétaire ne prévoit pas d'investissement significatif supplémentaire.

Ne lisez pas les deux dates de 2022 comme deux lancements de fonctionnalités confirmés.

## Comment l'utiliser {#how-to-use-this}

Au 2022-08-17, les praticiens doivent reconnaître le générateur d'art par IA de neural.love comme faisant partie de sa gamme produit. Au 2022-11-15, ils doivent aussi évaluer son flux d'entraînement de modèles lorsqu'ils analysent les capacités de création de l'organisation.

1. Ouvrez AI Art Generator, choisissez un modèle et un style, affinez le prompt et générez une image dans le navigateur.
  — <https://neural.love/ai-art-generator>
2. Utilisez AI Photo Studio lorsque la tâche consiste à transformer une seule photo plutôt qu'à suivre un flux de modèle personnalisé.
  — <https://neural.love/ai-photostudio>
3. Pour l'automatisation, connectez-vous, ouvrez Settings, générez le jeton API et envoyez-le dans l'en-tête Authorization Bearer.
  — <https://docs.neural.love/>
4. Construisez une demande d'art avec prompt, style, mise en page, quantité et choix HD ou visibilité ; estimez les crédits avant d'envoyer la demande de génération et conservez son identifiant de commande.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
5. Interrogez la commande à intervalles croissants jusqu'à ce que status.isReady soit vrai, puis récupérez le résultat.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
6. Pour un modèle d'art par IA personnalisé, appelez /ai-art/custom-model/create, attendez la fin de l'entraînement, puis utilisez le modèle dans /ai-art/generate.
  — <https://docs.neural.love/reference/ai-custom-model-generate>

## Bonnes pratiques {#best-practices}

- Estimez le coût en crédits avant chaque lot facturé ; le coût varie selon le nombre d'images, la visibilité et le mode HD.
  — <https://docs.neural.love/>
- Conservez l'identifiant de commande et utilisez des intervalles croissants pour les vérifications de statut plutôt qu'un interrogation serrée.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- Sécurisez et coordonnez la rotation des jetons API : un seul jeton est actif par compte, et la création d'un nouveau jeton désactive le précédent.
  — <https://docs.neural.love/>
- Traitez la confidentialité comme un paramètre au niveau du compte à vérifier avant d'envoyer des médias sensibles : le guide API et la FAQ décrivent des valeurs par défaut différentes pour les résultats publics et privés.
  — <https://docs.neural.love/faq>
- Limitez les tentatives et traitez le code HTTP 429 comme une réponse normale de limitation de débit, dans la limite par défaut documentée de 300 requêtes par cinq minutes.
  — <https://docs.neural.love/>
- Avant de créer une nouvelle dépendance de production, confirmez la propriété actuelle, le support et la portabilité des résultats, car le propriétaire a annoncé une vente d'actifs et de propriété intellectuelle.
  — <https://neural.love/blog/neural-love-is-for-sale>

## Remplacé par ce document {#superseded-by-this}

- 2022-11-15 — Considérer l'ancienne route Train a Model comme la page active d'entraînement de modèles personnalisés destinée aux utilisateurs est obsolète : elle redirige désormais vers AI Photo Studio ; l'entraînement de modèles personnalisés actuel est documenté via l'API.
- Avant le 2026-03-12 — Planifier en supposant un investissement continu et significatif du fournisseur est une recommandation obsolète : le propriétaire indique qu'il poursuit une vente d'actifs et de propriété intellectuelle.

## Points encore inconnus {#still-unknown}

- Le texte complet associé aux deux dates de 2022 n'est pas disponible ; aucune de ces dates ne prouve un lancement, un changement de tarification ou une publication de modèle.
- Les liens 2022 vers l'art par IA et Train a Model peuvent décrire des flux produit distincts au sein de la même entreprise ; la redirection actuelle ne prouve pas ce qu'était le flux d'entraînement historique.
- L'avis de vente du 12 mars 2026 n'établit pas si une vente a été conclue, qui exploite désormais le service, ni les conditions actuelles de support et de conservation des données.
- La documentation officielle est contradictoire sur la visibilité par défaut de l'API ; le paramètre de confidentialité effectif doit donc être vérifié au niveau du compte, avec des données non sensibles.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://neural.love/blog/neural-love-is-for-sale | Les actifs de neural.love sont à vendre | blog neural.love sur l'IA | 2026-09-04 |
| https://docs.neural.love/ | Prise en main | Le hub développeur API de neural.love | 2026-09-04 |
| https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api | Comment générer de l'art par IA avec l'API neural.love | Le hub développeur API de neural.love | 2026-09-04 |
| https://docs.neural.love/reference/ai-custom-model-generate | Démarrer l'entraînement d'un modèle personnalisé | Le hub développeur API de neural.love | 2026-09-04 |
| https://docs.neural.love/faq | API neural.love - Foire aux questions | Le hub développeur API de neural.love | 2026-09-04 |
| https://neural.love/ai-art-generator | AI Art Generator & AI Image Generator | neural.love | 2026-09-04 |
| https://neural.love/train-a-model | AI Photo Studio | Créez instantanément de superbes photos et vidéos IA | neural.love | 2026-09-04 |
| https://neural.love/ai-photostudio | AI Photo Studio | Créez instantanément de superbes photos et vidéos IA | neural.love | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `organization:neural-love`, fil `ai-creation-and-model-training`, 2 événements datés du 2022-08-17 au 2022-11-15.
- **Note pratique :** Au 2022-08-17, les praticiens doivent reconnaître le générateur d'art par IA de neural.love comme faisant partie de sa gamme produit ; au 2022-11-15, ils doivent aussi évaluer son flux d'entraînement de modèles lorsqu'ils analysent les capacités de création de l'organisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
