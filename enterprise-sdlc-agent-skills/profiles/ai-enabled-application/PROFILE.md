# AI-Enabled Application Profile

Use when an application depends materially on generative AI, ML inference, agentic tool use, retrieval or automated decision support.

## Additional design questions

- What model/provider assumptions exist?
- What data is sent to models or retrieval systems?
- Can prompts or retrieved content cross trust boundaries?
- Which tools/actions can the model invoke?
- What actions are reversible?
- Which decisions require human confirmation?
- How are hallucination/uncertainty handled?
- How are prompt injection and data exfiltration mitigated?
- How are model/version changes evaluated?
- What evaluations measure task quality and safety?
- What fallback exists if the model/provider is unavailable?

## Evidence

Add AI-specific acceptance criteria, adversarial tests/evals and observability for model/tool failures. Do not use a single benchmark score as proof of production suitability.
