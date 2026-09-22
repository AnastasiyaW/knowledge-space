"""
MkDocs hook: copy extra static files (robots.txt, llms*.txt) to site root.
MkDocs doesn't serve .txt files from docs/ by default.

Also writes the empty files the anonymous counter in overrides/main.html requests.
Each request is counted by path from the edge request log; no code runs for it.
"""

import shutil
from pathlib import Path

# One file per counter: a visit (new, or returning after N days; "reg-" once a browser
# has been here on 5+ days), a star-button click by placement, and a star-toast impression.
# overrides/main.html builds these names; tests/test_star_cta.py keeps both sides equal.
HELLO_DIR = "ks/hi"
HELLO_EVENTS = (
    "new",
    "ret-1d", "ret-2-7d", "ret-8-30d", "ret-31d-plus",
    "reg-1d", "reg-2-7d", "reg-8-30d", "reg-31d-plus",
    "star-topnav", "star-article", "star-toast",
    "toast-shown",
)


def on_post_build(config, **kwargs):
    """Copy static text files from docs/ to site/ after build."""
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])

    # Files to copy to site root
    extras = [
        "robots.txt",
        "llms.txt",
        "llms-zh.txt",
        "llms-ko.txt",
        "llms-es.txt",
        "llms-de.txt",
        "llms-fr.txt",
        "_headers",
    ]

    copied = 0
    for fname in extras:
        src = docs_dir / fname
        if src.exists():
            shutil.copy2(src, site_dir / fname)
            copied += 1

    print(f"[copy_extras] {copied} static files copied to site root")

    hello = site_dir / HELLO_DIR
    hello.mkdir(parents=True, exist_ok=True)
    for name in HELLO_EVENTS:
        (hello / f"{name}.txt").write_text("1\n", encoding="utf-8")
    print(f"[copy_extras] {len(HELLO_EVENTS)} counter files written to /{HELLO_DIR}/")
