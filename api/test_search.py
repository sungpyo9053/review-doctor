"""
네이버 지도 검색 기능 테스트
- 검색 함수 테스트
- API 엔드포인트 테스트
- 에러 처리 테스트
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from scraper import search_naver_places, ScrapeError
from main import app

client = TestClient(app)
API_KEY = "secret-demo-key"


# ============================================================================
# PART 1: 검색 함수 단위 테스트 (scraper.py)
# ============================================================================

class TestSearchNaverPlaces:
    """search_naver_places 함수 테스트"""
    
    def test_invalid_empty_query(self):
        """빈 검색어는 에러를 발생시켜야 함"""
        with pytest.raises(ScrapeError, match="Search query cannot be empty"):
            search_naver_places("")
        
        with pytest.raises(ScrapeError, match="Search query cannot be empty"):
            search_naver_places("   ")
    
    def test_none_query(self):
        """None 검색어는 에러를 발생시켜야 함"""
        with pytest.raises(ScrapeError, match="Search query cannot be empty"):
            search_naver_places(None)
    
    @patch('scraper.requests.get')
    def test_network_error(self, mock_get):
        """네트워크 오류 처리"""
        mock_get.side_effect = Exception("Connection error")
        
        with pytest.raises(ScrapeError, match="search_naver_places failed"):
            search_naver_places("아카시아")
    
    @patch('scraper.requests.get')
    def test_http_error(self, mock_get):
        """HTTP 상태 코드 에러 처리 (404, 500 등)"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        with pytest.raises(ScrapeError, match="Failed to fetch search results"):
            search_naver_places("아카시아")
    
    @patch('scraper.requests.get')
    def test_successful_search_single_result(self, mock_get):
        """검색 결과 1개인 경우"""
        # 목(Mock) HTML 응답
        html_response = """
        <html>
            <div class="place_list_item">
                <a class="place_link" href="/place/12345678">
                    아카시아 카페
                </a>
                <span class="place_address">서울 노원구 공릉로</span>
                <span class="place_category">카페</span>
            </div>
        </html>
        """
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_response
        mock_get.return_value = mock_response
        
        results = search_naver_places("아카시아")
        
        assert len(results) == 1
        assert results[0]['place_id'] == "12345678"
        assert results[0]['name'] == "아카시아 카페"
        assert results[0]['address'] == "서울 노원구 공릉로"
        assert results[0]['category'] == "카페"
        assert results[0]['url'] == "https://m.place.naver.com/place/12345678"
    
    @patch('scraper.requests.get')
    def test_successful_search_multiple_results(self, mock_get):
        """검색 결과 여러 개인 경우"""
        html_response = """
        <html>
            <div class="place_list_item">
                <a class="place_link" href="/place/11111111">
                    아카시아 카페
                </a>
                <span class="place_address">서울 노원구</span>
                <span class="place_category">카페</span>
            </div>
            <div class="place_list_item">
                <a class="place_link" href="/place/22222222">
                    아카시아 한식당
                </a>
                <span class="place_address">인천 부평구</span>
                <span class="place_category">한식</span>
            </div>
            <div class="place_list_item">
                <a class="place_link" href="/place/33333333">
                    아카시아 펜션
                </a>
                <span class="place_address">강원도 강릉시</span>
                <span class="place_category">펜션</span>
            </div>
        </html>
        """
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_response
        mock_get.return_value = mock_response
        
        results = search_naver_places("아카시아")
        
        assert len(results) == 3
        assert results[0]['place_id'] == "11111111"
        assert results[1]['place_id'] == "22222222"
        assert results[2]['place_id'] == "33333333"
    
    @patch('scraper.requests.get')
    def test_no_results(self, mock_get):
        """검색 결과가 없는 경우"""
        html_response = """
        <html>
            <div>검색 결과가 없습니다</div>
        </html>
        """
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_response
        mock_get.return_value = mock_response
        
        results = search_naver_places("xyz123abc존재하지않는가게")
        
        assert len(results) == 0
        assert isinstance(results, list)
    
    @patch('scraper.requests.get')
    def test_url_encoding(self, mock_get):
        """검색어 URL 인코딩 확인"""
        html_response = """<html><div class="place_list_item">
            <a class="place_link" href="/place/123">가게</a>
            <span class="place_address">주소</span>
            <span class="place_category">카테고리</span>
        </div></html>"""
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_response
        mock_get.return_value = mock_response
        
        # 특수 문자가 포함된 검색어 테스트
        search_naver_places("스시 & 복어")
        
        # 호출 확인
        called_url = mock_get.call_args[0][0]
        assert "query=" in called_url
        # URL이 올바르게 인코딩되었는지 확인
        assert " " not in called_url.split("query=")[1]


# ============================================================================
# PART 2: API 엔드포인트 테스트 (main.py)
# ============================================================================

class TestSearchNaverPlaceEndpoint:
    """POST /search/naver-place 엔드포인트 테스트"""
    
    def test_missing_query(self):
        """query 필드 누락"""
        response = client.post("/search/naver-place", json={
            "api_key": API_KEY
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_missing_api_key(self):
        """api_key 필드 누락"""
        response = client.post("/search/naver-place", json={
            "query": "아카시아"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_empty_query(self):
        """빈 검색어"""
        response = client.post("/search/naver-place", json={
            "query": "   ",
            "api_key": API_KEY
        })
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_invalid_api_key(self):
        """잘못된 API 키"""
        response = client.post("/search/naver-place", json={
            "query": "아카시아",
            "api_key": "wrong-key"
        })
        
        assert response.status_code == 401
        assert "Invalid API key" in response.json()["detail"]
    
    @patch('main.search_naver_places')
    def test_successful_search_one_result(self, mock_search):
        """검색 성공 - 결과 1개"""
        mock_search.return_value = [
            {
                'place_id': '12345678',
                'name': '아카시아 카페',
                'address': '서울 노원구',
                'category': '카페',
                'url': 'https://m.place.naver.com/place/12345678'
            }
        ]
        
        response = client.post("/search/naver-place", json={
            "query": "아카시아",
            "api_key": API_KEY
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert data['query'] == '아카시아'
        assert data['count'] == 1
        assert len(data['results']) == 1
        assert data['results'][0]['place_id'] == '12345678'
        assert data['results'][0]['name'] == '아카시아 카페'
    
    @patch('main.search_naver_places')
    def test_successful_search_multiple_results(self, mock_search):
        """검색 성공 - 결과 여러 개"""
        mock_search.return_value = [
            {
                'place_id': '11111111',
                'name': '아카시아 카페',
                'address': '서울 노원구',
                'category': '카페',
                'url': 'https://m.place.naver.com/place/11111111'
            },
            {
                'place_id': '22222222',
                'name': '아카시아 한식',
                'address': '인천 부평구',
                'category': '한식',
                'url': 'https://m.place.naver.com/place/22222222'
            }
        ]
        
        response = client.post("/search/naver-place", json={
            "query": "아카시아",
            "api_key": API_KEY
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 2
        assert len(data['results']) == 2
    
    @patch('main.search_naver_places')
    def test_no_results(self, mock_search):
        """검색 성공 - 결과 없음"""
        mock_search.return_value = []
        
        response = client.post("/search/naver-place", json={
            "query": "xyz존재하지않는가게",
            "api_key": API_KEY
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert data['count'] == 0
        assert data['results'] == []
    
    @patch('main.search_naver_places')
    def test_scrape_error_handling(self, mock_search):
        """ScrapeError 예외 처리"""
        mock_search.side_effect = ScrapeError("Network error")
        
        response = client.post("/search/naver-place", json={
            "query": "아카시아",
            "api_key": API_KEY
        })
        
        assert response.status_code == 502
        assert "Network error" in response.json()["detail"]
    
    @patch('main.search_naver_places')
    def test_unexpected_error_handling(self, mock_search):
        """예상치 못한 에러 처리"""
        mock_search.side_effect = Exception("Unexpected error")
        
        response = client.post("/search/naver-place", json={
            "query": "아카시아",
            "api_key": API_KEY
        })
        
        assert response.status_code == 500
        assert "Unexpected error" in response.json()["detail"]
    
    @patch('main.search_naver_places')
    def test_response_model_validation(self, mock_search):
        """응답 모델 검증"""
        mock_search.return_value = [
            {
                'place_id': '123',
                'name': '가게명',
                'address': '주소',
                'category': '카테고리',
                'url': 'https://m.place.naver.com/place/123'
            }
        ]
        
        response = client.post("/search/naver-place", json={
            "query": "테스트",
            "api_key": API_KEY
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # 필수 필드 확인
        assert 'status' in data
        assert 'query' in data
        assert 'count' in data
        assert 'results' in data
        
        # 결과 항목 필드 확인
        result = data['results'][0]
        assert 'place_id' in result
        assert 'name' in result
        assert 'address' in result
        assert 'category' in result
        assert 'url' in result


# ============================================================================
# PART 3: 시나리오 테스트 (E2E 유사)
# ============================================================================

class TestSearchScenarios:
    """실제 사용 시나리오 시뮬레이션"""
    
    @patch('main.search_naver_places')
    def test_scenario_single_result_selection(self, mock_search):
        """시나리오: 검색 결과 1개 - 사용자가 자동 선택"""
        mock_search.return_value = [
            {
                'place_id': '99999999',
                'name': '유일한 아카시아',
                'address': '서울 강남구 역삼로',
                'category': '카페',
                'url': 'https://m.place.naver.com/place/99999999'
            }
        ]
        
        response = client.post("/search/naver-place", json={
            "query": "유일한 아카시아",
            "api_key": API_KEY
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # 1개 결과 → 자동 선택 가능
        if data['count'] == 1:
            place_id = data['results'][0]['place_id']
            assert place_id == '99999999'
    
    @patch('main.search_naver_places')
    def test_scenario_multiple_results_user_selection(self, mock_search):
        """시나리오: 검색 결과 여러 개 - 사용자가 선택할 목록 표시"""
        mock_search.return_value = [
            {
                'place_id': '111',
                'name': '아카시아 강남점',
                'address': '서울 강남구',
                'category': '카페',
                'url': 'https://m.place.naver.com/place/111'
            },
            {
                'place_id': '222',
                'name': '아카시아 노원점',
                'address': '서울 노원구',
                'category': '카페',
                'url': 'https://m.place.naver.com/place/222'
            }
        ]
        
        response = client.post("/search/naver-place", json={
            "query": "아카시아",
            "api_key": API_KEY
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # 여러 개 결과 → 목록 표시하고 사용자 선택 대기
        if data['count'] > 1:
            names = [r['name'] for r in data['results']]
            assert '아카시아 강남점' in names
            assert '아카시아 노원점' in names
