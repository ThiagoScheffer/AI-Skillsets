---
name: kx-orchestrator
description: Coordinate end-to-end design, implementation and validation of motion-native web experiences in new or existing websites. Use when asked to make a site immersive, innovative, cinematic, smooth, or to introduce complex animated navigation across routes.
---

# KX Orchestrator — Motion-native experience delivery

## Trigger and goal
Use for multi-step requests: new motion-native websites, existing-site retrofits, synchronized route transitions, cinematic UI upgrades, or competing design directions. Delegate distinct subproblems to `kx-*` specialists as needed. **Do not equate more animation with better design.**

## Mode classifier
1. **RETROFIT:** existing repository; stabilize stack/functionality; prefer one pilot route pair.
2. **GREENFIELD:** idea or brief without a repo; define IA, visual direction, state topology and data constraints before stack.
3. **FOCUSED:** single component, route pair or UI behaviour; keep the change local.
4. **EXPLORATION:** user requests alternatives or creative ideation; use `kx-creative-exploration`.

When the user gives no mode, infer it from their request and existing files; explain your assumption briefly. Don't block safe progress for preferences that can be chosen from context.

## Mandatory workflow
1. **Discover:** read project guidance, package manifests, router topology, code conventions, deployment/SSR model, tests, a11y constraints and current animation usage. For greenfield, infer goals, audience, content and experience trajectory. Delegate repo inspection to `kx-experience-audit`.
2. **Diagnose:** identify navigation *relationships* (parent→child, sibling→sibling, overview→detail, state→state, environment→environment). Prioritize seams by user benefit, visual continuity, cost and risk.
3. **Art-direct:** establish typography, grid, color/contrast, density, focal object(s), spatial metaphors and motion grammar. If the brief is open, use three deliberately distinct directions, not three variations of the same fade.
4. **Blueprint:** create valid JSON following `.kinetic-experience/schemas/motion-blueprint.schema.json` (or source `schemas/`), including route/state identities, source/target anchors, motion intent, ownership, fallbacks, interruptions, focus, reduced motion and acceptance tests. Validate with `scripts/validate_blueprint.py`.
5. **Architect:** choose the simplest renderer and suitable router adapter. Prefer CSS/native/Motion for ordinary transitions; GSAP for demanding sequencing; GPU for justified persistent spatial interaction. Enforce property ownership. Never install multiple engines just because available.
6. **Implement in slices:** render correct static destination first; add one high-value semantic transition; wire lifecycle and cancellation; maintain direct-link and no-JS viability where applicable; scale to additional routes after the pilot passes.
7. **Verify:** functional tests, keyboard/focus, direct link, browser history, reduced motion, rapid navigation, slow assets, layout stability and real device/browser profiling when available. Use `kx-visual-qa`.
8. **Deliver:** explain user-visible design improvements, file changes, dependencies, test evidence, remaining risks, and how to alter timing/motion profiles.

## Hard gates
**Gate 1—Intent:** can you explain how each significant transition improves continuity, hierarchy, state feedback, orientation, or storytelling? If not, remove it.

**Gate 2—Feasibility:** can the chosen router support the requested lifecycle? Distinguish *true live DOM parallel mounts* from snapshots or sequential route changes. Do not claim Next.js implements Hyperkinetic semantics automatically.

**Gate 3—Ownership:** each animated property has exactly one driver per frame; route/scroll/focus ownership is explicit.

**Gate 4—Resilience:** interrupted navigation and failed resources recover to working UI; exit cleanup cannot leave a stale overlay or lock.

**Gate 5—Evidence:** tests run, screenshots inspected and performance values measured (or explicitly not available).

## Routing to specialists
- Audit → `kx-experience-audit`
- Visual grammar → `kx-creative-direction`
- Engines/lifecycle → `kx-motion-architecture`
- Parallel pages → `kx-transition-design`
- Shared object → `kx-morphing-layout`
- GPU persistence → `kx-spatial-experiences`
- Local UI state → `kx-microinteractions`
- Constraints → `kx-performance-accessibility`
- Browser proof → `kx-visual-qa`
- Unclear artistic direction → `kx-creative-exploration`

## Expected handoff
Mode; constraints; Motion Blueprint; selected design direction; concise ownership table; acceptance tests; actual verification results; rollback and maintenance notes. For a task limited to analysis, stop before code changes.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
