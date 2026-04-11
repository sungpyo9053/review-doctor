import type { HTMLAttributes } from "react";
import { cx } from "../../utils/cx";
import { Div } from "./html";
import styles from "./Surface.module.css";

type SurfaceTone = "default" | "glass" | "panel" | "accent" | "muted";

interface SurfaceProps extends HTMLAttributes<HTMLDivElement> {
  tone?: SurfaceTone;
  padded?: boolean;
}

export function Surface({
  tone = "default",
  padded = true,
  className,
  ...props
}: SurfaceProps) {
  return (
    <Div
      className={cx(
        styles.surface,
        styles[tone],
        padded && styles.padded,
        className,
      )}
      {...props}
    />
  );
}
