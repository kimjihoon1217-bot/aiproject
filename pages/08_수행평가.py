import streamlit as st

st.set_page_config(page_title="테스트", page_icon="🥊")
st.title("🥊 살아났다!")

name = st.selectbox("선수 선택", ["존 존스", "표도르", "마이크 타이슨", "척준경"])
st.write(f"선택한 선수: **{name}**")
