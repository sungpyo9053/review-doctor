import { observer } from "mobx-react-lite";
import { MarketingTemplate } from "@/components/templates/MarketingTemplate";
import { useStore } from "@/stores/useStore";

const HomePage = observer(() => {
  const { authStore } = useStore();

  return (
    <MarketingTemplate
      user={authStore.user}
      isAdmin={authStore.isAdmin}
      welcomeText={authStore.welcomeText}
      onLogout={() => {
        void authStore.signOut();
      }}
    />
  );
});

export default HomePage;
