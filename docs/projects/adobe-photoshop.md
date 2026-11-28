---
title: "Photoshop — Product updates"
category: "projects"
date: 2026-11-27
tags: ["adobe-photoshop", "product-updates", "product_updates", "project"]
aliases: ["Photoshop"]
---

# Photoshop — Product updates

Photoshop records AI use and edits as C2PA Content Credentials in image metadata; this page tracks its product updates for photographers.

**Development line:** project:adobe-photoshop · thread product-updates  
**Last event:** 2026-11-27 · 1 dated since 2026-11-27 · **Researched:** 2026-11-28 · confidence: medium

## What it is

Adobe Photoshop AI Content Credentials and policy is a provenance-tracking setup. It records edits and generative tool use in image metadata under the C2PA standard. It logs Firefly and AI tool operations automatically, signs an editing manifest cryptographically and embeds tamper-evident metadata.

The main limit: generative AI tags cannot be removed or disabled by hand once an underlying utility triggers them. Documentary photographers should avoid automated tools, so they do not trigger compliance flags by accident.

## Development line

- **2026-11-27 — New York Times Cautions Photographers Against Updated Adobe Photoshop Over AI Metadata Tagging.** The New York Times has asked freelance photographers not to use the latest version of Adobe Photoshop. Some AI features work in ways users cannot easily see, and they may add AI-use tags to photo metadata.
  - The guidance restricts Adobe Photoshop version twenty-eight (Photoshop 2027) and later builds. It follows an internal memo from photo department leaders Meaghan Looram and Josh Haner. The memo cites two concerns: AI that runs in the background without being obvious, and mandatory C2PA Content Credentials metadata. (2026-11-27) — <https://habr.com/ru/articles/1113002/>

## What changed

Adobe added Content Credentials to Photoshop to record image provenance and generative edits automatically under the C2PA standard. Later releases built machine-learning utilities into ordinary editing tools. As a result, routine retouching can trigger permanent AI metadata. Editorial organizations now restrict recent software versions, so news photographs are not tagged as AI-made by mistake.

## How to use this

1. Check the installed Photoshop version to see whether it adds AI Content Credentials in the background.
  — <https://habr.com/ru/articles/1113002/>
2. Do not use automated retouching or guided cleanup tools, since they trigger permanent generative AI metadata tags.
  — <https://habr.com/ru/articles/1113002/>
3. Process assignment photographs in older versions or in other software that does not write AI metadata to image headers.
  — <https://habr.com/ru/articles/1113002/>

## Best practices

- Keep the unaltered camera RAW masters next to the exported files, so authenticity can be shown in an editorial compliance review.
  — <https://habr.com/ru/articles/1113002/>
- Limit post-processing to manual global exposure, contrast and color corrections, and skip automated cleanup tools.
  — <https://habr.com/ru/articles/1113002/>

## Superseded by this

- Standard retouching and dust-cleanup tools in updated Photoshop releases can be used on news assignment photos without risking automated AI flags.
  — <https://habr.com/ru/articles/1113002/>

## Still unknown

- Secondary reports (Unite.ai, DPReview, Cut.pro and Reddit) gave only opaque redirect links, not direct URLs, so they are not listed as sources.
- Whether Adobe will add settings that let photographers switch off background AI processing in standard retouching tools, without applying Content Credentials, is unconfirmed.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/articles/1113002/ | New York Times Cautions Photographers Against Updated Adobe Photoshop Over AI Metadata Tagging | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:adobe-photoshop, thread product-updates, 1 dated events 2026-11-27 → 2026-11-27.
- **Practical note:** See the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
