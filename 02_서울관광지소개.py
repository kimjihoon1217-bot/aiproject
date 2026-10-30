
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Seoul Tourist TOP 10",
    page_icon="🗺️",
    layout="wide"
)

places = [
    {
        "rank": 1, "name": "명동",
        "eng": "Myeongdong",
        "lat": 37.5636, "lon": 126.9869,
        "category": "쇼핑·먹거리",
        "desc": "화장품 쇼핑과 길거리 음식으로 유명한 서울 대표 번화가"
    },
    {
        "rank": 2, "name": "N서울타워",
        "eng": "N Seoul Tower",
        "lat": 37.5512, "lon": 126.9882,
        "category": "전망·야경",
        "desc": "서울의 아름다운 전경과 야경을 볼 수 있는 남산 명소"
    },
    {
        "rank": 3, "name": "코엑스",
        "eng": "COEX",
        "lat": 37.5116, "lon": 127.0592,
        "category": "쇼핑·문화",
        "desc": "쇼핑몰과 별마당도서관, 다양한 전시를 즐길 수 있는 공간"
    },
    {
        "rank": 4, "name": "강남역",
        "eng": "Gangnam Station",
        "lat": 37.4979, "lon": 127.0276,
        "category": "쇼핑·도심",
        "desc": "다양한 음식점과 상점이 모여 있는 서울의 번화가"
    },
    {
        "rank": 5, "name": "홍대 거리",
        "eng": "Hongdae",
        "lat": 37.5563, "lon": 126.9236,
        "category": "문화·엔터테인먼트",
        "desc": "버스킹, 카페, 쇼핑과 젊은 문화를 경험할 수 있는 거리"
    },
    {
        "rank": 6, "name": "경복궁",
        "eng": "Gyeongbokgung Palace",
        "lat": 37.5796, "lon": 126.9770,
        "category": "역사·문화",
        "desc": "조선 왕조의 대표 궁궐로 한복 체험이 유명한 관광지"
    },
    {
        "rank": 7, "name": "북촌한옥마을",
        "eng": "Bukchon Hanok Village",
        "lat": 37.5826, "lon": 126.9830,
        "category": "전통·문화",
        "desc": "한국의 전통 한옥과 아름다운 골목길을 볼 수 있는 곳"
    },
    {
        "rank": 8, "name": "동대문디자인플라자",
        "eng": "DDP",
        "lat": 37.5671, "lon": 127.0095,
        "category": "건축·전시",
        "desc": "독특한 건축물과 디자인 전시를 즐길 수 있는 공간"
    },
    {
        "rank": 9, "name": "광장시장",
        "eng": "Gwangjang Market",
        "lat": 37.5701, "lon": 126.9997,
        "category": "전통시장·음식",
        "desc": "빈대떡과 김밥 등 한국 전통 음식을 맛볼 수 있는 시장"
    },
    {
        "rank": 10, "name": "창덕궁",
        "eng": "Changdeokgung Palace",
        "lat": 37.5794, "lon": 126.9910,
        "category": "역사·문화",
        "desc": "유네스코 세계유산으로 아름다운 궁궐과 후원이 유명한 곳"
    }
]

st.title("🗺️ Seoul Tourist TOP 10")
st.subheader("외국인 관광객을 위한 서울 인기 관광지")

st.info(
    "서울의 주요 관광 명소 10곳을 지도에서 확인해 보세요. "
    "공식 통계 순위가 아닌 관광 안내용 추천 목록입니다."
)

category = st.sidebar.selectbox(
    "관광지 종류 선택",
    ["전체"] + list(dict.fromkeys(p["category"] for p in places))
)

selected = [
    p for p in places
    if category == "전체" or p["category"] == category
]

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

for p in selected:
    popup = f"""
    <b>TOP {p['rank']} - {p['name']}</b><br>
    {p['eng']}<br><br>
    {p['desc']}<br><br>
    분야: {p['category']}
    """

    folium.Marker(
        [p["lat"], p["lon"]],
        popup=folium.Popup(popup, max_width=300),
        tooltip=p["name"],
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#1769aa;
                color:white;
                border:2px solid white;
                border-radius:50%;
                width:30px;
                height:30px;
                text-align:center;
                line-height:26px;
                font-weight:bold;">
                {p['rank']}
            </div>
            """
        )
    ).add_to(m)

col1, col2 = st.columns([1.7, 1])

with col1:
    st.subheader("📍 서울 관광지 지도")
    st_folium(m, width=None, height=600)

with col2:
    st.subheader("🏆 관광지 TOP 10")

    for p in selected:
        with st.expander(
            f"{p['rank']}. {p['name']}"
        ):
            st.write(p["eng"])
            st.write(p["desc"])
            st.write("종류:", p["category"])

            url = (
                "https://www.google.com/maps/search/?api=1"
                f"&query={p['lat']},{p['lon']}"
            )

            st.link_button(
                "Google 지도에서 보기",
                url
            )

st.caption(
    "※ 위치 좌표는 지도 표시용 근사값입니다. "
    "방문 전 운영 정보를 확인하세요."
)
