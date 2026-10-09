---
name: kx-microinteractions
description: Design and implement responsive menus, tabs, drawers, filters, drag, hover, feedback and local component animation. Use when motion should communicate UI state or interaction affordance without complex route choreography.
---

# KX Microinteractions

## Design rule
Microinteractions clarify causality and state. Keep utility actions predictable. Avoid delaying form controls, confirmations or safety-critical information for decoration.

## Procedure
1. Model discrete states (`closed`, `opening`, `open`, `closing`) and input events; define exact actions permitted during transitions.
2. Choose CSS transitions for simple feedback, Motion for local layout/reorder, GSAP if genuine choreography is required.
3. Wire semantics first: button labels, `aria-expanded`, focus trapping for modal dialogs, Escape to close, scroll locking only when needed, pointer/touch parity.
4. Design anticipation, response and settling using a small easing/timing vocabulary consistent with the larger experience.
5. Test rapid hover in/out, repeated tap/click, keyboard focus, offscreen movement, touch devices and reduced motion.
6. Ensure no invisible interactive nodes, clicks swallowed by decorative overlays or uncontrolled pointer capture.

## Exemplars
- Gallery hover: subtle scale/image displacement, focus-visible equivalent, no sticky mobile hover.
- Filters: layout reordering that preserves item identity and active selection.
- Menu: navigation affordance becomes panel/drawer while preserving Escape/Tab semantics.
- Notifications: state-based appearance and disappearance, with appropriate announcements but no gratuitous motion.

## Deliverable
State machine; chosen animation owner; reduced-motion behaviour; keyboard and pointer test; component-level example or implementation.

## Common engineering contract

- Follow the host project's existing conventions and explicit user requirements. Before installing a runtime dependency, confirm the current framework, versions, package manager and licensing.
- Never treat an unmeasured animation as performant. Report observed browser metrics, hardware and test conditions if available; otherwise mark as unverified.
- Ensure deep links, browser Back/Forward, slow resources, invalid routes, interruptions and reduced-motion paths leave the UI functional.
- The animation layer must never own business logic or force a rewrite of routing/data fetching. Prefer progressively enhanced behaviour and reversible changes.
- Use current `.kinetic-experience/references/` after installation, or package `references/` when working in the source repository.

## Local guide
Read `references/checklist.md` before final handoff. The package README describes installation and the shared reference path.
