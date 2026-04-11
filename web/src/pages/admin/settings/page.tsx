import { observer } from "mobx-react-lite";
import { useState } from "react";
import { AdminEmailManager } from "@/components/organisms/AdminSections";
import { AdminConsoleTemplate } from "@/components/templates/AdminConsoleTemplate";
import { useStore } from "@/stores/useStore";

const AdminSettingsPage = observer(() => {
  const { adminStore, authStore } = useStore();
  const [newEmail, setNewEmail] = useState("");
  const [message, setMessage] = useState("");
  const [messageTone, setMessageTone] = useState<"success" | "error">("success");

  const handleAdd = () => {
    const result = adminStore.addAdminEmail(newEmail);
    setMessage(result.message);
    setMessageTone(result.success ? "success" : "error");

    if (result.success) {
      setNewEmail("");
    }
  };

  const handleRemove = (email: string) => {
    const result = adminStore.removeAdminEmail(email, authStore.user?.email);
    setMessage(result.message);
    setMessageTone(result.success ? "success" : "error");
  };

  return (
    <AdminConsoleTemplate
      title="설정"
      description="관리자 이메일 목록을 MobX store를 통해 전역적으로 관리합니다."
    >
      <AdminEmailManager
        emails={adminStore.adminEmails}
        currentUserEmail={authStore.user?.email}
        newEmail={newEmail}
        message={message}
        messageTone={messageTone}
        onEmailChange={setNewEmail}
        onAdd={handleAdd}
        onRemove={handleRemove}
      />
    </AdminConsoleTemplate>
  );
});

export default AdminSettingsPage;
