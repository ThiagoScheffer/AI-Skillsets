# Source Review and Qualification Rules

Use this file to preserve the distinction between the user's source material, synthesized guidance, current standards, and hypotheses.

## Source-derived themes

The supplied material consistently supports these themes:

- UI, UX, and CX are related but different layers.
- Start with the user's task and problem before choosing components.
- Visual hierarchy is created by contrast in size, weight, position, color, spacing, imagery, and visibility.
- Signifiers and states should communicate how the UI works without requiring instructions.
- Good product design reduces unnecessary interaction and decision cost.
- Recognition can reduce recall burden.
- Feedback should acknowledge both interaction and outcome.
- Progressive disclosure can reduce density when secondary functionality remains discoverable.
- Product pages should reduce uncertainty through imagery, trust, comparison, and decision-point reassurance.
- Dashboards should organize around data structure and user decisions rather than generic cards.
- Empty/loading/error and other invisible states are part of the product.
- Generated UI often fails through inconsistent tokens, dense repeated cards, excessive effects, and generic layouts.
- Case studies are stronger when they show reasoning and narrative rather than a mechanical process checklist.
- Security/privacy should be reviewed while UX/UI changes are being made, not bolted on later.

## Context-dependent claims: do not hard-code as universal laws

### F-pattern
One source rejects forcing an F-pattern and another uses it to justify left-side controls. Treat scan patterns as contextual observations. Prefer task-specific hierarchy and usability evidence.

### Ghost buttons
A source warns against ghost buttons for a main CTA; another uses ghost-style links/buttons as secondary actions. Reconcile by hierarchy: primary actions generally need stronger salience; secondary/tertiary actions can be quieter.

### Dropdowns
A source calls dropdowns lazy. Do not repeat this as a rule. Expose options when comparison and low option count justify it; use a dropdown or other compact selector when space, count, or context justifies it.

### One font
“One family is usually enough” is a consistency heuristic, not a prohibition against deliberate type pairing.

### Exact spacing/type recipes
4px or 8px grids, -2% tracking, 110-120% line-height, or dashboard type-size ceilings are heuristics. Follow the project's existing system when coherent.

### Dark-mode shadows
Do not turn “dark mode has no shadows” into a rule. Re-evaluate elevation and contrast for dark surfaces; use the technique that communicates depth without excessive contrast.

### Infinite scroll, skeletons, motion, gradients
Evaluate the user/system problem. Avoid absolute always/never claims unless a standard or safety constraint requires one.

### CTA copy
Outcome-oriented language may help motivation, but clarity remains primary. Treat copy changes as experiments unless strong product evidence exists.

### Specific numbers/social proof
Specificity may feel credible but fabricated or stale numbers are a trust failure. Verify all claims.

## Behavioral/psychology claims

The supplied psychology transcript includes smart defaults, progress/goal-gradient framing, reciprocity, ownership/endowment, loss framing, and contrast/anchoring. Use them as design hypotheses with ethical constraints.

Do not reproduce source claims about exact conversion percentages or behavioral effect sizes as fact unless independently verified.

## Evidence discipline

Tag findings mentally or explicitly as:

- OBSERVED — directly visible in code, UI, data, or test output.
- SOURCE — supported by the supplied source set.
- STANDARD — supported by an authoritative accessibility/security standard.
- INFERRED — likely but not confirmed.
- HYPOTHESIS — proposed improvement requiring testing.
- UNKNOWN — missing information.

Screenshot-only review cannot prove server authorization, real interaction states, analytics lift, performance, error timing, or accessibility conformance.
