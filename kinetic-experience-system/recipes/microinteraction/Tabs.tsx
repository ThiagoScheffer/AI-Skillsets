import { useRef, useState } from "react";
import { LayoutGroup, motion, useReducedMotion } from "motion/react";

type Tab = { id: string; label: string; panel: string };

export function KxTabs({ tabs }: { tabs: Tab[] }) {
  const [active, setActive] = useState(tabs[0]?.id ?? "");
  const reduced = useReducedMotion();
  const buttonRefs = useRef<Record<string, HTMLButtonElement | null>>({});
  const index = tabs.findIndex((t) => t.id === active);
  const choose = (i: number) => {
    const next = tabs[(i + tabs.length) % tabs.length];
    setActive(next.id);
    buttonRefs.current[next.id]?.focus();
  };
  if (!tabs.length) return null;
  return (
    <LayoutGroup id="kx-tabs">
      <div role="tablist" aria-label="Content sections">
        {tabs.map((tab, i) => (
          <button key={tab.id} id={`tab-${tab.id}`} type="button" role="tab"
            ref={(node) => { buttonRefs.current[tab.id] = node; }}
            aria-selected={tab.id === active} aria-controls={`panel-${tab.id}`}
            tabIndex={tab.id === active ? 0 : -1}
            onClick={() => setActive(tab.id)}
            onKeyDown={(event) => {
              if (event.key === "ArrowRight") { event.preventDefault(); choose(index + 1); }
              if (event.key === "ArrowLeft") { event.preventDefault(); choose(index - 1); }
              if (event.key === "Home") { event.preventDefault(); choose(0); }
              if (event.key === "End") { event.preventDefault(); choose(tabs.length - 1); }
            }}>
            {tab.label}
            {tab.id === active && (
              <motion.span aria-hidden="true" className="kx-tab-indicator" layoutId="active-tab"
                transition={reduced ? { duration: 0 } : { type: "spring", stiffness: 400, damping: 35 }} />
            )}
          </button>
        ))}
      </div>
      {tabs.map((tab) => tab.id === active && (
        <section key={tab.id} role="tabpanel" id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`} tabIndex={0}>{tab.panel}</section>
      ))}
    </LayoutGroup>
  );
}
