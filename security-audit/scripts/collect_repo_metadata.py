#!/usr/bin/env python3
"""Collect stack/security-relevant repository metadata without modifying the repo."""
from __future__ import annotations
import argparse, json, os, re, subprocess
from pathlib import Path

SKIP = {'.git','node_modules','vendor','dist','build','.next','.nuxt','.venv','venv','target','coverage','__pycache__'}
MANIFESTS = {'package.json','pyproject.toml','requirements.txt','Pipfile','poetry.lock','Gemfile','composer.json','pom.xml','build.gradle','build.gradle.kts','go.mod','Cargo.toml'}
INFRA_NAMES = {'Dockerfile','docker-compose.yml','docker-compose.yaml','compose.yml','compose.yaml','Jenkinsfile','serverless.yml','serverless.yaml','vercel.json','netlify.toml'}

def run(cmd, cwd):
    try:
        return subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.DEVNULL, text=True, timeout=10).strip()
    except Exception:
        return ''

def walk(root: Path):
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith('.tox')]
        bp = Path(base)
        for name in names:
            yield bp / name

def parse_package_json(path: Path):
    out = []
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig', errors='replace'))
        deps = {**data.get('dependencies',{}), **data.get('devDependencies',{})}
        known = ['next','react','vue','nuxt','@angular/core','svelte','express','fastify','@nestjs/core','hono','prisma','@prisma/client','drizzle-orm','sequelize','typeorm','knex','mongoose','@supabase/supabase-js','passport','next-auth','@auth/core']
        out = [k for k in known if k in deps]
    except Exception:
        pass
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', nargs='?', default='.')
    ap.add_argument('--output')
    args = ap.parse_args()
    root = Path(args.repo).resolve()
    files = list(walk(root))
    rels = [str(p.relative_to(root)) for p in files]
    manifests = [r for r in rels if Path(r).name in MANIFESTS]
    infra = [r for r in rels if Path(r).name in INFRA_NAMES or r.startswith('.github/workflows/') or '/helm/' in ('/'+r.lower()+'/') or r.endswith('.tf') or r.endswith('.tfvars') or '/k8s/' in ('/'+r.lower()+'/') or '/kubernetes/' in ('/'+r.lower()+'/')]
    exts = {}
    for p in files:
        if p.suffix:
            exts[p.suffix.lower()] = exts.get(p.suffix.lower(), 0) + 1
    frameworks = []
    for p in files:
        if p.name == 'package.json': frameworks += parse_package_json(p)
    text_markers = {
      'supabase':['@supabase/supabase-js','auth.uid()','create policy','row level security'],
      'django':['django','rest_framework'], 'fastapi':['fastapi'], 'flask':['flask'],
      'rails':['rails','before_action'], 'spring':['org.springframework','@PreAuthorize'],
      'aspnet':['Microsoft.AspNetCore','[Authorize]'], 'laravel':['Illuminate\\','Route::'],
    }
    marker_hits = {k: [] for k in text_markers}
    candidate_text = [p for p in files if p.suffix.lower() in {'.js','.jsx','.ts','.tsx','.py','.rb','.php','.java','.kt','.cs','.go','.sql','.toml','.yaml','.yml','.json','.xml'} and p.stat().st_size < 2_000_000]
    for p in candidate_text:
        try: txt = p.read_text(encoding='utf-8', errors='replace')
        except Exception: continue
        for k, markers in text_markers.items():
            if any(m.lower() in txt.lower() for m in markers):
                marker_hits[k].append(str(p.relative_to(root)))
    git = {
      'available': (root/'.git').exists() or bool(run(['git','rev-parse','--git-dir'], root)),
      'head': run(['git','rev-parse','HEAD'], root),
      'branch': run(['git','branch','--show-current'], root),
      'status_porcelain': run(['git','status','--porcelain'], root).splitlines() if run(['git','rev-parse','--git-dir'], root) else []
    }
    result = {
      'repo_root': str(root), 'manifests': manifests, 'infra_files': sorted(infra),
      'extension_counts': dict(sorted(exts.items(), key=lambda kv: -kv[1])[:30]),
      'package_framework_dependencies': sorted(set(frameworks)),
      'stack_marker_files': {k:v[:50] for k,v in marker_hits.items() if v},
      'git': git
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output: Path(args.output).write_text(text+'\n', encoding='utf-8')
    else: print(text)

if __name__ == '__main__': main()
