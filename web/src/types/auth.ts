export type GenderOption = "male" | "female" | "none";

export interface SignupFormValues {
  name: string;
  birth: string;
  gender: GenderOption;
  email: string;
  password: string;
  phone: string;
  isOwner: boolean;
  storeName: string;
}

export interface AuthActionResult {
  success: boolean;
  message?: string;
}
