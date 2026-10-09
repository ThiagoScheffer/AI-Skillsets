# Source references / provenance

Primary references checked on **2026-10-09**. These links are for continued reading; external packages/assets are **not** bundled and their behavior can change with new releases.

1. [Codrops — Building Parallel Page Transitions with GSAP and React Router (2026-10-08)](https://tympanus.net/codrops/2026/10/08/building-parallel-page-transitions-with-gsap-and-react-router/) — live concurrent route DOM, shared GSAP timeline, persistent R3F scene, interrupted navigation; accessibility tradeoffs.
2. [Amber Genetics demo/source](https://github.com/ismamz/amber) — exploratory reference project; review its credits and third-party licenses before reuse.
3. [Hyperkinetic](https://github.com/ismamz/hyperkinetic) — experimental React Router transition engine, alpha at publication; verify package API and constraints.
4. [Motion — Layout animation](https://motion.dev/docs/react-layout-animations) — `layout`, `layoutId`, shared layout, transform projection.
5. [Motion — AnimatePresence](https://motion.dev/docs/react-animate-presence) — React exit retention and propagation semantics.
6. [GSAP React integration](https://gsap.com/resources/React/) — `useGSAP` and scoped context cleanup.
7. [GSAP context API](https://gsap.com/docs/v3/GSAP/gsap.context%28%29/) — scope and `revert()`.
8. [React Router — View Transitions](https://reactrouter.com/how-to/view-transitions) — router-owned native transitions and `Link viewTransition`.
9. [Chrome — View Transition API](https://developer.chrome.com/docs/web-platform/view-transitions/) — snapshot-based browser transitions.
10. [OpenAI — Skills](https://developers.openai.com/api/docs/guides/tools-skills) — `SKILL.md` bundles and metadata.
11. [Claude Code — Skills](https://code.claude.com/docs/en/skills) — project `/.claude/skills` discovery and skill invocation.
12. [Codex skills in repositories](https://developers.openai.com/blog/skills-agents-sdk) — `.agents/skills` practice.

### Source & license policy

Third-party articles, fonts, models, illustrations and code remain property of their respective owners. KX offers independent prompts/specifications and sample patterns; do not redistribute the Amber demo or its assets as part of this package. All framework APIs must be checked against installed project versions at implementation time.
