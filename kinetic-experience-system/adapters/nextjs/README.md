# Next.js App Router adapter

**Do not insert React Router/Hyperkinetic into Next.js.** Preserve Next.js routing, RSC/server-client boundaries, streaming and Suspense. For complex shared elements, isolate a compatible client boundary and implement Motion or browser-native transitions if integration can be demonstrated in the project's actual version.

Start with local morphing within a client component or a route snapshot effect when supported. Verify experimental flags, framework APIs and hydration behaviour for installed version; do not claim global true live parallel page mounts by default.

Keep links and prefetching intact; never force `window.location` page reload to animate. Don't hide server content until JS animation begins. Focus/announcements, Back scroll, loading and error segments remain owners of their respective behaviour. Prototype one route pair and measure before rolling out.
