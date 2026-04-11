import { Suspense, type ReactElement } from "react";
import { observer } from "mobx-react-lite";
import { Navigate, Route, Routes } from "react-router-dom";
import { Div, P } from "@/components/atoms/html";
import { useStore } from "@/stores/useStore";
import styles from "./AppRouter.module.css";
import { fileRoutes, type RouteAccess } from "./fileRoutes";

interface RouteGateProps {
  access: RouteAccess;
  children: ReactElement;
}

const RouteGate = observer(({ access, children }: RouteGateProps) => {
  const { authStore } = useStore();

  if (access === "guest" && authStore.isAuthenticated) {
    return <Navigate to={authStore.primaryConsolePath} replace />;
  }

  if (access === "private" && !authStore.isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (access === "admin") {
    if (!authStore.isAuthenticated) {
      return <Navigate to="/login" replace />;
    }

    if (!authStore.isAdmin) {
      return <Navigate to="/dashboard" replace />;
    }
  }

  return children;
});

export const AppRouter = observer(() => {
  const { authStore } = useStore();

  if (authStore.authLoading) {
    return (
      <Div className={styles.loading}>
        <P className={styles.loadingLabel}>Review Doctor를 불러오는 중입니다.</P>
      </Div>
    );
  }

  return (
    <Routes>
      {fileRoutes.map(({ path, Component, access }) => (
        <Route
          key={path}
          path={path}
          element={
            <RouteGate access={access}>
              <Suspense fallback={<RouteLoading />}>
                <Component />
              </Suspense>
            </RouteGate>
          }
        />
      ))}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
});

function RouteLoading() {
  return (
    <Div className={styles.loading}>
      <P className={styles.loadingLabel}>페이지를 불러오는 중입니다.</P>
    </Div>
  );
}
