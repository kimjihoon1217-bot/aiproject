import streamlit as st
st.title('빨리빨리 다녀라')
a=st.text_input('이름을 입력해라 죽기전에')
b=st.selectbox('좋아하는 음식을 선택해라 마지막 만찬이다!',['민트초코','엄마는 외계인','슈팅스타'])
if st.button('인사말 생성'):
  st.write('반갑소')
