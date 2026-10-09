# Motion shared-layout identity — React

**Use for:** local React state changes such as selected tile → detail preview or a real shared-element route transition where a compatible layout projection tree is available.

Install current `motion` package per installed app conventions, then use imports from `motion/react`. The example uses a single React component to demonstrate stable IDs, `LayoutGroup`, and `AnimatePresence` without claiming cross-route support.

- Keep state keyed by immutable domain IDs, not array position.
- Ensure the shared image and text layout IDs are unique within the layout group.
- If using modal semantics, implement focus trapping, Escape and focus restore; the inline example deliberately avoids pretending it is a dialog.
- If using GSAP for text reveal, put it on a nested child, not the wrapper Motion owns.
- Test content reflow, direct entry without a source, reduced motion, and rapid state changes.
