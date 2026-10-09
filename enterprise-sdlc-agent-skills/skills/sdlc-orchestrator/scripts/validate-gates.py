#!/usr/bin/env python3
from pathlib import Path
import sys, re

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
ledger = root/'.sdlc'/'gate-ledger.yaml'
if not ledger.exists():
    print('ERROR: .sdlc/gate-ledger.yaml missing')
    raise SystemExit(1)
text = ledger.read_text(encoding='utf-8')
if re.search(r'approved_by:\s*(ai|agent|codex|claude)\b', text, re.I):
    print('ERROR: AI agent cannot be recorded as human approval authority')
    raise SystemExit(2)
print('Gate ledger basic validation: PASS')
