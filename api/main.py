import os
from urllib.parse import urlparse

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from scraper import ScrapeError, is_naver_place_url, scrape_naver_place_reviews

app = FastAPI(title="리뷰닥터 API - POC")

NAVER_PLACE_API_KEY = os.environ.get("NAVER_PLACE_API_KEY", "secret-demo-key")


def _check_api_key(key: str):
    if not NAVER_PLACE_API_KEY:
        raise HTTPException(status_code=500, detail="Server API key not configured")
    if key != NAVER_PLACE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


class ReviewRequest(BaseModel):
    store_name: str


class NaverPlaceScrapeRequest(BaseModel):
    url: str = Field(..., example="https://m.place.naver.com/place/12345678/review/visitor")
    api_key: str = Field(..., example="YOUR_API_KEY")
    max_reviews: int = Field(30, ge=1, le=100)
    use_selenium: bool = Field(False, example=False)


@app.get("/")
def root():
    return {"message": "리뷰닥터 POC API 동작 중"}


@app.post("/analyze")
def analyze(request: ReviewRequest):
    dummy = [
        "음식 맛있고 양 많아요!",
        "서비스 친절해요 재방문 의사 있어요",
        "기다리는 시간이 좀 길었어요",
        "가격이 좀 비싸요",
        "청결 상태 좋음",
    ]

    report = {
        "store": request.store_name,
        "review_count": len(dummy),
        "sentiment": "긍정 60%, 부정 40%",
        "strong_points": ["맛", "친절함", "청결"],
        "weak_points": ["기다림", "가격"],
        "action_items": ["서비스 속도 개선", "가격 재검토", "청결 관리 강화"],
    }

    return report


@app.post("/scrape/naver-place")
def scrape_naver_place(req: NaverPlaceScrapeRequest):
    _check_api_key(req.api_key)

    if not is_naver_place_url(req.url):
        raise HTTPException(status_code=400, detail="URL must point to m.place.naver.com")

    try:
        data = scrape_naver_place_reviews(req.url, max_reviews=req.max_reviews, use_selenium=req.use_selenium)
        return {
            "status": "ok",
            "url": req.url,
            "count": data.get("count", 0),
            "reviews": data.get("reviews", []),
            "via_selenium": req.use_selenium,
        }
    except ScrapeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

