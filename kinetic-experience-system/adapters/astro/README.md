# Astro adapter

Astro sites often prioritize content delivery. First verify whether client navigation/View Transitions are configured and what persists across pages or islands. Prefer native view transitions and CSS for route snapshots and microinteractions. Maintain ordinary links and SSR correctness as fallback.

Only add persistent client-side GPU islands if justified and supported by hydration/deployment. Test focus, forms, Head updates, script execution, transition hooks and browser Back on the exact Astro version. Avoid converting the site to a SPA purely for spectacle.
