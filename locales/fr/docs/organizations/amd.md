---
title: "AMD — Plateforme de calcul IA AMD"
category: organizations
tags: [amd, amd-ai-compute-platform, amd_mi300x, instinct-mi300x, organization]
aliases: ["AMD"]
level: 2
source_sha256: d846ed7c7ea769d98f78b5b9ed9b903a1f032614bb1411d814c416fa8fba6dbe
translation: machine
translated_at: '2026-10-24'
---
# AMD — Plateforme de calcul IA AMD {#amd-amd-ai-compute-platform}

**Ligne de développement :** `organization:amd` · fil `amd-ai-compute-platform`  
**Événements :** 2 datés, 2023-06-14 → 2025-08-13 · **Recherche :** 2026-09-03 · confiance : moyenne

## Ce que c'est {#what-it-is}

AMD — une plateforme de calcul pour les équipes qui exécutent de l'IA, du HPC, des PC et des charges graphiques ; sa voie pour les data centers repose sur le matériel Instinct et ROCm. — MI455X et Helios pour l'inférence, l'entraînement et le fine-tuning à grande échelle. — MI430X pour le HPC scientifique et l'IA souveraine. — Builds ROCm pour PyTorch, TensorFlow, JAX, vLLM et les outils associés. Limite : la prise en charge dépend d'un tuple exact de versions matériel, OS, firmware, pilote, ROCm et framework ; le MI430X est attendu en 2027 et les déploiements en volume de Helios au S2 2026. Verdict : utilisez AMD lorsque la configuration complète figure dans la matrice ROCm en vigueur, et non simplement parce que le GPU porte la marque AMD.

## Ligne de développement {#development-line}

- **2023-06-14 — AMD a élargi son portefeuille IA pour data centers autour de l'Instinct MI300X.** Le 2023-06-14, les documents liés publiés par AMD décrivaient une extension de son portefeuille data center associée à la série Instinct MI300 et au fil MI300X. Le lien vers PyTorch 2.0 qui accompagne l'annonce replace celle-ci dans un contexte d'écosystème logiciel IA. Les liens fournis ne permettent pas à eux seuls d'établir des spécifications détaillées, une disponibilité ou une adoption par des clients.
- **2025-08-13 — AMD a publié un Space de chatbot GPT-OSS-120B.** Le 2025-08-13, le lien daté renvoyait vers un Space Hugging Face appartenant à AMD, pour un chatbot GPT-OSS-120B. Il s'agit d'une étape de démonstration ou de déploiement de modèle accessible au public, dans la présence d'AMD sur les plateformes IA. Le lien fourni ne permet pas d'établir le matériel de backend, la provenance du modèle, la disponibilité actuelle ni les garanties de service.

## Ce qui a changé {#what-changed}

AMD, 2023-06-14 — présentation détaillée de l'Instinct MI300X : CDNA 3, jusqu'à 192 Go de HBM3, une plateforme à huit GPU, échantillonnage au T3, et prise en charge dès le jour zéro de PyTorch 2.0 avec ROCm 5.4.2. AMD, 2023-11-03 — publication d'Adrenalin 23.11.1 pour les systèmes Windows Radeon, avec des optimisations DirectML pour Stable Diffusion, Lightroom, DaVinci Resolve et Procyon ; il s'agissait d'une branche de pilotes client distincte, et non d'une version serveur Instinct/ROCm. AMD, 2025-08-13 — le Space `amd/gpt-oss-120b-chatbot` nommé était une référence de démonstration ; son point d'accès est désormais soumis à restriction d'accès, il n'établit donc aucune pile de service actuelle ni aucun contrat de support. AMD, 2026-07-23 (trouvé aujourd'hui) — lancement de la famille Instinct MI400 : MI455X pour l'IA de pointe et les usines d'IA, MI430X pour l'IA souveraine et le HPC, avec ROCm comme voie logicielle commune.

## Comment l'utiliser {#how-to-use-this}

À partir du 2023-06-14, les praticiens devraient évaluer l'Instinct MI300X d'AMD et l'écosystème PyTorch associé comme option de plateforme de calcul IA ; à partir du 2025-08-13, ils peuvent utiliser le Space GPT-OSS-120B d'AMD comme référence de déploiement ou de démonstration, tout en vérifiant de manière indépendante les détails techniques et de service actuels.

1. Commencez par le sélecteur et notez les versions exactes du GPU, de l'OS, du noyau ou du firmware, du pilote, de ROCm, de Python et du framework ; ne poursuivez qu'avec une configuration compatible listée.
  — <https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html>
2. Installez le pilote GPU AMD et ROCm selon la méthode prise en charge actuelle ; le guide recommande une installation par gestionnaire de paquets sous Linux, et une archive tarball pour les configurations Windows portables en cas de doute.
  — <https://rocm.docs.amd.com/en/develop/install/rocm.html>
3. Utilisez le sélecteur PyTorch pour le matériel, l'OS et la version exacts, puis choisissez le conteneur AMD ou la voie d'installation pip correspondante.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>
4. Validez le SDK ROCm après l'installation avec `rocm-sdk targets` et `rocm-sdk test`.
  — <https://rocm.docs.amd.com/en/develop/install/rocm.html>
5. Validez le framework avant une charge de travail : `python -c "import torch; print(torch.cuda.is_available())"` doit afficher `True` lorsque PyTorch et ROCm détectent le GPU.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>

## Bonnes pratiques {#best-practices}

- Ne mélangez pas les versions de firmware, de pilote, de ROCm et de framework issues de lignes de publication différentes ; ROCm exige la pile coordonnée indiquée dans sa matrice de compatibilité.
  — <https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html>
- Utilisez le conteneur ou la roue PyTorch ROCm d'AMD correspondant, plutôt qu'un binaire quelconque, puis exécutez la vérification de détection documentée avant de planifier une charge de travail.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>
- Traitez les MI455X/Helios et les MI430X comme deux pistes de disponibilité distinctes : vérifiez la voie de déploiement auprès de l'OEM, et ne planifiez pas de capacité de production MI430X avant la disponibilité annoncée en 2027.
  — <https://www.amd.com/en/products/accelerators/instinct/mi400.html>
- Pour les portables et les tout-en-un Radeon, privilégiez le pilote fourni par l'OEM lorsque les fonctions propres au système ou la prise en charge comptent.
  — <https://www.amd.com/en/support/kb/release-notes/rn-rad-win-23-11-1>

## Remplacé par ceci {#superseded-by-this}

- AMD, 2023-06-14 : les spécifications de l'époque de l'échantillonnage du MI300X et les recommandations ROCm 5.4.2/PyTorch 2.0 sont historiques ; la sélection actuelle doit utiliser le MI400, ROCm 10 et la matrice de compatibilité en vigueur.
- AMD, 2023-11-03 : Adrenalin 23.11.1 est un pilote Windows historique, et non une recommandation actuelle pour le choix de logiciels ; la documentation d'installation ROCm actuelle renvoie vers une version ultérieure, Adrenalin 26.8.1.
- AMD, 2025-08-13 : une démonstration nommée de chatbot gpt-oss n'est pas une recommandation de déploiement actuelle, car aucun support, matériel ou contrat de service actif n'a pu être vérifié.

## Points toujours inconnus {#still-unknown}

- Le point d'accès `amd/gpt-oss-120b-chatbot` a renvoyé une erreur HTTP 401 lors de l'examen ; sa disponibilité actuelle, la révision du modèle, l'accélérateur et les conditions de service sont inconnus.
- Les éléments datés couvrent le matériel data center Instinct/ROCm, les pilotes Windows Radeon et une démonstration de modèle hébergée. Ils ne forment pas une seule séquence de versions techniques ; seule l'identité de l'entreprise est commune.
- La disponibilité, les prix et le cycle de vie du support des MI400 par OEM n'ont pas été vérifiés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.amd.com/en/newsroom/press-releases/2023-6-13-amd-expands-leadership-data-center-portfolio-with-.html | AMD Expands Leadership Data Center Portfolio with New EPYC CPUs and Shares Details on Next-Generation AMD Instinct Accelerator and Software Enablement for Generative AI | 2026-09-03 |
| https://www.amd.com/en/support/kb/release-notes/rn-rad-win-23-11-1 | AMD Software: Adrenalin Edition 23.11.1 Release Notes | 2026-09-03 |
| https://huggingface.co/spaces/amd/gpt-oss-120b-chatbot | amd/gpt-oss-120b-chatbot | 2026-09-03 |
| https://newsroom.amd.com/news/aai-2026-mi400-instinct-update/ | AAI 2026: AMD Launches AMD Instinct MI400 Series GPUs for Frontier AI, HPC | 2026-09-03 |
| https://www.amd.com/en/products/accelerators/instinct/mi400.html | AMD Instinct MI400 Series GPUs | 2026-09-03 |
| https://www.amd.com/zh-cn/newsroom/press-releases/aai-2026-mi400-instinct-update.html | AAI 2026：AMD推出面向前沿AI与HPC的AMD Instinct MI400系列GPU | 2026-09-03 |
| https://rocm.docs.amd.com/en/develop/install/rocm.html | Install AMD ROCm 10.0.0 | 2026-09-03 |
| https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html | ROCm 10.0.0 compatibility matrix | 2026-09-03 |
| https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html | Install PyTorch for ROCm | 2026-09-03 |

## Brief agent {#agent-brief}

- **Sujet :** `organization:amd`, fil `amd-ai-compute-platform`, 2 événements datés du 2023-06-14 au 2025-08-13.
- **Note pratique :** À partir du 2023-06-14, les praticiens devraient évaluer l'Instinct MI300X d'AMD et l'écosystème PyTorch associé comme option de plateforme de calcul IA ; à partir du 2025-08-13, ils peuvent utiliser le Space GPT-OSS-120B d'AMD comme référence de déploiement ou de démonstration, tout en vérifiant de manière indépendante les détails techniques et de service actuels.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
