# Native View Transition — React Router

**Use for:** route-to-route visual continuity when browser snapshots are sufficient and React Router's View Transitions integration is available.

This is **not live dual DOM**. The browser captures old/new states; the old view is a screenshot. Progressive enhancement means normal router links still work where animations do not.

## Usage

1. Verify React Router version and the app's routing mode.
2. Enable transition on the specific `<Link viewTransition>` or `navigate(...,{viewTransition:true})`.
3. Apply one unique `view-transition-name` for the selected entity in each capture. Do not assign the same active name to many cards simultaneously.
4. Use `useViewTransitionState(to)` for conditional source styles; apply equivalent destination styles in its route context with care.
5. Make the no-API and reduced-motion route still fully functional.
6. Test Back/deep-link and cases where the source tile does not exist.

See `CardLink.tsx` and `view-transitions.css`; these illustrate the *source endpoint*. The actual destination page must also assign a matching name during relevant navigation. A real app should coordinate IDs and location to prevent collisions.

## Acceptance

- Valid link navigation with/without native API.
- No duplicated names in the same old or new view.
- No forced global CSS animations on every route.
- Reduced-motion variant has no large displacement.
