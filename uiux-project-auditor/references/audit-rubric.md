# Audit Rubric

## Quality score

A 100-point score is optional. Never allow a high average to hide P0/P1 findings.

| Dimension | Weight | Core question |
|---|---:|---|
| Intent & task fit | 10 | Does the screen serve the user's actual job? |
| Hierarchy & readability | 10 | Can users scan and prioritize information? |
| Interaction & states | 10 | Are controls discoverable, responsive, and complete? |
| Flow & friction | 10 | Are steps, decisions, and recovery efficient? |
| Accessibility | 10 | Are current accessibility fundamentals addressed? |
| Trust & content | 10 | Does information resolve uncertainty honestly? |
| Security & privacy design | 15 | Are product/UI choices aligned with protection? |
| System robustness | 10 | Does it survive real data, states, devices, and latency? |
| Business/conversion fit | 10 | Does it support useful outcomes without manipulation? |
| Consistency/design system | 5 | Is the product coherent and reusable? |

## Product/design severity

- **P0 Critical** — primary task blocked; irreversible/high-impact user harm; severe high-consequence ambiguity; product inaccessible to a major target group.
- **P1 Major** — materially harms completion, comprehension, trust, accessibility, conversion, or core efficiency.
- **P2 Moderate** — noticeable friction, inconsistency, weak state handling, or quality issue.
- **P3 Polish** — refinement with limited standalone impact on task success.

Security severity is separate. Use a security-appropriate severity/risk assessment based on impact, exploitability, exposure, data sensitivity, and controls.

## Confidence

- **High** — directly confirmed in code, UI behavior, data, or tests.
- **Medium** — strong evidence but one or more execution assumptions remain.
- **Low** — screenshot/static inference or incomplete project context.

## Core screen checklist

### Intent
- [ ] Primary user and job are clear.
- [ ] Primary action is identifiable.
- [ ] Secondary actions do not dominate.
- [ ] Information order follows the decision/task.

### Hierarchy/content
- [ ] Important elements have appropriate visual emphasis.
- [ ] Body text is readable and supporting.
- [ ] Labels/badges are concise.
- [ ] Trust/reassurance appears near hesitation.
- [ ] No unsupported social proof, urgency, or claims.

### Interaction/state
- [ ] Selected/active state is clear.
- [ ] Focus is visible.
- [ ] Hover is useful on pointer devices.
- [ ] Pressed/loading state acknowledges action.
- [ ] Success/failure outcome is clear.
- [ ] Disabled state is distinguishable and not used as authorization.

### Flow/friction
- [ ] Avoidable clicks/screens are removed.
- [ ] Repeated information is not re-entered unnecessarily.
- [ ] Recognition/presets/defaults are used where appropriate.
- [ ] Necessary safety confirmation remains.
- [ ] Recovery/back/cancel path exists where needed.

### Real states
- [ ] Empty.
- [ ] Loading.
- [ ] Error.
- [ ] Permission denied.
- [ ] Slow/timeout.
- [ ] Success/undo if applicable.
- [ ] Long/missing data.
- [ ] Mobile/responsive.

## Accessibility checklist

Use current WCAG 2.2 as baseline when applicable.

- [ ] Semantic headings/landmarks.
- [ ] Interactive controls have accessible names.
- [ ] Form inputs have labels/instructions.
- [ ] Errors are identified and described.
- [ ] Keyboard navigation works.
- [ ] Focus is visible and not obscured.
- [ ] Target sizes are usable.
- [ ] Text/background contrast is sufficient.
- [ ] State is not communicated by color alone.
- [ ] Motion can be reduced when appropriate.
- [ ] Reflow/text zoom does not destroy task completion.
- [ ] Dialog focus is trapped/restored correctly.
- [ ] Dynamic updates are announced where needed.
- [ ] Tables expose header relationships.
- [ ] Charts have non-visual/keyboard-accessible equivalents as needed.
- [ ] Drag-only actions have alternatives where required.
- [ ] Authentication does not rely on inaccessible cognitive tests when avoidable.

Do not claim conformance solely from this checklist.

## Stress fixture matrix

### Content
- empty string;
- 1 char;
- very long title/name;
- long unbroken URL/token-like string;
- Unicode/diacritics;
- RTL where relevant;
- missing image;
- bright/dark/busy image;
- zero/negative/large numbers;
- decimal/currency/locale variants;
- 0, 1, typical, and very large list counts.

### System
- fast response;
- slow response;
- timeout;
- partial failure;
- expired session;
- insufficient permission;
- stale data;
- concurrent update;
- optimistic rollback;
- reload/deep link;
- mobile/tablet/desktop;
- 200% text zoom where relevant;
- keyboard-only.

## E-commerce/PDP checklist

- [ ] Product imagery identifies product clearly.
- [ ] At least one view helps imagine use/scale/outcome when relevant.
- [ ] Imagery works across the catalog, not just one item.
- [ ] Overlay controls survive variable images.
- [ ] Reviews/trust near product identity.
- [ ] Options easy to compare/select.
- [ ] Subscription/recurring terms explicit.
- [ ] Price, unit, quantity, total clear.
- [ ] Category-specific safety/quality proof available.
- [ ] Sticky purchase UI does not obscure content/focus.

## Dashboard checklist

- [ ] Main content reflects the user's primary decision/job.
- [ ] Sidebar/global navigation is grouped and active state is clear.
- [ ] Data type drives representation.
- [ ] Tables support useful actions such as search/filter/sort when needed.
- [ ] Bulk/contextual actions appear only when relevant.
- [ ] Charts have scale/units/labels/reference cues.
- [ ] Empty/loading/error states exist.
- [ ] Dense UI remains scannable and keyboard accessible.

## High-consequence checklist

- [ ] Source and destination are explicit.
- [ ] Target identity is recognizable and exact.
- [ ] Consequence/total/new state previewed.
- [ ] Destructive/final action uses proportionate friction.
- [ ] Authorization is server-side.
- [ ] Result is unambiguous.
- [ ] Recovery/undo exists when appropriate.
