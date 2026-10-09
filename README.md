<div align="center">

# AI Engineering Skills Library

### Turning AI-assisted development into a disciplined engineering process.

A collection of reusable **AI agent skills, engineering playbooks, and quality gates** spanning the software lifecycle — from product discovery and system design to secure implementation, user experience, and release readiness.

![Skill definitions](https://img.shields.io/badge/Skill%20definitions-27-176B87?style=flat-square)
![Skill systems](https://img.shields.io/badge/Skill%20systems-6-176B87?style=flat-square)
![Approach](https://img.shields.io/badge/Approach-Evidence--driven-303F52?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Human--governed%20AI-303F52?style=flat-square)

**[Explore the systems](#the-six-skill-systems)** · **[See how they work together](#how-the-pieces-fit-together)** · **[For recruiters](#for-recruiters-and-engineering-teams)**

</div>

---

## The 30-second overview

**This repository explores a central engineering question:** How can AI coding agents produce software work that is not only faster, but also *traceable, reviewable, secure, and maintainable*?

The answer proposed here is a **modular set of agent skills**: structured instructions that guide compatible coding agents through defined tasks, evidence requirements, checks, and decision points. Instead of relying on a single “build the whole app” prompt, the skills separate responsibilities and introduce explicit verification and human-approval boundaries.

| What is here | Why it matters |
| :--- | :--- |
| **6 complementary skill systems** | Covers engineering process, autonomous-agent governance, API contracts, security, UX, and advanced web interactions. |
| **27 individual `SKILL.md` definitions** | Breaks broad tasks into focused, reusable agent capabilities. |
| **Risk-based workflows** | Gives simple changes lightweight treatment while escalating consequential changes. |
| **Evidence-led quality checks** | Distinguishes actual verification from heuristics, assumptions, and generated claims. |
| **Portable design** | Uses documentation-led skills, with guidance for environments such as Codex and Claude Code where supported. |

> **In plain English:** These are instructions and supporting tools for getting AI coding assistants to work more like a responsible engineering team: understand the problem, plan, implement carefully, test, explain trade-offs, and know when to ask a human.

## The six skill systems

| System | Main idea | Engineering value |
| :--- | :--- | :--- |
| **[01 · Enterprise SDLC Agent Skills](enterprise-sdlc-agent-skills/README.md)** | Organise software work from discovery to operations with traceability and risk-based gates. | Fewer gaps between requirements, implementation, testing, and release. |
| **[02 · Adaptive Agent Autonomy](adaptive-agent-autonomy/README.md)** | Give agents permission to act based on verified project evidence, not blanket trust. | More controlled automation, explicit approvals, and reusable project memory. |
| **[03 · Security Audit](security-audit/README.md)** | Inspect application source code for concrete, evidence-supported security weaknesses. | Actionable security reports rather than unverified scanner alerts. |
| **[04 · API Check](api-check/SKILL.md)** | Review and design API contracts for consistency, semantics, compatibility, and security. | More reliable integrations and clearer backend contracts. |
| **[05 · UI/UX Project Auditor](uiux-project-auditor/SKILL.md)** | Evaluate user journeys, interface states, accessibility, trust, and robustness in real projects. | Better usability and fewer design problems hidden behind visual polish. |
| **[06 · Kinetic Experience System](Kinetic%20Experience%20System/kinetic-experience-system/README.md)** | Design intentional, motion-native interfaces with performance and accessibility guardrails. | Richer interactive experiences without sacrificing fundamental web behaviour. |

### 01 / Enterprise SDLC Agent Skills

**From product idea to accountable delivery.**

This system structures an AI-assisted software development lifecycle instead of treating implementation as an isolated coding exercise. It establishes product intent, derives verifiable requirements, documents architecture, plans implementation, and tracks verification, release, and operational readiness.

**Core ideas**
- Persistent project artefacts under `.sdlc/`, including requirements, architecture decisions, security work, test plans, and release state.
- Traceability from business objectives and acceptance criteria to tasks and verification evidence.
- Risk tiers **R0–R3**: from trivial edits to high-assurance work requiring explicit human approvals.
- Policy overlays for baseline, AI-enabled, high-assurance, **New Zealand private-sector**, and **New Zealand government** contexts.
- Structured schemas, templates, and validation helpers to check artefact integrity and detect gaps or drift.

<details>
<summary><strong>View the 12 SDLC skills</strong></summary>

`product-discovery` · `prd-authoring` · `requirements-engineering` · `product-design-ux` · `system-design` · `architecture-decisions` · `secure-software-engineering` · `implementation-planning` · `software-implementation` · `verification-release` · `reliability-operations` · `sdlc-orchestrator`

</details>

**Read more:** [Enterprise SDLC documentation](enterprise-sdlc-agent-skills/README.md)

### 02 / Adaptive Agent Autonomy

**Autonomy should be earned — and scoped to the task.**

This system explores how an AI agent can operate efficiently without being given unrestricted authority. It combines compact project memory, outcome-based evidence, operation-level gates, and escalation to human review.

**Core ideas**
- Trust derives from **verified outcomes in the current project and task family**, not a permanent reputation score.
- Decisions distinguish routine work from actions that require review, approval, or blocking.
- Compact context retrieval limits unnecessary token usage while preserving relevant knowledge.
- Failures, uncertain rollback, high-impact changes, and stale evidence reduce permissible autonomy.
- Sensitive actions such as deployment, migration, permission changes, and financial operations have explicit human boundaries.

**Read more:** [Adaptive Agent Autonomy](adaptive-agent-autonomy/README.md)

### 03 / Security Audit

**A code pattern is not automatically a vulnerability.**

This skill proposes a defensible, source-based security review: first discover the actual technology and trust model, then map attack surfaces, validate candidate findings, and document them with precise evidence.

**Five review areas:** tenant/owner isolation; server-side authorisation; **IDOR/BOLA**; exposed secrets; and **XSS**.

**Core ideas**
- Clearly separate *candidate findings* from verified vulnerabilities.
- Assess server-side security controls, not just hidden frontend buttons or route guards.
- Record reviewed protections and audit coverage, including areas where no finding exists.
- Produce structured audit results, remediation guidance, GitHub issue content, and a reproducible **Portuguese-language PDF report**.
- Keep the process defensive and avoid invasive production testing or exposure of actual credentials.

**Read more:** [Security Audit documentation](security-audit/README.md)

### 04 / API Check

**Treat an API as a contract, not just a set of endpoints.**

This skill addresses API design and review across **REST/OpenAPI, GraphQL, and gRPC**, with protocol selection based on use case rather than fashion.

**Core ideas**
- Correct HTTP semantics, resource modelling, idempotency, status codes, errors, filtering, and pagination.
- Compatibility and versioning decisions that account for existing clients.
- Authentication and authorisation reviews, including JWT, bearer-token semantics, cookies, and token lifecycles.
- OpenAPI checks as supporting evidence — never a substitute for semantic or security review.
- Prioritised findings with concrete fixes and validation expectations.

**Read more:** [API Check skill](api-check/SKILL.md)

### 05 / UI/UX Project Auditor

**Audit the real user journey, not just the screenshot.**

This skill combines product thinking, interface inspection, design-system consistency, accessibility, privacy, and security-aware UX review. It starts with what users are trying to accomplish and examines how the product performs under realistic conditions.

**Core ideas**
- Evaluate complete flows, friction, information hierarchy, and recovery from errors.
- Check states often overlooked in mockups: loading, empty, failed, disabled, keyboard, responsive, and permission-dependent states.
- Review accessibility and contrast across relevant themes and component states.
- Challenge misleading conversion tactics and distinguish observations from hypotheses.
- Separate **audit-only** work from requested fixes, and verify implemented changes.

**Read more:** [UI/UX Project Auditor skill](uiux-project-auditor/SKILL.md)

### 06 / Kinetic Experience System (KX)

**Make motion meaningful, accessible, and technically controlled.**

KX is a set of specialist skills for designing and engineering immersive web experiences. Its central concept, **Semantic Motion Mapping**, asks how related interface states should transform into one another *before* choosing animation libraries or writing transitions.

**Core ideas**
- Plan transformations using a **Motion Blueprint**: which elements persist, morph, enter, exit, or stay interactive.
- Choose between CSS, native View Transitions, Motion, GSAP, and optional 3D/WebGL based on technical need.
- Handle interrupted navigation, browser Back, reduced-motion preferences, route lifecycle, and keyboard accessibility.
- Apply specialised skills for creative direction, transitions, layout morphing, microinteractions, spatial interfaces, performance, and visual QA.
- Provide framework-oriented guidance for React Router, Next.js, Vue/Nuxt, Astro, and vanilla web projects.

<details>
<summary><strong>View the 11 KX skills</strong></summary>

`kx-orchestrator` · `kx-experience-audit` · `kx-creative-exploration` · `kx-creative-direction` · `kx-motion-architecture` · `kx-transition-design` · `kx-morphing-layout` · `kx-microinteractions` · `kx-spatial-experiences` · `kx-performance-accessibility` · `kx-visual-qa`

</details>

**Read more:** [Kinetic Experience System](Kinetic%20Experience%20System/kinetic-experience-system/README.md)

---

## How the pieces fit together

These are **complementary systems**, not one monolithic agent. A project can use the full lifecycle or call a single specialist when the task is narrow.

```text
                         PRODUCT IDEA / EXISTING REPOSITORY
                                        │
                                        ▼
                       ENTERPRISE SDLC · DISCOVER & PLAN
                     Problem → Requirements → Architecture
                                        │
                  ┌─────────────────────┼─────────────────────┐
                  ▼                     ▼                     ▼
             API CHECK              SECURITY AUDIT      UI/UX AUDITOR
          Contracts & auth        Verified risk review   Flows & access
                  └─────────────────────┼─────────────────────┘
                                        │
                                        ▼
                         IMPLEMENTATION & VERIFICATION
                                        │
                                        ▼
                      KINETIC EXPERIENCE (when warranted)
                        Motion design → Build → Visual QA
                                        │
                                        ▼
                            RELEASE & OPERATIONS

          ADAPTIVE AGENT AUTONOMY: evidence, memory, and approval
                    boundaries across applicable steps
```

### Shared engineering principles

| Principle | What it means in practice |
| :--- | :--- |
| **Evidence over confidence** | Do not claim tests passed, vulnerabilities exist, or performance improved without relevant evidence. |
| **Human authority for consequential actions** | Approval gates matter for sensitive, destructive, financial, or production-affecting operations. |
| **Traceability over chat memory** | Preserve important requirements, decisions, verification, and project state in explicit artefacts. |
| **Proportionate process** | Match review and documentation effort to the change's risk and impact. |
| **Accessibility and security by design** | Address both during design and implementation rather than attaching them at the end. |
| **Specialists over one giant prompt** | Route work to focused capabilities with clear scope and expected outputs. |

## Example ways to use the collection

**Scenario A — Build a new product responsibly**  
Use the SDLC skills to define the problem, establish requirements, document architecture decisions, plan delivery, and gather release evidence. Add API Check for interface contracts and Security Audit for sensitive functionality.

**Scenario B — Review and strengthen an existing application**  
Run a UX or security-focused assessment, rank findings by evidence and impact, implement only the approved corrections, and verify the result. Use Adaptive Agent Autonomy to control which actions can be automated.

**Scenario C — Improve a web experience without breaking it**  
Use KX to inspect the existing navigation and rendering architecture, propose a motion blueprint, implement a justified interaction, and assess accessibility, responsiveness, and visual behaviour.

---

## For recruiters and engineering teams

This collection is a **portfolio of engineering approaches**, with an emphasis on turning AI assistance into reliable workflows rather than treating code generation as the end result.

It highlights the following areas of technical thinking:

| Area | What the work demonstrates |
| :--- | :--- |
| **Software engineering process** | Requirements decomposition, architecture decisions, delivery planning, verification, and operational thinking. |
| **AI agent design** | Task routing, bounded autonomy, context management, agent instructions, and human-in-the-loop controls. |
| **Quality and security** | Threat modelling, contract reviews, evidence standards, authorisation boundaries, and risk prioritisation. |
| **Product and frontend engineering** | UX evaluation, accessible interaction design, motion architecture, and progressive enhancement. |
| **Tooling and developer experience** | Portable `SKILL.md` conventions, structured schemas, templates, Python utilities, and repeatable checks. |
| **Pragmatic decision-making** | Explicit trade-offs, risk-adjusted workflow depth, and recognition of what automated checks cannot prove. |

**The key idea:** AI should accelerate engineering judgment and execution, **not replace the evidence and accountability that make software dependable**.

### What this repository is — and is not

- **It is** a library of documented agent workflows and supporting project artefacts, with some packages containing scripts, schemas, examples, and tests.
- **It is not** a single executable application, a universal autonomous agent, or proof that a particular software product has passed a production audit.
- **Validation is contextual:** provided checks can validate specified structures or help discover issues; a real deployment still needs integration tests, security assessment, browser/device testing where relevant, and human review.

## Repository navigation

```text
.
├── enterprise-sdlc-agent-skills/    # Product-to-production workflow
├── adaptive-agent-autonomy/         # Evidence-based agent autonomy
├── security-audit/                  # Source-driven security review
├── api-check/                       # API contracts and review
├── uiux-project-auditor/            # Product and interface auditing
└── Kinetic Experience System/
    └── kinetic-experience-system/   # Motion-native web experiences
```

**Where to begin:** Start with the system that matches your problem. Each linked package contains its own scope and, where available, implementation guidance, templates, and usage instructions. There is **no single installation command for the whole collection**.

---

<div align="center">

**Build faster. Verify carefully. Keep humans accountable.**

<sub>Documentation-oriented overview of the ideas and artefacts included in this repository.</sub>

</div>
