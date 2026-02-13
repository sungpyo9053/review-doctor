from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="리뷰닥터 API - POC")

class ReviewRequest(BaseModel):
    store_name: str

@app.get("/")
def root():
    return {"message": "리뷰닥터 POC API 동작 중"}

@app.post("/analyze")
def analyze(request: ReviewRequest):
    # POC 더미 데이터
    dummy = [
        "음식 맛있고 양 많아요!",
        "서비스 친절해요 재방문 의사 있어요",
        "기다리는 시간이 좀 길었어요",
        "가격이 좀 비싸요",
        "청결 상태 좋음"
    ]

    report = {
        "store": request.store_name,
        "review_count": len(dummy),
        "sentiment": "긍정 60%, 부정 40%",
        "strong_points": ["맛", "친절함", "청결"],
        "weak_points": ["기다림", "가격"],
        "action_items": ["서비스 속도 개선", "가격 재검토", "청결 관리 강화"]
    }

    return report
