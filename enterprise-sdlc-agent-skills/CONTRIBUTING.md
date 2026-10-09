# Contributing

## Skill design rules

- Keep `SKILL.md` focused on trigger, workflow and invariants.
- Put long reference material in `references/`.
- Prefer deterministic scripts for validation.
- Avoid provider-specific tool names in core skills.
- Avoid legal/compliance claims that a skill cannot prove.
- Add an eval case for every important routing or safety invariant.

## Backward compatibility

Changes to artifact locations, IDs or schemas should be treated as compatibility-sensitive. Prefer migration notes to silent format changes.
