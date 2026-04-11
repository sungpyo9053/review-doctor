import type { ReactNode } from "react";
import { useLocation } from "react-router-dom";
import { adminMenuItems } from "../../data/mockData";
import { AppLink } from "../atoms/AppLink";
import { Aside, Div, H1, Main, Nav, P } from "../atoms/html";
import { BrandLockup } from "../molecules/BrandLockup";
import styles from "./AdminConsoleTemplate.module.css";

interface AdminConsoleTemplateProps {
  title: string;
  description: string;
  children: ReactNode;
}

export function AdminConsoleTemplate({
  title,
  description,
  children,
}: AdminConsoleTemplateProps) {
  const location = useLocation();

  return (
    <Main className={styles.template}>
      <Aside className={styles.sidebar}>
        <BrandLockup subtitle="Admin Console" inverse />
        <Nav className={styles.sidebarNav}>
          {adminMenuItems.map((item) => (
            <AppLink
              key={item.path}
              to={item.path}
              tone="nav"
              className={location.pathname === item.path ? "is-active" : undefined}
            >
              {item.label}
            </AppLink>
          ))}
        </Nav>
      </Aside>

      <Div className={styles.main}>
        <Div className={styles.topbar}>
          <Div>
            <H1>{title}</H1>
            <P>{description}</P>
          </Div>
          <AppLink to="/" tone="dark" size="sm">
            서비스 홈
          </AppLink>
        </Div>
        <Div className={styles.content}>{children}</Div>
      </Div>
    </Main>
  );
}
