---
level: 3
source_sha256: 65091d694c862a03524c0eee6423a6c58f9eeaa2171460b9cf7e6d1a01aa424a
translation: machine
translated_at: '2026-10-24'
---
# Application des priorités de mémoire {#memory-priority-enforcement}

Modèle de structuration de la mémoire d'un agent en deux niveaux : un niveau chargé systématiquement (critique) et un niveau chargé à la demande (référence), avec une application mécanique pour les règles les plus critiques. Convergence de 8 domaines indépendants vers le même principe.

## Principe fondamental {#core-principle}

Si l'oubli d'une règle a des conséquences irréversibles → chargement systématique.  
Tout le reste → à la demande.

Il ne s'agit pas d'une optimisation de performance, mais d'une propriété de sûreté : le contexte critique doit survivre à la compaction du contexte, aux sessions longues et à la dégradation de l'attention.

## Critères : chargement systématique ou à la demande {#always-vs-on-demand-criteria}

**Chargement systématique** (répondre à au moins un critère) :
1. **Conséquences irréversibles** : l'oubli entraîne une perte de données, un préjudice financier, une interruption de production ou une faille de sécurité
2. **Invariants inter-sessions** : règles qui doivent être respectées quelle que soit la tâche (« ne jamais supprimer sans confirmation », « ne jamais utiliser un GPU de production sans vérifier l'allocation »)
3. **Profil et préférences de l'utilisateur** : style de communication, niveau d'expertise, préférences d'outils

**À la demande** (charger quand le sujet devient pertinent) :
- Détails des projets actifs (chargés lorsqu'on travaille sur le projet concerné)
- Documents de référence et méthodologies
- Informations historiques et incidents passés
- Intégrations d'outils spécifiques, peu utilisées au quotidien

## Règle Boeing : garder le chargement systématique court {#boeing-rule-keep-always-load-short}

Les « memory items » de l'aéronautique (procédures d'urgence exécutées de mémoire, sans liste de contrôle) :
- Typiquement : 3 à 4 éléments par procédure d'urgence
- Maximum : environ 10 éléments (considéré comme élevé)
- Au-delà de 10 : saturation de la liste de contrôle → les éléments critiques sont oubliés sous stress

**Pour la mémoire d'un agent :** la section à chargement systématique doit compter 10 à 15 entrées au maximum. Au-delà, les éléments importants tombent dans la zone du « lost in the middle ».

**Lost in the Middle (Liu et al. 2023, arxiv 2307.03172) :** les performances des LLM suivent une courbe en U selon la position dans le contexte. Les éléments situés au début ou à la fin reçoivent le plus d'attention ; ceux du milieu se dégradent nettement. Avec 36 entrées à chargement systématique, les règles critiques occupent les rangs 5 à 35 dans un long contexte, soit précisément la zone dégradée.

## Principe des deux couches de l'AIEA {#iaea-two-layer-principle}

Issu de la défense en profondeur définie dans l'INSAG-10 de l'AIEA : les barrières de sûreté critiques doivent être indépendantes et redondantes. S'appuyer sur une seule couche (une règle) pour imposer un comportement critique échoue en cas de défaillance de cause commune (pression du contexte, compaction, distraction).

**Application :**
- Règle dans CLAUDE.md ou la mémoire (décrit le POURQUOI et le COMMENT)
- Application mécanique par hook ou script (s'exécute quel que soit l'état du contexte)

**Exemples de couples efficaces :**
```text
Documentation integrity:
  Rule → "validate file references"
  Hook → SessionStart → validate_config.py (runs every session, blocks on drift)

Handoff reminder:
  Rule → "write handoff before ending long sessions"
  Hook → Stop → remind_handoff.py (blocks session end if no recent handoff)

Supply chain defense:
  Rule → "delay fresh packages"
  Enforcement → .npmrc min-release-age=7 (mechanically applied to every install)
```

**Question à se poser lors de l'ajout d'une nouvelle règle critique :** « Cette règle peut-elle être contournée si l'on oublie de lire la mémoire ? »  
Si oui → elle nécessite un hook, pas seulement une règle.

## Architecture à deux niveaux de MemGPT {#memgpt-two-tier-architecture}

```text
Core memory    ← in-context, fixed-size, agent can read/write via tool calls
               ← User profile, current task state, active invariants

Archival memory ← searchable database, paged in on-demand
                ← Historical context, past projects, reference materials
```

**Propriété clé :** l'agent décide explicitement ce qu'il fait remonter de l'archive vers le cœur de la mémoire. Le cœur reste ainsi petit et ciblé, tout en conservant l'historique complet.

**Pour les systèmes à base de fichiers :**  
La section `MEMORY.md Always Load` correspond à la mémoire centrale  
La section `MEMORY.md On Demand` correspond à l'index d'archive  
Les fichiers effectivement chargés à la demande correspondent au stockage d'archive

## Tableau de convergence des domaines {#domain-convergence-table}

| Domaine | Critique / systématique | Référence / à la demande | Mécanisme d'application |
|--------|------------------|-----------------------|----------------------|
| Contexte des LLM (Liu 2023) | Début / fin du contexte | Milieu (attention dégradée) | Position dans le prompt |
| MemGPT | Mémoire centrale (fixe) | Archive (paginée) | Appels d'outils pour le chargement |
| Aéronautique | Memory items (3 à 10) | Listes de contrôle (documentées) | Formation et répétition |
| Neurosciences | Mémoire procédurale (striatum) | Épisodique (hippocampe) | Architecture neuronale |
| Psychologie cognitive | Mémoire de travail (4±1 chunks) | Mémoire à long terme (illimitée) | Attention / répétition |
| Sûreté nucléaire (INSAG-10) | Barrières de défense à 5 niveaux | Procédures / manuels | Redondance physique |
| Syslog Linux | EMERG/ALERT → console | DEBUG → tampon circulaire | `console_loglevel` |
| Kubernetes | Politiques des admission webhooks | Journaux du serveur d'API | Interception par webhook |

Les 8 domaines convergent vers un même principe : **un petit ensemble critique + un vaste ensemble de référence + une application mécanique de l'ensemble critique.**

## Gestion de l'obsolescence de la mémoire {#memory-staleness-management}

Les entrées de mémoire doivent comporter un champ `created: YYYY-MM-DD`. Obsolescence selon le type :

| Type | Obsolète après | Vérification à l'usage |
|------|-------------|--------------|
| `project` | 30 jours | Vérifier avant usage si plus ancien |
| `reference` (IP, chemins, ports) | 7 jours | Toujours vérifier si lié à l'infrastructure |
| `feedback` | Stable (les préférences utilisateur changent rarement) | Priorité faible |
| `user` | Très stable | Vérifier uniquement en cas de changement de contexte majeur |

## Schéma d'extraction automatique de la mémoire {#automatic-memory-extraction-pattern}

À la fin des sessions, extraire vers la mémoire :
1. **Capacités** : nouveaux workflows, outils et intégrations découverts
2. **Corrections** : approches corrigées par l'utilisateur (→ mémoire de type feedback)
3. **Permissions** : nouvelles commandes autorisées (→ paramètres)
4. **Couples bug/correctif** : symptôme → cause racine → solution (→ pièges)
5. **Décisions** : choix d'architecture avec leur justification (→ DECISIONS.md ou mémoire)

Étiquettes de tri : `[DECISION]`, `[GOTCHA]`, `[REUSE]`, `[DEFER]`

## Pièges courants {#gotchas}

- **Problème :** la section à chargement systématique grossit sans limite, car de nouvelles règles sont ajoutées sans que les anciennes soient retirées. -> **Correctif :** appliquer la règle Boeing lors de la revue : si la section dépasse 15 entrées, effectuer un tri selon le critère des conséquences irréversibles. La plupart des éléments « utiles à retenir » relèvent du chargement à la demande.
- **Problème :** une règle en mémoire empêche une action en début de session, mais est oubliée après une compaction du contexte en cours de session. -> **Correctif :** pour toute règle qui doit tenir pendant toute la session (par exemple « ne pas modifier la production »), créer un hook qui la vérifie à chaque appel d'outil pertinent, et pas seulement en début de session.
- **Problème :** la mémoire à la demande devient un vidage non structuré, ce qui rend la recherche peu fiable. -> **Correctif :** utiliser les liens wiki `[[filename]]` pour créer un graphe navigable. La mémoire sur le projet X doit renvoyer vers l'infrastructure sur laquelle il tourne, les outils qu'il utilise et la méthodologie appliquée.
- **Problème :** des entrées de mémoire créées il y a des années font référence à des chemins de fichiers, des adresses IP ou des ports qui n'existent plus. -> **Correctif :** un hook SessionStart (par exemple `validate_config.py`) parcourt la mémoire à la recherche de chemins absolus et vérifie leur existence. Il signale les dérives avant que la session n'agisse sur des données obsolètes.

## Voir aussi {#see-also}

- [[context-window-management]]
- [[memory-architectures]]
- [[session-persistence]]
- [[knowledge-graph-memory]]
