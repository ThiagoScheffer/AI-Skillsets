/**
 * Animate a decorative proxy between two DOM rectangles.
 * The source and destination remain under the app's normal routing/state control.
 * The proxy must be non-interactive and accessible name remains on the real content.
 */
export async function morphProxy(
  source: HTMLElement | null,
  destination: HTMLElement | null,
  proxy: HTMLElement,
  duration = 420,
): Promise<void> {
  if (!source || !destination) { proxy.remove(); return; }
  const a = source.getBoundingClientRect();
  const b = destination.getBoundingClientRect();
  if (!a.width || !a.height || !b.width || !b.height) { proxy.remove(); return; }
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) { proxy.remove(); return; }

  proxy.setAttribute("aria-hidden", "true");
  proxy.style.pointerEvents = "none";
  proxy.style.position = "fixed";
  proxy.style.left = `${b.left}px`;
  proxy.style.top = `${b.top}px`;
  proxy.style.width = `${b.width}px`;
  proxy.style.height = `${b.height}px`;
  proxy.style.transformOrigin = "top left";
  const dx = a.left - b.left;
  const dy = a.top - b.top;
  const sx = a.width / b.width;
  const sy = a.height / b.height;
  try {
    const animation = proxy.animate(
      [{ transform: `translate(${dx}px, ${dy}px) scale(${sx}, ${sy})` }, { transform: "none" }],
      { duration, easing: "cubic-bezier(.2,.8,.2,1)" },
    );
    await animation.finished;
  } catch {
    // An interrupted animation rejects finished; cleanup remains mandatory.
  } finally {
    proxy.remove();
  }
}
