import re
import os
import csv
import time
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

ALLOWED_HOSTNAME = "m.place.naver.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class ScrapeError(Exception):
    pass


def is_naver_place_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in ["http", "https"]:
        return False

    host = parsed.netloc.lower()
    return host == ALLOWED_HOSTNAME


def fetch_html(url: str, timeout: int = 10, retries: int = 3) -> str:
    if not is_naver_place_url(url):
        raise ScrapeError("Not a m.place.naver.com URL")

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code != 200:
                raise ScrapeError(f"Failed to fetch page, status={resp.status_code}")
            return resp.text
        except Exception as e:
            last_exc = e
            if attempt == retries:
                raise ScrapeError(f"fetch_html failed after {retries} attempts: {e}")

    raise ScrapeError(f"fetch_html failed: {last_exc}")


def fetch_html_selenium(url: str, timeout: int = 20) -> str:
    if not is_naver_place_url(url):
        raise ScrapeError("Not a m.place.naver.com URL")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={USER_AGENT}")

    try:
        chrome_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.set_page_load_timeout(timeout)
        driver.get(url)

        # 전체 더보기 반복 클릭
        while True:
            try:
                more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.fvwqf'))
                )
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)
            except Exception:
                break

        # 리뷰 리스트 로드 대기
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "li.place_apply_pui.EjjAW, li.EjjAW, li._3oG8X, li.review_item, div._1km0z")
            )
        )

        time.sleep(1)
        return driver.page_source
    except Exception as e:
        raise ScrapeError(f"fetch_html_selenium failed: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass


def _extract_text(node):
    if node is None:
        return ""
    return node.get_text(separator=" ", strip=True)


def _extract_rating(item):
    # 대표적인 네이버 평점 구조 추출
    rating = None

    # CSS class 형식
    star = item.select_one("div.review_score div.star_score span")
    if star is not None:
        star_text = star.get("style", "")
        m = re.search(r"width:\s*(\d+)%", star_text)
        if m:
            rating = float(m.group(1)) / 20.0

    if rating is None:
        score_node = item.select_one("span.score, span._1D7MQ")
        if score_node:
            txt = score_node.get_text(strip=True)
            try:
                rating = float(txt)
            except Exception:
                pass

    return rating


def _normalize_review_text(text):
    if not text:
        return text
    text = text.strip()

    # 본문으로 보이는 곳까지 추출
    # common tail indicators: '반응 남기기', '방문일'
    m_tail = re.search(r"^(.*?)(?:\s*반응 남기기|\s*방문일).*", text)
    if m_tail:
        text = m_tail.group(1).strip()

    # sometimes starts with '닉네임 리뷰 ...' or '닉네임 리뷰 XX 사진 ...'
    m = re.search(r"^[^\n]+리뷰[^\n]*?\s+(.*)$", text)
    if m and len(m.group(1).strip()) > 5:
        candidate = m.group(1).strip()
        # 후반에 다시 중복 안내가 있으면 자른다.
        m_tail2 = re.search(r"^(.*?)(?:\s*반응 남기기|\s*방문일).*", candidate)
        if m_tail2:
            candidate = m_tail2.group(1).strip()
        if len(candidate) <= len(text):
            text = candidate

    return text


def _normalize_review_date(date_text):
    if not date_text:
        return date_text
    date_text = date_text.strip()

    # 2026년 1월 28일 수요일 등 형태 탐지
    m = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일\s*([월화수목금토일]+요일)", date_text)
    if m:
        yyyy = int(m.group(1)); mm = int(m.group(2)); dd = int(m.group(3)); dow = m.group(4)
        return f"{yyyy:04d}{mm:02d}{dd:02d} {dow}"

    # 간혹 23.1.28.수 형태
    m2 = re.search(r"(\d{2})\.(\d{1,2})\.(\d{1,2})\.([월화수목금토일])", date_text)
    if m2:
        prefix = int(m2.group(1))
        yyyy = 2000 + prefix if prefix < 70 else 1900 + prefix
        mm = int(m2.group(2)); dd = int(m2.group(3)); wik = m2.group(4)
        return f"{yyyy:04d}{mm:02d}{dd:02d} {wik}요일"

    return date_text


def _extract_tags(item):
    tags = []
    # 다수의 태그 셀렉터 대응
    tag_selectors = [
        "div.pui__HLNvmI",
        "span._2-GE-",
        "div.review_tag",
        "div._1I3nE span",
    ]
    for sel in tag_selectors:
        for node in item.select(sel):
            txt = _extract_text(node)
            if txt and txt not in tags:
                tags.append(txt)
    return tags


def parse_naver_place_reviews(html: str):
    soup = BeautifulSoup(html, "lxml")

    # 네이버 리뷰 아이템 후보
    candidates = []

    selectors = [
        "li.place_apply_pui.EjjAW",
        "li.EjjAW",
        "li._3oG8X",
        "li.review_item",
        "div.review_item",
        "div._1km0z",
        "div._3QPE6",
        "div._3Rixz",
        "div.section_review_list li",
    ]

    for sel in selectors:
        found = soup.select(sel)
        if found:
            candidates = found
            break

    if not candidates:
        # 리뷰 항목이 명확히 감지되지 않으면 리턴
        return {"count": 0, "reviews": []}

    reviews = []

    for item in candidates:
        text = ""
        author = ""
        date = ""
        rating = None
        tags = []

        # 리뷰 텍스트 추출 (가장 정확한 선택자 우선)
        for x in ["div.pui__vn15t2", "div.review_text", "span._1W6Y3", "span._3oJ5G", "p._1i3d0", "div._1U3gJ", "div._2tkPb"]:
            node = item.select_one(x)
            if node:
                text = _extract_text(node)
                if text:
                    break

        if not text:
            text = _extract_text(item.select_one("p") or item)

        text = _normalize_review_text(text)

        # 작성자
        author_node = item.select_one("span.pui__uslU0d, span._3hl2F, span._1Gy50, div._3-1M1, span._2s0fL")
        if author_node:
            author = _extract_text(author_node)

        # 날짜
        date_node = item.select_one("span.pui__gfuUIT, span._3fM31, span._1Q9DG, time, span._2Aa_p")
        if date_node:
            date = _normalize_review_date(_extract_text(date_node))

        # 평점
        rating = _extract_rating(item)

        # 태그
        tags = _extract_tags(item)

        # 필터: 유효한 리뷰 텍스트가 없는 경우 제외
        if not text:
            continue

        reviews.append({
            "author": author,
            "text": text,
            "tags": tags,
            "date": date,
            "rating": rating,
        })

    return {
        "count": len(reviews),
        "reviews": reviews,
    }


def save_reviews_to_csv(reviews, directory="testData"):
    os.makedirs(directory, exist_ok=True)
    filename = datetime.now().strftime("%y%m%d_%H%M%S") + ".csv"
    filepath = os.path.join(directory, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["author", "text", "tags", "date", "rating"])
        writer.writeheader()
        for review in reviews:
            writer.writerow({
                "author": review.get("author", ""),
                "text": review.get("text", ""),
                "tags": ", ".join(review.get("tags", [])),
                "date": review.get("date", ""),
                "rating": review.get("rating", ""),
            })

    return filepath


def scrape_naver_place_reviews(url: str, use_selenium: bool = False):
    if use_selenium:
        html = fetch_html_selenium(url)
    else:
        html = fetch_html(url)

    result = parse_naver_place_reviews(html)

    reviews = result.get("reviews", [])
    print(f"[INFO] Total reviews found: {len(reviews)}")

    for i, r in enumerate(reviews, start=1):
        print(f"[REVIEW {i}] author={r.get('author')!r}, date={r.get('date')!r}, rating={r.get('rating')!r}, tags={r.get('tags')!r}")
        print(f"          content={r.get('text')!r}")

    csv_path = save_reviews_to_csv(reviews, directory=os.path.join(os.getcwd(), "testData"))
    print(f"[INFO] Reviews saved to CSV: {csv_path}")

    return result

