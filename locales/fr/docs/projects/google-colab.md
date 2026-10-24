---
title: "Google Colab"
category: projects
date: 2023-05-19
tags: [colab_ai_codey, google-colab, google-colab-platform-evolution, google-colab:subscription-policy, project]
aliases: ["Google Colab"]
level: 3
source_sha256: 2509e165f739f1b50df56a84ec82beb2ff4accf9cba2a78bc659ed516d5e831d
translation: machine
translated_at: '2026-10-24'
---
# Google Colab {#google-colab}

**Ligne de développement :** `project:google-colab` · fil `google-colab-platform-evolution`  
**Dernier événement :** 2023-05-19 · 2 événements datés depuis 2022-08-31 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Google Colab est un Jupyter hébergé destiné aux utilisateurs de Python qui ont besoin d'un notebook dans le navigateur plutôt que d'une installation locale de Jupyter.

- Machine virtuelle dédiée qui exécute le code de l'utilisateur.
- Accès aux GPU et aux TPU lorsque des ressources de calcul sont disponibles.
- Intégration avec Google Drive et GitHub pour stocker, partager et charger des fichiers `.ipynb`.
- Intégration de Gemini qui ajoute un chat, la complétion de code et un agent de science des données pour les comptes éligibles.

L'environnement d'exécution gratuit n'est pas garanti ; il dure généralement 12 heures au maximum, et les quotas de calcul évoluent avec le temps.

La plateforme convient aux tutoriels, aux prototypes rapides et aux tâches interactives de machine learning, mais pas aux charges de calcul continues ou à ressources fixes.

## Ligne de développement {#development-line}

- **2022-08-31 — Une modification de la politique d'abonnement de Google Colab a été signalée publiquement.** L'enregistrement lié n'est pas consultable ; la modification précise de l'abonnement n'est pas confirmée et ne peut pas servir de règle en vigueur.
- **2023-05-19 — Google Colab a introduit des fonctionnalités de codage assisté par IA.** Google a annoncé les fonctionnalités Codey, à savoir la génération de code à partir de langage naturel, la complétion de code pour les abonnés payants éligibles et un assistant de discussion, d'abord pour les comptes payants aux États-Unis.

## Changements {#what-changed}

Google Colab a mis à jour les politiques d'accès au calcul et son assistant IA intégré.

- 2022-08-31 : l'enregistrement lié n'est pas consultable ; la modification de l'abonnement n'est donc pas confirmée et ne peut pas servir de règle en vigueur.
- 2023-05-19 (annonce officielle datée du 2023-05-17) : Google a annoncé les fonctionnalités Codey, notamment la génération de code à partir de langage naturel, la complétion de code pour les utilisateurs payants éligibles et un assistant de discussion, d'abord pour les formules payantes aux États-Unis.
- 2026-04-08 : l'intégration de Gemini a ajouté des instructions personnalisées enregistrées dans le notebook et le Learn Mode pour un tutorat pas à pas.
- 2026-09-04 : la documentation actuelle décrit Colab orienté IA (AI-First Colab) avec le chat Gemini, la complétion de code et un Data Science Agent qui propose un plan et l'exécute après validation de l'utilisateur, l'accès variant selon l'âge et la région.
- 2026-09-04 : l'allocation de calcul est explicitement dynamique ; ni les formules gratuites ni les formules payantes ne garantissent des ressources, et les limites, la durée de vie des machines virtuelles et les types d'accélérateurs fluctuent.

Le déploiement initial de Codey ne reflète pas l'interface Gemini actuelle, et les anciennes déclarations tarifaires ne remplacent pas la page d'abonnement en vigueur.

Colab reste un service unique, mais les utilisateurs doivent évaluer séparément les environnements d'exécution disponibles et les outils IA.

## Mode d'emploi {#how-to-use-this}

Depuis le 2023-05-19, les praticiens doivent considérer Google Colab à la fois comme un environnement de notebook hébergé et comme un environnement de codage assisté par IA, tout en vérifiant la politique d'abonnement et d'accès applicable à leur charge de travail.

1. Ouvrez Colab, créez un nouveau notebook via File, ou importez un fichier `.ipynb` existant via File > Upload notebook.
  — <https://research.google.com/colaboratory/faq.html>
2. Ajoutez des cellules de code et de texte ; si la charge de travail nécessite une accélération matérielle, sélectionnez Runtime > Change runtime type pour choisir un GPU ou un TPU.
  — <https://research.google.com/colaboratory/faq.html>
3. Enregistrez les notebooks dans Google Drive ou chargez-les depuis GitHub ; partagez les notebooks via Share, en gardant à l'esprit que la machine virtuelle sous-jacente et les fichiers locaux ne sont pas transférés.
  — <https://research.google.com/colaboratory/faq.html>
4. Ouvrez l'assistant Gemini en bas du notebook, décrivez la tâche et examinez le plan généré avant d'exécuter le code.
  — <https://research.google.com/colaboratory/faq.html>
5. Pour utiliser une machine locale, lancez Jupyter ou un environnement d'exécution local compatible, sélectionnez Connect > Connect to local runtime et indiquez l'URL du backend.
  — <https://research.google.com/colaboratory/local-runtimes.html>

## Bonnes pratiques {#best-practices}

- Considérez les machines virtuelles gérées comme temporaires : installez les dépendances et téléchargez les fichiers d'entrée directement dans le notebook, et conservez les résultats en dehors de l'environnement d'exécution.
  — <https://research.google.com/colaboratory/faq.html>
- Évitez de demander des GPU ou une mémoire importante sans nécessité, et fermez les onglets inactifs pour préserver le quota de calcul.
  — <https://research.google.com/colaboratory/faq.html>
- Épinglez explicitement les versions des bibliothèques pour les notebooks partagés ou pédagogiques ; sélectionnez une version plus ancienne de l'environnement d'exécution si nécessaire, en gardant à l'esprit que les anciennes versions ont une durée de vie limitée.
  — <https://research.google.com/colaboratory/runtime-version-faq.html>
- Relisez, testez et validez le code généré par Gemini ; ne transmettez pas de données confidentielles ou personnelles dans les requêtes adressées à l'IA.
  — <https://research.google.com/colaboratory/faq.html>
- Ne connectez des environnements d'exécution locaux qu'à des notebooks de confiance dont le code a été vérifié, car ces environnements peuvent exécuter des commandes shell arbitraires et lire des fichiers locaux.
  — <https://research.google.com/colaboratory/local-runtimes.html>

## Remplacé par ce document {#superseded-by-this}

- 2022-08-31 : les affirmations non vérifiées sur les règles d'abonnement sont obsolètes ; la politique actuelle définit tous les quotas et ressources de calcul comme dynamiques.
- 2023-05-17/2023-05-19 : le déploiement de Codey pour les comptes payants aux États-Unis est remplacé par AI-First Colab utilisant Gemini pour les utilisateurs éligibles.
- 2025-03-21 : le lancement de Colab via les machines virtuelles GCP Marketplace est déprécié ; la documentation Google oriente les utilisateurs vers Colab Enterprise ou les environnements d'exécution locaux.

## Points inconnus {#still-unknown}

- Le texte source du 2022-08-31 est inaccessible, si bien que la modification précise de la politique d'abonnement n'est pas confirmée.
- La date d'événement enregistrée, 2023-05-19, diffère de la date d'annonce officielle, 2023-05-17.
- Les limites de calcul et le codage assisté par IA relèvent du même service, mais Google n'a confirmé aucun lien de causalité entre les évolutions de politique.
- Les tarifs exacts, les unités de calcul, les modèles de GPU et de TPU ainsi que la disponibilité de Gemini varient selon le compte, la formule et la région, et doivent être vérifiés directement dans l'interface d'abonnement.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://twitter.com/EMostaque/status/1564773589886320640 | Publication de @EMostaque — contenu indisponible lors de la revue | 2026-09-04 |
| https://blog.google/technology/developers/google-colab-ai-coding-features/ | AI-powered coding, free of charge with Colab | 2026-09-04 |
| https://research.google.com/colaboratory/faq.html | Frequently Asked Questions | 2026-09-04 |
| https://blog.google/innovation-and-ai/technology/developers-tools/colab-updates/ | Introducing Learn Mode: your personal coding tutor in Google Colab | 2026-09-04 |
| https://research.google.com/colaboratory/local-runtimes.html | Local runtimes | 2026-09-04 |
| https://research.google.com/colaboratory/runtime-version-faq.html | Frequently Asked Questions - Past Runtime Versions | 2026-09-04 |
| https://research.google.com/colaboratory/marketplace.html | Instructions for starting a GCE VM on Colab via GCP Marketplace | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:google-colab`, fil `google-colab-platform-evolution`, 2 événements datés du 2022-08-31 au 2023-05-19.
- **Note pratique :** Depuis le 2023-05-19, les praticiens doivent considérer Google Colab à la fois comme un environnement de notebook hébergé et comme un environnement de codage assisté par IA, tout en vérifiant la politique d'abonnement et d'accès applicable à leur charge de travail.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
