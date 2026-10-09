---
name: kx-motion-architecture
description: Choose animation engines, renderers, route lifecycle, cancellation policy and CSS property ownership for complex web motion. Use before combining GSAP, Motion, native View Transitions, Hyperkinetic or WebGL in a new or existing app.
---

# KX Motion Architecture

## Architecture decision protocol
1. Classify the interaction: local state, layout reflow, shared identity across views, route replacement, live parallel route orchestration, or persistent GPU scene.
2. Determine whether old and new content must **both remain live**. Native View Transitions use snapshots, not two arbitrarily controllable live React route trees. Motion `AnimatePresence` retains removed React children within component boundaries. Hyperkinetic targets a React Router outlet and is alpha; validate runtime API/version first.
3. Choose minimal engines: CSS/WAAPI for simple feedback; Motion for React layoutId/layout; React Router native View Transition for route snapshots; GSAP timelines for choreography; WebGL/R3F for justified persistent 3D. Avoid a new global router just for effects.
4. Build a property ownership table: element, property, engine, lifecycle, cleanup. **Never let GSAP and Motion both mutate the same `transform` on the same DOM node.** Isolate with separate wrappers or explicit ownership handoffs.
5. Specify navigation state machine: idle → requested → preparing → ready → transitioning → commit → cleanup → idle; cancellation/interrupt and timeout branches at every async boundary.
6. Define anchor identity, reference readiness, resource preload boundaries, scroll/focus authority, document title/announcer responsibility, inert/outgoing rules, stacking and pointer events.
7. Guard reentrancy and continuity: latest-wins or queue policy; never implicitly stack competing in-flight route transitions. Preserve browser history semantics.
8. Build one route-pair spike, profile and test; generalize only after observed success.

## Specific constraints
- GSAP React: use `useGSAP` or `gsap.context` plus `revert()`; scope targets and clean up async callbacks.
- Motion: use `layoutId` within compatible projection/layout contexts; stable identity, matching origin/destination and `AnimatePresence` if exit retention is required.
- Native view transitions: ensure name uniqueness *in each captured view*, scope names to active pair, and provide feature-detected fallbacks.
- Next.js: read current App Router implementation constraints. Do not claim React Router-only APIs work in Next, or route loaders/DOM persistence are supported without a tested adapter.
- GPU: canvas must stay mounted if continuity is needed; synchronize scene state with route without duplicating independent timeline clocks.

## Output
Architecture decision record covering selected engine(s), rejected alternatives, router integration, ownership matrix, lifecycle, interruption strategy, resource/scroll/focus policy, fallback path, migration/rollback and validation plan.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
