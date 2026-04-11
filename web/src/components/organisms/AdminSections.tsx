import type { ReactNode } from "react";
import { adminStats } from "../../data/mockData";
import { Button } from "../atoms/Button";
import { FieldInput } from "../atoms/FieldInput";
import { Notice } from "../atoms/Notice";
import { Pill } from "../atoms/Pill";
import { Surface } from "../atoms/Surface";
import { Div, H2, H3, P, Span } from "../atoms/html";
import { StatCard } from "../molecules/StatCard";
import styles from "./AdminSections.module.css";

interface PanelShellProps {
  title: string;
  description?: string;
  children: ReactNode;
}

interface AdminEmailManagerProps {
  emails: string[];
  currentUserEmail?: string | null;
  newEmail: string;
  message: string;
  messageTone: "success" | "error";
  onEmailChange: (value: string) => void;
  onAdd: () => void;
  onRemove: (email: string) => void;
}

export function PanelShell({ title, description, children }: PanelShellProps) {
  return (
    <Surface tone="panel" className={styles.panel}>
      <Div className={styles.panelHeading}>
        <H3>{title}</H3>
        {description ? <P>{description}</P> : null}
      </Div>
      {children}
    </Surface>
  );
}

export function AdminMetricsGrid() {
  return (
    <Div className={styles.metricGrid}>
      {adminStats.map((item) => (
        <StatCard key={item.label} label={item.label} value={item.value} note={item.note} />
      ))}
    </Div>
  );
}

export function AdminEmailManager({
  emails,
  currentUserEmail,
  newEmail,
  message,
  messageTone,
  onEmailChange,
  onAdd,
  onRemove,
}: AdminEmailManagerProps) {
  return (
    <Div className={styles.stack}>
      <PanelShell
        title="현재 관리자 목록"
        description="등록된 관리자 이메일은 즉시 권한 계산에 반영되며 브라우저 로컬 스토리지에도 저장됩니다."
      >
        <Div className={styles.emailManager}>
          {emails.length > 0 ? (
            emails.map((email) => (
              <Div key={email} className={styles.emailManagerRow}>
                <Div className={styles.emailManagerCopy}>
                  <Span>{email}</Span>
                  {email === currentUserEmail ? <Pill tone="info">현재 로그인 계정</Pill> : null}
                </Div>
                <Button
                  tone="ghost"
                  size="sm"
                  onClick={() => onRemove(email)}
                  disabled={email === currentUserEmail}
                >
                  삭제
                </Button>
              </Div>
            ))
          ) : (
            <Notice tone="info">등록된 관리자 이메일이 없습니다.</Notice>
          )}
        </Div>
      </PanelShell>

      <PanelShell
        title="관리자 추가"
        description="새 관리자 이메일을 등록하면 다음 로그인부터 관리자 콘솔 접근이 가능합니다."
      >
        <Div className={styles.emailManagerCreate}>
          <FieldInput
            type="email"
            placeholder="관리자 이메일 입력"
            value={newEmail}
            onChange={(event) => onEmailChange(event.target.value)}
          />
          <Button tone="primary" onClick={onAdd}>
            추가
          </Button>
        </Div>
        {message ? <Notice tone={messageTone}>{message}</Notice> : null}
      </PanelShell>
    </Div>
  );
}

export function PlaceholderPanel({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <Surface tone="panel" className={styles.placeholder}>
      <Pill tone="highlight">준비 중</Pill>
      <H2>{title}</H2>
      <P>{description}</P>
      <Div className={styles.placeholderList}>
        <Span>공통 atom/molecule 기반으로 세부 기능을 이어 붙일 수 있게 템플릿을 먼저 정리해두었습니다.</Span>
        <Span>이제 실제 API 연동만 얹으면 동일한 레이아웃 체계로 자연스럽게 확장할 수 있습니다.</Span>
      </Div>
    </Surface>
  );
}
