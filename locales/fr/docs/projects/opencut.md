---
title: "OpenCut"
category: projects
date: 2026-07-18
tags: [opencut, opencut-development, project]
aliases: ["OpenCut"]
level: 3
source_sha256: e53112df81f1409a49e085135c8c55ae689ce12280a06186ab0f288f67b66298
translation: machine
translated_at: '2026-10-24'
---
# OpenCut {#opencut}

**Ligne de développement :** `project:opencut` · fil `opencut-development`  
**Dernier événement :** 2026-07-18 · 1 événement daté depuis le 2026-07-18 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

OpenCut est un éditeur vidéo sous licence MIT destiné aux créateurs qui souhaitent un flux de travail à la CapCut.

- Espace de travail web : offre un point d'entrée public en bêta anticipée.
- Réécriture multiplateforme : utilise un cœur en Rust pour le web, le bureau et le mobile.
- Version v0.3.0 : documente les masques, les courbes d'images clés, les contrôles de vitesse, les contrôles de volume et l'importation de sous-titres à partir de fichiers de transcription.

## Ligne de développement {#development-line}

- **2026-07-18 — Le site web d'OpenCut et le dépôt source ont été publiquement référencés.** Le 2026-07-18, une publication a fait un lien vers le site du projet et le dépôt GitHub. Nous le suivons parce qu'il oriente les lecteurs vers le site et le code source. La publication ne indique pas s'il s'agissait d'un lancement, d'une version ou d'une mise à jour fonctionnelle.

## Ce qui a changé {#what-changed}

2026-07-18 — OpenCut était accessible à l'adresse opencut.app et dans le dépôt OpenCut-app/OpenCut. Les pages liées ne montrent aucune version publiée ni aucune modification fonctionnelle à cette date.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-18, partez du site officiel d'OpenCut et du dépôt GitHub pour évaluer ou adopter le projet.

1. Ouvrez le site officiel et sélectionnez « Essayer la bêta anticipée » pour accéder à l'espace de travail du projet.
  — <https://opencut.app/>
2. Pour le développement de la réécriture, clonez le dépôt principal, installez Proto et exécutez `proto use` afin d'installer les outils épinglés dans `.prototools`.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>
3. Exécutez la cible locale requise : `moon run web:dev`, `moon run api:dev` ou `moon run desktop:dev`.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>

## Bonnes pratiques {#best-practices}

- Épinglez la chaîne d'outils avec `proto use` avant d'exécuter les tâches Moon.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>
- Considérez les plugins, MCP, le mode sans interface, et les scripts comme des travaux planifiés, et non comme des dépendances actives.
  — <https://github.com/OpenCut-app/OpenCut/issues/811>
- Consultez les plans d'architecture avant de soumettre du code : le projet indique que les contributions extérieures sont fermées pendant la refonte.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-05-17 — Les consignes de contribution pour opencut-classic sont obsolètes : le propriétaire a archivé le dépôt et abandonné la maintenance.
- 2026-05-26 — Considérer l'API de l'éditeur, les plugins multiplateformes, le serveur MCP, le rendu sans interface ou les scripts intégrés à l'éditeur comme des fonctionnalités livrées est obsolète : ce sont toujours des cibles de la réécriture, sans dates de livraison.

## Toujours inconnu {#still-unknown}

- Nous ne savons pas si le 2026-07-18 a marqué une version, un changement de disponibilité ou une simple référence aux points d'entrée existants.
- Le site présente son point d'entrée comme une bêta anticipée, mais le README indique que opencut.app exécute toujours l'éditeur classique.
- Nous n'avons trouvé aucune documentation ni annonce officielle en chinois simplifié.
- Le projet ne donne aucune date de sortie pour la réécriture, les plugins, MCP, le mode sans interface, les scripts, ni les versions bureau ou mobile.
- La ligne de versions GitHub s'arrête à v0.3.0 au 2026-04-15 ; les sources officielles n'indiquent pas quelle version sous-tend la bêta anticipée.
- Des forks et miroirs sans lien utilisent le nom OpenCut ; cette page ne couvre que OpenCut-app/OpenCut et opencut.app.
- Nous n'avons trouvé aucun canal de distribution vérifié et actuel pour le bureau ou le mobile.
- Le dépôt historique et le dépôt de la réécriture suivent des contrats différents, sans parité fonctionnelle documentée.
- La bêta anticipée s'affiche via JavaScript, ce qui laisse le flux d'édition non documenté en texte.
- Nous n'avons trouvé aucune entrée de journal des modifications officielle après l'annonce de la réécriture.
- Le stockage, l'exportation et la confidentialité de la bêta anticipée ne correspondent qu'à ce que le projet déclare lui-même.
- Les utilisateurs non développeurs n'ont pas de moyen confirmé d'accéder aujourd'hui aux outils d'automatisation prévus.
- Les sources officielles ne listent pas les navigateurs, systèmes d'exploitation, GPU ou codecs vidéo pris en charge pour la bêta.
- Les notes de version de v0.3.0 décrivent l'application de bureau comme précoce et minimale, sans modification datée depuis.
- Nous ignorons si les projets créés dans la bêta anticipée s'ouvrent dans l'éditeur classique archivé.
- Nous n'avons trouvé aucun gestionnaire de paquets, programme d'installation ou version de bureau signée officiels.
- Le bouton « Essayer la bêta anticipée » ouvre un espace de travail, mais la documentation ne décrit ni les règles de compte ni le stockage des projets.
- Le serveur MCP prévu, l'hôte de plugins, le mode sans interface et l'onglet de scripts n'ont aucune note de version.
- Le dépôt refuse les pull requests externes pendant la préparation de la documentation d'architecture, sans date de fin annoncée.
- Aucun engagement de niveau de service ni politique d'assistance n'est publié pour la bêta anticipée.
- Un cœur en Rust est une orientation affichée pour la réécriture, et non une preuve que les fonctionnalités actuelles de l'éditeur l'utilisent.
- Nous n'avons trouvé aucune source en langue chinoise de première main permettant de vérifier les conditions, l'assistance ou la disponibilité régionale.
- L'ancienne liste de fonctionnalités des versions ne prouve pas la parité fonctionnelle avec l'espace de travail web.
- Les pages liées établissent l'identité, mais pas le contexte privé de la publication du 2026-07-18.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://opencut.app/ | OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut | Dépôt OpenCut-app/OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/blob/main/README.md | README d'OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/releases | Versions d'OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/issues/811 | Suivi : réécriture d'OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/opencut-classic | Dépôt historique d'OpenCut | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:opencut`, fil `opencut-development`, 1 événement daté du 2026-07-18 au 2026-07-18.
- **Note pratique :** Au 2026-07-18, les praticiens doivent utiliser le site officiel d'OpenCut et le dépôt GitHub comme points de départ pour évaluer ou adopter le projet, en attendant la vérification du contenu lié.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
