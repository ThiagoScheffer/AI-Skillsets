#!/usr/bin/env python3
"""Create an integrity manifest and the full KX source-package ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {'__pycache__', '.git', 'node_modules', '.DS_Store'}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def source_files():
    return sorted(p for p in ROOT.rglob('*')
                  if p.is_file() and p.name != 'PACKAGE_MANIFEST.json'
                  and not any(part in SKIP_PARTS for part in p.relative_to(ROOT).parts)
                  and p.suffix != '.pyc')


def build(out: Path):
    files = source_files()
    entries = [{'path': file.relative_to(ROOT).as_posix(), 'bytes': file.stat().st_size,
                'sha256': digest(file.read_bytes())} for file in files]
    manifest = {'package': ROOT.name, 'version': '1.0.0', 'generated_utc': '2026-10-09',
                'file_count_excluding_manifest': len(entries), 'files': entries}
    (ROOT / 'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    out.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(out, 'w', compression=ZIP_DEFLATED, compresslevel=9) as zf:
        for file in files + [ROOT / 'PACKAGE_MANIFEST.json']:
            zf.write(file, arcname=(ROOT.name + '/' + file.relative_to(ROOT).as_posix()))
    return manifest, out


def verify(root: Path):
    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    errors = []
    for entry in manifest['files']:
        file = root / entry['path']
        if not file.is_file() or digest(file.read_bytes()) != entry['sha256']:
            errors.append(entry['path'])
    return errors


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--out', type=Path, required=True)
    args = cli.parse_args()
    m, output = build(args.out)
    print(f'Wrote {output} with {len(m["files"])+1} files')
    print(f'Archive size: {output.stat().st_size} bytes')
    broken = verify(ROOT)
    print('Manifest SHA-256 validation:', 'PASS' if not broken else f'FAIL {broken}')
