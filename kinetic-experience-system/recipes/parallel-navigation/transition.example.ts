// Illustrative Hyperkinetic alpha API as documented on 2026-10-08.
// VERIFY against the actual installed version before copying.
import gsap from "gsap";
import type { AnimatedOutletProps } from "hyperkinetic";

export const transition = {
  initial: false,
  beforeEnter: ({ next }) => {
    // Prepare the incoming route to avoid a visible flash.
    gsap.set(next.container, { autoAlpha: 0 });
  },
  choreograph: ({ tl, current, next }) => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    tl.addLabel("navigation-start", 0);
    tl.to(current.container, { autoAlpha: 0, duration: reduced ? 0 : 0.32 }, "navigation-start");
    tl.to(next.container, { autoAlpha: 1, duration: reduced ? 0 : 0.46 }, "navigation-start+=0.12");
  },
} satisfies AnimatedOutletProps;
