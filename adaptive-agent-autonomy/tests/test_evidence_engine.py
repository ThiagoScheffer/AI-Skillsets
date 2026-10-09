from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "scripts" / "evidence_engine.py"
DECISION = ROOT / "scripts" / "decision_engine.py"


def run_json(script, *args):
    p = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)
    return p, json.loads(p.stdout)


def record_success(repo, family="generated-refresh", reviewed=True):
    args = [
        "record", "--repo", repo, "--task-family", family,
        "--operation", "commit", "--outcome", "success", "--verified",
        "--blast-radius", "low", "--rollback", "known",
        "--files", "src/generated/client.ts",
        "--verification", "focused tests exit 0",
    ]
    if reviewed:
        args.append("--reviewed")
    p = subprocess.run([sys.executable, str(EVIDENCE), *args], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


def record_failure(repo, family="generated-refresh"):
    p = subprocess.run([
        sys.executable, str(EVIDENCE), "record", "--repo", repo,
        "--task-family", family, "--operation", "commit",
        "--outcome", "failure", "--blast-radius", "low",
        "--rollback", "known", "--files", "src/generated/client.ts",
        "--verification", "focused tests failed",
    ], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


def assess(repo, *extra):
    base = [
        "assess", "--repo", repo, "--task-family", "generated-refresh",
        "--operation", "commit", "--blast-radius", "low",
        "--test-stability", "stable", "--rollback", "known",
        "--files", "src/generated/client.ts",
    ]
    return run_json(EVIDENCE, *(base + list(extra)))


def test_three_verified_successes_can_earn_routine():
    with tempfile.TemporaryDirectory() as d:
        for _ in range(3):
            record_success(d)
        p, data = assess(d)
        assert p.returncode == 0
        assert data["risk"] == "routine-proven"
        assert data["history"]["verified_successes"] == 3
        assert data["evidence_score"] >= 82.0


def test_recent_failure_demotes_routine():
    with tempfile.TemporaryDirectory() as d:
        for _ in range(3):
            record_success(d)
        record_failure(d)
        _, data = assess(d)
        assert data["risk"] == "non-trivial"
        assert data["history"]["recent_failures"] >= 1


def test_protected_domain_forces_high_risk():
    with tempfile.TemporaryDirectory() as d:
        for _ in range(5):
            record_success(d)
        _, data = assess(d, "--protected", "auth")
        assert data["risk"] == "novel-high-risk"


def test_unverified_success_is_rejected():
    with tempfile.TemporaryDirectory() as d:
        p = subprocess.run([
            sys.executable, str(EVIDENCE), "record", "--repo", d,
            "--task-family", "x", "--operation", "commit",
            "--outcome", "success"
        ], capture_output=True, text=True)
        assert p.returncode == 4


def test_decision_engine_requires_push_approval_even_when_routine():
    with tempfile.TemporaryDirectory() as d:
        for _ in range(3):
            record_success(d)
        p, data = run_json(
            DECISION,
            "--repo", d, "--task-family", "generated-refresh",
            "--operation", "push", "--files", "src/generated/client.ts",
            "--blast-radius", "low", "--test-stability", "stable",
            "--rollback", "known", "--verified", "--reviewed"
        )
        assert data["classification"] == "routine-proven"
        assert data["gate"] == "HUMAN_REQUIRED"
        assert p.returncode != 0


def test_explicit_human_approval_unlocks_verified_push():
    with tempfile.TemporaryDirectory() as d:
        for _ in range(3):
            record_success(d)
        p, data = run_json(
            DECISION,
            "--repo", d, "--task-family", "generated-refresh",
            "--operation", "push", "--files", "src/generated/client.ts",
            "--blast-radius", "low", "--test-stability", "stable",
            "--rollback", "known", "--verified", "--reviewed", "--human-approved"
        )
        assert data["gate"] == "AUTO_PROCEED"
        assert p.returncode == 0
