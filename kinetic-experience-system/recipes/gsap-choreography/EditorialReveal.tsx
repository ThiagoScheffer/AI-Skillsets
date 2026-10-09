import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

export function EditorialReveal({ title, copy }: { title: string; copy: string }) {
  const root = useRef<HTMLElement>(null);
  useGSAP(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
    tl.addLabel("start", 0)
      .from("[data-kx-eyebrow]", { autoAlpha: 0, y: 12, duration: 0.25 }, "start")
      .from("[data-kx-heading]", { autoAlpha: 0, y: 26, duration: 0.55 }, "start+=0.1")
      .from("[data-kx-copy]", { autoAlpha: 0, y: 12, duration: 0.3 }, "<45%");
  }, { scope: root });

  return (
    <section ref={root} aria-labelledby="kx-heading">
      <span data-kx-eyebrow>Selected work</span>
      <h2 id="kx-heading" data-kx-heading>{title}</h2>
      <p data-kx-copy>{copy}</p>
    </section>
  );
}
