# Review Doctor Frontend

Vite 기반 React + TypeScript 프론트엔드입니다. MobX로 전역 인증/관리자 상태를 관리하고, UI는 Atomic Design과 CSS Modules 기준으로 정리되어 있습니다.

## 스택

| 분류 | 사용 기술 |
| --- | --- |
| Runtime | React 19, React DOM |
| Language | TypeScript |
| Bundler | Vite |
| Routing | React Router, file-based route loader |
| State | MobX, mobx-react-lite |
| Styling | CSS Modules, CSS Custom Properties |
| Quality | ESLint, TypeScript build |

## 실행

```bash
npm install
npm run dev
```

개발 서버는 `0.0.0.0:5173`에서 실행되며, `/api` 요청은 `http://127.0.0.1:8000`으로 프록시됩니다. 저장 시 HMR이 동작하고, Vite watch polling도 켜져 있어 로컬 변경사항을 바로 확인할 수 있습니다.

## 환경 변수

`web/.env.local`에 Supabase 설정을 추가합니다.

```bash
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

값이 없으면 인증 요청은 막고 안내 메시지를 보여줍니다.

## 디렉터리 구조

```text
src
├── app
│   ├── AppRouter.tsx
│   └── fileRoutes.tsx
├── components
│   ├── atoms
│   ├── molecules
│   ├── organisms
│   └── templates
├── data
├── lib
├── pages
├── stores
├── styles
├── types
└── utils
```

## 컴포넌트 규칙

- `atoms`: HTML wrapper, Button, AppLink, Input, Checkbox처럼 더 쪼개기 어려운 기본 단위입니다.
- `molecules`: FormField, BrandLockup, DataTable, StatCard처럼 atom을 조합한 재사용 단위입니다.
- `organisms`: 랜딩 섹션, 대시보드 섹션, 관리자 패널처럼 도메인 맥락이 있는 UI 블록입니다.
- `templates`: AuthSplitTemplate, DashboardTemplate, AdminConsoleTemplate처럼 페이지 레이아웃을 담당합니다.
- `pages`: 라우트 진입점만 담당하고, 복잡한 화면 조립은 template/organism으로 내려보냅니다.

## 라우팅 규칙

`src/pages/**/page.tsx` 파일은 자동으로 라우트가 됩니다.

```text
src/pages/index/page.tsx              -> /
src/pages/login/page.tsx              -> /login
src/pages/join/page.tsx               -> /join
src/pages/join/success/page.tsx       -> /join/success
src/pages/dashboard/page.tsx          -> /dashboard
src/pages/admin/page.tsx              -> /admin
src/pages/admin/users/page.tsx        -> /admin/users
```

접근 제어는 `src/app/AppRouter.tsx`에서 경로 기준으로 처리합니다.

| 경로 | 접근 정책 |
| --- | --- |
| `/admin/**` | 관리자 전용 |
| `/dashboard/**` | 로그인 사용자 전용 |
| `/login`, `/join/**` | 비로그인 사용자 전용 |
| 그 외 | 공개 페이지 |

## 스타일 규칙

전역 스타일은 최소화하고, 실제 UI 스타일은 컴포넌트 가까이에 둡니다.

```text
src/styles
├── tokens.css       # 색상, radius, shadow 등 디자인 토큰
├── reset.css        # 브라우저 기본값과 한글 줄바꿈 기본 정책
└── global.css       # tokens/reset import 진입점
```

- 재사용 컴포넌트 스타일은 `components/**/ComponentName.module.css`에 둡니다.
- 라우트 전용 배치 스타일은 `pages/**/page.module.css`에 둡니다.
- 한글 줄바꿈은 기본적으로 `word-break: keep-all`, `overflow-wrap: break-word`, `text-wrap` 계열을 사용합니다.
- 새 색상/간격이 여러 곳에서 반복되면 먼저 `src/styles/tokens.css`에 토큰으로 추가합니다.

## 상태 관리

- `src/stores/AuthStore.ts`: Supabase 인증 상태, 로그인, 회원가입, 비밀번호 변경, 콘솔 진입 경로를 관리합니다.
- `src/stores/AdminStore.ts`: 관리자 이메일 목록과 관리자 판별 로직을 관리합니다.
- `src/stores/StoreProvider.tsx`: MobX store를 React context로 제공합니다.
- 화면에서 store를 읽는 컴포넌트는 `observer`로 감싸 필요한 부분만 반응형으로 렌더링합니다.

## 스크립트

```bash
npm run dev              # Vite 개발 서버
npm run lint             # ESLint
npm run typecheck        # TypeScript 검사
npm run build            # typecheck + production build
npm run build:watch      # dist 자동 재빌드
npm run typecheck:watch  # TypeScript watch
npm run preview          # 빌드 결과 미리보기
```

## 검증 기준

PR 전에는 최소한 아래 두 명령을 통과시키는 것을 기준으로 합니다.

```bash
npm run lint
npm run build
```
