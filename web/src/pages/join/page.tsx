import { observer } from "mobx-react-lite";
import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { AppLink } from "@/components/atoms/AppLink";
import { Button } from "@/components/atoms/Button";
import { Checkbox } from "@/components/atoms/Checkbox";
import { FieldInput } from "@/components/atoms/FieldInput";
import { Notice } from "@/components/atoms/Notice";
import { Div, Form, H2, P, Span } from "@/components/atoms/html";
import { FormField } from "@/components/molecules/FormField";
import { AuthSplitTemplate } from "@/components/templates/AuthSplitTemplate";
import { useStore } from "@/stores/useStore";
import type { GenderOption } from "@/types/auth";
import { cx } from "@/utils/cx";
import styles from "../auth/AuthForm.module.css";

interface SignupFormState {
  name: string;
  birth: string;
  gender: GenderOption;
  email: string;
  password: string;
  passwordConfirm: string;
  phone: string;
  isOwner: boolean;
  storeName: string;
}

const initialState: SignupFormState = {
  name: "",
  birth: "",
  gender: "none",
  email: "",
  password: "",
  passwordConfirm: "",
  phone: "",
  isOwner: false,
  storeName: "",
};

const SignupPage = observer(() => {
  const navigate = useNavigate();
  const { authStore } = useStore();
  const [form, setForm] = useState<SignupFormState>(initialState);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const updateField = <K extends keyof SignupFormState>(key: K, value: SignupFormState[K]) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!form.name.trim() || !form.email.trim() || !form.password.trim() || !form.passwordConfirm.trim()) {
      setMessage("필수 항목을 모두 입력하세요.");
      return;
    }

    if (form.password !== form.passwordConfirm) {
      setMessage("비밀번호가 일치하지 않습니다.");
      return;
    }

    if (form.password.length < 6) {
      setMessage("비밀번호는 6자 이상이어야 합니다.");
      return;
    }

    if (form.isOwner && !form.storeName.trim()) {
      setMessage("사업주 계정은 가게명을 입력해주세요.");
      return;
    }

    setLoading(true);
    setMessage("");

    const result = await authStore.signUp({
      name: form.name,
      birth: form.birth,
      gender: form.gender,
      email: form.email,
      password: form.password,
      phone: form.phone,
      isOwner: form.isOwner,
      storeName: form.storeName,
    });

    setLoading(false);

    if (!result.success) {
      setMessage(result.message ?? "회원가입 중 문제가 발생했습니다.");
      return;
    }

    navigate("/join/success");
  };

  return (
    <AuthSplitTemplate
      eyebrow="Create Account"
      title="회원 유형에 맞는 리뷰 운영 워크스페이스를 시작하세요"
      description="가입 화면도 atom과 molecule로 정리해 이후 입력 폼 확장이나 검증 규칙 추가가 쉬운 구조로 바꿨습니다."
      footer={
        <P className={styles.footerCopy}>
          이미 계정이 있나요?{" "}
          <AppLink to="/login" tone="inline" size="sm">
            로그인
          </AppLink>
        </P>
      }
    >
      <P className={styles.eyebrow}>Membership Setup</P>
      <H2 className={styles.title}>회원가입</H2>
      <P className={styles.description}>회원가입 정보를 입력해주세요.</P>

      {!authStore.isAuthConfigured ? (
        <Notice tone="error">{authStore.authUnavailableMessage}</Notice>
      ) : null}

      <Form className={cx(styles.form, styles.formSpacious)} onSubmit={handleSubmit}>
        <Div className={styles.section}>
          <P className={styles.sectionTitle}>계정 정보</P>
          <Div className={styles.grid}>
            <FormField label="이름">
              <FieldInput
                type="text"
                placeholder="이름"
                value={form.name}
                onChange={(event) => updateField("name", event.target.value)}
              />
            </FormField>

            <FormField label="이메일">
              <FieldInput
                type="email"
                placeholder="example@email.com"
                value={form.email}
                onChange={(event) => updateField("email", event.target.value)}
              />
            </FormField>

            <FormField label="비밀번호">
              <FieldInput
                type="password"
                placeholder="비밀번호"
                value={form.password}
                onChange={(event) => updateField("password", event.target.value)}
              />
            </FormField>

            <FormField label="비밀번호 확인">
              <FieldInput
                type="password"
                placeholder="비밀번호 확인"
                value={form.passwordConfirm}
                onChange={(event) => updateField("passwordConfirm", event.target.value)}
              />
            </FormField>
          </Div>
        </Div>

        <Div className={styles.section}>
          <P className={styles.sectionTitle}>추가 정보</P>
          <Div className={styles.grid}>
            <FormField label="생년월일 8자리" hint="예: 19900101">
              <FieldInput
                type="text"
                inputMode="numeric"
                placeholder="19900101"
                value={form.birth}
                onChange={(event) => updateField("birth", event.target.value)}
              />
            </FormField>

            <FormField label="휴대전화번호" hint="숫자만 입력">
              <FieldInput
                type="text"
                inputMode="tel"
                placeholder="01012345678"
                value={form.phone}
                onChange={(event) => updateField("phone", event.target.value)}
              />
            </FormField>
          </Div>

          <Div className={styles.choiceGroup}>
            <Span className={styles.choiceLabel}>성별</Span>
            <Div className={styles.choiceButtons}>
              {[
                { label: "남자", value: "male" },
                { label: "여자", value: "female" },
                { label: "선택안함", value: "none" },
              ].map((option) => (
                <Button
                  key={option.value}
                  tone={form.gender === option.value ? "dark" : "secondary"}
                  size="sm"
                  onClick={() => updateField("gender", option.value as GenderOption)}
                >
                  {option.label}
                </Button>
              ))}
            </Div>
          </Div>
        </Div>

        <Div className={styles.section}>
          <P className={styles.sectionTitle}>가입 유형</P>
          <Div className={styles.checkboxRow}>
            <Checkbox
              checked={form.isOwner}
              onChange={(event) => updateField("isOwner", event.target.checked)}
            />
            <P>사업주로 가입합니다</P>
          </Div>
          <P className={styles.helper}>
            사업주 계정은 가게 등록, 리뷰 분석 리포트, 대시보드 기능을 사용할 수 있습니다.
          </P>

          {form.isOwner ? (
            <FormField label="가게명">
              <FieldInput
                type="text"
                placeholder="예: 홍대 김밥천국"
                value={form.storeName}
                onChange={(event) => updateField("storeName", event.target.value)}
              />
            </FormField>
          ) : null}
        </Div>

        {message ? <Notice tone="error">{message}</Notice> : null}

        <Div className={styles.actions}>
          <Button type="submit" tone="dark" stretch disabled={loading}>
            {loading ? "가입 중..." : "회원가입"}
          </Button>
        </Div>
      </Form>
    </AuthSplitTemplate>
  );
});

export default SignupPage;
