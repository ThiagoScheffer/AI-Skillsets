#!/usr/bin/env python3
"""Validate portable skill frontmatter, descriptions, and package references."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
EXPECTED = {
    'kx-orchestrator', 'kx-experience-audit', 'kx-creative-direction',
    'kx-motion-architecture', 'kx-transition-design', 'kx-morphing-layout',
    'kx-spatial-experiences', 'kx-microinteractions',
    'kx-performance-accessibility', 'kx-visual-qa', 'kx-creative-exploration',
}


def validate(root: Path = ROOT) -> list[str]:
    problems = []
    actual = {p.name for p in (root / 'skills').iterdir() if p.is_dir()}
    for name in sorted(EXPECTED - actual):
        problems.append(f'{name}: missing directory')
    for name in sorted(actual - EXPECTED):
        problems.append(f'{name}: unregistered skill; update expected set if intentional')
    for folder in sorted((root / 'skills').iterdir()):
        if not folder.is_dir():
            continue
        skill = folder / 'SKILL.md'
        if not skill.is_file():
            problems.append(f'{folder.name}: missing SKILL.md')
            continue
        content = skill.read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
        if not match:
            problems.append(f'{folder.name}: missing YAML frontmatter')
            continue
        fields = {}
        for line in match.group(1).splitlines():
            if not line or line.startswith(' '):
                problems.append(f'{folder.name}: unexpected multiline frontmatter')
                continue
            if ':' not in line:
                problems.append(f'{folder.name}: malformed frontmatter line {line!r}')
                continue
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()
        if set(fields) - ALLOWED:
            problems.append(f'{folder.name}: nonportable frontmatter keys {set(fields) - ALLOWED}')
        if fields.get('name') != folder.name:
            problems.append(f'{folder.name}: name mismatch')
        if len(fields.get('description', '')) < 80:
            problems.append(f'{folder.name}: description too vague for discovery')
        if len(content) < 1400:
            problems.append(f'{folder.name}: insufficient instruction content')
        if not (folder / 'references' / 'checklist.md').is_file():
            problems.append(f'{folder.name}: missing local checklist')
    for relative in ['schemas/motion-blueprint.schema.json', 'README.md', 'scripts/install.py',
                     'references/semantic-motion-mapping.md', 'templates/qa-report.md']:
        if not (root / relative).is_file():
            problems.append(f'package: missing {relative}')
    return problems


if __name__ == '__main__':
    failures = validate()
    for f in failures:
        print('ERROR:', f)
    if not failures:
        print(f'PASS: {len(EXPECTED)} standalone skills and core package metadata validated')
    sys.exit(1 if failures else 0)
