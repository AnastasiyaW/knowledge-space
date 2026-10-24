---
title: "Latent-to-4D — Au-delà des pixels"
category: projects
date: 2026-08-13
tags: [beyond-pixels, latent-to-4d, latent_to_4d, project]
aliases: ["Latent-to-4D"]
level: 2
source_sha256: c39e57cf8849a7ab4cec5b991b58d4a4ac363902dd94b51231feafc47b68ccf8
translation: machine
translated_at: '2026-10-24'
---
# Latent-to-4D — Au-delà des pixels {#latent-to-4d-beyond-pixels}

**Ligne de développement :** `project:latent-to-4d` · fil `beyond-pixels`  
**Dernier événement :** 2026-08-13 · 1 daté depuis le 2026-08-13 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Latent-to-4D est une méthode de recherche issue de Beyond Pixels pour la génération de 4D à partir de texte ou d'image. L4AR prend le latent final d'un DiT vidéo compatible et produit des caméras ainsi que des cartes de points dynamiques dans l'espace monde. Les points de contrôle ne se transfèrent d'un DiT à l'autre qu'à l'intérieur d'un VAE partagé. Le code, les poids et un flux de travail d'inférence ne sont pas encore publiés. Nous suivons le projet et évaluons ses résultats ; nous ne pouvons pas le déployer de manière reproductible aujourd'hui.

## Ligne de développement {#development-line}

- **2026-08-13 — Enregistrement de la page du projet Beyond Pixels et du dépôt source.** Le 2026-08-13, la ligne de développement Latent-to-4D a enregistré des liens vers la page du projet Beyond Pixels et vers son dépôt source. Cela établit un artefact de projet public accompagné d'un emplacement d'implémentation.

## Ce qui a changé {#what-changed}

2026-08-13 — La page du projet et le dépôt établissent Latent-to-4D comme une méthode directe de génération latent-vers-4D. La source indique que l'article, la page et le dépôt sont devenus disponibles le 2026-08-11, tandis que le code d'inférence, le code d'entraînement et les poids pré-entraînés sont encore en préparation. Le modèle est entraîné sur environ 1 000 clips de 81 images et revendique un gain de +2,88 à +5,81 en projection-based DINO-F1 par rapport à Wan+4RC. Ce gain ne démontre pas la précision métrique de la géométrie 4D.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-13, considérez Beyond Pixels comme une référence de projet Latent-to-4D disposant à la fois d'une page de projet publique et d'un dépôt source. Validez les méthodes et leur utilisation directement à partir des artefacts liés avant de les adopter.

1. Ouvrez la galerie interactive pour vérifier si les caméras et les cartes de points dynamiques conviennent à la tâche ; les démonstrations couvrent des exemples de 4D par texte, par image et contrôlés.
  — <https://hayd-zju.github.io/Beyond-Pixels/>
2. Ne planifiez pas d'exécutions reproductibles avant la publication du code d'inférence et des poids : le dépôt ne contient qu'un README et indique que les deux sont en préparation.
  — <https://github.com/hayd-zju/Beyond-Pixels>

## Bonnes pratiques {#best-practices}

- Considérez la compatibilité comme limitée : vérifiez que le DiT vidéo source partage un VAE avec Latent-to-4D avant toute intégration.
  — <https://arxiv.org/abs/2608.10744>
- Ne transformez pas les démonstrations de contrôle de mouvement, de manipulation ou de navigation en affirmations de réussite physique : les auteurs les décrivent uniquement comme des vérifications de compatibilité d'interface.
  — <https://hayd-zju.github.io/Beyond-Pixels/>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

- Aucun code d'inférence, code d'entraînement, poids pré-entraînés, instructions d'installation, licence, exigences matérielles ni mesures reproductibles de temps d'exécution n'étaient disponibles sur le dépôt officiel au moment de la lecture.
- L'ajout daté du 2026-08-13 est conservé dans what_changed ; la soumission arXiv datée séparément est celle du 2026-08-11.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://hayd-zju.github.io/Beyond-Pixels/ | Beyond Pixels: From Video Priors to 4D Worlds — page du projet | 2026-09-05 |
| https://github.com/hayd-zju/Beyond-Pixels | Beyond-Pixels — dépôt officiel | 2026-09-05 |
| https://arxiv.org/abs/2608.10744 | Beyond Pixels: From Video Priors to 4D Worlds — arXiv | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:latent-to-4d`, fil `beyond-pixels`, 1 événement daté du 2026-08-13 au 2026-08-13.
- **Note pratique :** À partir du 2026-08-13, les praticiens doivent considérer Beyond Pixels comme une référence de projet Latent-to-4D disposant à la fois d'une page de projet publique et d'un dépôt source, et valider les méthodes et leur utilisation directement à partir des artefacts liés avant de les adopter.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
