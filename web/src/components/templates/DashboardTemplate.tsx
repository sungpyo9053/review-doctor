import type { ReactNode } from "react";
import { Main } from "../atoms/html";
import styles from "./DashboardTemplate.module.css";

interface DashboardTemplateProps {
  children: ReactNode;
}

export function DashboardTemplate({ children }: DashboardTemplateProps) {
  return <Main className={styles.template}>{children}</Main>;
}
