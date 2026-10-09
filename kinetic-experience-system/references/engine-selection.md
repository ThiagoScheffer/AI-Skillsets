# Motion engine decision matrix

Choose engines by *required semantics*, not by popularity. Verify versions against installed packages and vendor docs when implementation begins.

| Requirement | Default recommendation | Caution |
|---|---|---|
| Button hover, small reveal | CSS transitions / WAAPI | Beware `transition: all` |
| Local React layout reflow/reorder | Motion (`layout`) | Keep stable component keys |
| Shared React element identity | Motion (`layoutId`) | Both endpoints need compatible projection context; test across routes |
| Route snapshot morph | Native View Transitions + router integration | Outgoing view is a snapshot; name collisions need prevention |
| Multi-element overlapping chronology | GSAP timeline | Cleanup and property ownership |
| True live old/new route DOM in React Router | Tested route-preserving integration, e.g. Hyperkinetic | Alpha, one outlet per article; verify API/version |
| Spatial 3D navigation | Three.js / React Three Fiber | Canvas persistence, GPU fallback, input lifecycle |
| Framework-specific page transitions | Router-native adapter where possible | Respect SSR/streaming/nested routes |

## Selection algorithm

1. Does it require an actual transition? If no, prioritize static clarity.
2. Can CSS/WAAPI handle it with correct a11y? Prefer it.
3. Does it involve React layout state/identity? Consider Motion.
4. Does it require precise cross-component scheduling? Consider GSAP, with distinct transform ownership.
5. Is live dual-route interaction essential? Investigate a verified router lifecycle adapter. Do not mistake native snapshots for live outgoing pages.
6. Does spatial/3D manipulation materially improve meaning? Add GPU rendering only after a simpler alternative is rejected.
7. Can the chosen engine meet reduced-motion, route focus, cancellation and performance requirements? Otherwise change the design.

## Motion ownership policy

For each relevant node/property/time interval, select one engine. If GSAP owns ancestor `transform`, Motion may own *child* transform, not the same node; write down the wrappers explicitly. CSS may own background colors while JS owns transform, provided no competing cascade or transition on that property. A WebGL object's world transform must have one authoritative clock.

## Adoption notes

- `framer-motion` is the legacy package name; modern Motion examples use `motion/react` imports from the `motion` package. Inspect actual app dependencies before replacing imports.
- Native View Transitions are progressive enhancement and may not behave consistently across every browser/framework combination.
- Hyperkinetic was alpha at the October 8 2026 Codrops article. The adapter here is evaluation guidance, not a pinned bundled dependency.
- GSAP feature availability/licensing can evolve; verify current terms for special plugins and distribution.
