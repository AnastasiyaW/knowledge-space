# Stats Update Checklist

After adding or removing articles, these places need updating:

## Auto-updated (via stats.js at build time)
- Homepage spans: `ks-total-articles`, `ks-total-domains`, `ks-graph-nodes`, `ks-desc-domains`
- Any element with class `ks-stat-articles` or `ks-stat-domains`

## Manual update required
- `README.md` line with "XXX articles | YY domains | ZZZZ+ cross-references"
- `docs/blog/posts/welcome.md` mention of "600+ dense reference articles"
- `docs/index.md` snippet text with "600+ articles across 23 domains"
- GitHub repo description (via `gh repo edit --description "... XXX+ articles across YY domains ..."`)
- `mkdocs.yml` site_description (for OG meta tags and Telegram previews)

## How to get current stats
```bash
# From stats.js (generated at build)
python hooks/stats.py  # prints counts

# Quick count
find docs/ -name "*.md" -not -name "index.md" -not -path "*/blog/*" | wc -l
ls -d docs/*/ | wc -l  # domains
```

## When to update
- After article generation batch
- After new domain creation
- After PR merge that adds/removes articles
