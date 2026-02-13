#!/usr/bin/env bash

# 리뷰닥터 POC 프로젝트 폴더 구조 자동 생성 스크립트
# 실행 위치: 빈 폴더 안에서 실행하거나, review-doctor-poc 폴더를 만들고 들어가서 실행

set -euo pipefail

PROJECT_NAME="review-doctor-poc"
echo "프로젝트 폴더 구조 생성 시작: $PROJECT_NAME"

# 프로젝트 루트 생성 (이미 있으면 스킵)
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# 백엔드 폴더
mkdir -p api
cd api

# 기본 FastAPI 파일 생성
cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="리뷰닥터 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시 제한 추천
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "리뷰닥터 API에 오신 걸 환영합니다!"}

@app.post("/analyze")
async def analyze(data: dict):
    store_name = data.get("store_name")
    if not store_name:
        return {"error": "store_name이 필요합니다"}
    # 여기에 실제 분석 로직 구현
    return {
        "store": store_name,
        "review_count": 5,
        "sentiment": "긍정 60%, 부정 40%",
        "strong_points": ["맛", "친절함", "청결"],
        "weak_points": ["기다림", "가격"],
        "action_items": ["서비스 속도 개선", "가격 재검토", "청결 관리 강화"]
    }
EOF

cat > requirements.txt << 'EOF'
fastapi
uvicorn[standard]
requests
beautifulsoup4
httpx
python-dotenv
EOF

cd ..

# 프론트엔드 폴더 (Vite + React)
mkdir -p web
cd web

# Vite 프로젝트 생성 (이미 있으면 스킵 안 하고 강제 생성)
echo "Vite + React 프로젝트 생성 중..."
npm create vite@latest . -- --template react --yes

# 기본 package.json에 proxy 추가 (개발용)
sed -i '' '/"scripts": {/a\
    "dev": "vite",\
    "build": "vite build",\
    "preview": "vite preview",\
' package.json

# vite.config.js에 proxy 설정 추가
cat > vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
EOF

cd ..

# 루트에 .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
venv/
.venv/

# Node
node_modules/
dist/
dist-ssr/
*.local

# macOS
.DS_Store
EOF

# README 기본 틀
cat > README.md << 'EOF'
# 리뷰닥터 POC

가게 리뷰 자동 분석 웹 앱 (FastAPI + Vite React)

## 구조
- api/     : FastAPI 백엔드
- web/     : Vite + React 프론트엔드

## 로컬 실행

### 백엔드
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000