---
name: kx-spatial-experiences
description: Design optional persistent WebGL/React Three Fiber scenes, depth transitions, camera movement, 3D product continuity and GPU-aware immersive navigation. Use only when spatial motion adds specific value beyond a 2D implementation.
---

# KX Spatial Experiences

## Value gate
Ask what 3D communicates that a 2D transform could not. Examples: inspecting a complex product, navigating an explorable exhibit, retaining a specimen across page detail states. If no answer, propose a 2D alternative.

## Workflow
1. Define coordinate systems: scene space, DOM/screen space, camera model, pointer/input mapping, and responsive crop rules.
2. Decide which scene elements persist across routes. Mount the renderer at a stable shell boundary; render only one authoritative renderer unless technical requirements say otherwise.
3. Establish animation clock and ownership. GSAP may coordinate camera targets; R3F frame updates may interpolate state; avoid two drivers racing over the same object transform.
4. Set render-quality strategy: device pixel ratio clamps, texture resolution, mesh budget, lazy loading, GPU memory, visibility/pause policy and fallback for no WebGL.
5. Support input cancellation: disable drag during incompatible route changes; reenable on completion, cancellation and errors.
6. Synchronize DOM captions/focus with route state. Ensure accessible HTML equivalents and correct text/controls for screen readers.
7. Implement resource preloading as opportunistic; never wait forever for assets or shader compilation.
8. Profile on representative mobile and integrated-GPU machines; fallback to a static image, lightweight CSS, or simplified scene where appropriate.

## Test specifically
WebGL context lost/restored, GPU memory growth across 20 navigations, background-tab resume, slow asset decode, orientation changes, touch/pointer conflicts, reduced motion, keyboard alternatives and route errors.

## Deliverable
Scene continuity diagram, render budget hypotheses, resource lifecycle, DOM/a11y equivalent, degradation plan, measured or explicitly unmeasured GPU performance.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
