import re
import time
from urllib.parse import urlparse
from collections import Counter, defaultdict

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


ALLOWED_HOSTNAME = "m.place.naver.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

CHROMEDRIVER_PATH = None
N_CLUSTERS = 4
TOP_N_CLUSTER_KEYWORDS = 5
TOP_N_REPRESENTATIVE_REVIEWS = 3

TOPIC_RULES = {
    "맛": ["맛", "커피", "라떼", "아메리카노", "디저트", "빵", "케이크", "고소", "담백", "신선"],
    "친절/서비스": ["친절", "응대", "사장님", "직원", "서비스", "상냥"],
    "분위기/공간": ["분위기", "조용", "아늑", "인테리어", "힐링", "감성", "편안", "쾌적"],
    "가격/가성비": ["비싸", "가격", "가성비", "부담", "저렴"],
    "청결": ["깨끗", "청결", "위생", "더럽", "깔끔", "비위생"],
    "좌석/공간": ["자리", "좌석", "테이블", "의자", "넓", "좁"],
    "대기/속도": ["기다", "느리", "오래", "빨리", "속도", "주문"],
    "재방문": ["다시", "재방문", "또 오", "추천", "단골"],
}

STOPWORDS = {
    "정말", "너무", "조금", "그냥", "진짜", "그리고", "근데", "약간",
    "여기", "저기", "이", "그", "저", "수", "것", "곳", "좀", "되다",
    "하다", "있다", "없다", "이다", "같다", "느낌", "생각"
}


class ScrapeError(Exception):
    pass


class ReviewAnalysisPipeline:
    def __init__(self):
        self.sentiment_model = None
        self.embedding_model = None

    # --------------------------------------------------
    # 공통 진행 알림
    # --------------------------------------------------
    def _notify(self, callback, step, message, percent):
        if callback:
            callback(step=step, message=message, percent=percent)

    # --------------------------------------------------
    # 모델 로딩
    # --------------------------------------------------
    def load_models(self, callback=None):
        if self.sentiment_model is not None and self.embedding_model is not None:
            return

        self._notify(callback, "load_models", "감성분석 모델 로딩 중", 5)
        self.sentiment_model = pipeline(
            "text-classification",
            model="daekeun-ml/koelectra-small-v3-nsmc"
        )

        self._notify(callback, "load_models", "임베딩 모델 로딩 중", 10)
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        self._notify(callback, "load_models", "기본 분석기 초기화 중", 15)

    # --------------------------------------------------
    # URL 검증
    # --------------------------------------------------
    def is_naver_place_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
        except Exception:
            return False

        if parsed.scheme not in ["http", "https"]:
            return False

        return parsed.netloc.lower() == ALLOWED_HOSTNAME

    # --------------------------------------------------
    # webdriver service
    # --------------------------------------------------
    def _build_driver_service(self):
        if CHROMEDRIVER_PATH:
            return Service(CHROMEDRIVER_PATH)
        return Service(ChromeDriverManager().install())

    # --------------------------------------------------
    # 유틸
    # --------------------------------------------------
    def _clean_text(self, text: str) -> str:
        if text is None:
            return ""
        text = str(text).strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def _extract_text(self, node):
        if node is None:
            return ""
        return node.get_text(separator=" ", strip=True)

    def _extract_rating(self, item):
        rating = None

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

    def _normalize_review_text(self, text):
        if not text:
            return text

        text = text.strip()

        m_tail = re.search(r"^(.*?)(?:\s*반응 남기기|\s*방문일).*", text)
        if m_tail:
            text = m_tail.group(1).strip()

        m = re.search(r"^[^\n]+리뷰[^\n]*?\s+(.*)$", text)
        if m and len(m.group(1).strip()) > 5:
            candidate = m.group(1).strip()
            m_tail2 = re.search(r"^(.*?)(?:\s*반응 남기기|\s*방문일).*", candidate)
            if m_tail2:
                candidate = m_tail2.group(1).strip()
            if len(candidate) <= len(text):
                text = candidate

        return text

    def _normalize_review_date(self, date_text):
        if not date_text:
            return date_text

        date_text = date_text.strip()

        m = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일\s*([월화수목금토일]+요일)", date_text)
        if m:
            yyyy = int(m.group(1))
            mm = int(m.group(2))
            dd = int(m.group(3))
            dow = m.group(4)
            return f"{yyyy:04d}-{mm:02d}-{dd:02d} {dow}"

        m2 = re.search(r"(\d{2})\.(\d{1,2})\.(\d{1,2})\.([월화수목금토일])", date_text)
        if m2:
            prefix = int(m2.group(1))
            yyyy = 2000 + prefix if prefix < 70 else 1900 + prefix
            mm = int(m2.group(2))
            dd = int(m2.group(3))
            wik = m2.group(4)
            return f"{yyyy:04d}-{mm:02d}-{dd:02d} {wik}요일"

        return date_text

    def _extract_tags(self, item):
        tags = []
        tag_selectors = [
            "div.pui__HLNvmI",
            "span._2-GE-",
            "div.review_tag",
            "div._1I3nE span",
        ]
        for sel in tag_selectors:
            for node in item.select(sel):
                txt = self._extract_text(node)
                if txt and txt not in tags:
                    tags.append(txt)
        return tags

    def _get_store_name_from_page(self, driver):
        selectors = [
            "span.GHAhO",
            "h2.place_name",
            "div.zD5Nm span",
            "div._3XamX",
        ]

        for sel in selectors:
            try:
                node = driver.find_element(By.CSS_SELECTOR, sel)
                text = self._clean_text(node.text)
                if text:
                    return text
            except Exception:
                pass

        return "unknown_store"

    # --------------------------------------------------
    # 감성분석
    # --------------------------------------------------
    def predict_sentiment(self, text: str):
        result = self.sentiment_model(text[:512])[0]
        label = result["label"]
        score = float(result["score"])

        if label == "1":
            mapped = "positive"
        elif label == "0":
            mapped = "negative"
        else:
            mapped = "neutral"

        return mapped, score

    # --------------------------------------------------
    # 단순 키워드
    # --------------------------------------------------
    def extract_keywords_morph(self, text: str):
        text = re.sub(r"[^가-힣a-zA-Z0-9\s]", " ", text)
        words = text.split()

        keywords = []
        for word in words:
            word = word.strip()
            if len(word) >= 2 and word not in STOPWORDS:
                keywords.append(word)

        return keywords

    # --------------------------------------------------
    # 주제 분류
    # --------------------------------------------------
    def detect_topics(self, text: str):
        found_topics = []

        for topic, words in TOPIC_RULES.items():
            if any(w in text for w in words):
                found_topics.append(topic)

        return found_topics

    def infer_topic_from_keywords(self, keywords):
        scores = defaultdict(int)

        for keyword, count in keywords:
            for topic, rules in TOPIC_RULES.items():
                for rule in rules:
                    if rule in keyword:
                        scores[topic] += count

        if not scores:
            return "기타"

        return sorted(scores.items(), key=lambda x: -x[1])[0][0]

    # --------------------------------------------------
    # 크롤링
    # --------------------------------------------------
    def fetch_html_selenium(self, url: str, callback=None, timeout: int = 20):
        if not self.is_naver_place_url(url):
            raise ScrapeError("Not a m.place.naver.com URL")

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={USER_AGENT}")
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

        driver = None

        try:
            self._notify(callback, "crawl", "브라우저 실행 중", 20)
            chrome_service = self._build_driver_service()
            driver = webdriver.Chrome(service=chrome_service, options=options)

            driver.set_page_load_timeout(timeout)
            driver.get(url)

            self._notify(callback, "crawl", "리뷰 페이지 로딩 완료", 30)
            time.sleep(3)

            store_name = self._get_store_name_from_page(driver)

            for _ in range(10):
                try:
                    more_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fvwqf"))
                    )
                    driver.execute_script("arguments[0].click();", more_button)
                    time.sleep(1)
                except Exception:
                    break

            self._notify(callback, "crawl", "리뷰 더보기 로딩 완료", 40)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "li.place_apply_pui.EjjAW, li.EjjAW, li._3oG8X, "
                        "li.review_item, div._1km0z, div._3QPE6, div._3Rixz"
                    )
                )
            )

            html = driver.page_source
            return store_name, html

        except Exception as e:
            raise ScrapeError(f"fetch_html_selenium failed: {e}")

        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

    # --------------------------------------------------
    # 리뷰 파싱
    # --------------------------------------------------
    def parse_reviews(self, html: str, callback=None):
        self._notify(callback, "parse", "리뷰 파싱 중", 50)

        try:
            soup = BeautifulSoup(html, "lxml")
        except Exception:
            soup = BeautifulSoup(html, "html.parser")

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
            return []

        reviews = []

        for idx, item in enumerate(candidates, start=1):
            text = ""
            author = ""
            date = ""
            rating = None
            tags = []

            for x in [
                "div.pui__vn15t2",
                "div.review_text",
                "span._1W6Y3",
                "span._3oJ5G",
                "p._1i3d0",
                "div._1U3gJ",
                "div._2tkPb",
            ]:
                node = item.select_one(x)
                if node:
                    text = self._extract_text(node)
                    if text:
                        break

            if not text:
                text = self._extract_text(item.select_one("p") or item)

            text = self._normalize_review_text(text)
            if not text:
                continue

            author_node = item.select_one(
                "span.pui__uslU0d, span._3hl2F, span._1Gy50, div._3-1M1, span._2s0fL"
            )
            if author_node:
                author = self._extract_text(author_node)

            date_node = item.select_one(
                "span.pui__gfuUIT, span._3fM31, span._1Q9DG, time, span._2Aa_p"
            )
            if date_node:
                date = self._normalize_review_date(self._extract_text(date_node))

            rating = self._extract_rating(item)
            tags = self._extract_tags(item)

            reviews.append({
                "author": author,
                "text": text,
                "tags": tags,
                "date": date,
                "rating": rating,
            })

            if idx % 10 == 0:
                self._notify(callback, "parse", f"리뷰 파싱 중... {idx}건", 50)

        return reviews

    # --------------------------------------------------
    # 감성 / 키워드 / 주제 enrich
    # --------------------------------------------------
    def enrich_reviews(self, reviews, callback=None):
        self._notify(callback, "analyze", "감성분석 및 주제 분석 중", 60)

        enriched = []
        for idx, review in enumerate(reviews, start=1):
            text = review["text"]

            sentiment_label, sentiment_score = self.predict_sentiment(text)
            topics = self.detect_topics(text)
            keywords = self.extract_keywords_morph(text)

            item = review.copy()
            item["sentiment"] = sentiment_label
            item["sentiment_score"] = sentiment_score
            item["topics"] = topics
            item["keywords"] = keywords
            enriched.append(item)

            if idx % 10 == 0:
                self._notify(callback, "analyze", f"감성분석 진행 중... {idx}건", 60)

        return enriched

    # --------------------------------------------------
    # 임베딩 + 군집화
    # --------------------------------------------------
    def cluster_reviews(self, reviews, callback=None, n_clusters=4):
        self._notify(callback, "embedding", "임베딩 생성 중", 70)

        texts = [r["text"] for r in reviews]
        embeddings = self.embedding_model.encode(texts)

        self._notify(callback, "cluster", "유사 리뷰 군집화 중", 80)

        n_clusters = min(n_clusters, len(texts))
        if n_clusters < 2:
            for r in reviews:
                r["cluster"] = 0
            return reviews, embeddings, None

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)

        for r, label in zip(reviews, labels):
            r["cluster"] = int(label)

        return reviews, embeddings, kmeans

    # --------------------------------------------------
    # 군집 리포트
    # --------------------------------------------------
    def build_cluster_reports(self, reviews, embeddings, kmeans, callback=None):
        self._notify(callback, "summarize", "군집 요약 생성 중", 90)

        cluster_reports = []
        cluster_to_reviews = defaultdict(list)
        cluster_to_indices = defaultdict(list)

        for idx, r in enumerate(reviews):
            cluster_to_reviews[r["cluster"]].append(r)
            cluster_to_indices[r["cluster"]].append(idx)

        for cluster_id, cluster_reviews in cluster_to_reviews.items():
            indices = cluster_to_indices[cluster_id]
            cluster_embeddings = embeddings[indices]

            if kmeans is not None:
                centroid = kmeans.cluster_centers_[cluster_id].reshape(1, -1)
                sims = cosine_similarity(centroid, cluster_embeddings)[0]
                sorted_pairs = sorted(zip(indices, sims), key=lambda x: -x[1])
                representative_indices = [idx for idx, _ in sorted_pairs[:TOP_N_REPRESENTATIVE_REVIEWS]]
            else:
                representative_indices = indices[:TOP_N_REPRESENTATIVE_REVIEWS]

            representative_reviews = [reviews[i]["text"] for i in representative_indices]
            sentiments = Counter([r["sentiment"] for r in cluster_reviews])

            keyword_counter = Counter()
            for r in cluster_reviews:
                keyword_counter.update(r.get("keywords", []))

            top_keywords = keyword_counter.most_common(TOP_N_CLUSTER_KEYWORDS)
            inferred_topic = self.infer_topic_from_keywords(top_keywords)

            cluster_reports.append({
                "cluster_id": cluster_id,
                "size": len(cluster_reviews),
                "dominant_sentiment": sentiments.most_common(1)[0][0] if sentiments else "unknown",
                "topic": inferred_topic,
                "top_keywords": top_keywords,
                "representative_reviews": representative_reviews,
            })

        return sorted(cluster_reports, key=lambda x: -x["size"])

    # --------------------------------------------------
    # 최종 요약
    # --------------------------------------------------
    def build_summary(self, reviews, cluster_reports, callback=None):
        self._notify(callback, "report", "강점/약점/개선점 생성 중", 95)

        sentiment_counter = Counter([r["sentiment"] for r in reviews])
        topic_counter = Counter()

        for r in reviews:
            topic_counter.update(r.get("topics", []))

        positive_clusters = [c for c in cluster_reports if c["dominant_sentiment"] == "positive"]
        negative_clusters = [c for c in cluster_reports if c["dominant_sentiment"] == "negative"]
        neutral_clusters = [c for c in cluster_reports if c["dominant_sentiment"] == "neutral"]

        strength_clusters = sorted(positive_clusters, key=lambda x: -x["size"])[:3]

        if negative_clusters:
            weakness_clusters = sorted(negative_clusters, key=lambda x: -x["size"])[:3]
            weakness_source = "negative"
        elif neutral_clusters:
            weakness_clusters = sorted(neutral_clusters, key=lambda x: -x["size"])[:3]
            weakness_source = "neutral"
        else:
            weakness_clusters = []
            weakness_source = "fallback"

        improvement_actions = []

        if weakness_clusters:
            for w in weakness_clusters:
                topic = w["topic"]

                if topic == "가격/가성비":
                    if weakness_source == "negative":
                        improvement_actions.append("가격 부담을 느끼는 리뷰가 반복됩니다. 세트 메뉴나 대표 메뉴 구성을 점검해 가격 설득력을 높일 필요가 있습니다.")
                    else:
                        improvement_actions.append("가격 관련 언급이 반복됩니다. 현재 만족도를 유지하면서도 가성비 인식을 높일 수 있는 구성을 검토할 필요가 있습니다.")

                elif topic == "친절/서비스":
                    if weakness_source == "negative":
                        improvement_actions.append("응대 경험에 대한 아쉬움이 보입니다. 주문, 서빙, 마감 인사까지 서비스 톤을 더 일관되게 맞출 필요가 있습니다.")
                    else:
                        improvement_actions.append("서비스 경험을 더 강점으로 키울 여지가 있습니다. 응대 방식과 추천 멘트를 정리하면 재방문 유도에 도움이 됩니다.")

                elif topic == "대기/속도":
                    if weakness_source == "negative":
                        improvement_actions.append("대기 시간이나 주문 속도에 대한 불편이 보입니다. 피크타임 동선과 제조 속도 개선이 필요합니다.")
                    else:
                        improvement_actions.append("속도 관련 만족을 더 높일 수 있습니다. 주문-제조-픽업 흐름을 한 번 더 점검할 필요가 있습니다.")

                elif topic == "좌석/공간":
                    if weakness_source == "negative":
                        improvement_actions.append("좌석이나 공간 이용 경험에서 불편이 보입니다. 좌석 배치와 공간 동선을 재점검할 필요가 있습니다.")
                    else:
                        improvement_actions.append("공간 경험을 더 강하게 만들 여지가 있습니다. 좌석 간격, 체류 편의성, 동선을 점검해보는 것이 좋습니다.")

                elif topic == "청결":
                    if weakness_source == "negative":
                        improvement_actions.append("청결 관련 불만 신호가 있습니다. 테이블, 매장 바닥, 화장실 관리 기준을 더 강화할 필요가 있습니다.")
                    else:
                        improvement_actions.append("청결은 큰 불만은 없지만, 강한 신뢰 요소로 만들 수 있습니다. 눈에 띄는 관리 포인트를 강화해보는 것이 좋습니다.")

                elif topic == "분위기/공간":
                    if weakness_source == "negative":
                        improvement_actions.append("분위기나 공간 경험에서 일부 아쉬움이 보입니다. 음악, 조명, 소음, 체류 경험의 일관성을 점검할 필요가 있습니다.")
                    else:
                        improvement_actions.append("현재 분위기 장점을 더 선명하게 만들 여지가 있습니다. 감성, 편안함, 머무름 경험을 더 강화하는 방향이 좋습니다.")

                elif topic == "맛":
                    if weakness_source == "negative":
                        improvement_actions.append("맛 관련 기대 대비 아쉬움이 일부 보입니다. 대표 메뉴의 맛 일관성과 시그니처 메뉴 완성도를 점검할 필요가 있습니다.")
                    else:
                        improvement_actions.append("맛에 대한 반응은 전반적으로 나쁘지 않지만, 대표 메뉴를 더 강하게 인식시키면 경쟁력이 높아질 수 있습니다.")

                elif topic == "재방문":
                    improvement_actions.append("재방문 유도 요소를 더 강화할 필요가 있습니다. 시그니처 메뉴, 계절 메뉴, 단골 요소를 고민해보는 것이 좋습니다.")

                else:
                    improvement_actions.append(f"{topic} 관련 경험을 더 세밀하게 점검하고 보완할 필요가 있습니다.")

        else:
            improvement_actions.append("전반적인 리뷰 반응은 긍정적입니다. 현재 강점을 유지하면서 가격 체감, 좌석 편의성, 대기 시간 같은 운영 요소를 정기적으로 점검하는 것이 좋습니다.")

            expected_topics = ["맛", "친절/서비스", "분위기/공간", "가격/가성비", "청결", "재방문"]
            weak_topics = [t for t in expected_topics if topic_counter.get(t, 0) == 0]

            if "친절/서비스" in weak_topics:
                improvement_actions.append("서비스 관련 언급이 두드러지지 않습니다. 응대 경험을 더 강한 브랜드 포인트로 만들 여지가 있습니다.")
            if "재방문" in weak_topics:
                improvement_actions.append("재방문 의사를 더 끌어낼 요소가 필요할 수 있습니다. 시그니처 메뉴나 단골화 장치를 고민해볼 수 있습니다.")
            if "청결" in weak_topics:
                improvement_actions.append("청결은 불만이 없더라도 신뢰 형성에 중요합니다. 눈에 보이는 관리 포인트를 꾸준히 강화하는 것이 좋습니다.")

        return {
            "total_reviews": len(reviews),
            "sentiment_distribution": dict(sentiment_counter),
            "topic_distribution": dict(topic_counter),
            "strength_clusters": strength_clusters,
            "weakness_clusters": weakness_clusters,
            "weakness_source": weakness_source,
            "improvement_actions": improvement_actions,
        }

    # --------------------------------------------------
    # 단일 매장 분석
    # --------------------------------------------------
    def analyze_single_store(self, url: str, callback=None):
        store_name, html = self.fetch_html_selenium(url, callback)
        reviews = self.parse_reviews(html, callback)

        if not reviews:
            raise ScrapeError(f"리뷰를 수집하지 못했습니다: {url}")

        reviews = self.enrich_reviews(reviews, callback)
        reviews, embeddings, kmeans = self.cluster_reviews(reviews, callback, n_clusters=N_CLUSTERS)
        cluster_reports = self.build_cluster_reports(reviews, embeddings, kmeans, callback)
        summary = self.build_summary(reviews, cluster_reports, callback)

        return {
            "store_name": store_name,
            "reviews": reviews,
            "cluster_reports": cluster_reports,
            "summary": summary,
        }

    # --------------------------------------------------
    # 비교용 비율 계산
    # --------------------------------------------------
    def _topic_ratio(self, summary, topic):
        total = summary.get("total_reviews", 0)
        if total == 0:
            return 0.0
        return summary.get("topic_distribution", {}).get(topic, 0) / total

    # --------------------------------------------------
    # 경쟁 매장 비교
    # --------------------------------------------------
    def compare_with_competitors(self, my_result, competitor_results):
        topics = [
            "맛", "친절/서비스", "분위기/공간", "가격/가성비",
            "청결", "좌석/공간", "대기/속도", "재방문"
        ]

        my_summary = my_result["summary"]
        comparison_rows = []

        for topic in topics:
            my_ratio = self._topic_ratio(my_summary, topic)

            competitor_ratios = []
            for comp in competitor_results:
                comp_ratio = self._topic_ratio(comp["summary"], topic)
                competitor_ratios.append(comp_ratio)

            competitor_avg = sum(competitor_ratios) / len(competitor_ratios) if competitor_ratios else 0.0
            gap = my_ratio - competitor_avg

            comparison_rows.append({
                "topic": topic,
                "my_ratio": round(my_ratio, 4),
                "competitor_avg_ratio": round(competitor_avg, 4),
                "gap": round(gap, 4),
            })

        return comparison_rows

    # --------------------------------------------------
    # 경쟁 비교 개선 제안
    # --------------------------------------------------
    def build_competitive_actions(self, comparison_rows):
        actions = []

        sorted_rows = sorted(comparison_rows, key=lambda x: x["gap"])

        for idx, row in enumerate(sorted_rows[:3], start=1):
            topic = row["topic"]
            my_ratio = row.get("my_ratio", 0.0)
            competitor_avg_ratio = row.get("competitor_avg_ratio", 0.0)
            gap = row.get("gap", 0.0)

            if abs(gap) < 0.01:
                continue

            if topic == "재방문":
                actions.append({
                    "priority": idx,
                    "title": "재방문 이유 강화",
                    "diagnosis": f"재방문 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "손님이 한 번 만족하고 끝나는 매장일 가능성이 있습니다. 다시 오고 싶은 명확한 이유가 부족하면 상권 내 더 강한 매장으로 수요가 이동할 수 있습니다.",
                    "todo": [
                        "대표 메뉴 1~2개를 '다시 먹으러 오는 메뉴'로 명확히 지정",
                        "계절 한정 메뉴 또는 주간 추천 메뉴를 운영해 재방문 명분 만들기",
                        "적립, 단골 혜택, 재방문 쿠폰 등 반복 방문 장치를 최소 1개 도입"
                    ],
                    "metric": [
                        "'또 오고 싶다', '재방문', '다시 방문' 관련 리뷰 증가 여부",
                        "시그니처 메뉴 주문 비중 변화",
                        "재방문 쿠폰/단골 이벤트 사용률"
                    ]
                })

            elif topic == "친절/서비스":
                actions.append({
                    "priority": idx,
                    "title": "서비스 경험 차별화",
                    "diagnosis": f"서비스 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "불친절하다는 뜻은 아니지만, 손님 기억에 남는 서비스 경험이 경쟁 매장보다 약할 수 있습니다. 무난함은 경쟁 우위가 아닙니다.",
                    "todo": [
                        "주문 시 추천 멘트 1개, 마무리 인사 멘트 1개를 표준화",
                        "초행 손님에게 대표 메뉴 설명을 자연스럽게 붙이는 응대 스크립트 만들기",
                        "피크타임에도 최소 한 번은 고객과 눈 맞춤/인사되는 동선 정리"
                    ],
                    "metric": [
                        "'친절', '서비스 좋다', '응대 좋다' 리뷰 증가 여부",
                        "대표 메뉴 추천 후 주문 전환율",
                        "서비스 관련 부정 리뷰 발생 빈도"
                    ]
                })

            elif topic == "맛":
                actions.append({
                    "priority": idx,
                    "title": "대표 메뉴 인지도 강화",
                    "diagnosis": f"맛/메뉴 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "공간이나 분위기는 괜찮아도 메뉴 자체가 방문 목적이 되는 힘이 약할 수 있습니다. 선택 이유가 약하면 경쟁 매장으로 쉽게 이동합니다.",
                    "todo": [
                        "대표 메뉴 3개를 메뉴판 최상단에 고정 배치",
                        "대표 메뉴 옆에 맛 포인트 한 줄 설명 추가",
                        "리뷰에서 자주 언급된 장점 키워드를 메뉴 설명에 반영"
                    ],
                    "metric": [
                        "'맛있다', 메뉴명 직접 언급 리뷰 증가 여부",
                        "대표 메뉴 3개 주문 비중 변화",
                        "신규 고객의 대표 메뉴 주문 전환율"
                    ]
                })

            elif topic == "분위기/공간":
                actions.append({
                    "priority": idx,
                    "title": "공간 경험 선명화",
                    "diagnosis": f"분위기/공간 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "이 공간이라서 간다는 이유가 경쟁 매장보다 약할 수 있습니다. 체류 경험이 흐리면 재방문 동기도 약해집니다.",
                    "todo": [
                        "사진이 가장 잘 나오는 좌석/구역 1곳을 명확히 연출",
                        "조명, 음악, 테이블 간격 중 가장 약한 요소 1개 우선 수정",
                        "혼자 머무는 손님용 좌석과 대화형 좌석을 구분"
                    ],
                    "metric": [
                        "'분위기', '감성', '공간 좋다' 리뷰 증가 여부",
                        "사진 업로드 포함 리뷰 비중 변화",
                        "체류 관련 언급 증가 여부"
                    ]
                })

            elif topic == "가격/가성비":
                actions.append({
                    "priority": idx,
                    "title": "가성비 인식 재설계",
                    "diagnosis": f"가격/가성비 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "단순히 비싸다는 뜻보다, 손님이 이 가격이면 납득된다고 느끼는 구성이 약할 가능성이 큽니다.",
                    "todo": [
                        "대표 음료 1개 + 디저트 1개를 묶은 입문 세트 1종 추가",
                        "대표 메뉴 3개에 가격 납득 포인트 한 줄 문구 추가",
                        "메뉴판에서 세트/단품 비교가 쉬운 구조로 재배치"
                    ],
                    "metric": [
                        "'가성비', '알차다', '구성 좋다' 리뷰 증가 여부",
                        "세트 메뉴 판매 비중 변화",
                        "대표 메뉴 주문 집중도 변화"
                    ]
                })

            elif topic == "청결":
                actions.append({
                    "priority": idx,
                    "title": "청결 신뢰 포인트 강화",
                    "diagnosis": f"청결 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "청결은 불만이 없으면 잘 드러나지 않지만, 경쟁 매장보다 언급이 적으면 신뢰 요소로 인식되지 못할 수 있습니다.",
                    "todo": [
                        "테이블, 바닥, 화장실 중 고객이 가장 먼저 보는 포인트 우선 관리",
                        "피크타임 전/후 청결 체크리스트 운영",
                        "정리정돈이 보이는 구역을 의도적으로 유지"
                    ],
                    "metric": [
                        "'깨끗', '깔끔', '청결' 리뷰 증가 여부",
                        "청결 관련 불만 발생 빈도",
                        "화장실/테이블 관련 민원 수"
                    ]
                })

            elif topic == "좌석/공간":
                actions.append({
                    "priority": idx,
                    "title": "체류형 좌석 경험 개선",
                    "diagnosis": f"좌석/체류 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "손님이 머물기 편한 곳으로 인식하지 않을 가능성이 있습니다. 체류 경험이 좋은 경쟁 매장으로 선택이 이동할 수 있습니다.",
                    "todo": [
                        "노트북 가능한 넓은 테이블 좌석 2개 이상 확보",
                        "콘센트 접근 가능한 좌석을 명확히 표시",
                        "혼자 오는 손님용 좌석과 대화형 좌석을 분리"
                    ],
                    "metric": [
                        "'자리 편하다', '오래 있기 좋다', '작업하기 좋다' 리뷰 증가 여부",
                        "피크 시간대 좌석 회전률 변화",
                        "체류 시간 관련 언급 증가 여부"
                    ]
                })

            elif topic == "대기/속도":
                actions.append({
                    "priority": idx,
                    "title": "주문·제조 체감 속도 개선",
                    "diagnosis": f"대기/속도 관련 언급 비율이 경쟁 평균보다 낮습니다. (내 매장 {my_ratio:.2%} / 경쟁 평균 {competitor_avg_ratio:.2%}, gap {gap:.2%})",
                    "why": "실제 시간이 아니라 손님이 기다린다고 느끼는 체감 구간이 문제일 수 있습니다.",
                    "todo": [
                        "피크타임 인기 메뉴 2개는 반선조립 상태로 준비",
                        "주문 대기 위치와 픽업 위치를 분리",
                        "제조 시간이 긴 메뉴는 주문 단계에서 먼저 안내"
                    ],
                    "metric": [
                        "주문부터 수령까지 평균 시간",
                        "'빠르다', '오래 걸린다' 리뷰 변화",
                        "피크타임 줄 막힘 발생 횟수"
                    ]
                })

        if not actions:
            actions.append({
                "priority": 1,
                "title": "상대 경쟁력 정밀 진단 필요",
                "diagnosis": "현재 비교 지표상 큰 차이가 뚜렷하지 않습니다.",
                "why": "리뷰만으로는 체감 차이를 완전히 설명하기 어렵습니다. 실제 운영 정보와 결합한 추가 진단이 필요합니다.",
                "todo": [
                    "대표 메뉴 3개와 실제 판매 비중 정리",
                    "피크타임 대기 시간 측정",
                    "좌석 수, 콘센트 수, 체류 가능 좌석 수 정리"
                ],
                "metric": [
                    "대표 메뉴 주문 비중",
                    "피크타임 평균 대기시간",
                    "재방문 리뷰 비율"
                ]
            })

        return actions

    # --------------------------------------------------
    # 단일 실행
    # --------------------------------------------------
    def run(self, url: str, callback=None):
        self.load_models(callback)
        result = self.analyze_single_store(url, callback)
        self._notify(callback, "done", "분석 완료", 100)
        return result

    # --------------------------------------------------
    # 경쟁 비교 실행
    # --------------------------------------------------
    def run_with_competitors(self, my_url: str, competitor_urls: list, callback=None):
        self.load_models(callback)

        my_result = self.analyze_single_store(my_url, callback)

        competitor_results = []
        total = len(competitor_urls)

        for idx, comp_url in enumerate(competitor_urls, start=1):
            self._notify(callback, "report", f"경쟁 매장 분석 중 {idx}/{total}", 95)
            comp_result = self.analyze_single_store(comp_url, callback)
            competitor_results.append(comp_result)

        comparison_rows = self.compare_with_competitors(my_result, competitor_results)
        competitive_actions = self.build_competitive_actions(comparison_rows)

        self._notify(callback, "done", "비교 분석 완료", 100)

        return {
            "my_result": my_result,
            "competitor_results": competitor_results,
            "comparison_rows": comparison_rows,
            "competitive_actions": competitive_actions,
        }