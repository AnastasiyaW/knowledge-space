---
title: "GalaxyAce LoRA"
category: projects
date: 2026-03-30
tags: [galaxyace-lora, project]
aliases: ["GalaxyAce LoRA"]
level: 2
source_sha256: ad1af1e87bacec8240fd3b0895e174a0897c793cbab229c9736b77fc81e36bca
translation: machine
translated_at: '2026-10-24'
---
# GalaxyAce LoRA {#galaxyace-lora}

**Ligne de développement :** `project:galaxyace-lora` · fil `galaxyace-lora`  
**Dernier événement :** 2026-03-30 · 1 événement daté depuis le 2026-03-30 · **Consulté :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

GalaxyAce LoRA — ce sont des style-LoRA distincts destinés à un auteur de photos et de vidéos qui a besoin d'une prise de vue présentant les caractéristiques d'un appareil Android bon marché du début des années 2010. — rendu des couleurs, exposition et douceur de l'objectif; — pour les variantes LTX — bruit du capteur, compression et tremblement de la main; — pour H3 — le même effet visuel sur une vidéo avec audio natif. Chaque fichier est lié à son modèle de base : LTX-2/2.3, Z-Image-Turbo, Krea 2 et MiniMax H3 n'utilisent pas des poids interchangeables. Conclusion : il s'agit d'un adaptateur pour un workflow précis, et non d'un filtre universel pour n'importe quel checkpoint.

## Ligne de développement {#development-line}

- **2026-03-30 — référence Civitai spécifique à la version de GalaxyAce LoRA enregistrée.** Le 2026-03-30, cette ligne de développement a enregistré une URL Civitai propre à une version de GalaxyAce LoRA, identifiant le modèle 2200329 et la version 2808759. Elle fournit un point d'ancrage daté pour l'identité de cette version du modèle, tandis que son contexte de publication, les détails d'entraînement et la compatibilité restent non vérifiés.

## Ce qui a changé {#what-changed}

GalaxyAce LoRA — la ligne est passée de LTX-2.3 à des variantes distinctes pour Krea 2 et MiniMax H3. 2026-03-30 — la référence à la version 2808759 fixe la variante LTXV 2.3; la mise à jour publique décrit une force de 1.0, l'absence de trigger word et un branchement après le checkpoint, à l'intérieur du subgraph ComfyUI T2V/I2V. 2026-06-25 (trouvé aujourd'hui, mise à jour de l'auteur) — une variante distincte pour Krea 2 Raw et Turbo a été ajoutée; la force dépend désormais de la proximité du prompt avec les scènes du quotidien présentes dans l'entraînement. 2026-07-06 — la page racine du modèle est indiquée sans version ID; il est impossible d'établir un nouveau poids ou un nouveau réglage à cette date. 2026-08-05 (trouvé aujourd'hui, mise à jour de l'auteur) — une variante MiniMax H3 3201619 a été ajoutée pour la vidéo avec son natif et une autre forme de prompt. Au 2026-09-04, la fiche disponible est désignée comme MiniMax H3, mais son contenu nécessite une connexion.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-30, les praticiens peuvent conserver le modèle Civitai 2200329, version 2808759, comme référence de provenance datée pour GalaxyAce LoRA, mais ils ne doivent pas déduire de cette seule ligne sa méthode d'entraînement, son contenu, sa compatibilité ni ses mises à jour ultérieures.

1. Ouvrez la fiche, connectez-vous à Civitai et sélectionnez précisément la variante MiniMax H3; ne chargez pas de poids LTX ou Krea dans un workflow H3.
  — <https://civitai.red/models/2200329/galaxyace-lora>
2. Déployez MiniMax H3 Base selon la notice officielle et commencez par le template ComfyUI T2V ou R2V recommandé.
  — <https://github.com/MiniMax-AI/MiniMax-H3>
3. Branchez le GalaxyAce LoRA compatible H3 dans l'emplacement LoRA du workflow H3; le miroir de la version actuelle indique les valeurs de départ suivantes : strength 1.0, guidance_scale 1, 768p/24 fps, nombre d'images 17n+5 et dimensions multiples de 32.
  — <https://fastsdmodel.com/models/2200329?lang=zh>
4. Rédigez un prompt cohérent dans l'ordre « scène → temps forts avec timecodes → comportement de la caméra → audio → sans texte ni logos ».
  — <https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/>

## Bonnes pratiques {#best-practices}

- Pour MiniMax H3, décrivez explicitement le son souhaité et n'utilisez pas de tag tails ni de pondérations entre parenthèses comme dans les pipelines CLIP; la structure et les formulations positives fonctionnent mieux.
  — <https://fastsdmodel.com/models/2200329?lang=zh>
- Ne combinez pas l'effet de caméra bon marché avec des termes comme cinematic, anamorphic, depth of field, iPhone ou des colour grades nommés : ils contredisent un petit objectif fixe et l'exposition automatique.
  — <https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/>
- Uniquement pour la variante Krea 2 : commencez à 1.0 pour les scènes du quotidien, utilisez 1.25–1.45 comme Realism Detailer et 1.7–2.0 pour l'effet complet ou un scénario inhabituel; ce ne sont pas des paramètres de H3.
  — <https://www.reddit.com/r/comfyui/comments/1ufksvg/galaxyace_lora_update_now_supports_krea_2/>
- Si, dans H3, la parole perd sa synchronisation, l'instruction du miroir conseille d'abord de réduire la force du LoRA à 0.7 plutôt que de réécrire le prompt; le prompt négatif n'y est pas présenté comme un moyen fiable d'exclure un élément.
  — <https://fastsdmodel.com/models/2200329?lang=zh>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-30 — l'instruction LTX-2.3 consistant à brancher le LoRA après le checkpoint n'est plus une instruction universelle depuis l'apparition de la variante H3; elle reste applicable uniquement au poids LTXV 2.3.
- 2026-06-25 — l'échelle de force Krea 2, de 1.0 à 2.0, est obsolète comme recommandation générale pour GalaxyAce LoRA : elle ne concerne que Krea-2 Raw/Turbo.
- 2026-07-06 — le lien racine sans version ID ne peut pas être considéré comme indiquant le poids actuel; la variante H3 3201619 a été publiée par la suite.

## Toujours inconnu {#still-unknown}

- La fiche Civitai directe nécessite une connexion : la liste des fichiers, le SHA-256, la licence, le compte de l'auteur et la disponibilité des anciennes versions ne sont pas confirmés.
- Les paramètres H3 du site Fast SD Model proviennent d'un miroir tiers et n'ont pas été vérifiés par rapport au fichier téléchargeable sur Civitai.
- Deux références datées partagent le même model ID 2200329; rien n'indique donc deux objets distincts. LTX, Krea et H3 apparaissent comme des versions distinctes, propres à chaque modèle de base, d'une même série.
- Il existe un dépôt Hugging Face portant le même nom, mais son origine n'est reliée à la modèle Civitai par aucune source vérifiable; il est exclu des instructions.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://civitai.red/models/2200329/galaxyace-lora | GalaxyAce LoRA - MiniMax H3 GalaxyAce LoRA | Hailuo H3 by MiniMax LoRA | Civitai | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/ | Sora 2 vibes on MiniMax H3 — GalaxyAce LoRA Update | 2026-09-04 |
| https://github.com/MiniMax-AI/MiniMax-H3 | MiniMax H3 | 2026-09-04 |
| https://fastsdmodel.com/models/2200329?lang=zh | GalaxyAce LoRA | Fast SD Model | 2026-09-04 |
| https://civitai.com/models/2200329/galaxyace-lora?modelVersionId=2808759 | GalaxyAce LoRA model URL (version 2808759) | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1s5g11w/galaxyace_lora_update_now_supports_ltx23/ | GalaxyAce LoRA Update — Now Supports LTX-2.3 | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1ufksvg/galaxyace_lora_update_now_supports_krea_2/ | GalaxyAce LoRA Update — Now Supports Krea 2 | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:galaxyace-lora`, fil `galaxyace-lora`, 1 événement daté, du 2026-03-30 au 2026-03-30.
- **Note pratique :** Au 2026-03-30, les praticiens peuvent conserver le modèle Civitai 2200329, version 2808759, comme référence de provenance datée pour GalaxyAce LoRA, mais ils ne doivent pas déduire de cette seule ligne sa méthode d'entraînement, son contenu, sa compatibilité ni ses mises à jour ultérieures.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
