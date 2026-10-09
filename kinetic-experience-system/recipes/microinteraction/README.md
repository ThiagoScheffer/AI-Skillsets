# Local state as motion system

Use subtle local Motion/CSS reactions to reinforce state and hierarchy without changing routing. Complex menus and dialogs need correct ARIA, focus and Escape semantics independently from animation.

Example: `Tabs.tsx` animates a shared active underline via Motion `layoutId` and retains real `role=tab` semantics. Test rapid keyboard navigation, Home/End (add as needed), reduced motion and overflow. For production tabs, implement the full WAI-ARIA tabs keyboard pattern, focus model and stable tabpanel IDs.
