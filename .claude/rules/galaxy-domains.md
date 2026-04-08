# Galaxy Domains Sync Rule

When new domains are added to `docs/` (new folders with articles), update the 3D galaxy in `docs/javascripts/graph.js`:

## What to update

1. **FALLBACK object** (~line 11-38) — add entry:
   ```javascript
   "domain-slug": { name: "Display Name", articles: N, color: "#hexcolor" },
   ```

2. **LINKS array** (~line 48-68) — add 1-3 connections to related domains:
   ```javascript
   ["Display Name","Related Domain"],
   ```

## Color assignment rules

Each domain gets a unique color. Use these group palettes:
- **data** (data-science, data-engineering, sql, bi): purples/blues `#a07ad0`, `#8878b8`, `#9888c0`, `#70a0b0`
- **code** (python, rust, java, php, nodejs, web-frontend, ios, cpp, go): greens/teals `#50b89a`, `#68b080`, `#58c098`, `#60b8c8`
- **infra** (devops, kafka, linux, security): warm reds/oranges `#c88060`, `#d07870`, `#a08878`, `#b87080`
- **ai** (llm-agents, image-generation, llm-memory, audio-voice): yellows/golds `#c0b060`, `#c8a058`, `#c8b070`, `#a080c0`
- **design** (architecture, algorithms, testing-qa): blues `#7088c8`, `#80a0d0`, `#9090b8`
- **other** (misc, seo, writing): muted `#8898a8`, `#80b868`, `#90b8a0`

Pick a color that doesn't clash with existing neighbors in the same group.

## Link rules

Links create visible connections (neural pulses) between planets. Only add links if there is a real semantic relationship between domains. Not every domain needs links — isolated planets are fine. Don't force connections.

## When to check

After adding a new domain folder to `docs/`, verify:
```bash
# Count domains in stats vs galaxy FALLBACK
python hooks/stats.py
grep -c '"[a-z-]*":' docs/javascripts/graph.js  # should match
```

## Also update

- `docs/knowledge-base/index.md` — add new collapsible admonition with planet icon
- Stats will auto-update via `hooks/stats.py` → `window.KS_STATS`
