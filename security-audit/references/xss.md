# Category 5 - XSS / Unsafe Rendering

## Goal

Trace untrusted data to an executable/rendering context and verify context-appropriate defense. Modern frameworks often escape normal text rendering; bypass APIs deserve review but are not automatically vulnerabilities.

OWASP XSS guidance emphasizes output-context handling, safe sinks, URL validation, and HTML sanitization when HTML must be accepted.

## Frontend sinks

Search framework/runtime equivalents of:

- `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`;
- React `dangerouslySetInnerHTML`;
- Vue `v-html`;
- Angular `[innerHTML]` and sanitization-bypass APIs;
- Svelte `{@html}`;
- jQuery `.html()`;
- iframe `srcdoc`;
- raw HTML/Markdown/WYSIWYG renderers;
- dynamic event-handler/script creation;
- `eval`, `new Function`, string-to-code APIs.

For each candidate identify the source: persisted user content, query params, API fields, third-party data, admin-authored rich text, etc. Then establish sanitization/encoding and its configuration.

## URLs

Trace untrusted input into:

- `href`, `src`, navigation targets;
- iframe/embed URLs;
- redirects opened in browser contexts;
- CSS/resource URLs where applicable.

Check allowed schemes/protocols and URL parsing. HTML encoding alone does not make a `javascript:` URL safe.

## Markdown and rich text

Determine whether raw HTML is allowed. Verify sanitizer library/version/config, dangerous URI handling, hook/customization behavior, and whether sanitization occurs after all transformations that can reintroduce markup.

## Backend HTML

Review user-controlled values entering:

- HTML emails;
- server templates;
- raw HTML responses;
- preview/rendering services.

Determine whether the template engine auto-escapes in the specific context. HTML body escaping does not solve JavaScript/CSS/URL contexts.

## Finding threshold

Report when attacker-controlled or insufficiently trusted content reaches a dangerous rendering/execution context without an effective context-specific control.

If dangerous APIs only consume constants or data proven sanitized immediately before the sink, record as reviewed/strength where meaningful rather than a vulnerability.

## Preferred remediation

- use safe text/DOM/framework rendering APIs;
- use context-aware escaping;
- validate URL schemes with allowlists;
- use a well-maintained HTML sanitizer only when HTML must be rendered;
- avoid dynamic code evaluation;
- add regression payloads appropriate to the exact sink/context.
