---
title: "Conception de politiques de persona pour les systèmes LLM"
description: "Concevoir une persona LLM comme une politique comportementale versionnée, avec des limites explicites d'autorité, de confidentialité, d'escalade et d'évaluation, plutôt que comme une personnalité supposée du modèle."
tags: [llm-agents, persona, policy, safety, evaluation, privacy]
level: 3
source_sha256: 1b586484cead5814f647a72196f160fab2676062abbe7bc970833ffab51e71ef
translation: machine
translated_at: '2026-10-24'
---
# Conception de politiques de persona pour les systèmes LLM {#persona-policy-design-for-llm-systems}

**Périmètre vérifié : 2026-09-04.** Une persona est utile lorsqu'elle rend le comportement d'un agent plus prévisible pour un public et une tâche définis. Ce n'est ni un test de personnalité, ni une affirmation sur l'état interne du modèle, ni un substitut à la sécurité, au contrôle d'accès et à la vérification.

## Définir le comportement, non les adjectifs {#define-behavior-not-adjectives}

Des termes comme « amical », « strict » ou « créatif » sont trop vagues pour régir une décision concrète. Traduisez chaque qualité souhaitée en comportement observable, en règle d'exception et en chemin d'escalade.

| Intention | Politique opérationnelle |
|---|---|
| enseignement bienveillant | reconnaître la tentative de l'apprenant ; identifier l'erreur précise ; proposer l'exercice suivant approprié |
| assistance experte et concise | commencer par la décision et les éléments de preuve ; omettre le contexte non demandé ; signaler l'incertitude |
| support sûr en santé ou en droit | fournir uniquement des informations générales ; éviter les conclusions individualisées ; orienter l'utilisateur vers un professionnel approprié |
| assistant respectueux de la vie privée | collecter uniquement les champs déclarés ; expliquer la finalité et la conservation ; respecter les demandes de suppression et les changements de consentement |

La voix, le ton et le registre influent sur la présentation. Ils ne doivent pas primer sur l'exactitude factuelle, la confidentialité, une instruction de priorité supérieure ou une limite d'approbation.

## Contrat de persona {#persona-contract}

Stockez la persona effective sous forme de politique réduite et versionnée. L'exemple ci-dessous est volontairement neutre vis-à-vis du produit.

```yaml
persona_id: learning-coach
version: 2026-09-04
purpose: guide practice without inventing learner progress
audience: opted-in adult learners
voice: direct, respectful, plain language
allowed:
  - explain supplied learning material
  - ask a clarifying question when the task is ambiguous
prohibited:
  - infer sensitive traits from conversation
  - promise outcomes or credentials
  - bypass a teacher or owner approval
memory:
  allowed_fields: [declared_goal, opted_in_preference]
  retention: documented service policy
escalate_when:
  - safety risk
  - conflicting instructions
  - requested action exceeds declared authority
```

Un contrat de politique permet aux responsables ingénierie, éditorial et confidentialité d'examiner un artefact concret. Il rend aussi les changements réversibles : déployez une nouvelle version de manière délibérée, conservez la version précédente et ses résultats d'évaluation, et révoquez la politique lorsque sa finalité ne s'applique plus.

## Traiter le contenu utilisateur comme des données, non comme une autorité {#treat-user-content-as-data-not-authority}

Une persona doit continuer à respecter l'ordre d'autorité du système lorsqu'elle rencontre des instructions dans des messages, des fichiers, des sorties d'outils, des pages web, des tickets ou une mémoire récupérée. Un contenu non fiable peut demander un changement de style, mais il ne peut ni autoriser un accès, ni modifier une règle de conservation, ni faire ignorer une validation.

Pour les systèmes utilisant des outils, rendez la limite explicite : la persona peut façonner une explication, tandis que les permissions et approbations des outils déterminent ce que le système peut faire. Cela réduit le risque qu'un « personnage » convaincant masque une action dangereuse.

## État, consentement et révocation {#state-consent-and-revocation}

Si une persona s'adapte à une personne, documentez le cycle de vie de chaque champ d'état :

1. nommer le champ, sa finalité, sa source et son responsable ;
2. obtenir le consentement ou toute autre base légale requise pour cet usage ;
3. limiter la récupération à la tâche qui a besoin du champ ;
4. exposer des chemins de correction, de suppression et de révocation ;
5. tester le système après chaque changement de consentement, et pas seulement à l'intégration initiale.

Ne transformez pas une préférence de style en profil sensible par inférence. Lorsqu'un service conserve des données issues des conversations, les comportements de conservation et de suppression relèvent de la politique de données documentée du produit, et non d'une consigne informelle.

## Évaluer la politique par scénarios {#evaluate-the-policy-in-scenarios}

Évaluez une persona à l'aide de jeux de scénarios, et non sur une impression vague qu'elle « reste dans le personnage ».

| Scénario | Points à vérifier |
|---|---|
| tâche courante | la voix est claire et la réponse accomplit la tâche autorisée |
| demande ambiguë | l'agent demande des précisions ou escalade au lieu d'inventer une hypothèse |
| instruction contradictoire | la politique de priorité supérieure reste en vigueur |
| demande de données sensibles | l'agent limite la divulgation et respecte les limites de consentement |
| outil ou action externe | la persona ne s'accorde pas elle-même une permission |
| mise à jour de la politique | le comportement visé change tandis que les comportements de sécurité non liés restent stables |

Utilisez des contrôles déterministes pour les formulations interdites connues, les appels d'outils et les champs de schéma. Ajoutez une revue humaine indépendante pour les jugements de qualité, d'équité ou de sécurité qui ne peuvent pas être réduits à un validateur binaire. Consignez la version de la persona, la révision des jeux de scénarios, la configuration du modèle et des outils, ainsi que le résultat.

## Garder les modifications de persona petites et relisibles {#keep-persona-changes-small-and-reviewable}

Une politique de persona devient fragile lorsqu'elle accumule une biographie, plusieurs publics contradictoires et des règles de ton non testables. Privilégiez une politique clairement délimitée par surface de produit. Si un même système a besoin d'un rôle distinct, comme tuteur, éditeur ou triage de support, rendez le changement explicite et consignez la politique active.

Évitez de reformuler la même règle à plusieurs endroits. Une politique unique et faisant autorité, avec un ordre de priorité visible, est plus facile à tester que des fragments de prompt dispersés.

## Modes de défaillance courants {#common-failure-modes}

- **Empilement d'adjectifs :** le système ne peut pas déterminer ce qu'un trait modifie dans une décision concrète.
- **La persona prime sur la sécurité :** une voix chaleureuse ou affirmée est traitée à tort comme une autorité.
- **Profilage implicite :** des traits inférés sont conservés sans consentement ni finalité déclarée.
- **Modifications non versionnées :** le comportement change, mais aucun relecteur ne peut identifier la politique active.
- **Tests limités au style :** les réponses sonnent juste alors que le comportement des outils, de la confidentialité ou de l'escalade est erroné.
- **Mémoire permanente par défaut :** les préférences utilisateur survivent au-delà de leur finalité documentée.

## Références {#references}

- [NIST AI RMF : Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — contexte de gestion des risques pour les systèmes d'IA générative.
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) — injection de prompt, usage abusif d'outils et risques liés aux frontières des données.
- [[persona-adaptive-llm]] — un guide de conception voisin portant sur les champs de profil, la mémoire de récupération, le consentement et les limites de suppression.
