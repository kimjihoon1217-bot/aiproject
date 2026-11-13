import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import DecisionBoundaryDisplay

# 페이지 기본 설정
st.set_page_config(page_title="붓꽃(Iris) 품종 예측기", page_icon="🌸", layout="centered")

st.title("🌸 붓꽃(Iris) 품종 예측 및 분류 시각화")
st.write("꽃잎의 길이와 너비를 입력하면 머신러닝(Random Forest) 모델이 품종을 예측하고 분류 근거를 시각화합니다.")

# 1. 데이터 로드 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    # 제공된 파일의 인코딩(cp949) 및 깨진 첫 번째 컬럼명 처리
    df = pd.read_csv("Iris.csv", encoding="cp949")
    df.columns = ['꽃받침길이', '꽃받침너비', '꽃잎길이', '꽃잎너비', '품종']
    return df

df = load_data()

# 특성(X)과 타겟(y) 분리
X = df[['꽃잎길이', '꽃잎너비']]
y_labels = df['품종'].astype('category')
y = y_labels.cat.codes
class_names = list(y_labels.cat.categories)

# 2. 모델 학습 (가장 널리 사용되는 분류 알고리즘: Random Forest)
@st.cache_resource
def train_model(X, y):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X.values, y)
    return clf

model = train_model(X, y)

# 3. 사용자 입력 범위 안내 및 입력 UI (사이드바)
st.sidebar.header("📏 꽃잎 크기 입력")

min_len, max_len = float(df['꽃잎길이'].min()), float(df['꽃잎길이'].max())
min_wid, max_wid = float(df['꽃잎너비'].min()), float(df['꽃잎너비'].max())

st.sidebar.info(
    f"**💡 권장 입력 범위 (학습 데이터 기준)**\n\n"
    f"- **꽃잎 길이 (Petal Length):** `{min_len} cm` ~ `{max_len} cm`\n"
    f"- **꽃잎 너비 (Petal Width):** `{min_wid} cm` ~ `{max_wid} cm`"
)

petal_length = st.sidebar.slider(
    "꽃잎 길이 (cm)",
    min_value=0.5,
    max_value=8.0,
    value=3.8,
    step=0.1
)

petal_width = st.sidebar.slider(
    "꽃잎 너비 (cm)",
    min_value=0.1,
    max_value=3.5,
    value=1.2,
    step=0.1
)

# 4. 예측 수행
user_input = np.array([[petal_length, petal_width]])
pred_idx = model.predict(user_input)[0]
pred_proba = model.predict_proba(user_input)[0]
predicted_species = class_names[pred_idx]

# 예측 결과 출력
st.subheader("🔍 예측 결과")
col1, col2 = st.columns([1, 1])

with col1:
    st.success(f"예측된 품종: **{predicted_species}**")
    st.write(f"- 입력한 꽃잎 길이: **{petal_length} cm**")
    st.write(f"- 입력한 꽃잎 너비: **{petal_width} cm**")

with col2:
    st.write("**품종별 예측 확률:**")
    proba_df = pd.DataFrame({
        "품종": class_names,
        "확률 (%)": np.round(pred_proba * 100, 1)
    })
    st.dataframe(proba_df, hide_index=True, use_container_width=True)

# 5. 결정 경계 및 분류 근거 시각화
st.subheader("📊 분류 근거 시각화 (결정 경계 및 데이터 분포)")
st.write(
    "아래 그래프의 **배경색 영역**은 모델이 각 품종으로 판단하는 구역(결정 경계)입니다. "
    "입력하신 위치(**초록색 별 ★**)가 어느 품종의 영역과 기존 데이터 군집에 속해 있는지 확인해 보세요."
)

fig, ax = plt.subplots(figsize=(8, 6))

# 결정 경계 그리기
DecisionBoundaryDisplay.from_estimator(
    model,
    X.values,
    cmap=plt.cm.Pastel1,
    response_method="predict",
    ax=ax,
    xlabel="Petal Length (cm)",
    ylabel="Petal Width (cm)",
    alpha=0.8
)

# 기존 150개 데이터 산점도
colors = ['#e41a1c', '#377eb8', '#984ea3']
for idx, species in enumerate(class_names):
    subset = df[df['품종'] == species]
    ax.scatter(
        subset['꽃잎길이'],
        subset['꽃잎너비'],
        c=colors[idx],
        label=species,
        edgecolors='k',
        s=50,
        alpha=0.85
    )

# 사용자 입력값 표시 (초록색 별)
ax.scatter(
    petal_length,
    petal_width,
    c='lime',
    marker='*',
    s=400,
    edgecolors='black',
    linewidths=1.5,
    label='Your Input (Predicted)',
    zorder=10
)

ax.set_title("Iris Classification Decision Boundary (Random Forest)", fontsize=13, pad=12)
ax.legend(loc="upper left", frameon=True)
ax.grid(True, linestyle='--', alpha=0.4)

st.pyplot(fig)
