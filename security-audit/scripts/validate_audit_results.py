#!/usr/bin/env python3
"""Validate audit-results.json invariants without third-party packages."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

SEV={'Critical','High','Medium','Low','Informational'}
CAT={'tenant-isolation','authorization','idor-bola','secrets','xss'}
TOKEN_PATTERNS=[
 re.compile(r'sb_secret_[A-Za-z0-9_-]{16,}'),
 re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 re.compile(r'\bsk_(?:live|test|proj)_[A-Za-z0-9_-]{16,}',re.I),
]

MOJIBAKE_TOKENS=('Ã','Â','â€','â€™','â€œ','â€�','â€“','â€”','â€¢','ðŸ','\ufffd')

def mojibake_score(value):
    return sum(value.count(token) for token in MOJIBAKE_TOKENS)

def repair_mojibake(value):
    current=value
    for _ in range(2):
        base=mojibake_score(current)
        if base == 0: break
        best=current; best_score=base
        for encoding in ('cp1252','latin-1'):
            try: candidate=current.encode(encoding).decode('utf-8')
            except (UnicodeEncodeError,UnicodeDecodeError): continue
            score=mojibake_score(candidate)
            if score < best_score: best,best_score=candidate,score
        if best == current: break
        current=best
    return current

def fail(errors,msg): errors.append(msg)

def scan_strings(obj,path='$'):
    if isinstance(obj,str): yield path,obj
    elif isinstance(obj,list):
        for i,v in enumerate(obj): yield from scan_strings(v,f'{path}[{i}]')
    elif isinstance(obj,dict):
        for k,v in obj.items(): yield from scan_strings(v,f'{path}.{k}')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('json_file'); ap.add_argument('--repo')
    a=ap.parse_args(); path=Path(a.json_file); data=json.loads(path.read_text(encoding='utf-8-sig')); errors=[]; warnings=[]
    for key in ['schema_version','project','scope','stack','coverage','findings','strengths','limitations','recommendations']:
        if key not in data: fail(errors,f'missing top-level key: {key}')
    if data.get('schema_version')!='1.0': fail(errors,'schema_version must be 1.0')
    cov=data.get('coverage',{})
    d=cov.get('backend_handlers_discovered',0); r=cov.get('backend_handlers_reviewed',0)
    if isinstance(d,int) and isinstance(r,int) and r>d: fail(errors,'backend_handlers_reviewed cannot exceed discovered')
    fg=cov.get('frontend_privilege_gates',0); fm=cov.get('frontend_gates_mapped',0)
    if isinstance(fg,int) and isinstance(fm,int) and fm>fg: fail(errors,'frontend_gates_mapped cannot exceed discovered gates')
    ids=set(); repo=Path(a.repo).resolve() if a.repo else None
    for i,f in enumerate(data.get('findings',[])):
        p=f'findings[{i}]'; fid=f.get('id','')
        if not re.fullmatch(r'SEC-\d{3,}',fid): fail(errors,f'{p}.id invalid: {fid!r}')
        if fid in ids: fail(errors,f'duplicate finding id: {fid}')
        ids.add(fid)
        if f.get('severity') not in SEV: fail(errors,f'{p}.severity invalid')
        if f.get('category') not in CAT: fail(errors,f'{p}.category invalid')
        for key in ['title','description','exploitability','impact','remediation','regression_test']:
            if not str(f.get(key,'')).strip(): fail(errors,f'{p}.{key} is required')
        ev=f.get('evidence') or []
        if not ev: fail(errors,f'{p}.evidence must not be empty')
        if repo:
            for e in ev:
                loc=e.get('location','')
                m=re.match(r'(.+?):(\d+)(?:-(\d+))?$',loc)
                if m:
                    fp=repo/m.group(1)
                    if not fp.exists(): warnings.append(f'{fid}: evidence file missing: {m.group(1)}')
                    else:
                        try: n=sum(1 for _ in fp.open(errors='ignore'))
                        except Exception: n=0
                        if int(m.group(2))>n: warnings.append(f'{fid}: line {m.group(2)} exceeds {m.group(1)} line count {n}')
    for p,s in scan_strings(data):
        if any(rx.search(s) for rx in TOKEN_PATTERNS): fail(errors,f'possible unredacted credential at {p}')
        repaired=repair_mojibake(s)
        if repaired != s:
            fail(errors,f'likely text-encoding mojibake at {p}; save audit-results.json as UTF-8 (example repair: {repaired[:120]!r})')
        elif '\ufffd' in s:
            fail(errors,f'Unicode replacement character found at {p}; source text was decoded with data loss')
    if cov.get('git_history_scanned') and not cov.get('git_history_available'): fail(errors,'git_history_scanned=true but git_history_available=false')
    if errors:
        print('INVALID')
        for e in errors: print('ERROR:',e)
        for w in warnings: print('WARNING:',w)
        return 1
    print('VALID')
    for w in warnings: print('WARNING:',w)
    print(f"findings={len(data.get('findings',[]))} strengths={len(data.get('strengths',[]))} limitations={len(data.get('limitations',[]))}")
    return 0
if __name__=='__main__': sys.exit(main())
