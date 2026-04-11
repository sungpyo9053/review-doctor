# 리뷰닥터

음식점/매장 리뷰를 한곳에 모아 운영 인사이트를 빠르게 확인하는 풀스택 POC입니다. 프론트엔드는 React + TypeScript 기반으로 재구성했고, MobX 상태 관리, Atomic Design 컴포넌트 계층, 파일 기반 라우팅, CSS Modules 스타일 구조를 적용했습니다.

## 기술 스택

| 영역 | 사용 기술 |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, React Router, MobX, CSS Modules |
| UI Architecture | Atomic Design, HTML atom wrapper, component-scoped styles |
| Backend | FastAPI, Python, Pydantic |
| Auth | Supabase Auth |

## 빠른 실행

### 백엔드

```bash
cd api
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 프론트엔드

```bash
cd web
npm install
npm run dev
```

Vite 개발 서버는 `http://localhost:5173`에서 실행됩니다. `/api` 요청은 `http://127.0.0.1:8000`으로 프록시되며, 파일 저장 시 HMR과 polling watch로 변경사항이 즉시 반영됩니다.

## 환경 변수

프론트 인증 기능을 사용하려면 `web/.env.local`에 아래 값을 설정합니다.

```bash
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

환경 변수가 없어도 앱은 빈 화면으로 죽지 않고 인증 설정 안내를 보여주도록 처리되어 있습니다.

## 프론트엔드 구조

```text
web/src
├── app                  # AppRouter, fileRoutes 등 앱 진입/라우팅
├── components
│   ├── atoms            # HTML atom wrapper, Button, Input 등 최소 UI 단위
│   ├── molecules        # FormField, DataTable, StatCard 등 조합 컴포넌트
│   ├── organisms        # 랜딩/대시보드/관리자 섹션
│   └── templates        # 페이지 레이아웃 템플릿
├── data                 # 임시 목데이터
├── lib                  # 외부 SDK 초기화
├── pages                # 파일 기반 라우트 진입점
├── stores               # MobX 전역 상태
├── styles               # tokens, reset, global
├── types                # 공유 타입
└── utils                # 공통 유틸
```

## 핵심 설계

- Atomic Design 계층은 `atoms -> molecules -> organisms -> templates -> pages` 흐름으로 구성합니다.
- HTML 태그는 `web/src/components/atoms/html.tsx`의 atom wrapper를 통해 사용합니다.
- 전역 인증 상태와 관리자 상태는 MobX store에서 관리합니다.
- `web/src/pages/**/page.tsx` 파일은 자동으로 라우트가 됩니다.
- `/admin/**`, `/dashboard/**`, `/login`, `/join/**` 접근 제어는 `AppRouter`에서 경로 기준으로 처리합니다.
- 컴포넌트 스타일은 파일 옆 `*.module.css`로 관리하고, 전역 CSS는 `styles/global.css`에서 `tokens.css`와 `reset.css`만 불러옵니다.

## 라우트 예시

```text
web/src/pages/index/page.tsx              -> /
web/src/pages/login/page.tsx              -> /login
web/src/pages/join/page.tsx               -> /join
web/src/pages/join/success/page.tsx       -> /join/success
web/src/pages/dashboard/page.tsx          -> /dashboard
web/src/pages/admin/page.tsx              -> /admin
web/src/pages/admin/users/page.tsx        -> /admin/users
```

## 개발 커맨드

```bash
cd web
npm run dev              # 개발 서버
npm run lint             # ESLint
npm run typecheck        # TypeScript 검사
npm run build            # 프로덕션 빌드
npm run build:watch      # dist 자동 재빌드
npm run preview          # 빌드 결과 미리보기
```

## 포함된 화면

- 랜딩 페이지
- 로그인
- 회원가입
- 가입 완료
- 비밀번호 재설정
- 사용자 대시보드
- 관리자 대시보드
- 관리자 회원 관리
- 관리자 설정
- 관리자 가게 관리, 분석 이력, 리포트 placeholder

## 현재 참고사항

- 백엔드 `/analyze`는 POC 더미 리포트를 반환합니다.
- 관리자 이메일 목록은 현재 브라우저 `localStorage` 기반으로 관리됩니다.
- 실제 매장/리뷰 API 연결 시에도 기존 Atomic Design 계층과 MobX store 위에 기능을 확장하는 방향을 권장합니다.
