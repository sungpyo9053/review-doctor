import type { ReactNode } from "react";
import { Div, Label, P } from "../atoms/html";
import styles from "./FormField.module.css";

interface FormFieldProps {
  label: string;
  hint?: string;
  children: ReactNode;
}

export function FormField({ label, hint, children }: FormFieldProps) {
  return (
    <Div className={styles.field}>
      <Label className={styles.label}>{label}</Label>
      {children}
      {hint ? <P className={styles.hint}>{hint}</P> : null}
    </Div>
  );
}
