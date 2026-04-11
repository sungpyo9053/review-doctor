import type { User } from "@supabase/supabase-js";
import { makeAutoObservable, runInAction } from "mobx";
import {
  isSupabaseConfigured,
  supabase,
  supabaseConfigMessage,
} from "../lib/supabase";
import type { SignupFormValues } from "../types/auth";
import type { RootStore } from "./RootStore";

export class AuthStore {
  user: User | null = null;
  authLoading = true;
  private authUnsubscribe?: () => void;

  constructor(private readonly rootStore: RootStore) {
    makeAutoObservable(this, {}, { autoBind: true });
  }

  get isAuthConfigured(): boolean {
    return isSupabaseConfigured;
  }

  get authUnavailableMessage(): string {
    return supabaseConfigMessage;
  }

  get isAuthenticated(): boolean {
    return Boolean(this.user);
  }

  get isAdmin(): boolean {
    return this.rootStore.adminStore.isAdminEmail(this.user?.email);
  }

  get userName(): string {
    return (this.user?.user_metadata?.name as string | undefined) || "회원";
  }

  get storeName(): string {
    return (this.user?.user_metadata?.store_name as string | undefined) || "가게";
  }

  get roleLabel(): string {
    if (this.isAdmin) {
      return "관리자";
    }

    const role = this.user?.user_metadata?.role;
    return role === "owner" ? "사업주" : "일반 사용자";
  }

  get welcomeText(): string {
    if (!this.user) {
      return "";
    }

    if (this.isAdmin) {
      return "관리자님 안녕하세요";
    }

    if (this.user?.user_metadata?.role === "owner") {
      return `${this.storeName} 사장님 안녕하세요`;
    }

    return `${this.userName}님 안녕하세요`;
  }

  get primaryConsolePath(): string {
    if (!this.user) {
      return "/login";
    }

    return this.isAdmin ? "/admin" : "/dashboard";
  }

  async initialize(): Promise<void> {
    if (!supabase) {
      runInAction(() => {
        this.user = null;
        this.authLoading = false;
      });
      return;
    }

    await this.loadCurrentUser();

    if (this.authUnsubscribe) {
      return;
    }

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      runInAction(() => {
        this.user = session?.user ?? null;
        this.authLoading = false;
      });
    });

    this.authUnsubscribe = () => {
      subscription.unsubscribe();
    };
  }

  dispose(): void {
    this.authUnsubscribe?.();
    this.authUnsubscribe = undefined;
  }

  async signIn(
    email: string,
    password: string,
  ): Promise<{ success: boolean; message?: string; user?: User | null }> {
    if (!supabase) {
      return { success: false, message: supabaseConfigMessage };
    }

    const { data, error } = await supabase.auth.signInWithPassword({
      email: email.trim().toLowerCase(),
      password,
    });

    if (error) {
      return { success: false, message: error.message };
    }

    runInAction(() => {
      this.user = data.user ?? null;
    });

    return { success: true, user: data.user };
  }

  async signUp(values: SignupFormValues): Promise<{ success: boolean; message?: string }> {
    if (!supabase) {
      return { success: false, message: supabaseConfigMessage };
    }

    const { error } = await supabase.auth.signUp({
      email: values.email.trim().toLowerCase(),
      password: values.password,
      options: {
        data: {
          name: values.name.trim(),
          birth: values.birth.trim(),
          gender: values.gender,
          phone: values.phone.trim(),
          role: values.isOwner ? "owner" : "user",
          store_name: values.storeName.trim(),
        },
      },
    });

    if (error) {
      return { success: false, message: error.message };
    }

    return { success: true };
  }

  async updatePassword(password: string): Promise<{ success: boolean; message?: string }> {
    if (!supabase) {
      return { success: false, message: supabaseConfigMessage };
    }

    const { error } = await supabase.auth.updateUser({ password });

    if (error) {
      return { success: false, message: error.message };
    }

    return { success: true, message: "비밀번호가 성공적으로 변경되었습니다." };
  }

  async signOut(): Promise<void> {
    if (supabase) {
      await supabase.auth.signOut();
    }

    runInAction(() => {
      this.user = null;
    });
  }

  private async loadCurrentUser(): Promise<void> {
    if (!supabase) {
      runInAction(() => {
        this.user = null;
        this.authLoading = false;
      });
      return;
    }

    try {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      runInAction(() => {
        this.user = user ?? null;
        this.authLoading = false;
      });
    } catch {
      runInAction(() => {
        this.user = null;
        this.authLoading = false;
      });
    }
  }
}
