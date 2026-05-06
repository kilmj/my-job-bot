import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 에듀테크 스타일 CSS 적용
st.set_page_config(page_title="충북 맞춤형 직업 가이드", layout="wide")

st.markdown("""
    <style>
    /* 전체 배경색 - 아주 연한 회색으로 고급스럽게 */
    .stApp {
        background-color: #F0F4F8;
    }
    /* 상단 네비게이션바 느낌의 헤더 */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        padding: 20px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .nav-item {
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: bold;
        cursor: pointer;
    }
    .active-nav { background-color: #4F46E5; color: white; }
    .inactive-nav { background-color: #F8FAFC; color: #64748B; border: 1px solid #E2E8F0; }

    /* 메인 카드 스타일 */
    .main-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    /* 통계 카드 스타일 (참고 이미지의 하단 카드 느낌) */
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #E2E8F0;
        transition: transform 0.3s ease;
    }
    .stat-card:hover { transform: translateY(-5px); }
    
    .icon-box {
        background-color: #4F46E5;
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px auto;
        color: white;
        font-size: 20px;
    }
    
    .start-btn {
        background-color: #475569;
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-top: 15px;
        font-weight: bold;
        text-decoration: none;
        display: block;
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

    # 상단 탭 버튼 UI
    st.markdown("""
        <div class="nav-container">
            <div class="nav-item inactive-nav">📖 통합 대시보드</div>
            <div class="nav-item active-nav">🎓 맞춤형 직무 탐색</div>
        </div>
    """, unsafe_allow_html=True)

    # 섹션 1: 충북 채용 시장 현황
    st.markdown(f"""
        <div class="main-card">
            <h2 style='margin:0; color:#1E293B;'>🏔️ 충청북도 맞춤형 직업 가이드</h2>
            <p style='color:#64748B;'>충북 지역의 채용 데이터와 구직 현황을 기반으로 한 개인화 서비스입니다.</p>
        </div>
    """, unsafe_allow_html=True)

    # 중앙 콘텐츠 레이아웃
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 🏢 지역 채용 시장 TOP 3")
        top_hiring = cb_stats.sort_values(by=cb_stats.columns[-1], ascending=False)
        filtered_hiring = top_hiring[~top_hiring.iloc[:, 1].str.contains('계|충청북도', na=False)].head(3)
        
        for i in range(len(filtered_hiring)):
            st.markdown(f"""
                <div class="stat-card" style="margin-bottom:15px; text-align:left; border-left: 5px solid #4F46E5;">
                    <div style="font-size:0.8rem; color:#4F46E5; font-weight:bold;">시장 수요 {i+1}위</div>
                    <div style="font-size:1.2rem; font-weight:bold; color:#1E293B;">{filtered_hiring.iloc[i, 1]}</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ♿ 장애인 구직 선호 TOP 3")
        try:
            loc_idx = next((i for i, c in enumerate(seekers.columns) if '지역' in c), 0)
            job_idx = next((i for i, c in enumerate(seekers.columns) if '직종' in c), 1)
            cb_seekers = seekers[seekers.iloc[:, loc_idx].str.contains('충북|충청북도', na=False)]
            pref_jobs = cb_seekers.iloc[:, job_idx].value_counts().head(3)
            
            for idx, (job, count) in enumerate(pref_jobs.items()):
                st.markdown(f"""
                    <div class="stat-card" style="margin-bottom:15px; text-align:left; border-left: 5px solid #10B981;">
                        <div style="font-size:0.8rem; color:#10B981; font-weight:bold;">선호도 {idx+1}위</div>
                        <div style="font-size:1.2rem; font-weight:bold; color:#1E293B;">{job}</div>
                        <div style="font-size:0.8rem; color:#64748B;">현재 {count}명의 구직자가 희망 중</div>
                    </div>
                """, unsafe_allow_html=True)
        except:
            st.write("데이터 로딩 중...")

    st.markdown("<br>", unsafe_allow_html=True)

    # 하단 검색 섹션 (참고 이미지의 3단 카드 레이아웃 느낌 적용)
    st.markdown("### 🔍 직무 체험 및 상세 검색")
    query = st.text_input("검색어를 입력하여 상세 직무 가이드를 확인하세요.", placeholder="예: 사무원, 요양보호사...")

    if query:
        result = job_desc[job_desc['직종'].str.contains(query, na=False)].head(3)
        if not result.empty:
            search_cols = st.columns(len(result))
            for i in range(len(result)):
                with search_cols[i]:
                    st.markdown(f"""
                        <div class="stat-card">
                            <div class="icon-box">🧠</div>
                            <h4 style="margin:5px 0;">{result.iloc[i]['직종']}</h4>
                            <p style="font-size:0.8rem; color:#64748B; height:60px; overflow:hidden;">
                                {result.iloc[i]['표준직무능력내용'][:60]}...
                            </p>
                            <div class="start-btn">상세 보기 →</div>
                        </div>
                    """, unsafe_allow_html=True)
                    # 실제 내용은 Expander로 하단에 별도 표기
                    with st.expander(f"{result.iloc[i]['직종']} 자격증/직무 자세히 보기"):
                        st.info(f"**추천 자격증:** {result.iloc[i]['표준직무자격증내용']}")
                        st.write(f"**전체 직무 기술:** {result.iloc[i]['표준직무능력내용']}")

    # 푸터 근거 섹션 (참고 이미지 하단 파란 버튼 섹션 느낌)
    st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #E2E8F0; margin-top: 50px;">
            <div>
                <strong style="color:#1E293B;">📊 데이터 기반 설계 근거</strong><br>
                <span style="font-size:0.8rem; color:#64748B;">본 서비스는 2025-2026 공공데이터 포털 및 한국장애인고용공단 자료를 근거로 제작되었습니다.</span>
            </div>
            <div style="background-color: #4F46E5; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 0.9rem;">자세히 보기 〉</div>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"디자인 엔진 로드 중 오류 발생: {e}")
