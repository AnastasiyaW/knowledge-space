---
title: "Entraînement text-to-mask axé sur les droits"
description: "Contrat d'entraînement et d'évaluation à traçabilité contrôlée pour les requêtes en russe, l'ancrage visuel, les masques d'instance et les mattes alpha."
level: 3
source_sha256: 4fc59906598afc1af9c1337757c9cc5da9f6145b09798d7212aab0229e9c6e6f
translation: machine
translated_at: '2026-10-24'
---
# Entraînement text-to-mask axé sur les droits {#rights-first-text-to-mask-training}

Architecture de référence pour un système de masquage dirigé par texte, qui doit distinguer un objet demandé, produire un masque d'instance et préserver les bords alpha doux. L'unité de gouvernance est une lignée d'actifs auditable, et non un « dataset » collecté par scraping. Il s'agit d'une référence d'ingénierie, et non d'un avis juridique ni d'une garantie qu'une source, un actif, un modèle ou un dérivé est utilisable commercialement.

## Périmètre et sorties non interchangeables {#scope-and-non-interchangeable-outputs}

Gardez trois tâches et leurs cibles séparées :

| Dataset | Entrée | Cible | Objectif | Ne jamais le substituer à |
|---|---|---|---|---|
| `alpha_refine` | recadrage RGB + instance sélectionnée | matte alpha exacte | Entraîner et évaluer l'affinement des bords et de la transparence | l'ancrage visuel ou la compréhension du russe |
| `grounding` | image complète + syntagme nominal canonique en anglais | boîte et masque d'instance | Évaluer, puis optionnellement affiner le module d'ancrage | une cible alpha douce |
| `ru_resolver_eval` | requête en russe | concept canonique en anglais, attributs, `single`/`all` | Entraîner et évaluer le résolveur de requêtes | un modèle visuel |

Le pipeline mesurable par défaut est `Russian resolver -> Grounding DINO -> MobileSAM -> AlphaRefiner`. Un modèle vision-langage peut uniquement contester l'étape d'ancrage : les boîtes ou les étiquettes ne sont pas des valeurs alpha par pixel. Considérez le budget mémoire local de 4 Go comme un critère de benchmark obligatoire, et non comme une propriété d'un dépôt amont.

## Voies de droits {#rights-lanes}

| Voie | Peut entrer dans des poids d'entraînement déployables ? | Règle d'admission |
|---|---:|---|
| `P0-commercial` | Oui | Droits d'entraînement/déploiement écrits, ou licence au niveau de l'actif, provenance et approbation interne consignées dans le registre |
| `P1-research` | Non | Travaux d'architecture, ablations et benchmarks non destinés à la production uniquement |
| `P2-restricted` | Non | Conserver uniquement les métadonnées source tant que le titulaire des droits n'accorde pas des conditions adaptées à l'usage visé |

Le code, les poids pré-entraînés, les annotations de dataset, les pixels d'image et un composite généré posent des questions de droits indépendantes. Une licence permissive de dépôt ne confère aucun droit sur les images ; une licence d'annotation ne régit pas nécessairement l'actif pixel ; une condition de fiche modèle ou de checkpoint peut différer de celle du code. Un composite reste soumis à la condition la plus restrictive parmi celles des éléments contributeurs, qu'il s'agisse du premier plan, de l'arrière-plan ou de la source. Ne placez ni annonces de revendeurs, ni images de réseaux sociaux, ni dérivés non vérifiés dans `P0`.

## Registre des sources (conditions vérifiées au 2026-08-21) {#source-register-conditions-checked-2026-08-21}

Utilisez les datasets publics comme preuves et entrées de recherche, sauf si l'enregistrement au niveau de l'actif satisfait la règle `P0` ci-dessus. La mention de licence indiquée ne constitue pas une conclusion sur l'admissibilité commerciale en aval.

| Source | Apport vérifié | Voie par défaut | Interprétation des droits |
|---|---|---|---|
| [P3M-10k](https://github.com/JizhiziLi/P3M) | Portraits à visage flouté et mattes alpha ; la documentation amont décrit environ 10 000 images et un accord de diffusion étiqueté MIT | `P1` | Conservez l'accord exact et la provenance ; ne déduisez pas une chaîne commerciale complète de la seule licence du dépôt |
| [Accord AM-2k](https://jizhizili.github.io/files/gfm_datasets_agreements/AM-2k_Dataset_Release_Agreement.pdf) | 2 000 images d'animaux dans 20 catégories, avec mattes alpha annotées manuellement | `P1` | L'accord qualifie le dataset de MIT mais précise que le droit d'auteur sur les images reste à leurs propriétaires d'origine ; exigez une revue par actif pour `P0` |
| [Open Images V7](https://storage.googleapis.com/openimages/web/factsfigures_v7.html) | boîtes, masques d'instance et étiquettes au niveau image | `P1`, revue possible par sous-ensemble | Google publie les annotations sous CC BY 4.0 ; sa page V7 indique que les images sont listées en CC BY 2.0 mais ne garantit pas le statut de chaque image ; conservez l'URL d'origine et la preuve de licence |
| [RefMatte / RIM](https://github.com/JizhiziLi/RIM) | benchmark syntagme-vers-alpha ; le registre amont décrit 47 500 images et 474 996 expressions | `P1` | La version amont est sous CC BY-NC ; ne faites jamais passer en `P0` des échantillons, des composites ou des poids entraînés sur ces données |
| [Trans10K](https://github.com/xieenze/Segment_Transparent_Objects) | masques sémantiques d'objets transparents | `P2` | Le dépôt demande aux utilisateurs commerciaux de contacter les auteurs ; ces masques sont des cibles sémantiques, et non des mattes alpha |
| [SA-1B](https://ai.meta.com/datasets/segment-anything/) | vaste corpus générique de segmentation | `P1` | Appliquez la licence du dataset et ses conditions d'accès dans une revue distincte ; ce n'est pas une source commerciale générale |

Grounding DINO et MobileSAM publient leurs [dépôts de code](https://github.com/IDEA-Research/GroundingDINO), sous licences de code [Apache-2.0](https://github.com/ChaoningZhang/MobileSAM). Vérifiez la licence et la provenance de chaque checkpoint retenu au moment de son acquisition : la licence du code ne règle ni les droits sur les données d'entraînement ni ceux relatifs à la distribution des poids.

## Contrat de traçabilité {#lineage-contract}

Stockez les médias et les masques dérivés dans un stockage objet à accès contrôlé, et non dans Git. Validez des manifestes en ajout seul et des empreintes de hachage. Chaque dérivé doit remonter à sa source d'origine et à son groupe de découpage.

```json
{"source_id":"src_00017","terms_url":"https://rights.example/terms","rights_lane":"P0-commercial","approval_id":"APR-2026-041","evidence_sha256":"..."}
{"asset_id":"asset_00421","source_id":"src_00017","original_url":"https://rights.example/a.jpg","media_sha256":"...","width":2048,"height":1365,"origin_asset_group":"origin_008"}
{"instance_id":"inst_00831","asset_id":"asset_00421","concept_en":"earring","bbox_xyxy":[812,190,1118,801],"mask_uri":"s3://private/masks/00831.png","alpha_uri":"s3://private/alpha/00831.png"}
{"query_id":"q_019","entity_id":"inst_00831","canonical_en":"earring","ru_text":"все серьги","mode":"all","attributes":{"material":"gold"}}
{"entity_id":"origin_008","split":"test","split_reason":"sealed-origin-group"}
```

Implémentez ceci sous forme de `sources.jsonl`, `queries.jsonl` et de tables Parquet pour `assets`, `instances`, `scenes`, `splits` et `quality`. Les champs requis incluent `rights_lane`, la référence d'approbation/de preuve, le hachage de contenu, `origin_asset_group`, la graine du compositeur pour une scène, le relecteur et la révision d'annotation. Conservez l'alpha 16 bits fournie ; dérivez les masques binaires et les boîtes à partir de l'alpha, et ne synthétisez jamais un alpha doux à partir d'un masque binaire.

## Construction des données {#data-construction}

1. Constituez une banque de premiers plans `P0` à partir d'actifs RGBA commandés ou sous licence indépendante : bijoux, vêtements, accessoires, personnes ayant donné leur consentement, animaux de compagnie et objets domestiques sélectionnés. Faites relire chaque matte alpha par un humain.
2. Composez un à cinq premiers plans approuvés sur des arrière-plans approuvés séparément. Consignez les identifiants des premiers plans, l'identifiant de l'arrière-plan, la version et la graine du compositeur, les transformations, l'alpha individuel et le masque d'union pour une requête `all`. Faites varier l'occlusion, l'échelle, la lumière, les ombres, les artefacts JPEG, le flou, le faible contraste et l'aberration chromatique.
3. Ajoutez un lot scellé de photos réelles sous licence, couvrant les cas blanc-sur-blanc, la translucidité, les reflets, les cheveux/la fourrure, les chevauchements et les petits bijoux. Les composites synthétiques ne remplacent pas cet ensemble de test.
4. Rédigez l'ensemble de résolution à partir d'entités d'image scellées. Faites correspondre lemme russe, déclinaison, `ё/е`, synonyme, faute de frappe, pluriel, couleur/matière et ambiguïté à un seul concept canonique en anglais. Exemple : `кот`, `кошка` et `котёнок` se résolvent en `cat` ; `все серьги` se résout en `earring` avec `mode=all`.

L'idée clé concernant le résolveur : un corpus visuel public étiqueté en anglais ne rend pas le système capable de traiter le russe. Conservez la normalisation russe et la cardinalité comme un contrat explicite, évalué indépendamment ; une requête ambiguë doit faire apparaître l'ambiguïté plutôt que de sélectionner silencieusement un autre concept.

## Contrôles de fuite {#leakage-controls}

`origin_asset_group` est la clé de découpage. Aucune image originale, aucun premier plan, aucun quasi-doublon, aucun recadrage, aucun dérivé alpha/masque ni aucun composite partageant un premier plan ou un arrière-plan source ne peut passer entre l'entraînement, la validation et le test. Calculez le hachage des médias exacts et des doublons perceptuels ; bloquez l'affectation à un split en cas de collision. Scellez le manifeste de test et les hachages des actifs avant toute sélection de modèle. Utilisez `GroupKFold` ou un découpeur équivalent tenant compte des groupes pour le développement, puis un ensemble de test scellé séparé. Consultez [[segmentation-dataset-preparation]] pour les modes de défaillance de fuite au niveau des recadrages, et [[synthetic-dataset-pipeline]] pour la génération reproductible de composites.

## Portes de qualité et métriques {#quality-gates-and-metrics}

Rejetez un alpha vide, un bord opaque et dur là où un bord doux est attendu, une boîte invalide ou hors image, une prémultiplication incorrecte, un halo visible, une collision de sources ou une preuve de droits manquante. Consignez la révision rejetée au lieu de l'écraser.

| Composant | Métriques figées | Strates obligatoires |
|---|---|---|
| Module d'ancrage | rappel à IoU 0,50/0,75, précision de sélection du syntagme, taux de faux positifs sur objet absent | bijoux, vêtements, personne/enfant, chat/chien, transparent/réfléchissant, blanc-sur-blanc, multi-instance |
| Affineur alpha | SAD, MSE, F-score de frontière | bord doux, faible contraste, cheveux/fourrure, transparent/réfléchissant |
| Résolveur russe | concept canonique exact, précision des modificateurs, précision `single`/`all`, taux d'ambiguïté explicite | flexion, `ё/е`, synonymes, fautes de frappe, pluriels, couleur/matière |

## Entraînement et promotion {#training-and-promotion}

1. Figez le schéma, le pilote `P0`, les groupes de découpage et le harnais d'évaluation ; mesurez la référence Grounding DINO + MobileSAM non ajustée.
2. Entraînez AlphaRefiner exclusivement sur `P0` ; sélectionnez-le uniquement sur les strates alpha scellées.
3. N'affinez le module d'ancrage que lorsqu'un écart mesuré de concepts `P0` persiste. Évaluez les strates historiques personne/chat/chien pour détecter toute régression.
4. Exécutez tout challenger d'ancrage VLM comme expérience séparée, avec une interface de boîte JSON normalisée ; transmettez la boîte retenue aux étapes de masque et d'affinement, inchangées.
5. Ne promouvez que si toutes les conditions sont remplies : registre des droits, audit de fuite, amélioration sur le holdout figé, absence de régression par strate, hachages reproductibles du manifeste et du checkpoint, et pic mémoire local ainsi que latence mesurés dans l'environnement cible de 4 Go.

## Limites {#limitations}

- La vérité terrain alpha est intrinsèquement ambiguë pour le flou de mouvement, les objets transparents, les reflets, les cheveux, la fourrure et les contrastes très faibles ; les métriques ne remplacent pas une revue visuelle humaine.
- Les étiquettes de licence et les conditions des datasets peuvent évoluer et ne répondent pas nécessairement aux questions de droit à l'image, de vie privée, de marque, de consentement, de juridiction ou d'œuvre dérivée. Revérifiez la page d'origine et l'enregistrement de l'actif avant chaque nouvelle utilisation.
- Le résolveur peut faire correspondre des mots et une cardinalité, mais il ne peut pas établir qu'une image contient l'objet demandé ; la gestion des objets absents reste une exigence d'ancrage visuel.
- Une mesure de 4 Go sur un seul appareil, un pilote, une résolution et un environnement d'exécution ne se généralise pas à d'autres matériels ou tailles d'image.

## Pièges fréquents {#gotchas}

- **Licence de dépôt confondue avec une autorisation sur les données :** un code sous Apache/MIT ou un téléchargement de checkpoint ne licencie ni les images du dataset ni le corpus d'entraînement du modèle. -> **Correction :** contrôlez séparément le code, les poids, les annotations et les pixels dans le registre des sources.
- **Découpage après composition :** des scènes dérivées peuvent placer le même premier plan ou le même arrière-plan dans l'entraînement et le test, ce qui produit des scores artificiellement élevés. -> **Correction :** affectez à chaque dérivé son `origin_asset_group` immuable avant tout découpage, et faites échouer le pipeline en cas de collision exacte ou perceptuelle.
- **Masque binaire traité comme un alpha :** un masque de segmentation ne peut pas restituer les cheveux, le verre ou les bords anticrénelés. -> **Correction :** stockez et évaluez l'alpha séparément ; ne dérivez boîte et masque de l'alpha que pour les étapes auxiliaires.
- **Requête russe transmise sans transformation :** la flexion, le pluriel et `все` modifient la sémantique de sélection même lorsque le nom est correctement associé. -> **Correction :** émettez un concept canonique en anglais, les modificateurs, la cardinalité et un statut d'ambiguïté explicite avant l'ancrage.

## Voir aussi {#see-also}

- [[segmentation-dataset-preparation]]
- [[synthetic-dataset-pipeline]]
- [[in-context-segmentation]]
- [[paired-training-for-restoration]]
