---
title: "Happyin Knowledge Space"
category: architecture
tags: [knowledge-base, llm-agents, mkdocs, cloudflare-pages, project-history]
level: 3
source_sha256: b15d7b571b0bc98fe0d9af2b1ff834068c1b0160e40707febc7df6a48d90e52e
translation: machine
translated_at: '2026-10-24'
---
# Happyin Knowledge Space {#happyin-knowledge-space}

## Identité du projet {#project-identity}

| Champ | Valeur vérifiée |
|---|---|
| Nom public | Happyin Knowledge Space |
| Dépôt et projet Cloudflare Pages | [`knowledge-space`](https://github.com/AnastasiyaW/knowledge-space) |
| Site public | [happyin.space](https://happyin.space/) |
| Format source | Markdown rendu par MkDocs Material |
| Chemin de déploiement | GitHub Actions construit le site, puis le déploie sur Cloudflare Pages avec Wrangler |
| Déploiement de référence audité avant cette version | [`a99e8c6`](https://github.com/AnastasiyaW/knowledge-space/commit/a99e8c6), 2026-06-19 |
| Observation historique du service | `https://happyin.space/` a renvoyé HTTP 200 le 2026-08-21 ; ceci ne constitue pas une affirmation sur un déploiement ultérieur |

Happyin Knowledge Space est une référence technique publique. Le Markdown versionné dans Git
constitue la source du contenu et l'historique de référence ; le site statique en est la
surface de diffusion rendue. La révision de référence citée ci-dessus a terminé avec succès
le workflow de déploiement Cloudflare le 2026-06-19 ; la version actuelle nécessite son propre
workflow et ses propres vérifications de pages en ligne.

## Modèle de contenu et de navigation {#content-and-navigation-model}

Le registre de build défini dans `hooks/stats.py` déclare 28 domaines de contenu acceptés. Il compte
récursivement les fichiers Markdown situés sous ces répertoires de domaine, en excluant chaque
`index.md` ; les tags restent des métadonnées de découverte libres.

Le dépôt ne contient aucune correspondance explicite `nav:` dans `mkdocs.yml`. MkDocs dérive donc la
navigation de l'arborescence `docs/`, tandis que `navigation.indexes`, `navigation.sections`,
`navigation.expand` et les autres fonctionnalités de Material contrôlent le comportement de navigation rendu.

Les préoccupations pertinentes du projet correspondent aux domaines existants :

- `architecture` — frontières du contenu et documentation système
- `llm-agents` et `llm-memory` — récupération orientée agents et contexte durable
- `data-engineering` — métadonnées générées et schémas de validation
- `web-frontend` — comportement du site rendu
- `devops` — build CI et diffusion sur Cloudflare Pages

## Chaîne de publication implémentée {#implemented-publication-path}

```text
docs/{domain}/{article}.md
          |
          v
MkDocs hooks (stats, validation, links, descriptions, wiki-links, public checks)
          |
          v
mkdocs build --strict
          |
          v
GitHub Actions on master -> Wrangler -> Cloudflare Pages -> happyin.space
```

Le fichier `.github/workflows/deploy-cloudflare.yml` s'exécute sur les pushes qualifiants vers `master`
et exécute `mkdocs build --strict` avant `pages deploy site
--project-name=knowledge-space --branch=main`. Des workflows GitHub Actions distincts valident le
format des articles, leur fraîcheur et les liens internes ; le workflow de déploiement ne déclare pas
ces jobs comme dépendances.

La configuration Cloudflare définit également un binding `DB` pour la base D1 `happyin-subscribers`.
Ce binding seul n'établit pas l'existence d'une API d'actualités ou d'historique de projets.

## Historique documenté par le dépôt {#repository-backed-history}

| Date | Jalon | Preuve |
|---|---|---|
| 2026-03-30 | Corpus initial : 385 articles répartis sur 21 domaines | [commit `c8bb9eaf`](https://github.com/AnastasiyaW/knowledge-space/commit/c8bb9eaf) |
| 2026-04-03 | Nom public passé de Knowledge Space à Happyin Knowledge Space | [commit `2af768`](https://github.com/AnastasiyaW/knowledge-space/commit/2af768) |
| 2026-04-22 | 785 articles répartis sur 26 domaines | [commit `a0be61c`](https://github.com/AnastasiyaW/knowledge-space/commit/a0be61c) |
| 2026-05-05 | 806 articles répartis sur 26 domaines | [commit `a2cdc2b`](https://github.com/AnastasiyaW/knowledge-space/commit/a2cdc2b) |
| 2026-06-04 | 834 articles répartis sur 26 domaines | [commit `ab204db`](https://github.com/AnastasiyaW/knowledge-space/commit/ab204db) |
| 2026-06-19 | Articles de recherche sur les agents enrichis ; le total est resté à 834 | [commit `a99e8c6`](https://github.com/AnastasiyaW/knowledge-space/commit/a99e8c6) |
| 2026-08-21 | Schéma d'actualités public 1.3 publié avec historiques de projets et jointures de domaines | [release du flux `730f7cf`](https://github.com/AnastasiyaW/diffusion-love-news/commit/730f7cf5a47a52e6d0ba75c90dceab15ce6e3b95) |
| 2026-08-21 | Le portail protégé a figé chaque lecture du flux sur un unique instantané immuable du producteur | [release web `102c15b`](https://github.com/AnastasiyaW/diffusion-love-web/commit/102c15b3e999beff4114e28c0b24b2b8d2d49bd5) |
| 2026-08-28 | 851 articles répartis sur 26 domaines ; chaque article est accessible depuis un index de domaine et depuis la page de parcours | [commit `aad5ff7`](https://github.com/AnastasiyaW/knowledge-space/commit/aad5ff7) |

Il s'agit de jalons adossés à Git, et non d'une chronologie marketing reconstituée. Un commit
prouve l'état du dépôt qu'il contient ; il ne prouve pas à lui seul un état ultérieur du site en ligne.

## Instantané de la surface publique actuelle (2026-10-10) {#current-public-surface-snapshot-2026-10-10}

| Périmètre | Statut actuel, adossé aux sources | Limite de la preuve |
|---|---|---|
| Registre de contenu | Le registre actuel de `hooks/stats.py` compte **1 321 articles répartis sur 28 domaines**. Il s'agit du nombre d'articles calculé au moment du build : il exclut les fichiers `index.md` des domaines et ne doit pas être remplacé par un total de fichiers Markdown. | Instantané des sources actuelles ; un déploiement futur peut contenir une autre révision. |
| Site public | [happyin.space](https://happyin.space/) reste l'URL de diffusion publique configurée. Les pushes qualifiants vers `master` déclenchent le build strict et le déploiement Cloudflare Pages ; le workflow permet aussi un lancement manuel. | La configuration et la source du workflow prouvent le chemin de publication prévu, pas une réponse en ligne particulière. |
| MCP public | [`io.github.AnastasiyaW/diffusion-love-knowledge` v0.1.0](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.AnastasiyaW%2Fdiffusion-love-knowledge/versions/0.1.0) est active dans le registre officiel MCP ; son point de terminaison public est [https://diffusion.love/mcp](https://diffusion.love/mcp). L'enregistrement a été publié le `2026-10-10T11:01:27.866718Z`. | L'enregistrement établit la découvrabilité et le statut publics à la relecture ; le comportement du point de terminaison exige une vérification de protocole distincte. |
| Recherche et travaux sur les dates de recherche | **Tel que vérifié le 2026-10-10**, la PR [#564](https://github.com/AnastasiyaW/knowledge-space/pull/564) contenait la recherche publique et la prise en charge des dates de recherche par article, qui n'étaient pas encore déployées. Il s'agit d'une observation de déploiement datée, non d'un statut permanent. | Source de la PR et relecture du déploiement à la date de vérification ; aucune affirmation de déploiement ultérieur n'est déduite. |

Le jalon des 851 articles et la release 1.3 du schéma du flux d'actualités restent des
archives historiques datées. Ils ne sont volontairement pas réécrits pour correspondre à cet instantané actuel.

## Dépôt de données d'actualités distinct : frontière {#separate-news-data-repository-boundary}

[`AnastasiyaW/diffusion-love-news`](https://github.com/AnastasiyaW/diffusion-love-news)
est un dépôt public distinct. Le 2026-10-10, `main` correspondait au commit
[`4f631f2`](https://github.com/AnastasiyaW/diffusion-love-news/commit/4f631f2b0fe8ba4ed105bb19bf0beca523da416a).
Ses [métadonnées de flux](https://raw.githubusercontent.com/AnastasiyaW/diffusion-love-news/4f631f2b0fe8ba4ed105bb19bf0beca523da416a/news/_meta.json),
épinglées sur ce commit, déclarent le schéma **1.4**, **917 éléments**, **794 projets** et **5 organisations** ;
l'horodatage de génération est `2026-09-12T11:16:33Z`. La date d'observation n'est pas la date de génération
et ne prouve pas que chaque consommateur sert cette révision.

La release antérieure du schéma 1.3, à l'adresse
[`730f7cf`](https://github.com/AnastasiyaW/diffusion-love-news/commit/730f7cf5a47a52e6d0ba75c90dceab15ce6e3b95),
a ajouté des événements et des affirmations de cycle de vie assortis de preuves, des références de domaines
explicites, des chronologies de projets déterministes, ainsi que des contrôles de schéma et de build.

[`AnastasiyaW/diffusion-love-web`](https://github.com/AnastasiyaW/diffusion-love-web)
est le consommateur distinct. La release
[`102c15b`](https://github.com/AnastasiyaW/diffusion-love-web/commit/102c15b3e999beff4114e28c0b24b2b8d2d49bd5)
valide les versions 1.2 et 1.3 du flux, résout la branche `main` du producteur en un unique SHA de commit complet
par amorçage du navigateur, et affiche les fiches projet à l'adresse `/project/{family_slug}`. Ce commit immuable
prouve la source du consommateur ; le présent article n'infère pas d'état de déploiement ou de trafic actuel à partir
de l'historique des sources. Consultez [le portail lecteur](https://diffusion.love/) séparément lorsqu'une preuve
de déploiement en direct est requise.

Aucun fichier suivi dans `knowledge-space` ne consomme le flux JSON. Le contrat de données ouvert, le portail
d'actualités et cette référence technique publique restent des surfaces de diffusion distinctes, reliées par des
identifiants explicites de dépôt et de projet.

## Règles de preuve {#evidence-rules}

- Un commit de dépôt ne prouve que la modification visible dans ce commit.
- Une réponse HTTP en direct prouve la disponibilité au moment de l'observation, et non une date ou une cause de modification passée.
- Les affirmations importées d'un dépôt distinct exigent une source versionnée et une preuve d'intégration explicite.
- Les relations déduites doivent être marquées `inferred` ; ce ne sont pas des faits vérifiés.
- Le texte source privé et les transcriptions des fournisseurs n'ont pas leur place dans les données publiques.

## Vérification locale {#local-verification}

Exécutez les contrôles du dépôt depuis sa racine :

```powershell
python hooks/freshness_check.py --ci
python lint.link-check.py --strict
python lint.py
mkdocs build --strict
```

Le workflow de déploiement constitue l'automatisation de référence pour la publication. Un article
ajouté localement n'est pas une page en ligne tant qu'une révision des sources le contenant n'a pas
terminé ce workflow.

## Pièges courants {#gotchas}

- **Supposer qu'un fichier de navigation explicite existe :** il n'existe aucune liste `nav:` dans
  `mkdocs.yml`. **Correction :** conservez la hiérarchie `docs/` et vérifiez la navigation MkDocs rendue.
- **Confondre la réussite d'un job de validation de contenu avec un déploiement :** ce sont des workflows
  distincts. **Correction :** inspectez l'exécution du déploiement Cloudflare correspondant au commit concerné.
- **Traiter le binding D1 comme un backend d'historique de projets :** la seule déclaration d'un binding
  n'établit pas cette API. **Correction :** exigez des handlers implémentés et des tests consommateurs avant de documenter une API.
- **Supposer qu'un CDN adressé par branche se met à jour de façon atomique :** jsDelivr peut continuer à servir
  le flux compatible précédent après une modification de `main`. **Correction :** vérifiez la charge utile GitHub Raw
  adressée par commit pour les preuves de release, et maintenez le consommateur compatible avec les deux versions de
  schéma prises en charge pendant la propagation.
- **Présenter le flux d'actualités distinct comme une intégration :** un flux JSON d'apparence compatible n'est pas un
  contrat consommateur. **Correction :** prouvez un schéma publié, un consommateur versionné et un build de bout en bout.
- **Utiliser le site actuel comme preuve historique :** le contenu en ligne peut changer. **Correction :** citez le commit
  ou l'exécution de déploiement datés pour toute affirmation historique.

## Voir aussi {#see-also}

- [[news-development-graph]]
- [[news-research-knowledge-lifecycle]]
- [[architecture-documentation]]
- [[data-serialization-formats]]
- [[testing-and-quality]]
- [[devops-cicd]]
