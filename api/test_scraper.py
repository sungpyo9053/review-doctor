import pytest

from scraper import is_naver_place_url, parse_naver_place_reviews, ScrapeError


def test_is_naver_place_url_valid():
    assert is_naver_place_url("https://m.place.naver.com/place/12345678/review/visitor")


def test_is_naver_place_url_invalid():
    assert not is_naver_place_url("https://example.com")
    assert not is_naver_place_url("ftp://m.place.naver.com/place/123")


def test_parse_naver_place_reviews_simple_html():
    html = '''
    <html>
    <body>
      <ul>
        <li class="_3oG8X">
          <div class="review_text">이곳 정말 좋아요.</div>
          <span class="_3hl2F">홍길동</span>
          <span class="_3fM31">2026년 3월 17일 수요일</span>
          <span class="score">4.5</span>
        </li>
        <li class="_3oG8X">
          <div class="review_text">서비스가 훌륭합니다.</div>
          <span class="_3hl2F">김철수</span>
          <span class="_3fM31">2026년 3월 16일 화요일</span>
          <span class="score">5.0</span>
        </li>
      </ul>
    </body>
    </html>
    '''

    result = parse_naver_place_reviews(html)
    assert result["count"] == 2
    assert result["reviews"][0]["text"] == "이곳 정말 좋아요."
    assert result["reviews"][0]["author"] == "홍길동"
    assert result["reviews"][0]["date"] == "20260317 수요일"
    assert result["reviews"][0]["rating"] == 4.5


def test_parse_naver_place_reviews_no_review():
    html = '<html><body><div>리뷰가 없습니다.</div></body></html>'
    result = parse_naver_place_reviews(html)
    assert result["count"] == 0
    assert result["reviews"] == []
