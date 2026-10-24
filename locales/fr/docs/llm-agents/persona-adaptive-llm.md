---
title: "Personnalisation dans les systèmes LLM"
description: "Un cadre de décision pour les champs de profil, la mémoire par recherche et la personnalisation par adaptateurs, avec isolation des locataires, évaluation, consentement et limites de suppression."
tags: [personalization, llm, lora, peft, privacy, evaluation]
level: 3
source_sha256: db84ab10e1c4365be242dc846d3035c2cd9700d02cb6f1fd5dc5e9ebfccd22bd
translation: machine
translated_at: '2026-10-24'
---
# Personnalisation dans les systèmes LLM {#personalization-in-llm-systems}

**Périmètre vérifié : 2026-09-03.** La personnalisation n'est pas une fonctionnalité unique, et un persona n'est pas un fait fiable sur une personne. Séparez les préférences explicites, l'historique récupéré, l'état de la tâche et les adaptations du modèle, afin que chacun ait un responsable, une provenance, une méthode d'évaluation et un chemin de suppression.

La personnalisation par adaptateurs peut être utile, mais c'est un choix opérationnel et de gouvernance des données, et non un remplacement par défaut d'un système de profil et de recherche bien délimité.

## Choisir la couche la plus petite et réversible {#choose-the-smallest-reversible-layer}

| Besoin | Point de départ | Pourquoi |
|---|---|---|
| format ou ton de réponse pour une tâche | demande explicite ou politique système bornée | temporaire et facile à inspecter |
| préférence stable de l'utilisateur | champ de profil structuré avec source et expiration | vérifiable et corrigeable |
| contexte factuel passé | recherche tenant compte de la provenance | les données peuvent être mises à jour ou supprimées indépendamment |
| comportement répété du modèle sur une population définie | adaptateur ou fine-tuning évalué | exige traçabilité, déploiement progressif et retour arrière |

N'entraînez pas un adaptateur par utilisateur simplement parce qu'il existe quelques préférences. La recherche et la configuration structurée offrent en général un chemin de correction et de suppression plus clair.

## Modéliser l'enregistrement de personnalisation {#model-the-personalization-record}

Conservez un enregistrement côté serveur qui sépare l'observation de l'autorisation :

```json
{
  "subject_ref": "opaque-user-reference",
  "attribute": "preferred_explanation_style",
  "value": "short examples before detail",
  "source": "user-confirmed-setting",
  "confidence": "confirmed",
  "allowed_uses": ["response-formatting"],
  "review_at": "2026-12-01",
  "revocation_ref": "privacy-request-reference"
}
```

L'application, et non le modèle, décide quels champs sont éligibles pour une requête. Ne laissez jamais un prompt non fiable sélectionner des lignes de profil arbitraires, des enregistrements d'autres locataires, des chemins d'adaptateurs ou des artefacts d'entraînement.

## Ce que LoRA et PEFT apportent réellement {#what-lora-and-peft-actually-provide}

Le fine-tuning efficace en paramètres (PEFT) attache des adaptateurs entraînables à un modèle de base, au lieu de mettre à jour chaque paramètre de base. Les outils PEFT actuels peuvent charger, changer, activer, désactiver et supprimer des adaptateurs nommés ; la compatibilité dépend toujours du modèle, du type d'adaptateur et de l'environnement d'exécution. [Vue d'ensemble de PEFT](https://huggingface.co/docs/transformers/peft) [Gestion des adaptateurs PEFT](https://huggingface.co/docs/peft/en/developer_guides/troubleshooting)

Il s'agit d'une capacité d'implémentation, et non d'une garantie que :

- un adaptateur représente fidèlement une personne ;
- deux adaptateurs se composent en toute sécurité ;
- un adaptateur remplacé à chaud a un coût de latence ou de mémoire fixe ;
- la suppression d'un profil supprime aussi chaque effet dérivé de l'entraînement ;
- un point de contrôle est sûr à charger depuis une source non fiable.

Traitez les affirmations sur l'adaptation des modèles comme des hypothèses qui nécessitent un plan d'évaluation.

## Frontière de service {#serving-boundary}

vLLM peut servir des adaptateurs LoRA nommés sur un modèle de base pris en charge, et documente à la fois la configuration au démarrage et le chargement dynamique d'adaptateurs. Il avertit explicitement que les mises à jour d'adaptateurs à l'exécution ne doivent pas être activées pour des clients non fiables. [Adaptateurs LoRA dans vLLM](https://docs.vllm.ai/en/stable/features/lora/) [Recommandations de sécurité de vLLM](https://docs.vllm.ai/en/stable/usage/security/)

Pour un service multi-locataires :

1. associez un locataire authentifié et une politique approuvée à un identifiant d'adaptateur présent dans une liste d'autorisation, côté serveur ;
2. épinglez la révision du modèle de base, la configuration de l'adaptateur, l'empreinte de l'artefact et le résultat d'évaluation ;
3. exposez aux utilisateurs finaux des points de génération, et non des points de chargement d'adaptateurs arbitraires ;
4. isolez le chargement administratif du traitement des requêtes ;
5. conservez un reçu de déploiement idempotent et une cible de retour arrière ;
6. rejetez tout adaptateur inconnu, tout modèle de base non concordant ou tout artefact non vérifié.

Le chargement dynamique est une opération réservée à un administrateur de confiance, sauf si une conception isolée et vérifiée démontre le contraire.

## Évaluation avant personnalisation {#evaluation-before-personalization}

Comparez les approches viables les plus simples sur un corpus fixe et consenti :

| Dimension | Preuves attendues |
|---|---|
| utilité pour la tâche | test d'acceptation déclaré à l'avance ou grille d'évaluation en aveugle |
| fidélité aux préférences | exemples confirmés par l'utilisateur et taux de correction |
| sécurité | tests inter-locataires, d'injection de prompt et de profil non autorisé |
| confidentialité | revue des flux de données, règle de conservation, plan de suppression ou de réentraînement |
| exploitation | reçus de latence, mémoire, erreurs et retour arrière dans l'environnement cible |

Exécutez la même suite de tests sur le modèle de base, sur la référence profil/recherche et sur le modèle adapté. Une amélioration de qualité ne justifie pas un échec de confidentialité ou d'isolation.

## Cycle de vie des données {#data-lifecycle}

Avant de collecter des données pour une couche de personnalisation, décidez :

- la finalité, la base juridique et les classes de données autorisées pour la juridiction concernée ;
- qui peut voir, modifier, exporter ou révoquer chaque enregistrement ;
- si un adaptateur contient des données qui exigent un réentraînement, un remplacement ou un retrait après une révocation ;
- comment les sauvegardes et les jeux de données d'évaluation suivent la même règle de conservation ;
- comment le système prouvera qu'une suppression ou un retour arrière s'est achevé.

Le Privacy Framework du NIST est une référence utile pour la gestion des risques, mais il ne remplace pas les exigences juridiques ou propres à un domaine. [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

## Quand un adaptateur est justifié {#when-an-adapter-is-justified}

Utilisez un adaptateur appris uniquement si toutes les conditions suivantes sont réunies :

1. le comportement est assez stable pour être défini et évalué ;
2. les références profil et recherche ont été mesurées et s'avèrent insuffisantes ;
3. les responsabilités en matière de consentement, de locataires, de provenance et de suppression sont définies ;
4. l'artefact a un modèle de base épinglé et une évaluation reproductible ;
5. un chemin de retour arrière et de traitement d'incident existe avant toute exposition.

Sinon, conservez la personnalisation dans des données structurées et modifiables.

## Pièges {#gotchas}

- **Un prompt désigne un autre utilisateur.** Il ne doit pas sélectionner son historique ou son adaptateur. **Correctif :** lier la sélection à la politique du locataire authentifié, en dehors du modèle.
- **Un adaptateur fonctionne dans un notebook.** Ce n'est pas une preuve de production multi-locataires. **Correctif :** testez l'isolation, la mémoire, les pannes et le retour arrière dans l'environnement de service réel.
- **Un point de terminaison à l'exécution accepte des chemins arbitraires.** Le chargement d'artefacts devient un risque de code et de chaîne d'approvisionnement. **Correctif :** utilisez une liste d'autorisation, la vérification des artefacts et un chargement réservé aux administrateurs.
- **Une préférence devient obsolète.** La réutiliser peut rendre le système moins utile. **Correctif :** stockez la source, la date de revue et la procédure de correction.
- **Une demande de suppression n'atteint que la table de profils.** Les adaptateurs dérivés ou les copies d'évaluation peuvent subsister. **Correctif :** tenez un inventaire de traçabilité et vérifiez l'ensemble du processus de suppression.

## Sources {#sources}

- [Hugging Face PEFT dans Transformers](https://huggingface.co/docs/transformers/peft)
- [Gestion des adaptateurs PEFT sur Hugging Face](https://huggingface.co/docs/peft/en/developer_guides/troubleshooting)
- [Adaptateurs LoRA dans vLLM](https://docs.vllm.ai/en/stable/features/lora/)
- [Recommandations de sécurité de vLLM](https://docs.vllm.ai/en/stable/usage/security/)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

## Voir aussi {#see-also}

- [[agent-memory]]
- [[llm-fine-tuning-practical]]
- [[agentic-security-2026]]
- [[ai-adaptive-learning-systems]]
