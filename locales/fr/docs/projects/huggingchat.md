---
title: "HuggingChat"
category: projects
tags: [huggingchat, huggingchat-launch, project]
aliases: ["HuggingChat"]
level: 2
source_sha256: f64d57ca7de4b638158a0193013973f91b53836db6b6a0b87728d601d827bee9
translation: machine
translated_at: '2026-10-24'
---
# HuggingChat {#huggingchat}

**Ligne de développement :** `project:huggingchat` · fil `huggingchat-launch`  
**Événements :** 1 daté, 2023-04-25 → 2023-04-25 · **Recherche :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

HuggingChat est une interface de chat web de type ChatGPT destinée aux utilisateurs de Hugging Face qui exploitent des modèles open source. Il est également possible d'héberger soi-même sa base de code Chat UI.

- Utilisation hébergée : Omni achemine automatiquement une requête, ou un utilisateur sélectionne directement un modèle.
- Déploiement : Chat UI se connecte à une API compatible OpenAI et à son point de terminaison `/models`.

## Ligne de développement {#development-line}

- **2023-04-25 — HuggingChat a été lancé avec un lien vers un modèle OpenAssistant.** Le lien de chat pointait vers `OpenAssistant/oasst-sft-6-llama-30b-xor`, que la fiche nomme OpenAssistant LLaMA 30B SFT 6. Cela révèle un contexte de modèle initial, et non un backend hébergé unique.

## Ce qui a changé {#what-changed}

HuggingChat est passé d'une interface de chat OpenAssistant à un service routé multi-fournisseurs.

- 2023-04-25 : le lien de chat pointait vers `OpenAssistant/oasst-sft-6-llama-30b-xor`, que la fiche identifie comme OpenAssistant LLaMA 30B SFT 6. Cela révèle un contexte de modèle initial, et non un backend hébergé unique.
- 2023-06-11 : la recherche web fonctionnait déjà à cette date. Une publication de première partie datée du 2023-06-02 indique que le commutateur venait d'être lancé et qu'il en était encore à ses débuts. Le lien de chat générique ne montre aucune modification distincte au 11 juin.
- 2025-07-01 : HuggingChat a annoncé la fermeture de l'ancien service hébergé et a proposé l'export des conversations, tout en maintenant Chat UI.
- 2025-10-16 : HuggingChat est revenu avec Omni, un routeur de politiques couvrant plus de 115 modèles et plus de 15 fournisseurs. Il indique quel modèle a traité chaque requête routée.
- Constaté aujourd'hui : la page en ligne propose Omni et le choix direct parmi 138 modèles. Le README actuel de Chat UI utilise des API compatibles OpenAI ; sa documentation sur la recherche web et son README divergent quant au maintien des anciens assistants de recherche web.

## Comment l'utiliser {#how-to-use-this}

À partir du 2023-04-25, nous pouvions utiliser le point d'entrée public de HuggingChat comme interface précoce vers un modèle lié à OpenAssistant.

1. Ouvrez l'application hébergée, connectez-vous avec un compte Hugging Face si cela est demandé, puis sélectionnez Start chatting.
  — <https://huggingface.co/chat/>
2. Choisissez Omni pour un routage automatique, ou un modèle nommé pour une comparaison directe ; lorsque Omni achemine la requête, notez le modèle affiché pendant le streaming.
  — <https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764>
3. Pour un déploiement maîtrisé, clonez Chat UI, configurez `MONGODB_URL`, `OPENAI_API_KEY` et `OPENAI_BASE_URL`, puis exécutez-le avec un fournisseur compatible OpenAI.
  — <https://github.com/huggingface/chat-ui>

## Bonnes pratiques {#best-practices}

- Vérifiez les contenus factuels ou à fort enjeu auprès de sources primaires. L'interface hébergée avertit que le contenu généré peut être inexact ou faux.
  — <https://huggingface.co/chat/>
- Sélectionnez un modèle nommé ou consignez le modèle affiché par Omni pour une évaluation reproductible. Omni route chaque requête selon une politique et bascule vers un autre modèle lorsqu'un modèle principal est indisponible.
  — <https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764>
- Examinez les conditions des fournisseurs avant d'envoyer des données sensibles. HuggingChat achemine les requêtes vers des fournisseurs externes, et chaque fournisseur gère sa propre sécurité des données.
  — <https://github.com/huggingface/chat-ui/blob/main/PRIVACY.md>
- Épinglez la révision de Chat UI pour l'auto-hébergement. Testez directement les fonctionnalités nécessaires au lieu de supposer que l'ancien comportement de recherche web persiste dans le code actuel.
  — <https://github.com/huggingface/chat-ui>

## Remplacé par ceci {#superseded-by-this}

- 2023-04-25 : considérez HuggingChat comme un routeur dynamique, et non comme un point de terminaison fixe OpenAssistant LLaMA 30B. Le produit actuel fournit le routage Omni et le choix direct dans un catalogue évolutif.
- 2023-06-02 / 2023-06-11 : les premières consignes relatives au commutateur de recherche web sont obsolètes. Le README actuel indique que les anciens assistants de recherche web ont été supprimés, bien que la documentation de Chat UI décrive toujours la recherche web.
- 2025-07-01 : l'avis de fermeture ne s'applique plus. HuggingChat a annoncé son retour le 2025-10-16, et la page hébergée était en ligne lors de la vérification.

## Points encore inconnus {#still-unknown}

- La source du 2023-04-25 n'a pas pu être récupérée ; son libellé exact et son intention restent donc non vérifiés. Son lien vers la fiche de modèle ne prouve pas l'existence d'un backend de production unique.
- Le lien du 2023-06-11 ne renvoie qu'à l'URL générique du chat. La publication du 2023-06-02 confirme la date de lancement de la recherche web, mais non le fait que le 11 juin corresponde à un déploiement distinct, à un correctif ou à une republication.
- Le statut actuel de la recherche web sur l'instance hébergée n'est pas tranché. La documentation officielle de Chat UI décrit la recherche web, mais le README GitHub actuel indique que les anciens assistants de recherche web ont été supprimés. Aucune de ces sources ne confirme ce qui fonctionne sur la page hébergée.
- HuggingChat et Chat UI auto-hébergé ne sont pas des configurations identiques. Le code source public de Chat UI ne prouve pas les modèles, fonctionnalités ou la configuration des fournisseurs exacts de l'instance hébergée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/chat/ | HuggingChat - Discuter avec des modèles d'IA | 2026-09-04 |
| https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor | OpenAssistant/oasst-sft-6-llama-30b-xor · Hugging Face | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/185 | huggingchat/chat-ui · Retours sur la fonctionnalité de recherche web | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/747 | huggingchat/chat-ui · [ANNONCE] HuggingChat ferme provisoirement | 2026-09-04 |
| https://huggingface.co/spaces/huggingchat/chat-ui/discussions/764 | huggingchat/chat-ui · [NOUVEAU] HuggingChat Omni | 2026-09-04 |
| https://github.com/huggingface/chat-ui | GitHub - huggingface/chat-ui: The open source codebase powering HuggingChat | 2026-09-04 |
| https://github.com/huggingface/chat-ui/blob/main/PRIVACY.md | chat-ui/PRIVACY.md at main · huggingface/chat-ui · GitHub | 2026-09-04 |
| https://huggingface.co/docs/chat-ui/en/configuration/web-search | Recherche web · Hugging Face | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:huggingchat`, fil `huggingchat-launch`, 1 événement daté, 2023-04-25 → 2023-04-25.
- **Note pratique :** À partir du 2023-04-25, les praticiens pouvaient utiliser le point d'entrée public de HuggingChat comme interface précoce vers un modèle conversationnel lié à OpenAssistant.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
