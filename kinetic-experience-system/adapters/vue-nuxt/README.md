# Vue / Nuxt adapter

Prefer the project's native routing and layout mechanisms. Inspect Vue/Nuxt version, route transitions, `<NuxtPage>` and `<Transition>` semantics; use mode defaults appropriate to intended overlap. Preserve cached layout state where needed, and coordinate GSAP via lifecycle hooks with scoped cleanup. Check route async data, error page, scroll and history carefully.

Semantic Motion Mapping is framework-neutral: stable entity IDs, source/destination anchors, interruption fallback and reduced-motion behaviour are the same. Avoid importing React-only Motion/Hyperkinetic patterns into Vue.
