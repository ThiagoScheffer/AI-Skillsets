# Framework routing contract rules

## React Router

Verify Declarative/Data/Framework mode and installed version. `Link viewTransition` and `useViewTransitionState` are routes to browser-managed transitions. A true live dual-route mount may be possible with `useOutlet` and a tested library; do not implement multiple independently mounted trees without understanding loaders, scroll and nested outlets. Hyperkinetic from the Codrops article is alpha and described as supporting one outlet; follow actual version API documentation.

## Next.js App Router

Preserve streaming/Suspense, route loaders, server/client component boundaries, automatic prefetch and browser history. Snapshot/native View Transitions or local client-boundary Motion can be used where supported. Do **not** promise global live parallel old/new page mounts as a generic App Router capability. Build a tested adapter spike before shipping complex route choreography.

## Nuxt / Vue

Use framework-native transitions (`<NuxtPage>` / Vue `<Transition>` or `<TransitionGroup>`), route metadata and layout persistence where appropriate. Confirm Nuxt version API. Assign focus, scroll and resource lifecycle explicitly.

## Astro

Determine whether the project uses client-side view transitions and persistent client islands; browser API availability, hydration boundaries and router history must be verified. Avoid forcing an SPA rewrite.

## Vanilla / other

Prefer native browser platform and existing navigation. Build custom router interception only if justified by the project and after addressing History API, cache, links, forms, SEO and accessibility; default to progressive enhancement.

## Universal

Never change route architecture solely to duplicate a reference demo. If exact requested motion is incompatible with the current framework, explain tradeoffs and propose a less intrusive technique or a separately approved architectural migration.
