import streamlit as st
import pandas as pd

# 웹 페이지 설정 (브라우저 탭 이름과 아이콘)
st.set_page_config(page_title="직업 추천 챗봇", page_icon="🤖")

# 데이터 불러오기 함수 (캐싱을 통해 속도 향상)
@st.cache_data
def load_data():
    return pd.read_csv('한국고용정보원_구인표준직무기술서_20250901.csv', encoding='cp949')

df = load_data()

# 웹 화면 구성
st.title("🤖 맞춤형 직무 & 자격증 추천")
st.write("궁금한 직업명이나 관심 있는 분야를 입력해 보세요!")

# 사용자 입력창
query = st.text_input("검색어 입력", placeholder="예: 제품 디자이너, 데이터 분석, 디자인...")

if query:
    # 데이터 검색
    result = df[df['직종'].str.contains(query, na=False) | 
                df['표준직무전공내용'].str.contains(query, na=False)]

    if not result.empty:
        st.success(f"'{query}'와(과) 관련된 결과를 {len(result)}건 찾았습니다.")
        
        # 결과를 카드 형식으로 출력
        for i in range(len(result)):
            with st.expander(f"📌 추천 직종: {result.iloc[i]['직종']}"):
                st.subheader("🛠 필요 직무 기술")
                st.write(result.iloc[i]['표준직무능력내용'])
                
                st.subheader("📜 추천 자격증")
                st.info(result.iloc[i]['표준직무자격증내용'])
                
                st.caption(f"전공 분야: {result.iloc[i]['표준직무전공내용']}")
    else:
        st.error("아쉽게도 관련 정보를 찾지 못했습니다. 다른 키워드로 검색해 보세요.")