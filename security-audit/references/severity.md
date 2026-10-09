# Severity Method

Use `Critical`, `High`, `Medium`, `Low`, or `Informational` based on actual likelihood and impact. Vulnerability class alone does not determine severity.

## Evaluate likelihood

Consider:

- unauthenticated vs authenticated;
- required role/privilege;
- user interaction;
- attacker knowledge/control of identifiers;
- feature flags or insecure configuration required;
- attack complexity/race/preconditions;
- whether a vulnerable endpoint is internet/client reachable;
- exploit reliability.

## Evaluate impact

Consider:

- cross-tenant or cross-user confidentiality;
- unauthorized modification/deletion;
- privilege escalation/admin capability;
- credential privilege and blast radius;
- stored/persistent execution in privileged users' sessions;
- number/sensitivity of affected records;
- business-critical actions;
- persistence and recoverability.

## Practical calibration

### Critical

Reserve for plausible compromise with exceptional blast radius: systemic unauthenticated tenant bypass, exposed highly privileged production credential with broad control, direct admin takeover, or equivalent impact.

### High

Serious cross-tenant data access/modification, privilege escalation to powerful roles, privileged credential exposure, or persistent XSS in high-value/admin contexts with realistic exploitation.

### Medium

Material but narrower authorization/data exposure, constrained stored/reflected XSS, or secret/config issue requiring meaningful preconditions.

### Low

Limited impact/exploitability, defense-in-depth gaps with a concrete security consequence, or narrow issues requiring unusual conditions.

### Informational

Verified observations without a directly exploitable security impact. Do not use Informational to hide speculative vulnerabilities; put unresolved hypotheses in Manual Follow-up instead.

## CVSS

Do not emit a CVSS number unless the repository evidence supports a complete defensible CVSS v4.0 vector. Avoid false numerical precision.

Always state important severity assumptions and exploitability conditions.
