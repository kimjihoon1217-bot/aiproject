import os
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(
    page_title="서울시 행정구별 인구 통계 대시보드",
    page_icon="👥",
    layout="wide"
)

# 2. 상위 폴더 경로 탐색 로직 (population.csv 찾기)
def get_csv_filepath():
    possible_paths = [
        os.path.join("..", "population.csv"),  # pages 폴더 기준 상위 폴더
        "population.csv",                      # 현재 디렉토리
        os.path.join(os.path.dirname(__file__), "..", "population.csv")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return "population.csv"

# 3. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    file_path = get_csv_filepath()
    try:
        df = pd.read_csv(file_path, encoding='cp949', thousands=',')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='euc-kr', thousands=',')
    
    # 행정구역명 정제 (예: "서울특별시 종로구 (1111000000)" -> "서울특별시 종로구")
    df['지역명'] = df['행정구역'].apply(lambda x: re.sub(r'\s*\(\d+\)', '', str(x)).strip())
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"population.csv 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 4. 사이드바 - 메인 메뉴 및 필터
st.sidebar.header("🧭 대시보드 메뉴")
menu = st.sidebar.radio(
    "분석 항목 선택",
    ["📈 연도별 남녀 연령별 인구 비교", "🏆 연령대별 자치구 순위 막대그래프", "🌟 [추가] 자치구별 고령화율(노령화 지표) 분석"]
)

# 공통 연령대 목록
age_categories = [
    '0~9세', '10~19세', '20~29세', '30~39세', '40~49세',
    '50~59세', '60~69세', '70~79세', '80~89세', '90~99세', '100세 이상'
]

# ==========================================
# MENU 1: 연도별 남녀 연령별 인구 비교 (꺾은선 그래프)
# ==========================================
if menu == "📈 연도별 남녀 연령별 인구 비교":
    st.title("📈 연도별 행정구 및 남녀 연령별 인구 비교")
    st.write("선택한 연도와 행정구의 **남성(핑크색)** 및 **여성(초록색)** 연령별 인구 분포를 꺾은선 그래프로 비교합니다.")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        region_list = df['지역명'].tolist()
        selected_region = st.selectbox("행정구 선택", region_list, index=0)
    with col2:
        years = [str(y) for y in range(2020, 2026)]
        selected_year = st.selectbox("기준 연도", years, index=len(years) - 1)

    # 데이터 추출
    selected_row = df[df['지역명'] == selected_region].iloc[0]
    
    male_values = [selected_row[f'{selected_year}년_남_거주자_{age}'] for age in age_categories]
    female_values = [selected_row[f'{selected_year}년_여_거주자_{age}'] for age in age_categories]

    # Plotly 꺾은선 그래프 작성 (남성: 핑크색, 여성: 초록색)
    fig = go.Figure()

    # 남성: 핫핑크색 (#FF1493)
    fig.add_trace(go.Scatter(
        x=age_categories, y=male_values,
        mode='lines+markers', name='남성',
        line=dict(color='#FF1493', width=3),
        marker=dict(size=8, color='#FF1493')
    ))

    # 여성: 초록색 (#228B22 - Forest Green)
    fig.add_trace(go.Scatter(
        x=age_categories, y=female_values,
        mode='lines+markers', name='여성',
        line=dict(color='#228B22', width=3),
        marker=dict(size=8, color='#228B22')
    ))

    fig.update_layout(
        title=f"<b>{selected_region}</b> ({selected_year}년) 남녀 연령별 인구 분포",
        xaxis_title="나이 (연령대)",
        yaxis_title="인구수 (명)",
        xaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis=dict(showgrid=True, gridcolor='LightGray', dtick=100000, tickformat=','),
        height=550,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MENU 2: 연령대별 자치구 순위 막대그래프 (요청하신 기능!)
# ==========================================
elif menu == "🏆 연령대별 자치구 순위 막대그래프":
    st.title("🏆 특정 연령대별 행정구 순위 막대 그래프")
    st.write("원하는 **연도**와 **10살 단위 연령대**를 선택하면, 서울시 자치구 중 해당 연령 인구가 많은 순서대로 막대 그래프가 정렬되어 나타납니다.")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        years = [str(y) for y in range(2020, 2026)]
        selected_year = st.selectbox("기준 연도", years, index=len(years) - 1)
    with col2:
        selected_age = st.selectbox("연령대 선택 (10살 단위)", age_categories, index=2) # 기본 20~29세

    # '서울특별시' 전체 행 제외하고 구별 데이터만 추출
    gu_df = df[df['지역명'] != '서울특별시'].copy()
    
    # 선택된 연도 + 연령대의 총 거주자 컬럼명 조합
    target_col = f'{selected_year}년_거주자_{selected_age}'
    
    # 데이터 오름차순 정렬 (가로형 막대그래프에서 위쪽이 1위로 나오도록 정렬)
    gu_sorted = gu_df.sort_values(by=target_col, ascending=True)

    fig = px.bar(
        gu_sorted,
        x=target_col,
        y='지역명',
        orientation='h',
        title=f"<b>{selected_year}년</b> <b>{selected_age}</b> 인구수가 많은 자치구 순위",
        labels={target_col: '인구수 (명)', '지역명': '행정구역'},
        color=target_col,
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(height=650, xaxis=dict(tickformat=','))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MENU 3: [추가] 자치구별 고령화율(노령화 지표) 분석
# ==========================================
elif menu == "🌟 [추가] 자치구별 고령화율(노령화 지표) 분석":
    st.title("🌟 [AI 추천 추가 기능] 자치구별 고령 인구 비율 분석")
    st.write("지속적인 저출산·고령화 사회에 맞춰, 각 자치구별 **60세 이상 고령 인구의 비율(총인구 대비)**을 비교하여 어느 지역이 고령화가 진행되었는지 한눈에 보여줍니다.")

    years = [str(y) for y in range(2020, 2026)]
    selected_year = st.sidebar.selectbox("기준 연도 선택", years, index=len(years) - 1)

    gu_df = df[df['지역명'] != '서울특별시'].copy()

    # 60세 이상 인구 합산 계산
    old_age_cols = [f'{selected_year}년_거주자_60~69세', f'{selected_year}년_거주자_70~79세', 
                    f'{selected_year}년_거주자_80~89세', f'{selected_year}년_거주자_90~99세', f'{selected_year}년_거주자_100세 이상']
    
    total_col = f'{selected_year}년_거주자_총인구수'

    gu_df['60세이상_인구합계'] = gu_df[old_age_cols].sum(axis=1)
    gu_df['고령인구비율(%)'] = (gu_df['60세이상_인구합계'] / gu_df[total_col]) * 100

    # 비율 높은 순으로 정렬
    gu_df_aged = gu_df.sort_values(by='고령인구비율(%)', ascending=False)

    fig = px.bar(
        gu_df_aged,
        x='고령인구비율(%)',
        y='지역명',
        orientation='h',
        title=f"<b>{selected_year}년</b> 서울시 자치구별 60세 이상 고령 인구 비율 (%)",
        text='고령인구비율(%)',
        color='고령인구비율(%)',
        color_continuous_scale='Reds'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=650)
    
    st.plotly_chart(fig, use_container_width=True)
