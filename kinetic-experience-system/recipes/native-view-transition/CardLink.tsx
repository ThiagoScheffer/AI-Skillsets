import { Link, useViewTransitionState } from "react-router";

type Props = { id: string; title: string; imageUrl: string };

/** Example source endpoint; coordinate destination names in your route. */
export function ProductCardLink({ id, title, imageUrl }: Props) {
  const to = `/products/${encodeURIComponent(id)}`;
  const isTransitioning = useViewTransitionState(to);
  return (
    <Link to={to} viewTransition className="kx-product-card">
      <img
        alt=""
        src={imageUrl}
        style={{ viewTransitionName: isTransitioning ? "kx-selected-product" : "none" }}
      />
      <span>{title}</span>
    </Link>
  );
}
