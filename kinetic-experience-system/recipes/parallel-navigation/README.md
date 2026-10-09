# Live parallel pages — React Router + Hyperkinetic evaluation

**Source concept:** October 8, 2026 Codrops article on Amber Genetics and Hyperkinetic, see `references/sources.md`.

Unlike browser snapshots, a live parallel transition keeps old and new routed content mounted together long enough to animate their elements on the same GSAP timeline. This is valuable for persistent scenes and detailed choreographies but brings substantial lifecycle, scroll and focus complexity.

## Preflight

1. Confirm installed React Router mode, version and nested outlets.
2. Confirm latest Hyperkinetic type definitions and installation instructions. It was **alpha** at publication; do not treat this reference as a stable API promise.
3. A single `AnimatedOutlet` per the reference article; verify support before using nested/multiple animated outlets.
4. Do not include competing scroll restoration helpers without explicitly reconciling them.
5. Confirm outgoing `inert` and pointer exclusion timing; implement destination focus and route announcements.
6. Define interrupted navigation, resource timeout and reduced motion paths.

`transition.example.ts` demonstrates the documented API shape as of the article. Review upstream types prior to using. It is not preinstalled or shipped as a runtime dependency.

## Not recommended for

A Next.js App Router retrofit without an approved architectural migration; a tiny interaction that CSS handles; pages that cannot afford dynamic outgoing DOM retention or strict focus management.
