# Semantic Motion Mapping (SMM) — normative design protocol

**Definition:** SMM maps a user action and source interface state to a destination state using object identity, task hierarchy and visual continuity, rather than default effects chosen by route name.

## Relations

| Relation | Intent | Usual motion | When not to animate |
|---|---|---|---|
| parent → child | Narrow attention | Zoom, expand, reveal | Deep link without source |
| child → parent | Restore orientation | Contract to known origin | Origin filtered/unmounted |
| sibling → sibling | Change peer context | Directional exchange, object carry | Arbitrary direction misrepresents hierarchy |
| overview → detail | Isolate selected object | Shared card→hero, contextual dim | High-frequency utilitarian flows |
| state A → state B | Explain change without navigation | Reorder, morph, controlled feedback | Instant validation/critical controls |
| environment → environment | Travel inside continuous scene | Camera/scene shift | Low-power or no-WebGL |

## Required map per interaction

1. Trigger and semantic relation.
2. Origin and target route/component IDs, with stable shared **domain identity** when applicable.
3. Primary object(s) with continuity evidence (e.g. `product.id`, not `nth-child`).
4. Entering, exiting and persistent nodes with focus/interaction priorities.
5. Geometry and spatial mapping (origin bounds, target bounds, image crop and font strategy).
6. Primary motion purpose: orientation, hierarchy, focus, state feedback or narrative.
7. Fallback when origin is missing, animation is blocked, a loader fails or reduced motion is requested.
8. Ownership map, cancellation policy, and acceptance tests.

## Identity resolution

`{entityType}:{stableID}:{role}` is a useful naming convention (e.g. `product:42:hero`). The exact form may vary by codebase. Route params should determine identity, never temporary list positions. When multiple elements share a role, scope by route and entity ID. If an anchor is absent, degrade to safe direct entry; do not keep an obsolete source route rendered indefinitely.

## Transition priority

First preserve **what** the user selected, then **where** they are going, then atmospheric polish. An animation without a semantic invariant can be considered decoration and receives the lowest priority.

## Example

Catalog tile `product:42:thumbnail` → product page `product:42:hero` preserves `product:42` identity. Heading can inherit label identity and shift typography; other tiles leave/blur; price and CTA enter once hero settles. Browser Back contracts only if tile 42 exists and is visible; otherwise restore list and focus the list heading.

## Failure cases

Duplicate business IDs; unmounted virtualized rows; asset decoding after geometry capture; layout reflow during animation; changing filter/search during navigation; deep-link entry without source; animation history diverging from browser history; source visible to screen readers after destination becomes active.
