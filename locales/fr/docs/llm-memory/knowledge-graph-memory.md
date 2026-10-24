---
title: "Graphe de connaissances comme mémoire pour agents IA"
description: "Schémas de graphe de connaissances persistant pour agents IA : résolution d'entités, étapes du pipeline, notes d'agent et tâches exécutables intégrées dans des coffres Markdown."
level: 3
source_sha256: c10a8d6dc31652682e61639131f51131ab715ec899b96f22e135a4b4bd74b524
translation: machine
translated_at: '2026-10-24'
---
# Mémoire à graphe de connaissances pour agents IA {#knowledge-graph-memory-for-ai-agents}

Des graphes de connaissances structurés comme mémoire persistante pour les agents, au-delà des simples fichiers de notes. L'agent extrait en continu des entités à partir des données entrantes (emails, réunions, transcriptions), les résout vers des enregistrements canoniques et maintient un coffre Obsidian compatible, à liens bidirectionnels.

Implémentation de référence : [Rowboat](https://github.com/rowboatlabs/rowboat) (YC S24, Apache 2.0).

## Architecture : stockage en deux couches {#architecture-two-layer-storage}

```text
raw/           - Append-only sources (email, transcripts, voice memos)
               - Never modified by agent, only read
knowledge/
  People/      - Person entities with roles, orgs, emails
  Organizations/
  Projects/    - Status, stakeholders, timeline
  Topics/      - Keywords, related notes
  Meetings/    - Attendees, decisions, action items
  Agent Notes/ - User model (identity, preferences, style)
  Today.md     - Auto-generated daily brief (inline task)
```

**Invariant central :** les données brutes sont la source de vérité immuable ; `knowledge/` est le modèle du monde traité et interconnecté de l'agent.

## Pipeline en trois étapes {#three-stage-pipeline}

### Étape 1 : filtrage des signaux (pour les emails et flux) {#stage-1-signal-filtering-for-emailfeeds}

Avant de construire le graphe, il faut filtrer le bruit. Le LLM applique un frontmatter YAML à chaque élément source :

```yaml
---
labels:
  relationship: [investor, customer, team]
  topics: [fundraising, hiring, legal]
  type: "intro" | "followup" | ""
  filter: [cold-outreach, newsletter, spam]
  action: "action-required" | "urgent" | "waiting" | ""
processed: true
labeled_at: "2026-04-11T10:00:00Z"
---
```

**Principe « bruit d'abord » :** identifier ce qu'il faut IGNORER avant de décider ce qu'il faut garder. Si le tableau `filter` n'est pas vide, l'élément est exclu de la construction du graphe, quelles que soient les autres balises.

```text
"Founder Signal Test": would a busy domain expert want this in their knowledge system?
```

Les niveaux de sévérité contrôlent l'agressivité avec laquelle les notes sont créées :
- `high` - seules les interactions explicites créent des notes ; les emails ne mettent à jour que les contacts existants
- `medium` - les emails professionnels personnalisés créent des notes ; filtre les services grand public
- `low` - la plupart des expéditeurs humains, filtrage minimal

### Étape 2 : construction du graphe {#stage-2-graph-building}

Traite les sources filtrées pour en faire des notes d'entités. Avant chaque lot :

1. **Reconstruire l'index de connaissances** - parcourir tous les fichiers .md de `knowledge/` et extraire les entités
2. **Injecter l'index dans le prompt** - l'agent reçoit un tableau structuré des entités connues
3. **Traiter le lot** - l'agent écrit ou met à jour les notes et résout les noms vers leurs formes canoniques

La détection des changements repose sur une approche hybride :

```text
mtime check (fast) → if changed, SHA-256 hash → if hash differs → process
```

Cela élimine les faux positifs dus aux seuls changements d'horodatage.

### Étape 3 : étiquetage {#stage-3-tagging}

Applique des étiquettes catégorielles aux notes de connaissances générées. Catégories d'étiquettes : relationship (12), topic (11), email-type (2), noise (13), action (3), status (5), source (6).

## Résolution d'entités {#entity-resolution}

**Schéma critique :** avant de traiter chaque lot, reconstruire un index en mémoire de toutes les entités connues :

```typescript
interface KnowledgeIndex {
  people: { file, name, email?, aliases[], organization?, role? }[]
  organizations: { file, name, domain?, aliases[] }[]
  projects: { file, name, status?, aliases[] }[]
  topics: { file, name, keywords[], aliases[] }[]
}
```

L'agent reçoit cet index sous forme de tableau markdown formaté. Lorsqu'il rencontre « John Smith » dans les données source, il le résout vers le `[[People/John Smith]]` existant plutôt que de créer un doublon.

**Sans cela :** les agents créent `John Smith.md`, `J. Smith.md` et `Smith, John.md` pour la même personne.

## Modèles de notes {#note-templates}

### Note de personne {#people-note}

```markdown
# Person Name

## Info
- **Role:** 
- **Organization:** [[Organizations/OrgName]]
- **Email:** 

## Summary

## Connected to

## Activity

## Key facts

## Open items
```

### Conventions de liens wiki {#wiki-link-conventions}

- Syntaxe : `[[Folder/Canonical Name]]` (chemin absolu dans `knowledge/`)
- Toujours bidirectionnels : si Person pointe vers Org, Org doit pointer en retour vers Person
- L'agent résout les variantes de noms vers les noms canoniques via l'index de connaissances avant d'écrire les liens

## Notes d'agent : modèle structuré de l'utilisateur {#agent-notes-structured-user-model}

Répertoire séparé `knowledge/Agent Notes/` pour la compréhension qu'a l'IA de l'utilisateur :

```text
Agent Notes/
  user.md          - identity facts only (roles, companies, location)
  preferences.md   - explicit rules ("no meetings before 11am")
  style/
    email.md       - writing patterns by recipient type
```

**Sources de données :** messages envoyés par l'utilisateur, éléments de la boîte de réception (notes manuelles), journaux de conversation.

**Traitement :** déduplication agressive, horodatage des faits pour détecter l'obsolescence.

Ceci est distinct du graphe de connaissances principal : c'est le modèle que l'agent a de POUR QUI il travaille, et non de CE Qu'il sait du monde.

## Tâches intégrées (notes vivantes) {#inline-tasks-live-notes}

Blocs JSON exécutables intégrés dans le Markdown. Les notes dont le frontmatter contient `live_note: true` sont interrogées selon un calendrier :

```markdown
---
live_note: true
---

# Today

```task
{
  "instruction": "Create a daily brief for me",
  "schedule": { "type": "cron", "expression": "*/15 * * * *" },
  "lastRunAt": "2026-04-11T10:30:00Z",
  "targetId": "dailybrief"
}
```php

<!--task-target:dailybrief-->
Results written here automatically
<!--/task-target-->
```

Types de planification : `cron`, `window` (exécution soumise à des contraintes horaires), `one-shot`.

**Effet :** les fichiers de connaissances statiques deviennent des agents actifs. Le graphe n'est pas seulement un entrepôt, il s'exécute.

## Historique des versions {#version-history}

Suivre le coffre de connaissances avec Git via isomorphic-git :
- Seuls les fichiers `.md` sont suivis
- Commit après chaque lot de traitement
- Restauration complète depuis n'importe quel commit
- Piste d'audit de l'évolution des connaissances

```typescript
// After each batch completes
await git.commit({
  dir: knowledgeDir,
  message: `Processed batch: ${files.join(', ')}`,
  author: { name: 'agent', email: 'agent@local' }
});
```

## Schémas de passage à l'échelle {#scaling-patterns}

| Échelle | Stratégie de recherche |
|---------|------------------------|
| <200 notes | Navigation par fichier d'index uniquement |
| 200-1000 | Index spécifiques au domaine + recherche grep |
| 1000-5000 | BM25 avec reclassement par LLM |
| 5000+ | [[rag-pipeline]] complet + [[vector-databases]] |

Pour une échelle modérée (le cas le plus courant), un index structuré combiné à des outils Unix (grep, find) surpasse la recherche vectorielle en latence et en coût.

## Appliquer ces schémas sans la pile complète {#applying-these-patterns-without-the-full-stack}

### Résolution d'entités pour une mémoire basée sur des fichiers {#entity-resolution-for-file-based-memory}

Avant de créer de nouvelles entrées de mémoire, parcourir les fichiers existants à la recherche de la même entité :

```python
def resolve_entity(name: str, memory_dir: Path) -> Optional[Path]:
    """Find existing file for entity before creating duplicate."""
    for f in memory_dir.rglob("*.md"):
        content = f.read_text()
        if name.lower() in content.lower():
            # Check aliases in frontmatter or body
            return f
    return None
```

### Filtrage « bruit d'abord » pour toute ingestion {#noise-first-filtering-for-any-ingestion}

Définir des règles d'exclusion explicites avant les règles d'extraction :

```python
SKIP_PATTERNS = ["newsletter", "no-reply", "unsubscribe", "automated"]

def should_skip(source: dict) -> bool:
    """Noise-first: skip known noise categories first."""
    return any(p in str(source).lower() for p in SKIP_PATTERNS)
```

### Séparation brut / traité en deux couches {#two-layer-rawprocessed-separation}

```sql
sessions/raw/     - immutable session transcripts, never modified
memory/           - extracted, consolidated knowledge
                  - derived from raw but not tied to it
```

Permet de retraiter les données brutes avec une logique d'extraction améliorée, sans perte de données.

## Pièges à éviter {#gotchas}

- **La résolution d'entités doit s'exécuter AVANT chaque lot, et non une seule fois au démarrage.** Le graphe de connaissances grandit pendant le traitement ; un lot à l'étape 5 peut avoir besoin d'entités créées à l'étape 2. Reconstruire l'index avant chaque lot, et pas seulement à l'initialisation
- **Les étiquettes d'exclusion doivent être des filtres stricts.** Si le filtrage du bruit est consultatif (pondéré), le spam finit par s'infiltrer dans le graphe. Faire en sorte que les étiquettes skip/filter priment sur tous les signaux de création : un email de prospection à froid ne crée jamais de note de personne, quelles que soient les étiquettes de relation
- **Les liens wiki sans application de la bidirectionnalité divergent.** Les liens unidirectionnels créent des nœuds orphelins que l'agent ne peut pas atteindre. Appliquer la bidirectionnalité au moment de l'écriture : lorsque l'agent écrit `[[People/Alice]]` dans une note d'organisation, vérifier que la note d'Alice renvoie vers cette organisation
- **Les tâches intégrées dans les notes vivantes nécessitent une interrogation (polling) plutôt que des surveillants de fichiers.** Les événements du système de fichiers ne transportent pas le contexte de planification. Une boucle d'interrogation (toutes les 15 s) lisant le frontmatter `live_note: true` est plus fiable sur les différents systèmes d'exploitation qu'inotify ou FSEvents

## Schéma LLM Wiki (Karpathy) {#llm-wiki-pattern-karpathy}

Alternative plus simple aux systèmes de graphe de connaissances complets : **collections markdown structurées avec références croisées**. Pas de RAG, pas de base vectorielle, seulement des fichiers texte navigués par le LLM.

### Architecture en trois couches {#three-layer-architecture}

```bash
raw/          - immutable source materials (PDFs, clipped articles, notes)
              - LLM reads but NEVER modifies
wiki/         - LLM-generated structured markdown
              - encyclopedia articles for concepts and entities
              - summaries, comparisons, cross-references via backlinks
              - index.md: catalog updated on every ingest
              - log.md: append-only chronological operation log
schema/       - CLAUDE.md: structure conventions, workflows
```

### Trois opérations {#three-operations}

```bash
Ingest:  user drops source file
         LLM reads → discusses takeaways → writes summary pages
         updates index.md → revises entity/concept pages → appends to log
         one source → ~10-15 wiki pages touched

Query:   user asks question
         LLM navigates via index → synthesizes answer with citations
         valuable answers → new wiki pages

Lint:    periodic health-check passes
         find: contradictions, stale claims, orphan pages, missing cross-refs
```

### Pourquoi le markdown brut l'emporte sur le RAG (à échelle modérée) {#why-plain-markdown-beats-rag-at-moderate-scale}

À environ 100 articles / 400 K mots, le LLM navigue via les résumés et l'index, sans recherche vectorielle. Le wiki est un « artefact persistant et cumulatif » : les connaissances sont compilées une fois et maintenues, au lieu d'être redérivées à chaque requête comme dans le RAG. Le LLM gère l'intendance : il n'oublie pas de mettre à jour les références croisées et peut modifier 15 fichiers en une seule passe.

À plus grande échelle : ajouter une recherche BM25 ou vectorielle optionnelle avec reclassement par LLM.

### Comparaison {#comparison}

| Approche | Échelle | Vitesse de requête | Mise en place | Idéal pour |
|----------|---------|--------------------|---------------|------------|
| LLM Wiki (markdown brut) | <500 articles | Navigation LLM complète | Minimale | Base de connaissances personnelle |
| Graphe de connaissances (Rowboat) | 500-5000 entités | Recherche dans l'index + LLM | Moyenne | Contexte professionnel issu des emails et réunions |
| RAG + base vectorielle | 5000+ articles | Récupération en moins de 100 ms | Importante | Questions-réponses sur un large corpus |

### Pipeline session vers wiki {#session-to-wiki-pipeline}

Relier le travail de session au wiki persistant :

```python
# After each session, extract learnings
session_summary = extract_session_insights(conversation_log)

# Ingest into wiki
wiki.ingest(session_summary)
# → LLM reads, updates relevant concept pages, appends to log

# At session start, query wiki for context
context = wiki.query("current project architecture decisions")
```

## Voir aussi {#see-also}

- [[knowledge-base-as-memory]]
- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[session-persistence]]
- [[temporal-memory]]
- [[rag-pipeline]]
