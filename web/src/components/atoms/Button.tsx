import type { ButtonHTMLAttributes } from "react";
import { cx } from "../../utils/cx";
import { ButtonBase } from "./html";
import styles from "./Button.module.css";

type ButtonTone = "primary" | "secondary" | "ghost" | "dark" | "danger";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  tone?: ButtonTone;
  size?: ButtonSize;
  stretch?: boolean;
}

export function Button({
  tone = "primary",
  size = "md",
  stretch = false,
  className,
  type = "button",
  ...props
}: ButtonProps) {
  return (
    <ButtonBase
      type={type}
      className={cx(
        styles.button,
        styles[tone],
        styles[size],
        stretch && styles.stretch,
        className,
      )}
      {...props}
    />
  );
}
