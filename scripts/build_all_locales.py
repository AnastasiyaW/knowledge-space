"""Build the canonical English site and complete reviewed language branches.

Each locale is a separate MkDocs project, as Material supports one canonical
document language per configuration. We deliberately do not fall back to an
English article under a localized URL: a missing translation stays absent until
there is reviewed content for it.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIGS = ("mkdocs.yml", "mkdocs.ru.yml", "mkdocs.zh-CN.yml")
REQUIRED_OUTPUTS = (
    "index.html",
    "ru/index.html",
    "ru/start-here/index.html",
    "ru/privacy/index.html",
    "zh-CN/index.html",
    "zh-CN/start-here/index.html",
    "zh-CN/privacy/index.html",
)


def main() -> int:
    environment = os.environ.copy()
    environment.setdefault("DISABLE_MKDOCS_2_WARNING", "true")

    for config in CONFIGS:
        subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", config],
            cwd=ROOT,
            env=environment,
            check=True,
        )

    missing = [path for path in REQUIRED_OUTPUTS if not (ROOT / "site" / path).is_file()]
    if missing:
        raise RuntimeError(f"Localized build did not produce: {', '.join(missing)}")

    print("PASS localized build: en, ru, zh-CN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
