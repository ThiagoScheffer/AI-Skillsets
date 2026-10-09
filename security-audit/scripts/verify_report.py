#!/usr/bin/env python3
"""Structural PDF checks plus optional representative page rasterization."""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError as e:
    raise SystemExit('Missing pypdf. Use an isolated venv and install requirements-report.txt') from e

MOJIBAKE_TOKENS=('Ã','Â','â€','â€™','â€œ','â€�','â€“','â€”','â€¢','ðŸ','\ufffd')

def mojibake_score(value):
    return sum(value.count(token) for token in MOJIBAKE_TOKENS)

def has_likely_mojibake(value):
    if '\ufffd' in value:
        return True
    base=mojibake_score(value)
    if base == 0:
        return False
    for encoding in ('cp1252','latin-1'):
        try: candidate=value.encode(encoding).decode('utf-8')
        except (UnicodeEncodeError,UnicodeDecodeError): continue
        if mojibake_score(candidate) < base:
            return True
    return False

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('pdf'); ap.add_argument('--render-dir'); args=ap.parse_args(); p=Path(args.pdf).resolve()
    result={'pdf':str(p),'exists':p.exists(),'pages':0,'checks':{},'rendered_pages':[],'warnings':[]}
    if not p.exists(): print(json.dumps(result,indent=2)); return 1
    reader=PdfReader(str(p)); result['pages']=len(reader.pages)
    text='\n'.join((page.extract_text() or '') for page in reader.pages)
    result['checks']['title_present']='Relatório de Auditoria de Segurança' in text
    result['checks']['github_issues_section']='ISSUES PARA O GITHUB' in text
    result['checks']['nonempty_text']=len(text.strip())>200
    result['checks']['reasonable_size']=p.stat().st_size>3_000
    result['checks']['text_encoding_clean']=not has_likely_mojibake(text)
    if not result['checks']['text_encoding_clean']:
        result['warnings'].append('likely mojibake or Unicode replacement glyph detected in extracted PDF text')
    renderer=shutil.which('pdftoppm')
    if renderer and result['pages']:
        outdir=Path(args.render_dir).resolve() if args.render_dir else p.parent/'_verification_renders'; outdir.mkdir(parents=True,exist_ok=True)
        pages=sorted(set([1,max(1,(result['pages']+1)//2),result['pages']]))
        for page in pages:
            prefix=outdir/f'page-{page:03d}'
            cp=subprocess.run([renderer,'-f',str(page),'-singlefile','-png','-r','130',str(p),str(prefix)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            image=prefix.with_suffix('.png')
            if cp.returncode==0 and image.exists() and image.stat().st_size>1000: result['rendered_pages'].append(str(image))
            else: result['warnings'].append(f'failed to render page {page}: {cp.stderr[-300:]}')
    else: result['warnings'].append('pdftoppm unavailable; visual rasterization not performed')
    ok=all(result['checks'].values()) and result['pages']>=1
    result['ok']=ok
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
