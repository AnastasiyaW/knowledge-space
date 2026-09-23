"""
MkDocs hook: tell the template which domains have their own Open Graph image.

main.html used /assets/og-<domain>.png for every page below a domain folder, but only 28
domains have one, so organizations/, projects/ and knowledge-base/ (435+ pages) shipped an
og:image that answered 404 (measured 2026-09-23). The template now uses the domain image
only when it exists and og-image.png otherwise.
"""

from pathlib import Path


def og_domains(docs_dir: Path) -> list[str]:
    """Domains with docs/assets/og-<domain>.png; og-image.png is the site-wide default."""
    return sorted(
        p.stem.removeprefix("og-")
        for p in (docs_dir / "assets").glob("og-*.png")
        if p.stem != "og-image"
    )


def on_config(config, **kwargs):
    config["extra"]["og_domains"] = og_domains(Path(config["docs_dir"]))
    return config
