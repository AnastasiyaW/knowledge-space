---
title: SEO Tools and Daily Workflow
category: reference
tags: [seo, tools, screaming-frog, ahrefs, semrush, browser-extensions, workflow, audit-tools]
---

# SEO Tools and Daily Workflow

The essential toolkit and daily workflow patterns for SEO specialists. Covers browser extensions, desktop applications, SaaS platforms, and how they integrate into routine SEO tasks.

## Key Facts

- Minimum SEO toolkit: **browser extensions** (SEO Meta in 1 Click, Web Developer, Lighthouse), **crawler** (Screaming Frog), **analytics** (GA4 + Yandex Metrica), **webmaster tools** (GSC + Yandex Webmaster), **keyword tool** (Wordstat + Keyword Planner), **position tracker** (Rush Analytics / SE Ranking)
- **Screaming Frog SEO Spider** = desktop crawler for technical audits; crawls up to 500 URLs free; essential for finding broken links, duplicate content, missing meta tags, redirect chains
- **Ahrefs** = SaaS platform for backlink analysis, keyword research, competitor analysis, rank tracking, content exploration; strongest backlink database
- **SEMrush** = similar to Ahrefs with additional focus on advertising, social media, and content marketing; better for PPC integration
- **Keys.so / SpyWords** = Russian-market SEO intelligence tools for competitor keyword and ad analysis
- **Rush Analytics** = position tracking and analytics tool used by Rush Agency; provides rank tracking, keyword grouping, search volume data
- Browser-based inspection: right-click > Inspect Element > check `<title>`, `<h1>`, `<meta>` tags, Schema markup, canonical, robots directives
- See [[seo-analytics-tools]] for detailed analytics platform guides
- See [[technical-seo-audit]] for how tools fit into audit workflow

## Patterns

### Browser extensions for SEO

```
MUST-HAVE:
- SEO Meta in 1 Click: instant view of title, description, h1-h6,
  canonical, robots, Open Graph, structured data
- Web Developer Toolbar: disable CSS/JS, view page source,
  outline headings, check forms
- Lighthouse (built into Chrome DevTools): performance audit,
  accessibility, SEO score, Core Web Vitals

USEFUL:
- Redirect Path: shows redirect chains (301/302/307)
- Link Redirect Trace: detailed redirect and header analysis
- SimilarWeb: quick traffic estimates for any site
- Check My Links: highlights broken links on page
- Wappalyzer: identifies technologies used by a website
```

### Daily SEO workflow

```
MORNING CHECK (15 min):
1. GSC: check for new indexing errors or coverage drops
2. Position tracker: review significant rank changes
3. Yandex Webmaster: check for new warnings or errors
4. Analytics: check organic traffic vs previous period

WEEKLY TASKS:
- Review search query performance in GSC (new queries, CTR drops)
- Check competitor position changes
- Content performance review (traffic to published content)
- Internal linking opportunities for new content
- Backlink monitoring (new links acquired, lost links)

MONTHLY TASKS:
- Mini technical audit (Screaming Frog crawl, check for new issues)
- Content plan review and adjustment
- Link building pipeline review
- Client/stakeholder reporting
- Strategy review against KPIs

QUARTERLY:
- Full technical audit
- Semantic core expansion
- Strategy pivot if needed based on performance data
- Competitor landscape re-analysis
```

### Screaming Frog workflow

```
QUICK AUDIT (30 min):
1. Configuration:
   - Set crawler to respect robots.txt
   - Set user agent to Googlebot
   - Enable JavaScript rendering (if site uses it)
   - Set crawl limit appropriate to site size

2. Crawl and review tabs:
   Response Codes -> filter 4xx, 5xx errors
   Page Titles   -> filter missing, duplicate, over 60 chars
   Meta Desc     -> filter missing, duplicate, over 160 chars
   H1            -> filter missing, duplicate, multiple per page
   Canonicals    -> filter missing, non-self-referencing
   Directives    -> find noindex/nofollow pages (intentional?)
   Images        -> filter missing alt text, oversized images

3. Export findings to spreadsheet
4. Prioritize: critical (blocking indexing) > major > minor
5. Create task list with specific fix instructions
```

### Tool cost comparison (approximate)

```
| Tool              | Free Tier        | Paid Start     | Best For          |
|-------------------|------------------|----------------|-------------------|
| Screaming Frog    | 500 URLs         | $259/year      | Technical audits  |
| Ahrefs            | Limited free      | $99/month      | Backlink analysis |
| SEMrush           | 10 queries/day   | $130/month     | All-in-one SEO    |
| Rush Analytics    | Trial            | ~$30/month     | RU market tracking|
| Keys.so           | Limited          | ~$20/month     | RU competitor data|
| SE Ranking        | Trial            | $44/month      | Position tracking |
| Google tools      | Fully free       | -              | Core analytics    |
| Yandex tools      | Fully free       | -              | Yandex analytics  |
```

## Gotchas

- **Free Screaming Frog is limited to 500 URLs** - sufficient for small sites but enterprise sites need the paid license; if budget is tight, crawl the most important sections separately
- **Ahrefs and SEMrush data differs** - each has its own crawler and index; neither has complete data; cross-reference both for important decisions
- **Browser extension data can be inaccurate** - tools like SimilarWeb show estimates, not real numbers; never quote these to clients as facts
- **Tool overload is real** - beginners often spend more time learning tools than doing SEO; master the free Google/Yandex tools first, add paid tools as specific needs arise
- **Automated audit scores are misleading** - a 95/100 Lighthouse score doesn't mean SEO is perfect; many critical issues (keyword targeting, content quality, link profile) aren't measured by automated tools
- **Position data from rank trackers differs from GSC** - rank trackers check from specific locations, GSC shows actual impression data; both are useful, neither is "the real position"

## See Also

- [[seo-analytics-tools]] - Deep dive into analytics platforms
- [[technical-seo-audit]] - Full audit methodology using these tools
- [Screaming Frog User Guide](https://www.screamingfrog.co.uk/seo-spider/user-guide/)
- [Ahrefs Academy](https://ahrefs.com/academy)
- [SEMrush Academy](https://www.semrush.com/academy/)
- [Google Search Console Help](https://support.google.com/webmasters/)
