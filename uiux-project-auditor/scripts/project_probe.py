#!/usr/bin/env python3
"""Read-only project orientation helper for uiux-project-auditor."""
from __future__ import annotations
import argparse, json, os, re
from pathlib import Path

EXCLUDE={'.git','node_modules','vendor','.next','dist','build','coverage','.venv','venv','__pycache__','.turbo','.cache'}
CODE_EXT={'.js','.jsx','.ts','.tsx','.vue','.svelte','.py','.rb','.php','.go','.rs','.java','.kt','.swift','.html','.css','.scss','.sass','.less','.md','.json','.yaml','.yml','.toml'}
MANIFESTS=['package.json','pnpm-lock.yaml','yarn.lock','package-lock.json','bun.lockb','pyproject.toml','requirements.txt','Pipfile','poetry.lock','Cargo.toml','go.mod','Gemfile','composer.json','pom.xml','build.gradle','build.gradle.kts']


def walk(root:Path):
    for dp, dns, fns in os.walk(root):
        dns[:]=[d for d in dns if d not in EXCLUDE]
        p=Path(dp)
        for fn in fns:
            yield p/fn


def read_text(path:Path, limit=500_000):
    try:
        if path.stat().st_size>limit: return ''
        return path.read_text(errors='ignore')
    except Exception:
        return ''


def detect_frameworks(root:Path, manifests:list[Path]):
    fw=set(); deps=set()
    pkg=root/'package.json'
    if pkg.exists():
        try:
            data=json.loads(pkg.read_text())
            for sec in ('dependencies','devDependencies','peerDependencies'):
                deps.update((data.get(sec) or {}).keys())
        except Exception: pass
    mapping={
        'next':'Next.js','react':'React','vue':'Vue','nuxt':'Nuxt','svelte':'Svelte','@sveltejs/kit':'SvelteKit',
        'astro':'Astro','angular':'Angular','@angular/core':'Angular','remix':'Remix','@remix-run/react':'Remix',
        'tailwindcss':'Tailwind CSS','@mui/material':'MUI','@chakra-ui/react':'Chakra UI','antd':'Ant Design',
        'shadcn':'shadcn/ui','@radix-ui/react-dialog':'Radix UI','framer-motion':'Framer Motion',
        'express':'Express','fastify':'Fastify','hono':'Hono'
    }
    for k,v in mapping.items():
        if k in deps: fw.add(v)
    py=(root/'pyproject.toml')
    pytext=read_text(py).lower() if py.exists() else ''
    req=read_text(root/'requirements.txt').lower() if (root/'requirements.txt').exists() else ''
    blob=pytext+'\n'+req
    for k,v in [('django','Django'),('flask','Flask'),('fastapi','FastAPI'),('streamlit','Streamlit'),('gradio','Gradio')]:
        if k in blob: fw.add(v)
    return sorted(fw), sorted(deps)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    files=list(walk(root))
    manifests=[p for p in files if p.name in MANIFESTS]
    frameworks,deps=detect_frameworks(root,manifests)
    source=[p for p in files if p.suffix.lower() in CODE_EXT]
    style=[p for p in source if p.suffix.lower() in {'.css','.scss','.sass','.less'} or any(x in p.name.lower() for x in ('theme','token','style'))]
    tests=[p for p in source if re.search(r'(test|spec)\.',p.name,re.I) or any(part.lower() in {'test','tests','__tests__','spec'} for part in p.parts)]
    route_dirs=[]
    for d in ('app','pages','routes','src/app','src/pages','src/routes'):
        p=root/d
        if p.exists() and p.is_dir(): route_dirs.append(str(p.relative_to(root)))
    surfaces={k:[] for k in ('auth','admin','payment','upload','url_fetch','ai_llm','rich_content')}
    pats={
        'auth':r'auth|login|signin|signup|register|password|session|magic[-_ ]?link|mfa|oauth',
        'admin':r'admin|role|permission|rbac|acl',
        'payment':r'payment|checkout|billing|stripe|invoice|subscription',
        'upload':r'upload|attachment|file[-_ ]?input|multipart',
        'url_fetch':r'webhook|callback|preview|fetch[-_ ]?url|import[-_ ]?url|scrape|crawler|seo',
        'ai_llm':r'llm|openai|anthropic|gemini|prompt|agent|embedding|vector|rag|mcp',
        'rich_content':r'markdown|rich[-_ ]?text|html|sanitize|wysiwyg|editor'
    }
    for p in source:
        rel=str(p.relative_to(root))
        low=rel.lower()
        for k,pat in pats.items():
            if re.search(pat,low):
                if len(surfaces[k])<25: surfaces[k].append(rel)
    result={
        'root':str(root),
        'file_count':len(files),
        'source_file_count':len(source),
        'frameworks':frameworks,
        'manifests':[str(p.relative_to(root)) for p in manifests],
        'route_dirs':route_dirs,
        'style_or_token_files':[str(p.relative_to(root)) for p in style[:40]],
        'test_file_count':len(tests),
        'sample_test_files':[str(p.relative_to(root)) for p in tests[:20]],
        'sensitive_surface_hints':surfaces,
    }
    if args.json:
        print(json.dumps(result,indent=2))
        return
    print(f"Root: {root}")
    print(f"Files: {len(files)} | source-like: {len(source)} | tests: {len(tests)}")
    print('Frameworks: '+(', '.join(frameworks) if frameworks else 'not confidently detected'))
    print('Manifests: '+(', '.join(result['manifests']) if manifests else 'none detected'))
    print('Route dirs: '+(', '.join(route_dirs) if route_dirs else 'none detected'))
    if result['style_or_token_files']:
        print('\nStyle/token candidates:')
        for x in result['style_or_token_files'][:20]: print('  -',x)
    print('\nSensitive surface hints (filename/path heuristics):')
    for k,vals in surfaces.items():
        if vals:
            print(f"  {k}: {len(vals)} shown")
            for x in vals[:8]: print('    -',x)
    print('\nReminder: filename/path detection is orientation only. Read actual call paths before reporting findings.')

if __name__=='__main__': main()
