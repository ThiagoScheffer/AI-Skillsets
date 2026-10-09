# Navigation & motion lifecycle contract

KX defines a *logical* orchestration state machine; adapt it to real router and framework hooks. Never replace the framework router without a compelling integration requirement.

```
IDLE ──navigate──> REQUESTED → PREPARE → READY → TRANSITIONING → COMMIT → CLEANUP → IDLE
                       │            │           │                  │
                       ├─timeout────┤           ├─interrupt────────┤
                       ├─failure────┤           └─error────────────┤
                       └─cancel─────────────────────────────────────┘
```

### Invariants

- Latest-wins is the default for high-frequency web navigation, but first verify whether your router can resolve or cancel earlier navigation safely; otherwise use a one-navigation-at-a-time policy without silently discarding destinations.
- **Prepare:** destination route and essential visible content are known. Load only essential resources; allow bounded waits.
- **Ready:** anchors measured after intended layout/asset readiness, with a valid fallback if not ready.
- **Transition:** outgoing/incoming can overlap *only* when DOM/router model supports it; ensure outgoing content is inert and pointer-disabled as appropriate.
- **Commit:** URL/history state is managed by the router; visual commit timing must not corrupt history, focus or scroll. A visual snapshot is different from a live DOM tree.
- **Cleanup:** dispose snapshots, animation contexts, event listeners, animation frames, temporary layers, old route DOM, pointer blocks, aria overrides and scroll locks.

### Interrupt/cancel policy

At each event, choose exactly one of:
- **Supersede:** stop current visual timeline, capture authoritative current visual state if possible and transition to the newest navigation.
- **Complete-then-navigate:** for runtimes where supersession is unsafe; keep duration bounded and allow user escape where feasible.
- **Fallback:** stop effect and reveal correct route immediately if state becomes ambiguous.

Never implement `click → setTimeout → force navigate` as the only critical path. Never require the user's next click to recover a stalled overlay. Suppress or reconcile stale async callback completion using generation/sequence tokens and lifecycle cleanup.

### Preloading

- Prefetch assets opportunistically and bound waits; prefer displaying valid content over waiting for all decorative images.
- Image decode/3D shader compilation may be non-deterministic. Provide timeout and no-GPU path.
- If the route loader rejects, preserve the app's error boundary and accessible error UI.

### Cross-cutting owners

Explicitly assign URL/history, scroll restoration, document title, route announcements, focus, animation properties, pointer gating and resources to an owner. The orchestrator must not become a second router or silently override framework scroll semantics.
