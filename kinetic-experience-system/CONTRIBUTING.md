# Extending the KX skillset

KX is designed to be iterated, not frozen into a single brand of motion.

## Add a specialist skill

1. Choose a stable hyphenated folder name `kx-new-capability`.
2. Create `skills/kx-new-capability/SKILL.md` with *portable* `name` and `description` YAML frontmatter, first line starting `---`. The description must clearly state when the skill triggers.
3. Define scope, a sequenced workflow, explicit stop conditions, deliverables, measurable verification, integration with other skills and failure fallbacks.
4. Include `references/checklist.md`; avoid duplicating entire shared references in the skill file.
5. Register the new name in `scripts/validate_skills.py` `EXPECTED`, and add it to README inventory.
6. Add at least one evaluation prompt in `evals/` where the new skill should activate and one where it should not.
7. Run all validation commands below.

## Add an engine / framework adapter

- Document APIs and version constraints, capabilities, alternative choices, fallback and likely failure modes.
- Distinguish snapshot from live DOM semantics; never claim an untested router behavior.
- Include example source only when the example is cohesive, non-destructive and compatible with the documented stack.
- Verify licenses of code/assets and do not copy proprietary visual identities.

## Change the blueprint schema

- Introduce a `version` bump for incompatible changes and provide migration notes.
- Update examples and the dependency-free subset validator.
- Add invalid fixtures/tests for semantic consistency checks.
- Full JSON Schema spec compliance requires an external validator; note any unsupported keywords.

## Validate

```sh
python scripts/validate_skills.py
python scripts/validate_blueprint.py examples/blueprints/*.json
python -m unittest discover -s tests -v
python scripts/install.py --target /path/to/a/test-repo --platform both --dry-run
```

## Quality and evidence

Agent skill reliability must be evaluated against tasks, not inferred from a clean Markdown linter. Test a greenfield app, a React Router retrofit, a Next.js constrained app, a low-motion user and an interrupted navigation. Provide before/after screenshots or recordings plus verifiable tests when possible. Keep all metrics tied to the test environment.

## Release

Update CHANGELOG and README; rerun tests; package a single full repository ZIP for developer installation and, optionally, separate per-skill ZIPs with `scripts/package_individual_skills.py` for hosted Skills APIs that require one top-level skill folder.
