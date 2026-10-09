# GSAP timeline choreography — React

**Use for:** precisely sequenced local component exits, reveals, masks and typography. A GSAP timeline is an excellent *orchestrator* but does not automatically provide a router lifecycle. Use the router-specific adapter for route transitions.

The example is a single React component animation on mount. Use `@gsap/react` scoped `useGSAP`; revert/cleanup automatically. It deliberately does not animate the parent transform owned by any Motion shared layout.

- Prefer relative labels/position markers to unrelated timeouts.
- Keep one animation property owner per DOM node.
- Wrap event-generated GSAP animations in `contextSafe` if they need teardown.
- Do not hide a server-rendered page indefinitely waiting for hydration.
