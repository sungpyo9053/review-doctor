import { Surface } from "../atoms/Surface";
import { H3, P } from "../atoms/html";
import styles from "./StatCard.module.css";

interface StatCardProps {
  label: string;
  value: string;
  note: string;
}

export function StatCard({ label, value, note }: StatCardProps) {
  return (
    <Surface tone="panel" className={styles.statCard}>
      <P className={styles.label}>{label}</P>
      <H3 className={styles.value}>{value}</H3>
      <P className={styles.note}>{note}</P>
    </Surface>
  );
}
