---
title: SEO Content Strategy
category: concepts
tags: [seo, content, seo-text, content-plan, copywriting, e-e-a-t, content-types]
---

# SEO Content Strategy

Planning and creating content that ranks in search engines and satisfies user intent. Goes beyond individual page optimization to encompass the entire content lifecycle: planning, creation, optimization, updating, and pruning.

## Key Facts

- **SEO text** = the primary text content on a page that influences its ranking in search engines; not just keyword-stuffed filler but substantive content that answers user queries
- Content types by site type: **e-commerce** (category descriptions, product descriptions, buying guides), **service sites** (service descriptions, case studies, FAQ), **info sites** (articles, guides, tutorials)
- Content quality spectrum: no text < copy-pasted < template/generated < manually written generic < expert content with original data
- Google's **Helpful Content System** evaluates site-wide content quality; sites with substantial unhelpful content get demoted across all pages
- **E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness): Google expects content creators to demonstrate real experience and expertise, especially for YMYL (Your Money Your Life) topics
- Content freshness matters for time-sensitive queries; updating published date without meaningful content changes is a spam signal
- Typical content production workflow: keyword cluster -> competitor SERP analysis -> outline -> draft -> SEO optimization -> publish -> track -> update
- See [[on-page-optimization]] for optimizing individual content pieces
- See [[ai-for-seo]] for using AI tools in content production

## Patterns

### Content plan template

```
For each planned content piece:
| Field          | Example                                   |
|----------------|-------------------------------------------|
| Target cluster | "how to choose running shoes"              |
| URL            | /blog/how-to-choose-running-shoes/         |
| Content type   | Long-form guide                            |
| Target queries | 15 queries from cluster                    |
| Word count     | 2500 (based on top-5 competitor average)   |
| Search volume  | 12,000/month (cluster total)               |
| Competition    | Medium (DR 30-50 in top-10)                |
| Priority       | High (commercial intent, good volume)      |
| Deadline       | Week 3 of content sprint                   |
| Status         | Draft / Review / Published / Updated       |
```

### Content quality criteria

```
TECHNICAL QUALITY:
- Primary keyword in Title, H1, first 100 words
- LSI keywords distributed naturally throughout
- H2-H3 structure covers all subtopics from cluster
- Images with descriptive alt text
- Internal links to related pages (2-5 per 1000 words)
- External links to authoritative sources (1-3 per article)

CONTENT QUALITY:
- Answers the primary user intent completely
- Covers subtopics that top-ranking competitors cover
- Includes original data, examples, or expert opinion
- Uses tables, lists, images to improve scannability
- No filler paragraphs or obvious AI-generated padding
- Author attribution with expertise credentials (E-E-A-T)

ENGAGEMENT QUALITY:
- Clear structure with descriptive headings
- Actionable advice (not just theory)
- FAQ section addressing related questions
- Call-to-action appropriate to user intent
```

### Content types for SEO by funnel stage

```
TOP OF FUNNEL (informational):
  "What is..." articles
  "How to..." guides
  Listicles ("10 best...")
  Glossaries and definitions
  -> Goal: attract traffic, build authority

MIDDLE OF FUNNEL (commercial):
  Comparison articles ("X vs Y")
  Reviews and ratings
  Best-of roundups
  Case studies
  -> Goal: build trust, guide decision

BOTTOM OF FUNNEL (transactional):
  Product/service pages
  Pricing pages
  Landing pages
  FAQ pages
  -> Goal: convert visitor to customer
```

### Content refresh workflow

```
1. Identify underperforming content:
   - GSC: pages with high impressions but low CTR
   - GSC: pages that dropped from page 1 to page 2+
   - Analytics: pages with declining organic traffic

2. Analyze why:
   - Competitor content is newer/better
   - Information is outdated
   - Missing subtopics that competitors cover
   - Poor engagement metrics (high bounce rate)

3. Update:
   - Refresh statistics, examples, links
   - Add missing sections based on current SERP
   - Improve meta tags if CTR is the issue
   - Add visuals (images, tables, infographics)
   - Update published date ONLY if content meaningfully changed

4. Track:
   - Monitor position changes for 4-6 weeks post-update
   - If improved -> schedule next refresh in 6-12 months
   - If not improved -> deeper analysis needed
```

## Gotchas

- **AI-generated content is not automatically penalized** - Google penalizes low-quality content regardless of how it's produced; AI content that provides genuine value and demonstrates expertise can rank well
- **Word count targeting is misleading** - writing 5000 words when competitors rank with 1500 doesn't help; match depth and completeness, not word count
- **Duplicate content across your own site** is more common than you think - similar service pages, city-specific pages with identical content, product variants with copied descriptions
- **Publishing frequency matters less than quality** - 2 excellent articles/month outperform 20 thin articles; Google's Helpful Content System demotes sites with high volumes of unhelpful content
- **Content pruning** (removing or noindexing low-quality pages) can improve site-wide rankings by raising average content quality signals

## See Also

- [[on-page-optimization]] - Technical optimization of content elements
- [[ai-for-seo]] - AI tools for content creation and optimization
- [[keyword-research-semantic-core]] - Research that drives content planning
- [Google Helpful Content Documentation](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google E-E-A-T Guidelines](https://developers.google.com/search/docs/fundamentals/creating-helpful-content#get-to-know-the-quality-rater-guidelines)
- [Ahrefs Content Strategy Guide](https://ahrefs.com/blog/content-strategy/)
