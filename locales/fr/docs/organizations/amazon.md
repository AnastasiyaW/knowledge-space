---
title: "Amazon — plateforme et modèles d'IA générative d'Amazon"
category: organizations
tags: [amazon, amazon-generative-ai-platform-and-models, amazon-nova, amazon_bedrock_codewhisperer, organization]
aliases: ["Amazon"]
level: 3
source_sha256: 31178a9e3f54d82301179f59e97570cfb1c01c535d740578682af70ac51b232d
translation: machine
translated_at: '2026-10-24'
---
# Amazon — plateforme et modèles d'IA générative d'Amazon {#amazon-amazon-generative-ai-platform-and-models}

**Ligne de développement :** `organization:amazon` · fil `amazon-generative-ai-platform-and-models`  
**Événements :** 2 datés, 2023-04-13 → 2024-12-04 · **Recherche :** 2026-09-03 · confiance : moyenne

## Ce que c'est {#what-it-is}

Amazon — dans cette ligne AWS, il existe deux parcours de travail distincts : Amazon Bedrock, plateforme gérée pour les applications et agents GenAI ; Amazon Nova, famille de modèles propriétaires dans Bedrock ; Amazon Q Developer, assistant de code dans lequel CodeWhisperer a été intégré. Capacités : - accéder aux modèles d'AWS et de fournisseurs tiers via le Model Catalog et l'API Bedrock ; - prototyper avec Nova 2 Lite et Sonic dans le playground, ou appeler Nova 2 via Converse et InvokeModel ; - utiliser Q Developer dans l'IDE pour les suggestions de code et le chat, tant que la prise en charge des plugins est active. Limite : une requête Nova peut durer jusqu'à 60 minutes, et la prise en charge des plugins IDE de Q Developer prend fin le 2027-04-30. Conclusion : pour un nouveau service GenAI, choisissez Bedrock et le modèle Nova ou tiers adapté ; CodeWhisperer/Q Developer ne doit pas être considéré comme une base à long terme pour une nouvelle intégration IDE.

## Ligne de développement {#development-line}

- **2023-04-13 — Amazon présente Bedrock et étoffe son offre d'IA générative.** Le 2023-04-13, Amazon a présenté Amazon Bedrock dans le cadre de son entrée sur le marché des plateformes d'IA générative. Les documents associés placent également Amazon CodeWhisperer dans cette extension de l'IA destinée aux développeurs, ce qui fait de cette publication une étape importante du développement de l'IA générative chez Amazon.
- **2024-12-04 — Amazon annonce les modèles Amazon Nova pour Bedrock.** Le 2024-12-04, Amazon a annoncé la famille de modèles d'IA Amazon Nova, utilisable via Amazon Bedrock. Il s'agit d'une évolution importante, car elle fait passer la ligne d'IA générative d'Amazon d'une plateforme d'accès aux modèles à des offres de modèles propriétaires nommés.

## Ce qui a changé {#what-changed}

2023-04-13 — Amazon Bedrock est sorti en preview limitée, sous forme d'API vers les modèles de base d'AWS et de fournisseurs tiers. Le même jour, CodeWhisperer est devenu généralement disponible comme assistant de code dans l'IDE, avec les niveaux individual et professional. Dès le départ, il s'agissait de produits différents : une plateforme d'inférence et un assistant de code. 2023-09-28 (trouvé aujourd'hui) — Bedrock est devenu généralement disponible : AWS a ajouté le choix géré de modèles, le provisioned throughput et les intégrations avec CloudWatch et CloudTrail ; l'état de preview a pris fin. 2024-04-30 (trouvé aujourd'hui) — Amazon CodeWhisperer a été intégré à Amazon Q Developer ; le nom autonome CodeWhisperer n'est plus le nom actuel du produit IDE. 2024-12-04 — Amazon a présenté Nova dans Bedrock : les modèles initiaux Micro (texte uniquement), Lite et Pro (multimodaux), ainsi que Canvas pour les images et Reel pour la vidéo ; Premier a été annoncé comme le modèle suivant. 2026-08-17 (trouvé aujourd'hui) — AWS a documenté que la prise en charge des plugins IDE d'Amazon Q Developer prendra fin le 2027-04-30, et indique Kiro comme voie pour des fonctionnalités comparables. 2026-09-03 (trouvé aujourd'hui) — le catalogue actuel de Bedrock et la documentation de Nova montrent une ligne plus récente, Nova 2, incluant Lite et Sonic ; pour la plupart des cas d'usage, AWS recommande l'API Converse. Ne considérez pas l'ensemble de modèles de l'annonce de 2024 comme la liste actuelle complète.

## Comment l'utiliser {#how-to-use-this}

Depuis le 2023-04-13, les praticiens qui évaluent la pile d'IA d'Amazon doivent considérer Bedrock comme une option de plateforme centrale ; depuis le 2024-12-04, ils doivent aussi évaluer Amazon Nova aux côtés des modèles tiers de Bedrock pour les charges de travail concernées.

1. Pour une nouvelle application GenAI, ouvrez le Model Catalog d'Amazon Bedrock, sélectionnez un modèle et vérifiez les autorisations AWS Marketplace : avec des autorisations correctes, les modèles sont disponibles par défaut ; lancez ensuite le playground ou appelez InvokeModel ou Converse.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html>
2. Pour un prototype rapide avec Amazon Nova 2, utilisez le playground Chat ou Text avec Nova 2 Lite ou Sonic ; pour une application, passez à l'API Bedrock InvokeModel ou Converse.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/getting-started-nova-2.html>
3. Dans le code, créez un client bedrock-runtime et appelez Converse avec un modelId et un tableau de messages ; ajoutez une instruction system, des paramètres d'inférence et une réponse en flux uniquement lorsque l'interface en a besoin.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-converse-api.html>
4. Pour un scénario soumis à des contraintes de conformité, liez un guardrail précis et sa version numérique à la politique IAM au moyen de la condition bedrock:GuardrailIdentifier, afin qu'une requête sans la protection requise soit rejetée.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html>
5. Si l'équipe continue temporairement d'utiliser Amazon Q Developer, installez l'extension pour votre IDE et connectez-vous avec AWS Builder ID ou IAM Identity Center ; parallèlement, établissez un plan de migration distinct avant le 2027-04-30.
  — <https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html>

## Bonnes pratiques {#best-practices}

- Par défaut, choisissez Converse : il offre une interface unifiée pour différents modèles ; réservez l'API Invoke aux cas où le schéma natif d'un modèle donné est requis.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html>
- Configurez le read timeout du client pour les requêtes Nova longues : AWS prévient qu'une inférence isolée peut durer jusqu'à 60 minutes et indique une configuration de 3600 secondes.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html>
- Rédigez une instruction simple et sans ambiguïté après le contexte, séparez les données d'entrée par des délimiteurs, précisez explicitement le format de sortie et les paramètres d'inférence ; vérifiez les modifications de prompt sur un jeu de données de test réservé, et non seulement sur les exemples de développement.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html>
- Ne comptez pas sur le code appelant pour appliquer volontairement une protection : IAM doit exiger un identifiant et une version de guardrail précis pour chaque requête d'inférence.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html>
- Avant d'accepter une suggestion de CodeWhisperer/Q Developer, vérifiez le code, l'URL du dépôt source et la licence si le système a signalé une similarité avec du code public ; cette vérification ne peut pas être remplacée par une acceptation automatique de la recommandation.
  — <https://aws.amazon.com/ru/codewhisperer/>

## Remplacé par ce qui suit {#superseded-by-this}

- 2023-04-13 — le statut de Amazon Bedrock en tant que preview limitée est obsolète : le service est devenu généralement disponible le 2023-09-28.
- 2023-04-13 — le nom autonome Amazon CodeWhisperer comme produit IDE actuel est obsolète : depuis le 2024-04-30, il fait partie d'Amazon Q Developer.
- 2024-12-04 — considérer Nova Micro, Lite, Pro, Canvas et Reel d'origine comme le choix complet et actuel de modèles est obsolète : le catalogue actuel inclut la ligne Nova 2, y compris Lite et Sonic.
- Jusqu'au 2026-08-17 — la recommandation de construire une nouvelle intégration IDE durable sur Amazon Q Developer sans délai de migration est obsolète : la fin de prise en charge des seuls plugins IDE est annoncée pour le 2027-04-30.

## Points encore inconnus {#still-unknown}

- Amazon Nova/Bedrock et CodeWhisperer/Amazon Q Developer sont deux lignes de produits AWS distinctes, et non un seul produit ni des versions successives ; cette fiche ne les réunit qu'au niveau de l'entreprise.
- La notification du 2027-04-30 concerne précisément les plugins IDE d'Amazon Q Developer ; à partir des sources vérifiées, on ne peut pas déduire le statut de Q Developer CLI, de la console et des autres composants après cette date.
- La disponibilité de Nova, les tarifs, les quotas, les conditions Marketplace et les autorisations requises dépendent de la région et du compte AWS ; cette vérification n'a pas permis d'accéder à un compte ou une région précis.
- L'annonce de 2024 prévoyait Nova Premier pour le premier trimestre 2025 ; sa disponibilité régionale actuelle et son prix n'ont pas été vérifiés séparément.
- Pour Bedrock au 2023-04-13, une source secondaire datée a été utilisée ; l'annonce primaire d'AWS concernant la preview limitée n'a pas été obtenue.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://techcrunch.com/2023/04/13/with-bedrock-amazon-enters-the-generative-ai-race/ | With Bedrock, Amazon enters the generative AI race | 2026-09-03 |
| https://aws.amazon.com/ru/codewhisperer/ | Генератор кода на основе искусственного интеллекта – Amazon CodeWhisperer – AWS | 2026-09-03 |
| https://aws.amazon.com/about-aws/whats-new/2023/04/amazon-codewhisperer-generally-available/ | Amazon CodeWhisperer is now generally available | 2026-09-03 |
| https://aws.amazon.com/about-aws/whats-new/2023/09/amazon-bedrock-generally-available/ | Amazon Bedrock is now generally available | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/doc-history.html | Document history for Amazon Q Developer User Guide | 2026-09-03 |
| https://www.aboutamazon.com/news/aws/amazon-nova-artificial-intelligence-bedrock-aws | Amazon Nova: Meet our new foundation models in Amazon Bedrock | 2026-09-03 |
| https://aws.amazon.com/bedrock | Amazon Bedrock – Build genAI applications and agents at production scale – AWS | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html | Models at a glance - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html | Request access to models - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/getting-started-nova-2.html | Getting started with Amazon Nova 2 - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-converse-api.html | Using the Converse API - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html | Core inference - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html | Design a prompt - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html | Enforce the use of specific guardrails in model inference requests - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html | Installing the Amazon Q Developer extension or plugin in your IDE - Amazon Q Developer | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html | Amazon Q Developer IDE plugins end of support - Amazon Q Developer | 2026-09-03 |

## Brief agent {#agent-brief}

- **Sujet :** `organization:amazon`, fil `amazon-generative-ai-platform-and-models`, 2 événements datés du 2023-04-13 au 2024-12-04.
- **Note pratique :** depuis le 2023-04-13, les praticiens qui évaluent la pile d'IA d'Amazon doivent considérer Bedrock comme une option de plateforme centrale ; depuis le 2024-12-04, ils doivent aussi évaluer Amazon Nova aux côtés des modèles tiers de Bedrock pour les charges de travail concernées.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
