import { useContext } from "react";
import { StoreContext } from "./StoreContext";

export function useStore() {
  const store = useContext(StoreContext);

  if (!store) {
    throw new Error("StoreProvider 내부에서만 useStore를 사용할 수 있습니다.");
  }

  return store;
}
