import type { User } from "@supabase/supabase-js";
import { Main } from "../atoms/html";
import {
  FeatureSection,
  MarketingCta,
  MarketingFooterSection,
  MarketingHeader,
  MarketingHero,
  PlatformStrip,
  ReportSection,
} from "../organisms/MarketingSections";
import styles from "./MarketingTemplate.module.css";

interface MarketingTemplateProps {
  user: User | null;
  isAdmin: boolean;
  welcomeText: string;
  onLogout: () => void;
}

export function MarketingTemplate({
  user,
  isAdmin,
  welcomeText,
  onLogout,
}: MarketingTemplateProps) {
  return (
    <Main className={styles.page}>
      <MarketingHeader
        user={user}
        isAdmin={isAdmin}
        welcomeText={welcomeText}
        onLogout={onLogout}
      />
      <MarketingHero user={user} isAdmin={isAdmin} />
      <PlatformStrip />
      <FeatureSection />
      <ReportSection />
      <MarketingCta user={user} isAdmin={isAdmin} />
      <MarketingFooterSection />
    </Main>
  );
}
