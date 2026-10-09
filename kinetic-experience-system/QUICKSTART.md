# Quickstart

## 1. Extract and inspect

Read `README.md`, `skills/kx-orchestrator/SKILL.md`, `references/decision-matrix.md` and `references/semantic-motion-mapping.md`.

## 2. Install into a project

```sh
python scripts/install.py --target /path/to/project --platform both --dry-run
python scripts/install.py --target /path/to/project --platform both
```

**Important:** Installation copies instruction files, reference patterns, and helpers. It does not add animation runtime libraries to your app.

## 3. Start your agent at the project root

**Existing app:** `Use kx-orchestrator in RETROFIT mode. Audit routes and navigation, propose three viable transition opportunities, choose one with rationale, generate a valid Blueprint, implement a small vertical slice, then validate Back navigation, focus, reduced motion and layout stability.`

**New app:** `Use kx-orchestrator in GREENFIELD mode. Define the visual identity, semantic motion map, and route/state architecture first. Show three directions and select with explicit tradeoffs. Build an MVP and validate it.`

**Single interaction:** `Use kx-morphing-layout in FOCUSED mode to connect card ID product-42 to its detail hero. Ensure a direct deep link works without an origin card and Back restores the list.`

## 4. Validate a blueprint

```sh
python .kinetic-experience/scripts/validate_blueprint.py \
  .kinetic-experience/examples/blueprints/portfolio.json
```

On Windows, use `py -3` and write paths on one line.

## 5. Review actual evidence

Request a QA report with route matrix, screenshots or frame sequence, failed/succeeded checks, changed files, and known limitations. Don't accept an invented performance score.
