import { useState } from "react";
import { AnimatePresence, LayoutGroup, motion, useReducedMotion } from "motion/react";

type Project = { id: string; title: string; summary: string; image: string };

export function SharedPreview({ projects }: { projects: Project[] }) {
  const [selected, setSelected] = useState<string | null>(null);
  const reduced = useReducedMotion();
  const item = projects.find((project) => project.id === selected);
  const spring = { type: "spring" as const, stiffness: 320, damping: 34 };
  const transition = reduced ? { duration: 0 } : spring;

  return (
    <LayoutGroup id="kx-portfolio">
      <section aria-label="Projects" className="kx-grid">
        {projects.map((project) => (
          <button type="button" key={project.id} onClick={() => setSelected(project.id)}>
            <motion.img
              layoutId={`project-image-${project.id}`}
              transition={transition}
              src={project.image}
              alt=""
            />
            <span>{project.title}</span>
          </button>
        ))}
      </section>
      <AnimatePresence mode="sync">
        {item && (
          <motion.section
            key={item.id}
            aria-label={`Selected project: ${item.title}`}
            className="kx-preview"
            initial={reduced ? false : { opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <button type="button" onClick={() => setSelected(null)}>
              Close preview
            </button>
            <motion.img
              layoutId={`project-image-${item.id}`}
              transition={transition}
              src={item.image}
              alt=""
            />
            <h2>{item.title}</h2>
            <p>{item.summary}</p>
          </motion.section>
        )}
      </AnimatePresence>
    </LayoutGroup>
  );
}
