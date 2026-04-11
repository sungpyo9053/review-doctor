import { dashboardActionCards, dashboardMetrics, dashboardWeeklyTimeline } from "../../data/mockData";
import { AppLink } from "../atoms/AppLink";
import { Button } from "../atoms/Button";
import { Notice } from "../atoms/Notice";
import { Pill } from "../atoms/Pill";
import { Surface } from "../atoms/Surface";
import { Div, H2, H3, Li, P, Strong, Ul } from "../atoms/html";
import { StatCard } from "../molecules/StatCard";
import styles from "./DashboardSections.module.css";

interface DashboardOverviewProps {
  email: string;
  roleLabel: string;
  storeName: string;
  isOwner: boolean;
  onLogout: () => void;
}

export function DashboardOverview({
  email,
  roleLabel,
  storeName,
  isOwner,
  onLogout,
}: DashboardOverviewProps) {
  return (
    <>
      <Surface tone="accent" className={styles.hero}>
        <Div className={styles.heroCopy}>
          <Pill tone="highlight">{roleLabel}</Pill>
          <H2>{storeName} 운영 상태를 한눈에 확인하세요</H2>
          <P>
            {email} 계정으로 로그인되어 있으며, 이번 주 핵심 리뷰 인사이트와 다음 실행
            우선순위를 함께 볼 수 있습니다.
          </P>
        </Div>
        <Div className={styles.heroActions}>
          <AppLink to="/" tone="dark" size="sm">
            서비스 홈
          </AppLink>
          <Button tone="ghost" size="sm" onClick={onLogout}>
            로그아웃
          </Button>
        </Div>
      </Surface>

      <Div className={styles.metricGrid}>
        {dashboardMetrics.map((metric) => (
          <StatCard
            key={metric.label}
            label={metric.label}
            value={metric.value}
            note={metric.note}
          />
        ))}
      </Div>

      <Div className={styles.contentGrid}>
        <Surface tone="panel" className={styles.panel}>
          <P className={styles.panelEyebrow}>이번 주 액션</P>
          <H3>운영팀이 바로 실행할 수 있는 다음 단계</H3>
          <Div className={styles.actionGrid}>
            {dashboardActionCards.map((card) => (
              <Surface key={card.title} tone="muted" className={styles.actionCard}>
                <H3>{card.title}</H3>
                <P>{card.description}</P>
              </Surface>
            ))}
          </Div>
          {isOwner ? (
            <Notice tone="success">
              사업주 계정으로 로그인되어 있어 향후 가게 등록과 리포트 발행 흐름을 바로
              연결할 수 있습니다.
            </Notice>
          ) : (
            <Notice tone="info">
              일반 사용자 계정은 운영 리포트를 확인하고 팀 협업 용도로 활용할 수
              있도록 구성했습니다.
            </Notice>
          )}
        </Surface>

        <Surface tone="panel" className={styles.panel}>
          <P className={styles.panelEyebrow}>주간 흐름</P>
          <H3>리뷰 변화 포인트</H3>
          <Ul className={styles.timeline}>
            {dashboardWeeklyTimeline.map((item) => (
              <Li key={item}>{item}</Li>
            ))}
          </Ul>
          <Div className={styles.highlight}>
            <Strong>다음 추천 작업</Strong>
            <P>배달 속도 관련 개선 공지를 노출하고, 가격 언급 리뷰에 대한 응답 템플릿을 준비하세요.</P>
          </Div>
        </Surface>
      </Div>
    </>
  );
}
