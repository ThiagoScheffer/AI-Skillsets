# Delivery gates and defect classification

## Gate A — Design intent

Each effect has a documented semantic relation and an orientation/attention/state benefit. Static composition works first.

## Gate B — Architecture

Router contract verified; owners assigned for URL/history, animation properties, focus, scroll, resource loading and cleanup. Separate DOM wrappers prevent GSAP/Motion transform contention.

## Gate C — Functional correctness

Deep link, Back/Forward, slow loader, route error, repeated navigation, in-flight cancellation, unmount and reduced motion all resolve to functioning UI. No content permanently hidden or pointer blocked.

## Gate D — Visual polish

No stutter visible on supported test devices, overlapping opacity collision, clipping, z-index inversion, distorted object-fit, unreadable intermediate states or typography jump. Treat qualitative observations as observations.

## Gate E — Evidence

Automated tests and/or manual browser QA log what ran with device/context; performance claims have trace data. Clearly disclose anything not executed.

## Severity

- **P0 blocker:** nav broken, content inaccessible or hidden indefinitely, focus trap/dead UI, hydration error, leaked route overlay/scroll lock.
- **P1 serious:** Back incorrect, important mobile clipping, significant measured performance regression, screen-reader duplicate content.
- **P2 cosmetic:** stagger issue, subtle jitter on unsupported slow devices with working fallback, slight easing mismatch.

Release only after P0/P1 resolution or explicit documented scope change.
