import { AdminStore } from "./AdminStore";
import { AuthStore } from "./AuthStore";

export class RootStore {
  readonly adminStore = new AdminStore();
  readonly authStore = new AuthStore(this);

  initialize(): void {
    this.adminStore.hydrate();
    void this.authStore.initialize();
  }

  dispose(): void {
    this.authStore.dispose();
  }
}
