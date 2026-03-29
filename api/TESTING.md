# 🧪 네이버 지도 검색 기능 - 테스트 가이드

> 언제든지 이 문서를 참고하여 테스트를 실행하고 검증할 수 있습니다.

---

## 📑 목차

1. [개요](#개요)
2. [빠른 시작](#빠른-시작)
3. [설치 및 준비](#설치-및-준비)
4. [테스트 실행](#테스트-실행)
5. [테스트 상세 내용](#테스트-상세-내용)
6. [실제 사용 시나리오](#실제-사용-시나리오)
7. [API 명세](#api-명세)
8. [트러블슈팅](#트러블슈팅)

---

## 개요

네이버 지도에서 가게를 검색하고 업체 정보를 자동으로 가져오는 기능입니다.

### 기능 설명
- 📱 **검색**: 가게 이름으로 네이버 지도 검색 (`search_naver_places()`)
- 🔍 **파싱**: HTML에서 place_id, 주소, 카테고리 등 추출
- 📡 **API**: POST `/search/naver-place` 엔드포인트 제공
- ✅ **검증**: 결과 1개면 자동 선택, 다중이면 목록 표시

### 테스트 구성
| 부분 | 파일 | 테스트 수 | 상태 |
|------|------|----------|------|
| PART 1 | 검색 함수 (`scraper.py`) | 8개 | ✅ PASSED |
| PART 2 | API 엔드포인트 (`main.py`) | 10개 | ✅ PASSED |
| PART 3 | 실제 시나리오 | 2개 | ✅ PASSED |
| **총합** | `test_search.py` | **20개** | **✅ 20/20** |

---

## 빠른 시작

### 🚀 가장 간단한 방법 (3줄)

```bash
cd c:\workspace\review-doctor\api
pip install -r requirements.txt  # 첫 번째만 필요
python -m pytest test_search.py -v
```

### ⏱️ 소요 시간
- 첫 설치: ~2분 (의존성 다운로드)
- 이후 테스트: ~1초

### 📊 예상 결과
```
======================= 20 passed in 1.05s ========================
```

---

## 설치 및 준비

### 📌 사전 요구사항
- Python 3.9 이상
- pip (Python 패키지 관리자)

### 💾 의존성 설치

**방법 1: requirements.txt 사용 (권장)**
```bash
cd c:\workspace\review-doctor\api
pip install -r requirements.txt
```

**방법 2: 개별 패키지 설치**
```bash
pip install fastapi uvicorn requests beautifulsoup4 lxml selenium webdriver-manager pytest pytest-cov
```

### ✅ 설치 확인
```bash
python -c "import pytest; print(f'pytest {pytest.__version__}')"
```
출력: `pytest 9.0.2` (또는 다른 버전)

---

## 테스트 실행

### 1️⃣ 모든 테스트 실행하기

```bash
python -m pytest test_search.py -v
```

**출력 예시:**
```
test_search.py::TestSearchNaverPlaces::test_invalid_empty_query PASSED   [  5%]
test_search.py::TestSearchNaverPlaces::test_none_query PASSED            [ 10%]
test_search.py::TestSearchNaverPlaces::test_network_error PASSED         [ 15%]
...
test_search.py::TestSearchScenarios::test_scenario_multiple_results_user_selection PASSED [100%]

======================= 20 passed in 1.05s ========================
```

### 2️⃣ 특정 부분만 테스트하기

#### PART 1: 검색 함수 테스트 (8개)
검색 함수의 기본 동작 검증 (입력 검증, 에러 처리, 파싱)

```bash
python -m pytest test_search.py::TestSearchNaverPlaces -v
```

**테스트 항목:**
```
✅ test_invalid_empty_query        - 빈 검색어 처리
✅ test_none_query                 - None 값 처리
✅ test_network_error              - 네트워크 오류 처리
✅ test_http_error                 - HTTP 500 에러 처리
✅ test_successful_search_single_result    - 결과 1개 파싱
✅ test_successful_search_multiple_results - 결과 여러 개 파싱
✅ test_no_results                 - 빈 결과 처리
✅ test_url_encoding               - 검색어 URL 인코딩
```

**예상 결과:**
```
======================= 8 passed in 0.52s ========================
```

#### PART 2: API 엔드포인트 테스트 (10개)
API 레이어의 HTTP 요청/응답 검증

```bash
python -m pytest test_search.py::TestSearchNaverPlaceEndpoint -v
```

**테스트 항목:**
```
✅ test_missing_query              - query 필드 누락 검증
✅ test_missing_api_key            - api_key 필드 누락 검증
✅ test_empty_query                - 빈 검색어 검증
✅ test_invalid_api_key            - API 키 인증
✅ test_successful_search_one_result      - 성공 (1개 결과)
✅ test_successful_search_multiple_results - 성공 (다중 결과)
✅ test_no_results                 - 빈 결과 처리
✅ test_scrape_error_handling      - 502 에러 처리
✅ test_unexpected_error_handling  - 500 에러 처리
✅ test_response_model_validation  - 응답 모델 검증
```

**예상 결과:**
```
======================= 10 passed in 0.64s ========================
```

#### PART 3: 시나리오 테스트 (2개)
실제 사용 케이스 시뮬레이션

```bash
python -m pytest test_search.py::TestSearchScenarios -v
```

**테스트 항목:**
```
✅ test_scenario_single_result_selection      - 결과 1개 → 자동 선택
✅ test_scenario_multiple_results_user_selection - 결과 다중 → 목록 표시
```

### 3️⃣ 특정 테스트만 실행하기

**빈 검색어 처리 테스트만:**
```bash
python -m pytest test_search.py::TestSearchNaverPlaces::test_invalid_empty_query -v
```

**API 키 인증 테스트만:**
```bash
python -m pytest test_search.py::TestSearchNaverPlaceEndpoint::test_invalid_api_key -v
```

### 4️⃣ 상세 정보와 함께 실행하기

**더 자세한 출력:**
```bash
python -m pytest test_search.py -vv
```

**print() 확인 포함:**
```bash
python -m pytest test_search.py -v -s
```

**실패한 테스트만 보기:**
```bash
python -m pytest test_search.py -v --tb=short
```

### 5️⃣ 커버리지 확인하기

코드의 몇 %가 테스트되었는지 확인

```bash
python -m pytest test_search.py --cov=scraper --cov=main --cov-report=term-missing
```

**출력 예시:**
```
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
main.py             120     15    87%    
scraper.py          250     40    84%
TOTAL               370     55    85%
```

**HTML 리포트 생성 (브라우저로 보기):**
```bash
python -m pytest test_search.py --cov=scraper --cov=main --cov-report=html
# 브라우저에서 htmlcov/index.html 열기
```

---

## 테스트 상세 내용

### 📋 PART 1: 검색 함수 단위 테스트

`scraper.py`의 `search_naver_places()` 함수 테스트

#### 테스트별 상세 설명

| 테스트 | 테스트하는 것 | 예시 |
|--------|--------------|------|
| `test_invalid_empty_query` | 빈 검색어 거부 | `search_naver_places("")` → ScrapeError |
| `test_none_query` | None 값 거부 | `search_naver_places(None)` → ScrapeError |
| `test_network_error` | 네트워크 오류 처리 | 인터넷 끊김 → ScrapeError |
| `test_http_error` | HTTP 500 에러 처리 | 네이버 서버 오류 → ScrapeError |
| `test_successful_search_single_result` | 결과 1개 파싱 | "특정 가게" → place_id 추출 성공 |
| `test_successful_search_multiple_results` | 결과 여러 개 파싱 | "아카시아" → 3개 가게 리스트 |
| `test_no_results` | 빈 결과 처리 | "xyz존재하지않는가게" → [] |
| `test_url_encoding` | 특수문자 인코딩 | "스시 & 복어" → URL 인코딩 확인 |

#### 검증하는 항목
- ✅ 입력값 유효성 검사
- ✅ 네트워크/HTTP 오류 처리
- ✅ HTML 파싱 정확성
- ✅ place_id 추출
- ✅ 주소/카테고리 추출
- ✅ 특수 문자 처리

### 📋 PART 2: API 엔드포인트 테스트

`main.py`의 `/search/naver-place` 엔드포인트 테스트

#### 테스트별 상세 설명

| 테스트 | 테스트하는 것 | 상태 코드 |
|--------|--------------|---------|
| `test_missing_query` | query 필드 누락 | 422 |
| `test_missing_api_key` | api_key 필드 누락 | 422 |
| `test_empty_query` | 빈 검색어 | 400 |
| `test_invalid_api_key` | 잘못된 API 키 | 401 |
| `test_successful_search_one_result` | 성공 - 결과 1개 | 200 |
| `test_successful_search_multiple_results` | 성공 - 결과 여러 개 | 200 |
| `test_no_results` | 성공 - 결과 없음 | 200 |
| `test_scrape_error_handling` | ScrapeError 예외 | 502 |
| `test_unexpected_error_handling` | 예상치 못한 에러 | 500 |
| `test_response_model_validation` | 응답 데이터 구조 | 200 + 데이터 검증 |

#### 검증하는 항목
- ✅ HTTP 요청 검증 (필수 필드)
- ✅ API 키 인증
- ✅ HTTP 상태 코드
- ✅ 응답 JSON 구조
- ✅ 에러 메시지

### 📋 PART 3: 시나리오 테스트

실제 사용 케이스 시뮬레이션

#### 시나리오 1: 검색 결과 1개
```
[상황] 사용자가 "유일한 아카시아" 검색
      (검색 결과가 정확히 1개)

[기대 동작]
- API가 1개 결과 반환
- place_id 추출 성공
- count = 1
- 프론트에서 자동으로 이 가게 선택
```

#### 시나리오 2: 검색 결과 여러 개
```
[상황] 사용자가 "아카시아" 검색
      (검색 결과가 3개 이상)

[기대 동작]
- API가 여러 개 결과 반환
- count > 1
- results 배열에 모든 결과 포함
- 프론트에서 사용자가 선택할 목록 표시
```

---

## 실제 사용 시나리오

### 🎯 시나리오 1: 결과 1개인 경우

```
┌─────────────────────────┐
│ 사업자 페이지           │
│ [검색창] "아카시아카페" │
└────────────┬────────────┘
             │ (검색)
             ↓
┌─────────────────────────┐
│ 백엔드 API              │
│ GET /search/naver-place │
└────────────┬────────────┘
             │ (1개 결과)
             ↓
┌─────────────────────────────────────────┐
│ 응답:                                    │
│ {                                        │
│   "status": "ok",                        │
│   "query": "아카시아카페",               │
│   "count": 1,                            │
│   "results": [{                          │
│     "place_id": "12345678",              │
│     "name": "아카시아카페",              │
│     "address": "서울 노원구 공릉로",     │
│     "category": "카페",                  │
│     "url": "https://m.place.naver..."   │
│   }]                                     │
│ }                                        │
└────────────┬─────────────────────────────┘
             │ (자동 처리)
             ↓
┌─────────────────────────┐
│ 프론트엔드              │
│ 해당 가게 정보 자동 표시 │
│ (다음 단계로 진행)      │
└─────────────────────────┘
```

### 🎯 시나리오 2: 결과 여러 개인 경우

```
┌─────────────────────────┐
│ 사업자 페이지           │
│ [검색창] "아카시아"     │
└────────────┬────────────┘
             │ (검색)
             ↓
┌─────────────────────────┐
│ 백엔드 API              │
│ GET /search/naver-place │
└────────────┬────────────┘
             │ (3개 결과)
             ↓
┌────────────────────────────────────────┐
│ 응답:                                   │
│ {                                       │
│   "count": 3,                           │
│   "results": [                          │
│     {"place_id": "111", "name": "..."},│
│     {"place_id": "222", "name": "..."},│
│     {"place_id": "333", "name": "..."}│
│   ]                                     │
│ }                                       │
└────────────┬────────────────────────────┘
             │ (사용자 선택 필요)
             ↓
┌──────────────────────────────────────┐
│ 프론트엔드                           │
│ □ 아카시아 강남점                    │
│ □ 아카시아 노원점 (선택됨) ✓         │
│ □ 아카시아 펜션                      │
│                                       │
│ [확인] 버튼                           │
└──────────────────────────────────────┘
             │ (사용자가 노원점 선택)
             ↓
┌──────────────────────────────┐
│ 다음 단계로 진행             │
│ (리뷰 크롤링 등)             │
└──────────────────────────────┘
```

---

## API 명세

### 엔드포인트
```
POST /search/naver-place
```

### 요청 형식

```http
POST /search/naver-place HTTP/1.1
Content-Type: application/json

{
  "query": "아카시아",
  "api_key": "secret-demo-key"
}
```

### 요청 필드

| 필드 | 타입 | 필수 | 설명 | 예시 |
|------|------|------|------|------|
| `query` | string | ✅ | 검색할 가게/업체 이름 | "아카시아" |
| `api_key` | string | ✅ | API 인증 키 | "secret-demo-key" |

### 응답 형식

#### 성공 (200)
```json
{
  "status": "ok",
  "query": "아카시아",
  "count": 2,
  "results": [
    {
      "place_id": "11111111",
      "name": "아카시아 카페",
      "address": "서울 노원구 공릉로",
      "category": "카페",
      "url": "https://m.place.naver.com/place/11111111"
    },
    {
      "place_id": "22222222",
      "name": "아카시아 한식",
      "address": "인천 부평구 경원대로",
      "category": "한식",
      "url": "https://m.place.naver.com/place/22222222"
    }
  ]
}
```

#### 에러 응답

**빈 검색어 (400)**
```json
{
  "detail": "Search query cannot be empty"
}
```

**잘못된 API 키 (401)**
```json
{
  "detail": "Invalid API key"
}
```

**필드 누락 (422)**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "query"],
      "msg": "Field required"
    }
  ]
}
```

**네트워크 오류 (502)**
```json
{
  "detail": "Failed to fetch search results, status=500"
}
```

**서버 오류 (500)**
```json
{
  "detail": "Unexpected error: ..."
}
```

### 응답 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | string | 상태 ("ok" 또는 에러) |
| `query` | string | 원본 검색어 |
| `count` | integer | 검색 결과 개수 |
| `results` | array | 검색 결과 배열 |
| `results[].place_id` | string | 네이버 장소 고유 ID |
| `results[].name` | string | 가게/업체명 |
| `results[].address` | string | 주소 |
| `results[].category` | string | 카테고리 (카페, 한식 등) |
| `results[].url` | string | 네이버 지도 URL |

---

## curl 예제

### 기본 검색 요청
```bash
curl -X POST http://localhost:8000/search/naver-place \
  -H "Content-Type: application/json" \
  -d '{"query":"아카시아","api_key":"secret-demo-key"}'
```

### 특수문자가 있는 검색
```bash
curl -X POST http://localhost:8000/search/naver-place \
  -H "Content-Type: application/json" \
  -d '{"query":"스시 & 복어","api_key":"secret-demo-key"}'
```

### jq로 출력 정렬
```bash
curl -X POST http://localhost:8000/search/naver-place \
  -H "Content-Type: application/json" \
  -d '{"query":"아카시아","api_key":"secret-demo-key"}' | jq .
```

---

## 트러블슈팅

### ❌ pytest: command not found

**원인:** pytest가 설치되지 않음

**해결:**
```bash
pip install pytest pytest-cov
# 또는
pip install -r requirements.txt
```

### ❌ ModuleNotFoundError: No module named 'fastapi'

**원인:** 필수 패키지가 설치되지 않음

**해결:**
```bash
# api 폴더에 있는지 확인
cd c:\workspace\review-doctor\api

# 의존성 설치
pip install -r requirements.txt
```

### ❌ No module named 'scraper' 또는 'main'

**원인:** 워킹 디렉토리가 잘못됨

**해결:**
```bash
# 반드시 api 폴더에서 실행
cd c:\workspace\review-doctor\api
python -m pytest test_search.py -v
```

### ❌ 특정 테스트만 실패

**상세 정보 보기:**
```bash
python -m pytest test_search.py::ClassName::test_name -vv
```

**에러 스택 보기:**
```bash
python -m pytest test_search.py::ClassName::test_name -vv --tb=long
```

### ❌ 모든 테스트가 느림

**원인:** 네트워크 오류 또는 기다리는 중

**해결:**
```bash
# 특정 테스트만 빠르게 실행
python -m pytest test_search.py::TestSearchNaverPlaces::test_invalid_empty_query -v

# 또는 Mock이 제대로 작동하는지 확인
python -m pytest test_search.py::TestSearchNaverPlaces -v
```

### ❌ Python 버전 오류

**요구사항:** Python 3.9 이상

**확인:**
```bash
python --version
```

**업그레이드 필요 시:**
https://www.python.org/downloads/

---

## 📚 참고 자료

### 파일 구조
```
api/
├── test_search.py           # 테스트 코드 (20개 테스트)
├── scraper.py               # 검색 함수 구현
├── main.py                  # API 엔드포인트
├── requirements.txt         # 의존성 목록
├── TESTING.md               # 이 파일 (테스트 가이드)
└── testData/                # 테스트 데이터 디렉토리
```

### 주요 함수

**`search_naver_places(query: str) -> list`**
- 네이버 지도에서 가게 검색
- 입력: 검색어 (문자열)
- 반환: 검색 결과 리스트

**`POST /search/naver-place`**
- FastAPI 엔드포인트
- 입력: JSON 바디 (query, api_key)
- 반환: JSON 응답

### 외부 라이브러리

| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| fastapi | 최신 | REST API |
| uvicorn | 최신 | ASGI 서버 |
| requests | 최신 | HTTP 요청 |
| beautifulsoup4 | 최신 | HTML 파싱 |
| lxml | 최신 | XML 파서 |
| pytest | 최신 | 테스트 프레임워크 |
| pytest-cov | 최신 | 커버리지 리포트 |

---

## 🎓 학습 포인트

이 테스트를 통해 배우는 것:

1. **단위 테스트 작성**
   - Mock을 활용한 외부 의존성 제거
   - 입력 검증 테스트
   - 예외 처리 테스트

2. **API 테스트**
   - HTTP 상태 코드 검증
   - 요청/응답 데이터 구조 검증
   - FastAPI TestClient 사용

3. **웹 스크래핑**
   - HTML 파싱
   - CSS Selector 사용
   - 정규표현식으로 데이터 추출

4. **에러 처리**
   - 사용자 정의 예외
   - 예외 계층 구조
   - 에러 메시지

---

## 💡 다음 단계

### 1️⃣ 로컬 API 서버 실행
```bash
python -m uvicorn main:app --reload
```

API 서버가 실행되면:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2️⃣ API 테스트
```bash
# 터미널에서 직접 테스트
curl -X POST http://localhost:8000/search/naver-place \
  -H "Content-Type: application/json" \
  -d '{"query":"아카시아","api_key":"secret-demo-key"}'

# 또는 Postman/Thunder Client 사용
```

### 3️⃣ 프론트엔드 연동
React/Vue에서 이 API 호출:
```javascript
const response = await fetch('/search/naver-place', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: searchTerm,
    api_key: 'secret-demo-key'
  })
});
const data = await response.json();

// 결과 처리
if (data.count === 1) {
  // 결과 1개 → 자동 선택
  selectPlace(data.results[0].place_id);
} else if (data.count > 1) {
  // 결과 다중 → 목록 표시
  showPlaceList(data.results);
}
```

### 4️⃣ 리뷰 크롤링
선택한 place_id로 `/scrape/naver-place` 호출:
```bash
curl -X POST http://localhost:8000/scrape/naver-place \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://m.place.naver.com/place/12345678",
    "api_key": "secret-demo-key"
  }'
```

---

## 📞 문제 해결

테스트 실행 중 문제가 발생하면:

1. **에러 메시지 읽기** - 정확한 문제를 알 수 있음
2. **이 문서의 트러블슈팅 섹션 참고**
3. **상세 출력으로 실행** - `python -m pytest test_search.py -vv`
4. **특정 테스트만 실행** - 문제 격리

---

## 📝 마지막으로

> 🎯 **핵심: 이 테스트는 기능이 정상 작동함을 보증합니다.**

- ✅ 검색 함수 동작 보증
- ✅ API 동작 보증
- ✅ 에러 처리 보증
- ✅ 데이터 구조 보증

**테스트 모두 통과 = 기능 준비 완료 = 프론트엔드 연동 가능**

---

**마지막 업데이트:** 2026년 3월 28일
**테스트 상태:** ✅ 20/20 PASSED
**작성자:** GitHub Copilot
