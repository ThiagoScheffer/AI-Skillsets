# Adapter - Ruby / Rails

Inspect `config/routes.rb`, controllers, concerns, `before_action`, policy gems such as Pundit/CanCanCan, model scopes, ActiveRecord queries, serializers, mailers, and views.

## Authorization

Confirm sensitive actions call/derive the relevant policy and that bulk/custom controller actions are not omitted. With Pundit, verify policy scopes for collection endpoints and object authorization for member actions.

## IDOR / isolation

Prefer tenant/user association lookups such as `current_account.projects.find(params[:id])` over global `Project.find(params[:id])` unless a policy immediately constrains the loaded object.

## XSS

Rails escapes view output by default. Review `html_safe`, `raw`, `sanitize` configurations, rich text rendering, URL helpers fed by untrusted schemes, and mailer HTML templates.

## Secrets

Review credentials files, master keys, environment fallbacks, initializer defaults, CI/deploy configs, and committed `.env` material.
