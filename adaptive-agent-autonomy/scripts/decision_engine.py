#!/usr/bin/env python3
"""One-shot classification + autonomy gate decision."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from autonomy_gate import decide
from evidence_engine import assess, csv_list, evidence_path, read_records


def next_step(decision: str, operation: str) -> str:
    if decision == "AUTO_PROCEED":
        return f"proceed with {operation}, capture outcome, then record verified evidence"
    if decision == "GATED_REVIEW":
        return "run targeted review, resolve findings, re-verify, then re-run the gate"
    if decision == "HUMAN_REQUIRED":
        return f"present the evidence packet and request approval for {operation}; do not perform it yet"
    return "repair missing/failed verification evidence before advancing"


def main() -> int:
    p = argparse.ArgumentParser(description="Assess task reputation and decide the exact next operation")
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
    p.add_argument("--verified", action="store_true", help="current change has fresh verification evidence")
    p.add_argument("--reviewed", action="store_true")
    p.add_argument("--standing-approval", action="store_true")
    p.add_argument("--human-approved", action="store_true")
    p.add_argument("--compact", action="store_true")
    a = p.parse_args()

    protected = csv_list(a.protected)
    records = read_records(evidence_path(Path(a.repo).resolve()))
    assessment = assess(
        records,
        task_family=a.task_family,
        operation=a.operation,
        files=csv_list(a.files),
        blast_radius=a.blast_radius,
        test_stability=a.test_stability,
        rollback=a.rollback,
        protected=protected,
        novel=a.novel,
        external_side_effects=a.external_side_effects,
    )
    decision, gate_reasons = decide(
        assessment["risk"], a.operation, a.verified, a.reviewed,
        protected, a.standing_approval, a.human_approved,
    )
    result = {
        "classification": assessment["risk"],
        "confidence": assessment["confidence"],
        "evidence_score": assessment["evidence_score"],
        "history": assessment["history"],
        "classification_reasons": assessment["reasons"],
        "gate": decision,
        "gate_reasons": gate_reasons,
        "next_step": next_step(decision, a.operation),
        "promotion_candidate": assessment["promotion_candidate"],
    }
    if a.compact:
        print(
            f"class={result['classification']} confidence={result['confidence']:.3f} "
            f"gate={decision} next={result['next_step']}"
        )
    else:
        print(json.dumps(result, indent=2))
    return 0 if decision == "AUTO_PROCEED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
