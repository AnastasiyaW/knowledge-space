---
title: Rights-First Text-to-Mask Training
description: A lineage-controlled training and evaluation contract for Russian text requests, visual grounding, instance masks, and alpha mattes.
---

# Rights-First Text-to-Mask Training

Reference architecture for a text-directed masking system that must distinguish a requested object, produce an instance mask, and preserve soft alpha edges. The governing unit is an auditable asset lineage, not a scraped “dataset.” This is an engineering reference, not legal advice or a warranty that a source, asset, model, or derivative is commercially usable.

## Scope and non-interchangeable outputs

Keep three tasks and their targets separate:

| Dataset | Input | Target | Purpose | Never substitute it for |
|---|---|---|---|---|
| `alpha_refine` | RGB crop + selected instance | exact alpha matte | Train/evaluate boundary and transparency refinement | visual grounding or Russian language understanding |
| `grounding` | full image + canonical English noun phrase | instance box and mask | Benchmark, then optionally tune the grounder | a soft alpha target |
| `ru_resolver_eval` | Russian request | canonical English concept, attributes, `single`/`all` | Train/evaluate the request resolver | a visual model |

The default measurable pipeline is `Russian resolver -> Grounding DINO -> MobileSAM -> AlphaRefiner`. A vision-language model may challenge the grounding stage only: boxes or labels are not per-pixel alpha. Treat the 4 GB local-memory budget as a required benchmark, not as a property of any upstream repository.

## Rights lanes

| Lane | May enter deployable training weights? | Admission rule |
|---|---:|---|
| `P0-commercial` | Yes | Written training/deployment rights or an asset-level licence, provenance, and internal approval recorded in the ledger |
| `P1-research` | No | Architecture work, ablations, and non-production benchmarks only |
| `P2-restricted` | No | Retain source metadata only until the rightsholder grants terms adequate for the intended use |

Code, pretrained weights, dataset annotations, image pixels, and a generated composite have independent rights questions. A permissive repository licence does not grant image rights; an annotation licence does not necessarily govern the pixel asset; a model-card or checkpoint term can differ from code. A composite remains constrained by the most restrictive contributing foreground, background, or source term. Do not place retailer listings, social-media images, or unverified derivatives in `P0`.

## Source register (conditions checked 2026-08-21)

Use public datasets as evidence and research inputs unless the asset-level record meets the `P0` rule above. The listed licence statement is not a conclusion about downstream commercial eligibility.

| Source | Verified contribution | Default lane | Rights interpretation |
|---|---|---|---|
| [P3M-10k](https://github.com/JizhiziLi/P3M) | Face-obfuscated portraits and alpha mattes; upstream describes about 10k images and a release agreement labelled MIT | `P1` | Preserve the exact agreement and provenance; do not infer a complete commercial chain from the repository licence |
| [AM-2k agreement](https://jizhizili.github.io/files/gfm_datasets_agreements/AM-2k_Dataset_Release_Agreement.pdf) | 2,000 animal images in 20 categories with manually labelled alpha mattes | `P1` | The agreement calls the dataset MIT yet says image copyright remains with original owners; require per-asset review for `P0` |
| [Open Images V7](https://storage.googleapis.com/openimages/web/factsfigures_v7.html) | boxes, instance masks, and image-level labels | `P1`, subset review possible | Google licenses annotations CC BY 4.0; its V7 page says images are listed CC BY 2.0 but provides no warranty of each image's status, so retain original URL and licence evidence |
| [RefMatte / RIM](https://github.com/JizhiziLi/RIM) | phrase-to-alpha benchmark; the upstream register describes 47,500 images and 474,996 expressions | `P1` | Upstream release is CC BY-NC; never promote samples, composites, or weights trained on them into `P0` |
| [Trans10K](https://github.com/xieenze/Segment_Transparent_Objects) | transparent-object semantic masks | `P2` | The repository directs commercial users to contact authors; masks are semantic targets, not alpha mattes |
| [SA-1B](https://ai.meta.com/datasets/segment-anything/) | large generic segmentation corpus | `P1` | Apply the dataset licence and access terms as a separate review; it is not a blanket commercial source |

Grounding DINO and MobileSAM publish [code repositories](https://github.com/IDEA-Research/GroundingDINO) with [Apache-2.0 code licences](https://github.com/ChaoningZhang/MobileSAM). Confirm the licence and provenance of every selected checkpoint at acquisition time; code licensing does not resolve its training-data or weight-distribution rights.

## Lineage contract

Store media and derived masks in access-controlled object storage, not Git. Commit append-only manifests and hashes. Each derivative must trace to its original source and its split group.

```json
{"source_id":"src_00017","terms_url":"https://rights.example/terms","rights_lane":"P0-commercial","approval_id":"APR-2026-041","evidence_sha256":"..."}
{"asset_id":"asset_00421","source_id":"src_00017","original_url":"https://rights.example/a.jpg","media_sha256":"...","width":2048,"height":1365,"origin_asset_group":"origin_008"}
{"instance_id":"inst_00831","asset_id":"asset_00421","concept_en":"earring","bbox_xyxy":[812,190,1118,801],"mask_uri":"s3://private/masks/00831.png","alpha_uri":"s3://private/alpha/00831.png"}
{"query_id":"q_019","entity_id":"inst_00831","canonical_en":"earring","ru_text":"все серьги","mode":"all","attributes":{"material":"gold"}}
{"entity_id":"origin_008","split":"test","split_reason":"sealed-origin-group"}
```

Implement this as `sources.jsonl`, `queries.jsonl`, and Parquet tables for `assets`, `instances`, `scenes`, `splits`, and `quality`. Required fields include `rights_lane`, approval/evidence reference, content hash, `origin_asset_group`, compositor seed for a scene, reviewer, and annotation revision. Preserve supplied 16-bit alpha; derive binary masks and boxes from alpha, never synthesize soft alpha from a binary mask.

## Data construction

1. Build a `P0` foreground bank from commissioned or independently licensed RGBA assets: jewellery, apparel, accessories, consented people, pets, and selected household objects. Human-review every alpha matte.
2. Composite one to five approved foregrounds over separately approved backgrounds. Record foreground IDs, background ID, compositor version/seed, transformations, individual alpha, and union mask for an `all` request. Vary occlusion, scale, light, shadow, JPEG artifacts, blur, low contrast, and chromatic aberration.
3. Add a sealed tranche of real, licensed photos for white-on-white, translucency, reflections, hair/fur, overlaps, and small jewellery. Synthetic composites do not replace this test set.
4. Author the resolver set against sealed image entities. Map Russian lemma, declension, `ё/е`, synonym, typo, plural, color/material, and ambiguity to one canonical English concept. Example: `кот`, `кошка`, and `котёнок` resolve to `cat`; `все серьги` resolves to `earring` with `mode=all`.

The key resolver insight: a public English-labelled vision corpus does not make the system Russian-capable. Keep Russian normalization and cardinality as an explicit, independently scored contract; an ambiguous request must surface ambiguity rather than silently select another concept.

## Leakage controls

`origin_asset_group` is the split key. No original image, foreground, near duplicate, crop, alpha/mask derivative, or composite sharing a source foreground/background may cross train, validation, or test. Hash both exact media and perceptual duplicates; block split assignment on a collision. Seal the test manifest and asset hashes before model selection. Use `GroupKFold` or an equivalent group-aware splitter for development, then a separate sealed test set. See [[segmentation-dataset-preparation]] for crop-level leakage failure modes and [[synthetic-dataset-pipeline]] for reproducible composite generation.

## Quality gates and metrics

Reject empty alpha, a hard opaque edge where a soft edge is expected, invalid/out-of-image box, incorrect premultiplication, visible halo, source collision, or missing rights evidence. Record the rejected revision rather than overwriting it.

| Component | Frozen metrics | Required strata |
|---|---|---|
| Grounder | recall at IoU 0.50/0.75, phrase-selection accuracy, absent-object false-positive rate | jewellery, apparel, person/child, cat/dog, transparent/reflective, white-on-white, multi-instance |
| Alpha refiner | SAD, MSE, boundary F-score | soft-edge, low-contrast, hair/fur, transparent/reflective |
| Russian resolver | exact canonical concept, modifier accuracy, `single`/`all` accuracy, explicit ambiguity rate | inflection, `ё/е`, synonyms, typos, plurals, color/material |

## Training and promotion

1. Freeze the schema, pilot `P0`, split groups, and evaluation harness; measure the untuned Grounding DINO + MobileSAM baseline.
2. Train the AlphaRefiner exclusively on `P0`; select it only against sealed alpha strata.
3. Tune the grounder only when a measured `P0` concept gap remains. Evaluate legacy person/cat/dog strata for non-regression.
4. Run any VLM grounding challenger as a separate experiment with a normalized JSON box interface; feed its selected box to the unchanged mask/refinement stages.
5. Promote only when all conditions pass: rights ledger, leakage audit, frozen-holdout improvement, per-stratum non-regression, reproducible manifest/checkpoint hashes, and measured local peak memory plus latency within the 4 GB target environment.

## Limitations

- Alpha ground truth is inherently ambiguous for motion blur, transparent objects, reflections, hair, fur, and very low contrast; metrics do not replace human visual review.
- Licence labels and dataset terms can change and may not answer publicity, privacy, trademark, consent, jurisdiction, or derivative-work questions. Re-check the original page and the asset record before each new use.
- The resolver can map words and cardinality but cannot establish that an image contains the requested object; absent-object handling remains a visual-grounding requirement.
- A 4 GB measurement on one device, driver, resolution, and runtime does not generalize to other hardware or image sizes.

## Gotchas

- **Repository licence mistaken for data clearance:** Apache/MIT code or a checkpoint download does not license the dataset images or the model's training corpus. -> **Fix:** gate code, weights, annotations, and pixels separately in the source ledger.
- **Split after compositing:** derived scenes can place the same foreground or background in train and test, creating implausibly high scores. -> **Fix:** assign every derivative its immutable `origin_asset_group` before any split and fail on exact/perceptual collisions.
- **Binary mask treated as alpha:** a segmentation mask cannot recover hair, glass, or antialiased edges. -> **Fix:** store and score alpha separately; derive box/mask from alpha only for auxiliary stages.
- **Russian prompt passed through unchanged:** inflection, plurality, and `все` alter selection semantics even when the noun maps correctly. -> **Fix:** emit canonical English concept, modifiers, cardinality, and an explicit ambiguity status before grounding.

## See Also

- [[segmentation-dataset-preparation]]
- [[synthetic-dataset-pipeline]]
- [[in-context-segmentation]]
- [[paired-training-for-restoration]]
