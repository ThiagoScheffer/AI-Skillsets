#!/usr/bin/env python3
"""Heuristic, read-only UI/accessibility/security scan. Leads, not proof."""
from __future__ import annotations
import argparse, json, os, re
from collections import Counter, defaultdict
from pathlib import Path

EXCLUDE={'.git','node_modules','vendor','.next','dist','build','coverage','.venv','venv','__pycache__','.turbo','.cache'}
EXT={'.js','.jsx','.ts','.tsx','.vue','.svelte','.py','.rb','.php','.go','.rs','.java','.kt','.swift','.html','.htm','.css','.scss','.sass','.less'}
MAX_FILE=1_500_000

RULES=[
 ('SEC-EVAL','security','High','High',re.compile(r'\beval\s*\('),'Dynamic eval can turn data into code. Confirm whether input can be untrusted.'),
 ('SEC-NEWFUNC','security','High','High',re.compile(r'\bnew\s+Function\s*\('),'Dynamic Function construction can execute generated/untrusted code.'),
 ('SEC-DANGEROUS-HTML','security','Medium','High',re.compile(r'\bdangerouslySetInnerHTML\b'),'Raw HTML rendering requires trusted/sanitized, context-appropriate handling.'),
 ('SEC-INNERHTML','security','Medium','Medium',re.compile(r'\.innerHTML\s*='),'DOM HTML sink: trace the value and confirm safe output handling.'),
 ('SEC-SHELL','security','High','High',re.compile(r'\bshell\s*=\s*True\b'),'Shell execution increases command-injection risk; inspect data flow.'),
 ('SEC-CHILD-EXEC','security','High','Medium',re.compile(r'\b(?:exec|execSync)\s*\('),'Command execution call: confirm arguments are not built from untrusted input.'),
 ('SEC-TLS-VERIFY','security','High','High',re.compile(r'\bverify\s*=\s*False\b'),'TLS certificate verification appears disabled.'),
 ('SEC-CORS-WILDCARD','security','Medium','Medium',re.compile(r'(?:allow_origins|Access-Control-Allow-Origin)[^\n]{0,80}[\[\(\{\"\']\*'),'Potential wildcard CORS policy. Confirm credentials/exposure and intended trust boundary.'),
 ('SEC-AUTH-ENUM','security','Medium','Medium',re.compile(r'(?i)(email|user|account).{0,30}(already exists|does not exist|not found|is registered)|already registered'),'User-visible account-existence wording can enable enumeration. Confirm context, response code, timing, and abuse controls.'),
 ('SEC-LOCALSTORAGE-TOKEN','security','Medium','Low',re.compile(r'(?i)localStorage\.(?:setItem|getItem)\s*\([^\n]{0,80}(token|jwt|access|refresh)'),'Token in localStorage may increase XSS impact; review auth architecture.'),
 ('SEC-SECRET','security','High','Medium',re.compile(r'(?i)(api[_-]?key|secret|private[_-]?key|client[_-]?secret)\s*[:=]\s*[\"\'][A-Za-z0-9_\-]{16,}'),'Possible hard-coded secret. Confirm whether this is a real credential or test placeholder.'),
 ('SEC-HTTP','security','Low','Low',re.compile(r'http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)'), 'Plain HTTP endpoint detected; confirm whether transport security is required.'),
 ('A11Y-IMG-ALT','accessibility','Medium','Medium',re.compile(r'<img\b(?![^>]*\balt\s*=)[^>]*>', re.I),'Image tag appears to lack alt text. Confirm decorative vs informative use.'),
 ('A11Y-OUTLINE','accessibility','Medium','Medium',re.compile(r'outline\s*:\s*(?:none|0)\b', re.I),'Focus outline removed. Confirm an equally visible replacement focus style exists.'),
 ('A11Y-AUTOFOCUS','accessibility','Low','Low',re.compile(r'\bautoFocus\b|\bautofocus\b'),'Autofocus can disrupt keyboard/screen-reader context; confirm it is intentional.'),
 ('UI-INLINE-STYLE','design-system','Low','Low',re.compile(r'\bstyle\s*=\s*\{\{'),'Inline style object may bypass shared tokens/components; inspect for intentional dynamic styling.'),
 ('UI-IMPORTANT','design-system','Low','Low',re.compile(r'!important\b'),'Frequent !important can indicate cascading/token problems; inspect if repeated.'),
]

HEX_RE=re.compile(r'#[0-9a-fA-F]{3,8}\b')
RADIUS_RE=re.compile(r'border-radius\s*:\s*([^;}{]+)',re.I)
FONT_RE=re.compile(r'font-size\s*:\s*([^;}{]+)',re.I)
SHADOW_RE=re.compile(r'box-shadow\s*:',re.I)
GRAD_RE=re.compile(r'(?:linear|radial)-gradient\s*\(',re.I)


def walk(root):
    for dp,dns,fns in os.walk(root):
        dns[:]=[d for d in dns if d not in EXCLUDE]
        p=Path(dp)
        for fn in fns:
            q=p/fn
            if q.suffix.lower() in EXT:
                yield q


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root',nargs='?',default='.')
    ap.add_argument('--format',choices=('text','json'),default='text')
    ap.add_argument('--max-findings',type=int,default=250)
    args=ap.parse_args(); root=Path(args.root).resolve()
    findings=[]; metrics=defaultdict(Counter); counts=Counter()
    for p in walk(root):
        try:
            if p.stat().st_size>MAX_FILE: continue
            text=p.read_text(errors='ignore')
        except Exception: continue
        rel=str(p.relative_to(root)); counts['files']+=1
        for m in HEX_RE.finditer(text): metrics['colors'][m.group(0).lower()]+=1
        for m in RADIUS_RE.finditer(text): metrics['radii'][m.group(1).strip()]+=1
        for m in FONT_RE.finditer(text): metrics['font_sizes'][m.group(1).strip()]+=1
        counts['box_shadows']+=len(SHADOW_RE.findall(text)); counts['gradients']+=len(GRAD_RE.findall(text))
        lines=text.splitlines()
        for lineno,line in enumerate(lines,1):
            for rid,cat,sev,conf,rx,msg in RULES:
                if rx.search(line):
                    findings.append({'id':rid,'category':cat,'severity':sev,'confidence':conf,'file':rel,'line':lineno,'message':msg,'snippet':line.strip()[:240]})
                    if len(findings)>=args.max_findings: break
            if len(findings)>=args.max_findings: break
        if len(findings)>=args.max_findings: break
    summary={
      'scanned_files':counts['files'],
      'finding_count':len(findings),
      'design_metrics':{
        'unique_hex_colors':len(metrics['colors']), 'top_hex_colors':metrics['colors'].most_common(15),
        'unique_border_radius_values':len(metrics['radii']), 'top_border_radii':metrics['radii'].most_common(12),
        'unique_font_size_values':len(metrics['font_sizes']), 'top_font_sizes':metrics['font_sizes'].most_common(12),
        'box_shadow_declarations':counts['box_shadows'], 'gradient_usages':counts['gradients']
      },
      'findings':findings,
      'disclaimer':'Heuristic leads only. Confirm every finding in context. Zero findings does not mean the project is secure, accessible, or well designed.'
    }
    if args.format=='json': print(json.dumps(summary,indent=2)); return
    print(f"Scanned {summary['scanned_files']} files; {len(findings)} heuristic leads.\n")
    dm=summary['design_metrics']
    print('Design-system signals:')
    print(f"  unique hex colors: {dm['unique_hex_colors']} | radii: {dm['unique_border_radius_values']} | font sizes: {dm['unique_font_size_values']}")
    print(f"  box-shadow declarations: {dm['box_shadow_declarations']} | gradients: {dm['gradient_usages']}")
    if dm['top_hex_colors']: print('  top colors:', ', '.join(f'{k}({v})' for k,v in dm['top_hex_colors'][:8]))
    print('\nLeads:')
    for f in findings:
        print(f"[{f['severity']}/{f['confidence']}] {f['id']} {f['file']}:{f['line']} — {f['message']}")
        if f['snippet']: print('   ',f['snippet'])
    print('\n'+summary['disclaimer'])

if __name__=='__main__': main()
