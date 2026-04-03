---
title: Link Building Strategy
category: techniques
tags: [seo-marketing, link-building, backlinks, anchor-text, light-links, heavy-links, link-dynamics]
---

# Link Building Strategy

Link types, anchor composition, strategies by site age, and search engine differences. Links are the #1 ranking factor in Google and #3 in Yandex.

## Link Terminology

- **Acceptor** - domain receiving the link
- **Donor** - domain providing the link
- **Donor document** - specific page where link is placed
- **Anchor** - visible text of the link
- **rel attribute** - link attribute (nofollow, sponsored, etc.)

## Why Links Matter

1. **Static weight** - PageRank and derivatives
2. **Dynamic (anchor) weight** - anchor list, monolithic index
3. **BrowseRank** - link click-through data
4. **Robot delivery** - indexation
5. **Geo-binding** - regional signals

## Link Types by Anchor

| Type | Examples |
|------|---------|
| Anchor | "buy television", "rent apartment" |
| Non-anchor | URL, brand name, "here", "source" |
| URL links | Text to the right counts as anchor |
| Sitewide | Footer/header links on all donor pages |
| Nofollow | Google considers at its discretion |
| Redirect links | `/out.php?where=site.ru` (counted by Google) |
| Image links | `alt` attribute goes into anchor list |

## Link Categories

### Light Links
Easy to obtain; site can receive many quickly; mainly nofollow; purpose = dilution + natural dynamics.

**Types**:
1. **Crowd marketing** - forum posts, comments, Q&A
2. **Submits** - self-placement in directories, catalogs, profiles
3. **Press releases** - news/PR distribution to media outlets

### Heavy Links
Hard/expensive to obtain; can't handle many at once; mostly dofollow; purpose = direct ranking push.

**Types**: outreach, PBN, glue/redirect, dynamic sitewide, link exchanges, multi-tier links.

**Important**: If query below TOP-50, heavy links won't push to TOP. First: on-page + internal linking + light links. THEN heavy links.

## Crowd Marketing Best Practices
- Only verified contractors
- Fill brief in maximum detail: platform types, topics
- Require pre-moderation of platforms, topics, and texts
- Reject spam-filled forums: zero DR, dead/broken, adult/pharma contaminated
- Require "survival guarantee" of 2 weeks
- Monitor link presence (LinkChecker.pro)

## Submits Best Practices
- Unique company descriptions (don't reuse site texts)
- No logos/images (only logo allowed)
- Never order automatic mass submissions
- No anchor links from submits
- Smooth growth: 10, 20, 30 per month

## Press Releases
- No anchors
- Test with satellite site first
- Service: pressfeed.ru
- Quick nofollow links from authoritative hosts; helps LF rankings start faster

## Anchor List Composition

### Recommended Ratio
- **70%** - URL variations, company name, brand, images
- **10%** - exact keyword matches
- **20%** - dilution anchors and variations

### Process
1. Analyze competitor anchor lists document-by-document for top-ranking pages
2. Estimate anchor/dilution/non-anchor ratio
3. Build your own anchor list based on findings

### AI-Assisted Anchor List Construction
**Iteration 1**: Submit CSV exports from Ahrefs (competitor links+anchors) and semantic core. Analyze anchor patterns.

**Iteration 2**: Calculate percentage breakdown by type: full URL, URL without protocol, URL with www, brand anchors, image links, exact keyword matches, diluted matches, generic phrases. Exclude irrelevant.

**Iteration 3**: Create 30 anchors for target page following discovered ratios.

## Strategy by Site Age

### New Site (First 3 Months)
- Minimum anchor links
- Light links only (non-anchor and brand): directories, forums, Q&A, press releases, manufacturer/partner links
- Glue/301 from drops: 2-3 max, every 2 months
- After 100 quality donors -> add anchor links
- Quality > Quantity
- Find young competitor that grew quickly -> replicate

### Aged Site with Link History
1. Find competitors of similar site type
2. Research fastest-growing ones in detail
3. Compile plan by types, dynamics, anchors
4. Improve on competitors' strategies
5. Use heavy links
6. Continuously monitor and adjust

## Link Timeline for New Sites
- First 2-3 months: zero link building (focus on technical, content, structure)
- Month 3-6: 2-3 light links per week
- No "jagged dynamics" - consistent growth (6->6->6->8->8->8->10)
- After year 1 with ~100 donors: increase pace per competitor analysis
- Yandex: results in 2-3 months; Google: ~1 year; 1.5-2 years to equalize both

## Search Engine Differences

### Yandex
- Links to documents (internal weight limited)
- Non-commercial hosts required (otherwise Minusinsk penalty)
- Yandex has link classifier: ~94% precision, ~99% coverage
- Links classified as Good (work) or Bad (weight=0)
- Critical mass of bad links -> Minusinsk

### Google
- Can link to homepage or hub pages
- Link growth dynamics important
- Anchor list critically important
- Diverse link types required

## Link Strategy Framework
1. Collect competitors
2. Identify those actively building links
3. Compile baseline: donor domains/pages, project age, growth dynamics, anchor ratio, link types
4. Target average competitor metrics
5. Map onto your project's current state
6. Plan smooth systematic growth over 1-2 years
7. Execute consistently

## Testing Link Effectiveness
- Use test site or weak competitor (TOP-50 for key, page with zero links)
- Place exact LF anchor and assess effect
- Don't place many links at once on live site

## Gotchas
- **Heavy links won't push below-TOP-50 queries** - fix on-page first
- **Yandex knows who buys and sells links** - 95% of links from known exchanges are marked as SEO links
- **Even non-anchor links bought on exchanges can count as SEO links** - "here", "there" from exchanges are detected
- **Jagged dynamics flag manipulation** - smooth consistent growth is critical
- **Avoid using "here/there" as anchors** - exposes your link profile to competitor analysis
- **Don't use anchor links from submits** - submits are for dilution only

## See Also
- [[link-quality-assessment]] - Donor quality, drop domains, PBN
- [[filters-and-penalties]] - Minusinsk and Penguin filter details
- [[seo-strategy-by-site-type]] - Link strategy by site type
- [[internal-linking]] - Internal linking complements external
