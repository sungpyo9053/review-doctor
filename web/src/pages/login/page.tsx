import { observer } from "mobx-react-lite";
import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { AppLink } from "@/components/atoms/AppLink";
import { Button } from "@/components/atoms/Button";
import { FieldInput } from "@/components/atoms/FieldInput";
import { Notice } from "@/components/atoms/Notice";
import { Div, Form, H2, P } from "@/components/atoms/html";
import { FormField } from "@/components/molecules/FormField";
import { AuthSplitTemplate } from "@/components/templates/AuthSplitTemplate";
import { useStore } from "@/stores/useStore";
import styles from "../auth/AuthForm.module.css";

const LoginPage = observer(() => {
  const navigate = useNavigate();
  const { authStore, adminStore } = useStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!email.trim() || !password.trim()) {
      setMessage("이메일과 비밀번호를 입력하세요.");
      return;
    }

    setLoading(true);
    setMessage("");

    const result = await authStore.signIn(email, password);

    setLoading(false);

    if (!result.success) {
      setMessage(result.message ?? "로그인 중 문제가 발생했습니다.");
      return;
    }

    const destination = adminStore.isAdminEmail(result.user?.email) ? "/admin" : "/dashboard";
    navigate(destination);
  };

  return (
    <AuthSplitTemplate
      eyebrow="Account Access"
      title="로그인과 동시에 매장 리뷰 흐름을 파악하세요"
      description="운영팀과 사업주가 같은 데이터 흐름을 보도록 인증 화면도 템플릿 기반으로 정리했습니다."
      footer={
        <P className={styles.footerCopy}>
          계정이 없나요?{" "}
          <AppLink to="/join" tone="inline" size="sm">
            회원가입
          </AppLink>
        </P>
      }
    >
      <P className={styles.eyebrow}>Review Doctor Access</P>
      <H2 className={styles.title}>로그인</H2>
      <P className={styles.description}>Review Doctor를 시작하세요.</P>

      {!authStore.isAuthConfigured ? (
        <Notice tone="error">{authStore.authUnavailableMessage}</Notice>
      ) : null}

      <Form className={styles.form} onSubmit={handleSubmit}>
        <FormField label="이메일">
          <FieldInput
            type="email"
            placeholder="example@email.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </FormField>

        <FormField label="비밀번호">
          <FieldInput
            type="password"
            placeholder="비밀번호를 입력하세요"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </FormField>

        {message ? <Notice tone="error">{message}</Notice> : null}

        <Div className={styles.actions}>
          <Button type="submit" tone="dark" stretch disabled={loading}>
            {loading ? "로그인 중..." : "로그인"}
          </Button>
        </Div>
      </Form>
    </AuthSplitTemplate>
  );
});

export default LoginPage;
