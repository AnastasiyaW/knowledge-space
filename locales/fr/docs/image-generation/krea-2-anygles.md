---
title: "Krea 2 Anygles : adaptateur de vue caméra"
description: "Krea 2 Anygles régénère une personne clairement visible depuis un nouveau lacet, une nouvelle élévation ou une nouvelle distance de caméra, grâce à un Control-LoRA piloté par une carte de normales SAM 3D Body. Il nécessite son propre chargeur et une étape de préparation par pickle soumise à accès restreint. Inclut notre test d'orbite de 80 images avec un maillage 3D ouvert issu d'image à la place de SAM 3D Body."
category: models
tags: [krea-2, anygles, camera-control, novel-view, control-lora, comfyui, sam-3d-body, normal-map]
aliases: ["krea2-anygles", "Anygles", "Krea 2 camera angle LoRA"]
level: 4
source_sha256: c5bcc7f604686a662d18d9f5521d5e9dfa8d8a16024299af8399ab681ee51e2f
translation: machine
translated_at: '2026-10-24'
---
# Krea 2 Anygles : adaptateur de vue caméra {#krea-2-anygles-camera-view-adapter}

Krea 2 Anygles est un adaptateur communautaire pour Krea 2 Turbo. À partir d'une image d'une personne, il génère la même personne et la même scène depuis un nouvel angle de caméra. Il associe un Control-LoRA de rang 32 à 4 nœuds ComfyUI. La vue cible est une carte de normales rendue, et non de simples prompts textuels. Nous l'avons examiné le 2026-09-30 à partir de la fiche du modèle, du README des nœuds et du code des nœuds.

Nous avons exécuté l'adaptateur réel avec un maillage 3D ouvert issu d'une image (TripoSG) à la place de SAM 3D Body, qui est soumis à accès restreint. Les résultats sur petit échantillon sont présentés dans [Notre test d'orbite](#our-orbit-test).

## Ce qu'il contrôle {#what-it-controls}

| Contrôle | Plage du nœud | Démos de l'auteur | Signification |
|---|---|---|---|
| Lacet (yaw) | -180 à +180 degrés | orbite complète | négatif déplace la caméra vers la gauche, positif vers la droite |
| Élévation | -60 à +60 degrés | -45 à +45 | négatif déplace la caméra vers le bas, positif vers le haut |
| Distance | 0,6x à 1,8x | 0,78x à 1,35x | en dessous de 1 plus proche, au-dessus de 1 plus loin |

- Périmètre : **un sujet humain clairement visible.** Il ne gère pas les animaux, les objets génériques, les foules ni la reconstruction 3D exacte. Le modèle génère les faces cachées et l'arrière-plan au lieu de les restituer.
- L'élévation et la distance sont des contrôles utiles plutôt qu'une reconstruction de scène calibrée. Considérez les valeurs comme des directions.

## Fonctionnement {#how-it-works}

1. **Nœud caméra.** SAM 3D Body extrait le maillage du corps, et MoGe estime le champ de vision de la caméra. Le nœud fait pivoter le maillage autour du bassin et rend une carte de normales cible au ratio d'aspect de la source. Il génère aussi la phrase de caméra utilisée à l'entraînement.
2. **Nœud d'encodage.** Ce nœud envoie l'image vers Qwen3-VL et vers un chemin de référence propre, à une taille maximale de 384 px. Il encode ensuite par VAE la normale cible pleine toile.
3. **Nœud Load LoRA.** Ce nœud charge les paires LoRA et le tenseur de projection `transformer.first_control.weight`. Les chargeurs standard omettent ce tenseur et perdent silencieusement le contrôle spatial.
4. **Nœud de patch du modèle.** Il injecte les tokens de normales à l'entrée de l'image bruitée et met en cache les K/V de référence une fois par exécution.

Le fichier de poids `krea2_anygles_rank32.safetensors` pèse 229 Mo en BF16. Il contient 256 paires LoRA de rang 32, réparties sur les 32 blocs du transformeur (attention q, k, v, out, gate, et MLP), ainsi que la projection de contrôle unique de forme [6144, 64]. Nous avons inspecté le fichier et confirmé la somme de contrôle publiée par l'auteur.

### Phrase de caméra {#camera-sentence}

L'entraînement utilisait uniquement des formulations de lacet vers la gauche. Le nœud convertit le lacet signé via `left_angle = (-yaw) mod 360`. Une rotation vers la droite de +50 degrés devient :

```text
Same figure. Move the camera 310 degrees to the left relative to the input view.
```

Le nœud n'ajoute les clauses d'élévation et de distance que si elles sont demandées, et transmet le texte utilisateur sans modification. Placez les détails de scène dans le texte supplémentaire (« lumière douce d'après-midi »). N'écrivez pas d'instructions de caméra qui contredisent la carte de normales.

## Réglages (fiche et README de l'auteur) {#settings-authors-card-and-readme}

```yaml
inference_base: krea/Krea-2-Turbo      # ComfyUI graph validated with krea2_turbo_int8_convrot
steps: 8
sampler: euler
scheduler: simple
guidance: 0.0 in diffusers / cfg 1.0 in ComfyUI
lora_strength: 1.0                     # node allows 0-2; no other value is documented
reference_max_edge: 384                # px; Qwen3-VL image input on
reference_kv_cache: on
output: source aspect ratio, sides multiple of 16, at most 2 * 1024 * 1024 px
validated_size: 1008x1344
```

Pour les conventions de guidance (Krea 0.0 = ComfyUI 1.0), voir [[krea-2-prompting]].

## Utilisation {#running-it}

Pour ComfyUI, clonez le dépôt dans `custom_nodes`, installez `requirements.txt`, acceptez la licence pour télécharger le checkpoint SAM 3D Body, copiez le LoRA dans `models/loras` et chargez `krea2_anygles_workflow.json`.

La fiche du modèle fournit un workflow Python autonome :

```bash
python prepare_normal.py --source person.webp --output target_normal.png \
  --yaw 50 --elevation 0 --distance 1.0 \
  --sam3d-root ./sam-3d-body \
  --checkpoint ./checkpoints/sam-3d-body-dinov3/model.ckpt \
  --mhr-model ./checkpoints/sam-3d-body-dinov3/assets/mhr_model.pt

python example.py --source person.webp --normal target_normal.png --output result.webp \
  --yaw 50 --elevation 0 --distance 1.0 --prompt "soft afternoon light" --steps 8 --seed 42
```

### Ce que l'étape de préparation des normales installe {#what-the-normal-preparation-step-pulls-in}

Notre audit de code avant installation a montré que les nœuds de diffusion chargent directement les fichiers safetensors, sans appels réseau, sous-processus, `eval` ni `exec`. Le pipeline de préparation des normales apporte en revanche des dépendances lourdes :

- deux checkpoints pickle chargés via `torch.load(weights_only=False)` et `torch.jit.load`
- un modèle MoGe au format pickle
- un téléchargement à l'exécution, via `torch.hub`, du code DINOv3 depuis GitHub
- environ 20 paquets supplémentaires, dont pyrender, pytorch-lightning et MoGe depuis git
- le dépôt à accès restreint `facebook/sam-3d-body-dinov3`.

Le dépôt à accès restreint nous a renvoyé une erreur HTTP 403, et nous ne désérialisons pas de checkpoints tiers dans un environnement d'exécution partagé. Nous n'avons donc pas utilisé ce chemin.

Exécutez la préparation des normales dans un conteneur ou une machine dédiée, qui ne produit que `target_normal.png`. Transmettez ce fichier et la phrase de caméra au nœud d'encodage afin que l'environnement ComfyUI principal ne manipule jamais de fichiers pickle.

## Notre test d'orbite {#our-orbit-test}

Nous avons remplacé le générateur de maillage et conservé le reste du pipeline de l'auteur :

- **Maillage :** [TripoSG](https://github.com/VAST-AI-Research/TripoSG) (licence MIT, sans accès restreint, poids `.safetensors`), exécuté sur un masque de personne [BiRefNet](https://huggingface.co/ZhengPeng7/BiRefNet) dans un environnement isolé. TripoSG a tourné avec 50 étapes, guidance 7.0 et seed 42.
- **Normales :** le moteur de rendu de normales de l'auteur a été exécuté sans modification sur notre maillage, avec les phrases de caméra de l'auteur. Nous avons fixé la focale à 1680 px (valeur par défaut de SAM 3D Body sans estimation du FOV) pour éviter le checkpoint MoGe au format pickle.
- **Diffusion :** nous n'avons exécuté que les nœuds Encode, Load LoRA et Model patch dans ComfyUI : Turbo en fp8, 8 étapes, euler/simple, cfg 1, force 1.0, bord de référence 384 px, résolution 1008x1344 et une seed fixe.
- **Matrice :** 4 sujets à une personne (un sujet avec LoRA d'identité et trois scènes photoréalistes) sur 20 angles de caméra. Cela couvre un cercle de lacet complet par pas de 22,5 degrés (16 vues), une élévation de ±20 et des distances de 0,78 et 1,35, soit 80 images au total.

La similarité faciale utilise la distance cosinus SFace d'OpenCV par rapport au visage source. Une valeur de 0,363 ou plus indique la même identité :

| Signal | Résultat |
|---|---|
| Silhouette de la personne vs normale cible (IoU, médiane par sujet) | 0,83-0,91 (le sujet assis est le moins bien ajusté) |
| Similarité faciale, vues quasi frontales (médiane par sujet) | 0,47-0,61 |
| Similarité faciale à ±90 degrés (profils) | 0,07-0,53, fortement dépendante du sujet |
| Vues de dos (environ ±135 à 180 degrés) | le détecteur ne trouve généralement pas de visage, comme attendu |
| Visages détectés au niveau ou au-dessus du seuil de même personne | 43 sur 60 |

TripoSG produit un contour habillé. SAM 3D Body génère un maillage corporel paramétrique nu, qui correspond aux données d'entraînement de l'adaptateur. Les poses assises s'ajustent moins bien à notre maillage ouvert. Ces chiffres décrivent cette configuration de substitution, et non le pipeline SAM 3D Body d'origine.

## Pièges courants {#gotchas}

- **Ne chargez pas les poids avec un chargeur LoRA standard.** Utilisez le nœud Anygles Load LoRA. Les chargeurs génériques suppriment `transformer.first_control.weight`, ce qui retire silencieusement le contrôle de la vue.
- **Adaptez les dimensions de la carte de normales à la toile.** Rendez les normales à la résolution et au ratio de sortie exacts, afin que le guidage spatial reste précis.
- **Recadrez sur une personne clairement visible.** L'adaptateur ne gère pas les groupes ni les personnages éloignés ; recadrez d'abord l'image.
- **Vérifiez l'identité sur les vues de dos.** Le modèle invente les angles et les arrière-plans non visibles au lieu de les reconstruire. Vérifiez la cohérence du visage et de la tenue sur les grands virages en lacet.
- **Testez les checkpoints quantifiés.** Le graphe ComfyUI a été validé avec un checkpoint Turbo int8 ConvRot. Le comportement en fp8 n'a pas été testé ; vérifiez le résultat lorsque vous changez de format.
- **Exécutez la préparation des normales dans son propre environnement.** Les scripts de préparation désérialisent des checkpoints tiers et téléchargent du code à l'exécution.

## Questions ouvertes {#open-questions}

- Résultats d'orbite avec les normales natives en maillage nu de SAM 3D Body, au lieu des maillages habillés.
- Comportement de l'adaptateur pour des forces LoRA autres que 1.0.
- Parité entre le Turbo fp8 et le checkpoint int8 ConvRot validé par l'auteur.

## Voir aussi {#see-also}

- [[krea-2-prompting]] - Réglages, conventions de guidance et structure des prompts pour Krea 2
- [[krea-2]] - Jalons de sortie de Krea 2
- [[flux-klein-capability-map]] - Règles de vérification des variantes et de l'exécution

## Sources {#sources}

- Fiche du modèle (réglages, plages, usage portable, licence) : https://huggingface.co/yijunwang2/krea2-anygles
- Nœuds ComfyUI, README et workflow : https://github.com/alexw5702-afk/krea2-anygles
- Plages des widgets des nœuds : https://github.com/alexw5702-afk/krea2-anygles/blob/main/nodes.py
- Budget de pixels (`MAX_PIXELS = 2 * 1024 * 1024`) : https://github.com/alexw5702-afk/krea2-anygles/blob/main/anygles.py
- Démo Space : https://huggingface.co/spaces/yijunwang2/krea2-anygles
- Dépôt SAM 3D Body : https://github.com/facebookresearch/sam-3d-body
- Checkpoint SAM 3D Body (accès restreint) : https://huggingface.co/facebook/sam-3d-body-dinov3
- TripoSG (image vers 3D, MIT) : https://github.com/VAST-AI-Research/TripoSG et poids https://huggingface.co/VAST-AI/TripoSG
- BiRefNet (détourage) : https://huggingface.co/ZhengPeng7/BiRefNet
- Reconnaissance faciale OpenCV (SFace, seuil cosinus 0,363) : https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html
