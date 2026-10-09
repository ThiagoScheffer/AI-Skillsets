---
name: kx-creative-exploration
description: Explore and compare multiple distinctive immersive-interface concepts before implementation. Use when a user asks for creative options, innovative page transitions, nontraditional navigation, or art-direction ideation.
---

# KX Creative Exploration

## Objective
Generate genuinely different experience concepts grounded in user intent and stack constraints. Avoid producing three aesthetic names for the same fade/slide transition.

## Workflow
1. Identify audience and purpose, journey topology, anchor objects, interaction frequency, content density, brand restrictions and performance/compatibility constraints.
2. Draft exactly three defensible directions unless user requests a different number:
   - **Continuity-first:** morph, identity persistence, overview→detail.
   - **Spatial-first:** camera/depth/plane movement, only if product justifies it.
   - **Editorial-first:** masks, typography, rhythm, layered narrative.
3. For each direction provide: visual concept, motion grammar, flagship interaction story (3–5 beats), stack fit, technical risks, reduced-motion variant, expected complexity and likely tradeoffs.
4. Score 1–5 using explicit weights for relevance, attention guidance, originality, feasibility, accessibility and performance cost. Treat scores as design judgments, not empirical user data.
5. Select the strongest direction or a justified hybrid. Warn when hybridization compromises consistency.
6. If code requested and environment permits, prototype a small representative seam; compare using real browser observations before generalizing.

## Anti-patterns
- Same effect at different speeds as three concepts.
- Citing Awwwards-like novelty as proof of usability.
- Claiming GPU effects are required when 2D can deliver.
- Providing unreachable desktop-only effects without mobile/fallback design.

## Output
Three option briefs and a decision table; chosen direction; why the others lost; pilot route-pair plan; signature and quiet-zone motion grammar.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
