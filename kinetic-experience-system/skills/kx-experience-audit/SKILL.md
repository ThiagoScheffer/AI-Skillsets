---
name: kx-experience-audit
description: Audit an existing website or React/Vue/Next/Astro repository for safe immersive-motion upgrades. Use before retrofitting transitions, selecting animation libraries, or changing routing, page layouts or persistent elements.
---

# KX Experience Audit

## Objective
Build an evidence-based inventory of an existing interface. Do not add animation yet. Inspect code and runtime where possible. Output a ranked opportunity map with operational constraints.

## Inspection sequence
1. Read README, project policy files, package.json/lockfiles, dependency constraints, bundler, SSR and deployment configuration.
2. Identify framework/router mode, nested layouts/outlets, navigation APIs, data loaders, streaming/Suspense, auth guards, analytics, scroll restoration, and error boundaries.
3. Map route pairs, user journeys, persistent shells (navbar, global canvas, audio, fixed overlays), and existing state transitions. Include flows reached with Back and deep links.
4. Inspect design system, typography, color tokens, responsive breakpoints, component library, existing animation code, CSS transforms, portals, scroll engines, z-index systems, and GPU scene.
5. Flag sources of animation conflict: libraries animating same properties, fixed/overflow constraints, stacking contexts, dynamic content height, virtualization, reduced-motion rules, race conditions and stale refs.
6. Check baseline behaviours via available tests and browser: focus, link semantics, scroll, skeleton/loading, route errors, keyboard, mobile; record the browser/device and unknowns.
7. Optionally run read-only `scripts/audit_repo.py --repo PATH --out FILE`. This is a heuristic inventory only and does not evaluate semantics of source code.

## Opportunity scoring
Rate each transition seam 1–5 for (a) semantic continuity, (b) experience gain, (c) implementation feasibility, (d) accessibility, (e) cost/complexity (higher is cheaper/safer). Ranking rubric in `references/decision-matrix.md`. Do not present those numbers as measured user impact. Prefer one flagship transition plus a coherent supporting motion language.

## Deliverable
Audit brief with: stack and route topology; current baseline and unknowns; 3–7 opportunities; selected pilot; exclusions; technical and accessibility risks; recommended specialist skills; rollout/rollback plan. Specifically distinguish retrofitting from rewriting.

## Stop conditions
If inspection reveals an unknown SSR/navigation contract, do not silently replace it. Propose a minimal test spike with reversible changes or default to a non-routing interaction. If user asks only for audit, do not edit source code.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
