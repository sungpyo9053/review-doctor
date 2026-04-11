
from scraper import is_naver_place_url, parse_naver_place_reviews, ScrapeError


def test_is_naver_place_url_valid():
    assert is_naver_place_url("https://m.place.naver.com/restaurant/1212622367")


def test_is_naver_place_url_invalid():
    assert not is_naver_place_url("https://m.place.naver.com/restaurant/1212622367")
    #assert not is_naver_place_url("https://m.place.naver.com/restaurant/1212622367")


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
if __name__ == "__main__":
    print("테스트 시작")

    test_is_naver_place_url_valid()
    print("1번 통과")

    test_is_naver_place_url_invalid()
    print("2번 통과")

    test_parse_naver_place_reviews_simple_html()
    print("3번 통과")

    test_parse_naver_place_reviews_no_review()
    print("4번 통과")

    print("모든 테스트 통과")