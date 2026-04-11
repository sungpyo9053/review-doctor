import { makeAutoObservable } from "mobx";

const STORAGE_KEY = "reviewdr_admin_emails";
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const DEFAULT_ADMIN_EMAILS = [
  "reviewdrtest01@gmail.com",
  "sungpyo9053@kookmin.ac.kr",
];

export class AdminStore {
  adminEmails = [...DEFAULT_ADMIN_EMAILS];

  constructor() {
    makeAutoObservable(this, {}, { autoBind: true });
  }

  hydrate(): void {
    if (typeof window === "undefined") {
      return;
    }

    const raw = window.localStorage.getItem(STORAGE_KEY);

    if (!raw) {
      this.adminEmails = [...DEFAULT_ADMIN_EMAILS];
      return;
    }

    try {
      const parsed = JSON.parse(raw) as unknown;

      if (Array.isArray(parsed) && parsed.length > 0) {
        this.adminEmails = parsed
          .filter((item): item is string => typeof item === "string")
          .map((item) => item.trim().toLowerCase());
        return;
      }
    } catch {
      // Ignore malformed localStorage values and fall back to defaults.
    }

    this.adminEmails = [...DEFAULT_ADMIN_EMAILS];
  }

  isAdminEmail(email?: string | null): boolean {
    if (!email) {
      return false;
    }

    return this.adminEmails.includes(email.trim().toLowerCase());
  }

  addAdminEmail(input: string): { success: boolean; message: string } {
    const email = input.trim().toLowerCase();

    if (!email) {
      return { success: false, message: "추가할 관리자 이메일을 입력하세요." };
    }

    if (!EMAIL_PATTERN.test(email)) {
      return { success: false, message: "올바른 이메일 형식을 입력하세요." };
    }

    if (this.adminEmails.includes(email)) {
      return { success: false, message: "이미 등록된 관리자 이메일입니다." };
    }

    this.adminEmails = [...this.adminEmails, email];
    this.persist();

    return { success: true, message: "관리자 이메일이 추가되었습니다." };
  }

  removeAdminEmail(
    email: string,
    currentUserEmail?: string | null,
  ): { success: boolean; message: string } {
    const normalizedEmail = email.trim().toLowerCase();

    if (normalizedEmail === currentUserEmail?.trim().toLowerCase()) {
      return {
        success: false,
        message: "현재 로그인한 관리자 계정은 여기서 삭제할 수 없습니다.",
      };
    }

    this.adminEmails = this.adminEmails.filter((item) => item !== normalizedEmail);
    this.persist();

    return { success: true, message: "관리자 이메일이 삭제되었습니다." };
  }

  private persist(): void {
    if (typeof window === "undefined") {
      return;
    }

    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(this.adminEmails));
  }
}
