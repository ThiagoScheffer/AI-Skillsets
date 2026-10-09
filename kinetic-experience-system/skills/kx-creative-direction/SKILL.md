---
name: kx-creative-direction
description: Design a visual and kinetic art direction for immersive interfaces, including typography, composition, color, spatial language, attention choreography and restraint. Use when a page looks generic or its transitions need a coherent visual identity.
---

# KX Creative Direction

## Core principle
Motion is part of visual identity. An excellent experience is a designed progression of attention, not an anthology of effects. Produce differentiated art direction consistent with audience, brand, information density and interaction criticality.

## Process
1. Define the experience objective: orientation, product comprehension, emotional immersion, conversion, storytelling or workflow speed. Separate business outcomes from aesthetic preference.
2. Identify anchor objects and visual hierarchy on each screen. Record what persists, what morphs, what is replaced and where attention should end up.
3. Define a visual grammar: type scale and kinetic type behavior; grid and whitespace; color/contrast; surfaces; image aspect ratios; mask/shape language; depth and layering; visual cadence.
4. Define a motion grammar: entrance/exit direction, speed family, easing family, spacing/stagger, overlap rules, hero vs utility component behavior, mobile adaptation. Avoid one-size-fits-all timings.
5. Create a **hero moment**, **supporting transitions**, and **quiet zones**. The hero moment earns prominence; routine controls should stay fast and predictable.
6. Test static screens first. Motion must not rescue weak typography, unstructured layouts, or low contrast.
7. Evaluate at three breakpoints, keyboard focus, content expansion and a reduced-motion rendition.

## Direction quality gate
Does each signature transition communicate a relationship, guide attention or intentionally create character? Does the motion work in reverse? Do timing and dynamic effects preserve task speed? If an effect fails these tests, simplify it.

## Output
A creative-direction sheet: 4–6 adjectives with specific meanings, reference-free visual description, type/spacing/color tokens, primary object continuity plan, spatial layers, 3 motion rules, 3 anti-patterns, device-specific changes and a motion intensity profile (subtle/expressive/cinematic).

For creative exploration, coordinate with `kx-creative-exploration`; avoid copying third-party designs or unlicensed assets.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
