import streamlit as st
import pandas as pd

st.set_page_config(page_title="충북 맞춤형 직업 추천", layout="wide")

# 데이터 로드 함수
@st.cache_data
def load_data():
    # 1. 기본 직무 기술서
    job_desc = pd.read_csv('한국고용정보원_구인표준직무기술서_20250901.csv', encoding='cp949')
    # 2. 충북 취업자 통계
    cb_stats = pd.read_csv('행정구역_시도__직업별_취업자_충북.csv', encoding='cp949')
    # 3. 구직자 현황 (장애인 고용공단)
    seekers = pd.read_csv('한국장애인고용공단_장애인 구직자 현황_20251231.CSV', encoding='cp949')
    return job_desc, cb_stats, seekers

job_desc, cb_stats, seekers = load_data()

# 사이드바: 충북 지역 통계 브리핑
st.sidebar.title("📍 충북 지역 데이터 요약")

# [분석 1] 충북 내 다수 취업 분야 (가정: 컬럼명에 '직업별'과 '취업자'가 있다고 가정)
st.sidebar.subheader("🔥 충북 인기 직종 TOP 5")
# 실제 파일의 컬럼명에 따라 수정이 필요할 수 있습니다.
top_jobs = cb_stats.sort_values(by=cb_stats.columns[-1], ascending=False).head(5)
for i, row in top_jobs.iterrows():
    st.sidebar.write(f"- {row[0]}")

# 메인 화면
st.title("🏔️ 충청북도 맞춤형 직업/직무 추천 서비스")

# [분석 2] 충북 구직자 선호 직종
st.subheader("💡 충북 지역 구직자들은 이런 직종을 희망해요")
cb_seekers = seekers[seekers['희망근무지역'].str.contains('충북|충청북도', na=False)]
if not cb_seekers.empty:
    pref_jobs = cb_seekers['희망직종'].value_counts().head(5)
    cols = st.columns(5)
    for idx, (job, count) in enumerate(pref_jobs.items()):
        cols[idx].metric(label=f"TOP {idx+1}", value=job, delta=f"{count}명 희망")

st.divider()

# 기존 검색 기능
st.subheader("🔍 직무 기술 및 자격증 상세 검색")
query = st.text_input("직업명이나 관심 분야를 입력하세요", placeholder="예: 요양보호사, 사무원, 사회복지...")

if query:
    result = job_desc[job_desc['직종'].str.contains(query, na=False)]
    if not result.empty:
        for i in range(len(result)):
            with st.expander(f"📌 {result.iloc[i]['직종']} (상세 정보)"):
                st.write(f"**🛠 필요 기술:** {result.iloc[i]['표준직무능력내용']}")
                st.info(f"**📜 추천 자격증:** {result.iloc[i]['표준직무자격증내용']}")
    else:
        st.warning("관련 정보를 찾지 못했습니다.")
