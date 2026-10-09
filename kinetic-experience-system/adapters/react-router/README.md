# React Router adapter

**Choose:** (A) built-in View Transitions for snapshot based route enhancement, (B) component-level Motion `AnimatePresence` for local state/compatible boundaries, or (C) experimentally verified live route overlaps (e.g. Hyperkinetic) if true simultaneous old/new DOM animation is required.

## A — Native first

`<Link to="/work/42" viewTransition>` enables browser-supported router-managed transitions; pair with `useViewTransitionState` and scoped `view-transition-name` on an active source only. Follow `recipes/native-view-transition/`.

## C — Live concurrent DOM

Read the Codrops article and the actual pinned `hyperkinetic` docs. Its `AnimatedOutlet` wraps **one** outlet in the example, owns old/new route lifecycles and can provide one GSAP timeline and persistent scene hooks. Verify installed API. Ensure scroll rules do not conflict with `<ScrollRestoration />`, and outgoing content is inert. Never duplicate the outlet. See `recipes/parallel-navigation/` for evaluation rubric, not bundled alpha code.

## Checks

- Framework / Data / Declarative mode and nested route hierarchy.
- Loader states, pending navigation, ScrollRestoration compatibility, SEO and route error boundaries.
- Back/Forward, direct link, asset timeout, reduced motion, keyboard/focus.
- Explicit clean-up on aborted navigation.
