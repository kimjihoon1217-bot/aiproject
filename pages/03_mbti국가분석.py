
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="세계 MBTI 분석",
    page_icon="🌎",
    layout="wide"
)

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(
        "countriesMBTI_16types.csv",
        encoding="utf-8-sig"
    )
    return df

df = load_data()

# MBTI 유형
mbti_types = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

st.title("🌎 세계 국가별 MBTI 분석")
st.caption("158개 국가의 MBTI 16가지 유형 통계")

# 데이터 확인
if "Country" not in df.columns:
    st.error("Country 열을 찾을 수 없습니다.")
    st.stop()

if not set(mbti_types).issubset(df.columns):
    st.error("MBTI 데이터 열이 누락되었습니다.")
    st.stop()

# 데이터 전처리
for col in mbti_types:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Country"] + mbti_types)

# 상단 통계
col1, col2, col3 = st.columns(3)

col1.metric("🌍 국가 수", f"{len(df)}개")
col2.metric("🧠 MBTI 유형", "16개")
col3.metric("📊 데이터 항목", f"{len(df) * 16:,}개")

st.divider()

# 메뉴
menu = st.sidebar.radio(
    "분석 메뉴",
    [
        "전체 통계",
        "국가별 MBTI",
        "MBTI별 국가 순위",
        "국가별 최고 MBTI"
    ]
)

# 1. 전체 통계
if menu == "전체 통계":

    st.header("📊 세계 MBTI 평균")

    avg = df[mbti_types].mean() * 100
    avg = avg.sort_values(ascending=False)

    st.bar_chart(avg)

    result = avg.reset_index()
    result.columns = ["MBTI", "평균 비율(%)"]

    st.dataframe(
        result.style.format({
            "평균 비율(%)": "{:.2f}%"
        }),
        use_container_width=True
    )

# 2. 국가별 MBTI
elif menu == "국가별 MBTI":

    st.header("🌏 국가별 MBTI 분석")

    country = st.selectbox(
        "국가 선택",
        sorted(df["Country"].unique())
    )

    data = df[df["Country"] == country].iloc[0]

    values = pd.Series({
        mbti: data[mbti] * 100
        for mbti in mbti_types
    }).sort_values(ascending=False)

    st.subheader(f"📍 {country}의 MBTI 분포")

    st.metric(
        "가장 높은 MBTI",
        values.index[0],
        f"{values.iloc[0]:.2f}%"
    )

    st.bar_chart(values)

    st.dataframe(
        values.rename("비율(%)").reset_index()
        .rename(columns={"index": "MBTI"})
        .style.format({"비율(%)": "{:.2f}%"}),
        use_container_width=True
    )

# 3. MBTI별 국가 순위
elif menu == "MBTI별 국가 순위":

    st.header("🏆 MBTI별 국가 순위")

    selected = st.selectbox(
        "MBTI 선택",
        mbti_types
    )

    ranking = df[["Country", selected]].copy()

    ranking["비율(%)"] = ranking[selected] * 100

    ranking = ranking.sort_values(
        "비율(%)",
        ascending=False
    )

    top_n = st.slider(
        "표시할 국가 수",
        5, 50, 10
    )

    st.subheader(f"🏆 {selected} 비율 TOP {top_n}")

    st.bar_chart(
        ranking.head(top_n).set_index("Country")["비율(%)"]
    )

    ranking.insert(
        0, "순위", range(1, len(ranking) + 1)
    )

    st.dataframe(
        ranking[["순위", "Country", "비율(%)"]]
        .head(top_n)
        .style.format({"비율(%)": "{:.2f}%"}),
        use_container_width=True
    )

# 4. 국가별 최고 MBTI
elif menu == "국가별 최고 MBTI":

    st.header("🥇 국가별 가장 높은 MBTI")

    result = df[["Country"]].copy()

    result["최고 MBTI"] = df[mbti_types].idxmax(axis=1)

    result["비율(%)"] = (
        df[mbti_types].max(axis=1) * 100
    )

    search = st.text_input("🔎 국가 검색")

    if search:
        result = result[
            result["Country"].str.contains(
                search, case=False, na=False
            )
        ]

    st.dataframe(
        result.style.format({
            "비율(%)": "{:.2f}%"
        }),
        use_container_width=True
    )

st.divider()

st.caption(
    "※ 본 통계는 제공된 CSV 데이터에 기반하며 "
    "실제 전 세계 인구의 MBTI 분포를 보증하지 않습니다."
)
