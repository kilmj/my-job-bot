import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 디자인 최적화
st.set_page_config(page_title="충북 맞춤 직업 가이드", layout="wide")

# 레이아웃 가독성을 위한 커스텀 CSS
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .job-card { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 5px solid #1E3A8A; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .stat-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; color: #333; }
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

    # --- [ 사이드바: 고정 정보 ] ---
    with st.sidebar:
        st.header("📍 충북 데이터 센터")
        st.info("실시간 공공데이터를 기반으로 충청북도 지역 특화 정보를 제공합니다.")
        st.divider()
        st.caption("데이터 출처: 한국고용정보원, 한국장애인고용공단, 통계청")

    # --- [ 메인 화면 ] ---
    st.title("🏔️ 충청북도 맞춤형 직업 정보 가이드")
    st.markdown("#### 충북 지역의 **일반 채용 현황**과 **장애인 구직자 선호도**를 비교해 드립니다.")
    st.write("")

    # --- [ 핵심 통계: 두 영역 구분 표시 ] ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='stat-title'>🏢 충북 상위 채용(취업) 직종</div>", unsafe_allow_html=True)
        # '계' 항목 제외하고 취업자 수 상위 5개 추출
        top_hiring = cb_stats.sort_values(by=cb_stats.columns[-1], ascending=False)
        filtered_hiring = top_hiring[~top_hiring.iloc[:, 1].str.contains('계|충청북도', na=False)].head(5)
        
        for i in range(len(filtered_hiring)):
            with st.container():
                st.markdown(f"""
                <div class='job-card'>
                    <small style='color: #1E3A8A;'>채용 순위 {i+1}위</small><br>
                    <strong style='font-size: 1.2rem;'>{filtered_hiring.iloc[i, 1]}</strong>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='stat-title'>♿ 장애인 구직자 선호 직종 (충북)</div>", unsafe_allow_html=True)
        try:
            loc_idx = next((i for i, c in enumerate(seekers.columns) if '지역' in c), 0)
            job_idx = next((i for i, c in enumerate(seekers.columns) if '직종' in c), 1)
            cb_seekers = seekers[seekers.iloc[:, loc_idx].str.contains('충북|충청북도', na=False)]
            
            if not cb_seekers.empty:
                pref_jobs = cb_seekers.iloc[:, job_idx].value_counts().head(5)
                for idx, (job, count) in enumerate(pref_jobs.items()):
                    with st.container():
                        st.markdown(f"""
                        <div class='job-card' style='border-left-color: #10B981;'>
                            <small style='color: #10B981;'>선호 순위 {idx+1}위</small><br>
                            <strong style='font-size: 1.2rem;'>{job}</strong> <span style='font-size: 0.9rem; color: #666;'>({count}명 희망)</span>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.write("해당 지역의 데이터가 부족합니다.")
        except:
            st.error("장애인 구직자 데이터를 불러오는 중 오류가 발생했습니다.")

    st.markdown("---")

    # --- [ 하단 상세 검색 섹션 ] ---
    st.markdown("### 🔍 상세 직무 가이드 검색")
    st.write("위에서 확인한 직종이 실제로 어떤 일을 하는지, 어떤 자격증이 필요한지 검색해 보세요.")
    
    query = st.text_input("", placeholder="예: 사무원, 미화원, 조리사 등 입력...")

    if query:
        result = job_desc[job_desc['직종'].str.contains(query, na=False)]
        if not result.empty:
            st.write(f"**'{query}'**에 대한 {len(result)}건의 직무 상세 정보입니다.")
            for i in range(len(result)):
                with st.expander(f"📖 {result.iloc[i]['직종']} 상세 분석"):
                    c_left, c_right = st.columns([3, 2])
                    with c_left:
                        st.markdown("**[ 핵심 직무 기술 ]**")
                        st.write(result.iloc[i]['표준직무능력내용'])
                    with c_right:
                        st.markdown("**[ 추천 자격증 ]**")
                        st.success(result.iloc[i]['표준직무자격증내용'])
        else:
            st.warning("상세 직무 기술서에 등록되지 않은 직종입니다. 다른 키워드로 검색해 보세요.")

except Exception as e:
    st.error(f"시스템 오류: {e}")
