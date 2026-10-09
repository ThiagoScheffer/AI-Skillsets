#!/usr/bin/env python3
"""Project-local evidence and reputation engine for adaptive-agent-autonomy.

The score is scoped to a task family in the current project. It is deliberately
not a permanent score for the model/agent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    from memory_store import contains_secret
except Exception:  # pragma: no cover - defensive when imported unusually
    def contains_secret(_text: str) -> bool:
        return False

PROTECTED = {
    "auth", "authentication", "authorization", "permissions", "identity",
    "secrets", "money", "billing", "payments", "migration", "migrations",
    "destructive-data", "production", "security", "legal", "compliance",
    "irreversible", "privacy", "dns", "certificates",
}
CONSEQUENTIAL = {"commit", "push", "merge", "deploy", "production-action"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def evidence_path(repo: Path) -> Path:
    return repo / ".agent" / "evidence.jsonl"


def csv_list(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


def normalize_family(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")


def parse_ts(value: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def file_similarity(current: set[str], prior: set[str]) -> float:
    if not current or not prior:
        return 1.0
    exact = len(current & prior) / max(1, len(current | prior))
    cur_top = {p.split("/", 1)[0] for p in current}
    prv_top = {p.split("/", 1)[0] for p in prior}
    top = len(cur_top & prv_top) / max(1, len(cur_top | prv_top))
    return max(exact, top * 0.75)


def recency_weight(ts: str, *, half_life_days: float = 90.0) -> float:
    age = max(0.0, (datetime.now(timezone.utc) - parse_ts(ts)).total_seconds() / 86400.0)
    return max(0.10, math.pow(0.5, age / half_life_days))


def assess(
    records: Iterable[dict], *, task_family: str, operation: str,
    files: list[str], blast_radius: str, test_stability: str, rollback: str,
    protected: list[str], novel: bool = False, external_side_effects: bool = False,
    max_history: int = 20,
) -> dict:
    family = normalize_family(task_family)
    current_files = set(files)
    relevant = [r for r in records if normalize_family(str(r.get("task_family", ""))) == family]
    relevant.sort(key=lambda r: r.get("ts", ""), reverse=True)
    relevant = relevant[:max_history]

    weighted_success = 0.0
    weighted_total = 0.0
    weighted_review = 0.0
    weighted_verified = 0.0
    similarity_sum = 0.0
    successes = 0
    failures = 0
    recent_failures = 0
    freshest_success_weight = 0.0

    for idx, r in enumerate(relevant):
        sim = file_similarity(current_files, set(r.get("files", [])))
        op_factor = 1.0 if r.get("operation") == operation else 0.85
        weight = recency_weight(str(r.get("ts", ""))) * (0.55 + 0.45 * sim) * op_factor
        outcome = r.get("outcome")
        verified = bool(r.get("verified"))
        trusted_success = outcome == "success" and verified
        if trusted_success:
            successes += 1
            weighted_success += weight
            freshest_success_weight = max(freshest_success_weight, recency_weight(str(r.get("ts", ""))))
        elif outcome in {"failure", "rollback"}:
            failures += 1
            if idx < 5:
                recent_failures += 1
        weighted_total += weight
        weighted_review += weight * (1.0 if r.get("reviewed") else 0.0)
        weighted_verified += weight * (1.0 if verified else 0.0)
        similarity_sum += sim

    # Beta prior prevents tiny sample sets from looking certain.
    history_rate = (weighted_success + 1.0) / (weighted_total + 2.0)
    volume = min(successes / 5.0, 1.0)
    review_ratio = weighted_review / weighted_total if weighted_total else 0.0
    verified_ratio = weighted_verified / weighted_total if weighted_total else 0.0
    avg_similarity = similarity_sum / len(relevant) if relevant else 0.0

    test_score = {"stable": 1.0, "flaky": 0.35, "failing": 0.0, "unknown": 0.20}[test_stability]
    rollback_score = {"known": 1.0, "partial": 0.50, "unknown": 0.10, "irreversible": 0.0}[rollback]
    blast_score = {"low": 1.0, "medium": 0.45, "high": 0.0}[blast_radius]
    recency_score = freshest_success_weight if successes else 0.0

    score = 100.0 * (
        0.30 * history_rate
        + 0.15 * volume
        + 0.10 * review_ratio
        + 0.10 * verified_ratio
        + 0.10 * test_score
        + 0.10 * rollback_score
        + 0.10 * blast_score
        + 0.05 * recency_score
    )
    if recent_failures:
        score -= min(20.0, 8.0 * recent_failures)
    if novel:
        score -= 12.0
    if external_side_effects:
        score -= 8.0
    score = max(0.0, min(100.0, score))

    protected_hit = sorted({p.lower() for p in protected} & PROTECTED)
    reasons: list[str] = []
    if protected_hit:
        risk = "novel-high-risk"
        reasons.append("protected domain: " + ", ".join(protected_hit))
    elif rollback == "irreversible":
        risk = "novel-high-risk"
        reasons.append("rollback is irreversible")
    elif blast_radius == "high":
        risk = "novel-high-risk"
        reasons.append("high blast radius")
    elif external_side_effects and rollback != "known":
        risk = "novel-high-risk"
        reasons.append("external side effects without a known rollback")
    elif novel and successes < 2:
        risk = "novel-high-risk"
        reasons.append("novel task with insufficient project precedent")
    else:
        routine_ok = (
            score >= 82.0
            and successes >= 3
            and recent_failures == 0
            and test_stability == "stable"
            and blast_radius == "low"
            and rollback == "known"
            and not novel
            and not external_side_effects
            and (not current_files or avg_similarity >= 0.50)
        )
        if routine_ok:
            risk = "routine-proven"
            reasons.append("repeated verified project precedent meets routine threshold")
        else:
            risk = "non-trivial"
            if successes < 3:
                reasons.append(f"only {successes} verified prior successes; 3 required for routine")
            if score < 82.0:
                reasons.append(f"evidence score {score:.1f} is below the 82.0 routine threshold")
            if recent_failures:
                reasons.append(f"{recent_failures} failure(s) in the five most recent matching outcomes")
            if test_stability != "stable":
                reasons.append(f"test stability is {test_stability}")
            if blast_radius != "low":
                reasons.append(f"blast radius is {blast_radius}")
            if rollback != "known":
                reasons.append(f"rollback is {rollback}")
            if current_files and relevant and avg_similarity < 0.50:
                reasons.append("current file scope has weak overlap with prior successes")

    promotion_candidate = (
        risk == "routine-proven" and successes >= 3 and recent_failures == 0
    )
    return {
        "task_family": family,
        "risk": risk,
        "confidence": round(score / 100.0, 3),
        "evidence_score": round(score, 1),
        "history": {
            "matching_records": len(relevant),
            "verified_successes": successes,
            "failures": failures,
            "recent_failures": recent_failures,
            "weighted_success_rate": round(history_rate, 3),
            "review_ratio": round(review_ratio, 3),
            "verification_ratio": round(verified_ratio, 3),
            "file_similarity": round(avg_similarity, 3),
        },
        "current": {
            "operation": operation,
            "blast_radius": blast_radius,
            "test_stability": test_stability,
            "rollback": rollback,
            "protected": protected_hit,
            "novel": novel,
            "external_side_effects": external_side_effects,
        },
        "reasons": reasons,
        "promotion_candidate": promotion_candidate,
        "next": (
            "verification + gate"
            if risk == "routine-proven"
            else "verification + targeted review + gate"
            if risk == "non-trivial"
            else "prepare evidence packet + human decision"
        ),
    }


def cmd_record(a: argparse.Namespace) -> int:
    repo = Path(a.repo).resolve()
    path = evidence_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    task_family = normalize_family(a.task_family)
    blob = "\n".join([a.task_family, a.verification, a.notes, a.commit, a.files, a.protected])
    if contains_secret(blob):
        print("Refusing to store evidence that looks like a secret/credential.", file=sys.stderr)
        return 3
    if a.outcome == "success" and not a.verified:
        print("A successful reputation event must be current and verified; pass --verified.", file=sys.stderr)
        return 4
    rec = {
        "id": hashlib.sha256((task_family + "\0" + a.operation + "\0" + now() + "\0" + a.outcome).encode()).hexdigest()[:16],
        "ts": now(),
        "task_family": task_family,
        "operation": a.operation,
        "outcome": a.outcome,
        "verified": bool(a.verified),
        "reviewed": bool(a.reviewed),
        "files": csv_list(a.files),
        "verification": a.verification.strip(),
        "rollback": a.rollback,
        "blast_radius": a.blast_radius,
        "protected": csv_list(a.protected),
        "commit": a.commit.strip() or None,
        "notes": a.notes.strip() or None,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print(json.dumps(rec, indent=2))
    return 0


def cmd_assess(a: argparse.Namespace) -> int:
    records = read_records(evidence_path(Path(a.repo).resolve()))
    result = assess(
        records,
        task_family=a.task_family,
        operation=a.operation,
        files=csv_list(a.files),
        blast_radius=a.blast_radius,
        test_stability=a.test_stability,
        rollback=a.rollback,
        protected=csv_list(a.protected),
        novel=a.novel,
        external_side_effects=a.external_side_effects,
        max_history=a.max_history,
    )
    if a.compact:
        h = result["history"]
        print(
            f"risk={result['risk']} confidence={result['confidence']:.3f} "
            f"score={result['evidence_score']:.1f} successes={h['verified_successes']} "
            f"recent_failures={h['recent_failures']} next={result['next']}"
        )
    else:
        print(json.dumps(result, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Task-scoped evidence/reputation engine")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("record", help="record a verified success/failure outcome")
    p.add_argument("--repo", default=".")
    p.add_argument("--task-family", required=True, help="stable task type, e.g. generated-client-refresh")
    p.add_argument("--operation", required=True, choices=["test", "edit", "commit", "push", "merge", "deploy", "production-action"])
    p.add_argument("--outcome", required=True, choices=["success", "failure", "rollback"])
    p.add_argument("--verified", action="store_true")
    p.add_argument("--reviewed", action="store_true")
    p.add_argument("--files", default="", help="comma-separated relevant paths")
    p.add_argument("--verification", default="", help="concise command/result evidence")
    p.add_argument("--rollback", default="unknown", choices=["known", "partial", "unknown", "irreversible"])
    p.add_argument("--blast-radius", default="medium", choices=["low", "medium", "high"])
    p.add_argument("--protected", default="", help="comma-separated protected-domain tags")
    p.add_argument("--commit", default="")
    p.add_argument("--notes", default="")

    p = sp.add_parser("assess", help="score current task against project-local precedent")
    p.add_argument("--repo", default=".")
    p.add_argument("--task-family", required=True)
    p.add_argument("--operation", required=True, choices=["inspect", "plan", "test", "edit", "commit", "push", "merge", "deploy", "production-action"])
    p.add_argument("--files", default="")
    p.add_argument("--blast-radius", default="medium", choices=["low", "medium", "high"])
    p.add_argument("--test-stability", default="unknown", choices=["stable", "flaky", "failing", "unknown"])
    p.add_argument("--rollback", default="unknown", choices=["known", "partial", "unknown", "irreversible"])
    p.add_argument("--protected", default="")
    p.add_argument("--novel", action="store_true")
    p.add_argument("--external-side-effects", action="store_true")
    p.add_argument("--max-history", type=int, default=20)
    p.add_argument("--compact", action="store_true", help="token-efficient one-line digest")
    return ap


def main() -> int:
    a = build_parser().parse_args()
    if a.cmd == "record":
        return cmd_record(a)
    if a.cmd == "assess":
        return cmd_assess(a)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
