from pathlib import Path
import subprocess, sys, tempfile, json

ROOT=Path(__file__).resolve().parents[1]
SKILL=(ROOT/"SKILL.md").read_text()

def test_skill_has_core_contracts():
    for phrase in ["Autonomy is earned", "1,200 tokens", "Human decision", "Learn from outcomes", "superpowers", "evidence_engine.py", "decision_engine.py"]:
        assert phrase in SKILL

def test_references_exist():
    for name in ["autonomy-policy.md","memory-contract.md","token-economy.md","evidence-reputation.md"]:
        assert (ROOT/"references"/name).exists()

def run_gate(*args):
    p=subprocess.run([sys.executable,str(ROOT/"scripts"/"autonomy_gate.py"),*args],capture_output=True,text=True)
    return p, json.loads(p.stdout)

def test_routine_local_verified_auto_proceeds():
    p,j=run_gate("--risk","routine-proven","--operation","commit","--verified")
    assert j["decision"]=="AUTO_PROCEED" and p.returncode==0

def test_push_without_standing_approval_stops():
    p,j=run_gate("--risk","routine-proven","--operation","push","--verified")
    assert j["decision"]=="HUMAN_REQUIRED" and p.returncode!=0

def test_explicit_approval_unlocks_push_but_not_missing_verification():
    p,j=run_gate("--risk","routine-proven","--operation","push","--verified","--human-approved")
    assert j["decision"]=="AUTO_PROCEED" and p.returncode==0
    p,j=run_gate("--risk","routine-proven","--operation","push","--human-approved")
    assert j["decision"]=="BLOCKED" and p.returncode!=0

def test_protected_domain_escalates_mutation():
    p,j=run_gate("--risk","routine-proven","--operation","edit","--protected","auth")
    assert j["decision"]=="HUMAN_REQUIRED"

def test_high_risk_testing_is_allowed():
    p,j=run_gate("--risk","novel-high-risk","--operation","test","--protected","auth")
    assert j["decision"]=="AUTO_PROCEED" and p.returncode==0

def test_memory_rejects_unverified_and_secret():
    with tempfile.TemporaryDirectory() as d:
        script=str(ROOT/"scripts"/"memory_store.py")
        p=subprocess.run([sys.executable,script,"record","--repo",d,"--kind","lesson","--summary","x","--evidence","guess"],capture_output=True,text=True)
        assert p.returncode==4
        p=subprocess.run([sys.executable,script,"record","--repo",d,"--kind","lesson","--summary","api_key=sk_abcdefghijklmnopqrstuvwxyz","--evidence","human","--human-confirmed"],capture_output=True,text=True)
        assert p.returncode==3
