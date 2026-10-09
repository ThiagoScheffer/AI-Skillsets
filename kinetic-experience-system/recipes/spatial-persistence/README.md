# Persistent 3D scene architecture

**Use only when:** scene continuity conveys spatial meaning or product identity; do not add a renderer for atmospheric decoration alone.

## React Router/R3F shell

```text
<AppShell>
  <PersistentCanvas aria-hidden />  ← mount outside changing outlet
  <RouteContent />                   ← semantic HTML content and controls
</AppShell>
```

Treat this as a conceptual diagram, not a drop-in R3F component. Keep accessible textual equivalents in HTML. Decide who owns camera positions, model transforms, DOM overlays and pointer gating.

## Route-state synchronization

- Router selects desired scene state (artifact ID, camera target).
- A single scene controller accepts a transition intent and resolves completion/cancellation; UI controls use authoritative route state.
- Preload textures/models opportunistically; limit waits and fallback to 2D poster in WebGL failure.
- Pause or scale down idle render work when tab hidden or device quality is low.
- If GSAP timelines drive 3D properties, R3F `useFrame` must not independently overwrite those properties during the same interval.

## QA

20 back-to-back route changes, slow decoding, context loss, devicePixelRatio scaling, integrated GPU, touch drag cancellation, reduced motion and keyboard-first navigation. Measure memory and frame timing rather than assuming persistence is automatically faster.
