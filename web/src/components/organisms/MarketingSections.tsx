import type { User } from "@supabase/supabase-js";
import {
  authFeatureBullets,
  footerColumns,
  marketingFeatures,
  marketingPlatforms,
  reportProgressItems,
} from "../../data/mockData";
import { cx } from "../../utils/cx";
import { AppLink } from "../atoms/AppLink";
import { Button } from "../atoms/Button";
import { Pill } from "../atoms/Pill";
import { Surface } from "../atoms/Surface";
import {
  Div,
  Footer,
  H1,
  H2,
  H3,
  H4,
  Header,
  Li,
  Nav,
  P,
  Section,
  Small,
  Span,
  Strong,
  Ul,
} from "../atoms/html";
import { BrandLockup } from "../molecules/BrandLockup";
import styles from "./MarketingSections.module.css";

interface MarketingActionProps {
  user: User | null;
  isAdmin: boolean;
}

export function MarketingHeader({
  user,
  isAdmin,
  welcomeText,
  onLogout,
}: MarketingActionProps & {
  welcomeText: string;
  onLogout: () => void;
}) {
  return (
    <Header className={styles.header}>
      <Div className={cx(styles.container, styles.headerInner)}>
        <BrandLockup inverse subtitle="Store Intelligence Platform" />
        <Nav className={styles.nav}>
          {!user ? (
            <>
              <AppLink href="#features" tone="nav" size="sm">
                Features
              </AppLink>
              <AppLink href="#report" tone="nav" size="sm">
                Report
              </AppLink>
              <AppLink to="/login" tone="inline" size="sm">
                Login
              </AppLink>
              <AppLink to="/join" tone="primary" size="sm">
                Get Started
              </AppLink>
            </>
          ) : (
            <>
              <P className={styles.navWelcome}>{welcomeText}</P>
              <AppLink to={isAdmin ? "/admin" : "/dashboard"} tone="secondary" size="sm">
                {isAdmin ? "관리자페이지" : "대시보드"}
              </AppLink>
              <Button tone="ghost" size="sm" onClick={onLogout}>
                로그아웃
              </Button>
            </>
          )}
        </Nav>
      </Div>
    </Header>
  );
}

export function MarketingHero({ user, isAdmin }: MarketingActionProps) {
  return (
    <Section className={styles.hero}>
      <Div className={cx(styles.container, styles.heroGrid)}>
        <Div className={styles.heroCopy}>
          <Pill tone="info">NEW · AI Review Intelligence</Pill>
          <H1 className={styles.heroTitle}>
            <Span className={styles.titleLine}>사장님의 운영 고민을</Span>
            <Span className={styles.titleAccentLine}>리뷰 데이터</Span>
            <Span className={styles.titleLine}>중심으로 바꿉니다</Span>
          </H1>
          <P className={styles.heroDescription}>
            네이버, 배민, 쿠팡이츠, 구글 리뷰를 한곳에 모아 AI가 감정 분석, 키워드
            추적, 강점과 약점 정리까지 자동으로 제공합니다.
          </P>

          <Div className={styles.heroActions}>
            {!user ? (
              <>
                <AppLink to="/join" tone="primary">
                  무료로 시작하기
                </AppLink>
                <AppLink href="#report" tone="secondary">
                  리포트 보기
                </AppLink>
              </>
            ) : (
              <>
                <AppLink to={isAdmin ? "/admin" : "/dashboard"} tone="primary">
                  {isAdmin ? "관리자페이지로 이동" : "대시보드로 이동"}
                </AppLink>
                <AppLink href="#report" tone="secondary">
                  분석 예시 보기
                </AppLink>
              </>
            )}
          </Div>

          <Ul className={styles.heroBulletList}>
            {authFeatureBullets.map((item) => (
              <Li key={item}>{item}</Li>
            ))}
          </Ul>
        </Div>

        <Surface tone="glass" className={styles.preview}>
          <Div className={styles.floating}>
            <Span className={styles.dot} />
            불만 키워드 18% 감소
            <Small>지난주보다 개선됨</Small>
          </Div>

          <Div className={styles.window}>
            <Span />
            <Span />
            <Span />
          </Div>

          <Surface tone="accent" className={styles.summary}>
            <P className={styles.eyebrow}>이번 주 리뷰 분석</P>
            <Strong className={styles.headline}>128</Strong>
            <P className={styles.caption}>수집된 리뷰 수</P>

            <Div className={styles.stats}>
              <Div>
                <Strong>72%</Strong>
                <Span>긍정</Span>
              </Div>
              <Div>
                <Strong>18%</Strong>
                <Span>부정</Span>
              </Div>
              <Div>
                <Strong>10%</Strong>
                <Span>중립</Span>
              </Div>
            </Div>
          </Surface>

          <Div className={styles.cards}>
            <Surface tone="panel" className={styles.miniCard}>
              <P className={styles.miniLabel}>긍정 키워드</P>
              <Strong>맛 · 친절 · 청결</Strong>
            </Surface>
            <Surface tone="panel" className={styles.miniCard}>
              <P className={styles.miniLabel}>개선 필요</P>
              <Strong>배달시간 · 가격</Strong>
            </Surface>
          </Div>

          <Surface tone="panel" className={styles.chart}>
            <Div className={styles.chartHead}>
              <Span>주간 평점 변화</Span>
              <Strong>4.8</Strong>
            </Div>
            <Div className={styles.bars}>
              {[60, 68, 62, 74, 82, 76, 70].map((value, index) => (
                <Span
                  key={`${value}-${index}`}
                  className={cx(styles.bar, (index === 4 || index === 5) && styles.barActive)}
                  style={{ height: `${value}%` }}
                />
              ))}
            </Div>
            <Div className={styles.labels}>
              {["월", "화", "수", "목", "금", "토", "일"].map((day) => (
                <Span key={day}>{day}</Span>
              ))}
            </Div>
          </Surface>
        </Surface>
      </Div>
    </Section>
  );
}

export function PlatformStrip() {
  return (
    <Section className={styles.platforms}>
      <Div className={styles.container}>
        <P className={styles.platformsTitle}>활용 중인 리뷰 플랫폼</P>
        <Div className={styles.platformsGrid}>
          {marketingPlatforms.map((platform) => (
            <Surface key={platform} tone="glass" className={styles.platformsCard}>
              {platform}
            </Surface>
          ))}
        </Div>
      </Div>
    </Section>
  );
}

export function FeatureSection() {
  return (
    <Section id="features" className={styles.section}>
      <Div className={styles.container}>
        <Div className={styles.sectionHeading}>
          <Pill tone="highlight">Atomic Design + MobX</Pill>
          <H2>강력한 AI 리뷰 분석 서비스</H2>
          <P>국내 주요 리뷰 플랫폼의 고객 반응을 한눈에 모아보고 분석하세요.</P>
        </Div>
        <Div className={styles.featureGrid}>
          {marketingFeatures.map((feature) => (
            <Surface key={feature.title} tone="panel" className={styles.featureCard}>
              <Div className={styles.featureCardIndex}>{feature.icon}</Div>
              <H3>{feature.title}</H3>
              <P>{feature.description}</P>
            </Surface>
          ))}
        </Div>
      </Div>
    </Section>
  );
}

export function ReportSection() {
  return (
    <Section id="report" className={styles.report}>
      <Div className={cx(styles.container, styles.reportGrid)}>
        <Div className={styles.reportCopy}>
          <Pill tone="positive">Weekly Report Snapshot</Pill>
          <H2>리뷰 분석 리포트를 매주 한 장으로 요약합니다</H2>
          <P>
            매장의 강점과 약점이 어떻게 변하는지 확인하고, AI가 추천한 운영 개선
            방향까지 한 번에 연결하세요.
          </P>
          <Ul className={styles.reportList}>
            <Li>실시간 키워드 급증 추적</Li>
            <Li>경쟁점 비교 분석</Li>
            <Li>고객 만족도 추이 확인</Li>
          </Ul>
        </Div>

        <Div className={styles.reportCards}>
          <Surface tone="panel" className={styles.reportCard}>
            <Div className={styles.reportCardHead}>
              <Span>긍정 키워드 TOP 5</Span>
              <Strong>+12%</Strong>
            </Div>
            <H3 className={styles.keywordLine}>
              맛, 서비스, 청결, 가성비, 양
            </H3>
            <Div className={styles.progressList}>
              {reportProgressItems.map((item) => (
                <Div key={item.label} className={styles.progressRow}>
                  <Span>{item.label}</Span>
                  <Div className={styles.progressTrack}>
                    <Div className={styles.progressFill} style={{ width: `${item.value}%` }} />
                  </Div>
                </Div>
              ))}
            </Div>
          </Surface>

          <Surface tone="panel" className={styles.reportCard}>
            <Div className={styles.reportCardHead}>
              <Span>주간 평점 변화</Span>
              <Strong className={styles.negative}>-0.1</Strong>
            </Div>
            <H3 className={styles.score}>4.8</H3>
            <Div className={cx(styles.bars, styles.barsWide)}>
              {[60, 66, 58, 72, 84, 74, 68].map((value, index) => (
                <Span
                  key={`${value}-${index}`}
                  className={cx(styles.bar, (index === 4 || index === 5) && styles.barActive)}
                  style={{ height: `${value}%` }}
                />
              ))}
            </Div>
            <Div className={styles.labels}>
              {["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"].map((day) => (
                <Span key={day}>{day}</Span>
              ))}
            </Div>
          </Surface>
        </Div>
      </Div>
    </Section>
  );
}

export function MarketingCta({ user, isAdmin }: MarketingActionProps) {
  return (
    <Section className={styles.cta}>
      <Div className={styles.container}>
        <Surface tone="accent" className={styles.ctaCard}>
          <Div>
            <Pill tone="highlight">2주 무료 체험</Pill>
            <H2>지금 바로 리뷰 운영 체계를 정리해보세요</H2>
            <P>
              복잡한 설정 없이 가게 정보만 입력하면 AI가 즉시 분석을 시작합니다.
            </P>
          </Div>
          <Div className={styles.ctaActions}>
            {!user ? (
              <>
                <AppLink to="/join" tone="dark">
                  2주 무료 체험 시작하기
                </AppLink>
                <AppLink href="#features" tone="ghost">
                  기능 먼저 보기
                </AppLink>
              </>
            ) : (
              <>
                <AppLink to={isAdmin ? "/admin" : "/dashboard"} tone="dark">
                  {isAdmin ? "관리자페이지 이동" : "대시보드 바로가기"}
                </AppLink>
                <AppLink href="#report" tone="ghost">
                  가격 플랜 확인
                </AppLink>
              </>
            )}
          </Div>
        </Surface>
      </Div>
    </Section>
  );
}

export function MarketingFooterSection() {
  return (
    <Footer className={styles.footer}>
      <Div className={cx(styles.container, styles.footerGrid)}>
        <Div className={styles.footerBrand}>
          <BrandLockup inverse />
          <P>
            AI 기반 리뷰 분석으로 자영업자의 운영 결정을 더 빠르게 돕습니다.
          </P>
        </Div>
        <Div className={styles.footerColumns}>
          {footerColumns.map((column) => (
            <Div key={column.title} className={styles.footerColumn}>
              <H4>{column.title}</H4>
              {column.links.map((link) => (
                <AppLink
                  key={link.label}
                  href={link.href}
                  tone="inline"
                  size="sm"
                  className={styles.footerLink}
                >
                  {link.label}
                </AppLink>
              ))}
            </Div>
          ))}
        </Div>
      </Div>
    </Footer>
  );
}
