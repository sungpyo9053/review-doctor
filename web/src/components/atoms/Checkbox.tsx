import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils/cx";
import { InputBase } from "./html";
import styles from "./Checkbox.module.css";

export function Checkbox({
  className,
  type = "checkbox",
  ...props
}: InputHTMLAttributes<HTMLInputElement>) {
  return <InputBase type={type} className={cx(styles.checkbox, className)} {...props} />;
}
