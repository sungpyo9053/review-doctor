import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/atoms/Button";
import { FieldInput } from "@/components/atoms/FieldInput";
import { Notice } from "@/components/atoms/Notice";
import { Form, H2, P } from "@/components/atoms/html";
import { FormField } from "@/components/molecules/FormField";
import { AuthSplitTemplate } from "@/components/templates/AuthSplitTemplate";
import { useStore } from "@/stores/useStore";
import styles from "../auth/AuthForm.module.css";

function ResetPasswordPage() {
  const navigate = useNavigate();
  const { authStore } = useStore();
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [tone, setTone] = useState<"success" | "error">("error");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!password.trim()) {
      setTone("error");
      setMessage("새 비밀번호를 입력하세요.");
      return;
    }

    if (password.length < 6) {
      setTone("error");
      setMessage("비밀번호는 최소 6자 이상이어야 합니다.");
      return;
    }

    setLoading(true);
    setMessage("");

    const result = await authStore.updatePassword(password);

    setLoading(false);

    if (!result.success) {
      setTone("error");
      setMessage(result.message ?? "비밀번호 변경 중 문제가 발생했습니다.");
      return;
    }

    setTone("success");
    setMessage(result.message ?? "비밀번호가 변경되었습니다.");

    window.setTimeout(() => {
      navigate("/login");
    }, 1600);
  };

  return (
    <AuthSplitTemplate
      eyebrow="Reset Password"
      title="보안을 유지하면서 빠르게 비밀번호를 재설정하세요"
      description="새 비밀번호 설정 화면도 동일한 입력 atom과 폼 molecule을 사용하도록 맞춰두었습니다."
    >
      <P className={styles.eyebrow}>Credential Update</P>
      <H2 className={styles.title}>새 비밀번호 설정</H2>
      <P className={styles.description}>새 비밀번호를 입력하면 로그인 화면으로 이동합니다.</P>

      {!authStore.isAuthConfigured ? (
        <Notice tone="error">{authStore.authUnavailableMessage}</Notice>
      ) : null}

      <Form className={styles.form} onSubmit={handleSubmit}>
        <FormField label="새 비밀번호">
          <FieldInput
            type="password"
            placeholder="새 비밀번호 입력"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </FormField>

        {message ? <Notice tone={tone}>{message}</Notice> : null}

        <Button type="submit" tone="dark" stretch disabled={loading}>
          {loading ? "변경 중..." : "비밀번호 변경"}
        </Button>
      </Form>
    </AuthSplitTemplate>
  );
}

export default ResetPasswordPage;
