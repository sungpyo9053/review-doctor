#!/usr/bin/env bash

echo "리뷰닥터 서버 시작 (백그라운드 모드)"

# 백엔드 백그라운드 실행
echo "백엔드 시작..."
(cd api && source venv/bin/activate && uvicorn main:app --reload --port 8000) > backend.log 2>&1 &

# 프론트 백그라운드 실행
echo "프론트 시작..."
(cd web && npm run dev) > frontend.log 2>&1 &

echo ""
echo "모든 서버 백그라운드 실행 완료!"
echo "프론트: http://localhost:5173"
echo "백엔드 Swagger: http://127.0.0.1:8000/docs"
echo ""
echo "로그 확인:"
echo "  tail -f backend.log"
echo "  tail -f frontend.log"
echo ""
echo "종료하려면:"
echo "  killall uvicorn"
echo "  pkill node"
echo "또는 터미널 닫기"