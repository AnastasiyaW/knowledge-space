# Stats Update Checklist

After adding or removing articles, these places need updating:

## Auto-updated (via stats.js at build time)
- Homepage spans: `ks-total-articles`, `ks-total-domains`, `ks-graph-nodes`, `ks-desc-domains`
- Any element with class `ks-stat-articles` or `ks-stat-domains`

## Manual update required
- `README.md` - "XXX+ articles | YY domains | ZZZZ+ cross-references"
- `README.md` - "across YY domains" in description line
- `docs/index.md` - "across YY domains" (3 places: description, engineer line, snippet text)
- `docs/blog/posts/welcome.md` - "XXX+ dense reference articles" and "across YY domains"
- `AGENTS.md` - "XXX+ articles, YY domains"
- `mkdocs.yml` - site_description "XXX+ curated articles" and comment at bottom
- `mkdocs.yml` - site_description "17 more domains" count
- GitHub repo description: `gh repo edit --description "... XXX+ articles across YY domains ..."`

## Also check after adding NEW domains
- `hooks/stats.py` - DOMAIN_META dict (add new domain)
- `hooks/validate.py` - VALID_DOMAINS set (add new domain)
- `docs/javascripts/graph.js` - links array (add connections for new domain)
- `CONTRIBUTING.md` - domains table
- `.claude/rules/article-rules.md` - domain folders list

## How to get current stats
```bash
# Quick count
find docs/ -name "*.md" -not -name "index.md" -not -path "*/blog/*" -not -path "*/contributing/*" | wc -l
ls -d docs/*/ | grep -v blog | grep -v contributing | grep -v javascripts | grep -v stylesheets | wc -l
```

## When to update
- After article generation batch
- After new domain creation
- After PR merge that adds/removes articles
