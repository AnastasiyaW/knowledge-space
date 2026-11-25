---
title: "Rechtebasiertes Text-to-Mask-Training"
description: "Ein lineage-kontrollierter Trainings- und Evaluierungsvertrag für russischsprachige Textanfragen, visuelles Grounding, Instanzmasken und Alpha-Mattes."
level: 3
source_sha256: 4fc59906598afc1af9c1337757c9cc5da9f6145b09798d7212aab0229e9c6e6f
translation: machine
translated_at: '2026-10-24'
---
# Rechtebasiertes Text-to-Mask-Training {#rights-first-text-to-mask-training}

Referenzarchitektur für ein textgesteuertes Maskierungssystem, das ein angefragtes Objekt identifizieren, eine Instanzmaske erzeugen und weiche Alpha-Kanten erhalten muss. Die maßgebliche Einheit ist eine prüfbare Asset-Lineage, kein gescrapptes „Dataset“. Dies ist eine technische Referenz, keine Rechtsberatung und keine Zusicherung, dass eine Quelle, ein Asset, ein Modell oder ein Derivat kommerziell nutzbar ist.

## Umfang und nicht austauschbare Ausgaben {#scope-and-non-interchangeable-outputs}

Halten Sie drei Aufgaben und ihre Zielgrößen getrennt:

| Dataset | Eingabe | Ziel | Zweck | Niemals ersetzen durch |
|---|---|---|---|---|
| `alpha_refine` | RGB-Ausschnitt + ausgewählte Instanz | exaktes Alpha-Matte | Training/Evaluierung der Kanten- und Transparenzverfeinerung | visuelles Grounding oder Verständnis der russischen Sprache |
| `grounding` | vollständiges Bild + kanonische englische Nominalphrase | Instanzbox und Maske | Benchmark, anschließend optionale Feinabstimmung des Grounders | ein weiches Alpha-Ziel |
| `ru_resolver_eval` | russische Anfrage | kanonisches englisches Konzept, Attribute, `single`/`all` | Training/Evaluierung des Anfrage-Resolvers | ein visuelles Modell |

Die standardmäßige messbare Pipeline lautet `Russian resolver -> Grounding DINO -> MobileSAM -> AlphaRefiner`. Ein Vision-Language-Modell darf nur die Grounding-Stufe herausfordern: Boxen oder Labels sind kein pixelgenaues Alpha. Behandeln Sie das lokale Speicherbudget von 4 GB als verpflichtenden Benchmark und nicht als Eigenschaft eines vorgelagerten Repositorys.

## Rechte-Lanes {#rights-lanes}

| Lane | Darf in deploybare Trainingsgewichte einfließen? | Zulassungsregel |
|---|---:|---|
| `P0-commercial` | Ja | Schriftliche Trainings-/Deployment-Rechte oder eine Lizenz auf Asset-Ebene, Provenienz und interne Freigabe, im Ledger erfasst |
| `P1-research` | Nein | Nur Architekturarbeit, Ablationen und nicht produktive Benchmarks |
| `P2-restricted` | Nein | Nur Quellmetadaten speichern, bis die Rechteinhaber Bedingungen gewähren, die für den vorgesehenen Zweck ausreichen |

Code, vortrainierte Gewichte, Dataset-Annotationen, Bildpixel und ein generiertes Composite werfen jeweils eigenständige Rechtefragen auf. Eine permissive Repository-Lizenz gewährt keine Bildrechte; eine Annotationslizenz regelt nicht zwingend das Pixel-Asset; eine Modellkarten- oder Checkpoint-Bedingung kann vom Code abweichen. Ein Composite unterliegt weiterhin der restriktivsten Bedingung eines beitragenden Vordergrunds, Hintergrunds oder einer Quelle. Platzieren Sie keine Händlerangebote, Social-Media-Bilder oder ungeprüften Derivate in `P0`.

## Quellenregister (Bedingungen geprüft am 2026-08-21) {#source-register-conditions-checked-2026-08-21}

Verwenden Sie öffentliche Datasets als Evidenz und Forschungsinput, es sei denn, der Asset-Datensatz erfüllt die obige `P0`-Regel. Die aufgeführte Lizenzangabe ist keine Aussage über die kommerzielle Verwendbarkeit im Downstream.

| Quelle | Geprüfter Beitrag | Standard-Lane | Rechtliche Einordnung |
|---|---|---|---|
| [P3M-10k](https://github.com/JizhiziLi/P3M) | Porträts mit verpixelten Gesichtern und Alpha-Mattes; die Upstream-Beschreibung nennt etwa 10k Bilder und eine als MIT bezeichnete Freigabevereinbarung | `P1` | Die exakte Vereinbarung und Provenienz bewahren; aus der Repository-Lizenz keine vollständige kommerzielle Kette ableiten |
| [AM-2k-Vereinbarung](https://jizhizili.github.io/files/gfm_datasets_agreements/AM-2k_Dataset_Release_Agreement.pdf) | 2.000 Tierbilder in 20 Kategorien mit manuell annotierten Alpha-Mattes | `P1` | Die Vereinbarung bezeichnet das Dataset als MIT, besagt aber, dass die Bildrechte bei den ursprünglichen Inhabern verbleiben; für `P0` ist eine Prüfung pro Asset erforderlich |
| [Open Images V7](https://storage.googleapis.com/openimages/web/factsfigures_v7.html) | Boxen, Instanzmasken und Bild-Labels | `P1`, Teilmengenprüfung möglich | Google lizenziert Annotationen unter CC BY 4.0; die V7-Seite nennt die Bilder als CC BY 2.0, übernimmt aber keine Gewähr für den Status jedes einzelnen Bildes; daher ursprüngliche URL und Lizenznachweis aufbewahren |
| [RefMatte / RIM](https://github.com/JizhiziLi/RIM) | Phrase-zu-Alpha-Benchmark; das Upstream-Register beschreibt 47.500 Bilder und 474.996 Ausdrücke | `P1` | Upstream-Veröffentlichung unter CC BY-NC; Samples, Composites oder Gewichte, die darauf trainiert wurden, niemals nach `P0` überführen |
| [Trans10K](https://github.com/xieenze/Segment_Transparent_Objects) | semantische Masken transparenter Objekte | `P2` | Das Repository verweist kommerzielle Nutzer an die Autoren; die Masken sind semantische Ziele, keine Alpha-Mattes |
| [SA-1B](https://ai.meta.com/datasets/segment-anything/) | großer generischer Segmentierungskorpus | `P1` | Dataset-Lizenz und Zugriffsbedingungen als separate Prüfung anwenden; keine pauschale kommerzielle Quelle |

Grounding DINO und MobileSAM veröffentlichen [Code-Repositorys](https://github.com/IDEA-Research/GroundingDINO) mit [Apache-2.0-Code-Lizenzen](https://github.com/ChaoningZhang/MobileSAM). Prüfen Sie Lizenz und Provenienz jedes ausgewählten Checkpoints zum Zeitpunkt der Beschaffung; die Code-Lizenzierung klärt weder die Rechte an den Trainingsdaten noch an der Weitergabe der Gewichte.

## Lineage-Vertrag {#lineage-contract}

Speichern Sie Medien und abgeleitete Masken in zugriffsgeschütztem Objektspeicher, nicht in Git. Committen Sie nur anhängbare Manifeste und Hashes. Jedes Derivat muss auf seine Originalquelle und seine Split-Gruppe zurückführbar sein.

```json
{"source_id":"src_00017","terms_url":"https://rights.example/terms","rights_lane":"P0-commercial","approval_id":"APR-2026-041","evidence_sha256":"..."}
{"asset_id":"asset_00421","source_id":"src_00017","original_url":"https://rights.example/a.jpg","media_sha256":"...","width":2048,"height":1365,"origin_asset_group":"origin_008"}
{"instance_id":"inst_00831","asset_id":"asset_00421","concept_en":"earring","bbox_xyxy":[812,190,1118,801],"mask_uri":"s3://private/masks/00831.png","alpha_uri":"s3://private/alpha/00831.png"}
{"query_id":"q_019","entity_id":"inst_00831","canonical_en":"earring","ru_text":"все серьги","mode":"all","attributes":{"material":"gold"}}
{"entity_id":"origin_008","split":"test","split_reason":"sealed-origin-group"}
```

Implementieren Sie dies als `sources.jsonl`, `queries.jsonl` und Parquet-Tabellen für `assets`, `instances`, `scenes`, `splits` und `quality`. Pflichtfelder umfassen `rights_lane`, Freigabe-/Nachweisreferenz, Content-Hash, `origin_asset_group`, Compositor-Seed für eine Szene, Reviewer und Annotations-Revision. Bewahren Sie das gelieferte 16-Bit-Alpha; leiten Sie binäre Masken und Boxen aus dem Alpha ab, erzeugen Sie niemals weiches Alpha aus einer binären Maske.

## Datenaufbau {#data-construction}

1. Erstellen Sie einen `P0`-Vordergrund-Bestand aus beauftragten oder unabhängig lizenzierten RGBA-Assets: Schmuck, Bekleidung, Accessoires, einwilligende Personen, Haustiere und ausgewählte Haushaltsgegenstände. Jedes Alpha-Matte wird von Menschen geprüft.
2. Komponieren Sie einen bis fünf freigegebene Vordergründe über separat freigegebenen Hintergründen. Erfassen Sie Vordergrund-IDs, Hintergrund-ID, Compositor-Version/Seed, Transformationen, individuelles Alpha und die Vereinigungsmaske für eine `all`-Anfrage. Variieren Sie Verdeckung, Skalierung, Licht, Schatten, JPEG-Artefakte, Unschärfe, geringen Kontrast und chromatische Aberration.
3. Ergänzen Sie ein gesperrtes Kontingent realer, lizenzierter Fotos für Weiß-auf-Weiß, Transluzenz, Reflexionen, Haare/Fell, Überlappungen und kleinen Schmuck. Synthetische Composites ersetzen dieses Testset nicht.
4. Erstellen Sie das Resolver-Set anhand gesperrter Bildentitäten. Ordnen Sie russisches Lemma, Deklination, `ё/е`, Synonym, Tippfehler, Plural, Farbe/Material und Mehrdeutigkeit einem einzigen kanonischen englischen Konzept zu. Beispiel: `кот`, `кошка` und `котёнок` werden zu `cat` aufgelöst; `все серьги` wird zu `earring` mit `mode=all` aufgelöst.

Die zentrale Erkenntnis zum Resolver: Ein öffentlicher, englisch beschrifteter Bildkorpus macht das System nicht russischfähig. Halten Sie russische Normalisierung und Kardinalität als explizites, unabhängig bewertetes Vertragselement; eine mehrdeutige Anfrage muss die Mehrdeutigkeit sichtbar machen, statt stillschweigend ein anderes Konzept auszuwählen.

## Leakage-Kontrollen {#leakage-controls}

`origin_asset_group` ist der Split-Schlüssel. Kein Originalbild, kein Vordergrund, kein Near-Duplicate, kein Ausschnitt, kein Alpha-/Masken-Derivat und kein Composite, das einen Quell-Vordergrund oder -Hintergrund teilt, darf zwischen Training, Validierung und Test wechseln. Hashen Sie sowohl exakte Medien als auch perzeptuelle Duplikate; blockieren Sie die Split-Zuweisung bei einer Kollision. Versiegeln Sie das Testmanifest und die Asset-Hashes vor der Modellauswahl. Verwenden Sie `GroupKFold` oder einen gleichwertigen gruppenbewussten Splitter für die Entwicklung, danach ein separates, versiegeltes Testset. Siehe [[segmentation-dataset-preparation]] für Leakage-Fehlerbilder auf Ausschnittebene und [[synthetic-dataset-pipeline]] für reproduzierbare Composite-Erzeugung.

## Qualitätsgates und Metriken {#quality-gates-and-metrics}

Verwerfen Sie leeres Alpha, eine harte, undurchsichtige Kante, wo eine weiche Kante erwartet wird, eine ungültige oder außerhalb des Bildes liegende Box, falsche Premultiplikation, sichtbaren Halo, Quellenkollision oder fehlende Rechtenachweise. Erfassen Sie die abgelehnte Revision, statt sie zu überschreiben.

| Komponente | Festgelegte Metriken | Pflicht-Stratifizierung |
|---|---|---|
| Grounder | Recall bei IoU 0,50/0,75, Genauigkeit der Phrasenauswahl, Falsch-Positiv-Rate bei abwesendem Objekt | Schmuck, Bekleidung, Person/Kind, Katze/Hund, transparent/reflektierend, Weiß-auf-Weiß, Mehrfachinstanzen |
| Alpha-Verfeinerung | SAD, MSE, Boundary-F-Score | weiche Kante, geringer Kontrast, Haare/Fell, transparent/reflektierend |
| Russischer Resolver | exakte kanonische Konzeptzuordnung, Genauigkeit der Modifikatoren, Genauigkeit für `single`/`all`, Rate expliziter Mehrdeutigkeit | Flexion, `ё/е`, Synonyme, Tippfehler, Plurale, Farbe/Material |

## Training und Freigabe {#training-and-promotion}

1. Frieren Sie Schema, Pilot-`P0`, Split-Gruppen und Evaluierungsumgebung ein; messen Sie die ungetunte Baseline aus Grounding DINO + MobileSAM.
2. Trainieren Sie den AlphaRefiner ausschließlich auf `P0`; wählen Sie ihn nur anhand der versiegelten Alpha-Stratifizierungen aus.
3. Tunen Sie den Grounder nur, wenn eine gemessene `P0`-Konzeptlücke verbleibt. Evaluieren Sie die bestehenden Person-/Katze-/Hund-Stratifizierungen auf Nicht-Regression.
4. Führen Sie jede VLM-Grounding-Herausforderung als separates Experiment mit einer normalisierten JSON-Box-Schnittstelle aus; geben Sie die ausgewählte Box an die unveränderten Masken- und Verfeinerungsstufen weiter.
5. Geben Sie nur frei, wenn alle Bedingungen erfüllt sind: Rechte-Ledger, Leakage-Audit, Verbesserung auf dem eingefrorenen Holdout, Nicht-Regression je Stratum, reproduzierbare Manifest-/Checkpoint-Hashes sowie gemessener lokaler Speicherspitzenwert und Latenz innerhalb der 4-GB-Zielumgebung.

## Einschränkungen {#limitations}

- Alpha-Ground-Truth ist bei Bewegungsunschärfe, transparenten Objekten, Reflexionen, Haaren, Fell und sehr geringem Kontrast inhärent mehrdeutig; Metriken ersetzen keine visuelle Prüfung durch Menschen.
- Lizenzangaben und Dataset-Bedingungen können sich ändern und beantworten möglicherweise keine Fragen zu Persönlichkeitsrechten, Datenschutz, Marken, Einwilligung, Rechtsordnung oder Bearbeitungen. Prüfen Sie die Originalseite und den Asset-Datensatz vor jeder neuen Verwendung erneut.
- Der Resolver kann Wörter und Kardinalität abbilden, kann aber nicht belegen, dass ein Bild das angefragte Objekt enthält; die Behandlung abwesender Objekte bleibt eine Anforderung an das visuelle Grounding.
- Eine 4-GB-Messung auf einem Gerät, mit einem Treiber, einer Auflösung und einer Laufzeitumgebung lässt sich nicht auf andere Hardware oder Bildgrößen übertragen.

## Fallstricke {#gotchas}

- **Repository-Lizenz mit Datenfreigabe verwechselt:** Apache-/MIT-Code oder ein Checkpoint-Download lizenziert weder die Datasetbilder noch den Trainingskorpus des Modells. -> **Lösung:** Code, Gewichte, Annotationen und Pixel im Quellen-Ledger getrennt freigeben.
- **Split nach dem Compositing:** Abgeleitete Szenen können denselben Vordergrund oder Hintergrund in Training und Test platzieren und so unrealistisch hohe Scores erzeugen. -> **Lösung:** Jedem Derivat vor jedem Split seine unveränderliche `origin_asset_group` zuweisen und bei exakten/perzeptuellen Kollisionen fehlschlagen.
- **Binäre Maske als Alpha behandelt:** Eine Segmentierungsmaske kann Haare, Glas oder antialiasierte Kanten nicht rekonstruieren. -> **Lösung:** Alpha getrennt speichern und bewerten; Box/Maske nur für Hilfsstufen aus dem Alpha ableiten.
- **Russischer Prompt unverändert weitergereicht:** Flexion, Plural und `все` verändern die Auswahlsemantik, selbst wenn das Substantiv korrekt abgebildet wird. -> **Lösung:** Vor dem Grounding kanonisches englisches Konzept, Modifikatoren, Kardinalität und einen expliziten Mehrdeutigkeitsstatus ausgeben.

## Siehe auch {#see-also}

- [[segmentation-dataset-preparation]]
- [[synthetic-dataset-pipeline]]
- [[in-context-segmentation]]
- [[paired-training-for-restoration]]
