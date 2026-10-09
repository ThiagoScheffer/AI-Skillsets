---
name: kx-morphing-layout
description: Implement shared-element transitions, layout morphing, FLIP, card-to-detail, thumbnail-to-hero, SVG morphs and semantic continuity between UI states or routes. Use when an element should visually transform rather than disappear and reappear.
---

# KX Morphing & Layout Continuity

## Objective
Make a real semantic object retain identity across interface states. A successful morph feels like a transformation of the same thing rather than unrelated entrance and exit animations.

## Procedure
1. Select a stable business identity (product ID, project slug, gallery ID), not an array index or ephemeral DOM reference.
2. Locate origin and destination anchors, measure content/geometry once at an appropriate phase, and define behaviour when origin is absent (direct link, filtered list, virtualized offscreen item).
3. Choose implementation: Motion `layoutId`, FLIP transforms, temporary visual overlay, native View Transition names, SVG path interpolation, or a GPU shader only when justified.
4. Declare transition ownership: wrapper for shared transform; child for local opacity/scale; never concurrently animate same style property with two engines.
5. Protect intrinsic content: aspect ratios, object-fit, text wrapping, image load/decoding, clipped corners, dynamic sizes and fonts.
6. Reverse mapping on Back only when origin remains valid; otherwise fall back to a graceful destination entrance and restore logical focus/scroll.
7. Test changing grid columns, 320px width, device rotation, long titles, reduced motion and interrupted morph.

## Avoid
- Fake continuity by animating unrelated objects with similar colors.
- Duplicate visible identical IDs or interactive controls during transition.
- Using `layoutId` across scopes/trees where the chosen engine cannot see both elements.
- Retaining offscreen source pages indefinitely to preserve a morph.

## Deliverable
Identity map; geometry/measurement strategy; engine and ownership; source absent policy; forward/reverse fallbacks; accessibility focus change; edge-case test results.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
