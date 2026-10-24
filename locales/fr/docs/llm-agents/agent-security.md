---
title: "Sécurité et sûreté des agents"
description: "Modélisation des menaces et contrôles pour les agents LLM : prompts, outils, mémoire, identités, chaîne d'approvisionnement et observabilité"
level: 3
source_sha256: 5ae1808b1dbc505fb594077149225f007b4b2e7da2e0391aecbebdcae8203626
translation: machine
translated_at: '2026-10-24'
---
# Sécurité et sûreté des agents (septembre 2026) {#agent-security-and-safety-september-2026}

Contexte de version : utiliser les recommandations OWASP actuelles pour les applications agentiques, la documentation de sécurité actuelle des fournisseurs et les révisions de protocole réellement déployées. Les modèles de menaces doivent être réexaminés à chaque changement d'outils, de sources de données, d'identités ou de comportement de la mémoire.

Le risque lié aux agents résulte de la combinaison de contenus non fiables, de décisions du modèle et d'effets de bord. Un modèle peut être utile tout en étant amené à détourner une capacité pourtant autorisée. La sécurité se situe donc dans la frontière du système, et non dans la seule formulation des prompts.

## Modèle de menaces {#threat-model}

Recensez chaque frontière de confiance :

| Surface | Menace typique | Contrôle requis |
|---|---|---|
| Entrée utilisateur | Injection de prompt directe, requête dangereuse | Politique d'entrée, validation du périmètre, limitation de débit |
| Contenu web/document récupéré | Instructions indirectes, faits empoisonnés | Traiter comme des données, provenance, isolation des actions |
| Métadonnées d'outils / skills | Description trompeuse, compromission de la chaîne d'approvisionnement | Identité, revue, révision épinglée, liste d'autorisation |
| Mémoire à long terme | Empoisonnement du contexte ou de la mémoire | Autorisation d'écriture, provenance, expiration, revue |
| Exécution d'outils | Périmètre excessif, abus de paramètres, exfiltration | Autorisation côté serveur, schémas, moindre privilège |
| Échanges agent-à-agent | Contexte surdimensionné, autorité confuse | Transfert typé, identité, politique par action |
| Télémétrie | Divulgation d'entrées/sorties sensibles | Caviardage, rétention, contrôles d'accès |

Le Top 10 OWASP 2026 pour les applications agentiques est une taxonomie utile, mais il ne remplace pas une analyse de cas d'abus propre au système.

## Frontière non négociable {#non-negotiable-boundary}

```text
untrusted content -> model proposal -> schema validation -> policy authorization
                  -> scoped tool execution -> immutable receipt -> response
```

Un contenu non fiable peut influencer la réponse d'un modèle, mais il ne doit jamais modifier directement ses permissions, sa liste d'outils autorisés, son identité ou son état d'approbation.

## Autorisation des outils {#tool-authorization}

Chaque appel d'outil nécessite une classe d'effets de bord déclarée et un périmètre appliqué côté serveur.

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolRequest:
    actor_id: str
    tenant_id: str
    action: str
    resource_id: str
    arguments: dict[str, Any]


def authorize_export(request: ToolRequest) -> None:
    if request.action != "export_report":
        raise PermissionError("action is not available")
    if not request.resource_id.startswith(f"{request.tenant_id}:"):
        raise PermissionError("resource is outside tenant scope")
    if "destination" not in request.arguments:
        raise ValueError("destination is required")
```

Après autorisation, valider l'entrée typée complète et lier l'identifiant de service au moindre privilège nécessaire à cette action. Ne donnez pas au modèle un jeton largement privilégié en lui demandant d'être prudent.

## Injection de prompt et contenu récupéré {#prompt-injection-and-retrieved-content}

L'injection de prompt est un problème d'intégrité des entrées. Les prompts défensifs et les classifieurs peuvent réduire le risque, mais ne peuvent pas rendre fiable un texte non fiable.

Contrôles :

1. Étiqueter comme non fiables les données provenant des utilisateurs, des pages web, des e-mails, des fichiers et des réponses d'outils.
2. Garder le texte non fiable hors des instructions et des définitions de politique.
3. Exiger un contexte explicite d'utilisateur ou d'autorisation avant tout effet de bord externe.
4. Restreindre les outils disponibles à chaque étape ; ne jamais exposer un univers global d'outils.
5. Vérifier la provenance des sources et les citations avant de s'appuyer sur des affirmations récupérées.
6. Tester les scénarios d'injection indirecte à plusieurs étapes dans un environnement contrôlé.

Ne jamais copier des instructions issues d'un document récupéré dans un prompt système, un enregistrement de mémoire ou un skill sans revue.

## Intégrité de la mémoire et du contexte {#memory-and-context-integrity}

La mémoire à long terme est une surface d'attaque inscriptible. Chaque enregistrement nécessite une identité d'auteur, une référence de source, un horodatage, un schéma, un périmètre de locataire, un niveau de confiance/provenance, une règle de rétention et, éventuellement, un statut d'approbation.

Utilisez une porte de promotion explicite :

```json
{
  "memory_id": "mem_01J...",
  "writer": "service:knowledge-curator",
  "source_ref": "artifact://approved/...",
  "tenant_id": "tenant_42",
  "classification": "internal",
  "expires_at": "2026-12-31T00:00:00Z",
  "promotion_state": "approved"
}
```

Une suggestion générée par le modèle n'est pas automatiquement éligible à la mémoire durable. Elle doit respecter les mêmes règles de source et d'autorisation que tout autre contenu.

## Identité, secrets et chaîne d'approvisionnement {#identity-secrets-and-supply-chain}

- Accordez à chaque identité d'agent ou de service uniquement les permissions dont elle a besoin.
- Conservez les identifiants dans un gestionnaire de secrets ou une identité de charge de travail déléguée, jamais dans les prompts, les descriptions d'outils, les journaux ou la mémoire.
- Épinglez les dépendances ainsi que les révisions des outils et des skills ; examinez la provenance avant installation.
- Séparez les identifiants en lecture seule destinés à la recherche des identifiants en écriture destinés aux opérations.
- Désactivez ou soumettez à approbation la messagerie externe, les paiements, les écritures destructives et les changements de privilèges.
- Renouvelez ou révoquez l'identité d'un agent lorsqu'un outil, un skill ou une source de mémoire est soupçonné d'avoir été compromis.

Les worktrees Git isolent les extractions de branches, mais ne constituent pas un bac à sable pour le réseau, les identifiants, les processus ou le stockage monté. Ajoutez des contrôles au niveau du système d'exploitation, du conteneur ou du cloud lorsque ces frontières sont nécessaires.

## Observabilité, réponse et red teaming {#observability-response-and-red-teaming}

Journalisez les événements modèle/outil caviardés avec l'identifiant de tâche, la révision de politique, le périmètre de l'acteur/locataire, la décision de l'outil, le reçu et l'état final. Alertez sur les tentatives à haut risque refusées, les volumes de données inattendus, les nouvelles tentatives répétées, les tentatives d'accès inter-locataires et les destinations inattendues.

Un plan de réponse à incident doit prévoir un interrupteur d'arrêt pour l'exécution des outils, la révocation d'identité, la préservation des traces, la mise en quarantaine des mémoires touchées, le retour arrière des dépendances et une revalidation documentée avant de réactiver l'autonomie.

Faites du red teaming sur le flux réel : injection directe et indirecte, mémoire empoisonnée, sortie d'outil malformée, requêtes dupliquées, métadonnées de dépendance compromises, transferts au périmètre excessif et tentatives de contournement des refus.

## Pièges courants {#gotchas}

- **Les prompts système ne constituent pas une couche d'autorisation.** Ils peuvent être ignorés ou manipulés. **Correctif :** appliquer l'autorisation et les contrôles d'effets de bord dans le code avant l'exécution d'un outil.
- **Les documents récupérés ne sont pas des instructions.** Ils peuvent contenir du texte hostile ou des métadonnées trompeuses. **Correctif :** les isoler comme données non fiables et exiger des vérifications de source et de provenance.
- **La mémoire rend la compromission persistante.** Un enregistrement empoisonné peut affecter les exécutions ultérieures. **Correctif :** utiliser des permissions d'écriture, une provenance immuable, une expiration et un circuit de quarantaine/revue.
- **Les garde-fous peuvent fuiter des données via la télémétrie.** Les traces peuvent capturer les prompts bruts et les entrées d'outils. **Correctif :** tester le caviardage, la rétention et les contrôles d'accès avec des contenus sensibles représentatifs.
- **Les worktrees ne sont pas un bac à sable de sécurité.** Ils partagent les ressources et identifiants de l'hôte sauf s'ils sont contraints séparément. **Correctif :** isoler identifiants, réseau, processus et stockage au niveau de l'environnement.

## Sources {#sources}

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI Agents SDK: guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)

## Voir aussi {#see-also}

- [[agent-fundamentals]]
- [[agent-memory]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[production-patterns]]
