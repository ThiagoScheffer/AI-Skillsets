# Performance & measurement playbook

**Do not promise performance without measuring.** The goal is interaction quality in the target browser, network and device mix.

## Measures

- Animation frame times: 60Hz display has ~16.7ms/frame budget; a large portion may be consumed by browser/compositing, so the JS animation work should be much less than total budget.
- Monitor dropped/long frames, main-thread tasks, style/reflow, paint and texture upload.
- Core Web Vitals evaluation: target INP ≤200ms and CLS ≤0.1 at 75th-percentile field population when those metrics are available. Motion regressions must be tested, not assumed.
- Track memory across repeated navigations and WebGL context count if relevant.

## Prefer

1. `transform`/`opacity`, well-scoped compositing and bounded animations.
2. Cache layout measurements within the same stable transition phase. Avoid read/write/read/write layout thrashing.
3. Decoded images, correct sizes/srcset, aspect-ratio placeholders; avoid blocking all navigation on decorative resources.
4. Rate-limited/paused idle loops in background tabs. Clamp devicePixelRatio for 3D.
5. `prefers-reduced-motion` and user-configured motion intensity as independent quality modes.

## Profile scenarios

- Midrange phone and desktop; keyboard/touch; both warm/cold loads.
- Resize or rotate during a transition.
- 20 consecutive transitions and rapid reverse navigation to surface leaks.
- Slow network, failed image, WebGL unavailable, background/resume.

## Report template

`Browser/version, device/CPU/GPU, viewport, refresh rate, route pair, reduced-motion preference, network profile, cold/warm, trace file, fps/frame distributions, INP/CLS source, before→after.`

If trace collection is unavailable, label performance **unverified** and explain how to run it in the project's browser/tooling.
