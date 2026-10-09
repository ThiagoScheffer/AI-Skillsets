# Adapter - Frontend Frameworks

Load when a browser/mobile frontend exists.

## React / Next.js

Review `dangerouslySetInnerHTML`, URL-bearing props from untrusted data, Markdown/renderers, client role gates, and `NEXT_PUBLIC_*`. React normally escapes text interpolation; do not flag normal JSX text rendering.

## Vue / Nuxt

Review `v-html`, URL bindings, Markdown/renderers, route/navigation guards, role composables, and public runtime config. Normal moustache interpolation escapes text.

## Angular

Review `[innerHTML]`, `DomSanitizer.bypassSecurityTrust*`, dynamic component/template code, URL/resource URL contexts, guards, and environment/build config. Understand Angular's built-in sanitization before reporting.

## Svelte / SvelteKit

Review `{@html}`, actions manipulating DOM, links/src from untrusted values, load/actions/server routes, and public env modules.

## General privilege mapping

Client guards/buttons/menus improve UX only. Map each sensitive client action to a trusted server endpoint/action and verify backend authorization.
