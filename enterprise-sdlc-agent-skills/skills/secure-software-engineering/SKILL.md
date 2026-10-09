---
name: secure-software-engineering
description: Use for security and privacy requirements, threat modelling, trust boundaries, sensitive-data analysis, controls, abuse cases, security verification, and profile-specific NZ privacy/NZ government security overlays.
---

# Secure Software Engineering

Integrate security and privacy into requirements and design. Do not treat scanning as a substitute for threat analysis.

## Analyze

- assets and sensitive data
- actors and privilege levels
- trust boundaries
- authentication/session model
- authorization and tenant isolation
- external inputs/integrations/webhooks
- secrets and key management
- file/content handling
- injection/output risks
- data lifecycle/retention
- logging/audit exposure
- dependency/supply-chain risk
- abuse/misuse cases
- recovery/security failure modes

## Canonical artifacts

- `.sdlc/security/threat-model.md`
- `.sdlc/security/data-classification.md`
- `.sdlc/security/privacy-assessment.md`
- `.sdlc/security/security-requirements.yaml`

## Identifiers

- `THR-###`
- `CTRL-###`
- `TEST-###` for verification

Use `templates/THREAT-MODEL.md`.

## Profiles

If a project profile is selected, load the matching material under `/profiles`. Profiles add obligations; they do not replace engineering judgment.

Never claim compliance solely because a template is filled out.
