---
title: Link Quality Assessment
category: techniques
tags: [seo-marketing, link-quality, outreach, pbn, drop-domains, donor-evaluation, link-audit]
---

# Link Quality Assessment

Donor quality evaluation criteria, outreach methodology, PBN (Private Blog Network) usage, drop domain strategies, and link audit procedures.

## Outreach

Direct contact with sites to buy/negotiate article placement with a link.

**Pros**: actively pushes queries to TOP; improves whole site through authoritative links; good indexation.

**Cons**: expensive; time-consuming; hard to control; ~20% chance of being scammed.

### Donor Selection Criteria
- Active link growth dynamics in Ahrefs
- Niche-relevant or adjacent + media
- DR >= 20, traffic >= 1000, index >= 100 pages
- No spam niches (adult, pharma) in index
- No labeled "sponsored content" / "advertising" posts
- Has queries from your niche in TOP
- Good design (not 90s style)
- Quality inbound links from content
- No spam words in source code
- Quality content, regular new articles
- Not created solely for selling links

## Dynamic Sitewide Links

One donor places different links to your site from different pages with varying anchors.

### Setup Rules
- 10-20 links to 1 of your pages (from different donor pages)
- Different anchors per query cluster
- 1 link per anchor/query
- ~30% dilution for Google (URL, brand, toponym)
- No duplicate links on 1 donor page
- Don't link from ALL donor pages
- Max 3-4 "neighbor" sites per donor page
- Donor must be authoritative: portals, news sites, regional sites

## PBN (Private Blog Network)

Managed network of sites for boosting main domain.

### When to Use
- Black/gray niches
- High-competition niches
- Point boosts for HF/ultra-HF queries in white niches
- Not profitable in RU market for most niches

### Quality Requirements
- PBN: DR 5, TF 8, CF/TF > 1.8; web archive preferred
- Money site: DR 15, TF 15, CF/TF > 2
- Glue: similar to PBN, slightly lower if highly niche-specific

### Rules
- PBN volume <= 10-30% of total link profile (point boost only)
- Links must organically fit the site
- No PBN on young sites without dilution, especially first 6 months
- Don't buy cheap networks from unverified webmasters

## Drop Domain Strategies

### What Drop Domains Are
Previously existing but abandoned domains with residual value: age, trust, backlinks, query index.

### 301 Redirect / Glue
Redirect from drop domain to your site. Transfers links, age, trust.

**Purpose**: boost entire host with link mass; attach domain age; boost promoted page; increase Google trust.

**Selection criteria**:
- Strong domain with links from hard-to-get sources (.gov, niche sites, competitor sites)
- Highly niche-relevant (or very authoritative adjacent)
- Ideally auction domain (age preserved)
- Domain in index and ranking

### Testing Protocol Before Applying
1. Buy domain
2. Find competitor in TOP 20-30 for your queries
3. Track competitor's positions
4. Apply redirect to competitor (same way you'd apply to yourself)
5. Monitor 2-4 weeks
6. If growth -> redirect to your site
7. If no reaction -> don't use
8. If competitor drops -> remove redirect, discard domain

### Redirect Setup
- Install antibot .htaccess on drop domain (block crawlers initially)
- 301: homepage -> homepage; other pages -> homepage OR by redirect map
- Manually redirect pages with strongest links
- Option: redirect topically relevant drop to relevant category

### Where to Find
- mydrop.io, expired.ru, reg.ru, nic.ru, dropmonitor.ru
- Webarchive parsing via rush-analytics.ru
- Backlink parsing from authoritative sites
- SERP parsing (top 100 for keywords -> extract domains -> check WHOIS)

### Drop Domain Evaluation
1. Verify top 10-15 links still alive (manually)
2. Links point directly (no chains)
3. Dofollow >= 60%
4. Check for Chinese characters (reuse indicator)
5. Check for link explosions
6. Pharma, gambling, essay, retail -> skip
7. Many anchor links -> skip
8. Web archive exists -> good; check topic change history
9. Drop count: >2 resets -> bad
10. Check IKS and query index via Keys.So

## Link Audit

### What to Check
1. Quantity (links, hosts)
2. Spam and SEO anchors (by hosts)
3. Link growth dynamics (especially SEO links)
4. Spam-filled donors actively trading on exchanges
5. Broken sites, Xrumer links, hidden links
6. **Special attention to new links**

### Auto-Detection of Link Spam
1. Export from Ahrefs + GSC: 1 link per domain
2. Check in Screaming Frog (with browser emulation):
   - Custom Search: regex for your domain links
   - Custom Search: spam words (`viagra|payday|porn`)
3. Reject via Google Disavow Links

Alternative: Rush-Analytics PBN section -> "Spam in links"

## Donor Quality Checklist

### Article Links (Yandex + Google)
- IKS >= 50 (check: be1.ru/yandex-iks/)
- Google traffic via Ahrefs >= 5,000
- Price <= 1,000-1,500 RUB
- TF >= 5 (Majestic.com)
- Niche: topic, adjacent, newspapers, media, portals
- Indexation > 1,000 pages (`site:` operator)
- Spam check: `site:site.com "spam words"` - inspect results
- Sort remaining by traffic or IKS; manually review:
  - Site alive, fresh articles posted regularly
  - Not all articles commercial
  - Ahrefs: outbound links don't exceed indexed pages
  - Ahrefs UR of paid articles != 0

### Forum Links
- Google traffic via Ahrefs >= 100
- Indexation > 1,000 pages
- Spam check (same as article links)
- Forum alive with regular fresh topics
- Paid topics should not dominate
- Find forums: `inurl:forum OR inurl:showthread [keyword]`

## Link Exchange Platforms

Marketplaces for buying eternal (one-time) or rental links.

**Rules**:
- Manual donor selection mandatory
- Plan anchors and dynamics based on competitors
- No point buying links > 1,500-2,000 RUB
- Don't follow exchange recommendations
- Don't use "link boosting" (exchange sends bots -> penalty risk)

**Platforms (RU)**: Miralinks, GGL, pr.Sape

## Link Analysis Tools

| Tool | Purpose |
|------|---------|
| Ahrefs | Full backlink database, anchor analysis, dynamics, metrics |
| MegaIndex | Free RU: SEO vs organic link ratio (>40-50% SEO = warning) |
| LinkPad | RU market backlink analysis |
| Majestic | Trust Flow / Citation Flow metrics |

## Gotchas
- **Always test drop domains on a competitor first** - applying untested redirect to your site can tank rankings
- **20% scam rate in outreach** - verify donor quality independently before paying
- **PBN should never exceed 30% of link profile** - use as point boost only
- **Chinese characters in web archive = domain was reused** - usually low quality
- **More than 2 domain drops/resets = toxic** - skip these domains
- **Link exchange recommendations are unreliable** - always select donors manually

## See Also
- [[link-building-strategy]] - Overall link strategy and anchor composition
- [[filters-and-penalties]] - Minusinsk and Penguin penalties from bad links
- [[seo-analytics-reporting]] - Link tracking in monthly reports
- [[seo-tools-workflow]] - Ahrefs and link analysis tools
