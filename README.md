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

## 로컬 실행 방법

### 백엔드
```bash
cd api
source venv/bin/activate  # Windows면 venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000