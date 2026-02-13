#!/usr/bin/env bash

set -euo pipefail

echo "리뷰닥터 서버 실행 스크립트"

# 터미널 여러 개 띄우기 귀찮아서 tmux 사용 추천 (없으면 그냥 두 개 터미널 열기)
if ! command -v tmux &> /dev/null; then
  echo "tmux가 없어서 일반 실행 모드로 갑니다."
  echo "백엔드와 프론트를 따로 터미널에서 실행해주세요."
  echo ""
  echo "백엔드:"
  echo "  cd api && source venv/bin/activate && uvicorn main:app --reload --port 8000"
  echo ""
  echo "프론트:"
  echo "  cd web && npm run dev"
  exit 0
fi

SESSION="review-doctor"

# 기존 세션 있으면 죽이기
tmux kill-session -t $SESSION 2>/dev/null || true

# 새 세션 생성
tmux new-session -d -s $SESSION

# 백엔드 창
tmux rename-window -t $SESSION:0 "Backend"
tmux send-keys -t $SESSION:0 "cd api && source venv/bin/activate && uvicorn main:app --reload --port 8000" C-m

# 프론트 창
tmux new-window -t $SESSION -n "Frontend"
tmux send-keys -t $SESSION:1 "cd web && npm run dev" C-m

# 첫 창으로 이동
tmux select-window -t $SESSION:0

echo "서버 실행 중..."
echo "tmux 세션 '$SESSION'에 연결하려면:"
echo "  tmux attach -t $SESSION"
echo ""
echo "종료하려면:"
echo "  tmux kill-session -t $SESSION"
echo ""
tmux attach -t $SESSION