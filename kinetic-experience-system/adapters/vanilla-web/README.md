# Vanilla web adapter

Prefer native CSS animations, WAAPI and `document.startViewTransition` (feature detect). Respect native anchor navigation and full reload fallback; never intercept form submission or cross-origin links indiscriminately.

A custom async router adds major obligations: History API, direct links, scroll restoration, metadata/Head management, error documents, caching, scripts, analytics, accessibility and stale request races. Only introduce one when a documented need exceeds platform/router capabilities. See `recipes/native-view-transition` for the minimal feature-detected local-state pattern.
