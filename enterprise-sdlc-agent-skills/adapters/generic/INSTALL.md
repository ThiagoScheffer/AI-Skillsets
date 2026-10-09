# Generic agent-host integration

For hosts that understand the open Agent Skills pattern, expose each `skills/<name>/SKILL.md` as a separately discoverable skill and preserve sibling `references/` and `scripts/` directories.

For hosts without native Skill discovery:

1. index skill names/descriptions for routing;
2. load only the selected `SKILL.md` into context;
3. allow the skill to reference its local files;
4. keep project state in `.sdlc/`;
5. never merge all skills into a permanent system prompt unless the host has no alternative.

The portable contract is behavior and artifact structure, not any specific agent tool API.
