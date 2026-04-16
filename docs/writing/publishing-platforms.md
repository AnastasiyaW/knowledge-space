---
title: Publishing Platforms for Technical Content
category: tools
tags: [writing, publishing, platforms, seo, marketing]
---

# Publishing Platforms for Technical Content

Where to publish technical articles, with audience profiles, formatting requirements, and cross-posting strategy. Platform choice depends on audience (developers vs data scientists vs general tech), language (EN/RU), and goal (SEO ownership vs reach vs community).

## Platform Comparison

| Platform | Audience | Language | Best for | SEO ownership |
|----------|----------|----------|----------|--------------|
| Personal blog (Hashnode/Hugo) | Your audience | Any | Canonical home, full control | Full |
| Habr | RU developers, senior-heavy | RU | Deep technical, investigations, OSS | Partial |
| Dev.to | EN developers, junior-mid | EN | Tutorials, cross-posts | Partial (canonical) |
| Medium / Towards Data Science | EN, data science, ML | EN | AI/ML content, broad reach | None (paywall) |
| HackerNoon | EN developers | EN | Editorial reach, long-form | Partial |
| Hacker News (Show HN) | EN, senior/startup | EN | OSS launches, highest single-channel impact | N/A (link) |
| Reddit | Varies by subreddit | EN | Niche audiences, hands-on feedback | N/A (link) |

## Habr (Russian)

**Audience**: experienced RU-speaking developers. Senior-heavy. Low tolerance for shallow content.

**What works:**
- Pet projects with technical depth ("I built X, here's how")
- Investigations and reverse engineering
- Explaining complex topics simply (but with depth)
- Contrarian takes with evidence
- Real metrics and before/after comparisons

**What fails:**
- Product announcements disguised as articles (treated as advertising)
- Surface-level overviews without personal experience
- AI-generated text (explicitly against rules, community detects it quickly)
- Content aimed at beginners without novel angle

**Formatting:** WYSIWYG + Habr Flavored Markdown. H1/H2/H3, code blocks with syntax highlighting (30+ languages), spoilers, tables. KPVD (lead image) is critical for CTR - must be bright, relevant, not a logo.

**Karma system:** Community moderation. New accounts start limited. Negative karma restricts commenting. Building karma requires genuine contributions before publishing in competitive hubs.

**Key stats for first articles:**
- Average rating: +12
- Average views: 6,716
- Average comments: 20
- Only 18% of authors write a second article

**Optimal length:** 1500-2000 words (7-10 minute read). Habr counts reading speed at 1500 chars/min.

**Karma privilege thresholds:**

| Karma | Unlocks |
|-------|---------|
| 0+ | Post to non-primary hubs |
| 1+ | Vote on articles and comments |
| 2+ | Vote on others' karma |
| 5+ | Full voting access |
| 30+ | Post in "Я пиарюсь" hub |
| 50+ | Invite new users |
| -1 to -5 | 1 comment per 5 minutes |
| -6 to -10 | 1 comment per hour |
| -31 or less | Read-only |

**Vote weight:** Regular user = +1; Author/Senior/Star = +2; Legend = +3 per vote on articles.

**Google Discover:** First-hour momentum (1000+ views) triggers trending placement. Discover is a major secondary traffic source for well-performing articles. 0.3-1.2% of article viewers subscribe to the author's Telegram channel.

## Hacker News

**Best for:** OSS project launches, technical articles with novelty.

**Format:** "Show HN: [name] - [one-line description]" for project launches.

**Timing:** Tuesday-Thursday, 8-10 AM ET.

**Rules:**
- Respond to every comment (engagement drives ranking)
- No hype language - understated and technical wins
- The article/project must stand on technical merit
- Repeat submissions are OK if the first didn't get traction

**Risk:** HN commenters will find every flaw. Ship something solid before posting.

## Dev.to

**Audience:** EN developers, skews junior-to-mid. Friendly community.

**Best for:** Cross-posting (supports canonical URL), tutorials, getting indexed.

**Formatting:** Markdown. Supports cover images, series, tags. Liquid tags for embeds.

**SEO:** Supports `canonical_url` in frontmatter - use this when cross-posting from your own blog to avoid duplicate content penalties.

## Medium / Towards Data Science / Towards AI

**Audience:** Broad tech audience for Medium, data science/ML for TDS/TAI.

**Best for:** AI/ML articles targeting data science audience.

**Drawbacks:**
- Paywall reduces reach for non-subscribers
- No canonical URL support - Google may rank Medium over your blog
- Editing experience is clean but limited for technical content
- Platform owns the distribution

**Strategy:** Publish on your own blog first, then submit to TDS/TAI publications. They accept external submissions with editorial review.

## Personal Blog

**Options:**
- **Hashnode**: developer-focused, custom domain, canonical URL handling, built-in newsletter
- **Hugo/Jekyll + GitHub Pages**: full control, free hosting, requires setup
- **Astro/Next.js**: maximum flexibility, more maintenance

**Why bother:** Own your SEO. Cross-posted content on dev.to/Medium can outrank your original. A personal blog with a custom domain builds cumulative authority.

## Cross-Posting Strategy

```bash
1. Publish on personal blog (canonical URL)
2. Cross-post to dev.to (with canonical_url in frontmatter)
3. Submit to HackerNoon (with canonical link)
4. Submit to TDS/TAI if ML-focused (accept editorial changes)
5. Post link on HN / Reddit after publication
6. For RU audience: write separate Habr version (not a translation - adapt for the audience)
```

**Key rule:** Canonical URL always points to your own domain. Every cross-post includes the canonical link. This prevents SEO cannibalization.

## Reddit Subreddits for Technical Content

| Subreddit | Audience | Notes |
|-----------|----------|-------|
| r/MachineLearning | ML researchers/practitioners | Strict quality standards, paper discussion |
| r/LocalLLaMA | Local inference, quantization | Hands-on audience, practical focus |
| r/programming | General programming | High traffic, competitive |
| r/ExperiencedDevs | Senior engineers | Career + technical depth |
| r/devops | DevOps/SRE | Infrastructure, tooling |
| r/selfhosted | Self-hosting | OSS tools, home lab |

**Reddit etiquette:** Don't just drop links. Provide a text summary in the post or comments. Engage with discussion. Subreddit-specific rules vary.

## Article Format for Maximum Engagement

Across all platforms, highest-performing articles follow:
- **1200-2000 words** (7-10 minute read)
- **Hook -> Problem -> Solution -> Results -> CTA** structure
- **Diagrams/images every 300-500 words** (breaks up text, increases time on page)
- **Code examples** within the first third of the article
- **Specific, non-clickbait title** that states what the reader will learn

## Gotchas

- **Issue:** Cross-posting the same article to multiple platforms without canonical URLs causes Google to pick one version as canonical - often not yours. **Fix:** Always publish on your domain first, wait 24-48 hours for indexing, then cross-post with canonical_url pointing to your domain.
- **Issue:** Writing one article and translating it for both EN and RU audiences produces content that feels unnatural in both languages. **Fix:** Write separate versions. RU and EN technical audiences have different cultural expectations, humor styles, and reference points. Habr readers expect more depth and personality than dev.to readers.
- **Issue:** Posting to HN/Reddit without being prepared to respond to comments for the first 2-3 hours wastes the launch. **Fix:** Post when you can actively engage. The first hour of comments determines whether the post gets traction.

## See Also

- [[technical-article-structure]]
- [[seo-for-articles]]
- [[natural-writing-style]]
- [[editing-checklist]]
