# Adapter - Python Backends

Applicable to Django/DRF, Flask, FastAPI/Starlette, SQLAlchemy, Django ORM, and related stacks.

## Django / DRF

Review `urlpatterns`, routers/viewsets, `permission_classes`, decorators/mixins, object permission hooks, and queryset filtering. `get_queryset()` can be a central tenant/object scope; verify all actions actually use it and that custom actions/raw queries do not bypass it.

Mass assignment concerns often appear in serializers/forms where protected fields are writable.

## FastAPI / Flask

Inventory decorators/router registrations and dependencies/middleware. Verify authentication dependencies are distinct from role/object authorization. Trace DB queries in endpoint/service layers.

## Data access

For SQLAlchemy/Django ORM, inspect whether filters use trusted caller context. A primary-key lookup alone is only a candidate; prove that no subsequent policy/ownership check applies.

## Templates/XSS

Jinja/Django templates normally auto-escape HTML contexts, but review `safe`, `mark_safe`, `Markup`, raw HTML responses, email templates, and JavaScript/URL contexts separately.
