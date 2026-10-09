from pathlib import Path
import re

ID_RE = re.compile(r'\b(?:BUS|USR|FR|NFR|AC|ADR|THR|CTRL|TASK|TEST|REL)-\d{3,}\b')

def project_root(arg='.'):
    return Path(arg).resolve()

def collect_ids(root):
    ids = set()
    sdlc = root/'.sdlc'
    if not sdlc.exists():
        return ids
    for p in sdlc.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.md','.yaml','.yml','.json','.txt'}:
            try:
                ids.update(ID_RE.findall(p.read_text(encoding='utf-8')))
            except Exception:
                pass
    return ids
