---
title: Search Engine Filters and Penalties
category: reference
tags: [seo-marketing, filters, penalties, baden-baden, minusinsk, penguin, panda, ymyl]
---

# Search Engine Filters and Penalties

Complete reference of Yandex and Google filters, their triggers, symptoms, diagnostics, and recovery procedures.

## Traffic Drop Diagnostics

When analytics show traffic drop:
1. Check if page is in index: `url:site.ru/the-dropped-document/`
2. Check validity of saved copy in search engine
3. Check nesting level
4. Analyze drop character:
   - **Host dropped** -> check sanctions
   - **Page dropped** -> check: relevant page change, document sanctions, text issues, link issues

## What Search Engines Penalize For
1. Text quality issues (spam, thin content)
2. User deception on site
3. Behavioral factor manipulation
4. Affiliation: multiple commercial sites from one owner
5. Link manipulation
6. Search engine deception
7. Porn content, intrusive advertising
8. Piracy, content theft

## Where to Check Filter Status
- **Yandex Webmaster** -> "Violations" section
- **Google Search Console** -> "Manual Actions"

### Filter Scope Types
- Query-document, document, domain, page/section removal, domain removal
- By type: automatic or manual

## Yandex Filters

### Baden-Baden
**Date**: March 2017 | **Type**: automatic | **Scope**: query-document and domain

**Triggers**: keyword density spam, excessive text volume, hidden text, low text quality.

**Symptoms**:
- Query-level: sharp drop of a query group (not all) by 5-40 positions; document still ranks for other queries
- Host-level: sharp drop of ALL queries by 20+ positions; only branded queries remain; Webmaster notification

**Diagnosis**: `arsenkin.ru/tools/filter/`; mass drop of 10+ positions = likely Baden-Baden.

**Removal**:
- Query-level: first add `<noindex>` tag, then rewrite; reduce keyword occurrences and text volume; if nothing works -> delete text
- Host-level: **ONLY DELETE TEXT** - nothing else works

### Minusinsk
**Date**: May 2015 | **Type**: automatic | **Scope**: domain

**Triggers**: link manipulation to promote site.

**What counts as SEO links**: almost all anchor links to commercial site; 95% of links from known exchanges; even non-anchor links from exchanges.

**Removal**:
1. Remove ALL SEO links at once
2. Wait for donor page re-indexation
3. Filter lifts in 1-8 months
4. Traffic fully restores if site is high quality
5. Yandex support can show examples of detected links

### Behavioral Factor Manipulation
**Date**: July 2011 | **Scope**: domain | **Type**: manual or automatic

**Symptoms**:
- Automatic: -30-40 positions across whole site except brand (no notification)
- Manual: notification in Webmaster -> Diagnostics -> Security and Violations

**Characteristics**:
- Harshest sanctions in Yandex
- Ban lifted 6-8 months AFTER admitting manipulation
- **Quick exit**: 301 redirect to another domain
- **Never give Webmaster/Metrika access to third parties**

### Clickjacking
**Date**: December 2015 | **Scope**: domain | **Type**: automatic

**Trigger**: invisible elements collecting user data without consent.

**Removal**: stop using exploiting services; click "I fixed everything" in Webmaster; lifts within 30 days.

### Reputation Filter
**Date**: October 2021 | **Scope**: domain | **Type**: automatic

**Trigger**: negative reviews, scam phone calls via SIP telephony. Drop of 15-30 positions.

### Affiliate Filter
**Type**: manual

**Trigger**: 2+ commercial sites from one company for identical products/services.

**How to avoid with multiple sites**:
- Different hosting/registrars
- Register under different person
- Different assortment and prices
- Different product naming conventions
- Webmaster/Metrika on different accounts (different computer or VM)
- Different contacts
- Advertising from different accounts

### Other Yandex Filters
- **Intrusive Subscription Notifications** (Jan 2019)
- **Aggressive Advertising** (Apr 2019) - mainly Adsense monetization; ad blocks disguised as navigation

## Google Filters

### Google Panda
**Date**: February 2011 | **Scope**: document and domain | **Type**: automatic

**Triggers**: low quality content, stolen/duplicate content, internal duplication.

**Recovery**: find non-traffic pages via GSC/GA; rewrite (remove copy-paste, spam); add quality content, images, video; add moderated UGC.

### Google Fred
**Date**: March 2017 | **Scope**: domain | **Type**: automatic

**Triggers**: low content quality, low quality links, excessive advertising, no added value.

**Recovery**: reduce ad blocks; improve link profile; add value-added services (calculators, tests).

### YMYL (Your Money or Your Life)
**Date**: August 2018 | **Scope**: domain | **Type**: automatic

**YMYL niches**: finance, medical, legal, child safety, driving safety.

**Recovery via E-A-T**: certificates, proof/evidence, authoritative links, content quality, grammar, assortment, purchase/delivery info.

### Google Penguin
**Date**: April 2012 | **Scope**: query-document | **Type**: automatic

**Triggers**:
- Large number of commercial anchors
- Unnatural anchor distribution (no branded anchors)
- Links only to homepage or small set of pages
- High share of purchased/low quality links

**Recovery**:
- Remove bad links, change link profile
- Distribute links across host
- Increase non-anchor share to >20%
- Dilute anchor spam with non-anchor links
- Close bad links in Google Disavow Links

### Micromarkup Spam
**Date**: 2016 | **Scope**: document | **Type**: automatic

**Trigger**: micromarkup abuse to manipulate snippets. Check all types, remove inappropriate markup.

### DMCA (Piracy)
**Date**: 2012 | **Scope**: document

**Trigger**: copying content from other sites. Delete non-unique content, request filter removal.

### Exact Match Domain (EMD)
**Date**: 2012 | **Scope**: domain | **Type**: automatic

**Trigger**: commercial keyword phrase in domain name. Fix: change domain with 301 redirect. Prevention: don't use more than one keyword in domain.

## Filter Reference Table

| Filter | Engine | Scope | Type | Key Trigger |
|--------|--------|-------|------|-------------|
| Baden-Baden | Yandex | Query-doc/domain | Auto | Text spam |
| Minusinsk | Yandex | Domain | Auto | Link manipulation |
| Clickjacking | Yandex | Domain | Auto | Invisible data collection |
| Behavioral | Yandex | Domain | Manual/Auto | Bot/paid clicks |
| Reputation | Yandex | Domain | Auto | Negative reviews/scam |
| Affiliate | Yandex | Domain | Manual | Multiple sites same niche |
| Panda | Google | Doc/domain | Auto | Low quality/duplicate |
| Fred | Google | Domain | Auto | Low quality + excessive ads |
| YMYL | Google | Domain | Auto | E-A-T deficiency |
| Penguin | Google | Query-doc | Auto | Link spam |
| Micromarkup | Google | Document | Auto | Markup manipulation |
| DMCA | Google | Document | - | Copyright violation |
| EMD | Google | Domain | Auto | Keyword domain |

## Gotchas
- **Baden-Baden host-level: ONLY delete text** - rewriting doesn't work, only complete removal
- **Minusinsk calculates by hosts, not pages** - one bad link per domain counts the same as 100
- **Behavioral manipulation is the harshest penalty** - 6-8 month ban with no workaround except domain change
- **Affiliate filter requires extreme separation** - even analytics on the same account can trigger detection
- **Penguin is query-document scope** - individual pages can recover while others stay penalized
- **EMD still matters** - avoid putting more than one commercial keyword in domain name

## See Also
- [[link-building-strategy]] - Link strategies that avoid penalties
- [[text-optimization]] - Text optimization within safe limits
- [[behavioral-factors-ctr]] - Behavioral factor best practices
- [[commercial-ranking-factors]] - E-A-T for YMYL recovery
