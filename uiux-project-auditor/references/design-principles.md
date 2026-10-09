# Design Principles and Domain Patterns

## 1. Intent before interface

For every screen identify:

1. user and journey stage;
2. arrival trigger;
3. primary job;
4. minimum information needed to act;
5. primary and secondary actions;
6. failure/recovery path;
7. what the user should understand after completion.

If a screen has no clear job, simplify before styling.

## 2. Signifiers and states

A user should infer relationship, selection, availability, and interactivity through structure and feedback.

### Buttons
Consider default, hover, focus, pressed, disabled, loading, success/failure feedback.

### Inputs
Consider empty, focus, filled, valid, warning, error with actionable explanation, disabled, read-only, loading/autocomplete.

### Navigation
Show current location. Collapsed icon-only navigation needs recognizable icons and labels/tooltips where ambiguity exists.

### Feedback
A pressed state acknowledges input. A result state confirms outcome. Use both when needed.

## 3. Visual hierarchy

Use size, weight, position, color, spacing, imagery, contrast, and visibility to direct attention.

Review four layers:

- visual hierarchy — what looks strongest;
- information hierarchy — what appears first;
- interaction hierarchy — what action is easiest to find;
- disclosure hierarchy — what remains hidden until relevant.

Do not force a universal scan pattern.

## 4. Spacing, alignment, and grids

Use proximity to communicate grouping. Use a tokenized spacing system where practical. Grids are especially useful for repeated/responsive layouts, but intentional custom compositions can break them.

Alignment errors in repeated content create subtle distrust and visual noise.

## 5. Typography

Prefer a coherent type system over many styles. A single family can often handle product UI through size, weight, color, and line-height. Dense dashboards typically need a tighter scale than marketing surfaces.

Body text supports understanding; headlines attract attention. Badges and labels should be concise and quickly scannable.

## 6. Color

Color should have a job:

- brand identity;
- hierarchy/action;
- semantics/status;
- data encoding.

Use restrained neutral surfaces plus purposeful accent/semantic colors as a reliable starting point. Treat 60/30/10 as a loose heuristic, not a calculation.

Color associations are culturally influenced. Never rely on color alone for meaning.

## 7. Effects and depth

Shadows, gradients, blur, strokes, and glow should support hierarchy. Excess effect density makes components compete.

For dark mode, re-evaluate surface luminance, borders, saturation, text, data colors, and media overlays instead of simply inverting light mode.

Controls or text over images must remain legible across bright, dark, and busy media.

## 8. Icons

Check recognition, label need, stroke/fill consistency, optical size, baseline alignment, and functional family. Different icon styles can coexist when deliberately separated by context.

Avoid arbitrary emoji substitution for production iconography unless it is part of the visual language.

## 9. Friction and smart defaults

Reduce blank decisions with safe, editable defaults when the likely answer is known. Do not preselect recurring billing, invasive permissions, or other consent-critical choices just to increase completion.

Count interaction cost across clicks, screens, typing, recall, waiting, repeated input, and recovery. Necessary safety friction is valid.

## 10. Recognition over recall

Use recent recipients, recent searches, recognizable avatars, presets, known categories, and visible options where they make the task faster and safer.

In high-consequence flows pair recognition cues with exact identifying details.

## 11. Input method

Choose by frequency, precision, range, motor effort, device, and error cost.

- bounded, low-frequency, low-precision: slider/wheel can fit;
- repeated or precise numeric input: direct number entry/stepper often fits;
- small known set: visible options/presets can fit;
- open answer space: free text.

## 12. Progressive disclosure

Keep primary/frequent functionality visible. Reveal secondary/advanced functionality in context. Never hide information needed for informed consent, safety, recurring billing, or destructive consequence understanding.

## 13. Search

Audit empty/focus state, recent items, suggestions, typed results, filters/sort, no-results recovery, tolerance, loading, and error states. Suggestions should help rather than distract.

## 14. Motion and perceived performance

Motion should communicate progress, cause/effect, orientation, completion, or deliberate delight. Avoid motion that adds delay or removes control.

Users need evidence that work is happening. Choose skeleton, spinner, progress indicator, optimistic update, or task-specific loading pattern based on actual latency and risk.

Optimistic UI is most appropriate for low-risk reversible operations. Be conservative with money, permissions, credentials, destructive changes, and other high-consequence actions.

## 15. Trust architecture

Place proof near the question it resolves:

- reviews near product identity;
- cancellation terms near subscription choice;
- testing/safety proof near health claims;
- recipient/source/destination near transfer amount;
- resulting balance/total price before commitment;
- permissions/data use before consent.

## 16. Behavioral patterns with ethical constraints

### Smart defaults
Start from a likely safe choice; keep it editable and visible.

### Progress framing
Show legitimate progress; do not fake completion.

### Reciprocity
Give useful value before asking for commitment when possible.

### Ownership/pre-investment
Let users create genuine value before signup; do not trap work behind a surprise data wall.

### Loss framing
Show real consequences. Flag fake countdowns, fabricated threats, and guilt/shame dismissal.

### Anchoring/contrast
Clarify relative value without hiding total or recurring cost.

## 17. E-commerce / PDP

Review:

- product identity and imagery;
- catalog-level image consistency;
- product-in-use/context where useful;
- rating and proof proximity;
- option visibility and selected state;
- price, unit, quantity, and total cost clarity;
- purchase-plan comparison and recurring terms;
- category-specific trust proof;
- sticky actions without obstruction;
- mobile/responsive and real-data resilience.

A product page should help the user move through notice -> understand -> evaluate -> trust -> compare -> resolve objections -> commit.

## 18. High-consequence flows

Show:

- source and destination;
- recognizable identity plus exact detail;
- amount/object/action;
- consequence preview;
- confirmation or re-authentication when risk warrants it;
- unambiguous result and recovery.

## 19. Dashboards

### Structure
Persistent/global navigation belongs in stable locations; group links by relevance and show active state.

### Let data drive form
- categories/status -> chips or compact categorical cues;
- numbers -> aligned for comparison;
- time sequence -> timeline where that aids understanding;
- time-series summary -> chart;
- people -> identity cues;
- rare actions -> contextual disclosure.

### Tables
A mature table may need search, filter, sort, pagination/virtualization, selection, bulk actions, column management, empty/loading/error, responsive behavior, and accessibility.

### Charts
Include enough axes, units, baseline, scale, legend, labels, date range, and hover/focus data to answer the question. Avoid ornamental chart forms that block comparison.

### Popover/modal/page
Use the smallest container that preserves clarity and context. Consider task complexity, blocking behavior, persistence, deep linking, mobile constraints, and accessibility.

## 20. Onboarding and journey stage

New, returning, and highly engaged users may need different information density and guidance. Progressive onboarding usually beats a pre-use lecture: make the first valuable action obvious, help complete it, then reveal the next.

## 21. Post-purchase/CX

Review discovery -> evaluation -> purchase -> confirmation -> fulfillment -> delivery -> support -> return/renewal when product performance depends on lifecycle experience.

Order tracking should reduce uncertainty with current status, expected timing, items, destination, responsible party where relevant, contact path, and next step.

## 22. Generated/vibe-coded UI

Common smells:

- inconsistent type sizes, spacing, radii, verbs, and icon families;
- clashing gradients and saturation;
- glow/shadow overuse;
- generic repeated KPI cards;
- overloaded repeated cards;
- every action always visible;
- too many status colors;
- demo-data-only layouts;
- missing empty/loading/error states.

Fix the product-specific system and intent rather than cosmetically hiding the source of generation.
