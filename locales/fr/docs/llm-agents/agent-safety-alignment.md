---
title: "Sécurité et alignement des agents"
description: "Construire la sécurité des agents comme des frontières explicites d'autorité, de données, d'outils, d'approbation et de preuves, plutôt que comme une simple promesse dans le prompt."
tags: [llm-agents, safety, alignment, guardrails, prompt-injection, sandboxing, approvals]
level: 5
source_sha256: c399383899c40f672c7e15c143344a9e5d3d43e5f27e9ebd55928224a707ca3c
translation: machine
translated_at: '2026-10-24'
---
# Sécurité et alignement des agents (septembre 2026) {#agent-safety-and-alignment-september-2026}

Contexte de version : le comportement des modèles, les protocoles d'outils, les produits de sandbox, les fonctionnalités de modération et les contrôles de politique des fournisseurs évoluent. Cette page décrit une architecture de sécurité au niveau produit, qui doit être évaluée au regard du modèle exact, des outils, des classes de données et de l'environnement de déploiement.

Un agent peut résumer, planifier, appeler des outils, écrire des fichiers ou demander des effets externes. Le discours d'alignement dans un prompt système peut guider le comportement, mais il ne crée pas d'autorisation, n'isole pas les données, ne valide pas un paiement et ne prouve pas le résultat d'une action. La sécurité repose sur des contrôles techniques et opérationnels superposés.

## Commencer par un modèle de menace {#start-with-a-threat-model}

Identifiez ce qui est de confiance, ce qui ne l'est pas, et quels effets nécessitent une décision d'autorité distincte.

| Frontière | Exemples | Contrôle requis |
|---|---|---|
| Politique de confiance | configuration applicative, schémas approuvés, règles signées | versionnement, contrôle d'accès, revue des changements |
| Contenu non fiable | saisie utilisateur, pages web, courriels, documents récupérés, sorties d'outils | traiter comme des données ; jamais comme une autorité |
| Sortie du modèle | réponse proposée, arguments d'outils, décision de routage | schéma, validation métier, autorisation |
| Identifiants et identité | compte de service, périmètre de locataire, session utilisateur | moindre privilège, expiration, audit |
| Effet externe | envoi, publication, déploiement, achat, suppression | approbation, idempotence, reçu terminal |

Un modèle de menace doit nommer les actifs, les acteurs, les points d'entrée, l'impact d'une défaillance, le responsable du contrôle et la preuve nécessaire pour affirmer que le contrôle a fonctionné.

## L'injection de prompt est un problème de frontière de données {#prompt-injection-is-a-data-boundary-problem}

Les instructions intégrées dans un document, une page web, un résultat d'outil ou un message utilisateur sont du contenu non fiable. Une suppression de texte fondée sur des motifs ne suffit pas à les rendre sûres : un attaquant peut reformuler, encoder ces instructions ou exploiter un flux d'outil plutôt qu'une formule précise.

Construisez un chemin plus sûr :

1. identifier explicitement les instructions de confiance et les entrées non fiables ;
2. ne transmettre que le minimum de données nécessaire à la tâche ;
3. restreindre le modèle à un ensemble d'outils étroit et approuvé localement ;
4. valider chaque appel d'outil proposé en dehors du modèle ;
5. garder l'autorisation, le périmètre de locataire et les effets externes dans du code déterministe ;
6. tester les contenus adverses dans le pipeline réel de récupération et d'outils.

Les recommandations de sécurité actuelles d'OpenAI préconisent de contraindre les entrées et les sorties et de recourir à une revue humaine lorsque c'est approprié. Ce sont des mesures de réduction de risque, et non une garantie qu'un contenu arbitraire soit sûr. [Bonnes pratiques de sécurité d'OpenAI](https://developers.openai.com/api/docs/guides/safety-best-practices)

## Accorder des capacités, non des intentions larges {#grant-capabilities-not-broad-intent}

Utilisez une référence de capacité ou d'approbation de courte durée et immuable pour une action. Stockez-la côté serveur ou signez-la ; ne laissez pas l'exécutant modifier ses champs :

```json
{
  "capability_id": "cap_01...",
  "capability_profile": "effect-capability/v1",
  "issuer": "policy-service",
  "issuer_key_id": "policy-service-key-2026-01",
  "subject": "workflow:research-review",
  "audience": "editorial-effect-service",
  "presenter_principal": "workload:research-reviewer@prod",
  "presenter_key_thumbprint": "sha256:...",
  "identity_source": "approved-workload-identity",
  "task_id": "publish-research-044",
  "action": "create_draft",
  "arguments_digest": "sha256:...",
  "resource_scope": "project:happyin-space",
  "data_classification": "public",
  "approval_decision_ref": "approval:appr_01...",
  "idempotency_key": "publish-research-044:v1",
  "expires_at": "2026-09-03T16:00:00Z",
  "policy_revision": "editorial-policy@6",
  "integrity_proof": "server-record-or-signature"
}
```

L'agent peut demander une action, mais le point d'application résout ou vérifie l'enregistrement immuable, puis contrôle avant exécution le profil, l'émetteur, la clé liée à l'émetteur, le sujet, la tâche, le condensat des arguments de l'action, le périmètre, l'expiration, la décision d'approbation et la clé d'idempotence. Un enregistrement serveur doit provenir d'un magasin autorisé ; une capacité signée doit être vérifiée auprès d'un émetteur présent dans une liste d'autorisation et avec la clé configurée pour cet émetteur. Les émetteurs inconnus, les mauvais profils et les signatures invalides échouent en mode fermé.

Le service d'effet est la frontière de destinataire et de terminaison de l'identité. Il n'accepte l'identité du présentateur que depuis son vérificateur d'identité de charge de travail configuré, jamais depuis un en-tête transmis par l'appelant. Il exige que le principal authentifié en direct soit égal à `presenter_principal` et une preuve de possession de l'identifiant correspondant à `presenter_key_thumbprint` ; il exige par ailleurs que `audience` soit égal à ce service local. Une valeur absente ou non égale rejette l'action, de sorte qu'une capacité copiée ne puisse pas être rejouée par un autre principal. Les schémas de jetons liés au certificat ou à la clé illustrent cette liaison et la validation du destinataire. [RFC 8705](https://www.rfc-editor.org/rfc/rfc8705) [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725)

Tout argument ou périmètre modifié exige une nouvelle capacité. Un agent ne peut pas étendre son propre périmètre en affirmant qu'une tâche urgente nécessite davantage d'accès.

## Placer les effets irréversibles derrière une barrière {#put-irreversible-effects-behind-a-gate}

Utilisez un flux allant de la proposition à l'effet :

```text
propose -> parse and validate -> authorize -> approve if required
       -> atomically reserve effect key -> execute -> reconcile -> terminal receipt
```

Le reçu terminal doit indiquer si l'effet externe a eu lieu, et non simplement que le modèle a produit un message de succès. Un délai d'attente ou un navigateur déconnecté constitue un état inconnu tant que l'effet n'a pas été réconcilié.

Avant un effet externe, réservez de manière atomique le tuple `capability_id`, `idempotency_key`, `arguments_digest` canonique et `resource_scope`. Une nouvelle tentative identique renvoie le reçu terminal d'origine ; un doublon en cours attend ou déclenche une réconciliation. Réutiliser une clé avec une capacité, un condensat d'arguments ou un périmètre modifié constitue une collision, qui doit être rejetée avant qu'un autre effet puisse se produire.

Pour les actions à fort impact, les relecteurs ont besoin des preuves sources et de l'effet exact proposé avant d'approuver. Relire seulement un résumé produit par le modèle ne constitue pas une supervision significative.

## Le bac à sable réduit une classe de risques {#sandboxing-reduces-one-class-of-risk}

Un espace de travail isolé peut limiter l'impact sur le système de fichiers ou sur les processus, mais il ne contraint pas automatiquement les sorties réseau, les identifiants, la visibilité des données, les capacités des outils ou les permissions d'un service aval.

Définissez séparément :

- le périmètre du système de fichiers et les chemins inscriptibles ;
- la politique des processus, des paquets et des interpréteurs ;
- les destinations réseau et le budget de requêtes ;
- les secrets et l'identité montés ;
- la classification des données autorisée dans l'environnement ;
- le chemin d'export et la rétention des artefacts ;
- les preuves d'annulation et de nettoyage.

L'architecture hôte-client-serveur de MCP place les permissions de connexion, le consentement de l'utilisateur et l'autorisation auprès de l'hôte. Considérez-la comme une frontière de protocole qui nécessite toujours une politique de sécurité propre à l'application. [Architecture MCP](https://modelcontextprotocol.io/specification/latest/architecture)

## Valider la sortie à trois niveaux {#validate-output-at-three-levels}

| Niveau | Question | Exemple de preuve |
|---|---|---|
| Structurel | la réponse respecte-t-elle le schéma déclaré ? | résultat de l'analyseur et du validateur de schéma |
| Métier | l'action demandée est-elle valide pour ce compte et cet état ? | validation par la politique et la base de données |
| Sécurité et provenance | est-elle autorisée, étayée par une source et classifiée correctement ? | reçu de citation, d'approbation et de politique |

Un objet JSON valide ou une commande syntaxiquement correcte ne constitue pas une action métier sûre.

## Tester le système réel {#test-the-actual-system}

Une suite d'évaluation de sécurité doit inclure :

- des instructions hostiles dans les saisies utilisateur, les fichiers récupérés, les résultats d'outils et les tickets ;
- des attributs d'autorisation absents ou contradictoires ;
- des tentatives de récupération inter-locataires et de sources périmées ;
- des arguments d'outils mal formés ou valides mais dangereux ;
- les chemins de nouvelle tentative, d'annulation et de réponse perdue pour les effets réels ;
- des tests de journalisation et de caviardage, ainsi que le rejeu d'incidents à partir de références contrôlées ;
- une revue humaine indépendante pour les workflows à fort enjeu.

Consignez les classifications des entrées de test et les preuves caviardées afin que l'affirmation de sécurité puisse être revérifiée après un changement de modèle, de prompt, d'outil ou de politique.

## Pièges à éviter {#gotchas}

- **Le retrait par expressions régulières n'est pas une défense contre l'injection de prompt.** Il ne détecte que les formulations que quelqu'un a anticipées. **Correctif :** préserver les frontières de confiance et autoriser les outils en dehors du modèle.
- **Un prompt de sécurité n'est pas un système de permissions.** Le modèle peut toujours proposer une action non autorisée. **Correctif :** lier les capacités à l'identité de l'application, au périmètre et à l'expiration.
- **Un bac à sable doté d'identifiants larges reste à haut risque.** L'isolation ne neutralise pas l'autorité montée à l'intérieur. **Correctif :** appliquer le moindre privilège et bloquer les sorties réseau inutiles.
- **Une revue après action n'est pas un plan de retour arrière.** Un relecteur ne peut pas annuler chaque message, suppression ou publication. **Correctif :** conditionner les effets irréversibles à une barrière avant exécution, et utiliser l'idempotence et la réconciliation.
- **Les journaux peuvent divulguer précisément ce que le bac à sable protégeait.** Des prompts et résultats d'outils complets peuvent devenir un magasin de données parallèle. **Correctif :** n'émettre que des références caviardées, protéger l'accès et appliquer une politique de rétention.
- **Un refus après la récupération est trop tardif.** Les données ont pu déjà franchir une frontière d'autorisation. **Correctif :** appliquer la politique avant que le contexte récupéré n'atteigne le modèle.

## Sources {#sources}

- [Bonnes pratiques de sécurité d'OpenAI](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [Guide d'appel de fonctions d'OpenAI](https://developers.openai.com/api/docs/guides/function-calling)
- [Architecture du Model Context Protocol](https://modelcontextprotocol.io/specification/latest/architecture)
- [RFC 8705 : OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 8725 : JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)

## Voir aussi {#see-also}

- [[agent-security]]
- [[agent-orchestration]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[llmops]]
