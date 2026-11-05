import os
import re
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(
    page_title="서울시 행정구별 인구 통계 그래프",
    page_icon="📈",
    layout="wide"
)

# 2. 상위 폴더 및 현재 폴더 경로 탐색 로직 (파일 경로 문제 해결)
def get_csv_filepath():
    possible_paths = [
        os.path.join("..", "population.csv"),  # 상위 폴더 (pages 기준)
        "population.csv",                      # 현재 작업 디렉토리
        os.path.join(os.path.dirname(__file__), "..", "population.csv") # 절대 경로 기반 상위 폴더
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return "population.csv"  # 기본값

# 3. 데이터 불러오기 (Streamlit 캐싱 적용 및 인코딩 예외 처리)
@st.cache_data
def load_data():
    file_path = get_csv_filepath()
    try:
        # CP949 인코딩 및 천단위 쉼표 제거
        df = pd.read_csv(file_path, encoding='cp949', thousands=',')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='euc-kr', thousands=',')
    
    # 행정구역명 정제 (예: "서울특별시 종로구 (1111000000)" -> "서울특별시 종로구")
    df['지역명'] = df['행정구역'].apply(lambda x: re.sub(r'\s*\(\d+\)', '', str(x)).strip())
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"상위 폴더에서 population.csv 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.info("파일 위치 확인: population.csv 파일이 pages 폴더의 상위 폴더(루트 디렉토리)에 존재하는지 확인해 주세요.")
    st.stop()

# 4. 사이드바 - 조건 선택 필터 (행정구, 성별, 연도)
st.sidebar.header("⚙️ 그래프 설정")

# 1) 행정구 선택
region_list = df['지역명'].tolist()
selected_region = st.sidebar.selectbox("행정구 선택", region_list, index=0)

# 2) 성별 선택
gender_options = {"전체": "거주자", "남성": "남_거주자", "여성": "여_거주자"}
selected_gender_label = st.sidebar.selectbox("성별 선택", list(gender_options.keys()), index=0)
gender_prefix = gender_options[selected_gender_label]

# 3) 연도 선택
years = [str(y) for y in range(2020, 2026)]
selected_year = st.sidebar.selectbox("연도 선택", years, index=len(years) - 1)

# 5. 데이터 추출 및 가공
selected_row = df[df['지역명'] == selected_region].iloc[0]

# 연령대 구간 정의
age_categories = [
    '0~9세', '10~19세', '20~29세', '30~39세', '40~49세',
    '50~59세', '60~69세', '70~79세', '80~89세', '90~99세', '100세 이상'
]

# 선택 조건에 맞는 연령별 인구수 데이터 추출
population_values = []
for age in age_categories:
    col_name = f"{selected_year}년_{gender_prefix}_{age}"
    population_values.append(selected_row[col_name])

# 6. 시각화 (Plotly 꺾은선 그래프)
st.title(f"📊 {selected_region} ({selected_year}년 / {selected_gender_label}) 연령별 인구수")

fig = go.Figure()

# 핫핑크색(#FF1493) 꺾은선 추가
fig.add_trace(go.Scatter(
    x=age_categories,
    y=population_values,
    mode='lines+markers',
    name='인구수',
    line=dict(color='#FF1493', width=3),            # 핫핑크 라인 색상
    marker=dict(size=8, color='#FF1493')            # 핫핑크 마커
))

# 그래프 레이아웃 설정 (구분선 및 축 단위 설정)
fig.update_layout(
    xaxis_title="나이 (연령대)",
    yaxis_title="인구수 (명)",
    
    # 가로축 (10살 단위 연령대 및 구분선)
    xaxis=dict(
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=1
    ),
    
    # 세로축 (10만 단위 구분선: 100,000 Step)
    yaxis=dict(
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=1,
        dtick=100000,                               # 10만 단위 격자 구분선
        tickformat=','                              # 천단위 쉼표 표기
    ),
    height=600,
    hovermode="x unified"
)

# Streamlit 화면에 차트 출력
st.plotly_chart(fig, use_container_width=True)

# 7. 원본 데이터표 보기 옵션
with st.expander("📋 상세 수치 데이터 보기"):
    detail_df = pd.DataFrame({
        "연령대": age_categories,
        "인구수(명)": population_values
    })
    st.dataframe(detail_df, use_container_width=True)
