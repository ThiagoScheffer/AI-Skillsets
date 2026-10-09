---
name: kx-visual-qa
description: Verify immersive-motion implementations with deterministic screenshots or frame capture, navigation tests, a11y audits, performance traces and visual critique. Use after implementing transitions or when animation appears janky, broken or inconsistent.
---

# KX Visual QA

## Test evidence contract
State what was run and what was not. Capture viewport dimensions, browser/device, reduced-motion setting, network conditions, route pairs and navigation method. No invented frame rates, scores or passing tests.

## Verification protocol
1. Validate static starting and ending views for typography, hierarchy, spacing, contrast and responsive layout.
2. Capture initial, 25%, 50%, 75% and settled states using deterministic clocks/timeline pause where supported. Compare for clipping, jump cuts, scale distortion, opacity collisions and z-index ordering.
3. Evaluate actual motion with recording/frame sequence (screenshots alone do not reveal easing/jitter). Check continuity and reading order.
4. Run functionality matrix: direct URLs, deep links, Back/Forward, click spam, interruption, network delay, rejected asset, route error, window resizing mid-transition, scroll restoration.
5. Run accessibility matrix: keyboard, screen reader where feasible, focus target, reduced motion, touch; verify no duplicate focusable outgoing route.
6. Profile real animation work: long tasks, transform ownership, memory growth, layout shifts and frame budget on representative hardware.
7. Fix issues and retest the *failing path*, then run high-value regression paths.

## Review criteria
Continuity, hierarchy, spatial legibility, rhythm, visual finish, responsiveness, accessibility, system robustness. Separate qualitative design ratings from objective measurements.

## Release thresholds
- Blocking: inaccessible navigation; broken deep link/Back; content hidden after cancellation; loader timeout deadlock; uncontrolled scroll lock; hydration failure.
- Conditional: cosmetic stagger discrepancy on one breakpoint; minor animation simplification on low-end devices. Document and prioritize.

## Deliverable
Filled `templates/qa-report.md`, explicit pass/fail and evidence; list of changed files and known limitations. If no browser is available, supply a reproducible test plan and label status "not executed" rather than passed.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
