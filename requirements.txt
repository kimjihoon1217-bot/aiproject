
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen, MiniMap, LocateControl

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Seoul Travel TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}
.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #17365d;
}
.sub-title {
    color: #64748b;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 관광지 데이터
# -----------------------------
places = [
    {
        "rank": 1,
        "name": "명동",
        "eng": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9869,
        "category": "쇼핑",
        "description": "화장품 쇼핑과 다양한 길거리 음식을 즐길 수 있는 서울 대표 번화가입니다."
    },
    {
        "rank": 2,
        "name": "N서울타워",
        "eng": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "category": "전망",
        "description": "남산 정상에서 서울의 아름다운 전경과 야경을 감상할 수 있습니다."
    },
    {
        "rank": 3,
        "name": "코엑스",
        "eng": "COEX",
        "lat": 37.5116,
        "lon": 127.0592,
        "category": "쇼핑",
        "description": "쇼핑몰, 별마당도서관, 전시관 등을 즐길 수 있는 복합문화공간입니다."
    },
    {
        "rank": 4,
        "name": "강남역",
        "eng": "Gangnam Station",
        "lat": 37.4979,
        "lon": 127.0276,
        "category": "쇼핑",
        "description": "다양한 음식점과 패션 매장, 상점들이 모여 있는 번화가입니다."
    },
    {
        "rank": 5,
        "name": "홍대 거리",
        "eng": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "category": "문화",
        "description": "버스킹, 카페, 쇼핑, 거리 공연 등 젊은 문화를 경험할 수 있습니다."
    },
    {
        "rank": 6,
        "name": "경복궁",
        "eng": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "category": "역사",
        "description": "조선 왕조의 대표 궁궐이며 한복 체험과 전통문화를 경험할 수 있습니다."
    },
    {
        "rank": 7,
        "name": "북촌한옥마을",
        "eng": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "category": "전통문화",
        "description": "전통 한옥과 아름다운 골목길을 볼 수 있는 서울의 대표 관광지입니다."
    },
    {
        "rank": 8,
        "name": "동대문디자인플라자",
        "eng": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "category": "문화",
        "description": "독특한 건축물과 디자인 전시, 다양한 문화 행사가 열리는 공간입니다."
    },
    {
        "rank": 9,
        "name": "광장시장",
        "eng": "Gwangjang Market",
        "lat": 37.5701,
        "lon": 126.9997,
        "category": "음식",
        "description": "빈대떡, 김밥 등 한국의 전통 먹거리를 경험할 수 있는 시장입니다."
    },
    {
        "rank": 10,
        "name": "창덕궁",
        "eng": "Changdeokgung Palace",
        "lat": 37.5794,
        "lon": 126.9910,
        "category": "역사",
        "description": "유네스코 세계유산으로 아름다운 궁궐 건축과 후원이 유명합니다."
    }
]

# -----------------------------
# 상단 제목
# -----------------------------
st.markdown(
    '<div class="main-title">🗺️ SEOUL TRAVEL TOP 10</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">외국인 관광객을 위한 서울 주요 관광지 지도</div>',
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.title("🔍 관광지 검색")

category = st.sidebar.selectbox(
    "관광지 종류",
    ["전체", "쇼핑", "전망", "문화", "역사", "전통문화", "음식"]
)

search = st.sidebar.text_input(
    "관광지 이름 검색"
)

# 필터링
filtered_places = []

for place in places:
    category_match = (
        category == "전체"
        or place["category"] == category
    )

    search_match = (
        search.lower() in place["name"].lower()
        or search.lower() in place["eng"].lower()
    )

    if category_match and search_match:
        filtered_places.append(place)

st.sidebar.markdown("---")
st.sidebar.write("📍 총 관광지:", len(filtered_places))

# -----------------------------
# Folium 지도 생성
# -----------------------------
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

# 지도 기능 추가
Fullscreen(
    position="topright"
).add_to(m)

MiniMap(
    toggle_display=True
).add_to(m)

LocateControl(
    auto_start=False
).add_to(m)

# -----------------------------
# 관광지 마커
# -----------------------------
for place in filtered_places:

    popup_html = f"""
    <div style="width:250px; font-family:Arial;">
        <h3 style="color:#1769aa;">
            TOP {place['rank']} - {place['name']}
        </h3>

        <p><b>{place['eng']}</b></p>

        <hr>

        <p>{place['description']}</p>

        <p>
            <b>분류:</b> {place['category']}
        </p>

        <a href="https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lon']}"
        target="_blank">
            Google Maps에서 보기
        </a>
    </div>
    """

    folium.Marker(
        location=[
            place["lat"],
            place["lon"]
        ],

        tooltip=place["name"],

        popup=folium.Popup(
            popup_html,
            max_width=300
        ),

        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#1769aa;
                color:white;
                width:34px;
                height:34px;
                border-radius:50%;
                border:3px solid white;
                text-align:center;
                line-height:28px;
                font-weight:bold;
                font-size:14px;
                box-shadow:0 2px 5px #555;
            ">
                {place['rank']}
            </div>
            """
        )
    ).add_to(m)

# -----------------------------
# 지도 표시
# -----------------------------
st.subheader("📍 서울 관광지 지도")

st.caption(
    "지도에 표시된 숫자를 클릭하면 관광지 정보를 확인할 수 있습니다."
)

map_data = st_folium(
    m,
    width=None,
    height=650,
    returned_objects=["last_object_clicked"]
)

# -----------------------------
# 관광지 목록
# -----------------------------
st.markdown("---")
st.subheader("🏆 SEOUL TOP 10 관광지")

col1, col2 = st.columns(2)

for index, place in enumerate(filtered_places):

    target_col = col1 if index % 2 == 0 else col2

    with target_col:

        with st.container(border=True):

            st.markdown(
                f"### {place['rank']}. {place['name']}"
            )

            st.caption(place["eng"])

            st.write(place["description"])

            st.write(
                f"📌 관광 유형: {place['category']}"
            )

            url = (
                "https://www.google.com/maps/search/?api=1"
                f"&query={place['lat']},{place['lon']}"
            )

            st.link_button(
                "Google 지도에서 위치 확인",
                url
            )

# -----------------------------
# 하단
# -----------------------------
st.markdown("---")

st.markdown("""
<div style="text-align:center; color:#64748b;">
    <h4>SEOUL TRAVEL GUIDE 🇰🇷</h4>
    Discover the beauty of Seoul
    <br><br>
    서울의 대표 관광지를 지도에서 만나보세요.
</div>
""", unsafe_allow_html=True)
