import type { ReactNode } from "react";
import { authFeatureBullets } from "../../data/mockData";
import { AppLink } from "../atoms/AppLink";
import { Pill } from "../atoms/Pill";
import { Surface } from "../atoms/Surface";
import { Div, H1, Li, Main, P, Ul } from "../atoms/html";
import { BrandLockup } from "../molecules/BrandLockup";
import { cx } from "../../utils/cx";
import styles from "./AuthSplitTemplate.module.css";

interface AuthSplitTemplateProps {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
  footer?: ReactNode;
}

export function AuthSplitTemplate({
  eyebrow,
  title,
  description,
  children,
  footer,
}: AuthSplitTemplateProps) {
  return (
    <Main className={styles.template}>
      <Div className={cx(styles.panel, styles.featurePanel)}>
        <Div className={styles.featureContent}>
          <BrandLockup subtitle="Store Intelligence Platform" />
          <Pill tone="highlight">{eyebrow}</Pill>
          <H1>{title}</H1>
          <P>{description}</P>
          <Ul className={styles.featureList}>
            {authFeatureBullets.map((item) => (
              <Li key={item}>{item}</Li>
            ))}
          </Ul>
          <AppLink to="/" tone="secondary">
            홈으로 돌아가기
          </AppLink>
        </Div>
      </Div>

      <Div className={cx(styles.panel, styles.formPanel)}>
        <Surface tone="panel" className={styles.panelCard}>
          {children}
          {footer ? <Div className={styles.panelCardFooter}>{footer}</Div> : null}
        </Surface>
      </Div>
    </Main>
  );
}
