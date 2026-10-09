#!/usr/bin/env python3
"""Create a canonical audit-results.json skeleton in a target repository."""
from __future__ import annotations
import argparse, json, subprocess
from datetime import date
from pathlib import Path

def git_remote(root):
    try: return subprocess.check_output(['git','remote','get-url','origin'],cwd=root,text=True,stderr=subprocess.DEVNULL,timeout=5).strip()
    except Exception: return ''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('repo',nargs='?',default='.'); ap.add_argument('--force',action='store_true')
    args=ap.parse_args(); root=Path(args.repo).resolve(); outdir=root/'docs/security-audit'; outdir.mkdir(parents=True,exist_ok=True)
    out=outdir/'audit-results.json'
    if out.exists() and not args.force: raise SystemExit(f'{out} already exists; use --force to replace')
    data={
      'schema_version':'1.0',
      'project':{'name':root.name,'audit_date':date.today().isoformat(),'repository':git_remote(root)},
      'scope':{'audited':[],'excluded':[],'methodology_note':''},
      'stack':{'languages':[],'backend':[],'frontend':[],'database':[],'data_access':[],'authentication':[],'authorization':[],'tenant_isolation':[],'deployment':[],'evidence':[]},
      'coverage':{'backend_handlers_discovered':0,'backend_handlers_reviewed':0,'authenticated_handlers':0,'privileged_operations':0,'object_id_handlers':0,'tenant_scoped_operations':0,'frontend_privilege_gates':0,'frontend_gates_mapped':0,'unsafe_rendering_sinks':0,'secret_locations_scanned':0,'git_history_available':False,'git_history_scanned':False,'deployment_files_reviewed':0,'notes':[]},
      'findings':[], 'strengths':[], 'limitations':[], 'recommendations':[], 'github_issues':[]
    }
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n', encoding='utf-8')
    print(out)
if __name__=='__main__': main()
