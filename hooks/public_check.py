"""
MkDocs hook: check that public-facing files don't leak internal details.
Runs on every build. Fails the build if forbidden internal terms found.
"""

import re
import sys
from pathlib import Path

# Internal terms that should NEVER appear in public files
INTERNAL_PATTERNS = [
    # Infrastructure
    (r'Cloudflare\s+Pages', 'deployment platform'),
    (r'cloudflare', 'deployment platform'),
    (r'wrangler', 'deployment tool'),
    (r'\.claude/', 'agent config path'),
    (r'CLAUDE\.md', 'agent config file'),
    # Deploy details
    (r'push to.*master', 'deploy workflow'),
    (r'auto.deploy', 'deploy workflow'),
    (r'CI/CD pipeline', 'internal infra'),
    # MkDocs internals
    (r'MkDocs Material', 'site engine'),
    (r'mkdocs\.yml', 'site config'),
    (r'overrides/', 'template dir'),
    (r'Jinja2', 'template engine'),
    # Pipeline / source
    (r'skill.generator', 'internal pipeline'),
    (r'compressed.*chunks', 'internal pipeline'),
    (r'incoming.research', 'internal pipeline'),
    (r'COURSES\.md', 'internal file'),
    # Agent internals
    (r'agent.guardrail', 'internal detail'),
    (r'bypassPermissions', 'internal detail'),
    (r'hooks/\w+\.py', 'internal hook'),
    # Server infra
    (r'fal-h200', 'internal server'),
    (r'faln-\d', 'internal server'),
    (r'216\.\d+\.\d+\.\d+', 'internal IP'),
    (r'h200_manager', 'internal script'),
]

# Files to check (public-facing)
PUBLIC_FILES = ['README.md', 'CONTRIBUTING.md', 'AGENTS.md']

# Compile
COMPILED = [(re.compile(p, re.IGNORECASE), desc) for p, desc in INTERNAL_PATTERNS]


def on_pre_build(config, **kwargs):
    """Check public files for internal details."""
    root = Path(config['docs_dir']).parent
    issues = []

    for fname in PUBLIC_FILES:
        fpath = root / fname
        if not fpath.exists():
            continue

        content = fpath.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Skip badge URLs (shields.io etc)
            if 'img.shields.io' in line or 'badge' in line.lower():
                continue
            for pattern, desc in COMPILED:
                if pattern.search(line):
                    issues.append(f"  BLOCK: {fname}:{i} - contains '{desc}' ({pattern.pattern})")

    if issues:
        print(f"[public_check] {len(issues)} internal details found in public files:")
        for issue in issues:
            print(issue)
        print("[public_check] Fix these before pushing to public repo!")
        # Warning only, don't break build
    else:
        print("[public_check] Public files clean - no internal details leaked")
