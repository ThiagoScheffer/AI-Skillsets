# KX guidance for Codex (optional example; merge, do not overwrite project policies)

When a task involves significant animation, immersive navigation, shared elements, kinetic typography, morphing, visual storytelling, or motion regression, use the relevant `kx-*` skills. For multi-page changes begin with `kx-orchestrator`.

For an existing project: inspect before editing; honor package manager, router, SSR, styling conventions, auth, state, a11y, and tests. Produce a Motion Blueprint before introducing heavy animation dependencies. One property has one animation owner. Add explicit interruption/reduced-motion/focus behaviour. Implement in reversible slices and report observed verification separately from untested claims.

Shared guidance after installation: `.kinetic-experience/references/`. Schema: `.kinetic-experience/schemas/motion-blueprint.schema.json`.
