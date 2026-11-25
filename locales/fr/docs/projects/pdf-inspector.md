---
title: "pdf-inspector"
category: projects
date: 2026-08-03
tags: [firecrawl, pdf-inspector, pdf-inspector-development, project]
aliases: ["pdf-inspector"]
level: 3
source_sha256: 1e48e5441065519fb29b77de8d0959d7ad85cc1dc5bb9341a260d7e684400e7f
translation: machine
translated_at: '2026-10-24'
---
# pdf-inspector {#pdf-inspector}

**Ligne de développement :** `project:pdf-inspector` · fil `pdf-inspector-development`  
**Dernier événement :** 2026-08-03 · 1 événement daté depuis le 2026-08-03 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

pdf-inspector est une bibliothèque et une CLI Rust locales destinées aux développeurs de traitement de PDF : elle classe les PDF à texte natif, numérisés, basés sur des images et mixtes, puis renvoie du Markdown structuré et des données de routage au niveau de la page. — Points d'entrée Rust, Python, Node.js, CLI et WebAssembly pour navigateur. — Texte tenant compte de la position, ordre de lecture, détection de tableaux et OCR optionnel avec provenance. La classification est documentée à environ 10–50 ms ; l'OCR routé nécessite PDFium, ONNX Runtime externes et un ensemble de modèles d'environ 31 Mo. Utilisez-le comme couche locale de classification et d'extraction, mais validez les structures de documents qui comptent pour votre flux de travail.

## Ligne de développement {#development-line}

- **2026-08-03 — dépôt pdf-inspector lié dans le fil Firecrawl.** Le 2026-08-03, le dépôt GitHub de pdf-inspector a été lié dans le fil Firecrawl. Il s'agit d'une référence historique importante, car elle identifie le dépôt source du projet à cette date. Les éléments disponibles n'établissent ni une version publiée, ni une évolution fonctionnelle, ni la maturité du projet.

## Ce qui a changé {#what-changed}

2026-08-03 — le paquet Python de pdf-inspector était déjà public en version 0.2.6 ; des rapports publiés le même jour ont mis en évidence des échecs liés à des xref malformées et à des tableaux épars, de sorte que cette date ne correspond pas à un lancement vérifié. 2026-08-06 — pdf-inspector a été documenté comme le moteur PDF open source distinct de Firecrawl et comme élément des points de terminaison hébergés pour les documents. 2026-08-10 — pdf-inspector a reçu le tag vérifié packages-2026-08-10, qui consolide les versions de paquets au-delà de la lignée Python 0.2.6. 2026-08-13 — pdf-inspector v1.14.2 a ajouté des bornes de ressources pour les PDF pathologiques ainsi que des corrections sur les Form XObject et la mise en page. 2026-08-17 — pdf-inspector v1.15.0 a ajouté l'OCR sélectif via PDFium, ONNX Runtime et PP-OCRv6 Small. 2026-08-21 — PyPI a publié pdf-inspector 1.17.0, la lignée Python publique actuelle. 2026-09-03 — la branche main de pdf-inspector a intégré des modifications de géométrie du texte pivoté et des coordonnées de page visible ; ces modifications du code source restent non publiées.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-03, les praticiens peuvent utiliser le dépôt pdf-inspector lié comme référence source datée lorsqu'ils évaluent des travaux d'inspection de PDF liés à Firecrawl.

1. Installez le binding Python avec `pip install pdf-inspector`, puis appelez `detect_pdf()` sur chaque entrée avant de choisir une voie de traitement.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
2. Pour un résultat à texte natif, appelez `process_pdf()` afin d'obtenir le Markdown ainsi que le type, la confiance, le nombre de pages, les pages nécessitant un OCR, les signaux de mise en page et les indicateurs de problèmes d'encodage.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
3. Pour les documents numérisés ou mixtes, appelez `process_pdf_with_ocr()` en mode auto et conservez la provenance de chaque page (native, OCR ou fusionnée).
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
4. Lorsque l'OCR est routé, installez les builds PDFium et ONNX Runtime documentés, définissez leurs chemins de bibliothèques et préchargez un répertoire de modèles avec le mode hors ligne si l'accès réseau est interdit.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md>
5. Dans un serveur Node, utilisez `processPdfWithOcr()` en asynchrone et inspectez `pagesRoutedToOcr` et `pagesRecommendingHosted`.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md>

## Bonnes pratiques {#best-practices}

- Considérez la classification comme un routage et non comme une décision d'OCR généralisée : conservez le type, la confiance, les raisons par page et la provenance des pages avec le contenu extrait.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md>
- Figez PDFium 153.0.7988.0, ONNX Runtime 1.27.0 et la révision de l'artefact PP-OCRv6 Small pour un OCR reproductible ; préchargez les modèles et utilisez le mode hors ligne pour les déploiements hermétiques.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md>
- Évaluez les performances sur des PDF représentatifs plutôt que de généraliser à partir de la comparaison publiée sur 200 documents, OCR désactivé, sur Apple M4 Pro.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
- Conservez les PDF à startxref malformé dans le registre de non-régression ; un rapport du 3 août a montré que la classification et l'extraction pouvaient toutes deux échouer sur ces fichiers dans la version 0.2.6.
  — <https://github.com/firecrawl/pdf-inspector/issues/228>
- Validez les tableaux épars et regroupés par rapport aux pages sources, car un rapport du 3 août a montré un Markdown bien formé mais structurellement erroné, avec des lignes fusionnées, dans la version 0.2.6.
  — <https://github.com/firecrawl/pdf-inspector/issues/229>
- Normalisez les conventions de numérotation des pages à la frontière de votre système : la classification et l'extraction de régions utilisent des listes de pages indexées à partir de 0, tandis que les sélecteurs OCR et plusieurs types de résultats utilisent une numérotation à partir de 1.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-03 — considérer le lien vers le dépôt comme la preuve que pdf-inspector a été lancé ce jour-là.
- Avant le 2026-08-17 — confier manuellement chaque page numérisée ou mixte à un autre système OCR comme seule voie prise en charge.

## Points encore inconnus {#still-unknown}

- La version exacte ou l'intention associée au 2026-08-03 n'est pas vérifiée : le lien vers le dépôt ne comporte ni version ni note de publication, tandis que les rapports de problèmes du même jour identifient un paquet 0.2.6 déjà public.
- GitHub Releases indique toujours 1.15.0 comme dernière version, alors que le manifeste source actuel et PyPI indiquent 1.17.0 ; aucune page GitHub Release pour 1.16.0 ou 1.17.0 n'a été trouvée.
- Les modifications de coordonnées et de texte pivoté du 2026-09-03 figurent dans le code source actuel et dans la section Unreleased du changelog ; la première version packagée est donc non vérifiée.
- Firecrawl indique que les points de terminaison hébergés /parse et /scrape utilisent pdf-inspector, mais cette recherche n'a pas exécuté indépendamment l'un ou l'autre de ces points de terminaison.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/firecrawl/pdf-inspector | firecrawl/pdf-inspector | 2026-09-05 |
| https://raw.githubusercontent.com/firecrawl/pdf-inspector/main/README.md | README de pdf-inspector | 2026-09-05 |
| https://raw.githubusercontent.com/firecrawl/pdf-inspector/main/Cargo.toml | Cargo.toml de pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/issues/228 | Issue #228 : pas de récupération xref | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/issues/229 | Issue #229 : lignes de tableaux épars/regroupés fusionnées | 2026-09-05 |
| https://www.firecrawl.dev/blog/anydoc-and-pdf-inspector | Présentation d'AnyDoc et de pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/tags | tags de pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/releases/tag/v1.14.2 | Version 1.14.2 — Analyse renforcée pour les PDF pathologiques | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/releases/tag/v1.15.0 | Version 1.15.0 — OCR sélectif pour les PDF numérisés et mixtes | 2026-09-05 |
| https://pypi.org/project/pdf-inspector/ | pdf-inspector sur PyPI | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/commit/636ca1a58bdc1af4cd3fc20b8c1f549a1121cca7 | Commit 636ca1a : géométrie du texte pivoté | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/CHANGELOG.md | changelog de pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md | API Python de pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md | API Node.js de pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md | Configuration de l'environnement OCR de pdf-inspector | 2026-09-05 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:pdf-inspector`, fil `pdf-inspector-development`, 1 événement daté du 2026-08-03 au 2026-08-03.
- **Note pratique :** Au 2026-08-03, les praticiens peuvent utiliser le dépôt pdf-inspector lié comme référence source datée lorsqu'ils évaluent des travaux d'inspection de PDF liés à Firecrawl.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
