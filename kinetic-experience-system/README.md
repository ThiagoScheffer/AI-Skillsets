# Kinetic Experience System (KX)

**Portable creative-motion engineering skillset for OpenAI Codex and Claude Code**  
Version: **1.0.0** · Prepared: **2026-10-09** · Language: English · License: MIT

KX helps an AI coding agent **design, implement, audit and validate** motion-native web experiences in an existing application or a greenfield project. It is a reusable engineering playbook, not a runnable animation framework and not a promise of automatic production-grade design.

Its distinguishing framework is **Semantic Motion Mapping (SMM)**: treat navigation as transformations between meaningfully related interface states. Use a **Motion Blueprint** to decide what should persist, morph, enter, exit, and remain interactive *before* writing animation code.

## What is inside

- **11 standalone agent skills** under `skills/`, with standard `SKILL.md` frontmatter, a domain-specific checklist, and clear delivery criteria.
- **Motion Blueprint JSON Schema + 3 valid scenarios**, a blueprint template, and a validator.
- **Technical references** for semantic relationships, timelines, engine selection, lifecycle, ownership, accessibility, performance, creative direction, QA and framework constraints.
- **Recipes** for shared elements, synchronized routes, native View Transitions, GSAP, Motion, typography, a persistent 3D scene, and microinteractions.
- **Adapter guidance** for React Router, Next.js App Router, Vue/Nuxt, Astro, and vanilla web applications.
- **Local tooling** for installation, repository reconnaissance, schema validation, skill validation, and unit tests.
- **Agent instructions** (`AGENTS.md`, `CLAUDE.md`) intended as examples to merge into a target project's policy, not as replacements for its existing policies.

## Install into an existing project

Requires **Python 3.10+** for the installation/validation helpers (no third-party Python dependencies). You do **not** need Python to read or manually copy the skills.

From this extracted package:

```bash
python scripts/install.py --target /absolute/path/to/your-project --platform both
```

On Windows PowerShell, from the extracted folder:

```powershell
py -3 scripts/install.py --target "C:\\path\\to\\project" --platform both
```

Valid platform values: `codex`, `claude`, or `both`.

- Codex skills: `<project>/.agents/skills/kx-*/SKILL.md`
- Claude Code skills: `<project>/.claude/skills/kx-*/SKILL.md`
- Shared resources: `<project>/.kinetic-experience/` (schemas, references, recipes, templates, adapters and scripts)

**Safety:** The installer will **not overwrite** an existing skill or shared resources unless `--force` is explicitly supplied. It does **not** modify the target app's source files, `AGENTS.md`, `CLAUDE.md`, package.json or lockfiles. Inspect the planned changes with `--dry-run`.

```bash
python scripts/install.py --target /absolute/path/to/your-project --platform both --dry-run
```

To update an earlier KX install, first review local modifications, then use `--force` and version-control the result.

### Invoke

Ask your agent:

- **Codex:** `Use $kx-orchestrator to audit this React app and add coherent shared-element transitions to its product listing/detail flow. Start with a Motion Blueprint and preserve its existing routing.`
- **Claude Code:** `/kx-orchestrator Retrofit this site with intentional motion and run visual QA. Do not change business logic.`
- **Greenfield:** `Use kx-orchestrator to create a motion-native portfolio from scratch. Propose 3 creative directions, implement the selected direction, and test navigation and reduced motion.`
- **Targeted:** `Use kx-morphing-layout to transform a gallery card into a detail hero, including browser Back.`

Agents may auto-select a specialist skill when the trigger matches. Invocation and automatic selection depend on the host and current agent settings; the package itself does not execute animations or install JavaScript packages.

## Modes

| Mode | What happens | Default risk posture |
|---|---|---|
| **RETROFIT** | Discover existing constraints, score high-value seams, make localized changes, regression-test | Conservative; preserve current stack |
| **GREENFIELD** | Plan the interaction architecture and design system before choosing rendering technology | Exploratory, but incremental |
| **FOCUSED** | Change one route pair, component, or interaction | Smallest reversible change |
| **EXPLORATION** | Propose and optionally prototype three competing directions before selection | Distinguish judgments from measurements |

## Non-negotiable rules

1. **Preserve product behaviour.** Never trade navigation correctness, keyboard access, deep linking, content visibility, analytics, or SEO for a visual effect.
2. **One owner per animated property** at any given time. Do not let GSAP, Motion, CSS, and WebGL compete for the same transform/style.
3. **Keep navigation interruptible.** Rapid clicks, browser Back, failed loaders and reduced motion must always resolve to valid UI states.
4. **Choose the lightest sufficient engine.** CSS → Motion/native view transitions → GSAP orchestration → GPU only when justified.
5. **Use real evidence.** Report untested assumptions as untested; never invent FPS, CWV, or browser results.
6. **Design before animating.** The route/state relationship, motion rationale and fallback must be explicit.
7. **Work with the current repo.** Honor existing conventions, coding guidelines, dependency constraints and approvals.

## Agent workflow

```
Repo audit → Semantic motion map → Explore directions (optional)
          → Blueprint (validated) → Architecture & ownership
          → Implement in vertical slices → Interaction/visual/perf QA
          → Refine → Document decisions and maintenance notes
```

Use `templates/motion-blueprint.template.json` and `schemas/motion-blueprint.schema.json`. See `examples/blueprints/` for passing examples.

```bash
python scripts/validate_blueprint.py examples/blueprints/portfolio.json
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/audit_repo.py --repo /absolute/path/to/app --out /tmp/kx-audit.json
```

Validation checks package structure and a **subset** of blueprint schema semantics without extra dependencies. Full JSON Schema validation requires an external JSON Schema validator and is not implied by the local script.

## Skill inventory

| Skill | Role |
|---|---|
| `kx-orchestrator` | Select mode, sequence the skill workflow and enforce gates |
| `kx-experience-audit` | Discover stack, nav model, states, risks and retrofit opportunities |
| `kx-creative-direction` | Create a coherent visual and kinetic design language |
| `kx-motion-architecture` | Choose engines, route adapters, lifecycle and style ownership |
| `kx-transition-design` | Sequence page choreography and parallel transitions |
| `kx-morphing-layout` | Shared elements, identity mapping, FLIP and visual continuity |
| `kx-spatial-experiences` | Optional GPU, persistent canvases, 3D and camera continuity |
| `kx-microinteractions` | Local state, drag, menus, galleries and feedback |
| `kx-performance-accessibility` | Motion-safe/keyboard/performance architecture and budgets |
| `kx-visual-qa` | Test matrix, trace-driven critique and release gates |
| `kx-creative-exploration` | Compare three credible directions using explicit tradeoffs |

## Project structure

```
kinetic-experience-system/
  skills/kx-*/SKILL.md + references/checklist.md
  references/                 Reusable specifications and decision documents
  adapters/                   Integration-specific guidance
  recipes/                    Patterns and source examples; not a drop-in SDK
  schemas/                    JSON Schema
  templates/                  Audit, blueprint and review artifacts
  examples/blueprints/        Passing blueprints
  scripts/                    Portable Python utilities
  tests/                      Unit tests and optional browser test sample
  AGENTS.md / CLAUDE.md        Optional repo policy snippets
```

## What has / hasn't been tested

The package includes validators and unit tests run during generation; see release summary in the download response. The example React/GSAP/Motion integrations are **documented patterns** and not compiled into a verified production site here. A real project requires package installation, integration, visual browser QA and device profiling.

## Credits and source boundaries

KX is independently structured from the design discussion. It **references but does not bundle** the Amber Genetics demo, its 3D models, fonts, Hyperkinetic source, or any commercial assets. Consult upstream project licenses before copying their code or media. All URLs and relevant documentation live in `references/sources.md`.

## Extending KX

Add specialist skill directories with `SKILL.md` and explicit trigger descriptions. Add a versioned adapter or recipe when a new implementation pattern proves useful. Extend the Blueprint schema conservatively and add passing/failing fixtures. Run all validators and update `CHANGELOG.md`.

### Hosting individual skills

The downloaded ZIP is a **repository containing 11 skills**, not a single `SKILL.md` bundle. To upload a skill to a hosted Skills API that accepts only one skill per archive, extract this package and run:

```bash
python scripts/package_individual_skills.py --out /path/to/individual-skill-zips
```

Each output has exactly one top-level skill folder with its own `SKILL.md`. Shared references and recipes remain in this full source repository or an installed `.kinetic-experience/` directory.
