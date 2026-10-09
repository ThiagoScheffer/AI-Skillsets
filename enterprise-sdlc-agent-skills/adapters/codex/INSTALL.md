# Codex installation

The core skills are provider-neutral.

## Project-local approach

Copy the desired directories from `skills/` to the Codex-compatible project skill location, commonly:

```text
.agents/skills/
```

Example:

```bash
mkdir -p .agents/skills
cp -R /path/to/enterprise-sdlc-agent-skills/skills/* .agents/skills/
```

Keep repository-specific commands and conventions in the project's normal Codex/agent guidance rather than duplicating the entire SDLC there.

## Recommended minimum

Install all skills for greenfield application work. For a smaller repository, `sdlc-orchestrator`, `software-implementation`, `verification-release` and any domain-relevant specialists may be enough.
