# Motion Blueprint — JSON contract

The file is an **intermediate design/engineering artifact**, not a generated application runtime configuration and not an existing Hyperkinetic/Motion/GSAP API.

Validate using `python scripts/validate_blueprint.py file.json` and inspect `schemas/motion-blueprint.schema.json`.

## Sections

- `version`, `project`, `mode`, `experience`: project context and motion profile.
- `constraints`: performance/a11y/functional guards; architecture must respect these before effects.
- `navigation`: routing strategy (`native-view-transition`, `motion-presence`, `live-parallel`, `local-state`, `progressive-enhancement`, `none`), interruption and scroll authority.
- `ownership`: engine/property assignment to avoid collisions.
- `transitions[]`: named state transition, semantic relation, trigger, component anchors, choreography with named beats, fallbacks and acceptance criteria.
- `verification`: objective test matrix and evidence tracking.

## Usage sequence

1. Produce blueprint in design phase.
2. Validate syntax and schema-compatible field types.
3. Review semantic logic and architecture constraints (validators cannot decide good design).
4. Create an implementation plan and PR-sized milestones.
5. Keep blueprint synchronized with actual implementation; annotate deviations.
6. Run visual/functional/perf tests, filling results only from observed evidence.

## Versioning

Initial version `1.0`. Future versions should be migrated with a script. Unknown fields can be stored in explicit `notes` strings rather than silently extending schema. For automation consumers that need extensions, fork the schema and document new fields.
