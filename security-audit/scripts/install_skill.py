#!/usr/bin/env python3
"""Install this extracted skill into a Codex user or repository skill directory."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path

IGNORE=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store','_verification_renders')

def main():
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True); g.add_argument('--user',action='store_true'); g.add_argument('--repo')
    ap.add_argument('--force',action='store_true')
    a=ap.parse_args(); src=Path(__file__).resolve().parents[1]
    if a.user: base=Path.home()/'.agents/skills'
    else: base=Path(a.repo).expanduser().resolve()/'.agents/skills'
    dst=base/'security-audit'; base.mkdir(parents=True,exist_ok=True)
    if dst.exists():
        if not a.force: raise SystemExit(f'{dst} exists; rerun with --force to replace')
        shutil.rmtree(dst)
    shutil.copytree(src,dst,ignore=IGNORE)
    print(dst)
if __name__=='__main__': main()
