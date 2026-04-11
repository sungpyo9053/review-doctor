import pandas as pd
import streamlit as st

from pipeline_service import ReviewAnalysisPipeline


st.set_page_config(page_title="리뷰 분석 파이프라인", layout="wide")

st.title("네이버 플레이스 리뷰 분석 툴")
st.caption("URL 입력 → 크롤링 → 감성분석 → 임베딩 → 군집화 → 내부 진단 + 경쟁 비교 확장")

my_url = st.text_input(
    "내 매장 네이버 플레이스 리뷰 URL",
    value="https://m.place.naver.com/restaurant/2051084271/review/visitor"
)

competitor_urls_text = st.text_area(
    "비교 매장 URL들 (선택, 줄바꿈으로 여러 개 입력)",
    value="https://m.place.naver.com/restaurant/1212622367/review/visitor",
    placeholder=(
        #"https://m.place.naver.com/restaurant/1212622367/review/visitor\n"
        #"https://m.place.naver.com/restaurant/2222222222/review/visitor"
    ),
    height=120,
)

run_button = st.button("분석 시작", use_container_width=True)

progress_bar = st.progress(0)
status_text = st.empty()
step_box = st.empty()

steps_done = {
    "load_models": False,
    "crawl": False,
    "parse": False,
    "analyze": False,
    "embedding": False,
    "cluster": False,
    "summarize": False,
    "report": False,
    "done": False,
}


def render_steps():
    labels = {
        "load_models": "1. 모델 로딩",
        "crawl": "2. 리뷰 크롤링",
        "parse": "3. 리뷰 파싱",
        "analyze": "4. 감성/주제 분석",
        "embedding": "5. 임베딩 생성",
        "cluster": "6. 유사 리뷰 군집화",
        "summarize": "7. 대표 리뷰/핵심 주제 추출",
        "report": "8. 리포트 생성",
        "done": "9. 완료",
    }

    lines = []
    for key, label in labels.items():
        mark = "✅" if steps_done[key] else "⬜"
        lines.append(f"{mark} {label}")

    step_box.markdown("\n\n".join(lines))


def on_progress(step, message, percent):
    if step in steps_done:
        steps_done[step] = True

    progress_bar.progress(percent)
    status_text.info(message)
    render_steps()


def render_cluster_section(title, clusters, empty_message, tone="info"):
    st.markdown(f"### {title}")

    if not clusters:
        if tone == "warning":
            st.warning(empty_message)
        elif tone == "success":
            st.success(empty_message)
        else:
            st.info(empty_message)
        return

    for c in clusters:
        with st.expander(f"군집 {c['cluster_id']} | {c['topic']} | {c['size']}건"):
            st.write("대표 감성:", c.get("dominant_sentiment", ""))
            st.write("핵심 키워드:", c.get("top_keywords", []))
            st.write("대표 리뷰")
            for review in c.get("representative_reviews", []):
                st.markdown(f"- {review}")


def render_action_cards(actions, title):
    st.markdown(f"### {title}")

    if not actions:
        st.info("현재 출력 가능한 실행 항목이 없습니다.")
        return

    for idx, action in enumerate(actions, start=1):
        st.markdown(
            f"""
            <div style="
                padding:14px 16px;
                border-radius:12px;
                background-color:#f7f9fc;
                border:1px solid #e6ebf2;
                margin-bottom:10px;
            ">
                <div style="font-weight:700; margin-bottom:6px;">액션 {idx}</div>
                <div>{action}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def build_internal_insight(summary, strength_clusters, weakness_clusters):
    weakness_source = summary.get("weakness_source", "fallback")

    if weakness_clusters and weakness_source == "negative":
        return (
            "리뷰 안에서 반복적으로 드러나는 불편 신호가 있습니다. "
            "현재는 강점 확대보다, 눈에 보이는 불편 요소를 먼저 줄이는 것이 우선입니다."
        )

    if weakness_clusters and weakness_source == "neutral":
        return (
            "큰 불만은 아니지만, 애매하거나 아쉬운 반응이 반복되는 포인트가 있습니다. "
            "즉시 문제 해결보다 운영 완성도를 높이는 개선이 적절한 단계입니다."
        )

    if not weakness_clusters and strength_clusters:
        return (
            "현재 리뷰 반응은 전반적으로 긍정적입니다. 다만 이것이 곧 경쟁 우위를 의미하는 것은 아닙니다. "
            "내부 불만이 적을 뿐, 같은 상권의 더 강한 매장과 비교하면 부족한 선택 이유가 있을 수 있습니다."
        )

    return (
        "리뷰 수나 표현 분산 정도 때문에 내부 진단 신호가 약할 수 있습니다. "
        "리뷰 수가 더 쌓이거나 경쟁 매장 비교가 함께 들어오면 해석 품질이 높아집니다."
    )


def build_comparison_needed_actions(summary, weakness_clusters, competitor_urls):
    actions = []

    if weakness_clusters:
        return actions

    actions.append(
        "현재 리뷰만 보면 큰 불만은 두드러지지 않습니다. 다음 단계로는 같은 상권 경쟁 매장과 비교해 상대적 약점을 찾아야 합니다."
    )

    actions.append(
        "특히 재방문 이유, 시그니처 메뉴 인식, 서비스 차별화, 공간 체류 경험 같은 항목은 경쟁 매장과의 Gap 분석이 필요합니다."
    )

    if competitor_urls:
        actions.append(
            "비교 매장 URL이 입력되어 있으므로, 각 매장의 주제 분포와 대표 강점/약점을 같은 기준으로 비교해 상대적 개선점을 도출하는 단계가 필요합니다."
        )
    else:
        actions.append(
            "비교 리포트를 위해 같은 상권의 유사 업종 매장 2~5개의 리뷰 URL을 함께 입력받는 방식으로 확장하는 것이 좋습니다."
        )

    return actions


def render_comparison_section(comparison_rows, competitor_results):
    st.markdown("### 경쟁 비교 결과")

    if not comparison_rows:
        st.info("경쟁 비교 결과가 아직 없습니다. 비교 URL을 입력하고, 서비스 로직에 비교 분석 기능이 연결되면 이 영역에 Gap 분석이 표시됩니다.")
        return

    st.success(f"경쟁 매장 {len(competitor_results)}곳과 비교한 결과입니다.")

    comparison_df = pd.DataFrame(comparison_rows)
    st.dataframe(comparison_df, use_container_width=True)

    if competitor_results:
        st.markdown("#### 비교 대상 매장")
        for comp in competitor_results:
            st.markdown(f"- {comp.get('store_name', 'unknown_store')}")


def serialize_reviews_for_table(reviews):
    review_rows = []
    for r in reviews:
        review_rows.append({
            "date": r.get("date", ""),
            "author": r.get("author", ""),
            "rating": r.get("rating", ""),
            "sentiment": r.get("sentiment", ""),
            "sentiment_score": r.get("sentiment_score", ""),
            "topics": ", ".join(r.get("topics", [])),
            "keywords": ", ".join(r.get("keywords", [])),
            "tags": ", ".join(r.get("tags", [])),
            "text": r.get("text", ""),
        })
    return pd.DataFrame(review_rows)


def serialize_clusters_for_table(cluster_reports):
    cluster_rows = []
    for c in cluster_reports:
        cluster_rows.append({
            "cluster_id": c.get("cluster_id"),
            "size": c.get("size"),
            "dominant_sentiment": c.get("dominant_sentiment"),
            "topic": c.get("topic"),
            "top_keywords": ", ".join([f"{k}:{v}" for k, v in c.get("top_keywords", [])]),
            "representative_reviews": " / ".join(c.get("representative_reviews", [])),
        })
    return pd.DataFrame(cluster_rows)


render_steps()

if run_button:
    pipeline = ReviewAnalysisPipeline()
    competitor_urls = [x.strip() for x in competitor_urls_text.splitlines() if x.strip()]

    with st.spinner("전체 파이프라인 실행 중..."):
        # 비교 분석 함수가 구현되어 있으면 사용
        if competitor_urls and hasattr(pipeline, "run_with_competitors"):
            result = pipeline.run_with_competitors(my_url, competitor_urls, callback=on_progress)
            my_result = result.get("my_result", {})
            competitor_results = result.get("competitor_results", [])
            comparison_rows = result.get("comparison_rows", [])
            competitive_actions = result.get("competitive_actions", [])
        else:
            my_result = pipeline.run(my_url, callback=on_progress)
            competitor_results = []
            comparison_rows = []
            competitive_actions = []

    st.success("분석 완료")

    store_name = my_result.get("store_name", "unknown_store")
    reviews = my_result.get("reviews", [])
    cluster_reports = my_result.get("cluster_reports", [])
    summary = my_result.get("summary", {})

    strength_clusters = summary.get("strength_clusters", [])
    weakness_clusters = summary.get("weakness_clusters", [])
    improvement_actions = summary.get("improvement_actions", [])
    weakness_source = summary.get("weakness_source", "fallback")

    internal_insight = build_internal_insight(summary, strength_clusters, weakness_clusters)
    comparison_needed_actions = build_comparison_needed_actions(summary, weakness_clusters, competitor_urls)

    st.subheader(f"가게명: {store_name}")

    col1, col2, col3 = st.columns(3)
    col1.metric("총 리뷰 수", summary.get("total_reviews", 0))
    col2.metric("긍정 리뷰 수", summary.get("sentiment_distribution", {}).get("positive", 0))
    col3.metric("부정 리뷰 수", summary.get("sentiment_distribution", {}).get("negative", 0))

    st.markdown("### 내부 진단 해석")
    if weakness_clusters and weakness_source == "negative":
        st.warning(internal_insight)
    elif weakness_clusters and weakness_source == "neutral":
        st.info(internal_insight)
    else:
        st.success(internal_insight)

    st.markdown("### 감성 분포")
    sentiment_dist = summary.get("sentiment_distribution", {})
    if sentiment_dist:
        sentiment_df = pd.DataFrame(
            list(sentiment_dist.items()),
            columns=["sentiment", "count"]
        )
        st.bar_chart(sentiment_df.set_index("sentiment"))
    else:
        st.info("감성 분포 데이터가 없습니다.")

    st.markdown("### 주제 분포")
    topic_dist = summary.get("topic_distribution", {})
    if topic_dist:
        topic_df = pd.DataFrame(
            list(topic_dist.items()),
            columns=["topic", "count"]
        )
        st.bar_chart(topic_df.set_index("topic"))
    else:
        st.info("주제 데이터가 없습니다.")

    render_cluster_section(
        "강점 군집",
        strength_clusters,
        "뚜렷한 강점 군집을 아직 추출하지 못했습니다. 리뷰 수가 적거나 표현이 분산되었을 수 있습니다.",
        tone="success"
    )

    if weakness_source == "negative":
        weakness_empty_message = "부정 군집이 추출되지 않았습니다."
    elif weakness_source == "neutral":
        weakness_empty_message = "명확한 부정 군집은 없지만, 애매한 반응을 보완 포인트로 추출할 수 있습니다."
    else:
        weakness_empty_message = (
            "뚜렷한 불만 군집은 크게 보이지 않습니다. "
            "다만 이것이 곧 경쟁 매장 대비 우위라는 뜻은 아닙니다."
        )

    render_cluster_section(
        "내부 보완 포인트",
        weakness_clusters,
        weakness_empty_message,
        tone="info"
    )

    render_action_cards(improvement_actions, "내부 기준 개선 제안")

    if competitor_urls:
        render_action_cards(competitive_actions, "경쟁 비교 기반 개선 제안")
        render_comparison_section(comparison_rows, competitor_results)
    else:
        render_action_cards(comparison_needed_actions, "비교 기반 추가 분석 제안")

    st.markdown("### 비교 분석 상태")
    if competitor_urls and hasattr(pipeline, "run_with_competitors"):
        st.success(
            f"경쟁 매장 URL {len(competitor_urls)}개가 입력되었고, 비교 분석 함수가 연결되어 있습니다."
        )
    elif competitor_urls and not hasattr(pipeline, "run_with_competitors"):
        st.warning(
            f"경쟁 매장 URL {len(competitor_urls)}개가 입력되었지만, 현재 `pipeline_service.py`에 "
            "`run_with_competitors()`가 없어 실제 비교 분석은 수행되지 않았습니다."
        )
    else:
        st.info(
            "현재는 단일 매장 내부 진단만 수행하고 있습니다. "
            "실질적인 상대 개선 포인트를 얻으려면 같은 상권 경쟁 매장 URL을 함께 넣어 비교 분석으로 확장해야 합니다."
        )

    st.markdown("### 전체 리뷰 데이터")
    review_df = serialize_reviews_for_table(reviews)
    st.dataframe(review_df, use_container_width=True)

    st.markdown("### 군집 원본 데이터")
    cluster_df = serialize_clusters_for_table(cluster_reports)
    st.dataframe(cluster_df, use_container_width=True)