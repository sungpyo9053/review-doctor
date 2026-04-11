import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils/cx";
import { InputBase } from "./html";
import styles from "./FieldInput.module.css";

export function FieldInput({
  className,
  ...props
}: InputHTMLAttributes<HTMLInputElement>) {
  return <InputBase className={cx(styles.input, className)} {...props} />;
}
