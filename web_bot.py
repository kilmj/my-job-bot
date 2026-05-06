import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 다크 테마 디자인 최적화
st.set_page_config(page_title="충북 맞춤 직업 가이드", layout="wide")

# 가독성을 위한 고대비 다크 모드 CSS 적용
st.markdown("""
    <style>
    /* 전체 배경색 설정 */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    /* 카드 스타일링 (고대비) */
    .job-card {
        background-color: #1e293b;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #38bdf8;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .stat-title {
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 20px;
        color: #38bdf8;
        border-bottom: 2px solid #334155;
        padding-bottom: 10px;
    }
    /* 입력창 및 검색바 스타일 */
    .stTextInput input {
        background-color: #334155 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }
    /* 익스팬더(상세정보) 스타일 */
    .stDetailed {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    h1, h2, h3 {
        color: #f1f5f9 !important;
    }
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

    # --- [ 사이드바 ] ---
    with st.sidebar:
        st.markdown("<h2 style='color:#38bdf8;'>📍 충북 데이터 센터</h2>", unsafe_allow_html=True)
        st.write("실시간 공공데이터를 기반으로 분석한 충청북도 지역 특화 정보입니다.")
        st.divider()
        st.caption("© 2026 충북 직업 가이드 서비스")

    # --- [ 메인 화면 ] ---
    st.markdown("<h1 style='text-align: center;'>🏔️ 충청북도 직업 매칭 대시보드</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#94a3b8;'>채용 현황과 구직자 선호를 비교하여 최적의 직업군을 제안합니다.</p>", unsafe_allow_html=True)
    st.write("")

    # --- [ 핵심 통계 영역 ] ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<div class='stat-title'>🏢 충북 시장 채용 현황 (Top 5)</div>", unsafe_allow_html=True)
        top_hiring = cb_stats.sort_values(by=cb_stats.columns[-1], ascending=False)
        filtered_hiring = top_hiring[~top_hiring.iloc[:, 1].str.contains('계|충청북도', na=False)].head(5)
        
        for i in range(len(filtered_hiring)):
            job_name = filtered_hiring.iloc[i, 1]
            st.markdown(f"""
            <div class='job-card' style='border-left-color: #38bdf8;'>
                <span style='color: #7dd3fc; font-size: 0.85rem; font-weight:bold;'>MARKET RANK {i+1}</span><br>
                <span style='font-size: 1.15rem; font-weight: 700;'>{job_name}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='stat-title'>♿ 장애인 구직자 선호 직종 (Top 5)</div>", unsafe_allow_html=True)
        try:
            loc_idx = next((i for i, c in enumerate(seekers.columns) if '지역' in c), 0)
            job_idx = next((i for i, c in enumerate(seekers.columns) if '직종' in c), 1)
            cb_seekers = seekers[seekers.iloc[:, loc_idx].str.contains('충북|충청북도', na=False)]
            
            if not cb_seekers.empty:
                pref_jobs = cb_seekers.iloc[:, job_idx].value_counts().head(5)
                for idx, (job, count) in enumerate(pref_jobs.items()):
                    st.markdown(f"""
                    <div class='job-card' style='border-left-color: #fbbf24;'>
                        <span style='color: #fcd34d; font-size: 0.85rem; font-weight:bold;'>PREFERENCE RANK {idx+1}</span><br>
                        <span style='font-size: 1.15rem; font-weight: 700;'>{job}</span>
                        <span style='color: #94a3b8; font-size: 0.9rem; margin-left:10px;'>{count}명 대기 중</span>
                    </div>
                    """, unsafe_allow_html=True)
        except:
            st.error("구직자 데이터를 로드할 수 없습니다.")

    st.write("")
    st.markdown("<div style='background-color:#334155; height:2px; margin: 40px 0;'></div>", unsafe_allow_html=True)

    # --- [ 상세 검색 섹션 ] ---
    st.markdown("### 🔍 직무 상세 정보 검색")
    query = st.text_input("", placeholder="궁금한 직종명을 입력하세요 (예: 사무원, 조리사, 청소원...)")

    if query:
        result = job_desc[job_desc['직종'].str.contains(query, na=False)]
        if not result.empty:
            for i in range(len(result)):
                with st.expander(f"📄 {result.iloc[i]['직종']} 분석 결과"):
                    res_col1, res_col2 = st.columns([3, 2])
                    with res_col1:
                        st.markdown("<p style='color:#38bdf8; font-weight:bold;'>[ 주요 수행 직무 ]</p>", unsafe_allow_html=True)
                        st.write(result.iloc[i]['표준직무능력내용'])
                    with res_col2:
                        st.markdown("<p style='color:#fbbf24; font-weight:bold;'>[ 권장 자격증 ]</p>", unsafe_allow_html=True)
                        st.info(result.iloc[i]['표준직무자격증내용'])
        else:
            st.warning("입력하신 직종에 대한 상세 가이드가 없습니다.")

except Exception as e:
    st.error(f"시스템 초기화 오류: {e}")
