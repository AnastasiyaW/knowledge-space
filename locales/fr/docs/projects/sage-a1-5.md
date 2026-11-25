---
title: "Sage-A1.5 : sage-a1-5-release — Sortie de Sage A1 5"
category: "projects"
date: 2026-10-22
tags: ["project", "sage-a1-5", "sage-a1-5-release"]
aliases: ["Sage-A1.5: sage-a1-5-release"]
level: 2
source_sha256: 565f221edffe659f96a7fdb836597b250480c7eac74c779098dee491d48ee3f5
translation: machine
translated_at: '2026-10-24'
---
# Sage-A1.5 : sage-a1-5-release — Sortie de Sage A1 5 {#sage-a15-sage-a1-5-release-sage-a1-5-release}

**Ligne de développement :** project:sage-a1-5 · fil sage-a1-5-release  
**Dernier événement :** 2026-10-22 · 2 événements datés depuis le 2026-10-22 · **Recherche :** 2026-10-23 · confiance : moyenne

## Présentation {#what-it-is}

Sage-A1.5 est un modèle de fondation agentique à poids ouverts, de type mixture-of-experts de 35B paramètres. Il s'adresse aux chercheurs et aux ingénieurs logiciels qui exécutent des tâches à long horizon, et rivalise directement avec les modèles de raisonnement propriétaires.

- **Sous-agents parallèles :** il les orchestre, chacun dans un contexte d'exécution isolé.
- **Auto-vérification :** il se contrôle lui-même au sein de sa chaîne de pensée, sans modèle de récompense externe.
- **Découverte scientifique :** il exécute des flux de travail transdisciplinaires.
- **Service :** il expose une API compatible OpenAI via vLLM ou SGLang.

3B des 35B paramètres sont actifs à chaque passe avant. Le contexte est de 256K tokens nativement, extensible à 512K via YaRN. Sous une charge élevée de sous-agents concurrents, la surcharge du routage MoE et la capacité mémoire fixent la limite.

C'est une base ouverte, efficace et auto-hébergeable, adaptée aux pipelines agentiques complexes qui doivent se corriger en cours de trajectoire.

## Ligne de développement {#development-line}

- **2026-10-22 — Shanghai AI Lab publie le modèle agentique Sage-A1.5.** Il s'agit d'un modèle agentique MoE de 35B paramètres, construit sur Qwen3.6-35B-A3B et Agents-A1. Il a été annoncé avec une fenêtre de contexte de 262K tokens et un service compatible OpenAI via SGLang ou vLLM. Scores annoncés : GAIA 95,1, XBench-DS 92,0, SWE-bench Pro 61,2, MLE-Lite 65,2.
- **2026-10-22 — autres informations relevées à cette date.**
  - Le modèle est publié sous licence Apache 2.0 par le groupe InternScience de Shanghai AI Lab. Il active 3B paramètres par token sur 35B au total. Il ajoute la délégation native de tâches multi-agents via des sous-agents parallèles isolés. (2026-10-22) — <https://huggingface.co/InternScience/Sage-A1.5>
  - La fiche du modèle décrit une auto-vérification intégrée à la chaîne de pensée : le modèle se corrige pendant l'exécution, sans vérificateurs externes. Le contexte dépasse les 256K natifs et atteint 512K tokens via YaRN. (2026-10-22) — <https://huggingface.co/InternScience/Sage-A1.5>

## Ce qui a changé {#what-changed}

La série Agents-A1 utilisait des modèles denses ; Sage-A1.5 est un mixture-of-experts épars basé sur Qwen3.6-35B-A3B. Les pipelines séquentiels à agent unique cèdent la place à une délégation dynamique vers des sous-agents aux contextes isolés. La correction d'erreurs au sein d'une trajectoire reposait auparavant sur des modèles critiques externes ; elle est désormais intégrée à la chaîne de pensée. Le contexte est passé des fenêtres standard à 256K nativement, extensibles à 512K avec YaRN.

## Mode d'emploi {#how-to-use-this}

1. Téléchargez les poids depuis le dépôt InternScience/Sage-A1.5 sur Hugging Face ou ModelScope.
  — <https://huggingface.co/InternScience/Sage-A1.5>
2. Déployez avec vLLM ou SGLang en utilisant la configuration MoE standard de Qwen, afin d'exposer un point de terminaison d'API compatible OpenAI.
  — <https://huggingface.co/InternScience/Sage-A1.5>
3. Activez la création de sous-agents dans le runtime d'agent, afin que le modèle puisse répartir des sous-tâches en parallèle dans des contextes isolés.
  — <https://huggingface.co/InternScience/Sage-A1.5>
4. Activez la vérification native dans les paramètres de génération ou le prompt système, afin que le modèle se relise et récupère de ses erreurs sur les longues trajectoires.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Bonnes pratiques {#best-practices}

- Attribuez à chaque branche d'investigation parallèle son propre contexte de sous-agent, afin que les sorties intermédiaires bruitées des outils ne distraient pas l'agent racine.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Appliquez la mise à l'échelle YaRN lorsqu'un dépôt ou un ensemble d'articles dépasse la fenêtre native de 256K tokens.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Servez les quantifications FP8/INT4 avec SGLang ou vLLM pour réduire l'usage mémoire tout en conservant un routage MoE efficace.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Remplacé par cette version {#superseded-by-this}

- Les architectures denses Agents-A1 et les pipelines séquentiels à agent unique sont remplacés par l'architecture MoE de Sage-A1.5, avec orchestration native des sous-agents.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Les modèles critiques externes pour l'auto-correction des trajectoires sont remplacés par la vérification intégrée à la chaîne de pensée de Sage-A1.5.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Points restant inconnus {#still-unknown}

- Les retours de la communauté et les rapports de bogues issus des forums de praticiens n'ont pas pu être vérifiés : les recherches n'ont mené qu'à des pages de redirection.
- Les besoins en bande passante mémoire et les performances sur différents accélérateurs matériels nationaux n'ont pas encore fait l'objet de benchmarks indépendants.

## Sources {#sources}

| source | titre | consultée |
|---|---|---|
| https://huggingface.co/InternScience/Sage-A1.5 | InternScience/Sage-A1.5 · Hugging Face | 2026-10-23 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** project:sage-a1-5, fil sage-a1-5-release, 2 événements datés du 2026-10-22 au 2026-10-22.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
