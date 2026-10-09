---
name: kx-transition-design
description: Design and implement meaningful route-to-route choreography, overlapping exits and entrances, page mount sequencing and persistent-shell animation. Use for parallel transitions, route navigation, GSAP timelines and complex page entrance/exit effects.
---

# KX Transition Design

## Intent
Create page transitions that express navigation hierarchy and preserve orientation without delaying basic tasks. Start with semantic route relationships and an explicit timeline plan; do not select effects by novelty alone.

## Workflow
1. Draw source/destination visual states and mark primary anchor, metadata, persistent shell, outgoing-only/incoming-only objects.
2. Identify navigation topology: sibling navigation (directional exchange), parent→child (expand/focus), child→parent (contract/restore), environment→environment (spatial movement).
3. Specify a choreography map using **relative anchors** (`start`, `exit-end`, `shared-settled`, `content-ready`) rather than unrelated `setTimeout` calls. Avoid blocking transitions on nonessential resources.
4. Choose technique: single-page Motion presence; browser snapshot View Transition; or live overlapping route mounts where actually supported and justified.
5. Define layering and interaction: ensure outgoing subtree becomes inert when it should no longer accept interaction; incoming subtree receives focus at the correct time; no duplicate accessible navigation landmarks during overlap.
6. Program animation ownership, interruption policy, fallback and cleanup. Test clicks during 20%, 50% and 90% of the timeline, and browser Back.
7. Implement route-specific variants without applying the same elaborate transition to utility actions or sensitive forms.
8. Document precise acceptance tests, including transitions on slow networks, no origin anchor, direct links and reduced motion.

## Choreography constraints
- Prefer transform/opacity; animate masks/clip paths after profiling.
- Use GSAP timeline labels / relative positions when choreography is complex.
- An initial page load is *not* equivalent to a route-to-route transition; do not hide SSR-rendered content forever if JS fails.
- Never break user history via a fake router or replace native links blindly.
- Keep animations short enough for intended context; avoid fixed lockouts when user navigates rapidly.

## Deliverable
A route-pair sheet: states, timeline dependency graph, visual order, DOM stacking strategy, focus/scroll rules, cancel mode, reduced-motion alternative, tests, chosen recipe.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
