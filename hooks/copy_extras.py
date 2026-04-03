"""
MkDocs hook: copy extra static files (robots.txt, llms*.txt) to site root.
MkDocs doesn't serve .txt files from docs/ by default.
"""

import shutil
from pathlib import Path


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
    ]

    copied = 0
    for fname in extras:
        src = docs_dir / fname
        if src.exists():
            shutil.copy2(src, site_dir / fname)
            copied += 1

    print(f"[copy_extras] {copied} static files copied to site root")
