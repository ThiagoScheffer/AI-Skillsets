#!/usr/bin/env python3
"""Build one upload-ready ZIP per skill (one top-level skill folder per archive)."""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def package_all(output: Path) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    paths = []
    for folder in sorted((ROOT / 'skills').iterdir()):
        if not folder.is_dir():
            continue
        zip_path = output / f'{folder.name}.zip'
        with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for file in folder.rglob('*'):
                if file.is_file():
                    archive.write(file, arcname=file.relative_to(folder.parent).as_posix())
        paths.append(zip_path)
    return paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = package_all(args.out)
    for path in result:
        print(path)
    print(f'Packaged {len(result)} individual skills. Each contains its SKILL.md and local checklist.')
