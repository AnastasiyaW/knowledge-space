---
title: Link Building and Backlink Strategy
category: concepts
tags: [seo, backlinks, link-building, anchor-text, link-equity, dofollow, nofollow, donor]
---

# Link Building and Backlink Strategy

Acquiring external links (backlinks) pointing to your site from other websites. Links remain one of the top 3 ranking factors for Google. The approach differs significantly between Google (where links are paramount) and Yandex (where links matter less and text/behavioral factors dominate).

## Key Facts

- A **backlink** = a hyperlink from an external website (donor) to your website (acceptor); search engines treat each backlink as a "vote of confidence"
- Link equity (link juice) flows from the donor page to the acceptor page, increasing its authority and ranking potential
- **dofollow** links pass equity (default); **nofollow** links signal to search engines not to follow or pass equity (Google treats nofollow as a "hint" since 2019)
- Additional link attributes: `rel="sponsored"` for paid links, `rel="ugc"` for user-generated content
- Key link quality metrics: **Domain Rating/Authority** (DR/DA), **page authority**, **topical relevance**, **anchor text diversity**, **link placement** (contextual > footer/sidebar)
- **Anchor text** = the visible clickable text of a link; over-optimized (exact-match keyword) anchors trigger spam filters; natural anchor profile includes brand, URL, generic ("click here"), and partial-match anchors
- Google **Penguin algorithm** penalizes unnatural link patterns (paid links, link farms, PBNs with footprints)
- Yandex **Minusinsk filter** specifically targets paid link abuse; can demote a site 20-50 positions
- See [[search-engine-fundamentals]] for how links fit into the overall ranking algorithm
- See [[seo-promotion-strategy]] for integrating link building into an overall SEO plan

## Patterns

### Link building methods (by budget and risk)

```
FREE / LOW RISK:
- Guest posting on relevant blogs
- Broken link building (find 404s on donors, offer your content)
- Resource page link building (get listed on curated lists)
- HARO / journalist outreach (provide expert quotes)
- Creating linkable assets (tools, calculators, infographics)
- Social profiles and business directories

PAID / MODERATE RISK:
- Crowd marketing (forum posts, Q&A sites with natural links)
- Article placements on niche media sites
- Link exchange with thematically relevant sites (limited)
- Digital PR / press releases with links

HIGH RISK (avoid):
- Private Blog Networks (PBNs) - easy to detect, heavy penalty
- Link farms / automated link schemes
- Sitewide footer/sidebar links from unrelated sites
- Comment spam with keyword anchors
```

### Competitor backlink analysis workflow

```
1. Identify top 5-10 competitors for your primary keywords
2. Pull their backlink profiles:
   - Ahrefs: Site Explorer > Backlinks
   - SEMrush: Backlink Analytics
3. Filter for high-quality donors:
   - DR > 30
   - Relevant topic/niche
   - Real traffic (not a dead site)
4. Identify link gaps: donors linking to competitors but not you
5. Prioritize outreach targets by:
   - Relevance to your content
   - Likelihood of success (already linking to similar content)
   - Authority (DR/DA)
6. Create outreach plan with personalized pitches
```

### Anchor text distribution (safe profile)

```
Brand anchors:        30-40%  ("CompanyName", "companyname.com")
URL anchors:          15-20%  ("https://site.com/page")
Generic anchors:      15-20%  ("click here", "read more", "this site")
Partial-match:        10-15%  ("best running shoes guide")
Exact-match keyword:   5-10%  ("buy running shoes online")
Image links (no text):  5-10% (alt text used as anchor)

WARNING: >20% exact-match anchors = spam signal
```

### Link quality evaluation checklist

```
Donor page assessment:
[ ] Is the donor site topically relevant to your niche?
[ ] Does the donor have real organic traffic? (check in Ahrefs/SEMrush)
[ ] Is the link placed within editorial content (not sidebar/footer)?
[ ] Does the donor page itself have backlinks and authority?
[ ] Is the donor indexed in Google? (site:donor-domain.com)
[ ] No signs of being a link farm (hundreds of outbound links)?
```

## Gotchas

- **Yandex Minusinsk is aggressive** - even a moderate paid link campaign can trigger it; for Yandex-focused SEO, prioritize text optimization over link building
- **Link velocity matters** - acquiring 100 links in one week for a new site looks unnatural; gradual, steady acquisition is safer
- **Link disavow is a last resort** - Google's Disavow Tool tells Google to ignore specific links; only use it if you have a manual penalty or clear toxic link attack
- **Nofollow links still have value** - they don't pass PageRank directly, but links from Wikipedia, Reddit, major media sites drive referral traffic and brand awareness
- **Internal links are free and powerful** - before pursuing external links, optimize internal linking; a well-linked internal page can outrank a poorly-linked one with external backlinks
- **Link relevance > link authority** - a DR-30 link from a highly relevant niche site often outperforms a DR-80 link from an unrelated site

## See Also

- [[seo-promotion-strategy]] - Where link building fits in the overall plan
- [[search-engine-fundamentals]] - How link signals work in ranking algorithms
- [Ahrefs Backlink Checker](https://ahrefs.com/backlink-checker)
- [Google Link Spam Documentation](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)
- [SEMrush Backlink Analytics](https://www.semrush.com/analytics/backlinks/)
- [Moz Link Explorer](https://moz.com/link-explorer)
