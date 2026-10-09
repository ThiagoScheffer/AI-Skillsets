# Stack and Security-Model Detection

Detect technologies from evidence, not filenames alone. Strong evidence includes manifests, imports, bootstrap code, middleware registration, dependency injection, migrations, database configuration, deployment files, and runtime entry points.

## Detection checklist

### Languages/runtime

Inspect manifests and source extensions, but confirm active use from entry points and build config.

Common indicators:

- JS/TS: `package.json`, lockfiles, `tsconfig.json`;
- Python: `pyproject.toml`, `requirements*.txt`, `Pipfile`, `poetry.lock`;
- Ruby: `Gemfile`;
- PHP: `composer.json`;
- Java/Kotlin: `pom.xml`, `build.gradle*`;
- .NET: `*.csproj`, `*.sln`;
- Go: `go.mod`;
- Rust: `Cargo.toml`.

### Backend/API

Identify framework and route-registration style. Determine whether authorization is global middleware/guards, per-controller decorators, policy calls, service-layer checks, DB policies, or a mixture.

### Database/data access

Identify direct SQL, database SDK, ORM/query builder, stored procedures/RPC, database views/functions, and any service credential that can bypass row-level controls.

### Authentication

Find session/JWT/API-key validation, auth middleware/guards, identity-provider SDKs, cookie/session settings, token verification, and how authenticated identity reaches data-access code.

### Authorization and tenant isolation

Search for concepts such as:

`tenant`, `workspace`, `organization`, `account`, `team`, `owner`, `user_id`, `member`, `membership`, `role`, `permission`, `policy`, `ability`, `scope`, `RLS`.

Determine the intended invariant. Examples:

- every query is automatically tenant scoped by repository/session context;
- every controller must pass `organization_id` derived from authenticated membership;
- Postgres RLS enforces row access for unprivileged clients;
- policy objects decide object/function access;
- global guards perform RBAC but object ownership is checked in services.

### Frontend

Identify the rendering model and public environment-variable semantics. Client code is an untrusted enforcement layer even when server-rendered UI is used.

### Deployment/configuration

Review at minimum when present:

- Dockerfile / docker-compose;
- Kubernetes manifests / Helm charts;
- Terraform / Pulumi / CloudFormation;
- GitHub Actions / GitLab CI / Jenkins / CircleCI;
- serverless/provider configs;
- `.env.example` and committed `.env*`;
- reverse proxy/web server configuration;
- startup scripts.

## Output: Stack & Security Model

Record concise evidence-backed statements for:

- backend;
- frontend;
- database/data layer;
- authn;
- function authz;
- tenant/owner isolation;
- deployment/configuration;
- limitations or ambiguous components.

After detection, load only the applicable files under `references/adapters/`.
