#!/bin/bash

echo "리뷰닥터 POC 초기 설정 시작... 🚀"

# 1. 백엔드 (api) 설정
echo "백엔드 설정 중..."
cd api || { echo "api 폴더 없음!"; exit 1; }

# venv 재생성 (이미 있으면 스킵 가능하지만 안전하게)
if [ -d "venv" ]; then
  echo "기존 venv 삭제 후 재생성..."
  rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install --upgrade pip setuptools wheel
pip install fastapi "uvicorn[standard]" urllib3==1.26.20
# 추가 필요 패키지 (리뷰 크롤링용 예시)
pip install requests beautifulsoup4 httpx python-dotenv

# requirements.txt 생성 (나중에 배포용)
pip freeze > requirements.txt

echo "백엔드 venv & 패키지 설치 완료!"

# 2. 프론트엔드 (web) 설정 - Vite + React 추천
cd ../web || { echo "web 폴더 없음! 생성함..."; mkdir -p ../web; cd ../web; }

if [ ! -f "package.json" ]; then
  echo "Vite React 프로젝트 생성 중..."
  npm create vite@latest . -- --template react
  # 또는 이미 있으면 스킵
fi

npm install

# CORS용 proxy 설정 (vite.config.js에 추가 - 개발 시 편함)
if [ -f "vite.config.js" ]; then
  echo "vite.config.js에 proxy 설정 추가..."
  cat <<EOT >> vite.config.js

// Proxy 설정 (개발 중 백엔드 호출 편하게)
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
EOT
fi

echo "프론트엔드 설정 완료! npm run dev로 실행하세요."

# 3. 전체 안내
cd ..
echo ""
echo "완료! 실행 방법:"
echo "1. 백엔드: cd api && source venv/bin/activate && python -m uvicorn main:app --reload --port 8000"
echo "2. 프론트: cd web && npm run dev  (http://localhost:5173)"
echo "프론트에서 API 호출 시 /api/analyze 로 하면 자동 proxy됨 (CORS 걱정 ㄴㄴ)"
echo "화이팅 성표! 이제 진짜 웹에서 테스트 가능 ㅋㅋ"
