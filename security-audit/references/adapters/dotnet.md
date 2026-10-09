# Adapter - .NET / ASP.NET Core

Inventory endpoint routing, controllers/minimal APIs, `[Authorize]`, policies/roles, authorization handlers, endpoint groups, filters, and middleware order.

## Authorization

Authentication via `[Authorize]` does not prove role/object permission. Check policy requirements and resource-based authorization on sensitive handlers.

## Data access

Review EF Core LINQ, repositories, Dapper/raw SQL and global query filters. Confirm tenant filters cannot be disabled or bypassed on user-request paths (`IgnoreQueryFilters` is a high-signal candidate).

## Binding

Review DTO/model binding for protected role/owner/tenant fields and overposting.

## XSS

Razor normally encodes expressions; review `Html.Raw`, custom HTML builders, rich text, unsafe URL values, and client-side sinks.
