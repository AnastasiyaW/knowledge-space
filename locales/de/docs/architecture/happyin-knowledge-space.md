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

## Projektidentität {#project-identity}

| Feld | Geprüfter Wert |
|---|---|
| Öffentlicher Name | Happyin Knowledge Space |
| Repository und Cloudflare-Pages-Projekt | [`knowledge-space`](https://github.com/AnastasiyaW/knowledge-space) |
| Öffentliche Website | [happyin.space](https://happyin.space/) |
| Quellformat | Markdown, gerendert mit MkDocs Material |
| Bereitstellungspfad | GitHub Actions baut die Seite und stellt sie anschließend mit Wrangler auf Cloudflare Pages bereit |
| Vor diesem Release geprüfte Basis-Bereitstellung | [`a99e8c6`](https://github.com/AnastasiyaW/knowledge-space/commit/a99e8c6), 2026-06-19 |
| Historische Beobachtung zum Dienst | `https://happyin.space/` lieferte am 2026-08-21 HTTP 200; dies ist keine Aussage über eine spätere Bereitstellung |

Happyin Knowledge Space ist eine öffentliche technische Referenz. Markdown in Git ist die Inhaltsquelle und die historische Aufzeichnung; die statische Website ist die gerenderte Auslieferungsfläche. Die oben genannte Basisrevision hat den Cloudflare-Bereitstellungsworkflow am 2026-06-19 erfolgreich abgeschlossen. Das aktuelle Release benötigt einen eigenen Workflow-Lauf und eigene Prüfungen der Live-Seiten.

## Inhalts- und Navigationsmodell {#content-and-navigation-model}

Die zur Build-Zeit verwendete Registry in `hooks/stats.py` definiert 28 zugelassene Inhaltsdomänen. Sie zählt rekursiv Markdown-Dateien unterhalb dieser Domänenverzeichnisse und schließt jeweils die `index.md` aus; Tags bleiben frei formulierbare Metadaten zur Auffindbarkeit.

Das Repository enthält in `mkdocs.yml` keine explizite `nav:`-Zuordnung. MkDocs leitet die Navigation daher aus dem Verzeichnisbaum `docs/` ab, während `navigation.indexes`, `navigation.sections`, `navigation.expand` und weitere verwandte Funktionen von Material das gerenderte Navigationsverhalten steuern.

Relevante Themenbereiche des Projekts ordnen sich bestehenden Domänen zu:

- `architecture` — Inhaltsgrenzen und Systemdokumentation
- `llm-agents` und `llm-memory` — agentenorientiertes Retrieval und dauerhafter Kontext
- `data-engineering` — generierte Metadaten und Validierungsmuster
- `web-frontend` — Verhalten der gerenderten Website
- `devops` — CI-Build und Auslieferung über Cloudflare Pages

## Implementierter Veröffentlichungspfad {#implemented-publication-path}

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

Der Workflow `.github/workflows/deploy-cloudflare.yml` läuft bei qualifizierenden Pushes auf `master` und führt `mkdocs build --strict` aus, bevor `pages deploy site --project-name=knowledge-space --branch=main` gestartet wird. Separate GitHub-Actions-Jobs prüfen das Artikelformat, die Aktualität und die internen Links; der Bereitstellungsworkflow deklariert diese Jobs nicht als Abhängigkeiten.

Die Cloudflare-Konfiguration definiert außerdem eine `DB`-Bindung für die D1-Datenbank `happyin-subscribers`. Allein diese Bindung begründet keine API für Nachrichten oder Projekthistorien.

## Aus dem Repository abgeleitete Historie {#repository-backed-history}

| Datum | Meilenstein | Nachweis |
|---|---|---|
| 2026-03-30 | Ursprüngliches Korpus: 385 Artikel in 21 Domänen | [Commit `c8bb9eaf`](https://github.com/AnastasiyaW/knowledge-space/commit/c8bb9eaf) |
| 2026-04-03 | Öffentlicher Name von Knowledge Space zu Happyin Knowledge Space geändert | [Commit `2af768`](https://github.com/AnastasiyaW/knowledge-space/commit/2af768) |
| 2026-04-22 | 785 Artikel in 26 Domänen | [Commit `a0be61c`](https://github.com/AnastasiyaW/knowledge-space/commit/a0be61c) |
| 2026-05-05 | 806 Artikel in 26 Domänen | [Commit `a2cdc2b`](https://github.com/AnastasiyaW/knowledge-space/commit/a2cdc2b) |
| 2026-06-04 | 834 Artikel in 26 Domänen | [Commit `ab204db`](https://github.com/AnastasiyaW/knowledge-space/commit/ab204db) |
| 2026-06-19 | Artikel zur Agentenforschung angereichert; die Anzahl blieb bei 834 | [Commit `a99e8c6`](https://github.com/AnastasiyaW/knowledge-space/commit/a99e8c6) |
| 2026-08-21 | Öffentliches News-Schema 1.3 veröffentlicht, mit Projekthistorien und Domänenverknüpfungen | [Feed-Release `730f7cf`](https://github.com/AnastasiyaW/diffusion-love-news/commit/730f7cf5a47a52e6d0ba75c90dceab15ce6e3b95) |
| 2026-08-21 | Geschütztes Portal hat jeden Feed-Abruf an einen unveränderlichen Snapshot des Produzenten gebunden | [Web-Release `102c15b`](https://github.com/AnastasiyaW/diffusion-love-web/commit/102c15b3e999beff4114e28c0b24b2b8d2d49bd5) |
| 2026-08-28 | 851 Artikel in 26 Domänen; jeder Artikel ist über einen Domänenindex und über die Durchsuchseite erreichbar | [Commit `aad5ff7`](https://github.com/AnastasiyaW/knowledge-space/commit/aad5ff7) |

Dies sind git-gestützte Meilensteine und keine nachträglich rekonstruierte Marketing-Zeitleiste. Ein Commit belegt den Repository-Zustand, den er enthält; allein belegt er keinen späteren Zustand der Live-Website.

## Aktuelle Momentaufnahme der öffentlichen Oberfläche (2026-10-10) {#current-public-surface-snapshot-2026-10-10}

| Grenze | Aktueller, quellengestützter Status | Belegrahmen |
|---|---|---|
| Inhalts-Registry | Die aktuelle Registry in `hooks/stats.py` zählt **1.321 Artikel in 28 Domänen**. Dies ist die Artikelanzahl zur Build-Zeit: Sie schließt Domänen-`index.md`-Dateien aus und darf nicht durch eine Gesamtzahl der Markdown-Dateien ersetzt werden. | Aktuelle Quell-Momentaufnahme; eine künftige Bereitstellung kann eine andere Revision enthalten. |
| Öffentliche Website | [happyin.space](https://happyin.space/) bleibt die konfigurierte öffentliche Auslieferungs-URL. Qualifizierende Pushes auf `master` lösen den strikten Build und die Bereitstellung auf Cloudflare Pages aus; der Workflow unterstützt außerdem den manuellen Start. | Konfiguration und Workflow-Quelle belegen den vorgesehenen Veröffentlichungspfad, nicht eine bestimmte Live-Antwort. |
| Öffentlicher MCP-Server | [`io.github.AnastasiyaW/diffusion-love-knowledge` v0.1.0](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.AnastasiyaW%2Fdiffusion-love-knowledge/versions/0.1.0) ist in der offiziellen MCP Registry aktiv; sein öffentlicher Endpunkt ist [https://diffusion.love/mcp](https://diffusion.love/mcp). Der Registry-Eintrag wurde am `2026-10-10T11:01:27.866718Z` veröffentlicht. | Der Registry-Eintrag belegt die öffentliche Auffindbarkeit und den Status zum Zeitpunkt der Abfrage; das Verhalten des Endpunkts erfordert eine eigene Protokollprüfung. |
| Suche und Arbeit mit Recherchedaten | **Stand der Prüfung am 2026-10-10**: PR [#564](https://github.com/AnastasiyaW/knowledge-space/pull/564) enthielt eine öffentliche Suche und Unterstützung für Recherchedaten je Artikel, die noch nicht bereitgestellt waren. Dies ist eine datierte Beobachtung zur Bereitstellung, kein dauerhafter Status. | PR-Quelle und Bereitstellungsabfrage zum Prüfzeitpunkt; daraus wird kein späterer Bereitstellungsstand abgeleitet. |

Der Meilenstein mit 851 Artikeln und das Release des News-Feed-Schemas 1.3 bleiben datierte historische Aufzeichnungen. Sie werden bewusst nicht umgeschrieben, damit sie zu dieser aktuellen Momentaufnahme passen.

## Separates News-Datenrepository: Abgrenzung {#separate-news-data-repository-boundary}

[`AnastasiyaW/diffusion-love-news`](https://github.com/AnastasiyaW/diffusion-love-news) ist ein separates öffentliches Repository. Am 2026-10-10 zeigte `main` auf [`4f631f2`](https://github.com/AnastasiyaW/diffusion-love-news/commit/4f631f2b0fe8ba4ed105bb19bf0beca523da416a). Die an einen Commit gebundenen [Feed-Metadaten](https://raw.githubusercontent.com/AnastasiyaW/diffusion-love-news/4f631f2b0fe8ba4ed105bb19bf0beca523da416a/news/_meta.json) deklarieren Schema **1.4**, **917 Einträge**, **794 Projekte** und **5 Organisationen**; der Erzeugungszeitstempel lautet `2026-09-12T11:16:33Z`. Das Beobachtungsdatum ist nicht das Erzeugungsdatum und belegt nicht, dass jeder Konsument genau diese Revision ausliefert.

Das frühere Release 1.3 des Schemas unter [`730f7cf`](https://github.com/AnastasiyaW/diffusion-love-news/commit/730f7cf5a47a52e6d0ba75c90dceab15ce6e3b95) hat belegbare Lebenszyklus-Ereignisse und Aussagen, explizite Domänenverweise, deterministische Projektzeitleisten sowie Schema- und Build-Prüfungen hinzugefügt.

[`AnastasiyaW/diffusion-love-web`](https://github.com/AnastasiyaW/diffusion-love-web) ist der separate Konsument. Das Release [`102c15b`](https://github.com/AnastasiyaW/diffusion-love-web/commit/102c15b3e999beff4114e28c0b24b2b8d2d49bd5) validiert Feed-Versionen 1.2 und 1.3, löst den `main`-Branch des Produzenten pro Browser-Bootstrap auf genau einen vollständigen Commit-SHA auf und rendert Projektpässe unter `/project/{family_slug}`. Dieser unveränderliche Commit belegt den Quellcode des Konsumenten; dieser Artikel leitet aus der Quellhistorie keinen aktuellen Bereitstellungs- oder Nutzungsstand ab. Wenn Nachweise einer Live-Bereitstellung nötig sind, ist das [Leser-Portal](https://diffusion.love/) gesondert zu prüfen.

Keine versionierte Datei in `knowledge-space` verarbeitet den JSON-Feed. Der offene Datenvertrag, das News-Portal und diese öffentliche technische Referenz bleiben getrennte Auslieferungsflächen, die über explizite Repository- und Projekt-IDs verknüpft sind.

## Nachweisregeln {#evidence-rules}

- Ein Repository-Commit belegt nur die Änderung, die in diesem Commit sichtbar ist.
- Eine Live-HTTP-Antwort belegt die Verfügbarkeit zum Beobachtungszeitpunkt, nicht ein früheres Änderungsdatum oder dessen Ursache.
- Aussagen, die aus einem separaten Repository übernommen werden, erfordern eine versionierte Quelle und einen expliziten Integrationsnachweis.
- Abgeleitete Beziehungen müssen als `inferred` gekennzeichnet werden; sie sind keine verifizierten Fakten.
- Private Quelltexte und Transkripte von Anbietern gehören nicht in öffentliche Daten.

## Lokale Überprüfung {#local-verification}

Führen Sie die Prüfungen des Repositorys aus dessen Wurzelverzeichnis aus:

```powershell
python hooks/freshness_check.py --ci
python lint.link-check.py --strict
python lint.py
mkdocs build --strict
```

Der Bereitstellungsworkflow ist die maßgebliche Automatisierung für die Veröffentlichung. Ein lokal hinzugefügter Artikel ist keine Live-Seite, solange keine Quellrevision, die ihn enthält, diesen Workflow vollständig durchlaufen hat.

## Fallstricke {#gotchas}

- **Annahme, eine explizite Navigationsdatei sei vorhanden:** In `mkdocs.yml` gibt es keine `nav:`-Liste. **Lösung:** Die Hierarchie unter `docs/` beibehalten und die gerenderte MkDocs-Navigation prüfen.
- **Gleichsetzen eines erfolgreichen Validierungsjobs für Inhalte mit einer Bereitstellung:** Dies sind getrennte Workflows. **Lösung:** Den Cloudflare-Bereitstellungslauf für den betreffenden Commit prüfen.
- **Behandlung der D1-Bindung als Backend für Projekthistorien:** Allein eine Bindungsdeklaration begründet diese API nicht. **Lösung:** Vor der Dokumentation einer API implementierte Handler und Konsumententests verlangen.
- **Annahme, dass ein branchbasiertes CDN atomar aktualisiert wird:** jsDelivr kann nach einer Änderung von `main` weiterhin den vorherigen kompatiblen Feed ausliefern. **Lösung:** Für Release-Nachweise die commit-adressierte Nutzlast über GitHub Raw prüfen und den Konsumenten während der Verbreitung mit beiden unterstützten Schema-Versionen kompatibel halten.
- **Den separaten News-Feed als Integration bezeichnen:** Ein scheinbar kompatibler JSON-Feed ist kein Konsumentenvertrag. **Lösung:** Ein veröffentlichtes Schema, einen eingecheckten Konsumenten und einen durchgängigen Build nachweisen.
- **Die aktuelle Website als historischen Nachweis verwenden:** Live-Inhalte können sich ändern. **Lösung:** Für historische Aussagen den datierten Commit oder Bereitstellungslauf zitieren.

## Siehe auch {#see-also}

- [[news-development-graph]]
- [[news-research-knowledge-lifecycle]]
- [[architecture-documentation]]
- [[data-serialization-formats]]
- [[testing-and-quality]]
- [[devops-cicd]]
