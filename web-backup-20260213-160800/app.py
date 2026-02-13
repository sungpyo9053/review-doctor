import streamlit as st
import requests

st.set_page_config(page_title="리뷰닥터 POC", layout="wide")
st.title("리뷰닥터 - POC 버전")

store_name = st.text_input("가게명 입력", placeholder="예: 홍대 김밥천국")

if st.button("분석 시작", type="primary"):
    if not store_name.strip():
        st.error("가게명을 입력해주세요.")
    else:
        with st.spinner("분석 중..."):
            try:
                res = requests.post("http://127.0.0.1:8000/analyze", json={"store_name": store_name.strip()})
                res.raise_for_status()
                data = res.json()

                st.success("분석 완료!")
                st.subheader(f"{data['store']} 리포트")
                st.metric("리뷰 수", data['review_count'])
                st.info(data['sentiment'])

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**강점**")
                    for p in data['strong_points']:
                        st.success(p)
                with col2:
                    st.markdown("**약점**")
                    for w in data['weak_points']:
                        st.warning(w)

                st.markdown("**개선 제안**")
                for a in data['action_items']:
                    st.info(a)
            except Exception as e:
                st.error(f"오류: {str(e)}")
