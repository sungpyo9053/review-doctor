export interface FeatureItem {
  icon: string;
  title: string;
  description: string;
}

export interface FooterColumn {
  title: string;
  links: Array<{ label: string; href: string }>;
}

export interface ProgressItem {
  label: string;
  value: number;
}

export interface AdminMenuItem {
  label: string;
  path: string;
}

export interface AdminUserRow {
  name: string;
  email: string;
  role: string;
  phone?: string;
  joined: string;
}

export interface AnalysisJobRow {
  store: string;
  reviews: number;
  status: "성공" | "실패";
  time: string;
}

export const marketingPlatforms = ["NAVER", "BAEMIN", "COUPANG", "GOOGLE MAPS"];

export const marketingFeatures: FeatureItem[] = [
  {
    icon: "01",
    title: "자동 리뷰 수집",
    description:
      "네이버, 배민, 쿠팡이츠, 구글 지도의 리뷰를 자동으로 모아 하나의 흐름으로 정리합니다.",
  },
  {
    icon: "02",
    title: "AI 감정 분석",
    description:
      "평점 숫자만 보는 것이 아니라 실제 문맥을 읽고 고객이 좋아한 지점과 불만 포인트를 나눕니다.",
  },
  {
    icon: "03",
    title: "키워드 트렌드",
    description:
      "주간 변화를 기준으로 강점, 약점, 급증 키워드를 추적해 운영 우선순위를 빠르게 정할 수 있습니다.",
  },
];

export const reportProgressItems: ProgressItem[] = [
  { label: "맛", value: 85 },
  { label: "서비스", value: 72 },
  { label: "청결", value: 64 },
];

export const footerColumns: FooterColumn[] = [
  {
    title: "서비스",
    links: [
      { label: "기능 소개", href: "#features" },
      { label: "리포트 예시", href: "#report" },
      { label: "API 연동", href: "/" },
    ],
  },
  {
    title: "고객 지원",
    links: [
      { label: "자주 묻는 질문", href: "/" },
      { label: "문의하기", href: "/" },
      { label: "공지사항", href: "/" },
    ],
  },
  {
    title: "법적 고지",
    links: [
      { label: "이용약관", href: "/" },
      { label: "개인정보처리방침", href: "/" },
    ],
  },
];

export const adminMenuItems: AdminMenuItem[] = [
  { label: "대시보드", path: "/admin" },
  { label: "회원 관리", path: "/admin/users" },
  { label: "가게 관리", path: "/admin/stores" },
  { label: "분석 이력", path: "/admin/analysis" },
  { label: "리포트", path: "/admin/reports" },
  { label: "설정", path: "/admin/settings" },
];

export const adminStats = [
  { label: "총 회원 수", value: "128", note: "+12% 지난주 대비" },
  { label: "사업주 계정", value: "37", note: "+5% 활성 증가" },
  { label: "등록된 가게", value: "24", note: "+3개 신규 등록" },
  { label: "이번 주 분석 요청", value: "412", note: "+18% 요청 증가" },
];

export const recentAdminUsers: AdminUserRow[] = [
  {
    name: "홍성표",
    email: "sungpyo@example.com",
    role: "사업주",
    joined: "2026-03-14",
  },
  {
    name: "김민수",
    email: "minsuk@example.com",
    role: "일반",
    joined: "2026-03-13",
  },
  {
    name: "이하늘",
    email: "haneul@example.com",
    role: "사업주",
    joined: "2026-03-13",
  },
  {
    name: "박서연",
    email: "seoyeon@example.com",
    role: "일반",
    joined: "2026-03-12",
  },
];

export const allAdminUsers: AdminUserRow[] = [
  {
    name: "홍성표",
    email: "sungpyo@example.com",
    role: "admin",
    phone: "01012345678",
    joined: "2026-03-14",
  },
  {
    name: "김민수",
    email: "minsuk@example.com",
    role: "user",
    phone: "01023456789",
    joined: "2026-03-13",
  },
  {
    name: "이하늘",
    email: "haneul@example.com",
    role: "owner",
    phone: "01034567890",
    joined: "2026-03-13",
  },
  {
    name: "박서연",
    email: "seoyeon@example.com",
    role: "owner",
    phone: "01098765432",
    joined: "2026-03-12",
  },
];

export const recentAnalysisJobs: AnalysisJobRow[] = [
  {
    store: "홍대 김밥천국",
    reviews: 132,
    status: "성공",
    time: "2026-03-14 18:20",
  },
  {
    store: "합정 카페블루",
    reviews: 89,
    status: "성공",
    time: "2026-03-14 17:10",
  },
  {
    store: "마포 떡볶이집",
    reviews: 44,
    status: "실패",
    time: "2026-03-14 16:35",
  },
  {
    store: "연남 우동집",
    reviews: 73,
    status: "성공",
    time: "2026-03-14 15:42",
  },
];

export const dashboardMetrics = [
  { label: "이번 주 수집 리뷰", value: "128", note: "지난주 대비 16% 증가" },
  { label: "긍정 비율", value: "72%", note: "배달 속도 언급이 개선됨" },
  { label: "주의 키워드", value: "3개", note: "가격, 대기시간, 주차" },
];

export const dashboardActionCards = [
  {
    title: "리뷰 분석 준비",
    description:
      "플랫폼 연동 상태를 확인하고 다음 자동 수집 스케줄을 설정해두면 운영 루틴이 훨씬 안정적입니다.",
  },
  {
    title: "운영 개선 리포트",
    description:
      "AI가 지난 7일 리뷰를 기반으로 강점과 약점을 요약하고, 바로 실행할 개선 제안을 추천합니다.",
  },
];

export const dashboardWeeklyTimeline = [
  "월요일: 서비스 키워드 언급량 상승",
  "수요일: 대기시간 관련 부정 리뷰 감소",
  "금요일: 배달 속도 만족도 최고치 기록",
];

export const authFeatureBullets = [
  "리뷰 수집부터 분석 리포트까지 하나의 흐름으로 연결",
  "사업주와 운영팀이 함께 보는 대시보드 구조",
  "주간 인사이트와 개선 포인트를 빠르게 정리",
];
