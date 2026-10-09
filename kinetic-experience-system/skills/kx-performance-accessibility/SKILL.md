---
name: kx-performance-accessibility
description: Engineer and review accessible, performant motion: reduced motion, route focus, announcements, frame timing, INP, CLS, scroll, cleanup and progressive enhancement. Use before release or whenever complex transitions risk responsiveness.
---

# KX Performance & Accessibility

## Policy
Performance and accessibility are design requirements, not a late-stage optimization task. Define baselines and evidence before attributing outcomes to animation work.

## Accessibility contract
1. Respect `prefers-reduced-motion: reduce`, while retaining meaningful state cues; disable parallax/large spatial displacement rather than simply hiding content.
2. Keep DOM order and semantics; outgoing routes should be inert or otherwise removed from focus/assistive-tech traversal during overlap.
3. Focus target after route navigation: usually new primary heading or main region; preserve user intent for in-page state changes. Announce route title if SPA routing does not already communicate it.
4. Ensure keyboard operation, Escape semantics, touch parity and adequate contrast. Never make motion the sole signal of state.
5. Avoid `display:none` and delayed mounting strategies that permanently conceal SSR content when JS is absent.
6. Follow scroll restoration ownership contract; do not unexpectedly reset scroll during Back or persist `overflow:hidden` after cancellation.

## Performance contract
- Prioritize transform/opacity and minimize layout thrashing. Profile costly filters, clip-path, blur, huge textures and infinite loops.
- LCP, CLS and INP are user-centric signals; target INP <=200ms at p75 and CLS <=0.1 when measured from representative field data. These are *goals*, not results of the recipe.
- Prefer 60 FPS where appropriate, but measure actual frame times across devices and higher-refresh-rate displays rather than promising a fixed FPS.
- Define memory/CPU/GPU and frame-time budgets for expensive routes. Include asset-loading priorities and responsive degradation.
- Run the test matrix: desktop/mobile, reduced motion, rapid navigation, slow network, asset failure, page hidden/resumed, keyboard, direct URL and browser history.

## Deliverable
Constraints table, selected degradations, measured traces/metrics with test conditions, accessibility findings, fixed vs unresolved issues, release pass/fail. Avoid unverifiable numeric claims.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
