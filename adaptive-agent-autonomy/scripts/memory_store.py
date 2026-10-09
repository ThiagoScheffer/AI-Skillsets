#!/usr/bin/env python3
"""Tiny local verified-memory store with lexical retrieval and token budgeting."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:sk|pk)_[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*\S+")
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def mem_path(repo: Path) -> Path:
    return repo / ".agent" / "memory.jsonl"

def contains_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)

def tokenize(text: str) -> set[str]:
    return {x for x in re.findall(r"[A-Za-z0-9_./:-]+", text.lower()) if len(x) > 2}

def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4)

def read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out

def cmd_init(repo: Path) -> None:
    p=mem_path(repo); p.parent.mkdir(parents=True, exist_ok=True); p.touch(exist_ok=True)
    gi=repo/".gitignore"
    line=".agent/session/"
    if gi.exists():
        txt=gi.read_text(encoding="utf-8")
        if line not in txt.splitlines():
            gi.write_text(txt + ("\n" if txt and not txt.endswith("\n") else "") + line + "\n", encoding="utf-8")
    print(p)

def cmd_record(a) -> int:
    repo=Path(a.repo).resolve(); p=mem_path(repo); p.parent.mkdir(parents=True, exist_ok=True)
    blob="\n".join([a.summary,a.evidence,a.tags,a.files])
    if contains_secret(blob):
        print("Refusing to store content that looks like a secret/credential.", file=sys.stderr); return 3
    if not a.verified and not a.human_confirmed:
        print("Refusing unverified durable memory: pass --verified or --human-confirmed.", file=sys.stderr); return 4
    rec={
        "id": hashlib.sha256((a.kind+"\0"+a.summary+"\0"+a.evidence).encode()).hexdigest()[:16],
        "ts": now(), "kind": a.kind, "summary": a.summary.strip(),
        "evidence": a.evidence.strip(), "tags": [x for x in a.tags.split(",") if x],
        "files": [x for x in a.files.split(",") if x], "confidence": a.confidence,
        "verified": bool(a.verified), "human_confirmed": bool(a.human_confirmed), "supersedes": a.supersedes or None
    }
    with p.open("a",encoding="utf-8") as f: f.write(json.dumps(rec,sort_keys=True)+"\n")
    print(json.dumps(rec,indent=2)); return 0

def cmd_context(a) -> None:
    records=read_records(mem_path(Path(a.repo).resolve()))
    q=tokenize(" ".join([a.query,a.files,a.tags]))
    scored=[]
    for r in records:
        hay=" ".join([r.get("summary",""),r.get("evidence","")," ".join(r.get("tags",[]))," ".join(r.get("files",[]))])
        score=len(q & tokenize(hay)) + float(r.get("confidence",0)) * 0.25
        if score>0: scored.append((score,r))
    scored.sort(key=lambda x:(x[0],x[1].get("ts","")), reverse=True)
    used=0; selected=[]
    for score,r in scored[:max(a.limit*3,a.limit)]:
        line=f"- [{r['kind']}] {r['summary']} | evidence: {r['evidence']} | id:{r['id']}"
        cost=estimate_tokens(line)
        if selected and used+cost>a.max_tokens: continue
        selected.append(line); used+=cost
        if len(selected)>=a.limit: break
    print("\n".join(selected) if selected else "(no relevant verified memory)")
    print(f"\n# estimated_tokens={used}", file=sys.stderr)

def cmd_compact(a) -> None:
    p=mem_path(Path(a.repo).resolve()); records=read_records(p)
    latest={}
    for r in records:
        key=(r.get("kind"),r.get("summary","").strip().lower())
        prev=latest.get(key)
        if prev is None or (r.get("confidence",0),r.get("ts","")) >= (prev.get("confidence",0),prev.get("ts","")):
            latest[key]=r
    compacted=sorted(latest.values(),key=lambda r:r.get("ts",""))
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in compacted),encoding="utf-8")
    print(json.dumps({"before":len(records),"after":len(compacted)},indent=2))

def main() -> int:
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("init"); p.add_argument("--repo",default=".")
    p=sp.add_parser("record"); p.add_argument("--repo",default="."); p.add_argument("--kind",required=True,choices=["decision","lesson","pattern","command","risk"]); p.add_argument("--summary",required=True); p.add_argument("--evidence",required=True); p.add_argument("--tags",default=""); p.add_argument("--files",default=""); p.add_argument("--confidence",type=float,default=.8); p.add_argument("--verified",action="store_true"); p.add_argument("--human-confirmed",action="store_true"); p.add_argument("--supersedes",default="")
    p=sp.add_parser("context"); p.add_argument("--repo",default="."); p.add_argument("--query",default=""); p.add_argument("--files",default=""); p.add_argument("--tags",default=""); p.add_argument("--max-tokens",type=int,default=1200); p.add_argument("--limit",type=int,default=8)
    p=sp.add_parser("compact"); p.add_argument("--repo",default=".")
    a=ap.parse_args()
    if a.cmd=="init": cmd_init(Path(a.repo).resolve()); return 0
    if a.cmd=="record": return cmd_record(a)
    if a.cmd=="context": cmd_context(a); return 0
    if a.cmd=="compact": cmd_compact(a); return 0
    return 1
if __name__=="__main__": raise SystemExit(main())
