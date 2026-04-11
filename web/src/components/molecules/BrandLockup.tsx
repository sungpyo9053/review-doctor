import { AppLink } from "../atoms/AppLink";
import { Div, P, Strong } from "../atoms/html";
import { cx } from "../../utils/cx";
import styles from "./BrandLockup.module.css";

interface BrandLockupProps {
  subtitle?: string;
  to?: string;
  inverse?: boolean;
}

export function BrandLockup({
  subtitle = "AI Review Intelligence",
  to = "/",
  inverse = false,
}: BrandLockupProps) {
  return (
    <AppLink
      to={to}
      tone="inline"
      className={cx(styles.brandLockup, inverse && styles.inverse)}
    >
      <Div className={styles.icon}>RD</Div>
      <Div className={styles.copy}>
        <Strong className={styles.title}>Review Doctor</Strong>
        <P className={styles.subtitle}>{subtitle}</P>
      </Div>
    </AppLink>
  );
}
