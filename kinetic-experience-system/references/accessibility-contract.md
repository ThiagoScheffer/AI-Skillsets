# Accessibility contract for immersive motion

Motion cannot disable access to the interface. Comply with host app accessibility requirements and applicable WCAG guidelines.

- Honor `prefers-reduced-motion`. Preserve information and visible feedback while avoiding unnecessary displacement/zoom/parallax; avoid automatic looping motion if unsafe or distracting.
- Use semantic links for navigation, accessible labels for controls, focus-visible indications and keyboard activation.
- With two live route subtrees, make the outgoing subtree non-interactive and not focusable/readable when the incoming route owns navigation; use `inert` where supported and correctly timed.
- After successful navigation, move focus to the destination's primary heading/main or use the framework's route-focus pattern. SPA route announcements should identify the new page without spam.
- On Back, respect history and scroll restoration; do not reset reading position unconditionally.
- Avoid hidden server HTML waiting indefinitely for JavaScript to start; no-JS and load-error flows should display usable content when required by the architecture.
- Avoid motion as the sole carrier of state; use text/icon/semantic attributes.
- Respect modal dialog semantics, Escape and focus management, and do not leave backdrop hit areas after cancellation.
- If animated text is cloned or split into glyphs, present one semantically complete accessible version; decorative copies `aria-hidden`.
- For 3D, provide accessible HTML equivalents for any information needed to complete tasks.

## Test matrix

Keyboard Tab/Shift+Tab; Enter/Space; Escape; screen-reader smoke test; 200% zoom; mobile viewport; reduced motion; direct route link; Back; mid-transition navigation; asset error.
