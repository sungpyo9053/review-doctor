import { AppLink } from "@/components/atoms/AppLink";
import { Notice } from "@/components/atoms/Notice";
import { H2, P } from "@/components/atoms/html";
import { AuthSplitTemplate } from "@/components/templates/AuthSplitTemplate";
import styles from "../../auth/AuthForm.module.css";

function JoinSuccessPage() {
  return (
    <AuthSplitTemplate
      eyebrow="Signup Complete"
      title="가입이 완료되었습니다"
      description="이제 이메일 인증 여부를 확인한 뒤 로그인해서 대시보드와 관리자 콘솔 구조를 바로 확인할 수 있습니다."
    >
      <Notice tone="success" className={styles.successBanner}>
        계정이 정상적으로 생성되었습니다.
      </Notice>
      <H2 className={styles.title}>회원가입이 완료되었습니다</H2>
      <P className={styles.description}>
        이메일 인증이 필요한 경우 메일함을 확인한 뒤 로그인해주세요.
      </P>
      <AppLink to="/login" tone="dark" stretch>
        로그인 하러가기
      </AppLink>
    </AuthSplitTemplate>
  );
}

export default JoinSuccessPage;
