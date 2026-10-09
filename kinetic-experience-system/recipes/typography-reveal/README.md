# Accessible kinetic typography

Text animation must not create multiple accessible copies, disturb logical reading order, or introduce layout shifts when fonts load. Split headings only for decorative motion while retaining one semantic text source. Prefer CSS `clip-path` on a single heading or two-layer design where the clone is `aria-hidden="true"` and the original remains readable by assistive technology.

The example uses a simple wrapper reveal, **not per-letter DOM splitting**. For per-character kinetic typography, ensure each character is decorative and the full text remains the only announced version. GSAP SplitText may have licensing/version constraints; verify them before using.
