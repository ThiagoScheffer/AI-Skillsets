#!/usr/bin/env python3
"""Find security-review candidates. Matches are NOT vulnerability findings."""
from __future__ import annotations
import argparse, json, os, re
from pathlib import Path

SKIP = {'.git','node_modules','vendor','dist','build','.next','.nuxt','.venv','venv','target','coverage','__pycache__'}
TEXT_EXTS = {'.js','.jsx','.mjs','.cjs','.ts','.tsx','.vue','.svelte','.py','.rb','.php','.java','.kt','.cs','.go','.rs','.sql','.html','.htm','.jinja','.jinja2','.twig','.erb','.cshtml','.yaml','.yml','.toml','.json','.xml','.tf','.sh','.md'}

PATTERNS = {
 'frontend_privilege_gate': [r'\bisAdmin\b',r'\bisOwner\b',r'\bcan(?:Edit|Delete|Manage|Invite|Approve)\b',r'\brole\s*={2,3}\s*[\'\"](?:admin|owner|manager)',r'\bpermissions?\b'],
 'xss_sink': [r'dangerouslySetInnerHTML',r'\bv-html\b',r'\{@html\b',r'\[innerHTML\]',r'\.innerHTML\s*=',r'\.outerHTML\s*=',r'insertAdjacentHTML\s*\(',r'document\.write\s*\(',r'\bHtml\.Raw\s*\(',r'\bhtml_safe\b',r'\bmark_safe\s*\(',r'\beval\s*\(',r'new\s+Function\s*\(',r'\bsrcdoc\b'],
 'sanitizer': [r'DOMPurify',r'\bsanitize-html\b',r'\bbleach\b',r'OWASP.*Sanitizer',r'HtmlSanitizer',r'bluemonday',r'Rails::Html::SafeListSanitizer'],
 'tenant_marker': [r'\btenant_id\b',r'\borganization_id\b',r'\bworkspace_id\b',r'\baccount_id\b',r'\buser_id\b',r'\bauth\.uid\s*\(',r'row\s+level\s+security',r'create\s+policy'],
 'object_id_candidate': [r'params\[[\'\"](?:id|.*_id)[\'\"]\]',r'params\.(?:id|\w+Id)\b',r'req\.params\.',r'req\.query\.',r'path_params',r'@PathVariable',r'\[FromRoute\]',r'c\.Param\s*\(',r'ctx\.Param\s*\('],
 'privileged_secret_name': [r'SERVICE_ROLE',r'SECRET_KEY',r'JWT_SECRET',r'WEBHOOK_SECRET',r'PRIVATE_KEY',r'CLIENT_SECRET',r'DATABASE_PASSWORD',r'DB_PASSWORD',r'API_SECRET'],
 'secret_fallback': [r'\$\{[A-Z0-9_]+:-[^}]+\}',r'getenv\([^)]*\)\s*(?:or|\|\|)\s*[\'\"][^\'\"]+[\'\"]'],
 'supabase_privileged_key': [r'sb_secret_[A-Za-z0-9_-]{8,}',r'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'],
 'generic_private_key': [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'],
}
COMPILED = {k:[re.compile(p,re.I) for p in ps] for k,ps in PATTERNS.items()}

def redact(s: str) -> str:
    s = re.sub(r'(sb_secret_[A-Za-z0-9_-]{4})[A-Za-z0-9_-]+', r'\1...REDACTED', s)
    s = re.sub(r'(eyJ[A-Za-z0-9_-]{8})[A-Za-z0-9_.-]{20,}', r'\1...REDACTED', s)
    s = re.sub(r'(?i)(password|secret|token|api[_-]?key)(\s*[:=]\s*[\'\"]?)([^\s\'\",}]{8,})', lambda m: m.group(1)+m.group(2)+m.group(3)[:4]+'...REDACTED', s)
    return s[:500]

def walk(root):
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for n in names:
            p = Path(base)/n
            if p.suffix.lower() in TEXT_EXTS or n in {'Dockerfile','Jenkinsfile'}:
                try:
                    if p.stat().st_size <= 2_000_000: yield p
                except OSError: pass

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo', nargs='?', default='.')
    ap.add_argument('--output')
    args=ap.parse_args(); root=Path(args.repo).resolve()
    results=[]
    for p in walk(root):
        try: lines=p.read_text(encoding='utf-8', errors='replace').splitlines()
        except Exception: continue
        rel=str(p.relative_to(root))
        for no,line in enumerate(lines,1):
            for kind,res in COMPILED.items():
                if any(r.search(line) for r in res):
                    results.append({'kind':kind,'file':rel,'line':no,'snippet':redact(line.strip())})
    out={'warning':'Candidate discovery only. Every match requires semantic verification.','count':len(results),'candidates':results}
    text=json.dumps(out,indent=2,ensure_ascii=False)
    if args.output: Path(args.output).write_text(text+'\n', encoding='utf-8')
    else: print(text)

if __name__=='__main__': main()
