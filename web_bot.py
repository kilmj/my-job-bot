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
    # 3. 구직자 현황 (장애인 고용공단) - 파일명이 대소문자 섞여있을 수 있으니 주의
    seekers = pd.read_csv('한국장애인고용공단_장애인 구직자 현황_20251231.CSV', encoding='cp949')
    return job_desc, cb_stats, seekers

try:
    job_desc, cb_stats, seekers = load_data()

    # 사이드바: 충북 지역 통계 브리핑
    st.sidebar.title("📍 충북 지역 데이터 요약")

    # [분석 1] 충북 내 취업 분야 TOP 5 (KeyError 방지를 위해 iloc 사용)
    st.sidebar.subheader("🔥 충북 인기 직종 TOP 5")
    # 마지막 컬럼(취업자 수)을 기준으로 정렬
    top_jobs = cb_stats.sort_values(by=cb_stats.columns[-1], ascending=False).head(5)
    
    for i in range(len(top_jobs)):
        # iloc[i, 0]은 i번째 행의 첫 번째 열 값을 가져옵니다 (보통 직업명)
        job_name = top_jobs.iloc[i, 0]
        st.sidebar.write(f"- {job_name}")

    # 메인 화면
    st.title("🏔️ 충청북도 맞춤형 직업/직무 추천 서비스")

    # [분석 2] 충북 구직자 선호 직종
    st.subheader("💡 충북 지역 구직자 선호 직종 (충북 기준)")
    
    # 컬럼명에 '희망근무지역'이나 '희망직종'이 포함된 것을 자동으로 찾음
    loc_col = [c for c in seekers.columns if '희망근무지역' in c][0]
    job_col = [c for c in seekers.columns if '희망직종' in c][0]

    cb_seekers = seekers[seekers[loc_col].str.contains('충북|충청북도', na=False)]
    
    if not cb_seekers.empty:
        pref_jobs = cb_seekers[job_col].value_counts().head(5)
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

except Exception as e:
    st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")
    st.info("CSV 파일의 컬럼명이나 형식이 코드와 맞지 않을 수 있습니다. 파일의 첫 줄 내용을 확인해 주세요.")
