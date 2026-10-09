#!/usr/bin/env python3
"""Deterministic enforcement helper for adaptive-agent-autonomy."""
from __future__ import annotations
import argparse, json

PROTECTED = {
    "auth", "authentication", "authorization", "permissions", "identity",
    "secrets", "money", "billing", "payments", "migration", "migrations",
    "destructive-data", "production", "security", "legal", "compliance",
    "irreversible", "privacy", "dns", "certificates"
}
REMOTE = {"push", "merge", "deploy", "production-action"}
SAFE = {"inspect", "plan", "test"}
CONSEQUENTIAL = {"commit", *REMOTE}


def decide(risk: str, operation: str, verified: bool, reviewed: bool,
           protected: list[str], standing_approval: bool,
           human_approved: bool = False) -> tuple[str, list[str]]:
    reasons: list[str] = []
    protected_set = {p.strip().lower() for p in protected if p.strip()}
    hit = sorted(protected_set & PROTECTED)
    if hit:
        risk = "novel-high-risk"
        reasons.append("protected domain: " + ", ".join(hit))

    # Inspection, planning and verification are allowed even for risky work;
    # the gate controls consequential mutation/advancement, not analysis.
    if operation in SAFE:
        return "AUTO_PROCEED", reasons + [f"{operation} is a non-consequential verification step"]

    if operation in CONSEQUENTIAL and not verified:
        return "BLOCKED", reasons + ["current verification evidence is required"]

    if risk == "novel-high-risk":
        if not human_approved:
            return "HUMAN_REQUIRED", reasons + ["novel/high-risk work requires human decision"]
        return "AUTO_PROCEED", reasons + ["human approved this high-risk operation after current verification"]

    if risk == "non-trivial":
        if operation in {"commit", "push", "merge", "deploy", "production-action"} and not reviewed:
            return "GATED_REVIEW", reasons + ["targeted review required before advancing project state"]
        if operation in REMOTE and not (standing_approval or human_approved):
            return "HUMAN_REQUIRED", reasons + [f"{operation} lacks bounded standing approval or explicit human approval"]
        return "AUTO_PROCEED", reasons + ["verification/review gates satisfied"]

    if risk == "routine-proven":
        if operation in REMOTE and not (standing_approval or human_approved):
            return "HUMAN_REQUIRED", reasons + [f"{operation} requires standing or explicit human approval"]
        return "AUTO_PROCEED", reasons + ["routine/proven gate satisfied"]

    return "BLOCKED", reasons + ["unknown risk class"]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--risk", required=True, choices=["routine-proven", "non-trivial", "novel-high-risk"])
    p.add_argument("--operation", required=True, choices=["inspect", "plan", "test", "edit", "commit", "push", "merge", "deploy", "production-action"])
    p.add_argument("--verified", action="store_true")
    p.add_argument("--reviewed", action="store_true")
    p.add_argument("--protected", default="", help="comma-separated protected-domain tags")
    p.add_argument("--standing-approval", action="store_true")
    p.add_argument("--human-approved", action="store_true", help="explicit approval for this exact operation/change")
    a = p.parse_args()
    decision, reasons = decide(a.risk, a.operation, a.verified, a.reviewed,
                               a.protected.split(","), a.standing_approval,
                               a.human_approved)
    print(json.dumps({"decision": decision, "reasons": reasons}, indent=2))
    return 0 if decision == "AUTO_PROCEED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
