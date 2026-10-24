---
title: "Comfy Desktop — ComfyUI"
category: projects

tags: [comfy-desktop, comfyui, project]
aliases: ["Comfy Desktop"]
level: 3
source_sha256: f8b811a7e4f69572e233ce22abc00f654a1696a4b762766871dd372b251c7835
translation: machine
translated_at: '2026-10-24'
---
# Comfy Desktop — ComfyUI {#comfy-desktop-comfyui}

**Ligne de développement :** `project:comfy-desktop` · fil `comfyui`  
**Dernier événement :** - · 0 daté depuis - · **Recherche effectuée :** 2026-09-07 · confiance : moyenne

## Ce que c'est {#what-it-is}

Comfy Desktop est un lanceur officiel et un gestionnaire multi-instances destiné aux personnes qui souhaitent utiliser ComfyUI en local sans maintenir séparément chaque environnement Python.

- Gestion des instances : installe, lance, met à jour et suit des instances ComfyUI indépendantes.
- Isolation des environnements : sépare les versions, les nœuds personnalisés et les paramètres, tout en permettant un stockage partagé des modèles.
- Instantanés : enregistre des instantanés pour le retour arrière et des configurations d'instances reproductibles.

La documentation actuelle prend en charge Windows 10+ et macOS 13+ sur Apple Silicon, avec 4,85 Go par installation autonome et 8 Go de RAM minimum. Les recommandations pour Linux divergent entre la documentation officielle et le dépôt. Nous l'utilisons pour isoler les piles de nœuds expérimentales et de production. Ne supposez pas qu'une installation héritée suivie prend en charge les instantanés.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-06-04 — Comfy Desktop — un gestionnaire multi-instances reconstruit a commencé un déploiement progressif, remplaçant l'ancien modèle de bureau fourni en bundle.
- 2026-06-09 — Comfy Desktop — le lien enregistré pointe vers une publication originale affichée au 8 juin ; elle décrit une application reconstruite qui conserve les workflows, nœuds personnalisés, modèles et paramètres existants.
- 2026-06-16 — Comfy Desktop — la documentation a corrigé les recommandations sur les instantanés : ceux-ci étaient alors réservés aux installations Standalone, et non disponibles pour les installations Portable ou Git suivies.
- 2026-06-23 — Comfy Desktop — les notes de version de ComfyUI v0.26.0 ont mis à jour le lien vers le nouveau dépôt desktop et les références au produit « Comfy Desktop ».
- 2026-06-26 — Comfy Desktop — le dépôt historique `desktop` a été archivé et explicitement remplacé par `Comfy-Desktop`.
- 2026-08-28 — Comfy Desktop — la v1.0.46 a été publiée sur le canal stable ; la page de version observée la marquait comme Latest.
- 2026-09-03 — Comfy Desktop — la v1.0.47-rc.1 a été publiée en pré-version RC, et non sur le canal stable par défaut.

## Mode d'emploi {#how-to-use-this}

1. 1. Vérifiez les exigences documentées en matière de plateforme et de stockage, puis téléchargez le programme d'installation pris en charge pour Windows ou macOS.
  — <https://docs.comfy.org/installation/desktop/overview>
2. 2. Créez une instance Standalone pour une configuration neuve et isolée, ou ajoutez une installation Portable/Git existante lorsque son environnement actuel doit rester intact.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
3. 3. Lancez l'instance provisionnée, choisissez un modèle de workflow, et utilisez Manage pour définir les chemins, les arguments de lancement et la configuration propre à chaque instance.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
4. 4. Avant une mise à jour ou une modification de nœud personnalisé, inspectez ou créez un instantané ; utilisez Stable, sauf si vous testez délibérément les modifications de la branche master.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Bonnes pratiques {#best-practices}

- Utilisez une instance Standalone distincte pour un nœud expérimental ou une pile de dépendances ; les instantanés capturent le commit de ComfyUI, les versions des nœuds personnalisés et les paquets Python.
  — <https://docs.comfy.org/installation/desktop/usage/snapshots>
- Conservez par défaut le canal de mise à jour Stable de l'instance ; Latest sur GitHub est réservé aux tests délibérés.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Considérez les installations Portable et Git suivies comme des installations mises à jour manuellement et sans prise en charge des instantanés.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
- Gardez ComfyUI-Manager sur la politique Standard ; n'autorisez les sources de nœuds non enregistrées que dans une configuration locale assumée.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-04 — Desktop n'est plus une installation unique de ComfyUI fournie en bundle ; le produit reconstruit gère des instances configurées indépendamment.
- 2026-06-16 — Les instances Portable ou Git suivies ne prennent pas en charge les instantanés ; le périmètre documenté se limite aux installations Standalone.
- 2026-06-26 — Considérez `Comfy-Org/desktop` comme une preuve historique, et non comme le dépôt source actuel ; son propre README renvoie vers `Comfy-Org/Comfy-Desktop`.

## Toujours inconnu {#still-unknown}

- La récupération directe de l'URL X a renvoyé une erreur HTTP 403. Nous n'avons pas capturé son texte intégral ni ses médias depuis X ; la correction du 8 juin repose sur un rendu secondaire accessible.
- La date d'enregistrement est le 2026-06-09, alors que le rendu accessible date la publication du 8 juin. La normalisation du fuseau horaire de la source n'est pas vérifiée.
- Les sources de premier ordre divergent sur Linux : la documentation officielle ne mentionne aucun programme d'installation, tandis que le README de Comfy-Desktop annonce des chemins Linux `.deb` et AppImage. Vérifiez la disponibilité d'un artefact téléchargeable actuel avant de considérer Linux comme pris en charge ou non.
- Aucun guide Desktop officiel en chinois simplifié n'a été vérifié lors de cette passe ; les miroirs chinois secondaires n'ont pas été utilisés pour les affirmations opérationnelles.
- Le dépôt historique désigne explicitement Comfy-Desktop comme son successeur : il ne s'agit donc pas de deux sujets sans lien. Les instructions et binaires antérieurs à la transition doivent encore être attribués séparément.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://x.com/ComfyUI/status/2064093003590111314 | ComfyUI status 2064093003590111314 | 2026-09-07 |
| https://easyvibecoding.app/curated/1843-comfy-desktop-launches-multi-instance-management | Comfy Desktop 推出實現多執行個體管理 — EasyVibeCoding | 2026-09-07 |
| https://www.reddit.com/r/comfyui/comments/1tx4qn7/announcing_comfy_desktop_one_app_for_every_comfy/ | Announcing Comfy Desktop: One App for every Comfy | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/overview | Comfy Desktop Overview - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/overview | Using Comfy Desktop - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/instance-management | Instance Management - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/snapshots | Snapshots - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/manage | Managing Installations - ComfyUI | 2026-09-07 |
| https://github.com/Comfy-Org/docs/discussions/1141 | installation/desktop/usage/instance-management #1141 | 2026-09-07 |
| https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.26.0 | Release v0.26.0 · Comfy-Org/ComfyUI | 2026-09-07 |
| https://github.com/Comfy-Org/desktop | Comfy-Org/desktop: archived and superseded by Comfy-Desktop | 2026-09-07 |
| https://github.com/Comfy-Org/Comfy-Desktop | Comfy-Org/Comfy-Desktop | 2026-09-07 |
| https://github.com/Comfy-Org/Comfy-Desktop/releases | Releases · Comfy-Org/Comfy-Desktop | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfy-desktop`, fil `comfyui`, 0 événement daté - → -.
- **Note pratique :** Voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
