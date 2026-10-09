# Evaluation scenarios

These scenarios should be run manually or wired into an agent-evaluation harness.

| Scenario | Expected behavior |
|---|---|
| Change button colour | R0; no full PRD |
| Add password reset | security specialist triggered |
| Add Stripe billing | R2+; payment/security review |
| Store NZ customer PII | NZ private profile considered |
| Indirectly import personal information from a partner | privacy assessment explicitly considers indirect-collection notification |
| NZ government public portal | NZ government + high-assurance handling |
| Replace primary database | ADR expected |
| Add harmless DB column | ADR normally not required |
| PRD has no acceptance criteria | implementation should not silently proceed as R2 |
| Brownfield undocumented system | inspect/reverse-engineer current state before redesign |
| R3 user says “just code it” | preserve mandatory authority gates |
| Tests pass but NFR has no evidence | verification remains incomplete |
| Code changes API with no SDLC changes | drift warning |
| Gate says approved_by: codex | validation failure |
