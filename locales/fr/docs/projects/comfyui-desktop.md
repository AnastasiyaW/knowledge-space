---
title: "ComfyUI Desktop"
category: projects
date: 2026-01-06
tags: [comfyui-desktop, project]
aliases: ["ComfyUI Desktop"]
level: 3
source_sha256: b8856925ec583ac8cc82309d79f080a16d6e526a8ca05f9375bfaa270b50d1e0
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Desktop {#comfyui-desktop}

**Ligne de développement :** `project:comfyui-desktop` · fil `comfyui-desktop`  
**Dernier événement :** 2026-01-06 · 2 événements datés depuis le 2024-11-27 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI Desktop, désormais remplacé par Comfy Desktop, est un lanceur local destiné aux praticiens qui ont besoin d'environnements ComfyUI distincts, plutôt que de maintenir une installation Python manuelle unique.

- Instances : crée, lance et gère des instances ComfyUI indépendantes.
- Isolation : sépare la version, les nœuds personnalisés, les paramètres et l'environnement Python de chaque instance.
- Opérations : prend en charge les modèles, la migration depuis des installations existantes ou héritées, les canaux de mise à jour, les instantanés et le retour à un état antérieur.

## Ligne de développement {#development-line}

- **2024-11-27 — ComfyUI Desktop devient disponible en tant que projet open source.** Le 2024-11-27, ComfyUI a rendu son application Desktop disponible en tant que projet open source. Cette date marque une étape publique dans la ligne de produits. Les documents de publication ne précisent pas le périmètre fonctionnel initial exact, les plateformes prises en charge ni les détails de la version.
- **2026-01-06 — ComfyUI ajoute la prise en charge officielle d'AMD ROCm.** Le 2026-01-06, ComfyUI a annoncé la prise en charge officielle d'AMD ROCm. Il s'agit d'une mise à jour de compatibilité de plateforme pour la ligne Desktop. L'annonce ne précise pas les versions exactes de Desktop, les systèmes d'exploitation, le matériel ni les exigences d'installation.

## Évolutions {#what-changed}

Ligne de développement de ComfyUI Desktop :

- 2024-11-27 — Le Desktop v1 a été publié en open source. Nous n'avons pas pu relire aujourd'hui l'ensemble détaillé des fonctionnalités dans l'article de lancement d'origine.
- 2026-01-06 — Le Desktop Windows v0.7.0 ajoute la prise en charge officielle d'AMD ROCm ; l'installation doit sélectionner ROCm automatiquement. La version utilise ROCm 7.1.1 et recommande son pilote en préversion.
- Constaté aujourd'hui (2026-09-04) — la documentation décrit le successeur maintenu comme Comfy Desktop : un gestionnaire multi-installations plutôt que l'ancienne application à installation unique. Il peut migrer les anciens workflows, nœuds, modèles, entrées, sorties et paramètres vers un environnement autonome neuf.
- Constaté aujourd'hui (2026-09-04) — l'ancien dépôt Comfy-Org/desktop est archivé et renvoie vers Comfy-Org/Comfy-Desktop.

## Comment l'utiliser {#how-to-use-this}

À partir du 2024-11-27, les praticiens peuvent évaluer ComfyUI Desktop via son dépôt source public et les guides d'utilisation ; à partir du 2026-01-06, les utilisateurs AMD doivent également consulter les recommandations officielles de prise en charge ROCm lors de l'évaluation d'un déploiement Desktop.

1. Vérifiez la plateforme et les capacités documentées avant l'installation : Windows 10 ou plus récent, ou macOS 13 ou plus récent sur Apple Silicon, avec au moins 4,85 Go par instance autonome et 8 Go de RAM.
  — <https://docs.comfy.org/installation/desktop/overview>
2. Sous Windows, exécutez le fichier .exe téléchargé, lancez Comfy Desktop et créez la première installation depuis l'écran d'accueil.
  — <https://docs.comfy.org/installation/desktop/windows>
3. Sous macOS avec Apple Silicon, ouvrez le fichier .dmg, faites glisser Comfy Desktop dans Applications, puis lancez-le.
  — <https://docs.comfy.org/installation/desktop/macos>
4. Dans le Chooser, créez une instance Standalone nommée sur un SSD, puis sélectionnez un modèle de workflow une fois la configuration terminée.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
5. Si une installation portable, Git ou Legacy Desktop existante contient déjà des travaux, ajoutez-la ou migrez-la au lieu de reconstruire manuellement les modèles et les workflows ; vérifiez ensuite les workflows, les nœuds, les modèles et l'URL reprise.
  — <https://docs.comfy.org/installation/desktop/usage/migrate>
6. Utilisez Manage → Update pour rester sur Stable pour un usage courant, ou sélectionnez délibérément Latest sur GitHub lorsqu'un workflow nécessite les derniers commits du cœur.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Bonnes pratiques {#best-practices}

- Placez les projets incompatibles dans des instances Standalone distinctes afin que leurs environnements Python, révisions de ComfyUI et nœuds personnalisés ne puissent pas entrer en conflit.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
- Utilisez par défaut le canal de mise à jour Stable ; Latest sur GitHub est réservé aux tests intentionnels de commits plus récents.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Créez un instantané manuel étiqueté avant d'ajouter un nœud ou de mettre à jour une pile de travail ; les instantanés enregistrent le commit de ComfyUI, les versions des nœuds et les paquets pip, et permettent de restaurer l'état précédent.
  — <https://docs.comfy.org/installation/desktop/usage/snapshots>
- Conservez ComfyUI-Manager au niveau de sécurité Standard recommandé : il autorise les packs de nœuds enregistrés et bloque les sources Git arbitraires.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Si un nœud personnalisé empêche le démarrage ou l'interface de fonctionner, désactivez d'abord tous les nœuds personnalisés, puis procédez par dichotomie sur l'ensemble ; sauvegardez custom_nodes avant de faire une dichotomie manuelle.
  — <https://docs.comfy.org/troubleshooting/custom-node-issues>

## Remplacé par {#superseded-by-this}

- Recommandations héritées de ComfyUI Desktop à installation unique, datant du 2024-11-27 : remplacez-les par le modèle actuel de Comfy Desktop multi-instances et migrez au lieu d'écraser l'ancienne installation.
- Recommandations Windows Desktop antérieures au 2026-01-06 supposant un matériel exclusivement NVIDIA : la v0.7.0 a introduit la prise en charge officielle d'AMD ROCm sous Windows pour les GPU Radeon et les processeurs Ryzen AI pris en charge.
- Comfy-Org/desktop comme dépôt source actif, depuis le 2026-06-26 : il est archivé et explicitement remplacé par Comfy-Org/Comfy-Desktop.
- Recommandation du 2026-09-04 selon laquelle Desktop correspond toujours au dernier commit de ComfyUI : Stable est le canal par défaut ; Latest doit être sélectionné délibérément.

## Points encore inconnus {#still-unknown}

- La page de lancement de 2024 ne s'est pas affichée lors de la consultation ; son ensemble de fonctionnalités exact de la v1 n'est donc pas vérifié indépendamment au-delà de l'événement daté d'ouverture du code source.
- La documentation anglaise actuelle indique que Linux n'est disponible qu'à partir des sources, sans installateur officiel, tandis que le dépôt Comfy-Desktop maintenu documente l'installation par .deb et AppImage. Résolvez cette contradiction à partir de l'artefact de publication avant de choisir Linux pour Desktop.
- La documentation anglaise décrit désormais le successeur multi-instances, alors que la page Windows en chinois décrit encore l'ancienne bêta à installation unique et le chemin exclusivement NVIDIA. Les sources publiques n'indiquent pas la date limite de localisation ou de migration.
- L'annonce AMD cite les GPU Radeon et les processeurs Ryzen AI pris en charge, mais ne fournit pas de matrice matérielle complète et actuelle pour Desktop ; validez la combinaison exacte de GPU et de pilote lors de l'installation.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.comfy.org/open-sourcing-v1-desktop/ | Open Sourcing V1 Desktop | 2026-09-04 |
| https://blog.comfy.org/p/official-amd-rocm-support-arrives | Official AMD ROCm Support Arrives on Windows for ComfyUI Desktop | 2026-09-04 |
| https://github.com/Comfy-Org/desktop | Comfy-Org/desktop — archivé et remplacé par Comfy-Org/Comfy-Desktop | 2026-09-04 |
| https://github.com/Comfy-Org/Comfy-Desktop | Comfy-Org/Comfy-Desktop — L'application de bureau pour ComfyUI | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/overview | Comfy Desktop Overview | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/windows | Comfy Desktop for Windows | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/macos | Comfy Desktop for macOS | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/instance-management | Instance Management | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/manage | Managing Installations | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/snapshots | Snapshots | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/migrate | Migrate from Legacy Desktop | 2026-09-04 |
| https://docs.comfy.org/troubleshooting/custom-node-issues | How to Troubleshoot and Solve ComfyUI Issues | 2026-09-04 |
| https://docs.comfy.org/zh/installation/desktop/windows | Windows Desktop — ComfyUI (Chinese) | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfyui-desktop`, fil `comfyui-desktop`, 2 événements datés du 2024-11-27 au 2026-01-06.
- **Note pratique :** À partir du 2024-11-27, les praticiens peuvent évaluer ComfyUI Desktop via son dépôt source public et les guides d'utilisation ; à partir du 2026-01-06, les utilisateurs AMD doivent également consulter les recommandations officielles de prise en charge ROCm lors de l'évaluation d'un déploiement Desktop.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
