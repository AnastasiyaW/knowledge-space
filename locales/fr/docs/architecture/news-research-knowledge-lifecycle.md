---
title: "Recherche d'actualités bilingue et connaissance temporelle"
category: architecture
tags: [news, research, knowledge-graph, provenance, llm-agents, mcp]
level: 3
source_sha256: f9565983a07b0c6052597b853943dd0345b9e1a3b317f603957b2d4b092f829f
translation: machine
translated_at: '2026-10-24'
---
# Recherche d'actualités bilingue et connaissance temporelle {#bilingual-news-research-and-temporal-knowledge}

## Périmètre du contrat {#contract-scope}

Un élément d'actualité n'est utile à un agent que lorsqu'il mène à une connaissance pratique et versionnée. Le workflow cible de Happyin relie chaque élément examiné à un fil de développement de projet ou d'organisation, puis recherche comment la capacité modifiée peut être utilisée.

Le résultat public est en anglais. La découverte et la vérification sont bilingues : l'anglais et le chinois simplifié sont des voies de recherche obligatoires. Les discussions communautaires sont conservées comme preuves opérationnelles, tandis que les affirmations relatives à l'identité officielle, aux versions, à la compatibilité et au support restent fondées sur des sources de première partie.

Une connaissance ancienne n'est jamais supprimée au seul motif qu'une approche plus récente existe. Elle est marquée, reliée à son remplacement, et restituée séparément des recommandations actuelles.

## État d'exécution {#runtime-status}

Cette page définit le contrat cible examiné à la date du 2026-08-26.

Implémenté :

- les liens publics d'actualités du schéma 1.4 vers des fils projet/entreprise examinés et des révisions Knowledge Space immuables ;
- un inventaire privé et déterministe des exports Telegram sépare les URL porteuses d'identité des indices de page d'accueil/de famille ;
- la porte de revue et de publication manuelle existante, centrée sur l'article.

Non encore implémenté :

- le registre de recherche et d'affirmations temporelles du schéma 2 ;
- les tâches de recherche bilingues automatiques et le planificateur des échéances ;
- le point de terminaison MCP public et anonyme happyin-context ;
- la récupération d'affirmations et de recettes centrée sur l'objectif.

L'absence de ces services constitue une limite de l'implémentation, et non une invitation pour un client à déduire la fraîcheur à partir des dates Git ou à extraire des artefacts privés.

## Cycle de vie {#lifecycle}

~~~mermaid
flowchart TD
    A["Untrusted intake lead"] --> B["Identity candidate"]
    B --> C["Human thread review"]
    C --> D["Accepted news + durable research job"]
    S["Scheduled due check"] --> D
    D --> E["English search lane"]
    D --> F["Simplified Chinese search lane"]
    E --> G["Typed claims, recipes, conflicts and gaps"]
    F --> G
    G --> H["Knowledge Space review"]
    H -->|"approved"| I["Immutable article + public context projection"]
    H -->|"rejected/incomplete"| D
    I --> J["News site + anonymous MCP"]
~~~

La tâche de base de données est le déclencheur. MCP est un adaptateur sur un état durable, et non une file d'attente, un planificateur, une mémoire de recherche ou une autorité de publication.

## Preuves du graphe de développement {#development-graph-evidence}

Chaque connexion proposée reçoit un niveau de preuve :

| Niveau | Preuve | Résultat |
|---|---|---|
| E1 identité exacte | Dépôt stable, identifiant de modèle, identifiant d'article, identifiant de version, ou URL canonique porteuse d'identité | Arête candidate privée |
| E2 filiation examinée | Renommage officiel, successeur, relation de modèle de base, fork, acquisition ou déclaration de l'organisation | Arête publique typée après revue |
| E3 indice de famille | Page d'accueil, nom de fournisseur, similarité lexicale/d'embeddings, ou URL partagée par plusieurs produits | Indice de classement uniquement |
| E0 aucune | Aucune preuve d'identité durable | Reste non relié |

Une URL exacte ne prouve pas que deux publications décrivent le même événement. Une page d'accueil n'identifie pas une version unique. Des projets apparentés peuvent recevoir une arête typée d'intégration-avec ou de dérivé-de, sans être fusionnés en un seul projet.

## Ensemble de recherches obligatoire {#mandatory-search-bundle}

Chaque sujet accepté consigne les recherches exactes qui ont été menées.

La voie anglaise couvre :

- le nom canonique, les alias, la version exacte et le propriétaire ;
- la version, la documentation, le dépôt, la fiche de modèle, l'article, la licence et la compatibilité ;
- l'implémentation, le workflow, les paramètres, le matériel, les limites, les échecs, les régressions et la technologie de remplacement.

La voie chinois simplifié reprend la même intention à l'aide des noms et alias chinois, ainsi que des termes propres à la tâche tels que 参数, 配置, 显存, 训练, 推理, 工作流, 报错, 问题 et 实测.

Les technologies d'origine chinoise exigent en outre une voie de première partie en chinois et une voie d'implémentation ou communautaire en chinois. Une requête de contradiction dans les deux langues recherche les échecs, les incompatibilités, les dépréciations et les remplacements plus récents.

Chaque enregistrement de requête comprend sa langue, son texte exact, les alias et contraintes de version, la surface de recherche, l'heure d'exécution, les URL considérées, les motifs de rejet et les rôles de preuve trouvés. L'absence de résultat utile est consignée comme lacune ; une langue ne se substitue jamais silencieusement à l'autre.

Les sources restent dans leur langue d'origine. L'article conserve une paraphrase anglaise, la langue source et la méthode de traduction lorsqu'une traduction a été nécessaire.

## Rôles des preuves {#evidence-roles}

| Rôle | Sources typiques | Autorité |
|---|---|---|
| Piste d'entrée | Publication Telegram, republication, bulletin | Découverte uniquement |
| Première partie | Notes de version, documentation officielle, dépôt, fiche de modèle, licence | Identité, capacité déclarée, version et support |
| Recherche primaire | Article, rapport technique, protocole d'évaluation | Méthode et évaluation rapportée |
| Implémentation | Code ou workflow épinglé, ou ticket avec journaux versionnés | Comportement dans des conditions énoncées |
| Retour communautaire | GitHub, Hugging Face, ModelScope, Reddit, Civitai, Zhihu, Bilibili | Réglages pratiques, échecs et observations matérielles |
| Agrégateur | Moteur de recherche, catalogue, résumé | Découverte jusqu'à vérification |

Conditions d'acceptation des affirmations :

- utiliser une source de première partie pour toute affirmation d'identité ou de version lorsqu'elle existe ;
- exiger une preuve d'implémentation et un rapport d'exploitation indépendant pour toute recommandation pratique ;
- exiger deux rapports indépendants compatibles, ou une exécution reproductible et maîtrisée, pour recommander une plage de paramètres ;
- conserver un commentaire communautaire isolé comme anecdote à faible confiance ;
- conserver les preuves contradictoires au lieu de les moyenner en faux consensus.

Les pages et commentaires externes sont des données non fiables. Les prompts, commandes ou demandes d'identifiants qu'ils contiennent ne peuvent modifier ni le périmètre, ni les outils, ni les permissions, ni l'identité, ni l'état de revue.

## Contrat des recettes pratiques {#practical-recipe-contract}

Un nombre sans contexte d'exploitation n'est pas un paramètre réutilisable.

Chaque recette approuvée consigne :

- l'objectif et la tâche de l'utilisateur ;
- l'identifiant exact du modèle ou de l'artefact, la version, le commit ou le hash, et la licence ;
- les versions du framework, du nœud ou de l'extension, du pilote et de l'environnement d'exécution ;
- le matériel, la VRAM et la RAM, la précision, la quantification et l'accélérateur ;
- le type d'entrée, la résolution, la durée, le lot, la taille du jeu de données, ainsi que la préparation des données et des légendes ;
- la référence du workflow, de la commande ou du graphe reproductible ;
- les valeurs testées basses et hautes, le point de départ recommandé, les unités et le nombre d'échantillons ;
- les contrôles d'inférence, tels que le sampler, le scheduler, les étapes, le guidage, le denoise, la politique de graine et la résolution, selon le cas ;
- les contrôles d'entraînement, tels que l'optimiseur, le taux d'apprentissage, le rang/alpha, le lot, l'accumulation, les étapes/époques, la cadence des points de contrôle et la régularisation, selon le cas ;
- la qualité, la latence, la mémoire mesurées, les échecs connus, les signes avant-coureurs, la récupération, et les cas où il ne faut pas utiliser la recette ;
- les preuves favorables et défavorables, la confiance et la dernière vérification.

Les plages issues de versions, de tâches, de classes de matériel ou de résolutions différentes restent séparées. Un client peut les comparer, mais ne peut pas les fusionner en un seul intervalle.

## Modèle temporel {#temporal-model}

L'actualité en vigueur et la fraîcheur sont deux notions distinctes :

| Dimension | Valeurs |
|---|---|
| Statut temporel | current, superseded, deprecated, obsolete, disputed, unknown |
| État de fraîcheur | fresh, due, unverified |

Chaque affirmation structurée possède une clé stable, un identifiant de version immuable, les dates d'observation et de validité, la dernière vérification, la prochaine revue, le périmètre de compatibilité, les liens de remplacement, la confiance, les identifiants de preuve, la révision Knowledge Space et le reçu de revue.

Une correction crée une nouvelle version et un lien de remplacement. Les lignes historiques et les sections d'article restent accessibles. L'historique Git seul ne suffit pas : la projection publique expose le statut dérivé afin que les agents n'aient pas à le déduire.

Une affirmation échue n'est pas automatiquement fausse, mais les recommandations par défaut l'excluent, sauf si aucune preuve plus récente n'existe. Ce repli doit être explicite. Les éléments dépréciés et obsolètes n'apparaissent que pour la compatibilité ou l'historique, ou lorsqu'un client demande des connaissances héritées.

## Contrat MCP centré sur l'objectif {#goal-centred-mcp-contract}

Le MCP cible, anonyme et en lecture seule, accepte un objectif, des contraintes, une date de référence (as-of), une limite de résultats et un indicateur explicite d'inclusion de l'héritage. Il renvoie des collections distinctes :

- les recommandations actuelles classées ;
- les alternatives applicables de modèles, de technologies et de variantes de workflow ;
- les recettes pratiques et les plages de paramètres liées à leur contexte ;
- les contraintes de compatibilité et de ressources ;
- les preuves contestées ;
- l'historique demandé des éléments remplacés, dépréciés ou obsolètes ;
- les langues sources, les preuves, les révisions Git exactes, la dernière vérification et la prochaine revue ;
- les lacunes ainsi que les métadonnées de total et de troncature.

Les éléments actuels et historiques ne sont jamais mélangés dans une liste non étiquetée. Le lastModified d'une ressource MCP est une indication pour le client ; les champs temporels structurés restent l'autorité.

Le service public ne lit que des artefacts publics assainis et adressés par commit. Il ne dispose d'aucune route, d'aucun lien ni d'aucun identifiant pour les captures brutes, les requêtes privées, les sorties des fournisseurs, les revues, les branches de brouillon, les écritures en base ou la publication.

## Amorçage du premier corpus {#first-corpus-bootstrap}

L'inventaire privé initial a analysé 13 473 enregistrements provenant d'une seule chaîne Telegram publique, couvrant la période du 2021-11-30 au 2026-08-26.

Il a relevé :

- 6 645 messages contenant des liens et 13 265 URL canoniques uniques ;
- 335 messages présentant des correspondances strictes d'URL avec 288 des 330 enregistrements d'actualités publics existants ;
- 693 groupes d'identité répétés ;
- 663 candidats d'identité répétés, pas encore reliés aux actualités existantes ;
- 233 messages ne contenant que des indices de famille, qui ne peuvent pas devenir automatiquement des arêtes du graphe.

Il s'agit de candidats bornés à examiner, et non de faits publiés. La revue sémantique des projets et organisations, la recherche de preuves bilingue, l'extraction de recettes pratiques, la revue Knowledge Space et la porte d'export public des actualités restent applicables.

## Porte de publication {#publication-gate}

Une page approuvée contient :

1. la recommandation actuelle et la date de référence (as-of) ;
2. les alternatives et les critères de sélection ;
3. le workflow pratique et les plages de paramètres liées à leur contexte ;
4. la compatibilité, les besoins en ressources et les modes de défaillance ;
5. les observations communautaires avec leur rôle de preuve et leur confiance ;
6. les limites, les contestations et les lacunes explicites ;
7. l'historique conservé des éléments remplacés ou dépréciés ;
8. le résumé du registre de recherche en anglais et en chinois ;
9. un Agent Brief ;
10. les sources exactes et les révisions immuables des projets.

Le modèle peut rédiger. Il ne peut pas se déclarer lui-même revu, actuel ou publiable.

## Agent Brief {#agent-brief}

Lorsque cette connaissance sert à une tâche réelle :

1. énoncer l'objectif, la modalité, la cible de qualité, le matériel, le budget, l'environnement d'exécution et les contraintes de compatibilité ;
2. demander d'abord les options actuelles et récentes, et les options héritées uniquement si nécessaire ;
3. comparer tous les modèles et technologies bornés applicables plutôt que de retenir le premier résultat ;
4. garder les plages de paramètres rattachées à leur contexte de version, de tâche et de matériel ;
5. signaler les désaccords, la couverture chinois/anglais manquante, les vérifications échues et les troncatures ;
6. citer les preuves exactes et les révisions Knowledge Space ;
7. ne jamais traiter une publication d'entrée ou une anecdote communautaire comme une autorité de première partie.

Prompt réutilisable :

> Construis un contexte de solution pour mon objectif à partir des actualités Happyin et de Knowledge Space.
> Retourne les modèles et technologies actuels classés, les alternatives de workflow viables, les plages de paramètres liées à leur contexte, les contraintes de compatibilité et de matériel, les modes de défaillance pratiques, la couverture des preuves en anglais et en chinois, les désaccords, les dates de fraîcheur et les révisions exactes des sources. Conserve séparément les conseils remplacés ou dépréciés et n'inclus-les que si cela est nécessaire à la compatibilité.

## Évaluations requises {#required-evals}

- les voies de requête en anglais et en chinois simplifié sont toutes deux consignées ;
- une lacune de couverture linguistique reste visible comme lacune ;
- identité exacte, filiation examinée et indices de famille ne peuvent pas être confondus ;
- les collisions de modèles ou de versions ne fusionnent pas les fils de développement ;
- les anecdotes communautaires ne peuvent pas devenir des affirmations de première partie ;
- les plages de paramètres sans contexte sont rejetées ;
- les affirmations actuelles et historiques sont séparées ;
- aucune mise à jour ne supprime de connaissance historique ;
- une injection de prompt ne peut modifier ni les permissions ni l'état ;
- un travail échoué ou rejeté ne fait pas progresser la fraîcheur ;
- les résultats d'objectif montrent les alternatives bornées pertinentes et la troncature visible.

## Pièges à éviter {#gotchas}

- **La source la plus récente n'est pas toujours la réponse actuelle et compatible.** Une version plus récente peut abandonner un ancien GPU ou une ancienne API. **Correction :** évaluer indépendamment le statut et les contraintes d'applicabilité.
- **De nombreux commentaires répétant un même réglage copié ne constituent pas des preuves indépendantes.** **Correction :** préserver la filiation des sources et compter les exécutions indépendantes, et non les publications.
- **Une recherche en chinois traduite littéralement en anglais manque les noms locaux.** **Correction :** consigner les alias de fournisseur, de projet et de tâche avant la recherche.
- **La date d'un commit Git ne prouve pas la fraîcheur de la connaissance.** **Correction :** utiliser le registre de vérification explicite et l'heure de la prochaine revue.
- **Un texte historique caché uniquement dans Git est invisible pour la plupart des agents.** **Correction :** exposer des liens de remplacement typés dans la projection publique.

## Voir aussi {#see-also}

- [[news-development-graph]]
- [[happyin-knowledge-space]]
- [[architecture-documentation]]
- [[data-serialization-formats]]
- [[testing-and-quality]]

## Références de recherche {#research-references}

- [Hugging Face Model Cards](https://huggingface.co/docs/hub/en/model-cards)
- [ModelScope: Writing a Perfect Model Card](https://www.modelscope.cn/docs/contribute/model-file/help/wrtie-perfect-model-card)
- [W3C PROV overview](https://www.w3.org/TR/prov-overview/)
- [W3C PROV vocabulary](https://www.w3.org/ns/prov)
- [MCP Resources and annotations](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)
