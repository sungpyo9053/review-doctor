# 리뷰닥터 POC

가게 이름을 입력하면 네이버·구글·블로그 리뷰를 크롤링해  
긍정/부정 비율, 강점·약점, 개선 제안을 자동 분석해주는 풀스택 웹 앱 POC입니다.

## 데모 (배포)
🔗 https://review-doctor-poc.vercel.app  
(배포 후 실제 URL로 교체)

![메인 화면 예시]


## 주요 기능
- 실시간 리뷰 크롤링 & 감성 분석
- 강점/약점 키워드 추출
- 실질적인 개선 제안 생성
- 로딩/에러 처리 UI

## 기술 스택
**Frontend**  
- React + Vite  
- 상태 관리: useState  

**Backend**  
- FastAPI (Python)  
- 크롤링: requests + BeautifulSoup4  

**배포**  
- Vercel (Frontend + Serverless Python)

## 로컬 실행 방법 (가장 중요!)

### 1. 프로젝트 구조 생성 (최초 1회만)
프로젝트 폴더를 처음 만들거나 구조를 새로 잡을 때 아래 스크립트를 실행하세요.
review-doctor-poc/
├── api/                        # FastAPI 백엔드
│   ├── main.py                 # FastAPI 앱 메인 파일
│   ├── requirements.txt        # 필요한 pip 패키지 목록
│   └── venv/                   # Python 가상환경 (자동 생성)
│
├── web/                        # Vite + React 프론트엔드
│   ├── node_modules/           # npm 패키지 (git ignore)
│   ├── public/                 # 정적 파일 (favicon 등)
│   ├── src/                    # React 소스 코드
│   │   ├── App.jsx             # 메인 컴포넌트 (입력창·버튼·결과 UI)
│   │   ├── main.jsx            # 앱 진입점
│   │   ├── index.css           # 전역 스타일
│   │   └── assets/             # 이미지 등
│   ├── vite.config.js          # Vite 설정 (proxy 포함)
│   ├── package.json            # npm 의존성 & 스크립트
│   ├── package-lock.json
│   └── .gitignore
│
├── init-project.sh             # 구조 생성 스크립트
├── run.sh                      # 서버 실행 스크립트
├── .gitignore                  # git 무시 파일
└── README.md                   # 이 파일

```bash
chmod +x init-project.sh
./init-project.sh

### 백엔드
```bash
cd api
source venv/bin/activate  # Windows면 venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000