# Adapter - PHP / Laravel

Review route files, middleware, controllers, policies/gates, Form Requests, Eloquent scopes, route-model binding, Blade templates, queues/mailables, and deployment config.

## Authorization / IDOR

Authentication middleware does not establish object authorization. Verify policies/gates or tenant-scoped model resolution for sensitive actions. Review implicit route-model binding when objects can belong to different tenants.

## Mass assignment

`$fillable`/`$guarded` and request validation are relevant, but protected fields also require authorization logic when a privileged caller subset may change them.

## XSS

Blade `{{ }}` escapes by default. Review `{!! !!}`, raw HTML helpers, Markdown/rich text, sanitizer configuration, mailables, and client-side framework sinks.
