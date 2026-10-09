# QA test matrix

| Scenario | Expected invariant | Evidence |
|---|---|---|
| Initial load / direct deep link | All important content accessible; no source anchor required | Screenshot and keyboard test |
| Normal forward navigation | Correct URL, final focus, destination content | Interaction trace |
| Back/Forward | Correct history/scroll; valid reverse or fallback | Interaction trace |
| Rapid clicks at 20/50/90% | No stale route, overlay or frozen pointer | Video/automation |
| Long/failed asset | Route resolves with fallback/error state | Throttled test |
| Resize mid-flight | No invalid geometry/overflow at settle | Viewport sequence |
| Reduced motion | Minimal displacement; content remains legible | Emulated preference |
| Keyboard/screen reader | No duplicate focusable route; heading/announcement | Keyboard or assistive-tech check |
| Background tab and resume | Animation completes or recovers | Tab visibility test |
| GPU unavailable/context loss | Static/2D fallback retains function | Emulated/runtime check |
| SSR/hydration | No route mismatch or hidden SSR content | Logs/console |
| 20 route switches | No growing DOM or listeners/memory leak | Memory/DOM profiling |

For each executed row capture browser version, viewport, platform, network, pass/fail, issue link. Use `templates/qa-report.md`. For deterministic frame testing, control GSAP timelines in development where possible, disable unrelated idle animation, wait for fonts/assets, and avoid screen capture timestamps that race with rendering.
