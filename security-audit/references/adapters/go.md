# Adapter - Go

Applicable to net/http, Gin, Echo, Fiber, Chi, gRPC and similar stacks.

Inventory route registrations/middleware groups, handlers, interceptors, service methods, database queries, and templates.

## Authorization

Verify middleware grouping does not leave sensitive routes outside expected auth/role checks. For gRPC inspect unary/stream interceptors and per-method authorization.

## Data access

Review database/sql, sqlc, GORM, Ent, Bun and repository methods for trusted tenant/object predicates. Pay attention to reusable queries called from both privileged and user-facing contexts.

## XSS

`html/template` performs contextual escaping; `text/template` does not. Review conversions to `template.HTML`/`template.URL` and raw HTML email/response construction.
