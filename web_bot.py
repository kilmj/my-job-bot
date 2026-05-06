import streamlit as st
import pandas as pd

st.set_page_config(page_title="충북 맞춤형 직업 추천", layout="wide")

@st.cache_data
def load_data():
    # 파일 로드 (파일명 및 인코딩 설정)
    job_desc = pd.read_csv('한국고용정보원_구인표준직무기술서_20250901.csv', encoding='cp949')
    cb_stats = pd.read_csv('행정구역_시도__직업별_취업자_충북.csv', encoding='cp949')
    seekers = pd.read_csv('한국장애인고용공단_장애인 구직자 현황_20251231.CSV', encoding='cp949')
    return job_desc, cb_stats, seekers

try:
    job_desc, cb_stats, seekers = load_data()

    # 사이드바 설정
    st.sidebar.title("📍 충북 지역 데이터 요약")
    st.sidebar.subheader("🔥 충북 인기 직종 TOP 5")

    # [분석 1] 취업자 통계 처리
    # 보통 0번 열이 지역, 1번 열이 직업명인 경우가 많으므로 1번 열을 가져옵니다.
    # 만약 직업명이 여전히 안 나온다면 iloc[i, 1]의 숫자 1을 2나 0으로 바꿔보세요.
    top_jobs = cb_stats.sort_values(by=cb_stats.columns[-1], ascending=False).head(5)
    for i in range(len(top_jobs)):
        job_name = top_jobs.iloc[i, 1] # 첫 번째(0)가 아닌 두 번째(1) 열을 시도
        st.sidebar.write(f"- {job_name}")

    # 메인 화면
    st.title("🏔️ 충청북도 맞춤형 직업/직무 추천 서비스")

    # [분석 2] 구직자 선호 직종 처리
    st.subheader("💡 충북 지역 구직자 선호 직종 (충북 기준)")
    
    # 컬럼 이름에 상관없이 '위치'로 접근 (보통 희망지역은 앞쪽, 희망직종은 뒤쪽에 있음)
    # 아래 숫자는 파일 구조에 따라 조정이 필요할 수 있습니다.
    try:
        # '희망근무지역' 단어가 포함된 열 찾기 (없으면 0번 열 사용)
        loc_idx = next((i for i, c in enumerate(seekers.columns) if '지역' in c), 0)
        # '희망직종' 단어가 포함된 열 찾기 (없으면 1번 열 사용)
        job_idx = next((i for i, c in enumerate(seekers.columns) if '직종' in c), 1)

        cb_seekers = seekers[seekers.iloc[:, loc_idx].str.contains('충북|충청북도', na=False)]
        
        if not cb_seekers.empty:
            pref_jobs = cb_seekers.iloc[:, job_idx].value_counts().head(5)
            cols = st.columns(5)
            for idx, (job, count) in enumerate(pref_jobs.items()):
                cols[idx].metric(label=f"TOP {idx+1}", value=job, delta=f"{count}명 희망")
        else:
            st.info("충북 지역 구직자 데이터를 찾는 중입니다...")
    except:
        st.warning("구직자 현황 데이터의 컬럼 구조를 확인 중입니다.")

    st.divider()

    # 검색 기능
    st.subheader("🔍 직무 기술 및 자격증 상세 검색")
    query = st.text_input("직업명이나 관심 분야를 입력하세요", placeholder="예: 요양보호사, 사무원, 사회복지...")

    if query:
        # '직종' 컬럼에서 검색
        result = job_desc[job_desc['직종'].str.contains(query, na=False)]
        if not result.empty:
            for i in range(len(result)):
                with st.expander(f"📌 {result.iloc[i]['직종']} (상세 정보)"):
                    st.write(f"**🛠 필요 기술:** {result.iloc[i]['표준직무능력내용']}")
                    st.info(f"**📜 추천 자격증:** {result.iloc[i]['표준직무자격증내용']}")
        else:
            st.warning("관련 정보를 찾지 못했습니다.")

except Exception as e:
    st.error(f"오류 발생: {e}")
