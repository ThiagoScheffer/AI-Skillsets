# FLIP morph strategy — framework neutral

For First–Last–Invert–Play, capture stable source and destination geometry; apply an invert transform to a **visual proxy**, animate to identity, then dispose. The example intentionally does not mutate router state or clone interactive controls. It runs on a dedicated temporary element to avoid engine conflicts and leaking focusable nodes.

- Source and target must refer to the same logical domain entity.
- Check for missing/moved targets and zero-size rectangles.
- Use opacity/static fallback under reduced motion.
- Remove the proxy on success, cancellation or rejection.
- Do not duplicate sensitive or interactive content into a focusable overlay.
