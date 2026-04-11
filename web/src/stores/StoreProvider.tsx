import { useEffect, useState, type PropsWithChildren } from "react";
import { RootStore } from "./RootStore";
import { StoreContext } from "./StoreContext";

export function StoreProvider({ children }: PropsWithChildren) {
  const [store] = useState(() => new RootStore());

  useEffect(() => {
    store.initialize();

    return () => {
      store.dispose();
    };
  }, [store]);

  return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>;
}
