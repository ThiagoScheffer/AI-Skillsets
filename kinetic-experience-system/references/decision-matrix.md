# Decision matrix: which motion deserves to ship?

Use this as a **comparative design tool**, not an empirical metric. All scores are human/agent judgments unless tied to actual tests.

## Opportunity ranking

Rate 1–5 (5=best) for semantic continuity C, attention guidance A, context fit F, implementation feasibility I, accessibility feasibility X, and operational cost K (5=low burden). Proposed weighted score:

`score = .25*C + .20*A + .20*F + .15*I + .10*X + .10*K`

Exclude any proposal that violates a release-blocking a11y/functionality invariant, regardless of score.

## Animation value test

A significant effect must directly improve at least one: **orientation**, **hierarchy**, **attention**, **state feedback**, **brand expression**, or **storytelling**. If none, remove the effect. High task frequency favors subtle motion.

## Default duration hypotheses (not standards)

| Profile | Typical route change | Intended context |
|---|---|---|
| Subtle | 120–350ms | Dashboards, tools, information-heavy UI |
| Expressive | 250–800ms | Product storytelling, portfolio, premium commerce |
| Cinematic | 500–1400ms (rare, skippable) | Exhibitions, narrative experiences, targeted hero moments |

Never make every click wait through the longest cinematic sequence. Reduce motion by removing large movement and providing immediate state changes; do not apply a simplistic global 0.2x time multiplier.

## Review rubric

Look for static design quality, coherent direction, visual identity, semantic relevance, interruption safety, accessible fallback and cost. Three options should differ in navigation model, not just palette/speed.
