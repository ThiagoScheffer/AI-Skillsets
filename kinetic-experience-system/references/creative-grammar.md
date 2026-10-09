# Kinetic visual grammar

A coherent design system uses a limited vocabulary of appearance, timing, and spatial transitions.

## Build the grammar

- **Static foundation:** clear type hierarchy, intentional whitespace, contrast, imagery/texture and responsive grid.
- **Anchor object:** visual entity that survives a navigation or transforms between meaningful states.
- **Layer architecture:** specify fixed shell, route plane, shared transition layer, overlays, and optional GPU plane; document stacking order and hit-testing.
- **Motion rhythm:** distinguish fast direct controls, medium layout transitions, rare long hero transitions; use relative timeline anchors instead of arbitrary wait timers.
- **Easing families:** natural acceleration/deceleration; momentum for spatial gestures where it communicates physicality; avoid unrelated easing curves on every component.
- **Typography:** preserve reading order. SplitText-like effects can create duplicate accessible content if not carefully managed. Keep a semantic text source and hide decorative clones from accessibility tree.
- **Intensity:** quiet zone, expressive zone, signature moment. Never put maximum spectacle everywhere.
- **Responsive:** retime or remove unnecessary layers on small screens; account for touch, viewport resize and safe areas.

## Design review questions

What should users notice first? Can they predict where selected content goes? Is the destination stable/readable? Does the reverse movement preserve orientation? Are UI controls responsive throughout? What disappears in reduced motion? Does the effect survive slow content and long text?

## Originality

Borrow concepts, not source art direction wholesale. Do not bundle copied backgrounds, typefaces, textures, models or commercial site code without suitable licenses.
