---
title: "KnowAct-GUIClaw"
category: projects
date: 2026-07-18
tags: [knowact-guiclaw, project]
aliases: ["KnowAct-GUIClaw"]
level: 2
source_sha256: 3a656cbdd112b0aacc462b62c7bd4b5e662a3595d1a488601d15cd7a6a998754
translation: machine
translated_at: '2026-10-24'
---
# KnowAct-GUIClaw {#knowact-guiclaw}

**Ligne de développement :** `project:knowact-guiclaw` · fil `knowact-guiclaw`  
**Dernier événement :** 2026-07-18 · 1 événement daté depuis le 2026-07-18 · **Consulté le :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

KnowAct-GUIClaw est un hôte de type OpenClaw et un exécuteur d'interface graphique (GUI) destiné aux développeurs qui automatisent des travaux de longue haleine sur Android, iOS, HarmonyOS et ordinateur de bureau.

- Achemine les tâches et transporte des valeurs typées entre les applications.
- Récupère la mémoire d'expérience.
- Valide les raccourcis mobiles et les compétences (skills) réutilisables.

## Ligne de développement {#development-line}

- **2026-07-18 — Site du projet KnowAct-GUIClaw et dépôt source liés.** Le 18 juillet 2026, un message public a relié le site du projet KnowAct-GUIClaw et le dépôt GitHub de KnowAct. Cela établit une association publique datée entre le projet GUIClaw et la base de code KnowAct, mais n'atteste ni une version particulière, ni une fonctionnalité, ni une étape d'implémentation.

## Ce qui a changé {#what-changed}

2026-07-18 — Aucune version officielle, révision d'article ni modification du dépôt n'est documentée à cette date ; le code avait fait un premier commit public le 2026-07-14, et MobileWorld a enregistré son résultat le 2026-07-17.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-18, les praticiens doivent considérer KnowAct-GUIClaw comme un projet disposant d'une page publique et d'un dépôt source KnowAct associé, et vérifier directement à partir de ces ressources les capacités et la configuration avant toute adoption.

1. Choisissez la voie nanobot intégrée pour une WebUI, une passerelle (gateway) ou un hôte d'agent, ou utilisez guiclaw en autonome lorsqu'un autre hôte, script ou terminal doit appeler la couche GUI.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
2. Installez Python 3.11+, uv, un fournisseur multimodal compatible OpenAI, ainsi que le seul extra backend nécessaire pour Android ou HarmonyOS, le bureau ou iOS ; créez ensuite la configuration YAML du fournisseur.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
3. Exécutez d'abord un dry-run ; il sollicite le modèle et la boucle de l'agent sans modifier un appareil réel. Sélectionnez ensuite le backend adb, ios, hdc ou local.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
4. Pour les hôtes d'automatisation, demandez une sortie JSON et exploitez ses champs success, error et trace, au lieu de supposer qu'une action à l'écran a réussi.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>

## Bonnes pratiques {#best-practices}

- Commencez par un dry-run et avec un appareil ou un compte de test : la validation peut lancer des intents et modifier l'état des applications.
  — <https://github.com/HITsz-TMG/KnowAct>
- Traitez la mémoire POLICY comme purement indicative ; appliquez les restrictions obligatoires à l'aide des permissions de l'appareil ou de l'application, de listes d'autorisation au niveau du backend, d'approbations de l'hôte ou d'un bac à sable (sandboxing).
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Utilisez le profil par défaut pour un appel de fonction natif fiable ; ne sélectionnez un autre profil que si le format d'action du modèle lui correspond.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Validez les candidats de raccourcis Android sur un appareil ADB avant leur promotion ; un intent ou un deep link déclaré ne prouve pas que la page attendue s'ouvre.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Ne comptez pas sur les skills pour macOS, Linux ou Windows : les skills de bureau ne récupèrent, n'exécutent, n'extraient ni n'évoluent ; l'extraction de mémoire reste disponible.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points non élucidés {#still-unknown}

- Aucune version, aucun commit, aucune révision d'article ni annonce de projet d'origine primaire datée du 2026-07-18 n'a été trouvé ; cette date ne peut donc pas être considérée comme une version distincte du produit.
- Le site et la documentation du dépôt sont modifiables ; le chemin d'installation exact, la version des paquets, les versions figées des dépendances et la licence à la date du 18 juillet ne sont pas vérifiés.
- Aucun point de contrôle officiel de modèle ni aucune version de paquet sémantique n'ont été identifiés.
- Un détail de démonstration diverge entre les sources primaires actuelles : le site indique une marche de 43 minutes pour le cas de récupération de l'hôte, tandis que arXiv v2 indique 13 minutes pour l'exemple correspondant.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://shibosusu.github.io/KnowAct-GUIClaw/ | KnowAct-GUIClaw | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct | HITsz-TMG/KnowAct | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/commits/main | Historique des commits · HITsz-TMG/KnowAct | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/releases/tag/Result | Version GUIClaw-Result · HITsz-TMG/KnowAct | 2026-09-06 |
| https://arxiv.org/abs/2607.12625 | KnowAct-GUIClaw: Know Deeply, Act Perfectly, Personal GUI Assistant with Self-Evolving Memory and Skill | 2026-09-06 |
| https://arxiv.org/html/2607.12625v2 | Rapport technique de KnowAct-GUIClaw, arXiv v2 | 2026-09-06 |
| https://raw.githubusercontent.com/Tongyi-MAI/MobileWorld/main/site/leaderboard.json | Données du classement MobileWorld | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md | Référence CLI et configuration de GUIClaw | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/blob/main/README_CN.md | README chinois de KnowAct | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:knowact-guiclaw`, fil `knowact-guiclaw`, 1 événement daté du 2026-07-18 au 2026-07-18.
- **Note pratique :** Au 2026-07-18, les praticiens doivent considérer KnowAct-GUIClaw comme un projet disposant d'une page publique et d'un dépôt source KnowAct associé, et vérifier directement à partir de ces ressources les capacités et la configuration avant toute adoption.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
