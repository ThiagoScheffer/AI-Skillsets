#!/usr/bin/env python3
"""Read-only static reconnaissance; never writes to or executes code from target repo."""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path

IGNORED = {'.git', 'node_modules', 'dist', 'build', '.next', '.nuxt', 'coverage',
           '.vercel', '.astro', '.agents', '.claude', '.kinetic-experience'}
ROUTING_PACKAGES = ('react-router', 'next', 'nuxt', 'vue-router', 'astro', '@tanstack/react-router')
MOTION_PACKAGES = ('gsap', '@gsap/react', 'motion', 'framer-motion', 'hyperkinetic', 'three', '@react-three/fiber', 'lenis')


def audit(repo: Path) -> dict:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError(f'Not a directory: {repo}')
    package = {}
    manifest = repo / 'package.json'
    if manifest.is_file():
        package = json.loads(manifest.read_text(encoding='utf-8'))
    all_deps = {**package.get('dependencies', {}), **package.get('devDependencies', {})}
    manifests = [p for p in ['pnpm-lock.yaml', 'package-lock.json', 'yarn.lock', 'bun.lockb', 'bun.lock']
                 if (repo / p).exists()]
    counts: Counter[str] = Counter()
    routes = []
    policies = [p for p in ['AGENTS.md', 'CLAUDE.md', 'README.md'] if (repo / p).is_file()]
    file_count = 0
    max_files = 25000
    # Conservatively inspect extensions and likely route filenames only; no secrets/source contents dumped.
    for dirpath, dirs, files in os.walk(repo, followlinks=False):
        # Prune heavy/vendor/hidden configuration directories *before* descent.
        dirs[:] = [d for d in dirs if d not in IGNORED and not d.startswith('.git')]
        for filename in files:
            path = Path(dirpath) / filename
            if path.is_symlink() or not path.is_file():
                continue
            file_count += 1
            if file_count > max_files:
                break
            counts[path.suffix.lower() or '[no extension]'] += 1
            rel = path.relative_to(repo).as_posix()
            if any(part in rel.lower() for part in ('routes/', 'pages/', 'app/')) and path.suffix in ('.tsx', '.jsx', '.ts', '.js', '.vue', '.astro'):
                routes.append(rel)
        if file_count > max_files:
            break
    return {
        'repo': str(repo),
        'package_name': package.get('name'),
        'package_manager': package.get('packageManager'),
        'lockfiles': manifests,
        'routing_packages': {n: v for n, v in all_deps.items() if n in ROUTING_PACKAGES},
        'motion_packages': {n: v for n, v in all_deps.items() if n in MOTION_PACKAGES},
        'framework_signals': [p for p in ['next.config.js', 'next.config.mjs', 'vite.config.ts', 'astro.config.mjs', 'nuxt.config.ts'] if (repo / p).is_file()],
        'policy_files': policies,
        'source_extensions': dict(counts.most_common(12)),
        'route_candidates': routes[:80],
        'scanned_file_count': min(file_count, max_files),
        'truncated': file_count > max_files,
        'limitations': 'Static filenames/dependency heuristic; not a runtime or security audit. No source files executed.'
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--out', type=Path, help='Optional JSON output path outside or inside repo')
    args = p.parse_args()
    result = audit(args.repo)
    formatted = json.dumps(result, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(formatted + '\n', encoding='utf-8')
        print(f'Wrote heuristic audit to {args.out}')
    else:
        print(formatted)


if __name__ == '__main__':
    main()
