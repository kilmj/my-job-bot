import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 디자인 최적화
st.set_page_config(page_title="충북 맞춤 직업 가이드", layout="wide")

# 가독성을 위한 커스텀 CSS 적용
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stMetric label { font-size: 0.9rem !important; color: #666 !important; }
    .stMetric [data-testid="stMetricValue"] { font-size: 1.2rem !important; font-weight: 700 !important; color: #1E3A8A !important; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    div[data-testid="stExpander"] { background-color: white; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    job_desc = pd.read_csv('한국고용정보원_구인표준직무기술서_20250901.csv', encoding='cp949')
    cb_stats = pd.read_csv('행정구역_시도__직업별_취업자_충북.csv', encoding='cp949')
    seekers = pd.read_csv('한국장애인고용공단_장애인 구직자 현황_20251231.CSV', encoding='cp949')
    return job_desc, cb_stats, seekers

try:
    job_desc, cb_stats, seekers = load_data()

    # --- [ 사이드바 디자인 ] ---
    with st.sidebar:
        st.header("📍 지역 통계 요약")
        st.markdown("---")
        st.subheader("🔥 충북 인기 직종")
        
        # '계'와 '충청북도' 제외하고 순수 직업명만 추출하기 위한 처리
        top_jobs = cb_stats.sort_values(by=cb_stats.columns[-1], ascending=False)
        # 불필요한 행 필터링 (가정: '계'라는 단어가 포함된 행 제외)
        filtered_jobs = top_jobs[~top_jobs.iloc[:, 1].str.contains('계|충청북도', na=False)].head(5)
        
        for i in range(len(filtered_jobs)):
            st.success(f"**{i+1}위** | {filtered_jobs.iloc[i, 1]}")

    # --- [ 메인 화면 디자인 ] ---
    st.title("🏔️ 충청북도 맞춤형 직업 정보 가이드")
    st.info("충북 지역의 실제 채용 데이터와 구직 현황을 기반으로 정보를 제공합니다.")

    # [분석 2] 구직자 선호 직종 카드 섹션
    st.markdown("### 💡 충북 구직자 선호 직종 TOP 5")
    
    try:
        loc_idx = next((i for i, c in enumerate(seekers.columns) if '지역' in c), 0)
        job_idx = next((i for i, c in enumerate(seekers.columns) if '직종' in c), 1)
        cb_seekers = seekers[seekers.iloc[:, loc_idx].str.contains('충북|충청북도', na=False)]
        
        if not cb_seekers.empty:
            pref_jobs = cb_seekers.iloc[:, job_idx].value_counts().head(5)
            cols = st.columns(5)
            for idx, (job, count) in enumerate(pref_jobs.items()):
                # Metric 대신 깔끔한 카드로 표시 (글자 잘림 방지)
                with cols[idx]:
                    st.metric(label=f"TOP {idx+1}", value=job[:8] + '..' if len(job) > 8 else job, delta=f"{count}명")
    except:
        st.write("데이터 분석 중...")

    st.markdown("---")

    # [ 검색 섹션 ]
    st.markdown("### 🔍 상세 직무 및 자격증 검색")
    query = st.text_input("", placeholder="궁금한 직업이나 분야를 입력해 보세요 (예: 요양보호사, 사무원...)")

    if query:
        result = job_desc[job_desc['직종'].str.contains(query, na=False)]
        if not result.empty:
            st.write(f"**'{query}'** 관련 검색 결과입니다.")
            for i in range(len(result)):
                with st.expander(f"📂 {result.iloc[i]['직종']}"):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.markdown("**🛠 핵심 직무 기술**")
                        st.write(result.iloc[i]['표준직무능력내용'])
                    with c2:
                        st.markdown("**📜 추천 자격증**")
                        st.info(result.iloc[i]['표준직무자격증내용'])
        else:
            st.warning("일치하는 정보를 찾지 못했습니다. 다른 키워드로 검색해 보세요.")

except Exception as e:
    st.error(f"시스템 오류: {e}")
