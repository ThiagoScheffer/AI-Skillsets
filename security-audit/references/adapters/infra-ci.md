# Adapter - Deployment, IaC and CI/CD

Load when Docker, Compose, Kubernetes/Helm, Terraform/IaC, or CI files are present.

## Secrets/defaults

Inspect:

- Docker `ENV`/`ARG`, build args and copied config;
- Compose environment values and `${VAR:-default}` fallbacks;
- Kubernetes `Secret` manifests (base64 is encoding, not secrecy), ConfigMaps, env injection;
- Helm `values.yaml`, templates and chart defaults;
- Terraform variables/defaults, provider credentials, outputs/state-related configuration;
- CI workflow `env`, inline credentials, generated artifacts/logging;
- startup scripts and example commands.

A sample/default becomes actionable when it is privileged and can realistically become the running production credential due to fallback/startup behavior.

## Frontend builds

Check build arguments/environment that are statically embedded into browser bundles.

## Startup validation

Prefer production startup that fails closed when required secrets are absent, weak, or equal to known development defaults.

## Historical exposure

CI/IaC files are common historical secret locations; include them in Git-history review.
