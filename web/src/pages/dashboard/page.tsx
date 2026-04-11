import { observer } from "mobx-react-lite";
import { DashboardOverview } from "@/components/organisms/DashboardSections";
import { DashboardTemplate } from "@/components/templates/DashboardTemplate";
import { useStore } from "@/stores/useStore";

const DashboardPage = observer(() => {
  const { authStore } = useStore();

  if (!authStore.user) {
    return null;
  }

  return (
    <DashboardTemplate>
      <DashboardOverview
        email={authStore.user.email ?? ""}
        roleLabel={authStore.roleLabel}
        storeName={authStore.storeName}
        isOwner={authStore.user.user_metadata?.role === "owner"}
        onLogout={() => {
          void authStore.signOut();
        }}
      />
    </DashboardTemplate>
  );
});

export default DashboardPage;
