#!/usr/bin/env python3
"""Install KX skills into a Codex and/or Claude Code project safely."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ('references', 'adapters', 'recipes', 'schemas', 'templates', 'examples', 'scripts')


def plan(target: Path, platform: str):
    """Pairs of (source, destination) to copy as whole directories."""
    tasks = []
    platforms = ['codex', 'claude'] if platform == 'both' else [platform]
    for platform_name in platforms:
        folder = '.agents/skills' if platform_name == 'codex' else '.claude/skills'
        for skill in sorted((ROOT / 'skills').iterdir()):
            if skill.is_dir():
                tasks.append((skill, target / folder / skill.name))
    # Bundle shared materials so installed skill references can find recipes and schemas.
    for resource in RESOURCES:
        tasks.append((ROOT / resource, target / '.kinetic-experience' / resource))
    return tasks


def install(target: Path, platform: str, *, force: bool = False, dry_run: bool = False):
    tasks = plan(target, platform)
    if not target.is_dir():
        raise ValueError(f'Target directory does not exist: {target}')
    conflicts = [dst for _, dst in tasks if dst.exists()]
    if conflicts and not force:
        raise FileExistsError('Existing paths would be overwritten. Review changes or use --force:\n' +
                              '\n'.join(f'  {p}' for p in conflicts))
    if not dry_run:
        for src, dst in tasks:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                shutil.rmtree(dst)  # Only known KX subdirectories, and --force required.
            shutil.copytree(src, dst)
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=Path, help='Existing application root')
    parser.add_argument('--platform', choices=['codex', 'claude', 'both'], default='both')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', action='store_true', help='Replace installed KX directories after review')
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    try:
        tasks = install(target, args.platform, force=args.force, dry_run=args.dry_run)
    except (ValueError, FileExistsError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    for src, dst in tasks:
        print(f'{"WOULD COPY" if args.dry_run else "COPIED"}: {src.relative_to(ROOT)} → {dst}')
    print(f'{"DRY-RUN" if args.dry_run else "INSTALLED"}: {len(tasks)} directory copies')
    return 0


if __name__ == '__main__':
    sys.exit(main())
