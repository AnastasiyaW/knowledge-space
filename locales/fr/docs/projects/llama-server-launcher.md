---
title: "LlamaServerLauncher"
category: projects
date: 2026-06-17
tags: [llama-server-launcher, llama-server-launcher-development, llama_server_launcher, project]
aliases: ["LlamaServerLauncher"]
level: 2
source_sha256: f2dd56e143b364599a402a44615be4b8a9ade3cc4bb33e2fd551ea2de4cb90c2
translation: machine
translated_at: '2026-10-24'
---
# LlamaServerLauncher {#llamaserverlauncher}

**Ligne de développement :** `project:llama-server-launcher` · fil `llama-server-launcher-development`  
**Dernier événement :** 2026-06-17 · 1 événement daté depuis le 2026-06-17 · **Consulté le :** 2026-09-05 · confiance : élevée

## Qu'est-ce que c'est {#what-it-is}

LlamaServerLauncher : application .NET 8/Avalonia multiplateforme destinée aux utilisateurs de llama.cpp qui ont besoin de profils, de lancement de plusieurs serveurs et de configuration des modèles GGUF via une interface graphique. — sélectionne `llama-server`, un GGUF local ou un dépôt Hugging Face ; — configure le contexte, les couches GPU, l'échantillonnage et l'accès réseau ; — surveille `/health`, `/slots`, les journaux et la vitesse d'inférence ; — permet de télécharger et de basculer entre les builds de llama.cpp. Limite : un binaire `llama-server` compatible est requis ; l'application ne remplace ni le moteur ni le modèle. Conclusion : c'est une alternative pratique aux lignes de commande manuelles de llama.cpp lorsque des profils reproductibles et une observabilité sont nécessaires.

## Ligne de développement {#development-line}

- **2026-06-17 — Le dépôt LlamaServerLauncherAvalonia a été cité.** Le 2026-06-17, la ligne de développement LlamaServerLauncher a cité le dépôt GitHub LlamaServerLauncherAvalonia. Les éléments disponibles établissent l'association avec ce dépôt, mais n'établissent ni une version publiée, ni une modification de code, ni une fonctionnalité, ni une instruction d'utilisation.

## Ce qui a changé {#what-changed}

2026-06-17 — LlamaServerLauncher a été présenté comme une interface graphique pour lancer llama.cpp et réaliser l'inférence locale, à la place de la configuration manuelle en ligne de commande.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-17, les praticiens doivent consulter le dépôt LlamaServerLauncherAvalonia comme source identifiée pour cette ligne de développement, en considérant sa version, ses capacités et ses prérequis d'installation comme non vérifiés tant que le dépôt n'a pas été étudié.

1. Téléchargez le binaire actuel pour votre plateforme depuis la page des releases et lancez l'application.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia#installation>
2. Indiquez `llama-server` ou téléchargez llama.cpp depuis l'application, puis sélectionnez un modèle GGUF ou un dépôt/fichier Hugging Face.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
3. Créez un profil : définissez le contexte, le nombre de couches GPU, le port, si nécessaire une clé API et les paramètres de génération ; lancez le serveur.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
4. Attendez l'état de disponibilité, puis copiez l'URL de base compatible OpenAI `/v1` ou la commande `curl` prête à l'emploi pour votre client.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>

## Bonnes pratiques {#best-practices}

- Vérifiez le binaire via l'attestation de provenance GitHub et le SHA-256 : les releases ne sont pas signées par une signature de code.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia#verifying-releases>
- Laissez le serveur sur `127.0.0.1` si l'accès LAN n'est pas nécessaire ; en cas d'accès réseau, définissez une clé API.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
- Avant le lancement, vérifiez la prise en charge des options par la build de llama.cpp choisie : l'application lit `llama-server --help` et signale les options non prises en charge.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
- Pour MCP, tenez compte du fait que les serveurs enfants sont lancés avec les droits du lanceur ; l'activation de MCP limite le CORS localhost si vous ne le configurez pas explicitement.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-23 — sous Windows, l'attente antérieure selon laquelle les processus MCP enfants pourraient rester après l'arrêt du serveur n'est plus le comportement par défaut : le serveur et ses descendants sont maintenus par un Windows Job Object ; l'exception est disponible dans les paramètres de comportement.

## Points encore inconnus {#still-unknown}

- Le dépôt principal confirme l'objectif actuel et les releases ultérieures, mais ne contient pas de description de release datée spécifiquement du 2026-06-17 ; par conséquent, les détails de l'état initial se limitent à la mention contemporaine d'une interface graphique pour llama.cpp.
- Le README actuel énumère des capacités qui ont pu apparaître après la dernière release publiée, v1.9 du 2026-08-23 ; la limite de version de chaque fonctionnalité n'a pas été vérifiée individuellement.
- Les event_findings et new_events sont inclus ci-dessous, comme demandé.
- event_findings: [{"event_date":"2026-06-17","finding":"Une mention indépendante du même jour précise la portée pratique de l'étape initiale : il s'agit d'une interface graphique pour llama.cpp destinée à l'inférence locale de LLM ; aucun numéro de version précis n'est indiqué dans la source.","source_url":"https://2ch.org/ai/res/1633496.html","source_date":"2026-06-17"}]
- new_events: [{"date":"2026-06-20","summary":"La v1.2 a ajouté la sélection automatique de `-t`, de la taille batch/ubatch, de `-ngl`, de Flash Attention, des tensor overrides et du CPU MoE via une série de benchmarks ; l'implémentation a été portée en C#/.NET sans dépendance à Python.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-06-20"},{"date":"2026-06-25","summary":"La v1.3 a ajouté un proxy compatible OpenAI qui charge un profil selon le champ `model`, prend en charge le streaming et décharge le modèle après un idle timeout ; un seul modèle est maintenu simultanément en VRAM.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-06-25"},{"date":"2026-07-22","summary":"La v1.5 a ajouté des benchmarks sauvegardables, un moniteur CPU/RAM/GPU/VRAM, la lecture des métadonnées GGUF, la vérification de disponibilité via `/health` et les métriques en direct via `/slots` et le journal serveur.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-07-22"},{"date":"2026-08-23","summary":"La v1.9 a ajouté des serveurs MCP par profil via `--mcp-servers-config`, la vérification des outils détectés avant le chargement du modèle, un Windows Job Object pour l'arborescence enfant et l'exécution de prompts dans les benchmarks.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-08-23"}]

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/pytraveler/LlamaServerLauncherAvalonia | GitHub - pytraveler/LlamaServerLauncherAvalonia | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia#installation | Instructions d'installation de LlamaServerLauncher | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia#verifying-releases | Instructions de vérification des releases de LlamaServerLauncher | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases | Releases de LlamaServerLauncher | 2026-09-05 |
| https://2ch.org/ai/res/1633496.html | Modèles de langage locaux (LLM) : Gemma, Qwen, GLM et autres n°242 | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:llama-server-launcher`, fil `llama-server-launcher-development`, 1 événement daté, du 2026-06-17 au 2026-06-17.
- **Remarque pratique :** Au 2026-06-17, les praticiens doivent consulter le dépôt LlamaServerLauncherAvalonia comme source identifiée pour cette ligne de développement, en considérant sa version, ses capacités et ses prérequis d'installation comme non vérifiés tant que le dépôt n'a pas été étudié.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
